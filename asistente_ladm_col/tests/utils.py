# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 16/01/18
        git sha              : :%H$
        copyright            : (C) 2018 by Jorge Useche (Incige SAS)
        email                : naturalmentejorge@gmail.com
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
from shutil import copyfile
from sys import platform

import psycopg2
import qgis.utils
from qgis.core import (QgsApplication,
                       edit)
from qgis.analysis import QgsNativeAlgorithms

from asistente_ladm_col.config.change_detection_config import PLOT_GEOMETRY_KEY
from asistente_ladm_col.config.refactor_fields_mappings import RefactorFieldsMappings
from asistente_ladm_col.asistente_ladm_col_plugin import AsistenteLADMCOLPlugin

QgsApplication.setPrefixPath('/usr', True)
qgs = QgsApplication([], False)
qgs.initQgis()

import processing

# get from https://github.com/qgis/QGIS/blob/master/tests/src/python/test_qgssymbolexpressionvariables.py
from qgis.testing.mocked import get_iface

from .config.test_config import TEST_SCHEMAS_MAPPING

# PostgreSQL connection to schema with a LADM_COL model from ./etl_script_uaecd.py
DB_HOSTNAME = "postgres"
DB_PORT = "5432"
DB_NAME = "ladm_col"
DB_USER = "usuario_ladm_col"
DB_PASSWORD = "clave_ladm_col"
iface = get_iface()
asistente_ladm_col_plugin = AsistenteLADMCOLPlugin(iface, True)
asistente_ladm_col_plugin.initGui()
refactor_fields = RefactorFieldsMappings()


def get_pg_conn(schema):
    #global DB_HOSTNAME DB_PORT DB_NAME DB_SCHEMA DB_USER DB_USER DB_PASSWORD
    dict_conn = dict()
    dict_conn['host'] = DB_HOSTNAME
    dict_conn['port'] = DB_PORT
    dict_conn['database'] = DB_NAME
    dict_conn['schema'] = schema
    dict_conn['username'] = DB_USER
    dict_conn['password'] = DB_PASSWORD
    db = asistente_ladm_col_plugin.conn_manager.get_opened_db_connector_for_tests('pg', dict_conn)

    return db

def get_gpkg_conn_from_path(path):
    dict_conn = dict()
    dict_conn['dbfile'] = path
    db = asistente_ladm_col_plugin.conn_manager.get_opened_db_connector_for_tests('gpkg', dict_conn)

    return db


def get_gpkg_conn(gpkg_schema_name):
    dict_conn = dict()
    db = None
    if gpkg_schema_name in TEST_SCHEMAS_MAPPING:
        gpkg_file_name = TEST_SCHEMAS_MAPPING[gpkg_schema_name]
        gpkg_path = get_test_path('geopackage/{gpkg_file_name}'.format(gpkg_file_name=gpkg_file_name))
        dict_conn['dbfile'] = gpkg_path
        db = asistente_ladm_col_plugin.conn_manager.get_opened_db_connector_for_tests('gpkg', dict_conn)

    return db

def get_copy_gpkg_conn(gpkg_schema_name):
    dict_conn = dict()
    db = None
    if gpkg_schema_name in TEST_SCHEMAS_MAPPING:
        gpkg_file_name = TEST_SCHEMAS_MAPPING[gpkg_schema_name]
        gpkg_path = get_test_copy_path('geopackage/{gpkg_file_name}'.format(gpkg_file_name=gpkg_file_name))
        dict_conn['dbfile'] = gpkg_path
        db = asistente_ladm_col_plugin.conn_manager.get_opened_db_connector_for_tests('gpkg', dict_conn)

    return db

def restore_schema(schema):
    print("\nRestoring schema {}...".format(schema))
    db_connection = get_pg_conn(schema)
    print("Testing Connection...", db_connection.test_connection())
    cur = db_connection.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{}';""".format(schema))
    result = cur.fetchone()
    if result is not None and len(result) > 0:
        print("The schema {} already exists".format(schema))
        return

    print("Restoring ladm_col database...")
    script_dir = get_test_path("restore_db.sh")
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        script_dir = get_test_path("restore_db.sh")
    elif platform == "win32":
        script_dir = get_test_path("restore_db.bat")
    else:
        print("Please add the test script")

    process = os.popen("{} {} {}".format(script_dir, TEST_SCHEMAS_MAPPING[schema], schema))
    output = process.readlines()
    process.close()
    print("Done restoring ladm_col database.")
    if len(output) > 0:
        print("Warning:", output)

