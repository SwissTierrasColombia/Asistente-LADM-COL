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
from qgis.PyQt.QtCore import (Qt, QCoreApplication,pyqtSignal)
from qgis.PyQt.QtWidgets import (QWidget,
                                 QLabel,
                                 QGridLayout,
                                 QLineEdit,
                                 QComboBox,
                                 QPushButton
                                 )
from qgis.core import Qgis
from .db_schema_db_panel import DbSchemaDbPanel
from ...lib.db.mssql_connector import MssqlConnector
from QgisModelBaker.utils.mssql_utils import get_odbc_drivers


class MssqlConfigPanel(QWidget, DbSchemaDbPanel):
    notify_message_requested = pyqtSignal(str, Qgis.MessageLevel)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        DbSchemaDbPanel.__init__(self, MssqlConnector(''))

        # FIXME unused code (probably)
        self.mode = "mssql"

        lbl_odbc_driver = QLabel(self.tr("Odbc Driver"))
        lbl_host = QLabel(self.tr("Host"))
        lbl_port = QLabel(self.tr("Port"))
        lbl_database = QLabel(self.tr("Database"))
        lbl_instance = QLabel(self.tr("Instance"))
        lbl_user = QLabel(self.tr("User"))
        lbl_password = QLabel(self.tr("Password"))
        lbl_schema = QLabel(self.tr("Schema"))

        self.cbx_odbc_driver = QComboBox()

        for item_odbc_driver in get_odbc_drivers():
            self.cbx_odbc_driver.addItem(item_odbc_driver)

        self.txt_host = QLineEdit()
        self.txt_host.setPlaceholderText(QCoreApplication.translate("SettingsDialog", "[Leave empty to use standard host: localhost]"))

        self.txt_port = QLineEdit()
        self.txt_port.setPlaceholderText(
            QCoreApplication.translate("SettingsDialog", "[Leave empty to use dinamic or standard port 1433]"))

        self.txt_instance = QLineEdit()
        self.txt_instance.setPlaceholderText(
            QCoreApplication.translate("SettingsDialog", "[Leave empty to use default instance]"))

        self.txt_user = QLineEdit()
        self.txt_user.setPlaceholderText(QCoreApplication.translate("SettingsDialog", "Database username"))

        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_password.setPlaceholderText(
            QCoreApplication.translate("SettingsDialog", "[Leave empty to use system password]"))

        self.create_db_button.setToolTip(QCoreApplication.translate("SettingsDialog", "Create database"))

        self.create_schema_button.setToolTip(QCoreApplication.translate("SettingsDialog", "Create schema"))

        layout = QGridLayout(self)
        layout.addWidget(lbl_odbc_driver, 0, 0)
        layout.addWidget(lbl_host, 1, 0)
        layout.addWidget(lbl_port, 2, 0)
        layout.addWidget(lbl_instance, 3, 0)
        layout.addWidget(lbl_user, 4, 0)
        layout.addWidget(lbl_password, 5, 0)
        layout.addWidget(lbl_database, 7, 0)
        layout.addWidget(lbl_schema, 8, 0)

        layout.addWidget(self.cbx_odbc_driver, 0, 1)
        layout.addWidget(self.txt_host, 1, 1)
        layout.addWidget(self.txt_port, 2, 1)
        layout.addWidget(self.txt_instance, 3, 1)
        layout.addWidget(self.txt_user, 4, 1)
        layout.addWidget(self.txt_password, 5, 1)

        layout.addWidget(self.refresh_db_button, 6, 0, 1, 2)

        layout.addWidget(self.selected_db_combobox, 7, 1)
        layout.addWidget(self.selected_schema_combobox, 8, 1)

        layout.addWidget(self.create_db_button, 7, 2)
        layout.addWidget(self.create_schema_button, 8, 2)

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
        dict_conn['instance'] = self.txt_instance.text().strip()
        # TODO empty schema? dbo?
        dict_conn['schema'] = self.selected_schema_combobox.currentText().strip()
        dict_conn['username'] = self.txt_user.text().strip()
        dict_conn['password'] = self.txt_password.text().strip()
        dict_conn['db_odbc_driver'] = self.cbx_odbc_driver.currentText()

        return dict_conn

    def get_keys_connection_parameters(self):
        return list(self.read_connection_parameters().keys())

    def write_connection_parameters(self, dict_conn):
        self._disconnect_change_signals()

        self.txt_host.setText(dict_conn['host'])
        self.txt_port.setText(dict_conn['port'])
        self.txt_instance.setText(dict_conn['instance'])
        self.txt_user.setText(dict_conn['username'])
        self.txt_password.setText(dict_conn['password'])

        if not dict_conn['database']:
            self._connect_change_signals()
            return
        db_name_setting = dict_conn['database'].strip("'")

        self.selected_db_combobox.clear()
        self.selected_schema_combobox.clear()

        if db_name_setting:
            self.selected_db_combobox.addItem(db_name_setting)
        if dict_conn['schema']:
            self.selected_schema_combobox.addItem(dict_conn['schema'])

        index = self.cbx_odbc_driver.findText(dict_conn['db_odbc_driver'])
        if index != -1:
            self.cbx_odbc_driver.setCurrentIndex(index)

        self._connect_change_signals()

    def state_changed(self):
        result = True

        if self.state:
            result = (self.state['host'] != self.txt_host.text().strip() or \
                self.state['port'] != self.txt_port.text().strip() or \
                self.state['database'] != self.selected_db_combobox.currentText().strip() or \
                self.state['instance'] != self.txt_instance.text().strip() or \
                self.state['schema'] != self.selected_schema_combobox.currentText().strip() or \
                self.state['username'] != self.txt_user.text().strip() or \
                self.state['password'] != self.txt_password.text().strip() or \
                self.state['db_odbc_driver'] != self.cbx_odbc_driver.currentText().strip())

        return result
