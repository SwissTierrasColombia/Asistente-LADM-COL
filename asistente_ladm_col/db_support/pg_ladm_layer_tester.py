# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-03-15
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
from .db_ladm_layer_tester import DbLadmLayerTester
from qgis.core import (QgsDataSourceUri)


class PgLadmLayerTester(DbLadmLayerTester):
    _PROVIDER_NAME = 'postgres'

    def __init__(self):
        pass

    def is_ladm_layer(self, layer, db):
        result = False
        if layer.dataProvider().name() == PgLadmLayerTester._PROVIDER_NAME:
            layer_uri = layer.dataProvider().uri()
            db_uri = QgsDataSourceUri(db.uri)

            result = (layer_uri.schema() == db.schema and \
                    layer_uri.database() == db_uri.database() and \
                    layer_uri.host() == db_uri.host() and \
                    layer_uri.port() == db_uri.port() and \
                    layer_uri.username() == db_uri.username() and \
                    layer_uri.password() == db_uri.password())

        return result