def drop_schema(schema):
    print("\nDropping schema {}...".format(schema))
    db_connection = get_pg_conn(schema)
    print("Testing Connection...", db_connection.test_connection())
    cur = db_connection.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = cur.execute("""DROP SCHEMA "{}" CASCADE;""".format(schema))
    db_connection.conn.commit()
    cur.close()
    print("Schema {} removed...".format(schema))
    db_connection.conn.close()
    if query is not None:
        print("The drop schema is not working")

def clean_table(schema, table):
    print("\nCleaning table {}.{}...".format(schema, table))
    db_connection = get_pg_conn(schema)
    print("Testing Connection...", db_connection.test_connection())
    cur = db_connection.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = cur.execute("""DELETE FROM {}.{} WHERE True;""".format(schema, table))
    db_connection.conn.commit()
    cur.close()
    print('Table {}.{} cleaned...'.format(schema, table))
    if query is not None:
        print('The clean {}.{} is not working'.format(schema, table))

def get_iface():
    global iface

    def rewrite_method():
        return "I'm rewritten"
    iface.rewrite_method = rewrite_method
    return iface

def get_test_path(path):
    basepath = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(basepath, "resources", path)

def get_test_copy_path(path):
    src_path = get_test_path(path)
    dst_path = os.path.split(src_path)
    dst_path = os.path.join(dst_path[0], "_" + dst_path[1])
    copyfile(src_path, dst_path)
    return dst_path

def import_asistente_ladm_col():
    global iface
    plugin_found = "asistente_ladm_col" in qgis.utils.plugins
    if not plugin_found:
        qgis.utils.plugins["asistente_ladm_col"] = asistente_ladm_col_plugin

def import_qgis_model_baker():
    global iface
    plugin_found = "QgisModelBaker" in qgis.utils.plugins
    if not plugin_found:
        import QgisModelBaker
        pg = QgisModelBaker.classFactory(iface)
        qgis.utils.plugins["QgisModelBaker"] = pg

def import_processing():
    global iface
    plugin_found = "processing" in qgis.utils.plugins
    if not plugin_found:
        processing_plugin = processing.classFactory(iface)
        qgis.utils.plugins["processing"] = processing_plugin
        qgis.utils.active_plugins.append("processing")

        from processing.core.Processing import Processing
        Processing.initialize()
        QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

def unload_qgis_model_baker():
    global iface
    plugin_found = "QgisModelBaker" in qgis.utils.plugins
    if plugin_found:
        del(qgis.utils.plugins["QgisModelBaker"])

def run_etl_model(names, input_layer, out_layer, ladm_col_layer_name):
    import_processing()
    model = QgsApplication.processingRegistry().algorithmById("model:ETL-model")

    if model:
        automatic_fields_definition = True

        mapping = refactor_fields.get_refactor_fields_mapping(names, ladm_col_layer_name, asistente_ladm_col_plugin.qgis_utils)
        params = {
            'INPUT': input_layer,
            'mapping': mapping,
            'output': out_layer
        }
        res = processing.run("model:ETL-model", params)

    else:
        print("Error: Model ETL-model was not found and cannot be opened!")
        return

    return out_layer


def get_required_fields(db_connection):
    required_fields = list()
    for key, value in db_connection.names.TABLE_DICT.items():
        for key_field, value_field in value[db_connection.names.FIELDS_DICT].items():
            if getattr(db_connection.names, value_field):
                required_fields.append(value_field)
    return required_fields


def get_required_tables(db_connection):
    required_tables = list()
    for key, value in db_connection.names.TABLE_DICT.items():
        if getattr(db_connection.names, value[db_connection.names.VARIABLE_NAME]):
            required_tables.append(value[db_connection.names.VARIABLE_NAME])
    return required_tables

def testdata_path(path):
    basepath = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(basepath, 'resources', path)

def normalize_response(dict_response):
    """
    Converts geometry values to WKT, so that we can compare them with expected plain values.

    :param dict_response: Response dict to normalize.
    :return: Normalized response dict.
    """
    for key_parcel in dict_response:
        features = dict_response[key_parcel]
        for feature in features:
            if PLOT_GEOMETRY_KEY in feature:
                if feature[PLOT_GEOMETRY_KEY]:
                    feature[PLOT_GEOMETRY_KEY] = feature[PLOT_GEOMETRY_KEY].asWkt()

def delete_features(layer):
    with edit(layer):
        list_ids = [feat.id() for feat in layer.getFeatures()]
        layer.deleteFeatures(list_ids)


def standardize_query_results(result):
    if isinstance(result, (list, dict)):
        if isinstance(result, dict):
            result.pop('id', None)
            for item in result:
                standardize_query_results(result[item])

        elif isinstance(result, list):
            for item in result:
                if isinstance(item, dict):
                    standardize_query_results(item)
    return result