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

from asistente_ladm_col.utils.model_parser import ModelParser
from asistente_ladm_col.config.enums import (EnumTestLevel,
                                             EnumUserLevel)
from asistente_ladm_col.config.mapping_config import (TableAndFieldNames,
                                                      QueryNames,
                                                      LADMNames,
                                                      T_ID_KEY,
                                                      DISPLAY_NAME_KEY,
                                                      ILICODE_KEY,
                                                      DESCRIPTION_KEY)
from asistente_ladm_col.lib.logger import Logger

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

    def test_connection(self, test_level=EnumTestLevel.LADM, user_level=EnumUserLevel.CREATE):
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

    def operation_model_exists(self):
        if self.read_model_parser():
            return self.model_parser.operation_model_exists()

        return False

    def valuation_model_exists(self):
        if self.read_model_parser():
            return self.model_parser.valuation_model_exists()

        return False

    def cadastral_form_model_exists(self):
        if self.read_model_parser():
            return self.model_parser.cadastral_form_model_exists()

        return False

    def ant_model_exists(self):
        if self.read_model_parser():
            return self.model_parser.ant_model_exists()

        return False

    def ladm_model_exists(self):
        if self.read_model_parser():
            return self.model_parser.ladm_model_exists()

        return False

    def reference_cartography_model_exists(self):
        if self.read_model_parser():
            return self.model_parser.reference_cartography_model_exists()

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

    def get_interlis_version(self):
        raise NotImplementedError

    def get_table_and_field_names(self):  # TODO: Add test
        """
        Get table and field names from the DB. Should be called only once for a single connection.

        :return: dict with table ilinames as keys and dict as values. The dicts found in the value contain field
                 ilinames as keys and sqlnames as values. The table name itself is added with the key 'table_name'.
                 Example:

            "LADM_COL.LADM_Nucleo.col_masCcl": {
                'table_name': 'col_masccl',
                'LADM_COL.LADM_Nucleo.col_masCcl.ccl_mas..Operacion.Operacion.OP_Lindero': 'ccl_mas',
                'LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_Construccion': 'ue_mas_op_construccion',
                'LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_ServidumbrePaso': 'ue_mas_op_servidumbrepaso',
                'LADM_COL.LADM_Nucleo.col_masCcl.another_ili_attr': 'corresponding_sql_name'
            }
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
            if k not in [T_ID_KEY, DISPLAY_NAME_KEY, ILICODE_KEY, DESCRIPTION_KEY]:  # Custom names will be handled by Names class
                self._table_and_field_names.append(k)  # Table names
                for k1, v1 in v.items():
                    if k1 != QueryNames.TABLE_NAME:
                        self._table_and_field_names.append(k1)  # Field names

    def check_at_least_one_ladm_model_exists(self):
        result = True
        msg = QCoreApplication.translate("DBConnector", "The version of all models is valid.")
        models = self.get_models()
        if len(set(models) & set(LADMNames.ASSISTANT_SUPPORTED_MODELS)) == 0:
            result = False
            msg = QCoreApplication.translate("DBConnector",
                                             "At least one LADM_COL model should exist! Supported models are '{}' but you have '{}'.").format(
                ', '.join(LADMNames.ASSISTANT_SUPPORTED_MODELS), ', '.join(models))
        return result, msg

    def open_connection(self):
        """
        :return: Whether the connection is opened after calling this method or not
        """
        raise NotImplementedError