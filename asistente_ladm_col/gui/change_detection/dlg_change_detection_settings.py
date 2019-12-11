# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2017-11-20
        git sha              : :%H$
        copyright            : (C) 219 by Leo Cardona (BSF Swissphoto)
        email                : leo.cardona.p@gmail.com
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
                              QCoreApplication)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QSizePolicy)
from qgis.gui import QgsMessageBar

from asistente_ladm_col.config.general_config import (SUPPLIES_DB_SOURCE,
                                                      SETTINGS_CONNECTION_TAB_INDEX)
from asistente_ladm_col.gui.dialogs.dlg_settings import SettingsDialog
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils import get_ui_class

DIALOG_UI = get_ui_class('change_detection/dlg_change_detection_settings.ui')


class ChangeDetectionSettingsDialog(QDialog, DIALOG_UI):
    CHANGE_DETECTIONS_MODE_SUPPLIES_MODEL = "CHANGE_DETECTIONS_MODE_SUPPLIES_MODEL"
    CHANGE_DETECTIONS_MODES = {CHANGE_DETECTIONS_MODE_SUPPLIES_MODEL: QCoreApplication.translate("ChangeDetectionSettingsDialog", "Change detection supplies model")}

    def __init__(self, parent=None, qgis_utils=None, conn_manager=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.logger = Logger()

        self.conn_manager = conn_manager
        self.qgis_utils = qgis_utils
        self._db_collected = self.conn_manager.get_db_connector_from_source()
        self._db_supplies = self.conn_manager.get_db_connector_from_source(SUPPLIES_DB_SOURCE)

        self._db_collected_was_changed = False  # To postpone calling refresh gui until we close this dialog instead of settings
        self._db_supplies_was_changed = False  # To postpone calling refresh gui until we close this dialog instead of settings

        for mode, label_mode in self.CHANGE_DETECTIONS_MODES.items():
            self.cbo_change_detection_modes.addItem(label_mode, mode)

        self.radio_button_other_db.setChecked(True)
        if not self._db_collected.supplies_model_exists():
            self.radio_button_same_db.setEnabled(False)

        self.radio_button_same_db.toggled.connect(self.update_supplies_db_options)
        self.update_supplies_db_options()

        self.btn_collected_db.clicked.connect(self.show_settings_collected_db)
        self.btn_supplies_db.clicked.connect(self.show_settings_supplies_db)

        # Set connections
        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.helpRequested.connect(self.show_help)

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

        self.rejected.connect(self.close_dialog)
        self.update_connection_info_collected()
        self.update_connection_info_supplies()

    def update_supplies_db_options(self):

        if self.radio_button_same_db.isChecked():
            self.btn_supplies_db.setEnabled(False)
        else:
            self.btn_supplies_db.setEnabled(True)

    def show_settings_collected_db(self):
        tab_pages_list = [SETTINGS_CONNECTION_TAB_INDEX]
        dlg = SettingsDialog(qgis_utils=self.qgis_utils, conn_manager=self.conn_manager, tab_pages_list=tab_pages_list)

        # Connect signals (DBUtils, QgisUtils)
        dlg.db_connection_changed.connect(self.db_connection_changed)
        dlg.db_connection_changed.connect(self.qgis_utils.cache_layers_and_relations)

        if dlg.exec_():
            self._db_collected = dlg.get_db_connection()
            self.update_connection_info_collected()

    def show_settings_supplies_db(self):
        tab_pages_list = [SETTINGS_CONNECTION_TAB_INDEX]
        dlg = SettingsDialog(qgis_utils=self.qgis_utils, conn_manager=self.conn_manager, tab_pages_list=tab_pages_list)
        dlg.db_connection_changed.connect(self.db_connection_changed)

        if dlg.exec_():
            self._db_supplies = dlg.get_db_connection()
            self.update_connection_info_supplies()

    def db_connection_changed(self, db, ladm_col_db):
        # We dismiss parameters here, after all, we already have the db, and the ladm_col_db may change from this moment
        # until we close the import schema dialog
        self._db_collected_was_changed = True
        self._db_supplies_was_changed = True

    def close_dialog(self):
        if self._db_collected_was_changed:
            self.conn_manager.db_connection_changed.emit(self._db_collected, self._db_collected.test_connection()[0])

        if self._db_supplies_was_changed:
            self.conn_manager.db_connection_changed.emit(self._db_supplies, self._db_supplies.test_connection()[0])

        self.logger.info(__name__, "Dialog closed.")
        self.close()

    def update_connection_info_collected(self):
        db_description = self._db_collected.get_description_conn_string()
        if db_description:
            self.db_collected_connect_label.setText(db_description)
            self.db_collected_connect_label.setToolTip(self._db_collected.get_display_conn_string())
            #self._accept_button.setEnabled(True)
        else:
            self.db_collected_connect_label.setText(QCoreApplication.translate("DialogImportSchema", "The database is not defined!"))
            self.db_collected_connect_label.setToolTip('')
            #self._accept_button.setEnabled(False)

    def update_connection_info_supplies(self):
        db_description = self._db_supplies.get_description_conn_string()
        if db_description:
            self.db_supplies_connect_label.setText(db_description)
            self.db_supplies_connect_label.setToolTip(self._db_supplies.get_display_conn_string())
            #self._accept_button.setEnabled(True)
        else:
            self.db_supplies_connect_label.setText(QCoreApplication.translate("DialogImportSchema", "The database is not defined!"))
            self.db_supplies_connect_label.setToolTip('')
            #self._accept_button.setEnabled(False)

    def accepted(self):
        pass

    def reject(self):
        self.done(0)

    def show_help(self):
        self.qgis_utils.show_help("change_detection_settings")