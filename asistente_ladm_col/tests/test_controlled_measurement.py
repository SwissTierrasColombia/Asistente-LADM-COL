import nose2
from qgis.core import QgsVectorLayer, QgsApplication
from asistente_ladm_col.tests.utils import get_test_copy_path
from qgis.testing import unittest


class TestExport(unittest.TestCase):

    def test_dummy(self):

        self.assertTrue(True)

    def test_to_get_point_groups(self):
        print('\nINFO: Validating too long segments...')
        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        uri = gpkg_path + '|layername={layername}'.format(layername='tests_controlled_measurement')
        measure_layer = QgsVectorLayer(uri, 'tests_controlled_measurement', 'ogr')

        features = [feature for feature in measure_layer.getFeatures()]
        self.assertEqual(len(features), 38)

        expr = QgsExpression("\"tipe_def\"='Bien_Definido'")
        ids = [i.id() for i in lyr.getFeatures(QgsFeatureRequest(expr))]
        self.assertEqual(len(features), 20)

        expr = QgsExpression("\"tipe_def\"='No_Bien_Definido'")
        ids = [i.id() for i in lyr.getFeatures(QgsFeatureRequest(expr))]
        self.assertEqual(len(features), 18)


if __name__ == '__main__':
    nose2.main()
