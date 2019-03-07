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
from .enum_action_type import EnumActionType
from .db_schema_db_panel import DbSchemaDbPanel
from ..lib.dbconnector.pg_connector import PGConnector
from qgis.core import (Qgis)


class PgConfigPanel(QWidget, DbSchemaDbPanel):

    notify_message_requested = pyqtSignal(str, Qgis.MessageLevel)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        DbSchemaDbPanel.__init__(self, PGConnector(''))

        self.mode = "pg"

        lbl_host = QLabel(self.tr("Host"))
        lbl_port = QLabel(self.tr("Port"))
        lbl_user = QLabel(self.tr("User"))
        lbl_password = QLabel(self.tr("Password"))
        lbl_database = QLabel(self.tr("Database"))
        lbl_schema = QLabel(self.tr("Schema"))

        self.txt_host = QLineEdit()
        self.txt_host.setPlaceholderText(QCoreApplication.translate("SettingsDialog", "[Leave empty to use standard host: localhost]"))

        self.txt_port = QLineEdit()
        self.txt_port.setPlaceholderText(
            QCoreApplication.translate("SettingsDialog", "[Leave empty to use standard port: 5432]"))

        self.txt_user = QLineEdit()
        self.txt_user.setPlaceholderText(QCoreApplication.translate("SettingsDialog", "Database username"))

        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_password.setPlaceholderText(
            QCoreApplication.translate("SettingsDialog", "[Leave empty to use system password]"))

        self.create_db_button.setToolTip(QCoreApplication.translate("SettingsDialog", "Create database"))

        #
        # self.create_db_button.setIcon(icon)

        self.create_schema_button.setToolTip(QCoreApplication.translate("SettingsDialog", "Create schema"))

        layout = QGridLayout(self)
        layout.addWidget(lbl_host, 0, 0)
        layout.addWidget(lbl_port, 1, 0)
        layout.addWidget(lbl_user, 2, 0)
        layout.addWidget(lbl_password, 3, 0)
        layout.addWidget(lbl_database, 4, 0)
        layout.addWidget(lbl_schema, 5, 0)

        layout.addWidget(self.txt_host, 0, 1)
        layout.addWidget(self.txt_port, 1, 1)
        layout.addWidget(self.txt_user, 2, 1)
        layout.addWidget(self.txt_password, 3, 1)

        layout.addWidget(self.selected_db_combobox, 4, 1)
        layout.addWidget(self.selected_schema_combobox, 5, 1)

        layout.addWidget(self.create_db_button, 4, 2)
        layout.addWidget(self.create_schema_button, 5, 2)

        self.txt_host.textChanged.connect(self.request_for_refresh_connection)
        self.txt_port.textChanged.connect(self.request_for_refresh_connection)
        self.txt_user.textChanged.connect(self.request_for_refresh_connection)
        self.txt_password.textChanged.connect(self.request_for_refresh_connection)

        self.txt_host.textEdited.connect(self._set_params_changed)
        self.txt_port.textEdited.connect(self._set_params_changed)
        self.txt_user.textEdited.connect(self._set_params_changed)
        self.txt_password.textEdited.connect(self._set_params_changed)

    def read_connection_parameters(self):
        """
        Convenient function to read connection parameters and apply default
        values if needed.
        """
        dict_conn = dict()

        dict_conn['host'] = self.txt_host.text().strip() or 'localhost'
        dict_conn['port'] = self.txt_port.text().strip() or '5432'
        dict_conn['database'] = "'{}'".format(self.selected_db_combobox.currentText().strip())
        dict_conn['schema'] = self.selected_schema_combobox.currentText().strip() or 'public'
        dict_conn['username'] = self.txt_user.text().strip()
        dict_conn['password'] = self.txt_password.text().strip()

        return dict_conn

    def get_keys_connection_parameters(self):
        return list(self.read_connection_parameters().keys())

    def write_connection_parameters(self, dict_conn):
        self.txt_host.setText(dict_conn['host'])
        self.txt_port.setText(dict_conn['port'])
        self.txt_user.setText(dict_conn['username'])
        self.txt_password.setText(dict_conn['password'])

        if not dict_conn['database']:
            return
        db_name_setting = dict_conn['database'].strip("'")
        self.update_db_names()

        if self.selected_db_combobox.count():
            index = self.selected_db_combobox.findText(db_name_setting, Qt.MatchFixedString)
            if index >= 0:
                self.selected_db_combobox.setCurrentIndex(index)
                schema_setting = dict_conn['schema']
                self.update_db_schemas()
                if self.selected_schema_combobox.count():
                    index = self.selected_schema_combobox.findText(schema_setting, Qt.MatchFixedString)

                    if index >= 0:
                        self.selected_schema_combobox.setCurrentIndex(index)

    def check_for_refresh(self):
        return self.txt_user.text().strip() and self.txt_password.text().strip()
