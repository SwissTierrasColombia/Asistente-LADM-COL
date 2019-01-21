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
from qgis.PyQt.QtWidgets import QDialog

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
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.rejected)
        self.buttonBox.helpRequested.connect(self.show_help)
        self.txt_log_quality.setHtml(self.quality.send_log_dialog_quality_text())

    def accepted(self):
        self.quality.clean_log_dialog_quality_text()
    def rejected(self):
        self.quality.clean_log_dialog_quality_text()
    def show_help(self):
        print ("Aceptar")
