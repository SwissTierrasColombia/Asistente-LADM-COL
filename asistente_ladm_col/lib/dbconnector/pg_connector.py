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

from qgis.core import QgsWkbTypes, Qgis, QgsApplication
from qgis.PyQt.QtCore import QCoreApplication

from .db_connector import DBConnector
from ...config.general_config import PLUGIN_NAME, INTERLIS_TEST_METADATA_TABLE_PG

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

        if not self._schema_exists():
            return (False, QCoreApplication.translate("PGConnector",
                    "The schema '{}' does not exist in the database!").format(self.schema))
        if not self._metadata_exists():
            return (False, QCoreApplication.translate("PGConnector",
                    "The schema '{}' is not a valid INTERLIS schema. That is, the schema doesn't have some INTERLIS metadata tables.").format(self.schema))

        return (True, QCoreApplication.translate("PGConnector", "Connection to PostGIS successful!"))

    def save_connection(self):
        if self.conn is None:
            self.conn = psycopg2.connect(self.uri)
            self.log.logMessage("Connection was set! {}".format(self.conn), PLUGIN_NAME, Qgis.Info)

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

    def retrieveSqlData(self, sql_query):
        if self.conn is None:
            res, msg = self.test_connection()
            if not res:
                return (res, msg)
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = cur.execute(sql_query)
        results = cur.fetchall()
        colnames = {desc[0]: cur.description.index(desc) for desc in cur.description}
        return colnames, results

    def get_parcels_and_parties_by_plot(self, plot__t_id):
        sql_query = """
             SELECT     predio.fmi            AS "Folio" ,
                       predio.nupre          AS "NUPRE" ,
                       predio.numero_predial AS "Número Predial" ,
                       predio.nombre         AS "Nombre del predio" ,
                       Json_agg(derecho)     AS derecho ,
                       CASE
                                  WHEN Json_agg(servidumbre)::text <> '[null]' THEN Json_agg(servidumbre)
                                  ELSE NULL
                       END AS servidumbre
            FROM       {db_schema}.terreno
            LEFT JOIN  {db_schema}.uebaunit
            ON         terreno.t_id = uebaunit.ue_terreno
            LEFT JOIN  {db_schema}.predio
            ON         predio.t_id = uebaunit.baunit_predio
            INNER JOIN
                       (
                                 SELECT    col_derecho.unidad_predio ,
                                           col_derecho.tipo "Tipo derecho" ,
                                           col_derecho.codigo_registral_derecho "Codigo Registral" ,
                                           col_derecho.descripcion "Descripción" ,
                                           interesado_natural.documento_identidad "Documento Identidad" ,
                                           interesado_natural.tipo_documento "Tipo Documento" ,
                                           interesado_natural.primer_apellido "Primer Apellido" ,
                                           interesado_natural.primer_nombre "Primer Nombre" ,
                                           interesado_natural.segundo_apellido "Segundo Apellido" ,
                                           interesado_natural.segundo_nombre "Segundo Nombre" ,
                                           interesado_natural.genero "Género"
                                 FROM      {db_schema}.col_derecho
                                 LEFT JOIN {db_schema}.interesado_natural
                                 ON        col_derecho.interesado_interesado_natural = interesado_natural.t_id ) derecho
            ON         derecho.unidad_predio = predio.t_id
            LEFT JOIN
                       (
                              SELECT servidumbrepaso.identificador,
                                     uebaunit.baunit_predio,
                                     uebaunit.ue_servidumbrepaso,
                                     servidumbrepaso.etiqueta
                              FROM   {db_schema}.uebaunit
                              JOIN   {db_schema}.servidumbrepaso
                              ON     uebaunit.ue_servidumbrepaso = servidumbrepaso.t_id ) servidumbre
            ON         servidumbre.baunit_predio = predio.t_id
            WHERE      terreno.t_id = '{plot_t_id}'
            GROUP BY   predio.fmi ,
                       predio.nupre ,
                       predio.numero_predial ,
                       predio.nombre;
            """.format(db_schema=self.schema, plot_t_id=plot__t_id)
        return self.retrieveSqlData(sql_query)

