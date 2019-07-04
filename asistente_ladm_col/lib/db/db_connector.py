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

from qgis.PyQt.QtCore import QObject
from asistente_ladm_col.utils.model_parser import ModelParser
from enum import IntFlag


class EnumTestLevel(IntFlag):
    SERVER = 1
    DB = 2
    DB_SCHEMA = 6
    DB_FILE = 6
    LADM = 14
    CREATE_SCHEMA = 128

    _CHECK_DB = 2
    _CHECK_SCHEMA = 4
    _CHECK_LADM = 8


class DBConnector(QObject):
    '''SuperClass for all DB connectors.'''
    def __init__(self, uri, schema=None, conn_dict={}):
        QObject.__init__(self)
        self.mode = ''
        self.provider = '' # QGIS provider name. e.g., postgres
        self._uri = None
        self.schema = schema
        self.conn = None
        self._dict_conn_params = None
        
        if uri:
            self.uri = uri
        elif conn_dict:
            self.dict_conn_params = conn_dict

        self.model_parser = None

    @property
    def dict_conn_params(self):
        return self._dict_conn_params.copy()

    @dict_conn_params.setter
    def dict_conn_params(self, value):
        self._dict_conn_params = value
        self._uri = self.get_connection_uri(value, level=1)

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, value):
        raise NotImplementedError

    def test_connection(self, test_level=EnumTestLevel.LADM):
        raise NotImplementedError

    def validate_db(self):
        raise NotImplementedError

    def close_connection(self):
        raise NotImplementedError

    def get_uri_for_layer(self, layer_name, geometry_type=None):
        raise NotImplementedError

    def get_description(self):
        return "Current connection details: '{}' -> {} {}".format(
            self.mode,
            self._uri,
            'schema:{}'.format(self.schema) if self.schema else '')

    def get_models(self, schema=None):
        raise NotImplementedError

    def get_display_conn_string(self):
        # Do not use to connect to a DB, only for display purposes
        tmp_dict_conn_params = self._dict_conn_params.copy()
        if 'password' in tmp_dict_conn_params:
            del tmp_dict_conn_params['password']
        if 'schema' in tmp_dict_conn_params:
            del tmp_dict_conn_params['schema']

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

    def valuation_model_exists(self):
        if self.model_parser is None:
            res = self._parse_models()
            if not res:
                return False

        return self.model_parser.valuation_model_exists()

    def property_record_card_model_exists(self):
        if self.model_parser is None:
            res = self._parse_models()
            if not res:
                return False

        return self.model_parser.property_record_card_model_exists()

    def _parse_models(self):
        try:
            if self.model_parser is None:
                self.model_parser = ModelParser(self)
                return True
        except psycopg2.ProgrammingError as e:
            # if it is not possible to access the schema due to lack of privileges
            return False

    def is_ladm_layer(self, layer):
        raise NotImplementedError

    def get_ladm_layer_name(self, layer, validate_is_ladm=False):
        raise NotImplementedError
