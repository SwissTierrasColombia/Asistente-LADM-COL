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
import json

from qgis.PyQt.QtNetwork import (QNetworkRequest,
                          QNetworkAccessManager)
from qgis.PyQt.QtCore import (Qt,
                              QSettings,
                              pyqtSignal,
                              QUrl,
                              QCoreApplication,
                              QTextStream,
                              QIODevice,
                              QEventLoop,
                              QTimer)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QSizePolicy,
                                 QGridLayout)
from qgis.core import (Qgis,
                       QgsApplication)
from qgis.gui import QgsMessageBar

from ..config.general_config import PLUGIN_NAME
from ..lib.db.db_connector import (DBConnector, EnumTestLevel)
from ..utils import get_ui_class
from ..config.config_db_supported import ConfigDbSupported

DIALOG_UI = get_ui_class('official_data_settings_dialog.ui')


class OfficialDataSettingsDialog(QDialog, DIALOG_UI):
    official_db_connection_changed = pyqtSignal(DBConnector, bool) # dbconn, ladm_col_db

    def __init__(self, qgis_utils=None, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.log = QgsApplication.messageLog()
        self._db = None
        self.qgis_utils = qgis_utils

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
        self.setLayout(QGridLayout())
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

        self.cbo_db_source.clear()

        self._lst_db = self.conf_db.get_db_items()
        self._lst_panel = dict()

        for key, value in self._lst_db.items():
            self.cbo_db_source.addItem(value.get_name(), key)
            self._lst_panel[key] = value.get_config_panel()
            self._lst_panel[key].notify_message_requested.connect(self.show_message)
            self.db_layout.addWidget(self._lst_panel[key])

        self.db_source_changed()

        # Trigger some default behaviours
        self.restore_settings()

        self.cbo_db_source.currentIndexChanged.connect(self.db_source_changed)

    def showEvent(self, event):
        # It is necessary to reload the variables
        # to load the database and schema name
        self.restore_settings()

    def _get_db_connector_from_gui(self):
        current_db = self.cbo_db_source.currentData()
        params = self._lst_panel[current_db].read_connection_parameters()
        db = self._lst_db[current_db].get_db_connector(params)

        return db

    def get_db_connection(self):
        if self._db is not None:
            self.log.logMessage("Returning existing db connection...", PLUGIN_NAME, Qgis.Info)
        else:
            self.log.logMessage("Getting new db connection...", PLUGIN_NAME, Qgis.Info)
            self._db = self._get_db_connector_from_gui()

        return self._db

    def accepted(self):
        current_db = self.cbo_db_source.currentData()
        if self._lst_panel[current_db].state_changed():
            valid_connection = True
            ladm_col_schema = False

            db = self._get_db_connector_from_gui()

            test_level = EnumTestLevel.DB_SCHEMA

            res, msg = db.test_connection(test_level=test_level)

            if res:
                ladm_col_schema, msg = db.test_connection(test_level=EnumTestLevel.LADM)
            else:
                self.show_message(msg, Qgis.Warning)
                valid_connection = False

            if valid_connection:
                if self._db is not None:
                    self._db.close_connection()

                # FIXME is it overwriting itself?
                self._db = None
                self._db = self.get_db_connection()

                self.official_db_connection_changed.emit(self._db, ladm_col_schema)

                self.save_settings()
                QDialog.accept(self)  # TODO remove?
            else:
                return  # Do not close the dialog

        else:
            QDialog.accept(self)  # TODO remove?

    def reject(self):
        self.done(0)

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
        settings.setValue('Asistente-LADM_COL/official_db/db_connection_source', self.cbo_db_source.currentData())

        # Save QSettings
        current_db = self.cbo_db_source.currentData()
        dict_conn = self._lst_panel[current_db].read_connection_parameters()

        for key, value in dict_conn.items():
            settings.setValue('Asistente-LADM_COL/official_db/' + current_db + '/' + key, value)

    def _restore_settings_db(self):
        settings = QSettings()
        # reload all panels
        for index_db, item_db in self._lst_panel.items():
            dict_conn = dict()
            keys = item_db.get_keys_connection_parameters()
            for key in keys:
                dict_conn[key] = settings.value('Asistente-LADM_COL/official_db/' + index_db + '/' + key)

            item_db.write_connection_parameters(dict_conn)
            item_db.save_state()

    def restore_settings(self):
        # Restore QSettings
        settings = QSettings()
        default_db = self.conf_db.id_default_db

        index_db = self.cbo_db_source.findData(settings.value('Asistente-LADM_COL/official_db/db_connection_source', default_db))

        if index_db == -1:
            index_db = self.cbo_db_source.findData(default_db)

        self.cbo_db_source.setCurrentIndex(index_db)
        self.db_source_changed()

        self._restore_settings_db()

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
        self.log.logMessage("Test connection!", PLUGIN_NAME, Qgis.Info)

    def test_ladm_col_structure(self):
        db = self._get_db_connector_from_gui()
        res, msg = db.test_connection(test_level=EnumTestLevel.LADM)

        if db is not None:
            db.close_connection()

        self.show_message(msg, Qgis.Info if res else Qgis.Warning)
        self.log.logMessage("Test connection!", PLUGIN_NAME, Qgis.Info)

    def show_message(self, message, level):
        self.bar.pushMessage(message, level, 10)

    def show_help(self):
        self.qgis_utils.show_help("settings")
