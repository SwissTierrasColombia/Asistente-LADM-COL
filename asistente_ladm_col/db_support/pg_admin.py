from .db_admin import DbAdmin

from .pg_config_panel import PgConfigPanel
from ..lib.dbconnector.pg_connector import PGConnector
from .enum_action_type import EnumActionType
from QgisModelBaker.libili2db.ili2dbconfig import (SchemaImportConfiguration,
                                                   ImportDataConfiguration,
                                                   ExportConfiguration,
                                                   BaseConfiguration)


class PgAdmin(DbAdmin):
    def __init__(self):
        DbAdmin.__init__(self)
        self._mode = "pg"

    def get_name(self):
        return "PostgreSQL / PostGIS"

    def get_id(self):
        return "pg"

    def get_model_baker_tool_name(self):
        return "ili2pg"

    def get_config_panel(self):
        return PgConfigPanel()

    def get_db_connector(self, parameters):
        return PGConnector(None, parameters['schema'], parameters)

    def get_schema_import_configuration(self, params):
        configuration = SchemaImportConfiguration()

        configuration.tool_name = 'pg'
        configuration.dbhost = params['host']
        configuration.dbport = params['port']
        configuration.dbusr = params['username']
        configuration.database = params['database']
        configuration.dbschema = params['schema']
        configuration.dbpwd = params['password']

        return configuration

    def get_import_configuration(self, params):
        configuration = ImportDataConfiguration()

        configuration.dbhost = params['host']
        configuration.dbport = params['port']
        configuration.dbusr = params['username']
        configuration.database = params['database']
        configuration.dbschema = params['schema']
        configuration.dbpwd = params['password']

        return configuration

    def get_export_configuration(self, params):
        configuration = ExportConfiguration()

        configuration.dbhost = params['host']
        configuration.dbport = params['port']
        configuration.dbusr = params['username']
        configuration.database = params['database']
        configuration.dbschema = params['schema']
        configuration.dbpwd = params['password']

        return configuration