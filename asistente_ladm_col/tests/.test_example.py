#import qgis
import nose2
#import os

#from sys import platform
#from qgis.core import QgsVectorLayer
from qgis.testing import start_app, unittest

start_app() # need to start before asistente_ladm_col.tests.utils

#from asistente_ladm_col.gui.point_spa_uni_operation_wizard import PointsSpatialUnitOperationWizard
#from asistente_ladm_col.tests.utils import import_qgis_model_baker, get_test_path
#from asistente_ladm_col.utils.qgis_utils import QGISUtils

#import_qgis_model_baker()

class TestExample(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #self.qgis_utils = QGISUtils()
        pass

    def test_01_example(self):
        # some tests here
        pass

    def test_02_example(self):
        # some tests here, this execute before 02_example
        pass

    @classmethod
    def tearDownClass(cls):
        print('tearDown test_example')


if __name__ == '__main__':
    nose2.main()
