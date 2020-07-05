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
from PyQt5.QtCore import QCoreApplication

from qgis.PyQt.QtCore import QObject

from asistente_ladm_col.core.model_parser import ModelParser
from asistente_ladm_col.config.enums import (EnumTestLevel,
                                             EnumUserLevel,
                                             EnumTestConnectionMsg)
from asistente_ladm_col.config.mapping_config import (TableAndFieldNames,
                                                      T_ID_KEY,
                                                      T_ILI_TID_KEY,
                                                      DISPLAY_NAME_KEY,
                                                      ILICODE_KEY,
                                                      DESCRIPTION_KEY)
from asistente_ladm_col.config.query_names import QueryNames
from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.utils import normalize_iliname

COMPOSED_KEY_SEPARATOR = ".."


class DBConnector(QObject):
    """
    Superclass for all DB connectors.
    """
    _DEFAULT_VALUES = dict()  # You should set it, so that testing empty parameters can be handled easily.

    def __init__(self, uri, conn_dict=dict()):
        QObject.__init__(self)
        self.logger = Logger()
        self.engine = ''
        self.provider = '' # QGIS provider name. e.g., postgres
        self._uri = None
        self.schema = None
        self.conn = None
        self._dict_conn_params = None
        self.names = TableAndFieldNames()
        self._table_and_field_names = list()  # Table/field names should be read only once per connector
        
        if uri is not None:
            self.uri = uri
        else:
            self.dict_conn_params = conn_dict

        self.model_parser = None

    @property
    def dict_conn_params(self):
        return self._dict_conn_params.copy()

    @dict_conn_params.setter
    def dict_conn_params(self, dict_values):
        dict_values = {k:v for k,v in dict_values.items() if v}  # To avoid empty values to overwrite default values
        self._dict_conn_params = self._DEFAULT_VALUES.copy()
        self._dict_conn_params.update(dict_values)
        self._uri = self.get_connection_uri(self._dict_conn_params, level=1)

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, value):
        raise NotImplementedError

    def equals(self, db):
        return self.dict_conn_params == db.dict_conn_params

    def _metadata_exists(self):
        raise NotImplementedError

    def close_connection(self):
        raise NotImplementedError

    def get_description(self):
        return "Current connection details: '{}' -> {} {}".format(
            self.engine,
            self._uri,
            'schema:{}'.format(self.schema) if self.schema else '')

    def get_ladm_units(self):
        raise NotImplementedError

    def get_models(self, schema=None):
        raise NotImplementedError

    def get_display_conn_string(self):
        # Do not use to connect to a DB, only for display purposes
        tmp_dict_conn_params = self._dict_conn_params.copy()
        if 'password' in tmp_dict_conn_params:
            del tmp_dict_conn_params['password']

        return ' '.join(["{}={}".format(k, v) for k, v in tmp_dict_conn_params.items()])

    def get_description_conn_string(self):
        raise NotImplementedError

    def get_connection_uri(self, dict_conn, level=1):
        """
        :param dict_conn: (dict) dictionary with the parameters to establish a connection
        :param level: (int) At what level the connection will be established
            0: server level
            1: database level
        :return: (str) string uri to establish a connection
        """
        raise NotImplementedError

    def survey_model_exists(self):
        if self.read_model_parser():
            return self.model_parser.survey_model_exists()

        return False

    def valuation_model_exists(self):
        if self.read_model_parser():
            return self.model_parser.valuation_model_exists()

        return False

    def ladm_model_exists(self):
        if self.read_model_parser():
            return self.model_parser.ladm_model_exists()

        return False

    def cadastral_cartography_model_exists(self):
        if self.read_model_parser():
            return self.model_parser.cadastral_cartography_model_exists()

        return False

    def snr_data_model_exists(self):
        if self.read_model_parser():
            return self.model_parser.snr_data_model_exists()

        return False

    def supplies_integration_model_exists(self):
        if self.read_model_parser():
            return self.model_parser.supplies_integration_model_exists()

        return False

    def supplies_model_exists(self):
        if self.read_model_parser():
            return self.model_parser.supplies_model_exists()

        return False

    def ladm_col_model_exists(self, model_prefix):
        if self.read_model_parser():
            return self.model_parser.ladm_col_model_exists(model_prefix)

        return False

    def at_least_one_ladm_col_model_exists(self):
        if self.read_model_parser():
            return self.model_parser.at_least_one_ladm_col_model_exists()

        return False

    def read_model_parser(self):
        if self.model_parser is None:
            try:
                self.model_parser = ModelParser(self)
            except psycopg2.ProgrammingError as e:
                # if it is not possible to access the schema due to lack of privileges
                return False

        return True

    def is_ladm_layer(self, layer):
        raise NotImplementedError

    def get_ladm_layer_name(self, layer, validate_is_ladm=False):
        raise NotImplementedError

    def get_ili2db_version(self):
        raise NotImplementedError

    def get_table_and_field_names(self):  # TODO: Add test
        """
        Get table and field names from the DB. Should be called only once for a single connection.

        :return: dict with table ilinames as keys and dict as values. The dicts found in the value contain field
                 ilinames as keys and sqlnames as values. The table name itself is added with the key 'table_name'.
                 Example:

            "LADM_COL.LADM_Nucleo.col_masCcl": {
                'table_name': 'col_masccl',
                'LADM_COL.LADM_Nucleo.col_masCcl.ccl_mas..Levantamiento_Catastral.Levantamiento_Catastral.LC_Lindero': 'ccl_mas',
                'LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Levantamiento_Catastral.Levantamiento_Catastral.LC_Construccion': 'ue_mas_lc_construccion',
                'LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Levantamiento_Catastral.Levantamiento_Catastral.LC_ServidumbreTransito': 'ue_mas_lc_servidumbretransito',
                'LADM_COL.LADM_Nucleo.col_masCcl.another_ili_attr': 'corresponding_sql_name'
            }
        """
        # Get both table and field names. Only include field names that are not FKs, they will be added in a second step
        records = self._get_table_and_field_names()

        dict_names = dict()
        for record in records:
            if record[QueryNames.TABLE_ILINAME] is None:
                # Any t_ili2db_* tables (INTERLIS meta-attrs)
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
        # Spatial_Unit-->Ext_Address_ID (Ext_Address)
        #   Key: "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID"
        #   Values: lc_construccion_ext_direccion_id and  lc_terreno_ext_direccion_id
        records = self._get_fk_fields()
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

        dict_names.update(self._get_common_db_names())

        return dict_names

    def _get_table_and_field_names(self):
        """Gets both table and field names from DB. Only includes field names that are not FKs.

        Execute below Sql statement (seudo-SQL):
        SELECT
          IliName AS {QueryNames.TABLE_ILINAME}, -- (1)
          table_name AS {QueryNames.TABLE_NAME}, -- (2)
          IliName AS {QueryNames.FIELD_ILINAME}, -- (3)
          SqlName AS {QueryNames.FIELD_NAME}     -- (4)
        FROM Dbms_tbl_metadata INNER JOIN T_ILI2DB_CLASSNAME LEFT JOIN T_ILI2DB_ATTRNAME
        WHERE ilicol.Target IS NULL (because it does not include FKs)

        *Dbms_tbl_metadata="Metadata table of specific DBMS"

        +-----------------+       +------------------+       +-----------------+
        |Dbms_tbl_metadata|       |T_ILI2DB_CLASSNAME|       |T_ILI2DB_ATTRNAME|
        |-----------------|       |------------------|       |-----------------|
        |table_name (2)+  +---+   |IliName   (1)     |       |IliName   (3)    |
        +--------------|--+   +---+SqlName           |       |SqlName   (4)    |
                       |          +------------------+   +---+ColOwner         |
                       |                                 |   |Target           |
                       +---------------------------------+   +-----------------+

        :return: dict
        """
        raise NotImplementedError

    def _get_fk_fields(self):
        """Maps FK ilinames (i.e., those whose t_ili2db_attrname target column is not NULL)

        i.e.
        Spatial_Unit-->Ext_Address_ID (Ext_Address)
        Key: "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID"
        Values: lc_construccion_ext_direccion_id and  lc_terreno_ext_direccion_id

        Execute below Sql statement (seudo-SQL):
        SELECT  "iliname before the last point" as QueryNames.TABLE_ILINAME,
          iliname, -- (2)
          sqlname, -- (3)
          iliname as iliname2, (4)
          iliname as colowner
        FROM T_ILI2DB_CLASSNAME AS main_class INNER_JOIN T_ILI2DB_ATTRNAME INNER JOIN T_ILI2DB_CLASSNAME as target class

        +------------------+     +-----------------+     +------------------+
        |T_ILI2DB_CLASSNAME|     |T_ILI2DB_ATTRNAME|     |T_ILI2DB_CLASSNAME|
        |   (main class)   |     |-----------------|     |  (target class)  |
        |------------------|     |IliName   (1,2)  |     |------------------|
        |IliName   (5)     |     |SqlName   (3)    |     |IliName           |
        |SqlName    <------------+ColOwner         |  +-->SqlName    (4)    |
        +------------------+     |Target       +------+  +------------------+
                                 +-----------------+
        :return: dict
        """
        raise NotImplementedError

    def _get_common_db_names(self):
        """Returns field common names of databases. T_Id, T_Ili_Tid, dispName, iliCode and description.

        :return: Dictionary with the next keys:
                 T_ID_KEY, T_ILI_TID_KEY, DISPLAY_NAME_KEY, ILICODE_KEY, and DESCRIPTION_KEY from mapping_config.py file
        """
        raise NotImplementedError

    def _initialize_names(self):
        """
        Gets table and field names from the DB, initializes Names() and sets the member list for table and field names.
        Should be called only once per DB connector.
        """
        dict_names = self.get_table_and_field_names()
        self.names.initialize_table_and_field_names(dict_names)
        self._set_table_and_field_names_list(dict_names)

        # self.logger.debug(__name__, "DEBUG DICT: {}".format(dict_names["Operacion.Operacion.OP_Derecho"]))

    def _set_table_and_field_names_list(self, dict_names):
        """
        Fill table_and_field_names list.
        :param dict_names: See docs in _get_table_and_field_names
        """
        # Fill table names
        for k,v in dict_names.items():
            if k not in [T_ID_KEY, T_ILI_TID_KEY, DISPLAY_NAME_KEY, ILICODE_KEY, DESCRIPTION_KEY]:  # Custom names will be handled by Names class
                self._table_and_field_names.append(k)  # Table names
                for k1, v1 in v.items():
                    if k1 != QueryNames.TABLE_NAME:
                        self._table_and_field_names.append(k1)  # Field names

    def check_db_models(self, required_models):
        res = True
        code = EnumTestConnectionMsg.DB_MODELS_ARE_CORRECT
        msg = ""

        if required_models:
            res, msg = self.check_required_models(required_models)
            if not res:
                code = EnumTestConnectionMsg.REQUIRED_LADM_MODELS_NOT_FOUND
        else:
            res = self.at_least_one_ladm_col_model_exists()
            if not res:
                code = EnumTestConnectionMsg.NO_LADM_MODELS_FOUND_IN_SUPPORTED_VERSION
                msg = QCoreApplication.translate("DBConnector",
                            "At least one LADM-COL model should exist in the required version! Supported models are: '{}', but you have '{}'").format(
                                ', '.join(LADMNames.SUPPORTED_MODELS), ', '.join(self.get_models()))

        return res, code, msg

    def check_required_models(self, models):
        msg = QCoreApplication.translate("DBConnector", "All required models are in the DB!")

        not_found = [model for model in models if not self.ladm_col_model_exists(model)]

        if not_found:
            msg = QCoreApplication.translate("SettingsDialog",
                                             "The following required model(s) could not be found in the DB: {}.").format(', '.join(not_found))

        return not bool(not_found), msg

    def open_connection(self):
        """
        :return: Whether the connection is opened after calling this method or not
        """
        raise NotImplementedError

    def test_connection(self, test_level=EnumTestLevel.LADM, user_level=EnumUserLevel.CREATE, required_models=[]):
        """
        'Template method' subclasses should overwrite it, proposing their own way to test a connection.
        """
        raise NotImplementedError

    def _test_connection_to_db(self):
        raise NotImplementedError

    def _test_connection_to_ladm(self, required_models):
        raise NotImplementedError


