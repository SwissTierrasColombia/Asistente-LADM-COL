# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-06-09
        git sha              : :%H$
        copyright            : (C) 2018 by Germán Carrillo (BSF Swissphoto)
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

from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtWidgets import QDialog

from ..utils import get_ui_class


DIALOG_UI = get_ui_class('upload_progress_dialog.ui')

class UploadProgressDialog(QDialog, DIALOG_UI):
    def __init__(self, total_steps, not_found, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.total_steps = total_steps
        self.not_found = not_found
        self.set_total_process_label(0)
        self.total_progress_bar.setRange(0, total_steps)
        self.current_progress_bar.setRange(0, 0)
        self.buttonBox.setEnabled(False)

    def set_total_process_label(self, step):
        message = ''
        if self.not_found:
            message = QCoreApplication.translate("UploadProgressDialog",
                "Uploading {} out of {} files ({} files not found in the local disk)").format(
                    step + 1,
                    self.total_steps,
                    self.not_found)
        else:
            message = QCoreApplication.translate("UploadProgressDialog",
                "Uploading {} out of {} files").format(
                    step + 1,
                    self.total_steps)

        self.lbl_total_process.setText(message)

    def update_total_progress(self, step):
        self.total_progress_bar.setValue(step)
        self.set_total_process_label(step)

    def update_current_progress(self, current, total):
        print(current, total)
        if total == 0 and current == 0 or total == -1:
            self.current_progress_bar.setRange(0, 0)
        elif total > 0:
            self.current_progress_bar.setRange(0, 100)
            self.current_progress_bar.setValue(100 * current/total)
