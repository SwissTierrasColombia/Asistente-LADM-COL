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
from qgis.PyQt.QtCore import QCoreApplication
from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.qt_utils import save_pdf_format
from asistente_ladm_col.utils.utils import Utils

DIALOG_LOG_QUALITY_UI = get_ui_class('dialogs/dlg_log_quality.ui')


class LogQualityDialog(QDialog, DIALOG_LOG_QUALITY_UI):
    def __init__(self, db, text, tolerance, total_time, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.db = db

        # Set connections
        self.buttonBox.accepted.connect(self.save)

        self.buttonBox.button(QDialogButtonBox.Save).setText(QCoreApplication.translate("LogQualityDialog", "Export to PDF"))
        self.text = text
        self.tolerance = tolerance
        self.execution_total_time = total_time
        self.txt_log_quality.setHtml(self.text)
        self.lbl_tolerance.setText(self.lbl_tolerance.text().format(self.tolerance))

    def save(self):
        title = QCoreApplication.translate(
                "LogQualityDialog",
                "<h2 align='center'>Quality Check Results</h2><div style='text-align:center;'>{}<br>Database: {}<br>Total execution time: {}<br>Tolerance {}mm.</div>").format(
                    time.strftime("%d/%m/%y %H:%M:%S"),
                    self.db.get_description_conn_string(),
                    Utils.set_time_format(self.execution_total_time),
                    self.tolerance)

        save_pdf_format('Asistente-LADM-COL/log_quality_dialog/save_path', title, self.text)

