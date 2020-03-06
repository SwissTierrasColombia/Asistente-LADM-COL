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

from asistente_ladm_col.config.enums import (EnumTestLevel,
                                             EnumUserLevel,
                                             EnumTestConnectionMsg)
from asistente_ladm_col.config.mapping_config import (T_ID_KEY,
                                                      DISPLAY_NAME_KEY,
                                                      ILICODE_KEY,
                                                      DESCRIPTION_KEY,
                                                      QueryNames,
                                                      LADMNames)
from asistente_ladm_col.lib.db.db_connector import (DBConnector,
                                                    COMPOSED_KEY_SEPARATOR)
from asistente_ladm_col.utils.model_parser import ModelParser
from asistente_ladm_col.utils.utils import normalize_iliname


class GPKGConnector(DBConnector):

    _PROVIDER_NAME = 'ogr'
    _DEFAULT_VALUES = {
        'dbfile': ''
    }

    def __init__(self, uri, conn_dict={}):
        DBConnector.__init__(self, uri, conn_dict)
        self.engine = 'gpkg'
        self.conn = None
        self.provider = 'ogr'

    @DBConnector.uri.setter
    def uri(self, value):
        self._dict_conn_params = {'dbfile': value}
        self._uri = value

    def test_connection(self, test_level=EnumTestLevel.LADM, user_level=EnumUserLevel.CREATE):
        """
        WARNING: We check several levels in order:
            1. SERVER
            2. DB
            #  We don't check SCHEMAs for GPKG
            3. LADM
            4. SCHEMA_IMPORT
          If you need to modify this method, be careful and preserve the order!!!

        :param test_level: (EnumTestLevel) level of connection with postgres
        :param user_level: (EnumUserLevel) level of permissions a user has
        :return Triple: boolean result, message code, message text
        """
        uri = self._uri
        database = os.path.basename(self._dict_conn_params['dbfile'])

        # The most basic check first :)
        if not os.path.splitext(uri)[1] == ".gpkg":
            return False, EnumTestConnectionMsg.WRONG_FILE_EXTENSION, QCoreApplication.translate("GPKGConnector",
                                                                                                 "The file should have the '.gpkg' extension!")

        # First we do a very basic check, looking that the directory or file exists
        if test_level & EnumTestLevel.SCHEMA_IMPORT:
            # file does not exist, but directory must exist
            directory = os.path.dirname(uri)

            if not os.path.exists(directory):
                return False, EnumTestConnectionMsg.DIR_NOT_FOUND, QCoreApplication.translate("GPKGConnector",
                                                                                              "GeoPackage directory not found.")
        else:
            if not os.path.exists(uri):
                return False, EnumTestConnectionMsg.GPKG_FILE_NOT_FOUND, QCoreApplication.translate("GPKGConnector",
                                                                                                    "GeoPackage file not found.")

        # Now we can proceed in the order given in the docs
        if test_level & EnumTestLevel.SERVER:
            uri = self.get_connection_uri(self._dict_conn_params, 0)
            res, msg = self.open_connection()
            if res:
                return True, EnumTestConnectionMsg.CONNECTION_TO_SERVER_SUCCESSFUL, QCoreApplication.translate(
                    "GPKGConnector",
                    "Connection to server was successful.")
            else:
                return False, EnumTestConnectionMsg.CONNECTION_TO_SERVER_FAILED, msg

        if test_level == EnumTestLevel.DB:  # Just in the DB case
            return True, EnumTestConnectionMsg.CONNECTION_TO_DB_SUCCESSFUL, QCoreApplication.translate("GPKGConnector",
                                                                                                       "Connection to the database was successful.")

        if test_level & EnumTestLevel.SCHEMA_IMPORT:
            return True, EnumTestConnectionMsg.CONNECTION_TO_DB_SUCCESSFUL_NO_LADM_COL, QCoreApplication.translate(
                "PGConnector", "Connection successful!")

        if self.conn is None:
            res, msg = self.open_connection()
            if not res:
                return res, EnumTestConnectionMsg.CONNECTION_COULD_NOT_BE_OPEN, msg

        #  No schemas in GPKG, skipping EnumTestLevel.CHECK_SCHEMA

        if test_level == EnumTestLevel.DB_SCHEMA:  # Test connection stops here
            return True, EnumTestConnectionMsg.CONNECTION_TO_DB_SUCCESSFUL, QCoreApplication.translate("GPKGConnector",
                                                                                                       "Connection to the database was successful.")

        if test_level & EnumTestLevel._CHECK_LADM:
            if not self._metadata_exists():
                return False, EnumTestConnectionMsg.INTERLIS_META_ATTRIBUTES_NOT_FOUND, QCoreApplication.translate(
                    "GPKGConnector",
                    "The database '{}' is not a valid LADM_COL database. That is, the database doesn't have the structure of the LADM_COL model.").format(
                    database)

            if self.get_ili2db_version() != 4:
                return False, EnumTestConnectionMsg.INVALID_ILI2DB_VERSION, QCoreApplication.translate("GPKGConnector",
                                                                                                       "The database '{}' was created with an old version of ili2db (v3), which is no longer supported. You need to migrate it to ili2db4.").format(
                    database)


            res, msg = self.check_at_least_one_ladm_model_exists()
            if not res:
                return res, EnumTestConnectionMsg.NO_LADM_MODELS_FOUND, msg  # No LADM model found

            if self.model_parser is None:
                self.model_parser = ModelParser(self)

            # Validate table and field names
            if not self._table_and_field_names:
                self._initialize_names()

            models = list()
            if self.ladm_model_exists():
                models.append(LADMNames.LADM_MODEL_PREFIX)
            if self.operation_model_exists():
                models.append(LADMNames.OPERATION_MODEL_PREFIX)
            if self.cadastral_form_model_exists():
                models.append(LADMNames.CADASTRAL_FORM_MODEL_PREFIX)
            if self.valuation_model_exists():
                models.append(LADMNames.VALUATION_MODEL_PREFIX)
            if self.ant_model_exists():
                models.append(LADMNames.ANT_MODEL_PREFIX)
            if self.reference_cartography_model_exists():
                models.append(LADMNames.REFERENCE_CARTOGRAPHY_PREFIX)
            if self.snr_data_model_exists():
                models.append(LADMNames.SNR_DATA_MODEL_PREFIX)
            if self.supplies_integration_model_exists():
                models.append(LADMNames.SUPPLIES_INTEGRATION_MODEL_PREFIX)
            if self.supplies_model_exists():
                models.append(LADMNames.SUPPLIES_MODEL_PREFIX)

            if not models:
                return False, EnumTestConnectionMsg.NO_LADM_MODELS_FOUND, QCoreApplication.translate("GPKGConnector",
                                                                                                     "The database has no models from LADM_COL! As is, it cannot be used for LADM_COL Assistant!")

            res, msg = self.names.test_names(self._table_and_field_names)
            if not res:
                return False, EnumTestConnectionMsg.DB_NAMES_INCOMPLETE, QCoreApplication.translate("PGConnector",
                                                                                                    "Table/field names from the DB are not correct. Details: {}.").format(
                    msg)

        if test_level == EnumTestLevel.LADM:
            return True, EnumTestConnectionMsg.DB_WITH_VALID_LADM_COL_STRUCTURE, QCoreApplication.translate("GPKGConnector", "The database '{}' has a valid LADM_COL structure!").format(
                database)

        return False, EnumTestConnectionMsg.UNKNOWN_CONNECTION_ERROR, QCoreApplication.translate("GPKGConnector",
                                                                                                 "There was a problem checking the connection. Most likely due to invalid or not supported test_level!")

    def get_table_and_field_names(self):
        """
        Documented in super class
        """
        dict_names = dict()
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

        for record in records:
            if record[QueryNames.TABLE_ILINAME] is None:
                # Either t_ili2db_* tables (INTERLIS meta-attrs)
                continue

            table_iliname = normalize_iliname(record[QueryNames.TABLE_ILINAME])

            if not table_iliname in dict_names:
                dict_names[table_iliname] = dict()
                dict_names[table_iliname][QueryNames.TABLE_NAME] = record[QueryNames.TABLE_NAME]

            if record[QueryNames.FIELD_ILINAME] is None:
                # Fields for domains, like 'description' (we map it in a custom way later in this class method)
                continue

            field_iliname = normalize_iliname(record[QueryNames.FIELD_ILINAME])
            dict_names[table_iliname][field_iliname] = record[QueryNames.FIELD_NAME]

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

        for record in records:
            composed_key = "{}{}{}".format(normalize_iliname(record['iliname']),
                                           COMPOSED_KEY_SEPARATOR,
                                           normalize_iliname(record['iliname2']))
            table_iliname = normalize_iliname(record[QueryNames.TABLE_ILINAME])
            if table_iliname in dict_names:
                dict_names[table_iliname][composed_key] = record['sqlname']
            else:
                colowner = normalize_iliname(record['colowner'])
                if colowner in dict_names:
                    dict_names[colowner][composed_key] = record['sqlname']

        cursor.close()

        # Custom names
        dict_names[T_ID_KEY] = "T_Id"
        dict_names[DISPLAY_NAME_KEY] = "dispName"
        dict_names[ILICODE_KEY] = "iliCode"
        dict_names[DESCRIPTION_KEY] = "description"

        return dict_names

    def _metadata_exists(self):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT * from pragma_table_info('{}');""".format(LADMNames.INTERLIS_TEST_METADATA_TABLE_PG))

        return bool(cursor.fetchall())

    def get_uri_for_layer(self, layer_name):
        return (True, '{uri}|layername={table}'.format(
                uri=self._uri,
                table=layer_name.lower()
            ))

    def get_ladm_units(self):
        cursor = self.conn.cursor()
        result = cursor.execute("""SELECT DISTINCT tablename || '..' || columnname AS unit_key, ' [' || setting || ']' AS unit_value FROM t_ili2db_column_prop WHERE tag LIKE 'ch.ehi.ili2db.unit'""")
        dict_units = dict()
        if result is not None:
            for unit in result:
                dict_units[unit['unit_key']] = unit['unit_value']
        #self.logger.debug(__name__, "Units found: {}".format(dict_units))
        return dict_units

    def get_models(self):
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
        if os.path.exists(self._uri):
            self.conn = qgis.utils.spatialite_connect(self._uri)
            self.conn.row_factory = sqlite3.Row
            return (True, QCoreApplication.translate("GPKGConnector", "Connection is open!"))
        else:
            return (False, QCoreApplication.translate("GPKGConnector",
                           "Connection could not be open! The file ('{}') does not exist!".format(self._uri)))

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

    def execute_sql_query(self, query):
        """
        Generic function for executing SQL statements
        :param query: SQL Statement
        :return: List of RealDictRow
        """
        # self.conn.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
        #self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()

        try:
            cursor.execute(query)
            return True, cursor.fetchall()
        except sqlite3.ProgrammingError as e:
            return False, e
