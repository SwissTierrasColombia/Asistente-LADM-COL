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
import os

import qgis.utils
from qgis.PyQt.QtCore import QCoreApplication

from .db_connector import DBConnector


class GPKGConnector(DBConnector):
    def __init__(self, uri, schema=None, conn_dict={}):
        DBConnector.__init__(self, uri, schema)
        self.mode = 'gpkg'
        self.uri = uri if uri is not None else self.get_connection_uri(conn_dict, self.mode)
        self.conn = None
        self.provider = 'ogr'

        self.dict_conn_params = {'dbfile': self.uri}

    def test_connection(self):
        try:
            if not os.path.exists(self.uri):
                raise Exception("GeoPackage file not found.")
            self.conn = qgis.utils.spatialite_connect(self.uri)
        except Exception as e:
            return (False, QCoreApplication.translate("GPKGConnector",
                    "There was an error connecting to the database: {}").format(e))
        return (True, QCoreApplication.translate("GPKGConnector",
                "Connection to GeoPackage successful!"))

    def save_connection(self):
        self.conn = qgis.utils.spatialite_connect(self.uri)

    def validate_db(self):
        pass

    def get_uri_for_layer(self, layer_name, geometry_type=None):
        return (True, '{uri}|layername={table}'.format(
                uri=self.uri,
                table=layer_name.lower()
            ))

    def get_models(self):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT modelname, content
                          FROM t_ili2db_model""")
        return cursor
