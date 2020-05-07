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
from asistente_ladm_col.gui.db_panel.gpkg_config_panel import GPKGConfigPanel
from asistente_ladm_col.lib.db.gpkg_connector import GPKGConnector
from asistente_ladm_col.logic.ladm_col.gpkg_ladm_query import GPKGLADMQuery


class GPKGFactory(DBFactory):
    def __init__(self):
        DBFactory.__init__(self)
        self._engine = "gpkg"

    def get_name(self):
        return 'GeoPackage'

    def get_model_baker_db_ili_mode(self):
        from QgisModelBaker.libili2db.globals import DbIliMode
        return DbIliMode.ili2gpkg

    def get_config_panel(self, parent):
        return GPKGConfigPanel(parent)

    def get_db_connector(self, parameters={}):
        return GPKGConnector(None, conn_dict=parameters)

    def get_ladm_queries(self):
        return GPKGLADMQuery()

    def set_ili2db_configuration_params(self, params, configuration):
        configuration.tool_name = 'gpkg'
        configuration.dbfile = params['dbfile']
