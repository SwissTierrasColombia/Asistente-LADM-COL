# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-02-06
        git sha              : :%H$
        copyright            : (C) 2019 by Jhon Galindo
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
from ...utils import get_ui_class
from ...utils.qt_utils import save_pdf_format

DIALOG_LOG_EXCEL_UI = get_ui_class('dialogs/dlg_log_excel.ui')


class LogExcelDialog(QDialog, DIALOG_LOG_EXCEL_UI):
    def __init__(self, qgis_utils, text, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.qgis_utils = qgis_utils
        self.buttonBox.accepted.connect(self.save)
        self.buttonBox.button(QDialogButtonBox.Save).setText(QCoreApplication.translate("LogExcelDialog", "Export to PDF"))
        self.txt_log_excel.setHtml(text)
        self.export_text = text

    def save(self):
        title = QCoreApplication.translate("LogExcelDialog","<h2 align='center'>Errors importing from Excel into LADM-COL</h2>")
        save_pdf_format(self.qgis_utils, 'Asistente-LADM_COL/log_excel_dialog/save_path', title, self.export_text )
