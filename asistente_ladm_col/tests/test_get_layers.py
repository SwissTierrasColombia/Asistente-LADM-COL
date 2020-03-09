import nose2
import itertools
from qgis.core import QgsProject
from qgis.testing import (unittest,
                          start_app)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.config.enums import LayerRegisterType
from asistente_ladm_col.tests.utils import (import_qgis_model_baker,
                                            get_pg_conn,
                                            get_gpkg_conn,
                                            restore_schema)

from asistente_ladm_col.config.general_config import (LAYER_NAME,
                                                      LAYER)
from asistente_ladm_col.utils.qgis_utils import QGISUtils
import_qgis_model_baker()


class TestGetLayers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.qgis_utils = QGISUtils()
        cls.db_gpkg = get_gpkg_conn('test_ladm_operation_model_gpkg')

        print("INFO: Restoring databases to be used")
        restore_schema('test_ladm_col')
        cls.db_pg = get_pg_conn('test_ladm_col')

    def test_get_layer_in_pg(self):
        print("\nINFO: Validating get_layer() method in PG...")
        self.check_get_layer(self.db_pg)

    def test_get_layer_in_gpkg(self):
        print("\nINFO: Validating get_layer() method in GPKG...")
        self.check_get_layer(self.db_gpkg)

    def check_get_layer(self, db):
        result = db.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')

        self.assertIsNotNone(db.names.OP_BOUNDARY_POINT_T, 'Names is None')

        RELATED_TABLES = {db.names.OP_BOUNDARY_POINT_T: [db.names.OP_AGREEMENT_TYPE_D,
                                                         db.names.OP_PHOTO_IDENTIFICATION_TYPE_D,
                                                         db.names.COL_PRODUCTION_METHOD_TYPE_D,
                                                         db.names.COL_INTERPOLATION_TYPE_D,
                                                         db.names.OP_LOCATION_POINT_TYPE_D,
                                                         db.names.OP_POINT_TYPE_D,
                                                         db.names.COL_MONUMENTATION_TYPE_D,
                                                         db.names.OP_BOUNDARY_POINT_T],
                          db.names.OP_PLOT_T: [db.names.COL_SURFACE_RELATION_TYPE_D,
                                               db.names.COL_DIMENSION_TYPE_D,
                                               db.names.OP_PLOT_T]
                          }

        self.qgis_utils.cache_layers_and_relations(db, ladm_col_db=True, db_source=None) # Gather information from the database
        QgsProject.instance().clear()

        print("\nINFO: Validating get_layer() on empty project...")
        # This test loads puntolindero and terreno tables, checks layers in layer tree after this
        # and finishes with a comparison between loaded layers and expected layers.
        for layer in [db.names.OP_BOUNDARY_POINT_T, db.names.OP_PLOT_T]:
            loaded_table = self.qgis_utils.get_layer(db, layer, load=True)
            self.assertEqual(db.get_ladm_layer_name(loaded_table), layer)
            loaded_layers_tree_names = [db.get_ladm_layer_name(layer) for layer in self.qgis_utils.get_ladm_layers_by_register_type(db, LayerRegisterType.IN_REGISTER)]
            for layer_related in RELATED_TABLES[layer]:
                print("Check if {} exists in loaded layers {}".format(layer_related, loaded_layers_tree_names))
                self.assertIn(layer_related, loaded_layers_tree_names)
            QgsProject.instance().clear()

        print("\nINFO: Validating get_layer() when the project contains some of the related tables...")

        print("First for {} layer".format(db.names.OP_BOUNDARY_POINT_T))

        for pre_load in [db.names.OP_AGREEMENT_TYPE_D, db.names.COL_MONUMENTATION_TYPE_D]: # preload some layers
            self.qgis_utils.get_layer(db, pre_load, load=True)

        self.qgis_utils.get_layer(db, db.names.OP_BOUNDARY_POINT_T, load=True)

        # check number if element in Layer Tree and needed element are the same.
        loaded_layers_tree_names = len(RELATED_TABLES[db.names.OP_BOUNDARY_POINT_T])
        layer_tree_elements = len([layer.name() for layer in self.qgis_utils.get_ladm_layers_by_register_type(db, LayerRegisterType.IN_REGISTER)])
        self.assertEqual(loaded_layers_tree_names, layer_tree_elements, "Number of loaded layers when loading PuntoLindero is not what we expect...")

        # Load again preloaded layer to check not duplicate layers in load
        for pre_load in [db.names.OP_AGREEMENT_TYPE_D, db.names.COL_MONUMENTATION_TYPE_D]:
            self.qgis_utils.get_layer(db, pre_load, load=True)
        layer_tree_elements = len([layer.name() for layer in self.qgis_utils.get_ladm_layers_by_register_type(db, LayerRegisterType.IN_REGISTER)])
        self.assertEqual(loaded_layers_tree_names, layer_tree_elements, "Duplicate layers found... This is an error!!!")
        QgsProject.instance().clear()

        print("Then for {} layer".format(db.names.OP_PLOT_T))
        for pre_load in [db.names.COL_SURFACE_RELATION_TYPE_D]: # preload some layers
            self.qgis_utils.get_layer(db, pre_load, load=True)

        self.qgis_utils.get_layer(db, db.names.OP_PLOT_T, load=True)

        # check number if element in Layer Tree and needed element are the same.
        loaded_layers_tree_names = len(RELATED_TABLES[db.names.OP_PLOT_T])
        layer_tree_elements = len([layer.name() for layer in self.qgis_utils.get_ladm_layers_by_register_type(db, LayerRegisterType.IN_REGISTER)])
        self.assertEqual(loaded_layers_tree_names, layer_tree_elements, "Number of loaded layers when loading Terreno is not what we expect...")

        # Check duplicate layers...
        for pre_load in [db.names.COL_SURFACE_RELATION_TYPE_D]:
            self.qgis_utils.get_layer(db, pre_load, load=True)
        layer_tree_elements = len([layer.name() for layer in self.qgis_utils.get_ladm_layers_by_register_type(db, LayerRegisterType.IN_REGISTER)])
        self.assertEqual(loaded_layers_tree_names, layer_tree_elements, "Duplicate layers found... This is an error!!!")
        QgsProject.instance().clear()

        print("\nINFO: Validating when loaded layers have the same name...")
        # Load terreno without geometry parameter load point and polygon layer with different geometries (10 layers)
        self.qgis_utils.get_layer(db, db.names.OP_PLOT_T, load=True)
        toc_layers = [l for l in self.qgis_utils.get_ladm_layers_by_register_type(db, LayerRegisterType.IN_REGISTER)]
        toc_names = [l.name() for l in toc_layers]
        same_name_layers = [layer for layer in toc_layers if toc_names.count(layer.name()) > 1]
        for layer_1, layer_2 in itertools.combinations(same_name_layers, 2):
            if layer_1.name() == layer_2.name():
                print("Testing {} ({}) against {} ({})".format(layer_1.name(), layer_1.geometryType(), layer_2.name(), layer_2.geometryType()))
                self.assertNotEqual(layer_1.geometryType(), layer_2.geometryType(), "Function get_layer loads layers with same name and geometry... This is an error!!!")

    def test_get_layers_in_pg(self):
        print("\nINFO: Validating get_layers() method in PG...")
        self.check_get_layers(self.db_pg)

    def test_get_layers_in_qpkg(self):
        print("\nINFO: Validating get_layers() method in GPKG...")
        self.check_get_layers(self.db_gpkg)

    def check_get_layers(self, db):
        print("\nINFO: Get layers without loading to the map canvas")
        QgsProject.instance().removeAllMapLayers()  # remove previous load layers in the register

        layers = {
            db.names.OP_PLOT_T: {LAYER_NAME: db.names.OP_PLOT_T, LAYER: None},
            db.names.COL_UE_BAUNIT_T: {LAYER_NAME: db.names.COL_UE_BAUNIT_T, LAYER: None}
        }

        self.qgis_utils.get_layers(db, layers, load=False)
        layers_in_register = self.qgis_utils.get_ladm_layers_by_register_type(db, LayerRegisterType.IN_REGISTER)
        layers_in_canvas = self.qgis_utils.get_ladm_layers_by_register_type(db, LayerRegisterType.IN_CANVAS)
        layers_not_in_canvas = self.qgis_utils.get_ladm_layers_by_register_type(db, LayerRegisterType.NOT_IN_CANVAS)

        self.assertEqual(len(layers_in_register), 2)
        self.assertEqual(len(layers_in_canvas), 0)
        self.assertEqual(len(layers_not_in_canvas), 2)

        layers_names = [db.get_ladm_layer_name(layer_not_in_canvas) for layer_not_in_canvas in layers_not_in_canvas]
        self.assertIn(db.names.OP_PLOT_T, layers_names)
        self.assertIn(db.names.COL_UE_BAUNIT_T, layers_names)

        print("\nINFO: Get layers retrieve previous layers load in project register")
        layers = {
            db.names.OP_PLOT_T: {LAYER_NAME: db.names.OP_PLOT_T, LAYER: None},
            db.names.OP_PARCEL_T: {LAYER_NAME: db.names.OP_PARCEL_T, LAYER: None}
        }

        self.qgis_utils.get_layers(db, layers, load=True)
        layers_in_register = self.qgis_utils.get_ladm_layers_by_register_type(db, LayerRegisterType.IN_REGISTER)
        layers_in_canvas = self.qgis_utils.get_ladm_layers_by_register_type(db, LayerRegisterType.IN_CANVAS)
        layers_not_in_canvas = self.qgis_utils.get_ladm_layers_by_register_type(db, LayerRegisterType.NOT_IN_CANVAS)

        self.assertEqual(len(layers_in_register), 7)
        self.assertEqual(len(layers_in_canvas), 6)
        self.assertEqual(len(layers_not_in_canvas), 1)

        layers_names_not_in_canvas = [db.get_ladm_layer_name(layer_not_in_canvas) for layer_not_in_canvas in layers_not_in_canvas]
        self.assertIn(db.names.COL_UE_BAUNIT_T, layers_names_not_in_canvas)

        layers_names_in_canvas = [db.get_ladm_layer_name(layer_in_canvas) for layer_in_canvas in layers_in_canvas]
        self.assertIn(db.names.OP_PLOT_T, layers_names_in_canvas)
        self.assertIn(db.names.OP_PARCEL_T, layers_names_in_canvas)
        self.assertIn(db.names.COL_DIMENSION_TYPE_D, layers_names_in_canvas)
        self.assertIn(db.names.COL_SURFACE_RELATION_TYPE_D, layers_names_in_canvas)
        self.assertIn(db.names.OP_CONDITION_PARCEL_TYPE_D, layers_names_in_canvas)
        self.assertIn(db.names.OP_PARCEL_TYPE_D, layers_names_in_canvas)

    @classmethod
    def tearDownClass(cls):
        print('Close connection')
        cls.db_pg.conn.close()


if __name__ == '__main__':
    nose2.main()
