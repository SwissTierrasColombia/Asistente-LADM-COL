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
from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.QtWidgets import QDialogButtonBox
from qgis.PyQt.QtCore import QCoreApplication
from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.qt_utils import save_pdf_format

DIALOG_LOG_QUALITY_UI = get_ui_class('dialogs/dlg_log_quality.ui')


class LogQualityDialog(QDialog, DIALOG_LOG_QUALITY_UI):
    def __init__(self, db, log_result, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.db = db

        # Set connections
        self.buttonBox.accepted.connect(self.save)

        self.buttonBox.button(QDialogButtonBox.Save).setText(QCoreApplication.translate("LogQualityDialog", "Export to PDF"))
        self.log_result = log_result
        self.txt_log_quality.setHtml(self.log_result.text)
        self.lbl_tolerance.setText(self.lbl_tolerance.text().format(self.log_result.tolerance))

    def save(self):
        save_pdf_format('Asistente-LADM-COL/log_quality_dialog/save_path', self.log_result.title, self.log_result.text)

