"""
/***************************************************************************
                              Asistente LADM-COL
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
                              pyqtSignal)
from qgis.gui import QgsMessageBar

from asistente_ladm_col.utils.st_utils import STUtils
from asistente_ladm_col.utils.ui import get_ui_class
from asistente_ladm_col.utils.utils import show_plugin_help

DIALOG_TRANSITION_SYSTEM_UI = get_ui_class('supplies/dlg_upload_file.ui')


class STBaseUploadFileDialog(QDialog, DIALOG_TRANSITION_SYSTEM_UI):
    on_result = pyqtSignal(bool)  # whether the tool was run successfully or not

    def __init__(self, request_id, other_params, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.request_id = request_id
        self.other_params = other_params
        self.st_utils = STUtils()

        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.upload_file)
        self.buttonBox.helpRequested.connect(self.show_help)

        self.restore_settings()  # To update file paths, which will be used as basis in FileDialogs

        self.initialize_progress()

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

    def upload_file(self):
        self.bar.clearWidgets()
        self.start_progress()
        self.enable_controls(False)

        res, res_msg = self._upload_file()

        self._show_message(res_msg, Qgis.Success if res else Qgis.Warning)

        self.initialize_progress()

        if res:
            self.store_settings()
        else:
            self.enable_controls(True)  # Prepare next run

        self.on_result.emit(res)  # Inform other classes if the execution was successful

        return  # Do not close dialog

    def _handle_upload_file(self):
        raise NotImplementedError

    def _show_message(self, message, level):
        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.bar.pushMessage(message, level, 0)

    def store_settings(self):
        raise NotImplementedError

    def restore_settings(self):
        raise NotImplementedError

    def start_progress(self):
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)

    def initialize_progress(self):
        self.progress.setVisible(False)

    def enable_controls(self, enable):
        self.gbx_page_1.setEnabled(enable)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(enable)

    def show_help(self):
        show_plugin_help('transitional_system_upload_file')