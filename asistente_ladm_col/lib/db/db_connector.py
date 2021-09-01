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

from asistente_ladm_col.config.keys.ili2db_keys import ILI2DB_SCHEMAIMPORT, ILI2DB_CREATE_BASKET_COL_KEY
from asistente_ladm_col.lib.model_registry import LADMColModelRegistry

from qgis.PyQt.QtCore import QObject

from asistente_ladm_col.config.enums import (EnumTestLevel,
                                             EnumUserLevel,
                                             EnumTestConnectionMsg)
from asistente_ladm_col.config.keys.common import (REQUIRED_MODELS,
                                                   ROLE_HIDDEN_MODELS,
                                                   ROLE_SUPPORTED_MODELS)
from asistente_ladm_col.config.query_names import QueryNames
from asistente_ladm_col.core.model_parser import ModelParser
from asistente_ladm_col.core.db_mapping_registry import DBMappingRegistry
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
        self.names = DBMappingRegistry()
        self.__db_mapping = None  # To cache query response from the DB getting table and field names.

        # Flag to control whether the DB connector should update the name registry. It should be True in two scenarios:
        # 1) when the DB connector is created, and 2) when the plugin's active role has changed.
        self._should_update_db_mapping_values = True

        # Model parser instance. If it's None, it will be recreated.
        # The ModelParser compares DB models vs. role supported models.
        # It should be set to None in two scenarios:
        # 1) when the DB connector is created, and 2) when the plugin's active role has changed.
        self._model_parser = None

        if uri is not None:
            self.uri = uri
        else:
            self.dict_conn_params = conn_dict

        self.__ladmcol_models = LADMColModelRegistry()

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

    def _table_exists(self, table_name):
        raise NotImplementedError

    def _metadata_exists(self):
        raise NotImplementedError

    def _has_basket_col(self):
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

    def reset_db_model_parser(self):
        """
        Call it to let the connector know it has to update the DB model parser (e.g.,
        when the active role has changed, since the new one could support other models).
        """
        self._model_parser = None

    def read_model_parser(self):
        if self._model_parser is None:
            try:
                self._model_parser = ModelParser(self)
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

    def get_db_mapping(self):
        """
        Cache the get_db_mapping call, which should be called only once per db connector.

        :return: A dict with table ilinames as keys and dict as values. See __get_db_mapping for details.
        """
        if not self.__db_mapping:
            self.__db_mapping = self.__get_db_mapping()

        return self.__db_mapping

    def __get_db_mapping(self):
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

        dict_names.update(self._get_ili2db_names())  # Now add ili2db names like t_id, t_ili_id, t_basket, etc.

        return dict_names

    def _get_table_and_field_names(self):
        """Gets both table and field names from DB. Only includes field names that are not FKs.

        Execute below Sql statement (pseudo-SQL):
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

    def _get_ili2db_names(self):
        """Returns field common names of databases, e.g., T_Id, T_Ili_Tid, dispName, t_basket, etc.

        :return: Dictionary with ili2db keys:
                 T_ID_KEY, T_ILI_TID_KEY, etc., from db_mapping_registry
        """
        raise NotImplementedError

    def _initialize_names(self):
        """
        Gets table and field names from the DB and initializes the db mapping values in the registry.

        Could be called more than once per connector, namely, when the role changes, the db mapping registry values
        should be updated.
        """
        self.logger.info(__name__, "Resetting db mapping registry values from the DB!")
        self.names.initialize_table_and_field_names(self.get_db_mapping(), self.get_models())
        self._should_update_db_mapping_values = False  # Since we just updated, avoid it for the next test_connection.

        # self.logger.debug(__name__, "DEBUG DICT: {}".format(dict_names["Operacion.Operacion.OP_Derecho"]))

    def reset_db_mapping_values(self):
        """
        Call it to let the connector know it has to update the DB mapping values in the DB Mapping Registry (e.g., when
        the active role has changed, since the new one could support other models).
        """
        self._should_update_db_mapping_values = True

    def check_db_models(self, models):
        code = EnumTestConnectionMsg.DB_MODELS_ARE_CORRECT

        if models.get(REQUIRED_MODELS):
            res, msg = self.check_required_models(models[REQUIRED_MODELS])
            if not res:
                code = EnumTestConnectionMsg.REQUIRED_LADM_MODELS_NOT_FOUND
        else:
            # 2 options here: if models has info, we test against such info, but if not,
            # we test against the info from model parser. In both scenarios, we test that
            # all hidden (base) models are in the DB and that at least one of the non-hidden
            # models is present in the DB.
            res, msg = self.at_least_one_ladm_col_model_exists(models)
            if not res:
                code = EnumTestConnectionMsg.NO_LADM_MODELS_FOUND_IN_SUPPORTED_VERSION

        return res, code, msg

    def check_required_models(self, models):
        msg = QCoreApplication.translate("DBConnector", "All required models are in the DB!")

        not_found = [model for model in models if not self.ladm_col_model_exists(model)]

        if not_found:
            msg = QCoreApplication.translate("DBConnector",
                                             "The following required model(s) could not be found in the DB: {}.").format(', '.join(not_found))

        return not bool(not_found), msg

    def at_least_one_ladm_col_model_exists(self, models):
        if self.read_model_parser():
            if models.get(ROLE_SUPPORTED_MODELS) and models.get(ROLE_HIDDEN_MODELS):
                # We won't test against model registry (active role), but only against info in models dict

                # All hidden models should exist in the DB
                not_found = [model for model in models[ROLE_HIDDEN_MODELS] if not self.ladm_col_model_exists(model)]
                if not_found:
                    return False, QCoreApplication.translate("DBConnector",
                                                             "The following required model(s) could not be found in the DB: '{}'.").format(', '.join(not_found))

                # At least one non-hidden model should exist in the DB
                non_hidden_models = [model for model in models[ROLE_SUPPORTED_MODELS] if model not in models[ROLE_HIDDEN_MODELS]]
                found = [model for model in non_hidden_models if self.ladm_col_model_exists(model)]
                if not found:
                    return False, QCoreApplication.translate("DBConnector",
                                                             "At least one of the following required model(s) should exist in the DB: '{}'. Your DB has '{}'.").format(
                        ', '.join(non_hidden_models),
                        ', '.join(self.get_models()))
            else:
                # Go to the model_parser, which deals with model_registry and will use info from the active role.
                msg = ''
                res = self._model_parser.at_least_one_ladm_col_model_exists()

                if not res:
                    msg = QCoreApplication.translate("DBConnector",
                                                     "At least one LADM-COL model should exist in the required version (besides the basic ones: '{}')! Supported models are: '{}', but your DB has '{}'").format(
                        ', '.join([m.full_name() for m in self.__ladmcol_models.hidden_and_supported_models()]),
                        ', '.join([m.full_name() for m in self.__ladmcol_models.supported_models()]),
                        ', '.join(self.get_models()))
                    return False, msg

            return True, ""

        return False, "Error getting the model parser!"

    def ladm_col_model_exists(self, model_prefix):
        if self.read_model_parser():
            return self._model_parser.ladm_col_model_exists(model_prefix)

        return False

    def survey_model_exists(self):
        if self.read_model_parser():
            return self._model_parser.survey_model_exists()

        return False

    def valuation_model_exists(self):
        if self.read_model_parser():
            return self._model_parser.valuation_model_exists()

        return False

    def ladm_model_exists(self):
        if self.read_model_parser():
            return self._model_parser.ladm_model_exists()

        return False

    def cadastral_cartography_model_exists(self):
        if self.read_model_parser():
            return self._model_parser.cadastral_cartography_model_exists()

        return False

    def snr_data_model_exists(self):
        if self.read_model_parser():
            return self._model_parser.snr_data_model_exists()

        return False

    def supplies_integration_model_exists(self):
        if self.read_model_parser():
            return self._model_parser.supplies_integration_model_exists()

        return False

    def supplies_model_exists(self):
        if self.read_model_parser():
            return self._model_parser.supplies_model_exists()

        return False

    def open_connection(self):
        """
        :return: Whether the connection is opened after calling this method or not
        """
        raise NotImplementedError

    def test_connection(self, test_level=EnumTestLevel.LADM, user_level=EnumUserLevel.CONNECT, models={}):
        """
        'Template method' subclasses should overwrite it, proposing their own way to test a connection.
        """
        raise NotImplementedError

    def _test_connection_to_db(self):
        raise NotImplementedError

    def _test_connection_to_ladm(self, models):
        raise NotImplementedError

    def _db_should_have_basket_support(self):
        """
        :return: Tuple: Whether the current DB should have baskets or not, name of the 1st model that requires baskets!
        """
        # Get models in the DB that are supported and not hidden
        model_names_in_db = self.get_models()
        if model_names_in_db:
            for model in self.__ladmcol_models.supported_models():
                if not model.hidden() and model.full_name() in model_names_in_db:
                    params = model.get_ili2db_params()  # Note: params depend on the model and on the active role
                    if ILI2DB_SCHEMAIMPORT in params:
                        for param in params[ILI2DB_SCHEMAIMPORT]:  # List of tuples
                            if param[0] == ILI2DB_CREATE_BASKET_COL_KEY:  # param: (option, value)
                                self.logger.debug(__name__, "Model '{}' requires baskets...".format(model.alias()))
                                return True, model.alias()

        return False, ''

    @staticmethod
    def _parse_models_from_db_meta_attrs(lst_models):
        """
        Reads a list of models as saved by ili2db and  returns a dict of model dependencies.

        E.g.:
        INPUT-> ["D_G_C_V2_9_6{ LADM_COL_V1_2 ISO19107_PLANAS_V1} D_SNR_V2_9_6{ LADM_COL_V1_2} D_I_I_V2_9_6{ D_SNR_V2_9_6 D_G_C_V2_9_6}", "LADM_COL_V1_2"]
        OUTPUT-> {'D_G_C_V2_9_6': ['LADM_COL_V1_2', 'ISO19107_PLANAS_V1'], 'D_SNR_V2_9_6': ['LADM_COL_V1_2'], 'D_I_I_V2_9_6': ['D_SNR_V2_9_6', 'D_G_C_V2_9_6'], 'LADM_COL_V1_2': []}

        :param lst_models: The list of values stored in the DB meta attrs model table (column 'modelname').
        :return: Dict of model dependencies.
        """
        model_hierarchy = dict()
        for str_model in lst_models:
            parts = str_model.split("}")
            if len(parts) > 1:  # With dependencies
                for part in parts:
                    if part:  # The last element of parts is ''
                        model, dependencies = part.split("{")
                        model_hierarchy[model.strip()] = dependencies.strip().split(" ")
            elif len(parts) == 1:  # No dependencies
                model_hierarchy[parts[0].strip()] = list()

        return model_hierarchy


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

    def test_connection(self, test_level=EnumTestLevel.LADM, user_level=EnumUserLevel.CONNECT, models={}):
        """We check several levels in order:
            1. FILE SERVER (DB file)
            2. DB
            3. ili2db's SCHEMA_IMPORT
            4. LADM-COL

        Note that we don't check connection to SCHEMAs here.

        :param test_level: (EnumTestLevel) level of connection with postgres
        :param user_level: (EnumUserLevel) level of permissions a user has
        :param models: A dict of model prefixes that are required for this DB connection. If key is REQUIRED_MODELS,
                       models are mandatory, whereas if keys are ROLE_SUPPORTED_MODELS and ROLE_HIDDEN_MODELS, we test
                       the DB has at list all hidden (base) models and at least one non-hidden one.
        :return Triple: boolean result, message code, message text
        """
        is_schema_import = bool(test_level & EnumTestLevel.SCHEMA_IMPORT)
        res, code, msg = self._test_db_file(is_schema_import)
        if not res or test_level == EnumTestLevel.SERVER_OR_FILE or is_schema_import:
            return res, code, msg

        res, code, msg = self._test_connection_to_db()

        if not res or test_level == EnumTestLevel.DB or test_level == EnumTestLevel.DB_FILE:
            return res, code, msg

        res, code, msg = self._test_connection_to_ladm(models)

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

    def test_connection(self, test_level=EnumTestLevel.LADM, user_level=EnumUserLevel.CONNECT, models={}):
        """We check several levels in order:
            1. SERVER
            2. DB
            3. SCHEMA
            4. ili2db's SCHEMA_IMPORT
            5. LADM-COL

        :param test_level: (EnumTestLevel) level of connection with postgres
        :param user_level: (EnumUserLevel) level of permissions a user has
        :param models: A list of model prefixes that are required for this DB connection. If key is REQUIRED_MODELS,
                       models are mandatory, whereas if keys are ROLE_SUPPORTED_MODELS and ROLE_HIDDEN_MODELS, we test
                       the DB has at list all hidden (base) models and at least one non-hidden one.
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

        res, code, msg = self._test_connection_to_ladm(models)

        if not res or test_level == EnumTestLevel.LADM:
            return res, code, msg

        return False, EnumTestConnectionMsg.UNKNOWN_CONNECTION_ERROR, QCoreApplication.translate("ClientServerDB",
                                                                                                 "There was a problem checking the connection. Most likely due to invalid or not supported test_level!")
    def execute_sql_query(self, query):
        raise NotImplementedError

    def get_qgis_layer_uri(self, table_name):
        # Beware, this should be used only for geometryless layers. It was created to access ili2db metadata tables.
        raise NotImplementedError