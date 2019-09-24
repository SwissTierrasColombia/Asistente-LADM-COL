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
from .db_connector import DBConnector

import pyodbc
from pyodbc import (ProgrammingError, InterfaceError)
from qgis.PyQt.QtCore import QCoreApplication
from ...config.general_config import (PLUGIN_NAME, INTERLIS_TEST_METADATA_TABLE_PG, PLUGIN_DOWNLOAD_URL_IN_QGIS_REPO)
from qgis.core import (Qgis, QgsApplication)
from ...utils.model_parser import ModelParser
from .db_connector import (DBConnector, EnumTestLevel)


class MssqlConnector(DBConnector):

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
        self.mode = 'mssql'
        self.conn = None
        self.schema = conn_dict['schema'] if 'schema' in conn_dict else ''
        self.log = QgsApplication.messageLog()
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

        result = dict()

        result['host'] = 'localhost'
        result['port'] = ''
        result['instance'] = ''
        result['username'] = ''
        result['password'] = ''
        result['database'] = ''

        if 'SERVER' in lst_item_uri:
            server_parts = lst_item_uri["SERVER"].split(',')

            if len(server_parts) > 1:
                result['port'] = server_parts[1]

            server_parts2 = server_parts[0].split('\\')

            if len(server_parts2) > 1:
                result['instance'] = server_parts2[1]

            # FIXME check if no result
            result['host'] = server_parts2[0]

        result['username'] = lst_item_uri['UID'] if 'UID' in lst_item_uri else ''
        result['password'] = lst_item_uri['PWD'] if 'PWD' in lst_item_uri else ''
        result['database'] = lst_item_uri['DATABASE'] if 'DATABASE' in lst_item_uri else ''

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
            """.format(self.schema, INTERLIS_TEST_METADATA_TABLE_PG))

            return bool(cur.fetchone()[0])

        return False

    def test_connection(self, test_level=EnumTestLevel.LADM):
        """
        :param test_level: (EnumTestLevel) level of connection
        """
        uri = self._uri

        if test_level & EnumTestLevel.SERVER:
            uri = self.get_connection_uri(self._dict_conn_params, 0)
            res, msg = self.open_connection()
            if res:
                return (True, QCoreApplication.translate("MSSQLConnector",
                                                         "Connection to server was successful."))
            else:
                return (False, msg)

        if test_level & EnumTestLevel.DB:
            if not self._dict_conn_params['database'] or self._dict_conn_params['database'] == 'master':
                return (False, QCoreApplication.translate("MSSQLConnector",
                    "You should first select a database."))

        # Client side check
        if self.conn is None:
            res, msg = self.open_connection()
            if not res:
                return (res, msg)

        try:
            # Server side check
            cur = self.conn.cursor()
            cur.execute('SELECT 1')  # This query will fail if the db is no longer connected
            cur.close()
        except Exception as e:
            # Reopen the connection if it is closed due to timeout
            self.conn.close()
            res, msg = self.open_connection()
            if not res:
                return (res, msg)

        if test_level == EnumTestLevel.DB:  # Just in the DB case
            return (True, QCoreApplication.translate("MSSQLConnector",
                                                     "Connection to the database was successful."))

        if test_level & EnumTestLevel._CHECK_SCHEMA:
            # TODO # is 'dbo' database valid?  self._dict_conn_params['schema'] == 'dbo':
            if not self._dict_conn_params['schema']:
                return (False, QCoreApplication.translate("MSSQLConnector",
                    "You should first select a schema."))
            if not self._schema_exists():
                return (False, QCoreApplication.translate("MSSQLConnector",
                    "The schema '{}' does not exist in the database!").format(self.schema))
            # TODO Test schema permissions (*)

        if test_level == EnumTestLevel.DB_SCHEMA:
            return (True, QCoreApplication.translate("PGConnector",
                                                     "Connection to the database schema was successful."))

        if test_level & EnumTestLevel._CHECK_LADM:
            if not self._metadata_exists():
                return (False, QCoreApplication.translate("MSSQLConnector",
                        "The schema '{}' is not a valid INTERLIS schema. That is, the schema doesn't have some INTERLIS metadata tables.").format(self.schema))

            if self.model_parser is None:
                self.model_parser = ModelParser(self)

            res_parser, msg_parser = self.model_parser.validate_cadastre_model_version()
            if not res_parser:
                return (False, msg_parser)

        if test_level == EnumTestLevel.LADM:
            return (True, QCoreApplication.translate("MSSQLConnector", "The schema '{}' has a valid LADM-COL structure!").format(self.schema))

        if test_level & EnumTestLevel.SCHEMA_IMPORT:
            return (True, QCoreApplication.translate("MSSQLConnector", "Connection successful!"))

        return (False, QCoreApplication.translate("MSSQLConnector", "There was a problem checking the connection. Most likely due to invalid or not supported test_level!"))

    def open_connection(self, uri=None):
        if uri is None:
            uri = self._uri
        else:
            self.conn.close()

        if self.conn is None:
            try:
                self.conn = pyodbc.connect(uri)
            except (ProgrammingError, InterfaceError, pyodbc.Error, pyodbc.OperationalError) as e:
                return (False, QCoreApplication.translate("MssqlConnector", "Could not open connection! Details: {}".format(e)))

            self.log.logMessage("Connection was open! {}".format(self.conn), PLUGIN_NAME, Qgis.Info)
        else:
            self.log.logMessage("Connection is already open! {}".format(self.conn), PLUGIN_NAME, Qgis.Info)

        return (True, QCoreApplication.translate("MssqlConnector", "Connection is open!"))

    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.log.logMessage("Connection was closed!", PLUGIN_NAME, Qgis.Info)

    def get_dbnames_list(self, uri):
        res, msg = self.test_connection(EnumTestLevel.SERVER)
        if not res:
            return (False, msg)
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

        return (True, dbnames_list)

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
            return (False, QCoreApplication.translate("MSSQLConnector",
                                               "There was an error when obtaining the list of existing schemas: {}").format(e))
        return (True, schemas_list)

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
                return (False, QCoreApplication.translate("MssqlConnector", "An error occurred while trying to create the '{}' schema: {}".format(schema_name, e)))
        cur.close()
        conn.close()
        return (True, QCoreApplication.translate("MssqlConnector", "Schema '{}' was successfully created!".format(schema_name)))

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
                return (False, QCoreApplication.translate("MssqlConnector", "An error occurred while trying to create the '{}' database: {}".format(db_name, e)))
        cur.close()
        conn.close()
        return (True, QCoreApplication.translate("MssqlConnector", "Database '{}' was successfully created!".format(db_name)))

    def get_models(self, schema=None):
        query = "SELECT modelname FROM {schema}.t_ili2db_model".format(schema=schema if schema else self.schema)
        result = self.execute_sql_query(query)
        return result if not isinstance(result, tuple) else None

    def execute_sql_query(self, query):
        """
        Generic function for executing SQL statements
        :param query: SQL Statement
        :return: List of RealDictRow
        """
        if self.conn is None:
            res, msg = self.test_connection()
            if not res:
                return (res, msg)
        cur = self.conn.cursor()

        try:
            cur.execute(query)
            return self._get_dict_result(cur)
        except pyodbc.ProgrammingError:
            return None

    def _get_dict_result(self, cur):
        columns = [column[0] for column in cur.description]

        res = []
        for row in cur.fetchall():
            my_rec = dict(zip(columns, row))
            res.append(my_rec)

        return res

    def is_ladm_layer(self, layer):
        result = False
        if layer.dataProvider().name() == MssqlConnector._PROVIDER_NAME:
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
