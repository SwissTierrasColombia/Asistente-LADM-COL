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
import os

from qgis.core import QgsProject, QgsVectorLayer, Qgis, QgsApplication
from qgis.gui import QgsMessageBar
from qgis.PyQt.QtCore import Qt, QSettings
from qgis.PyQt.QtWidgets import QDialog, QSizePolicy, QGridLayout

from ..config.general_config import (
    DEFAULT_TOO_LONG_BOUNDARY_SEGMENTS_TOLERANCE
)
from ..lib.dbconnector.gpkg_connector import GPKGConnector
from ..lib.dbconnector.pg_connector import PGConnector
from ..utils import get_ui_class
from ..utils.qt_utils import make_file_selector, get_plugin_metadata

DIALOG_UI = get_ui_class('settings_dialog.ui')

class SettingsDialog(QDialog, DIALOG_UI):
    def __init__(self, iface=None, parent=None, qgis_utils=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._db = None
        self.qgis_utils = qgis_utils
        self.plugin_name = get_plugin_metadata('asistente_ladm_col', 'name')

        self.cbo_db_source.clear()
        self.cbo_db_source.addItem(self.tr('PostgreSQL / PostGIS'), 'pg')
        self.cbo_db_source.addItem(self.tr('GeoPackage'), 'gpkg')
        self.cbo_db_source.currentIndexChanged.connect(self.db_source_changed)

        # Set connections
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.helpRequested.connect(self.show_help)
        self.btn_test_connection.clicked.connect(self.test_connection)

        # Trigger some default behaviours
        self.restore_settings()

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.setLayout(QGridLayout())
        #self.tabWidget.currentWidget().layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

    def get_db_connection(self):
        if self._db is not None:
            self.log.logMessage("Returning existing db connection...", self.plugin_name, Qgis.Info)
            return self._db
        else:
            self.log.logMessage("Getting new db connection...", self.plugin_name, Qgis.Info)
            dict_conn = self.read_connection_parameters()
            uri = self.get_connection_uri(dict_conn)
            if self.cbo_db_source.currentData() == 'pg':
                db = PGConnector(uri, dict_conn['schema'])
            else:
                db = GPKGConnector(uri)
            return db

    def accepted(self):
        self._db = None # Reset db connection
        self._db = self.get_db_connection()
        self.save_settings()

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
        dict_conn['port'] = self.txt_pg_port.text().strip() or 5432
        dict_conn['database'] = self.txt_pg_database.text().strip()
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
        settings.setValue('Asistente-LADM_COL/pg/database', dict_conn['database'])
        settings.setValue('Asistente-LADM_COL/pg/schema', dict_conn['schema'])
        settings.setValue('Asistente-LADM_COL/pg/user', dict_conn['user'])
        settings.setValue('Asistente-LADM_COL/pg/password', dict_conn['password'])
        settings.setValue('Asistente-LADM_COL/gpkg/dbfile', dict_conn['dbfile'])

        settings.setValue('Asistente-LADM_COL/quality/too_long_tolerance', int(self.txt_too_long_tolerance.text()) or DEFAULT_TOO_LONG_BOUNDARY_SEGMENTS_TOLERANCE)

        settings.setValue('Asistente-LADM_COL/automatic_values/disable_automatic_fields', self.chk_disable_automatic_fields.isChecked())

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

        self.chk_disable_automatic_fields.setChecked(settings.value('Asistente-LADM_COL/automatic_values/disable_automatic_fields', True, bool))
        self.namespace_collapsible_group_box.setChecked(settings.value('Asistente-LADM_COL/automatic_values/namespace_enabled', True, bool))
        self.chk_local_id.setChecked(settings.value('Asistente-LADM_COL/automatic_values/local_id_enabled', True, bool))
        self.txt_namespace.setText(str(settings.value('Asistente-LADM_COL/automatic_values/namespace_prefix', "")))

    def db_source_changed(self):
        self._db = None
        if self.cbo_db_source.currentData() == 'pg':
            self.gpkg_config.setVisible(False)
            self.pg_config.setVisible(True)
        else:
            self.pg_config.setVisible(False)
            self.gpkg_config.setVisible(True)

    def test_connection(self):
        self._db = None # Reset db connection
        res, msg = self.get_db_connection().test_connection()
        self.show_message(msg, Qgis.Info if res else Qgis.Warning)
        self.log.logMessage("Test connection!", self.plugin_name, Qgis.Info)

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

    def show_help(self):
        self.qgis_utils.show_help("settings")
