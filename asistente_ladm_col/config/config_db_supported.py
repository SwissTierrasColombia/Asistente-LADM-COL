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

from asistente_ladm_col.lib.db.pg_factory import PgFactory
from asistente_ladm_col.lib.db.gpkg_factory import GpkgFactory


class ConfigDbSupported(QObject):

    def __init__(self):
        self.id_default_db = None
        self._db_factories = dict()
        self._init_db_factories()

    def _init_db_factories(self):
        db_factory = PgFactory()
        self._db_factories[db_factory.get_id()] = db_factory
        self.id_default_db = db_factory.get_id()  # Make PostgreSQL the default DB engine

        db_factory = GpkgFactory()
        self._db_factories[db_factory.get_id()] = db_factory

    def get_db_factories(self):
        return self._db_factories

    def get_db_factory(self, id):
        return self._db_factories[id] if id in self._db_factories else None