# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-06-11
        git sha              : :%H$
        copyright            : (C) 2018 by Germán Carrillo (BSF Swissphoto)
                               (C) 2019 by Leonardo Cardona (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
                               leocardonapiedrahita@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
import os
import re

from QgisModelBaker.libili2db import iliimporter
from QgisModelBaker.libili2db.ili2dbconfig import (ImportDataConfiguration,
                                                   BaseConfiguration)
from QgisModelBaker.libili2db.ili2dbutils import color_log_text
from QgisModelBaker.libili2db.ilicache import IliCache
from QgisModelBaker.libili2db.iliimporter import JavaNotFoundError
from qgis.PyQt.QtCore import (Qt,
                              pyqtSignal,
                              QCoreApplication,
                              QSettings)
from qgis.PyQt.QtGui import (QColor,
                             QValidator,
                             QStandardItemModel,
                             QStandardItem)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QSizePolicy,
                                 QDialogButtonBox)
from qgis.core import Qgis
from qgis.gui import QgsGui
from qgis.gui import QgsMessageBar

from ...config.general_config import (DEFAULT_EPSG,
                                      DEFAULT_INHERITANCE,
                                      DEFAULT_HIDDEN_MODELS,
                                      SETTINGS_CONNECTION_TAB_INDEX,
                                      CREATE_BASKET_COL,
                                      CREATE_IMPORT_TID,
                                      STROKE_ARCS)
from ...gui.dlg_get_java_path import DialogGetJavaPath
from ...gui.settings_dialog import SettingsDialog
from ...utils.qgis_model_baker_utils import get_java_path_from_qgis_model_baker
from ...utils import get_ui_class
from ...utils.qt_utils import (Validators,
                               FileValidator,
                               make_file_selector,
                               OverrideCursor)

from ...resources_rc import * # Necessary to show icons
from ...config.config_db_supported import ConfigDbSupported
from ...lib.db.enum_db_action_type import EnumDbActionType

DIALOG_UI = get_ui_class('qgis_model_baker/dlg_import_data.ui')


