# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-12-20
        git sha              : :%H$
        copyright            : (C) 2019 by Leo Cardona (BSF Swissphoto)
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

from qgis.core import QgsProject
from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QDialogButtonBox,
                                 QMessageBox,
                                 QPushButton,
                                 QSizePolicy)
from qgis.gui import QgsMessageBar

from asistente_ladm_col.config.general_config import (SUPPLIES_DB_SOURCE,
                                                      COLLECTED_DB_SOURCE,
                                                      SETTINGS_CONNECTION_TAB_INDEX)
from asistente_ladm_col.config.mapping_config import LADMNames
from asistente_ladm_col.gui.dialogs.dlg_settings import SettingsDialog
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.config.help_strings import HelpStrings

DIALOG_UI = get_ui_class('change_detection/dlg_change_detection_settings.ui')


class ChangeDetectionSettingsDialog(QDialog, DIALOG_UI):
    CHANGE_DETECTIONS_MODE_SUPPLIES_MODEL = "CHANGE_DETECTIONS_MODE_SUPPLIES_MODEL"
    CHANGE_DETECTIONS_MODES = {CHANGE_DETECTIONS_MODE_SUPPLIES_MODEL: QCoreApplication.translate("ChangeDetectionSettingsDialog", "Change detection supplies model")}

    def __init__(self, parent=None, qgis_utils=None, conn_manager=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.logger = Logger()
        self.help_strings = HelpStrings()
        self.txt_help_page.setHtml(self.help_strings.CHANGE_DETECTION_SETTING_DIALOG_HELP)

        self.conn_manager = conn_manager
        self.qgis_utils = qgis_utils
        self._db_collected = self.conn_manager.get_db_connector_from_source()
        self._db_supplies = self.conn_manager.get_db_connector_from_source(SUPPLIES_DB_SOURCE)

        # To postpone calling refresh gui until we close this dialog instead of settings
        self._db_collected_was_changed = False
        self._db_supplies_was_changed = False

        # The database configuration is saved if it becomes necessary
        # to restore the configuration when the user rejects the dialog
        self._init_db_collected_active_mode = None
        self._init_db_supplies_active_mode = None
        self._init_db_collected_dict_config = dict()
        self._init_db_supplies_dict_config = dict()
        self.set_init_db_config()

        for mode, label_mode in self.CHANGE_DETECTIONS_MODES.items():
            self.cbo_change_detection_modes.addItem(label_mode, mode)

        self.radio_button_other_db.setChecked(True)
        self.radio_button_same_db.setEnabled(True)
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

        self.update_connection_info(COLLECTED_DB_SOURCE)
        self.update_connection_info(SUPPLIES_DB_SOURCE)

    def set_init_db_config(self):
        dlg_collected_config = SettingsDialog(qgis_utils=self.qgis_utils, conn_manager=self.conn_manager, db_source=COLLECTED_DB_SOURCE)
        dlg_supplies_config = SettingsDialog(qgis_utils=self.qgis_utils, conn_manager=self.conn_manager, db_source=SUPPLIES_DB_SOURCE)

        self._init_db_collected_active_mode = dlg_collected_config.cbo_db_engine.itemData(dlg_collected_config.cbo_db_engine.currentIndex())
        self._init_db_supplies_active_mode = dlg_supplies_config.cbo_db_engine.itemData(dlg_supplies_config.cbo_db_engine.currentIndex())

        for id_db, db_factory in dlg_collected_config._lst_db.items():
            dict_conn = db_factory.get_parameters_conn(COLLECTED_DB_SOURCE)
            self._init_db_collected_dict_config[id_db] = dict_conn

        for id_db, db_factory in dlg_supplies_config._lst_db.items():
            dict_conn = db_factory.get_parameters_conn(SUPPLIES_DB_SOURCE)
            self._init_db_supplies_dict_config[id_db] = dict_conn

    def update_supplies_db_options(self):
        if self.radio_button_same_db.isChecked():
            self.btn_supplies_db.setEnabled(False)
        else:
            self.btn_supplies_db.setEnabled(True)
        self.update_connection_info(SUPPLIES_DB_SOURCE)

    def show_settings_collected_db(self):
        tab_pages_list = [SETTINGS_CONNECTION_TAB_INDEX]
        dlg = SettingsDialog(qgis_utils=self.qgis_utils, conn_manager=self.conn_manager, tab_pages_list=tab_pages_list)
        dlg.set_required_models([LADMNames.OPERATION_MODEL_PREFIX])

        # Connect signals (DBUtils, QgisUtils)
        dlg.db_connection_changed.connect(self.db_connection_changed)
        dlg.db_connection_changed.connect(self.qgis_utils.cache_layers_and_relations)

        if dlg.exec_():
            self._db_collected = dlg.get_db_connection()
            self.update_connection_info(COLLECTED_DB_SOURCE)

    def show_settings_supplies_db(self):
        tab_pages_list = [SETTINGS_CONNECTION_TAB_INDEX]
        dlg = SettingsDialog(qgis_utils=self.qgis_utils, conn_manager=self.conn_manager, db_source=SUPPLIES_DB_SOURCE, tab_pages_list=tab_pages_list)
        dlg.set_required_models([LADMNames.SUPPLIES_MODEL_PREFIX])
        dlg.db_connection_changed.connect(self.db_connection_changed)

        if dlg.exec_():
            self._db_supplies = dlg.get_db_connection()
            self.update_connection_info(SUPPLIES_DB_SOURCE)

    def db_connection_changed(self, db, ladm_col_db, db_source):
        # We dismiss parameters here, after all, we already have the db, and the ladm_col_db
        # may change from this moment until we close the import schema dialog
        if db_source == COLLECTED_DB_SOURCE:
            self._db_collected_was_changed = True
        else:
            self._db_supplies_was_changed = True

    def close_dialog(self):
        if self._db_collected_was_changed:
            self.conn_manager.db_connection_changed.emit(self._db_collected, self._db_collected.test_connection()[0], COLLECTED_DB_SOURCE)

        if self._db_supplies_was_changed:
            self.conn_manager.db_connection_changed.emit(self._db_supplies, self._db_supplies.test_connection()[0], SUPPLIES_DB_SOURCE)

        self.logger.info(__name__, "Dialog closed.")
        self.done(0)

    def update_connection_info(self, db_source):
        # Validate db connections
        self.lb_msg_collected.setText("")
        self.lb_msg_supplies.setText("")
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        if self._db_collected.test_connection()[0] and self.radio_button_same_db.isChecked():
            if not self._db_collected.operation_model_exists():
                self.lb_msg_collected.setText("Warning: DB connection is not valid")
                self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            else:
                self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        if self._db_collected.test_connection()[0] and self._db_supplies.test_connection()[0]:
            if not self._db_supplies.supplies_model_exists() or not self._db_collected.operation_model_exists():
                if not self._db_collected.operation_model_exists():
                    self.lb_msg_collected.setText("Warning: DB connection is not valid")
                    self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

                if not self._db_supplies.supplies_model_exists():
                    self.lb_msg_supplies.setText("Warning: DB connection is not valid")
                    self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            else:
                self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)

        # validate selected db
        if self._db_collected.supplies_model_exists():
            self.radio_button_same_db.setEnabled(True)
            if self.radio_button_same_db.isChecked():
                self.db_supplies_connect_label.setText(self.db_collected_connect_label.text())
        else:
            self.radio_button_same_db.setEnabled(False)
            if self.radio_button_same_db.isChecked():
                self.radio_button_same_db.setChecked(False) # signal update the label

        if db_source == COLLECTED_DB_SOURCE:
            db_description = self._db_collected.get_description_conn_string()
            if db_description:
                self.db_collected_connect_label.setText(db_description)
                self.db_collected_connect_label.setToolTip(self._db_collected.get_display_conn_string())
            else:
                self.db_collected_connect_label.setText(QCoreApplication.translate("DialogImportSchema", "The database is not defined!"))
                self.db_collected_connect_label.setToolTip('')
        elif db_source == SUPPLIES_DB_SOURCE:
            if self.radio_button_same_db.isChecked():
                self.db_supplies_connect_label.setText(self.db_collected_connect_label.text())
            else:
                db_description = self._db_supplies.get_description_conn_string()
                if db_description:
                    self.db_supplies_connect_label.setText(db_description)
                    self.db_supplies_connect_label.setToolTip(self._db_supplies.get_display_conn_string())
                else:
                    self.db_supplies_connect_label.setText(QCoreApplication.translate("DialogImportSchema", "The database is not defined!"))
                    self.db_supplies_connect_label.setToolTip('')

    def accepted(self):
        if self.radio_button_same_db.isChecked():
            # Get collected db dict config
            dlg_collected_setting = SettingsDialog(qgis_utils=self.qgis_utils, conn_manager=self.conn_manager)
            db_collected_active_mode = dlg_collected_setting.cbo_db_engine.itemData(dlg_collected_setting.cbo_db_engine.currentIndex())
            db_collected_dict_conn = dict()

            for id_db, db_factory in dlg_collected_setting._lst_db.items():
                if id_db == db_collected_active_mode:
                    dict_conn = db_factory.get_parameters_conn(COLLECTED_DB_SOURCE)
                    db_collected_dict_conn[id_db] = dict_conn

            dlg_supplies_config = SettingsDialog(qgis_utils=self.qgis_utils, conn_manager=self.conn_manager, db_source=SUPPLIES_DB_SOURCE)
            dlg_supplies_config.set_db_connection(db_collected_active_mode, db_collected_dict_conn[db_collected_active_mode])

            self._db_supplies = dlg_supplies_config.get_db_connection()
            self.conn_manager.db_connection_changed.emit(self._db_supplies, self._db_supplies.test_connection()[0], SUPPLIES_DB_SOURCE)

        if self._db_collected_was_changed or self._db_supplies_was_changed:
            if list(QgsProject.instance().mapLayers().values()):
                message = None
                if self._db_collected_was_changed and self._db_supplies_was_changed:
                    message = "The connection of the collected and supplies database has changed,"
                elif self._db_collected_was_changed:
                    message = "The collected database connection has changed,"
                elif self._db_supplies_was_changed:
                    message = "The supplies database connection has changed,"

                message = message + " do you want to remove the layers that are loaded in the workspace?"
                self.show_message_clean_workspace(message)
            else:
                self.close_dialog()
        else:
            # Connections have not changed
            self.close_dialog()

    def show_message_clean_workspace(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setText(message)
        msg.setWindowTitle(QCoreApplication.translate("ChangeDetectionSettingsDialog", "Remove layers?"))
        msg.addButton(QPushButton(QCoreApplication.translate("ChangeDetectionSettingsDialog", "Yes, remove layers")), QMessageBox.YesRole)
        msg.addButton(QPushButton(QCoreApplication.translate("ChangeDetectionSettingsDialog", "No")), QMessageBox.NoRole)
        msg.addButton(QPushButton(QCoreApplication.translate("ChangeDetectionSettingsDialog", "Cancel")), QMessageBox.RejectRole)
        reply = msg.exec_()

        if reply == 0:  # 0 YES
            QgsProject.instance().layerTreeRoot().removeAllChildren()
            self.close_dialog()
        elif reply == 1:  # 1 NO
            self.close_dialog()
        elif reply == 2:  # 2 CANCEL
            pass  # Continue config db connections

    def reject(self):
        if self._db_collected_was_changed:
            dlg_collected_config = SettingsDialog(qgis_utils=self.qgis_utils, conn_manager=self.conn_manager, db_source=COLLECTED_DB_SOURCE)
            dlg_collected_config.set_db_connection(self._init_db_collected_active_mode, self._init_db_collected_dict_config[self._init_db_collected_active_mode])

            self._db_collected = dlg_collected_config.get_db_connection()
            self.conn_manager.db_connection_changed.emit(self._db_collected, self._db_collected.test_connection()[0], COLLECTED_DB_SOURCE)

        if self._db_supplies_was_changed:
            dlg_supplies_config = SettingsDialog(qgis_utils=self.qgis_utils, conn_manager=self.conn_manager, db_source=SUPPLIES_DB_SOURCE)
            dlg_supplies_config.set_db_connection(self._init_db_supplies_active_mode, self._init_db_supplies_dict_config[self._init_db_supplies_active_mode])

            self._db_supplies = dlg_supplies_config.get_db_connection()
            self.conn_manager.db_connection_changed.emit(self._db_supplies, self._db_supplies.test_connection()[0], SUPPLIES_DB_SOURCE)
        self.done(0)

    def show_help(self):
        self.qgis_utils.show_help("change_detection_settings")
