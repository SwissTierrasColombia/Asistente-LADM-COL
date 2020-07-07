# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-05-04
        git sha              : :%H$
        copyright            : (C) 2020 by Leonardo Cardona (BSF Swissphoto)
        email                : leocardonapiedrahita@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""

from functools import partial

from qgis.core import (QgsNetworkContentFetcherTask,
                       QgsApplication)
from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject,
                              pyqtSignal,
                              Qt,
                              QUrl)
from qgis.PyQt.QtWidgets import QApplication


from asistente_ladm_col.config.general_config import TEST_SERVER
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.utils import is_connected


class Dependency(QObject):
    download_dependency_completed = pyqtSignal()
    download_dependency_progress_changed = pyqtSignal(int)  # progress

    def __init__(self):
        QObject.__init__(self)
        self.logger = Logger()
        self._downloading = False
        self._show_cursor = True
        self.dependency_name = ""
        self.fetcher_task = None

    def download_dependency(self, uri):
        if not uri:
            self.logger.warning_msg(__name__, QCoreApplication.translate("Dependency",
                                                                         "Invalid URL to download dependency."))

        self.logger.clear_message_bar()
        is_valid = self.check_if_dependency_is_valid()

        if is_valid:
            self.logger.debug(__name__, QCoreApplication.translate("Dependency", "The {} dependency is already valid, so it won't be downloaded! (Dev, why did you asked to download it :P?)".format(self.dependency_name)))
            return

        if not self._downloading:  # Already downloading dependency?
            if is_connected(TEST_SERVER):
                self._downloading = True
                self.logger.clear_message_bar()
                self.logger.info_msg(__name__, QCoreApplication.translate("Dependency", "A {} dependency will be downloaded...".format(self.dependency_name)))
                self.fetcher_task = QgsNetworkContentFetcherTask(QUrl(uri))
                self.fetcher_task.begun.connect(self._task_begun)
                self.fetcher_task.progressChanged.connect(self._task_progress_changed)
                self.fetcher_task.fetched.connect(partial(self._save_dependency_file, self.fetcher_task))
                self.fetcher_task.taskCompleted.connect(self._task_completed)
                QgsApplication.taskManager().addTask(self.fetcher_task)
            else:
                self.logger.clear_message_bar()
                self.logger.warning_msg(__name__, QCoreApplication.translate("Dependency", "There was a problem connecting to Internet."))
                self._downloading = False

    def check_if_dependency_is_valid(self):
        raise NotImplementedError

    def _task_begun(self):
        if self._show_cursor:
            QApplication.setOverrideCursor(Qt.WaitCursor)

    def _task_progress_changed(self, progress):
        self.download_dependency_progress_changed.emit(progress)

    def _save_dependency_file(self, fetcher_task):
        raise NotImplementedError

    def _task_completed(self):
        if self._show_cursor:
            QApplication.restoreOverrideCursor()
        self.download_dependency_completed.emit()
