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

DIALOG_TRANSITION_SYSTEM_UI = get_ui_class('transitional_system/dlg_base_upload_file.ui')


class STBaseUploadFileDialog(QDialog, DIALOG_TRANSITION_SYSTEM_UI):
    on_result = pyqtSignal(bool)  # whether the tool was run successfully or not

    def __init__(self, request_id, other_params, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self._request_id = request_id
        self._other_params = other_params
        self._st_utils = STUtils()

        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.upload_file)
        self.buttonBox.helpRequested.connect(self.show_help)

        self.restore_settings()

        self.file_layout.addWidget(self._file_widget)
        self._file_widget.setVisible(True)

        self.initialize_progress()

        self.txt_help_page.setHtml(self._get_help_text())

        self._bar = QgsMessageBar()
        self._bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self._bar, 0, 0, Qt.AlignTop)

    def upload_file(self):
        self._bar.clearWidgets()
        self.start_progress()
        self.enable_controls(False)

        res, res_msg = self._handle_upload_file()

        self._show_message(res_msg, Qgis.Success if res else Qgis.Warning)

        self.initialize_progress()

        if res:
            self.save_settings()
        else:
            self.enable_controls(True)  # Prepare next run

        self.on_result.emit(res)  # Inform other classes if the execution was successful

        return  # Do not close dialog

    def _handle_upload_file(self):
        raise NotImplementedError

    def _show_message(self, message, level):
        self._bar.clearWidgets()  # Remove previous messages before showing a new one
        self._bar.pushMessage(message, level, 0)

    def save_settings(self):
        self._file_widget.save_settings()

    def restore_settings(self):
        pass

    def start_progress(self):
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)

    def initialize_progress(self):
        self.progress.setVisible(False)

    def enable_controls(self, enable):
        self.gbx_page_1.setEnabled(enable)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(enable)

    def _get_help_text(self):
        # We expect an HTML here
        raise NotImplementedError

    def show_help(self):
        show_plugin_help('transitional_system_upload_file')
