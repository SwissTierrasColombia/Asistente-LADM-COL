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
from asistente_ladm_col.lib.db.db_connector import (ClientServerDB,
                                                    DBConnector)
from asistente_ladm_col.logic.ladm_col.config.reports.ant_report.pg import ant_map_plot_query
from asistente_ladm_col.logic.ladm_col.config.reports.annex_17_report.pg import (annex17_building_data_query,
                                                                                 annex17_point_data_query,
                                                                                 annex17_plot_data_query)
from asistente_ladm_col.config.ili2db_names import ILI2DBNames
from asistente_ladm_col.core.model_parser import ModelParser
from asistente_ladm_col.config.keys.ili2db_keys import *
from asistente_ladm_col.config.query_names import QueryNames


class PGConnector(ClientServerDB):
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
        self.engine = 'pg'
        self.conn = None
        self.schema = conn_dict['schema'] if 'schema' in conn_dict else ''
        self.provider = 'postgres'
        self._tables_info = None

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

    def _table_exists(self, table_name):
        if self.schema:
            cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("""
                        SELECT
                          count(tablename)
                        FROM pg_catalog.pg_tables
                        WHERE schemaname = '{}' and tablename = '{}'
            """.format(self.schema, table_name))

            return bool(cur.fetchone()[0])

        return False

    def _metadata_exists(self):
        return self._table_exists(ILI2DBNames.INTERLIS_TEST_METADATA_TABLE_PG)

    def _has_basket_col(self):
        sql_query = """SELECT count(tag)
                       FROM {schema}.t_ili2db_settings
                       WHERE tag ='{tag}' and setting='{value}';""".format(schema=self.schema,
                                                                           tag=ILI2DBNames.BASKET_COL_TAG,
                                                                           value=ILI2DBNames.BASKET_COL_VALUE)
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(sql_query)
        return bool(cur.fetchone()[0])

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

    def _get_table_and_field_names(self):
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
        return cur.fetchall()

    def _get_fk_fields(self):
        # Map FK ilinames (i.e., those whose t_ili2db_attrname target column is not NULL)
        # Spatial_Unit-->Ext_Address_ID (Ext_Address)
        #   Key: "LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID"
        #   Values: lc_construccion_ext_direccion_id and  lc_terreno_ext_direccion_id
        sql_query = """SELECT substring(a.iliname from 1 for (length(a.iliname) - position('.' in reverse(a.iliname)))) as {table_iliname},
            a.iliname, a.sqlname, c.iliname as iliname2, o.iliname as colowner
            FROM {schema}.t_ili2db_attrname a
                INNER JOIN {schema}.t_ili2db_classname o ON o.sqlname = a.colowner
                INNER JOIN {schema}.t_ili2db_classname c ON c.sqlname = a.target
            ORDER BY a.iliname""".format(table_iliname=QueryNames.TABLE_ILINAME,
                                         schema=self.schema)
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(sql_query)
        return cur.fetchall()

    def _get_ili2db_names(self):
        dict_names = dict()
        # Add required key-value pairs that do not come from the DB query
        dict_names[T_ID_KEY] = "t_id"
        dict_names[T_ILI_TID_KEY] = "t_ili_tid"
        dict_names[DISPLAY_NAME_KEY] = "dispname"
        dict_names[ILICODE_KEY] = "ilicode"
        dict_names[DESCRIPTION_KEY] = "description"
        dict_names[T_BASKET_KEY] = "t_basket"
        dict_names[T_ILI2DB_BASKET_KEY] = "t_ili2db_basket"
        dict_names[T_ILI2DB_DATASET_KEY] = "t_ili2db_dataset"
        dict_names[DATASET_T_DATASETNAME_KEY] = "datasetname"
        dict_names[BASKET_T_DATASET_KEY] = "dataset"
        dict_names[BASKET_T_TOPIC_KEY] = "topic"
        dict_names[BASKET_T_ATTACHMENT_KEY] = "attachmentkey"

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

    def get_annex17_plot_data(self, plot_id, mode, overview):
        """

        :param plot_id: t_id id of plot
        :param mode: True if you want the selected plot and False if you want the others plots
        :return:
        """
        res, msg = self.check_and_fix_connection()
        if not res:
            return (res, msg)

        if mode:
            where_id = "WHERE l.{T_ID_F} = {plot_id}".format(T_ID_F=self.names.T_ID_F, plot_id=plot_id)
        else:
            scale_zoom = 1000 if overview else 100
            where_id = """
                        WHERE l.{LC_PLOT_T_GEOMETRY_F} &&
                        (SELECT ST_Expand(ST_Envelope({LC_PLOT_T}.{LC_PLOT_T_GEOMETRY_F}), {scale_zoom})
                        FROM {schema}.{LC_PLOT_T} WHERE t_id = {plot_id}) AND l.{T_ID_F} != {plot_id}
                       """.format(LC_PLOT_T_GEOMETRY_F=self.names.LC_PLOT_T_GEOMETRY_F,
                                  LC_PLOT_T=self.names.LC_PLOT_T,
                                  T_ID_F=self.names.T_ID_F,
                                  plot_id=plot_id,
                                  scale_zoom=scale_zoom,
                                  schema=self.schema)

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = annex17_plot_data_query.get_annex17_plot_data_query(self.names, self.schema, where_id)
        cur.execute(query)

        if mode:
            return True, cur.fetchone()[0]
        else:
            return True, cur.fetchall()[0][0]

    def get_annex17_building_data(self, plot_id):
        res, msg = self.check_and_fix_connection()
        if not res:
            return (res, msg)

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = annex17_building_data_query.get_annex17_building_data_query(self.names, self.schema, plot_id)
        cur.execute(query)

        return True, cur.fetchall()[0][0]

    def get_annex17_point_data(self, plot_id):
        res, msg = self.check_and_fix_connection()
        if not res:
            return (res, msg)

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = annex17_point_data_query.get_annex17_point_data_query(self.names, self.schema, plot_id)
        cur.execute(query)

        return True, cur.fetchone()[0]

    def get_ant_map_plot_data(self, plot_id, mode, overview):
        res, msg = self.check_and_fix_connection()
        if not res:
            return (res, msg)

        if mode:
            where_id = "WHERE {LC_PLOT_T}.{T_ID_F} = {plot_id}".format(LC_PLOT_T=self.names.LC_PLOT_T,
                                                                       T_ID_F=self.names.T_ID_F,
                                                                       plot_id=plot_id)
        else:
            scale_zoom = 1000 if overview else 100
            where_id = """
                        WHERE {LC_PLOT_T}.{LC_PLOT_T_GEOMETRY_F} &&
                        (SELECT ST_Expand(ST_Envelope({LC_PLOT_T}.{LC_PLOT_T_GEOMETRY_F}), {scale_zoom})
                        FROM {schema}.{LC_PLOT_T} WHERE t_id = {plot_id}) AND {LC_PLOT_T}.{T_ID_F} != {plot_id} 
                       """.format(LC_PLOT_T_GEOMETRY_F=self.names.LC_PLOT_T_GEOMETRY_F,
                                  LC_PLOT_T=self.names.LC_PLOT_T,
                                  T_ID_F=self.names.T_ID_F,
                                  plot_id=plot_id,
                                  scale_zoom=scale_zoom,
                                  schema=self.schema)

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = ant_map_plot_query.get_ant_map_query(self.names, self.schema, where_id)
        cur.execute(query)

        if mode:
            return True, cur.fetchone()[0]
        else:
            return True, cur.fetchall()[0][0]

    def get_ant_map_road_nomenclature(self, plot_id, overview):
        res, msg = self.check_and_fix_connection()
        if not res:
            return res, msg

        if not self.cadastral_cartography_model_exists():
            return False, 'Cadastral cartography model was not found in the database.'

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = ant_map_plot_query.get_road_nomenclature(self.names, self.schema, plot_id, overview)
        cur.execute(query)

        return True, cur.fetchone()[0]

    def get_ant_map_urban_limit(self, plot_id, overview):
        res, msg = self.check_and_fix_connection()
        if not res:
            return res, msg

        if not self.cadastral_cartography_model_exists():
            return False, 'Cadastral cartography model it is not implemented'

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = ant_map_plot_query.get_urban_limit(self.names, self.schema, plot_id, overview)
        cur.execute(query)

        return True, cur.fetchone()[0]

    def get_ant_map_municipality_boundary(self, plot_id, overview):
        res, msg = self.check_and_fix_connection()
        if not res:
            return res, msg

        if not self.cadastral_cartography_model_exists():
            return False, 'Cadastral cartography model it is not implemented'

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = ant_map_plot_query.get_municipality_boundary(self.names, self.schema, plot_id, overview)
        cur.execute(query)

        return True, cur.fetchone()[0]

    def get_ant_map_boundaries(self, plot_id):
        res, msg = self.check_and_fix_connection()
        if not res:
            return res, msg

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = ant_map_plot_query.get_map_boundaries(self.names, self.schema, plot_id)
        cur.execute(query)

        return True, cur.fetchone()[0]

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

    def get_ladm_units(self):
        query = """SELECT DISTINCT tablename || '..' || columnname AS unit_key, ' [' || setting || ']' AS unit_value FROM {schema}.t_ili2db_column_prop WHERE tag LIKE 'ch.ehi.ili2db.unit'""".format(schema=self.schema)
        res, result = self.execute_sql_query(query)

        dict_units = dict()
        if res:
            for unit in result:
                dict_units[unit['unit_key']] = unit['unit_value']
            self.logger.debug(__name__, "Units found: {}".format(len(dict_units)))
        else:
            self.logger.error_msg(__name__, "Error getting units: {}".format(result))

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
        res, code, msg = self.test_connection(EnumTestLevel.SERVER_OR_FILE)
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

    def _test_connection_to_server(self):
        uri = self.get_connection_uri(self._dict_conn_params, 0)
        res, msg = self.open_connection()
        if res:
            return True, EnumTestConnectionMsg.CONNECTION_TO_SERVER_SUCCESSFUL, QCoreApplication.translate(
                "PGConnector",
                "Connection to server was successful.")
        else:
            return False, EnumTestConnectionMsg.CONNECTION_TO_SERVER_FAILED, msg

    def _test_connection_to_db(self):
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

        return True, EnumTestConnectionMsg.CONNECTION_TO_DB_SUCCESSFUL, QCoreApplication.translate("PGConnector",
                                                     "Connection to the database was successful.")

    def _test_connection_to_schema(self, user_level):
        if not self._dict_conn_params['schema'] or self._dict_conn_params['schema'] == '':
            return False, EnumTestConnectionMsg.SCHEMA_NOT_FOUND, QCoreApplication.translate("PGConnector",
                                                                                             "You should first select a schema.")

        if not self._schema_exists():
            return False, EnumTestConnectionMsg.SCHEMA_NOT_FOUND, QCoreApplication.translate("PGConnector",
                                                                                             "The schema '{}' does not exist in the database!").format(
                self.schema)

        res, msg = self.has_schema_privileges(self._uri, self.schema, user_level)
        if not res:
            return False, EnumTestConnectionMsg.USER_HAS_NO_PERMISSION, QCoreApplication.translate("PGConnector",
                                                                                                   "User '{}' has not enough permissions over the schema '{}'.").format(
                self._dict_conn_params['username'],
                self.schema)

        return True, EnumTestConnectionMsg.CONNECTION_TO_SCHEMA_SUCCESSFUL, QCoreApplication.translate("PGConnector",
                                                                                     "Connection to the database schema was successful.")

    def _test_connection_to_ladm(self, required_models):
        if not self._metadata_exists():
            return False, EnumTestConnectionMsg.INTERLIS_META_ATTRIBUTES_NOT_FOUND, QCoreApplication.translate("PGConnector",
                                                      "The schema '{}' is not a valid LADM-COL schema. That is, the schema doesn't have the structure of the LADM-COL model.").format(
                self.schema)

        if self.get_ili2db_version() != 4:
            return False, EnumTestConnectionMsg.INVALID_ILI2DB_VERSION, QCoreApplication.translate("PGConnector",
                                                      "The DB schema '{}' was created with an old version of ili2db (v3), which is no longer supported. You need to migrate it to ili2db4.").format(
                self.schema)

        if self.model_parser is None:
            self.model_parser = ModelParser(self)

        res, code, msg = self.check_db_models(required_models)
        if not res:
            return res, code, msg

        basket_required, model_name = self._db_should_have_basket_support()
        if basket_required and not self._has_basket_col():
            return False, EnumTestConnectionMsg.BASKET_COLUMN_NOT_FOUND, \
                   QCoreApplication.translate("PGConnector", "Basket column not found, but it is required by model '{}'!.").format(model_name)

        # Validate table and field names
        if self._should_update_db_mapping_values:
            self._initialize_names()

        res, msg = self.names.test_names()
        if not res:
            return False, EnumTestConnectionMsg.DB_NAMES_INCOMPLETE, QCoreApplication.translate("PGConnector",
                                                                                                "Table/field names from the DB are not correct. Details: {}.").format(
                msg)

        return True, EnumTestConnectionMsg.SCHEMA_WITH_VALID_LADM_COL_STRUCTURE, QCoreApplication.translate(
            "PGConnector", "The schema '{}' has a valid LADM-COL structure!").format(
            self.schema)

    def get_qgis_layer_uri(self, table_name):
        data_source_uri = '{uri} key={primary_key} table="{schema}"."{table}"'.format(
            uri=self.uri,
            primary_key=self.names.T_ID_F,
            schema=self.schema,
            table=table_name
        )
        return data_source_uri
