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

from ..lib.db.pg_factory import PgFactory
from ..lib.db.gpkg_factory import GpkgFactory
from ..lib.db.mssql_factory import MssqlFactory


class ConfigDbSupported(QObject):

    def __init__(self):
        self.id_default_db = None
        self._db_items = dict()
        self._init_db_items()

    def _init_db_items(self):
        db_item = PgFactory()
        self._db_items[db_item.get_id()] = db_item
        self.id_default_db = db_item.get_id()

        db_item = GpkgFactory()
        self._db_items[db_item.get_id()] = db_item

        db_item = MssqlFactory()
        self._db_items[db_item.get_id()] = db_item

    def get_db_items(self):
        return self._db_items

    def get_db_admin(self, db_type):
        result = None

        if db_type in self._db_items:
            result = self._db_items[db_type]

        return result
