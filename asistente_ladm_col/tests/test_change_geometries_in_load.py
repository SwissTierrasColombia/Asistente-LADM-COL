import nose2

from qgis.PyQt.QtCore import QVariant

from qgis.core import (QgsVectorLayer,
                       QgsField,
                       edit,
                       QgsWkbTypes)
from qgis.testing import (unittest,
                          start_app)

from asistente_ladm_col.app_interface import AppInterface

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.lib.model_registry import LADMColModelRegistry
from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.tests.utils import (get_test_path,
                                            restore_gpkg_db,
                                            delete_features,
                                            run_etl_model)
from asistente_ladm_col.tests.utils import get_test_copy_path

import processing


class TestGeomsLoad(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nINFO: Setting up copy layer With different Geometries to DB validation...")

        cls.app = AppInterface()

        # restore schemas
        print("INFO: Restoring databases to be used")
        cls.gpkg_path = get_test_copy_path('db/static/gpkg/test_distinct_geoms.gpkg')

        cls.db_pg = restore_gpkg_db('test_ladm_col_empty', [LADMColModelRegistry().model(LADMNames.SURVEY_MODEL_KEY).full_name()])

    def test_valid_import_geom_3d_to_db_gpkg(self):
        print('\nINFO: Validating ETL-Model from [ Point, PointZ, PointM, PointZM ] to Point geometries...')
        res, code, msg = self.db_pg.test_connection()
        self.assertTrue(res, msg)
        self.assertIsNotNone(self.db_pg.names.LC_BOUNDARY_POINT_T, 'Names is None')

        test_layer = self.app.core.get_layer(self.db_pg, self.db_pg.names.LC_BOUNDARY_POINT_T, load=True)

        point_layers = ['points', 'points_Z', 'points_M', 'points_ZM']

        for point_layer_name in point_layers:
            print("Validating {} to Point".format(point_layer_name))

            field_to_add = {
                'acuerdo': self.db_pg.names.LC_AGREEMENT_TYPE_D,
                'puntotipo': self.db_pg.names.COL_POINT_TYPE_D,
                'metodoproduccion': self.db_pg.names.COL_PRODUCTION_METHOD_TYPE_D
            }

            layers = {
                self.db_pg.names.LC_AGREEMENT_TYPE_D: None,
                self.db_pg.names.COL_POINT_TYPE_D: None,
                self.db_pg.names.COL_PRODUCTION_METHOD_TYPE_D: None
            }

            self.app.core.get_layers(self.db_pg, layers, load=True)

            uri = self.gpkg_path + '|layername={layername}'.format(layername=point_layer_name)
            point_layer = QgsVectorLayer(uri, point_layer_name, 'ogr')

            self.assertTrue(point_layer.isValid())
            if point_layer_name == 'points':
                self.assertEqual(point_layer.wkbType(), QgsWkbTypes.Point)
            elif point_layer_name == 'points_Z':
                self.assertIn(point_layer.wkbType(), [QgsWkbTypes.PointZ, QgsWkbTypes.Point25D])
            elif point_layer_name == 'points_M':
                self.assertEqual(point_layer.wkbType(), QgsWkbTypes.PointM)
            elif point_layer_name == 'points_ZM':
                self.assertEqual(point_layer.wkbType(), QgsWkbTypes.PointZM)

            with edit(point_layer):
                provider = point_layer.dataProvider()
                fields = [QgsField(field_name, QVariant.Int) for field_name in field_to_add]
                provider.addAttributes(fields)

            for field_name, layer_name in field_to_add.items():
                processing.run("ladm_col:fieldcalculatorforinputlayer", {
                    'INPUT': point_layer,
                    'FIELD_NAME': field_name,
                    'FIELD_TYPE': 0,
                    'FIELD_LENGTH': 10,
                    'FIELD_PRECISION': 3,
                    'NEW_FIELD': False,
                    'FORMULA': layers[layer_name].getFeature(1)['T_Id']})

            run_etl_model(self.db_pg.names, point_layer, test_layer, self.db_pg.names.LC_BOUNDARY_POINT_T)
            self.assertTrue(point_layer.isValid())
            print("Info: Validating geometry {}...".format(point_layer_name))
            self.assertEqual(test_layer.wkbType(), QgsWkbTypes.PointZ)
            self.assertEqual(test_layer.featureCount(), 51)

            delete_features(test_layer)
            self.assertEqual(test_layer.featureCount(), 0)

    @classmethod
    def tearDownClass(cls):
        print("INFO: Closing open connections to databases")
        # cls.db_distinct_geoms.conn.close()
        cls.db_pg.conn.close()


if __name__ == '__main__':
    nose2.main()
