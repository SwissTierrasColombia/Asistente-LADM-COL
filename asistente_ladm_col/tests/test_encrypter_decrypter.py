# -*- coding: utf-8 -*-
import nose2
import os
import shutil

from qgis.testing import (start_app,
                          unittest)

from asistente_ladm_col.tests.utils import (get_iface)
from asistente_ladm_col.asistente_ladm_col_plugin import AsistenteLADMCOLPlugin
from asistente_ladm_col.config.general_config import (DEPENDENCY_CRYPTO_DIR,
                                                      CRYPTO_LIBRARY_NAME,
                                                      CRYPTO_LIBRARY)
from asistente_ladm_col.core.encrypter_decrypter import EncrypterDecrypter
from asistente_ladm_col.tests.utils import get_test_path

asistente_ladm_col = AsistenteLADMCOLPlugin(get_iface(), True)

start_app()

asistente_ladm_col.initGui()


class TestEncrypterDecrypter(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # Config dependency
        if not os.path.exists(DEPENDENCY_CRYPTO_DIR):
            os.makedirs(DEPENDENCY_CRYPTO_DIR)
        test_dependency = get_test_path('lib/crypto_utils/{}'.format(CRYPTO_LIBRARY_NAME))
        shutil.copyfile(test_dependency, CRYPTO_LIBRARY)

        self.encrypter_decrypter = EncrypterDecrypter()

    def test_encrypter_decrypter(self):
        plain_text = "ultra_secret"
        encrypted1 = self.encrypter_decrypter.encrypt_with_AES(plain_text)
        decrypted1 = self.encrypter_decrypter.decrypt_with_AES(encrypted1)
        self.assertEqual(plain_text, decrypted1)

        encrypted2 = self.encrypter_decrypter.encrypt_with_AES(plain_text)
        decrypted2 = self.encrypter_decrypter.decrypt_with_AES(encrypted2)
        self.assertEqual(plain_text, decrypted2)

        self.assertNotEqual(encrypted1, encrypted2)

    def _test_encrypter_decrypter_none(self):
        encrypted = self.encrypter_decrypter.encrypt_with_AES('mLiodFJacH4aIzCKaLRP32J6qZy3qylg5D/NOdvuFOE=')
        self.assertEqual('', encrypted)
        decrypted = self.encrypter_decrypter.decrypt_with_AES('asistente_ladm_col')
        self.assertEqual('', decrypted)

if __name__ == '__main__':
    nose2.main()
