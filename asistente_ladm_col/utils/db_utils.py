# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-07-19
        git sha              : :%H$
        copyright            : (C) 2019 by Leo Cardona (BSF Swissphoto)
        email                : leo dot cardona dot p at gmail dot com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
 """
from qgis.PyQt.QtCore import (pyqtSignal,
                              QCoreApplication,
                              QObject,
                              QSettings)

from qgis.core import (QgsApplication,
                       Qgis)
from ..config.config_db_supported import ConfigDbSupported
from ..config.general_config import (COLLECTED_DB_SOURCE,
                                     PLUGIN_NAME,
                                     OFFICIAL_DB_SOURCE)

from ..lib.db.db_connector import DBConnector


class DbUtils(QObject):
    db_connection_changed = pyqtSignal(DBConnector, bool)  # dbconn, ladm_col_db
    official_db_connection_changed = pyqtSignal(DBConnector, bool)  # dbconn, ladm_col_db

    def __init__(self):
        QObject.__init__(self)
        self.settings = QSettings()
        self.conf_db = ConfigDbSupported()
        self.log = QgsApplication.messageLog()

        self._db_sources = {
            COLLECTED_DB_SOURCE: None,
            OFFICIAL_DB_SOURCE: None
        }

        # Init collected db source
        self.update_db_source()

    def update_db_source(self, db_source=COLLECTED_DB_SOURCE):
        db_connection_source = self.settings.value('Asistente-LADM_COL/db/{db_source}/db_connection_source'.format(db_source=db_source))

        if db_connection_source:
            db_factory = self.conf_db.get_db_items()[db_connection_source]
            parameters_conn = db_factory.get_parameters_conn(db_source=db_source)
            db = db_factory.get_db_connector(parameters_conn)
            db.open_connection()  # Open db connection
        else:
            # when the connection parameters are not filling we use empty values
            db_connection_source = "pg"
            db_factory = self.conf_db.get_db_items()[db_connection_source]
            parameters_conn = {'database': '', 'host': '', 'password': '', 'port': '', 'schema': '', 'username': ''}
            db = db_factory.get_db_connector(parameters_conn)

        self.set_db_source(db, db_source)

    def get_db_source(self, db_source=COLLECTED_DB_SOURCE):
        return self._db_sources[db_source]

    def set_db_source(self, db_connector, db_source=COLLECTED_DB_SOURCE):
        try:
            if self._db_sources[db_source]:
                self._db_sources[db_source].close_connection()
            self._db_sources[db_source] = db_connector
        except:
            self.log.logMessage(QCoreApplication.translate("DbUtils", "An error occurred while trying to close the connection"),
                                PLUGIN_NAME,
                                Qgis.Info)

    def close_db_sources(self):
        for _db_source in self._db_sources:
            if self._db_sources[_db_source]:
                self._db_sources[_db_source].close_connection()

    def get_db_source_test(self, scope, parameters):
        """
        This function was implemented for the tests
        """
        db_connection_source = scope
        db_factory = self.conf_db.get_db_items()[db_connection_source]
        parameters_conn = parameters
        db = db_factory.get_db_connector(parameters_conn)
        db.open_connection()  # Open db connection

        return db