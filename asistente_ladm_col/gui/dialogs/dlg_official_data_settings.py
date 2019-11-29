# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-04-24
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
from qgis.PyQt.QtCore import (Qt,
                              QSettings,
                              pyqtSignal)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QSizePolicy)
from qgis.core import Qgis
from qgis.gui import QgsMessageBar

from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.config.general_config import (PLUGIN_NAME,
                                   OFFICIAL_DB_SOURCE)
from asistente_ladm_col.lib.db.db_connector import (DBConnector, EnumTestLevel)
from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.config.config_db_supported import ConfigDbSupported
from asistente_ladm_col.resources_rc import * # Necessary to show icons

DIALOG_UI = get_ui_class('dialogs/dlg_official_data_settings.ui')


class OfficialDataSettingsDialog(QDialog, DIALOG_UI):
    official_db_connection_changed = pyqtSignal(DBConnector, bool) # dbconn, ladm_col_db

    def __init__(self, qgis_utils=None, conn_manager=None, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.qgis_utils = qgis_utils
        self.conn_manager = conn_manager
        self.logger = Logger()
        self._db = None
        self.db_source = OFFICIAL_DB_SOURCE
        self.conf_db = ConfigDbSupported()

        # Set connections
        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.helpRequested.connect(self.show_help)
        self.finished.connect(self.finished_slot)
        self.btn_test_connection.clicked.connect(self.test_connection)
        self.btn_test_ladm_col_structure.clicked.connect(self.test_ladm_col_structure)

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

        self.cbo_db_source.clear()

        self._lst_db = self.conf_db.get_db_items()
        self._lst_panel = dict()

        for key, value in self._lst_db.items():
            self.cbo_db_source.addItem(value.get_name(), key)
            self._lst_panel[key] = value.get_config_panel(self)
            self._lst_panel[key].notify_message_requested.connect(self.show_message)
            self.db_layout.addWidget(self._lst_panel[key])

        self.db_source_changed()

        # Trigger some default behaviours
        self.restore_settings()

        self.cbo_db_source.currentIndexChanged.connect(self.db_source_changed)
        self.rejected.connect(self.close_dialog)

    def close_dialog(self):
        self.close()

    def showEvent(self, event):
        # It is necessary to reload the variables
        # to load the database and schema name
        self.restore_settings()

    def _get_db_connector_from_gui(self):
        current_db = self.cbo_db_source.currentData()
        params = self._lst_panel[current_db].read_connection_parameters()
        db = self._lst_db[current_db].get_db_connector(params)
        db.open_connection() # Open connection using gui parameters
        return db

    def get_db_connection(self):
        if self._db is not None:
            self.logger.info(__name__, "Returning existing db connection...")
        else:
            self.logger.info(__name__, "Getting new db connection...")
            self._db = self._get_db_connector_from_gui()
            self._db.open_connection()

        return self._db

    def accepted(self):
        current_db = self.cbo_db_source.currentData()
        if self._lst_panel[current_db].state_changed():
            valid_connection = True
            ladm_col_schema = False

            db = self._get_db_connector_from_gui()
            res, msg = db.test_connection(EnumTestLevel.DB_SCHEMA)

            if res:
                ladm_col_schema, msg = db.test_connection(EnumTestLevel.LADM)
            else:
                self.show_message(msg, Qgis.Warning)
                valid_connection = False

            if not ladm_col_schema:
                self.show_message(msg, Qgis.Warning)
                return  # Do not close the dialog

            if valid_connection:
                if self._db is not None:
                    self._db.close_connection()

                self._db = db

                # Update db connect with new db conn
                self.conn_manager.set_db_connector_for_source(self._db, self.db_source)

                # Emmit signal when change db source
                self.official_db_connection_changed.emit(self._db, ladm_col_schema)

                self.save_settings()
                QDialog.accept(self)  # TODO remove?
            else:
                return  # Do not close the dialog

        else:
            QDialog.accept(self)  # TODO remove?

    def finished_slot(self, result):
        self.bar.clearWidgets()

    def set_db_connection(self, mode, dict_conn):
        """
        To be used by external scripts and unit tests
        """
        self.cbo_db_source.setCurrentIndex(self.cbo_db_source.findData(mode))
        self.db_source_changed()

        current_db = self.cbo_db_source.currentData()

        self._lst_panel[current_db].write_connection_parameters(dict_conn)

        self.accepted() # Create/update the db object

    def save_settings(self):
        settings = QSettings()
        current_db = self.cbo_db_source.currentData()
        settings.setValue('Asistente-LADM_COL/db/{db_source}/db_connection_source'.format(db_source=self.db_source), current_db)
        dict_conn = self._lst_panel[current_db].read_connection_parameters()

        self._lst_db[current_db].save_parameters_conn(dict_conn=dict_conn, db_source=self.db_source)

    def restore_settings(self):
        # Restore QSettings
        settings = QSettings()
        default_db = self.conf_db.id_default_db

        index_db = self.cbo_db_source.findData(settings.value('Asistente-LADM_COL/db/{db_source}/db_connection_source'.format(db_source=self.db_source), default_db))

        if index_db == -1:
            index_db = self.cbo_db_source.findData(default_db)

        self.cbo_db_source.setCurrentIndex(index_db)
        self.db_source_changed()

        # restore db settings for all panels
        for id_db, db_factory in self._lst_db.items():
            dict_conn = db_factory.get_parameters_conn(self.db_source)
            self._lst_panel[id_db].write_connection_parameters(dict_conn)
            self._lst_panel[id_db].save_state()

    def db_source_changed(self):
        if self._db is not None:
            self._db.close_connection()

        self._db = None # Reset db connection

        for key, value in self._lst_panel.items():
            value.setVisible(False)

        current_db = self.cbo_db_source.currentData()

        self._lst_panel[current_db].setVisible(True)

    def test_connection(self):
        db = self._get_db_connector_from_gui()
        res, msg = db.test_connection(test_level=EnumTestLevel.DB_SCHEMA)

        if db is not None:
            db.close_connection()

        self.show_message(msg, Qgis.Info if res else Qgis.Warning)
        self.logger.info(__name__, "Test connection!")

    def test_ladm_col_structure(self):
        db = self._get_db_connector_from_gui()
        res, msg = db.test_connection(test_level=EnumTestLevel.LADM)

        if db is not None:
            db.close_connection()

        self.show_message(msg, Qgis.Info if res else Qgis.Warning)
        self.logger.info(__name__, "Test LADM structure!")

    def show_message(self, message, level):
        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.bar.pushMessage(message, level, 10)

    def show_help(self):
        self.qgis_utils.show_help("settings")
