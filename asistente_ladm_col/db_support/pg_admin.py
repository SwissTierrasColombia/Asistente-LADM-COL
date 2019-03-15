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
from .db_admin import DbAdmin

from .pg_config_panel import PgConfigPanel
from ..lib.dbconnector.pg_connector import PGConnector
from .pg_ladm_layer_tester import PgLadmLayerTester
from QgisModelBaker.libili2db.ili2dbconfig import (SchemaImportConfiguration,
                                                   ImportDataConfiguration,
                                                   ExportConfiguration,
                                                   BaseConfiguration)


class PgAdmin(DbAdmin):
    def __init__(self):
        DbAdmin.__init__(self)
        self._mode = "pg"

    def get_name(self):
        return "PostgreSQL / PostGIS"

    def get_id(self):
        return "pg"

    def get_model_baker_tool_name(self):
        return "ili2pg"

    def get_config_panel(self):
        return PgConfigPanel()

    def get_db_connector(self, parameters):
        return PGConnector(None, parameters['schema'], parameters)

    def get_schema_import_configuration(self, params):
        configuration = SchemaImportConfiguration()

        configuration.tool_name = 'pg'
        configuration.dbhost = params['host']
        configuration.dbport = params['port']
        configuration.dbusr = params['username']
        configuration.database = params['database']
        configuration.dbschema = params['schema']
        configuration.dbpwd = params['password']

        return configuration

    def get_import_configuration(self, params):
        configuration = ImportDataConfiguration()

        configuration.dbhost = params['host']
        configuration.dbport = params['port']
        configuration.dbusr = params['username']
        configuration.database = params['database']
        configuration.dbschema = params['schema']
        configuration.dbpwd = params['password']

        return configuration

    def get_export_configuration(self, params):
        configuration = ExportConfiguration()

        configuration.dbhost = params['host']
        configuration.dbport = params['port']
        configuration.dbusr = params['username']
        configuration.database = params['database']
        configuration.dbschema = params['schema']
        configuration.dbpwd = params['password']

        return configuration

    def get_ladm_layer_tester(self):
        return PgLadmLayerTester()