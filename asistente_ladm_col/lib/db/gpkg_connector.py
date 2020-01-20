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
import os
import sqlite3

import qgis.utils
from qgis.PyQt.QtCore import QCoreApplication

from asistente_ladm_col.config.table_mapping_config import (T_ID,
                                                            DISPLAY_NAME,
                                                            ILICODE,
                                                            DESCRIPTION,
                                                            TABLE_NAME,
                                                            COMPOSED_KEY_SEPARATOR)
from asistente_ladm_col.lib.db.db_connector import (DBConnector,
                                                    EnumTestLevel)
from asistente_ladm_col.utils.utils import normalize_iliname


class GPKGConnector(DBConnector):

    _PROVIDER_NAME = 'ogr'

    def __init__(self, uri, conn_dict={}):
        DBConnector.__init__(self, uri, conn_dict)
        self.mode = 'gpkg'
        self.conn = None
        self.provider = 'ogr'

    @DBConnector.uri.setter
    def uri(self, value):
        self._dict_conn_params = {'dbfile': value}
        self._uri = value

    def test_connection(self, test_level=EnumTestLevel.LADM):
        try:

            # file no exist, but directory must exist
            if test_level & EnumTestLevel.SCHEMA_IMPORT:
                directory = os.path.dirname(self._uri)

                if not os.path.exists(directory):
                    raise Exception("GeoPackage directory file not found.")
            elif not os.path.exists(self._uri):
                raise Exception("GeoPackage file not found.")
            # TODO verify EnumTestLevel.LADM
        except Exception as e:
            return (False, QCoreApplication.translate("GPKGConnector",
                    "There was an error connecting to the database: {}").format(e))

        if not self._table_and_field_names:
            self._initialize_names()

        res, msg = self.names.test_names(self._table_and_field_names)
        if not res:
            return (False, QCoreApplication.translate("PGConnector",
                    "Table/field names from the DB are not correct. Details: {}.").format(msg))

        return (True, QCoreApplication.translate("GPKGConnector",
                "Connection to GeoPackage successful!"))

    def get_table_and_field_names(self):
        """
        Documented in super class
        """
        dict_names = dict()
        cursor = self.conn.cursor()

        # Get both table and field names. Only include field names that are not FKs, they will be added in a second step
        cursor.execute("""SELECT iliclass.iliname AS table_iliname,
                                s.name AS tablename,
                                ilicol.iliname AS field_iliname,
                                ilicol.sqlname AS fieldname
                            FROM sqlite_master s
                            LEFT JOIN t_ili2db_attrname ilicol
                            ON ilicol.colowner = s.name 
                            AND ilicol.target IS NULL
                            LEFT JOIN t_ili2db_classname iliclass
                               ON s.name == iliclass.sqlname
                            WHERE s.type='table' AND iliclass.iliname IS NOT NULL;""")
        records = cursor.fetchall()

        print("GPKG TEST1", len(records))
        for record in records:
            if record['table_iliname'] is None:
                # Either t_ili2db_* tables (INTERLIS meta-attrs)
                continue

            table_iliname = normalize_iliname(record['table_iliname'])

            if not table_iliname in dict_names:
                dict_names[table_iliname] = dict()
                dict_names[table_iliname][TABLE_NAME] = record['tablename']

            if record['field_iliname'] is None:
                # Fields for domains, like 'description' (we map it in a custom way later in this class method)
                continue

            field_iliname = normalize_iliname(record['field_iliname'])
            dict_names[table_iliname][field_iliname] = record['fieldname']

        # Map FK ilinames (i.e., those whose t_ili2db_attrname target column is not NULL)
        cursor.execute("""SELECT a.iliname as table_iliname,
                                   a.iliname, a.sqlname, 
                                   c.iliname as iliname2, 
                                   o.iliname as colowner
                            FROM t_ili2db_attrname a
                            INNER JOIN t_ili2db_classname o ON o.sqlname = a.colowner
                            INNER JOIN t_ili2db_classname c ON c.sqlname = a.target
                            ORDER BY a.iliname;""")
        records = cursor.fetchall()
        print("GPKG TEST2", len(records))
        for record in records:
            composed_key = "{}{}{}".format(normalize_iliname(record['iliname']),
                                           COMPOSED_KEY_SEPARATOR,
                                           normalize_iliname(record['iliname2']))
            table_iliname = normalize_iliname(record['table_iliname'])
            if table_iliname in dict_names:
                dict_names[table_iliname][composed_key] = record['sqlname']
            else:
                colowner = normalize_iliname(record['colowner'])
                if colowner in dict_names:
                    dict_names[colowner][composed_key] = record['sqlname']

        cursor.close()

        # Custom names
        dict_names[T_ID] = "T_Id"
        dict_names[DISPLAY_NAME] = "dispName"
        dict_names[ILICODE] = "iliCode"
        dict_names[DESCRIPTION] = "description"

        return dict_names

    def validate_db(self):
        pass

    def get_uri_for_layer(self, layer_name, geometry_type=None):
        return (True, '{uri}|layername={table}'.format(
                uri=self._uri,
                table=layer_name.lower()
            ))

    def get_models(self):
        cursor = self.conn.cursor()
        result = cursor.execute("""SELECT distinct substr(iliname, 1, pos-1) AS modelname from 
                                    (SELECT *, instr(iliname,'.') AS pos FROM t_ili2db_trafo)""")
        lst_models = list()
        if result is not None and not isinstance(result, tuple):
            lst_models = [db_model['modelname'] for db_model in result] 
            
        return lst_models

    def get_logic_validation_queries(self):
        raise NotImplementedError

    def is_ladm_layer(self, layer):
        result = False
        if layer.dataProvider().name() == GPKGConnector._PROVIDER_NAME:
            # Dbfile should be equal to _uri
            dbfile = layer.source().split('|')[0]
            result = (dbfile == self._uri)
        return result

    def get_ladm_layer_name(self, layer, validate_is_ladm=False):
        name = None
        if validate_is_ladm:
            if self.is_ladm_layer(layer):
                name = layer.source().split('|layername=')[1]
        else:
            name = layer.source().split('|layername=')[1]
        return name

    def get_description_conn_string(self):
        result = None
        if self.dict_conn_params['dbfile']:
            result = os.path.basename(self.dict_conn_params['dbfile'])
        return result

    def get_connection_uri(self, dict_conn, level=1):
        return dict_conn['dbfile']

    def open_connection(self):
        self.conn = qgis.utils.spatialite_connect(self._uri)
        self.conn.row_factory = sqlite3.Row

    def close_connection(self):
        pass  # this connection does not need to be closed
