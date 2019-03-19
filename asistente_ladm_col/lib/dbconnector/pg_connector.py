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
                       Qgis,
                       QgsDataSourceUri,
                       QgsApplication)

from .db_connector import DBConnector
from ...config.general_config import (INTERLIS_TEST_METADATA_TABLE_PG,
                                      PLUGIN_NAME,
                                      PLUGIN_DOWNLOAD_URL_IN_QGIS_REPO)
from ...config.table_mapping_config import (ID_FIELD,
                                            PARCEL_TABLE,
                                            DEPARTMENT_FIELD,
                                            MUNICIPALITY_FIELD,
                                            ZONE_FIELD,
                                            PARCEL_NUMBER_FIELD,
                                            PARCEL_NUMBER_BEFORE_FIELD,
                                            PARCEL_TYPE_FIELD,
                                            COL_PARTY_TABLE,
                                            COL_PARTY_TYPE_FIELD,
                                            COL_PARTY_BUSINESS_NAME_FIELD,
                                            COL_PARTY_LEGAL_PARTY_FIELD,
                                            COL_PARTY_SURNAME_FIELD,
                                            COL_PARTY_FIRST_NAME_FIELD,
                                            COL_PARTY_DOC_TYPE_FIELD,
                                            UEBAUNIT_TABLE,
                                            UEBAUNIT_TABLE_PARCEL_FIELD,
                                            UEBAUNIT_TABLE_PLOT_FIELD,
                                            UEBAUNIT_TABLE_BUILDING_FIELD,
                                            UEBAUNIT_TABLE_BUILDING_UNIT_FIELD,
                                            FRACTION_TABLE,
                                            MEMBERS_TABLE)
from ...utils.model_parser import ModelParser


