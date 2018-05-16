# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-04-30
        git sha              : :%H$
        copyright            : (C) 2018 by Germán Carrillo (BSF Swissphoto)
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
from ..utils import get_ui_class

import os
import glob
import shutil
import zipfile
import tempfile
from functools import partial
from qgis.utils import iface

from qgis.core import QgsNetworkContentFetcherTask as QNCFT
from qgis.core import QgsApplication
from qgis.PyQt.QtCore import (QUrl, QFile, QIODevice)
from qgis.PyQt.QtWidgets import QDialog, QSizePolicy, QGridLayout

from ..config.general_config import (
    PLUGIN_VERSION,
    HELP_DOWNLOAD,
    PLUGIN_NAME
)


DIALOG_UI = get_ui_class('about_dialog.ui')


class AboutDialog(QDialog, DIALOG_UI):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        #self.PLUGIN_VERSION='0.0.10-alpha'
        self.btn_download_help.clicked.connect(self.down_help)
        self.iface = iface

    def save_file(self, a):
        tmpFile = tempfile.mktemp()
        tmpFold = tempfile.mktemp()
        outFile = QFile(tmpFile)
        outFile.open(QIODevice.WriteOnly)
        outFile.write(a.reply().readAll())
        outFile.close()
        print(os.path.join(QgsApplication.qgisSettingsDirPath(), 'python/plugins', 'asistente_ladm_col', 'help'))
        try:
            with zipfile.ZipFile(tmpFile, "r") as zip_ref:
                zip_ref.extractall(tmpFold)
                lang = glob.glob(os.path.join(tmpFold, 'asistente_ladm_col_docs/*'))
                print(lang)
                b = os.path.join(QgsApplication.qgisSettingsDirPath(), 'python/plugins', 'asistente_ladm_col', 'help')
                for i in lang:
                    print(i)
                    shutil.move(i, os.path.join(b, i[-2:]))
        except zipfile.BadZipFile as e:
            self.iface.messageBar().pushMessage("Asistente LADM_COL", "Error, el archivo descargado no es valido.",1, 30)

    def down_help(self):
        a = QNCFT(QUrl(os.path.join(HELP_DOWNLOAD, PLUGIN_VERSION, 'asistente_ladm_col_docs.zip')))
        #a.fetched.connect(lambda: self.save_file(a))
        a.fetched.connect(partial(self.save_file, a))
        QgsApplication.taskManager().addTask(a)
