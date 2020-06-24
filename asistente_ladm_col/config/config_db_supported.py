from qgis.PyQt.QtCore import QObject

from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.db.pg_factory import PGFactory
from asistente_ladm_col.lib.db.gpkg_factory import GPKGFactory
from asistente_ladm_col.utils.mssql_utils import (is_libqt5sql5_odbc_available,
                                                  is_pyodbc_available)

from qgis.PyQt.QtCore import QCoreApplication


class ConfigDBsSupported(QObject):

    def __init__(self):
        self.id_default_db = None
        self._db_factories = dict()
        self.logger = Logger()
        self._init_db_factories()

    def _init_db_factories(self):
        db_factory = PGFactory()
        self._db_factories[db_factory.get_id()] = db_factory
        self.id_default_db = db_factory.get_id()  # Make PostgreSQL the default DB engine

        db_factory = GPKGFactory()
        self._db_factories[db_factory.get_id()] = db_factory

        pyodbc_installed = is_pyodbc_available()
        libqt5sql5_odbc_installed = is_libqt5sql5_odbc_available()

        if pyodbc_installed and libqt5sql5_odbc_installed:
            from asistente_ladm_col.lib.db.mssql_factory import MSSQLFactory
            db_factory = MSSQLFactory()
            self._db_factories[db_factory.get_id()] = db_factory

        if not pyodbc_installed:
            self.logger.warning(__name__, QCoreApplication.translate("ConfigDBsSupported",
                                                   "MS SQL Server could not be configured. Library 'pyodbc' is missing!"))
        if not libqt5sql5_odbc_installed:
            self.logger.warning(__name__, QCoreApplication.translate("ConfigDBsSupported",
                                                           "MS SQL Server could not be configured. Library 'libqt5sql5-odbc' is missing!"))

    def get_db_factories(self):
        return self._db_factories

    def get_db_factory(self, engine):
        return self._db_factories[engine] if engine in self._db_factories else None
