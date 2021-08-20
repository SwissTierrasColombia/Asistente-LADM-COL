# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2017-11-20
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
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
                              pyqtSignal,
                              QCoreApplication)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QSizePolicy,
                                 QVBoxLayout,
                                 QRadioButton,
                                 QMessageBox)
from qgis.core import Qgis
from qgis.gui import QgsMessageBar

from asistente_ladm_col.config.config_db_supported import ConfigDBsSupported
from asistente_ladm_col.config.enums import EnumDbActionType
from asistente_ladm_col.config.general_config import (DEFAULT_ENDPOINT_SOURCE_SERVICE,
                                                      DEFAULT_USE_SOURCE_SERVICE_SETTING,
                                                      DEFAULT_AUTOMATIC_VALUES_IN_BATCH_MODE,
                                                      TOLERANCE_MAX_VALUE)
from asistente_ladm_col.config.transitional_system_config import TransitionalSystemConfig
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.gui.dialogs.dlg_custom_model_dir import CustomModelDirDialog
from asistente_ladm_col.gui.gui_builder.role_registry import RoleRegistry
from asistente_ladm_col.lib.context import (SettingsContext,
                                            Context)
from asistente_ladm_col.lib.db.db_connector import (DBConnector,
                                                    EnumTestLevel)
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.transitional_system.st_session.st_session import STSession
from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.utils import show_plugin_help

DIALOG_UI = get_ui_class('dialogs/dlg_settings.ui')


