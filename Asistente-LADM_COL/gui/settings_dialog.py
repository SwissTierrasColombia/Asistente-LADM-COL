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

from qgis.core import QgsProject, QgsVectorLayer
from qgis.gui import QgsMessageBar
from qgis.PyQt.QtCore import Qt, QSettings
from qgis.PyQt.QtWidgets import QDialog, QSizePolicy, QGridLayout

from ..utils.qt_utils import make_file_selector
from ..utils import get_ui_class
from ..config.table_mapping_config import *
from ..lib.dbconnector.pg_connector import PGConnector
from ..lib.dbconnector.gpkg_connector import GPKGConnector

DIALOG_UI = get_ui_class('settings_dialog.ui')

class SettingsDialog(QDialog, DIALOG_UI):
    def __init__(self, iface, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface

        self.cbo_db_source.clear()
        self.cbo_db_source.addItem(self.tr('PostgreSQL / PostGIS'), 'pg')
        self.cbo_db_source.addItem(self.tr('GeoPackage'), 'gpkg')
        self.cbo_db_source.currentIndexChanged.connect(self.db_source_changed)

        # Set connections
        self.buttonBox.accepted.connect(self.accepted)
        self.btn_test_connection.clicked.connect(self.test_connection)

        # Trigger some default behaviours
        self.restore_settings()

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.setLayout(QGridLayout())
        #self.tabWidget.currentWidget().layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

    def accepted(self):
        print("Accepted!")
        self.save_settings()

    def save_settings(self):
        # Save QSettings
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/db_connection_source', self.cbo_db_source.currentData())
        settings.setValue('Asistente-LADM_COL/pg/host', self.txt_pg_host.text().strip())
        settings.setValue('Asistente-LADM_COL/pg/port', self.txt_pg_port.text().strip())
        settings.setValue('Asistente-LADM_COL/pg/database', self.txt_pg_database.text().strip())
        settings.setValue('Asistente-LADM_COL/pg/schema', self.txt_pg_schema.text().strip())
        settings.setValue('Asistente-LADM_COL/pg/user', self.txt_pg_user.text().strip())
        settings.setValue('Asistente-LADM_COL/pg/password', self.txt_pg_password.text().strip())
        settings.setValue('Asistente-LADM_COL/gpkg/dbfile', self.txt_gpkg_file.text().strip())

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

    def db_source_changed(self):
        if self.cbo_db_source.currentData() == 'pg':
            self.gpkg_config.setVisible(False)
            self.pg_config.setVisible(True)
        else:
            self.pg_config.setVisible(False)
            self.gpkg_config.setVisible(True)

    def test_connection(self):
        uri = self.get_connection_uri()
        if self.cbo_db_source.currentData() == 'pg':
            db = PGConnector(uri, self.txt_pg_schema.text().strip())
        elif self.cbo_db_source.currentData() == 'gpkg':
            db = GPKGConnector(uri)
        res, msg = db.test_connection()
        self.show_message(msg, QgsMessageBar.INFO if res else QgsMessageBar.WARNING)
        print("Test connection!")

    def show_message(self, message, level):
        self.bar.pushMessage(message, level, 10)

    def get_connection_uri(self):
        uri = []
        if self.cbo_db_source.currentData() == 'pg':
            uri += ['dbname={}'.format(self.txt_pg_database.text().strip())]
            uri += ['user={}'.format(self.txt_pg_user.text().strip())]
            if self.txt_pg_password.text().strip():
                uri += ['password={}'.format(self.txt_pg_password.text().strip())]
            uri += ['host={}'.format(self.txt_pg_host.text().strip())]
            if self.txt_pg_port.text().strip():
                uri += ['port={}'.format(self.txt_pg_port.text().strip())]
        elif self.cbo_db_source.currentData() == 'gpkg':
            uri = [self.txt_gpkg_file.text().strip()]
        return ' '.join(uri)
