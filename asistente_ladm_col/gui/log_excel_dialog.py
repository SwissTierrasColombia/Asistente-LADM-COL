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
import os
import time
from qgis.core import Qgis
from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.QtPrintSupport import QPrinter
from qgis.PyQt.QtWidgets import (QFileDialog,
                                 QDialogButtonBox)
from qgis.PyQt.QtCore import (QCoreApplication,
                              QSettings)
from ..utils import get_ui_class
from asistente_ladm_col.utils.utils import Utils
from ..utils.qt_utils import normalize_local_url
from .dialog_import_from_excel import DialogImportFromExcel

LOG_DIALOG_EXCEL_UI = get_ui_class('dlg_log_excel.ui')

class LogExcelDialog(QDialog, LOG_DIALOG_EXCEL_UI):
    def __init__(self, iface, db, qgis_utils, Utils, text, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self._db = db
        self.qgis_utils = qgis_utils
        self.utils = Utils
        self.dialog_excel = DialogImportFromExcel(self.iface, self._db, self.qgis_utils, self.utils)
 
        # Set connections
        self.buttonBox.accepted.connect(self.save)

        self.buttonBox.button(QDialogButtonBox.Save).setText(QCoreApplication.translate("LogQualityDialog", "Export to PDF"))
        self.txt_log_excel.setHtml(text)
        
    def save(self):
        print (self.txt_log_excel)