class SettingsDialog(QDialog, DIALOG_UI):
    """
    Customizable dialog to configure LADM-COL Assistant.

    It can be created passing a SettingsContext with specific params
    or it can be instantiated and then set params one by one.
    """
    db_connection_changed = pyqtSignal(DBConnector, bool, str)  # dbconn, ladm_col_db, source
    open_dlg_import_schema = pyqtSignal(Context)  # Context for the import schema dialog

    def __init__(self, conn_manager=None, context=None, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.logger = Logger()
        self.conn_manager = conn_manager
        self.app = AppInterface()

        self.sbx_tolerance.setMaximum(TOLERANCE_MAX_VALUE)
        self._valid_document_repository = False  # Needs to be True if users want to enable doc repo (using test button)

        context = context if context else SettingsContext()

        self.db_source = context.db_source  # default db source is COLLECTED_DB_SOURCE
        self._required_models = context.required_models
        self._tab_pages_list = context.tab_pages_list
        self._blocking_mode = context.blocking_mode  # Whether the dialog can only be accepted on valid DB connections or not
        self._action_type = context.action_type  # By default "config"
        self.setWindowTitle(context.title)

        self._db = None
        self.init_db_engine = None
        self.dbs_supported = ConfigDBsSupported()
        self._open_dlg_import_schema = False  # After accepting, if non-valid DB is configured, we can go to import schema

        self.online_models_radio_button.setEnabled(False)  # This option is disabled until we have online models back!
        self.online_models_radio_button.setChecked(True)
        self.online_models_radio_button.toggled.connect(self.model_provider_toggle)
        self.custom_model_directories_line_edit.setText("")
        self.custom_models_dir_button.clicked.connect(self.show_custom_model_dir)
        self.custom_model_directories_line_edit.setVisible(False)
        self.custom_models_dir_button.setVisible(False)

        # Set connections
        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.helpRequested.connect(self.show_help)
        self.finished.connect(self.finished_slot)
        self.btn_test_connection.clicked.connect(self.test_connection)
        self.btn_test_ladm_col_structure.clicked.connect(self.test_ladm_col_structure)

        self.btn_test_service.clicked.connect(self.test_service)
        self.btn_test_service_transitional_system.clicked.connect(self.test_service_transitional_system)
        self.txt_service_endpoint.textEdited.connect(self.source_service_endpoint_changed)  # For manual changes only

        self.btn_default_value_sources.clicked.connect(self.set_default_value_source_service)
        self.btn_default_value_transitional_system.clicked.connect(self.set_default_value_transitional_system_service)

        self.chk_use_roads.toggled.connect(self.update_images_state)

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

        self.cbo_db_engine.clear()

        self._lst_db = self.dbs_supported.get_db_factories()
        self._lst_panel = dict()

        for key, value in self._lst_db.items():
            self.cbo_db_engine.addItem(value.get_name(), key)
            self._lst_panel[key] = value.get_config_panel(self)
            self._lst_panel[key].notify_message_requested.connect(self.show_message)
            self.db_layout.addWidget(self._lst_panel[key])

        self.db_engine_changed()

        # Trigger some default behaviours
        self.restore_db_source_settings()  # restore settings with default db source
        self.restore_settings()

        self.roles = RoleRegistry()
        self.load_roles()

        self.cbo_db_engine.currentIndexChanged.connect(self.db_engine_changed)
        self.rejected.connect(self.close_dialog)

        self._update_tabs()

        if context.tip:
            self.show_tip(context.tip)

    def set_db_source(self, db_source):
        self.db_source = db_source
        self.restore_db_source_settings()

    def set_tab_pages_list(self, tab_pages_list):
        self._tab_pages_list = tab_pages_list
        self._update_tabs()

    def set_required_models(self, required_models):
        self._required_models = required_models

    def set_blocking_mode(self, block):
        self._blocking_mode = block

    def _update_tabs(self):
        """
        Show only those tabs that are listed in tab_pages_list, if any. If it's an empty list, show all tabs.
        """
        if self._tab_pages_list:
            for i in reversed(range(self.tabWidget.count())):
                if i not in self._tab_pages_list:
                    self.tabWidget.removeTab(i)

    def load_roles(self):
        """
        Initialize group box for selecting the active role
        """
        self.gbx_active_role_layout = QVBoxLayout()
        dict_roles = self.roles.get_roles_info()
        checked = False
        active_role = self.roles.get_active_role()

        # Initialize radio buttons
        for k, v in dict_roles.items():
            radio = QRadioButton(v)
            radio.setToolTip(self.roles.get_role_description(k))

            if not checked:
                if k == active_role:
                    radio.setChecked(True)
                    checked = True

            self.gbx_active_role_layout.addWidget(radio)

        self.gbx_active_role.setLayout(self.gbx_active_role_layout)

    def close_dialog(self):
        self.close()

    def showEvent(self, event):
        # It is necessary to reload the variables
        # to load the database and schema name
        self.restore_settings()

        self.btn_test_ladm_col_structure.setVisible(self._action_type != EnumDbActionType.SCHEMA_IMPORT)

    def model_provider_toggle(self):
        if self.offline_models_radio_button.isChecked():
            self.custom_model_directories_line_edit.setVisible(True)
            self.custom_models_dir_button.setVisible(True)
        else:
            self.custom_model_directories_line_edit.setVisible(False)
            self.custom_models_dir_button.setVisible(False)
            self.custom_model_directories_line_edit.setText("")

    def _get_db_connector_from_gui(self):
        current_db_engine = self.cbo_db_engine.currentData()
        params = self._lst_panel[current_db_engine].read_connection_parameters()
        db = self._lst_db[current_db_engine].get_db_connector(params)
        return db

    def get_db_connection(self):
        if self._db is not None:
            self.logger.info(__name__, "Returning existing db connection...")
        else:
            self.logger.info(__name__, "Getting new db connection...")
            self._db = self._get_db_connector_from_gui()
            self._db.open_connection()

        return self._db

    def show_custom_model_dir(self):
        dlg = CustomModelDirDialog(self.custom_model_directories_line_edit.text(), self)
        dlg.exec_()

    def accepted(self):
        """
        We start checking the document repository configuration and only allow to continue if we have a valid repo or
        if the repo won't be used.

        Then, check if connection to DB/schema is valid, if not, block the dialog.
        If valid, check it complies with LADM. If not, block the dialog. If it complies, we have two options: To emit
        db_connection changed or not. Finally, we store options in QSettings.
        """
        res_doc_repo, msg_doc_repo = self.check_document_repository_before_saving_settings()
        if not res_doc_repo:
            self.show_message(msg_doc_repo, Qgis.Warning, 0)
            return  # Do not close the dialog

        ladm_col_schema = False

        db = self._get_db_connector_from_gui()

        test_level = EnumTestLevel.DB_SCHEMA

        if self._action_type == EnumDbActionType.SCHEMA_IMPORT:
            # Limit the validation (used in GeoPackage)
            test_level |= EnumTestLevel.SCHEMA_IMPORT

        res, code, msg = db.test_connection(test_level)  # No need to pass required_models, we don't test that much

        if res:
            if self._action_type != EnumDbActionType.SCHEMA_IMPORT:
                # Only check LADM-schema if we are not in an SCHEMA IMPORT.
                # We know in an SCHEMA IMPORT, at this point the schema is still not LADM.
                ladm_col_schema, code, msg = db.test_connection(EnumTestLevel.LADM,
                                                                required_models=self._required_models)

            if not ladm_col_schema and self._action_type != EnumDbActionType.SCHEMA_IMPORT:
                if self._blocking_mode:
                    self.show_message(msg, Qgis.Warning)
                    return  # Do not close the dialog

        else:
            if self._blocking_mode:
                self.show_message(msg, Qgis.Warning)
                return  # Do not close the dialog

        # Connection is valid and complies with LADM
        current_db_engine = self.cbo_db_engine.currentData()
        if self._lst_panel[current_db_engine].state_changed() or self.init_db_engine != current_db_engine:
            # Emit db_connection_changed
            if self._db is not None:
                self._db.close_connection()

            self._db = db

            # Update db connect with new db conn
            self.conn_manager.set_db_connector_for_source(self._db, self.db_source)

            # Emmit signal when db source changes
            self.db_connection_changed.emit(self._db, ladm_col_schema, self.db_source)
            self.logger.debug(__name__, "Settings dialog emitted a db_connection_changed.")

        if not ladm_col_schema and self._action_type == EnumDbActionType.CONFIG:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Question)
            msg_box.setText(QCoreApplication.translate("SettingsDialog",
                "No LADM-COL DB has been configured! You'll continue with limited functionality until you configure a LADM-COL DB with models supported by the active role.\n\nDo you want to go to 'Create LADM-COL structure' dialog?"))
            msg_box.setWindowTitle(QCoreApplication.translate("SettingsDialog", "Important"))
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.Ignore)
            msg_box.setDefaultButton(QMessageBox.Ignore)
            msg_box.button(QMessageBox.Yes).setText(QCoreApplication.translate("SettingsDialog", "Yes, go to create structure"))
            msg_box.button(QMessageBox.Ignore).setText(QCoreApplication.translate("SettingsDialog", "No, I'll do it later"))
            reply = msg_box.exec_()

            if reply == QMessageBox.Yes:
                self._open_dlg_import_schema = True  # We will open it when we've closed this Settings dialog

        # If active role is changed (a check and confirmation may be needed), refresh the GUI
        # Note: Better to leave this check as the last one in the accepted() method.
        selected_role = self.get_selected_role()
        if self.roles.get_active_role() != selected_role:
            b_change_role = True
            if STSession().is_user_logged():
                reply = QMessageBox.question(self.parent,
                                             QCoreApplication.translate("SettingsDialog", "Warning"),
                                             QCoreApplication.translate("SettingsDialog",
                                                                        "You have a ST connection opened and you want to change your role.\nIf you confirm that you want to change your role, you'll be logged out from the ST.\n\nDo you really want to change your role?"),
                                             QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
                if reply == QMessageBox.Yes:
                    STSession().logout()
                elif reply == QMessageBox.Cancel:
                    # No need to switch back selected role, the Settings Dialog gets it from role registry
                    b_change_role = False

            if b_change_role:
                self.logger.info(__name__, "The active role has changed from '{}' to '{}'.".format(
                    self.roles.get_active_role(), selected_role))
                self.roles.set_active_role(selected_role)  # Emits signal that refreshed the plugin for this role

        self.save_settings(db)

        QDialog.accept(self)
        self.close()

        if self._open_dlg_import_schema:
            # After Settings dialog has been closed, we could call Import Schema depending on user's answer above
            self.open_dlg_import_schema.emit(Context())
            self.logger.debug(__name__, "Settings dialog emitted a show Import Schema dialog.")

    def check_document_repository_before_saving_settings(self):
        # Check if source service is checked (active). If so, check if either status or endpoint changed. If so,
        # check if self._valid_document_repository is False. If so, we need to test the service and only allow to save
        # if such test is successful.
        res, msg = True, ''
        if self.connection_box.isChecked():  # The user wants to have the source service enabled
            initial_config = QSettings().value('Asistente-LADM-COL/sources/use_service', DEFAULT_USE_SOURCE_SERVICE_SETTING, bool)
            initial_endpoint = QSettings().value('Asistente-LADM-COL/sources/service_endpoint', DEFAULT_ENDPOINT_SOURCE_SERVICE)

            # Config changed or Endpoint changed?
            if initial_config != self.connection_box.isChecked() or initial_endpoint.strip() != self.txt_service_endpoint.text().strip():
                if not self._valid_document_repository:  # A test service has not been run, so we need to do it now
                    self.logger.debug(__name__, "The user wants to enable the source service but the 'test service' has not been run on the current URL. Testing it...")
                    res_test, msg_test = self.test_service()
                    if not res_test:
                        res = False
                        msg = QCoreApplication.translate("SettingsDialog", "The source service is not valid, so it cannot be activated! Adjust such configuration before saving settings.")

        return res, msg

    def source_service_endpoint_changed(self, new_text):
        # Source service endpoint was changed, so a test_service is required to make the valid variable True
        self._valid_document_repository = False

    def get_selected_role(self):
        selected_role = None
        radio_checked = None
        for i in range(self.gbx_active_role_layout.count()):
            radio = self.gbx_active_role_layout.itemAt(i).widget()
            if radio.isChecked():
                radio_checked = radio.text()
                break

        for k, v in self.roles.get_roles_info().items():
            if v == radio_checked:
                selected_role = k
                break

        return selected_role  # Role key

    def reject(self):
        self.done(0)

    def finished_slot(self, result):
        self.bar.clearWidgets()

    def save_settings(self, db):
        settings = QSettings()
        current_db_engine = self.cbo_db_engine.currentData()
        settings.setValue('Asistente-LADM-COL/db/{db_source}/db_connection_engine'.format(db_source=self.db_source), current_db_engine)
        dict_conn = self._lst_panel[current_db_engine].read_connection_parameters()

        self._lst_db[current_db_engine].save_parameters_conn(dict_conn=dict_conn, db_source=self.db_source)

        self.app.settings.custom_models = self.offline_models_radio_button.isChecked()
        if self.offline_models_radio_button.isChecked():
            self.app.settings.custom_model_dirs = self.custom_model_directories_line_edit.text()

        self.app.settings.tolerance = self.sbx_tolerance.value()
        settings.setValue('Asistente-LADM-COL/quality/use_roads', self.chk_use_roads.isChecked())

        settings.setValue('Asistente-LADM-COL/models/validate_data_importing_exporting', self.chk_validate_data_importing_exporting.isChecked())

        endpoint_transitional_system = self.txt_service_transitional_system.text().strip()
        settings.setValue('Asistente-LADM-COL/sources/service_transitional_system', (endpoint_transitional_system[:-1] if endpoint_transitional_system.endswith('/') else endpoint_transitional_system) or TransitionalSystemConfig().ST_DEFAULT_DOMAIN)

        settings.setValue('Asistente-LADM-COL/sources/use_service', self.connection_box.isChecked())
        endpoint = self.txt_service_endpoint.text().strip()
        settings.setValue('Asistente-LADM-COL/sources/service_endpoint', (endpoint[:-1] if endpoint.endswith('/') else endpoint) or DEFAULT_ENDPOINT_SOURCE_SERVICE)

        settings.setValue('Asistente-LADM-COL/automatic_values/automatic_values_in_batch_mode', self.chk_automatic_values_in_batch_mode.isChecked())

        # Changes in automatic namespace, local_id or t_ili_tid configuration?
        current_namespace_enabled = settings.value('Asistente-LADM-COL/automatic_values/namespace_enabled', True, bool)
        current_namespace_prefix = settings.value('Asistente-LADM-COL/automatic_values/namespace_prefix', "")
        current_local_id_enabled = settings.value('Asistente-LADM-COL/automatic_values/local_id_enabled', True, bool)
        current_t_ili_tid_enabled = settings.value('Asistente-LADM-COL/automatic_values/t_ili_tid_enabled', True, bool)

        settings.setValue('Asistente-LADM-COL/automatic_values/namespace_enabled', self.namespace_collapsible_group_box.isChecked())
        if self.namespace_collapsible_group_box.isChecked():
            settings.setValue('Asistente-LADM-COL/automatic_values/namespace_prefix', self.txt_namespace.text())

        settings.setValue('Asistente-LADM-COL/automatic_values/local_id_enabled', self.chk_local_id.isChecked())
        settings.setValue('Asistente-LADM-COL/automatic_values/t_ili_tid_enabled', self.chk_t_ili_tid.isChecked())

        if current_namespace_enabled != self.namespace_collapsible_group_box.isChecked() or \
           current_namespace_prefix != self.txt_namespace.text() or \
           current_local_id_enabled != self.chk_local_id.isChecked() or \
           current_t_ili_tid_enabled != self.chk_t_ili_tid.isChecked():
            if db is not None:
                self.logger.info(__name__, "Automatic values changed in Settings dialog. All LADM-COL layers are being updated...")
                self.app.core.automatic_fields_settings_changed(db)

    def restore_db_source_settings(self):
        settings = QSettings()
        default_db_engine = self.dbs_supported.id_default_db

        self.init_db_engine = settings.value('Asistente-LADM-COL/db/{db_source}/db_connection_engine'.format(db_source=self.db_source), default_db_engine)
        index_db_engine = self.cbo_db_engine.findData(self.init_db_engine)

        if index_db_engine == -1:
            index_db_engine = self.cbo_db_engine.findData(default_db_engine)

        self.cbo_db_engine.setCurrentIndex(index_db_engine)
        self.db_engine_changed()

        # restore db settings for all panels
        for db_engine, db_factory in self._lst_db.items():
            dict_conn = db_factory.get_parameters_conn(self.db_source)
            self._lst_panel[db_engine].write_connection_parameters(dict_conn)
            self._lst_panel[db_engine].save_state()

    def restore_settings(self):
        # Restore QSettings
        settings = QSettings()

        custom_model_directories_is_checked = self.app.settings.custom_models
        if custom_model_directories_is_checked:
            self.offline_models_radio_button.setChecked(True)
            self.custom_model_directories_line_edit.setText(self.app.settings.custom_model_dirs)
            self.custom_model_directories_line_edit.setVisible(True)
            self.custom_models_dir_button.setVisible(True)
        else:
            self.online_models_radio_button.setChecked(True)
            self.custom_model_directories_line_edit.setText("")
            self.custom_model_directories_line_edit.setVisible(False)
            self.custom_models_dir_button.setVisible(False)

        self.sbx_tolerance.setValue(self.app.settings.tolerance)
        use_roads = settings.value('Asistente-LADM-COL/quality/use_roads', True, bool)
        self.chk_use_roads.setChecked(use_roads)
        self.update_images_state(use_roads)

        self.chk_automatic_values_in_batch_mode.setChecked(settings.value('Asistente-LADM-COL/automatic_values/automatic_values_in_batch_mode', DEFAULT_AUTOMATIC_VALUES_IN_BATCH_MODE, bool))
        self.connection_box.setChecked(settings.value('Asistente-LADM-COL/sources/use_service', DEFAULT_USE_SOURCE_SERVICE_SETTING, bool))
        self.namespace_collapsible_group_box.setChecked(settings.value('Asistente-LADM-COL/automatic_values/namespace_enabled', True, bool))
        self.chk_local_id.setChecked(settings.value('Asistente-LADM-COL/automatic_values/local_id_enabled', True, bool))
        self.chk_t_ili_tid.setChecked(settings.value('Asistente-LADM-COL/automatic_values/t_ili_tid_enabled', True, bool))
        self.txt_namespace.setText(str(settings.value('Asistente-LADM-COL/automatic_values/namespace_prefix', "")))

        self.chk_validate_data_importing_exporting.setChecked(settings.value('Asistente-LADM-COL/models/validate_data_importing_exporting', True, bool))

        self.txt_service_transitional_system.setText(settings.value('Asistente-LADM-COL/sources/service_transitional_system', TransitionalSystemConfig().ST_DEFAULT_DOMAIN))
        self.txt_service_endpoint.setText(settings.value('Asistente-LADM-COL/sources/service_endpoint', DEFAULT_ENDPOINT_SOURCE_SERVICE))

    def db_engine_changed(self):
        if self._db is not None:
            self._db.close_connection()

        self._db = None  # Reset db connection

        for key, value in self._lst_panel.items():
            value.setVisible(False)

        current_db_engine = self.cbo_db_engine.currentData()

        self._lst_panel[current_db_engine].setVisible(True)

    def test_connection(self):
        db = self._get_db_connector_from_gui()
        test_level = EnumTestLevel.DB_SCHEMA

        if self._action_type == EnumDbActionType.SCHEMA_IMPORT:
            test_level |= EnumTestLevel.SCHEMA_IMPORT

        res, code, msg = db.test_connection(test_level)  # No need to pass required_models, we don't test that much

        if db is not None:
            db.close_connection()

        self.show_message(msg, Qgis.Info if res else Qgis.Warning)
        self.logger.info(__name__, "Test connection!")
        self.logger.debug(__name__, "Test connection ({}): {}, {}".format(test_level, res, msg))

    def test_ladm_col_structure(self):
        db = self._get_db_connector_from_gui()
        res, code, msg = db.test_connection(test_level=EnumTestLevel.LADM, required_models=self._required_models)

        if db is not None:
            db.close_connection()

        self.show_message(msg, Qgis.Info if res else Qgis.Warning)
        self.logger.info(__name__, "Test LADM structure!")
        self.logger.debug(__name__, "Test connection ({}): {}, {}".format(EnumTestLevel.LADM, res, msg))

    def test_service(self):
        self.setEnabled(False)
        QCoreApplication.processEvents()
        res, msg = self.app.core.is_source_service_valid(self.txt_service_endpoint.text().strip())
        self._valid_document_repository = res  # Required to be True if the user wants to enable the source service
        self.setEnabled(True)
        self.show_message(msg['text'], msg['level'], 0)
        return res, msg

    def test_service_transitional_system(self):
        self.setEnabled(False)
        QCoreApplication.processEvents()
        res, msg = self.app.core.is_transitional_system_service_valid(self.txt_service_transitional_system.text().strip())
        self.setEnabled(True)
        self.show_message(msg['text'], msg['level'])

    def set_default_value_source_service(self):
        self.txt_service_endpoint.setText(DEFAULT_ENDPOINT_SOURCE_SERVICE)

    def set_default_value_transitional_system_service(self):
        self.txt_service_transitional_system.setText(TransitionalSystemConfig().ST_DEFAULT_DOMAIN)

    def show_message(self, message, level, duration=10):
        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.bar.pushMessage(message, level, duration)

    def show_tip(self, tip):
        self.show_message(tip, Qgis.Info, 0)  # Don't show counter for the tip message

    def update_images_state(self, checked):
        self.img_with_roads.setEnabled(checked)
        self.img_with_roads.setToolTip(QCoreApplication.translate(
            "SettingsDialog", "Missing roads will be marked as errors.")
            if checked else '')
        self.img_without_roads.setEnabled(not checked)
        self.img_without_roads.setToolTip('' if checked else QCoreApplication.translate(
            "SettingsDialog", "Missing roads will not be marked as errors."))

    def show_help(self):
        show_plugin_help("settings")

    def set_action_type(self, action_type):
        self._action_type = action_type

        for key, value in self._lst_panel.items():
            value.set_action(action_type)
