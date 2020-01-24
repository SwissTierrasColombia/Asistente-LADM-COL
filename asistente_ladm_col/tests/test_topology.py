import nose2

from qgis.core import QgsVectorLayer
from qgis.testing import (unittest,
                          start_app)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (import_qgis_model_baker,
                                            get_gpkg_conn,
                                            get_test_copy_path)
from asistente_ladm_col.utils.qgis_utils import QGISUtils

import_qgis_model_baker()


class TestTopology(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.qgis_utils = QGISUtils()

    def test_pair_boundary_plot(self):
        print('\nValidating boundaries plots')
        # extracted with: iface.activeLayer().dataProvider().dataSourceUri() in qgis console
        # and type is: layer.providerType()
        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        self.db_gpkg = get_gpkg_conn(gpkg_path)
        self.names = self.db_gpkg.names
        self.names.T_ID_F = 't_id'  # Static label is set because the database does not have the ladm structure

        uri = gpkg_path + '|layername={layername}'.format(layername='tests_boundaries')
        boundary_layer = QgsVectorLayer(uri, 'tests_boundaries', 'ogr')

        uri = gpkg_path + '|layername={layername}'.format(layername='tests_plots')
        plot_layer = QgsVectorLayer(uri, 'tests_plots', 'ogr')

        result1, result2 = self.qgis_utils.geometry.get_pair_boundary_plot(boundary_layer,
                                                                           plot_layer,
                                                                           self.names.T_ID_F,
                                                                           use_selection=False)

        self.assertEqual(result1, [(1, 3), (3, 3)])

        self.assertEqual(result2, [(1, 4)])

    def tearDownClass():
        print('tearDown test_topology')


if __name__ == '__main__':
    nose2.main()