class FileDB(DBConnector):
    """
    DB engines consisting of a single file, like GeoPackage, should inherit from this class.
    """
    def _test_db_file(self, is_schema_import=False):
        """
        Checks that the db file is accessible. Subclasses might use the is_schema_import parameter to know how far they
        should check. For instance, a DB file might not exist before a SCHEMA IMPORT operation.

        :param is_schema_import: boolean to indicate whether the tests is for a schema_import operation or not
        :return: boolean, was the connection successful?
        """
        raise NotImplementedError

    def test_connection(self, test_level=EnumTestLevel.LADM, user_level=EnumUserLevel.CREATE, required_models=[]):
        """We check several levels in order:
            1. FILE SERVER (DB file)
            2. DB
            3. ili2db's SCHEMA_IMPORT
            4. LADM-COL

        Note that we don't check connection to SCHEMAs here.

        :param test_level: (EnumTestLevel) level of connection with postgres
        :param user_level: (EnumUserLevel) level of permissions a user has
        :param required_models: A list of model prefixes that are mandatory for this DB connection
        :return Triple: boolean result, message code, message text
        """
        is_schema_import = bool(test_level & EnumTestLevel.SCHEMA_IMPORT)
        res, code, msg = self._test_db_file(is_schema_import)
        if not res or test_level == EnumTestLevel.SERVER_OR_FILE or is_schema_import:
            return res, code, msg

        res, code, msg = self._test_connection_to_db()

        if not res or test_level == EnumTestLevel.DB or test_level == EnumTestLevel.DB_FILE:
            return res, code, msg

        res, code, msg = self._test_connection_to_ladm(required_models)

        if not res or test_level == EnumTestLevel.LADM:
            return res, code, msg

        return False, EnumTestConnectionMsg.UNKNOWN_CONNECTION_ERROR, QCoreApplication.translate("FileDB",
                                                                                                 "There was a problem checking the connection. Most likely due to invalid or not supported test_level!")


