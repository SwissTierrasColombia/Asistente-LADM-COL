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


class DBConnector(QObject):
    '''SuperClass for all DB connectors.'''
    def __init__(self, uri, schema=None, conn_dict={}):
        QObject.__init__(self)
        self.mode = ''
        self.provider = '' # QGIS provider name. e.g., postgres
        self.uri = uri
        self.schema = schema
        self.conn = None
        self.dict_conn_params = dict()

        self.model_parser = None

    def test_connection(self):
        pass

    def validate_db(self):
        pass

    def close_connection(self):
        pass

    def get_uri_for_layer(self, layer_name, geometry_type=None):
        pass

    def get_description(self):
        return "Current connection details: '{}' -> {} {}".format(
            self.mode,
            self.uri,
            'schema:{}'.format(self.schema) if self.schema else '')

    def get_models(self, schema=None):
        pass

    def get_display_conn_string(self):
        # Do not use to connect to a DB, only for display purposes
        tmp_dict_conn_params = self.dict_conn_params.copy()
        if 'password' in tmp_dict_conn_params:
            del tmp_dict_conn_params['password']
        if 'schema' in tmp_dict_conn_params:
            del tmp_dict_conn_params['schema']

        return ' '.join(["{}={}".format(k, v) for k, v in tmp_dict_conn_params.items()])

    def get_connection_uri(self, dict_conn, mode='pg', level=1):
        """
        :param dict_conn: (dict) dictionary with the parameters to establish a connection
        :param level: (str) Connection mode:
            'pg': PostgreQSL/PostGIS
            'gpkg': GeoPackage
        :param level: (int) At what level the connection will be established
            0: server level
            1: database level
        :return: (str) string uri to establish a connection
        """
        uri = []
        separator = ' '

        if mode == 'pg':
            uri += ['host={}'.format(dict_conn['host'])]
            uri += ['port={}'.format(dict_conn['port'])]
            if dict_conn['username']:
                uri += ['user={}'.format(dict_conn['username'])]
            if dict_conn['password']:
                uri += ['password={}'.format(dict_conn['password'])]
            if dict_conn['database'] and level == 1:
                uri += ['dbname={}'.format(dict_conn['database'])]
            else:
                # It is necessary to define the database name for listing databases
                # PostgreSQL uses the db 'postgres' by default and it cannot be deleted, so we use it as last resort
                uri += ["dbname='postgres'"]
        elif mode == 'gpkg':
            uri = [dict_conn['dbfile']]
        elif mode == 'mssql':
            uri += ['DRIVER={SQL Server}']
            host = dict_conn['host'] or 'localhost'
            if dict_conn['port']:
                host += ',' + dict_conn['port']
            if dict_conn['instance']:
                host += '\\' + dict_conn['instance']

            uri += ['SERVER={}'.format(host)]
            if dict_conn['database'] and level == 1:
                uri += ['DATABASE={}'.format(dict_conn['database'])]
            uri += ['UID={}'.format(dict_conn['username'])]
            uri += ['PWD={}'.format(dict_conn['password'])]
            separator = ';'

        return separator.join(uri)

    def valuation_model_exists(self):
        if self.model_parser is None:
            res = self._parse_model()
            if not res:
                return False

        return self.model_parser.valuation_model_exists()

    def property_record_card_model_exists(self):
        if self.model_parser is None:
            res = self._parse_model()
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

