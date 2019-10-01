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
import json

from qgis.PyQt.QtNetwork import (QNetworkRequest,
                                 QNetworkAccessManager)
from qgis.PyQt.QtCore import (Qt,
                              QSettings,
                              pyqtSignal,
                              QUrl,
                              QCoreApplication,
                              QTextStream,
                              QIODevice,
                              QEventLoop)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QSizePolicy)
from qgis.core import (Qgis,
                       QgsCoordinateReferenceSystem,
                       QgsApplication)
from qgis.gui import QgsMessageBar

from ...config.general_config import (DEFAULT_TOO_LONG_BOUNDARY_SEGMENTS_TOLERANCE,
                                      DEFAULT_EPSG,
                                      PLUGIN_NAME,
                                      COLLECTED_DB_SOURCE,
                                      TEST_SERVER,
                                      DEFAULT_ENDPOINT_SOURCE_SERVICE,
                                      SOURCE_SERVICE_EXPECTED_ID,
                                      NATIONAL_LAND_AGENCY)
from ...gui.dialogs.dlg_custom_model_dir import CustomModelDirDialog
from ...lib.db.db_connector import (DBConnector,
                                    EnumTestLevel)
from ...utils import get_ui_class
from ...utils.qt_utils import OverrideCursor

from ...resources_rc import * # Necessary to show icons
from ...config.config_db_supported import ConfigDbSupported
from ...lib.db.enum_db_action_type import EnumDbActionType

DIALOG_UI = get_ui_class('dialogs/dlg_settings.ui')