class PGConnector(DBConnector):
    def __init__(self, uri, schema="public", conn_dict={}):
        DBConnector.__init__(self, uri, schema)
        self.mode = 'pg'
        self.uri = uri if uri is not None else self.get_connection_uri(conn_dict, self.mode, level=1)
        self.conn = None
        self.schema = schema
        self.log = QgsApplication.messageLog()
        self.provider = 'postgres'
        self._tables_info = None

        data_source_uri = QgsDataSourceUri(self.uri)
        self.dict_conn_params = {
            'host': data_source_uri.host(),
            'port': data_source_uri.port(),
            'username': data_source_uri.username(),
            'password': data_source_uri.password(),
            'database': data_source_uri.database(),
            'schema': self.schema
        }

        # Logical validations queries
        self.logic_validation_queries = {
            'DEPARTMENT_CODE_VALIDATION': {
                'query': """SELECT {id} FROM {schema}.{table} p WHERE (p.{field} IS NOT NULL AND (length(p.{field}) !=2 OR (p.{field}~ '^[0-9]*$') = FALSE))""".format(schema=schema, table=PARCEL_TABLE, id=ID_FIELD, field=DEPARTMENT_FIELD),
                'desc_error': 'Department code must have two numerical characters.',
                'table_name': QCoreApplication.translate("LogicChecksConfigStrings", "Logic Consistency Errors in table '{table}'").format(table=PARCEL_TABLE),
                'table': PARCEL_TABLE},
            'MUNICIPALITY_CODE_VALIDATION': {
                'query': """SELECT {id} FROM {schema}.{table} p WHERE (p.{field} IS NOT NULL AND (length(p.{field}) !=3 OR (p.{field}~ '^[0-9]*$') = FALSE))""".format(schema=schema, table=PARCEL_TABLE, id=ID_FIELD, field=MUNICIPALITY_FIELD),
                'desc_error': 'Municipality code must have three numerical characters.',
                'table_name': QCoreApplication.translate("LogicChecksConfigStrings", "Logic Consistency Errors in table '{table}'").format(table=PARCEL_TABLE),
                'table': PARCEL_TABLE},
            'ZONE_CODE_VALIDATION': {
                'query': """SELECT {id} FROM {schema}.{table} p WHERE (p.{field} IS NOT NULL AND (length(p.{field}) !=2 OR (p.{field}~ '^[0-9]*$') = FALSE))""".format(schema=schema, table=PARCEL_TABLE, id=ID_FIELD, field=ZONE_FIELD),
                'desc_error': 'Zone code must have two numerical characters.',
                'table_name': QCoreApplication.translate("LogicChecksConfigStrings", "Logic Consistency Errors in table '{table}'").format(table=PARCEL_TABLE),
                'table': PARCEL_TABLE},
            'PARCEL_NUMBER_VALIDATION': {
                'query': """SELECT {id} FROM {schema}.{table} p WHERE (p.{field} IS NOT NULL AND (length(p.{field}) !=30 OR (p.{field}~ '^[0-9]*$') = FALSE))""".format(schema=schema, table=PARCEL_TABLE, id=ID_FIELD, field=PARCEL_NUMBER_FIELD),
                'desc_error': 'Parcel number must have 30 numerical characters.',
                'table_name': QCoreApplication.translate("LogicChecksConfigStrings", "Logic Consistency Errors in table '{table}'").format(table=PARCEL_TABLE),
                'table': PARCEL_TABLE},
            'PARCEL_NUMBER_BEFORE_VALIDATION': {
                'query': """SELECT {id} FROM {schema}.{table} p WHERE (p.{field} IS NOT NULL AND (length(p.{field}) !=20 OR (p.{field}~ '^[0-9]*$') = FALSE))""".format(schema=schema, table=PARCEL_TABLE, id=ID_FIELD, field=PARCEL_NUMBER_BEFORE_FIELD),
                'desc_error': 'Parcel number before must have 20 numerical characters.',
                'table_name': QCoreApplication.translate("LogicChecksConfigStrings", "Logic Consistency Errors in table '{table}'").format(table=PARCEL_TABLE),
                'table': PARCEL_TABLE},
            'COL_PARTY_TYPE_NATURAL_VALIDATION': {
                'query': """
                        SELECT p.{id},
                               CASE WHEN p.{business_name} IS NOT NULL THEN 1 ELSE 0 END AS "{business_name}",
                               CASE WHEN p.{col_party_legal_party} IS NOT NULL THEN 1 ELSE 0 END "{col_party_legal_party}",
                               CASE WHEN p.{col_party_surname} IS NULL OR length(trim(p.{col_party_surname})) > 0 is False THEN 1 ELSE 0 END "{col_party_surname}",
                               CASE WHEN p.{col_party_first_name} IS NULL OR length(trim(p.{col_party_first_name})) > 0 is False THEN 1 ELSE 0 END "{col_party_first_name}",
                               CASE WHEN p.{col_party_doc_type} = 'NIT' THEN 1 ELSE 0 END "{col_party_doc_type}"
                        FROM {schema}.{table} p
                        WHERE p.{col_party_type} = 'Persona_Natural' AND (
                            p.{business_name} IS NOT NULL OR
                            p.{col_party_legal_party} IS NOT NULL OR
                            p.{col_party_surname} IS NULL OR
                            length(trim(p.{col_party_surname})) > 0 is False OR
                            p.{col_party_first_name} IS NULL OR 
                            length(trim(p.{col_party_first_name})) > 0 is False OR
                            p.{col_party_doc_type} = 'NIT')
                """.format(schema=schema, table=COL_PARTY_TABLE, id=ID_FIELD, col_party_type=COL_PARTY_TYPE_FIELD,
                           business_name=COL_PARTY_BUSINESS_NAME_FIELD,
                           col_party_legal_party=COL_PARTY_LEGAL_PARTY_FIELD, col_party_surname=COL_PARTY_SURNAME_FIELD,
                           col_party_first_name=COL_PARTY_FIRST_NAME_FIELD,
                           col_party_doc_type=COL_PARTY_DOC_TYPE_FIELD),
                'desc_error': 'Party with type \'Persona_Natural\' is invalid.',
                'table_name': QCoreApplication.translate("LogicChecksConfigStrings", "Logic Consistency Errors in table '{table}'").format(table=COL_PARTY_TABLE),
                'table': COL_PARTY_TABLE},
            'COL_PARTY_TYPE_NO_NATURAL_VALIDATION': {
                'query': """
                            SELECT p.t_id,
                                   CASE WHEN p.{business_name} IS NULL OR length(trim(p.{business_name})) > 0 is False THEN 1 ELSE 0 END AS "{business_name}",
                                   CASE WHEN p.{col_party_legal_party} IS NULL THEN 1 ELSE 0 END AS "{col_party_legal_party}",
                                   CASE WHEN p.{col_party_surname} IS NOT NULL THEN 1 ELSE 0 END AS "{col_party_surname}",
                                   CASE WHEN p.{col_party_first_name} IS NOT NULL THEN 1 ELSE 0 END AS "{col_party_first_name}",
                                   CASE WHEN p.{col_party_doc_type} NOT IN ('NIT', 'Secuencial_IGAC', 'Secuencial_SNR') THEN 1 ELSE 0 END AS "{col_party_doc_type}"
                            FROM {schema}.{table} p
                            WHERE p.{col_party_type} = 'Persona_No_Natural' AND (
                                p.{business_name} IS NULL OR
                                length(trim(p.{business_name})) > 0 is False OR
                                p.{col_party_legal_party} IS NULL OR
                                p.{col_party_surname} IS NOT NULL OR
                                p.{col_party_first_name} IS NOT NULL OR
                                p.{col_party_doc_type} NOT IN ('NIT', 'Secuencial_IGAC', 'Secuencial_SNR'))
                        """.format(schema=schema, table=COL_PARTY_TABLE, id=ID_FIELD,
                                   col_party_type=COL_PARTY_TYPE_FIELD, business_name=COL_PARTY_BUSINESS_NAME_FIELD,
                                   col_party_legal_party=COL_PARTY_LEGAL_PARTY_FIELD,
                                   col_party_surname=COL_PARTY_SURNAME_FIELD,
                                   col_party_first_name=COL_PARTY_FIRST_NAME_FIELD,
                                   col_party_doc_type=COL_PARTY_DOC_TYPE_FIELD),
                'desc_error': 'Party with type \'Persona_No_Natural\' is invalid.',
                'table_name': QCoreApplication.translate("LogicChecksConfigStrings", "Logic Consistency Errors in table '{table}'").format(table=COL_PARTY_TABLE),
                'table': COL_PARTY_TABLE},
            'UEBAUNIT_PARCEL_VALIDATION': {
                'query': """
                    SELECT * FROM (
                        SELECT {id}, {parcel_type}, sum(count_terreno) sum_t, sum(count_construccion) sum_c, sum(count_unidadconstruccion) sum_uc FROM (
                            SELECT p.{id},
                                    p.{parcel_type},
                                    (CASE WHEN ue.{ueb_plot} IS NOT NULL THEN 1 ELSE 0 END) count_terreno,
                                    (CASE WHEN ue.{ueb_building} IS NOT NULL THEN 1 ELSE 0 END) count_construccion,
                                    (CASE WHEN ue.{ueb_building_unit} IS NOT NULL THEN 1 ELSE 0 END) count_unidadconstruccion
                            FROM {schema}.{input_table} p left join {schema}.{join_table} ue on p.{id} = ue.{join_field}
                        ) AS p_ue GROUP BY {id}, {parcel_type}
                    ) AS report WHERE
                               ({parcel_type}='NPH' AND (sum_t !=1 OR sum_uc != 0)) OR 
                               ({parcel_type} in ('PropiedadHorizontal.Matriz', 'Condominio.Matriz', 'ParqueCementerio.Matriz', 'BienUsoPublico', 'Condominio.UnidadPredial') AND (sum_t!=1 OR sum_uc > 0)) OR 
                               ({parcel_type} in ('Via', 'ParqueCementerio.UnidadPrivada') AND (sum_t !=1 OR sum_uc > 0 OR sum_c > 0)) OR 
                               ({parcel_type}='PropiedadHorizontal.UnidadPredial' AND (sum_t !=0 OR sum_c != 0 OR sum_uc = 0 )) OR 
                               ({parcel_type}='Mejora' AND (sum_t !=0 OR sum_c != 1 OR sum_uc != 0))
                """.format(schema=schema, input_table=PARCEL_TABLE, join_table=UEBAUNIT_TABLE, join_field=UEBAUNIT_TABLE_PARCEL_FIELD, id=ID_FIELD, parcel_type=PARCEL_TYPE_FIELD,
                           ueb_plot=UEBAUNIT_TABLE_PLOT_FIELD, ueb_building=UEBAUNIT_TABLE_BUILDING_FIELD, ueb_building_unit=UEBAUNIT_TABLE_BUILDING_UNIT_FIELD),
                'desc_error': 'Parcel must have one or more spatial units associated with it.',
                'table_name': QCoreApplication.translate("LogicChecksConfigStrings", "Errors in relationships between Spatial Units and Parcels"),
                'table': PARCEL_TABLE},
            'PARCEL_TYPE_AND_22_POSITION_OF_PARCEL_NUMBER_VALIDATION': {
                'query': """
                        SELECT p.{id}, p.{parcel_type} FROM {schema}.{table} p
                        WHERE (p.{parcel_number} IS NOT NULL AND 
                               (substring(p.{parcel_number},22,1) != '0' AND p.{parcel_type}='NPH') OR
                               (substring(p.{parcel_number},22,1) != '9' AND strpos(p.{parcel_type}, 'PropiedadHorizontal.') != 0) OR
                               (substring(p.{parcel_number},22,1) != '8' AND strpos(p.{parcel_type}, 'Condominio.') != 0) OR
                               (substring(p.{parcel_number},22,1) != '7' AND strpos(p.{parcel_type}, 'ParqueCementerio.') != 0) OR
                               (substring(p.{parcel_number},22,1) != '5' AND p.{parcel_type}='Mejora') OR
                               (substring(p.{parcel_number},22,1) != '4' AND p.{parcel_type}='Via') OR
                               (substring(p.{parcel_number},22,1) != '3' AND p.{parcel_type}='BienUsoPublico')
                        )""".format(schema=schema, table=PARCEL_TABLE, id=ID_FIELD, parcel_number=PARCEL_NUMBER_FIELD, parcel_type=PARCEL_TYPE_FIELD),
                'desc_error': 'The position 22 of the parcel number must correspond to the type of parcel.',
                'table_name': QCoreApplication.translate("LogicChecksConfigStrings", "Logic Consistency Errors in table '{table}'").format(table=PARCEL_TABLE),
                'table': PARCEL_TABLE},
            'DUPLICATE_RECORDS_IN_TABLE': {
                'query': """
                    SELECT array_to_string(duplicate_ids, ',') AS "duplicate_ids", duplicate_total
                    FROM (
                        SELECT unique_concat,  array_agg({id}) duplicate_ids, array_length(array_agg({id}), 1) duplicate_total
                        FROM (
                            SELECT concat({fields}) unique_concat, {id}, 
                            row_number() OVER(PARTITION BY {fields} ORDER BY {id} asc) AS row
                            FROM {schema}.{table}
                        ) AS count_rows
                        GROUP BY unique_concat
                    ) report
                    WHERE duplicate_total > 1
                """,
                'desc_error': 'Check duplicate records in a table',
                'table_name': '',
                'table': ''},
            'GROUP_PARTY_FRACTIONS_SHOULD_SUM_1': {
                'query': """WITH grupos AS (
                        SELECT array_agg(t_id) AS tids, agrupacion
                        FROM {schema}.{members}
                        GROUP BY agrupacion
                    ),
                     sumas AS (
                        SELECT grupos.agrupacion, grupos.tids as miembros, SUM(fraccion.numerador::float/fraccion.denominador) as suma_fracciones
                        FROM {schema}.{fraction}, grupos
                        WHERE miembros_participacion = ANY(grupos.tids)
                        GROUP BY agrupacion, tids
                    )
                    SELECT sumas.*
                    FROM sumas
                    WHERE sumas.suma_fracciones != 1""".format(schema=self.schema, fraction=FRACTION_TABLE, members=MEMBERS_TABLE),
                'desc_error': 'Group Party Fractions should sum 1',
                'table_name': QCoreApplication.translate("LogicChecksConfigStrings", "Fractions do not sum 1").format(PARCEL_TABLE),
                'table': '{fraction}_and_{members}'.format(fraction=FRACTION_TABLE, members=MEMBERS_TABLE)},
            'PARCELS_WITH_NO_RIGHT': {
                'query': """SELECT p.t_id
                   FROM {schema}.predio p
                   WHERE p.t_id NOT IN (
                        SELECT unidad_predio FROM {schema}.col_derecho)""".format(schema=self.schema),
                'desc_error': 'Get parcels with no right',
                'table_name': QCoreApplication.translate("LogicChecksConfigStrings", 'Parcels with no right'),
                'table': PARCEL_TABLE},
            'PARCELS_WITH_REPEATED_DOMAIN_RIGHT': {
                'query': """SELECT conteo.unidad_predio
                    FROM {schema}.predio p, (
                        SELECT unidad_predio, count(tipo) as dominios
                        FROM {schema}.col_derecho
                        WHERE tipo='Dominio'
                        GROUP BY unidad_predio
                    ) as conteo
                    WHERE p.t_id = conteo.unidad_predio and conteo.dominios > 1""".format(schema=self.schema),
                'desc_error': 'Get parcels with duplicate rights',
                'table_name': QCoreApplication.translate("LogicChecksConfigStrings", "Parcels with repeated domain right"),
                'table': PARCEL_TABLE}
        }

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
        schema = schema if schema is not None else self.schema
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

    def test_connection(self, uri=None, level=1):
        """
        :param level: (int) level of connection with postgres
                    0 = Server
                    1 = Database
        """
        uri = self.uri if uri is None else uri
        try:
            self.conn = psycopg2.connect(uri)
            self.log.logMessage("Connection was set! {}".format(self.conn), PLUGIN_NAME, Qgis.Info)
        except Exception as e:
            return (False, QCoreApplication.translate("PGConnector",
                    "There was an error connecting to the database: {}").format(e))

        # No longer needed, we can connect to empty DBs, so we want to avoid showing this particular message
        # if not self._postgis_exists() and level == 1:
        #     return (False, QCoreApplication.translate("PGConnector",
        #             "The current database does not have PostGIS installed! Please install it before proceeding."))

        if not self._schema_exists() and level == 1:
            return (False, QCoreApplication.translate("PGConnector",
                    "The schema '{}' does not exist in the database!").format(self.schema))
        if not self._metadata_exists() and level == 1:
            return (False, QCoreApplication.translate("PGConnector",
                    "The schema '{}' is not a valid INTERLIS schema. That is, the schema doesn't have some INTERLIS metadata tables.").format(self.schema))

        res, msg = self.get_schema_privileges(uri, self.schema)
        if res:
            if msg['create'] and msg['usage']:
                if level == 1:
                    try:
                        if self.model_parser is None:
                            self.model_parser = ModelParser(self)
                        if not self.model_parser.validate_cadastre_model_version()[0]:
                            return (False, QCoreApplication.translate("PGConnector", "The version of the Cadastre-Registry model in the database is old and is not supported in this version of the plugin. Go to <a href=\"{}\">the QGIS Plugins Repo</a> to download another version of this plugin.").format(PLUGIN_DOWNLOAD_URL_IN_QGIS_REPO))
                    except psycopg2.ProgrammingError as e:
                        # if it is not possible to access the schema due to lack of privileges
                        return (False,
                                QCoreApplication.translate("PGConnector",
                                                           "User '{}' has not enough permissions over the schema '{}'. Details: {}").format(
                                                                self.dict_conn_params['username'],
                                                                self.schema,
                                                                e))
            else:
                return (False,
                        QCoreApplication.translate("PGConnector",
                                                   "User '{}' has not enough permissions over the schema '{}'.").format(
                            self.dict_conn_params['username'],
                            self.schema))
        else:
            return (False, msg)

        return (True, QCoreApplication.translate("PGConnector", "Connection to PostGIS successful!"))

    def save_connection(self):
        if self.conn is None:
            self.conn = psycopg2.connect(self.uri)
            self.log.logMessage("Connection was set! {}".format(self.conn), PLUGIN_NAME, Qgis.Info)

    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.log.logMessage("Connection was closed!", PLUGIN_NAME, Qgis.Info)

    def validate_db(self):
        pass

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
                                uri=self.uri,
                                primary_key=record['primary_key'],
                                srid=record['srid'],
                                type=record['type'],
                                schema=record['schemaname'],
                                table=record['tablename'],
                                geometry_column=record['geometry_column']
                            )
                    else:
                        data_source_uri = '{uri} key={primary_key} estimatedmetadata=true srid={srid} type={type} table="{schema}"."{table}" ({geometry_column})'.format(
                            uri=self.uri,
                            primary_key=record['primary_key'],
                            srid=record['srid'],
                            type=record['type'],
                            schema=record['schemaname'],
                            table=record['tablename'],
                            geometry_column=record['geometry_column']
                        )
                else:
                    data_source_uri = '{uri} key={primary_key} table="{schema}"."{table}"'.format(
                        uri=self.uri,
                        primary_key=record['primary_key'],
                        schema=record['schemaname'],
                        table=record['tablename']
                    )
        if data_source_uri:
            return (True, data_source_uri)
        return (False, QCoreApplication.translate("PGConnector", "Layer '{}' was not found in the database (schema: {}).").format(layer_name, self.schema))

    def get_tables_info(self):
        if self.conn is None:
            res, msg = self.test_connection()
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

        query = """
        WITH
         terrenos_seleccionados AS (
        	SELECT {plot_t_id} AS ue_terreno WHERE '{plot_t_id}' <> 'NULL'
        		UNION
        	SELECT uebaunit.ue_terreno FROM {schema}.predio LEFT JOIN {schema}.uebaunit ON predio.t_id = uebaunit.baunit_predio  WHERE uebaunit.ue_terreno IS NOT NULL AND CASE WHEN '{parcel_fmi}' = 'NULL' THEN  1 = 2 ELSE predio.fmi = '{parcel_fmi}' END
        		UNION
        	SELECT uebaunit.ue_terreno FROM {schema}.predio LEFT JOIN {schema}.uebaunit ON predio.t_id = uebaunit.baunit_predio  WHERE uebaunit.ue_terreno IS NOT NULL AND CASE WHEN '{parcel_number}' = 'NULL' THEN  1 = 2 ELSE predio.numero_predial = '{parcel_number}' END
        		UNION
        	SELECT uebaunit.ue_terreno FROM {schema}.predio LEFT JOIN {schema}.uebaunit ON predio.t_id = uebaunit.baunit_predio  WHERE uebaunit.ue_terreno IS NOT NULL AND CASE WHEN '{previous_parcel_number}' = 'NULL' THEN  1 = 2 ELSE predio.numero_predial_anterior = '{previous_parcel_number}' END
         ),
         predios_seleccionados AS (
        	SELECT uebaunit.baunit_predio as t_id FROM {schema}.uebaunit WHERE uebaunit.ue_terreno = {plot_t_id} AND '{plot_t_id}' <> 'NULL'
        		UNION
        	SELECT t_id FROM {schema}.predio WHERE CASE WHEN '{parcel_fmi}' = 'NULL' THEN  1 = 2 ELSE predio.fmi = '{parcel_fmi}' END
        		UNION
        	SELECT t_id FROM {schema}.predio WHERE CASE WHEN '{parcel_number}' = 'NULL' THEN  1 = 2 ELSE predio.numero_predial = '{parcel_number}' END
        		UNION
        	SELECT t_id FROM {schema}.predio WHERE CASE WHEN '{previous_parcel_number}' = 'NULL' THEN  1 = 2 ELSE predio.numero_predial_anterior = '{previous_parcel_number}' END
         ),
         construcciones_seleccionadas AS (
        	 SELECT ue_construccion FROM {schema}.uebaunit WHERE uebaunit.baunit_predio IN (SELECT predios_seleccionados.t_id FROM predios_seleccionados WHERE predios_seleccionados.t_id IS NOT NULL) AND ue_construccion IS NOT NULL
         ),
         unidadesconstruccion_seleccionadas AS (
        	 SELECT unidadconstruccion.t_id FROM {schema}.unidadconstruccion WHERE unidadconstruccion.construccion IN (SELECT ue_construccion FROM construcciones_seleccionadas)
         ),
         uc_extdireccion AS (
        	SELECT extdireccion.unidadconstruccion_ext_direccion_id,
        		json_agg(
        				json_build_object('id', extdireccion.t_id,
        									   'attributes', json_build_object('País', extdireccion.pais,
        																	   'Departamento', extdireccion.departamento,
        																	   'Ciudad', extdireccion.ciudad,
        																	   'Código postal', extdireccion.codigo_postal,
        																	   'Apartado correo', extdireccion.apartado_correo,
        																	   'Nombre calle', extdireccion.nombre_calle))
        		) FILTER(WHERE extdireccion.t_id IS NOT NULL) AS extdireccion
        	FROM {schema}.extdireccion WHERE unidadconstruccion_ext_direccion_id IN (SELECT * FROM unidadesconstruccion_seleccionadas)
        	GROUP BY extdireccion.unidadconstruccion_ext_direccion_id
         ),
         info_uc AS (
        	 SELECT unidadconstruccion.construccion,
        			json_agg(json_build_object('id', unidadconstruccion.t_id,
        							  'attributes', json_build_object('Número de pisos', unidadconstruccion.numero_pisos,
        """

        if self.valuation_model_exists():
            query += """
        															  'Número de habitaciones', unidad_construccion.num_habitaciones,
        															  'Número de baños', unidad_construccion.num_banios,
        															  'Número de locales', unidad_construccion.num_locales,
        															  'Uso', unidad_construccion.uso,
        															  'Puntuación', unidad_construccion.puntuacion,
            """
        else:
            query += """
            															  'Número de habitaciones', NULL,
            															  'Número de baños', NULL,
            															  'Número de locales', NULL,
            															  'Uso', NULL,
            															  'Puntuación', NULL,
                """

        query += """
        															  'Área construida', unidadconstruccion.area_construida,
        															  'extdireccion', COALESCE(uc_extdireccion.extdireccion, '[]')
        															 ))) FILTER(WHERE unidadconstruccion.t_id IS NOT NULL)  as unidadconstruccion
        	 FROM {schema}.unidadconstruccion LEFT JOIN uc_extdireccion ON unidadconstruccion.t_id = uc_extdireccion.unidadconstruccion_ext_direccion_id
        """

        if self.valuation_model_exists():
            query += """
        	 LEFT JOIN {schema}.avaluounidadconstruccion ON unidadconstruccion.t_id = avaluounidadconstruccion.ucons
        	 LEFT JOIN {schema}.unidad_construccion ON avaluounidadconstruccion.aucons = unidad_construccion.t_id
            """

        query += """
        	 WHERE unidadconstruccion.t_id IN (SELECT * FROM unidadesconstruccion_seleccionadas)
        	 GROUP BY unidadconstruccion.construccion
         ),
         c_extdireccion AS (
        	SELECT extdireccion.construccion_ext_direccion_id,
        		json_agg(
        				json_build_object('id', extdireccion.t_id,
        									   'attributes', json_build_object('País', extdireccion.pais,
        																	   'Departamento', extdireccion.departamento,
        																	   'Ciudad', extdireccion.ciudad,
        																	   'Código postal', extdireccion.codigo_postal,
        																	   'Apartado correo', extdireccion.apartado_correo,
        																	   'Nombre calle', extdireccion.nombre_calle))
        		) FILTER(WHERE extdireccion.t_id IS NOT NULL) AS extdireccion
        	FROM {schema}.extdireccion WHERE construccion_ext_direccion_id IN (SELECT * FROM construcciones_seleccionadas)
        	GROUP BY extdireccion.construccion_ext_direccion_id
         ),
         info_construccion as (
        	 SELECT uebaunit.baunit_predio,
        			json_agg(json_build_object('id', construccion.t_id,
        							  'attributes', json_build_object('Área construcción', construccion.area_construccion,
        															  'extdireccion', COALESCE(c_extdireccion.extdireccion, '[]'),
        															  'unidadconstruccion', COALESCE(info_uc.unidadconstruccion, '[]')
        															 ))) FILTER(WHERE construccion.t_id IS NOT NULL) as construccion
        	 FROM {schema}.construccion LEFT JOIN c_extdireccion ON construccion.t_id = c_extdireccion.construccion_ext_direccion_id
        	 LEFT JOIN info_uc ON construccion.t_id = info_uc.construccion
             LEFT JOIN {schema}.uebaunit ON uebaunit.ue_construccion = info_uc.construccion
        	 WHERE construccion.t_id IN (SELECT * FROM construcciones_seleccionadas)
        	 GROUP BY uebaunit.baunit_predio
         ),
         info_predio AS (
        	 SELECT uebaunit.ue_terreno,
        			json_agg(json_build_object('id', predio.t_id,
        							  'attributes', json_build_object('Departamento', predio.departamento,
        															  'Municipio', predio.municipio,
        															  'Zona', predio.zona,
        															  'NUPRE', predio.nupre,
        															  'FMI', predio.fmi,
        															  'Número predial', predio.numero_predial,
        															  'Número predial anterior', predio.numero_predial_anterior,
        															  'Tipo', predio.tipo,
        """

        if self.property_record_card_model_exists():
            query += """
        															  'Destinación económica', predio_ficha.destinacion_economica,
            """
        else:
            query += """
            														  'Destinación económica', NULL,
                """

        query += """
        															  'construccion', COALESCE(info_construccion.construccion, '[]')
        															 ))) FILTER(WHERE predio.t_id IS NOT NULL) as predio
        	 FROM {schema}.predio LEFT JOIN {schema}.uebaunit ON uebaunit.baunit_predio = predio.t_id
        	 LEFT JOIN info_construccion ON predio.t_id = info_construccion.baunit_predio
        """

        if self.property_record_card_model_exists():
            query += """
        	 LEFT JOIN {schema}.predio_ficha ON predio_ficha.crpredio = predio.t_id
            """

        query += """
        	 WHERE predio.t_id IN (SELECT * FROM predios_seleccionados) AND uebaunit.ue_terreno IS NOT NULL
             GROUP BY uebaunit.ue_terreno
         ),
         t_extdireccion AS (
        	SELECT extdireccion.terreno_ext_direccion_id,
        		json_agg(
        				json_build_object('id', extdireccion.t_id,
        									   'attributes', json_build_object('País', extdireccion.pais,
        																	   'Departamento', extdireccion.departamento,
        																	   'Ciudad', extdireccion.ciudad,
        																	   'Código postal', extdireccion.codigo_postal,
        																	   'Apartado correo', extdireccion.apartado_correo,
        																	   'Nombre calle', extdireccion.nombre_calle))
        		) FILTER(WHERE extdireccion.t_id IS NOT NULL) AS extdireccion
        	FROM {schema}.extdireccion WHERE terreno_ext_direccion_id IN (SELECT * FROM terrenos_seleccionados)
        	GROUP BY extdireccion.terreno_ext_direccion_id
         ),
         info_terreno AS (
        	SELECT terreno.t_id,
              json_build_object('id', terreno.t_id,
        						'attributes', json_build_object('Área de terreno', terreno.area_calculada,
        														'extdireccion', COALESCE(t_extdireccion.extdireccion, '[]'),
        														'predio', COALESCE(info_predio.predio, '[]')
        													   )) as terreno
            FROM {schema}.terreno LEFT JOIN info_predio ON info_predio.ue_terreno = terreno.t_id
        	LEFT JOIN t_extdireccion ON terreno.t_id = t_extdireccion.terreno_ext_direccion_id
        	WHERE terreno.t_id IN (SELECT * FROM terrenos_seleccionados)
         )
        SELECT json_agg(info_terreno.terreno) AS terreno FROM info_terreno
        """

        query = query.format(schema=self.schema,
                             plot_t_id=params['plot_t_id'],
                             parcel_fmi=params['parcel_fmi'],
                             parcel_number=params['parcel_number'],
                             previous_parcel_number=params['previous_parcel_number'])


        if self.conn is None:
            res, msg = self.test_connection()
            if not res:
                return (res, msg)
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        cur.execute(query)
        records = cur.fetchall()
        res = [record._asdict() for record in records]

        #print("BASIC QUERY:", query)

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

        query = """
        WITH
         terrenos_seleccionados AS (
        	SELECT {plot_t_id} AS ue_terreno WHERE '{plot_t_id}' <> 'NULL'
        		UNION
        	SELECT uebaunit.ue_terreno FROM {schema}.predio LEFT JOIN {schema}.uebaunit ON predio.t_id = uebaunit.baunit_predio  WHERE uebaunit.ue_terreno IS NOT NULL AND CASE WHEN '{parcel_fmi}' = 'NULL' THEN  1 = 2 ELSE predio.fmi = '{parcel_fmi}' END
        		UNION
        	SELECT uebaunit.ue_terreno FROM {schema}.predio LEFT JOIN {schema}.uebaunit ON predio.t_id = uebaunit.baunit_predio  WHERE uebaunit.ue_terreno IS NOT NULL AND CASE WHEN '{parcel_number}' = 'NULL' THEN  1 = 2 ELSE predio.numero_predial = '{parcel_number}' END
        		UNION
        	SELECT uebaunit.ue_terreno FROM {schema}.predio LEFT JOIN {schema}.uebaunit ON predio.t_id = uebaunit.baunit_predio  WHERE uebaunit.ue_terreno IS NOT NULL AND CASE WHEN '{previous_parcel_number}' = 'NULL' THEN  1 = 2 ELSE predio.numero_predial_anterior = '{previous_parcel_number}' END
         ),
         predios_seleccionados AS (
        	SELECT uebaunit.baunit_predio as t_id FROM {schema}.uebaunit WHERE uebaunit.ue_terreno = {plot_t_id} AND '{plot_t_id}' <> 'NULL'
        		UNION
        	SELECT t_id FROM {schema}.predio WHERE CASE WHEN '{parcel_fmi}' = 'NULL' THEN  1 = 2 ELSE predio.fmi = '{parcel_fmi}' END
        		UNION
        	SELECT t_id FROM {schema}.predio WHERE CASE WHEN '{parcel_number}' = 'NULL' THEN  1 = 2 ELSE predio.numero_predial = '{parcel_number}' END
        		UNION
        	SELECT t_id FROM {schema}.predio WHERE CASE WHEN '{previous_parcel_number}' = 'NULL' THEN  1 = 2 ELSE predio.numero_predial_anterior = '{previous_parcel_number}' END
         ),
         derechos_seleccionados AS (
        	 SELECT col_derecho.t_id FROM {schema}.col_derecho WHERE col_derecho.unidad_predio IN (SELECT * FROM predios_seleccionados)
         ),
         derecho_interesados AS (
        	 SELECT col_derecho.interesado_col_interesado, col_derecho.t_id FROM {schema}.col_derecho WHERE col_derecho.t_id IN (SELECT * FROM derechos_seleccionados) AND col_derecho.interesado_col_interesado IS NOT NULL
         ),
         derecho_agrupacion_interesados AS (
        	 SELECT col_derecho.interesado_la_agrupacion_interesados, miembros.interesados_col_interesado
        	 FROM {schema}.col_derecho LEFT JOIN {schema}.miembros ON col_derecho.interesado_la_agrupacion_interesados = miembros.agrupacion
        	 WHERE col_derecho.t_id IN (SELECT * FROM derechos_seleccionados) AND col_derecho.interesado_la_agrupacion_interesados IS NOT NULL
         ),
          restricciones_seleccionadas AS (
        	 SELECT col_restriccion.t_id FROM {schema}.col_restriccion WHERE col_restriccion.unidad_predio IN (SELECT * FROM predios_seleccionados)
         ),
         restriccion_interesados AS (
        	 SELECT col_restriccion.interesado_col_interesado, col_restriccion.t_id FROM {schema}.col_restriccion WHERE col_restriccion.t_id IN (SELECT * FROM restricciones_seleccionadas) AND col_restriccion.interesado_col_interesado IS NOT NULL
         ),
         restriccion_agrupacion_interesados AS (
        	 SELECT col_restriccion.interesado_la_agrupacion_interesados, miembros.interesados_col_interesado
        	 FROM {schema}.col_restriccion LEFT JOIN {schema}.miembros ON col_restriccion.interesado_la_agrupacion_interesados = miembros.agrupacion
        	 WHERE col_restriccion.t_id IN (SELECT * FROM restricciones_seleccionadas) AND col_restriccion.interesado_la_agrupacion_interesados IS NOT NULL
         ),
         responsabilidades_seleccionadas AS (
        	 SELECT col_responsabilidad.t_id FROM {schema}.col_responsabilidad WHERE col_responsabilidad.unidad_predio IN (SELECT * FROM predios_seleccionados)
         ),
         responsabilidades_interesados AS (
        	 SELECT col_responsabilidad.interesado_col_interesado, col_responsabilidad.t_id FROM {schema}.col_responsabilidad WHERE col_responsabilidad.t_id IN (SELECT * FROM responsabilidades_seleccionadas) AND col_responsabilidad.interesado_col_interesado IS NOT NULL
         ),
         responsabilidades_agrupacion_interesados AS (
        	 SELECT col_responsabilidad.interesado_la_agrupacion_interesados, miembros.interesados_col_interesado
        	 FROM {schema}.col_responsabilidad LEFT JOIN {schema}.miembros ON col_responsabilidad.interesado_la_agrupacion_interesados = miembros.agrupacion
        	 WHERE col_responsabilidad.t_id IN (SELECT * FROM responsabilidades_seleccionadas) AND col_responsabilidad.interesado_la_agrupacion_interesados IS NOT NULL
         ),
         hipotecas_seleccionadas AS (
        	 SELECT col_hipoteca.t_id FROM {schema}.col_hipoteca WHERE col_hipoteca.unidad_predio IN (SELECT * FROM predios_seleccionados)
         ),
         hipotecas_interesados AS (
        	 SELECT col_hipoteca.interesado_col_interesado, col_hipoteca.t_id FROM {schema}.col_hipoteca WHERE col_hipoteca.t_id IN (SELECT * FROM hipotecas_seleccionadas) AND col_hipoteca.interesado_col_interesado IS NOT NULL
         ),
         hipotecas_agrupacion_interesados AS (
        	 SELECT col_hipoteca.interesado_la_agrupacion_interesados, miembros.interesados_col_interesado
        	 FROM {schema}.col_hipoteca LEFT JOIN {schema}.miembros ON col_hipoteca.interesado_la_agrupacion_interesados = miembros.agrupacion
        	 WHERE col_hipoteca.t_id IN (SELECT * FROM hipotecas_seleccionadas) AND col_hipoteca.interesado_la_agrupacion_interesados IS NOT NULL
         ),
        ------------------------------------------------------------------------------------------
        -- INFO DERECHOS
        ------------------------------------------------------------------------------------------
         info_contacto_interesados_derecho AS (
        		SELECT interesado_contacto.interesado,
        		  json_agg(
        				json_build_object('id', interesado_contacto.t_id,
        									   'attributes', json_build_object('Teléfono 1', interesado_contacto.telefono1,
        																	   'Teléfono 2', interesado_contacto.telefono2,
        																	   'Domicilio notificación', interesado_contacto.domicilio_notificacion,
        																	   'Correo_Electrónico', interesado_contacto.correo_electronico,
        																	   'Origen_de_datos', interesado_contacto.origen_datos)))
        		FILTER(WHERE interesado_contacto.t_id IS NOT NULL) AS interesado_contacto
        		FROM {schema}.interesado_contacto LEFT JOIN derecho_interesados ON derecho_interesados.interesado_col_interesado = interesado_contacto.interesado
        		WHERE interesado_contacto.interesado IN (SELECT derecho_interesados.interesado_col_interesado FROM derecho_interesados)
        		GROUP BY interesado_contacto.interesado
         ),
         info_interesados_derecho AS (
        	 SELECT derecho_interesados.t_id,
        	  json_agg(
        		json_build_object('id', col_interesado.t_id,
        						  'attributes', json_build_object('Tipo', col_interesado.tipo,
        						                                  'Tipo interesado jurídico', col_interesado.tipo_interesado_juridico,
        														  'Documento de identidad', col_interesado.documento_identidad,
        														  'Tipo de documento', col_interesado.tipo_documento,
        														  'Primer apellido', col_interesado.primer_apellido,
        														  'Primer nombre', col_interesado.primer_nombre,
        														  'Segundo apellido', col_interesado.segundo_apellido,
        														  'Segundo nombre', col_interesado.segundo_nombre,
        														  'Género', col_interesado.genero,
        														  'Razón social',col_interesado.razon_social,
        														  'Nombre', col_interesado.nombre,
        														  'interesado_contacto', COALESCE(info_contacto_interesados_derecho.interesado_contacto, '[]')))
        	 ) FILTER (WHERE col_interesado.t_id IS NOT NULL) AS col_interesado
        	 FROM derecho_interesados LEFT JOIN {schema}.col_interesado ON col_interesado.t_id = derecho_interesados.interesado_col_interesado
        	 LEFT JOIN info_contacto_interesados_derecho ON info_contacto_interesados_derecho.interesado = col_interesado.t_id
        	 GROUP BY derecho_interesados.t_id
         ),
         info_contacto_interesado_agrupacion_interesados_derecho AS (
        		SELECT interesado_contacto.interesado,
        		  json_agg(
        				json_build_object('id', interesado_contacto.t_id,
        									   'attributes', json_build_object('Teléfono 1', interesado_contacto.telefono1,
        																	   'Teléfono 2', interesado_contacto.telefono2,
        																	   'Domicilio notificación', interesado_contacto.domicilio_notificacion,
        																	   'Correo_Electrónico', interesado_contacto.correo_electronico,
        																	   'Origen_de_datos', interesado_contacto.origen_datos)))
        		FILTER(WHERE interesado_contacto.t_id IS NOT NULL) AS interesado_contacto
        		FROM {schema}.interesado_contacto LEFT JOIN derecho_interesados ON derecho_interesados.interesado_col_interesado = interesado_contacto.interesado
        		WHERE interesado_contacto.interesado IN (SELECT DISTINCT derecho_agrupacion_interesados.interesados_col_interesado FROM derecho_agrupacion_interesados)
        		GROUP BY interesado_contacto.interesado
         ),
         info_interesados_agrupacion_interesados_derecho AS (
        	 SELECT derecho_agrupacion_interesados.interesado_la_agrupacion_interesados,
        	  json_agg(
        		json_build_object('id', col_interesado.t_id,
        						  'attributes', json_build_object('Tipo', col_interesado.tipo,
        														  'Tipo interesado jurídico', col_interesado.tipo_interesado_juridico,
        														  'Documento de identidad', col_interesado.documento_identidad,
        														  'Tipo de documento', col_interesado.tipo_documento,
        														  'Primer apellido', col_interesado.primer_apellido,
        														  'Primer nombre', col_interesado.primer_nombre,
        														  'Segundo apellido', col_interesado.segundo_apellido,
        														  'Segundo nombre', col_interesado.segundo_nombre,
        														  'Género', col_interesado.genero,
        														  'Razón social',col_interesado.razon_social,
        														  'Nombre', col_interesado.nombre,
        														  'interesado_contacto', COALESCE(info_contacto_interesado_agrupacion_interesados_derecho.interesado_contacto, '[]'),
        														  'fraccion', ROUND((fraccion.numerador::numeric/fraccion.denominador::numeric)*100,2) ))
        	 ) FILTER (WHERE col_interesado.t_id IS NOT NULL) AS col_interesado
        	 FROM derecho_agrupacion_interesados LEFT JOIN {schema}.col_interesado ON col_interesado.t_id = derecho_agrupacion_interesados.interesados_col_interesado
        	 LEFT JOIN info_contacto_interesado_agrupacion_interesados_derecho ON info_contacto_interesado_agrupacion_interesados_derecho.interesado = col_interesado.t_id
        	 LEFT JOIN {schema}.miembros ON (miembros.agrupacion::text || miembros.interesados_col_interesado::text) = (derecho_agrupacion_interesados.interesado_la_agrupacion_interesados::text|| col_interesado.t_id::text)
        	 LEFT JOIN {schema}.fraccion ON miembros.t_id = fraccion.miembros_participacion
        	 GROUP BY derecho_agrupacion_interesados.interesado_la_agrupacion_interesados
         ),
         info_agrupacion_interesados AS (
        	 SELECT col_derecho.t_id,
        	 json_agg(
        		json_build_object('id', la_agrupacion_interesados.t_id,
        						  'attributes', json_build_object('Tipo de agrupación de interesados', la_agrupacion_interesados.ai_tipo,
        														  'Nombre', la_agrupacion_interesados.nombre,
        														  'Tipo', la_agrupacion_interesados.tipo,
        														  'col_interesado', COALESCE(info_interesados_agrupacion_interesados_derecho.col_interesado, '[]')))
        	 ) FILTER (WHERE la_agrupacion_interesados.t_id IS NOT NULL) AS la_agrupacion_interesados
        	 FROM {schema}.la_agrupacion_interesados LEFT JOIN {schema}.col_derecho ON la_agrupacion_interesados.t_id = col_derecho.interesado_la_agrupacion_interesados
        	 LEFT JOIN info_interesados_agrupacion_interesados_derecho ON info_interesados_agrupacion_interesados_derecho.interesado_la_agrupacion_interesados = la_agrupacion_interesados.t_id
        	 WHERE la_agrupacion_interesados.t_id IN (SELECT DISTINCT derecho_agrupacion_interesados.interesado_la_agrupacion_interesados FROM derecho_agrupacion_interesados)
        	 AND col_derecho.t_id IN (SELECT derechos_seleccionados.t_id FROM derechos_seleccionados)
        	 GROUP BY col_derecho.t_id
         ),
         info_fuentes_administrativas_derecho AS (
        	SELECT col_derecho.t_id,
        	 json_agg(
        		json_build_object('id', col_fuenteadministrativa.t_id,
        						  'attributes', json_build_object('Tipo de fuente administrativa', col_fuenteadministrativa.tipo,
        														  'Estado disponibilidad', col_fuenteadministrativa.estado_disponibilidad,
        														  'Oficialidad fuente administrativa', col_fuenteadministrativa.oficialidad,
        														  'Enlace Soporte Fuente', extarchivo.datos))
        	 ) FILTER (WHERE col_fuenteadministrativa.t_id IS NOT NULL) AS col_fuenteadministrativa
        	FROM {schema}.col_derecho
        	LEFT JOIN {schema}.rrrfuente ON col_derecho.t_id = rrrfuente.rrr_col_derecho
        	LEFT JOIN {schema}.col_fuenteadministrativa ON rrrfuente.rfuente = col_fuenteadministrativa.t_id
        	LEFT JOIN {schema}.extarchivo ON extarchivo.col_fuenteadminstrtiva_ext_archivo_id = col_fuenteadministrativa.t_id
        	WHERE col_derecho.t_id IN (SELECT derechos_seleccionados.t_id FROM derechos_seleccionados)
            GROUP BY col_derecho.t_id
         ),
        info_derecho AS (
          SELECT col_derecho.unidad_predio,
        	json_agg(
        		json_build_object('id', col_derecho.t_id,
        						  'attributes', json_build_object('Tipo de derecho', col_derecho.tipo,
        														  'Código registral', col_derecho.codigo_registral_derecho,
        														  'Descripción', col_derecho.descripcion,
        														  'col_fuenteadministrativa', COALESCE(info_fuentes_administrativas_derecho.col_fuenteadministrativa, '[]'),
        														  'col_interesado', COALESCE(info_interesados_derecho.col_interesado, '[]'),
        														  'la_agrupacion_interesados', COALESCE(info_agrupacion_interesados.la_agrupacion_interesados, '[]')))
        	 ) FILTER (WHERE col_derecho.t_id IS NOT NULL) AS col_derecho
          FROM {schema}.col_derecho LEFT JOIN info_fuentes_administrativas_derecho ON col_derecho.t_id = info_fuentes_administrativas_derecho.t_id
          LEFT JOIN info_interesados_derecho ON col_derecho.t_id = info_interesados_derecho.t_id
          LEFT JOIN info_agrupacion_interesados ON col_derecho.t_id = info_agrupacion_interesados.t_id
          WHERE col_derecho.t_id IN (SELECT * FROM derechos_seleccionados)
          GROUP BY col_derecho.unidad_predio
        ),
        ------------------------------------------------------------------------------------------
        -- INFO RESTRICCIONES
        ------------------------------------------------------------------------------------------
         info_contacto_interesados_restriccion AS (
        		SELECT interesado_contacto.interesado,
        		  json_agg(
        				json_build_object('id', interesado_contacto.t_id,
        									   'attributes', json_build_object('Teléfono 1', interesado_contacto.telefono1,
        																	   'Teléfono 2', interesado_contacto.telefono2,
        																	   'Domicilio notificación', interesado_contacto.domicilio_notificacion,
        																	   'Correo_Electrónico', interesado_contacto.correo_electronico,
        																	   'Origen_de_datos', interesado_contacto.origen_datos)))
        		FILTER(WHERE interesado_contacto.t_id IS NOT NULL) AS interesado_contacto
        		FROM {schema}.interesado_contacto LEFT JOIN restriccion_interesados ON restriccion_interesados.interesado_col_interesado = interesado_contacto.interesado
        		WHERE interesado_contacto.interesado IN (SELECT restriccion_interesados.interesado_col_interesado FROM restriccion_interesados)
        		GROUP BY interesado_contacto.interesado
         ),
         info_interesados_restriccion AS (
        	 SELECT restriccion_interesados.t_id,
        	  json_agg(
        		json_build_object('id', col_interesado.t_id,
        						  'attributes', json_build_object('Tipo', col_interesado.tipo,
        														  'Tipo interesado jurídico', col_interesado.tipo_interesado_juridico,
        														  'Documento de identidad', col_interesado.documento_identidad,
        														  'Tipo de documento', col_interesado.tipo_documento,
        														  'Primer apellido', col_interesado.primer_apellido,
        														  'Primer nombre', col_interesado.primer_nombre,
        														  'Segundo apellido', col_interesado.segundo_apellido,
        														  'Segundo nombre', col_interesado.segundo_nombre,
        														  'Género', col_interesado.genero,
        														  'Razón social',col_interesado.razon_social,
        														  'Nombre', col_interesado.nombre,
        														  'interesado_contacto', COALESCE(info_contacto_interesados_restriccion.interesado_contacto, '[]')))
        	 ) FILTER (WHERE col_interesado.t_id IS NOT NULL) AS col_interesado
        	 FROM restriccion_interesados LEFT JOIN {schema}.col_interesado ON col_interesado.t_id = restriccion_interesados.interesado_col_interesado
        	 LEFT JOIN info_contacto_interesados_restriccion ON info_contacto_interesados_restriccion.interesado = col_interesado.t_id
        	 GROUP BY restriccion_interesados.t_id
         ),
         info_contacto_interesado_agrupacion_interesados_restriccion AS (
        		SELECT interesado_contacto.interesado,
        		  json_agg(
        				json_build_object('id', interesado_contacto.t_id,
        									   'attributes', json_build_object('Teléfono 1', interesado_contacto.telefono1,
        																	   'Teléfono 2', interesado_contacto.telefono2,
        																	   'Domicilio notificación', interesado_contacto.domicilio_notificacion,
        																	   'Correo_Electrónico', interesado_contacto.correo_electronico,
        																	   'Origen_de_datos', interesado_contacto.origen_datos)))
        		FILTER(WHERE interesado_contacto.t_id IS NOT NULL) AS interesado_contacto
        		FROM {schema}.interesado_contacto LEFT JOIN restriccion_interesados ON restriccion_interesados.interesado_col_interesado = interesado_contacto.interesado
        		WHERE interesado_contacto.interesado IN (SELECT DISTINCT restriccion_agrupacion_interesados.interesados_col_interesado FROM restriccion_agrupacion_interesados)
        		GROUP BY interesado_contacto.interesado
         ),
         info_interesados_agrupacion_interesados_restriccion AS (
        	 SELECT restriccion_agrupacion_interesados.interesado_la_agrupacion_interesados,
        	  json_agg(
        		json_build_object('id', col_interesado.t_id,
        						  'attributes', json_build_object('Tipo', col_interesado.tipo,
        														  'Tipo interesado jurídico', col_interesado.tipo_interesado_juridico,
        														  'Documento de identidad', col_interesado.documento_identidad,
        														  'Tipo de documento', col_interesado.tipo_documento,
        														  'Primer apellido', col_interesado.primer_apellido,
        														  'Primer nombre', col_interesado.primer_nombre,
        														  'Segundo apellido', col_interesado.segundo_apellido,
        														  'Segundo nombre', col_interesado.segundo_nombre,
        														  'Género', col_interesado.genero,
        														  'Razón social',col_interesado.razon_social,
        														  'Nombre', col_interesado.nombre,
        														  'interesado_contacto', COALESCE(info_contacto_interesado_agrupacion_interesados_restriccion.interesado_contacto, '[]'),
        														  'fraccion', ROUND((fraccion.numerador::numeric/fraccion.denominador::numeric)*100,2) ))
        	 ) FILTER (WHERE col_interesado.t_id IS NOT NULL) AS col_interesado
        	 FROM restriccion_agrupacion_interesados LEFT JOIN {schema}.col_interesado ON col_interesado.t_id = restriccion_agrupacion_interesados.interesados_col_interesado
        	 LEFT JOIN info_contacto_interesado_agrupacion_interesados_restriccion ON info_contacto_interesado_agrupacion_interesados_restriccion.interesado = col_interesado.t_id
        	 LEFT JOIN {schema}.miembros ON (miembros.agrupacion::text || miembros.interesados_col_interesado::text) = (restriccion_agrupacion_interesados.interesado_la_agrupacion_interesados::text|| col_interesado.t_id::text)
        	 LEFT JOIN {schema}.fraccion ON miembros.t_id = fraccion.miembros_participacion
        	 GROUP BY restriccion_agrupacion_interesados.interesado_la_agrupacion_interesados
         ),
         info_agrupacion_interesados_restriccion AS (
        	 SELECT col_restriccion.t_id,
        	 json_agg(
        		json_build_object('id', la_agrupacion_interesados.t_id,
        						  'attributes', json_build_object('Tipo de agrupación de interesados', la_agrupacion_interesados.ai_tipo,
        														  'Nombre', la_agrupacion_interesados.nombre,
        														  'Tipo', la_agrupacion_interesados.tipo,
        														  'col_interesado', COALESCE(info_interesados_agrupacion_interesados_restriccion.col_interesado, '[]')))
        	 ) FILTER (WHERE la_agrupacion_interesados.t_id IS NOT NULL) AS la_agrupacion_interesados
        	 FROM {schema}.la_agrupacion_interesados LEFT JOIN {schema}.col_restriccion ON la_agrupacion_interesados.t_id = col_restriccion.interesado_la_agrupacion_interesados
        	 LEFT JOIN info_interesados_agrupacion_interesados_restriccion ON info_interesados_agrupacion_interesados_restriccion.interesado_la_agrupacion_interesados = la_agrupacion_interesados.t_id
        	 WHERE la_agrupacion_interesados.t_id IN (SELECT DISTINCT restriccion_agrupacion_interesados.interesado_la_agrupacion_interesados FROM restriccion_agrupacion_interesados)
        	 AND col_restriccion.t_id IN (SELECT restricciones_seleccionadas.t_id FROM restricciones_seleccionadas)
        	 GROUP BY col_restriccion.t_id
         ),
         info_fuentes_administrativas_restriccion AS (
        	SELECT col_restriccion.t_id,
        	 json_agg(
        		json_build_object('id', col_fuenteadministrativa.t_id,
        						  'attributes', json_build_object('Tipo de fuente administrativa', col_fuenteadministrativa.tipo,
        														  'Estado disponibilidad', col_fuenteadministrativa.estado_disponibilidad,
        														  'Oficialidad fuente administrativa', col_fuenteadministrativa.oficialidad,
        														  'Enlace Soporte Fuente', extarchivo.datos))
        	 ) FILTER (WHERE col_fuenteadministrativa.t_id IS NOT NULL) AS col_fuenteadministrativa
        	FROM {schema}.col_restriccion
        	LEFT JOIN {schema}.rrrfuente ON col_restriccion.t_id = rrrfuente.rrr_col_restriccion
        	LEFT JOIN {schema}.col_fuenteadministrativa ON rrrfuente.rfuente = col_fuenteadministrativa.t_id
        	LEFT JOIN {schema}.extarchivo ON extarchivo.col_fuenteadminstrtiva_ext_archivo_id = col_fuenteadministrativa.t_id
        	WHERE col_restriccion.t_id IN (SELECT restricciones_seleccionadas.t_id FROM restricciones_seleccionadas)
            GROUP BY col_restriccion.t_id
         ),
        info_restriccion AS (
          SELECT col_restriccion.unidad_predio,
        	json_agg(
        		json_build_object('id', col_restriccion.t_id,
        						  'attributes', json_build_object('Tipo de derecho', col_restriccion.tipo,
        														  'Código registral', col_restriccion.codigo_registral_restriccion,
        														  'Descripción', col_restriccion.descripcion,
        														  'col_fuenteadministrativa', COALESCE(info_fuentes_administrativas_restriccion.col_fuenteadministrativa, '[]'),
        														  'col_interesado', COALESCE(info_interesados_restriccion.col_interesado, '[]'),
        														  'la_agrupacion_interesados', COALESCE(info_agrupacion_interesados_restriccion.la_agrupacion_interesados, '[]')))
        	 ) FILTER (WHERE col_restriccion.t_id IS NOT NULL) AS col_restriccion
          FROM {schema}.col_restriccion LEFT JOIN info_fuentes_administrativas_restriccion ON col_restriccion.t_id = info_fuentes_administrativas_restriccion.t_id
          LEFT JOIN info_interesados_restriccion ON col_restriccion.t_id = info_interesados_restriccion.t_id
          LEFT JOIN info_agrupacion_interesados_restriccion ON col_restriccion.t_id = info_agrupacion_interesados_restriccion.t_id
          WHERE col_restriccion.t_id IN (SELECT * FROM restricciones_seleccionadas)
          GROUP BY col_restriccion.unidad_predio
        ),
        ------------------------------------------------------------------------------------------
        -- INFO RESTRICCIONES
        ------------------------------------------------------------------------------------------
         info_contacto_interesados_responsabilidad AS (
        		SELECT interesado_contacto.interesado,
        		  json_agg(
        				json_build_object('id', interesado_contacto.t_id,
        									   'attributes', json_build_object('Teléfono 1', interesado_contacto.telefono1,
        																	   'Teléfono 2', interesado_contacto.telefono2,
        																	   'Domicilio notificación', interesado_contacto.domicilio_notificacion,
        																	   'Correo_Electrónico', interesado_contacto.correo_electronico,
        																	   'Origen_de_datos', interesado_contacto.origen_datos)))
        		FILTER(WHERE interesado_contacto.t_id IS NOT NULL) AS interesado_contacto
        		FROM {schema}.interesado_contacto LEFT JOIN responsabilidades_interesados ON responsabilidades_interesados.interesado_col_interesado = interesado_contacto.interesado
        		WHERE interesado_contacto.interesado IN (SELECT responsabilidades_interesados.interesado_col_interesado FROM responsabilidades_interesados)
        		GROUP BY interesado_contacto.interesado
         ),
         info_interesados_responsabilidad AS (
        	 SELECT responsabilidades_interesados.t_id,
        	  json_agg(
        		json_build_object('id', col_interesado.t_id,
        						  'attributes', json_build_object('Tipo', col_interesado.tipo,
        														  'Tipo interesado jurídico', col_interesado.tipo_interesado_juridico,
        														  'Documento de identidad', col_interesado.documento_identidad,
        														  'Tipo de documento', col_interesado.tipo_documento,
        														  'Primer apellido', col_interesado.primer_apellido,
        														  'Primer nombre', col_interesado.primer_nombre,
        														  'Segundo apellido', col_interesado.segundo_apellido,
        														  'Segundo nombre', col_interesado.segundo_nombre,
        														  'Género', col_interesado.genero,
        														  'Razón social',col_interesado.razon_social,
        														  'Nombre', col_interesado.nombre,
        														  'interesado_contacto', COALESCE(info_contacto_interesados_responsabilidad.interesado_contacto, '[]')))
        	 ) FILTER (WHERE col_interesado.t_id IS NOT NULL) AS col_interesado
        	 FROM responsabilidades_interesados LEFT JOIN {schema}.col_interesado ON col_interesado.t_id = responsabilidades_interesados.interesado_col_interesado
        	 LEFT JOIN info_contacto_interesados_responsabilidad ON info_contacto_interesados_responsabilidad.interesado = col_interesado.t_id
        	 GROUP BY responsabilidades_interesados.t_id
         ),
         info_contacto_interesado_agrupacion_interesados_responsabilidad AS (
        		SELECT interesado_contacto.interesado,
        		  json_agg(
        				json_build_object('id', interesado_contacto.t_id,
        									   'attributes', json_build_object('Teléfono 1', interesado_contacto.telefono1,
        																	   'Teléfono 2', interesado_contacto.telefono2,
        																	   'Domicilio notificación', interesado_contacto.domicilio_notificacion,
        																	   'Correo_Electrónico', interesado_contacto.correo_electronico,
        																	   'Origen_de_datos', interesado_contacto.origen_datos)))
        		FILTER(WHERE interesado_contacto.t_id IS NOT NULL) AS interesado_contacto
        		FROM {schema}.interesado_contacto LEFT JOIN responsabilidades_interesados ON responsabilidades_interesados.interesado_col_interesado = interesado_contacto.interesado
        		WHERE interesado_contacto.interesado IN (SELECT DISTINCT responsabilidades_agrupacion_interesados.interesados_col_interesado FROM responsabilidades_agrupacion_interesados)
        		GROUP BY interesado_contacto.interesado
         ),
         info_interesados_agrupacion_interesados_responsabilidad AS (
        	 SELECT responsabilidades_agrupacion_interesados.interesado_la_agrupacion_interesados,
        	  json_agg(
        		json_build_object('id', col_interesado.t_id,
        						  'attributes', json_build_object('Tipo', col_interesado.tipo,
        														  'Tipo interesado jurídico', col_interesado.tipo_interesado_juridico,
        														  'Documento de identidad', col_interesado.documento_identidad,
        														  'Tipo de documento', col_interesado.tipo_documento,
        														  'Primer apellido', col_interesado.primer_apellido,
        														  'Primer nombre', col_interesado.primer_nombre,
        														  'Segundo apellido', col_interesado.segundo_apellido,
        														  'Segundo nombre', col_interesado.segundo_nombre,
        														  'Género', col_interesado.genero,
        														  'Razón social',col_interesado.razon_social,
        														  'Nombre', col_interesado.nombre,
        														  'interesado_contacto', COALESCE(info_contacto_interesado_agrupacion_interesados_responsabilidad.interesado_contacto, '[]'),
        														  'fraccion', ROUND((fraccion.numerador::numeric/fraccion.denominador::numeric)*100,2) ))
        	 ) FILTER (WHERE col_interesado.t_id IS NOT NULL) AS col_interesado
        	 FROM responsabilidades_agrupacion_interesados LEFT JOIN {schema}.col_interesado ON col_interesado.t_id = responsabilidades_agrupacion_interesados.interesados_col_interesado
        	 LEFT JOIN info_contacto_interesado_agrupacion_interesados_responsabilidad ON info_contacto_interesado_agrupacion_interesados_responsabilidad.interesado = col_interesado.t_id
        	 LEFT JOIN {schema}.miembros ON (miembros.agrupacion::text || miembros.interesados_col_interesado::text) = (responsabilidades_agrupacion_interesados.interesado_la_agrupacion_interesados::text|| col_interesado.t_id::text)
        	 LEFT JOIN {schema}.fraccion ON miembros.t_id = fraccion.miembros_participacion
        	 GROUP BY responsabilidades_agrupacion_interesados.interesado_la_agrupacion_interesados
         ),
         info_agrupacion_interesados_responsabilidad AS (
        	 SELECT col_responsabilidad.t_id,
        	 json_agg(
        		json_build_object('id', la_agrupacion_interesados.t_id,
        						  'attributes', json_build_object('Tipo de agrupación de interesados', la_agrupacion_interesados.ai_tipo,
        														  'Nombre', la_agrupacion_interesados.nombre,
        														  'Tipo', la_agrupacion_interesados.tipo,
        														  'col_interesado', COALESCE(info_interesados_agrupacion_interesados_responsabilidad.col_interesado, '[]')))
        	 ) FILTER (WHERE la_agrupacion_interesados.t_id IS NOT NULL) AS la_agrupacion_interesados
        	 FROM {schema}.la_agrupacion_interesados LEFT JOIN {schema}.col_responsabilidad ON la_agrupacion_interesados.t_id = col_responsabilidad.interesado_la_agrupacion_interesados
        	 LEFT JOIN info_interesados_agrupacion_interesados_responsabilidad ON info_interesados_agrupacion_interesados_responsabilidad.interesado_la_agrupacion_interesados = la_agrupacion_interesados.t_id
        	 WHERE la_agrupacion_interesados.t_id IN (SELECT DISTINCT responsabilidades_agrupacion_interesados.interesado_la_agrupacion_interesados FROM responsabilidades_agrupacion_interesados)
        	 AND col_responsabilidad.t_id IN (SELECT responsabilidades_seleccionadas.t_id FROM responsabilidades_seleccionadas)
        	 GROUP BY col_responsabilidad.t_id
         ),
         info_fuentes_administrativas_responsabilidad AS (
        	SELECT col_responsabilidad.t_id,
        	 json_agg(
        		json_build_object('id', col_fuenteadministrativa.t_id,
        						  'attributes', json_build_object('Tipo de fuente administrativa', col_fuenteadministrativa.tipo,
        														  'Estado disponibilidad', col_fuenteadministrativa.estado_disponibilidad,
        														  'Oficialidad fuente administrativa', col_fuenteadministrativa.oficialidad,
        														  'Enlace Soporte Fuente', extarchivo.datos))
        	 ) FILTER (WHERE col_fuenteadministrativa.t_id IS NOT NULL) AS col_fuenteadministrativa
        	FROM {schema}.col_responsabilidad
        	LEFT JOIN {schema}.rrrfuente ON col_responsabilidad.t_id = rrrfuente.rrr_col_responsabilidad
        	LEFT JOIN {schema}.col_fuenteadministrativa ON rrrfuente.rfuente = col_fuenteadministrativa.t_id
        	LEFT JOIN {schema}.extarchivo ON extarchivo.col_fuenteadminstrtiva_ext_archivo_id = col_fuenteadministrativa.t_id
        	WHERE col_responsabilidad.t_id IN (SELECT responsabilidades_seleccionadas.t_id FROM responsabilidades_seleccionadas)
            GROUP BY col_responsabilidad.t_id
         ),
        info_responsabilidad AS (
          SELECT col_responsabilidad.unidad_predio,
        	json_agg(
        		json_build_object('id', col_responsabilidad.t_id,
        						  'attributes', json_build_object('Tipo de derecho', col_responsabilidad.tipo,
        														  'Código registral', col_responsabilidad.codigo_registral_responsabilidad,
        														  'Descripción', col_responsabilidad.descripcion,
        														  'col_fuenteadministrativa', COALESCE(info_fuentes_administrativas_responsabilidad.col_fuenteadministrativa, '[]'),
        														  'col_interesado', COALESCE(info_interesados_responsabilidad.col_interesado, '[]'),
        														  'la_agrupacion_interesados', COALESCE(info_agrupacion_interesados_responsabilidad.la_agrupacion_interesados, '[]')))
        	 ) FILTER (WHERE col_responsabilidad.t_id IS NOT NULL) AS col_responsabilidad
          FROM {schema}.col_responsabilidad LEFT JOIN info_fuentes_administrativas_responsabilidad ON col_responsabilidad.t_id = info_fuentes_administrativas_responsabilidad.t_id
          LEFT JOIN info_interesados_responsabilidad ON col_responsabilidad.t_id = info_interesados_responsabilidad.t_id
          LEFT JOIN info_agrupacion_interesados_responsabilidad ON col_responsabilidad.t_id = info_agrupacion_interesados_responsabilidad.t_id
          WHERE col_responsabilidad.t_id IN (SELECT * FROM responsabilidades_seleccionadas)
          GROUP BY col_responsabilidad.unidad_predio
        ),
        ------------------------------------------------------------------------------------------
        -- INFO HIPOTECA
        ------------------------------------------------------------------------------------------
         info_contacto_interesados_hipoteca AS (
        		SELECT interesado_contacto.interesado,
        		  json_agg(
        				json_build_object('id', interesado_contacto.t_id,
        									   'attributes', json_build_object('Teléfono 1', interesado_contacto.telefono1,
        																	   'Teléfono 2', interesado_contacto.telefono2,
        																	   'Domicilio notificación', interesado_contacto.domicilio_notificacion,
        																	   'Correo_Electrónico', interesado_contacto.correo_electronico,
        																	   'Origen_de_datos', interesado_contacto.origen_datos)))
        		FILTER(WHERE interesado_contacto.t_id IS NOT NULL) AS interesado_contacto
        		FROM {schema}.interesado_contacto LEFT JOIN hipotecas_interesados ON hipotecas_interesados.interesado_col_interesado = interesado_contacto.interesado
        		WHERE interesado_contacto.interesado IN (SELECT hipotecas_interesados.interesado_col_interesado FROM hipotecas_interesados)
        		GROUP BY interesado_contacto.interesado
         ),
         info_interesados_hipoteca AS (
        	 SELECT hipotecas_interesados.t_id,
        	  json_agg(
        		json_build_object('id', col_interesado.t_id,
        						  'attributes', json_build_object('Tipo', col_interesado.tipo,
        														  'Tipo interesado jurídico', col_interesado.tipo_interesado_juridico,
        														  'Documento de identidad', col_interesado.documento_identidad,
        														  'Tipo de documento', col_interesado.tipo_documento,
        														  'Primer apellido', col_interesado.primer_apellido,
        														  'Primer nombre', col_interesado.primer_nombre,
        														  'Segundo apellido', col_interesado.segundo_apellido,
        														  'Segundo nombre', col_interesado.segundo_nombre,
        														  'Género', col_interesado.genero,
        														  'Razón social',col_interesado.razon_social,
        														  'Nombre', col_interesado.nombre,
        														  'interesado_contacto', COALESCE(info_contacto_interesados_hipoteca.interesado_contacto, '[]')))
        	 ) FILTER (WHERE col_interesado.t_id IS NOT NULL) AS col_interesado
        	 FROM hipotecas_interesados LEFT JOIN {schema}.col_interesado ON col_interesado.t_id = hipotecas_interesados.interesado_col_interesado
        	 LEFT JOIN info_contacto_interesados_hipoteca ON info_contacto_interesados_hipoteca.interesado = col_interesado.t_id
        	 GROUP BY hipotecas_interesados.t_id
         ),
         info_contacto_interesado_agrupacion_interesados_hipoteca AS (
        		SELECT interesado_contacto.interesado,
        		  json_agg(
        				json_build_object('id', interesado_contacto.t_id,
        									   'attributes', json_build_object('Teléfono 1', interesado_contacto.telefono1,
        																	   'Teléfono 2', interesado_contacto.telefono2,
        																	   'Domicilio notificación', interesado_contacto.domicilio_notificacion,
        																	   'Correo_Electrónico', interesado_contacto.correo_electronico,
        																	   'Origen_de_datos', interesado_contacto.origen_datos)))
        		FILTER(WHERE interesado_contacto.t_id IS NOT NULL) AS interesado_contacto
        		FROM {schema}.interesado_contacto LEFT JOIN hipotecas_interesados ON hipotecas_interesados.interesado_col_interesado = interesado_contacto.interesado
        		WHERE interesado_contacto.interesado IN (SELECT DISTINCT hipotecas_agrupacion_interesados.interesados_col_interesado FROM hipotecas_agrupacion_interesados)
        		GROUP BY interesado_contacto.interesado
         ),
         info_interesados_agrupacion_interesados_hipoteca AS (
        	 SELECT hipotecas_agrupacion_interesados.interesado_la_agrupacion_interesados,
        	  json_agg(
        		json_build_object('id', col_interesado.t_id,
        						  'attributes', json_build_object('Tipo', col_interesado.tipo,
        														  'Tipo interesado jurídico', col_interesado.tipo_interesado_juridico,
        														  'Documento de identidad', col_interesado.documento_identidad,
        														  'Tipo de documento', col_interesado.tipo_documento,
        														  'Primer apellido', col_interesado.primer_apellido,
        														  'Primer nombre', col_interesado.primer_nombre,
        														  'Segundo apellido', col_interesado.segundo_apellido,
        														  'Segundo nombre', col_interesado.segundo_nombre,
        														  'Género', col_interesado.genero,
        														  'Razón social',col_interesado.razon_social,
        														  'Nombre', col_interesado.nombre,
        														  'interesado_contacto', COALESCE(info_contacto_interesado_agrupacion_interesados_hipoteca.interesado_contacto, '[]'),
        														  'fraccion', ROUND((fraccion.numerador::numeric/fraccion.denominador::numeric)*100,2) ))
        	 ) FILTER (WHERE col_interesado.t_id IS NOT NULL) AS col_interesado
        	 FROM hipotecas_agrupacion_interesados LEFT JOIN {schema}.col_interesado ON col_interesado.t_id = hipotecas_agrupacion_interesados.interesados_col_interesado
        	 LEFT JOIN info_contacto_interesado_agrupacion_interesados_hipoteca ON info_contacto_interesado_agrupacion_interesados_hipoteca.interesado = col_interesado.t_id
        	 LEFT JOIN {schema}.miembros ON (miembros.agrupacion::text || miembros.interesados_col_interesado::text) = (hipotecas_agrupacion_interesados.interesado_la_agrupacion_interesados::text|| col_interesado.t_id::text)
        	 LEFT JOIN {schema}.fraccion ON miembros.t_id = fraccion.miembros_participacion
        	 GROUP BY hipotecas_agrupacion_interesados.interesado_la_agrupacion_interesados
         ),
         info_agrupacion_interesados_hipoteca AS (
        	 SELECT col_hipoteca.t_id,
        	 json_agg(
        		json_build_object('id', la_agrupacion_interesados.t_id,
        						  'attributes', json_build_object('Tipo de agrupación de interesados', la_agrupacion_interesados.ai_tipo,
        														  'Nombre', la_agrupacion_interesados.nombre,
        														  'Tipo', la_agrupacion_interesados.tipo,
        														  'col_interesado', COALESCE(info_interesados_agrupacion_interesados_hipoteca.col_interesado, '[]')))
        	 ) FILTER (WHERE la_agrupacion_interesados.t_id IS NOT NULL) AS la_agrupacion_interesados
        	 FROM {schema}.la_agrupacion_interesados LEFT JOIN {schema}.col_hipoteca ON la_agrupacion_interesados.t_id = col_hipoteca.interesado_la_agrupacion_interesados
        	 LEFT JOIN info_interesados_agrupacion_interesados_hipoteca ON info_interesados_agrupacion_interesados_hipoteca.interesado_la_agrupacion_interesados = la_agrupacion_interesados.t_id
        	 WHERE la_agrupacion_interesados.t_id IN (SELECT DISTINCT hipotecas_agrupacion_interesados.interesado_la_agrupacion_interesados FROM hipotecas_agrupacion_interesados)
        	 AND col_hipoteca.t_id IN (SELECT hipotecas_seleccionadas.t_id FROM hipotecas_seleccionadas)
        	 GROUP BY col_hipoteca.t_id
         ),
         info_fuentes_administrativas_hipoteca AS (
        	SELECT col_hipoteca.t_id,
        	 json_agg(
        		json_build_object('id', col_fuenteadministrativa.t_id,
        						  'attributes', json_build_object('Tipo de fuente administrativa', col_fuenteadministrativa.tipo,
        														  'Estado disponibilidad', col_fuenteadministrativa.estado_disponibilidad,
        														  'Oficialidad fuente administrativa', col_fuenteadministrativa.oficialidad,
        														  'Enlace Soporte Fuente', extarchivo.datos))
        	 ) FILTER (WHERE col_fuenteadministrativa.t_id IS NOT NULL) AS col_fuenteadministrativa
        	FROM {schema}.col_hipoteca
        	LEFT JOIN {schema}.rrrfuente ON col_hipoteca.t_id = rrrfuente.rrr_col_hipoteca
        	LEFT JOIN {schema}.col_fuenteadministrativa ON rrrfuente.rfuente = col_fuenteadministrativa.t_id
        	LEFT JOIN {schema}.extarchivo ON extarchivo.col_fuenteadminstrtiva_ext_archivo_id = col_fuenteadministrativa.t_id
        	WHERE col_hipoteca.t_id IN (SELECT hipotecas_seleccionadas.t_id FROM hipotecas_seleccionadas)
            GROUP BY col_hipoteca.t_id
         ),
        info_hipoteca AS (
          SELECT col_hipoteca.unidad_predio,
        	json_agg(
        		json_build_object('id', col_hipoteca.t_id,
        						  'attributes', json_build_object('Tipo de derecho', col_hipoteca.tipo,
        														  'Código registral', col_hipoteca.codigo_registral_hipoteca,
        														  'Descripción', col_hipoteca.descripcion,
        														  'col_fuenteadministrativa', COALESCE(info_fuentes_administrativas_hipoteca.col_fuenteadministrativa, '[]'),
        														  'col_interesado', COALESCE(info_interesados_hipoteca.col_interesado, '[]'),
        														  'la_agrupacion_interesados', COALESCE(info_agrupacion_interesados_hipoteca.la_agrupacion_interesados, '[]')))
        	 ) FILTER (WHERE col_hipoteca.t_id IS NOT NULL) AS col_hipoteca
          FROM {schema}.col_hipoteca LEFT JOIN info_fuentes_administrativas_hipoteca ON col_hipoteca.t_id = info_fuentes_administrativas_hipoteca.t_id
          LEFT JOIN info_interesados_hipoteca ON col_hipoteca.t_id = info_interesados_hipoteca.t_id
          LEFT JOIN info_agrupacion_interesados_hipoteca ON col_hipoteca.t_id = info_agrupacion_interesados_hipoteca.t_id
          WHERE col_hipoteca.t_id IN (SELECT * FROM hipotecas_seleccionadas)
          GROUP BY col_hipoteca.unidad_predio
        ),
         info_predio AS (
        	 SELECT uebaunit.ue_terreno,
        			json_agg(json_build_object('id', predio.t_id,
        							  'attributes', json_build_object('NUPRE', predio.nupre,
        															  'FMI', predio.fmi,
        															  'Número predial', predio.numero_predial,
        															  'Número predial anterior', predio.numero_predial_anterior,
        															  'col_derecho', COALESCE(info_derecho.col_derecho, '[]'),
        															  'col_restriccion', COALESCE(info_restriccion.col_restriccion, '[]'),
        															  'col_responsabilidad', COALESCE(info_responsabilidad.col_responsabilidad, '[]'),
        															  'col_hipoteca', COALESCE(info_hipoteca.col_hipoteca, '[]')
        															 ))) FILTER(WHERE predio.t_id IS NOT NULL) as predio
        	 FROM {schema}.predio LEFT JOIN {schema}.uebaunit ON uebaunit.baunit_predio = predio.t_id
             LEFT JOIN info_derecho ON info_derecho.unidad_predio = predio.t_id
        	 LEFT JOIN info_restriccion ON info_restriccion.unidad_predio = predio.t_id
             LEFT JOIN info_responsabilidad ON info_responsabilidad.unidad_predio = predio.t_id
             LEFT JOIN info_hipoteca ON info_hipoteca.unidad_predio = predio.t_id
        	 WHERE predio.t_id IN (SELECT * FROM predios_seleccionados)
        		AND uebaunit.ue_terreno IS NOT NULL
        		AND uebaunit.ue_construccion IS NULL
        		AND uebaunit.ue_unidadconstruccion IS NULL
             GROUP BY uebaunit.ue_terreno
         ),
         info_terreno AS (
        	 SELECT terreno.t_id,
        	 json_build_object('id', terreno.t_id,
        						'attributes', json_build_object('Área de terreno', terreno.area_calculada,
        														'predio', COALESCE(info_predio.predio, '[]')
        													   )) as terreno 
        	 FROM {schema}.terreno LEFT JOIN info_predio ON terreno.t_id = info_predio.ue_terreno
        	 WHERE terreno.t_id IN (SELECT * FROM terrenos_seleccionados)
         )
        SELECT json_agg(info_terreno.terreno) AS terreno FROM info_terreno
        """

        query = query.format(schema=self.schema,
                             plot_t_id=params['plot_t_id'],
                             parcel_fmi=params['parcel_fmi'],
                             parcel_number=params['parcel_number'],
                             previous_parcel_number=params['previous_parcel_number'])

        if self.conn is None:
            res, msg = self.test_connection()
            if not res:
                return (res, msg)
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        cur.execute(query)
        records = cur.fetchall()
        res = [record._asdict() for record in records]

        #print("LEGAL QUERY:", query)

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

        query = """
        WITH
         terrenos_seleccionados AS (
        	SELECT {plot_t_id} AS ue_terreno WHERE '{plot_t_id}' <> 'NULL'
        		UNION
        	SELECT uebaunit.ue_terreno FROM {schema}.predio LEFT JOIN {schema}.uebaunit ON predio.t_id = uebaunit.baunit_predio  WHERE uebaunit.ue_terreno IS NOT NULL AND CASE WHEN '{parcel_fmi}' = 'NULL' THEN  1 = 2 ELSE predio.fmi = '{parcel_fmi}' END
        		UNION
        	SELECT uebaunit.ue_terreno FROM {schema}.predio LEFT JOIN {schema}.uebaunit ON predio.t_id = uebaunit.baunit_predio  WHERE uebaunit.ue_terreno IS NOT NULL AND CASE WHEN '{parcel_number}' = 'NULL' THEN  1 = 2 ELSE predio.numero_predial = '{parcel_number}' END
        		UNION
        	SELECT uebaunit.ue_terreno FROM {schema}.predio LEFT JOIN {schema}.uebaunit ON predio.t_id = uebaunit.baunit_predio  WHERE uebaunit.ue_terreno IS NOT NULL AND CASE WHEN '{previous_parcel_number}' = 'NULL' THEN  1 = 2 ELSE predio.numero_predial_anterior = '{previous_parcel_number}' END
         ),
         predios_seleccionados AS (
        	SELECT uebaunit.baunit_predio as t_id FROM {schema}.uebaunit WHERE uebaunit.ue_terreno = {plot_t_id} AND '{plot_t_id}' <> 'NULL'
        		UNION
        	SELECT t_id FROM {schema}.predio WHERE CASE WHEN '{parcel_fmi}' = 'NULL' THEN  1 = 2 ELSE predio.fmi = '{parcel_fmi}' END
        		UNION
        	SELECT t_id FROM {schema}.predio WHERE CASE WHEN '{parcel_number}' = 'NULL' THEN  1 = 2 ELSE predio.numero_predial = '{parcel_number}' END
        		UNION
        	SELECT t_id FROM {schema}.predio WHERE CASE WHEN '{previous_parcel_number}' = 'NULL' THEN  1 = 2 ELSE predio.numero_predial_anterior = '{previous_parcel_number}' END
         ),
        """

        if self.property_record_card_model_exists():
            query += """
         predio_ficha_seleccionados AS (
        	 SELECT predio_ficha.t_id FROM {schema}.predio_ficha WHERE predio_ficha.crpredio IN (SELECT * FROM predios_seleccionados)
         ),
         fpredio_investigacion_mercado AS (
        	SELECT investigacionmercado.fichapredio,
        		json_agg(
        				json_build_object('id', investigacionmercado.t_id,
        									   'attributes', json_build_object('Disponible en el mercado', investigacionmercado.disponible_mercado,
        																	   'Tipo de oferta', investigacionmercado.tipo_oferta,
        																	   'Valor', investigacionmercado.valor,
        																	   'Nombre oferente', investigacionmercado.nombre_oferente,
        																	   'Teléfono contacto oferente', investigacionmercado.telefono_contacto_oferente,
        																	   'Observaciones', investigacionmercado.observaciones))
        		) FILTER(WHERE investigacionmercado.t_id IS NOT NULL) AS investigacionmercado
        	FROM {schema}.investigacionmercado WHERE investigacionmercado.fichapredio IN (SELECT * FROM predio_ficha_seleccionados)
        	GROUP BY investigacionmercado.fichapredio
         ),
         fpredio_nucleo_familiar AS (
        	SELECT nucleofamiliar.fichapredio,
        		json_agg(
        				json_build_object('id', nucleofamiliar.t_id,
        									   'attributes', json_build_object('Documento de identidad', nucleofamiliar.documento_identidad,
        																	   'Tipo de documento', nucleofamiliar.tipo_documento,
        																	   'Organo emisor', nucleofamiliar.organo_emisor,
        																	   'Fecha de emisión', nucleofamiliar.fecha_emision,
        																	   'Primer nombre', nucleofamiliar.primer_nombre,
        																	   'Segundo nombre', nucleofamiliar.segundo_nombre,
        																	   'Primer apellido', nucleofamiliar.primer_apellido,
        																	   'Segundo apellido', nucleofamiliar.segundo_apellido,
        																	   'Fecha de nacimiento', nucleofamiliar.fecha_nacimiento,
        																	   'Lugar de nacimiento', nucleofamiliar.lugar_nacimiento,
        																	   'Nacionalidad', nucleofamiliar.nacionalidad,
        																	   'Discapacidad', nucleofamiliar.discapacidad,
        																	   'Género', nucleofamiliar.genero,
        																	   'Habita predio', nucleofamiliar.habita_predio,
        																	   'Parentesco', nucleofamiliar.parentesco,
        																	   'Etnia', nucleofamiliar.etnia,
        																	   'Dirección', nucleofamiliar.direccion,
        																	   'Celular', nucleofamiliar.celular))
        		) FILTER(WHERE nucleofamiliar.t_id IS NOT NULL) AS nucleofamiliar
        	FROM {schema}.nucleofamiliar WHERE nucleofamiliar.fichapredio IN (SELECT * FROM predio_ficha_seleccionados)
        	GROUP BY nucleofamiliar.fichapredio
         ),
            """

        query += """
         info_predio AS (
        	 SELECT uebaunit.ue_terreno,
        			json_agg(json_build_object('id', predio.t_id,
        							  'attributes', json_build_object('Departamento', predio.departamento,
        															  'Municipio', predio.municipio,
        															  'Zona', predio.zona,
        															  'NUPRE', predio.nupre,
        															  'FMI', predio.fmi,
        															  'Número predial', predio.numero_predial,
        															  'Número predial anterior', predio.numero_predial_anterior,
        """

        if self.property_record_card_model_exists():
            query += """
        															  'Sector', predio_ficha.sector,
        															  'Localidad/Comuna', predio_ficha.localidad_comuna,
        															  'Barrio', predio_ficha.barrio,
        															  'Manzana/Vereda', predio_ficha.manzana_vereda,
        															  'Terreno', predio_ficha.terreno,
        															  'Condición propiedad', predio_ficha.condicion_propiedad,
        															  'Edificio', predio_ficha.edificio,
        															  'Piso', predio_ficha.piso,
        															  'Unidad', predio_ficha.unidad,
        															  'Estado NUPRE', predio_ficha.estado_nupre,
        															  'Destinación económica', predio_ficha.destinacion_economica,
        															  'Tipo de predio', predio_ficha.predio_tipo,
        															  'Tipo predio público', predio_ficha.tipo_predio_publico,
        															  'Formalidad', predio_ficha.formalidad,
        															  'Estrato', predio_ficha.estrato,
        															  'Clase suelo POT', predio_ficha.clase_suelo_pot,
        															  'Categoría suelo POT', predio_ficha.categoria_suelo_pot,
        															  'Derecho FMI', predio_ficha.derecho_fmi,
        															  'Inscrito RUPTA', predio_ficha.inscrito_rupta,
        															  'Fecha medida RUPTA', predio_ficha.fecha_medida_rupta,
        															  'Anotación FMI RUPTA', predio_ficha.anotacion_fmi_rupta,
        															  'Inscrito protección colectiva', predio_ficha.inscrito_proteccion_colectiva,
        															  'Fecha protección colectiva', predio_ficha.fecha_proteccion_colectiva,
        															  'Anotación FMI protección colectiva', predio_ficha.anotacion_fmi_proteccion_colectiva,
        															  'Inscrito proteccion Ley 1448', predio_ficha.inscrito_proteccion_ley1448,
        															  'Fecha protección ley 1448', predio_ficha.fecha_proteccion_ley1448,
        															  'Anotación FDM Ley 1448', predio_ficha.anotacion_fmi_ley1448,
        															  'Inscripción URT', predio_ficha.inscripcion_urt,
        															  'Fecha de inscripción URT', predio_ficha.fecha_inscripcion_urt,
        															  'Anotación FMI URT', predio_ficha.anotacion_fmi_urt,
        															  'Vigencia fiscal', predio_ficha.vigencia_fiscal,
        															  'Observaciones', predio_ficha.observaciones,
        															  'Fecha visita predial', predio_ficha.fecha_visita_predial,
        															  'Nombre quien atendio', predio_ficha.nombre_quien_atendio,
        															  'Número de documento de quien atendio', predio_ficha.numero_documento_quien_atendio,
        															  'Categoría quien atendio', predio_ficha.categoria_quien_atendio,
        															  'Tipo de documento de quien atendio', predio_ficha.tipo_documento_quien_atendio,
        															  'Nombre encuestador', predio_ficha.nombre_encuestador,
        															  'Número de documento encuestador', predio_ficha.numero_documento_encuestador,
        															  'Tipo de documento encuestador', predio_ficha.tipo_documento_encuestador,
        															  'nucleofamiliar', COALESCE(fpredio_nucleo_familiar.nucleofamiliar, '[]'),
        															  'investigacionmercado', COALESCE(fpredio_investigacion_mercado.investigacionmercado, '[]'),
            """

        query += """
        															  'Tipo', predio.tipo
        															 ))) FILTER(WHERE predio.t_id IS NOT NULL) as predio
        	 FROM {schema}.predio LEFT JOIN {schema}.uebaunit ON uebaunit.baunit_predio = predio.t_id
        """

        if self.property_record_card_model_exists():
            query += """
        	 LEFT JOIN {schema}.predio_ficha ON predio_ficha.crpredio = predio.t_id
        	 LEFT JOIN fpredio_nucleo_familiar ON fpredio_nucleo_familiar.fichapredio = predio_ficha.t_id
        	 LEFT JOIN fpredio_investigacion_mercado ON fpredio_investigacion_mercado.fichapredio = predio_ficha.t_id
            """

        query += """
        	 WHERE predio.t_id IN (SELECT * FROM predios_seleccionados) AND uebaunit.ue_terreno IS NOT NULL
             GROUP BY uebaunit.ue_terreno
         ),
         info_terreno AS (
        	SELECT terreno.t_id,
              json_build_object('id', terreno.t_id,
        						'attributes', json_build_object('Área de terreno', terreno.area_calculada,
        														'predio', COALESCE(info_predio.predio, '[]')
        													   )) as terreno
            FROM {schema}.terreno LEFT JOIN info_predio ON info_predio.ue_terreno = terreno.t_id
        	WHERE terreno.t_id IN (SELECT * FROM terrenos_seleccionados)
         )
        SELECT json_agg(info_terreno.terreno) AS terreno FROM info_terreno
        """

        query = query.format(schema=self.schema,
                             plot_t_id=params['plot_t_id'],
                             parcel_fmi=params['parcel_fmi'],
                             parcel_number=params['parcel_number'],
                             previous_parcel_number=params['previous_parcel_number'])

        if self.conn is None:
            res, msg = self.test_connection()
            if not res:
                return (res, msg)
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        cur.execute(query)
        records = cur.fetchall()
        res = [record._asdict() for record in records]

        #print("PROPERTY RECORD CARD QUERY:", query)

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

        query = """
        WITH
         terrenos_seleccionados AS (
        	SELECT {plot_t_id} AS ue_terreno WHERE '{plot_t_id}' <> 'NULL'
        		UNION
        	SELECT uebaunit.ue_terreno FROM {schema}.predio LEFT JOIN {schema}.uebaunit ON predio.t_id = uebaunit.baunit_predio  WHERE uebaunit.ue_terreno IS NOT NULL AND CASE WHEN '{parcel_fmi}' = 'NULL' THEN  1 = 2 ELSE predio.fmi = '{parcel_fmi}' END
        		UNION
        	SELECT uebaunit.ue_terreno FROM {schema}.predio LEFT JOIN {schema}.uebaunit ON predio.t_id = uebaunit.baunit_predio  WHERE uebaunit.ue_terreno IS NOT NULL AND CASE WHEN '{parcel_number}' = 'NULL' THEN  1 = 2 ELSE predio.numero_predial = '{parcel_number}' END
        		UNION
        	SELECT uebaunit.ue_terreno FROM {schema}.predio LEFT JOIN {schema}.uebaunit ON predio.t_id = uebaunit.baunit_predio  WHERE uebaunit.ue_terreno IS NOT NULL AND CASE WHEN '{previous_parcel_number}' = 'NULL' THEN  1 = 2 ELSE predio.numero_predial_anterior = '{previous_parcel_number}' END
         ),
         predios_seleccionados AS (
        	SELECT uebaunit.baunit_predio as t_id FROM {schema}.uebaunit WHERE uebaunit.ue_terreno = {plot_t_id} AND '{plot_t_id}' <> 'NULL'
        		UNION
        	SELECT t_id FROM {schema}.predio WHERE CASE WHEN '{parcel_fmi}' = 'NULL' THEN  1 = 2 ELSE predio.fmi = '{parcel_fmi}' END
        		UNION
        	SELECT t_id FROM {schema}.predio WHERE CASE WHEN '{parcel_number}' = 'NULL' THEN  1 = 2 ELSE predio.numero_predial = '{parcel_number}' END
        		UNION
        	SELECT t_id FROM {schema}.predio WHERE CASE WHEN '{previous_parcel_number}' = 'NULL' THEN  1 = 2 ELSE predio.numero_predial_anterior = '{previous_parcel_number}' END
         ),
         construcciones_seleccionadas AS (
        	 SELECT ue_construccion FROM {schema}.uebaunit WHERE uebaunit.baunit_predio IN (SELECT predios_seleccionados.t_id FROM predios_seleccionados WHERE predios_seleccionados.t_id IS NOT NULL) AND ue_construccion IS NOT NULL
         ),
         unidadesconstruccion_seleccionadas AS (
        	 SELECT unidadconstruccion.t_id FROM {schema}.unidadconstruccion WHERE unidadconstruccion.construccion IN (SELECT ue_construccion FROM construcciones_seleccionadas)
         ),
         uc_fuente_espacial AS (
        	SELECT uefuente.ue_unidadconstruccion,
        		json_agg(
        				json_build_object('id', col_fuenteespacial.t_id,
        									   'attributes', json_build_object('Tipo de fuente espacial', col_fuenteespacial.Tipo,
        																	   'Estado disponibilidad', col_fuenteespacial.estado_disponibilidad,
        																	   'Tipo principal', col_fuenteespacial.tipo_principal,
        																	   'Oficialidad', col_fuenteespacial.oficialidad,
        																	   'Fecha de entrega', col_fuenteespacial.fecha_entrega,
        																	   'Fecha de grabación', col_fuenteespacial.fecha_grabacion,
        																	   'Enlace fuente espacial', extarchivo.datos))
        		) FILTER(WHERE ueFuente.pfuente IS NOT NULL) AS col_fuenteespacial
        	FROM {schema}.uefuente LEFT JOIN {schema}.col_fuenteespacial ON uefuente.pfuente = col_fuenteespacial.t_id
            LEFT JOIN {schema}.extarchivo ON extarchivo.col_fuenteespacial_ext_archivo_id = col_fuenteespacial.t_id
        	WHERE uefuente.ue_unidadconstruccion IN (SELECT * FROM unidadesconstruccion_seleccionadas)
        	GROUP BY ueFuente.ue_unidadconstruccion 
         ),
        info_uc AS (
        	 SELECT unidadconstruccion.construccion,
        			json_agg(json_build_object('id', unidadconstruccion.t_id,
        							  'attributes', json_build_object('Número de pisos', unidadconstruccion.numero_pisos,
        """

        if self.valuation_model_exists():
            query += """
        															  'Uso', unidad_construccion.uso,
        															  'Puntuación', unidad_construccion.puntuacion,
        															  'Tipología', unidad_construccion.tipologia,
        															  'Puntuación', unidad_construccion.puntuacion,
        															  'Destino económico', unidad_construccion.destino_econo,
        															  'Tipo de construcción', unidad_construccion.construccion_tipo,
            """
        else:
            query += """
        															  'Uso', NULL,
        															  'Puntuación', NULL,
        															  'Tipología', NULL,
        															  'Puntuación', NULL,
        															  'Destino económico', NULL,
        															  'Tipo de construcción', NULL,
            """

        query += """
        															  'Área privada construida', unidadconstruccion.area_privada_construida,
        															  'Área construida', unidadconstruccion.area_construida,
        															  'col_fuenteespacial', COALESCE(uc_fuente_espacial.col_fuenteespacial, '[]')
        															 ))) as unidadconstruccion
        	 FROM {schema}.unidadconstruccion LEFT JOIN uc_fuente_espacial ON unidadconstruccion.t_id = uc_fuente_espacial.ue_unidadconstruccion
        """

        if self.valuation_model_exists():
            query += """
        	 LEFT JOIN {schema}.avaluounidadconstruccion ON unidadconstruccion.t_id = avaluounidadconstruccion.ucons
        	 LEFT JOIN {schema}.unidad_construccion ON avaluounidadconstruccion.aucons = unidad_construccion.t_id
            """

        query += """
        	 WHERE unidadconstruccion.t_id IN (SELECT * FROM unidadesconstruccion_seleccionadas)
             GROUP BY unidadconstruccion.construccion
         ),
         c_fuente_espacial AS (
        	SELECT uefuente.ue_construccion,
        		json_agg(
        				json_build_object('id', col_fuenteespacial.t_id,
        									   'attributes', json_build_object('Tipo de fuente espacial', col_fuenteespacial.Tipo,
        																	   'Estado disponibilidad', col_fuenteespacial.estado_disponibilidad,
        																	   'Tipo principal', col_fuenteespacial.tipo_principal,
        																	   'Oficialidad', col_fuenteespacial.oficialidad,
        																	   'Fecha de entrega', col_fuenteespacial.fecha_entrega,
        																	   'Fecha de grabación', col_fuenteespacial.fecha_grabacion,
        																	   'Enlace fuente espacial', extarchivo.datos))														   
        		) FILTER(WHERE ueFuente.pfuente IS NOT NULL) AS col_fuenteespacial
        	FROM {schema}.uefuente LEFT JOIN {schema}.col_fuenteespacial ON uefuente.pfuente = col_fuenteespacial.t_id
        	LEFT JOIN {schema}.extarchivo ON extarchivo.col_fuenteespacial_ext_archivo_id = col_fuenteespacial.t_id
        	WHERE uefuente.ue_construccion IN (SELECT * FROM construcciones_seleccionadas)
        	GROUP BY uefuente.ue_construccion 
         ),
         info_construccion as (
          SELECT uebaunit.baunit_predio,
        		json_agg(json_build_object('id', construccion.t_id,
        						  'attributes', json_build_object('Área construcción', construccion.area_construccion,
        """

        if self.valuation_model_exists():
            query += """
        														  'Ńúmero de pisos', avaluos_v2_2_1avaluos_construccion.numero_pisos,
            """
        else:
            query += """
            														  'Ńúmero de pisos', NULL,
                """

        query += """
        														  'col_fuenteespacial', COALESCE(c_fuente_espacial.col_fuenteespacial, '[]'),
        														  'unidadconstruccion', COALESCE(info_uc.unidadconstruccion, '[]')
        														 ))) FILTER(WHERE construccion.t_id IS NOT NULL) as construccion
          FROM {schema}.construccion LEFT JOIN c_fuente_espacial ON construccion.t_id = c_fuente_espacial.ue_construccion
          LEFT JOIN info_uc ON construccion.t_id = info_uc.construccion
          LEFT JOIN {schema}.uebaunit ON uebaunit.ue_construccion = info_uc.construccion
        """

        if self.valuation_model_exists():
            query += """
            LEFT JOIN {schema}.avaluoconstruccion ON avaluoconstruccion.cons = construccion.t_id
            LEFT JOIN {schema}.avaluos_v2_2_1avaluos_construccion  ON avaluos_v2_2_1avaluos_construccion.t_id = avaluoconstruccion.cons
            """

        query += """
          WHERE construccion.t_id IN (SELECT * FROM construcciones_seleccionadas)
          GROUP BY uebaunit.baunit_predio
         ),
         info_predio AS (
        	 SELECT uebaunit.ue_terreno,
        			json_agg(json_build_object('id', predio.t_id,
        							  'attributes', json_build_object('NUPRE', predio.nupre,
        															  'FMI', predio.fmi,
        															  'Número predial', predio.numero_predial,
        															  'Número predial anterior', predio.numero_predial_anterior,
        															  'construccion', COALESCE(info_construccion.construccion, '[]')
        															 ))) FILTER(WHERE predio.t_id IS NOT NULL) as predio
        	 FROM {schema}.predio LEFT JOIN {schema}.uebaunit ON uebaunit.baunit_predio = predio.t_id
             LEFT JOIN info_construccion ON info_construccion.baunit_predio = predio.t_id
        	 WHERE predio.t_id IN (SELECT * FROM predios_seleccionados)
        		AND uebaunit.ue_terreno IS NOT NULL
        		AND uebaunit.ue_construccion IS NULL
        		AND uebaunit.ue_unidadconstruccion IS NULL
             GROUP BY uebaunit.ue_terreno
         ),
         t_fuente_espacial AS (
        	SELECT uefuente.ue_terreno,
        		json_agg(
        				json_build_object('id', col_fuenteespacial.t_id,
        									   'attributes', json_build_object('Tipo de fuente espacial', col_fuenteespacial.Tipo,
        																	   'Estado disponibilidad', col_fuenteespacial.estado_disponibilidad,
        																	   'Tipo principal', col_fuenteespacial.tipo_principal,
        																	   'Oficialidad', col_fuenteespacial.oficialidad,
        																	   'Fecha de entrega', col_fuenteespacial.fecha_entrega,
        																	   'Fecha de grabación', col_fuenteespacial.fecha_grabacion,
        																	   'Enlace fuente espacial', extarchivo.datos))														   
        		) FILTER(WHERE ueFuente.pfuente IS NOT NULL) AS col_fuenteespacial
        	FROM {schema}.uefuente LEFT JOIN {schema}.col_fuenteespacial ON uefuente.pfuente = col_fuenteespacial.t_id
            LEFT JOIN {schema}.extarchivo ON extarchivo.col_fuenteespacial_ext_archivo_id = col_fuenteespacial.t_id
        	WHERE uefuente.ue_terreno IN (SELECT * FROM terrenos_seleccionados)
        	GROUP BY uefuente.ue_terreno 
         ),
         info_linderos_externos AS (
        	SELECT masccl.uep_terreno,
        		json_agg(
        				json_build_object('id', lindero.t_id,
        									   'attributes', json_build_object('Longitud', lindero.longitud))
        		) FILTER(WHERE lindero.t_id IS NOT NULL) AS lindero
        	FROM {schema}.lindero LEFT JOIN {schema}.masccl ON lindero.t_id = masccl.cclp_lindero
            WHERE masccl.uep_terreno IN (SELECT * FROM terrenos_seleccionados)
        	GROUP BY masccl.uep_terreno
         ),
         info_linderos_internos AS (
        	SELECT menos.eu_terreno,
        		json_agg(
        				json_build_object('id', lindero.t_id,
        									   'attributes', json_build_object('Longitud', lindero.longitud))
        		) FILTER(WHERE lindero.t_id IS NOT NULL) AS lindero
        	FROM {schema}.lindero LEFT JOIN {schema}.menos ON lindero.t_id = menos.ccl_lindero
        	WHERE menos.eu_terreno IN (SELECT * FROM terrenos_seleccionados)
        	GROUP BY menos.eu_terreno
         ),
         info_punto_lindero_externos AS (
        	 SELECT masccl.uep_terreno,
        	 		json_agg(
        				json_build_object('id', puntoccl.t_id,
        									   'attributes', json_build_object('Nombre', puntolindero.nombre_punto,
        																	   'x', st_x(puntolindero.localizacion_original),
        																	   'y', st_y(puntolindero.localizacion_original),
        																	   'z', st_z(puntolindero.localizacion_original))
        			)) FILTER(WHERE puntoccl.t_id IS NOT NULL) AS puntolindero
        	 FROM {schema}.puntolindero LEFT JOIN {schema}.puntoccl ON puntolindero.t_id = puntoccl.punto_puntolindero
        	 LEFT JOIN {schema}.lindero ON puntoccl.ccl_lindero = lindero.t_id
        	 LEFT JOIN {schema}.masccl ON lindero.t_id = masccl.cclp_lindero
             WHERE masccl.uep_terreno IN (SELECT * FROM terrenos_seleccionados)
        	 GROUP BY masccl.uep_terreno
         ),
         info_punto_lindero_internos AS (
        	 SELECT menos.eu_terreno,
        	 		json_agg(
        				json_build_object('id', puntoccl.t_id,
        									   'attributes', json_build_object('Nombre', puntolindero.nombre_punto,
        																	   'x', st_x(puntolindero.localizacion_original),
        																	   'y', st_y(puntolindero.localizacion_original),
        																	   'z', st_z(puntolindero.localizacion_original))
        			)) FILTER(WHERE puntoccl.t_id IS NOT NULL) AS puntolindero
        	 FROM {schema}.puntolindero LEFT JOIN {schema}.puntoccl ON puntolindero.t_id = puntoccl.punto_puntolindero
        	 LEFT JOIN {schema}.lindero ON puntoccl.ccl_lindero = lindero.t_id
        	 LEFT JOIN {schema}.menos ON lindero.t_id = menos.ccl_lindero
             WHERE menos.eu_terreno IN (SELECT * FROM terrenos_seleccionados)
        	 GROUP BY menos.eu_terreno
         ),
        col_bosqueareasemi_terreno_bosque_area_seminaturale AS (
        	SELECT terreno_bosque_area_seminaturale,
        		json_agg(
        				json_build_object('id', t_id,
        									   'attributes', json_build_object('avalue', avalue))
        		) FILTER(WHERE t_id IS NOT NULL) AS col_bosqueareasemi_terreno_bosque_area_seminaturale
        	FROM {schema}.col_bosqueareasemi_terreno_bosque_area_seminaturale 
            WHERE terreno_bosque_area_seminaturale IN (SELECT * FROM terrenos_seleccionados)
        	GROUP BY terreno_bosque_area_seminaturale
         ),
        col_territorioagricola_terreno_territorio_agricola AS (
        	SELECT terreno_territorio_agricola,
        		json_agg(
        				json_build_object('id', t_id,
        									   'attributes', json_build_object('avalue', avalue))
        		) FILTER(WHERE t_id IS NOT NULL) AS col_territorioagricola_terreno_territorio_agricola
        	FROM {schema}.col_territorioagricola_terreno_territorio_agricola 
            WHERE terreno_territorio_agricola IN (SELECT * FROM terrenos_seleccionados)
        	GROUP BY terreno_territorio_agricola
         ),
        col_cuerpoagua_terreno_evidencia_cuerpo_agua AS (
        	SELECT terreno_evidencia_cuerpo_agua,
        		json_agg(
        				json_build_object('id', t_id,
        									   'attributes', json_build_object('avalue', avalue))
        		) FILTER(WHERE t_id IS NOT NULL) AS col_cuerpoagua_terreno_evidencia_cuerpo_agua
        	FROM {schema}.col_cuerpoagua_terreno_evidencia_cuerpo_agua 
            WHERE terreno_evidencia_cuerpo_agua IN (SELECT * FROM terrenos_seleccionados)
        	GROUP BY terreno_evidencia_cuerpo_agua
         ),
        col_explotaciontipo_terreno_explotacion AS (
        	SELECT terreno_explotacion,
        		json_agg(
        				json_build_object('id', t_id,
        									   'attributes', json_build_object('avalue', avalue))
        		) FILTER(WHERE t_id IS NOT NULL) AS col_explotaciontipo_terreno_explotacion
        	FROM {schema}.col_explotaciontipo_terreno_explotacion 
            WHERE terreno_explotacion IN (SELECT * FROM terrenos_seleccionados)
        	GROUP BY terreno_explotacion
         ),
        col_afectacion_terreno_afectacion AS (
        	SELECT terreno_afectacion,
        		json_agg(
        				json_build_object('id', t_id,
        									   'attributes', json_build_object('avalue', avalue))
        		) FILTER(WHERE t_id IS NOT NULL) AS col_afectacion_terreno_afectacion
        	FROM {schema}.col_afectacion_terreno_afectacion 
            WHERE terreno_afectacion IN (SELECT * FROM terrenos_seleccionados)
        	GROUP BY terreno_afectacion
         ),
        col_servidumbretipo_terreno_servidumbre AS (
        	SELECT terreno_servidumbre,
        		json_agg(
        				json_build_object('id', t_id,
        									   'attributes', json_build_object('avalue', avalue))
        		) FILTER(WHERE t_id IS NOT NULL) AS col_servidumbretipo_terreno_servidumbre
        	FROM {schema}.col_servidumbretipo_terreno_servidumbre 
            WHERE terreno_servidumbre IN (SELECT * FROM terrenos_seleccionados)
        	GROUP BY terreno_servidumbre
         ),
        info_puntolevantamiento AS (
        	SELECT uebaunit_predio.ue_terreno,
        			json_agg(
        					json_build_object('id', puntoslevantamiento_seleccionados.t_id_puntolevantamiento,
        										   'attributes', json_build_object('x', st_x(puntoslevantamiento_seleccionados.localizacion_original),
        																		   'y', st_y(puntoslevantamiento_seleccionados.localizacion_original),
        																		   'z', st_z(puntoslevantamiento_seleccionados.localizacion_original)))
        			) FILTER(WHERE puntoslevantamiento_seleccionados.t_id_puntolevantamiento IS NOT NULL) AS puntolevantamiento
        	FROM
        	(
        		SELECT puntolevantamiento.t_id AS t_id_puntolevantamiento, puntolevantamiento.localizacion_original, construccion.t_id AS t_id_construccion  FROM {schema}.construccion, {schema}.puntolevantamiento
        		WHERE ST_Intersects(construccion.poligono_creado, puntolevantamiento.localizacion_original) = True AND construccion.t_id IN (1179, 1180, 1181)
        	) AS puntoslevantamiento_seleccionados
        	LEFT JOIN {schema}.uebaunit AS uebaunit_construccion  ON uebaunit_construccion.ue_construccion = puntoslevantamiento_seleccionados.t_id_construccion
        	LEFT JOIN {schema}.uebaunit AS uebaunit_predio ON uebaunit_predio.baunit_predio = uebaunit_construccion.baunit_predio
        	WHERE uebaunit_predio.ue_terreno IS NOT NULL AND 
        		  uebaunit_predio.ue_construccion IS NULL AND 
        		  uebaunit_predio.ue_unidadconstruccion IS NULL
        	GROUP BY uebaunit_predio.ue_terreno
        ),
         info_terreno AS (
        	SELECT terreno.t_id,
              json_build_object('id', terreno.t_id,
        						'attributes', json_build_object('Área registral', terreno.area_registral, 
        														'Área calculada', terreno.area_calculada,
        														'col_territorioagricola_terreno_territorio_agricola', COALESCE(col_territorioagricola_terreno_territorio_agricola.col_territorioagricola_terreno_territorio_agricola, '[]'),
        														'col_bosqueareasemi_terreno_bosque_area_seminaturale', COALESCE(col_bosqueareasemi_terreno_bosque_area_seminaturale.col_bosqueareasemi_terreno_bosque_area_seminaturale, '[]'),
        														'col_cuerpoagua_terreno_evidencia_cuerpo_agua', COALESCE(col_cuerpoagua_terreno_evidencia_cuerpo_agua.col_cuerpoagua_terreno_evidencia_cuerpo_agua, '[]'),
        														'col_explotaciontipo_terreno_explotacion', COALESCE(col_explotaciontipo_terreno_explotacion.col_explotaciontipo_terreno_explotacion, '[]'),
        														'col_afectacion_terreno_afectacion', COALESCE(col_afectacion_terreno_afectacion.col_afectacion_terreno_afectacion, '[]'),
        														'col_servidumbretipo_terreno_servidumbre', COALESCE(col_servidumbretipo_terreno_servidumbre.col_servidumbretipo_terreno_servidumbre, '[]'),
        														'Linderos externos', COALESCE(info_linderos_externos.lindero, '[]'),
        														'Puntos linderos externos', COALESCE(info_punto_lindero_externos.puntolindero, '[]'),
        														'Linderos internos', COALESCE(info_linderos_internos.lindero, '[]'),
        														'Puntos linderos internos', COALESCE(info_punto_lindero_internos.puntolindero, '[]'),
        														'puntolevantamiento', COALESCE(info_puntolevantamiento.puntolevantamiento, '[]'),
        														'col_fuenteespacial', COALESCE(t_fuente_espacial.col_fuenteespacial, '[]'),
        														'predio', COALESCE(info_predio.predio, '[]')
        													   )) as terreno
            FROM {schema}.terreno LEFT JOIN info_predio ON info_predio.ue_terreno = terreno.t_id
        	LEFT JOIN t_fuente_espacial ON terreno.t_id = t_fuente_espacial.ue_terreno
        	LEFT JOIN info_linderos_externos ON terreno.t_id = info_linderos_externos.uep_terreno
        	LEFT JOIN info_linderos_internos ON terreno.t_id = info_linderos_internos.eu_terreno
            LEFT JOIN info_punto_lindero_externos ON terreno.t_id = info_punto_lindero_externos.uep_terreno
        	LEFT JOIN info_punto_lindero_internos ON terreno.t_id = info_punto_lindero_internos.eu_terreno
        	LEFT JOIN col_territorioagricola_terreno_territorio_agricola ON terreno.t_id = col_territorioagricola_terreno_territorio_agricola.terreno_territorio_agricola
        	LEFT JOIN col_bosqueareasemi_terreno_bosque_area_seminaturale ON terreno.t_id = col_bosqueareasemi_terreno_bosque_area_seminaturale.terreno_bosque_area_seminaturale
        	LEFT JOIN col_cuerpoagua_terreno_evidencia_cuerpo_agua ON terreno.t_id = col_cuerpoagua_terreno_evidencia_cuerpo_agua.terreno_evidencia_cuerpo_agua
        	LEFT JOIN col_explotaciontipo_terreno_explotacion ON terreno.t_id = col_explotaciontipo_terreno_explotacion.terreno_explotacion
        	LEFT JOIN col_afectacion_terreno_afectacion ON terreno.t_id = col_afectacion_terreno_afectacion.terreno_afectacion
        	LEFT JOIN col_servidumbretipo_terreno_servidumbre ON terreno.t_id = col_servidumbretipo_terreno_servidumbre.terreno_servidumbre
            LEFT JOIN info_puntolevantamiento ON terreno.t_id = info_puntolevantamiento.ue_terreno
        	WHERE terreno.t_id IN (SELECT * FROM terrenos_seleccionados)
         )				
        SELECT json_agg(info_terreno.terreno) AS terreno FROM info_terreno
        """

        query = query.format(schema=self.schema,
                             plot_t_id=params['plot_t_id'],
                             parcel_fmi=params['parcel_fmi'],
                             parcel_number=params['parcel_number'],
                             previous_parcel_number=params['previous_parcel_number'])

        if self.conn is None:
            res, msg = self.test_connection()
            if not res:
                return (res, msg)
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        cur.execute(query)
        records = cur.fetchall()
        res = [record._asdict() for record in records]

        #print("PHYSICAL QUERY:", query)

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

        query = """
        WITH
         terrenos_seleccionados AS (
        	SELECT {plot_t_id} AS ue_terreno WHERE '{plot_t_id}' <> 'NULL'
        		UNION
        	SELECT uebaunit.ue_terreno FROM {schema}.predio LEFT JOIN {schema}.uebaunit ON predio.t_id = uebaunit.baunit_predio  WHERE uebaunit.ue_terreno IS NOT NULL AND CASE WHEN '{parcel_fmi}' = 'NULL' THEN  1 = 2 ELSE predio.fmi = '{parcel_fmi}' END
        		UNION
        	SELECT uebaunit.ue_terreno FROM {schema}.predio LEFT JOIN {schema}.uebaunit ON predio.t_id = uebaunit.baunit_predio  WHERE uebaunit.ue_terreno IS NOT NULL AND CASE WHEN '{parcel_number}' = 'NULL' THEN  1 = 2 ELSE predio.numero_predial = '{parcel_number}' END
        		UNION
        	SELECT uebaunit.ue_terreno FROM {schema}.predio LEFT JOIN {schema}.uebaunit ON predio.t_id = uebaunit.baunit_predio  WHERE uebaunit.ue_terreno IS NOT NULL AND CASE WHEN '{previous_parcel_number}' = 'NULL' THEN  1 = 2 ELSE predio.numero_predial_anterior = '{previous_parcel_number}' END
         ),
         predios_seleccionados AS (
        	SELECT uebaunit.baunit_predio as t_id FROM {schema}.uebaunit WHERE uebaunit.ue_terreno = {plot_t_id} AND '{plot_t_id}' <> 'NULL'
        		UNION
        	SELECT t_id FROM {schema}.predio WHERE CASE WHEN '{parcel_fmi}' = 'NULL' THEN  1 = 2 ELSE predio.fmi = '{parcel_fmi}' END
        		UNION
        	SELECT t_id FROM {schema}.predio WHERE CASE WHEN '{parcel_number}' = 'NULL' THEN  1 = 2 ELSE predio.numero_predial = '{parcel_number}' END
        		UNION
        	SELECT t_id FROM {schema}.predio WHERE CASE WHEN '{previous_parcel_number}' = 'NULL' THEN  1 = 2 ELSE predio.numero_predial_anterior = '{previous_parcel_number}' END
         ),
         construcciones_seleccionadas AS (
        	 SELECT ue_construccion FROM {schema}.uebaunit WHERE uebaunit.baunit_predio IN (SELECT predios_seleccionados.t_id FROM predios_seleccionados WHERE predios_seleccionados.t_id IS NOT NULL) AND ue_construccion IS NOT NULL
         ),
         unidadesconstruccion_seleccionadas AS (
        	 SELECT unidadconstruccion.t_id FROM {schema}.unidadconstruccion WHERE unidadconstruccion.construccion IN (SELECT ue_construccion FROM construcciones_seleccionadas)
         ),
        """

        if self.valuation_model_exists():
            query += """
         info_calificacion_convencional AS (
        	SELECT avaluounidadconstruccion.aucons,
        				json_build_object('id', calificacion_convencional.t_id,
        									   'attributes', json_build_object('Tipo calificar', calificacion_convencional.tipo_calificar
        																	   , 'Armazón', calificacion_convencional.armazon
        																	   , 'Puntos armazón', calificacion_convencional.puntos_armazon
        																	   , 'Muros', calificacion_convencional.muros
        																	   , 'Puntos muro', calificacion_convencional.puntos_muro
        																	   , 'Cubierta', calificacion_convencional.cubierta
        																	   , 'Puntos cubierta', calificacion_convencional.puntos_cubierta
        																	   , 'Conservación estructura', calificacion_convencional.conservacion_estructura
        																	   , 'Puntos estructura conservación', calificacion_convencional.puntos_estructura_conservacion
        																	   , 'Subtotal estructura', calificacion_convencional.sub_total_estructura
        																	   , 'Fachada', calificacion_convencional.fachada
        																	   , 'Puntos fachada', calificacion_convencional.puntos_fachada
        																	   , 'Cubrimientos muros', calificacion_convencional.cubrimiento_muros
        																	   , 'Puntos cubrimiento muros', calificacion_convencional.puntos_cubrimiento_muros
        																	   , 'Piso', calificacion_convencional.piso
        																	   , 'Puntos piso', calificacion_convencional.puntos_piso
        																	   , 'Conservación acabados', calificacion_convencional.conservacion_acabados
        																	   , 'Puntos conservación acabados', calificacion_convencional.puntos_conservacion_acabados
        																	   , 'Subtotal acabados', calificacion_convencional.sub_total_acabados
        																	   , 'Tamaño baño', calificacion_convencional.tamanio_banio
        																	   , 'Puntos tamaño baño', calificacion_convencional.puntos_tamanio_banio
        																	   , 'Enchape baño', calificacion_convencional.enchape_banio
        																	   , 'Puntos enchape baño', calificacion_convencional.puntos_enchape_banio
        																	   , 'Mobiliario baño', calificacion_convencional.mobiliario_banio
        																	   , 'Puntos mobiliario baño', calificacion_convencional.puntos_mobiliario_banio
        																	   , 'Conservación baño', calificacion_convencional.conservacion_banio
        																	   , 'Puntos conservación baño', calificacion_convencional.puntos_conservacion_banio
        																	   , 'Subtotal baño', calificacion_convencional.sub_total_banio
        																	   , 'Tamaño cocina', calificacion_convencional.tamanio_cocina
        																	   , 'Puntos tamaño cocina', calificacion_convencional.puntos_tamanio_cocina
        																	   , 'Enchape cocina', calificacion_convencional.enchape_cocina
        																	   , 'Puntos enchape cocina', calificacion_convencional.puntos_enchape_cocina
        																	   , 'Mobiliario cocina', calificacion_convencional.mobiliario_cocina
        																	   , 'Puntos mobiliario cocina', calificacion_convencional.puntos_mobiliario_cocina
        																	   , 'Conservación cocina', calificacion_convencional.conservacion_cocina
        																	   , 'Puntos conservacion cocina', calificacion_convencional.puntos_conservacion_cocina
        																	   , 'Subtotal cocina', calificacion_convencional.sub_total_cocina
        																	   , 'Total residencial y comercial', calificacion_convencional.total_residencial_y_comercial
        																	   , 'Cerchas', calificacion_convencional.cerchas
        																	   , 'Puntos cerchas', calificacion_convencional.puntos_cerchas
        																	   , 'Total industrial', calificacion_convencional.total_industrial))
        		AS calificacion_convencional
        	FROM {schema}.calificacion_convencional LEFT JOIN {schema}.avaluounidadconstruccion ON calificacion_convencional.unidadconstruccion = avaluounidadconstruccion.aucons
        	WHERE avaluounidadconstruccion.ucons IN (SELECT * FROM unidadesconstruccion_seleccionadas)
         ),
         info_calificacion_no_convencional AS (
        	SELECT avaluounidadconstruccion.aucons,
        				json_build_object('id', calificacion_no_convencional.t_id,
        									   'attributes', json_build_object('Tipo de anexo', calificacion_no_convencional.tipo_anexo
        																	   , 'Descripción anexo', calificacion_no_convencional.descripcion_anexo
        																	   , 'Puntaje anexo', calificacion_no_convencional.puntaje_anexo))
        		AS calificacion_no_convencional
        	FROM {schema}.calificacion_no_convencional LEFT JOIN {schema}.avaluounidadconstruccion ON calificacion_no_convencional.unidadconstruccion = avaluounidadconstruccion.aucons
        	WHERE avaluounidadconstruccion.ucons IN (SELECT * FROM unidadesconstruccion_seleccionadas)
         ),
            """

        query += """
         info_uc AS (
        	 SELECT unidadconstruccion.construccion,
        			json_agg(json_build_object('id', unidadconstruccion.t_id,
        							  'attributes', json_build_object('Número de pisos', unidadconstruccion.numero_pisos
        															  , 'Área construida', unidadconstruccion.area_construida
        """

        if self.valuation_model_exists():
            query += """
        															  , 'Uso',  unidad_construccion.uso
        															  , 'Destino económico',  unidad_construccion.destino_econo
        															  , 'Tipología',  unidad_construccion.tipologia
        															  , 'Puntuación',  unidad_construccion.puntuacion
        															  , 'Valor m2 construcción',  unidad_construccion.valor_m2_construccion
        															  , 'Año construcción',  unidad_construccion.anio_construction
        															  , 'Estado conservación',  unidad_construccion.estado_conservacion
        															  , 'Número de habitaciones',  unidad_construccion.num_habitaciones
        															  , 'Número de baños',  unidad_construccion.num_banios
        															  , 'Número de cocinas',  unidad_construccion.num_cocinas
        															  , 'Número de oficinas',  unidad_construccion.num_oficinas
        															  , 'Número de estudios',  unidad_construccion.num_estudios
        															  , 'Número de bodegas',  unidad_construccion.num_bodegas
        															  , 'Numero de locales',  unidad_construccion.num_locales
        															  , 'Número de salas',  unidad_construccion.num_salas
        															  , 'Número de comedores',  unidad_construccion.num_comedores
        															  , 'Material',  unidad_construccion.material
        															  , 'Estilo',  unidad_construccion.estilo
        															  , 'Acceso',  unidad_construccion.acceso
        															  , 'nivel de acceso',  unidad_construccion.nivel_de_acceso
        															  , 'Ubicación en copropiedad',  unidad_construccion.ubicacion_en_copropiedad
        															  , 'Disposición',  unidad_construccion.disposicion
        															  , 'Funcionalidad',  unidad_construccion.funcionalidad
        															  , 'Tipo de construcción',  unidad_construccion.construccion_tipo
        															  , 'Calificación', CASE WHEN info_calificacion_convencional.calificacion_convencional IS NOT NULL THEN
        															  						COALESCE(info_calificacion_convencional.calificacion_convencional, '[]')
        															  					ELSE
        															  						COALESCE(info_calificacion_no_convencional.calificacion_no_convencional, '[]')
        															  					END
            """

        query += """
        															 ))) FILTER(WHERE unidadconstruccion.t_id IS NOT NULL)  as unidadconstruccion
        	 FROM {schema}.unidadconstruccion
        """

        if self.valuation_model_exists():
            query += """
        	 LEFT JOIN {schema}.avaluounidadconstruccion ON unidadconstruccion.t_id = avaluounidadconstruccion.ucons
        	 LEFT JOIN {schema}.unidad_construccion ON avaluounidadconstruccion.aucons = unidad_construccion.t_id
        	 LEFT JOIN info_calificacion_convencional ON unidad_construccion.t_id = info_calificacion_convencional.aucons
        	 LEFT JOIN info_calificacion_no_convencional ON unidad_construccion.t_id = info_calificacion_no_convencional.aucons
            """

        query += """
        	 WHERE unidadconstruccion.t_id IN (SELECT * FROM unidadesconstruccion_seleccionadas)
        	 GROUP BY unidadconstruccion.construccion
         ),
         info_construccion as (
        	 SELECT uebaunit.baunit_predio,
        			json_agg(json_build_object('id', construccion.t_id,
        							  'attributes', json_build_object('Área construcción', construccion.area_construccion,
        															  'unidadconstruccion', COALESCE(info_uc.unidadconstruccion, '[]')
        															 ))) FILTER(WHERE construccion.t_id IS NOT NULL) as construccion
        	 FROM {schema}.construccion LEFT JOIN info_uc ON construccion.t_id = info_uc.construccion
             LEFT JOIN {schema}.uebaunit ON uebaunit.ue_construccion = info_uc.construccion
        	 WHERE construccion.t_id IN (SELECT * FROM construcciones_seleccionadas)
        	 GROUP BY uebaunit.baunit_predio
         ),
         info_predio AS (
        	 SELECT uebaunit.ue_terreno,
        			json_agg(json_build_object('id', predio.t_id,
        							  'attributes', json_build_object('Departamento', predio.departamento,
        															  'Municipio', predio.municipio,
        															  'Zona', predio.zona,
        															  'NUPRE', predio.nupre,
        															  'FMI', predio.fmi,
        															  'Número predial', predio.numero_predial,
        															  'Número predial anterior', predio.numero_predial_anterior,
        															  'Avalúo predio', predio.avaluo_predio,
        															  'Tipo', predio.tipo,
        """

        if self.property_record_card_model_exists():
            query += """
        															  'Destinación económica', predio_ficha.destinacion_economica,
            """

        query += """
        															  'construccion', COALESCE(info_construccion.construccion, '[]')
        															 ))) FILTER(WHERE predio.t_id IS NOT NULL) as predio
        	 FROM {schema}.predio LEFT JOIN {schema}.uebaunit ON uebaunit.baunit_predio = predio.t_id
        	 LEFT JOIN info_construccion ON predio.t_id = info_construccion.baunit_predio
        """

        if self.property_record_card_model_exists():
            query += """
        	 LEFT JOIN {schema}.predio_ficha ON predio_ficha.crpredio = predio.t_id
            """

        query += """
        	 WHERE predio.t_id IN (SELECT * FROM predios_seleccionados) AND uebaunit.ue_terreno IS NOT NULL
             GROUP BY uebaunit.ue_terreno
         ),
        """

        if self.valuation_model_exists():
            query += """
         info_zona_homogenea_geoeconomica AS (
        	SELECT terreno.t_id,
        		json_agg(
        				json_build_object('id', zona_homogenea_geoeconomica.t_id,
        									   'attributes', json_build_object('Porcentaje', ROUND((st_area(st_intersection(terreno.poligono_creado, zona_homogenea_geoeconomica.geometria))/ st_area(terreno.poligono_creado))::numeric * 100,2),
        									                                   'Valor', zona_homogenea_geoeconomica.valor,
        																	   'Identificador', zona_homogenea_geoeconomica.identificador))
        		) FILTER(WHERE zona_homogenea_geoeconomica.t_id IS NOT NULL) AS zona_homogenea_geoeconomica
        	FROM {schema}.terreno, {schema}.zona_homogenea_geoeconomica
            WHERE terreno.t_id IN (SELECT * FROM terrenos_seleccionados) AND
        		  st_intersects(terreno.poligono_creado, zona_homogenea_geoeconomica.geometria) = True AND
        		  st_area(st_intersection(terreno.poligono_creado, zona_homogenea_geoeconomica.geometria)) > 0
        	GROUP BY terreno.t_id
         ),
         info_zona_homogenea_fisica AS (
        	SELECT terreno.t_id,
        		json_agg(
        				json_build_object('id', zona_homogenea_fisica.t_id,
        									   'attributes', json_build_object('Porcentaje', ROUND((st_area(st_intersection(terreno.poligono_creado, zona_homogenea_fisica.geometria))/ st_area(terreno.poligono_creado))::numeric * 100, 2),
        																	   'Identificador', zona_homogenea_fisica.identificador))
        		) FILTER(WHERE zona_homogenea_fisica.t_id IS NOT NULL) AS zona_homogenea_fisica
        	FROM {schema}.terreno, {schema}.zona_homogenea_fisica
            WHERE terreno.t_id IN (SELECT * FROM terrenos_seleccionados) AND
        		  st_intersects(terreno.poligono_creado, zona_homogenea_fisica.geometria) = True AND
        		  st_area(st_intersection(terreno.poligono_creado, zona_homogenea_fisica.geometria)) > 0
        	GROUP BY terreno.t_id
         ),
            """

        query += """
         info_terreno AS (
        	SELECT terreno.t_id,
              json_build_object('id', terreno.t_id,
        						'attributes', json_build_object('Área de terreno', terreno.area_calculada
        """

        if self.valuation_model_exists():
            query += """
        														, 'zona_homogenea_geoeconomica', COALESCE(info_zona_homogenea_geoeconomica.zona_homogenea_geoeconomica, '[]')
        														, 'info_zona_homogenea_fisica', COALESCE(info_zona_homogenea_fisica.zona_homogenea_fisica, '[]')
            """

        query += """
        														, 'predio', COALESCE(info_predio.predio, '[]')
        													   )) as terreno
            FROM {schema}.terreno LEFT JOIN info_predio ON info_predio.ue_terreno = terreno.t_id
        """

        if self.valuation_model_exists():
            query += """
            LEFT JOIN info_zona_homogenea_geoeconomica ON info_zona_homogenea_geoeconomica.t_id = terreno.t_id
            LEFT JOIN info_zona_homogenea_fisica ON info_zona_homogenea_fisica.t_id = terreno.t_id
            """

        query += """
        	WHERE terreno.t_id IN (SELECT * FROM terrenos_seleccionados)
         )
        SELECT json_agg(info_terreno.terreno) AS terreno FROM info_terreno
        """

        query = query.format(schema=self.schema,
                             plot_t_id=params['plot_t_id'],
                             parcel_fmi=params['parcel_fmi'],
                             parcel_number=params['parcel_number'],
                             previous_parcel_number=params['previous_parcel_number'])

        if self.conn is None:
            res, msg = self.test_connection()
            if not res:
                return (res, msg)
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        cur.execute(query)
        records = cur.fetchall()
        res = [record._asdict() for record in records]

        #print("ECONOMIC QUERY:", query)

        return res


    def get_annex17_plot_data(self, plot_id, mode='only_id'):
        if self.conn is None:
            res, msg = self.test_connection()
            if not res:
                return (res, msg)

        where_id = ""
        if mode != 'all':
            where_id = "WHERE l.t_id {} {}".format('=' if mode=='only_id' else '!=', plot_id)

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = """SELECT array_to_json(array_agg(features)) AS features
                    FROM (
                        SELECT f AS features
                        FROM (
                            SELECT 'Feature' AS type
                                ,row_to_json((
                                    SELECT l
                                    FROM (
                                        SELECT left(right(numero_predial,15),6) AS predio
                                        ) AS l
                                    )) AS properties
                                ,ST_AsGeoJSON(poligono_creado)::json AS geometry
                            FROM {schema}.terreno AS l
                            LEFT JOIN {schema}.uebaunit ON l.t_id = ue_terreno
                            LEFT JOIN {schema}.predio ON predio.t_id = baunit_predio
                            {where_id}
                            ) AS f
                        ) AS ff;""".format(schema=self.schema, where_id=where_id)
        cur.execute(query)

        if mode == 'only_id':
            return cur.fetchone()[0]
        else:
            return cur.fetchall()[0][0]

    def get_annex17_building_data(self):
        if self.conn is None:
            res, msg = self.test_connection()
            if not res:
                return (res, msg)

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = """SELECT array_to_json(array_agg(features)) AS features
                    FROM (
                    	SELECT f AS features
                    	FROM (
                    		SELECT 'Feature' AS type
                    			,ST_AsGeoJSON(poligono_creado)::json AS geometry
                    			,row_to_json((
                    					SELECT l
                    					FROM (
                    						SELECT t_id AS t_id
                    						) AS l
                    					)) AS properties
                            FROM {schema}.construccion AS c
                    		) AS f
                        ) AS ff;""".format(schema=self.schema)
        cur.execute(query)

        return cur.fetchall()[0][0]

    def get_annex17_point_data(self, plot_id):
        if self.conn is None:
            res, msg = self.test_connection()
            if not res:
                return (res, msg)

        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = """WITH parametros
                    AS (
                    	SELECT {id} AS poligono_t_id
                    		,2 AS criterio_punto_inicial
                    		,4 AS criterio_observador
                    		,true AS incluir_tipo_derecho
                    	)
                    	,t
                    AS (
                    	SELECT t_id
                    		,ST_ForceRHR(poligono_creado) AS poligono_creado
                    	FROM {schema}.terreno AS t
                    		,parametros
                    	WHERE t.t_id = poligono_t_id
                    	)
                    	,a
                    AS (
                    	SELECT ST_SetSRID(ST_MakePoint(st_xmin(t.poligono_creado), st_ymax(t.poligono_creado)), ST_SRID(t.poligono_creado)) AS p
                    	FROM t
                    	)
                    	,b
                    AS (
                    	SELECT ST_SetSRID(ST_MakePoint(st_xmax(t.poligono_creado), st_ymax(t.poligono_creado)), ST_SRID(t.poligono_creado)) AS p
                    	FROM t
                    	)
                    	,c
                    AS (
                    	SELECT ST_SetSRID(ST_MakePoint(st_xmax(t.poligono_creado), st_ymin(t.poligono_creado)), ST_SRID(t.poligono_creado)) AS p
                    	FROM t
                    	)
                    	,d
                    AS (
                    	SELECT ST_SetSRID(ST_MakePoint(st_xmin(t.poligono_creado), st_ymin(t.poligono_creado)), ST_SRID(t.poligono_creado)) AS p
                    	FROM t
                    	)
                    	,m
                    AS (
                    	SELECT CASE
                    			WHEN criterio_observador = 1
                    				THEN (
                    						SELECT ST_SetSRID(ST_MakePoint(st_x(ST_centroid(t.poligono_creado)), st_y(ST_centroid(t.poligono_creado))), ST_SRID(t.poligono_creado)) AS p
                    						FROM t
                    						)
                    			WHEN criterio_observador = 2
                    				THEN (
                    						SELECT ST_SetSRID(ST_MakePoint(st_x(ST_centroid(st_envelope(t.poligono_creado))), st_y(ST_centroid(st_envelope(t.poligono_creado)))), ST_SRID(t.poligono_creado)) AS p
                    						FROM t
                    						)
                    			WHEN criterio_observador = 3
                    				THEN (
                    						SELECT ST_SetSRID(ST_PointOnSurface(poligono_creado), ST_SRID(t.poligono_creado)) AS p
                    						FROM t
                    						)
                    			WHEN criterio_observador = 4
                    				THEN (
                    						SELECT ST_SetSRID(ST_MakePoint(st_x(ST_ClosestPoint(poligono_creado, ST_centroid(t.poligono_creado))), st_y(ST_ClosestPoint(poligono_creado, ST_centroid(t.poligono_creado)))), ST_SRID(t.poligono_creado)) AS p
                    						FROM t
                    						)
                    			ELSE (
                    					SELECT ST_SetSRID(ST_MakePoint(st_x(ST_centroid(st_envelope(t.poligono_creado))), st_y(ST_centroid(st_envelope(t.poligono_creado)))), ST_SRID(t.poligono_creado)) AS p
                    					FROM t
                    					)
                    			END AS p
                    	FROM parametros
                    	)
                    	,norte
                    AS (
                    	SELECT ST_SetSRID(ST_MakePolygon(ST_MakeLine(ARRAY [a.p, b.p, m.p, a.p])), ST_SRID(t.poligono_creado)) geom
                    	FROM t
                    		,a
                    		,b
                    		,m
                    	)
                    	,este
                    AS (
                    	SELECT ST_SetSRID(ST_MakePolygon(ST_MakeLine(ARRAY [m.p, b.p, c.p, m.p])), ST_SRID(t.poligono_creado)) geom
                    	FROM t
                    		,b
                    		,c
                    		,m
                    	)
                    	,sur
                    AS (
                    	SELECT ST_SetSRID(ST_MakePolygon(ST_MakeLine(ARRAY [m.p, c.p, d.p, m.p])), ST_SRID(t.poligono_creado)) geom
                    	FROM t
                    		,m
                    		,c
                    		,d
                    	)
                    	,oeste
                    AS (
                    	SELECT ST_SetSRID(ST_MakePolygon(ST_MakeLine(ARRAY [a.p, m.p, d.p, a.p])), ST_SRID(t.poligono_creado)) geom
                    	FROM t
                    		,a
                    		,m
                    		,d
                    	)
                    	,limite_poligono
                    AS (
                    	SELECT t_id
                    		,ST_Boundary(poligono_creado) geom
                    	FROM t
                    	)
                    	,limite_vecinos
                    AS (
                    	SELECT o.t_id
                    		,ST_Boundary(o.poligono_creado) geom
                    	FROM t
                    		,{schema}.terreno o
                    	WHERE o.poligono_creado && st_envelope(t.poligono_creado)
                    		AND t.t_id <> o.t_id
                    	)
                    	,pre_colindancias
                    AS (
                    	SELECT limite_vecinos.t_id
                    		,st_intersection(limite_poligono.geom, limite_vecinos.geom) geom
                    	FROM limite_poligono
                    		,limite_vecinos
                    	WHERE st_intersects(limite_poligono.geom, limite_vecinos.geom)
                    		AND limite_poligono.t_id <> limite_vecinos.t_id

                    	UNION

                    	SELECT NULL AS t_id
                    		,ST_Difference(limite_poligono.geom, a.geom) geom
                    	FROM limite_poligono
                    		,(
                    			SELECT ST_LineMerge(ST_Union(geom)) geom
                    			FROM limite_vecinos
                    			) a
                    	)
                    	,tmp_colindantes
                    AS (
                    	SELECT t_id
                    		,ST_LineMerge(ST_Union(geom)) geom
                    	FROM (
                    		SELECT SIMPLE.t_id
                    			,SIMPLE.simple_geom AS geom
                    			,ST_GeometryType(SIMPLE.simple_geom) AS geom_type
                    			,ST_AsEWKT(SIMPLE.simple_geom) AS geom_wkt
                    		FROM (
                    			SELECT dumped.*
                    				,(dumped.geom_dump).geom AS simple_geom
                    				,(dumped.geom_dump).path AS path
                    			FROM (
                    				SELECT *
                    					,ST_Dump(geom) AS geom_dump
                    				FROM pre_colindancias
                    				) AS dumped
                    			) AS SIMPLE
                    		) a
                    	GROUP BY t_id
                    	)
                    	,lineas_colindancia
                    AS (
                    	SELECT *
                    	FROM (
                    		SELECT SIMPLE.t_id
                    			,SIMPLE.simple_geom AS geom
                    		FROM (
                    			SELECT dumped.*
                    				,(dumped.geom_dump).geom AS simple_geom
                    				,(dumped.geom_dump).path AS path
                    			FROM (
                    				SELECT *
                    					,ST_Dump(geom) AS geom_dump
                    				FROM (
                    					SELECT *
                    					FROM tmp_colindantes
                    					WHERE ST_GeometryType(geom) = 'ST_MultiLineString'
                    					) a
                    				) AS dumped
                    			) AS SIMPLE
                    		) a

                    	UNION

                    	SELECT *
                    	FROM tmp_colindantes
                    	WHERE ST_GeometryType(geom) <> 'ST_MultiLineString'
                    	)
                    	,puntos_terreno
                    AS (
                    	SELECT (ST_DumpPoints(poligono_creado)).* AS dp
                    	FROM t
                    	)
                    	,punto_nw
                    AS (
                    	SELECT geom
                    		,st_distance(geom, nw) AS dist
                    	FROM puntos_terreno
                    		,(
                    			SELECT ST_SetSRID(ST_MakePoint(st_xmin(st_envelope(poligono_creado)), st_ymax(st_envelope(poligono_creado))), ST_SRID(poligono_creado)) AS nw
                    			FROM t
                    			) a
                    	ORDER BY dist limit 1
                    	)
                    	,punto_inicial_por_lindero_con_punto_nw
                    AS (
                    	SELECT st_startpoint(lineas_colindancia.geom) geom
                    	FROM lineas_colindancia
                    		,punto_nw
                    	WHERE st_intersects(lineas_colindancia.geom, punto_nw.geom)
                    		AND NOT st_intersects(st_endpoint(lineas_colindancia.geom), punto_nw.geom) limit 1
                    	)
                    	,punto_inicial_por_lindero_porcentaje_n
                    AS (
                    	SELECT round((st_length(st_intersection(lineas_colindancia.geom, norte.geom)) / st_length(lineas_colindancia.geom))::NUMERIC, 2) dist
                    		,st_startpoint(lineas_colindancia.geom) geom
                    		,st_distance(lineas_colindancia.geom, nw) distance_to_nw
                    	FROM lineas_colindancia
                    		,norte
                    		,(
                    			SELECT ST_SetSRID(ST_MakePoint(st_xmin(st_envelope(poligono_creado)), st_ymax(st_envelope(poligono_creado))), ST_SRID(poligono_creado)) AS nw
                    			FROM t
                    			) a
                    	WHERE st_intersects(lineas_colindancia.geom, norte.geom)
                    	ORDER BY dist DESC
                    		,distance_to_nw limit 1
                    	)
                    	,punto_inicial
                    AS (
                    	SELECT CASE
                    			WHEN criterio_punto_inicial = 1
                    				THEN (
                    						SELECT geom
                    						FROM punto_inicial_por_lindero_con_punto_nw
                    						)
                    			WHEN criterio_punto_inicial = 2
                    				THEN (
                    						SELECT geom
                    						FROM punto_inicial_por_lindero_porcentaje_n
                    						)
                    			END AS geom
                    	FROM parametros
                    	)
                    	,puntos_ordenados
                    AS (
                    	SELECT CASE
                    			WHEN id - m + 1 <= 0
                    				THEN total + id - m
                    			ELSE id - m + 1
                    			END AS id
                    		,geom
                    		,st_x(geom) x
                    		,st_y(geom) y
                    	FROM (
                    		SELECT row_number() OVER (
                    				ORDER BY path
                    				) AS id
                    			,m
                    			,path
                    			,geom
                    			,total
                    		FROM (
                    			SELECT (ST_DumpPoints(ST_ForceRHR(poligono_creado))).* AS dp
                    				,ST_NPoints(poligono_creado) total
                    				,poligono_creado
                    			FROM t
                    			) AS a
                    			,(
                    				SELECT row_number() OVER (
                    						ORDER BY path
                    						) AS m
                    					,st_distance(puntos_terreno.geom, punto_inicial.geom) AS dist
                    				FROM puntos_terreno
                    					,punto_inicial
                    				ORDER BY dist limit 1
                    				) b
                    		) t
                    	WHERE id <> total
                    	ORDER BY id
                    	)
                    SELECT array_to_json(array_agg(features)) AS features
                    FROM (
                    	SELECT f AS features
                    	FROM (
                    		SELECT 'Feature' AS type
                    			,ST_AsGeoJSON(geom)::json AS geometry
                    			,row_to_json((
                    					SELECT l
                    					FROM (
                    						SELECT id AS point_number
                    						) AS l
                    					)) AS properties
                    		FROM puntos_ordenados
                    		) AS f
                    	) AS ff;""".format(schema=self.schema, id=plot_id)
        cur.execute(query)

        return cur.fetchone()[0]

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
        if self.conn is None:
            res, msg = self.test_connection()
            if not res:
                return (res, msg)
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query)
        return cur.fetchall()

    def _schema_names_list(self):
        query = """
                    SELECT n.nspname as "schema_name"
                    FROM pg_catalog.pg_namespace n
                    WHERE n.nspname !~ '^pg_' AND n.nspname <> 'information_schema' AND nspname <> 'public'
                    ORDER BY 1"""

        result = self.execute_sql_query(query)
        return result if not isinstance(result, tuple) else None

    def get_models(self, schema=None):
        query = "SELECT modelname FROM {schema}.t_ili2db_model".format(schema=schema if schema else self.schema)
        result = self.execute_sql_query(query)
        return result if not isinstance(result, tuple) else None

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
                return (False, QCoreApplication.translate("PGConnector", "An error occurred while trying to create the '{}' database: {}".format(db_name, e)))
        cur.close()
        conn.close()
        return (True, QCoreApplication.translate("PGConnector", "Database '{}' was successfully created!".format(db_name)))

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
                return (False, QCoreApplication.translate("PGConnector", "An error occurred while trying to create the '{}' schema: {}".format(schema_name, e)))
        cur.close()
        conn.close()
        return (True, QCoreApplication.translate("PGConnector", "Schema '{}' was successfully created!".format(schema_name)))

    def get_dbnames_list(self, uri):
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
                                               "There was an error when obtaining the list of existing databases. : {}").format(e))
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
                                               "There was an error when obtaining the list of existing schemas: {}").format(e))
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
                return (False, QCoreApplication.translate("PGConnector", "No information for schema '{}'.").format(self.schema))
            cur.close()
            conn.close()
        except Exception as e:
            return (False, QCoreApplication.translate("PGConnector",
                                               "There was an error when obtaining privileges for schema '{}'. Details: {}").format(schema, e))
        return (True, privileges)
