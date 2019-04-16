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
from qgis.PyQt.QtCore import QObject


class DbFactory(QObject):

    def __init__(self):
        self._mode = None

    def get_id(self):
        raise Exception('unimplemented method')

    def get_name(self):
        raise Exception('unimplemented method')

    def get_config_panel(self):
        raise Exception('unimplemented method')

    def get_model_baker_tool_name(self):
        raise Exception('unimplemented method')

    def get_db_connector(self, parameters):
        raise Exception('unimplemented method')

    def get_schema_import_configuration(self, params):
        raise Exception('unimplemented method')

    def get_import_configuration(self, params):
        raise Exception('unimplemented method')

    def get_export_configuration(self, params):
        raise Exception('unimplemented method')
