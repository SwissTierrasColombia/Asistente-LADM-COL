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
from asistente_ladm_col.core.ili2db import Ili2DB
from asistente_ladm_col.lib.ili.ili2dbutils import color_log_text

from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication,
                              QSettings,
                              pyqtSignal)
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import (QDialog,
                                 QMessageBox,
                                 QListWidgetItem,
                                 QSizePolicy,
                                 QDialogButtonBox)
from qgis.core import Qgis
from qgis.gui import QgsMessageBar

from asistente_ladm_col.config.general_config import (DEFAULT_SRS_AUTH,
                                                      DEFAULT_SRS_CODE,
                                                      COLLECTED_DB_SOURCE,
                                                      SETTINGS_CONNECTION_TAB_INDEX,
                                                      JAVA_REQUIRED_VERSION,
                                                      SETTINGS_MODELS_TAB_INDEX,
                                                      DEFAULT_SRS_AUTHID)
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.keys.ili2db_keys import *
from asistente_ladm_col.gui.dialogs.dlg_settings import SettingsDialog
from asistente_ladm_col.lib.model_registry import LADMColModelRegistry
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.crs_utils import get_crs_from_auth_and_code, get_crs_authid
from asistente_ladm_col.lib.dependency.java_dependency import JavaDependency
from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.utils import show_plugin_help
from asistente_ladm_col.utils.qt_utils import Validators

from asistente_ladm_col.config.config_db_supported import ConfigDBsSupported
from asistente_ladm_col.config.enums import EnumDbActionType

DIALOG_UI = get_ui_class('qgis_model_baker/dlg_import_schema.ui')


