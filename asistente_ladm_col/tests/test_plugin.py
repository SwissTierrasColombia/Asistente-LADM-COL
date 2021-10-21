import nose2

from qgis.core import QgsApplication
from qgis.testing import (start_app,
                          unittest)

from asistente_ladm_col.tests.utils import (get_iface,
                                            import_qgis_model_baker,
                                            unload_qgis_model_baker)
from asistente_ladm_col.asistente_ladm_col_plugin import AsistenteLADMCOLPlugin
asistente_ladm_col = AsistenteLADMCOLPlugin(get_iface(), False)

from asistente_ladm_col.utils.utils import is_plugin_version_valid
from asistente_ladm_col.config.general_config import (QGIS_MODEL_BAKER_PLUGIN_NAME,
                                                      QGIS_MODEL_BAKER_MIN_REQUIRED_VERSION,
                                                      QGIS_MODEL_BAKER_EXACT_REQUIRED_VERSION)
start_app()


class TestPlugin(unittest.TestCase):

    def test_01_dependencies(self):
        print('\nINFO: Validating plugin dependencies...')
        global asistente_ladm_col

        unload_qgis_model_baker()
        valid = is_plugin_version_valid(QGIS_MODEL_BAKER_PLUGIN_NAME,
                                        QGIS_MODEL_BAKER_MIN_REQUIRED_VERSION,
                                        QGIS_MODEL_BAKER_EXACT_REQUIRED_VERSION)
        self.assertFalse(valid)

        import_qgis_model_baker()
        valid = is_plugin_version_valid(QGIS_MODEL_BAKER_PLUGIN_NAME,
                                        QGIS_MODEL_BAKER_MIN_REQUIRED_VERSION,
                                        QGIS_MODEL_BAKER_EXACT_REQUIRED_VERSION)
        self.assertTrue(valid)

    def test_processing_provider(self):
        print('\nINFO: Validating LADM-COL processing provider...')
        global asistente_ladm_col

        provider = QgsApplication.processingRegistry().providerById('ladm_col')

        self.assertIsNotNone(provider, "LADM-COL provider not found in processing registry!")
        self.assertTrue(provider.isActive(), "LADM-COL provider was found but is not active!")

        self.assertGreater(len(provider.algorithms()), 0, "LADM-COL processing provider has no registered algorithms!")

        alg_names = [a.name() for a in provider.algorithms()]
        self.assertIn('copy_vector_layer', alg_names)
        self.assertIn('fieldcalculatorforinputlayer', alg_names)
        self.assertIn('insertfeaturestolayer', alg_names)
        self.assertIn('polygonstolines', alg_names)

    @classmethod
    def tearDownClass(cls):
        global asistente_ladm_col
        #asistente_ladm_col.unload()
        pass

if __name__ == '__main__':
    nose2.main()
