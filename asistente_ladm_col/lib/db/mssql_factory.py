# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-03-07
        git sha              : :%H$
        copyright            : (C) 2019 by Yesid Polanía (BSF Swissphoto)
        email                : yesidpol.3@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from .db_factory import DBFactory

from asistente_ladm_col.gui.db_panel.mssql_config_panel import MSSQLConfigPanel
from .mssql_connector import MSSQLConnector
from ...logic.ladm_col.qgis_ladm_query import QGISLADMQuery


class MSSQLFactory(DBFactory):

    def __init__(self):
        DBFactory.__init__(self)
        self._engine = "mssql"

    def get_name(self):
        return "MS SQL Server"

    def get_model_baker_db_ili_mode(self):
        from QgisModelBaker.libili2db.globals import DbIliMode
        return DbIliMode.ili2mssql

    def get_config_panel(self, parent):
        return MSSQLConfigPanel(parent)

    def get_db_connector(self, parameters=dict()):
        return MSSQLConnector(None, parameters)

    def set_ili2db_configuration_params(self, params, configuration):
        configuration.tool_name = 'mssql'
        configuration.dbhost = params['host'] or "localhost"
        configuration.dbport = params['port']
        configuration.dbinstance = params['instance']
        configuration.dbusr = params['username']
        configuration.database = params['database']
        configuration.dbschema = params['schema']
        configuration.dbpwd = params['password']
        configuration.db_odbc_driver = params['db_odbc_driver']

    def get_ladm_queries(self):
        return QGISLADMQuery()
