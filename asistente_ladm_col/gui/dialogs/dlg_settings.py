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
                                 QRadioButton)
from qgis.core import Qgis
from qgis.gui import QgsMessageBar

from asistente_ladm_col.config.config_db_supported import ConfigDbSupported
from asistente_ladm_col.config.enums import EnumDbActionType
from asistente_ladm_col.config.general_config import (COLLECTED_DB_SOURCE,
                                                      DEFAULT_ENDPOINT_SOURCE_SERVICE)
from asistente_ladm_col.config.transitional_system_config import TransitionalSystemConfig
from asistente_ladm_col.gui.dialogs.dlg_custom_model_dir import CustomModelDirDialog
from asistente_ladm_col.gui.gui_builder.role_registry import Role_Registry
from asistente_ladm_col.lib.db.db_connector import (DBConnector,
                                                    EnumTestLevel)
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils import get_ui_class

DIALOG_UI = get_ui_class('dialogs/dlg_settings.ui')


class SettingsDialog(QDialog, DIALOG_UI):
    db_connection_changed = pyqtSignal(DBConnector, bool, str)  # dbconn, ladm_col_db, source
    active_role_changed = pyqtSignal()

    def __init__(self, parent=None, qgis_utils=None, conn_manager=None, db_source=COLLECTED_DB_SOURCE, tab_pages_list=list()):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.logger = Logger()
        self.conn_manager = conn_manager
        self._db = None
        self.qgis_utils = qgis_utils
        self.db_source = db_source
        self._required_models = list()
        self.init_db_engine = None

        self._action_type = None
        self.dbs_supported = ConfigDbSupported()
        self.show_tabs(tab_pages_list)

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
        self.restore_settings()

        self.roles = Role_Registry()
        self.load_roles()

        self.cbo_db_engine.currentIndexChanged.connect(self.db_engine_changed)
        self.rejected.connect(self.close_dialog)

    def show_tabs(self, tab_pages_list):
        """
        Show only those tabs that are listed in tab_pages_list, if any. If it's an empty list, show all tabs.
        """
        if tab_pages_list:
            for i in reversed(range(self.tabWidget.count())):
                if i not in tab_pages_list:
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
        current_db_engine = self.cbo_db_engine.currentData()
        if self._lst_panel[current_db_engine].state_changed() or self.init_db_engine != current_db_engine:
            valid_connection = True
            ladm_col_schema = False

            db = self._get_db_connector_from_gui()

            test_level = EnumTestLevel.DB_SCHEMA

            if self._action_type == EnumDbActionType.SCHEMA_IMPORT:
                # Limit the validation (used in GeoPackage)
                test_level |= EnumTestLevel.SCHEMA_IMPORT

            res, code, msg = db.test_connection(test_level)

            if res:
                if self._action_type != EnumDbActionType.SCHEMA_IMPORT:
                    # Only check LADM-schema if we are not in an SCHEMA IMPORT.
                    # We know in an SCHEMA IMPORT, at this point the schema is still not LADM.
                    ladm_col_schema, code, msg = db.test_connection(EnumTestLevel.LADM, required_models=self._required_models)

                if not ladm_col_schema and self._action_type != EnumDbActionType.SCHEMA_IMPORT:
                    self.show_message(msg, Qgis.Warning)
                    return  # Do not close the dialog

            else:
                self.show_message(msg, Qgis.Warning)
                valid_connection = False

            if valid_connection:
                if self._db is not None:
                    self._db.close_connection()

                self._db = db

                # Update db connect with new db conn
                self.conn_manager.set_db_connector_for_source(self._db, self.db_source)

                # Emmit signal when db source changes
                self.db_connection_changed.emit(self._db, ladm_col_schema, self.db_source)
                self.logger.debug(__name__, "Settings dialog emitted a db_connection_changed.")

                self.save_settings()
                QDialog.accept(self)
            else:
                return  # Do not close the dialog
        else:
            # Save settings from tabs other than database connection
            self.save_settings()
            QDialog.accept(self)

        # If active role changed, refresh theg GUI
        selected_role = self.get_selected_role()
        if self.roles.get_active_role() != selected_role:
            self.logger.info(__name__, "The active role has changed from '{}' to '{}'.".format(
                self.roles.get_active_role(), selected_role))
            self.roles.set_active_role(selected_role)
            self.active_role_changed.emit()

        self.close()

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

    def set_db_connection(self, mode, dict_conn):
        self.cbo_db_engine.setCurrentIndex(self.cbo_db_engine.findData(mode))
        self.db_engine_changed()
        current_db_engine = self.cbo_db_engine.currentData()

        self._lst_panel[current_db_engine].write_connection_parameters(dict_conn)

        self.accepted() # Create/update the db object

    def save_settings(self):
        settings = QSettings()
        current_db_engine = self.cbo_db_engine.currentData()
        settings.setValue('Asistente-LADM_COL/db/{db_source}/db_connection_engine'.format(db_source=self.db_source), current_db_engine)
        dict_conn = self._lst_panel[current_db_engine].read_connection_parameters()

        self._lst_db[current_db_engine].save_parameters_conn(dict_conn=dict_conn, db_source=self.db_source)

        settings.setValue('Asistente-LADM_COL/models/custom_model_directories_is_checked', self.offline_models_radio_button.isChecked())
        if self.offline_models_radio_button.isChecked():
            settings.setValue('Asistente-LADM_COL/models/custom_models', self.custom_model_directories_line_edit.text())

        settings.setValue('Asistente-LADM_COL/quality/use_roads', self.chk_use_roads.isChecked())

        settings.setValue('Asistente-LADM_COL/automatic_values/automatic_values_in_batch_mode', self.chk_automatic_values_in_batch_mode.isChecked())
        settings.setValue('Asistente-LADM_COL/sources/document_repository', self.connection_box.isChecked())

        settings.setValue('Asistente-LADM_COL/advanced_settings/validate_data_importing_exporting', self.chk_validate_data_importing_exporting.isChecked())

        endpoint_transitional_system = self.txt_service_transitional_system.text().strip()
        settings.setValue('Asistente-LADM_COL/sources/service_transitional_system', (endpoint_transitional_system[:-1] if endpoint_transitional_system.endswith('/') else endpoint_transitional_system) or TransitionalSystemConfig().ST_DEFAULT_DOMAIN)

        endpoint = self.txt_service_endpoint.text().strip()
        settings.setValue('Asistente-LADM_COL/sources/service_endpoint', (endpoint[:-1] if endpoint.endswith('/') else endpoint) or DEFAULT_ENDPOINT_SOURCE_SERVICE)

        # Changes in automatic namespace or local_id configuration?
        current_namespace_enabled = settings.value('Asistente-LADM_COL/automatic_values/namespace_enabled', True, bool)
        current_namespace_prefix = settings.value('Asistente-LADM_COL/automatic_values/namespace_prefix', "")
        current_local_id_enabled = settings.value('Asistente-LADM_COL/automatic_values/local_id_enabled', True, bool)

        settings.setValue('Asistente-LADM_COL/automatic_values/namespace_enabled', self.namespace_collapsible_group_box.isChecked())
        if self.namespace_collapsible_group_box.isChecked():
            settings.setValue('Asistente-LADM_COL/automatic_values/namespace_prefix', self.txt_namespace.text())

        settings.setValue('Asistente-LADM_COL/automatic_values/local_id_enabled', self.chk_local_id.isChecked())

        if current_namespace_enabled != self.namespace_collapsible_group_box.isChecked() or \
           current_namespace_prefix != self.txt_namespace.text() or \
           current_local_id_enabled != self.chk_local_id.isChecked():
            if self._db is not None:
                self.qgis_utils.automatic_namespace_local_id_configuration_changed(self._db)

    def restore_settings(self):
        # Restore QSettings
        settings = QSettings()
        default_db_engine = self.dbs_supported.id_default_db

        self.init_db_engine = settings.value('Asistente-LADM_COL/db/{db_source}/db_connection_engine'.format(db_source=self.db_source), default_db_engine)
        index_db_engine = self.cbo_db_engine.findData(self.init_db_engine)

        if index_db_engine == -1:
            index_db_engine = self.cbo_db_engine.findData(default_db_engine)

        self.cbo_db_engine.setCurrentIndex(index_db_engine)
        self.db_engine_changed()

        # restore db settings for all panels
        for id_db, db_factory in self._lst_db.items():
            dict_conn = db_factory.get_parameters_conn(self.db_source)
            self._lst_panel[id_db].write_connection_parameters(dict_conn)
            self._lst_panel[id_db].save_state()

        custom_model_directories_is_checked = settings.value('Asistente-LADM_COL/models/custom_model_directories_is_checked', type=bool)
        if custom_model_directories_is_checked:
            self.offline_models_radio_button.setChecked(True)
            self.custom_model_directories_line_edit.setText(settings.value('Asistente-LADM_COL/models/custom_models'))
            self.custom_model_directories_line_edit.setVisible(True)
            self.custom_models_dir_button.setVisible(True)
        else:
            self.online_models_radio_button.setChecked(True)
            self.custom_model_directories_line_edit.setText("")
            self.custom_model_directories_line_edit.setVisible(False)
            self.custom_models_dir_button.setVisible(False)

        use_roads = settings.value('Asistente-LADM_COL/quality/use_roads', True, bool)
        self.chk_use_roads.setChecked(use_roads)
        self.update_images_state(use_roads)

        self.chk_automatic_values_in_batch_mode.setChecked(settings.value('Asistente-LADM_COL/automatic_values/automatic_values_in_batch_mode', True, bool))
        self.connection_box.setChecked(settings.value('Asistente-LADM_COL/sources/document_repository', True, bool))
        self.namespace_collapsible_group_box.setChecked(settings.value('Asistente-LADM_COL/automatic_values/namespace_enabled', True, bool))
        self.chk_local_id.setChecked(settings.value('Asistente-LADM_COL/automatic_values/local_id_enabled', True, bool))
        self.txt_namespace.setText(str(settings.value('Asistente-LADM_COL/automatic_values/namespace_prefix', "")))

        self.chk_validate_data_importing_exporting.setChecked(settings.value('Asistente-LADM_COL/advanced_settings/validate_data_importing_exporting', True, bool))

        self.txt_service_transitional_system.setText(settings.value('Asistente-LADM_COL/sources/service_transitional_system', TransitionalSystemConfig().ST_DEFAULT_DOMAIN))
        self.txt_service_endpoint.setText(settings.value('Asistente-LADM_COL/sources/service_endpoint', DEFAULT_ENDPOINT_SOURCE_SERVICE))

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

        res, code, msg = db.test_connection(test_level)

        if db is not None:
            db.close_connection()

        self.show_message(msg, Qgis.Info if res else Qgis.Warning)
        self.logger.info(__name__, "Test connection!")
        self.logger.debug(__name__, "Test connection ({}): {}, {}".format(test_level, res, msg))

    def test_ladm_col_structure(self):
        db = self._get_db_connector_from_gui()
        res, code, msg = db.test_connection(test_level=EnumTestLevel.LADM)

        if db is not None:
            db.close_connection()

        self.show_message(msg, Qgis.Info if res else Qgis.Warning)
        self.logger.info(__name__, "Test LADM structure!")
        self.logger.debug(__name__, "Test connection ({}): {}, {}".format(EnumTestLevel.LADM, res, msg))

    def test_service(self):
        self.setEnabled(False)
        QCoreApplication.processEvents()
        res, msg = self.qgis_utils.is_source_service_valid(self.txt_service_endpoint.text().strip())
        self.setEnabled(True)
        self.show_message(msg['text'], msg['level'])

    def test_service_transitional_system(self):
        self.setEnabled(False)
        QCoreApplication.processEvents()
        res, msg = self.qgis_utils.is_transitional_system_service_valid(self.txt_service_transitional_system.text().strip())
        self.setEnabled(True)
        self.show_message(msg['text'], msg['level'])

    def set_default_value_source_service(self):
        self.txt_service_endpoint.setText(DEFAULT_ENDPOINT_SOURCE_SERVICE)

    def set_default_value_transitional_system_service(self):
        self.txt_service_transitional_system.setText(TransitionalSystemConfig().ST_DEFAULT_DOMAIN)

    def show_message(self, message, level):
        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.bar.pushMessage(message, level, 10)

    def update_images_state(self, checked):
        self.img_with_roads.setEnabled(checked)
        self.img_with_roads.setToolTip(QCoreApplication.translate(
            "SettingsDialog", "Missing roads will be marked as errors.")
            if checked else '')
        self.img_without_roads.setEnabled(not checked)
        self.img_without_roads.setToolTip('' if checked else QCoreApplication.translate(
            "SettingsDialog", "Missing roads will not be marked as errors."))

    def show_help(self):
        self.qgis_utils.show_help("settings")

    def set_action_type(self, action_type):
        self._action_type = action_type

        for key, value in self._lst_panel.items():
            value.set_action(action_type)

    def set_required_models(self, required_models):
        self._required_models = required_models
