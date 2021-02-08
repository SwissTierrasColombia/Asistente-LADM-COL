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

from QgisModelBaker.libili2db import iliimporter
from QgisModelBaker.libili2db.ili2dbconfig import (ImportDataConfiguration,
                                                   BaseConfiguration)
from QgisModelBaker.libili2db.ili2dbutils import color_log_text
from QgisModelBaker.libili2db.ilicache import IliCache
from QgisModelBaker.libili2db.ili2dbutils import JavaNotFoundError
from asistente_ladm_col.config.ili2db_names import ILI2DBNames
from qgis.PyQt.QtCore import (Qt,
                              pyqtSignal,
                              QCoreApplication,
                              QSettings)
from qgis.PyQt.QtGui import (QColor,
                             QValidator,
                             QStandardItemModel,
                             QStandardItem)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QMessageBox,
                                 QSizePolicy,
                                 QDialogButtonBox)
from qgis.core import Qgis
from qgis.gui import QgsGui
from qgis.gui import QgsMessageBar

from asistente_ladm_col.config.general_config import (COLLECTED_DB_SOURCE,
                                                      SETTINGS_CONNECTION_TAB_INDEX,
                                                      JAVA_REQUIRED_VERSION,
                                                      SETTINGS_MODELS_TAB_INDEX,
                                                      DEFAULT_USE_CUSTOM_MODELS,
                                                      DEFAULT_MODELS_DIR,
                                                      DEFAULT_SRS_CODE,
                                                      DEFAULT_SRS_AUTH)
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.gui.dialogs.dlg_settings import SettingsDialog
from asistente_ladm_col.lib.ladm_col_models import LADMColModelRegistry
from asistente_ladm_col.utils.interlis_utils import get_models_from_xtf
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.dependency.java_dependency import JavaDependency
from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.utils import show_plugin_help
from asistente_ladm_col.utils.qt_utils import (Validators,
                                               FileValidator,
                                               make_file_selector,
                                               OverrideCursor)

from asistente_ladm_col.config.config_db_supported import ConfigDBsSupported
from asistente_ladm_col.config.enums import EnumDbActionType

DIALOG_UI = get_ui_class('qgis_model_baker/dlg_import_data.ui')


