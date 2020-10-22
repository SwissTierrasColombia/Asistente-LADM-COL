# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-11-26
        git sha              : :%H$
        copyright            : (C) 2019 by Jhon Galindo (Incige SAS)
        email                : jhonsigpjc@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtWidgets import (QDialog,
                                 QMessageBox,
                                 QDialogButtonBox,
                                 QSizePolicy)
from qgis.PyQt.QtCore import (Qt,
                              QSettings,
                              QCoreApplication,
                              pyqtSignal)
from qgis.PyQt.QtGui import QValidator
from qgis.core import (Qgis,
                       QgsProject,
                       QgsVectorLayer)
from qgis.gui import QgsMessageBar

from asistente_ladm_col.config.general_config import BLO_LIS_FILE_PATH
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.qt_utils import (FileValidator,
                                               DirValidator,
                                               NonEmptyStringValidator,
                                               Validators,
                                               normalize_local_url,
                                               make_file_selector,
                                               make_folder_selector)
from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.lib.processing.custom_processing_feedback import CustomFeedback

DIALOG_LOG_EXCEL_UI = get_ui_class('supplies/dlg_missing_supplies.ui')


class MissingSuppliesBaseDialog(QDialog, DIALOG_LOG_EXCEL_UI):
    on_result = pyqtSignal(bool)  # whether the tool was run successfully or not

    def __init__(self, db, conn_manager, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self._db = db
        self.conn_manager = conn_manager
        self.parent = parent

        self.logger = Logger()
        self.app = AppInterface()
        self.validators = Validators()

        self.names = self._db.names
        self._dialog_mode = None
        self._running_tool = False        
        self._db_was_changed = False  # To postpone calling refresh gui until we close this dialog instead of settings
        self.tool_name = ""
        self.gdb_layer_paths = dict()
        self.alphanumeric_file_paths = dict()

        # Initialize
        self.initialize_feedback()

        # Set MessageBar for QDialog
        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

        # Set connections
        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.button(QDialogButtonBox.Ok).setText(QCoreApplication.translate("MissingSuppliesBaseDialog", "Import"))
        self.finished.connect(self.finished_slot)

        self.btn_browse_file_predio.clicked.connect(
            make_file_selector(self.txt_file_path_predio, QCoreApplication.translate("MissingSuppliesBaseDialog",
                        "Select the Predio .csv file with SNC data "),
                        QCoreApplication.translate("MissingSuppliesBaseDialog", 'CSV File (*.csv)')))

        self.btn_browse_file_uni.clicked.connect(
            make_file_selector(self.txt_file_path_uni, QCoreApplication.translate("MissingSuppliesBaseDialog",
                        "Select the UNI .lis file with Cobol data "),
                        QCoreApplication.translate("MissingSuppliesBaseDialog", 'lis File (*.lis)')))

        self.btn_browse_file_gdb.clicked.connect(
                make_folder_selector(self.txt_file_path_gdb, title=QCoreApplication.translate(
                'MissingSuppliesBaseDialog', 'Open GDB folder'), parent=None))

        self.btn_browse_file_folder_supplies.clicked.connect(
                make_folder_selector(self.txt_file_path_folder_supplies, title=QCoreApplication.translate(
                "MissingCobolSuppliesDialog", "Select folder to save data"), parent=None))

        # Set validations
        file_validator_predio = FileValidator(pattern='*.csv', allow_non_existing=False)
        file_validator_lis = FileValidator(pattern='*.lis', allow_non_existing=False)
        dir_validator_gdb = DirValidator(pattern='*.gdb', allow_non_existing=False)
        dir_validator_folder = DirValidator(pattern=None, allow_empty_dir=True)
        non_empty_validator_name = NonEmptyStringValidator()

        self.txt_file_path_predio.setValidator(file_validator_predio)
        self.txt_file_path_uni.setValidator(file_validator_lis)
        self.txt_file_path_gdb.setValidator(dir_validator_gdb)
        self.txt_file_path_folder_supplies.setValidator(dir_validator_folder)
        self.txt_files_name_supplies.setValidator(non_empty_validator_name)

        self.txt_file_path_predio.textChanged.connect(self.validators.validate_line_edits)
        self.txt_file_path_uni.textChanged.connect(self.validators.validate_line_edits)
        self.txt_file_path_gdb.textChanged.connect(self.validators.validate_line_edits)
        self.txt_file_path_folder_supplies.textChanged.connect(self.validators.validate_line_edits)
        self.txt_files_name_supplies.textChanged.connect(self.validators.validate_line_edits)

        self.txt_file_path_predio.textChanged.connect(self.input_data_changed)
        self.txt_file_path_uni.textChanged.connect(self.input_data_changed)
        self.txt_file_path_gdb.textChanged.connect(self.input_data_changed)
        self.txt_file_path_folder_supplies.textChanged.connect(self.input_data_changed)
        self.txt_files_name_supplies.textChanged.connect(self.input_data_changed)

    def progress_configuration(self, base, num_process):
        """
        :param base: Where to start counting from
        :param num_process: Number of steps
        """
        self.progress_base = base
        self.progress_maximum = 100 * num_process
        self.progress.setMaximum(self.progress_maximum)

    def progress_changed(self):
        QCoreApplication.processEvents()  # Listen to cancel from the user
        self.progress.setValue(self.progress_base + self.custom_feedback.progress())

    def reject(self):
        if self._running_tool:
            reply = QMessageBox.question(self,
                                         QCoreApplication.translate("MissingSuppliesBaseDialog", "Warning"),
                                         QCoreApplication.translate("MissingSuppliesBaseDialog",
                                                                    "The '{}' tool is still running. Do you want to cancel it? If you cancel, the data might be incomplete in the target database.").format(self.tool_name),
                                         QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.custom_feedback.cancel()
                self._running_tool = False
                msg = QCoreApplication.translate("MissingSuppliesBaseDialog", "The '{}' tool was cancelled.").format(self.tool_name)
                self.logger.info(__name__, msg)
                self.show_message(msg, Qgis.Info)
        else:
            if self._db_was_changed:
                self.conn_manager.db_connection_changed.emit(self._db, self._db.test_connection()[0], self.db_source)
            self.logger.info(__name__, "Dialog closed.")
            self.done(1)

    def finished_slot(self, result):
        self.bar.clearWidgets()

    def input_data_changed(self):
        self.set_import_button_enabled(self.validate_inputs())

    def set_import_button_enabled(self, enable):
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(enable)

    def validate_inputs(self):
        raise NotImplementedError

    def validate_common_inputs(self):
        return self.txt_file_path_gdb.validator().validate(self.txt_file_path_gdb.text().strip(), 0)[0] == QValidator.Acceptable

    def initialize_feedback(self):
        self.progress.setValue(0)
        self.progress.setVisible(False)
        self.custom_feedback = CustomFeedback()
        self.custom_feedback.progressChanged.connect(self.progress_changed)
        self.set_gui_controls_enabled(True)

    def set_gui_controls_enabled(self, enable):
        self.gbx_data_source.setEnabled(enable)
        if self.buttonBox.button(QDialogButtonBox.Ok) is not None:  # It's None if the tool finished successfully
            self.set_import_button_enabled(enable)

    def db_connection_changed(self, db, ladm_col_db, db_source):
        # We dismiss parameters here, after all, we already have the db, and the ladm_col_db may change from this moment
        # until we close the supplies dialog (e.g., we might run an import schema before under the hood)
        self._db_was_changed = True

    def save_settings(self, system):
        settings = QSettings()
        settings.setValue('Asistente-LADM-COL/missing_supplies_{}/predio_path'.format(system), self.txt_file_path_predio.text())
        settings.setValue('Asistente-LADM-COL/missing_supplies_{}/uni_path'.format(system), self.txt_file_path_uni.text())
        settings.setValue('Asistente-LADM-COL/missing_supplies_{}/gdb_path'.format(system), self.txt_file_path_gdb.text())
        settings.setValue('Asistente-LADM-COL/missing_supplies_{}/folder_path'.format(system), self.txt_file_path_folder_supplies.text())

    def restore_settings(self, system):
        settings = QSettings()
        self.txt_file_path_predio.setText(settings.value('Asistente-LADM-COL/missing_supplies_{}/predio_path'.format(system), ''))
        self.txt_file_path_uni.setText(settings.value('Asistente-LADM-COL/missing_supplies_{}/uni_path'.format(system), ''))
        self.txt_file_path_gdb.setText(settings.value('Asistente-LADM-COL/missing_supplies_{}/gdb_path'.format(system), ''))
        self.txt_file_path_folder_supplies.setText(settings.value('Asistente-LADM-COL/missing_supplies_{}/folder_path'.format(system), ''))

    def load_lis_files(self, alphanumeric_file_paths):
        root = QgsProject.instance().layerTreeRoot()
        alphanumeric_group = root.addGroup(QCoreApplication.translate("MissingSuppliesBaseDialog", "LIS Supplies"))

        for name in alphanumeric_file_paths:
            uri = 'file:///{}?type=csv&delimiter=;&detectTypes=yes&geomType=none&subsetIndex=no&watchFile=no'.format(normalize_local_url(alphanumeric_file_paths[name]))
            layer = QgsVectorLayer(uri, name, 'delimitedtext')
            if layer.isValid():
                self.alphanumeric_file_paths[name] = layer
                QgsProject.instance().addMapLayer(layer, False)
                alphanumeric_group.addLayer(layer)
            else:
                return False, QCoreApplication.translate("MissingSuppliesBaseDialog", "There were troubles loading the LIS file called '{}'.".format(name))

        return True, ''

    def load_csv_files(self, alphanumeric_file_paths):
        root = QgsProject.instance().layerTreeRoot()
        alphanumeric_group = root.addGroup(QCoreApplication.translate("MissingSuppliesBaseDialog", "SNC Alphanumeric Supplies"))

        for name in alphanumeric_file_paths:
            layer = QgsVectorLayer(alphanumeric_file_paths[name], name, 'ogr')
            if layer.isValid():
                self.alphanumeric_file_paths[name] = layer
                QgsProject.instance().addMapLayer(layer, False)
                alphanumeric_group.addLayer(layer)
            else:
                return False, QCoreApplication.translate("MissingSuppliesBaseDialog", "There were troubles loading the CSV file called '{}'.".format(name))

        return True, ''

    def load_gdb_files(self, required_layers):
        gdb_path = self.txt_file_path_gdb.text()
        layer = QgsVectorLayer(gdb_path, 'layer name', 'ogr')

        if not layer.isValid():
            return False, QCoreApplication.translate("MissingSuppliesBaseDialog", "There were troubles loading the GDB.")

        sublayers = layer.dataProvider().subLayers()

        root = QgsProject.instance().layerTreeRoot()
        gdb_group = root.addGroup(QCoreApplication.translate("MissingSuppliesBaseDialog", "GDB Supplies"))

        for data in sublayers:
            sublayer = data.split('!!::!!')[1]
            if sublayer in required_layers:
                layer = QgsVectorLayer(gdb_path + '|layername=' + sublayer, sublayer, 'ogr')
                self.gdb_layer_paths[sublayer] = layer
                QgsProject.instance().addMapLayer(layer, False)
                gdb_group.addLayer(layer)

        if len(self.gdb_layer_paths) != len(required_layers):
            return False, QCoreApplication.translate("MissingSuppliesBaseDialog", "The GDB does not have the required layers!")

        return True, ''

    def show_message(self, message, level):
        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.bar.pushMessage(message, level, 15)