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
                              QSettings)
from qgis.gui import QgsMessageBar

from asistente_ladm_col.utils.qt_utils import (make_file_selector,
                                               ProcessWithStatus)
from asistente_ladm_col.utils.st_utils import STUtils
from asistente_ladm_col.utils.ui import get_ui_class
from asistente_ladm_col.utils.utils import Utils

DIALOG_TRANSITION_SYSTEM_UI = get_ui_class('transitional_system/dlg_cancel_task.ui')


class STCancelTaskDialog(QDialog, DIALOG_TRANSITION_SYSTEM_UI):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.comments = ''

        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.validate_and_accept)
        self.buttonBox.helpRequested.connect(self.show_help)

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

    def validate_and_accept(self):
        self.bar.clearWidgets()

        if not self.txt_comments.toPlainText():
            res = False
            res_msg = QCoreApplication.translate("STUploadFileDialog", "Comments are required to cancel a task.")

            self.show_message(res_msg, Qgis.Success if res else Qgis.Warning)

            return  # Do not close the dialog

        self.comments = self.txt_comments.toPlainText()

        QDialog.accept(self)

    def show_message(self, message, level):
        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.bar.pushMessage(message, level, 0)

    def show_help(self):
        # self.qgis_utils.show_help("settings")
        pass