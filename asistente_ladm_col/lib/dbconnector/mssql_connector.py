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
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsDataSourceUri)
# FIXME No deberia ir aca
from ...config.general_config import (PLUGIN_NAME, INTERLIS_TEST_METADATA_TABLE_PG, PLUGIN_DOWNLOAD_URL_IN_QGIS_REPO)
# FIXME No deberia ir aca
from qgis.core import (Qgis, QgsApplication)
from ...utils.model_parser import ModelParser


class MssqlConnector(DBConnector):
    def __init__(self, uri, schema=None, conn_dict={}):
        DBConnector.__init__(self, uri, schema)
        self.mode = 'mssql'

        # TODO check get_connection_uri call
        self.uri = uri if uri is not None else self.get_connection_uri(conn_dict, self.mode, level=1)
        self.conn = None
        self.schema = schema
        # FIXME No debería ir acá
        self.log = QgsApplication.messageLog()
        self.provider = 'mssql'
        self._tables_info = None
        self.model_parser = None

        self.dict_conn_params = self._get_dict_conn()

    def _get_dict_conn(self, uri=None):
        uri_to_dict = uri if uri is not None else self.uri

        uri_parts = uri_to_dict.split(";")

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

        result['schema'] = self.schema

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

    def test_connection(self, uri=None, level=1):
        """
        :param level: (int) level of connection with postgres
                    0 = Server
                    1 = Database
        """
        uri = self.uri if uri is None else uri

        try:
            self.conn = conn = pyodbc.connect(uri)
            self.log.logMessage("Connection was set! {}".format(self.conn), PLUGIN_NAME, Qgis.Info)
        except Exception as e:
            return (False, QCoreApplication.translate("MSSQLConnector",
                    "There was an error connecting to the database: {}").format(e))

        if not self._schema_exists() and level == 1:
            return (False, QCoreApplication.translate("MSSQLConnector",
                    "The schema '{}' does not exist in the database!").format(self.schema))

        if not self._metadata_exists() and level == 1:
            return (False, QCoreApplication.translate("MSSQLConnector",
                    "The schema '{}' is not a valid INTERLIS schema. That is, the schema doesn't have some INTERLIS metadata tables.").format(self.schema))

        # TODO Test schema permissions (*)
        if level == 1:
            if self.model_parser is None:
                self.model_parser = ModelParser(self)
            if not self.model_parser.validate_cadastre_model_version()[0]:
                return (False, QCoreApplication.translate("PGConnector",
                                                          "The version of the Cadastre-Registry model in the database is old and is not supported in this version of the plugin. Go to <a href=\"{}\">the QGIS Plugins Repo</a> to download another version of this plugin.").format(
                    PLUGIN_DOWNLOAD_URL_IN_QGIS_REPO))

        return (True, QCoreApplication.translate("MSSQLConnector", "Connection to Mssql successful!"))

    def get_dbnames_list(self, uri):
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
                # TODO Isolation level autocommit
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