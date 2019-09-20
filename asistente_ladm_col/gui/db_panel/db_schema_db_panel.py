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
from qgis.core import Qgis
from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication)

from .db_config_panel import DbConfigPanel
from ...gui.dialogs.dlg_get_db_or_schema_name import GetDBOrSchemaNameDialog
from ...lib.db.db_connector import EnumTestLevel


class DbSchemaDbPanel(DbConfigPanel):
    def __init__(self, parent):
        DbConfigPanel.__init__(self, parent)

    def init_schema(self):
        self.create_db_button.clicked.connect(self.show_create_db_dialog)
        self.create_schema_button.clicked.connect(self.show_create_schema_dialog)
        self.refresh_db_button.clicked.connect(self._refresh_db_button_clicked)
        self._set_controls_enabled(False)

    def _connect_change_signals(self):
        self.selected_db_combobox.currentIndexChanged.connect(self.selected_database_changed)

    def _set_controls_enabled(self, value):
        self.selected_db_combobox.setEnabled(value)
        self.selected_schema_combobox.setEnabled(value)
        self.create_db_button.setEnabled(value)
        self.create_schema_button.setEnabled(value)

    def _refresh_db_button_clicked(self):
        self._disconnect_change_signals()

        old_db_selected = self.selected_db_combobox.currentText().strip()
        old_schema_selected = self.selected_schema_combobox.currentText().strip()

        if self.update_db_names():
            old_db_index = self.selected_db_combobox.findText(old_db_selected, Qt.MatchFixedString)
            if old_db_index >= 0:
                self.selected_db_combobox.setCurrentIndex(old_db_index)

            self.update_db_schemas()

            old_schema_index = self.selected_schema_combobox.findText(old_schema_selected, Qt.MatchFixedString)

            if old_schema_index >= 0:
                self.selected_schema_combobox.setCurrentIndex(old_schema_index)

            self._set_controls_enabled(True)
        else:
            self.selected_schema_combobox.clear()
            self._set_controls_enabled(False)

        self._connect_change_signals()

    def _disconnect_change_signals(self):
        try:
            self.selected_db_combobox.currentIndexChanged.disconnect(self.selected_database_changed)
        except TypeError:
            pass

    def update_db_names(self):
        result = False
        tmp_db_conn = self.get_connector()
        uri = tmp_db_conn.get_connection_uri(tmp_db_conn.dict_conn_params, level=0)
        tmp_db_conn.close_connection()
        res, data = tmp_db_conn.get_dbnames_list(uri)

        self.selected_db_combobox.clear()

        if res:
            self.selected_db_combobox.addItems(data)

            result = True
        else:
            self.notify_message_requested.emit(QCoreApplication.translate("SettingsDialog", data), Qgis.Warning)

        return result

    def selected_database_changed(self, index):
        self.update_db_schemas()

    def update_db_schemas(self):
        self.selected_schema_combobox.clear()
        tmp_db_conn = self.get_connector()

        if tmp_db_conn:
            uri = tmp_db_conn.uri
            tmp_db_conn.close_connection()
            res, data = tmp_db_conn.get_dbname_schema_list(uri)

            if res:
                self.selected_schema_combobox.addItems(data)
            else:
                # We won't show a message here to avoid bothering the user with potentially too much messages
                pass

    def database_created(self, db_name):
        self.update_db_names()

        # select the database created by the user
        index = self.selected_db_combobox.findText(db_name, Qt.MatchFixedString)
        if index >= 0:
            self.selected_db_combobox.setCurrentIndex(index)

    def schema_created(self, schema_name):
        self.update_db_schemas()

        # select the schema created by the user
        index = self.selected_schema_combobox.findText(schema_name, Qt.MatchFixedString)
        if index >= 0:
            self.selected_schema_combobox.setCurrentIndex(index)

    def show_create_db_dialog(self):
        tmp_db_conn = self.get_connector()
        tmp_db_conn.open_connection()
        res, msg = tmp_db_conn.test_connection(test_level=EnumTestLevel.SERVER)

        if res:
            create_db_dlg = GetDBOrSchemaNameDialog(tmp_db_conn, tmp_db_conn.uri, 'database', parent=self)
            create_db_dlg.db_or_schema_created.connect(self.database_created)
            create_db_dlg.setModal(True)
            create_db_dlg.exec_()
        else:
            msg = QCoreApplication.translate("SettingsDialog", "First set the connection to the database before attempting to create a database.")
            self.notify_message_requested.emit(msg, Qgis.Warning)

        tmp_db_conn.close_connection()

    def show_create_schema_dialog(self):
        tmp_db_conn = self.get_connector()
        tmp_db_conn.open_connection()
        res, msg = tmp_db_conn.test_connection(test_level=EnumTestLevel.DB)

        if res:
            create_db_dlg = GetDBOrSchemaNameDialog(tmp_db_conn, tmp_db_conn.uri, 'schema', parent=self)
            create_db_dlg.db_or_schema_created.connect(self.schema_created)
            create_db_dlg.setModal(True)
            create_db_dlg.exec_()
        else:
            msg = QCoreApplication.translate("SettingsDialog", "First set the connection to the database before attempting to create a schema.")
            self.notify_message_requested.emit(msg, Qgis.Warning)

        tmp_db_conn.close_connection()

    def get_connector(self):
        raise NotImplementedError
