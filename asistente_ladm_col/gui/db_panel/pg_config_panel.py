# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-02-21
        git sha              : :%H$
        copyright            : (C) 2019 by Yesid Polanía (BSF Swissphoto)
        email                : yesidpol.3@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import QWidget
from qgis.core import Qgis
from .db_schema_db_panel import DbSchemaDbPanel
from ...lib.db.pg_connector import PGConnector
from ...utils import get_ui_class

WIDGET_UI = get_ui_class('settings_pg.ui')


class PgConfigPanel(QWidget, WIDGET_UI, DbSchemaDbPanel):
    notify_message_requested = pyqtSignal(str, Qgis.MessageLevel)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        DbSchemaDbPanel.__init__(self)
        self.setupUi(self)
        self.mode = "pg"
        self.init_schema()

    def showEvent(self, event):
        self._set_controls_enabled(False)

    def read_connection_parameters(self):
        """
        Convenient function to read connection parameters and apply default
        values if needed.
        """
        dict_conn = dict()

        dict_conn['host'] = self.txt_host.text().strip()
        dict_conn['port'] = self.txt_port.text().strip()
        dict_conn['database'] = self.selected_db_combobox.currentText().strip()
        dict_conn['schema'] = self.selected_schema_combobox.currentText().strip()
        dict_conn['username'] = self.txt_user.text().strip()
        dict_conn['password'] = self.txt_password.text().strip()

        return dict_conn

    def get_keys_connection_parameters(self):
        return list(self.read_connection_parameters().keys())

    def write_connection_parameters(self, dict_conn):
        self._disconnect_change_signals()

        self.txt_host.setText(dict_conn['host'] if 'host' in dict_conn else '')
        self.txt_port.setText(dict_conn['port'] if 'port' in dict_conn else '')
        self.txt_user.setText(dict_conn['username'] if 'username' in dict_conn else '')
        self.txt_password.setText(dict_conn['password'] if 'password' in dict_conn else '')

        if 'database' in dict_conn and not dict_conn['database']:
            self._connect_change_signals()
            return

        db_name_setting = dict_conn['database'] if 'database' in dict_conn else ''

        self.selected_db_combobox.clear()
        self.selected_schema_combobox.clear()

        if db_name_setting:
            self.selected_db_combobox.addItem(db_name_setting)
        if 'schema' in dict_conn and dict_conn['schema']:
            self.selected_schema_combobox.addItem(dict_conn['schema'])

        self._connect_change_signals()

    def state_changed(self):
        result = True

        if self.state:
            result = (self.state['host'] != self.txt_host.text().strip() or \
                self.state['port'] != self.txt_port.text().strip() or \
                self.state['database'] != self.selected_db_combobox.currentText().strip() or \
                self.state['schema'] != self.selected_schema_combobox.currentText().strip() or \
                self.state['username'] != self.txt_user.text().strip() or \
                self.state['password'] != self.txt_password.text().strip())

        return result

    def get_connector(self):
        dict = self.read_connection_parameters()
        return PGConnector(None, dict)
