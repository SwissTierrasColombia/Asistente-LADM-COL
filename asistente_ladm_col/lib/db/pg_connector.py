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
from qgis.core import (QgsWkbTypes,
                       QgsDataSourceUri)

from asistente_ladm_col.lib.db.db_connector import (DBConnector,
                                                    EnumTestLevel)
from asistente_ladm_col.logic.ladm_col.queries.per_component.pg import (basic_query,
                                                                        economic_query,
                                                                        physical_query,
                                                                        legal_query,
                                                                        property_record_card_query)
from asistente_ladm_col.logic.ladm_col.queries.per_component.pg import logic_validation_queries
from asistente_ladm_col.logic.ladm_col.queries.reports.ant_report.pg import (ant_map_neighbouring_change_query,
                                                                             ant_map_plot_query)
from asistente_ladm_col.logic.ladm_col.queries.reports.annex_17_report.pg import (annex17_building_data_query,
                                                                                  annex17_point_data_query,
                                                                                  annex17_plot_data_query)
from asistente_ladm_col.config.general_config import (INTERLIS_TEST_METADATA_TABLE_PG,
                                                      ASSISTANT_SUPPORTED_MODELS,
                                                      OPERATION_MODEL_PREFIX,
                                                      CADASTRAL_FORM_MODEL_PREFIX,
                                                      VALUATION_MODEL_PREFIX,
                                                      LADM_MODEL_PREFIX,
                                                      ANT_MODEL_PREFIX,
                                                      REFERENCE_CARTOGRAPHY_PREFIX,
                                                      SNR_DATA_MODEL_PREFIX,
                                                      SUPPLIES_INTEGRATION_MODEL_PREFIX,
                                                      SUPPLIES_MODEL_PREFIX)
