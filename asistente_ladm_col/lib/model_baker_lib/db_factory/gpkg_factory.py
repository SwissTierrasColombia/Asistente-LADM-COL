
# -*- coding: utf-8 -*-
"""
/***************************************************************************
    begin                :    08/04/19
    git sha              :    :%H$
    copyright            :    (C) 2019 by Yesid Polania
    email                :    yesidpol.3@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from .db_factory import DbFactory
from asistente_ladm_col.lib.model_baker_lib.dbconnector.gpkg_connector import GPKGConnector
from .gpkg_layer_uri import GpkgLayerUri
from .gpkg_command_config_manager import GpkgCommandConfigManager


class GpkgFactory(DbFactory):
    """Creates an entire set of objects so that QgisModelBaker supports Geopackage database.
    """
    def get_db_connector(self, uri, schema):
        return GPKGConnector(uri, None)

    def get_db_command_config_manager(self, configuration):
        return GpkgCommandConfigManager(configuration)

    def get_layer_uri(self, uri):
        return GpkgLayerUri(uri)

    def pre_generate_project(self, configuration):
        return True, ''

    def post_generate_project_validations(self, configuration):
        return True, ''

    def get_specific_messages(self):
        messages = {
            'db_or_schema': 'database',
            'layers_source': 'GeoPackage'
        }

        return messages
