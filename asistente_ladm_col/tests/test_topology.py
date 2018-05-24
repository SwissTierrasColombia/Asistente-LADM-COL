import qgis
import nose2
import psycopg2
import os

from sys import platform
from qgis.core import QgsVectorLayer
from qgis.testing import unittest, start_app

start_app() # need to start before asistente_ladm_col.tests.utils
from asistente_ladm_col.config.table_mapping_config import ID_FIELD

from asistente_ladm_col.tests.utils import import_projectgenerator, get_test_copy_path
from asistente_ladm_col.utils.qgis_utils import QGISUtils

import_projectgenerator()

class TestTopology(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.qgis_utils = QGISUtils()

    def test_pair_boundary_plot(self):
        print('Validating boundaries plots')
        # extracted with: iface.activeLayer().dataProvider().dataSourceUri() in qgis console
        # and type is: layer.providerType()
        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        uri = gpkg_path + '|layername={layername}'.format(layername='tests_boundaries')
        boundary_layer = QgsVectorLayer(uri, 'tests_boundaries', 'ogr')

        uri = gpkg_path + '|layername={layername}'.format(layername='tests_plots')
        plot_layer = QgsVectorLayer(uri, 'tests_plots', 'ogr')

        use_selection = False
        result1, result2 = self.qgis_utils.geometry.get_pair_boundary_plot(boundary_layer, plot_layer, ID_FIELD, use_selection);

        self.assertEqual(result1, [(1, 3), (3, 3)])

        self.assertEqual(result2, [(1, 4)])

    def tearDownClass():
        print('tearDown test_topology')


if __name__ == '__main__':
    nose2.main()
