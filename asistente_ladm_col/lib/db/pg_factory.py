# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-02-21
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
from asistente_ladm_col.lib.db.db_factory import DBFactory
from asistente_ladm_col.gui.db_panel.pg_config_panel import PGConfigPanel
from asistente_ladm_col.lib.db.pg_connector import PGConnector
from asistente_ladm_col.logic.ladm_col.pg_ladm_query import PGLADMQuery


class PGFactory(DBFactory):
    def __init__(self):
        DBFactory.__init__(self)
        self._engine = "pg"

    def get_name(self):
        return "PostgreSQL/PostGIS"

    def get_mbaker_db_ili_mode(self):
        from QgisModelBaker.libili2db.globals import DbIliMode
        return DbIliMode.ili2pg

    def get_config_panel(self, parent):
        return PGConfigPanel(parent)

    def get_db_connector(self, parameters=dict()):
        return PGConnector(None, parameters)

    def get_ladm_queries(self, qgis_utils):
        return PGLADMQuery(qgis_utils)

    def set_ili2db_configuration_params(self, params, configuration):
        """
        ili2db parameters

        :param params:
        :param configuration:
        :return:
        """
        configuration.tool_name = 'pg'
        configuration.dbhost = params['host']
        configuration.dbport = params['port']
        configuration.dbusr = params['username']
        configuration.database = params['database']
        configuration.dbschema = params['schema']
        configuration.dbpwd = params['password']
