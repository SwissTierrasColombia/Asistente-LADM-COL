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

        for part in self.uri.split(' '):
            if 'host=' in part:
                self.host = part.split('host=')[1]
            elif 'port=' in part:
                self.port = part.split('port=')[1]
            elif 'dbname=' in part:
                self.dbname = part.split('dbname=')[1]
            elif 'user=' in part:
                self.user = part.split('user=')[1]
            elif 'password=' in part:
                self.password = part.split('password=')[1]

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

    def get_uri_without_password(self):
        uri_hide = [ part for part in self.uri.split(' ') if 'password' not in part]
        return ' '.join(uri_hide)

    def get_uri_without_schema(self):
        uri_hide = [ part for part in self.uri.split(' ') if 'schema' not in part]
        return ' '.join(uri_hide)
