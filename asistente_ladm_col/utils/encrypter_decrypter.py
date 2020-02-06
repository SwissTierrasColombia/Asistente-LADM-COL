# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-02-06
        copyright            : (C) 2020 by Andrés Acosta (BSF Swissphoto)
        email                : amacostapulido@gmail.com
        github               : MauricioAcosta
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
import base64
import hashlib
from asistente_ladm_col.lib.Crypto import Random
from asistente_ladm_col.lib.Crypto.Cipher import AES


class EncrypterDecrypter:
    """Adapted from: https://medium.com/@nipun.357/aes-encryption-decryption-java-python-6e9f261c24d6 """
    def __init__(self):
        self._secret_key = "secret123"
        self._salt = "salt123"
        self._cipher = ''
        self._block_size = 16
        self._un_pad = lambda s: s[0:-ord(s[-1:])]
        self._iv = Random.new().read(AES.block_size)  # Random IV
        self._pad = lambda  s: s + (self._block_size - len(s) % self._block_size) * chr(self._block_size - len(s) %
                                                                                    self._block_size)

    def get_private_key(self):
        return hashlib.pbkdf2_hmac('SHA256', self._secret_key.encode(), self._salt.encode(), 65536, 32)

    def encrypt_with_AES(self, message):
        private_key = self.get_private_key()
        message = self._pad(message)
        cipher = AES.new(private_key, AES.MODE_CBC, self._iv)
        cipher_bytes = base64.b64encode(self._iv + cipher.encrypt(message))
        return bytes.decode(cipher_bytes)

    def decrypt_with_AES(self, encoded):
        private_key = self.get_private_key()
        try:
            cipher_text = base64.b64decode(encoded)
            iv = cipher_text[:AES.block_size]
            cipher = AES.new(private_key, AES.MODE_CBC, iv)
            plain_bytes = self._un_pad(cipher.decrypt(cipher_text[self._block_size:]))
        except ValueError as e:
            return ''
        return bytes.decode(plain_bytes)
