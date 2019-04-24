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
from .db_factory import DbFactory
from ...gui.db_panel.gpkg_config_panel import GpkgConfigPanel
from ...lib.db.gpkg_connector import GPKGConnector


class GpkgFactory(DbFactory):

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

    def set_db_configuration_params(self, params, configuration):
        configuration.tool_name = 'gpkg'
        configuration.dbfile = params['dbfile']

