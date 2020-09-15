# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-02-15
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
import pyodbc
from pyodbc import (ProgrammingError, InterfaceError)

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import Qgis

from asistente_ladm_col.config.general_config import (PLUGIN_NAME)
from asistente_ladm_col.config.ili2db_names import ILI2DBNames
from asistente_ladm_col.core.model_parser import ModelParser
from asistente_ladm_col.lib.db.db_connector import (DBConnector,
                                                    ClientServerDB)
from asistente_ladm_col.config.enums import (EnumTestLevel,
                                             EnumTestConnectionMsg)
from asistente_ladm_col.config.query_names import QueryNames
from asistente_ladm_col.config.keys.ili2db_keys import *


class MSSQLConnector(ClientServerDB):
    _PROVIDER_NAME = 'mssql'
    _DEFAULT_HOST = 'localhost'
    _DEFAULT_VALUES = {
        'db_odbc_driver': '',
        'host': 'localhost',
        'port': '',
        'instance': '',
        'database': '',
        'username': '',
        'schema': '',
        'password': ''
    }

    def __init__(self, uri, conn_dict=dict()):
        DBConnector.__init__(self, uri, conn_dict)
        self.engine = 'mssql'
        self.conn = None
        self.schema = conn_dict['schema'] if 'schema' in conn_dict else ''
        self.provider = 'mssql'
        self._tables_info = None

    @staticmethod
    def _get_dict_conn(uri):
        uri_parts = uri.split(";")

        lst_item_uri = dict()

        for item in uri_parts:
            key_value = item.split("=")

            if key_value[0] and key_value[1]:
                lst_item_uri[key_value[0]] = key_value[1]

        result = dict(MSSQLConnector._DEFAULT_VALUES)

        if 'SERVER' in lst_item_uri:
            server_parts = lst_item_uri["SERVER"].split(',')

            if len(server_parts) > 1:
                result['port'] = server_parts[1]

            server_parts2 = server_parts[0].split('\\')

            if len(server_parts2) > 1:
                result['instance'] = server_parts2[1]

            # FIXME check if no result
            result['host'] = server_parts2[0]

        if 'DRIVER' in lst_item_uri:
            result['db_odbc_driver'] = lst_item_uri['DRIVER'].replace('{', '').replace('}', '')

        result['username'] = lst_item_uri['UID'] if 'UID' in lst_item_uri \
            else MSSQLConnector._DEFAULT_VALUES['username']
        result['password'] = lst_item_uri['PWD'] if 'PWD' in lst_item_uri \
            else MSSQLConnector._DEFAULT_VALUES['password']
        result['database'] = lst_item_uri['DATABASE'] if 'DATABASE' in lst_item_uri \
            else MSSQLConnector._DEFAULT_VALUES['database']

        return result

    @DBConnector.uri.setter
    def uri(self, value):
        self._dict_conn_params = self._get_dict_conn(value)
        self._dict_conn_params['schema'] = self.schema

        self._uri = value

    def get_description_conn_string(self):
        result = None
        if self._dict_conn_params['database'] and self._dict_conn_params['schema']:
            result = self._dict_conn_params['database'] + '.' + self._dict_conn_params['schema']

        return result

    def _schema_exists(self, schema=None):
        schema = schema if schema is not None else self.schema
        if schema:
            cur = self.conn.cursor()
            cur.execute("""
                        SELECT case when count(schema_name)>0 then 1 else 0 end
                        FROM information_schema.schemata
                        where schema_name = '{}'
            """.format(schema))

            return bool(cur.fetchone()[0])

        return False

    def _metadata_exists(self):
        if self.schema:
            cur = self.conn.cursor()
            cur.execute("""
            SELECT count(TABLE_NAME) as 'count'
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_TYPE = 'BASE TABLE'
                AND TABLE_SCHEMA = '{}'
                    AND TABLE_NAME = '{}'
            """.format(self.schema, ILI2DBNames.INTERLIS_TEST_METADATA_TABLE_PG))

            return bool(cur.fetchone()[0])

        return False

    def open_connection(self, uri=None):
        if uri is None:
            uri = self._uri
        else:
            self.conn.close()

        if self.conn is None or self.__is_conn_closed():
            try:
                self.conn = pyodbc.connect(uri)
            except (ProgrammingError, InterfaceError, pyodbc.Error, pyodbc.OperationalError) as e:
                return False, QCoreApplication.translate("MSSQLConnector", "Could not open connection! Details: {}".format(e))

            self.logger.info(__name__, "Connection was open! {}".format(self.conn), PLUGIN_NAME, Qgis.Info)
        else:
            self.logger.info(__name__, "Connection is already open! {}".format(self.conn), PLUGIN_NAME, Qgis.Info)

        return True, QCoreApplication.translate("MSSQLConnector", "Connection is open!")

    def close_connection(self):
        if self.conn:
            if not self.__is_conn_closed():
                self.conn.close()
            self.logger.info(__name__, "Connection was closed!")
            self.conn = None

    def get_dbnames_list(self, uri):
        res, code, msg = self.test_connection(EnumTestLevel.SERVER_OR_FILE)
        if not res:
            return False, msg
        dbnames_list = list()
        try:
            conn = pyodbc.connect(uri)
            cur = conn.cursor()
            query = """SELECT name FROM master.sys.databases WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb') order by name"""
            cur.execute(query)
            dbnames = cur.fetchall()

            for dbname in dbnames:
                dbnames_list.append(dbname[0])
            cur.close()
            conn.close()
        except Exception as e:
            return (False, QCoreApplication.translate("MSSQLConnector",
                                               "There was an error when obtaining the list of existing databases. : {}").format(e))

        return True, dbnames_list

    def get_dbname_schema_list(self, uri):
        schemas_list = list()
        try:
            conn = pyodbc.connect(uri)
            cur = conn.cursor()

            # TODO check "CURRENT USER"
            query = """SELECT schema_name FROM information_schema.schemata where schema_owner = CURRENT_USER order by schema_name"""
            cur.execute(query)
            schemas = cur.fetchall()

            for schema in schemas:
                schemas_list.append(schema[0])

            cur.close()
            conn.close()
        except Exception as e:
            return False, QCoreApplication.translate("MSSQLConnector",
                                               "There was an error when obtaining the list of existing schemas: {}").format(e)
        return True, schemas_list

    def create_schema(self, uri, schema_name):
        """
        Create a schema
        :param uri:  (str) connection uri only: (host, port, user, pass, db)
        :param schema_name: (str) schema name to be created
        :return: tuple(bool, str)
            bool: True if everything was executed successfully and False if not
            str: Message to the user indicating the type of error or if everything was executed correctly
        """
        sql = """CREATE SCHEMA "{}" """.format(schema_name)
        conn = pyodbc.connect(uri)

        if conn:
            try:
                cur = conn.cursor()
                cur.execute(sql)
                cur.commit()
            except pyodbc.ProgrammingError as e:
                return False, QCoreApplication.translate("MSSQLConnector", "An error occurred while trying to create the '{}' schema: {}".format(schema_name, e))

            cur.close()
            conn.close()

            return True, QCoreApplication.translate("MSSQLConnector", "Schema '{}' was successfully created!".format(schema_name))
        else:
            return False, QCoreApplication.translate("MSSQLConnector",
                                                     "Could not connect to schema '{}'!".format(schema_name))

    def create_database(self, uri, db_name):
        """
        Create a database
        :param uri: (str) Connection uri only: (host, port, user, pass)
        :param db_name: (str) Database name to be created
        :return: tuple(bool, str)
            bool: True if everything was executed successfully and False if not
            str: Message to the user indicating the type of error or if everything was executed correctly
        """
        sql = """CREATE DATABASE "{}" """.format(db_name)
        conn = pyodbc.connect(uri, autocommit=True)

        if conn:
            try:
                cur = conn.cursor()
                cur.execute(sql)

            except pyodbc.ProgrammingError as e:
                return False, QCoreApplication.translate("MSSQLConnector", "An error occurred while trying to create the '{}' database: {}".format(db_name, e))

            cur.close()
            conn.close()

            return True, QCoreApplication.translate("MSSQLConnector", "Database '{}' was successfully created!".format(db_name))
        else:
            return False, QCoreApplication.translate("MSSQLConnector",
                                                     "Could not connect to database '{}'!".format(db_name))

    def get_models(self, schema=None):
        query = "SELECT distinct LEFT(iliname, CHARINDEX('.',iliname)-1) as modelname FROM {schema}.t_ili2db_trafo".format(schema=schema if schema else self.schema)
        res, result = self.execute_sql_query(query)

        lst_models = list()
        if res:
            lst_models = [db_model['modelname'] for db_model in result]
            self.logger.debug(__name__, "Models found: {}".format(lst_models))
        else:
            self.logger.error_msg(__name__, "Error getting models: {}".format(result))
        return lst_models

    def execute_sql_query(self, query):
        """
        Generic function for executing SQL statements
        :param query: SQL Statement
        :return: List of RealDictRow
        """
        if self.conn is None:
            res, code, msg = self.test_connection()
            if not res:
                return res, msg
        cur = self.conn.cursor()

        try:
            cur.execute(query)
            return True, self._get_dict_result(cur)
        except pyodbc.ProgrammingError as e:
            return False, e

    def _get_dict_result(self, cur):
        columns = [column[0] for column in cur.description]

        res = []
        for row in cur.fetchall():
            my_rec = dict(zip(columns, row))
            res.append(my_rec)

        return res

    def is_ladm_layer(self, layer):
        result = False
        if layer.dataProvider().name() == MSSQLConnector._PROVIDER_NAME:
            layer_uri = layer.dataProvider().uri()
            db_uri = self.dict_conn_params

            host_test = db_uri['host']
            host_test += "\\" + db_uri['instance'] if db_uri['instance'] else ""
            host_test += "," + db_uri['port'] if db_uri['port'] else ""

            result = (layer_uri.schema() == self.schema and \
                layer_uri.database() == db_uri['database'] and \
                layer_uri.host() == host_test and \
                layer_uri.username() == db_uri['username'] and \
                layer_uri.password() == db_uri['password'])

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

        uri += ['DRIVER={{{}}}'.format(dict_conn['db_odbc_driver'])]
        host = dict_conn['host'] or self._DEFAULT_VALUES['host']
        if dict_conn['instance']:
            host += '\\' + dict_conn['instance']
        if dict_conn['port']:
            host += ',' + dict_conn['port']

        uri += ['SERVER={}'.format(host)]
        if dict_conn['database'] and level == 1:
            uri += ['DATABASE={}'.format(dict_conn['database'])]
        uri += ['UID={}'.format(dict_conn['username'])]
        uri += ['PWD={}'.format(dict_conn['password'])]

        return ';'.join(uri)

    def get_ili2db_version(self):
        res, msg = self.check_and_fix_connection()
        if not res:
            return res, msg

        # Borrowed from Model Baker
        cur = self.conn.cursor()
        cur.execute("""SELECT count(COLUMN_NAME)
                       FROM information_schema.columns
                       WHERE table_schema = '{schema}'
                       AND(table_name='t_ili2db_attrname' OR table_name='t_ili2db_model' )
                       AND(column_name='owner' OR column_name = 'file' )
                    """.format(schema=self.schema))

        columns_count = cur.fetchone()[0]

        if columns_count > 0:
            return 3
        else:
            return 4

    def check_and_fix_connection(self):
        if self.conn is None or self.__is_conn_closed():
            res, code, msg = self.test_connection()
            if not res:
                return res, msg

        return True, ''

    def get_logic_validation_queries(self):
        # return variables from logic_validation_queries for mssql
        pass

    def _test_connection_to_schema(self, user_level):
        # TODO # is 'dbo' database valid?  self._dict_conn_params['schema'] == 'dbo':
        if not self._dict_conn_params['schema']:
            return False, EnumTestConnectionMsg.SCHEMA_NOT_FOUND, QCoreApplication.translate("MSSQLConnector",
                                                                                             "You should first select a schema.")
        if not self._schema_exists():
            return False, EnumTestConnectionMsg.SCHEMA_NOT_FOUND, QCoreApplication.translate("MSSQLConnector",
                                                                                             "The schema '{}' does not exist in the database!").format(
                self.schema)
        # TODO Test schema permissions (*)

        return True, EnumTestConnectionMsg.CONNECTION_TO_SCHEMA_SUCCESSFUL, QCoreApplication.translate("MSSQLConnector",
                                                                                                       "Connection to the database schema was successful.")

    def _test_connection_to_server(self):
        uri = self.get_connection_uri(self._dict_conn_params, 0)
        res, msg = self.open_connection()
        if res:
            return True, EnumTestConnectionMsg.CONNECTION_TO_SERVER_SUCCESSFUL, QCoreApplication.translate(
                "MSSQLConnector",
                "Connection to server was successful.")
        else:
            return False, EnumTestConnectionMsg.CONNECTION_TO_SERVER_FAILED, msg

    def get_ladm_units(self):
        query = """SELECT DISTINCT concat(tablename,'..',columnname) AS unit_key, concat(' [',setting,']') AS unit_value FROM {schema}.t_ili2db_column_prop WHERE tag LIKE 'ch.ehi.ili2db.unit'""".format(schema=self.schema)

        res, result = self.execute_sql_query(query)

        dict_units = dict()
        if res:
            for unit in result:
                dict_units[unit['unit_key']] = unit['unit_value']
            self.logger.debug(__name__, "Units found: {}".format(len(dict_units)))
        else:
            self.logger.error_msg(__name__, "Error getting units: {}".format(result))

        return dict_units

    def _test_connection_to_db(self):
        if not self._dict_conn_params['database'] or self._dict_conn_params['database'] == 'master':
            return False, EnumTestConnectionMsg.DATABASE_NOT_FOUND, QCoreApplication.translate("MSSQLConnector",
                                                                                               "You should first select a database.")

        # Client side check
        if self.conn is None or self.__is_conn_closed():
            res, msg = self.open_connection()
            if not res:
                return res, EnumTestConnectionMsg.CONNECTION_COULD_NOT_BE_OPEN, msg

        try:
            # Server side check
            cur = self.conn.cursor()
            cur.execute('SELECT 1')  # This query will fail if the db is no longer connected
            cur.close()
        except Exception as e:
            res, msg = self.open_connection()
            if not res:
                return res, EnumTestConnectionMsg.CONNECTION_COULD_NOT_BE_OPEN, msg

        return True, EnumTestConnectionMsg.CONNECTION_TO_DB_SUCCESSFUL, QCoreApplication.translate("MSSQLConnector",
                                                                                                       "Connection to the database was successful.")

    def _test_connection_to_ladm(self, required_models):
        if not self._metadata_exists():
            return False, EnumTestConnectionMsg.INTERLIS_META_ATTRIBUTES_NOT_FOUND, QCoreApplication.translate(
                "MSSQLConnector",
                "The schema '{}' is not a valid LADM_COL schema. That is, the schema doesn't have the structure of the LADM_COL model.").format(
                self.schema)

        if self.get_ili2db_version() != 4:
            return False, EnumTestConnectionMsg.INVALID_ILI2DB_VERSION, QCoreApplication.translate("MSSQLConnector",
                                                                                                   "The DB schema '{}' was created with an old version of ili2db (v3), which is no longer supported. You need to migrate it to ili2db4.").format(
                self.schema)

        if self.model_parser is None:
            self.model_parser = ModelParser(self)

        res, code, msg = self.check_db_models(required_models)
        if not res:
            return res, code, msg

        # Validate table and field names
        if self._should_update_db_mapping_values:
            self._initialize_names()

        res, msg = self.names.test_names(self._get_flat_table_and_field_names_for_testing_names())
        if not res:
            return False, EnumTestConnectionMsg.DB_NAMES_INCOMPLETE, QCoreApplication.translate("MSSQLConnector",
                                                                                                "Table/field names from the DB are not correct. Details: {}.").format(
                msg)

        return True, EnumTestConnectionMsg.SCHEMA_WITH_VALID_LADM_COL_STRUCTURE, QCoreApplication.translate(
            "MSSQLConnector", "The schema '{}' has a valid LADM_COL structure!").format(self.schema)

    def _get_table_and_field_names(self):
        sql_query = """
        SELECT 
          iliclass.iliname AS {table_iliname},
          tbls.TABLE_NAME AS {table_name},
          ilicol.iliname AS {field_iliname},
          ilicol.sqlname AS {field_name}
        FROM INFORMATION_SCHEMA.TABLES AS tbls
        INNER JOIN {schema}.t_ili2db_classname AS iliclass
          ON tbls.TABLE_NAME=iliclass.SqlName
          AND TABLE_TYPE = 'BASE TABLE'
        LEFT JOIN {schema}.t_ili2db_attrname as ilicol
          ON tbls.TABLE_NAME = ilicol.colowner
          AND ilicol.Target IS NULL
        WHERE TABLE_SCHEMA='{schema}'
        ORDER BY tbls.TABLE_NAME, ilicol.sqlname
        """.format(table_iliname=QueryNames.TABLE_ILINAME,
                                                table_name=QueryNames.TABLE_NAME,
                                                field_iliname=QueryNames.FIELD_ILINAME,
                                                field_name=QueryNames.FIELD_NAME,
                                                schema=self.schema)

        is_success, res = self.execute_sql_query(sql_query)

        return res if is_success else None

    def _get_fk_fields(self):
        sql_query = """
        SELECT LEFT(a.iliname, LEN(a.iliname)-charindex('.', reverse(a.iliname))) as {table_iliname},
                    a.iliname, a.sqlname, c.iliname as iliname2, o.iliname as colowner
            FROM {schema}.t_ili2db_attrname as a
                INNER JOIN {schema}.t_ili2db_classname o ON o.sqlname = a.colowner
                INNER JOIN {schema}.t_ili2db_classname c ON c.sqlname = a.target
            ORDER BY a.iliname
            """.format(table_iliname=QueryNames.TABLE_ILINAME, schema=self.schema)

        is_success, res = self.execute_sql_query(sql_query)

        return res if is_success else None

    def _get_ili2db_names(self):
        dict_names = dict()
        # Add required key-value pairs that do not come from the DB query
        dict_names[T_ID_KEY] = "T_Id"
        dict_names[T_ILI_TID_KEY] = "T_Ili_Tid"
        dict_names[DISPLAY_NAME_KEY] = "dispName"
        dict_names[ILICODE_KEY] = "iliCode"
        dict_names[DESCRIPTION_KEY] = "description"
        dict_names[T_BASKET_KEY] = "t_basket"
        dict_names[T_ILI2DB_BASKET_KEY] = "t_ili2db_basket"
        dict_names[T_ILI2DB_DATASET_KEY] = "t_ili2db_dataset"
        dict_names[DATASET_T_DATASETNAME_KEY] = "datasetname"
        dict_names[BASKET_T_DATASET_KEY] = "dataset"
        dict_names[BASKET_T_TOPIC_KEY] = "topic"
        dict_names[BASKET_T_ATTACHMENT_KEY] = "attachmentkey"

        return dict_names

    def __is_conn_closed(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT @@version;")
            result = False
        except (ProgrammingError, InterfaceError, pyodbc.Error, pyodbc.OperationalError):
            result = True

        return result

    def get_qgis_layer_uri(self, table_name):
        def get_layer_uri_common(uri):
            # Borrowed from QgisModelBaker/libqgsprojectgen/db_factory/mssql_layer_uri.py
            param_db = dict()
            lst_item = uri.split(';')
            for item in lst_item:
                key_value = item.split('=')
                if len(key_value) == 2:
                    key = key_value[0].strip()
                    value = key_value[1].strip()
                    param_db[key] = value

            uri = 'service=\'driver={drv}\' dbname=\'{database}\' host={server} user=\'{uid}\' password=\'{pwd}\' '.format(
                drv=param_db['DRIVER'],
                database=param_db['DATABASE'],
                server=param_db['SERVER'],
                uid=param_db['UID'],
                pwd=param_db['PWD']
            )

            return uri

        data_source_uri = '{uri} key={primary_key} estimatedmetadata=true srid=0 table="{schema}"."{table}" sql='.format(
            uri=get_layer_uri_common(self.uri),
            primary_key=self.names.T_ID_F,
            schema=self.schema,
            table=table_name
        )
        return data_source_uri
