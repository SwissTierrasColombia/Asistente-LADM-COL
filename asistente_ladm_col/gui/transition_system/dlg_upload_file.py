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
from qgis.core import Qgis
from qgis.PyQt.QtWidgets import (QDialog,
                                 QSizePolicy)
from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication,
                              QSettings)
from qgis.gui import QgsMessageBar

from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.qt_utils import make_file_selector
from asistente_ladm_col.utils.st_utils import STUtils

DIALOG_TRANSITION_SYSTEM_UI = get_ui_class('transition_system/dlg_upload_file.ui')


class STUploadFileDialog(QDialog, DIALOG_TRANSITION_SYSTEM_UI):
    def __init__(self, request_id, supply_type, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.request_id = request_id
        self.supply_type = supply_type
        self.st_utils = STUtils()

        self.buttonBox.accepted.connect(self.upload_file)
        self.buttonBox.helpRequested.connect(self.show_help)
        self.btn_browse_file.clicked.connect(
            make_file_selector(self.txt_file_path,
                               QCoreApplication.translate("STUploadFileDialog",
                                                          "Select the file you want to upload to the transition system"),
                               QCoreApplication.translate("STUploadFileDialog",
                                                          'INTERLIS 2 transfer format (*.xtf)')))

        self.progress.setVisible(False)

        self.restore_settings()

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

    def upload_file(self):
        res, msg = self.st_utils.upload_file(self.request_id, self.supply_type, self.txt_file_path.text().strip(), self.txt_comments.toPlainText())
        self.show_message(msg, Qgis.Success if res else Qgis.Warning)

    def show_message(self, message, level):
        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.bar.pushMessage(message, level, 0)

    def restore_settings(self):
        settings = QSettings()
        self.txt_file_path.setText(settings.value('Asistente-LADM_COL/QgisModelBaker/ili2pg/xtffile_export'))

    def show_help(self):
        # self.qgis_utils.show_help("settings")
        pass