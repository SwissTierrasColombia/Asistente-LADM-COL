# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-11-13
        git sha              : :%H$
        copyright            : (C) 2019 by Jhon Galindo (Incige SAS)
        email                : jhonsigpjc@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
import os

from qgis.PyQt.QtWidgets import (QDialog,
                                 QMessageBox,
                                 QDialogButtonBox,
                                 QSizePolicy)
from qgis.PyQt.QtCore import (Qt,
                              QSettings,
                              QCoreApplication)
from qgis.PyQt.QtGui import  QValidator
from qgis.core import (Qgis,
                       QgsProject,
                       QgsWkbTypes,
                       QgsVectorLayer,
                       QgsProcessingFeedback,
                       QgsVectorLayerJoinInfo)
from qgis.gui import QgsMessageBar

import processing

from asistente_ladm_col.config.general_config import (BLO_LIS_FILE_PATH,
                                                      SETTINGS_CONNECTION_TAB_INDEX)

from asistente_ladm_col.config.table_mapping_config import Names
from asistente_ladm_col.config.general_config import LAYER
from asistente_ladm_col.config.enums import EnumDbActionType
from asistente_ladm_col.gui.dialogs.dlg_settings import SettingsDialog
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.qt_utils import (OverrideCursor,
                                               FileValidator,
                                               DirValidator,
                                               Validators,
                                               make_file_selector,
                                               make_folder_selector)
from asistente_ladm_col.utils import get_ui_class

from asistente_ladm_col.gui.dialogs.dlg_cobol_base import CobolBaseDialog
from qgis.PyQt.uic import loadUiType, loadUi

class MissingCobolSupplies(CobolBaseDialog):
    def __init__(self, qgis_utils, db, conn_manager, parent=None):
        CobolBaseDialog.__init__(self, qgis_utils, db, conn_manager, parent)
        self.qgis_utils = qgis_utils
        self._db = db
        self.conn_manager = conn_manager
        self.parent = parent

        loadUi('/home/shade/dev/Asistente-LADM_COL/asistente_ladm_col/ui/dialogs/wig_missing_cobol_supplies_export.ui', self.target_data)
        self.target_data.setVisible(True)

        self.disable_widgets()

        self.target_data.btn_browse_file_folder_supplies.clicked.connect(
                make_folder_selector(self.target_data.txt_file_path_folder_supplies, title=QCoreApplication.translate(
                'ETLCobolDialog', 'Select folder to save data'), parent=None))

        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.accepted)

    def accepted(self):
        self.save_settings()

        if self._db.test_connection()[0]:
            reply = QMessageBox.question(self,
                QCoreApplication.translate("ETLCobolDialog", "Warning"),
                QCoreApplication.translate("ETLCobolDialog","The schema <i>{schema}</i> already has a valid LADM_COL structure.<br/><br/>If such schema has any data, loading data into it might cause invalid data.<br/><br/>Do you still want to continue?".format(schema=self._db.schema)),
                QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                with OverrideCursor(Qt.WaitCursor):
                    res_lis, msg_lis = self.load_lis_files()
                    if res_lis:
                        res_gdb, msg_gdb = self.load_gdb_files()
                        if res_gdb:
                            res_model, msg_model = self.load_model_layers()
                            if res_model:
                                self._running_etl = True
                                self.run_model_etl_cobol()
                                if not self.feedback.isCanceled():
                                    self.progress.setValue(100)
                                    self.buttonBox.clear()
                                    self.buttonBox.setEnabled(True)
                                    self.buttonBox.addButton(QDialogButtonBox.Close)
                                else:
                                    self.initialize_feedback()  # Get ready for an eventual new execution
                                self._running_etl = False
                            else:
                                self.show_message(msg_model, Qgis.Warning)
                        else:
                            self.show_message(msg_gdb, Qgis.Warning)
                    else:
                        self.show_message(msg_lis, Qgis.Warning)
        else:
            with OverrideCursor(Qt.WaitCursor):
                # TODO: if an empty schema was selected, do the magic under the hood
                # self.create_model_into_database()
                # Now execute "accepted()"
                pass

    def show_settings(self):
        dlg = SettingsDialog(qgis_utils=self.qgis_utils, conn_manager=self.conn_manager)

        # Connect signals (DBUtils, QgisUtils)
        dlg.db_connection_changed.connect(self.db_connection_changed)
        dlg.db_connection_changed.connect(self.qgis_utils.cache_layers_and_relations)

        # We only need those tabs related to Model Baker/ili2db operations
        for i in reversed(range(dlg.tabWidget.count())):
            if i not in [SETTINGS_CONNECTION_TAB_INDEX]:
                dlg.tabWidget.removeTab(i)

        dlg.set_action_type(EnumDbActionType.SCHEMA_IMPORT)  # To avoid unnecessary validations (LADM compliance)

        if dlg.exec_():
            self._db = dlg.get_db_connection()
            self.update_connection_info()

    def update_connection_info(self):
        db_description = self._db.get_description_conn_string()
        if db_description:
            self.target_data.db_connect_label.setText(db_description)
            self.target_data.db_connect_label.setToolTip(self._db.get_display_conn_string())
        else:
            self.target_data.db_connect_label.setText(
                QCoreApplication.translate("ETLCobolDialog", "The database is not defined!"))
            self.target_data.db_connect_label.setToolTip('')

    def disable_widgets(self):
        self.label_blo.setVisible(False)
        self.label_ter.setVisible(False)
        self.label_pro.setVisible(False)

        self.txt_file_path_blo.setVisible(False)
        self.txt_file_path_ter.setVisible(False)
        self.txt_file_path_pro.setVisible(False)

        self.btn_browse_file_blo.setVisible(False)
        self.btn_browse_file_ter.setVisible(False)
        self.btn_browse_file_pro.setVisible(False)