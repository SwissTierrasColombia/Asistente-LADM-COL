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
                              QEventLoop,
                              QTimer)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QSizePolicy,
                                 QGridLayout)
from qgis.core import (Qgis,
                       QgsApplication)
from qgis.gui import QgsMessageBar

from ..config.general_config import (DEFAULT_TOO_LONG_BOUNDARY_SEGMENTS_TOLERANCE,
                                     PLUGIN_NAME,
                                     TEST_SERVER,
                                     DEFAULT_ENDPOINT_SOURCE_SERVICE,
                                     SOURCE_SERVICE_EXPECTED_ID)
from ..gui.custom_model_dir import CustomModelDirDialog
from ..gui.dlg_get_db_or_schema_name import DialogGetDBOrSchemaName
from ..lib.dbconnector.db_connector import DBConnector
from ..lib.dbconnector.gpkg_connector import GPKGConnector
from ..lib.dbconnector.pg_connector import PGConnector
from ..utils import get_ui_class
from ..utils.qt_utils import OverrideCursor
from ..resources_rc import *

DIALOG_UI = get_ui_class('settings_dialog.ui')

class SettingsDialog(QDialog, DIALOG_UI):

    db_connection_changed = pyqtSignal(DBConnector)
    fetcher_task = None

    def __init__(self, iface=None, parent=None, qgis_utils=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._db = None
        self.qgis_utils = qgis_utils
        self.connection_is_dirty = False

        self.cbo_db_source.clear()
        self.cbo_db_source.addItem(QCoreApplication.translate("SettingsDialog", 'PostgreSQL / PostGIS'), 'pg')
        self.cbo_db_source.addItem(QCoreApplication.translate("SettingsDialog", 'GeoPackage'), 'gpkg')
        self.cbo_db_source.currentIndexChanged.connect(self.db_source_changed)

        self.online_models_radio_button.setChecked(True)
        self.online_models_radio_button.toggled.connect(self.model_provider_toggle)
        self.custom_model_directories_line_edit.setText("")
        self.custom_models_dir_button.clicked.connect(self.show_custom_model_dir)
        self.custom_model_directories_line_edit.setVisible(False)
        self.custom_models_dir_button.setVisible(False)

        # Set connections
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.helpRequested.connect(self.show_help)
        self.btn_test_connection.clicked.connect(self.test_connection)

        self.txt_pg_host.setPlaceholderText(QCoreApplication.translate("SettingsDialog", "[Leave empty to use standard host: localhost]"))
        self.txt_pg_host.textEdited.connect(self.set_connection_dirty)

        self.txt_pg_port.setPlaceholderText(QCoreApplication.translate("SettingsDialog", "[Leave empty to use standard port: 5432]"))
        self.txt_pg_port.textEdited.connect(self.set_connection_dirty)

        self.create_db_button.setToolTip(QCoreApplication.translate("SettingsDialog", "Create database"))
        self.create_db_button.clicked.connect(self.show_modal_create_db)
        self.selected_db_combobox.currentIndexChanged.connect(self.selected_database_changed)

        self.create_schema_button.setToolTip(QCoreApplication.translate("SettingsDialog", "Create schema"))
        self.create_schema_button.clicked.connect(self.show_modal_create_schema)

        self.txt_pg_user.setPlaceholderText(QCoreApplication.translate("SettingsDialog", "Database username"))
        self.txt_pg_user.textEdited.connect(self.set_connection_dirty)

        self.txt_pg_password.setPlaceholderText(QCoreApplication.translate("SettingsDialog", "[Leave empty to use system password]"))
        self.txt_pg_password.textEdited.connect(self.set_connection_dirty)
        self.txt_gpkg_file.textEdited.connect(self.set_connection_dirty)
        self.btn_test_service.clicked.connect(self.test_service)
        self.chk_use_roads.toggled.connect(self.update_images_state)

        # Trigger some default behaviours
        self.restore_settings()

        # Set a timer to avoid creating too many db connections while editing connection parameters
        self.refreshTimer = QTimer()
        self.refreshTimer.setSingleShot(True)
        self.refreshTimer.timeout.connect(self.refresh_connection)
        self.txt_pg_host.textChanged.connect(self.request_for_refresh_connection)
        self.txt_pg_port.textChanged.connect(self.request_for_refresh_connection)
        self.txt_pg_user.textChanged.connect(self.request_for_refresh_connection)
        self.txt_pg_password.textChanged.connect(self.request_for_refresh_connection)

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.setLayout(QGridLayout())
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

    def showEvent(self, event):
        self.update_db_names()
        # It is necessary to reload the variables
        # to load the database and schema name
        self.restore_settings()

        self.selected_schema_combobox.currentIndexChanged.connect(self.selected_schema_changed)
        print("Conectado...")

    def request_for_refresh_connection(self, text):
        # Wait half a second before refreshing connection
        self.refreshTimer.start(500)

    def refresh_connection(self):
        if not self.txt_pg_user.text().strip() \
                or not self.txt_pg_password.text().strip():
            self.selected_db_combobox.clear()
            self.selected_schema_combobox.clear()
        else:
            # Update database name list
            self.update_db_names()

    def selected_database_changed(self, index):
        self.update_db_schemas()

    def selected_schema_changed(self, index):
        if not self.connection_is_dirty:
            self.connection_is_dirty = True

    def update_db_names(self):
        if self.cbo_db_source.currentData() == 'pg':
            dict_conn = self.read_connection_parameters()
            tmp_db_conn = PGConnector('')
            uri = tmp_db_conn.get_connection_uri(dict_conn, 'pg', level=0)

            dbnames = tmp_db_conn.get_dbnames_list(uri)
            self.selected_db_combobox.clear()

            if dbnames[0]:
                self.selected_db_combobox.addItems(dbnames[1])
            else:
                # We won't show a message here to avoid bothering the user with potentially too much messages
                pass

    def update_db_schemas(self):
        if self.cbo_db_source.currentData() == 'pg':
            dict_conn = self.read_connection_parameters()
            tmp_db_conn = PGConnector('')
            uri = tmp_db_conn.get_connection_uri(dict_conn, 'pg')

            schemas_db = tmp_db_conn.get_dbname_schema_list(uri)
            self.selected_schema_combobox.clear()

            if schemas_db[0]:
                self.selected_schema_combobox.addItems(schemas_db[1])
            else:
                # We won't show a message here to avoid bothering the user with potentially too much messages
                pass

    def model_provider_toggle(self):
        if self.offline_models_radio_button.isChecked():
            self.custom_model_directories_line_edit.setVisible(True)
            self.custom_models_dir_button.setVisible(True)
        else:
            self.custom_model_directories_line_edit.setVisible(False)
            self.custom_models_dir_button.setVisible(False)
            self.custom_model_directories_line_edit.setText("")

    def get_db_connection(self, update_connection=True):
        if self._db is not None:
            self.log.logMessage("Returning existing db connection...", PLUGIN_NAME, Qgis.Info)
            return self._db
        else:
            self.log.logMessage("Getting new db connection...", PLUGIN_NAME, Qgis.Info)
            dict_conn = self.read_connection_parameters()
            if self.cbo_db_source.currentData() == 'pg':
                db = PGConnector(None, dict_conn['schema'], dict_conn)
            else:
                db = GPKGConnector(None, conn_dict=dict_conn)

            if update_connection:
                self._db = db

            return db

    def show_custom_model_dir(self):
        dlg = CustomModelDirDialog(self.custom_model_directories_line_edit.text(), self)
        dlg.exec_()

    def accepted(self):
        if self._db is not None:
            self._db.close_connection()

        self._db = None # Reset db connection
        self._db = self.get_db_connection()

        # Schema combobox changes frequently, so control whether we listen to its changes to make the db conn dirty
        try:
            self.selected_schema_combobox.currentIndexChanged.disconnect(self.selected_schema_changed)
        except TypeError as e:
            pass

        if self.connection_is_dirty:
            self.connection_is_dirty = False

            res, msg = self._db.test_connection()
            if res:
                self.db_connection_changed.emit(self._db)
            else:
                self.show_message(msg, Qgis.Warning)
                return

        self.save_settings()

    def reject(self):
        self.restore_settings()
        self.connection_is_dirty = False

        # Schema combobox changes frequently, so control whether we listen to its changes to make the db conn dirty
        try:
            self.selected_schema_combobox.currentIndexChanged.disconnect(self.selected_schema_changed)
        except TypeError as e:
            pass

        self.done(0)

    def set_db_connection(self, mode, dict_conn):
        """
        To be used by external scripts and unit tests
        """
        self.cbo_db_source.setCurrentIndex(self.cbo_db_source.findData(mode))
        self.db_source_changed()

        if self.cbo_db_source.currentData() == 'pg':
            self.txt_pg_host.setText(dict_conn['host'])
            self.txt_pg_port.setText(dict_conn['port'])

            self.selected_db_combobox.clear()
            dbname_setting = dict_conn['database']
            self.selected_db_combobox.addItem(dbname_setting)

            self.selected_schema_combobox.clear()
            schema_setting = dict_conn['schema']
            self.selected_schema_combobox.addItem(schema_setting)

            self.txt_pg_user.setText(dict_conn['username'])
            self.txt_pg_password.setText(dict_conn['password'])
        else:
            self.txt_gpkg_file.setText(dict_conn['dbfile'])

        self.accepted() # Create/update the db object

    def read_connection_parameters(self):
        """
        Convenient function to read connection parameters and apply default
        values if needed.
        """
        dict_conn = dict()
        dict_conn['host'] = self.txt_pg_host.text().strip() or 'localhost'
        dict_conn['port'] = self.txt_pg_port.text().strip() or '5432'
        dict_conn['database'] = "'{}'".format(self.selected_db_combobox.currentText().strip())
        dict_conn['schema'] = self.selected_schema_combobox.currentText().strip() or 'public'
        dict_conn['username'] = self.txt_pg_user.text().strip()
        dict_conn['password'] = self.txt_pg_password.text().strip()
        dict_conn['dbfile'] = self.txt_gpkg_file.text().strip()
        return dict_conn

    def save_settings(self):
        # Save QSettings
        dict_conn = self.read_connection_parameters()
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/db_connection_source', self.cbo_db_source.currentData())
        settings.setValue('Asistente-LADM_COL/pg/host', dict_conn['host'])
        settings.setValue('Asistente-LADM_COL/pg/port', dict_conn['port'])
        settings.setValue('Asistente-LADM_COL/pg/database', dict_conn['database'].strip("'"))
        settings.setValue('Asistente-LADM_COL/pg/schema', dict_conn['schema'])
        settings.setValue('Asistente-LADM_COL/pg/username', dict_conn['username'])
        settings.setValue('Asistente-LADM_COL/pg/password', dict_conn['password'])
        settings.setValue('Asistente-LADM_COL/gpkg/dbfile', dict_conn['dbfile'])

        settings.setValue('Asistente-LADM_COL/models/custom_model_directories_is_checked', self.offline_models_radio_button.isChecked())
        if self.offline_models_radio_button.isChecked():
            settings.setValue('Asistente-LADM_COL/models/custom_models', self.custom_model_directories_line_edit.text())

        settings.setValue('Asistente-LADM_COL/quality/too_long_tolerance', int(self.txt_too_long_tolerance.text()) or DEFAULT_TOO_LONG_BOUNDARY_SEGMENTS_TOLERANCE)
        settings.setValue('Asistente-LADM_COL/quality/use_roads', self.chk_use_roads.isChecked())

        settings.setValue('Asistente-LADM_COL/automatic_values/automatic_values_in_batch_mode', self.chk_automatic_values_in_batch_mode.isChecked())
        settings.setValue('Asistente-LADM_COL/sources/document_repository', self.connection_box.isChecked())

        endpoint = self.txt_service_endpoint.text().strip()
        settings.setValue('Asistente-LADM_COL/source/service_endpoint', (endpoint[:-1] if endpoint.endswith('/') else endpoint) or DEFAULT_ENDPOINT_SOURCE_SERVICE)

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

            self.qgis_utils.automatic_namespace_local_id_configuration_changed(self._db)

    def restore_settings(self):
        # Restore QSettings
        settings = QSettings()
        self.cbo_db_source.setCurrentIndex(
            self.cbo_db_source.findData(settings.value('Asistente-LADM_COL/db_connection_source', 'pg')))
        self.db_source_changed()
        self.txt_pg_host.setText(settings.value('Asistente-LADM_COL/pg/host'))
        self.txt_pg_port.setText(settings.value('Asistente-LADM_COL/pg/port'))

        dbname_setting = settings.value('Asistente-LADM_COL/pg/database')
        if self.selected_db_combobox.count():
            index = self.selected_db_combobox.findText(dbname_setting, Qt.MatchFixedString)
            if index >= 0:
                self.selected_db_combobox.setCurrentIndex(index)
        else:
            self.selected_db_combobox.addItem(dbname_setting)

        schema_setting = settings.value('Asistente-LADM_COL/pg/schema')
        if self.selected_schema_combobox.count():
            index = self.selected_schema_combobox.findText(schema_setting, Qt.MatchFixedString)
            if index >= 0:
                self.selected_schema_combobox.setCurrentIndex(index)
        else:
            self.selected_schema_combobox.addItem(schema_setting)

        self.txt_pg_user.setText(settings.value('Asistente-LADM_COL/pg/username'))
        self.txt_pg_password.setText(settings.value('Asistente-LADM_COL/pg/password'))
        self.txt_gpkg_file.setText(settings.value('Asistente-LADM_COL/gpkg/dbfile'))

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

        self.txt_service_endpoint.setText(settings.value('Asistente-LADM_COL/source/service_endpoint', DEFAULT_ENDPOINT_SOURCE_SERVICE))

    def db_source_changed(self):
        if self._db is not None:
            self._db.close_connection()

        self._db = None # Reset db connection
        if self.cbo_db_source.currentData() == 'pg':
            self.gpkg_config.setVisible(False)
            self.pg_config.setVisible(True)
        else:
            self.pg_config.setVisible(False)
            self.gpkg_config.setVisible(True)

    def test_connection(self):
        if self._db is not None:
            self._db.close_connection()

        self._db = None # Reset db connection
        db = self.get_db_connection(False)
        res, msg = db.test_connection()

        if db is not None:
            db.close_connection()

        self.show_message(msg, Qgis.Info if res else Qgis.Warning)
        self.log.logMessage("Test connection!", PLUGIN_NAME, Qgis.Info)

    def test_service(self):
        self.setEnabled(False)
        QCoreApplication.processEvents()
        res, msg = self.is_source_service_valid()
        self.setEnabled(True)
        self.show_message(msg['text'], msg['level'])

    def is_source_service_valid(self):
        res = False
        msg = {'text': '', 'level': Qgis.Warning}
        url = self.txt_service_endpoint.text().strip()
        if url:
            with OverrideCursor(Qt.WaitCursor):
                self.qgis_utils.status_bar_message_emitted.emit("Checking source service availability (this might take a while)...", 0)
                QCoreApplication.processEvents()
                if self.qgis_utils.is_connected(TEST_SERVER):

                    nam = QNetworkAccessManager()
                    request = QNetworkRequest(QUrl(url))
                    reply = nam.get(request)

                    loop = QEventLoop()
                    reply.finished.connect(loop.quit)
                    loop.exec_()

                    allData = reply.readAll()
                    response = QTextStream(allData, QIODevice.ReadOnly)
                    status = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
                    if status == 200:
                        try:
                            data = json.loads(response.readAll())
                            if 'id' in data and data['id'] == SOURCE_SERVICE_EXPECTED_ID:
                                res = True
                                msg['text'] = QCoreApplication.translate("SettingsDialog",
                                    "The tested service is valid to upload files!")
                                msg['level'] = Qgis.Info
                            else:
                                res = False
                                msg['text'] = QCoreApplication.translate("SettingsDialog",
                                    "The tested upload service is not compatible: no valid 'id' found in response.")
                        except json.decoder.JSONDecodeError as e:
                            res = False
                            msg['text'] = QCoreApplication.translate("SettingsDialog",
                                "Response from the tested service is not compatible: not valid JSON found.")
                    else:
                        res = False
                        msg['text'] = QCoreApplication.translate("SettingsDialog",
                            "There was a problem connecting to the server. The server might be down or the service cannot be reached at the given URL.")
                else:
                    res = False
                    msg['text'] = QCoreApplication.translate("SettingsDialog",
                        "There was a problem connecting to Internet.")

                self.qgis_utils.clear_status_bar_emitted.emit()
        else:
            res = False
            msg['text'] = QCoreApplication.translate("SettingsDialog", "Not valid service URL to test!")

        return (res, msg)

    def show_message(self, message, level):
        self.bar.pushMessage(message, level, 10)

    def set_connection_dirty(self, text):
        if not self.connection_is_dirty:
            self.connection_is_dirty = True

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

    def database_created(self, db_name):
        self.update_db_names()

        # select the database created by the user
        index = self.selected_db_combobox.findText(db_name, Qt.MatchFixedString)
        if index >= 0:
            self.selected_db_combobox.setCurrentIndex(index)

    def schema_created(self, schema_name):
        self.update_db_schemas()

        # select the database created by the user
        index = self.selected_schema_combobox.findText(schema_name, Qt.MatchFixedString)
        if index >= 0:
            self.selected_schema_combobox.setCurrentIndex(index)

    def show_modal_create_db(self):
        if self.cbo_db_source.currentData() == 'pg':
            tmp_db_conn = PGConnector('')
            dict_conn = self.read_connection_parameters()
            uri = tmp_db_conn.get_connection_uri(dict_conn, 'pg', level=0)
            test_conn = tmp_db_conn.test_connection(uri=uri, level=0)
            if test_conn[0]:
                create_db_dlg = DialogGetDBOrSchemaName(dict_conn, 'database', parent=self)
                create_db_dlg.db_or_schema_created.connect(self.database_created)
                create_db_dlg.setModal(True)
                create_db_dlg.exec_()
            else:
                self.show_message(QCoreApplication.translate("SettingsDialog", "First set the connection to the database before attempting to create a database."), Qgis.Warning)

    def show_modal_create_schema(self):
        if self.cbo_db_source.currentData() == 'pg':
            tmp_db_conn = PGConnector('')
            dict_conn = self.read_connection_parameters()
            uri = tmp_db_conn.get_connection_uri(dict_conn, 'pg', level=0)
            test_conn = tmp_db_conn.test_connection(uri=uri, level=0)

            if test_conn[0]:
                create_db_dlg = DialogGetDBOrSchemaName(self.read_connection_parameters(), 'schema', parent=self)
                create_db_dlg.db_or_schema_created.connect(self.schema_created)
                create_db_dlg.setModal(True)
                create_db_dlg.exec_()
            else:
                self.show_message(QCoreApplication.translate("SettingsDialog", "First set the connection to the database before attempting to create a schema."), Qgis.Warning)
