import qgis
import nose2
import psycopg2
import os

from sys import platform
from qgis.core import QgsVectorLayer
from qgis.testing import unittest, start_app

start_app() # need to start before asistente_ladm_col.tests.utils

#from asistente_ladm_col.gui.point_spa_uni_cadastre_wizard import PointsSpatialUnitCadastreWizard
from asistente_ladm_col.tests.utils import import_projectgenerator, get_test_path
from asistente_ladm_col.utils.qgis_utils import QGISUtils

import_projectgenerator()

_QGISUtils = QGISUtils()

class TestDigitizing(unittest.TestCase):

    def setUpClass():
        print('setUpClass test_boundaries_digitizing')

    def test_pair_boundary_plot(self):
        print('Validating boundaries plots')
        # extracted with: iface.activeLayer().dataProvider().dataSourceUri() in qgis console
        # and type is: layer.providerType()
        gpkg_path = get_test_path('geopackage/tests_data.gpkg')
        uri = gpkg_path + '|layername={layername}'.format(layername='tests_boundaries')
        boundary_layer = QgsVectorLayer(uri, 'tests_boundaries', 'ogr')

        uri = gpkg_path + '|layername={layername}'.format(layername='tests_plots')
        plot_layer = QgsVectorLayer(uri, 'tests_plots', 'ogr')

        use_selection = False
        result1, result2 = _QGISUtils.get_pair_boundary_plot(boundary_layer, plot_layer, use_selection);

        self.assertEqual(result1, [(1, 3), (3, 3)])

        self.assertEqual(result2, [(1, 4)])

    def test_get_too_long_segments_from_simple_line(self):
        print('Validating too long segments')
        gpkg_path = get_test_path('geopackage/tests_data.gpkg')
        uri = gpkg_path + '|layername={layername}'.format(layername='too_long_lines')
        boundary_layer = QgsVectorLayer(uri, 'too_long_lines', 'ogr')

        tolerance = 200 # meters

        features = [feature for feature in boundary_layer.getFeatures()]

        self.assertEqual(len(features), 2)

        for feature in features:
            lines = feature.geometry()
            self.assertTrue(lines.isMultipart())
            for part in range(lines.constGet().numGeometries()):
                line = lines.constGet().geometryN(part)
                segments_info = _QGISUtils.get_too_long_segments_from_simple_line(line, tolerance)
                for segment_info in segments_info:
                    #print(segment_info[0].asWkt(), segment_info[1])
                    self.assertEqual(segment_info[0].length(), segment_info[1])
                    self.assertTrue(segment_info[1] >= tolerance)

    def tearDownClass():
        print('tearDown test_boundaries_digitizing')


if __name__ == '__main__':
    nose2.main()
