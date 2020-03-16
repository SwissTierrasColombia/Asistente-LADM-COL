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
                                 QSizePolicy)
from qgis.gui import QgsMessageBar

from asistente_ladm_col.config.general_config import (SUPPLIES_DB_SOURCE,
                                                      COLLECTED_DB_SOURCE,
                                                      SETTINGS_CONNECTION_TAB_INDEX)
from asistente_ladm_col.config.ladm_names import LADMNames
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

        # we will use a unique instance of setting dialog
        self.settings_dialog = SettingsDialog(qgis_utils=self.qgis_utils, conn_manager=self.conn_manager)
        # The database configuration is saved if it becomes necessary
        # to restore the configuration when the user rejects the dialog
        self.init_db_collected = None
        self.init_db_supplies = None
        self.set_init_db_config()  # Always call after the settings_dialog variable is set

        self._db_collected = self.conn_manager.get_db_connector_from_source()
        self._db_supplies = self.conn_manager.get_db_connector_from_source(SUPPLIES_DB_SOURCE)

        # There may be 1 case where we need to emit a db_connection_changed from the change detection settings dialog:
        #   1) Connection Settings was opened and the DB conn was changed.
        self._db_collected_was_changed = False  # To postpone calling refresh gui until we close this dialog instead of settings
        self._db_supplies_was_changed = False

        # Similarly, we could call a refresh on layers and relations cache in 1 case:
        #   1) If the change detection settings dialog was called for the COLLECTED source: opening Connection Settings
        #      and changing the DB connection.
        self._schedule_layers_and_relations_refresh = False

        for mode, label_mode in self.CHANGE_DETECTIONS_MODES.items():
            self.cbo_change_detection_modes.addItem(label_mode, mode)

        self.radio_button_other_db.setChecked(True)  # Default option
        self.radio_button_same_db.setEnabled(True)
        if not self._db_collected.supplies_model_exists():
            self.radio_button_same_db.setEnabled(False)

        self.radio_button_same_db.toggled.connect(self.update_supplies_db_options)
        self.update_supplies_db_options()

        self.btn_collected_db.clicked.connect(self.show_settings_collected_db)
        self.btn_supplies_db.clicked.connect(self.show_settings_supplies_db)

        # Default color error labels
        self.lbl_msg_collected.setStyleSheet('color: orange')
        self.lbl_msg_supplies.setStyleSheet('color: orange')

        # Set connections
        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.helpRequested.connect(self.show_help)

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

        self.update_connection_info()

        self.logger.clear_message_bar()  # Close any existing message in QGIS message bar

    def set_init_db_config(self):
        """
         A copy of the initial connections to the database is made,
         User can change the initial connections and then cancel the changes.
         Initial connections need to be re-established
        """
        self.init_db_collected = self.conn_manager.get_db_connector_from_source(COLLECTED_DB_SOURCE)
        self.init_db_supplies = self.conn_manager.get_db_connector_from_source(SUPPLIES_DB_SOURCE)

    def update_supplies_db_options(self):
        if self.radio_button_same_db.isChecked():
            self.btn_supplies_db.setEnabled(False)
        else:
            self.btn_supplies_db.setEnabled(True)
        self.update_connection_info()

    def show_settings_collected_db(self):
        self.settings_dialog.set_db_source(COLLECTED_DB_SOURCE)
        self.settings_dialog.set_tab_pages_list([SETTINGS_CONNECTION_TAB_INDEX])
        self.settings_dialog.set_required_models([LADMNames.OPERATION_MODEL_PREFIX])
        self.settings_dialog.db_connection_changed.connect(self.db_connection_changed)

        if self.settings_dialog.exec_():
            self._db_collected = self.settings_dialog.get_db_connection()
            self.update_connection_info()
        self.settings_dialog.db_connection_changed.disconnect(self.db_connection_changed)

    def show_settings_supplies_db(self):
        self.settings_dialog.set_db_source(SUPPLIES_DB_SOURCE)
        self.settings_dialog.set_tab_pages_list([SETTINGS_CONNECTION_TAB_INDEX])
        self.settings_dialog.set_required_models([LADMNames.SUPPLIES_MODEL_PREFIX])
        self.settings_dialog.db_connection_changed.connect(self.db_connection_changed)

        if self.settings_dialog.exec_():
            self._db_supplies = self.settings_dialog.get_db_connection()
            self.update_connection_info()
        self.settings_dialog.db_connection_changed.disconnect(self.db_connection_changed)

    def db_connection_changed(self, db, ladm_col_db, db_source):
        # We dismiss parameters here, after all, we already have the db, and the ladm_col_db
        # may change from this moment until we close the import schema dialog
        if db_source == COLLECTED_DB_SOURCE:
            self._db_collected_was_changed = True
            self._schedule_layers_and_relations_refresh = True
        else:
            self._db_supplies_was_changed = True

    def update_connection_info(self):
        # Validate db connections
        self.lbl_msg_collected.setText("")
        self.lbl_msg_supplies.setText("")
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        # First, update status of same_db button according to collected db connection
        res_collected, code_collected, msg_collected = self._db_collected.test_connection(required_models=[LADMNames.OPERATION_MODEL_PREFIX])
        res_supplies, code_supplies, msg_supplies = self._db_collected.test_connection(required_models=[LADMNames.SUPPLIES_MODEL_PREFIX])

        if res_supplies:
            self.radio_button_same_db.setEnabled(True)
        else:
            self.radio_button_same_db.setChecked(False)  # signal update the label

        if not self.radio_button_same_db.isChecked():
            res_supplies, code_supplies, msg_supplies = self._db_supplies.test_connection(required_models=[LADMNames.SUPPLIES_MODEL_PREFIX])

        # Update collected db connection label
        db_description = self._db_collected.get_description_conn_string()
        if db_description:
            self.db_collected_connect_label.setText(db_description)
            self.db_collected_connect_label.setToolTip(self._db_collected.get_display_conn_string())
        else:
            self.db_collected_connect_label.setText(QCoreApplication.translate("ChangeDetectionSettingsDialog", "The database is not defined!"))
            self.db_collected_connect_label.setToolTip('')

        # Update supplies db connection label
        if self.radio_button_same_db.isChecked():
            self.db_supplies_connect_label.setText(self.db_collected_connect_label.text())
            self.db_supplies_connect_label.setToolTip(self.db_collected_connect_label.toolTip())
        else:
            db_description = self._db_supplies.get_description_conn_string()
            if db_description:
                self.db_supplies_connect_label.setText(db_description)
                self.db_supplies_connect_label.setToolTip(self._db_supplies.get_display_conn_string())
            else:
                self.db_supplies_connect_label.setText(QCoreApplication.translate("ChangeDetectionSettingsDialog", "The database is not defined!"))
                self.db_supplies_connect_label.setToolTip('')

        # Update error message labels
        if not res_collected:
            self.lbl_msg_collected.setText(QCoreApplication.translate("ChangeDetectionSettingsDialog", "Warning: DB connection is not valid"))
            self.lbl_msg_collected.setToolTip(msg_collected)

        if not res_supplies:
            self.lbl_msg_supplies.setText(QCoreApplication.translate("ChangeDetectionSettingsDialog", "Warning: DB connection is not valid"))
            self.lbl_msg_supplies.setToolTip(msg_supplies)

        if res_collected and res_supplies:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)

    def accepted(self):
        """
        Confirm changes in db connections.
        If user select collected db as supplies db we update supplies db connection with collected db connection.

        If there are layers loaded in canvas from a previous connection that changed, we ask users
        if they want to clean the canvas or preserve the layers.

        If none of the connections changed, the dialog is closed without asking anything to users, and an info message
        is displayed.
        """
        if self.radio_button_same_db.isChecked():
            # Set supplies db connector from collected db connector
            self.conn_manager.save_parameters_conn(self._db_collected, SUPPLIES_DB_SOURCE)
            self._db_supplies = self._db_collected
            self.conn_manager.db_connection_changed.emit(self._db_supplies, self._db_supplies.test_connection()[0], SUPPLIES_DB_SOURCE)

        # Show messages when closing dialog
        if self._db_collected_was_changed or self._db_supplies_was_changed:
            if list(QgsProject.instance().mapLayers().values()):
                message = ""
                if self._db_collected_was_changed and self._db_supplies_was_changed:
                    message = "The connection of the collected and supplies databases has changed,"
                elif self._db_collected_was_changed:
                    message = "The collected database connection has changed,"
                elif self._db_supplies_was_changed:
                    message = "The supplies database connection has changed,"

                message += " do you want to remove the layers that are currently loaded in QGIS?"
                self.show_message_clean_layers_panel(message)
                self.show_message_change_detection_settings_status()  # Show information message indicating if setting is OK
            else:
                self.close_dialog(QDialog.Accepted)
        else:
            # Connections have not changed
            self.close_dialog(QDialog.Accepted)

    def show_message_change_detection_settings_status(self):
        if not self.collected_db_is_valid() and not self.supplies_db_is_valid():
            message = QCoreApplication.translate("ChangeDetectionSettingsDialog", "Neither Collected nor Supplies database connections is valid, you should first configure them before proceeding to detect changes.")
            self.logger.warning_msg(__name__, message, 5)
        elif not self.collected_db_is_valid() or not self.supplies_db_is_valid():

            if not self.collected_db_is_valid():
                message = QCoreApplication.translate("ChangeDetectionSettingsDialog", "Collected database connection is not valid, you should first configure it before proceeding to detect changes.")
                self.logger.warning_msg(__name__, message, 5)

            if not self.supplies_db_is_valid():
                message = QCoreApplication.translate("ChangeDetectionSettingsDialog", "Supplies database connection is not valid, you should first configure it before proceeding to detect changes.")
                self.logger.warning_msg(__name__, message, 5)
        else:
            message = QCoreApplication.translate("ChangeDetectionSettingsDialog", "Both Collected and Supplies database connections are valid, now you can proceed to detect changes.")
            self.logger.message_with_buttons_change_detection_all_and_per_parcel_emitted.emit(message)

    def show_message_clean_layers_panel(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setText(message)
        msg.setWindowTitle(QCoreApplication.translate("ChangeDetectionSettingsDialog", "Remove layers?"))
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        msg.button(QMessageBox.Yes).setText(QCoreApplication.translate("ChangeDetectionSettingsDialog", "Yes, remove layers"))
        msg.button(QMessageBox.No).setText(QCoreApplication.translate("ChangeDetectionSettingsDialog", "No, don't remove"))
        reply = msg.exec_()

        if reply == QMessageBox.Yes:
            QgsProject.instance().layerTreeRoot().removeAllChildren()
            self.close_dialog(QDialog.Accepted)
        elif reply == QMessageBox.No:
            self.close_dialog(QDialog.Accepted)
        elif reply == QMessageBox.Cancel:
            pass  # Continue config db connections

    def collected_db_is_valid(self):
        res, foo, bar = self._db_collected.test_connection(required_models=[LADMNames.OPERATION_MODEL_PREFIX])
        return res

    def supplies_db_is_valid(self):
        res, foo, bar = self._db_supplies.test_connection(required_models=[LADMNames.SUPPLIES_MODEL_PREFIX])
        return res

    def reject(self):
        self.close_dialog(QDialog.Rejected)

    def close_dialog(self, result):
        """
        We use this slot to be safe when emitting the db_connection_changed (should be done at the end), otherwise we
        could trigger slots that unload the plugin, destroying dialogs and thus, leading to crashes.
        """
        if result == QDialog.Accepted:
            if self._schedule_layers_and_relations_refresh:
                self.conn_manager.db_connection_changed.connect(self.qgis_utils.cache_layers_and_relations)

            if self._db_collected_was_changed:
                self.conn_manager.db_connection_changed.emit(self._db_collected,
                                                             self._db_collected.test_connection()[0],
                                                             COLLECTED_DB_SOURCE)

            if self._db_supplies_was_changed:
                self.conn_manager.db_connection_changed.emit(self._db_supplies,
                                                             self._db_supplies.test_connection()[0],
                                                             SUPPLIES_DB_SOURCE)

            if self._schedule_layers_and_relations_refresh:
                self.conn_manager.db_connection_changed.disconnect(self.qgis_utils.cache_layers_and_relations)

        elif result == QDialog.Rejected:
            # Go back to initial connections and don't emit db_connection_changed
            if self._db_collected_was_changed:
                self.conn_manager.save_parameters_conn(self.init_db_collected, COLLECTED_DB_SOURCE)

            if self._db_supplies_was_changed:
                self.conn_manager.save_parameters_conn(self.init_db_supplies, SUPPLIES_DB_SOURCE)

        self.show_message_change_detection_settings_status()  # Show information message indicating whether setting is OK
        self.logger.info(__name__, "Dialog closed.")
        self.done(result)

    def show_help(self):
        self.qgis_utils.show_help("change_detection_settings")
