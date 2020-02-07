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

from asistente_ladm_col.config.config_db_supported import ConfigDbSupported
from asistente_ladm_col.config.general_config import (COLLECTED_DB_SOURCE,
                                                      SUPPLIES_DB_SOURCE)
from asistente_ladm_col.lib.db.db_connector import DBConnector
from asistente_ladm_col.lib.logger import Logger


class ConnectionManager(QObject):
    """
    Access point to get and set DB Connectors used by the plugin.

    The plugin uses a DB Connector for Cadastral data collection (barrido) and one for the Supplies cadastral data.
    Other connections might be needed (e.g., while retrieving databases for the server in the settings dialog, but they
    are not handled by this class).
    """
    db_connection_changed = pyqtSignal(DBConnector, bool, str)  # dbconn, ladm_col_db, db_source

    def __init__(self):
        QObject.__init__(self)
        self.logger = Logger()
        self.dbs_supported = ConfigDbSupported()

        self._db_sources = {  # Values are DB Connectors
            COLLECTED_DB_SOURCE: None,
            SUPPLIES_DB_SOURCE: None
        }

    def update_db_connector_for_source(self, db_source=COLLECTED_DB_SOURCE):
        db_connection_source = QSettings().value('Asistente-LADM_COL/db/{db_source}/db_connection_source'.format(db_source=db_source))

        if db_connection_source:
            db_factory = self.dbs_supported.get_db_factory(db_connection_source)
            dict_conn = db_factory.get_parameters_conn(db_source)
            db = db_factory.get_db_connector(dict_conn)
            db.open_connection()  # Open db connection
        else:
            # By default, we use PostgreSQL
            # when the connection parameters are not filled we use empty values
            db_connection_source = "pg"
            db_factory = self.dbs_supported.get_db_factory(db_connection_source)
            db = db_factory.get_db_connector()

        self.set_db_connector_for_source(db, db_source)

    def get_db_connector_from_source(self, db_source=COLLECTED_DB_SOURCE):
        if self._db_sources[db_source] is None:
            # obtain the connection of the database on demand
            self.update_db_connector_for_source(db_source)
        return self._db_sources[db_source]

    def set_db_connector_for_source(self, db_connector, db_source=COLLECTED_DB_SOURCE):
        try:
            if self._db_sources[db_source]:
                self._db_sources[db_source].close_connection()
            self._db_sources[db_source] = db_connector
        except:
            self.logger.info(__name__, QCoreApplication.translate("ConnectionManager", "An error occurred while trying to close the connection."))

    def close_db_connections(self):
        for _db_source in self._db_sources:
            if self._db_sources[_db_source]:
                self._db_sources[_db_source].close_connection()

    def get_db_connector_for_tests(self, scope, parameters):
        """
        This function is implemented for tests
        """
        db_connection_source = scope
        db_factory = self.dbs_supported.get_db_factory(db_connection_source)
        db = db_factory.get_db_connector(parameters)
        db.open_connection()

        return db