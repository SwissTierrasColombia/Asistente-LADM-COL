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
import psycopg2.extras
from psycopg2 import ProgrammingError
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsWkbTypes,
                       Qgis,
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
    def __init__(self, uri, schema="public"):
        DBConnector.__init__(self, uri, schema)
        self.uri = uri
        self.conn = None
        self.schema = schema
        self.log = QgsApplication.messageLog()
        self.mode = 'pg'
        self.provider = 'postgres'
        self._tables_info = None
        self.model_parser = None

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
                'table_name': QCoreApplication.translate("LogicChecksConfigStrings","Logic Consistency Errors in table '{table}'").format(table=PARCEL_TABLE),
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
                'table_name': QCoreApplication.translate("LogicChecksConfigStrings", 'Parcels with repeated domain right'),
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

    def _schema_exists(self):
        if self.schema:
            cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("""
                        SELECT EXISTS(SELECT 1 FROM pg_namespace WHERE nspname = '{}');
            """.format(self.schema))

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

    def test_connection(self):
        try:
            self.conn = psycopg2.connect(self.uri)
            self.log.logMessage("Connection was set! {}".format(self.conn), PLUGIN_NAME, Qgis.Info)
        except Exception as e:
            return (False, QCoreApplication.translate("PGConnector",
                    "There was an error connecting to the database: {}").format(e))

        if not self._postgis_exists():
            return (False, QCoreApplication.translate("PGConnector",
                    "The current database does not have PostGIS installed! Please install it before proceeding."))
        if not self._schema_exists():
            return (False, QCoreApplication.translate("PGConnector",
                    "The schema '{}' does not exist in the database!").format(self.schema))
        if not self._metadata_exists():
            return (False, QCoreApplication.translate("PGConnector",
                    "The schema '{}' is not a valid INTERLIS schema. That is, the schema doesn't have some INTERLIS metadata tables.").format(self.schema))

        if self.model_parser is None:
            self.model_parser = ModelParser(self)
        if not self.model_parser.validate_cadastre_model_version()[0]:
            return (False, QCoreApplication.translate("PGConnector",
                    "The version of the Cadastre-Registry model in the database is old and is not supported in this version of the plugin. Go to <a href=\"{}\">the QGIS Plugins Repo</a> to download another version of this plugin.").format(PLUGIN_DOWNLOAD_URL_IN_QGIS_REPO))

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

    def _get_models(self, dbschema):
        query = "SELECT modelname FROM {schema}.t_ili2db_model".format(schema=dbschema)
        result = self.execute_sql_query(query)
        return result if not isinstance(result, tuple) else None
