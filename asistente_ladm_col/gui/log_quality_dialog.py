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
from ..utils.qt_utils import save_pdf_format

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
        settings = QSettings()
        text, total_time = self.quality.get_log_dialog_quality_text()
        title = QCoreApplication.translate(
                'LogQualityDialog',
                "<h2 align='center'>Quality Check Results</h2><div style='text-align:center;'>{}<br>Database: {}, Schema: {}<br>Total execution time: {}</div>").format(
                time.strftime("%d/%m/%y %H:%M:%S"), settings.value('Asistente-LADM_COL/pg/database'),
                settings.value('Asistente-LADM_COL/pg/schema'), self.quality.utils.set_time_format(total_time))

        save_pdf_format(self, 'Asistente-LADM_COL/log_quality_dialog/save_path', title, text )

