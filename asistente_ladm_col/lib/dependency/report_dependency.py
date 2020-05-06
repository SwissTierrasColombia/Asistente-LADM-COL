# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-05-04
        git sha              : :%H$
        copyright            : (C) 2020 by Leonardo Cardona (BSF Swissphoto)
                               (C) 2020 by Germán Carrillo (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
                               leocardonapiedrahita@gmail.com
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
import tempfile
import shutil
import zipfile

from qgis.PyQt.QtCore import (QCoreApplication,
                              QFile,
                              QIODevice,
                              pyqtSignal)

from asistente_ladm_col.config.general_config import (DEPENDENCIES_BASE_PATH,
                                                      REPORTS_REQUIRED_VERSION,
                                                      DEPENDENCY_REPORTS_DIR_NAME)
from asistente_ladm_col.lib.dependency.dependency import Dependency
from asistente_ladm_col.utils.qt_utils import normalize_local_url


class ReportDependency(Dependency):
    download_dependency_completed = pyqtSignal()
    download_dependency_progress_changed = pyqtSignal(int)  # progress

    def __init__(self):
        Dependency.__init__(self)
        self.dependency_name = QCoreApplication.translate("ReportDependency", "reports")

    def save_dependency_file(self, fetcher_task):
        if fetcher_task.reply() is not None:
            # Write response to tmp file
            tmp_file = tempfile.mktemp()
            out_file = QFile(tmp_file)
            out_file.open(QIODevice.WriteOnly)
            out_file.write(fetcher_task.reply().readAll())
            out_file.close()

            if not os.path.exists(DEPENDENCIES_BASE_PATH):
                os.makedirs(DEPENDENCIES_BASE_PATH)

            try:
                with zipfile.ZipFile(tmp_file, "r") as zip_ref:
                    zip_ref.extractall(DEPENDENCIES_BASE_PATH)
            except zipfile.BadZipFile as e:
                self.logger.warning_msg(__name__, QCoreApplication.translate("ReportGenerator",
                    "There was an error with the download. The downloaded file is invalid."))
            except PermissionError as e:
                self.logger.warning_msg(__name__, QCoreApplication.translate("ReportGenerator",
                    "Dependencies to generate reports couldn't be installed. Check if it is possible to write into this folder: <a href='file:///{path}'>{path}</a>").format(path=normalize_local_url(DEPENDENCY_REPORTS_DIR_NAME)))
            else:
                self.logger.clear_message_bar()
                self.logger.info_msg(__name__, QCoreApplication.translate("ReportGenerator", "The dependency to generate reports is properly installed! Select plots and click again the button in the toolbar to generate reports."))

            try:
                os.remove(tmp_file)
            except:
                pass

        self._downloading = False

    def check_if_dependency_is_valid(self):
        if os.path.exists(DEPENDENCY_REPORTS_DIR_NAME):
            # Check version
            version_path = os.path.join(DEPENDENCY_REPORTS_DIR_NAME, 'version')
            if not os.path.exists(version_path):
                return False
            else:
                version_found = ''
                with open(version_path) as f:
                    version_found = f.read()
                if version_found.strip() != REPORTS_REQUIRED_VERSION:
                    # Remove dependency. It's not valid.
                    shutil.rmtree(DEPENDENCY_REPORTS_DIR_NAME, ignore_errors=True)
                    return False
                else:
                    return True
        return False
