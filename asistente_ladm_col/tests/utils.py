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
import psycopg2

from sys import platform
from asistente_ladm_col.asistente_ladm_col_plugin import AsistenteLADMCOLPlugin
# get from https://github.com/qgis/QGIS/blob/master/tests/src/python/test_qgssymbolexpressionvariables.py
from qgis.testing.mocked import get_iface
import qgis.utils

# PostgreSQL connection to schema with a LADM_COL model from ./etl_script_uaecd.py
DB_HOSTNAME = "postgres"
DB_PORT = "5432"
DB_NAME = "ladm_col"
DB_SCHEMA = "test_ladm_col"
DB_USER = "usuario_ladm_col"
DB_PASSWORD = "clave_ladm_col"
iface = get_iface()
asistente_ladm_col_plugin = AsistenteLADMCOLPlugin(iface)
asistente_ladm_col_plugin.initGui()

def get_dbconn():
    #global DB_HOSTNAME DB_PORT DB_NAME DB_SCHEMA DB_USER DB_USER DB_PASSWORD
    dict_conn = dict()
    dict_conn['host'] = DB_HOSTNAME
    dict_conn['port'] = DB_PORT
    dict_conn['database'] = DB_NAME
    dict_conn['schema'] = DB_SCHEMA
    dict_conn['user'] = DB_USER
    dict_conn['password'] = DB_PASSWORD
    asistente_ladm_col_plugin.qgis_utils.set_db_connection('pg', dict_conn)

    db = asistente_ladm_col_plugin.qgis_utils.get_db_connection()
    return db

def restore_schema(db_connection):
    cur = db_connection.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'test_ladm_col';""")
    result = cur.fetchone()
    if result is not None and len(result) > 0:
        print("The schema test_ladm_col already exists")
        return

    print("Restoring ladm_col database...")
    script_dir = get_test_path("restore_db.sh")
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        script_dir = get_test_path("restore_db.sh")
    elif platform == "win32":
        script_dir = get_test_path("restore_db.bat")
    else:
        print("Please add the test script")

    process = os.popen(script_dir)
    output = process.readlines()
    process.close()
    print("Done restoring ladm_col database.")
    if len(output) > 0:
        print("Warning:", output)

def drop_schema(db_connection):
    print("Clean ladm_col database...")
    cur = db_connection.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = cur.execute("""DROP SCHEMA test_ladm_col CASCADE;""")
    db_connection.conn.commit()
    cur.close()
    db_connection.conn.close()
    if query is not None:
        print("The drop schema is not working")

def get_iface():
    global iface
    def rewrite_method():
        return "i'm rewrited"
    iface.rewrite_method = rewrite_method
    return iface

def get_test_path(path):
    basepath = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(basepath, "resources", path)

def import_projectgenerator():
    global iface
    plugin_found = "projectgenerator" in qgis.utils.plugins
    if not plugin_found:
        import sys
        if platform == "linux" or platform == "linux2" or platform == "darwin":
            sys.path.append("/usr/share/qgis/python/plugins")
        elif platform == "win32":
            sys.path.append("C:\\Users\\aimplementacion\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins")
        else:
            print("Please add the correct projectgenerator path")
        import projectgenerator
        pg = projectgenerator.classFactory(iface)
        qgis.utils.plugins["projectgenerator"] = pg

def unload_projectgenerator():
    global iface
    plugin_found = "projectgenerator" in qgis.utils.plugins
    if plugin_found:
        del(qgis.utils.plugins["projectgenerator"])
