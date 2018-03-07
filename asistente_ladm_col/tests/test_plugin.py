# -*- coding: utf-8 -*-
import nose2

from qgis.testing import start_app, unittest
start_app()

from asistente_ladm_col.tests.utils import get_iface, import_projectgenerator, unload_projectgenerator

from asistente_ladm_col.asistente_ladm_col_plugin import AsistenteLADMCOLPlugin
asistente_ladm_col = AsistenteLADMCOLPlugin(get_iface())
asistente_ladm_col.initGui()

class TestPlugin(unittest.TestCase):

    def test_01_dependencies(self):
        global asistente_ladm_col

        unload_projectgenerator()
        valid = asistente_ladm_col.is_plugin_version_valid()
        self.assertFalse(valid)

        import_projectgenerator()
        valid = asistente_ladm_col.is_plugin_version_valid()
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
