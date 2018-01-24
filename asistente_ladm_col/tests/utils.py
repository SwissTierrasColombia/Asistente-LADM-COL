# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 16/01/18
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BSF-Swissphoto)
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

__author__ = 'Germán Carrillo'
__date__ = 'Enero 2017'
__copyright__ = '(C) 2017, Germán Carrillo'
# This will get replaced with a git SHA1 when you do a git archive
__revision__ = '$Format:%H$'


import os
import psycopg2

from sys import platform
from asistente_ladm_col.asistente_ladm_col_plugin import AsistenteLADMCOLPlugin
# get from https://github.com/qgis/QGIS/blob/master/tests/src/python/test_qgssymbolexpressionvariables.py
from qgis.testing.mocked import get_iface

# PostgreSQL connection to schema with a LADM_COL model from ./etl_script_uaecd.py
DB_HOSTNAME = 'postgres'
DB_PORT = '5432'
DB_NAME = 'ladm_col'
DB_SCHEMA = 'test_ladm_col'
DB_USER = 'usuario_ladm_col'
DB_PASSWORD = 'clave_ladm_col'
iface = get_iface()
asistente_ladm_col_plugin = AsistenteLADMCOLPlugin(iface)
asistente_ladm_col_plugin.initGui()

def get_dbconn():
    #global DB_HOSTNAME DB_PORT DB_NAME DB_SCHEMA DB_USER DB_USER DB_PASSWORD
    settings = asistente_ladm_col_plugin.get_settings_dialog()
    settings.txt_pg_host.setText(DB_HOSTNAME)
    settings.txt_pg_port.setText(DB_PORT)
    settings.txt_pg_database.setText(DB_NAME)
    settings.txt_pg_schema.setText(DB_SCHEMA)
    settings.txt_pg_user.setText(DB_USER)
    settings.txt_pg_password.setText(DB_PASSWORD)
    settings.accepted()
    db = asistente_ladm_col_plugin.get_db_connection()
    return db

def restore_schema(db_connection):
    cur = db_connection.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'test_ladm_col';""")
    result = cur.fetchone()
    if result is not None and len(result) > 0:
        print('The schema test_ladm_col already exists')
        return

    print('Restoring ladm_col database...')
    script_dir = get_test_path('restore_db.sh')
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        script_dir = get_test_path('restore_db.sh')
    elif platform == "win32":
        script_dir = get_test_path('restore_db.bat')
    else:
        print('Please add the test script')

    process = os.popen(script_dir)
    output = process.readlines()
    process.close()
    print('Done restoring ladm_col database.')
    if len(output) > 0:
        print('Warning:', output)

def drop_schema(db_connection):
    print('Clean ladm_col database...')
    cur = db_connection.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = cur.execute("""DROP SCHEMA test_ladm_col CASCADE;""")
    db_connection.conn.commit()
    cur.close()
    db_connection.conn.close()
    if query is not None:
        print('The drop schema is not working')

def get_iface():
    global iface
    def rewrite_method():
        return "i'm rewrited"
    iface.rewrite_method = rewrite_method
    return iface

def get_test_path(path):
    basepath = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(basepath, 'resources', path)
