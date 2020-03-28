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

from QgisModelBaker.libili2db import iliexporter
from QgisModelBaker.libili2db.ili2dbconfig import (ExportConfiguration,
                                                   BaseConfiguration)
from QgisModelBaker.libili2db.ili2dbutils import color_log_text
from QgisModelBaker.libili2db.ilicache import IliCache
from QgisModelBaker.libili2db.iliimporter import JavaNotFoundError
from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication,
                              QSettings,
                              pyqtSignal)
from qgis.PyQt.QtGui import (QColor,
                             QValidator,
                             QStandardItemModel,
                             QStandardItem)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QSizePolicy,
                                 QMessageBox,
                                 QDialogButtonBox)
from qgis.core import Qgis
from qgis.gui import QgsGui
from qgis.gui import QgsMessageBar

from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.config.general_config import (COLLECTED_DB_SOURCE,
                                                      JAVA_REQUIRED_VERSION,
                                                      SETTINGS_CONNECTION_TAB_INDEX,
                                                      SETTINGS_MODELS_TAB_INDEX,
                                                      DEFAULT_USE_CUSTOM_MODELS,
                                                      DEFAULT_MODELS_DIR)
from asistente_ladm_col.gui.dialogs.dlg_settings import SettingsDialog
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.java_utils import JavaUtils
from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.utils import show_plugin_help
from asistente_ladm_col.utils.qt_utils import (Validators,
                                               FileValidator,
                                               make_save_file_selector,
                                               OverrideCursor)

from ...resources_rc import * # Necessary to show icons
from asistente_ladm_col.config.config_db_supported import ConfigDBsSupported
DIALOG_UI = get_ui_class('qgis_model_baker/dlg_export_data.ui')
from asistente_ladm_col.config.enums import EnumDbActionType