class ClientServerDB(DBConnector):
    """
    DB engines consisting of client-server connections, like PostgreSQL, should inherit from this class.
    """
    def _test_connection_to_server(self):
        raise NotImplementedError

    def _test_connection_to_schema(self, user_level):
        raise NotImplementedError

    def test_connection(self, test_level=EnumTestLevel.LADM, user_level=EnumUserLevel.CREATE, required_models=[]):
        """We check several levels in order:
            1. SERVER
            2. DB
            3. SCHEMA
            4. ili2db's SCHEMA_IMPORT
            5. LADM-COL

        :param test_level: (EnumTestLevel) level of connection with postgres
        :param user_level: (EnumUserLevel) level of permissions a user has
        :param required_models: A list of model prefixes that are mandatory for this DB connection
        :return Triple: boolean result, message code, message text
        """
        if test_level == EnumTestLevel.SERVER_OR_FILE:
            return self._test_connection_to_server()

        res, code, msg = self._test_connection_to_db()

        if not res or test_level == EnumTestLevel.DB:
            return res, code, msg

        res, code, msg = self._test_connection_to_schema(user_level)

        if test_level & EnumTestLevel.SCHEMA_IMPORT:
            return True, EnumTestConnectionMsg.CONNECTION_TO_DB_SUCCESSFUL_NO_LADM_COL, QCoreApplication.translate("ClientServerDB", "Connection successful!")

        if not res or test_level == EnumTestLevel.DB_SCHEMA:
            return res, code, msg

        res, code, msg = self._test_connection_to_ladm(required_models)

        if not res or test_level == EnumTestLevel.LADM:
            return res, code, msg

        return False, EnumTestConnectionMsg.UNKNOWN_CONNECTION_ERROR, QCoreApplication.translate("ClientServerDB",
                                                                                                 "There was a problem checking the connection. Most likely due to invalid or not supported test_level!")
    def execute_sql_query(self, query):
        raise NotImplementedError