class DialogImportData(QDialog, DIALOG_UI):
    open_dlg_import_schema = pyqtSignal(dict)  # dict with key-value params
    BUTTON_NAME_IMPORT_DATA = QCoreApplication.translate("DialogImportData", "Import data")
    BUTTON_NAME_GO_TO_CREATE_STRUCTURE = QCoreApplication.translate("DialogImportData",  "Go to Create Structure...")

    def __init__(self, iface, conn_manager, context, link_to_import_schema=True, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        QgsGui.instance().enableAutoGeometryRestore(self)
        self.iface = iface
        self.conn_manager = conn_manager
        self.db_source = context.get_db_sources()[0]
        self.link_to_import_schema = link_to_import_schema
        self.db = self.conn_manager.get_db_connector_from_source(self.db_source)
        self.base_configuration = BaseConfiguration()
        self.logger = Logger()
        self.app = AppInterface()
        self.__ladmcol_models = LADMColModelRegistry()

        self.java_dependency = JavaDependency()
        self.java_dependency.download_dependency_completed.connect(self.download_java_complete)
        self.java_dependency.download_dependency_progress_changed.connect(self.download_java_progress_change)

        self.ilicache = IliCache(self.base_configuration)
        self.ilicache.refresh()

        self._dbs_supported = ConfigDBsSupported()
        self._running_tool = False

        # There may be 1 case where we need to emit a db_connection_changed from the Import Data dialog:
        #   1) Connection Settings was opened and the DB conn was changed.
        self._db_was_changed = False  # To postpone calling refresh gui until we close this dialog instead of settings

        # Similarly, we could call a refresh on layers and relations cache in 1 case:
        #   1) If the ID dialog was called for the COLLECTED source: opening Connection Settings and changing the DB
        #      connection.
        self._schedule_layers_and_relations_refresh = False

        # We need bar definition above calling clear_messages
        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

        self.xtf_file_browse_button.clicked.connect(
            make_file_selector(self.xtf_file_line_edit, title=QCoreApplication.translate("DialogImportData", "Open Transfer or Catalog File"),
                               file_filter=QCoreApplication.translate("DialogImportData",'Transfer File (*.xtf *.itf);;Catalogue File (*.xml *.xls *.xlsx)')))

        self.validators = Validators()
        self.xtf_file_line_edit.setPlaceholderText(QCoreApplication.translate("DialogImportData", "[Name of the XTF to be imported]"))
        fileValidator = FileValidator(pattern=['*.xtf', '*.itf', '*.xml'])
        self.xtf_file_line_edit.setValidator(fileValidator)
        self.xtf_file_line_edit.textChanged.connect(self.update_import_models)
        self.xtf_file_line_edit.textChanged.emit(self.xtf_file_line_edit.text())

        # db
        self.connection_setting_button.clicked.connect(self.show_settings)
        self.connection_setting_button.setText(QCoreApplication.translate("DialogImportData", "Connection Settings"))

        # LOG
        self.log_config.setTitle(QCoreApplication.translate("DialogImportData", "Show log"))

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
                self.open_dlg_import_schema.emit({'selected_models': self.get_ili_models()})  # Emit signal to open import schema dialog

    def reject(self):
        if self._running_tool:
            QMessageBox.information(self,
                                    QCoreApplication.translate("DialogImportData", "Warning"),
                                    QCoreApplication.translate("DialogImportData", "The Import Data tool is still running. Please wait until it finishes."))
        else:
            self.close_dialog()

    def close_dialog(self):
        """
        We use this method to be safe when emitting the db_connection_changed, otherwise we could trigger slots that
        unload the plugin, destroying dialogs and thus, leading to crashes.
        """
        if self._schedule_layers_and_relations_refresh:
            self.conn_manager.db_connection_changed.connect(self.app.core.cache_layers_and_relations)

        if self._db_was_changed:
            # If the db was changed, it implies it complies with ladm_col, hence the second parameter
            self.conn_manager.db_connection_changed.emit(self.db, True, self.db_source)

        if self._schedule_layers_and_relations_refresh:
            self.conn_manager.db_connection_changed.disconnect(self.app.core.cache_layers_and_relations)

        self.logger.info(__name__, "Dialog closed.")
        self.done(QDialog.Accepted)

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
        self.clear_messages()
        error_msg = None

        if not self.xtf_file_line_edit.text().strip():
            color = '#ffd356'  # Light orange
            self.import_models_qmodel = QStandardItemModel()
            self.import_models_list_view.setModel(self.import_models_qmodel)
        else:
            if os.path.isfile(self.xtf_file_line_edit.text().strip()):
                color = '#fff'  # White

                self.import_models_qmodel = QStandardItemModel()
                model_names= get_models_from_xtf(self.xtf_file_line_edit.text().strip())

                for model in self.__ladmcol_models.supported_models():
                    if not model.hidden() and model.full_name() in model_names:
                        item = QStandardItem(model.full_alias())
                        item.setData(model.full_name(), Qt.UserRole)
                        item.setCheckable(False)
                        item.setEditable(False)
                        self.import_models_qmodel.appendRow(item)

                if self.import_models_qmodel.rowCount() > 0:
                    self.import_models_list_view.setModel(self.import_models_qmodel)
                else:
                    error_msg = QCoreApplication.translate("DialogImportData",
                                                               "No models were found in the XTF. Is it a valid file?")
                    color = '#ffd356'  # Light orange
                    self.import_models_qmodel = QStandardItemModel()
                    self.import_models_list_view.setModel(self.import_models_qmodel)
            else:
                error_msg = QCoreApplication.translate("DialogImportData", "Please set a valid XTF file")
                color = '#ffd356'  # Light orange
                self.import_models_qmodel = QStandardItemModel()
                self.import_models_list_view.setModel(self.import_models_qmodel)
        self.xtf_file_line_edit.setStyleSheet('QLineEdit {{ background-color: {} }}'.format(color))

        if error_msg:
            self.txtStdout.setText(error_msg)
            self.show_message(error_msg, Qgis.Warning)
            self.import_models_list_view.setFocus()
            return

    def get_ili_models(self):
        ili_models = list()
        for index in range(self.import_models_qmodel.rowCount()):
            item = self.import_models_qmodel.item(index)
            ili_models.append(item.data(Qt.UserRole))
        return ili_models

    def show_settings(self):
        # We only need those tabs related to Model Baker/ili2db operations
        dlg = SettingsDialog(self.conn_manager, parent=self)
        dlg.setWindowTitle(QCoreApplication.translate("DialogImportData", "Target DB Connection Settings"))
        dlg.show_tip(QCoreApplication.translate("DialogImportData", "Configure where do you want the XTF data to be imported."))
        dlg.set_db_source(self.db_source)
        dlg.set_tab_pages_list([SETTINGS_CONNECTION_TAB_INDEX, SETTINGS_MODELS_TAB_INDEX])

        # Connect signals (DBUtils, Core)
        dlg.db_connection_changed.connect(self.db_connection_changed)
        if self.db_source == COLLECTED_DB_SOURCE:
            self._schedule_layers_and_relations_refresh = True

        dlg.set_action_type(EnumDbActionType.IMPORT)

        if dlg.exec_():
            self.db = dlg.get_db_connection()
            self.update_connection_info()

    def db_connection_changed(self, db, ladm_col_db, db_source):
        self._db_was_changed = True
        self.clear_messages()

    def accepted(self):
        self._running_tool = True
        self.txtStdout.clear()
        self.progress_bar.setValue(0)
        self.bar.clearWidgets()

        if not os.path.isfile(self.xtf_file_line_edit.text().strip()):
            self._running_tool = False
            error_msg = QCoreApplication.translate("DialogImportData", "Please set a valid XTF file before importing data. XTF file does not exist.")
            self.txtStdout.setText(error_msg)
            self.show_message(error_msg, Qgis.Warning)
            self.xtf_file_line_edit.setFocus()
            return

        java_home_set = self.java_dependency.set_java_home()
        if not java_home_set:
            message_java = QCoreApplication.translate("DialogImportData", """Configuring Java {}...""").format(JAVA_REQUIRED_VERSION)
            self.txtStdout.setTextColor(QColor('#000000'))
            self.txtStdout.clear()
            self.txtStdout.setText(message_java)
            self.java_dependency.get_java_on_demand()
            self.disable()
            return

        configuration = self.update_configuration()

        if configuration.disable_validation:  # If data validation at import is disabled, we ask for confirmation
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Question)
            self.msg.setText(QCoreApplication.translate("DialogImportData",
                                                        "Are you sure you want to import your data without validation?"))
            self.msg.setWindowTitle(QCoreApplication.translate("DialogImportData", "Import XTF without validation?"))
            self.msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            res = self.msg.exec_()
            if res == QMessageBox.No:
                self._running_tool = False
                return

        if not self.xtf_file_line_edit.validator().validate(configuration.xtffile, 0)[0] == QValidator.Acceptable:
            self._running_tool = False
            error_msg = QCoreApplication.translate("DialogImportData", "Please set a valid XTF before importing data.")
            self.txtStdout.setText(error_msg)
            self.show_message(error_msg, Qgis.Warning)
            self.xtf_file_line_edit.setFocus()
            return

        if not self.get_ili_models():
            self._running_tool = False
            error_msg = QCoreApplication.translate("DialogImportData", "The selected XTF file does not have information according to the LADM-COL model to import.")
            self.txtStdout.setText(error_msg)
            self.show_message(error_msg, Qgis.Warning)
            self.import_models_list_view.setFocus()
            return

        # Get list of models present in the XTF file, in the DB and in the list of required models (by the plugin)
        ili_models = set([ili_model for ili_model in self.get_ili_models()])

        supported_models_in_ili = set([m.full_name() for m in self.__ladmcol_models.supported_models()]).intersection(ili_models)

        if not supported_models_in_ili:
            self._running_tool = False
            error_msg = QCoreApplication.translate("DialogImportData",
                                                   "The selected XTF file does not have data from any LADM-COL model supported by the LADM-COL Assistant. " \
                                                   "Therefore, you cannot import it! These are the models supported:\n\n * {}").format(" \n * ".join([m.full_alias() for m in self.__ladmcol_models.supported_models()]))
            self.txtStdout.setText(error_msg)
            self.show_message(error_msg, Qgis.Warning)
            self.import_models_list_view.setFocus()
            return

        db_models = set(self.db.get_models())
        suggested_models = sorted(ili_models.difference(db_models))

        if not ili_models.issubset(db_models):
            self._running_tool = False
            error_msg = QCoreApplication.translate("DialogImportData",
                                                   "IMPORT ERROR: The XTF file to import does not have the same models as the target database schema. " \
                                                   "Please create a schema that also includes the following missing modules:\n\n * {}").format(
                " \n * ".join(suggested_models))
            self.txtStdout.clear()
            self.txtStdout.setTextColor(QColor('#000000'))
            self.txtStdout.setText(error_msg)
            self.show_message(error_msg, Qgis.Warning)
            self.xtf_file_line_edit.setFocus()

            # button is removed to define order in GUI
            for button in self.buttonBox.buttons():
                if button.text() == self.BUTTON_NAME_IMPORT_DATA:
                    self.buttonBox.removeButton(button)

            # Check if button was previously added
            self.remove_create_structure_button()

            if self.link_to_import_schema:
                self.buttonBox.addButton(self.BUTTON_NAME_GO_TO_CREATE_STRUCTURE,
                                         QDialogButtonBox.AcceptRole).setStyleSheet("color: #aa2222;")
            self.buttonBox.addButton(self.BUTTON_NAME_IMPORT_DATA,
                                     QDialogButtonBox.AcceptRole)

            return

        with OverrideCursor(Qt.WaitCursor):
            self.progress_bar.show()

            self.disable()
            self.txtStdout.setTextColor(QColor('#000000'))
            self.txtStdout.clear()

            dataImporter = iliimporter.Importer(dataImport=True)

            db_factory = self._dbs_supported.get_db_factory(self.db.engine)

            dataImporter.tool = db_factory.get_model_baker_db_ili_mode()
            dataImporter.configuration = configuration

            self.save_configuration(configuration)

            dataImporter.stdout.connect(self.print_info)
            dataImporter.stderr.connect(self.on_stderr)
            dataImporter.process_started.connect(self.on_process_started)
            dataImporter.process_finished.connect(self.on_process_finished)

            self.progress_bar.setValue(25)

            try:
                if dataImporter.run() != iliimporter.Importer.SUCCESS:
                    self._running_tool = False
                    self.show_message(QCoreApplication.translate("DialogImportData", "An error occurred when importing the data. For more information see the log..."), Qgis.Warning)
                    return
            except JavaNotFoundError:
                self._running_tool = False
                error_msg_java = QCoreApplication.translate("DialogImportData", "Java {} could not be found. You can configure the JAVA_HOME environment variable manually, restart QGIS and try again.").format(JAVA_REQUIRED_VERSION)
                self.txtStdout.setTextColor(QColor('#000000'))
                self.txtStdout.clear()
                self.txtStdout.setText(error_msg_java)
                self.show_message(error_msg_java, Qgis.Warning)
                return

            self._running_tool = False
            self.buttonBox.clear()
            self.buttonBox.setEnabled(True)
            self.buttonBox.addButton(QDialogButtonBox.Close)
            self.progress_bar.setValue(100)
            self.show_message(QCoreApplication.translate("DialogImportData", "Import of the data was successfully completed"), Qgis.Success)

    def download_java_complete(self):
        self.accepted()

    def download_java_progress_change(self, progress):
        self.progress_bar.setValue(progress/2)
        if (progress % 20) == 0:
            self.txtStdout.append('...')

    def remove_create_structure_button(self):
        for button in self.buttonBox.buttons():
            if button.text() == self.BUTTON_NAME_GO_TO_CREATE_STRUCTURE:
                self.buttonBox.removeButton(button)

    def save_configuration(self, configuration):
        settings = QSettings()
        settings.setValue('Asistente-LADM-COL/QgisModelBaker/ili2pg/xtffile_import', configuration.xtffile)
        settings.setValue('Asistente-LADM-COL/QgisModelBaker/show_log', not self.log_config.isCollapsed())

    def restore_configuration(self):
        settings = QSettings()
        self.xtf_file_line_edit.setText(settings.value('Asistente-LADM-COL/QgisModelBaker/ili2pg/xtffile_import'))

        # Show log
        value_show_log = settings.value('Asistente-LADM-COL/QgisModelBaker/show_log', False, type=bool)
        self.log_config.setCollapsed(not value_show_log)

        # set model repository
        # if there is no option  by default use online model repository
        self.use_local_models = settings.value('Asistente-LADM-COL/models/custom_model_directories_is_checked', DEFAULT_USE_CUSTOM_MODELS, type=bool)
        if self.use_local_models:
            self.custom_model_directories = settings.value('Asistente-LADM-COL/models/custom_models', DEFAULT_MODELS_DIR)

    def update_configuration(self):
        """
        Get the configuration that is updated with the user configuration changes on the dialog.
        :return: Configuration
        """
        db_factory = self._dbs_supported.get_db_factory(self.db.engine)

        configuration = ImportDataConfiguration()
        db_factory.set_ili2db_configuration_params(self.db.dict_conn_params, configuration)

        configuration.xtffile = self.xtf_file_line_edit.text().strip()
        configuration.delete_data = False

        configuration.srs_auth = QSettings().value('Asistente-LADM-COL/QgisModelBaker/srs_auth', DEFAULT_SRS_AUTH, str)
        configuration.srs_code = QSettings().value('Asistente-LADM-COL/QgisModelBaker/srs_code', int(DEFAULT_SRS_CODE), int)
        configuration.inheritance = ILI2DBNames.DEFAULT_INHERITANCE
        configuration.create_basket_col = ILI2DBNames.CREATE_BASKET_COL
        configuration.create_import_tid = ILI2DBNames.CREATE_IMPORT_TID
        configuration.stroke_arcs = ILI2DBNames.STROKE_ARCS
        configuration.with_importtid = True

        full_java_exe_path = JavaDependency.get_full_java_exe_path()
        if full_java_exe_path:
            self.base_configuration.java_path = full_java_exe_path

        # User could have changed the default values
        self.use_local_models = QSettings().value('Asistente-LADM-COL/models/custom_model_directories_is_checked', DEFAULT_USE_CUSTOM_MODELS, type=bool)
        self.custom_model_directories = QSettings().value('Asistente-LADM-COL/models/custom_models', DEFAULT_MODELS_DIR)

        # Check custom model directories
        if self.use_local_models:
            if not self.custom_model_directories:
                self.base_configuration.custom_model_directories_enabled = False
            else:
                self.base_configuration.custom_model_directories = self.custom_model_directories
                self.base_configuration.custom_model_directories_enabled = True

        configuration.base_configuration = self.base_configuration
        if self.get_ili_models():
            configuration.ilimodels = ';'.join(self.get_ili_models())

        configuration.disable_validation = not QSettings().value('Asistente-LADM-COL/models/validate_data_importing_exporting', True, bool)

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

    def clear_messages(self):
        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.txtStdout.clear()  # Clear previous log messages
        self.progress_bar.setValue(0)  # Initialize progress bar

    def show_help(self):
        show_plugin_help("import_data")

    def disable(self):
        self.source_config.setEnabled(False)
        self.target_config.setEnabled(False)
        self.buttonBox.setEnabled(False)

    def enable(self):
        self.source_config.setEnabled(True)
        self.target_config.setEnabled(True)
        self.buttonBox.setEnabled(True)

    def show_message(self, message, level):
        if level == Qgis.Warning:
            self.enable()

        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.bar.pushMessage("Asistente LADM-COL", message, level, duration=0)
