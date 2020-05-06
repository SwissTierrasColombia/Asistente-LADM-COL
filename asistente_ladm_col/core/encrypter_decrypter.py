# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-02-12
        copyright            : (C) 2020 by Andrés Acosta (BSF Swissphoto)
        email                : amacostapulido@gmail.com
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

from asistente_ladm_col.config.general_config import (CRYPTO_LIBRARY,
                                                      URL_CRYPTO_LIBRARY)
from asistente_ladm_col.lib.dependency.java_dependency import JavaDependency
from asistente_ladm_col.lib.dependency.crypto_dependency import CrytoDependency
from asistente_ladm_col.lib.logger import Logger
from qgis.PyQt.QtCore import QProcess


class EncrypterDecrypter():
    def __init__(self):
        self._secret_key = 'dnREVzd3Y1NMaA=='  # 'c2VjcmV0MTIz'
        self._salt = 'bGpEVzM2dU8='  # 'c2FsdDEyMw=='
        self.logger = Logger()

        self.java_dependency = JavaDependency()
        self.cryto_dependency = CrytoDependency()

    def run(self, mode, value):

        java_home_set = self.java_dependency.set_java_home()
        if not java_home_set:
            self.java_dependency.get_java_on_demand()
            return

        if not self.cryto_dependency.check_if_dependency_is_valid():
            self.cryto_dependency.download_dependency(URL_CRYPTO_LIBRARY)
            return

        java_path = self.java_dependency.get_full_java_exe_path()
        args = ["-jar", CRYPTO_LIBRARY]
        args += [mode, self._secret_key, self._salt, value]

        proc = QProcess()
        proc.setProcessChannelMode(QProcess.MergedChannels)
        proc.start(java_path, args)
        proc.waitForReadyRead()
        output = bytearray(proc.readAllStandardOutput())
        output = output.decode("ascii")

        return output.strip()

    def encrypt_with_AES(self, value):
        return self.run('--encrypt', value)

    def decrypt_with_AES(self, value):
        return self.run('--decrypt', value)

