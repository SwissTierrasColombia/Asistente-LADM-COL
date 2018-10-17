import qgis
import nose2
import psycopg2
import datetime

from qgis.testing import unittest, start_app

start_app() # need to start before asistente_ladm_col.tests.utils


from qgis.core import QgsVectorLayer, QgsWkbTypes
from asistente_ladm_col.tests.utils import (
    import_projectgenerator,
    get_dbconn,
    get_test_path,
    restore_schema,
    run_etl_model)
from asistente_ladm_col.utils.qgis_utils import QGISUtils
from asistente_ladm_col.tests.utils import get_test_copy_path

import_projectgenerator()


class TestGeomsLoad(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print("\nINFO: Setting up copy Layer With different Geometries to DB validation...")
        self.qgis_utils = QGISUtils()
        self.gpkg_path = get_test_copy_path('geopackage/points_z_m_zm.gpkg')


    def test_valid_import_geom_2d_to_db(self):

        print('\nINFO: Validating ETL-Model from [ Point, PointZ, PointM, PointZM ] to Point geometries...')

        # Point To Point
        print("Validating Point to Point")
        uri = self.gpkg_path + '|layername={layername}'.format(layername='points')
        point_layer = QgsVectorLayer(uri, 'points', 'ogr')
        print("Is Valid layer :", point_layer.isValid())
        test_layer = QgsVectorLayer("Point?crs=EPSG:3116", "test_layer", "memory")
        output = run_etl_model(point_layer, out_layer=test_layer)
        print("Info: Validating geometry Point...")
        self.assertEqual(QgsWkbTypes.PointGeometry, output.type())
        self.assertEqual(QgsWkbTypes.Point, point_layer.wkbType())
        self.assertEqual(QgsWkbTypes.Point, output.wkbType())
        self.assertEqual(output.featureCount(), 51)

        # PointZ To Point
        print("Validating PointZ to Point")
        uri = self.gpkg_path + '|layername={layername}'.format(layername='points_Z')
        point_layer = QgsVectorLayer(uri, 'points_Z', 'ogr')
        print("Is Valid layer :", point_layer.isValid())
        self.assertIn(point_layer.wkbType(), [QgsWkbTypes.PointZ, QgsWkbTypes.Point25D])
        test_layer = QgsVectorLayer("Point?crs=EPSG:3116", "test_layer", "memory")
        output = run_etl_model(point_layer, out_layer=test_layer)
        print("Info: Validating geometry PointZ...", output.wkbType())
        self.assertEqual(QgsWkbTypes.PointGeometry, output.type())
        self.assertEqual(QgsWkbTypes.Point, output.wkbType())
        self.assertEqual(output.featureCount(), 51)


        # PointM To Point
        print("Validating PointM To Point")
        uri = self.gpkg_path + '|layername={layername}'.format(layername='points_M')
        point_layer = QgsVectorLayer(uri, 'points', 'ogr')
        print("Is Valid layer :", point_layer.isValid())
        test_layer = QgsVectorLayer("Point?crs=EPSG:3116", "test_layer", "memory")
        output = run_etl_model(point_layer, out_layer=test_layer)
        print("Info: Validating geometry PointZ...", output.wkbType())
        self.assertEqual(QgsWkbTypes.PointGeometry, output.type())
        self.assertEqual(QgsWkbTypes.PointM, point_layer.wkbType())
        self.assertEqual(QgsWkbTypes.Point, output.wkbType())
        self.assertEqual(output.featureCount(), 51)

        # PointZM To Point
        print("Validating PointZM To Point")
        uri = self.gpkg_path + '|layername={layername}'.format(layername='points_ZM')
        point_layer = QgsVectorLayer(uri, 'points', 'ogr')
        print("Is Valid layer :", point_layer.isValid())
        test_layer = QgsVectorLayer("Point?crs=EPSG:3116", "test_layer", "memory")
        output = run_etl_model(point_layer, out_layer=test_layer)
        print("Info: Validating geometry PointZ...", output.wkbType())
        self.assertEqual(QgsWkbTypes.PointGeometry, output.type())
        self.assertEqual(QgsWkbTypes.PointZM, point_layer.wkbType())
        self.assertEqual(QgsWkbTypes.Point, output.wkbType())
        self.assertEqual(output.featureCount(), 51)

    def test_valid_import_geom_3d_to_db(self):

        print('\nINFO: Validating ETL-Model from [ Point, PointZ, PointM, PointZM ] to PointZ geometries...')

        # Point To PointZ
        print("Validating Point to PointZ")
        uri = self.gpkg_path + '|layername={layername}'.format(layername='points')
        point_layer = QgsVectorLayer(uri, 'points', 'ogr')
        test_layer_3D = QgsVectorLayer("PointZ?crs=EPSG:3116", "test_layer", "memory")
        output = run_etl_model(point_layer, out_layer=test_layer_3D)
        print("Info: Validating geometry Point...")
        self.assertEqual(QgsWkbTypes.PointGeometry, output.type())
        self.assertEqual(QgsWkbTypes.Point, point_layer.wkbType())
        self.assertEqual(QgsWkbTypes.PointZ, output.wkbType())
        self.assertEqual(output.featureCount(), 51)

        # PointZ To PointZ
        print("Validating PointZ to PointZ")
        uri = self.gpkg_path + '|layername={layername}'.format(layername='points_Z')
        point_layer = QgsVectorLayer(uri, 'points', 'ogr')
        test_layer_3D = QgsVectorLayer("PointZ?crs=EPSG:3116", "test_layer", "memory")
        output = run_etl_model(point_layer, out_layer=test_layer_3D)
        print("Info: Validating geometry PointZ...", output.wkbType())
        self.assertEqual(QgsWkbTypes.PointGeometry, output.type())
        self.assertIn(point_layer.wkbType(), [QgsWkbTypes.PointZ, QgsWkbTypes.Point25D])
        self.assertEqual(QgsWkbTypes.PointZ, output.wkbType())
        self.assertEqual(output.featureCount(), 51)

        # PointM To PointZ
        print("Validating PointM To PointZ")
        uri = self.gpkg_path + '|layername={layername}'.format(layername='points_M')
        point_layer = QgsVectorLayer(uri, 'points', 'ogr')
        test_layer_3D = QgsVectorLayer("PointZ?crs=EPSG:3116", "test_layer", "memory")
        output = run_etl_model(point_layer, out_layer=test_layer_3D)
        print("Info: Validating geometry PointZ...", output.wkbType())
        self.assertEqual(QgsWkbTypes.PointGeometry, output.type())
        self.assertEqual(QgsWkbTypes.PointM, point_layer.wkbType())
        self.assertEqual(QgsWkbTypes.PointZ, output.wkbType())
        self.assertEqual(output.featureCount(), 51)

        # PointZM To PointZ
        print("Validating PointZM To PointZ")
        uri = self.gpkg_path + '|layername={layername}'.format(layername='points_ZM')
        point_layer = QgsVectorLayer(uri, 'points', 'ogr')
        test_layer_3D = QgsVectorLayer("PointZ?crs=EPSG:3116", "test_layer", "memory")
        output = run_etl_model(point_layer, out_layer=test_layer_3D)
        print("Info: Validating geometry PointZ...", output.wkbType())
        self.assertEqual(QgsWkbTypes.PointGeometry, output.type())
        self.assertEqual(QgsWkbTypes.PointZM, point_layer.wkbType())
        self.assertEqual(QgsWkbTypes.PointZ, output.wkbType())
        self.assertEqual(output.featureCount(), 51)




        # row = results[50]
        # #self.assertEqual(row[colnames['t_id']], 52)
        # self.assertEqual(row[colnames['acuerdo']], 'Acuerdo')
        # self.assertEqual(row[colnames['definicion_punto']], 'No_Bien_Definido')
        # self.assertEqual(row[colnames['descripcion_punto']], 'Otros')
        # self.assertEqual(row[colnames['exactitud_vertical']], 1)
        # self.assertEqual(row[colnames['exactitud_horizontal']], 1)
        # self.assertEqual(row[colnames['confiabilidad']], None)
        # self.assertEqual(row[colnames['nombre_punto']], None)
        # self.assertEqual(row[colnames['posicion_interpolacion']], 'Centro_Arco')
        # self.assertEqual(row[colnames['monumentacion']], None)
        # self.assertEqual(row[colnames['puntotipo']], 'Catastro')
        # self.assertEqual(row[colnames['p_espacio_de_nombres']], '-1')
        # self.assertEqual(row[colnames['p_local_id']], '-1')
        # self.assertEqual(row[colnames['ue_la_unidadespacial']], None)
        # self.assertEqual(row[colnames['ue_terreno']], None)
        # self.assertEqual(row[colnames['ue_la_espaciojuridicoredservicios']], None)
        # self.assertEqual(row[colnames['ue_la_espaciojuridicounidadedificacion']], None)
        # self.assertEqual(row[colnames['ue_servidumbrepaso']], None)
        # self.assertEqual(row[colnames['ue_unidadconstruccion']], None)
        # self.assertEqual(row[colnames['ue_construccion']], None)
        # self.assertEqual(row[colnames['comienzo_vida_util_version']], datetime.datetime(2017, 4, 19, 14, 16, 41, 221713))
        # self.assertEqual(row[colnames['fin_vida_util_version']], None)
        # self.assertEqual(row[colnames['localizacion_original']], '01010000202C0C0000B01E85ABFC642D41F2D24DE20A703041')


    @classmethod
    def tearDownClass(self):
        print('tearDown test_change_geometries_in_load')


if __name__ == '__main__':
    nose2.main()
