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
from .gpkg_config_panel import GpkgConfigPanel
from ..lib.dbconnector.gpkg_connector import GPKGConnector
from .none_ladm_layer_tester import NoneLadmLayerTester
from QgisModelBaker.libili2db.ili2dbconfig import (SchemaImportConfiguration,
                                                   ImportDataConfiguration,
                                                   ExportConfiguration,
                                                   BaseConfiguration)

class GpkgAdmin(DbAdmin):

    def __init__(self):
        self._mode = "gpkg"

    def get_id(self):
        return 'gpkg'

    def get_name(self):
        return 'GeoPackage'

    def get_model_baker_tool_name(self):
        return "ili2gpkg"

    def get_config_panel(self):
        return GpkgConfigPanel()

    def get_db_connector(self, parameters):
        return GPKGConnector(None, conn_dict=parameters)

    def get_schema_import_configuration(self, params):
        configuration = SchemaImportConfiguration()
        configuration.tool_name = 'gpkg'
        configuration.dbfile = params['dbfile']

        return configuration

    def get_import_configuration(self, params):
        configuration = ImportDataConfiguration()
        configuration.dbfile = params['dbfile']
        return configuration

    def get_export_configuration(self, params):
        configuration = ExportConfiguration()
        configuration.dbfile = params['dbfile']
        return configuration

    def get_ladm_layer_tester(self):
        return NoneLadmLayerTester()