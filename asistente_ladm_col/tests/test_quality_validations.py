import nose2
import re

from asistente_ladm_col.logic.quality.quality_rule_layer_manager import QualityRuleLayerManager
from qgis.core import (QgsVectorLayer,
                       QgsWkbTypes,
                       Qgis, 
                       QgsGeometry)
from qgis.testing import (unittest,
                          start_app)

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.lib.geometry import GeometryUtils
from asistente_ladm_col.utils.crs_utils import get_crs_authid

start_app()  # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.config.config_db_supported import ConfigDBsSupported
from asistente_ladm_col.logic.quality.quality_rules import QualityRules
from asistente_ladm_col.logic.quality.point_quality_rules import PointQualityRules
from asistente_ladm_col.logic.quality.polygon_quality_rules import PolygonQualityRules
from asistente_ladm_col.tests.utils import (import_qgis_model_baker,
                                            import_processing,
                                            get_test_copy_path,
                                            get_pg_conn,
                                            get_gpkg_conn,
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
                                                            QUALITY_RULE_ERROR_CODE_E200305)

import_processing()
import processing


class TesQualityValidations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import_qgis_model_baker()
        cls.app = AppInterface()
        cls.quality_rules = QualityRules()
        cls.geometry = GeometryUtils()
        cls.quality_rules_manager = QualityRuleManager()

        print("INFO: Restoring databases to be used")
        restore_schema('test_ladm_validations_topology_tables')

    def test_split_by_selected_boundary(self):
        print('\nINFO: Validation of the definition of selected boundary ...')

        gpkg_path = get_test_copy_path('geopackage/adjust_boundaries_cases.gpkg')
        self.db_gpkg = get_gpkg_conn('adjust_boundaries_cases_gpkg')
        names = self.db_gpkg.names
        names.T_ID_F = 't_id' # Static label is set because the database does not have the ladm structure

        test_result = [{'selected_ids': [1], 'boundaries_to_del': [1, 2, 3, 4], 'geoms': ['LineString (882256.9922020563390106 1545352.94816972548142076, 883830.40917081397492439 1545368.68233941309154034, 885435.29447894683107734 1545352.94816972548142076, 887291.92650208086706698 1545337.21400003810413182, 888881.07764052611310035 1545463.08735753851942718)']},
                       {'selected_ids': [1], 'boundaries_to_del': [1, 2], 'geoms': ['LineString (882325.469107756158337 1544955.88267589989118278, 883209.64509183121845126 1544960.13352197711355984, 884510.40399148012511432 1544985.6385984409134835, 885547.61043433740269393 1544964.3843680543359369, 886822.86425752262584865 1544977.13690628623589873, 887889.82662292092572898 1544989.88944451813586056, 888612.47045605920720845 1545002.64198275003582239)']},
                       {'selected_ids': [1], 'boundaries_to_del': [1, 2, 3], 'geoms': ['LineString (886476.29300758719909936 1544161.06105313077569008, 882415.14798706094734371 1544041.61561135039664805, 882407.18495760892983526 1541724.37404081481508911, 887200.92868772032670677 1541764.18918807501904666)', 'LineString (886476.29300758719909936 1544161.06105313077569008, 889390.76178702362813056 1543165.68237162916921079, 887200.92868772032670677 1541764.18918807501904666)', 'LineString (887200.92868772032670677 1541764.18918807501904666, 886476.29300758719909936 1544161.06105313077569008)']},
                       {'selected_ids': [3], 'boundaries_to_del': [1, 2, 3], 'geoms': ['LineString (886476.29300758719909936 1544161.06105313077569008, 882415.14798706094734371 1544041.61561135039664805, 882407.18495760892983526 1541724.37404081481508911, 887200.92868772032670677 1541764.18918807501904666)', 'LineString (886476.29300758719909936 1544161.06105313077569008, 889390.76178702362813056 1543165.68237162916921079, 887894.38694565510377288 1542208.00247315340675414, 887200.92868772032670677 1541764.18918807501904666)']},
                       {'selected_ids': [1], 'boundaries_to_del': [1, 2, 3], 'geoms': ['LineString (882709.45987063564825803 1543510.21952517866156995, 882696.0032627055188641 1542761.13501706859096885, 883485.45759460597764701 1543057.18039153120480478, 882709.45987063564825803 1543510.21952517866156995)', 'LineString (883485.45759460597764701 1543057.18039153120480478, 884898.40142726874910295 1543084.09360739146359265)', 'LineString (884898.40142726874910295 1543084.09360739146359265, 885629.54379147209692746 1543640.30006850324571133, 885719.25451100617647171 1542711.79412132478319108, 884898.40142726874910295 1543084.09360739146359265)']},
                       {'selected_ids': [2], 'boundaries_to_del': [1, 2], 'geoms': ['LineString (882696.91113005892839283 1543128.55981796747073531, 883485.45759460597764701 1543057.18039153120480478, 884898.40142726874910295 1543084.09360739146359265)']},
                       {'selected_ids': [1], 'boundaries_to_del': [1, 2], 'geoms': ['LineString (882376.98617732501588762 1543885.65919923176988959, 881339.55751997174229473 1543276.52677656547166407, 882234.22076576261315495 1542448.48738950374536216)']},
                       {'selected_ids': [1], 'boundaries_to_del': [1, 2, 3, 4], 'geoms': ['LineString (895937.47771990788169205 1543691.07968750013969839, 895937.47771990788169205 1543987.82934027793817222, 896479.9233217597939074 1543987.82934027793817222, 896479.9233217597939074 1543691.07968750013969839, 895937.47771990788169205 1543691.07968750013969839)']},
                       {'selected_ids': [8], 'boundaries_to_del': [1, 2, 3, 4, 5, 6, 7, 8], 'geoms': ['LineString (895922.15344387735240161 1545423.63106414745561779, 895823.74850363796576858 1545312.72245558886788785, 895753.01430986321065575 1545231.0768567833583802, 895752.70520490442868322 1545118.35534420749172568, 895755.45756576466374099 1545004.08130264561623335, 895750.58388843457214534 1544903.72545119561254978, 895751.76962125208228827 1544777.10258481604978442, 895944.93307849601842463 1544785.83842549938708544)','LineString (895922.15344387735240161 1545423.63106414745561779, 896065.97630945523269475 1545327.50076097156852484, 896159.22516733291558921 1545234.59747773432172835, 896159.51394954684656113 1544779.07535220449790359, 895944.93307849601842463 1544785.83842549938708544)']}]

        for i in range(len(test_result)):
            uri = gpkg_path + '|layername=boundary_case_{case}'.format(case=i+1)
            boundary_layer = QgsVectorLayer(uri, 'boundary_layer_{case}'.format(case=i+1), 'ogr')
            test_selected_ids = test_result[i]['selected_ids']
            #boundary_layer.selectByIds(selected_ids)
            new_geometries, boundaries_to_del_unique_ids = self.geometry.fix_selected_boundaries(names, boundary_layer, names.T_ID_F, selected_ids=test_selected_ids)
            self.assertEqual(boundaries_to_del_unique_ids, test_result[i]['boundaries_to_del'], 'Boundaries to be deleted are not valid: case {case}'.format(case=i + 1))

            for new_geom in new_geometries:
                found = False
                for geom in test_result[i]['geoms']:
                    if new_geom.isGeosEqual(QgsGeometry.fromWkt(geom)):
                        found = True
                        break
                self.assertTrue(found, 'The geometries are invalid: case {case}. Geometry in WKT: {geometry}'.format(
                    case=i + 1, geometry=new_geom.asWkt()))

    def _test_split_by_boundary(self):
        print('\nINFO: Validation of the definition of boundaries...')

        gpkg_path = get_test_copy_path('geopackage/adjust_boundaries_cases.gpkg')
        self.db_gpkg = get_gpkg_conn('adjust_boundaries_cases_gpkg')
        names = self.db_gpkg.names
        names.T_ID_F = 't_id'  # Static label is set because the database does not have the ladm structure

        test_result = [{'boundaries_to_del': [1, 2, 3, 4], 'geoms': ['LineString (882256.9922020563390106 1545352.94816972548142076, 883830.40917081397492439 1545368.68233941309154034, 885435.29447894683107734 1545352.94816972548142076, 887291.92650208086706698 1545337.21400003810413182, 888881.07764052611310035 1545463.08735753851942718)']},
                       {'boundaries_to_del': [1, 2], 'geoms': ['LineString (882325.469107756158337 1544955.88267589989118278, 883209.64509183121845126 1544960.13352197711355984, 884510.40399148012511432 1544985.6385984409134835, 885547.61043433740269393 1544964.3843680543359369, 886822.86425752262584865 1544977.13690628623589873, 887889.82662292092572898 1544989.88944451813586056, 888612.47045605920720845 1545002.64198275003582239)']},
                       {'boundaries_to_del': [1, 2, 3],'geoms': ['LineString (886476.29300758719909936 1544161.06105313077569008, 882415.14798706094734371 1544041.61561135039664805, 882407.18495760892983526 1541724.37404081481508911, 887200.92868772032670677 1541764.18918807501904666)', 'LineString (886476.29300758719909936 1544161.06105313077569008, 889390.76178702362813056 1543165.68237162916921079, 887200.92868772032670677 1541764.18918807501904666)', 'LineString (887200.92868772032670677 1541764.18918807501904666, 886476.29300758719909936 1544161.06105313077569008)']},
                       {'boundaries_to_del': [1, 2, 3, 4],'geoms': ['LineString (886476.29300758719909936 1544161.06105313077569008, 882415.14798706094734371 1544041.61561135039664805, 882407.18495760892983526 1541724.37404081481508911, 887200.92868772032670677 1541764.18918807501904666)', 'LineString (886476.29300758719909936 1544161.06105313077569008, 889390.76178702362813056 1543165.68237162916921079, 887894.38694565510377288 1542208.00247315340675414, 887200.92868772032670677 1541764.18918807501904666)', 'LineString (886476.29300758719909936 1544161.06105313077569008, 887200.92868772032670677 1541764.18918807501904666)']},
                       {'boundaries_to_del': [1, 2, 3],'geoms': ['LineString (882709.45987063564825803 1543510.21952517866156995, 882696.0032627055188641 1542761.13501706859096885, 883485.45759460597764701 1543057.18039153120480478, 882709.45987063564825803 1543510.21952517866156995)', 'LineString (883485.45759460597764701 1543057.18039153120480478, 884898.40142726874910295 1543084.09360739146359265)', 'LineString (884898.40142726874910295 1543084.09360739146359265, 885629.54379147209692746 1543640.30006850324571133, 885719.25451100617647171 1542711.79412132478319108, 884898.40142726874910295 1543084.09360739146359265)']},
                       {'boundaries_to_del': [1, 2, 3, 4],'geoms': ['LineString (882696.91113005892839283 1543128.55981796747073531, 883485.45759460597764701 1543057.18039153120480478, 884898.40142726874910295 1543084.09360739146359265)', 'LineString (884898.40142726874910295 1543084.09360739146359265, 885629.54379147209692746 1543640.30006850324571133)','LineString (884898.40142726874910295 1543084.09360739146359265, 885719.25451100617647171 1542711.79412132478319108)']},
                       {'boundaries_to_del': [1, 2, 3],'geoms': ['LineString (882376.98617732501588762 1543885.65919923176988959, 881339.55751997174229473 1543276.52677656547166407, 882234.22076576261315495 1542448.48738950374536216)', 'LineString (883128.88401155360043049 1543847.58842281508259475, 883994.99417503213044256 1543247.9736942530144006, 883043.22476461622864008 1542438.96969539951533079)']},
                       {'boundaries_to_del': [1, 2, 3, 4], 'geoms': ['LineString (895937.47771990788169205 1543691.07968750013969839, 895937.47771990788169205 1543987.82934027793817222, 896479.9233217597939074 1543987.82934027793817222, 896479.9233217597939074 1543691.07968750013969839, 895937.47771990788169205 1543691.07968750013969839)']},
                       {'boundaries_to_del': [1, 2, 3, 4, 5, 6, 7, 8, 9], 'geoms': ['LineString (895922.15344387735240161 1545423.63106414745561779, 895823.74850363796576858 1545312.72245558886788785, 895753.01430986321065575 1545231.0768567833583802, 895752.70520490442868322 1545118.35534420749172568, 895755.45756576466374099 1545004.08130264561623335, 895750.58388843457214534 1544903.72545119561254978, 895751.76962125208228827 1544777.10258481604978442, 895944.93307849601842463 1544785.83842549938708544)', 'LineString (895944.93307849601842463 1544785.83842549938708544, 896159.51394954684656113 1544779.07535220449790359, 896159.22516733291558921 1545234.59747773432172835, 896065.97630945523269475 1545327.50076097156852484, 895922.15344387735240161 1545423.63106414745561779)', 'LineString (895922.15344387735240161 1545423.63106414745561779, 895944.93307849601842463 1544785.83842549938708544)']}]

        for i in range(len(test_result)):
            uri = gpkg_path + '|layername=boundary_case_{case}'.format(case=i+1)
            boundary_layer = QgsVectorLayer(uri, 'boundary_layer_{case}'.format(case=i+1), 'ogr')
            self.assertEqual(boundary_layer.featureCount(), len(test_result[i]['boundaries_to_del']), 'Invalid number of features: case {case}'.format(case=i+1))
            merge_geoms, boundaries_to_del = self.geometry.fix_boundaries(boundary_layer, names.T_ID_F)
            self.assertEqual(boundaries_to_del, test_result[i]['boundaries_to_del'], 'The boundaries to delete are invalid: case {case}'.format(case=i + 1))

            for merge_geom in merge_geoms:
                found = False
                for geom in test_result[i]['geoms']:
                    if merge_geom.isGeosEqual(QgsGeometry.fromWkt(geom)):
                        found = True
                        break
                self.assertTrue(found,'The geometries are invalid: case {case}. Geometry in WKT: {geometry}'.format(case=i + 1, geometry=merge_geom.asWkt()))

        # TODO: Check what is happening with this test...

    def test_check_boundary_points_covered_by_plot_nodes(self):
        print('\nINFO: Validating boundary points are covered by plot nodes...')

        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        self.db_gpkg = get_gpkg_conn('tests_data_gpkg')
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

    def test_check_plot_nodes_covered_by_boundary_points(self):
        print('\nINFO: Validating plot nodes are covered by boundary points...')

        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        self.db_gpkg = get_gpkg_conn('tests_data_gpkg')
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

    def test_topology_boundary_nodes_must_be_covered_by_boundary_points(self):
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS)
        schema_name = 'test_ladm_validations_topology_tables'
        self.db_pg = get_pg_conn(schema_name)
        self.names = self.db_pg.names

        res, code, msg = self.db_pg.test_connection()
        self.assertTrue(res, msg)
        self.assertIsNotNone(self.names.LC_BOUNDARY_POINT_T, 'Names is None')

        boundary_point_layer = self.app.core.get_layer(self.db_pg, self.names.LC_BOUNDARY_POINT_T, load=True)
        self.assertEqual(boundary_point_layer.featureCount(), 109)

        boundary_layer = self.app.core.get_layer(self.db_pg, self.names.LC_BOUNDARY_T, load=True)
        self.assertEqual(boundary_layer.featureCount(), 22)

        plot_layer = self.app.core.get_layer(self.db_pg, self.names.LC_PLOT_T, load=True)
        self.assertEqual(plot_layer.featureCount(), 17)

        point_bfs_layer = self.app.core.get_layer(self.db_pg, self.names.POINT_BFS_T, load=True)
        self.assertEqual(point_bfs_layer.featureCount(), 81)

        error_layer = QgsVectorLayer("Point?crs={}".format(get_crs_authid(boundary_layer.sourceCrs())), rule.error_table_name, "memory")
        data_provider = error_layer.dataProvider()
        data_provider.addAttributes(rule.error_table_fields)
        error_layer.updateFields()

        features = self.quality_rules.line_quality_rules.get_boundary_nodes_features_not_covered_by_boundary_points(self.db_pg, boundary_point_layer, boundary_layer, point_bfs_layer, error_layer, self.names.T_ID_F)

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
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES)
        schema_name = 'test_ladm_validations_topology_tables'
        self.db_pg = get_pg_conn(schema_name)
        names = self.db_pg.names

        res, code, msg = self.db_pg.test_connection()
        self.assertTrue(res, msg)
        self.assertIsNotNone(names.LC_BOUNDARY_POINT_T, 'Names is None')

        boundary_point_layer = self.app.core.get_layer(self.db_pg, names.LC_BOUNDARY_POINT_T, load=True)
        self.assertEqual(boundary_point_layer.featureCount(), 109)

        boundary_layer = self.app.core.get_layer(self.db_pg, names.LC_BOUNDARY_T, load=True)
        self.assertEqual(boundary_layer.featureCount(), 22)

        plot_layer = self.app.core.get_layer(self.db_pg, names.LC_PLOT_T, load=True)
        self.assertEqual(plot_layer.featureCount(), 17)

        point_bfs_layer = self.app.core.get_layer(self.db_pg, names.POINT_BFS_T, load=True)
        self.assertEqual(point_bfs_layer.featureCount(), 81)

        more_bfs_layer = self.app.core.get_layer(self.db_pg, names.MORE_BFS_T, load=True)
        self.assertEqual(more_bfs_layer.featureCount(), 18)

        less_layer = self.app.core.get_layer(self.db_pg, names.LESS_BFS_T, load=True)
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
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Polygon.PLOTS_COVERED_BY_BOUNDARIES)
        schema_name = 'test_ladm_validations_topology_tables'
        self.db_pg = get_pg_conn(schema_name)
        names = self.db_pg.names

        res, code, msg = self.db_pg.test_connection()
        self.assertTrue(res, msg)
        self.assertIsNotNone(names.LC_BOUNDARY_POINT_T, 'Names is None')

        boundary_point_layer = self.app.core.get_layer(self.db_pg, names.LC_BOUNDARY_POINT_T, load=True)
        self.assertEqual(boundary_point_layer.featureCount(), 109)

        boundary_layer = self.app.core.get_layer(self.db_pg, names.LC_BOUNDARY_T, load=True)
        self.assertEqual(boundary_layer.featureCount(), 22)

        plot_layer = self.app.core.get_layer(self.db_pg, names.LC_PLOT_T, load=True)
        self.assertEqual(plot_layer.featureCount(), 17)

        point_bfs_layer = self.app.core.get_layer(self.db_pg, names.POINT_BFS_T, load=True)
        self.assertEqual(point_bfs_layer.featureCount(), 81)

        more_bfs_layer = self.app.core.get_layer(self.db_pg, names.MORE_BFS_T, load=True)
        self.assertEqual(more_bfs_layer.featureCount(), 18)

        less_layer = self.app.core.get_layer(self.db_pg, names.LESS_BFS_T, load=True)
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

        # test_result = [{'id': '1a972c2b-c4b1-4e7d-8b4a-5d88398e774a', 'geom': 'MultiLineStringZ ((894639.00399999995715916 1544574.38599999994039536 0, 894648.56400000001303852 1544485.16100000008009374 0, 894723.67700000002514571 1544488.34799999999813735 0, 894715.02700000000186265 1544590.31899999990127981 0, 894639.00399999995715916 1544574.38599999994039536 0))'},
        #                {'id': '4fbe53ea-4ca6-46ff-ba7e-feba78bef27b', 'geom': 'MultiLineStringZ ((894715.02700000000186265 1544590.31899999990127981 0, 894732.84299999999348074 1544594.1229999999050051 0),(894770.40800000005401671 1544602.14299999992363155 0, 894779.66099999996367842 1544604.11800000001676381 0),(894788.15800000005401671 1544496.48799999989569187 0, 894723.67700000002514571 1544488.34799999999813735 0, 894715.02700000000186265 1544590.31899999990127981 0))'},
        #                {'id': 'd1181ee8-a259-4d9f-87f6-d1f9912cc581', 'geom': 'MultiLineStringZ ((894856.60699999995995313 1544597.51000000000931323 0, 894860.856000000028871 1544572.962000000057742 0, 894879.26599999994505197 1544575.79499999992549419 0, 894882.57099999999627471 1544602.70200000004842877 0, 894856.60699999995995313 1544597.51000000000931323 0),(894810.34499999997206032 1544519.14700000011362135 0, 894837.25300000002607703 1544520.56300000008195639 0, 894833.94799999997485429 1544542.75 0, 894822.14000000001396984 1544541.38800000003539026 0))'},
        #                {'id': '5445a5f0-f453-4516-98de-7831fcef5718', 'geom': 'MultiLineStringZ ((894634.73699999996460974 1544430.39899999997578561 0, 894638.04099999996833503 1544358.17299999995157123 0, 894773.52399999997578561 1544367.14199999999254942 0, 894768.33100000000558794 1544443.6159999999217689 0, 894634.73699999996460974 1544430.39899999997578561 0))'},
        #                {'id': '3879a544-66b3-4284-8132-d88ce6b11fc3', 'geom': 'MultiLineStringZ ((894768.33100000000558794 1544443.6159999999217689 0, 894696.625 1544436.52200000011362135 0, 894702.99199999996926636 1544362.47299999999813735 0, 894773.52399999997578561 1544367.14199999999254942 0, 894768.33100000000558794 1544443.6159999999217689 0))'},
        #                {'id': 'a83e2386-2ab3-4540-ae1f-79df1a393267', 'geom': 'MultiLineStringZ ((894702.99199999996926636 1544362.47299999999813735 0, 894696.625 1544436.52200000011362135 0, 894634.73699999996460974 1544430.39899999997578561 0, 894638.04099999996833503 1544358.17299999995157123 0, 894702.99199999996926636 1544362.47299999999813735 0))'},
        #                {'id': '0a34acb7-c9d2-4439-a79e-ee4131eb6e67', 'geom': 'MultiLineStringZ ((894847.40200000000186265 1544448.57300000009126961 0, 894852.59499999997206032 1544369.26600000006146729 0),(894986.66099999996367842 1544377.29099999996833503 0, 894972.97100000001955777 1544459.43100000009872019 0, 894904.21900145395193249 1544453.48598809260874987 0),(894904.21900145395193249 1544453.48598809260874987 0, 894847.40200000000186265 1544448.57300000009126961 0))'},
        #                {'id': '303bffab-c8b6-4859-ab75-2179ec29a9e1', 'geom': 'MultiLineStringZ ((894847.40200000000186265 1544448.57300000009126961 0, 894852.59499999997206032 1544369.26600000006146729 0),(894852.59499999997206032 1544369.26600000006146729 0, 894914.05400000000372529 1544372.94500000006519258 0, 894911.74499999999534339 1544391.85100000002421439 0),(894904.21900000004097819 1544453.48600000003352761 0, 894847.40200000000186265 1544448.57300000009126961 0))'},
        #                {'id': '65a3e94f-8ae6-4aa1-b4b4-25bb45596056', 'geom': 'MultiLineStringZ ((894904.21900000004097819 1544453.48600000003352761 0, 894972.97100000001955777 1544459.43100000009872019 0, 894986.66099999996367842 1544377.29099999996833503 0),(894986.66099999996367842 1544377.29099999996833503 0, 894914.05400000000372529 1544372.94500000006519258 0, 894911.74499999999534339 1544391.85100000002421439 0))'},
        #                {'id': '76cc3820-e993-4c05-8ef9-c680dcb826dd', 'geom': 'MultiLineStringZ ((894863.92399999999906868 1544306.01000000000931323 0, 894862.50800000003073364 1544287.59899999992921948 0, 894910.65899999998509884 1544288.07099999999627471 0, 894905.93799999996554106 1544314.50699999998323619 0, 894863.92399999999906868 1544306.01000000000931323 0))'},
        #                {'id': 'dc922aaf-bbd1-425d-9527-1026ac380a4d', 'geom': 'MultiLineStringZ ((895053.2219999999506399 1544435.35499999998137355 0, 895076.28099999995902181 1544438.87899999995715916 0),(895076.28099999995902181 1544438.87899999995715916 0, 895119.085573127027601 1544445.42050326871685684 0),(895119.085573127027601 1544445.42050326871685684 0, 895126.55500278458930552 1544446.56200782209634781 0),(895126.55500278458930552 1544446.56200782209634781 0, 895126.55500278470572084 1544446.56200782209634781 0),(895126.55500278470572084 1544446.56200782209634781 0, 895150.11300000001210719 1544450.162999999942258 0))'},
        #                {'id': '7b13e43d-598c-4aae-a529-1aa2c51aafa9', 'geom': 'MultiLineStringZ ((871581.97699999995529652 1554559.162999999942258 0, 871583.06900000001769513 1554559.11199999996460974 0, 871586.15099999995436519 1554558.96699999994598329 0))'}]
        #
        # for item in test_result:
        #     self.assertIn(item, result, 'geometrical error in the polygon with id {}'.format(item['id']))

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

    def __test_topology_boundary_must_be_covered_by_plot(self):
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Line.BOUNDARIES_COVERED_BY_PLOTS)
        schema_name = 'test_ladm_validations_topology_tables'
        self.db_pg = get_pg_conn(schema_name)
        names = self.db_pg.names

        res, code, msg = self.db_pg.test_connection()
        self.assertTrue(res, msg)
        self.assertIsNotNone(names.LC_BOUNDARY_POINT_T, 'Names is None')

        boundary_point_layer = self.app.core.get_layer(self.db_pg, names.LC_BOUNDARY_POINT_T, load=True)
        self.assertEqual(boundary_point_layer.featureCount(), 109)

        boundary_layer = self.app.core.get_layer(self.db_pg, names.LC_BOUNDARY_T, load=True)
        self.assertEqual(boundary_layer.featureCount(), 22)

        plot_layer = self.app.core.get_layer(self.db_pg, names.LC_PLOT_T, load=True)
        self.assertEqual(plot_layer.featureCount(), 17)

        point_bfs_layer = self.app.core.get_layer(self.db_pg, names.POINT_BFS_T, load=True)
        self.assertEqual(point_bfs_layer.featureCount(), 81)

        more_bfs_layer = self.app.core.get_layer(self.db_pg, names.MORE_BFS_T, load=True)
        self.assertEqual(more_bfs_layer.featureCount(), 18)

        less_layer = self.app.core.get_layer(self.db_pg, names.LESS_BFS_T, load=True)
        self.assertEqual(less_layer.featureCount(), 6)

        error_layer = QgsVectorLayer("MultiLineString?crs={}".format(get_crs_authid(plot_layer.sourceCrs())), rule.error_table_name, "memory")
        data_provider = error_layer.dataProvider()
        data_provider.addAttributes(rule.error_table_fields)
        error_layer.updateFields()

        features = self.quality_rules.line_quality_rules.get_boundary_features_not_covered_by_plots(self.db_pg, plot_layer, boundary_layer, more_bfs_layer, less_layer, error_layer, names.T_ID_F)

        # the algorithm was successfully executed
        self.assertEqual(len(features), 11)

        error_layer.dataProvider().addFeatures(features)
        exp = "\"codigo_error\" = '{}'".format(QUALITY_RULE_ERROR_CODE_E200301)
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 3)

        result = [{'id': f['id_lindero'], 'id_plot': f['id_terreno'], 'geom': f.geometry().asWkt()} for f in error_layer.selectedFeatures()]

        test_result = [
            {'id': '67d2a8da-5f83-470b-b09c-97e97cff8ab0', 'id_plot': '7b13e43d-598c-4aae-a529-1aa2c51aafa9', 'geom': 'LineStringZ (871560.6650000000372529 1554564.43599999998696148 0, 871564.08799999998882413 1554562.86700000008568168 0, 871564.11399999994318932 1554562.17299999995157123 0, 871581.97699999995529652 1554559.162999999942258 0, 871586.15099999995436519 1554558.96699999994598329 0)'},
            {'id': '9d439543-9d1b-4df2-af32-82e11eccc15a', 'id_plot': None, 'geom': 'MultiLineStringZ ((895120.1720000000204891 1544364.95600000000558794 0, 895070.0779999999795109 1544331.15500000002793968 0, 895121.96699999994598329 1544243.82499999995343387 0, 895178.80000000004656613 1544283.712000000057742 0, 895120.1720000000204891 1544364.95600000000558794 0))'},
            {'id': 'edd15986-68f1-4cab-a6be-5455d6d1ee76', 'id_plot': None, 'geom': 'MultiLineStringZ ((895053.2219999999506399 1544435.35499999998137355 0, 895065.96799999999348074 1544460.84700000006705523 0, 895076.28099999995902181 1544438.87899999995715916 0),(895126.55500000005122274 1544446.56199999991804361 0, 895126.55500278470572084 1544446.56200782209634781 0),(895126.55500278470572084 1544446.56200782209634781 0, 895138.19400000001769513 1544479.25699999998323619 0, 895150.11300000001210719 1544450.162999999942258 0))'}
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

    def test_overlapping_points(self):
        print('\nINFO: Validating overlaps in points...')
        test_layer = 'tests_puntolindero'
        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        uri = gpkg_path + '|layername={}'.format(test_layer)
        overlapping_points_layer = QgsVectorLayer(uri, 'overlapping_points', 'ogr')

        features = [feature for feature in overlapping_points_layer.getFeatures()]
        self.assertEqual(len(features), 286, 'The number of features differs')

        expected_overlaps = {
            '286, 285': 'Point (963166.65579999983310699 1077249.80199999921023846)'
        }

        overlapping = self.geometry.get_overlapping_points(overlapping_points_layer)
        self.assertTrue(len(overlapping), 1) # One list of overlapping ids

        for overlapping_ids in overlapping:
            self.assertTrue(len(overlapping_ids), 2) # Two points overlap
            points = []

            for feature in overlapping_points_layer.getFeatures(overlapping_ids):
                points.append(feature.geometry().asWkt())

            unique_points = set(points) # get unique values
            self.assertEqual(len(unique_points), 1, 'The intersection failed, points are not equal')
            self.assertEqual(list(unique_points)[0], list(expected_overlaps.values())[0])

    def _test_get_overlapping_lines(self):
        print('\nINFO: Validating overlaps in boundaries...')
        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        self.db_gpkg = get_gpkg_conn('tests_data_gpkg')
        names = self.db_gpkg.names
        names.T_ID_F = 't_id'  # Static label is set because the database does not have the ladm structure

        uri = gpkg_path + '|layername={layername}'.format(layername='test_boundaries_overlap')
        boundary_overlap_layer = QgsVectorLayer(uri, 'test_boundaries_overlap', 'ogr')

        features = [feature for feature in boundary_overlap_layer.getFeatures()]
        self.assertEqual(len(features), 15)

        overlapping = self.geometry.get_overlapping_lines(boundary_overlap_layer)

        error_line_layer = overlapping['native:saveselectedfeatures_2:Intersected_Lines']
        error_point_layer = overlapping['native:saveselectedfeatures_3:Intersected_Points']

        self.assertEqual(error_point_layer.featureCount(), 13)
        self.assertEqual(error_line_layer.featureCount(), 5)

        point_features = error_point_layer.getFeatures()
        line_features = error_line_layer.getFeatures()
        overlapping = dict()

        def insert_into_res(ids, geometry):
            """
            Local function to append a geometry into a list for each pair of ids
            """
            pair = "{}-{}".format(min(ids), max(ids))
            if pair not in overlapping:
                overlapping[pair] = [geometry]
            else: # Pair is in dict already
                overlapping[pair].append(geometry)

        for point in point_features:
            insert_into_res([point[names.T_ID_F], point[names.T_ID_F+'_2']], point.geometry().asWkt())

        for line in line_features:
            insert_into_res([line[names.T_ID_F], line[names.T_ID_F+'_2']], line.geometry().asWkt())

        expected_overlaps = {
            '7-15': [
                     'MultiPoint ((963651.61653553508222103 1077966.0537187303416431))',
                     'MultiLineString ((964213.72614089539274573 1077962.10928706941194832, 963759.37523004529066384 1078021.79097451153211296))'
                    ],
            '7-10': ['MultiPoint ((963750.28136727144010365 1077824.19025488453917205))'],
            '9-335': ['MultiPoint ((963643.395574557245709 1077747.43814651435241103))'],
            '9-337': ['MultiPoint ((963643.395574557245709 1077747.43814651435241103))'],
            '9-334': ['MultiPoint ((963662.21440408274065703 1077708.90435272408649325))'],
            '6-325': ['MultiPoint ((963849.37875852338038385 1077949.20776149653829634))'],
            '4-7': ['MultiPoint ((963801.72997597197536379 1077798.46595053421333432))'],
            '4-5': [
                    'MultiPoint ((963850.90352329798042774 1077652.23999353917315602))',
                    'MultiPoint ((963880.39959512907080352 1077685.35838998109102249))'
                   ],
            '5-336': ['MultiPoint ((964079.46952913235872984 1077829.37777462997473776))'],
            '5-6': [
                    'MultiPoint ((964081.01700186752714217 1077722.2743631626944989))',
                    'MultiPoint ((964211.2347710223402828 1077618.29701916221529245))',
                    'MultiLineString ((963926.86899802810512483 1077925.5301883143838495, 963980.77503829856868833 1077802.31638198206201196))'
                   ],
            '13-14': [
                      'MultiPoint ((963384.55712854664307088 1077823.99900980317033827))',
                      'MultiLineString ((963210.47528458514716476 1077644.75307651958428323, 963255.32157539459876716 1077724.74916282831691206))'
                     ],
            '5-7': ['MultiLineString ((964309.98692709254100919 1077617.49567248369567096, 964144.41837483353447169 1077577.06614228105172515),(964144.41837483353447169 1077577.06614228105172515, 963905.69162506482098252 1077713.75645868084393442))'],
            '335-337': ['MultiLineString ((963643.395574557245709 1077747.43814651435241103, 963543.5341855603037402 1077760.18016819190233946))']
        }

        for pair, overlaps in overlapping.items():
            print("Testing pair {}...".format(pair))
            self.assertEqual(len(overlaps), len(expected_overlaps[pair]))
            for overlap in overlaps:
                self.assertIn(overlap, expected_overlaps[pair])

    def test_overlapping_polygons(self):
        print('\nINFO: Validating overlaps in polygons (plots)...')

        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        uri = gpkg_path + '|layername={layername}'.format(layername='topology_polygons_overlap')
        polygons_overlap_layer = QgsVectorLayer(uri, 'test_polygons_overlap', 'ogr')

        if QgsWkbTypes.isMultiType(polygons_overlap_layer.wkbType()) and \
            polygons_overlap_layer.geometryType() == QgsWkbTypes.PolygonGeometry:
            polygons_overlap_layer = processing.run("native:multiparttosingleparts",
                                           {'INPUT': polygons_overlap_layer, 'OUTPUT': 'memory:'})['OUTPUT']

        expected_overlaps = [[11, 44], [11, 47], [12, 44], [12, 45], [12, 57], [48, 49], [53, 55], [61, 62], [63, 64], [63, 65], [64, 65], [66, 68], [67, 68]]
        flat_expected_overlaps = list(set([id for items in expected_overlaps for id in items]))  # Build a flat list of uniques ids

        overlapping = self.geometry.get_overlapping_polygons(polygons_overlap_layer)
        flat_overlapping = list(set([id for items in overlapping for id in items]))

        # checks
        self.assertEqual(len(flat_overlapping), 18)
        flat_expected_overlaps.sort()
        flat_overlapping.sort()
        self.assertEqual(flat_expected_overlaps, flat_overlapping)

    def test_find_vertices(self):
        print('\nINFO: Validating search for missing vertices...')

        gpkg_path = get_test_copy_path('geopackage/topology_cases.gpkg')
        self.db_gpkg = get_gpkg_conn('topology_cases_gpkg')
        names = self.db_gpkg.names
        names.T_ID_F = 't_id'  # Static label is set because the database does not have the ladm structure

        # Map between case number and number of vertices that should be added
        # For instance, the 4th case (reflected in the layer's name) should
        # have 6 vertices found
        vertices_test_values = [2,2,2,6,4,0]

        for i in range(len(vertices_test_values)):
            uri_polygon = gpkg_path + '|layername={layername}_case{case}'.format(
                layername='polygon',
                case=i+1)
            uri_lines = gpkg_path + '|layername={layername}_case{case}'.format(
                layername='lines',
                case=i+1)
            polygon_layer = QgsVectorLayer(uri_polygon, 'polygon_layer_{}'.format(i+1), 'ogr')
            lines_layer = QgsVectorLayer(uri_lines, 'lines_layer_{}'.format(i+1), 'ogr')

            # We don't want to overwrite the original layer
            clone_polygons = self.geometry.clone_layer(polygon_layer)

            geom_polygon = clone_polygons.getFeature(1).geometry()
            init_vertex_geom = [vertex for vertex in geom_polygon.vertices()]

            clone_polygons = self.geometry.add_topological_vertices(clone_polygons, lines_layer)

            geom_polygon = clone_polygons.getFeature(1).geometry()
            adjusted_vertex_geom = [vertex for vertex in geom_polygon.vertices()]

            num_vertices_added = len(adjusted_vertex_geom) - len(init_vertex_geom)
            self.assertEqual(num_vertices_added, vertices_test_values[i])

    def test_polygons_must_be_covered_by_lines(self):
        print('\nINFO: Validating polygons must be covered by lines...')

        gpkg_path = get_test_copy_path('geopackage/topology_cases.gpkg')
        self.db_gpkg = get_gpkg_conn('topology_cases_gpkg')
        names = self.db_gpkg.names
        names.T_ID_F = 't_id'  # Static label is set because the database does not have the ladm structure

        diff_geom = [['MultiLineString ((780300.30731518880929798 1225605.22174088703468442, 780297.95234157983213663 1225599.8581298291683197, 780292.44514157995581627 1225602.31722982972860336, 780294.34505024075042456 1225606.57437412883155048))'],
                     ['MultiLineString ((780300.30731518880929798 1225605.22174088703468442, 780297.95234157983213663 1225599.8581298291683197, 780292.44514157995581627 1225602.31722982972860336, 780294.34505024075042456 1225606.57437412883155048))'],
                     ['MultiLineString ((780309.73902403307147324 1225602.49830744392238557, 780308.30989155941642821 1225603.05408118362538517, 780307.64825615496374667 1225603.95390533376485109),(780310.01870060083456337 1225599.16431454825215042, 780310.03014361101668328 1225598.66082209814339876, 780311.16639214521273971 1225598.61655267467722297))'],
                     ['MultiLineString ((780307.7805832359008491 1225598.39616793626919389, 780307.60049424471799284 1225599.58559290133416653),(780308.69099051796365529 1225598.27522822353057563, 780307.7805832359008491 1225598.39616793626919389),(780315.57867445563897491 1225608.45340170268900692, 780315.45555392769165337 1225607.63259818265214562, 780314.78905752801802009 1225607.92419035756029189),(780317.62428020488005131 1225603.16991792898625135, 780318.36674970726016909 1225602.84235785435885191, 780318.29131162946578115 1225603.45340628433041275))'],
                     ['MultiLineString ((780306.77080396702513099 1225605.06540775927715003, 780306.64257034030742943 1225605.91234613093547523, 780307.906158416881226 1225605.63026071945205331),(780314.52926436136476696 1225599.74590416136197746, 780312.94133939070161432 1225600.03702373942360282, 780312.34155925654340535 1225600.40004855743609369),(780312.43979134678374976 1225599.65884278574958444, 780314.52926436136476696 1225599.74590416136197746),(780318.10209554550237954 1225604.98605656484141946, 780317.2287368115503341 1225605.14484906173311174, 780316.19658558059018105 1225606.12406946043483913))'],
                     '',
                     ['MultiLineString ((871560.66490000020712614 1554564.43640000000596046, 871561.29310000035911798 1554568.61969999969005585, 871565.18800000008195639 1554569.14470000006258488, 871582.36809999961405993 1554569.08310000039637089, 871586.65579999983310699 1554568.74300000071525574, 871586.17630000039935112 1554559.7443000003695488, 871586.15149999968707561 1554558.96719999983906746))',  'MultiLineString ((871581.97680000029504299 1554559.16310000047087669, 871583.06890000030398369 1554559.11189999990165234, 871586.15149999968707561 1554558.96719999983906746),(871586.15149999968707561 1554558.96719999983906746, 871585.68250000011175871 1554551.27449999935925007, 871585.4917000001296401 1554549.15570000000298023, 871584.2698999997228384 1554549.2476000003516674, 871576.33000000007450581 1554549.84439999982714653, 871561.16789999976754189 1554551.16310000047087669, 871545.42370000015944242 1554551.99960000067949295, 871546.30889999959617853 1554566.21570000052452087, 871560.66490000020712614 1554564.43640000000596046))']]

        for i in range(len(diff_geom)):
            uri_polygon = gpkg_path + '|layername={layername}_case{case}'.format(
                layername='polygon', case=i+1)
            uri_lines = gpkg_path + '|layername={layername}_case{case}'.format(
                layername='lines', case=i+1)
            polygon_layer = QgsVectorLayer(uri_polygon, 'polygon_layer_{}'.format(i+1), 'ogr')
            lines_layer = QgsVectorLayer(uri_lines, 'lines_layer_{}'.format(i+1), 'ogr')

            polygon_as_lines_layer = processing.run("ladm_col:polygonstolines", {'INPUT': polygon_layer, 'OUTPUT': 'memory:'})['OUTPUT']
            diff_plot_boundary = self.geometry.difference_plot_boundary(names, polygon_as_lines_layer, lines_layer, 'fid')

            if diff_plot_boundary is not None:
                if len(diff_plot_boundary) > 0:
                    for element in range(len(diff_plot_boundary)):
                        self.assertIn(diff_plot_boundary[element]['geometry'].asWkt(), diff_geom[i], 'case_{}, element_{}'.format(i + 1, element))
                else: # Case 6
                    self.assertEqual('', diff_geom[i], 'case_{}'.format(i + 1))

    def test_lines_must_be_covered_by_polygons(self):
        print('\nINFO: Validating lines must be covered by polygons...')

        gpkg_path = get_test_copy_path('geopackage/topology_cases.gpkg')
        self.db_gpkg = get_gpkg_conn('topology_cases_gpkg')
        names = self.db_gpkg.names
        names.T_ID_F = 't_id'  # Static label is set because the database does not have the ladm structure

        diff_geom = ['',
                     '',
                     'MultiLineString ((780309.73902403307147324 1225602.49830744392238557, 780307.83351406815927476 1225602.05170354596339166, 780307.64825615496374667 1225603.95390533376485109))',
                     '',
                     'MultiLineString ((780318.10209554550237954 1225604.98605656484141946, 780317.50662368256598711 1225605.92888701660558581, 780316.19658558059018105 1225606.12406946043483913))',
                     'MultiLineString ((780314.52926436136476696 1225599.74590416136197746, 780312.94133939070161432 1225600.03702373942360282, 780310.92996776115614921 1225601.25443288357928395, 780310.00367819482926279 1225599.82530040992423892, 780310.03014361101668328 1225598.66082209814339876, 780312.06798065674956888 1225598.5814258495811373, 780311.35341442003846169 1225599.61357708042487502, 780314.52926436136476696 1225599.74590416136197746))',
                     '']

        for i in range(len(diff_geom)):
            uri_polygon = gpkg_path + '|layername={layername}_case{case}'.format(layername='polygon', case=i+1)
            uri_lines = gpkg_path + '|layername={layername}_case{case}'.format(layername='lines', case=i+1)
            polygon_layer = QgsVectorLayer(uri_polygon, 'polygon_layer_{}'.format(i+1), 'ogr')
            lines_layer = QgsVectorLayer(uri_lines, 'lines_layer_{}'.format(i+1), 'ogr')

            polygon_as_lines_layer = processing.run("ladm_col:polygonstolines", {'INPUT': polygon_layer, 'OUTPUT': 'memory:'})['OUTPUT']
            diff_boundary_plot = self.geometry.difference_boundary_plot(names, lines_layer, polygon_as_lines_layer, 'fid')

            if diff_boundary_plot is not None:
                if len(diff_boundary_plot) > 0:
                    self.assertEqual(diff_boundary_plot[0]['geometry'].asWkt(), diff_geom[i], 'case_{}'.format(i + 1))
                else:
                    self.assertEqual('', diff_geom[i], 'case_{}'.format(i + 1))

    def test_intersection_polygons_tolerance(self):
        print('\nINFO: Validating intersection in polygons (plots)...')

        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        uri = gpkg_path + '|layername={layername}'.format(layername='topology_polygons_overlap')
        polygons_intersection_layer = QgsVectorLayer(uri, 'test_polygons_intersection_tolerance', 'ogr')

        polygon_id = 61
        overlapping_id = 62
        polygon_intersection = self.geometry.get_intersection_polygons(polygons_intersection_layer,
                                                                                  polygon_id,
                                                                                  overlapping_id)
        self.assertEqual(polygon_intersection, None)

    def test_get_missing_boundary_points_in_boundaries(self):
        print('\nINFO: Validating missing boundary points in boundaries...')

        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        self.db_gpkg = get_gpkg_conn('tests_data_gpkg')
        self.db_gpkg.names.T_ID_F = 't_id'  # Static label is set because the database does not have the ladm structure

        uri = gpkg_path + '|layername={layername}'.format(layername='boundary')
        boundary_layer = QgsVectorLayer(uri, 'boundary', 'ogr')
        uri = gpkg_path + '|layername={layername}'.format(layername='boundary_points_')
        point_layer = QgsVectorLayer(uri, 'boundary_points_', 'ogr')

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

        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        self.db_gpkg = get_gpkg_conn('tests_data_gpkg')
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

        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        self.db_gpkg = get_gpkg_conn('tests_data_gpkg')
        self.db_gpkg.names.T_ID_F = 't_id'  # Static label is set because the database does not have the ladm structure

        uri = gpkg_path + '|layername={layername}'.format(layername='construccion')
        building_layer = QgsVectorLayer(uri, 'construccion', 'ogr')
        uril = gpkg_path + '|layername={layername}'.format(layername='p_levantamiento')
        survey_layer = QgsVectorLayer(uril, 'p_levantamiento', 'ogr')

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

    def test_validate_topology_relation_between_point_boundary_boundary(self):
        print('\nINFO: Validating that the relation between point boundary and boundary is registered in the topology table ...')

        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        self.db_gpkg = get_gpkg_conn('tests_data_gpkg')
        names = self.db_gpkg.names
        names.T_ID_F = 't_id'  # Static label is set because the database does not have the ladm structure

        uri_boundary_points = gpkg_path + '|layername=good_boundary_points'
        uri_boundary = gpkg_path + '|layername=good_boundary'
        uri_points_ccl_table = gpkg_path + '|layername=pointsCcl'

        boundary_layer = QgsVectorLayer(uri_boundary, 'boundary_points', 'ogr')
        boundary_points_layer = QgsVectorLayer(uri_boundary_points, 'boundary', 'ogr')
        points_ccl_table = QgsVectorLayer(uri_points_ccl_table, 'pointsCcl', 'ogr')

        dic_points_ccl = dict()
        for feature_point_ccl in points_ccl_table.getFeatures():
            key = "{}-{}".format(feature_point_ccl['boundary_point_id'], feature_point_ccl['boundary_id'])
            if key in dic_points_ccl:
                dic_points_ccl[key] += 1
            else:
                dic_points_ccl.update({key:1})

        # verify that the relation between point boundary and boundary is registered in the topology table
        missing_topology = list()
        duplicates_topology = list()
        points_selected = self.geometry.join_boundary_points_with_boundary_discard_nonmatching(boundary_points_layer, boundary_layer, names.T_ID_F)

        for point_selected in points_selected:
            boundary_point_id = point_selected[names.T_ID_F]
            boundary_id = point_selected['{}_2'.format(names.T_ID_F)]
            key_query = "{}-{}".format(boundary_point_id, boundary_id)

            if key_query in dic_points_ccl:
                if dic_points_ccl[key_query] > 1:
                    duplicates_topology.append([boundary_point_id, boundary_id])
            else:
                missing_topology.append([boundary_point_id, boundary_id])

        self.assertEqual(len(missing_topology), 0)
        self.assertEqual(len(duplicates_topology), 0)

        uri_points_ccl_table = gpkg_path + '|layername=pointsCcl_bad'
        points_ccl_table = QgsVectorLayer(uri_points_ccl_table, 'pointsCcl_bad', 'ogr')

        dic_points_ccl = dict()
        for feature_point_ccl in points_ccl_table.getFeatures():
            key = "{}-{}".format(feature_point_ccl['boundary_point_id'], feature_point_ccl['boundary_id'])
            if key in dic_points_ccl:
                dic_points_ccl[key] += 1
            else:
                dic_points_ccl.update({key: 1})

        # verify that the relation between point boundary and boundary is registered in the topology table
        missing_topology = list()
        duplicates_topology = list()
        points_selected = self.geometry.join_boundary_points_with_boundary_discard_nonmatching(boundary_points_layer, boundary_layer, names.T_ID_F)

        for point_selected in points_selected:
            boundary_point_id = point_selected[names.T_ID_F]
            boundary_id = point_selected['{}_2'.format(names.T_ID_F)]
            key_query = "{}-{}".format(boundary_point_id, boundary_id)

            if key_query in dic_points_ccl:
                if dic_points_ccl[key_query] > 1: # register more that once
                    duplicates_topology.append([boundary_point_id, boundary_id])
            else: # no register
                missing_topology.append([boundary_point_id, boundary_id])

        self.assertEqual(missing_topology, [[1, 1]])
        self.assertEqual(duplicates_topology, [[20, 1]])

    def test_check_right_of_way_overlaps_buildings(self):
        print('\nINFO: Validating Right of Way-Building overlaps...')

        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        uri = gpkg_path + '|layername={layername}'.format(layername='construccion')
        building_layer = QgsVectorLayer(uri, 'construccion', 'ogr')
        uri = gpkg_path + '|layername={layername}'.format(layername='servidumbrepaso')
        right_of_way_layer = QgsVectorLayer(uri, 'servidumbrepaso', 'ogr')

        building_features = [feature for feature in building_layer.getFeatures()]
        self.assertEqual(len(building_features), 4)

        right_of_way_features = [feature for feature in right_of_way_layer.getFeatures()]
        self.assertEqual(len(right_of_way_features), 6)

        ids, over_pol = self.geometry.get_inner_intersections_between_polygons(right_of_way_layer, building_layer)

        geometries = [v.asWkt() for v in over_pol.asGeometryCollection()]

        self.assertEqual(len(geometries), 4)

        self.assertIn('Polygon ((1091354.41819027159363031 1121694.23184006474912167, 1091354.2822037145961076 1121696.81558464490808547, 1091355.59206581697799265 1121695.52748471638187766, 1091354.41819027159363031 1121694.23184006474912167))', geometries)
        self.assertIn('Polygon ((1091254.39762192475609481 1121590.49773243162781, 1091250.73030774760991335 1121597.99486360652372241, 1091259.24529790692031384 1121594.80259312898851931, 1091254.39762192475609481 1121590.49773243162781))', geometries)
        self.assertIn('Polygon ((1091236.35652560647577047 1121774.96929413848556578, 1091240.31053024088032544 1121761.7039380690548569, 1091224.81715030129998922 1121764.51856614812277257, 1091236.35652560647577047 1121774.96929413848556578))', geometries)
        self.assertIn('Polygon ((1091210.77726722555235028 1121751.80323319789022207, 1091216.81715549202635884 1121740.58629784546792507, 1091200.99485773546621203 1121742.94371541915461421, 1091210.77726722555235028 1121751.80323319789022207))', geometries)

    def test_boundary_dangles(self):
        print('\nINFO: Validating boundary_dangles...')
        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        self.db_gpkg = get_gpkg_conn('tests_data_gpkg')
        names = self.db_gpkg.names
        names.T_ID_F = 't_id'  # Static label is set because the database does not have the ladm structure

        uri = gpkg_path + '|layername={layername}'.format(layername='test_boundaries_overlap')
        boundary_layer = QgsVectorLayer(uri, 'dangles', 'ogr')

        features = [feature for feature in boundary_layer.getFeatures()]
        self.assertEqual(len(features), 15)

        end_points, dangle_ids = self.geometry.get_dangle_ids(boundary_layer)
        self.assertEqual(len(dangle_ids), 19)

        boundary_ids = [feature[names.T_ID_F] for feature in end_points.getFeatures(dangle_ids)]
        boundary_ids.sort()
        expected_boundary_ids = [4, 4, 5, 6, 6, 7, 8, 10, 10, 13, 14, 325, 325, 334, 334, 335, 336, 336, 337]

        self.assertEqual(boundary_ids, expected_boundary_ids)

    def test_boundary_dangles_no_dangles(self):
        print('\nINFO: Validating boundary_dangles with no dangles...')
        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        uri = gpkg_path + '|layername={layername}'.format(layername='boundary')
        boundary_layer = QgsVectorLayer(uri, 'dangles', 'ogr')

        features = [feature for feature in boundary_layer.getFeatures()]
        self.assertEqual(len(features), 8)

        end_points, dangle_ids = self.geometry.get_dangle_ids(boundary_layer)
        self.assertEqual(len(dangle_ids), 0)

    def test_boundaries_are_not_split(self):
        print('\nINFO: Validating boundaries are not split...')
        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        self.db_gpkg = get_gpkg_conn('tests_data_gpkg')
        names = self.db_gpkg.names
        names.T_ID_F = 't_id'  # Static label is set because the database does not have the ladm structure
        names.T_ILI_TID_F = 't_ili_tid'  # Static label is set because the database does not have the ladm structure

        uri_bad_boundary = gpkg_path + '|layername={layername}'.format(layername='bad_boundary')
        uri_bbox_boundary = gpkg_path + '|layername={layername}'.format(layername='bbox_intersect_boundary')
        uri_good_boundary = gpkg_path + '|layername={layername}'.format(layername='good_boundary')
        bad_boundary_layer = QgsVectorLayer(uri_bad_boundary, 'bad_boundary', 'ogr')
        bbox_boundary_layer = QgsVectorLayer(uri_bbox_boundary, 'bbox_intersect_boundary', 'ogr')
        good_boundary_layer = QgsVectorLayer(uri_good_boundary, 'good_boundary', 'ogr')

        bad_boundary_errors = self.geometry.get_boundaries_connected_to_single_boundary(names, bad_boundary_layer)
        bad_boundary_errors_list = [item for item in bad_boundary_errors]
        self.assertEqual(len(bad_boundary_errors_list), 4)
        self.assertEqual([2, 3, 6, 7], [f['t_id'] for f in bad_boundary_errors])

        bbox_boundary_errors = self.geometry.get_boundaries_connected_to_single_boundary(names, bbox_boundary_layer)
        bbox_boundary_errors_list = [item for item in bbox_boundary_errors]
        self.assertEqual(len(bbox_boundary_errors_list), 9)
        self.assertEqual([39185, 39193, 39207, 39209, 39210, 39231, 39232, 48767, 48768], [f['t_id'] for f in bbox_boundary_errors_list])

        good_boundary_errors = self.geometry.get_boundaries_connected_to_single_boundary(names, good_boundary_layer)
        good_boundary_errors_list = [item for item in good_boundary_errors]
        self.assertEqual(len(good_boundary_errors_list), 0)

    def validate_segments(self, segments_info, tolerance):
        for segment_info in segments_info:
            #print(segment_info[0].asWkt(), segment_info[1])
            self.assertEqual(segment_info[0].length(), segment_info[1])
            self.assertTrue(segment_info[1] >= tolerance)

    def test_check_gaps_in_plots(self):
        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        uri = gpkg_path + '|layername={layername}'.format(layername='check_gaps_in_plots')
        test_plots_layer = QgsVectorLayer(uri, 'check_gaps_in_plots', 'ogr')

        print('\nINFO: Validating Gaps in Plots using roads and multiple geometries...')
        gaps = self.geometry.get_gaps_in_polygon_layer(test_plots_layer, include_roads=True)
        geometries = [g.asWkt() for g in gaps]

        expected_list = [
            'Polygon ((1001839.42949045938439667 1013500.23419545334763825, 1001838.68766217899974436 1013479.83391774445772171, 1001839.42949045938439667 1013450.16078653128352016, 1001855.74971262644976377 1013449.78987239114940166, 1001858.3461116076214239 1013430.87325124291237444, 1001885.42284383939113468 1013430.87325124291237444, 1001901.72405463655013591 1013411.57209242216777056, 1001910.64500537037383765 1013418.26217047742102295, 1001917.32145989337004721 1013392.29818066605366766, 1001845.19794039404951036 1013415.08188382943626493, 1001851.47861975431442261 1013424.31817700632382184, 1001833.74493685469496995 1013433.92392191023100168, 1001829.49624199338722974 1013421.7320149167208001, 1001839.42949045938439667 1013500.23419545334763825))', 'Polygon ((1001935.86716690135654062 1013432.35690780356526375, 1001921.03060129494406283 1013446.08073098957538605, 1001920.28877301455941051 1013475.7538622027495876, 1001957.38018703076522797 1013429.01868054212536663, 1001935.86716690135654062 1013432.35690780356526375))',
            'Polygon ((1001935.86716690135654062 1013432.35690780356526375, 1001921.03060129494406283 1013446.08073098957538605, 1001920.28877301455941051 1013475.7538622027495876, 1001957.38018703076522797 1013429.01868054212536663, 1001935.86716690135654062 1013432.35690780356526375))',
            'Polygon ((1001920.28877301455941051 1013475.7538622027495876, 1001861.31342472892720252 1013477.9793470436707139, 1001862.05525300919543952 1013498.37962475256063044, 1001920.28877301455941051 1013475.7538622027495876))',
            'Polygon ((1001895.43752562382724136 1013467.22283697873353958, 1001907.30677810893394053 1013464.25552385742776096, 1001907.67769224906805903 1013454.2408420731080696, 1001895.43752562382724136 1013454.2408420731080696, 1001895.43752562382724136 1013467.22283697873353958))',
            'Polygon ((1001847.96051568305119872 1013470.1901501000393182, 1001867.98987925180699676 1013469.07740767952054739, 1001869.10262167232576758 1013455.72449863376095891, 1001847.58960154291708022 1013455.72449863376095891, 1001847.96051568305119872 1013470.1901501000393182))']

        for expected in expected_list:
            self.assertIn(expected, geometries)

        self.assertEqual(len(geometries), 5)

        print('\nINFO: Validating Gaps in Plots using roads for one geometry...')
        test_plots_layer.startEditing()
        test_plots_layer.deleteFeature(2)
        gaps = self.geometry.get_gaps_in_polygon_layer(test_plots_layer, include_roads=True)
        geometries = [g.asWkt() for g in gaps]
        self.assertIn(
            'Polygon ((1001895.43752562382724136 1013467.22283697873353958, 1001907.30677810893394053 1013464.25552385742776096, 1001907.67769224906805903 1013454.2408420731080696, 1001895.43752562382724136 1013454.2408420731080696, 1001895.43752562382724136 1013467.22283697873353958))',
            geometries)
        self.assertIn(
            'Polygon ((1001847.96051568305119872 1013470.1901501000393182, 1001867.98987925180699676 1013469.07740767952054739, 1001869.10262167232576758 1013455.72449863376095891, 1001847.58960154291708022 1013455.72449863376095891, 1001847.96051568305119872 1013470.1901501000393182))',
            geometries)
        self.assertEqual(len(geometries), 2)
        test_plots_layer.rollBack()

        print('\nINFO: Validating Gaps in Plots without using roads and multiple geometries...')
        gaps = self.geometry.get_gaps_in_polygon_layer(test_plots_layer, include_roads=False)
        geometries = [g.asWkt() for g in gaps]
        self.assertIn(
            'Polygon ((1001895.43752562382724136 1013467.22283697873353958, 1001907.30677810893394053 1013464.25552385742776096, 1001907.67769224906805903 1013454.2408420731080696, 1001895.43752562382724136 1013454.2408420731080696, 1001895.43752562382724136 1013467.22283697873353958))',
            geometries)
        self.assertIn(
            'Polygon ((1001847.96051568305119872 1013470.1901501000393182, 1001867.98987925180699676 1013469.07740767952054739, 1001869.10262167232576758 1013455.72449863376095891, 1001847.58960154291708022 1013455.72449863376095891, 1001847.96051568305119872 1013470.1901501000393182))',
            geometries)
        self.assertEqual(len(geometries), 2)

        print('\nINFO: Validating Gaps in Plots without using roads for one geometry...')
        test_plots_layer.startEditing()
        test_plots_layer.deleteFeature(2)
        gaps = self.geometry.get_gaps_in_polygon_layer(test_plots_layer, include_roads=False)
        geometries = [g.asWkt() for g in gaps]
        self.assertIn(
            'Polygon ((1001895.43752562382724136 1013467.22283697873353958, 1001907.30677810893394053 1013464.25552385742776096, 1001907.67769224906805903 1013454.2408420731080696, 1001895.43752562382724136 1013454.2408420731080696, 1001895.43752562382724136 1013467.22283697873353958))',
            geometries)
        self.assertIn(
            'Polygon ((1001847.96051568305119872 1013470.1901501000393182, 1001867.98987925180699676 1013469.07740767952054739, 1001869.10262167232576758 1013455.72449863376095891, 1001847.58960154291708022 1013455.72449863376095891, 1001847.96051568305119872 1013470.1901501000393182))',
            geometries)
        self.assertEqual(len(geometries), 2)
        test_plots_layer.rollBack()

        print('\nINFO: Validating Gaps in Plots using roads for only one geometry...')
        test_plots_layer.startEditing()
        test_plots_layer.deleteFeature(1)
        test_plots_layer.deleteFeature(2)
        test_plots_layer.deleteFeature(3)
        gaps = self.geometry.get_gaps_in_polygon_layer(test_plots_layer, include_roads=True)
        geometries = [g.asWkt() for g in gaps]
        self.assertEqual([], geometries)
        self.assertEqual(len(geometries), 0)

        test_plots_layer.rollBack()

        print('\nINFO: Validating Gaps in Plots without using roads for only one geometry...')
        test_plots_layer.startEditing()
        test_plots_layer.deleteFeature(1)
        test_plots_layer.deleteFeature(2)
        test_plots_layer.deleteFeature(3)
        gaps = self.geometry.get_gaps_in_polygon_layer(test_plots_layer, include_roads=False)
        geometries = [g.asWkt() for g in gaps]
        self.assertEqual([], geometries)
        self.assertEqual(len(geometries), 0)

        test_plots_layer.rollBack()

        print('\nINFO: Validating Gaps in Plots using roads for two geometries...')
        test_plots_layer.startEditing()
        test_plots_layer.deleteFeature(1)
        test_plots_layer.deleteFeature(3)
        gaps = self.geometry.get_gaps_in_polygon_layer(test_plots_layer, include_roads=True)
        geometries = [g.asWkt() for g in gaps]
        self.assertIn(
            'Polygon ((1001889.87381352134980261 1013447.93530169036239386, 1001885.42284383939113468 1013430.87325124291237444, 1001901.72405463655013591 1013411.57209242216777056, 1001845.19794039404951036 1013415.08188382943626493, 1001851.47861975431442261 1013424.31817700632382184, 1001833.74493685469496995 1013433.92392191023100168, 1001889.87381352134980261 1013447.93530169036239386))',
            geometries)
        self.assertEqual(len(geometries), 1)

        test_plots_layer.rollBack()

        print('\nINFO: Validating Gaps in Plots without using roads for two geometries...')
        test_plots_layer.startEditing()
        test_plots_layer.deleteFeature(1)
        test_plots_layer.deleteFeature(3 )
        gaps = self.geometry.get_gaps_in_polygon_layer(test_plots_layer, include_roads=False)
        geometries = [g.asWkt() for g in gaps]
        self.assertEqual([], geometries)
        self.assertEqual(len(geometries), 0)

        test_plots_layer.rollBack()

    def test_multiparts_in_right_of_way(self):
        print('\nINFO: Validating right_of_way for no multipart geometries...')
        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        uri = gpkg_path + '|layername={layername}'.format(layername='right_of_way')
        right_of_way = QgsVectorLayer(uri, 'right_of_way', 'ogr')

        self.assertEqual(right_of_way.featureCount(), 6)

        single_parts, single_ids = self.geometry.get_multipart_geoms(right_of_way)
        unique_single_ids = set(single_ids)
        self.assertEqual(len(single_parts), 8)
        self.assertEqual(len(unique_single_ids), 3)

        geometries = [g.asWkt() for g in single_parts]

        expected_list = [
            'Polygon ((1091145.85694021754898131 1121724.4278288041241467, 1091173.73775773262605071 1121765.70312499976716936, 1091206.17259239125996828 1121797.18358423886820674, 1091254.27673969138413668 1121818.85067654610611498, 1091289.43588917586021125 1121819.66833118535578251, 1091291.07119845412671566 1121759.97954252548515797, 1091260.00032216543331742 1121759.97954252548515797, 1091223.61469072219915688 1121742.80879510287195444, 1091197.44974226853810251 1121710.92026417492888868, 1091175.37306701089255512 1121673.30815077293664217, 1091177.00837628915905952 1121614.43701675231568515, 1091122.48462500004097819 1121616.61360054323449731, 1091119.46884239139035344 1121678.4371440215036273, 1091145.85694021754898131 1121724.4278288041241467))',
            'Polygon ((1091336.04220360890030861 1121821.30364046362228692, 1091432.52545103151351213 1121818.85067654610611498, 1091433.34310567076317966 1121757.52657860796898603, 1091336.04220360890030861 1121762.4325064430013299, 1091336.04220360890030861 1121821.30364046362228692))',
            'Polygon ((1091123.04317010380327702 1121561.28946520597673953, 1091175.37306701089255512 1121560.471810566727072, 1091172.10244845412671566 1121306.18121778313070536, 1091121.40786082530394197 1121307.81652706163004041, 1091123.04317010380327702 1121561.28946520597673953))',
            'Polygon ((1091487.30831185611896217 1121755.89126932970248163, 1091747.3224871139973402 1121750.16768685542047024, 1091747.3224871139973402 1121813.94474871107377112, 1091487.30831185611896217 1121818.85067654610611498, 1091487.30831185611896217 1121755.89126932970248163))',
            'Polygon ((1091747.3224871139973402 1121813.94474871107377112, 1091751.00193299050442874 1121954.58134664944373071, 1091806.6024484543595463 1121951.31072809267789125, 1091804.9671391760930419 1121217.05686211329884827, 1091749.36662371223792434 1121218.69217139179818332, 1091036.37177835148759186 1121226.86871778359636664, 1091039.64239690802060068 1121298.8223260308150202, 1091041.27770618651993573 1121310.26949097937904298, 1091121.40786082530394197 1121307.81652706163004041, 1091172.10244845412671566 1121306.18121778313070536, 1091425.57538659870624542 1121310.26949097937904298, 1091474.63466494926251471 1121316.81072809267789125, 1091749.36662371223792434 1121300.45763530931435525, 1091747.3224871139973402 1121750.16768685542047024, 1091747.3224871139973402 1121813.94474871107377112))',
            'Polygon ((1091041.27770618651993573 1121310.26949097937904298, 1091039.64239690802060068 1121298.8223260308150202, 1091036.37177835148759186 1121226.86871778359636664, 1090936.91814493527635932 1121227.28393303113989532, 1090936.91814493527635932 1122080.91537633049301803, 1091813.44391813105903566 1122080.91537633049301803, 1091806.6024484543595463 1121951.31072809267789125, 1091751.00193299050442874 1121954.58134664944373071, 1091754.57278410973958671 1122030.62961602141149342, 1090996.1981062744744122 1122030.62961602141149342, 1090996.1981062744744122 1121309.86705158883705735, 1091033.88846642058342695 1121310.19713682751171291, 1091038.64362105960026383 1121310.19713682751171291, 1091041.27770618651993573 1121310.26949097937904298))',
            'Polygon ((1090495.31252119154669344 1121959.44378872332163155, 1090784.3099831254221499 1121950.85970569564960897, 1090784.3099831254221499 1121676.16904880781657994, 1090501.03524321014992893 1121679.03040981711819768, 1090495.31252119154669344 1121959.44378872332163155),(1090604.04423954291269183 1121859.29615339962765574, 1090698.46915284800343215 1121856.434792390326038, 1090701.3305138573050499 1121753.4257960575632751, 1090615.48968357988633215 1121756.28715706686489284, 1090604.04423954291269183 1121859.29615339962765574))',
            'Polygon ((1090592.59879550593905151 1121550.26916440110653639, 1090724.22140193125233054 1121547.40780339180491865, 1090724.22140193125233054 1121398.61703091091476381, 1090592.59879550593905151 1121407.20111393858678639, 1090592.59879550593905151 1121550.26916440110653639))'
            ]

        for expected in expected_list:
            self.assertIn(expected, geometries)

    def test_check_buildings_within_plots(self):
        print('\nINFO: Validating buldings are within plots...')

        gpkg_path = get_test_copy_path('geopackage/buildings_plots.gpkg')
        uri = gpkg_path + '|layername={layername}'.format(layername='buildings')
        building_layer = QgsVectorLayer(uri, 'buildings', 'ogr')
        self.assertEqual(building_layer.featureCount(), 6)

        uri = gpkg_path + '|layername={layername}'.format(layername='plots')
        plot_layer = QgsVectorLayer(uri, 'plots', 'ogr')
        self.assertEqual(plot_layer.featureCount(), 5)

        buildings_disjoint, buildings_overlaps, building_within = GeometryUtils.get_relationships_among_polygons(
            building_layer,
            plot_layer)

        test_buildings_disjoint = [5]
        test_buildings_overlaps = [2, 6]
        test_building_within = [1, 3, 4]

        self.assertListEqual(list(set(buildings_disjoint)), test_buildings_disjoint)
        self.assertListEqual(list(set(buildings_overlaps)), test_buildings_overlaps)
        self.assertListEqual(list(set(building_within)), test_building_within)

    def test_no_error_quality_rule(self):
        self.db_gpkg = get_gpkg_conn('test_valid_quality_rules_gpkg')
        res, code, msg = self.db_gpkg.test_connection()
        self.assertTrue(res, msg)

        # When the tests are run the REGEXP function is not found, so we register it
        self.db_gpkg.conn.create_function("REGEXP", 2, _regexp)
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
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Point.OVERLAPS_IN_BOUNDARY_POINTS, layer_manager.get_layers(EnumQualityRule.Point.OVERLAPS_IN_BOUNDARY_POINTS))[1], Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Point.OVERLAPS_IN_CONTROL_POINTS, layer_manager.get_layers(EnumQualityRule.Point.OVERLAPS_IN_CONTROL_POINTS))[1], Qgis.Warning)  # "There are no points in layer 'lc_puntocontrol' to check for overlaps!"
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES, layer_manager.get_layers(EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES))[1], Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_PLOT_NODES, layer_manager.get_layers(EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_PLOT_NODES))[1], Qgis.Success)

        # Lines rules
        # TODO: Fix the OVERLAPS_IN_BOUNDARIES test!
        # self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Line.OVERLAPS_IN_BOUNDARIES)[1], Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Line.BOUNDARIES_ARE_NOT_SPLIT, layer_manager.get_layers(EnumQualityRule.Line.BOUNDARIES_ARE_NOT_SPLIT))[1], Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Line.BOUNDARIES_COVERED_BY_PLOTS, layer_manager.get_layers(EnumQualityRule.Line.BOUNDARIES_COVERED_BY_PLOTS))[1], Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS, layer_manager.get_layers(EnumQualityRule.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS))[1], Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Line.DANGLES_IN_BOUNDARIES, layer_manager.get_layers(EnumQualityRule.Line.DANGLES_IN_BOUNDARIES))[1], Qgis.Success)

        # Polygons rules
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Polygon.OVERLAPS_IN_PLOTS, layer_manager.get_layers(EnumQualityRule.Polygon.OVERLAPS_IN_PLOTS))[1], Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Polygon.OVERLAPS_IN_BUILDINGS, layer_manager.get_layers(EnumQualityRule.Polygon.OVERLAPS_IN_BUILDINGS))[1], Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Polygon.OVERLAPS_IN_RIGHTS_OF_WAY, layer_manager.get_layers(EnumQualityRule.Polygon.OVERLAPS_IN_RIGHTS_OF_WAY))[1], Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Polygon.PLOTS_COVERED_BY_BOUNDARIES, layer_manager.get_layers(EnumQualityRule.Polygon.PLOTS_COVERED_BY_BOUNDARIES))[1], Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Polygon.RIGHT_OF_WAY_OVERLAPS_BUILDINGS, layer_manager.get_layers(EnumQualityRule.Polygon.RIGHT_OF_WAY_OVERLAPS_BUILDINGS))[1], Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Polygon.GAPS_IN_PLOTS, layer_manager.get_layers(EnumQualityRule.Polygon.GAPS_IN_PLOTS))[1], Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Polygon.MULTIPART_IN_RIGHT_OF_WAY, layer_manager.get_layers(EnumQualityRule.Polygon.MULTIPART_IN_RIGHT_OF_WAY))[1], Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Polygon.PLOT_NODES_COVERED_BY_BOUNDARY_POINTS, layer_manager.get_layers(EnumQualityRule.Polygon.PLOT_NODES_COVERED_BY_BOUNDARY_POINTS))[1], Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Polygon.BUILDINGS_SHOULD_BE_WITHIN_PLOTS, layer_manager.get_layers(EnumQualityRule.Polygon.BUILDINGS_SHOULD_BE_WITHIN_PLOTS))[1], Qgis.Success)
        self.assertEqual(self.quality_rules.validate_quality_rule(self.db_gpkg, EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_PLOTS, layer_manager.get_layers(EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_PLOTS))[1], Qgis.Success)

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
        restore_schema('test_logic_quality_rules')
        db_pg = get_pg_conn('test_logic_quality_rules')
        names = db_pg.names
        res, code, msg = db_pg.test_connection()

        self.assertTrue(res, msg)
        self.assertIsNotNone(names.LC_BOUNDARY_POINT_T, 'Names is None')

        self.check_logic_quality_rules(db_pg)

    def test_logic_quality_rules_gpkg(self):
        db_gpkg = get_gpkg_conn('test_logic_quality_rules_gpkg')
        res, code, msg = db_gpkg.test_connection()
        self.assertTrue(res, msg)

        # When the tests are run the REGEXP function is not found, so we register it
        db_gpkg.conn.create_function("REGEXP", 2, _regexp)
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

    @classmethod
    def tearDownClass(cls):
        print("INFO: Unloading Model Baker...")
        unload_qgis_model_baker()


def _regexp(pattern, value):
    if value is None:
        return None
    return re.search(pattern, value) is not None

if __name__ == '__main__':
    nose2.main()
