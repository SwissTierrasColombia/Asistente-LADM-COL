# -*- coding: utf-8 -*-
import nose2

from qgis.testing import start_app, unittest
start_app()

from asistente_ladm_col.tests.utils import import_projectgenerator, get_iface
import_projectgenerator()

from asistente_ladm_col.asistente_ladm_col_plugin import AsistenteLADMCOLPlugin
asistente_ladm_col = AsistenteLADMCOLPlugin(get_iface())
asistente_ladm_col.initGui()

class TestPlugin(unittest.TestCase):

    def test_dependencies(self):
        global asistente_ladm_col
        valid = asistente_ladm_col.is_plugin_version_valid()
        self.assertTrue(valid)

    def test_plugin(self):
        global asistente_ladm_col
        # la version de qgis no es la adecuada
        self.assertNotEqual(None, asistente_ladm_col.get_plugin_version(asistente_ladm_col.plugin_dir))
        #self.assertEqual(None, asistente_ladm_col.show_about_dialog())
        #self.assertEqual(None, asistente_ladm_col.installTranslator())

    @classmethod
    def tearDownClass(self):
        global asistente_ladm_col
        #asistente_ladm_col.unload()
        pass

if __name__ == '__main__':
    nose2.main()
