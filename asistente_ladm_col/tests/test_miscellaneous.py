import nose2
from qgis.core import QgsProject
from qgis.testing import (unittest,
                          start_app)

from asistente_ladm_col.app_interface import AppInterface

start_app()

class TestMiscellaneous(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = AppInterface()

    def test_add_remove_single_custom_model_dir(self):
        print("\nINFO: Validating add and remove single custom model dir...")
        new_model_dir = "/usr/share/qgis/"
        self.base_test_add_remove_custom_model_dirs(new_model_dir)

    def test_add_remove_multiple_custom_model_dir(self):
        print("\nINFO: Validating add and remove multiple custom model dir...")
        new_model_dirs = "/usr/share/qgis/;/usr/share/models;/usr/models"
        self.base_test_add_remove_custom_model_dirs(new_model_dirs)

    def base_test_add_remove_custom_model_dirs(self, new_model_dirs):
        current_model_dirs = self.app.settings.custom_model_dirs
        # Test add custom model dirs
        self.app.settings.add_custom_model_dir(new_model_dirs)
        for new_model_dir in new_model_dirs.split(";"):
            self.assertTrue(self.check_model_dir_in_dirs(new_model_dir))

        # Test remove custom model dirs
        self.app.settings.remove_custom_model_dir(new_model_dirs)
        for new_model_dir in new_model_dirs.split(";"):
            self.assertFalse(self.check_model_dir_in_dirs(new_model_dir))

        # Do we have the same paths as before
        self.assertListEqual(self.app.settings.custom_model_dirs.split(";"), current_model_dirs.split(";"))

    def check_model_dir_in_dirs(self, model_dir):
        return model_dir in self.app.settings.custom_model_dirs.split(";")

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    nose2.main()
