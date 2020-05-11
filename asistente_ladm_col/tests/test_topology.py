import nose2

from qgis.core import QgsVectorLayer
from qgis.testing import (unittest,
                          start_app)

from asistente_ladm_col.lib.geometry import GeometryUtils

start_app()  # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (import_qgis_model_baker,
                                            get_gpkg_conn,
                                            get_test_copy_path)

import_qgis_model_baker()


class TestTopology(unittest.TestCase):

    def _test_pair_boundary_plot(self):
        # TODO: Fix this test!
        # Message:
        # AssertionError: Lists differ: [(1, 1), (1, 4), (1, 3), (3, 3)] != [(1, 3), (3, 3)]
        #
        #     First differing element 0:
        #     (1, 1)
        #     (1, 3)
        #
        #     First list contains 2 additional elements.
        #     First extra element 2:
        #     (1, 3)
        #
        #     - [(1, 1), (1, 4), (1, 3), (3, 3)]
        #     + [(1, 3), (3, 3)]

        print('\nValidating boundaries plots')
        # extracted with: iface.activeLayer().dataProvider().dataSourceUri() in qgis console
        # and type is: layer.providerType()
        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        self.db_gpkg = get_gpkg_conn('tests_data_gpkg')
        self.names = self.db_gpkg.names
        self.names.T_ID_F = 't_id'  # Static label is set because the database does not have the ladm structure

        uri = gpkg_path + '|layername={layername}'.format(layername='tests_boundaries')
        boundary_layer = QgsVectorLayer(uri, 'tests_boundaries', 'ogr')

        uri = gpkg_path + '|layername={layername}'.format(layername='tests_plots')
        plot_layer = QgsVectorLayer(uri, 'tests_plots', 'ogr')

        result1, result2 = GeometryUtils().get_pair_boundary_plot(boundary_layer,
                                                                           plot_layer,
                                                                           self.names.T_ID_F,
                                                                           use_selection=False)

        self.assertEqual(result1, [(1, 3), (3, 3)])

        self.assertEqual(result2, [(1, 4)])


if __name__ == '__main__':
    nose2.main()
