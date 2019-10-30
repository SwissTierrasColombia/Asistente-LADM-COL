import nose2
import itertools
from qgis.core import QgsProject, QgsWkbTypes
from qgis.testing import (unittest,
                          start_app)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (import_qgis_model_baker,
                                            get_dbconn,
                                            restore_schema)

from asistente_ladm_col.utils.qgis_utils import QGISUtils
from asistente_ladm_col.config.table_mapping_config import (BOUNDARY_POINT_TABLE, PLOT_TABLE,
                                                            POINT_AGREEMENT_TYPE_TABLE,
                                                            PHOTO_IDENTIFICATION_TYPE_TABLE,
                                                            PRODUCTION_METHOD_TYPE_TABLE,
                                                            POINT_INTERPOLATION_TYPE_TABLE,
                                                            POINT_TYPE_TABLE,
                                                            POINT_MONUMENTATION_TYPE_TABLE,
                                                            POINT_LOCATION_POINT_TYPE_TABLE,
                                                            SURFACE_RELATION_TYPE_TABLE,
                                                            DIMENSION_TYPE_TABLE)

import_qgis_model_baker()


class TestGetLayers(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.qgis_utils = QGISUtils()
        self.db_connection = get_dbconn('test_ladm_col')
        result = self.db_connection.test_connection()
        print('test_connection', result)
        if not result[1]:
            print('The test connection is not working')
            return
        restore_schema('test_ladm_col')

    def test_get_layer(self):
        print("\nINFO: Validating get_layer() method...")
        RELATED_TABLES = {BOUNDARY_POINT_TABLE: [POINT_AGREEMENT_TYPE_TABLE,
                                                 PHOTO_IDENTIFICATION_TYPE_TABLE,
                                                 PRODUCTION_METHOD_TYPE_TABLE,
                                                 POINT_INTERPOLATION_TYPE_TABLE,
                                                 POINT_LOCATION_POINT_TYPE_TABLE,
                                                 POINT_TYPE_TABLE,
                                                 POINT_MONUMENTATION_TYPE_TABLE,
                                                 BOUNDARY_POINT_TABLE],
                          PLOT_TABLE: [SURFACE_RELATION_TYPE_TABLE,
                                       DIMENSION_TYPE_TABLE,
                                       PLOT_TABLE]
                          }

        self.qgis_utils.cache_layers_and_relations(self.db_connection, ladm_col_db=True) # Gather information from the database
        QgsProject.instance().clear()

        print("\nINFO: Validating get_layer() on empty project...")
        # This test loads puntolindero and terreno tables, checks layers in layer tree after this
        # and finishes with a comparison between loaded layers and expected layers.
        for layer in [BOUNDARY_POINT_TABLE, PLOT_TABLE]:
            loaded_table = self.qgis_utils.get_layer(self.db_connection, layer, load=True)
            self.assertEqual(loaded_table.name(), layer)
            loaded_layers_tree_names = [layer.name() for layer in self.qgis_utils.get_ladm_layers_from_layer_tree(self.db_connection)]
            for layer_related in RELATED_TABLES[layer]:
                print("Check if {} exists in loaded layers {}".format(layer_related, loaded_layers_tree_names))
                self.assertIn(layer_related, loaded_layers_tree_names)
            QgsProject.instance().clear()

        print("\nINFO: Validating get_layer() when the project contains some of the related tables...")

        print("First for {} layer".format(BOUNDARY_POINT_TABLE))

        for pre_load in [POINT_AGREEMENT_TYPE_TABLE, POINT_MONUMENTATION_TYPE_TABLE]: # preload some layers
            self.qgis_utils.get_layer(self.db_connection, pre_load, load=True)

        self.qgis_utils.get_layer(self.db_connection, BOUNDARY_POINT_TABLE, load=True)

        # check number if element in Layer Tree and needed element are the same.
        loaded_layers_tree_names = len(RELATED_TABLES[BOUNDARY_POINT_TABLE])
        layer_tree_elements = len([layer.name() for layer in self.qgis_utils.get_ladm_layers_from_layer_tree(self.db_connection)])
        self.assertEqual(loaded_layers_tree_names, layer_tree_elements, "Number of loaded layers when loading PuntoLindero is not what we expect...")

        # Load again preloaded layer to check not duplicate layers in load
        for pre_load in [POINT_AGREEMENT_TYPE_TABLE, POINT_MONUMENTATION_TYPE_TABLE]:
            self.qgis_utils.get_layer(self.db_connection, pre_load, load=True)
        layer_tree_elements = len([layer.name() for layer in self.qgis_utils.get_ladm_layers_from_layer_tree(self.db_connection)])
        self.assertEqual(loaded_layers_tree_names, layer_tree_elements, "Duplicate layers found... This is an error!!!")
        QgsProject.instance().clear()

        print("Then for {} layer".format(PLOT_TABLE))
        for pre_load in [SURFACE_RELATION_TYPE_TABLE]: # preload some layers
            self.qgis_utils.get_layer(self.db_connection, pre_load, load=True)

        self.qgis_utils.get_layer(self.db_connection, PLOT_TABLE, geometry_type=QgsWkbTypes.PolygonGeometry, load=True)

        # check number if element in Layer Tree and needed element are the same.
        loaded_layers_tree_names = len(RELATED_TABLES[PLOT_TABLE])
        layer_tree_elements = len([layer.name() for layer in self.qgis_utils.get_ladm_layers_from_layer_tree(self.db_connection)])
        self.assertEqual(loaded_layers_tree_names, layer_tree_elements, "Number of loaded layers when loading Terreno is not what we expect...")

        # Check duplicate layers...
        for pre_load in [SURFACE_RELATION_TYPE_TABLE]:
            self.qgis_utils.get_layer(self.db_connection, pre_load, load=True)
        layer_tree_elements = len([layer.name() for layer in self.qgis_utils.get_ladm_layers_from_layer_tree(self.db_connection)])
        self.assertEqual(loaded_layers_tree_names, layer_tree_elements, "Duplicate layers found... This is an error!!!")
        QgsProject.instance().clear()

        print("\nINFO: Validating when loaded layers have the same name...")
        # Load terreno without geometry parameter load point and polygon layer with different geometries (10 layers)
        self.qgis_utils.get_layer(self.db_connection, PLOT_TABLE, load=True)
        toc_layers = [l for l in self.qgis_utils.get_ladm_layers_from_layer_tree(self.db_connection)]
        toc_names = [l.name() for l in toc_layers]
        same_name_layers = [layer for layer in toc_layers if toc_names.count(layer.name()) > 1]
        for layer_1, layer_2 in itertools.combinations(same_name_layers, 2):
            if layer_1.name() == layer_2.name():
                print("Testing {} ({}) against {} ({})".format(layer_1.name(), layer_1.geometryType(), layer_2.name(), layer_2.geometryType()))
                self.assertNotEqual(layer_1.geometryType(), layer_2.geometryType(), "Function get_layer loads layers with same name and geometry... This is an error!!!")


if __name__ == '__main__':
    nose2.main()
