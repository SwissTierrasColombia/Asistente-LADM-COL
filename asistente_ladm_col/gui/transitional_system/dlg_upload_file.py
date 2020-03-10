# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-02-11
        git sha              : :%H$
        copyright            : (C) 2020 by Germán Carrillo (Swissphoto BSF)
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
import os.path

from qgis.core import Qgis
from qgis.PyQt.QtWidgets import (QDialog,
                                 QSizePolicy,
                                 QDialogButtonBox)
from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication,
                              QSettings,
                              pyqtSignal)
from qgis.gui import QgsMessageBar

from asistente_ladm_col.utils.qt_utils import (make_file_selector,
                                               ProcessWithStatus)
from asistente_ladm_col.utils.st_utils import STUtils
from asistente_ladm_col.utils.ui import get_ui_class
from asistente_ladm_col.utils.utils import Utils

DIALOG_TRANSITION_SYSTEM_UI = get_ui_class('transitional_system/dlg_upload_file.ui')


class STUploadFileDialog(QDialog, DIALOG_TRANSITION_SYSTEM_UI):
    on_result = pyqtSignal(bool)  # whether the tool was run successfully or not

    def __init__(self, request_id, supply_type, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.request_id = request_id
        self.supply_type = supply_type
        self.st_utils = STUtils()

        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.upload_file)
        self.buttonBox.helpRequested.connect(self.show_help)
        self.btn_browse_file.clicked.connect(
            make_file_selector(self.txt_file_path,
                               QCoreApplication.translate("STUploadFileDialog",
                                                          "Select the file you want to upload to the transitional system"),
                               QCoreApplication.translate("STUploadFileDialog",
                                                          'INTERLIS 2 transfer format (*.xtf)')))

        self.initialize_progress()

        self.restore_settings()

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

    def upload_file(self):
        self.bar.clearWidgets()
        self.start_progress()
        self.enable_controls(False)

        file_path = self.txt_file_path.text().strip()
        if not self.txt_comments.toPlainText():
            res = False
            res_msg = QCoreApplication.translate("STUploadFileDialog", "File was not uploaded! Details: Comments are required.")
        elif os.path.isfile(file_path):
            zip_file_path = Utils.compress_file(file_path)
            with ProcessWithStatus(QCoreApplication.translate("STUploadFileDialog", "Uploading file to ST server...")):
                res, res_msg = self.st_utils.upload_file(self.request_id, self.supply_type, zip_file_path, self.txt_comments.toPlainText())
        else:
            res = False
            res_msg = QCoreApplication.translate("STUploadFileDialog", "The file '{}' does not exist!").format(file_path)

        self.show_message(res_msg, Qgis.Success if res else Qgis.Warning)

        self.initialize_progress()

        if res:
            self.store_settings()
        else:
            self.enable_controls(True)  # Prepare next run

        self.on_result.emit(res)  # Inform other classes if the execution was successful

        return  # Do not close dialog

    def show_message(self, message, level):
        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.bar.pushMessage(message, level, 0)

    def store_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/QgisModelBaker/ili2pg/xtffile_export', self.txt_file_path.text().strip())

    def restore_settings(self):
        settings = QSettings()
        self.txt_file_path.setText(settings.value('Asistente-LADM_COL/QgisModelBaker/ili2pg/xtffile_export'))

    def start_progress(self):
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)

    def initialize_progress(self):
        self.progress.setVisible(False)

    def enable_controls(self, enable):
        self.gbx_page_1.setEnabled(enable)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(enable)

    def show_help(self):
        # self.qgis_utils.show_help("settings")
        pass