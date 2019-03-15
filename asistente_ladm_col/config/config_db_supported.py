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

from ..db_support.pg_admin import PgAdmin
from ..db_support.gpkg_admin import GpkgAdmin
from ..db_support.mssql_admin import MssqlAdmin


class ConfigDbSupported(QObject):

    def __init__(self):
        self.id_default_db = None
        self._db_items = dict()
        self._init_db_items()

    def _init_db_items(self):
        db_item = PgAdmin()
        self._db_items[db_item.get_id()] = db_item
        self.id_default_db = db_item.get_id()

        db_item = GpkgAdmin()
        self._db_items[db_item.get_id()] = db_item

        db_item = MssqlAdmin()
        self._db_items[db_item.get_id()] = db_item

    def get_db_items(self):
        return self._db_items

    def get_db_admin(self, db_type):
        result = None

        if db_type in self._db_items:
            result = self._db_items[db_type]

        return result
