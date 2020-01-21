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
from asistente_ladm_col.config.general_config import (OPERATION_MODEL_PREFIX,
                                                      CADASTRAL_FORM_MODEL_PREFIX,
                                                      VALUATION_MODEL_PREFIX,
                                                      LADM_MODEL_PREFIX,
                                                      ANT_MODEL_PREFIX,
                                                      REFERENCE_CARTOGRAPHY_PREFIX,
                                                      SNR_DATA_MODEL_PREFIX,
                                                      SUPPLIES_INTEGRATION_MODEL_PREFIX,
                                                      SUPPLIES_MODEL_PREFIX, INTERLIS_TEST_METADATA_TABLE_PG)
from asistente_ladm_col.lib.db.db_connector import (DBConnector,
                                                    EnumTestLevel)
from asistente_ladm_col.utils.model_parser import ModelParser
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
        """
        WARNING: We check several levels in order:
            1. SERVER
            2. DB
            #  We don't check SCHEMAs for GPKG
            3. LADM
            4. SCHEMA_IMPORT
          If you need to modify this method, be careful and preserve the order!!!

        :param test_level: (EnumTestLevel) level of connection with postgres
        """
        uri = self._uri
        database = os.path.basename(self._dict_conn_params['dbfile'])

        # First we do a very basic check, looking that the directory or file exists
        if test_level & EnumTestLevel.SCHEMA_IMPORT:
            # file does not exist, but directory must exist
            directory = os.path.dirname(uri)

            if not os.path.exists(directory):
                return (False, QCoreApplication.translate("GPKGConnector", "GeoPackage directory file not found."))
        else:
            if not os.path.exists(uri):
                return (False, QCoreApplication.translate("GPKGConnector", "GeoPackage file not found."))

        # Now we can proceed in the order given in the docs
        if test_level & EnumTestLevel.SERVER:
            uri = self.get_connection_uri(self._dict_conn_params, 0)
            res, msg = self.open_connection()
            if res:
                return (True, QCoreApplication.translate("GPKGConnector",
                                                         "Connection to server was successful."))
            else:
                return (False, msg)

        if test_level == EnumTestLevel.DB:  # Just in the DB case
            return (True, QCoreApplication.translate("GPKGConnector",
                                                     "Connection to the database was successful."))

        if self.conn is None:
            res, msg = self.open_connection()
            if not res:
                return (res, msg)

        #  No schemas in GPKG, skipping EnumTestLevel.CHECK_SCHEMA

        if test_level == EnumTestLevel.DB_SCHEMA:  # Test connection stops here
            return (True, QCoreApplication.translate("GPKGConnector",
                                                     "Connection to the database was successful."))

        if test_level & EnumTestLevel._CHECK_LADM:
            if not self._metadata_exists():
                return (False, QCoreApplication.translate("GPKGConnector",
                                                          "The database '{}' is not a valid LADM_COL database. That is, the database doesn't have the structure of the LADM_COL model.").format(
                    database))

            if self.get_ili2db_version() != 4:
                return (False, QCoreApplication.translate("GPKGConnector",
                                                          "The database '{}' was created with an old version of ili2db (v3), which is no longer supported. You need to migrate it to ili2db4.").format(
                    database))


            res, msg = self.check_at_least_one_ladm_model_exists()
            if not res:
                return (res, msg)  # No LADM model found

            if self.model_parser is None:
                self.model_parser = ModelParser(self)

            # Validate table and field names
            if not self._table_and_field_names:
                self._initialize_names()

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
                return (False, QCoreApplication.translate("GPKGConnector", "The database has no models from LADM_COL! As is, it cannot be used for LADM_COL Assistant!"))

            res, msg = self.names.test_names(self._table_and_field_names)
            if not res:
                return (False, QCoreApplication.translate("PGConnector",
                                                          "Table/field names from the DB are not correct. Details: {}.").format(
                    msg))

        if test_level == EnumTestLevel.LADM:
            return (True,
                    QCoreApplication.translate("GPKGConnector", "The database '{}' has a valid LADM_COL structure!").format(
                        database))

        # Next if captures and returns True on schema import
        if test_level & EnumTestLevel.SCHEMA_IMPORT:
            return (True, QCoreApplication.translate("PGConnector", "Connection successful!"))

        return (False, QCoreApplication.translate("GPKGConnector",
                                                  "There was a problem checking the connection. Most likely due to invalid or not supported test_level!"))

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
        cursor.execute("""SELECT rtrim(rtrim(a.iliname, replace(a.iliname, '.', '')), '.') as table_iliname,
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

    def _metadata_exists(self):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT * from pragma_table_info('{}');""".format(INTERLIS_TEST_METADATA_TABLE_PG))

        return bool(cursor.fetchall())

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
        if result is not None:
            lst_models = [db_model['modelname'] for db_model in result]
        self.logger.debug(__name__, "Models found: {}".format(lst_models))
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
        #if os.path.exists(self._uri):
        self.conn = qgis.utils.spatialite_connect(self._uri)
        self.conn.row_factory = sqlite3.Row
        return (True, QCoreApplication.translate("GPKGConnector", "Connection is open!"))
        #else:
        #    return (False, QCoreApplication.translate("GPKGConnector",
        #                   "Connection could not be open! The file ('{}') does not exist!".format(self._uri)))

    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.logger.info(__name__, "Connection was closed!")
            self.conn = None

    def get_ili2db_version(self):
        cur = self.conn.cursor()
        cur.execute("""SELECT * from pragma_table_info('t_ili2db_attrname') WHERE name='owner';""")
        if cur.fetchall():
            return 3
        else:
            return 4  # ili2db 4 renamed such column to ColOwner