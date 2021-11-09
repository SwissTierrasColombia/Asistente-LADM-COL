import nose2
import re

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsVectorLayer,
                       Qgis)
from qgis.testing import (unittest,
                          start_app)

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.utils.crs_utils import get_crs_authid

start_app()  # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.config.general_config import DEFAULT_TOLERANCE_VALUE
from asistente_ladm_col.core.quality_rules.quality_rule_engine import QualityRuleEngine
from asistente_ladm_col.core.quality_rules.quality_rule_layer_manager import QualityRuleLayerManager
from asistente_ladm_col.config.config_db_supported import ConfigDBsSupported
from asistente_ladm_col.logic.quality.quality_rules import QualityRules
from asistente_ladm_col.logic.quality.point_quality_rules import PointQualityRules
from asistente_ladm_col.logic.quality.polygon_quality_rules import PolygonQualityRules
from asistente_ladm_col.tests.utils import (import_qgis_model_baker,
                                            import_processing,
                                            get_test_copy_path,
                                            get_pg_conn,
                                            get_gpkg_conn,
                                            get_gpkg_conn_from_path,
                                            restore_schema,
                                            unload_qgis_model_baker)
from asistente_ladm_col.lib.geometry import GeometryUtils
from asistente_ladm_col.config.enums import EnumQualityRule
from asistente_ladm_col.lib.quality_rule.quality_rule_manager import QualityRuleManager
from asistente_ladm_col.config.quality_rules_config import (QUALITY_RULE_ERROR_CODE_E200401,
                                                            QUALITY_RULE_ERROR_CODE_E200402,
                                                            QUALITY_RULE_ERROR_CODE_E200403,
                                                            QUALITY_RULE_ERROR_CODE_E100301,
                                                            QUALITY_RULE_ERROR_CODE_E100302,
                                                            QUALITY_RULE_ERROR_CODE_E100303,
                                                            QUALITY_RULE_ERROR_CODE_E300401,
                                                            QUALITY_RULE_ERROR_CODE_E300402,
                                                            QUALITY_RULE_ERROR_CODE_E300403,
                                                            QUALITY_RULE_ERROR_CODE_E300404,
                                                            QUALITY_RULE_ERROR_CODE_E300405,
                                                            QUALITY_RULE_ERROR_CODE_E200301,
                                                            QUALITY_RULE_ERROR_CODE_E200302,
                                                            QUALITY_RULE_ERROR_CODE_E200303,
                                                            QUALITY_RULE_ERROR_CODE_E200304,
                                                            QUALITY_RULE_ERROR_CODE_E200305,
                                                            QUALITY_RULE_ERROR_CODE_E300902,
                                                            QUALITY_RULE_ERROR_CODE_E301002,
                                                            QUALITY_RULE_ERROR_CODE_E301102)

import_processing()
import processing


