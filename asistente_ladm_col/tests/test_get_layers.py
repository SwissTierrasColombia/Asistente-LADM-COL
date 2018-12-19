import nose2
import itertools
from qgis.core import QgsProject, QgsWkbTypes
from processing.core.Processing import Processing
from qgis.testing import (unittest,
                          start_app)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (import_projectgenerator,
                                            get_dbconn,
                                            restore_schema,
                                            )

from asistente_ladm_col.utils.qgis_utils import QGISUtils
from asistente_ladm_col.config.table_mapping_config import BOUNDARY_POINT_TABLE, PLOT_TABLE

import_projectgenerator()


class TestGetLayers(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        Processing.initialize()
        print("\nINFO: Setting up copy CSV points to DB validation...")
        self.qgis_utils = QGISUtils()
        self.db_connection = get_dbconn('test_ladm_col')
        result = self.db_connection.test_connection()
        print('test_connection', result)
        if not result[1]:
            print('The test connection is not working')
            return
        restore_schema('test_ladm_col')

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
        QgsProject.instance().clear()
        print("\nINFO: Validating when no exist loaded layers...")
        # This test load puntolindero and terreno tables, check layers in layer tree after this
        # and finish with comparision between loaded layers and needed layers.
        for layer in [BOUNDARY_POINT_TABLE, PLOT_TABLE]:
            loaded_tables = self.qgis_utils.get_layer(self.db_connection, layer, load=True)
            self.assertIn(loaded_tables.name(), layer)
            loaded_layers_tree_names = [layer.name() for layer in self.qgis_utils.get_ladm_layers_from_layer_tree(self.db_connection)]
            for layer_related in RELATED_TABLES_DOMAINS[layer]:
                print("Check if exist {} in loaded layers {}".format(layer_related, loaded_layers_tree_names))
                self.assertIn(layer_related, loaded_layers_tree_names)
            QgsProject.instance().clear()

        print("\nINFO: Validating when exist loaded layers...")

        print("Try this for {} layer".format(BOUNDARY_POINT_TABLE))
        # preload some layers
        for pre_load in ["col_acuerdotipo", "col_monumentaciontipo"]:
            self.qgis_utils.get_layer(self.db_connection, pre_load, load=True)
        # Load model layer
        self.qgis_utils.get_layer(self.db_connection, BOUNDARY_POINT_TABLE, load=True)
        # check number if element in Layer Tree and needed element are the same.
        loaded_layers_tree_names = len(RELATED_TABLES_DOMAINS[BOUNDARY_POINT_TABLE])
        layer_tree_elements = len([layer.name() for layer in self.qgis_utils.get_ladm_layers_from_layer_tree(self.db_connection)])
        self.assertEqual(loaded_layers_tree_names, layer_tree_elements, "Same Element Numbers... OK")
        # Load again preloaded layer for check not duplicate layers in load
        for pre_load in ["col_acuerdotipo", "col_monumentaciontipo"]:
            self.qgis_utils.get_layer(self.db_connection, pre_load, load=True)
        layer_tree_elements = len([layer.name() for layer in self.qgis_utils.get_ladm_layers_from_layer_tree(self.db_connection)])
        self.assertEqual(loaded_layers_tree_names, layer_tree_elements, "Function duplicate layers... Fail!!!")
        QgsProject.instance().clear()

        print("Try this for {} layer".format(PLOT_TABLE))
        # preload some layers
        for pre_load in ["la_nivel", "la_relacionsuperficietipo"]:
            self.qgis_utils.get_layer(self.db_connection, pre_load, load=True)
        # Load model layer
        self.qgis_utils.get_layer(self.db_connection, PLOT_TABLE, geometry_type=QgsWkbTypes.Polygon, load=True)
        # check number if element in Layer Tree and needed element are the same.
        loaded_layers_tree_names = len(RELATED_TABLES_DOMAINS[PLOT_TABLE])
        layer_tree_elements = len([layer.name() for layer in self.qgis_utils.get_ladm_layers_from_layer_tree(self.db_connection)])
        self.assertEqual(loaded_layers_tree_names, layer_tree_elements, "Same Element Numbers... OK")
        for pre_load in ["la_nivel", "la_relacionsuperficietipo"]:
            self.qgis_utils.get_layer(self.db_connection, pre_load, load=True)
        layer_tree_elements = len([layer.name() for layer in self.qgis_utils.get_ladm_layers_from_layer_tree(self.db_connection)])
        self.assertEqual(loaded_layers_tree_names, layer_tree_elements, "Function duplicate layers... Fail!!!")

        QgsProject.instance().clear()
        print("\nINFO: Validating when loaded layers are the same name...")
        # Load terreno without geometry parameter load point and polygon layer with different geometries (10 layers)
        self.qgis_utils.get_layer(self.db_connection, PLOT_TABLE, load=True)
        toc_layers = [l for l in self.qgis_utils.get_ladm_layers_from_layer_tree(self.db_connection)]
        toc_names = [l.name() for l in toc_layers]
        same_name_layers = [layer for layer in toc_layers if toc_names.count(layer.name()) > 1]
        for layer_1, layer_2 in itertools.combinations(same_name_layers, 2):
            if layer_1.name() == layer_2.name():
                self.assertNotEqual(layer_1.geometryType(), layer_2.geometryType(), "Function get_layers loas Layers with same name and geometry... Fail!!!")


if __name__ == '__main__':
    nose2.main()
