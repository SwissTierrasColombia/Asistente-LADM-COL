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

from .db_connector import (DBConnector, EnumTestLevel)


class GPKGConnector(DBConnector):

    _PROVIDER_NAME = 'ogr'

    def __init__(self, uri, schema=None, conn_dict={}):
        DBConnector.__init__(self, uri, schema, conn_dict)
        self.mode = 'gpkg'
        self.conn = None
        self.provider = 'ogr'

    @DBConnector.uri.setter
    def uri(self, value):
        self._dict_conn_params = {'dbfile': value}
        self._uri = value

    def test_connection(self, test_level=EnumTestLevel.LADM):
        try:

            # file no exist, but directory must exist
            if test_level & EnumTestLevel.CREATE_SCHEMA:
                directory = os.path.dirname(self._uri)

                if not os.path.exists(directory):
                    raise Exception("GeoPackage directory file not found.")
            elif not os.path.exists(self._uri):
                raise Exception("GeoPackage file not found.")
            self.conn = qgis.utils.spatialite_connect(self._uri)
            # TODO verify EnumTestLevel.LADM
        except Exception as e:
            return (False, QCoreApplication.translate("GPKGConnector",
                    "There was an error connecting to the database: {}").format(e))
        return (True, QCoreApplication.translate("GPKGConnector",
                "Connection to GeoPackage successful!"))

    def save_connection(self):
        self.conn = qgis.utils.spatialite_connect(self._uri)

    def validate_db(self):
        pass

    def get_uri_for_layer(self, layer_name, geometry_type=None):
        return (True, '{uri}|layername={table}'.format(
                uri=self._uri,
                table=layer_name.lower()
            ))

    def get_models(self):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT modelname, content
                          FROM t_ili2db_model""")
        return cursor

    def is_ladm_layer(self, layer):
        result = False
        if layer.dataProvider().name() == GPKGConnector._PROVIDER_NAME:
            # Dbfile should be equal to _uri
            dbfile = layer.source().split('|')[0]
            result = (dbfile == self._uri)
        return result

    def get_ladm_layer_name(self, layer, validate_is_ladm=False):
        name = None
        if validate_is_ladm:
            if self.is_ladm_layer(layer):
                name = layer.source().split('|layername=')[1]
        else:
            name = layer.source().split('|layername=')[1]
        return name

    def get_description_conn_string(self):
        result = None
        if self.dict_conn_params['dbfile']:
            result = os.path.basename(self.dict_conn_params['dbfile'])
        return result

    def get_connection_uri(self, dict_conn, level=1):
        return dict_conn['dbfile']

    def close_connection(self):
        pass  # this connection does not need to be closed
