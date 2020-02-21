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
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2.extras
from psycopg2 import ProgrammingError
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import QgsDataSourceUri

from asistente_ladm_col.config.enums import (EnumTestLevel,
                                             EnumUserLevel,
                                             EnumTestConnectionMsg)
from asistente_ladm_col.lib.db.db_connector import (DBConnector,
                                                    COMPOSED_KEY_SEPARATOR)
from asistente_ladm_col.logic.ladm_col.config.queries.pg import logic_validation_queries
from asistente_ladm_col.logic.ladm_col.config.reports.ant_report.pg import (ant_map_neighbouring_change_query,
                                                                            ant_map_plot_query)
from asistente_ladm_col.logic.ladm_col.config.reports.annex_17_report.pg import (annex17_building_data_query,
                                                                                 annex17_point_data_query,
                                                                                 annex17_plot_data_query)
from asistente_ladm_col.config.mapping_config import LADMNames

from asistente_ladm_col.utils.model_parser import ModelParser
from asistente_ladm_col.utils.utils import normalize_iliname
from asistente_ladm_col.config.mapping_config import (T_ID_KEY,
                                                      DISPLAY_NAME_KEY,
                                                      ILICODE_KEY,
                                                      DESCRIPTION_KEY,
                                                      QueryNames)


class PGConnector(DBConnector):
    _PROVIDER_NAME = 'postgres'
    _DEFAULT_VALUES = {
        'host': 'localhost',
        'port': '5432',
        'database': '',
        'username': '',
        'schema': '',
        'password': ''
    }

    def __init__(self, uri, conn_dict=dict()):
        DBConnector.__init__(self, uri, conn_dict)
        self.mode = 'pg'
        self.conn = None
        self.schema = conn_dict['schema'] if 'schema' in conn_dict else ''
        self.provider = 'postgres'
        self._tables_info = None
        self._logic_validation_queries = None

    @DBConnector.uri.setter
    def uri(self, value):
        data_source_uri = QgsDataSourceUri(value)

        self._dict_conn_params = {
            'host': data_source_uri.host(),
            'port': data_source_uri.port(),
            'username': data_source_uri.username(),
            'password': data_source_uri.password(),
            'database': data_source_uri.database(),
            'schema': self.schema
        }

        self._uri = value

    def get_description_conn_string(self):
        result = None
        if self._dict_conn_params['database'] and self._dict_conn_params['database'].strip("'") and \
                self._dict_conn_params['schema']:
            result = self._dict_conn_params['database'] + '.' + self._dict_conn_params['schema']

        return result

    def _postgis_exists(self):
        # Todo: Use it in test_connection()
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
                    SELECT
                        count(extversion)
                    FROM pg_catalog.pg_extension
                    WHERE extname='postgis'
                    """)

        return bool(cur.fetchone()[0])

    def _schema_exists(self, schema=None):
        if schema is None:
            schema = self.schema

        if schema:
            cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("""
                        SELECT EXISTS(SELECT 1 FROM pg_namespace WHERE nspname = '{}');
            """.format(schema))

            return bool(cur.fetchone()[0])

        return False

    def _metadata_exists(self):
        if self.schema:
            cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("""
                        SELECT
                          count(tablename)
                        FROM pg_catalog.pg_tables
                        WHERE schemaname = '{}' and tablename = '{}'
            """.format(self.schema, LADMNames.INTERLIS_TEST_METADATA_TABLE_PG))

            return bool(cur.fetchone()[0])

        return False

    def test_connection(self, test_level=EnumTestLevel.LADM, user_level=EnumUserLevel.CREATE):
        """
        WARNING: We check several levels in order:
            1. SERVER
            2. DB
            3. SCHEMA
            4. LADM
            5. SCHEMA_IMPORT
          If you need to modify this method, be careful and preserve the order!!!

        :param test_level: (EnumTestLevel) level of connection with postgres
        :param user_level: (EnumUserLevel) level of permissions a user has
        :return Triple: boolean result, message code, message text
        """
        uri = self._uri

        if test_level & EnumTestLevel.SERVER:
            uri = self.get_connection_uri(self._dict_conn_params, 0)
            res, msg = self.open_connection()
            if res:
                return True, EnumTestConnectionMsg.CONNECTION_TO_SERVER_SUCCESSFUL, QCoreApplication.translate("PGConnector",
                                                         "Connection to server was successful.")
            else:
                return False, EnumTestConnectionMsg.CONNECTION_TO_SERVER_FAILED, msg

        if test_level & EnumTestLevel.DB:
            if not self._dict_conn_params['database'].strip("'") or self._dict_conn_params['database'] == 'postgres':
                return False, EnumTestConnectionMsg.DATABASE_NOT_FOUND, QCoreApplication.translate("PGConnector",
                                                          "You should first select a database.")

        # Client side check
        if self.conn is None or self.conn.closed:
            res, msg = self.open_connection()
            if not res:
                return res, EnumTestConnectionMsg.CONNECTION_COULD_NOT_BE_OPEN, msg
        if self.conn.get_transaction_status() == psycopg2.extensions.TRANSACTION_STATUS_INERROR:  # 3
            self.conn.rollback()  # Go back to TRANSACTION_STATUS_IDLE (0)

        try:
            # Server side check
            cur = self.conn.cursor()
            cur.execute('SELECT 1')  # This query will fail if the db is no longer connected
            cur.close()
        except psycopg2.OperationalError:
            # Reopen the connection if it is closed due to timeout
            self.conn.close()
            res, msg = self.open_connection()
            if not res:
                return res, EnumTestConnectionMsg.CONNECTION_COULD_NOT_BE_OPEN, msg

        if test_level == EnumTestLevel.DB:  # Just in the DB case
            return True, EnumTestConnectionMsg.CONNECTION_TO_DB_SUCCESSFUL, QCoreApplication.translate("PGConnector",
                                                     "Connection to the database was successful.")

        if test_level & EnumTestLevel._CHECK_SCHEMA:
            if not self._dict_conn_params['schema'] or self._dict_conn_params['schema'] == '':
                return False, EnumTestConnectionMsg.SCHEMA_NOT_FOUND, QCoreApplication.translate("PGConnector",
                                                          "You should first select a schema.")

            if not self._schema_exists():
                return False, EnumTestConnectionMsg.SCHEMA_NOT_FOUND, QCoreApplication.translate("PGConnector",
                        "The schema '{}' does not exist in the database!").format(
                        self.schema)

            res, msg = self.has_schema_privileges(uri, self.schema, user_level)
            if not res:
                return False, EnumTestConnectionMsg.USER_HAS_NO_PERMISSION, QCoreApplication.translate("PGConnector",
                                                   "User '{}' has not enough permissions over the schema '{}'.").format(
                            self._dict_conn_params['username'],
                            self.schema)

        if test_level == EnumTestLevel.DB_SCHEMA:
            return True, EnumTestConnectionMsg.CONNECTION_TO_SCHEMA_SUCCESSFUL, QCoreApplication.translate("PGConnector",
                                                     "Connection to the database schema was successful.")

        if test_level & EnumTestLevel._CHECK_LADM:
            if not self._metadata_exists():
                return False, EnumTestConnectionMsg.INTERLIS_META_ATTRIBUTES_NOT_FOUND, QCoreApplication.translate("PGConnector",
                                                          "The schema '{}' is not a valid LADM_COL schema. That is, the schema doesn't have the structure of the LADM_COL model.").format(
                    self.schema)

            if self.get_ili2db_version() != 4:
                return False, EnumTestConnectionMsg.INVALID_ILI2DB_VERSION, QCoreApplication.translate("PGConnector",
                                                          "The DB schema '{}' was created with an old version of ili2db (v3), which is no longer supported. You need to migrate it to ili2db4.").format(
                    self.schema)


            res, msg = self.check_at_least_one_ladm_model_exists()
            if not res:
                return res, EnumTestConnectionMsg.NO_LADM_MODELS_FOUND, msg  # Version of the models is not valid

            if self.model_parser is None:
                self.model_parser = ModelParser(self)

            # Validate table and field names
            if not self._table_and_field_names:
                self._initialize_names()

            models = list()
            if self.ladm_model_exists():
                models.append(LADMNames.LADM_MODEL_PREFIX)
            if self.operation_model_exists():
                models.append(LADMNames.OPERATION_MODEL_PREFIX)
            if self.cadastral_form_model_exists():
                models.append(LADMNames.CADASTRAL_FORM_MODEL_PREFIX)
            if self.valuation_model_exists():
                models.append(LADMNames.VALUATION_MODEL_PREFIX)
            if self.ant_model_exists():
                models.append(LADMNames.ANT_MODEL_PREFIX)
            if self.reference_cartography_model_exists():
                models.append(LADMNames.REFERENCE_CARTOGRAPHY_PREFIX)
            if self.snr_data_model_exists():
                models.append(LADMNames.SNR_DATA_MODEL_PREFIX)
            if self.supplies_integration_model_exists():
                models.append(LADMNames.SUPPLIES_INTEGRATION_MODEL_PREFIX)
            if self.supplies_model_exists():
                models.append(LADMNames.SUPPLIES_MODEL_PREFIX)

            if not models:
                return False, EnumTestConnectionMsg.NO_LADM_MODELS_FOUND, QCoreApplication.translate("PGConnector", "The database has no models from LADM_COL! As is, it cannot be used for LADM_COL Assistant!")

            res, msg = self.names.test_names(self._table_and_field_names)
            if not res:
                return False, EnumTestConnectionMsg.DB_NAMES_INCOMPLETE, QCoreApplication.translate("PGConnector",
                                                                                                    "Table/field names from the DB are not correct. Details: {}.").format(
                    msg)

        if test_level == EnumTestLevel.LADM:
            return True, EnumTestConnectionMsg.SCHEMA_WITH_VALID_LADM_COL_STRUCTURE, QCoreApplication.translate(
                "PGConnector", "The schema '{}' has a valid LADM_COL structure!").format(
                self.schema)

        if test_level & EnumTestLevel.SCHEMA_IMPORT:
            return True, EnumTestConnectionMsg.CONNECTION_TO_DB_SUCCESSFUL_NO_LADM_COL, QCoreApplication.translate("PGConnector", "Connection successful!")

        return False, EnumTestConnectionMsg.UNKNOWN_CONNECTION_ERROR, QCoreApplication.translate("PGConnector",
                                                  "There was a problem checking the connection. Most likely due to invalid or not supported test_level!")

    def open_connection(self, uri=None):
        if uri is None:
            uri = self._uri
        else:
            self.conn.close()

        if self.conn is None or self.conn.closed:
            try:
                self.conn = psycopg2.connect(uri)
            except (psycopg2.OperationalError, psycopg2.ProgrammingError) as e:
                return False, QCoreApplication.translate("PGConnector", "Could not open connection! Details: {}".format(e))

            self.logger.info(__name__, "Connection was open! {}".format(self.conn))
        else:
            self.logger.info(__name__, "Connection is already open! {}".format(self.conn))

        return True, QCoreApplication.translate("PGConnector", "Connection is open!")

    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.logger.info(__name__, "Connection was closed ({}) !".format(self.conn.closed))
            self.conn = None

    def get_table_and_field_names(self):
        """
        Documented in the super class
        """
        # Get both table and field names. Only include field names that are not FKs, they will be added in a second step
        sql_query = """SELECT 
                      iliclass.iliname AS {table_iliname},
                      tbls.tablename AS {table_name},
                      ilicol.iliname AS {field_iliname},
                      ilicol.sqlname AS {field_name}      
                    FROM pg_catalog.pg_tables tbls
                    LEFT JOIN {schema}.t_ili2db_classname iliclass
                      ON tbls.tablename = iliclass.sqlname
                    LEFT JOIN {schema}.t_ili2db_attrname ilicol
                      ON ilicol.colowner = tbls.tablename
                      AND ilicol.target IS NULL
                    WHERE schemaname ='{schema}'
                    ORDER BY tbls.tablename, ilicol.sqlname;""".format(table_iliname=QueryNames.TABLE_ILINAME,
                                                                  table_name=QueryNames.TABLE_NAME,
                                                                  field_iliname=QueryNames.FIELD_ILINAME,
                                                                  field_name=QueryNames.FIELD_NAME,
                                                                  schema=self.schema)

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(sql_query)
        records = cur.fetchall()

        dict_names = dict()
        for record in records:
            if record[QueryNames.TABLE_ILINAME] is None:
                # Either t_ili2db_* tables (INTERLIS meta-attrs)
                continue

            record[QueryNames.TABLE_ILINAME] = normalize_iliname(record[QueryNames.TABLE_ILINAME])
            if not record[QueryNames.TABLE_ILINAME] in dict_names:
                dict_names[record[QueryNames.TABLE_ILINAME]] = dict()
                dict_names[record[QueryNames.TABLE_ILINAME]][QueryNames.TABLE_NAME] = record[QueryNames.TABLE_NAME]

            if record[QueryNames.FIELD_ILINAME] is None:
                # Fields for domains, like 'description' (we map it in a custom way later in this class method)
                continue

            record[QueryNames.FIELD_ILINAME] = normalize_iliname(record[QueryNames.FIELD_ILINAME])
            dict_names[record[QueryNames.TABLE_ILINAME]][record[QueryNames.FIELD_ILINAME]] = record[QueryNames.FIELD_NAME]

        # Map FK ilinames (i.e., those whose t_ili2db_attrname target column is not NULL)
        # Spatial_Unit-->Ext_Address_ID (Ext_Address)
        #   Key: "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID"
        #   Values: op_construccion_ext_direccion_id and  op_terreno_ext_direccion_id
        sql_query = """SELECT substring(a.iliname from 1 for (length(a.iliname) - position('.' in reverse(a.iliname)))) as {table_iliname},
            a.iliname, a.sqlname, c.iliname as iliname2, o.iliname as colowner
            FROM {schema}.t_ili2db_attrname a
                INNER JOIN {schema}.t_ili2db_classname o ON o.sqlname = a.colowner
                INNER JOIN {schema}.t_ili2db_classname c ON c.sqlname = a.target
            ORDER BY a.iliname""".format(table_iliname=QueryNames.TABLE_ILINAME,
                                         schema=self.schema)
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(sql_query)
        records = cur.fetchall()
        for record in records:
            composed_key = "{}{}{}".format(normalize_iliname(record['iliname']),
                                           COMPOSED_KEY_SEPARATOR,
                                           normalize_iliname(record['iliname2']))
            record[QueryNames.TABLE_ILINAME] = normalize_iliname(record[QueryNames.TABLE_ILINAME])
            if record[QueryNames.TABLE_ILINAME] in dict_names:
                dict_names[record[QueryNames.TABLE_ILINAME]][composed_key] = record['sqlname']
            else:
                record['colowner'] = normalize_iliname(record['colowner'])
                if record['colowner'] in dict_names:
                    dict_names[record['colowner']][composed_key] = record['sqlname']

        # Add required key-value pairs that do not come from the DB query
        dict_names[T_ID_KEY] = "t_id"
        dict_names[DISPLAY_NAME_KEY] = "dispname"
        dict_names[ILICODE_KEY] = "ilicode"
        dict_names[DESCRIPTION_KEY] = "description"

        return dict_names

    def check_and_fix_connection(self):
        if self.conn is None or self.conn.closed:
            res, code, msg = self.test_connection()
            if not res:
                return res, msg

        if self.conn.get_transaction_status() == psycopg2.extensions.TRANSACTION_STATUS_INERROR:  # 3
            self.conn.rollback()  # Go back to TRANSACTION_STATUS_IDLE (0)
            if self.conn.get_transaction_status() != psycopg2.extensions.TRANSACTION_STATUS_IDLE:
                return (False, "Error: PG transaction had an error and couldn't be recovered...")

        return True, ''

    def get_annex17_plot_data(self, plot_id, mode='only_id'):
        res, msg = self.check_and_fix_connection()
        if not res:
            return (res, msg)

        where_id = ""
        if mode != 'all':
            where_id = "WHERE l.t_id {} {}".format('=' if mode == 'only_id' else '!=', plot_id)

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = annex17_plot_data_query.get_annex17_plot_data_query(self.schema, where_id)
        cur.execute(query)

        if mode == 'only_id':
            return cur.fetchone()[0]
        else:
            return cur.fetchall()[0][0]

    def get_annex17_building_data(self):
        res, msg = self.check_and_fix_connection()
        if not res:
            return (res, msg)

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = annex17_building_data_query.get_annex17_building_data_query(self.schema)
        cur.execute(query)

        return cur.fetchall()[0][0]

    def get_annex17_point_data(self, plot_id):
        res, msg = self.check_and_fix_connection()
        if not res:
            return (res, msg)

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = annex17_point_data_query.get_annex17_point_data_query(self.schema, plot_id)
        cur.execute(query)

        return cur.fetchone()[0]

    def get_ant_map_plot_data(self, plot_id, mode='only_id'):
        res, msg = self.check_and_fix_connection()
        if not res:
            return (res, msg)

        where_id = ""
        if mode != 'all':
            where_id = "WHERE op_terreno.t_id {} {}".format('=' if mode == 'only_id' else '!=', plot_id)

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = ant_map_plot_query.get_ant_map_query(self.schema, where_id)
        cur.execute(query)

        if mode == 'only_id':
            return cur.fetchone()[0]
        else:
            return cur.fetchall()[0][0]

    def get_ant_map_neighbouring_change_data(self, plot_id, mode='only_id'):
        res, msg = self.check_and_fix_connection()
        if not res:
            return (res, msg)

        where_id = ""
        if mode != 'all':
            where_id = "WHERE t.t_id {} {}".format('=' if mode == 'only_id' else '!=', plot_id)

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = ant_map_neighbouring_change_query.get_ant_map_neighbouring_change_query(self.schema, where_id)
        cur.execute(query)

        if mode == 'only_id':
            return cur.fetchone()[0]
        else:
            return cur.fetchall()[0][0]

    def execute_sql_query(self, query):
        """
        Generic function for executing SQL statements
        :param query: SQL Statement
        :return: List of RealDictRow
        """
        res, msg = self.check_and_fix_connection()
        if not res:
            return res, msg

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        try:
            cur.execute(query)
            return True, cur.fetchall()
        except ProgrammingError as e:
            return False, e

    def execute_sql_query_dict_cursor(self, query):
        """
        Generic function for executing SQL statements
        :param query: SQL Statement
        :return: List of DictRow
        """
        res, msg = self.check_and_fix_connection()
        if not res:
            return (res, msg)

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query)
        return cur.fetchall()

    def get_logic_validation_queries(self):
        if self._logic_validation_queries is None:
            self._logic_validation_queries = logic_validation_queries.get_logic_validation_queries(self.schema, self.names)
        return self._logic_validation_queries

    def get_ladm_units(self):
        query = """SELECT DISTINCT tablename || '..' || columnname AS unit_key, ' [' || setting || ']' AS unit_value FROM {schema}.t_ili2db_column_prop WHERE tag LIKE 'ch.ehi.ili2db.unit'""".format(schema=self.schema)
        res, result = self.execute_sql_query(query)

        dict_units = dict()
        if res:
            for unit in result:
                dict_units[unit['unit_key']] = unit['unit_value']
            self.logger.debug(__name__, "Units found: {}".format(dict_units))
        else:
            self.logger.error_msg(__name__, "Error getting models: {}".format(result))

        return dict_units

    def get_models(self, schema=None):
        query = "SELECT distinct split_part(iliname,'.',1) as modelname FROM {schema}.t_ili2db_trafo".format(
            schema=schema if schema else self.schema)
        res, result = self.execute_sql_query(query)
        lst_models = list()
        if res:
            lst_models = [db_model['modelname'] for db_model in result]
            self.logger.debug(__name__, "Models found: {}".format(lst_models))
        else:
            self.logger.error_msg(__name__, "Error getting models: {}".format(result))
        return lst_models

    def create_database(self, uri, db_name):
        """
        Create a database
        :param uri: (str) Connection uri only: (host, port, user, pass)
        :param db_name: (str) Database name to be created
        :return: tuple(bool, str)
            bool: True if everything was executed successfully and False if not
            str: Message to the user indicating the type of error or if everything was executed correctly
        """
        sql = """CREATE DATABASE "{}" WITH ENCODING = 'UTF8' CONNECTION LIMIT = -1""".format(db_name)
        conn = psycopg2.connect(uri)

        if conn:
            try:
                conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                cur = conn.cursor()
                cur.execute(sql)
            except psycopg2.ProgrammingError as e:
                return (False, QCoreApplication.translate("PGConnector",
                                                          "An error occurred while trying to create the '{}' database: {}".format(
                                                              db_name, e)))
        cur.close()
        conn.close()
        return (
        True, QCoreApplication.translate("PGConnector", "Database '{}' was successfully created!".format(db_name)))

    def create_schema(self, uri, schema_name):
        """
        Create a schema
        :param uri:  (str) connection uri only: (host, port, user, pass, db)
        :param schema_name: (str) schema name to be created
        :return: tuple(bool, str)
            bool: True if everything was executed successfully and False if not
            str: Message to the user indicating the type of error or if everything was executed correctly
        """
        sql = 'CREATE SCHEMA "{}"'.format(schema_name)
        conn = psycopg2.connect(uri)

        if conn:
            try:
                conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                cur = conn.cursor()
                cur.execute(sql)
            except psycopg2.ProgrammingError as e:
                return (False, QCoreApplication.translate("PGConnector",
                                                          "An error occurred while trying to create the '{}' schema: {}".format(
                                                              schema_name, e)))
        cur.close()
        conn.close()
        return (
        True, QCoreApplication.translate("PGConnector", "Schema '{}' was successfully created!".format(schema_name)))

    def get_dbnames_list(self, uri):
        res, code, msg = self.test_connection(EnumTestLevel.SERVER)
        if not res:
            return (False, msg)

        dbnames_list = list()
        try:
            conn = psycopg2.connect(uri)
            cur = conn.cursor()
            query = """SELECT datname FROM pg_database WHERE datistemplate = false AND datname <> 'postgres' ORDER BY datname"""
            cur.execute(query)
            dbnames = cur.fetchall()
            for dbname in dbnames:
                dbnames_list.append(dbname[0])
            cur.close()
            conn.close()
        except Exception as e:
            return (False, QCoreApplication.translate("PGConnector",
                                                      "There was an error when obtaining the list of existing databases. : {}").format(
                e))
        return (True, dbnames_list)

    def get_dbname_schema_list(self, uri):
        schemas_list = list()
        try:
            conn = psycopg2.connect(uri)
            cur = conn.cursor()
            query = """
                SELECT n.nspname as "{schema_name}" FROM pg_catalog.pg_namespace n 
                WHERE n.nspname !~ '^pg_' AND n.nspname <> 'information_schema' AND nspname <> 'public' ORDER BY "{schema_name}"
            """.format(schema_name=QueryNames.SCHEMA_NAME)
            cur.execute(query)
            schemas = cur.fetchall()
            for schema in schemas:
                schemas_list.append(schema[0])
            cur.close()
            conn.close()
        except Exception as e:
            return (False, QCoreApplication.translate("PGConnector",
                                                      "There was an error when obtaining the list of existing schemas: {}").format(
                e))
        return (True, schemas_list)

    def has_schema_privileges(self, uri, schema, user_level=EnumUserLevel.CREATE):
        try:
            conn = psycopg2.connect(uri)
            cur = conn.cursor()
            query = """
                        SELECT
                            CASE WHEN pg_catalog.has_schema_privilege(current_user, '{schema}', 'CREATE') = True  THEN 1 ELSE 0 END AS "create",
                            CASE WHEN pg_catalog.has_schema_privilege(current_user, '{schema}', 'USAGE')  = True  THEN 1 ELSE 0 END AS "usage";
                    """.format(schema=schema)

            cur.execute(query)
            schema_privileges = cur.fetchone()
            if schema_privileges:
                privileges = {'create': bool(int(schema_privileges[0])),  # 'create'
                              'usage': bool(int(schema_privileges[1]))}  # 'usage'
            else:
                return False, QCoreApplication.translate("PGConnector", "No information for schema '{}'.").format(schema)
            cur.close()
            conn.close()
        except Exception as e:
            return False, QCoreApplication.translate("PGConnector",
                                                      "There was an error when obtaining privileges for schema '{}'. Details: {}").format(
                schema, e)

        if user_level == EnumUserLevel.CREATE and privileges['create'] and privileges['usage']:
            return True, QCoreApplication.translate("PGConnector",
                                                     "The user has both Create and Usage privileges over the schema.")
        elif user_level == EnumUserLevel.CONNECT and privileges['usage']:
            return True, QCoreApplication.translate("PGConnector",
                                                    "The user has Usage privileges over the schema.")
        else:
            return False, QCoreApplication.translate("PGConnector", "The user has not enough privileges over the schema.")

    def is_ladm_layer(self, layer):
        result = False
        if layer.dataProvider().name() == PGConnector._PROVIDER_NAME:
            layer_uri = layer.dataProvider().uri()
            db_uri = QgsDataSourceUri(self._uri)

            result = (layer_uri.schema() == self.schema and
                      layer_uri.database() == db_uri.database() and
                      layer_uri.host() == db_uri.host() and
                      layer_uri.port() == db_uri.port() and
                      layer_uri.username() == db_uri.username() and
                      layer_uri.password() == db_uri.password())

        return result

    def get_ladm_layer_name(self, layer, validate_is_ladm=False):
        name = None
        if validate_is_ladm:
            if self.is_ladm_layer(layer):
                name = layer.dataProvider().uri().table()
        else:
            name = layer.dataProvider().uri().table()
        return name

    def get_connection_uri(self, dict_conn, level=1):
        uri = []
        uri += ['host={}'.format(dict_conn['host'])]
        uri += ['port={}'.format(dict_conn['port'])]
        if dict_conn['username']:
            uri += ['user={}'.format(dict_conn['username'])]
        if dict_conn['password']:
            uri += ['password={}'.format(dict_conn['password'])]
        if level == 1 and dict_conn['database']:
            uri += ['dbname={}'.format(dict_conn['database'])]
        else:
            # It is necessary to define the database name for listing databases
            # PostgreSQL uses the db 'postgres' by default and it cannot be deleted, so we use it as last resort
            uri += ["dbname={}".format(self._PROVIDER_NAME)]

        return ' '.join(uri)

    def get_ili2db_version(self):
        res, msg = self.check_and_fix_connection()
        if not res:
            return (res, msg)

        # Borrowed from Model Baker
        cur = self.conn.cursor()
        cur.execute("""SELECT *
                       FROM information_schema.columns
                       WHERE table_schema = '{schema}'
                       AND(table_name='t_ili2db_attrname' OR table_name='t_ili2db_model' )
                       AND(column_name='owner' OR column_name = 'file' )
                    """.format(schema=self.schema))
        if cur.rowcount > 1:
            return 3
        else:
            return 4