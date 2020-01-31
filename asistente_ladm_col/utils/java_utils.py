# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-01-15
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
import os
import platform
import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path
from shutil import which
import functools
import tempfile

from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject,
                              Qt,
                              QIODevice,
                              pyqtSignal,
                              QFile,
                              QUrl,
                              QSettings)
from qgis.PyQt.QtWidgets import QApplication

from qgis.core import (QgsNetworkContentFetcherTask,
                       QgsApplication)
from asistente_ladm_col.config.general_config import (JAVA_REQUIRED_VERSION,
                                                      KEY_JAVA_OS_VERSION,
                                                      DEPENDENCIES_BASE_PATH,
                                                      DICT_JAVA_DOWNLOAD_URL,
                                                      DICT_JAVA_MD5SUM,
                                                      DICT_JAVA_DIR_NAME,
                                                      TEST_SERVER)
from asistente_ladm_col.utils.utils import md5sum
from asistente_ladm_col.utils.qt_utils import normalize_local_url
from asistente_ladm_col.utils.qgis_utils import QGISUtils
from asistente_ladm_col.lib.logger import Logger


class JavaUtils(QObject):
    download_java_completed = pyqtSignal()
    download_java_progress_changed = pyqtSignal(int)  # progress

    JAVA_NAME = 'java.exe' if platform.system() == 'Windows' else 'java'

    def __init__(self):
        QObject.__init__(self)
        self.logger = Logger()
        self._downloading = False
        self._show_cursor = False

    def set_display_wait_cursor(self, show):
        self._show_cursor = show

    def get_java_on_demand(self):
        # Create required directories
        Path(DEPENDENCIES_BASE_PATH).mkdir(parents=True, exist_ok=True)

        # Remove previous java download
        custom_java_dir_path = os.path.join(DEPENDENCIES_BASE_PATH, DICT_JAVA_DIR_NAME[KEY_JAVA_OS_VERSION])
        if os.path.exists(custom_java_dir_path):
            shutil.rmtree(custom_java_dir_path, ignore_errors=True)

        url_java = DICT_JAVA_DOWNLOAD_URL[KEY_JAVA_OS_VERSION]
        self.download_java_dependency(url_java)

    def download_java_dependency(self, uri):
        self.logger.clear_message_bar()

        if not self._downloading: # Already downloading report dependency?
            if QGISUtils.is_connected(TEST_SERVER):
                self._downloading = True
                fetcher_task = QgsNetworkContentFetcherTask(QUrl(uri))
                fetcher_task.begun.connect(self.task_begun)
                fetcher_task.progressChanged.connect(self.task_progress_changed)
                fetcher_task.fetched.connect(functools.partial(self.save_java_dependency_file, fetcher_task))
                fetcher_task.taskCompleted.connect(self.task_completed)
                QgsApplication.taskManager().addTask(fetcher_task)
            else:
                self.logger.warning_msg(__name__, QCoreApplication.translate("JavaUtils", "There was a problem connecting to Internet."))
                self._downloading = False

    def task_begun(self):
        if self._show_cursor:
            QApplication.setOverrideCursor(Qt.WaitCursor)

    def task_progress_changed(self, progress):
        self.download_java_progress_changed.emit(progress)

    def task_completed(self):
        if self._show_cursor:
            QApplication.restoreOverrideCursor()
        self.download_java_completed.emit()

    def save_java_dependency_file(self, fetcher_task):
        if fetcher_task.reply() is not None:
            # Write response to tmp file
            tmp_file = tempfile.mktemp()
            out_file = QFile(tmp_file)
            out_file.open(QIODevice.WriteOnly)
            out_file.write(fetcher_task.reply().readAll())
            out_file.close()

            if not os.path.exists(DEPENDENCIES_BASE_PATH):
                os.makedirs(DEPENDENCIES_BASE_PATH)

            if md5sum(tmp_file) == DICT_JAVA_MD5SUM[KEY_JAVA_OS_VERSION]:

                try:
                    tar = tarfile.open(tmp_file)
                    tar.extractall(DEPENDENCIES_BASE_PATH)
                    tar.close()
                except tarfile.ReadError as e:
                    self.logger.warning_msg(__name__, QCoreApplication.translate("JavaUtils",
                                                                                 "There was an error with the download. The downloaded file is invalid."))
                except PermissionError as e:
                    self.logger.warning_msg(__name__, QCoreApplication.translate("JavaUtils",
                                                                                 "Java couldn't be installed. Check if it is possible to write into this folder: <a href='file:///{path}'>{path}</a>").format(path=normalize_local_url(os.path.join(DEPENDENCIES_BASE_PATH), DICT_JAVA_DIR_NAME[KEY_JAVA_OS_VERSION])))

            else:
                self.logger.warning_msg(__name__, QCoreApplication.translate("JavaUtils",
                                                                             "There was an error with the download. The downloaded file is invalid."))
            try:
                os.remove(tmp_file)
            except:
                pass

        self._downloading = False

    def set_java_home(self):
        """
        Attempt to set a valid JAVA_HOME only for the current session, which is used by reports (MapFish).
        First try with the system JAVA_HOME, if not present, try with the Java configured in Model Baker.
        if not the user is asked if he wants to be downloaded java on demand. Otherwise return false.
        :return: Whether a proper Java could be set or not in the current session's JAVA_HOME
        """
        java_name = 'java.exe' if sys.platform == 'win32' else 'java'
        pattern_java = "bin{}java".format(os.sep)

        # Get JAVA_HOME environment variable
        if 'JAVA_HOME' in os.environ:
            java_home = os.environ['JAVA_HOME']

            java_exe = os.path.join(java_home, 'bin', java_name)
            (is_valid, java_message) = JavaUtils.java_path_is_valid(java_exe)

            if not is_valid:
                # Another try: does JAVA_HOME include bin dir?
                java_exe = os.path.join(java_home, java_name)
                (is_valid, java_message) = JavaUtils.java_path_is_valid(java_exe)

                if is_valid:
                    os.environ['JAVA_HOME'] = java_exe.split(pattern_java)[0]
                    return True
            else:
                os.environ['JAVA_HOME'] = java_exe.split(pattern_java)[0]
                # JAVA_HOME is valid, we'll use it as it is!
                return True
        else:
            java_exe = which(java_name)
            if java_exe:
                # verifies that the java configured in the system is valid.
                (is_valid, java_message) = JavaUtils.java_path_is_valid(java_exe)
                if is_valid:
                    os.environ['JAVA_HOME'] = java_exe.split(pattern_java)[0]
                    return True

        # If JAVA_HOME environment variable doesn't exist
        # We use the value defined in QgisModelBaker
        java_exe = JavaUtils.get_java_path_from_qgis_model_baker()

        if java_exe:
            (is_valid, java_message) = JavaUtils.java_path_is_valid(java_exe)
            if is_valid:
                os.environ['JAVA_HOME'] = java_exe.split(pattern_java)[0]
                return True

        # If JAVA_HOME environment variable doesn't exist
        # If JAVA_HOME is no defined in QgisModelBaker
        # We will download JAVA by demand

        # Check if java was not installed previously, if it was download it is download again
        full_path_java = os.path.join(DEPENDENCIES_BASE_PATH, DICT_JAVA_DIR_NAME[KEY_JAVA_OS_VERSION], 'bin', JavaUtils.JAVA_NAME)
        (is_valid, java_message) = JavaUtils.java_path_is_valid(full_path_java)

        if is_valid:
            # java was download previueslly, it is no necessary download again because it is valid.
            os.environ['JAVA_HOME'] = full_path_java.split(pattern_java)[0]
            return True

        return False

    @staticmethod
    def get_full_java_exe_path():
        java_name = 'java.exe' if sys.platform == 'win32' else 'java'
        pattern_java = "bin{}java".format(os.sep)
        full_java_exe_path = ""

        # Get JAVA_HOME environment variable
        if 'JAVA_HOME' in os.environ:
            java_home = os.environ['JAVA_HOME']

            full_java_exe_path = os.path.join(java_home, 'bin', java_name)
            (is_valid, java_message) = JavaUtils.java_path_is_valid(full_java_exe_path)

            if not is_valid:
                # Another try: does JAVA_HOME include bin dir?
                full_java_exe_path = os.path.join(java_home, java_name)
                (is_valid, java_message) = JavaUtils.java_path_is_valid(full_java_exe_path)
                if not is_valid:
                    full_java_exe_path = ""
        else:
            full_java_exe_path = which(java_name)
            # verifies that the java configured in the system is valid.
            (is_valid, java_message) = JavaUtils.java_path_is_valid(full_java_exe_path)
            if not is_valid:
                full_java_exe_path = ""

        return full_java_exe_path

    @staticmethod
    def java_path_is_valid(java_path):
        """
        Check if java path exists
        :param java_path: (str) java path to validate
        :return: (bool, str)  True if java Path is valid, False in another case
        """
        try:
            if os.name == 'nt':
                java_path = JavaUtils.validate_java_path(java_path)

            procs_message = subprocess.check_output([java_path, '-version'], stderr=subprocess.STDOUT).decode(
                'utf8').lower()
            types_java = ['jre', 'java', 'jdk']

            if procs_message:
                if any(type_java in procs_message for type_java in types_java):
                    pattern = '\"(\d+\.\d+).*\"'
                    java_version = re.search(pattern, procs_message).groups()[0]

                    if java_version:
                        if float(java_version) == JAVA_REQUIRED_VERSION:
                            return (
                            True, QCoreApplication.translate("JavaPath", "Java path has been configured correctly."))
                        else:
                            return (False, QCoreApplication.translate("JavaPath",
                                                                      "Java version is not valid. Current version is {}, but must be {}.").format(
                                java_version, JAVA_REQUIRED_VERSION))

                    return (False, QCoreApplication.translate("JavaPath",
                                                              "Java exists but it is not possible to know and validate its version."))
                else:
                    return (False, QCoreApplication.translate("JavaPath",
                                                              "Java path is not valid, please select a valid path..."))
            else:
                return (
                False, QCoreApplication.translate("JavaPath", "Java path is not valid, please select a valid path..."))
        except Exception as e:
            return (
            False, QCoreApplication.translate("JavaPath", "Java path is not valid, please select a valid path..."))

    @staticmethod
    def validate_java_path(java_path):
        escape_characters = [('\a', '\\a'), ('\b', '\\b'), ('\f', '\\f'), ('\n', '\\n'), ('\r', '\\r'), ('\t', '\\t'),
                             ('\v', '\\v')]
        for escape_character in escape_characters:
            java_path = java_path.replace(escape_character[0], escape_character[1])
        return java_path

    @staticmethod
    def get_java_path_from_qgis_model_baker():
        java_path = QSettings().value('QgisModelBaker/ili2db/JavaPath', '', str)
        return java_path