class TesQualityRules(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import_qgis_model_baker()
        cls.app = AppInterface()
        cls.quality_rules = QualityRules()
        cls.geometry = GeometryUtils()
        cls.quality_rules_manager = QualityRuleManager()

        print("INFO: Restoring databases to be used")
        restore_schema('test_ladm_validations_topology_tables')

    def test_check_boundary_points_covered_by_plot_nodes(self):
        print('\nINFO: Validating boundary points are covered by plot nodes...')

        gpkg_path = get_test_copy_path('db/static/gpkg/quality_validations.gpkg')
        self.db_gpkg = get_gpkg_conn('tests_quality_validations_gpkg')
        names = self.db_gpkg.names
        names.T_ID_F = 't_id'  # Static label is set because the database does not have the ladm structure

        uri = gpkg_path + '|layername={layername}'.format(layername='puntolindero')
        boundary_point_layer = QgsVectorLayer(uri, 'puntolindero', 'ogr')
        self.assertEqual(boundary_point_layer.featureCount(), 82)

        uri = gpkg_path + '|layername={layername}'.format(layername='terreno')
        plot_layer = QgsVectorLayer(uri, 'terreno', 'ogr')
        self.assertEqual(plot_layer.featureCount(), 12)

        features = PointQualityRules.get_boundary_points_features_not_covered_by_plot_nodes(boundary_point_layer,
                                                                                            plot_layer,
                                                                                            names.T_ID_F)
        self.assertEqual(len(features), 14)
        result = [{'geom': f[1].asWkt(), 'id': f[0]} for f in features]

        test_result = [{'geom': 'Point (895168.40587982360739261 1544541.0977809748146683)', 'id': 223},
                       {'geom': 'Point (894720.88864161947276443 1544285.23876925860531628)', 'id': 210},
                       {'geom': 'Point (894682.65140924125444144 1544280.9901878833770752)', 'id': 209},
                       {'geom': 'Point (895038.58811557665467262 1544506.16500077745877206)', 'id': 220},
                       {'geom': 'Point (894718.52831863309256732 1544310.25819291360676289)', 'id': 211},
                       {'geom': 'Point (894748.2683882606215775 1544266.82824996509589255)', 'id': 206},
                       {'geom': 'Point (894655.27166260010562837 1544261.16347479773685336)', 'id': 205},
                       {'geom': 'Point (894681.70728004665579647 1544310.25819291360676289)', 'id': 208},
                       {'geom': 'Point (894745.43600067705847323 1544332.91729358164593577)', 'id': 207},
                       {'geom': 'Point (894639.00421297014690936 1544574.38610569201409817)', 'id': 152},
                       {'geom': 'Point (894655.27166260010562837 1544329.14077680348418653)', 'id': 204},
                       {'geom': 'Point (894648.56400672777090222 1544485.16136395325884223)', 'id': 153},
                       {'geom': 'Point (895195.31356186757329851 1544457.07028266228735447)', 'id': 222},
                       {'geom': 'Point (895053.22211809176951647 1544435.35531118814833462)', 'id': 221}]

        for item in test_result:
            self.assertIn(item, result, 'Error in: Boundary point {} is not covered by plot node'.format(item['id']))

    def test_topology_boundary_nodes_must_be_covered_by_boundary_points(self):
        print('\nINFO: Validating boundary nodes must be covered by boundary points...')
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS)
        schema_name = 'test_ladm_validations_topology_tables'
        self.db_pg = get_pg_conn(schema_name)
        names = self.db_pg.names

        res, code, msg = self.db_pg.test_connection()
        self.assertTrue(res, msg)
        self.assertIsNotNone(names.LC_BOUNDARY_POINT_T, 'Names is None')

        layers = {names.LC_BOUNDARY_POINT_T: None,
                  names.LC_BOUNDARY_T: None,
                  names.LC_PLOT_T: None,
                  names.POINT_BFS_T: None}
        self.app.core.get_layers(self.db_pg, layers, load=True)

        boundary_point_layer = layers[names.LC_BOUNDARY_POINT_T]
        self.assertEqual(boundary_point_layer.featureCount(), 109)

        boundary_layer = layers[names.LC_BOUNDARY_T]
        self.assertEqual(boundary_layer.featureCount(), 22)

        plot_layer = layers[names.LC_PLOT_T]
        self.assertEqual(plot_layer.featureCount(), 17)

        point_bfs_layer = layers[names.POINT_BFS_T]
        self.assertEqual(point_bfs_layer.featureCount(), 81)

        error_layer = QgsVectorLayer("Point?crs={}".format(get_crs_authid(boundary_layer.sourceCrs())), rule.error_table_name, "memory")
        data_provider = error_layer.dataProvider()
        data_provider.addAttributes(rule.error_table_fields)
        error_layer.updateFields()

        features = self.quality_rules.line_quality_rules.get_boundary_nodes_features_not_covered_by_boundary_points(self.db_pg, boundary_point_layer, boundary_layer, point_bfs_layer, error_layer, names.T_ID_F)

        # the algorithm was successfully executed
        self.assertEqual(len(features), 33)
        error_layer.dataProvider().addFeatures(features)

        # English language is set as default for validations
        exp = "\"codigo_error\" = '{}'".format(QUALITY_RULE_ERROR_CODE_E200401)
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 13)

        result = [{'id': f['id_lindero'], 'geom': f.geometry().asWkt()} for f in error_layer.selectedFeatures()]

        test_result = [{'id': 'edd15986-68f1-4cab-a6be-5455d6d1ee76', 'geom': 'PointZ (895065.96799999999348074 1544460.84700000006705523 0)'},
                       {'id': 'edd15986-68f1-4cab-a6be-5455d6d1ee76', 'geom': 'PointZ (895076.28099999995902181 1544438.87899999995715916 0)'},
                       {'id': 'edd15986-68f1-4cab-a6be-5455d6d1ee76', 'geom': 'PointZ (895126.55500000005122274 1544446.56199999991804361 0)'},
                       {'id': 'edd15986-68f1-4cab-a6be-5455d6d1ee76', 'geom': 'PointZ (895138.19400000001769513 1544479.25699999998323619 0)'},
                       {'id': 'edd15986-68f1-4cab-a6be-5455d6d1ee76', 'geom': 'PointZ (895150.11300000001210719 1544450.162999999942258 0)'},
                       {'id': '539f19b2-c8d1-45b0-a256-44d6147196eb', 'geom': 'PointZ (894732.84299999999348074 1544594.1229999999050051 0)'},
                       {'id': '539f19b2-c8d1-45b0-a256-44d6147196eb', 'geom': 'PointZ (894770.40800000005401671 1544602.14299999992363155 0)'},
                       {'id': 'bf962a29-773e-4bf2-9cf3-99781cd5c46a', 'geom': 'PointZ (894822.14000000001396984 1544541.38800000003539026 0)'},
                       {'id': 'f38d0673-2d84-43a3-bb4d-0eb5ddaec02c', 'geom': 'PointZ (894911.74499999999534339 1544391.85100000002421439 0)'},
                       {'id': '9d439543-9d1b-4df2-af32-82e11eccc15a', 'geom': 'PointZ (895120.1720000000204891 1544364.95600000000558794 0)'},
                       {'id': '9d439543-9d1b-4df2-af32-82e11eccc15a', 'geom': 'PointZ (895070.0779999999795109 1544331.15500000002793968 0)'},
                       {'id': '9d439543-9d1b-4df2-af32-82e11eccc15a', 'geom': 'PointZ (895121.96699999994598329 1544243.82499999995343387 0)'},
                       {'id': '9d439543-9d1b-4df2-af32-82e11eccc15a', 'geom': 'PointZ (895178.80000000004656613 1544283.712000000057742 0)'}]

        for item in test_result:
            self.assertIn(item, result, 'Error in {}: {}'.format(item, self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E200401)))

        exp = "\"codigo_error\" = '{}'".format(QUALITY_RULE_ERROR_CODE_E200403)
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 8)
        result = [{'id_punto_lindero': f['id_punto_lindero'], 'id_lindero': f['id_lindero']} for f in error_layer.selectedFeatures()]

        test_result = [{'id_punto_lindero': '8f4e4333-5337-4e58-980a-8e5ca136a1c1', 'id_lindero': '899c1542-51dd-481c-956b-a3668fb9d958'},
                       {'id_punto_lindero': '54adb42d-da97-4cc7-99a9-53ec8160b987', 'id_lindero': '02b06ecb-3048-4d34-814f-ae7578279f5a'},
                       {'id_punto_lindero': 'fc623190-8aa3-49fa-9f15-5aeb7ed05761', 'id_lindero': '899c1542-51dd-481c-956b-a3668fb9d958'},
                       {'id_punto_lindero': '52409e41-1230-4f0b-89e6-5855e89076e2', 'id_lindero': '02b06ecb-3048-4d34-814f-ae7578279f5a'},
                       {'id_punto_lindero': '1cdeca9f-1d4d-4b95-b500-cfbe6bf9caa1', 'id_lindero': 'a9fa0542-687d-43fa-a512-e0368bd7b31a'},
                       {'id_punto_lindero': '19c02ab1-d5ad-4251-aa18-4b894bb7a673', 'id_lindero': 'a9fa0542-687d-43fa-a512-e0368bd7b31a'},
                       {'id_punto_lindero': '5f0a8b5f-c1cc-4c0a-833b-9be1c4d32f9e', 'id_lindero': '3541b8d7-f834-4689-a477-9d5dbd2587ee'},
                       {'id_punto_lindero': 'f7cb6052-4522-4a22-b41a-f6808823d939', 'id_lindero': '02512c9f-8d07-4661-b5a0-10775b16a77d'}]

        for item in test_result:
            self.assertIn(item, result, 'Error in {}: {}'.format(item, self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E200403)))

        exp = "\"codigo_error\" = '{}'".format(QUALITY_RULE_ERROR_CODE_E200402)
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 12)
        result = [{'id_punto_lindero': f['id_punto_lindero'], 'id_lindero': f['id_lindero']} for f in error_layer.selectedFeatures()]

        test_result = [{'id_punto_lindero': 'c5d06a58-447f-4ade-851a-b2a6cb718a61', 'id_lindero': '85f35cf2-8c77-4203-800b-23bdfc97288e'},
                       {'id_punto_lindero': '4dec05b5-5111-4efc-ab72-88699cc29562', 'id_lindero': '08dbd5df-ce3f-4451-9dc9-66f373d2a6fd'},
                       {'id_punto_lindero': '24da07a0-ee53-4055-9e7f-5c0d8f32e8cc', 'id_lindero': '08dbd5df-ce3f-4451-9dc9-66f373d2a6fd'},
                       {'id_punto_lindero': '70e7d6cb-7188-40dd-8c7f-37f7c5928507', 'id_lindero': '85f35cf2-8c77-4203-800b-23bdfc97288e'},
                       {'id_punto_lindero': '9685d46a-c7e1-4775-9695-016847c5b017', 'id_lindero': 'a49ef87f-1fa1-4528-96ff-0332e7e0d0ea'},
                       {'id_punto_lindero': 'b66a3fbb-1f29-407c-ab3c-76b79b9efb3b', 'id_lindero': 'a49ef87f-1fa1-4528-96ff-0332e7e0d0ea'},
                       {'id_punto_lindero': 'a10dc88a-f44e-4ae3-aa59-117a629d7c0e', 'id_lindero': 'a49ef87f-1fa1-4528-96ff-0332e7e0d0ea'},
                       {'id_punto_lindero': '0699195e-29d9-41e6-99d3-be204527266f', 'id_lindero': 'a49ef87f-1fa1-4528-96ff-0332e7e0d0ea'},
                       {'id_punto_lindero': '2daa6ffe-cd14-4303-bfb9-baa30c45ab23', 'id_lindero': '08dbd5df-ce3f-4451-9dc9-66f373d2a6fd'},
                       {'id_punto_lindero': 'ff7bc6db-a02c-47ac-9e8f-f7e9d8c751ff', 'id_lindero': '08dbd5df-ce3f-4451-9dc9-66f373d2a6fd'},
                       {'id_punto_lindero': '804b9ba5-667f-45a9-ac1f-4cddc3eacac9', 'id_lindero': '85f35cf2-8c77-4203-800b-23bdfc97288e'},
                       {'id_punto_lindero': '063c3cf1-bee8-45cf-afdf-7b66e56eb018', 'id_lindero': '85f35cf2-8c77-4203-800b-23bdfc97288e'}]

        for item in test_result:
            self.assertIn(item, result, 'Error in {}: {}'.format(item, self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E200402)))

    def test_topology_boundary_points_must_be_covered_by_boundary_nodes(self):
        print('\nINFO: Validating boundary points must be covered by boundary nodes...')
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES)
        schema_name = 'test_ladm_validations_topology_tables'
        self.db_pg = get_pg_conn(schema_name)
        names = self.db_pg.names

        res, code, msg = self.db_pg.test_connection()
        self.assertTrue(res, msg)
        self.assertIsNotNone(names.LC_BOUNDARY_POINT_T, 'Names is None')

        layers = {names.LC_BOUNDARY_POINT_T: None,
                  names.LC_BOUNDARY_T: None,
                  names.LC_PLOT_T: None,
                  names.POINT_BFS_T: None,
                  names.MORE_BFS_T: None,
                  names.LESS_BFS_T: None}
        self.app.core.get_layers(self.db_pg, layers, load=True)

        boundary_point_layer = layers[names.LC_BOUNDARY_POINT_T]
        self.assertEqual(boundary_point_layer.featureCount(), 109)

        boundary_layer = layers[names.LC_BOUNDARY_T]
        self.assertEqual(boundary_layer.featureCount(), 22)

        plot_layer = layers[names.LC_PLOT_T]
        self.assertEqual(plot_layer.featureCount(), 17)

        point_bfs_layer = layers[names.POINT_BFS_T]
        self.assertEqual(point_bfs_layer.featureCount(), 81)

        more_bfs_layer = layers[names.MORE_BFS_T]
        self.assertEqual(more_bfs_layer.featureCount(), 18)

        less_layer = layers[names.LESS_BFS_T]
        self.assertEqual(less_layer.featureCount(), 6)

        error_layer = QgsVectorLayer("Point?crs={}".format(get_crs_authid(boundary_layer.sourceCrs())), rule.error_table_name, "memory")

        data_provider = error_layer.dataProvider()
        data_provider.addAttributes(rule.error_table_fields)
        error_layer.updateFields()

        features = self.quality_rules.point_quality_rules.get_boundary_points_not_covered_by_boundary_nodes(self.db_pg, boundary_point_layer, boundary_layer, point_bfs_layer, error_layer, names.T_ID_F)

        # the algorithm was successfully executed
        self.assertEqual(len(features), 54)

        error_layer.dataProvider().addFeatures(features)

        exp = "\"codigo_error\" = '{}'".format(QUALITY_RULE_ERROR_CODE_E100301)
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 34)

        result = [{'id': f['id_punto_lindero'], 'geom': f.geometry().asWkt()} for f in error_layer.selectedFeatures()]

        test_result = [{'id': '75390c35-8e23-42a4-85d2-3a1b76ac1f6b', 'geom': 'PointZ (894639.00399999995715916 1544574.38599999994039536 0)'},
                       {'id': 'f6aa74ad-8b86-4f81-a35e-f197e650b7ad', 'geom': 'PointZ (894648.56400000001303852 1544485.16100000008009374 0)'},
                       {'id': '9d8ee614-8019-405a-96df-10f86fca0564', 'geom': 'PointZ (894723.67700000002514571 1544488.34799999999813735 0)'},
                       {'id': '505ed74b-edc0-46f4-a64d-59a45c0ef710', 'geom': 'PointZ (894715.02700000000186265 1544590.31899999990127981 0)'},
                       {'id': '0e6d0256-2bd0-45f0-a3f3-c44d749fa27b', 'geom': 'PointZ (894715.02700000000186265 1544590.31899999990127981 0)'},
                       {'id': '518979a9-e7ba-4c8b-b2bd-703958e724e6', 'geom': 'PointZ (894723.67700000002514571 1544488.34799999999813735 0)'},
                       {'id': '987ea9a0-e6ff-434e-a591-9cb3a655bfaa', 'geom': 'PointZ (894856.60699999995995313 1544597.51000000000931323 0)'},
                       {'id': 'f6f25f99-e9e7-41d4-aac7-b89d836d3be8', 'geom': 'PointZ (894860.856000000028871 1544572.962000000057742 0)'},
                       {'id': 'e3cbcb7e-6321-415c-94e4-81792c75f32d', 'geom': 'PointZ (894879.26599999994505197 1544575.79499999992549419 0)'},
                       {'id': '30e1c7a7-7cf2-4b4e-8924-dda27b91187c', 'geom': 'PointZ (894882.57099999999627471 1544602.70200000004842877 0)'},
                       {'id': '722960e5-923e-41da-a3c1-1dbd98895d3d', 'geom': 'PointZ (894837.25300000002607703 1544520.56300000008195639 0)'},
                       {'id': '56647b74-4146-4792-b64a-69abe1715576', 'geom': 'PointZ (894833.94799999997485429 1544542.75 0)'},
                       {'id': '6b6498c5-36ab-4e1b-bf5b-5078c3dc1661', 'geom': 'PointZ (894634.73699999996460974 1544430.39899999997578561 0)'},
                       {'id': '22ed8d9b-efb8-4fd3-ac6c-91fb310c84ef', 'geom': 'PointZ (894638.04099999996833503 1544358.17299999995157123 0)'},
                       {'id': '8b36e679-73ac-4102-888c-ae8d339e5ea5', 'geom': 'PointZ (894773.52399999997578561 1544367.14199999999254942 0)'},
                       {'id': 'dae06f3c-5be6-4df5-9b15-8d2f564fffba', 'geom': 'PointZ (894768.33100000000558794 1544443.6159999999217689 0)'},
                       {'id': '89b75d46-b128-442f-9125-ca5db804029e', 'geom': 'PointZ (894768.33100000000558794 1544443.6159999999217689 0)'},
                       {'id': 'a3fd37cb-1aa7-48bf-b8d1-1cfdc4083258', 'geom': 'PointZ (894696.625 1544436.52200000011362135 0)'},
                       {'id': '0b479349-9297-4f2a-accc-f5b63852d787', 'geom': 'PointZ (894702.99199999996926636 1544362.47299999999813735 0)'},
                       {'id': '200c5cdf-0cdd-421b-bf37-a19ef5489aa3', 'geom': 'PointZ (894773.52399999997578561 1544367.14199999999254942 0)'},
                       {'id': '62604cd8-f51d-4a3c-b862-ec2f6773c50a', 'geom': 'PointZ (894702.99199999996926636 1544362.47299999999813735 0)'},
                       {'id': '9ae5115d-04aa-4b21-9ead-a236b2fa5c12', 'geom': 'PointZ (894696.625 1544436.52200000011362135 0)'},
                       {'id': 'f5bbf19a-c71c-41ea-a999-ed2524f30042', 'geom': 'PointZ (894634.73699999996460974 1544430.39899999997578561 0)'},
                       {'id': '6edf9b08-2164-41e5-ab7b-8a9cb6897023', 'geom': 'PointZ (894638.04099999996833503 1544358.17299999995157123 0)'},
                       {'id': 'b5f3700f-6f87-4ed8-8369-8139fe4e0817', 'geom': 'PointZ (894847.40200000000186265 1544448.57300000009126961 0)'},
                       {'id': '4ea25d3e-2cd2-4013-83eb-e872f53a03f3', 'geom': 'PointZ (894972.97100000001955777 1544459.43100000009872019 0)'},
                       {'id': '513f1d65-6aad-4292-b6cf-bd5de204be9c', 'geom': 'PointZ (894847.40200000000186265 1544448.57300000009126961 0)'},
                       {'id': 'd67b63ee-4d35-404e-82e6-a067949a5ead', 'geom': 'PointZ (894914.05400000000372529 1544372.94500000006519258 0)'},
                       {'id': 'bcc65b33-fcf3-4ea2-958d-e40f92bf3163', 'geom': 'PointZ (894972.97100000001955777 1544459.43100000009872019 0)'},
                       {'id': '33d46b9d-f19f-4728-825a-d0aa037ce6cf', 'geom': 'PointZ (894914.05400000000372529 1544372.94500000006519258 0)'},
                       {'id': '7d79a0b6-397e-40be-a074-b3675884ae97', 'geom': 'PointZ (894863.92399999999906868 1544306.01000000000931323 0)'},
                       {'id': 'b099757c-2025-4c31-a55b-623106c7b914', 'geom': 'PointZ (894862.50800000003073364 1544287.59899999992921948 0)'},
                       {'id': '1eca7886-3144-443d-b804-ed73c3beb121', 'geom': 'PointZ (894910.65899999998509884 1544288.07099999999627471 0)'},
                       {'id': '0f1968dc-2b0f-4b1d-b7f5-fd755e4785e1', 'geom': 'PointZ (894905.93799999996554106 1544314.50699999998323619 0)'}]

        for item in test_result:
            self.assertIn(item, result, 'Error in {}: {}'.format(item, self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E100301)))

        exp = "\"codigo_error\" = '{}'".format(QUALITY_RULE_ERROR_CODE_E100303)
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 8)
        result = [{'id_punto_lindero': f['id_punto_lindero'], 'id_lindero': f['id_lindero']} for f in error_layer.selectedFeatures()]
        test_result = [{'id_punto_lindero': 'fc623190-8aa3-49fa-9f15-5aeb7ed05761', 'id_lindero': '899c1542-51dd-481c-956b-a3668fb9d958'},
                       {'id_punto_lindero': '54adb42d-da97-4cc7-99a9-53ec8160b987', 'id_lindero': '02b06ecb-3048-4d34-814f-ae7578279f5a'},
                       {'id_punto_lindero': '19c02ab1-d5ad-4251-aa18-4b894bb7a673', 'id_lindero': 'a9fa0542-687d-43fa-a512-e0368bd7b31a'},
                       {'id_punto_lindero': '52409e41-1230-4f0b-89e6-5855e89076e2', 'id_lindero': '02b06ecb-3048-4d34-814f-ae7578279f5a'},
                       {'id_punto_lindero': '8f4e4333-5337-4e58-980a-8e5ca136a1c1', 'id_lindero': '899c1542-51dd-481c-956b-a3668fb9d958'},
                       {'id_punto_lindero': 'f7cb6052-4522-4a22-b41a-f6808823d939', 'id_lindero': '02512c9f-8d07-4661-b5a0-10775b16a77d'},
                       {'id_punto_lindero': '1cdeca9f-1d4d-4b95-b500-cfbe6bf9caa1', 'id_lindero': 'a9fa0542-687d-43fa-a512-e0368bd7b31a'},
                       {'id_punto_lindero': '5f0a8b5f-c1cc-4c0a-833b-9be1c4d32f9e', 'id_lindero': '3541b8d7-f834-4689-a477-9d5dbd2587ee'}]

        for item in test_result:
            self.assertIn(item, result, 'Error in {}: {}'.format(item, self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E100303)))

        exp = "\"codigo_error\" = '{}'".format(QUALITY_RULE_ERROR_CODE_E100302)
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 12)
        result = [{'id_punto_lindero': f['id_punto_lindero'], 'id_lindero': f['id_lindero']} for f in error_layer.selectedFeatures()]

        test_result = [{'id_punto_lindero': '70e7d6cb-7188-40dd-8c7f-37f7c5928507', 'id_lindero': '85f35cf2-8c77-4203-800b-23bdfc97288e'},
                       {'id_punto_lindero': '2daa6ffe-cd14-4303-bfb9-baa30c45ab23', 'id_lindero': '08dbd5df-ce3f-4451-9dc9-66f373d2a6fd'},
                       {'id_punto_lindero': '24da07a0-ee53-4055-9e7f-5c0d8f32e8cc', 'id_lindero': '08dbd5df-ce3f-4451-9dc9-66f373d2a6fd'},
                       {'id_punto_lindero': '063c3cf1-bee8-45cf-afdf-7b66e56eb018', 'id_lindero': '85f35cf2-8c77-4203-800b-23bdfc97288e'},
                       {'id_punto_lindero': '0699195e-29d9-41e6-99d3-be204527266f', 'id_lindero': 'a49ef87f-1fa1-4528-96ff-0332e7e0d0ea'},
                       {'id_punto_lindero': '9685d46a-c7e1-4775-9695-016847c5b017', 'id_lindero': 'a49ef87f-1fa1-4528-96ff-0332e7e0d0ea'},
                       {'id_punto_lindero': 'a10dc88a-f44e-4ae3-aa59-117a629d7c0e', 'id_lindero': 'a49ef87f-1fa1-4528-96ff-0332e7e0d0ea'},
                       {'id_punto_lindero': 'ff7bc6db-a02c-47ac-9e8f-f7e9d8c751ff', 'id_lindero': '08dbd5df-ce3f-4451-9dc9-66f373d2a6fd'},
                       {'id_punto_lindero': 'b66a3fbb-1f29-407c-ab3c-76b79b9efb3b', 'id_lindero': 'a49ef87f-1fa1-4528-96ff-0332e7e0d0ea'},
                       {'id_punto_lindero': '4dec05b5-5111-4efc-ab72-88699cc29562', 'id_lindero': '08dbd5df-ce3f-4451-9dc9-66f373d2a6fd'},
                       {'id_punto_lindero': '804b9ba5-667f-45a9-ac1f-4cddc3eacac9', 'id_lindero': '85f35cf2-8c77-4203-800b-23bdfc97288e'},
                       {'id_punto_lindero': 'c5d06a58-447f-4ade-851a-b2a6cb718a61', 'id_lindero': '85f35cf2-8c77-4203-800b-23bdfc97288e'}]

        for item in test_result:
            self.assertIn(item, result, 'Error in {}: {}'.format(item, self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E100302)))

    def test_topology_plot_must_be_covered_by_boundary(self):
        print('\nINFO: Validating plots must be covered by boundaries...')
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Polygon.PLOTS_COVERED_BY_BOUNDARIES)
        schema_name = 'test_ladm_validations_topology_tables'
        self.db_pg = get_pg_conn(schema_name)
        names = self.db_pg.names

        res, code, msg = self.db_pg.test_connection()
        self.assertTrue(res, msg)
        self.assertIsNotNone(names.LC_BOUNDARY_POINT_T, 'Names is None')

        layers = {names.LC_BOUNDARY_POINT_T: None,
                  names.LC_BOUNDARY_T: None,
                  names.LC_PLOT_T: None,
                  names.POINT_BFS_T: None,
                  names.MORE_BFS_T: None,
                  names.LESS_BFS_T: None}
        self.app.core.get_layers(self.db_pg, layers, load=True)

        boundary_point_layer = layers[names.LC_BOUNDARY_POINT_T]
        self.assertEqual(boundary_point_layer.featureCount(), 109)

        boundary_layer = layers[names.LC_BOUNDARY_T]
        self.assertEqual(boundary_layer.featureCount(), 22)

        plot_layer = layers[names.LC_PLOT_T]
        self.assertEqual(plot_layer.featureCount(), 17)

        point_bfs_layer = layers[names.POINT_BFS_T]
        self.assertEqual(point_bfs_layer.featureCount(), 81)

        more_bfs_layer = layers[names.MORE_BFS_T]
        self.assertEqual(more_bfs_layer.featureCount(), 18)

        less_layer = layers[names.LESS_BFS_T]
        self.assertEqual(less_layer.featureCount(), 6)

        error_layer = QgsVectorLayer("MultiLineString?crs={}".format(get_crs_authid(plot_layer.sourceCrs())), rule.error_table_name, "memory")

        data_provider = error_layer.dataProvider()
        data_provider.addAttributes(rule.error_table_fields)
        error_layer.updateFields()

        features = self.quality_rules.polygon_quality_rules.get_plot_features_not_covered_by_boundaries(self.db_pg, plot_layer, boundary_layer, more_bfs_layer, less_layer, error_layer, names.T_ID_F)

        # the algorithm was successfully executed
        self.assertEqual(len(features), 16)

        error_layer.dataProvider().addFeatures(features)

        exp = "\"codigo_error\" = '{}'".format(QUALITY_RULE_ERROR_CODE_E300401)
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 12)

        result = [{'id': f['id_terreno'], 'geom': f.geometry().asWkt()} for f in error_layer.selectedFeatures()]

        test_result = [{'id': '1a972c2b-c4b1-4e7d-8b4a-5d88398e774a',
                        'geom': 'MultiLineStringZ ((894639.00399999995715916 1544574.38599999994039536 0, 894648.56400000001303852 1544485.16100000008009374 0, 894723.67700000002514571 1544488.34799999999813735 0, 894715.02700000000186265 1544590.31899999990127981 0, 894639.00399999995715916 1544574.38599999994039536 0))'},
                       {'id': '4fbe53ea-4ca6-46ff-ba7e-feba78bef27b',
                        'geom': 'MultiLineStringZ ((894715.02700000000186265 1544590.31899999990127981 0, 894779.66099999996367842 1544604.11800000001676381 0),(894788.15800000005401671 1544496.48799999989569187 0, 894723.67700000002514571 1544488.34799999999813735 0, 894715.02700000000186265 1544590.31899999990127981 0))'},
                       {'id': 'd1181ee8-a259-4d9f-87f6-d1f9912cc581',
                        'geom': 'MultiLineStringZ ((894856.60699999995995313 1544597.51000000000931323 0, 894860.856000000028871 1544572.962000000057742 0, 894879.26599999994505197 1544575.79499999992549419 0, 894882.57099999999627471 1544602.70200000004842877 0, 894856.60699999995995313 1544597.51000000000931323 0),(894810.34499999997206032 1544519.14700000011362135 0, 894837.25300000002607703 1544520.56300000008195639 0, 894833.94799999997485429 1544542.75 0, 894809.40099999995436519 1544539.91800000006332994 0))'},
                       {'id': '5445a5f0-f453-4516-98de-7831fcef5718',
                        'geom': 'MultiLineStringZ ((894634.73699999996460974 1544430.39899999997578561 0, 894638.04099999996833503 1544358.17299999995157123 0, 894773.52399999997578561 1544367.14199999999254942 0, 894768.33100000000558794 1544443.6159999999217689 0, 894634.73699999996460974 1544430.39899999997578561 0))'},
                       {'id': '3879a544-66b3-4284-8132-d88ce6b11fc3',
                        'geom': 'MultiLineStringZ ((894768.33100000000558794 1544443.6159999999217689 0, 894696.625 1544436.52200000011362135 0, 894702.99199999996926636 1544362.47299999999813735 0, 894773.52399999997578561 1544367.14199999999254942 0, 894768.33100000000558794 1544443.6159999999217689 0))'},
                       {'id': 'a83e2386-2ab3-4540-ae1f-79df1a393267',
                        'geom': 'MultiLineStringZ ((894702.99199999996926636 1544362.47299999999813735 0, 894696.625 1544436.52200000011362135 0, 894634.73699999996460974 1544430.39899999997578561 0, 894638.04099999996833503 1544358.17299999995157123 0, 894702.99199999996926636 1544362.47299999999813735 0))'},
                       {'id': '0a34acb7-c9d2-4439-a79e-ee4131eb6e67',
                        'geom': 'MultiLineStringZ ((894847.40200000000186265 1544448.57300000009126961 0, 894852.59499999997206032 1544369.26600000006146729 0),(894986.66099999996367842 1544377.29099999996833503 0, 894972.97100000001955777 1544459.43100000009872019 0, 894904.21900145395193249 1544453.48598809260874987 0),(894904.21900145395193249 1544453.48598809260874987 0, 894847.40200000000186265 1544448.57300000009126961 0))'},
                       {'id': '303bffab-c8b6-4859-ab75-2179ec29a9e1',
                        'geom': 'MultiLineStringZ ((894847.40200000000186265 1544448.57300000009126961 0, 894852.59499999997206032 1544369.26600000006146729 0),(894852.59499999997206032 1544369.26600000006146729 0, 894914.05400000000372529 1544372.94500000006519258 0, 894904.21900000004097819 1544453.48600000003352761 0),(894904.21900000004097819 1544453.48600000003352761 0, 894847.40200000000186265 1544448.57300000009126961 0))'},
                       {'id': '65a3e94f-8ae6-4aa1-b4b4-25bb45596056',
                        'geom': 'MultiLineStringZ ((894904.21900000004097819 1544453.48600000003352761 0, 894972.97100000001955777 1544459.43100000009872019 0, 894986.66099999996367842 1544377.29099999996833503 0),(894986.66099999996367842 1544377.29099999996833503 0, 894914.05400000000372529 1544372.94500000006519258 0, 894904.21900000004097819 1544453.48600000003352761 0))'},
                       {'id': '76cc3820-e993-4c05-8ef9-c680dcb826dd',
                        'geom': 'MultiLineStringZ ((894863.92399999999906868 1544306.01000000000931323 0, 894862.50800000003073364 1544287.59899999992921948 0, 894910.65899999998509884 1544288.07099999999627471 0, 894905.93799999996554106 1544314.50699999998323619 0, 894863.92399999999906868 1544306.01000000000931323 0))'},
                       {'id': 'dc922aaf-bbd1-425d-9527-1026ac380a4d',  # Duplicated vertices
                        'geom': 'MultiLineStringZ ((895053.2219999999506399 1544435.35499999998137355 0, 895119.085573127027601 1544445.42050326871685684 0),(895119.085573127027601 1544445.42050326871685684 0, 895126.55500278470572084 1544446.56200782209634781 0),(895126.55500278470572084 1544446.56200782209634781 0, 895195.31400000001303852 1544457.07000000006519258 0))'},
                       {'id': '7b13e43d-598c-4aae-a529-1aa2c51aafa9',
                        'geom': 'MultiLineStringZ ((871581.97699999995529652 1554559.162999999942258 0, 871583.06900000001769513 1554559.11199999996460974 0, 871586.15099999995436519 1554558.96699999994598329 0))'}]

        for item in test_result:
            self.assertIn(item, result, 'Geometric error in the polygon with id {}'.format(item['id']))

        exp = "\"codigo_error\" = '{}'".format(QUALITY_RULE_ERROR_CODE_E300402)
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 1)
        result = [{'id_terreno': f['id_terreno'], 'id_lindero': f['id_lindero']} for f in error_layer.selectedFeatures()]
        test_result = [{'id_lindero': '02b06ecb-3048-4d34-814f-ae7578279f5a', 'id_terreno': '6a26574f-8c18-42f6-87b9-d50c928afe46'}]
        self.assertEqual(result, test_result, 'Error in: {}'.format(self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E300402)))

        exp = "\"codigo_error\" = '{}'".format(QUALITY_RULE_ERROR_CODE_E300403)
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 1)
        result = [{'id_terreno': f['id_terreno'], 'id_lindero': f['id_lindero']} for f in error_layer.selectedFeatures()]
        test_result = [{'id_lindero': '899c1542-51dd-481c-956b-a3668fb9d958', 'id_terreno': '6a26574f-8c18-42f6-87b9-d50c928afe46'}]
        self.assertEqual(result, test_result, 'Error in: {}'.format(self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E300403)))

        exp = "\"codigo_error\" = '{}'".format(QUALITY_RULE_ERROR_CODE_E300404)
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 1)
        result = [{'id_terreno': f['id_terreno'], 'id_lindero': f['id_lindero']} for f in error_layer.selectedFeatures()]
        test_result = [{'id_lindero': '02512c9f-8d07-4661-b5a0-10775b16a77d', 'id_terreno': 'a10c90ef-58df-479f-9b9c-2cd4bf212378'}]
        self.assertEqual(result, test_result, 'Error in: {}'.format(self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E300404)))

        exp = "\"codigo_error\" = '{}'".format(QUALITY_RULE_ERROR_CODE_E300405)
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 1)
        result = [{'id_terreno': f['id_terreno'], 'id_lindero': f['id_lindero']} for f in error_layer.selectedFeatures()]
        test_result = [{'id_lindero': 'a49ef87f-1fa1-4528-96ff-0332e7e0d0ea', 'id_terreno': 'bbd2469c-ba49-4e7e-b294-68aaafe3c6f0'}]
        self.assertEqual(result, test_result, 'Error in: {}'.format(self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E300405)))

    def test_topology_boundary_must_be_covered_by_plot(self):
        print('\nINFO: Validating boundaries must be covered by plots...')
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Line.BOUNDARIES_COVERED_BY_PLOTS)
        schema_name = 'test_ladm_validations_topology_tables'
        self.db_pg = get_pg_conn(schema_name)
        names = self.db_pg.names

        res, code, msg = self.db_pg.test_connection()
        self.assertTrue(res, msg)
        self.assertIsNotNone(names.LC_BOUNDARY_POINT_T, 'Names is None')

        layers = {names.LC_BOUNDARY_POINT_T: None,
                  names.LC_BOUNDARY_T: None,
                  names.LC_PLOT_T: None,
                  names.POINT_BFS_T: None,
                  names.MORE_BFS_T: None,
                  names.LESS_BFS_T: None}
        self.app.core.get_layers(self.db_pg, layers, load=True)

        boundary_point_layer = layers[names.LC_BOUNDARY_POINT_T]
        self.assertEqual(boundary_point_layer.featureCount(), 109)

        boundary_layer = layers[names.LC_BOUNDARY_T]
        self.assertEqual(boundary_layer.featureCount(), 22)

        plot_layer = layers[names.LC_PLOT_T]
        self.assertEqual(plot_layer.featureCount(), 17)

        point_bfs_layer = layers[names.POINT_BFS_T]
        self.assertEqual(point_bfs_layer.featureCount(), 81)

        more_bfs_layer = layers[names.MORE_BFS_T]
        self.assertEqual(more_bfs_layer.featureCount(), 18)

        less_layer = layers[names.LESS_BFS_T]
        self.assertEqual(less_layer.featureCount(), 6)

        error_layer = QgsVectorLayer("MultiLineString?crs={}".format(get_crs_authid(plot_layer.sourceCrs())), rule.error_table_name, "memory")
        data_provider = error_layer.dataProvider()
        data_provider.addAttributes(rule.error_table_fields)
        error_layer.updateFields()

        features = self.quality_rules.line_quality_rules.get_boundary_features_not_covered_by_plots(self.db_pg, plot_layer, boundary_layer, more_bfs_layer, less_layer, error_layer, names.T_ID_F)

        # the algorithm was successfully executed
        self.assertEqual(len(features), 14)

        error_layer.dataProvider().addFeatures(features)
        exp = "\"codigo_error\" = '{}'".format(QUALITY_RULE_ERROR_CODE_E200301)
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 6)

        result = [{'id': f['id_lindero'], 'id_plot': f['id_terreno'], 'geom': f.geometry().asWkt()} for f in error_layer.selectedFeatures()]

        test_result = [
            {'id': '67d2a8da-5f83-470b-b09c-97e97cff8ab0', 'id_plot': '7b13e43d-598c-4aae-a529-1aa2c51aafa9', 'geom': 'LineStringZ (871560.6650000000372529 1554564.43599999998696148 0, 871564.08799999998882413 1554562.86700000008568168 0, 871564.11399999994318932 1554562.17299999995157123 0, 871581.97699999995529652 1554559.162999999942258 0, 871586.15099999995436519 1554558.96699999994598329 0)'},
            {'id': '9d439543-9d1b-4df2-af32-82e11eccc15a', 'id_plot': None, 'geom': 'MultiLineStringZ ((895120.1720000000204891 1544364.95600000000558794 0, 895070.0779999999795109 1544331.15500000002793968 0, 895121.96699999994598329 1544243.82499999995343387 0, 895178.80000000004656613 1544283.712000000057742 0, 895120.1720000000204891 1544364.95600000000558794 0))'},
            {'id': 'edd15986-68f1-4cab-a6be-5455d6d1ee76', 'id_plot': None, 'geom': 'MultiLineStringZ ((895053.2219999999506399 1544435.35499999998137355 0, 895065.96799999999348074 1544460.84700000006705523 0, 895076.28099999995902181 1544438.87899999995715916 0, 895119.085573127027601 1544445.42050326871685684 0),(895119.085573127027601 1544445.42050326871685684 0, 895126.55500000005122274 1544446.56199999991804361 0, 895126.55500278470572084 1544446.56200782209634781 0),(895126.55500278470572084 1544446.56200782209634781 0, 895138.19400000001769513 1544479.25699999998323619 0, 895150.11300000001210719 1544450.162999999942258 0, 895195.31400000001303852 1544457.07000000006519258 0))'},
            {'id': '539f19b2-c8d1-45b0-a256-44d6147196eb', 'id_plot': None, 'geom': 'MultiLineStringZ ((894732.84299999999348074 1544594.1229999999050051 0, 894770.40800000005401671 1544602.14299999992363155 0))'},
            {'id': 'bf962a29-773e-4bf2-9cf3-99781cd5c46a', 'id_plot': None, 'geom': 'MultiLineStringZ ((894822.14000000001396984 1544541.38800000003539026 0, 894809.40099999995436519 1544539.91800000006332994 0))'},
            {'id': 'f38d0673-2d84-43a3-bb4d-0eb5ddaec02c', 'id_plot': None, 'geom': 'MultiLineStringZ ((894904.21900000004097819 1544453.48600000003352761 0, 894904.21900145395193249 1544453.48598809260874987 0),(894904.21900145395193249 1544453.48598809260874987 0, 894911.74499999999534339 1544391.85100000002421439 0))'}
        ]

        for item in test_result:
           self.assertIn(item, result, 'Error: Boundary is not covered by the plot.  boundary_id = {}'.format(item['id']))

        exp = "\"codigo_error\" = '{}'".format(QUALITY_RULE_ERROR_CODE_E200302)
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 2)
        result = [{'id_terreno': f['id_terreno'], 'id_lindero': f['id_lindero']} for f in error_layer.selectedFeatures()]

        test_result = [{'id_terreno': '4fbe53ea-4ca6-46ff-ba7e-feba78bef27b', 'id_lindero': '96d5cd4f-b21f-4d09-a395-4532a9488676'},
                       {'id_terreno': '6a26574f-8c18-42f6-87b9-d50c928afe46', 'id_lindero': '02b06ecb-3048-4d34-814f-ae7578279f5a'}]

        for item in test_result:
           self.assertIn(item, result, 'Error in: {}'.format(self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E200302)))

        exp = "\"codigo_error\" = '{}'".format(QUALITY_RULE_ERROR_CODE_E200303)
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 2)
        result = [{'id_terreno': f['id_terreno'], 'id_lindero': f['id_lindero']} for f in error_layer.selectedFeatures()]

        test_result = [{'id_terreno': 'd1181ee8-a259-4d9f-87f6-d1f9912cc581', 'id_lindero': '96de69a6-72f4-4817-9456-d6786edc64f9'},
                       {'id_terreno': '6a26574f-8c18-42f6-87b9-d50c928afe46', 'id_lindero': '899c1542-51dd-481c-956b-a3668fb9d958'}]

        for item in test_result:
           self.assertIn(item, result, 'Error in: {}'.format(self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E200303)))

        exp = "\"codigo_error\" = '{}'".format(QUALITY_RULE_ERROR_CODE_E200304)
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 2)
        result = [{'id_terreno': f['id_terreno'], 'id_lindero': f['id_lindero']} for f in error_layer.selectedFeatures()]
        test_result = [{'id_terreno': '76cc3820-e993-4c05-8ef9-c680dcb826dd', 'id_lindero': '32283a5f-c945-4ba3-a2f4-8960fdd157d5'},
                       {'id_terreno': 'a10c90ef-58df-479f-9b9c-2cd4bf212378', 'id_lindero': '02512c9f-8d07-4661-b5a0-10775b16a77d'}]

        for item in test_result:
           self.assertIn(item, result, 'Error in: {}'.format(self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E200304)))

        exp = "\"codigo_error\" = '{}'".format(QUALITY_RULE_ERROR_CODE_E200304)
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 2)
        result = [{'id_terreno': f['id_terreno'], 'id_lindero': f['id_lindero']} for f in error_layer.selectedFeatures()]
        test_result = [{'id_terreno': '76cc3820-e993-4c05-8ef9-c680dcb826dd', 'id_lindero': '32283a5f-c945-4ba3-a2f4-8960fdd157d5'},
                       {'id_terreno': 'a10c90ef-58df-479f-9b9c-2cd4bf212378', 'id_lindero': '02512c9f-8d07-4661-b5a0-10775b16a77d'}]

        for item in test_result:
           self.assertIn(item, result, 'Error in: {}'.format(self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E200305)))

    def test_get_missing_boundary_points_in_boundaries(self):
        print('\nINFO: Validating missing boundary points in boundaries...')

        gpkg_path = get_test_copy_path('db/static/gpkg/quality_validations.gpkg')
        self.db_gpkg = get_gpkg_conn('tests_quality_validations_gpkg')
        self.db_gpkg.names.T_ID_F = 't_id'  # Static label is set because the database does not have the ladm structure

        uri = gpkg_path + '|layername={layername}'.format(layername='boundary')
        boundary_layer = QgsVectorLayer(uri, 'boundary', 'ogr')
        uri = gpkg_path + '|layername={layername}'.format(layername='boundary_points')
        point_layer = QgsVectorLayer(uri, 'boundary_points', 'ogr')

        boundary_features = [feature for feature in boundary_layer.getFeatures()]
        self.assertEqual(len(boundary_features), 8)

        point_features = [feature for feature in point_layer.getFeatures()]
        self.assertEqual(len(point_features), 9)

        missing_points = self.quality_rules.point_quality_rules.get_missing_boundary_points_in_boundaries(self.db_gpkg, point_layer, boundary_layer)

        geometries = [geom.asWkt() for k, v in missing_points.items() for geom in v]

        self.assertEqual(len(geometries), 7)
        self.assertIn('Point (962933.31867467891424894 1077991.8205501982010901)', geometries)
        self.assertIn('Point (963525.77339165192097425 1078270.34507849626243114)', geometries)
        self.assertIn('Point (963820.82056145928800106 1078251.46205962845124304)', geometries)
        self.assertIn('Point (963202.40169354318641126 1078020.14507849956862628)', geometries)
        self.assertIn('Point (963287.37527844763826579 1078395.44507849449291825)', geometries)
        self.assertIn('Point (963353.46584448451176286 1078440.2922483051661402)', geometries)
        self.assertIn('Point (963447.88093882286921144 1078482.77904075756669044)', geometries)

    def test_get_missing_boundary_points_in_boundaries_without_points(self):
        print('\nINFO: Validating missing boundary points in boundaries without points...')

        gpkg_path = get_test_copy_path('db/static/gpkg/quality_validations.gpkg')
        self.db_gpkg = get_gpkg_conn('tests_quality_validations_gpkg')
        self.db_gpkg.names.T_ID_F = 't_id'  # Static label is set because the database does not have the ladm structure

        uri = gpkg_path + '|layername={layername}'.format(layername='boundary')
        boundary_layer = QgsVectorLayer(uri, 'boundary', 'ogr')
        point_layer = QgsVectorLayer("MultiPoint?crs={}".format(get_crs_authid(boundary_layer.sourceCrs())), "Boundary points", "memory")

        boundary_features = [feature for feature in boundary_layer.getFeatures()]
        self.assertEqual(len(boundary_features), 8)

        point_features = [feature for feature in point_layer.getFeatures()]
        self.assertEqual(len(point_features), 0)

        missing_points = self.quality_rules.point_quality_rules.get_missing_boundary_points_in_boundaries(self.db_gpkg, point_layer, boundary_layer)

        geometries = [geom.asWkt() for k, v in missing_points.items() for geom in v]

        self.assertEqual(len(geometries), 16)
        self.assertIn('Point (963303.89791995682753623 1077772.30545586138032377)', geometries)
        self.assertIn('Point (962933.31867467891424894 1077991.8205501982010901)', geometries)
        self.assertIn('Point (963065.49980675254482776 1078159.40734264859929681)', geometries)
        self.assertIn('Point (963395.95263693667948246 1078256.18281434546224773)', geometries)
        self.assertIn('Point (963525.77339165192097425 1078270.34507849626243114)', geometries)
        self.assertIn('Point (963709.88282561174128205 1078376.56205962691456079)', geometries)
        self.assertIn('Point (963820.82056145928800106 1078251.46205962845124304)', geometries)
        self.assertIn('Point (963608.38659919798374176 1078138.16394642251543701)', geometries)
        self.assertIn('Point (963431.35829731356352568 1077965.85639925510622561)', geometries)
        self.assertIn('Point (963202.40169354318641126 1078020.14507849956862628)', geometries)
        self.assertIn('Point (963277.93376901384908706 1078371.84130490990355611)', geometries)
        self.assertIn('Point (963287.37527844763826579 1078395.44507849449291825)', geometries)
        self.assertIn('Point (963332.22244825831148773 1078402.52621057000942528)', geometries)
        self.assertIn('Point (963353.46584448451176286 1078440.2922483051661402)', geometries)
        self.assertIn('Point (963447.88093882286921144 1078482.77904075756669044)', geometries)
        self.assertIn('Point (963521.05263693502638489 1078508.74319170042872429)', geometries)

    def test_check_missing_survey_points_in_buildings(self):
        print('\nINFO: Validating missing survey points in buildings...')

        gpkg_path = get_test_copy_path('db/static/gpkg/quality_validations.gpkg')
        self.db_gpkg = get_gpkg_conn('tests_quality_validations_gpkg')
        self.db_gpkg.names.T_ID_F = 't_id'  # Static label is set because the database does not have the ladm structure

        uri = gpkg_path + '|layername={layername}'.format(layername='construccion')
        building_layer = QgsVectorLayer(uri, 'construccion', 'ogr')
        uril = gpkg_path + '|layername={layername}'.format(layername='puntolevantamiento')
        survey_layer = QgsVectorLayer(uril, 'puntolevantamiento', 'ogr')

        building_features = [feature for feature in building_layer.getFeatures()]
        self.assertEqual(len(building_features), 4)

        survey_features = [feature for feature in survey_layer.getFeatures()]
        self.assertEqual(len(survey_features), 11)

        missing_points = self.quality_rules.point_quality_rules.get_missing_boundary_points_in_boundaries(self.db_gpkg, survey_layer, building_layer)

        geometries = [geom.asWkt() for k, v in missing_points.items() for geom in v]

        self.assertEqual(len(geometries), 9)
        self.assertIn('Point (1091236.35652560647577047 1121774.96929413848556578)', geometries)
        self.assertIn('Point (1091186.87442427431233227 1121732.1977132954634726)', geometries)
        self.assertIn('Point (1091077.77337037585675716 1121602.12974193692207336)', geometries)
        self.assertIn('Point (1091205.35301685449667275 1121546.94486430194228888)', geometries)
        self.assertIn('Point (1091305.89359214110299945 1121627.02843385003507137)', geometries)
        self.assertIn('Point (1091408.70686221891082823 1121544.53974786633625627)', geometries)
        self.assertIn('Point (1091371.58370406995527446 1121507.19097788003273308)', geometries)
        self.assertIn('Point (1091314.24563915398903191 1121448.97160633862949908)', geometries)
        self.assertIn('Point (1091213.62314918311312795 1121543.89559642062522471)', geometries)

    def test_check_plot_nodes_covered_by_boundary_points(self):
        print('\nINFO: Validating plot nodes are covered by boundary points...')

        gpkg_path = get_test_copy_path('db/static/gpkg/quality_validations.gpkg')
        self.db_gpkg = get_gpkg_conn('tests_quality_validations_gpkg')
        names = self.db_gpkg.names
        names.T_ID_F = 't_id'  # Static label is set because the database does not have the ladm structure

        uri = gpkg_path + '|layername={layername}'.format(layername='puntolindero')
        boundary_point_layer = QgsVectorLayer(uri, 'puntolindero', 'ogr')
        self.assertEqual(boundary_point_layer.featureCount(), 82)

        uri = gpkg_path + '|layername={layername}'.format(layername='terreno')
        plot_layer = QgsVectorLayer(uri, 'terreno', 'ogr')
        self.assertEqual(plot_layer.featureCount(), 12)

        features = PolygonQualityRules.get_plot_nodes_features_not_covered_by_boundary_points(boundary_point_layer,
                                                                                              plot_layer,
                                                                                              names.T_ID_F)
        self.assertEqual(len(features), 10)
        result = [{'geom': f[1].asWkt(), 'id': f[0]} for f in features]

        test_result = [{'geom': 'Point (894809.40075360587798059 1544539.9176194816827774)', 'id': 4},
                       {'geom': 'Point (894810.34488280047662556 1544519.14677720214240253)', 'id': 4},
                       {'geom': 'Point (894837.25256484432611614 1544520.56297099380753934)', 'id': 4},
                       {'geom': 'Point (894833.94811266358010471 1544542.75000706524588168)', 'id': 4},
                       {'geom': 'Point (894852.59466425550635904 1544369.26626757089979947)', 'id': 11},
                       {'geom': 'Point (894852.59466425550635904 1544369.26626757089979947)', 'id': 12},
                       {'geom': 'Point (894934.73390417906921357 1544264.93999157636426389)', 'id': 19},
                       {'geom': 'Point (894484.66213072568643838 1544624.06759340292774141)', 'id': 41},
                       {'geom': 'Point (894533.21481920615769923 1544601.79047751193866134)', 'id': 41},
                       {'geom': 'Point (894505.22562231740448624 1544589.22389931697398424)', 'id': 41}]

        for item in test_result:
            self.assertIn(item, result,
                          'Error in: Plot node {} is not covered by boundary point'.format(item['id']))

    def test_no_error_quality_rule(self):
        print('\nINFO: Validating no errors in quality rules...')
        gpkg_path = get_test_copy_path('db/ladm/gpkg/test_valid_quality_rules_v1_1.gpkg')
        self.db_gpkg = get_gpkg_conn_from_path(gpkg_path)
        res, code, msg = self.db_gpkg.test_connection()
        self.assertTrue(res, msg)

        query_manager = ConfigDBsSupported().get_db_factory(self.db_gpkg.engine).get_ladm_queries()

        rules = [EnumQualityRule.Point.OVERLAPS_IN_BOUNDARY_POINTS,
                 EnumQualityRule.Point.OVERLAPS_IN_CONTROL_POINTS,
                 EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES,
                 EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_PLOT_NODES,
                 EnumQualityRule.Line.BOUNDARIES_ARE_NOT_SPLIT,
                 EnumQualityRule.Line.BOUNDARIES_COVERED_BY_PLOTS,
                 EnumQualityRule.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS,
                 EnumQualityRule.Line.DANGLES_IN_BOUNDARIES,
                 EnumQualityRule.Polygon.OVERLAPS_IN_PLOTS,
                 EnumQualityRule.Polygon.OVERLAPS_IN_BUILDINGS,
                 EnumQualityRule.Polygon.OVERLAPS_IN_RIGHTS_OF_WAY,
                 EnumQualityRule.Polygon.PLOTS_COVERED_BY_BOUNDARIES,
                 EnumQualityRule.Polygon.RIGHT_OF_WAY_OVERLAPS_BUILDINGS,
                 EnumQualityRule.Polygon.GAPS_IN_PLOTS,
                 EnumQualityRule.Polygon.MULTIPART_IN_RIGHT_OF_WAY,
                 EnumQualityRule.Polygon.PLOT_NODES_COVERED_BY_BOUNDARY_POINTS,
                 EnumQualityRule.Polygon.BUILDINGS_SHOULD_BE_WITHIN_PLOTS,
                 EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_PLOTS]

        layer_manager = QualityRuleLayerManager(self.db_gpkg, rules, 0)

        # Points rules
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Point.OVERLAPS_IN_BOUNDARY_POINTS, layer_manager.get_layers(EnumQualityRule.Point.OVERLAPS_IN_BOUNDARY_POINTS)).level, Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Point.OVERLAPS_IN_CONTROL_POINTS, layer_manager.get_layers(EnumQualityRule.Point.OVERLAPS_IN_CONTROL_POINTS)).level, Qgis.Warning)  # "There are no points in layer 'lc_puntocontrol' to check for overlaps!"
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES, layer_manager.get_layers(EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES)).level, Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_PLOT_NODES, layer_manager.get_layers(EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_PLOT_NODES)).level, Qgis.Success)

        # Lines rules
        # TODO: Fix the OVERLAPS_IN_BOUNDARIES test!
        # self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Line.OVERLAPS_IN_BOUNDARIES)[1], Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Line.BOUNDARIES_ARE_NOT_SPLIT, layer_manager.get_layers(EnumQualityRule.Line.BOUNDARIES_ARE_NOT_SPLIT)).level, Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Line.BOUNDARIES_COVERED_BY_PLOTS, layer_manager.get_layers(EnumQualityRule.Line.BOUNDARIES_COVERED_BY_PLOTS)).level, Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS, layer_manager.get_layers(EnumQualityRule.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS)).level, Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Line.DANGLES_IN_BOUNDARIES, layer_manager.get_layers(EnumQualityRule.Line.DANGLES_IN_BOUNDARIES)).level, Qgis.Success)

        # Polygons rules
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Polygon.OVERLAPS_IN_PLOTS, layer_manager.get_layers(EnumQualityRule.Polygon.OVERLAPS_IN_PLOTS)).level, Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Polygon.OVERLAPS_IN_BUILDINGS, layer_manager.get_layers(EnumQualityRule.Polygon.OVERLAPS_IN_BUILDINGS)).level, Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Polygon.OVERLAPS_IN_RIGHTS_OF_WAY, layer_manager.get_layers(EnumQualityRule.Polygon.OVERLAPS_IN_RIGHTS_OF_WAY)).level, Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Polygon.PLOTS_COVERED_BY_BOUNDARIES, layer_manager.get_layers(EnumQualityRule.Polygon.PLOTS_COVERED_BY_BOUNDARIES)).level, Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Polygon.RIGHT_OF_WAY_OVERLAPS_BUILDINGS, layer_manager.get_layers(EnumQualityRule.Polygon.RIGHT_OF_WAY_OVERLAPS_BUILDINGS)).level, Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Polygon.GAPS_IN_PLOTS, layer_manager.get_layers(EnumQualityRule.Polygon.GAPS_IN_PLOTS)).level, Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Polygon.MULTIPART_IN_RIGHT_OF_WAY, layer_manager.get_layers(EnumQualityRule.Polygon.MULTIPART_IN_RIGHT_OF_WAY)).level, Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Polygon.PLOT_NODES_COVERED_BY_BOUNDARY_POINTS, layer_manager.get_layers(EnumQualityRule.Polygon.PLOT_NODES_COVERED_BY_BOUNDARY_POINTS)).level, Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Polygon.BUILDINGS_SHOULD_BE_WITHIN_PLOTS, layer_manager.get_layers(EnumQualityRule.Polygon.BUILDINGS_SHOULD_BE_WITHIN_PLOTS)).level, Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_PLOTS, layer_manager.get_layers(EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_PLOTS)).level, Qgis.Success)

        # Logic rules
        res, records = query_manager.get_parcels_with_no_right(self.db_gpkg)
        self.assertTrue(res)
        self.assertEqual(len(records), 0)

        res, records = query_manager.get_group_party_fractions_that_do_not_make_one(self.db_gpkg)
        self.assertTrue(res)
        self.assertEqual(len(records), 0)

        res, records = query_manager.get_parcels_with_invalid_department_code(self.db_gpkg)
        self.assertTrue(res)
        self.assertEqual(len(records), 0)

        res, records = query_manager.get_parcels_with_invalid_municipality_code(self.db_gpkg)
        self.assertTrue(res)
        self.assertEqual(len(records), 0)

        res, records = query_manager.get_parcels_with_invalid_parcel_number(self.db_gpkg)
        self.assertTrue(res)
        self.assertEqual(len(records), 0)

        res, records = query_manager.get_parcels_with_invalid_previous_parcel_number(self.db_gpkg)
        self.assertTrue(res)
        self.assertEqual(len(records), 0)

        res, records = query_manager.get_invalid_col_party_type_natural(self.db_gpkg)
        self.assertTrue(res)
        self.assertEqual(len(records), 0)

        res, records = query_manager.get_invalid_col_party_type_no_natural(self.db_gpkg)
        self.assertTrue(res)
        self.assertEqual(len(records), 0)

        res, records = query_manager.get_parcels_with_invalid_parcel_type_and_22_position_number(self.db_gpkg)
        self.assertTrue(res)
        self.assertEqual(len(records), 0)

        res, records = query_manager.get_uebaunit_parcel(self.db_gpkg)
        self.assertTrue(res)
        self.assertEqual(len(records), 0)

    def test_logic_quality_rules_pg(self):
        print('\nINFO: Validating logic quality rules PG...')
        restore_schema('test_logic_quality_rules')
        db_pg = get_pg_conn('test_logic_quality_rules')
        names = db_pg.names
        res, code, msg = db_pg.test_connection()

        self.assertTrue(res, msg)
        self.assertIsNotNone(names.LC_BOUNDARY_POINT_T, 'Names is None')

        self.check_logic_quality_rules(db_pg)

    def test_logic_quality_rules_gpkg(self):
        print('\nINFO: Validating logic quality rules GPKG...')
        db_gpkg = get_gpkg_conn('test_logic_quality_rules_gpkg')
        res, code, msg = db_gpkg.test_connection()
        self.assertTrue(res, msg)

        self.check_logic_quality_rules(db_gpkg)

    def check_logic_quality_rules(self, db):
        query_manager = ConfigDBsSupported().get_db_factory(db.engine).get_ladm_queries()

        # Logic rules
        res, records = query_manager.get_parcels_with_no_right(db)
        self.assertTrue(res)
        self.assertEqual(len(records), 2)

        res, records = query_manager.get_group_party_fractions_that_do_not_make_one(db)
        self.assertTrue(res)
        self.assertEqual(len(records), 1)

        res, records = query_manager.get_parcels_with_invalid_department_code(db)
        self.assertTrue(res)
        self.assertEqual(len(records), 4)

        res, records = query_manager.get_parcels_with_invalid_municipality_code(db)
        self.assertTrue(res)
        self.assertEqual(len(records), 3)

        res, records = query_manager.get_parcels_with_invalid_parcel_number(db)
        self.assertTrue(res)
        self.assertEqual(len(records), 6)

        res, records = query_manager.get_parcels_with_invalid_previous_parcel_number(db)
        self.assertTrue(res)
        self.assertEqual(len(records), 4)

        res, records = query_manager.get_invalid_col_party_type_natural(db)
        self.assertTrue(res)
        self.assertEqual(len(records), 5)

        res, records = query_manager.get_invalid_col_party_type_no_natural(db)
        self.assertTrue(res)
        self.assertEqual(len(records), 3)

        res, records = query_manager.get_parcels_with_invalid_parcel_type_and_22_position_number(db)
        self.assertTrue(res)
        self.assertEqual(len(records), 10)

        res, records = query_manager.get_uebaunit_parcel(db)
        self.assertTrue(res)
        self.assertEqual(len(records), 10)

    def test_tolerance_for_building_should_be_within_plot_rule(self):
        print('\nINFO: Validating tolerance in building should be within plot...')

        db_gpkg = get_gpkg_conn('tests_quality_rules_tolerance_gpkg')
        db_gpkg.test_connection()  # To generate DBMappingRegistry object
        names = db_gpkg.names

        # Tolerance: 0mm
        print("INFO: Testing with 0mm of tolerance...")
        rule_key = EnumQualityRule.Polygon.BUILDINGS_SHOULD_BE_WITHIN_PLOTS
        rule_name = "Buildings should be within Plots"
        list_rules = [rule_key]  # We'll test that we can use a list of rule keys as parameter for the QREngine
        quality_rule_engine = QualityRuleEngine(db_gpkg, list_rules, 0)
        res = quality_rule_engine.validate_quality_rules()

        self.assertEqual(res.result(rule_key).level, Qgis.Critical)
        error_layer = res.result(rule_key).error_layer
        self.assertEqual(error_layer.featureCount(), 27)
        features = [f for f in error_layer.getFeatures("codigo_error = '{}'".format(QUALITY_RULE_ERROR_CODE_E300902))]
        expected_t_ili_tids = ['117f44fd-5485-4560-9708-911e88e03c15', '1b0d4d48-6f42-40f6-a196-947bf43ec708',
                               '1b1bfc0d-eaaf-4635-bc19-90daa1d9bd87', '1d0c1b12-cead-413c-b38c-de9a423cdc66',
                               '2d323bb9-19d7-41f7-8894-e9c62f80ceb5', '2e11e7f9-1209-4d8b-9bd2-84f268ac6faf',
                               '72567696-053c-4f78-8db6-17084bbce012', 'a468fa02-6cf6-4f20-986b-ccdfb4c201d2',
                               'b311be43-50e5-46ac-9e13-bc6730be36b6', 'c1b53a98-c3b0-4de1-8293-b3455c4bd517',
                               'c8ef8b15-c776-42ef-a30c-822001be7460', 'e5e60bc6-132a-4428-9b32-9046278e0bd2',
                               'e912cb4f-f76f-45d7-be83-702624db1ea0']
        self.assertEqual(len(features), len(expected_t_ili_tids))  # 13
        self.assertEqual(expected_t_ili_tids, sorted([f['id_construccion'] for f in features]))

        # Tolerance: 1mm
        print("INFO: Testing with 1mm of tolerance...")
        quality_rule_engine.initialize(db_gpkg, list_rules, 1, False)
        res = quality_rule_engine.validate_quality_rules()

        self.assertEqual(res.result(rule_key).level, Qgis.Critical)
        error_layer = res.result(rule_key).error_layer
        self.assertEqual(error_layer.featureCount(), 27)
        features = [f for f in
                    error_layer.getFeatures("codigo_error = '{}'".format(QUALITY_RULE_ERROR_CODE_E300902))]
        expected_t_ili_tids = ['117f44fd-5485-4560-9708-911e88e03c15',
                               'c8ef8b15-c776-42ef-a30c-822001be7460']
        self.assertEqual(len(features), len(expected_t_ili_tids))  # 2
        self.assertEqual(expected_t_ili_tids, sorted([f['id_construccion'] for f in features]))

        # Tolerance: 2mm
        print("INFO: Testing with 2mm of tolerance...")
        quality_rule_engine.initialize(db_gpkg, list_rules, 2, False)
        res = quality_rule_engine.validate_quality_rules()

        self.assertEqual(res.result(rule_key).level, Qgis.Critical)
        error_layer = res.result(rule_key).error_layer
        self.assertEqual(error_layer.featureCount(), 27)
        features = [f for f in error_layer.getFeatures("codigo_error = '{}'".format(QUALITY_RULE_ERROR_CODE_E300902))]
        expected_t_ili_tids = ['117f44fd-5485-4560-9708-911e88e03c15']
        self.assertEqual(len(features), len(expected_t_ili_tids))
        self.assertEqual(expected_t_ili_tids, [f['id_construccion'] for f in features])

    def test_tolerance_for_building_unit_should_be_within_plot_rule(self):
        print('\nINFO: Validating tolerance in building unit should be within plot...')

        db_gpkg = get_gpkg_conn('tests_quality_rules_tolerance_gpkg')
        db_gpkg.test_connection()  # To generate DBMappingRegistry object
        names = db_gpkg.names

        # Tolerance: 0mm
        print("INFO: Testing with 0mm of tolerance...")
        rule_key = EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_PLOTS
        rule_name = "Buildings units should be within Plots"
        dict_rules = {rule_key: rule_name}  # QualityRuleManager().get_quality_rule()
        quality_rule_engine = QualityRuleEngine(db_gpkg, dict_rules, 0)
        res = quality_rule_engine.validate_quality_rules()

        self.assertEqual(res.result(rule_key).level, Qgis.Critical)
        error_layer = res.result(rule_key).error_layer
        self.assertEqual(error_layer.featureCount(), 49)
        features = [f for f in error_layer.getFeatures("codigo_error = '{}'".format(QUALITY_RULE_ERROR_CODE_E301002))]
        expected_t_ili_tids = ['0af93cab-1989-4b44-ad8d-0f3a1fb8dbd5', '14c31044-de9d-4797-83c9-7b40c44a6a15',
                               '1cf7ee73-4d06-4134-bd3c-00d6c5dbab46', '1dcfd30f-ea16-4afb-9050-f09199b08162',
                               '27272d59-1635-4ce6-babf-efc1122815ad', '284415e7-5a71-49f6-af8c-6a8fab6f6e68',
                               '297870c1-063b-4e56-917e-ea2ed86e8cf7', '55988f7b-3b05-438c-8a2a-34948096cd63',
                               '6cf8733a-38b7-4923-8ccf-edd4b20c173f', '710bcff9-3b47-4ba9-a430-fcc6532092e3',
                               '8e043e1f-ab9c-47fd-9702-bb2301863a17', 'da374f95-4674-4e47-b0af-8780c7d2c94b',
                               'dcfbb7af-e211-48b4-b421-2a3b7d70b5ce', 'df24bc58-84f0-4fb1-9e3f-5ee1f961e63b',
                               'e2002bad-c64c-4b47-a00a-d62a565ea339', 'e3692ae7-0df9-4473-a6da-836539dcc077',
                               'ebc11cf4-53a1-4f8a-80ff-c7fc271bad90', 'f145a235-4eb9-476a-be73-64d33d5101d7',
                               'faafc505-6943-429c-8350-b5d4402199c4']
        self.assertEqual(len(features), len(expected_t_ili_tids))  # 19
        self.assertEqual(expected_t_ili_tids, sorted([f['id_unidad_construccion'] for f in features]))

        # Tolerance: 1mm
        print("INFO: Testing with 1mm of tolerance...")
        quality_rule_engine.initialize(db_gpkg, dict_rules, 1, False)
        res = quality_rule_engine.validate_quality_rules()

        self.assertEqual(res.result(rule_key).level, Qgis.Critical)
        error_layer = res.result(rule_key).error_layer
        self.assertEqual(error_layer.featureCount(), 49)
        features = [f for f in error_layer.getFeatures("codigo_error = '{}'".format(QUALITY_RULE_ERROR_CODE_E301002))]
        expected_t_ili_tids = ['ebc11cf4-53a1-4f8a-80ff-c7fc271bad90',
                               'faafc505-6943-429c-8350-b5d4402199c4',
                               'e2002bad-c64c-4b47-a00a-d62a565ea339']
        self.assertEqual(len(features), len(expected_t_ili_tids))  # 3
        self.assertEqual(sorted(expected_t_ili_tids), sorted([f['id_unidad_construccion'] for f in features]))

        # Tolerance: 2mm
        print("INFO: Testing with 2mm of tolerance...")
        quality_rule_engine.initialize(db_gpkg, dict_rules, 2, False)
        res = quality_rule_engine.validate_quality_rules()

        self.assertEqual(res.result(rule_key).level, Qgis.Critical)
        error_layer = res.result(rule_key).error_layer
        self.assertEqual(error_layer.featureCount(), 49)
        features = [f for f in error_layer.getFeatures("codigo_error = '{}'".format(QUALITY_RULE_ERROR_CODE_E301002))]
        expected_t_ili_tids = ['ebc11cf4-53a1-4f8a-80ff-c7fc271bad90']
        self.assertEqual(len(features), len(expected_t_ili_tids))
        self.assertEqual(expected_t_ili_tids, [f['id_unidad_construccion'] for f in features])

    def test_tolerance_for_building_unit_should_be_within_building_rule(self):
        print('\nINFO: Validating tolerance in building unit should be within building...')

        db_gpkg = get_gpkg_conn('tests_quality_rules_tolerance_gpkg')
        db_gpkg.test_connection()  # To generate DBMappingRegistry object
        names = db_gpkg.names

        # Tolerance: 0mm
        print("INFO: Testing with 0mm of tolerance...")
        rule_key = EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_BUILDINGS
        rule_name = "Buildings units should be within Buildings"
        dict_rules = {rule_key: rule_name}  # QualityRuleManager().get_quality_rule()
        quality_rule_engine = QualityRuleEngine(db_gpkg, dict_rules, 0)
        res = quality_rule_engine.validate_quality_rules()

        self.assertEqual(res.result(rule_key).level, Qgis.Critical)
        error_layer = res.result(rule_key).error_layer
        self.assertEqual(error_layer.featureCount(), 49)
        features = [f for f in error_layer.getFeatures("codigo_error = '{}'".format(QUALITY_RULE_ERROR_CODE_E301102))]
        expected_t_ili_tids = ['1dcfd30f-ea16-4afb-9050-f09199b08162',
                               '7504133f-9a00-40fa-9e8d-4ab64a3543aa',
                               '8e043e1f-ab9c-47fd-9702-bb2301863a17']
        self.assertEqual(len(features), len(expected_t_ili_tids))  # 3
        self.assertEqual(expected_t_ili_tids, sorted([f['id_unidad_construccion'] for f in features]))

        # Tolerance: 1mm
        print("INFO: Testing with 1mm of tolerance...")
        quality_rule_engine.initialize(db_gpkg, dict_rules, 1, False)
        res = quality_rule_engine.validate_quality_rules()

        self.assertEqual(res.result(rule_key).level, Qgis.Critical)
        error_layer = res.result(rule_key).error_layer
        self.assertEqual(error_layer.featureCount(), 49)
        features = [f for f in error_layer.getFeatures("codigo_error = '{}'".format(QUALITY_RULE_ERROR_CODE_E301102))]
        expected_t_ili_tids = ['1dcfd30f-ea16-4afb-9050-f09199b08162',
                               '8e043e1f-ab9c-47fd-9702-bb2301863a17']
        self.assertEqual(len(features), len(expected_t_ili_tids))
        self.assertEqual(sorted(expected_t_ili_tids), sorted([f['id_unidad_construccion'] for f in features]))

        # Tolerance: 2mm
        print("INFO: Testing with 2mm of tolerance...")
        quality_rule_engine.initialize(db_gpkg, dict_rules, 2, False)
        res = quality_rule_engine.validate_quality_rules()

        self.assertEqual(res.result(rule_key).level, Qgis.Critical)
        error_layer = res.result(rule_key).error_layer
        self.assertEqual(error_layer.featureCount(), 49)
        features = [f for f in error_layer.getFeatures("codigo_error = '{}'".format(QUALITY_RULE_ERROR_CODE_E301102))]
        expected_t_ili_tids = ['8e043e1f-ab9c-47fd-9702-bb2301863a17']
        self.assertEqual(len(features), len(expected_t_ili_tids))
        self.assertEqual(expected_t_ili_tids, [f['id_unidad_construccion'] for f in features])

    def test_validate_nonexistent_rule_key(self):
        print('\nINFO: Validating nonexistent rule key...')

        db_gpkg = get_gpkg_conn('tests_quality_rules_tolerance_gpkg')
        db_gpkg.test_connection()  # To generate DBMappingRegistry object

        rule_key = 9999
        quality_rule_engine = QualityRuleEngine(db_gpkg, [rule_key], 0)
        res = quality_rule_engine.validate_quality_rules()
        self.assertIsNone(res.result(rule_key).level)

    @classmethod
    def tearDownClass(cls):
        print("\nINFO: Resetting tolerance value to {}...".format(DEFAULT_TOLERANCE_VALUE))
        cls.app.settings.tolerance = DEFAULT_TOLERANCE_VALUE

        print("INFO: Unloading Model Baker...")
        unload_qgis_model_baker()


if __name__ == '__main__':
    nose2.main()
