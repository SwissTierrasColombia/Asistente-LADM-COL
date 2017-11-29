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
        self.conn = None

    def test_connection(self):
        pass

    def validate_db(self):
        pass

    def get_uri_for_layer(self, layer_name):
        pass

    def get_description(self):
        print(self.mode,self.uri,self.conn)
