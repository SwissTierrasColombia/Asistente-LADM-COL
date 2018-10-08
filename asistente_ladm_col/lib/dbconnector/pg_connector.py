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
from ...config.general_config import (
    INTERLIS_TEST_METADATA_TABLE_PG,
    PLUGIN_NAME,
    PLUGIN_DOWNLOAD_URL_IN_QGIS_REPO
)
from ... utils.model_parser import ModelParser

class PGConnector(DBConnector):
    def __init__(self, uri, schema="public"):
        DBConnector.__init__(self, uri, schema)
        con = dbfin = 0
        dbname = uri2 = ""

        for uri_s in uri.split(" "):
            if uri_s.find("=") == -1:
                con = con + 1

        if con != 0:
            for uri_s in uri.split(" "):

                if uri_s.find("dbname") == 0:
                    dbsplit = uri_s.split("=")
                    dbname += dbsplit[len(dbsplit)-1] + " "
                    uri2 += dbsplit[0] + "="
                else:
                    if dbfin == con:
                        uri2 += "'"+dbname.strip()+"' "
                    if uri_s.find("=") > 0:
                        uri2 += uri_s + " "
                        dbfin = 0
                    else:
                        dbname += uri_s + " "
                        dbfin = dbfin + 1
        else:
            uri2 = uri

        self.uri = uri2
        self.conn = None
        self.schema = schema
        self.log = QgsApplication.messageLog()
        self.mode = 'pg'
        self.provider = 'postgres'
        self._tables_info = None
        self.model_parser = None

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
