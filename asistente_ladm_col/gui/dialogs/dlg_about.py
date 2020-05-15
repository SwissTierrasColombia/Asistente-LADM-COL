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
import glob
import os
import shutil
import tempfile
import zipfile
from functools import partial

from qgis.PyQt.QtCore import (QUrl,
                              QFile,
                              QTextStream,
                              QIODevice,
                              QCoreApplication,
                              pyqtSignal)
from qgis.PyQt.QtWidgets import QDialog
from qgis.core import (QgsNetworkContentFetcherTask,
                       QgsApplication)

from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.config.general_config import (HELP_DIR_NAME,
                                                      HELP_DOWNLOAD,
                                                      PLUGIN_VERSION,
                                                      TEST_SERVER)
from asistente_ladm_col.config.translator import (QGIS_LANG,
                                                  PLUGIN_DIR)
from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.utils import (is_connected,
                                            show_plugin_help)

DIALOG_UI = get_ui_class('dialogs/dlg_about.ui')


class AboutDialog(QDialog, DIALOG_UI):
    message_with_button_open_about_emitted = pyqtSignal(str)

    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.logger = Logger()
        self.check_local_help()

        self.tb_changelog.setOpenExternalLinks(True)

        if QGIS_LANG == 'en':
            file = QFile(":/Asistente-LADM-COL/resources/html/Changelog_en.html")
        else:
            file = QFile(":/Asistente-LADM-COL/resources/html/Changelog.html")

        if not file.open(QIODevice.ReadOnly | QIODevice.Text):
            raise Exception(file.errorString())

        stream = QTextStream(file)
        stream.setCodec("UTF-8")

        self.tb_changelog.setHtml(stream.readAll())

    def check_local_help(self):
        try:
            self.btn_download_help.clicked.disconnect(self.show_help)
        except TypeError as e:
            pass
        try:
            self.btn_download_help.clicked.disconnect(self.download_help)
        except TypeError as e:
            pass

        if os.path.exists(os.path.join(PLUGIN_DIR,
                                       HELP_DIR_NAME,
                                       QGIS_LANG,
                                       'index.html')):
            self.btn_download_help.setText(QCoreApplication.translate("AboutDialog", "Open help from local folder"))
            self.btn_download_help.clicked.connect(self.show_help)
        else:
            self.btn_download_help.setText(QCoreApplication.translate("AboutDialog", "Download help for offline access"))
            self.btn_download_help.clicked.connect(self.download_help)

    def save_file(self, fetcher_task):
        if fetcher_task.reply() is not None:
            tmpFile = tempfile.mktemp()
            tmpFold = tempfile.mktemp()
            outFile = QFile(tmpFile)
            outFile.open(QIODevice.WriteOnly)
            outFile.write(fetcher_task.reply().readAll())
            outFile.close()

            try:
                with zipfile.ZipFile(tmpFile, "r") as zip_ref:
                    zip_ref.extractall(tmpFold)
                    languages = glob.glob(os.path.join(tmpFold, 'asistente_ladm_col_docs/*'))

                    for language in languages:
                        shutil.move(language, os.path.join(PLUGIN_DIR, HELP_DIR_NAME, language[-2:]))

            except zipfile.BadZipFile as e:
                self.logger.warning_msg(__name__, QCoreApplication.translate("AboutDialog",
                    "There was an error with the download. The downloaded file is invalid."))
            else:
                self.message_with_button_open_about_emitted.emit(
                    QCoreApplication.translate("AboutDialog", "Help files were successfully downloaded and can be accessed offline from the About dialog!"))

            try:
                os.remove(tmpFile)
                os.remove(tmpFold)
            except:
                pass

        self.check_local_help()

    def download_help(self):
        if is_connected(TEST_SERVER):
            self.btn_download_help.setEnabled(False)
            url = '/'.join([HELP_DOWNLOAD, PLUGIN_VERSION, 'asistente_ladm_col_docs.zip'])
            fetcher_task = QgsNetworkContentFetcherTask(QUrl(url))
            fetcher_task.taskCompleted.connect(self.enable_download_button)
            fetcher_task.fetched.connect(partial(self.save_file, fetcher_task))
            QgsApplication.taskManager().addTask(fetcher_task)
        else:
            self.logger.warning_msg(__name__, QCoreApplication.translate("AboutDialog",
                                                                         "There was a problem connecting to Internet."))

    def enable_download_button(self):
        self.btn_download_help.setEnabled(True)
        self.check_local_help()

    def show_help(self):
        show_plugin_help('', offline=True)
