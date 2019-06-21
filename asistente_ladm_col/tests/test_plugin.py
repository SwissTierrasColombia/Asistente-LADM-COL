# -*- coding: utf-8 -*-
import nose2

from qgis.testing import (start_app,
                          unittest)

from asistente_ladm_col.config.general_config import QGIS_MODEL_BAKER_PLUGIN_NAME, \
    QGIS_MODEL_BAKER_MIN_REQUIRED_VERSION, QGIS_MODEL_BAKER_EXACT_REQUIRED_VERSION

start_app()

from asistente_ladm_col.tests.utils import (get_iface,
                                            import_qgis_model_baker,
                                            unload_qgis_model_baker)

from asistente_ladm_col.asistente_ladm_col_plugin import AsistenteLADMCOLPlugin
asistente_ladm_col = AsistenteLADMCOLPlugin(get_iface())
asistente_ladm_col.initGui()

class TestPlugin(unittest.TestCase):

    def test_01_dependencies(self):
        global asistente_ladm_col

        unload_qgis_model_baker()
        valid = asistente_ladm_col.is_plugin_version_valid(QGIS_MODEL_BAKER_PLUGIN_NAME,
                                                           QGIS_MODEL_BAKER_MIN_REQUIRED_VERSION,
                                                           QGIS_MODEL_BAKER_EXACT_REQUIRED_VERSION)
        self.assertFalse(valid)

        import_qgis_model_baker()
        valid = asistente_ladm_col.is_plugin_version_valid(QGIS_MODEL_BAKER_PLUGIN_NAME,
                                                           QGIS_MODEL_BAKER_MIN_REQUIRED_VERSION,
                                                           QGIS_MODEL_BAKER_EXACT_REQUIRED_VERSION)
        self.assertTrue(valid)

    def test_02_plugin(self):
        global asistente_ladm_col
        # pending to add more validations
        pass

    @classmethod
    def tearDownClass(self):
        global asistente_ladm_col
        #asistente_ladm_col.unload()
        pass

if __name__ == '__main__':
    nose2.main()
