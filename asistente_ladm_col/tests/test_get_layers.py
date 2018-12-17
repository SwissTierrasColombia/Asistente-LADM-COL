import datetime

import nose2
import psycopg2
from qgis.core import QgsApplication, QgsProject
from qgis.analysis import QgsNativeAlgorithms
from processing.core.Processing import Processing
from qgis.testing import (unittest,
                          start_app)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (import_projectgenerator,
                                            get_dbconn,
                                            get_test_path,
                                            restore_schema,
                                            clean_table)


from asistente_ladm_col.utils.qgis_utils import QGISUtils
from asistente_ladm_col.config.table_mapping_config import BOUNDARY_POINT_TABLE, PLOT_TABLE
from asistente_ladm_col.config.general_config import DEFAULT_EPSG

import_projectgenerator()

class TestGetLayers(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        Processing.initialize()
        #QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
        print("\nINFO: Setting up copy CSV points to DB validation...")
        self.qgis_utils = QGISUtils()
        self.db_connection = get_dbconn('test_ladm_col')
        #self.db_connection_3d = get_dbconn('test_ladm_col_3d')
        result = self.db_connection.test_connection()
        print('test_connection', result)
        if not result[1]:
            print('The test connection is not working')
            return
        restore_schema('test_ladm_col')
        #restore_schema('test_ladm_col_3d')

    # def check_necessary_domains_load(self, layer):
    #     print("\nLoading layers...")
    #     related_domains = self.qgis_utils.get_related_domains(layer, [])
    #     return related_domains

    def test_get_layers(self):
        RELATED_TABLES_DOMAINS = {'puntolindero': ["col_acuerdotipo", "col_defpuntotipo",
                                                   "col_descripcionpuntotipo", "col_interpolaciontipo",
                                                   "col_monumentaciontipo", "la_puntotipo", "puntolindero"],
                                  'terreno': ["la_contenidoniveltipo", "la_dimensiontipo", "la_estructuratipo",
                                              "la_nivel", "la_registrotipo", "la_relacionsuperficietipo",
                                              "terreno"]
                                  }

        print("\nINFO: Validating Functionality of get_layers...")

        self.qgis_utils.cache_layers_and_relations(self.db_connection)
        print("---------------------->", self.qgis_utils._layers, self.qgis_utils._relations, self.qgis_utils._bags_of_enum)
        QgsProject.instance().clear()
        print("\nINFO: Validating when no exist loaded layers...")
        for layer in [BOUNDARY_POINT_TABLE, PLOT_TABLE]:
            loaded_tables = self.qgis_utils.get_layer(self.db_connection, layer, load=True)
            self.assertIn(loaded_tables.name(), layer)
            loaded_layers_tree_names = [layer.name() for layer in self.qgis_utils.get_ladm_layers_from_layer_tree(self.db_connection)]
            for layer_related in RELATED_TABLES_DOMAINS[layer]:
                print("Check if exist {} in loaded layers {}".format(layer_related, loaded_layers_tree_names))
                self.assertIn(layer_related, loaded_layers_tree_names)
            QgsProject.instance().clear()



        # self.qgis_utils.disable_automatic_fields(self.db_connection, BOUNDARY_POINT_TABLE)
        # self.upload_points_from_csv()
        # self.validate_points_in_db()
        # clean_table('test_ladm_col', BOUNDARY_POINT_TABLE)

    # def upload_points_from_csv(self):
    #     print("Copying CSV data with no elevation...")
    #     csv_path = get_test_path('csv/puntos_fixed.csv')
    #     txt_delimiter = ';'
    #     cbo_longitude = 'x'
    #     cbo_latitude = 'y'
    #     res = self.qgis_utils.copy_csv_to_db(csv_path,
    #                                 txt_delimiter,
    #                                 cbo_longitude,
    #                                 cbo_latitude,
    #                                 self.db_connection,
    #                                 DEFAULT_EPSG,
    #                                 BOUNDARY_POINT_TABLE)
    #     self.assertEqual(res, True)
    #
    # def test_upload_points_from_csv_crs_wgs84(self):
    #     print("\nINFO: Copying CSV data with EPSG:4326...")
    #     clean_table('test_ladm_col', BOUNDARY_POINT_TABLE)
    #     self.qgis_utils.disable_automatic_fields(self.db_connection, BOUNDARY_POINT_TABLE)
    #     self.upload_points_from_csv_crs_wgs84()
    #     self.validate_points_in_db_from_wgs84()
    #     clean_table('test_ladm_col', BOUNDARY_POINT_TABLE)
    #
    # def upload_points_from_csv_crs_wgs84(self):
    #     print("Copying CSV data in WGS84...")
    #     csv_path = get_test_path('csv/puntos_crs_4326_wgs84.csv')
    #     txt_delimiter = ';'
    #     cbo_longitude = 'x'
    #     cbo_latitude = 'y'
    #     epsg =  '4326'
    #
    #     res = self.qgis_utils.copy_csv_to_db(csv_path,
    #                                 txt_delimiter,
    #                                 cbo_longitude,
    #                                 cbo_latitude,
    #                                 self.db_connection,
    #                                 epsg,
    #                                 BOUNDARY_POINT_TABLE)
    #
    #     self.assertEqual(res, True)

if __name__ == '__main__':
    nose2.main()