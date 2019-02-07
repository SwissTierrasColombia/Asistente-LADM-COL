# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-01-15
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
from ..utils.qt_utils import normalize_local_url

LOG_DIALOG_UI = get_ui_class('dlg_log_quality.ui')

class LogQualityDialog(QDialog, LOG_DIALOG_UI):
    def __init__(self, qgis_utils, quality, iface, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.qgis_utils = qgis_utils
        self.quality = quality
        self.iface = iface
        # Set connections
        self.buttonBox.accepted.connect(self.save)

        self.buttonBox.button(QDialogButtonBox.Save).setText(QCoreApplication.translate("LogQualityDialog", "Export to PDF"))
        text, total_time = self.quality.get_log_dialog_quality_text()
        self.txt_log_quality.setHtml(text)

    def save(self):
        text, total_time = self.quality.get_log_dialog_quality_text()
        settings = QSettings()
        new_filename, filter = QFileDialog.getSaveFileName(self,
                                                           QCoreApplication.translate('LogQualityDialog',
                                                                                      'Export to PDF'),
                                                           settings.value(
                                                               'Asistente-LADM_COL/log_quality_dialog/save_path', '.'),
                                                           filter="PDF (*.pdf)")               

        if new_filename:
            settings.setValue('Asistente-LADM_COL/log_quality_dialog/save_path', os.path.dirname(new_filename))
            new_filename = new_filename if new_filename.lower().endswith(".pdf") else "{}.pdf".format(new_filename)

            title = QCoreApplication.translate(
                'LogQualityDialog',
                "<h2 align='center'>Quality Check Results</h2><div style='text-align:center;'>{}<br>Database: {}, Schema: {}<br>Total execution time: {}</div>").format(
                time.strftime("%d/%m/%y %H:%M:%S"), settings.value('Asistente-LADM_COL/pg/database'),
                settings.value('Asistente-LADM_COL/pg/schema'), self.quality.utils.set_time_format(total_time))

            self.txt_log_quality.setHtml("{}<br>{}".format(title, text))

            printer = QPrinter()
            printer.setPageSize(QPrinter.Letter)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(new_filename)
            self.txt_log_quality.print(printer)

            msg = QCoreApplication.translate("LogQualityDialog", 
                "All Quality Check report successfully generated in folder <a href='file:///{path}'>{path}</a>!").format(path=normalize_local_url(new_filename))
            self.qgis_utils.message_with_duration_emitted.emit(msg, Qgis.Success, 0) 

