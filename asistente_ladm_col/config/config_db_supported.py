from qgis.PyQt.QtCore import QObject

from asistente_ladm_col.lib.db.pg_factory import PGFactory
from asistente_ladm_col.lib.db.gpkg_factory import GPKGFactory

from QgisModelBaker.libili2db.globals import DbIliMode
from QgisModelBaker.libqgsprojectgen.db_factory.db_simple_factory import available_database_factories


class ConfigDBsSupported(QObject):

    def __init__(self):
        self.id_default_db = None
        self._db_factories = dict()
        self._init_db_factories()

    def _init_db_factories(self):
        db_factory = PGFactory()
        self._db_factories[db_factory.get_id()] = db_factory
        self.id_default_db = db_factory.get_id()  # Make PostgreSQL the default DB engine

        db_factory = GPKGFactory()
        self._db_factories[db_factory.get_id()] = db_factory

        if DbIliMode.mssql in available_database_factories:
            from asistente_ladm_col.lib.db.mssql_factory import MSSQLFactory
            db_factory = MSSQLFactory()
            self._db_factories[db_factory.get_id()] = db_factory

    def get_db_factories(self):
        return self._db_factories

    def get_db_factory(self, engine):
        return self._db_factories[engine] if engine in self._db_factories else None