class DialogImportSchema(QDialog, DIALOG_UI):
    open_dlg_import_data = pyqtSignal(dict)  # dict with key-value params
    on_result = pyqtSignal(bool)  # whether the tool was run successfully or not

    BUTTON_NAME_CREATE_STRUCTURE = QCoreApplication.translate("DialogImportSchema", "Create LADM-COL structure")
    BUTTON_NAME_GO_TO_IMPORT_DATA =  QCoreApplication.translate("DialogImportData", "Go to Import Data...")

    def __init__(self, iface, conn_manager, context, selected_models=list(), link_to_import_data=True, parent=None):
        QDialog.__init__(self, parent)
        self.iface = iface
        self.conn_manager = conn_manager
        self.selected_models = selected_models
        self.link_to_import_data = link_to_import_data
        self.logger = Logger()
        self.app = AppInterface()
        self.__ladmcol_models = LADMColModelRegistry()

        self.java_dependency = JavaDependency()
        self.java_dependency.download_dependency_completed.connect(self.download_java_complete)
        self.java_dependency.download_dependency_progress_changed.connect(self.download_java_progress_change)

        self.db_source = context.get_db_sources()[0]
        self.db = self.conn_manager.get_db_connector_from_source(self.db_source)

        self._dbs_supported = ConfigDBsSupported()
        self._running_tool = False

        # There may be two cases where we need to emit a db_connection_changed from the Schema Import dialog:
        #   1) Connection Settings was opened and the DB conn was changed.
        #   2) Connection Settings was never opened but the Schema Import ran successfully, in a way that new models may
        #      convert a db/schema LADM-COL compliant.
        self._db_was_changed = False  # To postpone calling refresh gui until we close this dialog instead of settings

        # Similarly, we could call a refresh on layers and relations cache in two cases:
        #   1) If the SI dialog was called for the COLLECTED source: opening Connection Settings and changing the DB
        #      connection.
        #   2) Not opening the Connection Settings, but running a successful Schema Import on the COLLECTED DB, which
        #      invalidates the cache as models change.
        self._schedule_layers_and_relations_refresh = False

        self.setupUi(self)

        self.validators = Validators()

        self.update_import_models()
        self.previous_item = QListWidgetItem()

        self.connection_setting_button.clicked.connect(self.show_settings)
        self.connection_setting_button.setText(QCoreApplication.translate("DialogImportSchema", "Connection Settings"))

        # CRS Setting
        self.srs_auth = DEFAULT_SRS_AUTH
        self.srs_code = DEFAULT_SRS_CODE
        self.crsSelector.crsChanged.connect(self.crs_changed)

        # LOG
        self.log_config.setTitle(QCoreApplication.translate("DialogImportSchema", "Show log"))

        self.buttonBox.accepted.disconnect()
        self.buttonBox.clicked.connect(self.accepted_import_schema)
        self.buttonBox.clear()
        self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self._accept_button = self.buttonBox.addButton(self.BUTTON_NAME_CREATE_STRUCTURE, QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(QDialogButtonBox.Help)
        self.buttonBox.helpRequested.connect(self.show_help)

        self.import_models_list_widget.setDisabled(bool(selected_models))  # If we got models from params, disable panel

        self.update_connection_info()
        self.restore_configuration()

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

    def accepted_import_schema(self, button):
        if self.buttonBox.buttonRole(button) == QDialogButtonBox.AcceptRole:
            if button.text() == self.BUTTON_NAME_CREATE_STRUCTURE:
                self.accepted()
            elif button.text() == self.BUTTON_NAME_GO_TO_IMPORT_DATA:
                self.close()  # Close import schema dialog and open import open dialog
                self.open_dlg_import_data.emit({"db_source": self.db_source})

    def reject(self):
        if self._running_tool:
            QMessageBox.information(self,
                                    QCoreApplication.translate("DialogImportSchema", "Warning"),
                                    QCoreApplication.translate("DialogImportSchema", "The Import Schema tool is still running. Please wait until it finishes."))
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
            self.conn_manager.db_connection_changed.emit(self.db, self.db.test_connection()[0], self.db_source)

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
            self.db_connect_label.setText(QCoreApplication.translate("DialogImportSchema", "The database is not defined!"))
            self.db_connect_label.setToolTip('')
            self._accept_button.setEnabled(False)

    def update_import_models(self):
        for model in self.__ladmcol_models.supported_models():
            if not model.hidden():
                item = QListWidgetItem(model.full_alias())
                item.setData(Qt.UserRole, model.full_name())
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                if self.selected_models:  # From parameters
                    item.setCheckState(Qt.Checked if model.full_name() in self.selected_models else Qt.Unchecked)
                else:  # By default
                    item.setCheckState(Qt.Checked if model.checked() else Qt.Unchecked)
                self.import_models_list_widget.addItem(item)

        self.import_models_list_widget.itemClicked.connect(self.on_item_clicked_import_model)
        self.import_models_list_widget.itemChanged.connect(self.on_itemchanged_import_model)

    def on_item_clicked_import_model(self, item):
        # disconnect signal to do changes in the items
        self.import_models_list_widget.itemChanged.disconnect(self.on_itemchanged_import_model)
        if self.previous_item.text() != item.text():
            item.setCheckState(Qt.Unchecked if item.checkState() == Qt.Checked else Qt.Checked)

        # connect signal to check when the items change
        self.import_models_list_widget.itemChanged.connect(self.on_itemchanged_import_model)
        self.previous_item = item

    def on_itemchanged_import_model(self, item):
        if self.previous_item.text() != item.text():
            item.setSelected(True)
        self.previous_item = item

    def get_checked_models(self):
        checked_models = list()
        for index in range(self.import_models_list_widget.count()):
            item = self.import_models_list_widget.item(index)
            if item.checkState() == Qt.Checked:
                checked_models.append(item.data(Qt.UserRole))

        return checked_models

    def show_settings(self):
        # We only need those tabs related to Model Baker/ili2db operations
        dlg = SettingsDialog(self.conn_manager, parent=self)
        dlg.setWindowTitle(QCoreApplication.translate("DialogImportSchema", "Target DB Connection Settings"))
        dlg.show_tip(QCoreApplication.translate("DialogImportSchema", "Configure where do you want the LADM-COL structure to be created."))
        dlg.set_db_source(self.db_source)
        dlg.set_tab_pages_list([SETTINGS_CONNECTION_TAB_INDEX, SETTINGS_MODELS_TAB_INDEX])

        # Connect signals (DBUtils, Core)
        dlg.db_connection_changed.connect(self.db_connection_changed)
        if self.db_source == COLLECTED_DB_SOURCE:
            self._schedule_layers_and_relations_refresh = True

        dlg.set_action_type(EnumDbActionType.SCHEMA_IMPORT)

        if dlg.exec_():
            self.db = dlg.get_db_connection()
            self.update_connection_info()

    def db_connection_changed(self, db, ladm_col_db, db_source):
        # We dismiss parameters here, after all, we already have the db, and the ladm_col_db may change from this moment
        # until we close the import schema dialog
        self._db_was_changed = True
        self.clear_messages()  # Clean GUI messages if db connection changed

    def accepted(self):
        self._running_tool = True
        self.txtStdout.clear()
        self.progress_bar.setValue(0)
        self.bar.clearWidgets()

        java_home_set = self.java_dependency.set_java_home()
        if not java_home_set:
            message_java = QCoreApplication.translate("DialogImportSchema", """Configuring Java {}...""").format(JAVA_REQUIRED_VERSION)
            self.txtStdout.setTextColor(QColor('#000000'))
            self.txtStdout.clear()
            self.txtStdout.setText(message_java)
            self.java_dependency.get_java_on_demand()
            self.disable()
            return

        if not self.get_checked_models():
            self._running_tool = False
            message_error = QCoreApplication.translate("DialogImportSchema", "You should select a valid model(s) before creating the LADM-COL structure.")
            self.txtStdout.setText(message_error)
            self.show_message(message_error, Qgis.Warning)
            self.import_models_list_widget.setFocus()
            return

        self.save_configuration()

        self.progress_bar.show()
        self.disable()
        self.txtStdout.setTextColor(QColor('#000000'))
        self.txtStdout.clear()

        ili2db = Ili2DB()

        self._connect_ili2db_signals(ili2db)

        models = self.get_checked_models()

        configuration = ili2db.get_import_schema_configuration(self.db, models)
        configuration = self.apply_role_model_configuration(configuration)

        res, msg = ili2db.import_schema(self.db, configuration)

        self._disconnect_ili2db_signals(ili2db)

        self._running_tool = False

        if res:
            self.buttonBox.clear()
            if self.link_to_import_data:
                self.buttonBox.addButton(self.BUTTON_NAME_GO_TO_IMPORT_DATA,
                                         QDialogButtonBox.AcceptRole).setStyleSheet("color: #007208;")
            self.buttonBox.setEnabled(True)
            self.buttonBox.addButton(QDialogButtonBox.Close)
            self.progress_bar.setValue(100)
            self.print_info(QCoreApplication.translate("DialogImportSchema", "\nDone!"), '#004905')
            self._db_was_changed = True  # Schema could become LADM compliant after a schema import

            if self.db_source == COLLECTED_DB_SOURCE:
                self.logger.info(__name__, "Schedule a call to refresh db relations cache since a Schema Import was run on the current 'collected' DB.")
                self._schedule_layers_and_relations_refresh = True

        message_type = Qgis.Success if res else Qgis.Warning
        self.show_message(msg, message_type)
        # Inform other classes whether the execution was successful or not
        self.on_result.emit(res)

    def download_java_complete(self):
        self.accepted()

    def download_java_progress_change(self, progress):
        self.progress_bar.setValue(progress/2)
        if (progress % 20) == 0:
            self.txtStdout.append('...')

    def save_configuration(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM-COL/QgisModelBaker/show_log', not self.log_config.isCollapsed())
        settings.setValue('Asistente-LADM-COL/QgisModelBaker/srs_auth', self.srs_auth)
        settings.setValue('Asistente-LADM-COL/QgisModelBaker/srs_code', self.srs_code)

    def restore_configuration(self):
        settings = QSettings()

        # CRS
        srs_auth = settings.value('Asistente-LADM-COL/QgisModelBaker/srs_auth', DEFAULT_SRS_AUTH, str)
        srs_code = settings.value('Asistente-LADM-COL/QgisModelBaker/srs_code', int(DEFAULT_SRS_CODE), int)
        self.crsSelector.setCrs(get_crs_from_auth_and_code(srs_auth, srs_code))
        self.crs_changed()

        # Show log
        value_show_log = settings.value('Asistente-LADM-COL/QgisModelBaker/show_log', False, type=bool)
        self.log_config.setCollapsed(not value_show_log)

        # set model repository
        # if there is no option  by default use online model repository
        self.use_local_models = self.app.settings.custom_models
        if self.use_local_models:
            self.custom_model_directories = self.app.settings.custom_model_dirs

    def crs_changed(self):
        self.srs_auth, self.srs_code = get_crs_authid(self.crsSelector.crs()).split(":")
        if self.srs_code != DEFAULT_SRS_CODE or self.srs_auth != DEFAULT_SRS_AUTH:
            self.crs_label.setStyleSheet('color: orange')
            self.crs_label.setToolTip(QCoreApplication.translate("DialogImportSchema", "The {} (Colombian National Origin) is recommended,<br>since official models were created for that projection.").format(DEFAULT_SRS_AUTHID))
        else:
            self.crs_label.setStyleSheet('')
            self.crs_label.setToolTip(QCoreApplication.translate("DialogImportSchema", "Coordinate Reference System"))

    def apply_role_model_configuration(self, configuration):
        """
        Applies the configuration that the active role has set over checked models.

        Important:
        Note that this works better if the checked models are limited to one (e.g. Field Data Capture) or limited to
        a group of related models (e.g., the 3 supplies models). When the checked models are heterogeneous, results
        start to be unpredictable, as the configuration for a single model may affect the others.

        :param configuration: SchemaImportConfiguration object
        :return: configuration object updated
        """
        for checked_model in self.get_checked_models():
            model = self.__ladmcol_models.model_by_full_name(checked_model)
            params = model.get_ili2db_params()
            if ILI2DB_SCHEMAIMPORT in params:
                for param in params[ILI2DB_SCHEMAIMPORT]:  # List of tuples
                    if param[0] == ILI2DB_CREATE_BASKET_COL_KEY:  # param: (option, value)
                        configuration.create_basket_col = True
                        self.logger.debug(__name__, "Schema Import createBasketCol enabled (model '{}')! (taken from role config)".format(model.id()))

        return configuration

    def print_info(self, text, text_color='#000000', clear=False):
        self.txtStdout.setTextColor(QColor(text_color))
        self.txtStdout.append(text)
        QCoreApplication.processEvents()

    def on_stderr(self, text):
        color_log_text(text, self.txtStdout)
        self.advance_progress_bar_by_text(text)

    def on_process_started(self, command):
        self.txtStdout.append(command)
        QCoreApplication.processEvents()

    def on_process_finished(self, exit_code, result):
        if exit_code == 0:
            color = '#004905'
            message = QCoreApplication.translate("DialogImportSchema", "Model(s) successfully imported into the database!")
        else:
            color = '#aa2222'
            message = QCoreApplication.translate("DialogImportSchema", "Finished with errors!")

            # Open log
            if self.log_config.isCollapsed():
                self.log_config.setCollapsed(False)

        self.txtStdout.setTextColor(QColor(color))
        self.txtStdout.append(message)

    def advance_progress_bar_by_text(self, text):
        if text.strip() == 'Info: compile models…':
            self.progress_bar.setValue(20)
            QCoreApplication.processEvents()
        elif text.strip() == 'Info: create table structure…':
            self.progress_bar.setValue(70)
            QCoreApplication.processEvents()

    def clear_messages(self):
        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.txtStdout.clear()  # Clear previous log messages
        self.progress_bar.setValue(0)  # Initialize progress bar

    def show_help(self):
        show_plugin_help("import_schema")

    def disable(self):
        self.db_config.setEnabled(False)
        self.ili_config.setEnabled(False)
        self.buttonBox.setEnabled(False)

    def enable(self):
        self.db_config.setEnabled(True)
        self.ili_config.setEnabled(True)
        self.buttonBox.setEnabled(True)

    def show_message(self, message, level):
        if level == Qgis.Warning:
            self.enable()

        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.bar.pushMessage("Asistente LADM-COL", message, level, duration = 0)

    def _connect_ili2db_signals(self, ili2db):
        ili2db.process_started.connect(self.on_process_started)
        ili2db.stderr.connect(self.on_stderr)
        ili2db.stdout.connect(self.print_info)
        ili2db.process_finished.connect(self.on_process_finished)

    def _disconnect_ili2db_signals(self, ili2db):
        ili2db.process_started.disconnect(self.on_process_started)
        ili2db.stderr.disconnect(self.on_stderr)
        ili2db.stdout.disconnect(self.print_info)
        ili2db.process_finished.disconnect(self.on_process_finished)
