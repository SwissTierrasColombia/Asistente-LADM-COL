# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-01-15
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
import time
from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.QtWidgets import QDialogButtonBox
from qgis.PyQt.QtCore import (QCoreApplication,
                              QSettings)
from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.qt_utils import save_pdf_format

DIALOG_LOG_QUALITY_UI = get_ui_class('dialogs/dlg_log_quality.ui')


class LogQualityDialog(QDialog, DIALOG_LOG_QUALITY_UI):
    def __init__(self, quality, db, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.quality = quality
        self.db = db

        # Set connections
        self.buttonBox.accepted.connect(self.save)

        self.buttonBox.button(QDialogButtonBox.Save).setText(QCoreApplication.translate("LogQualityDialog", "Export to PDF"))
        self.text, self.total_time = self.quality.get_log_dialog_quality_text()
        self.txt_log_quality.setHtml(self.text)

    def save(self):
        text, total_time = self.quality.get_log_dialog_quality_text()
        title = QCoreApplication.translate(
                "LogQualityDialog",
                "<h2 align='center'>Quality Check Results</h2><div style='text-align:center;'>{}<br>Database: {}<br>Total execution time: {}</div>").format(
                time.strftime("%d/%m/%y %H:%M:%S"), self.db.get_description_conn_string(),
                self.quality.utils.set_time_format(total_time))

        save_pdf_format('Asistente-LADM-COL/log_quality_dialog/save_path', title, text)

