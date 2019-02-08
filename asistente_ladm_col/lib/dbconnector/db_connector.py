# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2017-11-20
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
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

class DBConnector(QObject):
    '''SuperClass for all DB connectors.'''
    def __init__(self, uri, schema=None):
        QObject.__init__(self)
        self.mode = ''
        self.provider = '' # QGIS provider name. e.g., postgres
        self.uri = uri
        self.schema = schema
        self.conn = None
        self.dict_connection_params = dict()

    def test_connection(self):
        pass

    def validate_db(self):
        pass

    def close_connection(self):
        pass

    def get_uri_for_layer(self, layer_name, geometry_type=None):
        pass

    def get_description(self):
        return "Current connection details: '{}' -> {} {}".format(
            self.mode,
            self.uri,
            'schema:{}'.format(self.schema) if self.schema else '')

    def get_models(self, schema=None):
        pass

    def get_display_conn_string(self):
        # Do not use to connect to a DB, only for display purposes
        tmp_dict_conn_params = self.dict_connection_params
        if 'password' in tmp_dict_conn_params:
            del tmp_dict_conn_params['password']
        return ' '.join(["{}={}".format(k, v) for k, v in tmp_dict_conn_params.items()])