class DialogExportData(QDialog, DIALOG_UI):
    on_result = pyqtSignal(bool)  # whether the tool was run successfully or not

    ValidExtensions = ['xtf', 'itf', 'gml', 'xml']
    current_row_schema = 0

    def __init__(self, iface, qgis_utils, conn_manager, context):
        QDialog.__init__(self)
        self.setupUi(self)

        QgsGui.instance().enableAutoGeometryRestore(self)
        self.iface = iface
        self.conn_manager = conn_manager
        self.db_source = context.get_db_sources()[0]
        self.db = self.conn_manager.get_db_connector_from_source(self.db_source)
        self.qgis_utils = qgis_utils
        self.logger = Logger()

        self.java_utils = JavaUtils()
        self.java_utils.download_java_completed.connect(self.download_java_complete)
        self.java_utils.download_java_progress_changed.connect(self.download_java_progress_change)

        self.base_configuration = BaseConfiguration()
        self.ilicache = IliCache(self.base_configuration)
        self.ilicache.refresh()

        self._dbs_supported = ConfigDBsSupported()
        self._running_tool = False

        # There may be 1 case where we need to emit a db_connection_changed from the Export Data dialog:
        #   1) Connection Settings was opened and the DB conn was changed.
        self._db_was_changed = False  # To postpone calling refresh gui until we close this dialog instead of settings

        # Similarly, we could call a refresh on layers and relations cache in 1 case:
        #   1) If the ED dialog was called for the COLLECTED source: opening Connection Settings and changing the DB
        #      connection.
        self._schedule_layers_and_relations_refresh = False

        # We need bar definition above calling clear_messages
        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

        self.xtf_file_browse_button.clicked.connect(
            make_save_file_selector(self.xtf_file_line_edit, title=QCoreApplication.translate("DialogExportData", "Save in XTF Transfer File"),
                                    file_filter=QCoreApplication.translate("DialogExportData", "XTF Transfer File (*.xtf);;Interlis 1 Transfer File (*.itf);;XML (*.xml);;GML (*.gml)"), extension='.xtf', extensions=['.' + ext for ext in self.ValidExtensions]))
        self.xtf_file_browse_button.clicked.connect(self.xtf_browser_opened_to_true)
        self.xtf_browser_was_opened = False

        self.validators = Validators()
        fileValidator = FileValidator(pattern=['*.' + ext for ext in self.ValidExtensions], allow_non_existing=True)
        self.xtf_file_line_edit.setPlaceholderText(QCoreApplication.translate("DialogExportData", "[Name of the XTF to be created]"))
        self.xtf_file_line_edit.setValidator(fileValidator)
        self.xtf_file_line_edit.textChanged.connect(self.validators.validate_line_edits)
        self.xtf_file_line_edit.textChanged.connect(self.xtf_browser_opened_to_false)
        self.xtf_file_line_edit.textChanged.emit(self.xtf_file_line_edit.text())

        self.connection_setting_button.clicked.connect(self.show_settings)

        self.connection_setting_button.setText(QCoreApplication.translate("DialogExportData", "Connection Settings"))

        # LOG
        self.log_config.setTitle(QCoreApplication.translate("DialogExportData", "Show log"))
        self.log_config.setFlat(True)

        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.clear()
        self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self._accept_button = self.buttonBox.addButton(QCoreApplication.translate("DialogExportData", "Export data"), QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(QDialogButtonBox.Help)
        self.buttonBox.helpRequested.connect(self.show_help)

        self.update_connection_info()
        self.update_model_names()
        self.restore_configuration()

    def update_connection_info(self):
        db_description = self.db.get_description_conn_string()
        if db_description:
            self.db_connect_label.setText(db_description)
            self.db_connect_label.setToolTip(self.db.get_display_conn_string())
            self._accept_button.setEnabled(True)
        else:
            self.db_connect_label.setText(
                QCoreApplication.translate("DialogExportData", "The database is not defined!"))
            self.db_connect_label.setToolTip('')
            self._accept_button.setEnabled(False)

    def update_model_names(self):
        self.export_models_qmodel = QStandardItemModel()

        model_names = self.db.get_models()

        if model_names:
            for model_name in model_names:
                if model_name not in LADMNames.DEFAULT_HIDDEN_MODELS:
                    item = QStandardItem(model_name)
                    item.setCheckable(False)
                    item.setEditable(False)
                    self.export_models_qmodel.appendRow(item)

        self.export_models_list_view.setModel(self.export_models_qmodel)

    def reject(self):
        if self._running_tool:
            QMessageBox.information(self,
                                    QCoreApplication.translate("DialogExportData", "Warning"),
                                    QCoreApplication.translate("DialogExportData", "The Export Data tool is still running. Please wait until it finishes."))
        else:
            self.close_dialog()

    def close_dialog(self):
        """
        We use this method to be safe when emitting the db_connection_changed, otherwise we could trigger slots that
        unload the plugin, destroying dialogs and thus, leading to crashes.
        """
        if self._schedule_layers_and_relations_refresh:
            self.conn_manager.db_connection_changed.connect(self.qgis_utils.cache_layers_and_relations)

        if self._db_was_changed:
            # If the db was changed, it implies it complies with ladm_col, hence the second parameter
            self.conn_manager.db_connection_changed.emit(self.db, True, self.db_source)

        if self._schedule_layers_and_relations_refresh:
            self.conn_manager.db_connection_changed.disconnect(self.qgis_utils.cache_layers_and_relations)

        self.logger.info(__name__, "Dialog closed.")
        self.done(QDialog.Accepted)

    def get_ili_models(self):
        ili_models = list()
        for index in range(self.export_models_qmodel.rowCount()):
            item = self.export_models_qmodel.item(index)
            ili_models.append(item.text())
        return ili_models

    def show_settings(self):
        # We only need those tabs related to Model Baker/ili2db operations
        dlg = SettingsDialog(qgis_utils=self.qgis_utils, conn_manager=self.conn_manager)
        dlg.set_db_source(self.db_source)
        dlg.set_tab_pages_list([SETTINGS_CONNECTION_TAB_INDEX, SETTINGS_MODELS_TAB_INDEX])

        # Connect signals (DBUtils, QgisUtils)
        dlg.db_connection_changed.connect(self.db_connection_changed)
        if self.db_source == COLLECTED_DB_SOURCE:
            self._schedule_layers_and_relations_refresh = True

        dlg.set_action_type(EnumDbActionType.EXPORT)

        if dlg.exec_():
            self.db = dlg.get_db_connection()
            self.update_model_names()
            self.update_connection_info()

    def db_connection_changed(self, db, ladm_col_db, db_source):
        self._db_was_changed = True
        self.clear_messages()

    def accepted(self):
        self._running_tool = True
        self.txtStdout.clear()
        self.progress_bar.setValue(0)
        self.bar.clearWidgets()

        java_home_set = self.java_utils.set_java_home()
        if not java_home_set:
            message_java = QCoreApplication.translate("DialogExportData", """Configuring Java {}...""").format(JAVA_REQUIRED_VERSION)
            self.txtStdout.setTextColor(QColor('#000000'))
            self.txtStdout.clear()
            self.txtStdout.setText(message_java)
            self.java_utils.get_java_on_demand()
            self.disable()
            return

        configuration = self.update_configuration()

        if configuration.disable_validation:  # If data validation at export is disabled, we ask for confirmation
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Question)
            self.msg.setText(QCoreApplication.translate("DialogExportData",
                                                        "Are you sure you want to export your data without validation?"))
            self.msg.setWindowTitle(QCoreApplication.translate("DialogExportData", "Export XTF without validation?"))
            self.msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            res = self.msg.exec_()
            if res == QMessageBox.No:
                self._running_tool = False
                return

        if not self.xtf_file_line_edit.validator().validate(configuration.xtffile, 0)[0] == QValidator.Acceptable:
            self._running_tool = False
            message_error = QCoreApplication.translate("DialogExportData", "Please set a valid XTF file before exporting data.")
            self.txtStdout.setText(message_error)
            self.show_message(message_error, Qgis.Warning)
            self.xtf_file_line_edit.setFocus()
            return

        if not self.get_ili_models():
            self._running_tool = False
            message_error = QCoreApplication.translate("DialogExportData", "Please set a valid schema to export. This schema does not have information to export.")
            self.txtStdout.setText(message_error)
            self.show_message(message_error, Qgis.Warning)
            self.export_models_list_view.setFocus()
            return

        if not configuration.iliexportmodels:
            self._running_tool = False
            message_error = QCoreApplication.translate("DialogExportData", "Please set a model before exporting data.")
            self.txtStdout.setText(message_error)
            self.show_message(message_error, Qgis.Warning)
            self.export_models_list_view.setFocus()
            return

        # If xtf browser was opened and the file exists, the user already chose
        # to overwrite the file
        if os.path.isfile(self.xtf_file_line_edit.text().strip()) and not self.xtf_browser_was_opened:
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setText(QCoreApplication.translate("DialogExportData", "{filename} already exists.\nDo you want to replace it?").format(filename=os.path.basename(self.xtf_file_line_edit.text().strip())))
            self.msg.setWindowTitle(QCoreApplication.translate("DialogExportData", "Save in XTF Transfer File"))
            self.msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box = self.msg.exec_()
            if msg_box == QMessageBox.No:
                self._running_tool = False
                return

        with OverrideCursor(Qt.WaitCursor):
            self.progress_bar.show()

            self.disable()
            self.txtStdout.setTextColor(QColor('#000000'))
            self.txtStdout.clear()

            exporter = iliexporter.Exporter()

            db_factory = self._dbs_supported.get_db_factory(self.db.engine)

            exporter.tool = db_factory.get_model_baker_db_ili_mode()
            exporter.configuration = configuration

            self.save_configuration(configuration)

            exporter.stdout.connect(self.print_info)
            exporter.stderr.connect(self.on_stderr)
            exporter.process_started.connect(self.on_process_started)
            exporter.process_finished.connect(self.on_process_finished)

            self.progress_bar.setValue(25)

            try:
                if exporter.run() != iliexporter.Exporter.SUCCESS:
                    self._running_tool = False
                    self.show_message(QCoreApplication.translate("DialogExportData", "An error occurred when exporting the data. For more information see the log..."), Qgis.Warning)
                    self.on_result.emit(False)  # Inform other classes that the execution was not successful
                    return
            except JavaNotFoundError:
                self._running_tool = False
                message_error_java = QCoreApplication.translate("DialogExportData", "Java {} could not be found. You can configure the JAVA_HOME environment variable manually, restart QGIS and try again.").format(JAVA_REQUIRED_VERSION)
                self.txtStdout.setTextColor(QColor('#000000'))
                self.txtStdout.clear()
                self.txtStdout.setText(message_error_java)
                self.show_message(message_error_java, Qgis.Warning)
                return

            self._running_tool = False
            self.buttonBox.clear()
            self.buttonBox.setEnabled(True)
            self.buttonBox.addButton(QDialogButtonBox.Close)
            self.progress_bar.setValue(100)
            self.show_message(QCoreApplication.translate("DialogExportData", "Export of the data was successfully completed.") , Qgis.Success)
            self.on_result.emit(True)  # Inform other classes that the execution was successful

    def download_java_complete(self):
        self.accepted()

    def download_java_progress_change(self, progress):
        self.progress_bar.setValue(progress/2)
        if (progress % 20) == 0:
            self.txtStdout.append('...')

    def save_configuration(self, configuration):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/QgisModelBaker/ili2pg/xtffile_export', configuration.xtffile)
        settings.setValue('Asistente-LADM_COL/QgisModelBaker/show_log', not self.log_config.isCollapsed())

    def restore_configuration(self):
        settings = QSettings()
        self.xtf_file_line_edit.setText(settings.value('Asistente-LADM_COL/QgisModelBaker/ili2pg/xtffile_export'))

        # Show log
        value_show_log = settings.value('Asistente-LADM_COL/QgisModelBaker/show_log', False, type=bool)
        self.log_config.setCollapsed(not value_show_log)

        # set model repository
        # if there is no option by default use online model repository
        custom_model_is_checked =  settings.value('Asistente-LADM_COL/models/custom_model_directories_is_checked', DEFAULT_USE_CUSTOM_MODELS, type=bool)
        if custom_model_is_checked:
            self.custom_model_directories = settings.value('Asistente-LADM_COL/models/custom_models', DEFAULT_MODELS_DIR)

    def update_configuration(self):
        """
        Get the configuration that is updated with the user configuration changes on the dialog.
        :return: Configuration
        """
        db_factory = self._dbs_supported.get_db_factory(self.db.engine)

        configuration = ExportConfiguration()
        db_factory.set_ili2db_configuration_params(self.db.dict_conn_params, configuration)

        configuration.xtffile = self.xtf_file_line_edit.text().strip()
        full_java_exe_path = JavaUtils.get_full_java_exe_path()
        if full_java_exe_path:
            self.base_configuration.java_path = full_java_exe_path

        # User could have changed the default values
        self.use_local_models = QSettings().value('Asistente-LADM_COL/models/custom_model_directories_is_checked', DEFAULT_USE_CUSTOM_MODELS, type=bool)
        self.custom_model_directories = QSettings().value('Asistente-LADM_COL/models/custom_models', DEFAULT_MODELS_DIR)

        # Check custom model directories
        if self.use_local_models:
            if not self.custom_model_directories:
                self.base_configuration.custom_model_directories_enabled = False
            else:
                self.base_configuration.custom_model_directories = self.custom_model_directories
                self.base_configuration.custom_model_directories_enabled = True

        configuration.base_configuration = self.base_configuration
        if self.get_ili_models():
            configuration.iliexportmodels = ';'.join(self.get_ili_models())
            configuration.ilimodels = ';'.join(self.get_ili_models())

        configuration.disable_validation = not QSettings().value('Asistente-LADM_COL/models/validate_data_importing_exporting', True, bool)

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
        self.txtStdout.append(QCoreApplication.translate("DialogExportData", "Finished ({})").format(exit_code))
        if result == iliexporter.Exporter.SUCCESS:
            self.buttonBox.clear()
            self.buttonBox.setEnabled(True)
            self.buttonBox.addButton(QDialogButtonBox.Close)
        else:
            self.enable()

            # Open log
            if self.log_config.isCollapsed():
                self.log_config.setCollapsed(False)

    def advance_progress_bar_by_text(self, text):
        if text.strip() == 'Info: compile models...':
            self.progress_bar.setValue(50)
            QCoreApplication.processEvents()
        elif text.strip() == 'Info: process data...':
            self.progress_bar.setValue(55)
            QCoreApplication.processEvents()
        elif text.strip() == 'Info: first validation pass...':
            self.progress_bar.setValue(70)
            QCoreApplication.processEvents()
        elif text.strip() == 'Info: second validation pass...':
            self.progress_bar.setValue(85)
            QCoreApplication.processEvents()

    def clear_messages(self):
        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.txtStdout.clear()  # Clear previous log messages
        self.progress_bar.setValue(0)  # Initialize progress bar

    def show_help(self):
        show_plugin_help("export_data")

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
        self.bar.pushMessage("Asistente LADM_COL", message, level, duration=0)

    def xtf_browser_opened_to_true(self):
        """
        Slot. Sets a flag to true to eventually avoid asking a user whether to overwrite a file.
        """
        self.xtf_browser_was_opened = True

    def xtf_browser_opened_to_false(self):
        """
        Slot. Sets a flag to false to eventually ask a user whether to overwrite a file.
        """
        self.xtf_browser_was_opened = False
        self.clear_messages()
