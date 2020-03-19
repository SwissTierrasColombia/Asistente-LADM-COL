# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-03-18
        git sha              : :%H$
        copyright            : (C) 2020 by Germán Carrillo (BSF Swissphoto)
                               (C) 2020 by Jhon Galindo (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
                               jhonsigpjc@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import (Qt,
                              QSettings,
                              QCoreApplication,
                              pyqtSignal, QObject)
from qgis.PyQt.QtWidgets import (QWizard,
                                 QSizePolicy,
                                 QGridLayout,
                                 QMessageBox)
from qgis._core import QgsProject
from qgis.core import (Qgis,
                       QgsWkbTypes,
                       QgsVectorLayer)
from qgis.gui import QgsMessageBar

import processing

from asistente_ladm_col.config.enums import EnumDbActionType
from asistente_ladm_col.config.general_config import (LAYER,
                                                      COLLECTED_DB_SOURCE,
                                                      SETTINGS_CONNECTION_TAB_INDEX,
                                                      SUPPLIES_DB_SOURCE, BLO_LIS_FILE_PATH)
from asistente_ladm_col.config.help_strings import HelpStrings
from asistente_ladm_col.gui.dialogs.dlg_settings import SettingsDialog
from asistente_ladm_col.gui.supplies.cobol_data_sources_widget import CobolDataSourceWidget
from asistente_ladm_col.gui.supplies.snc_data_sources_widget import SNCDataSourceWidget
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.processing.custom_processing_feedback import CustomFeedback
from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.qt_utils import OverrideCursor


WIZARD_UI = get_ui_class('supplies/wiz_supplies_etl.ui')


class SuppliesETLWizard(QWizard, WIZARD_UI):

    on_result = pyqtSignal(bool)  # whether the tool was run successfully or not

    WIZARD_NAME = "SuppliesETLWizard"

    def __init__(self, qgis_utils, db, conn_manager, parent=None):
        QWizard.__init__(self)
        self.setupUi(self)
        self.qgis_utils = qgis_utils
        self._db = db
        self.conn_manager = conn_manager
        self.parent = parent
        self.logger = Logger()

        self.names = self._db.names
        self.help_strings = HelpStrings()
        self._data_source_widget = None
        self.db_source = SUPPLIES_DB_SOURCE
        self.tool_name = ""
        self._running_tool = False
        self._db_was_changed = False  # To postpone calling refresh gui until we close this dialog instead of settings
        self.progress_configuration(0, 1)  # start from: 0, number of steps: 1

        self.wizardPage2.setButtonText(QWizard.CustomButton1, QCoreApplication.translate(self.WIZARD_NAME, "Import"))

        # Auxiliary data to set nonlinear next pages
        self.pages = [self.wizardPage1, self.wizardPage2, self.wizardPage3]
        self.dict_pages_ids = {self.pages[idx] : pid for idx, pid in enumerate(self.pageIds())}

        # Set connections
        self.rad_snc_data.toggled.connect(self.etl_option_changed)
        self.etl_option_changed() # Initialize it
        self.button(QWizard.CustomButton1).clicked.connect(self.import_button_clicked)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)
        self.currentIdChanged.connect(self.current_page_changed)
        self.finished.connect(self.finished_slot)
        self.btn_browse_connection.clicked.connect(self.show_settings)

        # Initialize
        self.current_page_changed(1)
        self.update_connection_info()
        self.restore_settings()
        self.initialize_feedback()

        # Set help pages
        #self.txt_help_page_2.setHtml(self.help_strings.WIZ_ADD_POINTS_OPERATION_PAGE_2_OPTION_CSV)
        #self.txt_help_page_3.setHtml(self.help_strings.WIZ_ADD_POINTS_OPERATION_PAGE_3_OPTION_CSV)

        # Set MessageBar for QWizard
        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.setLayout(QGridLayout())
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

    def current_page_changed(self, id):
        """
        Reset the Next button. Needed because Next might have been disabled by a
        condition in a another SLOT.
        """
        #enable_next_wizard(self)
        button_list = [QWizard.HelpButton,
                       QWizard.Stretch,
                       QWizard.BackButton,
                       QWizard.CustomButton1,
                       QWizard.NextButton,
                       QWizard.FinishButton,
                       QWizard.CancelButton]
        not_visible = []

        if id == self.dict_pages_ids[self.wizardPage1]:
            self.setWindowTitle(QCoreApplication.translate(self.WIZARD_NAME, "Run supplies ETL"))
            button_list.remove(QWizard.BackButton)
            button_list.remove(QWizard.CustomButton1)
            button_list.remove(QWizard.FinishButton)
        elif id == self.dict_pages_ids[self.wizardPage2]:
            button_list.remove(QWizard.FinishButton)
            not_visible.append(self.NextButton)
            self.load_data_source_controls()
            if self.rad_snc_data.isChecked():
                self.setWindowTitle(QCoreApplication.translate(self.WIZARD_NAME, "ETL: SNC to Supplies model"))
            else:
                self.setWindowTitle(QCoreApplication.translate(self.WIZARD_NAME, "ETL: Cobol to Supplies model"))
        elif id == self.dict_pages_ids[self.wizardPage3]:
            self.bar.clearWidgets()
            button_list.remove(QWizard.CustomButton1)
            button_list.remove(QWizard.NextButton)
            self.wizardPage3.setFinalPage(True)

        self.setButtonLayout(button_list)
        for button in not_visible:
            self.button(button).setVisible(False)

    def etl_option_changed(self):
        """
        Adjust help, names and titles according to the selected option
        """
        if self.rad_snc_data.isChecked():
            #self.txt_help_page_1.setHtml(self.help_strings.WIZ_ADD_POINTS_OPERATION_PAGE_1_OPTION_BP)
            self.tool_name = QCoreApplication.translate("ETLCobolDialog", "ETL-SNC")
        elif self.rad_cobol_data.isChecked(): # self.rad_cobol_data is checked
            #self.txt_help_page_1.setHtml(self.help_strings.WIZ_ADD_POINTS_OPERATION_PAGE_1_OPTION_SP)
            self.tool_name = QCoreApplication.translate("ETLCobolDialog", "ETL-Cobol")

    def load_data_source_controls(self):
        self.clear_data_source_widget()
        if self.rad_snc_data.isChecked():
            self._data_source_widget = SNCDataSourceWidget()
        else:  # Cobol
            self._data_source_widget = CobolDataSourceWidget()

        self._data_source_widget.input_data_changed.connect(self.set_import_button_enabled)
        self._data_source_widget.emit_input_data_changed()  # Initialize input validation
        self.data_source_layout.addWidget(self._data_source_widget)
        self._data_source_widget.setVisible(True)

    def clear_data_source_widget(self):
        while self.data_source_layout.count():
            child = self.data_source_layout.takeAt(0)
            if child.widget():
                child.widget().setVisible(False)

    def initialize_feedback(self):
        self.progress.setValue(0)
        self.progress.setVisible(False)
        self.custom_feedback = CustomFeedback()
        self.custom_feedback.progressChanged.connect(self.progress_changed)
        self.set_gui_controls_enabled(True)

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

    def set_gui_controls_enabled(self, enable):
        self.gbx_data_source.setEnabled(enable)
        self.target_data.setEnabled(enable)
        self.set_import_button_enabled(enable)

    def set_import_button_enabled(self, enable):
        self.button(QWizard.CustomButton1).setEnabled(enable)

    def import_button_clicked(self):
        self.bar.clearWidgets()
        self.save_settings()
        etl_result = False

        if self.rad_snc_data.isChecked():
            etl = ETLCobol(self.names, self._data_source_widget)
        else:  # Cobol
            etl = ETLCobol(self.names, self._data_source_widget)

        if self._db.test_connection()[0]:
            reply = QMessageBox.question(self,
                QCoreApplication.translate(self.WIZARD_NAME, "Warning"),
                QCoreApplication.translate(self.WIZARD_NAME, "The database <i>{}</i> already has a valid LADM_COL structure.<br/><br/>If such database has any data, loading data into it might cause invalid data.<br/><br/>Do you still want to continue?").format(self._db.get_description_conn_string()),
                QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.set_gui_controls_enabled(False)
                self.button(self.BackButton).setEnabled(False)
                self.button(self.CustomButton1).setEnabled(False)
                with OverrideCursor(Qt.WaitCursor):
                    res_alpha, msg_alpha = etl.load_alphanumeric_layers()
                    if res_alpha:
                        res_spatial, msg_spatial = etl.load_spatial_layers()
                        if res_spatial:
                            res_model, msg_model = self.load_model_layers(etl.layers)
                            if res_model:
                                self._running_tool = True
                                self.progress.setVisible(True)
                                etl.run_etl_model(self.custom_feedback)
                                if not self.custom_feedback.isCanceled():
                                    self.progress.setValue(100)

                                    self.button(self.NextButton).setVisible(True)
                                    self.button(self.CustomButton1).setVisible(False)
                                    self.show_message(QCoreApplication.translate(self.WIZARD_NAME,
                                                        "The {} has finished successfully!").format(self.tool_name),
                                                      Qgis.Success, 0)

                                    self.logger.clear_status()
                                    etl_result = True
                                else:
                                    self.initialize_feedback()  # Get ready for an eventual new execution
                                    self.logger.clear_status()
                                self._running_tool = False
                            else:
                                self.show_message(msg_model, Qgis.Warning)
                        else:
                            self.show_message(msg_spatial, Qgis.Warning)
                    else:
                        self.show_message(msg_alpha, Qgis.Warning)
        else:
            with OverrideCursor(Qt.WaitCursor):
                # TODO: if an empty schema was selected, do the magic under the hood
                # self.create_model_into_database()
                # Now execute "accepted()"
                msg = QCoreApplication.translate("ETLCobolDialog", "To run the ETL, the database (schema) should have the Supplies LADM_COL structure. Choose a proper database (schema) and try again.")
                self.show_message(msg, Qgis.Warning)
                self.logger.warning(__name__, msg)

        self.on_result.emit(etl_result)  # Inform other classes if the execution was successful

    def reject(self):
        if self._running_tool:
            reply = QMessageBox.question(self,
                                         QCoreApplication.translate(self.WIZARD_NAME, "Warning"),
                                         QCoreApplication.translate(self.WIZARD_NAME,
                                                                    "The '{}' tool is still running. Do you want to cancel it? If you cancel, the data might be incomplete in the target database.").format(self.tool_name),
                                         QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.custom_feedback.cancel()
                self._running_tool = False
                msg = QCoreApplication.translate(self.WIZARD_NAME, "The '{}' tool was cancelled.").format(self.tool_name)
                self.logger.info(__name__, msg)
                self.show_message(msg, Qgis.Info)
        else:
            if self._db_was_changed:
                self.conn_manager.db_connection_changed.emit(self._db, self._db.test_connection()[0], self.db_source)
            self.logger.info(__name__, "Dialog closed.")
            self.done(1)

    def finished_slot(self, result):
        self.bar.clearWidgets()

    def show_message(self, message, level, duration=10):
        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.bar.pushMessage(message, level, duration)

    def save_settings(self):
        settings = QSettings()
        etl_source = "snc"
        if self.rad_snc_data.isChecked():
            etl_source = "snc"
        elif self.rad_cobol_data.isChecked():
            etl_source = "cobol"

        settings.setValue('Asistente-LADM_COL/supplies/etl_source', etl_source)

    def restore_settings(self):
        settings = QSettings()
        etl_source = settings.value('Asistente-LADM_COL/supplies/etl_source') or 'snc'
        if etl_source == 'snc':
            self.rad_snc_data.setChecked(True)
        elif etl_source == 'cobol':
            self.rad_cobol_data.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help()  # TODO show_help from utils

    def show_settings(self):
        dlg = SettingsDialog(qgis_utils=self.qgis_utils, conn_manager=self.conn_manager)
        dlg.set_db_source(self.db_source)

        dlg.db_connection_changed.connect(self.db_connection_changed)
        if self.db_source == COLLECTED_DB_SOURCE:
            dlg.db_connection_changed.connect(self.qgis_utils.cache_layers_and_relations)

        # We only need those tabs related to Model Baker/ili2db operations
        for i in reversed(range(dlg.tabWidget.count())):
            if i not in [SETTINGS_CONNECTION_TAB_INDEX]:
                dlg.tabWidget.removeTab(i)

        dlg.set_action_type(EnumDbActionType.SCHEMA_IMPORT)  # To avoid unnecessary validations (LADM compliance)

        if dlg.exec_():
            self._db = dlg.get_db_connection()
            self.update_connection_info()

    def update_connection_info(self):
        db_description = self._db.get_description_conn_string()
        if db_description:
            self.db_connect_label.setText(db_description)
            self.db_connect_label.setToolTip(self._db.get_display_conn_string())
        else:
            self.db_connect_label.setText(
                QCoreApplication.translate(self.WIZARD_NAME, "The database is not defined!"))
            self.db_connect_label.setToolTip('')

    def db_connection_changed(self, db, ladm_col_db, db_source):
        # We dismiss parameters here, after all, we already have the db, and the ladm_col_db may change from this moment
        # until we close the supplies dialog (e.g., we might run an import schema before under the hood)
        self._db_was_changed = True

    def load_model_layers(self, layers):
        self.qgis_utils.get_layers(self._db, layers, load=True)
        if not layers:
            return False, QCoreApplication.translate(self.WIZARD_NAME,
                                                     "There was a problem loading layers from the 'Supplies' model!")

        return True, ''


class ETLCobol(QObject):
    CLASS_NAME = "ETLCobol"

    def __init__(self, names, data_source_widget):
        QObject.__init__(self)
        self.names = names
        self.data_source_widget = data_source_widget
        self.logger = Logger()

        self.lis_paths = {}
        self.gdb_path = self.data_source_widget.txt_file_path_gdb.text()

        self.gdb_layer_paths = dict()
        self.layers = dict()

        self.initialize_layers()

    def initialize_layers(self):
        self.layers = {
            self.names.GC_PARCEL_T: {'name': self.names.GC_PARCEL_T, 'geometry': None, LAYER: None},
            self.names.GC_OWNER_T: {'name': self.names.GC_OWNER_T, 'geometry': None, LAYER: None},
            self.names.GC_ADDRESS_T: {'name': self.names.GC_ADDRESS_T, 'geometry': QgsWkbTypes.LineGeometry, LAYER: None},
            self.names.GC_BUILDING_UNIT_T: {'name': self.names.GC_BUILDING_UNIT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.GC_BUILDING_T: {'name': self.names.GC_BUILDING_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.GC_PLOT_T: {'name': self.names.GC_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.GC_RURAL_DIVISION_T: {'name': self.names.GC_RURAL_DIVISION_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.GC_URBAN_SECTOR_T: {'name': self.names.GC_URBAN_SECTOR_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.GC_RURAL_SECTOR_T: {'name': self.names.GC_RURAL_SECTOR_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.GC_PERIMETER_T: {'name': self.names.GC_PERIMETER_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.GC_BLOCK_T: {'name': self.names.GC_BLOCK_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.GC_NEIGHBOURHOOD_T: {'name': self.names.GC_NEIGHBOURHOOD_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.GC_COMMISSION_BUILDING_T: {'name': self.names.GC_COMMISSION_BUILDING_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.GC_COMMISSION_PLOT_T: {'name': self.names.GC_COMMISSION_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.GC_COMMISSION_BUILDING_UNIT_T: {'name': self.names.GC_COMMISSION_BUILDING_UNIT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None}
        }

    def run_etl_model(self, custom_feedback):
        self.logger.info(__name__, "Running ETL-Cobol model...")
        processing.run("model:ETL-model-supplies",
                       {'barrio': self.gdb_layer_paths['U_BARRIO'],
                        'gcbarrio': self.layers[self.names.GC_NEIGHBOURHOOD_T][LAYER],
                        'gccomisionconstruccion': self.layers[self.names.GC_COMMISSION_BUILDING_T][LAYER],
                        'gccomisionterreno': self.layers[self.names.GC_COMMISSION_PLOT_T][LAYER],
                        'gcconstruccion': self.layers[self.names.GC_BUILDING_T][LAYER],
                        'gcdireccion': self.layers[self.names.GC_ADDRESS_T][LAYER],
                        'gcmanzana': self.layers[self.names.GC_BLOCK_T][LAYER],
                        'gcperimetro': self.layers[self.names.GC_PERIMETER_T][LAYER],
                        'gcpropietario': self.layers[self.names.GC_OWNER_T][LAYER],
                        'gcsector': self.layers[self.names.GC_RURAL_SECTOR_T][LAYER],
                        'gcsectorurbano': self.layers[self.names.GC_URBAN_SECTOR_T][LAYER],
                        'gcterreno': self.layers[self.names.GC_PLOT_T][LAYER],
                        'gcunidad': self.layers[self.names.GC_BUILDING_UNIT_T][LAYER],
                        'gcunidadconstruccioncomision': self.layers[self.names.GC_COMMISSION_BUILDING_UNIT_T][LAYER],
                        'gcvereda': self.layers[self.names.GC_RURAL_DIVISION_T][LAYER],
                        'inputblo': self.lis_paths['blo'],
                        'inputconstruccion': self.gdb_layer_paths['R_CONSTRUCCION'],
                        'inputmanzana': self.gdb_layer_paths['U_MANZANA'],
                        'inputperimetro': self.gdb_layer_paths['U_PERIMETRO'],
                        'inputpro': self.lis_paths['pro'],
                        'inputrunidad': self.gdb_layer_paths['R_UNIDAD'],
                        'inputsector': self.gdb_layer_paths['R_SECTOR'],
                        'inputter': self.lis_paths['ter'],
                        'inputterreno': self.gdb_layer_paths['R_TERRENO'],
                        'inputuconstruccion': self.gdb_layer_paths['U_CONSTRUCCION'],
                        'inputuni': self.lis_paths['uni'],
                        'inputusector': self.gdb_layer_paths['U_SECTOR'],
                        'inpututerreno': self.gdb_layer_paths['U_TERRENO'],
                        'inputuunidad': self.gdb_layer_paths['U_UNIDAD'],
                        'inputvereda': self.gdb_layer_paths['R_VEREDA'],
                        'ouputlayer': self.layers[self.names.GC_PARCEL_T][LAYER],
                        'rnomenclatura': self.gdb_layer_paths['R_NOMENCLATURA_DOMICILIARIA'],
                        'unomenclatura': self.gdb_layer_paths['U_NOMENCLATURA_DOMICILIARIA']},
                       feedback=custom_feedback)
        self.logger.info(__name__, "ETL-Cobol model finished.")

    def load_alphanumeric_layers(self):
        self.lis_paths = {
            'blo': self.data_source_widget.txt_file_path_blo.text().strip(),
            'uni': self.data_source_widget.txt_file_path_uni.text().strip(),
            'ter': self.data_source_widget.txt_file_path_ter.text().strip(),
            'pro': self.data_source_widget.txt_file_path_pro.text().strip()
        }

        root = QgsProject.instance().layerTreeRoot()
        lis_group = root.addGroup(QCoreApplication.translate(self.CLASS_NAME, "LIS Supplies"))

        for name in self.lis_paths:
            uri = 'file:///{}?type=csv&delimiter=;&detectTypes=yes&geomType=none&subsetIndex=no&watchFile=no'.format(self.lis_paths[name])
            layer = QgsVectorLayer(uri, name, 'delimitedtext')
            if layer.isValid():
                self.lis_paths[name] = layer
                QgsProject.instance().addMapLayer(layer, False)
                lis_group.addLayer(layer)
            else:
                if name == 'blo':
                    # BLO is kind of optional, if it is not given, we pass a default one
                    uri = 'file:///{}?type=csv&delimiter=;&detectTypes=yes&geomType=none&subsetIndex=no&watchFile=no'.format(BLO_LIS_FILE_PATH)
                    layer = QgsVectorLayer(uri, name, 'delimitedtext')
                    self.lis_paths[name] = layer
                    QgsProject.instance().addMapLayer(layer, False)
                    lis_group.addLayer(layer)
                else:
                    return False, QCoreApplication.translate(self.CLASS_NAME, "There were troubles loading the LIS file called '{}'.".format(name))

        return True, ''

    def load_spatial_layers(self):
        required_layers = ['R_TERRENO', 'U_TERRENO', 'R_SECTOR', 'U_SECTOR', 'R_VEREDA', 'U_MANZANA', 'U_BARRIO',
                           'R_CONSTRUCCION', 'U_CONSTRUCCION', 'U_UNIDAD', 'R_UNIDAD',
                           'U_NOMENCLATURA_DOMICILIARIA', 'R_NOMENCLATURA_DOMICILIARIA', 'U_PERIMETRO']

        self.gdb_layer_paths = dict()

        layer = QgsVectorLayer(self.gdb_path, 'layer name', 'ogr')

        if not layer.isValid():
            return False, QCoreApplication.translate(self.CLASS_NAME, "There were troubles loading the GDB.")

        sublayers = layer.dataProvider().subLayers()

        root = QgsProject.instance().layerTreeRoot()
        gdb_group = root.addGroup(QCoreApplication.translate(self.CLASS_NAME, "GDB Supplies"))

        for data in sublayers:
            sublayer = data.split('!!::!!')[1]
            if sublayer in required_layers:
                layer = QgsVectorLayer(self.gdb_path + '|layername=' + sublayer, sublayer, 'ogr')
                self.gdb_layer_paths[sublayer] = layer
                QgsProject.instance().addMapLayer(layer, False)
                gdb_group.addLayer(layer)

        if len(self.gdb_layer_paths) != len(required_layers):
            return False, QCoreApplication.translate(self.CLASS_NAME, "The GDB does not have the required layers!")

        return True, ''