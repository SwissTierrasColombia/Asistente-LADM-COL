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

from asistente_ladm_col.config.enums import EnumTestConnectionMsg
from asistente_ladm_col.config.keys.ili2db_keys import *
from asistente_ladm_col.config.query_names import QueryNames
from asistente_ladm_col.config.ili2db_names import ILI2DBNames
from asistente_ladm_col.lib.db.db_connector import (FileDB,
                                                    DBConnector)
from asistente_ladm_col.core.model_parser import ModelParser


class GPKGConnector(FileDB):

    _PROVIDER_NAME = 'ogr'
    _DEFAULT_VALUES = {
        'dbfile': ''
    }

    def __init__(self, uri, conn_dict=dict()):
        DBConnector.__init__(self, uri, conn_dict)
        self.engine = 'gpkg'
        self.conn = None
        self.provider = 'ogr'

    @DBConnector.uri.setter
    def uri(self, value):
        self._dict_conn_params = {'dbfile': value}
        self._uri = value

    def _get_table_and_field_names(self):
        """
        Documented in super class
        """
        if self.conn is None:
            res, msg = self.open_connection()
            if not res:
                self.logger.warning_msg(__name__, msg)
                return dict()

        cursor = self.conn.cursor()

        # Get both table and field names. Only include field names that are not FKs, they will be added in a second step
        cursor.execute("""SELECT iliclass.iliname AS {table_iliname},
                                s.name AS {table_name},
                                ilicol.iliname AS {field_iliname},
                                ilicol.sqlname AS {field_name}
                            FROM sqlite_master s
                            LEFT JOIN t_ili2db_attrname ilicol
                            ON ilicol.colowner = s.name 
                            AND ilicol.target IS NULL
                            LEFT JOIN t_ili2db_classname iliclass
                               ON s.name == iliclass.sqlname
                            WHERE s.type='table' AND iliclass.iliname IS NOT NULL;""".format(
            table_iliname=QueryNames.TABLE_ILINAME,
            table_name=QueryNames.TABLE_NAME,
            field_iliname=QueryNames.FIELD_ILINAME,
            field_name=QueryNames.FIELD_NAME))

        records = cursor.fetchall()
        cursor.close()

        return records

    def _get_fk_fields(self):
        if self.conn is None:
            res, msg = self.open_connection()
            if not res:
                self.logger.warning_msg(__name__, msg)
                return dict()

        cursor = self.conn.cursor()

        # Map FK ilinames (i.e., those whose t_ili2db_attrname target column is not NULL)
        cursor.execute("""SELECT rtrim(rtrim(a.iliname, replace(a.iliname, '.', '')), '.') as {table_iliname},
                                   a.iliname, a.sqlname,
                                   c.iliname as iliname2,
                                   o.iliname as colowner
                            FROM t_ili2db_attrname a
                            INNER JOIN t_ili2db_classname o ON o.sqlname = a.colowner
                            INNER JOIN t_ili2db_classname c ON c.sqlname = a.target
                            ORDER BY a.iliname;""".format(table_iliname=QueryNames.TABLE_ILINAME))

        records = cursor.fetchall()
        cursor.close()

        return records

    def _get_ili2db_names(self):
        dict_names = dict()
        # Custom names
        dict_names[T_ID_KEY] = "T_Id"
        dict_names[T_ILI_TID_KEY] = "T_Ili_Tid"
        dict_names[DISPLAY_NAME_KEY] = "dispName"
        dict_names[ILICODE_KEY] = "iliCode"
        dict_names[DESCRIPTION_KEY] = "description"
        dict_names[T_BASKET_KEY] = "T_basket"
        dict_names[T_ILI2DB_BASKET_KEY] = "T_ILI2DB_BASKET"
        dict_names[T_ILI2DB_DATASET_KEY] = "T_ILI2DB_DATASET"
        dict_names[DATASET_T_DATASETNAME_KEY] = "datasetName"
        dict_names[BASKET_T_DATASET_KEY] = "dataset"
        dict_names[BASKET_T_TOPIC_KEY] = "topic"
        dict_names[BASKET_T_ATTACHMENT_KEY] = "attachmentKey"

        return dict_names

    def _metadata_exists(self):
        if self.conn is None:
            res, msg = self.open_connection()
            if not res:
                self.logger.warning_msg(__name__, msg)
                return False

        cursor = self.conn.cursor()
        cursor.execute("""SELECT * from pragma_table_info('{}');""".format(ILI2DBNames.INTERLIS_TEST_METADATA_TABLE_PG))

        return bool(cursor.fetchall())

    def get_uri_for_layer(self, layer_name):
        return (True, '{uri}|layername={table}'.format(
                uri=self._uri,
                table=layer_name.lower()
            ))

    def get_ladm_units(self):
        if self.conn is None:
            res, msg = self.open_connection()
            if not res:
                self.logger.warning_msg(__name__, msg)
                return dict()

        cursor = self.conn.cursor()
        result = cursor.execute("""SELECT DISTINCT tablename || '..' || columnname AS unit_key, ' [' || setting || ']' AS unit_value FROM t_ili2db_column_prop WHERE tag LIKE 'ch.ehi.ili2db.unit'""")
        dict_units = dict()
        if result is not None:
            for unit in result:
                dict_units[unit['unit_key']] = unit['unit_value']
        #self.logger.debug(__name__, "Units found: {}".format(dict_units))
        return dict_units

    def get_models(self):
        if self.conn is None:
            res, msg = self.open_connection()
            if not res:
                self.logger.warning_msg(__name__, msg)
                return list()

        cursor = self.conn.cursor()
        result = cursor.execute("""SELECT distinct substr(iliname, 1, pos-1) AS modelname from 
                                    (SELECT *, instr(iliname,'.') AS pos FROM t_ili2db_trafo)""")
        lst_models = list()
        if result is not None:
            lst_models = [db_model['modelname'] for db_model in result]
        self.logger.debug(__name__, "Models found: {}".format(lst_models))
        return lst_models

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
        if os.path.exists(self._uri) and os.path.isfile(self._uri):
            self.conn = qgis.utils.spatialite_connect(self._uri)
            self.conn.row_factory = sqlite3.Row
            return (True, QCoreApplication.translate("GPKGConnector", "Connection is open!"))
        elif not os.path.exists(self._uri):
            return (False, QCoreApplication.translate("GPKGConnector",
                           "Connection could not be open! The file ('{}') does not exist!".format(self._uri)))
        elif os.path.isdir(self._uri):
            return (False, QCoreApplication.translate("GPKGConnector",
                                                      "Connection could not be open! The URI ('{}') is not a file!".format(
                                                          self._uri)))

    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.logger.info(__name__, "Connection was closed!")
            self.conn = None

    def get_ili2db_version(self):
        if self.conn is None:
            res, msg = self.open_connection()
            if not res:
                self.logger.warning_msg(__name__, msg)
                return -1

        cur = self.conn.cursor()
        cur.execute("""SELECT * from pragma_table_info('t_ili2db_attrname') WHERE name='owner';""")
        if cur.fetchall():
            return 3
        else:
            return 4  # ili2db 4 renamed such column to ColOwner

    def _test_db_file(self, is_schema_import=False):
        uri = self._uri

        # The most basic check first :)
        if not os.path.splitext(uri)[1] == ".gpkg":
            return False, EnumTestConnectionMsg.WRONG_FILE_EXTENSION, QCoreApplication.translate("GPKGConnector",
                                                                                                 "The file should have the '.gpkg' extension!")

        # First we do a very basic check, looking that the directory or file exists
        if is_schema_import:
            # file does not exist, but directory must exist
            directory = os.path.dirname(uri)

            if not os.path.exists(directory):
                return False, EnumTestConnectionMsg.DIR_NOT_FOUND, QCoreApplication.translate("GPKGConnector",
                                                                                              "GeoPackage directory not found.")
        else:
            if not os.path.exists(uri):
                return False, EnumTestConnectionMsg.GPKG_FILE_NOT_FOUND, QCoreApplication.translate("GPKGConnector",
                                                                                                    "GeoPackage file not found.")

        return True, EnumTestConnectionMsg.CONNECTION_TO_SERVER_SUCCESSFUL, QCoreApplication.translate(
            "GPKGConnector",
            "Connection to server was successful.")

    def _test_connection_to_db(self):
        res, msg = self.open_connection()
        if res:
            return True, EnumTestConnectionMsg.CONNECTION_TO_DB_SUCCESSFUL, QCoreApplication.translate(
                "GPKGConnector",
                "Connection to db was successful.")
        else:
            return False, EnumTestConnectionMsg.CONNECTION_COULD_NOT_BE_OPEN, msg

    def _test_connection_to_ladm(self, required_models):
        database = os.path.basename(self._dict_conn_params['dbfile'])
        if not self._metadata_exists():
            return False, EnumTestConnectionMsg.INTERLIS_META_ATTRIBUTES_NOT_FOUND, QCoreApplication.translate(
                "GPKGConnector",
                "The database '{}' is not a valid LADM-COL database. That is, the database doesn't have the structure of the LADM-COL model.").format(
                database)

        if self.get_ili2db_version() != 4:
            return False, EnumTestConnectionMsg.INVALID_ILI2DB_VERSION, QCoreApplication.translate("GPKGConnector",
                                                                                                   "The database '{}' was created with an old version of ili2db (v3), which is no longer supported. You need to migrate it to ili2db4.").format(
                database)

        if self.model_parser is None:
            self.model_parser = ModelParser(self)

        res, code, msg = self.check_db_models(required_models)
        if not res:
            return res, code, msg

        # Validate table and field names
        if self._should_update_db_mapping_values:
            self._initialize_names()

        res, msg = self.names.test_names(self._get_flat_table_and_field_names_for_testing_names())
        if not res:
            return False, EnumTestConnectionMsg.DB_NAMES_INCOMPLETE, QCoreApplication.translate("PGConnector",
                                                                                                "Table/field names from the DB are not correct. Details: {}.").format(
                msg)

        return True, EnumTestConnectionMsg.DB_WITH_VALID_LADM_COL_STRUCTURE, QCoreApplication.translate("GPKGConnector",
                                                                                                    "The database '{}' has a valid LADM-COL structure!").format(database)

    def execute_sql_query(self, query):
        """
        Generic function for executing SQL statements

        :param query: SQL Statement
        :return: List of RealDictRow
        """
        cursor = self.conn.cursor()

        try:
            cursor.execute(query)
            return True, cursor.fetchall()
        except sqlite3.ProgrammingError as e:
            return False, e

    def get_qgis_layer_uri(self, table_name):
        data_source_uri = '{uri}|layername={table}'.format(
            uri=self.uri,
            table=table_name
        )
        return data_source_uri