class DialogImportData(QDialog, DIALOG_UI):

    open_dlg_import_schema = pyqtSignal(list) # selected models
    BUTTON_NAME_IMPORT_DATA = QCoreApplication.translate("DialogImportData", "Import data")
    BUTTON_NAME_GO_TO_CREATE_STRUCTURE = QCoreApplication.translate("DialogImportData",  "Go to Create Structure...")

    def __init__(self, iface, qgis_utils, conn_manager):
        QDialog.__init__(self)
        self.setupUi(self)

        QgsGui.instance().enableAutoGeometryRestore(self)
        self.iface = iface
        self.conn_manager = conn_manager
        self.db = self.conn_manager.get_db_connector_from_source()
        self.qgis_utils = qgis_utils
        self.base_configuration = BaseConfiguration()

        self.ilicache = IliCache(self.base_configuration)
        self.ilicache.refresh()

        self._conf_db = ConfigDbSupported()
        self._params = None
        self._current_db = None

        self.xtf_file_browse_button.clicked.connect(
            make_file_selector(self.xtf_file_line_edit, title=QCoreApplication.translate("DialogImportData",'Open Transfer or Catalog File'),
                               file_filter=QCoreApplication.translate("DialogImportData",'Transfer File (*.xtf *.itf);;Catalogue File (*.xml *.xls *.xlsx)')))

        self.validators = Validators()
        self.xtf_file_line_edit.setPlaceholderText(QCoreApplication.translate("DialogImportData", "[Name of the XTF to be imported]"))
        fileValidator = FileValidator(pattern=['*.xtf', '*.itf', '*.xml'])
        self.xtf_file_line_edit.setValidator(fileValidator)
        self.xtf_file_line_edit.textChanged.connect(self.update_import_models)
        self.xtf_file_line_edit.textChanged.emit(self.xtf_file_line_edit.text())

        # db
        self.connection_setting_button.clicked.connect(self.show_settings)

        self.connection_setting_button.setText(QCoreApplication.translate("DialogImportData", 'Connection Settings'))

        # LOG
        self.log_config.setTitle(QCoreApplication.translate("DialogImportData", "Show log"))

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

        self.buttonBox.accepted.disconnect()
        self.buttonBox.clicked.connect(self.accepted_import_data)
        self.buttonBox.clear()
        self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self._accept_button = self.buttonBox.addButton(self.BUTTON_NAME_IMPORT_DATA, QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(QDialogButtonBox.Help)
        self.buttonBox.helpRequested.connect(self.show_help)

        self.update_connection_info()
        self.restore_configuration()

    def accepted_import_data(self, button):
        if self.buttonBox.buttonRole(button) == QDialogButtonBox.AcceptRole:
            if button.text() == self.BUTTON_NAME_IMPORT_DATA:
                self.accepted()
            elif button.text() == self.BUTTON_NAME_GO_TO_CREATE_STRUCTURE:
                self.close()  # Close import data dialog
                self.open_dlg_import_schema.emit(self.get_ili_models())  # Emit signal to open import schema dialog

    def update_connection_info(self):
        db_description = self.db.get_description_conn_string()
        if db_description:
            self.db_connect_label.setText(db_description)
            self.db_connect_label.setToolTip(self.db.get_display_conn_string())
            self._accept_button.setEnabled(True)
        else:
            self.db_connect_label.setText(QCoreApplication.translate("DialogImportData", "The database is not defined!"))
            self.db_connect_label.setToolTip('')
            self._accept_button.setEnabled(False)

    def update_import_models(self):
        message_error = None

        if not self.xtf_file_line_edit.text().strip():
            color = '#ffd356'  # Light orange
            self.import_models_qmodel = QStandardItemModel()
            self.import_models_list_view.setModel(self.import_models_qmodel)
        else:

            if os.path.isfile(self.xtf_file_line_edit.text().strip()):
                color = '#fff'  # White

                self.import_models_qmodel = QStandardItemModel()
                models_name = self.find_models_xtf(self.xtf_file_line_edit.text().strip())

                for model_name in models_name:
                    if not model_name in DEFAULT_HIDDEN_MODELS:
                        item = QStandardItem(model_name)
                        item.setCheckable(False)
                        item.setEditable(False)
                        self.import_models_qmodel.appendRow(item)

                if self.import_models_qmodel.rowCount() > 0:
                    self.import_models_list_view.setModel(self.import_models_qmodel)
                else:
                    message_error = QCoreApplication.translate("DialogImportData",
                                                               "No models were found in the XTF. Is it a valid file?")
                    color = '#ffd356'  # Light orange
                    self.import_models_qmodel = QStandardItemModel()
                    self.import_models_list_view.setModel(self.import_models_qmodel)
            else:
                message_error = QCoreApplication.translate("DialogImportData", "Please set a valid XTF file")
                color = '#ffd356'  # Light orange
                self.import_models_qmodel = QStandardItemModel()
                self.import_models_list_view.setModel(self.import_models_qmodel)
        self.xtf_file_line_edit.setStyleSheet('QLineEdit {{ background-color: {} }}'.format(color))

        if message_error:
            self.txtStdout.setText(message_error)
            self.show_message(message_error, Qgis.Warning)
            self.import_models_list_view.setFocus()
            return

    def find_models_xtf(self, xtf_path):
        models_name = list()
        pattern = re.compile(r'<MODEL[^>]*>(?P<text>[^<]*)</MODEL>')
        with open(xtf_path, 'r') as f:
            for txt in pattern.finditer(f.read()):
                model_tag = str(txt.group(0))
                name = re.findall('NAME="(.*?)"', model_tag, re.IGNORECASE)
                models_name.extend(name)
        return sorted(models_name)

    def get_ili_models(self):
        ili_models = list()
        for index in range(self.import_models_qmodel.rowCount()):
            item = self.import_models_qmodel.item(index)
            ili_models.append(item.text())
        return ili_models

    def show_settings(self):
        dlg = SettingsDialog(qgis_utils=self.qgis_utils, conn_manager=self.conn_manager)

        # Connect signals (DBUtils, QgisUtils)
        dlg.db_connection_changed.connect(self.conn_manager.db_connection_changed)
        dlg.db_connection_changed.connect(self.qgis_utils.cache_layers_and_relations)
        dlg.organization_tools_changed.connect(self.qgis_utils.organization_tools_changed)

        dlg.set_action_type(EnumDbActionType.IMPORT)
        dlg.tabWidget.setCurrentIndex(SETTINGS_CONNECTION_TAB_INDEX)
        if dlg.exec_():
            self.db = dlg.get_db_connection()
            self.update_connection_info()

    def accepted(self):
        configuration = self.update_configuration()

        if not os.path.isfile(self.xtf_file_line_edit.text().strip()):
            message_error = 'Please set a valid XTF file before importing data. XTF file does not exist'
            self.txtStdout.setText(QCoreApplication.translate("DialogImportData", message_error))
            self.show_message(message_error, Qgis.Warning)
            self.xtf_file_line_edit.setFocus()
            return

        if not self.xtf_file_line_edit.validator().validate(configuration.xtffile, 0)[0] == QValidator.Acceptable:
            message_error = 'Please set a valid XTF before importing data.'
            self.txtStdout.setText(QCoreApplication.translate("DialogImportData", message_error))
            self.show_message(message_error, Qgis.Warning)
            self.xtf_file_line_edit.setFocus()
            return

        if not self.get_ili_models():
            message_error = QCoreApplication.translate("DialogImportData", "The selected XTF file does not have information according to the LADM-COL model to import.")
            self.txtStdout.setText(message_error)
            self.show_message(message_error, Qgis.Warning)
            self.import_models_list_view.setFocus()
            return

        # Get list models in db and xtf
        ili_models = set([ili_model for ili_model in self.get_ili_models()])

        db_models = list()
        for db_model in self.db.get_models():
            model_name_with_dependencies = db_model['modelname']
            model_name = model_name_with_dependencies.split('{')[0]
            db_models.append(model_name)
        db_models = set(db_models)

        if not ili_models.issubset(db_models):
            message_error = "The XTF file to import does not have the same models as the target database schema. " \
                            "Please create a schema that also includes the following missing modules:\n\n * {}".format(" \n * ".join(sorted(ili_models.difference(db_models))))
            self.txtStdout.clear()
            self.txtStdout.setTextColor(QColor('#000000'))
            self.txtStdout.setText(QCoreApplication.translate("DialogImportData", message_error))
            self.show_message(message_error, Qgis.Warning)
            self.xtf_file_line_edit.setFocus()

            # button is removed to define order in GUI
            for button in self.buttonBox.buttons():
                if button.text() == self.BUTTON_NAME_IMPORT_DATA:
                    self.buttonBox.removeButton(button)

            # Check if button was previously added
            self.remove_create_structure_button()

            self.buttonBox.addButton(self.BUTTON_NAME_GO_TO_CREATE_STRUCTURE,
                                     QDialogButtonBox.AcceptRole).setStyleSheet("color: #aa2222;")
            self.buttonBox.addButton(self.BUTTON_NAME_IMPORT_DATA,
                                     QDialogButtonBox.AcceptRole)

            return

        with OverrideCursor(Qt.WaitCursor):
            self.progress_bar.show()
            self.progress_bar.setValue(0)

            self.disable()
            self.txtStdout.setTextColor(QColor('#000000'))
            self.txtStdout.clear()

            dataImporter = iliimporter.Importer(dataImport=True)

            item_db = self._conf_db.get_db_items()[self.db.mode]

            dataImporter.tool = item_db.get_mbaker_db_ili_mode()
            dataImporter.configuration = configuration

            self.save_configuration(configuration)

            dataImporter.stdout.connect(self.print_info)
            dataImporter.stderr.connect(self.on_stderr)
            dataImporter.process_started.connect(self.on_process_started)
            dataImporter.process_finished.connect(self.on_process_finished)

            self.progress_bar.setValue(25)

            try:
                if dataImporter.run() != iliimporter.Importer.SUCCESS:
                    self.enable()
                    self.progress_bar.hide()
                    self.show_message(QCoreApplication.translate("DialogImportData", "An error occurred when importing the data. For more information see the log..."), Qgis.Warning)
                    return
            except JavaNotFoundError:

                # Set JAVA PATH
                get_java_path_dlg = DialogGetJavaPath()
                get_java_path_dlg.setModal(True)
                if get_java_path_dlg.exec_():
                    configuration = self.update_configuration()

                if not get_java_path_from_qgis_model_baker():
                    message_error_java = QCoreApplication.translate("DialogImportData",
                                                                    """Java could not be found. You can configure the JAVA_HOME environment variable, restart QGIS and try again.""")
                    self.txtStdout.setTextColor(QColor('#000000'))
                    self.txtStdout.clear()
                    self.txtStdout.setText(message_error_java)
                    self.show_message(message_error_java, Qgis.Warning)
                self.enable()
                self.progress_bar.hide()
                return

            self.buttonBox.clear()
            self.buttonBox.setEnabled(True)
            self.buttonBox.addButton(QDialogButtonBox.Close)
            self.progress_bar.setValue(100)
            self.show_message(QCoreApplication.translate("DialogImportData", "Import of the data was successfully completed"), Qgis.Success)

    def remove_create_structure_button(self):
        for button in self.buttonBox.buttons():
            if button.text() == self.BUTTON_NAME_GO_TO_CREATE_STRUCTURE:
                self.buttonBox.removeButton(button)

    def save_configuration(self, configuration):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/QgisModelBaker/ili2pg/xtffile_import', configuration.xtffile)
        settings.setValue('Asistente-LADM_COL/QgisModelBaker/show_log', not self.log_config.isCollapsed())

    def restore_configuration(self):
        settings = QSettings()

        self.xtf_file_line_edit.setText(settings.value('Asistente-LADM_COL/QgisModelBaker/ili2pg/xtffile_import'))

        # Show log
        value_show_log = settings.value('Asistente-LADM_COL/QgisModelBaker/show_log', False, type=bool)
        self.log_config.setCollapsed(not value_show_log)

        # set model repository
        # if there is no option  by default use online model repository
        self.use_local_models = settings.value('Asistente-LADM_COL/models/custom_model_directories_is_checked', type=bool)
        if self.use_local_models:
            self.custom_model_directories = settings.value('Asistente-LADM_COL/models/custom_models') if settings.value('Asistente-LADM_COL/models/custom_models') else None

    def update_configuration(self):
        """
        Get the configuration that is updated with the user configuration changes on the dialog.
        :return: Configuration
        """
        item_db = self._conf_db.get_db_items()[self.db.mode]

        configuration = ImportDataConfiguration()
        item_db.set_db_configuration_params(self.db.dict_conn_params, configuration)

        configuration.xtffile = self.xtf_file_line_edit.text().strip()
        configuration.delete_data = False

        configuration.epsg = QSettings().value('Asistente-LADM_COL/advanced_settings/epsg', int(DEFAULT_EPSG), int)
        configuration.inheritance = DEFAULT_INHERITANCE
        configuration.create_basket_col = CREATE_BASKET_COL
        configuration.create_import_tid = CREATE_IMPORT_TID
        configuration.stroke_arcs = STROKE_ARCS

        java_path = get_java_path_from_qgis_model_baker()
        if java_path:
            self.base_configuration.java_path = java_path

        # Check custom model directories
        if self.use_local_models:
            if self.custom_model_directories is None:
                self.base_configuration.custom_model_directories_enabled = False
            else:
                self.base_configuration.custom_model_directories = self.custom_model_directories
                self.base_configuration.custom_model_directories_enabled = True

        configuration.base_configuration = self.base_configuration
        if self.get_ili_models():
            configuration.ilimodels = ';'.join(self.get_ili_models())

        configuration.disable_validation = not QSettings().value('Asistente-LADM_COL/advanced_settings/validate_data_importing_exporting', True, bool)

        return configuration

    def print_info(self, text, text_color='#000000', clear=False):
        self.txtStdout.setTextColor(QColor(text_color))
        self.txtStdout.append(text)
        QCoreApplication.processEvents()

    def on_stderr(self, text):
        color_log_text(text, self.txtStdout)
        self.advance_progress_bar_by_text(text)

    def on_process_started(self, command):
        self.disable()
        self.txtStdout.setTextColor(QColor('#000000'))
        self.txtStdout.clear()
        self.txtStdout.setText(command)
        QCoreApplication.processEvents()

    def on_process_finished(self, exit_code, result):
        color = '#004905' if exit_code == 0 else '#aa2222'
        self.txtStdout.setTextColor(QColor(color))
        self.txtStdout.append('Finished ({})'.format(exit_code))
        if result == iliimporter.Importer.SUCCESS:
            self.buttonBox.clear()
            self.buttonBox.setEnabled(True)
            self.buttonBox.addButton(QDialogButtonBox.Close)
        else:
            self.show_message(QCoreApplication.translate("DialogImportData", "Error when importing data"), Qgis.Warning)
            self.enable()

            # Open log
            if self.log_config.isCollapsed():
                self.log_config.setCollapsed(False)

    def advance_progress_bar_by_text(self, text):
        if text.strip() == 'Info: compile models...':
            self.progress_bar.setValue(50)
            QCoreApplication.processEvents()
        elif text.strip() == 'Info: create table structure...':
            self.progress_bar.setValue(55)
            QCoreApplication.processEvents()
        elif text.strip() == 'Info: first validation pass...':
            self.progress_bar.setValue(60)
            QCoreApplication.processEvents()
        elif text.strip() == 'Info: second validation pass...':
            self.progress_bar.setValue(80)
            QCoreApplication.processEvents()

    def show_help(self):
        self.qgis_utils.show_help("import_data")

    def disable(self):
        self.db_config.setEnabled(False)
        self.ili_config.setEnabled(False)
        self.buttonBox.setEnabled(False)

    def enable(self):
        self.db_config.setEnabled(True)
        self.ili_config.setEnabled(True)
        self.buttonBox.setEnabled(True)

    def show_message(self, message, level):
        self.bar.pushMessage("Asistente LADM_COL", message, level, duration=0)
