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

from .db_connector import DBConnector

class PGConnector(DBConnector):
    def __init__(self, uri, schema="public"):
        DBConnector.__init__(self, uri, schema)
        self.uri = uri
        self.conn = None
        self.schema = schema
        self.mode = 'pg'
        self.provider = 'postgres'
        self._tables_info = None

    def test_connection(self):
        try:
            self.conn = psycopg2.connect(self.uri)
            print("Connection was set!", self.conn)
        except Exception as e:
            return (False,
                    self.tr("There was an error connecting to the database: {}".format(e)))
        return (True, self.tr("Connection to PostGIS successful!"))

        # TODO does the schema exist?

    def save_connection(self):
        if self.conn is None:
            self.conn = psycopg2.connect(self.uri)
            print("Connection was set!", self.conn)

    def validate_db(self):
        pass

    def get_uri_for_layer(self, layer_name):
        #uri = 'dbname=\'test3\' host=localhost port=5432 user=\'postgres\' password=\'postgres\' sslmode=disable key=\'t_id\' srid=3116 type=Point checkPrimaryKeyUnicity=\'1\' table="ladm_col_02"."puntolindero" (localizacion_original) sql='
        #if self._tables_info is None:
        #    res, cur = self.get_tables_info()
        #    if not res:
        #        return (res, cur)
        #    self._tables_info = cur

        res, cur = self.get_tables_info()
        if not res:
            return (res, cur)

        for record in cur:
            if record['schemaname'] == self.schema and record['tablename'] == layer_name.lower():
                if record['geometry_column']:
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
                return (True, data_source_uri)
        return (False, self.tr("Layer '{}' was not found in the database (schema: {}).").format(layer_name, self.schema))

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