from asistente_ladm_col.utils.model_parser import ModelParser
from asistente_ladm_col.utils.utils import normalize_iliname
from asistente_ladm_col.config.table_mapping_config import (T_ID,
                                                            DISPLAY_NAME,
                                                            ILICODE,
                                                            DESCRIPTION)


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
            """.format(self.schema, INTERLIS_TEST_METADATA_TABLE_PG))

            return bool(cur.fetchone()[0])

        return False

    def test_connection(self, test_level=EnumTestLevel.LADM):
        """
        WARNING: We check several levels in order:
            1. SERVER
            2. DB
            3. SCHEMA
            4. LADM
            5. SCHEMA_IMPORT
          If you need to modify this method, be careful and preserve the order!!!

        :param test_level: (EnumTestLevel) level of connection with postgres
        """
        uri = self._uri

        if test_level & EnumTestLevel.SERVER:
            uri = self.get_connection_uri(self._dict_conn_params, 0)
            res, msg = self.open_connection()
            if res:
                return (True, QCoreApplication.translate("PGConnector",
                                                         "Connection to server was successful."))
            else:
                return (False, msg)

        if test_level & EnumTestLevel.DB:
            if not self._dict_conn_params['database'].strip("'") or self._dict_conn_params['database'] == 'postgres':
                return (False, QCoreApplication.translate("PGConnector",
                                                          "You should first select a database."))

        # Client side check
        if self.conn is None or self.conn.closed:
            res, msg = self.open_connection()
            if not res:
                return (res, msg)
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
                return (res, msg)

        if test_level == EnumTestLevel.DB:  # Just in the DB case
            return (True, QCoreApplication.translate("PGConnector",
                                                     "Connection to the database was successful."))

        if test_level & EnumTestLevel._CHECK_SCHEMA:
            if not self._dict_conn_params['schema'] or self._dict_conn_params['schema'] == '':
                return (False, QCoreApplication.translate("PGConnector",
                                                          "You should first select a schema."))

            if not self._schema_exists():
                return (False, QCoreApplication.translate("PGConnector",
                                                          "The schema '{}' does not exist in the database!").format(
                    self.schema))

            res, msg = self.get_schema_privileges(uri, self.schema)
            if not res:
                return (False,
                        QCoreApplication.translate("PGConnector",
                                                   "User '{}' has not enough permissions over the schema '{}'.").format(
                            self._dict_conn_params['username'],
                            self.schema))

        if test_level == EnumTestLevel.DB_SCHEMA:
            return (True, QCoreApplication.translate("PGConnector",
                                                     "Connection to the database schema was successful."))

        if test_level & EnumTestLevel._CHECK_LADM:
            if not self._metadata_exists():
                return (False, QCoreApplication.translate("PGConnector",
                                                          "The schema '{}' is not a valid LADM_COL schema. That is, the schema doesn't have the structure of the LADM_COL model.").format(
                    self.schema))

            if self.get_ili2db_version() != 4:
                return (False, QCoreApplication.translate("PGConnector",
                                                          "The DB schema '{}' was created with an old version of ili2db (v3), which is no longer supported. You need to migrate it to ili2db4.").format(
                    self.schema))


            res, msg = self.check_at_least_one_ladm_model_exists()
            if not res:
                return (res, msg)  # Version of the models is not valid

            if self.model_parser is None:
                self.model_parser = ModelParser(self)

            # Validate table and field names
            if not self.names_read:
                self._get_table_and_field_names()

            models = list()
            if self.ladm_model_exists():
                models.append(LADM_MODEL_PREFIX)
            if self.operation_model_exists():
                models.append(OPERATION_MODEL_PREFIX)
            if self.cadastral_form_model_exists():
                models.append(CADASTRAL_FORM_MODEL_PREFIX)
            if self.valuation_model_exists():
                models.append(VALUATION_MODEL_PREFIX)
            if self.ant_model_exists():
                models.append(ANT_MODEL_PREFIX)
            if self.reference_cartography_model_exists():
                models.append(REFERENCE_CARTOGRAPHY_PREFIX)
            if self.snr_data_model_exists():
                models.append(SNR_DATA_MODEL_PREFIX)
            if self.supplies_integration_model_exists():
                models.append(SUPPLIES_INTEGRATION_MODEL_PREFIX)
            if self.supplies_model_exists():
                models.append(SUPPLIES_MODEL_PREFIX)

            if not models:
                return (False, QCoreApplication.translate("PGConnector", "The database has no models from LADM_COL! As is, it cannot be used for LADM_COL Assistant!"))

            res, msg = self.names.test_names(models)
            if not res:
                return (False, QCoreApplication.translate("PGConnector",
                                                          "Table/field names from the DB are not correct. Details: {}.").format(
                    msg))

        if test_level == EnumTestLevel.LADM:
            return (True,
                    QCoreApplication.translate("PGConnector", "The schema '{}' has a valid LADM_COL structure!").format(
                        self.schema))

        if test_level & EnumTestLevel.SCHEMA_IMPORT:
            return (True, QCoreApplication.translate("PGConnector", "Connection successful!"))

        return (False, QCoreApplication.translate("PGConnector",
                                                  "There was a problem checking the connection. Most likely due to invalid or not supported test_level!"))

    def check_at_least_one_ladm_model_exists(self):
        result = True
        msg = QCoreApplication.translate("PGConnector", "The version of the models is valid.")
        models = self.get_models()
        if len(set(models) & set(ASSISTANT_SUPPORTED_MODELS)) == 0:
            result = False
            msg = QCoreApplication.translate("PGConnector",
                                             "At least one LADM model must exist. "
                                             "Supported models are '{}' but you have '{}'").format(', '.join(ASSISTANT_SUPPORTED_MODELS),
                                                                                                   ', '.join(models))
        return (result, msg)

    def open_connection(self, uri=None):
        if uri is None:
            uri = self._uri
        else:
            self.conn.close()

        if self.conn is None or self.conn.closed:
            try:
                self.conn = psycopg2.connect(uri)
            except (psycopg2.OperationalError, psycopg2.ProgrammingError) as e:
                return (
                False, QCoreApplication.translate("PGConnector", "Could not open connection! Details: {}".format(e)))

            self.logger.info(__name__, "Connection was open! {}".format(self.conn))
        else:
            self.logger.info(__name__, "Connection is already open! {}".format(self.conn))

        return (True, QCoreApplication.translate("PGConnector", "Connection is open!"))

    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.logger.info(__name__, "Connection was closed ({}) !".format(self.conn.closed))
            self.conn = None

    def validate_db(self):
        pass

    def _get_table_and_field_names(self):
        """
        Get table and field names from the DB. Should only be called once for a single connection, and should be
        refreshed after a connection changes.

        :return: dict with ilinames as keys and sqlnames as values
        """
        sql_query = """SELECT DISTINCT
                      iliclass.iliname AS table_iliname,
                      tbls.tablename AS tablename,
                      ilicol.iliname AS field_iliname,
                      a.attname AS fieldname      
                    FROM pg_catalog.pg_tables tbls
                    LEFT JOIN {schema}.t_ili2db_table_prop tp
                      ON tp.tablename = tbls.tablename
                    LEFT JOIN pg_index i
                      ON i.indrelid = CONCAT(tbls.schemaname, '.', tbls.tablename)::regclass
                    LEFT JOIN pg_attribute a
                      ON a.attrelid = i.indrelid
                    LEFT JOIN public.geometry_columns g
                      ON g.f_table_schema = tbls.schemaname
                      AND g.f_table_name = tbls.tablename
                    LEFT JOIN {schema}.t_ili2db_classname iliclass
                      ON tbls.tablename = iliclass.sqlname
                    LEFT JOIN {schema}.t_ili2db_attrname ilicol
                      ON a.attname = ilicol.sqlname 
                      AND ilicol.colowner = tbls.tablename
                    WHERE i.indisprimary AND schemaname ='{schema}' AND a.attnum >= 0
                    ORDER BY tbls.tablename, fieldname;""".format(
            schema=self.schema)  # TODO: Remove DISTINCT when ili2db 4.3.2 is released

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(sql_query)
        records = cur.fetchall()

        dict_names = dict()
        for record in records:
            if record['table_iliname'] is None:
                # Either t_ili2db_* tables (INTERLIS meta-attrs)
                continue

            record['table_iliname'] = normalize_iliname(record['table_iliname'])
            if not record['table_iliname'] in dict_names:
                dict_names[record['table_iliname']] = dict()
                dict_names[record['table_iliname']]['table_name'] = record['tablename']

            if record['field_iliname'] is None:
                # Fields for domains, like 'description' (we map it in a custom later in this class method)
                continue

            record['field_iliname'] = normalize_iliname(record['field_iliname'])
            dict_names[record['table_iliname']][record['field_iliname']] = record['fieldname']

        # Add required key-value pairs that do not come from the DB query
        dict_names[T_ID] = "t_id"
        dict_names[DISPLAY_NAME] = "dispname"
        dict_names[ILICODE] = "ilicode"
        dict_names[DESCRIPTION] = "description"

        # Map duplicate ilinames (e.g., inheriting an attribute pointing to structure)
        # Spatial_Unit-->Ext_Address_ID (Ext_Address)
        # Key: "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID"
        # Values: op_construccion_ext_direccion_id and  op_terreno_ext_direccion_id
        sql_query = """SELECT substring(a.iliname from 1 for (length(a.iliname) - position('.' in reverse(a.iliname)))) as table_iliname,
            a.iliname, a.sqlname, c.iliname as iliname2, o.iliname as colowner
            FROM {schema}.t_ili2db_attrname a
                INNER JOIN {schema}.t_ili2db_classname o ON o.sqlname = a.colowner
                INNER JOIN {schema}.t_ili2db_classname c ON c.sqlname = a.target
                INNER JOIN (SELECT a_s.iliname
                    FROM {schema}.t_ili2db_attrname a_s
                    GROUP BY a_s.iliname
                    HAVING COUNT(a_s.iliname) > 1 ) s ON a.iliname = s.iliname
            GROUP BY a.iliname, a.sqlname, c.iliname, o.iliname
            HAVING COUNT(a.iliname) = 1
            ORDER BY a.iliname""".format(schema=self.schema)
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(sql_query)
        records = cur.fetchall()
        for record in records:
            composed_key = "{}_{}".format(normalize_iliname(record['iliname']),
                                          normalize_iliname(record['iliname2']))
            record['table_iliname'] = normalize_iliname(record['table_iliname'])
            if record['table_iliname'] in dict_names:
                dict_names[record['table_iliname']][composed_key] = record['sqlname']
            else:
                record['colowner'] = normalize_iliname(record['colowner'])
                if record['colowner'] in dict_names:
                    dict_names[record['colowner']][composed_key] = record['sqlname']

        self.names.initialize_table_and_field_names(dict_names)
        self.names_read = True

        return True

    def get_uri_for_layer(self, layer_name, geometry_type=None):
        res, cur = self.get_tables_info()
        if not res:
            return (res, cur)
        data_source_uri = ''

        for record in cur:
            if record['schemaname'] == self.schema and record['tablename'] == layer_name.lower():
                if record['geometry_column']:
                    if geometry_type is not None:
                        if QgsWkbTypes.geometryType(QgsWkbTypes.parseType(record['type'])) == geometry_type:
                            data_source_uri = '{uri} key={primary_key} estimatedmetadata=true srid={srid} type={type} table="{schema}"."{table}" ({geometry_column})'.format(
                                uri=self._uri,
                                primary_key=record['primary_key'],
                                srid=record['srid'],
                                type=record['type'],
                                schema=record['schemaname'],
                                table=record['tablename'],
                                geometry_column=record['geometry_column']
                            )
                    else:
                        data_source_uri = '{uri} key={primary_key} estimatedmetadata=true srid={srid} type={type} table="{schema}"."{table}" ({geometry_column})'.format(
                            uri=self._uri,
                            primary_key=record['primary_key'],
                            srid=record['srid'],
                            type=record['type'],
                            schema=record['schemaname'],
                            table=record['tablename'],
                            geometry_column=record['geometry_column']
                        )
                else:
                    data_source_uri = '{uri} key={primary_key} table="{schema}"."{table}"'.format(
                        uri=self._uri,
                        primary_key=record['primary_key'],
                        schema=record['schemaname'],
                        table=record['tablename']
                    )
        if data_source_uri:
            return (True, data_source_uri)
        return (False, QCoreApplication.translate("PGConnector",
                                                  "Layer '{}' was not found in the database (schema: {}).").format(
            layer_name, self.schema))

    def check_and_fix_connection(self):
        if self.conn is None or self.conn.closed:
            res, msg = self.test_connection()
            if not res:
                return (res, msg)

        if self.conn.get_transaction_status() == psycopg2.extensions.TRANSACTION_STATUS_INERROR:  # 3
            self.conn.rollback()  # Go back to TRANSACTION_STATUS_IDLE (0)
            if self.conn.get_transaction_status() != psycopg2.extensions.TRANSACTION_STATUS_IDLE:
                return (False, "Error: PG transaction had an error and couldn't be recovered...")

        return (True, '')

    def get_tables_info(self):
        res, msg = self.check_and_fix_connection()
        if not res:
            return (res, msg)

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
                    SELECT
                      tbls.schemaname AS schemaname,
                      tbls.tablename AS tablename,
                      a.attname AS primary_key,
                      g.f_geometry_column AS geometry_column,
                      g.srid AS srid,
                      g.type AS type
                    FROM pg_catalog.pg_tables tbls
                    LEFT JOIN pg_index i
                      ON i.indrelid = CONCAT(tbls.schemaname, '.', tbls.tablename)::regclass
                    LEFT JOIN pg_attribute a
                      ON a.attrelid = i.indrelid
                      AND a.attnum = ANY(i.indkey)
                    LEFT JOIN public.geometry_columns g
                      ON g.f_table_schema = tbls.schemaname
                      AND g.f_table_name = tbls.tablename
                    WHERE i.indisprimary AND schemaname ='{}'
                    """.format(self.schema))
        return (True, cur)

    def retrieve_sql_data(self, sql_query):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(sql_query)
        results = cur.fetchall()
        colnames = {desc[0]: cur.description.index(desc) for desc in cur.description}
        return colnames, results

    def get_igac_basic_info(self, **kwargs):
        """
        Query by component: Basic info
        :param kwargs: dict with one of the following key-value param
               plot_t_id
               parcel_fmi
               parcel_number
               previous_parcel_number
        :return:
        """
        params = {
            'plot_t_id': 'NULL',
            'parcel_fmi': 'NULL',
            'parcel_number': 'NULL',
            'previous_parcel_number': 'NULL'
        }
        params.update(kwargs)

        query = basic_query.get_igac_basic_query(schema=self.schema,
                                                 plot_t_id=params['plot_t_id'],
                                                 parcel_fmi=params['parcel_fmi'],
                                                 parcel_number=params['parcel_number'],
                                                 previous_parcel_number=params['previous_parcel_number'],
                                                 valuation_model=self.valuation_model_exists(),
                                                 cadastral_form_model=self.cadastral_form_model_exists())

        res, msg = self.check_and_fix_connection()
        if not res:
            return (res, msg)
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        cur.execute(query)
        records = cur.fetchall()
        res = [record._asdict() for record in records]

        return res

    def get_igac_legal_info(self, **kwargs):
        """
        Query by component: Legal info
        :param kwargs: dict with one of the following key-value param
               plot_t_id
               parcel_fmi
               parcel_number
               previous_parcel_number
        :return:
        """
        params = {
            'plot_t_id': 'NULL',
            'parcel_fmi': 'NULL',
            'parcel_number': 'NULL',
            'previous_parcel_number': 'NULL'
        }
        params.update(kwargs)

        query = legal_query.get_igac_legal_query(schema=self.schema,
                                                 plot_t_id=params['plot_t_id'],
                                                 parcel_fmi=params['parcel_fmi'],
                                                 parcel_number=params['parcel_number'],
                                                 previous_parcel_number=params['previous_parcel_number'])

        res, msg = self.check_and_fix_connection()
        if not res:
            return (res, msg)
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        cur.execute(query)
        records = cur.fetchall()
        res = [record._asdict() for record in records]

        return res

    def get_igac_property_record_card_info(self, **kwargs):
        """
        Query by component: Legal info
        :param kwargs: dict with one of the following key-value param
               plot_t_id
               parcel_fmi
               parcel_number
               previous_parcel_number
        :return:
        """
        params = {
            'plot_t_id': 'NULL',
            'parcel_fmi': 'NULL',
            'parcel_number': 'NULL',
            'previous_parcel_number': 'NULL'
        }
        params.update(kwargs)

        query = property_record_card_query.get_igac_property_record_card_query(schema=self.schema,
                                                                               plot_t_id=params['plot_t_id'],
                                                                               parcel_fmi=params['parcel_fmi'],
                                                                               parcel_number=params['parcel_number'],
                                                                               previous_parcel_number=params[
                                                                                   'previous_parcel_number'],
                                                                               cadastral_form_model=self.cadastral_form_model_exists())

        res, msg = self.check_and_fix_connection()
        if not res:
            return (res, msg)
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        cur.execute(query)
        records = cur.fetchall()
        res = [record._asdict() for record in records]

        # self.logger.debug(__name__, "PROPERTY RECORD CARD QUERY: {}".format(query))

        return res

    def get_igac_physical_info(self, **kwargs):
        """
        Query by component: Physical info
        :param kwargs: dict with one of the following key-value param
               plot_t_id
               parcel_fmi
               parcel_number
               previous_parcel_number
        :return:
        """
        params = {
            'plot_t_id': 'NULL',
            'parcel_fmi': 'NULL',
            'parcel_number': 'NULL',
            'previous_parcel_number': 'NULL'
        }
        params.update(kwargs)

        query = physical_query.get_igac_physical_query(schema=self.schema,
                                                       plot_t_id=params['plot_t_id'],
                                                       parcel_fmi=params['parcel_fmi'],
                                                       parcel_number=params['parcel_number'],
                                                       previous_parcel_number=params['previous_parcel_number'],
                                                       valuation_model=self.valuation_model_exists())

        res, msg = self.check_and_fix_connection()
        if not res:
            return (res, msg)
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        cur.execute(query)
        records = cur.fetchall()
        res = [record._asdict() for record in records]

        # self.logger.debug(__name__, "PHYSICAL QUERY: {}".format(query))

        return res

    def get_igac_economic_info(self, **kwargs):
        """
        Query by component: Economic info
        :param kwargs: dict with one of the following key-value param
               plot_t_id
               parcel_fmi
               parcel_number
               previous_parcel_number
        :return:
        """
        params = {
            'plot_t_id': 'NULL',
            'parcel_fmi': 'NULL',
            'parcel_number': 'NULL',
            'previous_parcel_number': 'NULL'
        }
        params.update(kwargs)

        query = economic_query.get_igac_economic_query(schema=self.schema,
                                                       plot_t_id=params['plot_t_id'],
                                                       parcel_fmi=params['parcel_fmi'],
                                                       parcel_number=params['parcel_number'],
                                                       previous_parcel_number=params['previous_parcel_number'],
                                                       valuation_model=self.valuation_model_exists(),
                                                       cadastral_form_model=self.cadastral_form_model_exists())

        res, msg = self.check_and_fix_connection()
        if not res:
            return (res, msg)
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        cur.execute(query)
        records = cur.fetchall()
        res = [record._asdict() for record in records]

        # self.logger.debug(__name__, "ECONOMIC QUERY:".format(query))

        return res

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
            return (res, msg)

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        try:
            cur.execute(query)
            return cur.fetchall()
        except ProgrammingError:
            return None

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

    def _schema_names_list(self):
        query = """
                    SELECT n.nspname as "schema_name"
                    FROM pg_catalog.pg_namespace n
                    WHERE n.nspname !~ '^pg_' AND n.nspname <> 'information_schema' AND nspname <> 'public'
                    ORDER BY 1"""

        result = self.execute_sql_query(query)
        return result if not isinstance(result, tuple) else None

    def get_models(self, schema=None):
        query = "SELECT distinct split_part(iliname,'.',1) as modelname FROM {schema}.t_ili2db_trafo".format(
            schema=schema if schema else self.schema)
        result = self.execute_sql_query(query)
        lst_models = list()
        if result is not None and not isinstance(result, tuple):
            lst_models = [db_model['modelname'] for db_model in result] 
        self.logger.debug(__name__, "Models found: {}".format(lst_models))
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
        res, msg = self.test_connection(EnumTestLevel.SERVER)
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
            SELECT n.nspname as "schema_name" FROM pg_catalog.pg_namespace n 
            WHERE n.nspname !~ '^pg_' AND n.nspname <> 'information_schema' AND nspname <> 'public' ORDER BY "schema_name"
            """
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

    def get_schema_privileges(self, uri, schema):
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
                return (
                False, QCoreApplication.translate("PGConnector", "No information for schema '{}'.").format(schema))
            cur.close()
            conn.close()
        except Exception as e:
            return (False, QCoreApplication.translate("PGConnector",
                                                      "There was an error when obtaining privileges for schema '{}'. Details: {}").format(
                schema, e))

        if privileges['create'] and privileges['usage']:
            return (True, QCoreApplication.translate("PGConnector",
                                                     "The user has both Create and Usage priviledges over the schema."))
        else:
            return (
            False, QCoreApplication.translate("PGConnector", "The user has not enough priviledges over the schema."))

    def is_ladm_layer(self, layer):
        result = False
        if layer.dataProvider().name() == PGConnector._PROVIDER_NAME:
            layer_uri = layer.dataProvider().uri()
            db_uri = QgsDataSourceUri(self._uri)

            result = (layer_uri.schema() == self.schema and \
                      layer_uri.database() == db_uri.database() and \
                      layer_uri.host() == db_uri.host() and \
                      layer_uri.port() == db_uri.port() and \
                      layer_uri.username() == db_uri.username() and \
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
                       AND(table_name='t_ili2db_attrname' OR table_name = 't_ili2db_model' )
                       AND(column_name='owner' OR column_name = 'file' )
                    """.format(schema=self.schema))
        if cur.rowcount > 1:
            return 3
        else:
            return 4