# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-01-15
        git sha              : :%H$
        copyright            : (C) 2019 by by Jhon Galindo
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

from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.QtPrintSupport import QPrinter
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.PyQt.QtCore import (QCoreApplication,
                              QSettings)

from ..utils import get_ui_class

LOG_DIALOG_UI = get_ui_class('log_dlg_quality.ui')

class LogDialogQuality(QDialog, LOG_DIALOG_UI):
    def __init__(self, qgis_utils, quality, iface, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.qgis_utils = qgis_utils
        self.quality = quality
        self.iface = iface

        # Set connections
        self.buttonBox.accepted.connect(self.saved)
        self.buttonBox.helpRequested.connect(self.show_help)
        self.txt_log_quality.setHtml(self.quality.send_log_dialog_quality_text())

    def saved(self):
        self.print_pdf(self.quality.send_log_dialog_quality_text())
    def show_help(self):
        self.qgis_utils.show_help("quality_rules")

    def print_pdf(self, text):

        settings = QSettings()

        new_filename, filter = QFileDialog.getSaveFileName(self,
                                           QCoreApplication.translate('LogDialogQuality', 'Save File'),
                                           os.path.expanduser("~"), filter = "PDF(*.pdf)")

        titulo = QCoreApplication.translate('LogDialogQuality', "Result topological validations - logical consistency {}_database: {}, schema: {}").format(
                time.strftime("%H:%M:%S_%d/%m/%y"), settings.value('Asistente-LADM_COL/pg/database'), 
                settings.value('Asistente-LADM_COL/pg/schema'))

        self.txt_log_quality.setHtml("<h2 align='center'>{}</h2> \n {}".format(titulo, self.quality.send_log_dialog_quality_text()))

        if new_filename:
            printer = QPrinter()
            printer.setPageSize(QPrinter.A4)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName("{}{}".format(new_filename, ".pdf"))
            self.txt_log_quality.print(printer)        
