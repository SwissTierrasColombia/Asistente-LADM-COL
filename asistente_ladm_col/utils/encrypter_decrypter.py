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

from PyQt5.QtCore import QProcess

from asistente_ladm_col.config.translator import PLUGIN_DIR
from asistente_ladm_col.utils.java_utils import JavaUtils

class EncrypterDecrypter():
    def __init__(self):
        self._secret_key = 'dnREVzd3Y1NMaA=='  # 'c2VjcmV0MTIz'
        self._salt = 'bGpEVzM2dU8='  # 'c2FsdDEyMw=='
        self.java_utils = JavaUtils()

    def run(self, mode, value):
        java_home_set = self.java_utils.set_java_home()
        if not java_home_set:
            self.java_utils.get_java_on_demand()

        java_path = self.java_utils.get_full_java_exe_path()
        args = ["-jar", os.path.join(PLUGIN_DIR, 'lib/crypto_utils/CryptoUtils.jar')]
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

