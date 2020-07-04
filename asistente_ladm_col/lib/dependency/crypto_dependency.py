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
import os

from qgis.PyQt.QtCore import (QCoreApplication,
                              QFile,
                              QIODevice,
                              pyqtSignal)

from asistente_ladm_col.config.general_config import (DEPENDENCY_CRYPTO_DIR,
                                                      CYPTO_MD5SUM,
                                                      CRYPTO_LIBRARY_PATH)
from asistente_ladm_col.lib.dependency.dependency import Dependency
from asistente_ladm_col.utils.qt_utils import normalize_local_url
from asistente_ladm_col.utils.utils import md5sum


class CryptoDependency(Dependency):
    download_dependency_completed = pyqtSignal()
    download_dependency_progress_changed = pyqtSignal(int)  # progress

    def __init__(self):
        Dependency.__init__(self)
        self.dependency_name = QCoreApplication.translate("Dependency", "cryptography")

    def _save_dependency_file(self, fetcher_task):
        self._downloading = False
        if fetcher_task.reply() is not None:
            try:
                if not os.path.exists(DEPENDENCY_CRYPTO_DIR):
                    os.makedirs(DEPENDENCY_CRYPTO_DIR)

                # Write response to tmp file
                out_file = QFile(CRYPTO_LIBRARY_PATH)
                out_file.open(QIODevice.WriteOnly)
                out_file.write(fetcher_task.reply().readAll())
                out_file.close()

            except PermissionError as e:
                self.logger.warning_msg(__name__, QCoreApplication.translate("EncrypterDecrypter",
                    "The dependency used to encrypt/decrypt couldn't be installed. Check if it is possible to write into this folder: <a href='file:///{path}'>{path}</a>").format(path=normalize_local_url(DEPENDENCY_CRYPTO_DIR)))
            else:
                self.logger.clear_message_bar()
                self.logger.info_msg(__name__, QCoreApplication.translate("EncrypterDecrypter", "The dependency used to encrypt/decrypt is properly installed!"))

    def check_if_dependency_is_valid(self):
        if os.path.exists(CRYPTO_LIBRARY_PATH):
            if md5sum(CRYPTO_LIBRARY_PATH) == CYPTO_MD5SUM:
                return True
            else:
                os.remove(CRYPTO_LIBRARY_PATH)
                return False
        return False
