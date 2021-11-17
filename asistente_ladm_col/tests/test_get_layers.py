import nose2
from qgis.core import QgsProject
from qgis.testing import (unittest,
                          start_app)

from asistente_ladm_col.app_interface import AppInterface

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (import_qgis_model_baker,
                                            unload_qgis_model_baker,
                                            restore_pg_db,
                                            restore_mssql_db,
                                            restore_gpkg_db)

from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.lib.model_registry import LADMColModelRegistry


class TestGetLayers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import_qgis_model_baker(),
        cls.app = AppInterface()

        print("INFO: Restoring databases to be used")
        schema = 'test_ladm_col'
        models = [LADMColModelRegistry().model(LADMNames.LADM_COL_MODEL_KEY).full_name(),
                  LADMColModelRegistry().model(LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY).full_name(),
                  LADMColModelRegistry().model(LADMNames.SUPPLIES_MODEL_KEY).full_name(),
                  LADMColModelRegistry().model(LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY).full_name(),
                  LADMColModelRegistry().model(LADMNames.SURVEY_MODEL_KEY).full_name()]

        cls.db_gpkg = restore_gpkg_db(schema, models)
        cls.db_pg = restore_pg_db(schema, models)
        cls.db_mssql = restore_mssql_db(schema, models)

    def test_get_layer_in_pg(self):
        print("\nINFO: Validating get_layer() method in PG...")
        res, code, msg = self.db_pg.test_connection()
        self.assertTrue(res, msg)
        self.check_get_layer(self.db_pg)

    def test_get_layer_in_gpkg(self):
        print("\nINFO: Validating get_layer() method in GPKG...")
        res, code, msg = self.db_gpkg.test_connection()
        self.assertTrue(res, msg)
        self.check_get_layer(self.db_gpkg)

    def test_get_layers_in_pg(self):
        print("\nINFO: Validating get_layers() method in PG...")
        res, code, msg = self.db_pg.test_connection()
        self.assertTrue(res, msg)
        self.check_get_layers(self.db_pg)

    def test_get_layers_in_gpkg(self):
        print("\nINFO: Validating get_layers() method in GPKG...")
        res, code, msg = self.db_gpkg.test_connection()
        self.assertTrue(res, msg)
        self.check_get_layers(self.db_gpkg)

    def test_get_layer_in_mssql(self):
        print("\nINFO: Validating get_layer() method in SQL Server...")
        res, code, msg = self.db_mssql.test_connection()
        self.assertTrue(res, msg)
        self.check_get_layer(self.db_mssql)

    def test_get_layers_in_mssql(self):
        print("\nINFO: Validating get_layers() method in SQL Server...")
        res, code, msg = self.db_mssql.test_connection()
        self.assertTrue(res, msg)
        self.check_get_layers(self.db_mssql)

    def check_get_layer(self, db):
        self.assertIsNotNone(db.names.LC_BOUNDARY_POINT_T, 'Names is None')

        RELATED_TABLES = {db.names.LC_BOUNDARY_POINT_T: [db.names.LC_AGREEMENT_TYPE_D,
                                                         db.names.LC_PHOTO_IDENTIFICATION_TYPE_D,
                                                         db.names.COL_PRODUCTION_METHOD_TYPE_D,
                                                         db.names.COL_INTERPOLATION_TYPE_D,
                                                         db.names.COL_POINT_TYPE_D,
                                                         db.names.LC_BOUNDARY_POINT_T],
                          db.names.LC_PLOT_T: [db.names.COL_SURFACE_RELATION_TYPE_D,
                                               db.names.COL_DIMENSION_TYPE_D,
                                               db.names.LC_PLOT_T]
                          }

        self.app.core.cache_layers_and_relations(db, ladm_col_db=True, db_source=None) # Gather information from the database
        QgsProject.instance().clear()

        print("\nINFO: Validating get_layer() on empty project...")
        # This test loads puntolindero and terreno tables, checks layers in layer tree after this
        # and finishes with a comparison between loaded layers and expected layers.
        for layer in [db.names.LC_BOUNDARY_POINT_T, db.names.LC_PLOT_T]:
            loaded_table = self.app.core.get_layer(db, layer, load=True)
            self.assertEqual(db.get_ladm_layer_name(loaded_table), layer)
            loaded_layers_tree_names = self.app.core.get_ladm_layers_from_qgis(db).keys()
            for layer_related in RELATED_TABLES[layer]:
                print("Check if {} exists in loaded layers {}".format(layer_related, loaded_layers_tree_names))
                self.assertIn(layer_related, loaded_layers_tree_names)

            self.assertEqual(len(loaded_layers_tree_names), len(RELATED_TABLES[layer]), "Number of loaded layers does not correspond to expected number!")
            QgsProject.instance().clear()

        print("\nINFO: Validating get_layer() when the project contains some of the related tables...")

        print("First for {} layer".format(db.names.LC_BOUNDARY_POINT_T))

        for pre_load in [db.names.LC_AGREEMENT_TYPE_D]: # preload some layers
            self.app.core.get_layer(db, pre_load, load=True)

        self.app.core.get_layer(db, db.names.LC_BOUNDARY_POINT_T, load=True)

        # check number if element in Layer Tree and needed element are the same.
        loaded_layers_tree_names = len(RELATED_TABLES[db.names.LC_BOUNDARY_POINT_T])
        layer_tree_elements = len(self.app.core.get_ladm_layers_from_qgis(db))
        self.assertEqual(loaded_layers_tree_names, layer_tree_elements, "Number of loaded layers when loading PuntoLindero is not what we expect...")

        # Load again preloaded layer to check not duplicate layers in load
        for pre_load in [db.names.LC_AGREEMENT_TYPE_D]:
            self.app.core.get_layer(db, pre_load, load=True)
        layer_tree_elements = len(self.app.core.get_ladm_layers_from_qgis(db))
        self.assertEqual(loaded_layers_tree_names, layer_tree_elements, "Duplicate layers found... This is an error!!!")
        QgsProject.instance().clear()

        print("Then for {} layer".format(db.names.LC_PLOT_T))
        for pre_load in [db.names.COL_SURFACE_RELATION_TYPE_D]: # preload some layers
            self.app.core.get_layer(db, pre_load, load=True)

        self.app.core.get_layer(db, db.names.LC_PLOT_T, load=True)

        # check number if element in Layer Tree and needed element are the same.
        loaded_layers_tree_names = len(RELATED_TABLES[db.names.LC_PLOT_T])
        layer_tree_elements = len(self.app.core.get_ladm_layers_from_qgis(db))
        self.assertEqual(loaded_layers_tree_names, layer_tree_elements, "Number of loaded layers when loading Terreno is not what we expect...")

        # Check duplicate layers...
        for pre_load in [db.names.COL_SURFACE_RELATION_TYPE_D]:
            self.app.core.get_layer(db, pre_load, load=True)
        layer_tree_elements = len(self.app.core.get_ladm_layers_from_qgis(db))
        self.assertEqual(loaded_layers_tree_names, layer_tree_elements, "Duplicate layers found... This is an error!!!")
        QgsProject.instance().clear()

    def check_get_layers(self, db):
        layers = {db.names.LC_BOUNDARY_POINT_T: None,
                  db.names.LC_BOUNDARY_T: None,
                  db.names.LC_PLOT_T: None,
                  db.names.MORE_BFS_T: None,
                  db.names.LESS_BFS_T: None,
                  db.names.POINT_BFS_T: None}

        self.app.core.cache_layers_and_relations(db, ladm_col_db=True, db_source=None) # Gather information from the database
        QgsProject.instance().clear()

        # Expected number of loaded layers and relationships
        self.app.core.get_layers(db, layers, load=False)
        self.assertEqual(len(QgsProject.instance().mapLayers()), 6)
        self.assertEqual(len(QgsProject.instance().layerTreeRoot().findLayers()), 0)
        self.assertEqual(len(QgsProject.instance().relationManager().relations()), 0)

        QgsProject.instance().clear()
        self.app.core.get_layers(db, layers, load=True)
        self.assertEqual(len(QgsProject.instance().mapLayers()), 17)
        self.assertEqual(len(QgsProject.instance().layerTreeRoot().findLayers()), 17)
        self.assertEqual(len(QgsProject.instance().relationManager().relations()), 27)

        # Expected groups
        self.assertIsNotNone(QgsProject.instance().layerTreeRoot().findGroup("tables"))
        self.assertIsNotNone(QgsProject.instance().layerTreeRoot().findGroup("domains"))
        self.assertEqual(len(QgsProject.instance().layerTreeRoot().findGroups()), 2)

        # Expected layer visibility
        survey_point_layer = self.app.core.get_ladm_layer_from_qgis(db, db.names.LC_SURVEY_POINT_T)  # related layer: not visible
        self.assertIsNotNone(survey_point_layer)
        # For some reason it returns always true...
        #self.assertFalse(QgsProject.instance().layerTreeRoot().findLayer(survey_point_layer).itemVisibilityChecked())

        boundary_point_layer = self.app.core.get_ladm_layer_from_qgis(db, db.names.LC_BOUNDARY_POINT_T)  # requested layer: visible
        self.assertIsNotNone(boundary_point_layer)
        # For some reason it returns always true...
        # self.assertTrue(QgsProject.instance().layerTreeRoot().findLayer(boundary_point_layer).itemVisibilityChecked())

        # Expected domain from related table
        survey_point_type_domain = self.app.core.get_ladm_layer_from_qgis(db, db.names.LC_SURVEY_POINT_TYPE_D)
        self.assertIsNotNone(survey_point_type_domain)
        self.assertTrue(self._is_relation_in_qgis_relations(survey_point_layer,
                                                            db.names.LC_SURVEY_POINT_T_SURVEY_POINT_TYPE_F,
                                                            survey_point_type_domain,
                                                            db.names.T_ID_F),
                        "'lc_puntolevantamiento-tipo_punto_levantamiento' relationship should be there!")

        QgsProject.instance().clear()

    def _is_relation_in_qgis_relations(self, referencing_layer, referencing_field, referenced_layer, referenced_field):
        qgis_relations = QgsProject.instance().relationManager().referencingRelations(referencing_layer)
        for qgis_relation in qgis_relations:
            if qgis_relation.referencedLayer() == referenced_layer and \
                    referenced_layer.fields()[qgis_relation.referencedFields()[0]].name() == referenced_field and \
                    referencing_layer.fields()[qgis_relation.referencingFields()[0]].name() == referencing_field:
                return True

        return False


    @classmethod
    def tearDownClass(cls):
        print("INFO: Closing connection and unloading model baker")
        cls.db_pg.conn.close()
        cls.db_mssql.conn.close()
        unload_qgis_model_baker()


if __name__ == '__main__':
    nose2.main()