class SettingsDialog(QDialog, DIALOG_UI):
    db_connection_changed = pyqtSignal(DBConnector, bool) # dbconn, ladm_col_db
    organization_tools_changed = pyqtSignal(str)

    def __init__(self, parent=None, qgis_utils=None, conn_manager=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.log = QgsApplication.messageLog()
        self.conn_manager = conn_manager
        self._db = None
        self.qgis_utils = qgis_utils
        self.db_source = COLLECTED_DB_SOURCE

        self.ant_tools_initial_chk_value = None

        self._action_type = None
        self.conf_db = ConfigDbSupported()

        self.online_models_radio_button.setChecked(True)
        self.online_models_radio_button.toggled.connect(self.model_provider_toggle)
        self.custom_model_directories_line_edit.setText("")
        self.custom_models_dir_button.clicked.connect(self.show_custom_model_dir)
        self.custom_model_directories_line_edit.setVisible(False)
        self.custom_models_dir_button.setVisible(False)

        # CRS Setting
        self.crsSelector.crsChanged.connect(self.crs_changed)

        # Set connections
        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.helpRequested.connect(self.show_help)
        self.finished.connect(self.finished_slot)
        self.btn_test_connection.clicked.connect(self.test_connection)
        self.btn_test_ladm_col_structure.clicked.connect(self.test_ladm_col_structure)

        self.btn_test_service.clicked.connect(self.test_service)
        self.chk_use_roads.toggled.connect(self.update_images_state)

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

        self.cbo_db_source.clear()

        self._lst_db = self.conf_db.get_db_items()
        self._lst_panel = dict()

        for key, value in self._lst_db.items():
            self.cbo_db_source.addItem(value.get_name(), key)
            self._lst_panel[key] = value.get_config_panel(self)
            self._lst_panel[key].notify_message_requested.connect(self.show_message)
            self.db_layout.addWidget(self._lst_panel[key])

        self.db_source_changed()

        # Trigger some default behaviours
        self.restore_settings()

        self.cbo_db_source.currentIndexChanged.connect(self.db_source_changed)
        self.rejected.connect(self.close_dialog)

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
        current_db = self.cbo_db_source.currentData()
        params = self._lst_panel[current_db].read_connection_parameters()
        db = self._lst_db[current_db].get_db_connector(params)
        db.open_connection() # Open connection using gui parameters
        return db

    def get_db_connection(self):
        if self._db is not None:
            self.log.logMessage("Returning existing db connection...", PLUGIN_NAME, Qgis.Info)
        else:
            self.log.logMessage("Getting new db connection...", PLUGIN_NAME, Qgis.Info)
            self._db = self._get_db_connector_from_gui()
            self._db.open_connection()

        return self._db

    def show_custom_model_dir(self):
        dlg = CustomModelDirDialog(self.custom_model_directories_line_edit.text(), self)
        dlg.exec_()

    def accepted(self):
        # Validate EPSG selected
        if self.crsSelector.crs().authid()[:5] != 'EPSG:':
            self.show_message(QCoreApplication.translate("SettingsDialog", "Select a valid EPSG!"), Qgis.Warning)
            return  # Do not close the dialog

        current_db = self.cbo_db_source.currentData()
        if self._lst_panel[current_db].state_changed():
            valid_connection = True
            ladm_col_schema = False

            db = self._get_db_connector_from_gui()

            test_level = EnumTestLevel.DB_SCHEMA

            if self._action_type == EnumDbActionType.SCHEMA_IMPORT:
                # Limit the validation (used in GeoPackage)
                test_level |= EnumTestLevel.SCHEMA_IMPORT

            res, msg = db.test_connection(test_level)

            if res:
                if self._action_type != EnumDbActionType.SCHEMA_IMPORT:
                    # Don't check if it's a LADM schema, we expect it to be after we run the schema import
                    ladm_col_schema, msg = db.test_connection(EnumTestLevel.LADM)

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

                # Emmit signal when change db source
                self.db_connection_changed.emit(self._db, ladm_col_schema)

                self.save_settings()
                QDialog.accept(self)
            else:
                return  # Do not close the dialog
        else:
            # Save settings from tabs other than database connection
            self.save_settings()
            QDialog.accept(self)

        if self.chk_ant_tools.isChecked() != self.ant_tools_initial_chk_value:
            self.organization_tools_changed.emit(NATIONAL_LAND_AGENCY)

        self.close()

    def reject(self):
        self.done(0)

    def finished_slot(self, result):
        self.bar.clearWidgets()

    def set_db_connection(self, mode, dict_conn):
        """
        To be used by external scripts and unit tests
        """
        self.cbo_db_source.setCurrentIndex(self.cbo_db_source.findData(mode))
        self.db_source_changed()

        current_db = self.cbo_db_source.currentData()

        self._lst_panel[current_db].write_connection_parameters(dict_conn)

        self.accepted() # Create/update the db object

    def save_settings(self):
        settings = QSettings()
        current_db = self.cbo_db_source.currentData()
        settings.setValue('Asistente-LADM_COL/db/{db_source}/db_connection_source'.format(db_source=self.db_source), current_db)
        dict_conn = self._lst_panel[current_db].read_connection_parameters()

        self._lst_db[current_db].save_parameters_conn(dict_conn=dict_conn, db_source=self.db_source)

        settings.setValue('Asistente-LADM_COL/models/custom_model_directories_is_checked', self.offline_models_radio_button.isChecked())
        if self.offline_models_radio_button.isChecked():
            settings.setValue('Asistente-LADM_COL/models/custom_models', self.custom_model_directories_line_edit.text())

        settings.setValue('Asistente-LADM_COL/quality/too_long_tolerance', int(self.txt_too_long_tolerance.text()) or DEFAULT_TOO_LONG_BOUNDARY_SEGMENTS_TOLERANCE)
        settings.setValue('Asistente-LADM_COL/quality/use_roads', self.chk_use_roads.isChecked())

        settings.setValue('Asistente-LADM_COL/automatic_values/automatic_values_in_batch_mode', self.chk_automatic_values_in_batch_mode.isChecked())
        settings.setValue('Asistente-LADM_COL/sources/document_repository', self.connection_box.isChecked())

        settings.setValue('Asistente-LADM_COL/advanced_settings/ant_tools', self.chk_ant_tools.isChecked())
        settings.setValue('Asistente-LADM_COL/advanced_settings/validate_data_importing_exporting', self.chk_validate_data_importing_exporting.isChecked())

        settings.setValue('Asistente-LADM_COL/advanced_settings/epsg', self.epsg)

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
        default_db = self.conf_db.id_default_db

        index_db = self.cbo_db_source.findData(settings.value('Asistente-LADM_COL/db/{db_source}/db_connection_source'.format(db_source=self.db_source), default_db))

        if index_db == -1:
            index_db = self.cbo_db_source.findData(default_db)

        self.cbo_db_source.setCurrentIndex(index_db)
        self.db_source_changed()

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

        self.txt_too_long_tolerance.setText(str(settings.value('Asistente-LADM_COL/quality/too_long_tolerance', DEFAULT_TOO_LONG_BOUNDARY_SEGMENTS_TOLERANCE)))
        use_roads = settings.value('Asistente-LADM_COL/quality/use_roads', True, bool)
        self.chk_use_roads.setChecked(use_roads)
        self.update_images_state(use_roads)

        self.chk_automatic_values_in_batch_mode.setChecked(settings.value('Asistente-LADM_COL/automatic_values/automatic_values_in_batch_mode', True, bool))
        self.connection_box.setChecked(settings.value('Asistente-LADM_COL/sources/document_repository', True, bool))
        self.namespace_collapsible_group_box.setChecked(settings.value('Asistente-LADM_COL/automatic_values/namespace_enabled', True, bool))
        self.chk_local_id.setChecked(settings.value('Asistente-LADM_COL/automatic_values/local_id_enabled', True, bool))
        self.txt_namespace.setText(str(settings.value('Asistente-LADM_COL/automatic_values/namespace_prefix', "")))

        self.ant_tools_initial_chk_value = settings.value('Asistente-LADM_COL/advanced_settings/ant_tools', False, bool)
        self.chk_ant_tools.setChecked(self.ant_tools_initial_chk_value)

        self.chk_validate_data_importing_exporting.setChecked(settings.value('Asistente-LADM_COL/advanced_settings/validate_data_importing_exporting', True, bool))
        crs = QgsCoordinateReferenceSystem(settings.value('Asistente-LADM_COL/advanced_settings/epsg', int(DEFAULT_EPSG), int))
        self.crsSelector.setCrs(crs)
        self.crs_changed()

        self.txt_service_endpoint.setText(settings.value('Asistente-LADM_COL/sources/service_endpoint', DEFAULT_ENDPOINT_SOURCE_SERVICE))

    def db_source_changed(self):
        if self._db is not None:
            self._db.close_connection()

        self._db = None # Reset db connection

        for key, value in self._lst_panel.items():
            value.setVisible(False)

        current_db = self.cbo_db_source.currentData()

        self._lst_panel[current_db].setVisible(True)

    def test_connection(self):
        db = self._get_db_connector_from_gui()
        test_level = EnumTestLevel.DB_SCHEMA

        if self._action_type == EnumDbActionType.SCHEMA_IMPORT:
            test_level |= EnumTestLevel.SCHEMA_IMPORT

        res, msg = db.test_connection(test_level)

        if db is not None:
            db.close_connection()

        self.show_message(msg, Qgis.Info if res else Qgis.Warning)
        self.log.logMessage("Test connection!", PLUGIN_NAME, Qgis.Info)

    def test_ladm_col_structure(self):
        db = self._get_db_connector_from_gui()
        test_level = EnumTestLevel.LADM
        res, msg = db.test_connection(test_level=test_level)

        if db is not None:
            db.close_connection()

        self.show_message(msg, Qgis.Info if res else Qgis.Warning)
        self.log.logMessage("Test connection!", PLUGIN_NAME, Qgis.Info)

    def test_service(self):
        self.setEnabled(False)
        QCoreApplication.processEvents()
        res, msg = self.qgis_utils.is_source_service_valid(self.txt_service_endpoint.text().strip())
        self.setEnabled(True)
        self.show_message(msg['text'], msg['level'])

    def show_message(self, message, level):
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

    def crs_changed(self):
        if self.crsSelector.crs().authid()[:5] != 'EPSG:':
            self.crs_label.setStyleSheet('color: orange')
            self.crs_label.setToolTip(QCoreApplication.translate("SettingsDialog", 'Please select an EPSG Coordinate Reference System'))
            self.epsg = int(DEFAULT_EPSG)
        else:
            self.crs_label.setStyleSheet('')
            self.crs_label.setToolTip(QCoreApplication.translate("SettingsDialog", 'Coordinate Reference System'))
            authid = self.crsSelector.crs().authid()
            self.epsg = int(authid[5:])
