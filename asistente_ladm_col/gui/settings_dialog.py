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
                              QEventLoop
                              )
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
from ..lib.dbconnector.db_connector import DBConnector
from ..lib.dbconnector.gpkg_connector import GPKGConnector
from ..lib.dbconnector.pg_connector import PGConnector
from ..utils import get_ui_class
from ..utils.qt_utils import OverrideCursor

DIALOG_UI = get_ui_class('settings_dialog.ui')

class SettingsDialog(QDialog, DIALOG_UI):

    cache_layers_and_relations_requested = pyqtSignal(DBConnector)
    refresh_menus_requested = pyqtSignal(DBConnector)
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
        self.cbo_db_source.addItem(self.tr('PostgreSQL / PostGIS'), 'pg')
        self.cbo_db_source.addItem(self.tr('GeoPackage'), 'gpkg')
        self.cbo_db_source.currentIndexChanged.connect(self.db_source_changed)

        # Set connections
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.helpRequested.connect(self.show_help)
        self.btn_test_connection.clicked.connect(self.test_connection)
        self.btn_get_from_project_generator.clicked.connect(self.get_from_project_generator)
        self.txt_pg_host.textEdited.connect(self.set_connection_dirty)
        self.txt_pg_port.textEdited.connect(self.set_connection_dirty)
        self.txt_pg_database.textEdited.connect(self.set_connection_dirty)
        self.txt_pg_schema.textEdited.connect(self.set_connection_dirty)
        self.txt_pg_user.textEdited.connect(self.set_connection_dirty)
        self.txt_pg_password.textEdited.connect(self.set_connection_dirty)
        self.txt_gpkg_file.textEdited.connect(self.set_connection_dirty)
        self.btn_test_service.clicked.connect(self.test_service)
        self.chk_use_roads.toggled.connect(self.update_images_state)

        # Trigger some default behaviours
        self.restore_settings()

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.setLayout(QGridLayout())
        #self.tabWidget.currentWidget().layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

    def get_db_connection(self, update_connection=True):
        if self._db is not None:
            self.log.logMessage("Returning existing db connection...", PLUGIN_NAME, Qgis.Info)
            return self._db
        else:
            self.log.logMessage("Getting new db connection...", PLUGIN_NAME, Qgis.Info)
            dict_conn = self.read_connection_parameters()
            uri = self.get_connection_uri(dict_conn)
            if self.cbo_db_source.currentData() == 'pg':
                db = PGConnector(uri, dict_conn['schema'])
            else:
                db = GPKGConnector(uri)

            if update_connection:
                self._db = db

            return db

    def accepted(self):
        if self._db is not None:
            self._db.close_connection()

        self._db = None # Reset db connection
        self._db = self.get_db_connection()

        if self.connection_is_dirty:
            self.connection_is_dirty = False
            if self._db.test_connection()[0]:
                self.cache_layers_and_relations_requested.emit(self._db)
                self.refresh_menus_requested.emit(self._db)

        self.save_settings()

    def reject(self):
        self.restore_settings()
        self.connection_is_dirty = False
        self.done(0)

    def set_db_connection(self, mode, dict_conn):
        """
        To be used by external scripts
        """
        self.cbo_db_source.setCurrentIndex(self.cbo_db_source.findData(mode))
        self.db_source_changed()

        if self.cbo_db_source.currentData() == 'pg':
            self.txt_pg_host.setText(dict_conn['host'])
            self.txt_pg_port.setText(dict_conn['port'])
            self.txt_pg_database.setText(dict_conn['database'])
            self.txt_pg_schema.setText(dict_conn['schema'])
            self.txt_pg_user.setText(dict_conn['user'])
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
        dict_conn['database'] = "'{}'".format(self.txt_pg_database.text().strip())
        dict_conn['schema'] = self.txt_pg_schema.text().strip() or 'public'
        dict_conn['user'] = self.txt_pg_user.text().strip()
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
        settings.setValue('Asistente-LADM_COL/pg/user', dict_conn['user'])
        settings.setValue('Asistente-LADM_COL/pg/password', dict_conn['password'])
        settings.setValue('Asistente-LADM_COL/gpkg/dbfile', dict_conn['dbfile'])

        settings.setValue('Asistente-LADM_COL/quality/too_long_tolerance', int(self.txt_too_long_tolerance.text()) or DEFAULT_TOO_LONG_BOUNDARY_SEGMENTS_TOLERANCE)
        settings.setValue('Asistente-LADM_COL/quality/use_roads', self.chk_use_roads.isChecked())

        settings.setValue('Asistente-LADM_COL/automatic_values/automatic_values_in_batch_mode', self.chk_automatic_values_in_batch_mode.isChecked())
        settings.setValue('Asistente-LADM_COL/sources/document_repository', self.connexion_box.isChecked())

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
        self.txt_pg_database.setText(settings.value('Asistente-LADM_COL/pg/database'))
        self.txt_pg_schema.setText(settings.value('Asistente-LADM_COL/pg/schema'))
        self.txt_pg_user.setText(settings.value('Asistente-LADM_COL/pg/user'))
        self.txt_pg_password.setText(settings.value('Asistente-LADM_COL/pg/password'))
        self.txt_gpkg_file.setText(settings.value('Asistente-LADM_COL/gpkg/dbfile'))

        self.txt_too_long_tolerance.setText(str(settings.value('Asistente-LADM_COL/quality/too_long_tolerance', DEFAULT_TOO_LONG_BOUNDARY_SEGMENTS_TOLERANCE)))
        use_roads = settings.value('Asistente-LADM_COL/quality/use_roads', True, bool)
        self.chk_use_roads.setChecked(use_roads)
        self.update_images_state(use_roads)

        self.chk_automatic_values_in_batch_mode.setChecked(settings.value('Asistente-LADM_COL/automatic_values/automatic_values_in_batch_mode', True, bool))
        self.connexion_box.setChecked(settings.value('Asistente-LADM_COL/sources/document_repository', True, bool))
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

    def get_from_project_generator(self):
        settings = QSettings()
        host = settings.value('QgsProjectGenerator/ili2pg/host')
        port = settings.value('QgsProjectGenerator/ili2pg/port')
        database = settings.value('QgsProjectGenerator/ili2pg/database')
        schema = settings.value('QgsProjectGenerator/ili2pg/schema')
        user = settings.value('QgsProjectGenerator/ili2pg/user')
        password = settings.value('QgsProjectGenerator/ili2pg/password')
        dbfile = settings.value('QgsProjectGenerator/ili2gpkg/dbfile')

        if self.cbo_db_source.currentData() == 'pg':
            msg_pg = QCoreApplication.translate("SettingsDialog",
                "Connection parameters couldn't be imported from Project Generator. Are you sure there are connection parameters to import?")
            if host is None and port is None and database is None and schema is None and user is None and password is None:
                self.show_message(msg_pg, Qgis.Warning)
            else:
                self.connection_is_dirty = True
                if host:
                    self.txt_pg_host.setText(host)
                if port:
                    self.txt_pg_port.setText(port)
                if database:
                    self.txt_pg_database.setText(database)
                if schema:
                    self.txt_pg_schema.setText(schema)
                if user:
                    self.txt_pg_user.setText(user)
                if password:
                    self.txt_pg_password.setText(password)

        elif self.cbo_db_source.currentData() == 'gpkg':
            msg_gpkg = QCoreApplication.translate("SettingsDialog",
                "Connection parameters couldn't be imported from Project Generator. Are you sure there are connection parameters to import?")
            if dbfile is None:
                self.show_message(msg_gpkg, Qgis.Warning)
            else:
                self.connection_is_dirty = True
                self.txt_gpkg_file.setText(dbfile)

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

    def get_connection_uri(self, dict_conn):
        uri = []
        if self.cbo_db_source.currentData() == 'pg':
            uri += ['host={}'.format(dict_conn['host'])]
            uri += ['port={}'.format(dict_conn['port'])]
            if dict_conn['database']:
                uri += ['dbname={}'.format(dict_conn['database'])]
            if dict_conn['user']:
                uri += ['user={}'.format(dict_conn['user'])]
            if dict_conn['password']:
                uri += ['password={}'.format(dict_conn['password'])]
        elif self.cbo_db_source.currentData() == 'gpkg':
            uri = [dict_conn['dbfile']]
        return ' '.join(uri)

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
