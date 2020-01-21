import nose2
from qgis.PyQt.QtCore import QVariant
from qgis.core import (QgsVectorLayer,
                       QgsDataSourceUri,
                       QgsField,
                       QgsWkbTypes)
from qgis.testing import (unittest,
                          start_app)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.config.general_config import (TranslatableConfigStrings,
                                                      ERROR_BOUNDARY_IS_NOT_COVERED_BY_PLOT,
                                                      ERROR_BOUNDARY_NODE_IS_NOT_COVERED_BY_BOUNDARY_POINT,
                                                      ERROR_NO_FOUND_POINT_BFS,
                                                      ERROR_DUPLICATE_POINT_BFS,
                                                      ERROR_DUPLICATE_LESS_TABLE,
                                                      ERROR_NO_LESS_TABLE,
                                                      ERROR_NO_MORE_BOUNDARY_FACE_STRING_TABLE,
                                                      ERROR_BOUNDARY_POINT_IS_NOT_COVERED_BY_BOUNDARY_NODE,
                                                      ERROR_PLOT_IS_NOT_COVERED_BY_BOUNDARY,
                                                      ERROR_DUPLICATE_MORE_BOUNDARY_FACE_STRING_TABLE)
from asistente_ladm_col.config.table_mapping_config import Names
from asistente_ladm_col.tests.utils import (import_qgis_model_baker,
                                            import_processing,
                                            get_test_copy_path,
                                            get_pg_conn,
                                            restore_schema)
from asistente_ladm_col.utils.qgis_utils import QGISUtils
from asistente_ladm_col.logic.quality.quality import QualityUtils
from asistente_ladm_col.logic.quality.logic_checks import LogicChecks

import_qgis_model_baker()
import_processing()
import processing

class TesQualityValidations(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.qgis_utils = QGISUtils()
        self.quality = QualityUtils(self.qgis_utils)
        self.logic_checks = LogicChecks()
        self.translatable_config_strings = TranslatableConfigStrings()

        test_connection_dbs = ['test_ladm_validations_topology_tables', 'test_ladm_col_logic_checks']

        for test_connection_db in test_connection_dbs:
            restore_schema(test_connection_db)
            self.db_pg = get_pg_conn(test_connection_db)

        self.names = Names()

    def test_find_duplicate_records(self):
        schema_name = 'test_ladm_col_logic_checks'
        self.db_pg = get_pg_conn(schema_name)
        result = self.db_pg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')
        self.assertIsNotNone(self.names.OP_BOUNDARY_POINT_T, 'Names is None')

        db = self.db_pg

        test_results = {
            self.names.OP_PARTY_T: [('1068,1071', 2), ('1066,1069', 2), ('1067,1070', 2)],
            self.names.OP_BUILDING_UNIT_T: [('1112,1113', 2)],
            self.names.OP_BUILDING_T: [('1063,1064', 2), ('1062,1065', 2)],
            self.names.OP_PLOT_T: [('1099,1103', 2), ('1102,1104', 2)] ,
            self.names.OP_BOUNDARY_T: [('1073,1081', 2), ('1072,1082', 2), ('1078,1083', 2)],
            self.names.OP_SURVEY_POINT_T: [('1107,1109', 2), ('1108,1110', 2)],
            self.names.OP_BOUNDARY_POINT_T: [('1094,1097', 2), ('1088,1091', 2), ('1095,1096', 2), ('1087,1092', 2), ('1089,1098', 2), ('1090,1093', 2)]
        }

        for table in test_results:
            test_result = test_results[table]
            fields = self.names.get_logic_consistency_tables()[table]
            error_layer = None
            error_layer = self.logic_checks.get_duplicate_records_in_a_table(db, table, fields, error_layer, self.names.T_ID_F)
            result = [(f['duplicate_ids'],f['count']) for f in error_layer.getFeatures()]

            for item in test_result:
                self.assertIn(item, result, 'the record {error_item} is not duplicated in the table {table}'.format(error_item=item,table=table))

    def test_split_by_selected_boundary(self):
        print('\nINFO: Validation of the definition of selected boundary ...')

        gpkg_path = get_test_copy_path('geopackage/adjust_boundaries_cases.gpkg')

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
            new_geometries, boundaries_to_del_unique_ids = self.qgis_utils.geometry.fix_selected_boundaries(boundary_layer, self.names.T_ID_F, selected_ids=test_selected_ids)
            self.assertEqual(boundaries_to_del_unique_ids, test_result[i]['boundaries_to_del'], 'Boundaries to be deleted are not valid: case {case}'.format(case=i + 1))

            for new_geom in new_geometries:
                self.assertIn(new_geom.asWkt(), test_result[i]['geoms'],
                                 'The geometries are invalid: case {case}'.format(case=i + 1))

    def test_split_by_boundary(self):
        print('\nINFO: Validation of the definition of boundaries...')

        gpkg_path = get_test_copy_path('geopackage/adjust_boundaries_cases.gpkg')

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
            merge_geoms, boundaries_to_del = self.qgis_utils.geometry.fix_boundaries(boundary_layer, self.names.T_ID_F)
            self.assertEqual(boundaries_to_del, test_result[i]['boundaries_to_del'], 'The boundaries to delete are invalid: case {case}'.format(case=i + 1))

            for merge_geom in merge_geoms:
                self.assertIn(merge_geom.asWkt(), test_result[i]['geoms'],
                                 'The geometries are invalid: case {case}'.format(case=i + 1))

    def test_check_boundary_points_covered_by_plot_nodes(self):
        print('\nINFO: Validating boundary points are covered by plot nodes...')

        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        uri = gpkg_path + '|layername={layername}'.format(layername='puntolindero')
        boundary_point_layer = QgsVectorLayer(uri, 'puntolindero', 'ogr')
        self.assertEqual(boundary_point_layer.featureCount(), 82)

        uri = gpkg_path + '|layername={layername}'.format(layername='terreno')
        plot_layer = QgsVectorLayer(uri, 'terreno', 'ogr')
        self.assertEqual(plot_layer.featureCount(), 12)

        error_layer = QgsVectorLayer("Point?crs={}".format(boundary_point_layer.sourceCrs().authid()), 'error layer', "memory")
        data_provider = error_layer.dataProvider()
        data_provider.addAttributes([QgsField('id', QVariant.Int)])
        error_layer.updateFields()

        topology_rule = 'boundary_points_covered_by_plot_nodes'
        features = self.quality.get_boundary_points_features_not_covered_by_plot_nodes_and_viceversa(boundary_point_layer,
                                                                                                     plot_layer, error_layer,
                                                                                                     topology_rule,
                                                                                                     self.names.T_ID_F)
        error_layer.dataProvider().addFeatures(features)
        self.assertEqual(error_layer.featureCount(), 14)

        result = [{'geom': f.geometry().asWkt(), 'id': f['id']} for f in error_layer.getFeatures()]

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
        uri = gpkg_path + '|layername={layername}'.format(layername='puntolindero')
        boundary_point_layer = QgsVectorLayer(uri, 'puntolindero', 'ogr')
        self.assertEqual(boundary_point_layer.featureCount(), 82)

        uri = gpkg_path + '|layername={layername}'.format(layername='terreno')
        plot_layer = QgsVectorLayer(uri, 'terreno', 'ogr')
        self.assertEqual(plot_layer.featureCount(), 12)

        error_layer = QgsVectorLayer("Point?crs={}".format(plot_layer.sourceCrs().authid()), 'error layer', "memory")
        data_provider = error_layer.dataProvider()
        data_provider.addAttributes([QgsField('id', QVariant.Int)])
        error_layer.updateFields()

        topology_rule = 'plot_nodes_covered_by_boundary_points'
        features = self.quality.get_boundary_points_features_not_covered_by_plot_nodes_and_viceversa(boundary_point_layer,
                                                                                                     plot_layer, error_layer,
                                                                                                     topology_rule,
                                                                                                     self.names.T_ID_F)
        error_layer.dataProvider().addFeatures(features)
        self.assertEqual(error_layer.featureCount(), 10)

        result = [{'geom': f.geometry().asWkt(), 'id': f['id']} for f in error_layer.getFeatures()]

        test_result = [{'geom': 'Point (894809.40075360587798059 1544539.9176194816827774)', 'id': 2},
                       {'geom': 'Point (894810.34488280047662556 1544519.14677720214240253)', 'id': 2},
                       {'geom': 'Point (894837.25256484432611614 1544520.56297099380753934)', 'id': 2},
                       {'geom': 'Point (894833.94811266358010471 1544542.75000706524588168)', 'id': 2},
                       {'geom': 'Point (894852.59466425550635904 1544369.26626757089979947)', 'id': 6},
                       {'geom': 'Point (894852.59466425550635904 1544369.26626757089979947)', 'id': 7},
                       {'geom': 'Point (894934.73390417906921357 1544264.93999157636426389)', 'id': 9},
                       {'geom': 'Point (894484.66213072568643838 1544624.06759340292774141)', 'id': 11},
                       {'geom': 'Point (894533.21481920615769923 1544601.79047751193866134)', 'id': 11},
                       {'geom': 'Point (894505.22562231740448624 1544589.22389931697398424)', 'id': 11}]

        for item in test_result:
            self.assertIn(item, result,
                          'Error in: Plot node {} is not covered by boundary point'.format(item['id']))

    def test_topology_boundary_nodes_must_be_covered_by_boundary_points(self):
        translated_strings = self.translatable_config_strings.get_translatable_config_strings()
        schema_name = 'test_ladm_validations_topology_tables'
        self.db_pg = get_pg_conn(schema_name)
        result = self.db_pg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')
        self.assertIsNotNone(self.names.OP_BOUNDARY_POINT_T, 'Names is None')

        boundary_point_layer = self.qgis_utils.get_layer(self.db_pg, self.names.OP_BOUNDARY_POINT_T, load=True)
        self.assertEqual(boundary_point_layer.featureCount(), 109)

        boundary_layer = self.qgis_utils.get_layer(self.db_pg, self.names.OP_BOUNDARY_T, load=True)
        self.assertEqual(boundary_layer.featureCount(), 22)

        plot_layer = self.qgis_utils.get_layer(self.db_pg, self.names.OP_PLOT_T, load=True)
        self.assertEqual(plot_layer.featureCount(), 17)

        point_bfs_layer = self.qgis_utils.get_layer(self.db_pg, self.names.POINT_BFS_T, load=True)
        self.assertEqual(point_bfs_layer.featureCount(), 81)

        error_layer = QgsVectorLayer("Point?crs={}".format(boundary_layer.sourceCrs().authid()), 'error layer', "memory")

        data_provider = error_layer.dataProvider()
        data_provider.addAttributes([QgsField('boundary_point_id', QVariant.Int),
                                     QgsField('boundary_id', QVariant.Int),
                                     QgsField('error_type', QVariant.String)])
        error_layer.updateFields()

        features = self.quality.get_boundary_nodes_features_not_covered_by_boundary_points(self.db_connection, boundary_point_layer, boundary_layer, point_bfs_layer, error_layer, translated_strings, self.names.T_ID_F)

        # the algorithm was successfully executed
        self.assertEqual(len(features), 33)
        error_layer.dataProvider().addFeatures(features)

        # English language is set as default for validations
        exp = "\"error_type\" = '{}'".format(translated_strings[ERROR_BOUNDARY_NODE_IS_NOT_COVERED_BY_BOUNDARY_POINT])
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 13)

        result = [{'id': f['boundary_id'], 'geom': f.geometry().asWkt()} for f in error_layer.selectedFeatures()]

        test_result = [{'id': 368, 'geom': 'PointZ (895065.96799999999348074 1544460.84700000006705523 0)'},
                       {'id': 368, 'geom': 'PointZ (895076.28099999995902181 1544438.87899999995715916 0)'},
                       {'id': 368, 'geom': 'PointZ (895126.55500000005122274 1544446.56199999991804361 0)'},
                       {'id': 368, 'geom': 'PointZ (895138.19400000001769513 1544479.25699999998323619 0)'},
                       {'id': 368, 'geom': 'PointZ (895150.11300000001210719 1544450.162999999942258 0)'},
                       {'id': 371, 'geom': 'PointZ (894732.84299999999348074 1544594.1229999999050051 0)'},
                       {'id': 371, 'geom': 'PointZ (894770.40800000005401671 1544602.14299999992363155 0)'},
                       {'id': 372, 'geom': 'PointZ (894822.14000000001396984 1544541.38800000003539026 0)'},
                       {'id': 373, 'geom': 'PointZ (894911.74499999999534339 1544391.85100000002421439 0)'},
                       {'id': 374, 'geom': 'PointZ (895120.1720000000204891 1544364.95600000000558794 0)'},
                       {'id': 374, 'geom': 'PointZ (895070.0779999999795109 1544331.15500000002793968 0)'},
                       {'id': 374, 'geom': 'PointZ (895121.96699999994598329 1544243.82499999995343387 0)'},
                       {'id': 374, 'geom': 'PointZ (895178.80000000004656613 1544283.712000000057742 0)'}]

        for item in test_result:
            self.assertIn(item, result, 'Error in {}: {}'.format(item, translated_strings[ERROR_BOUNDARY_NODE_IS_NOT_COVERED_BY_BOUNDARY_POINT]))

        exp = "\"error_type\" = '{}'".format(translated_strings[ERROR_DUPLICATE_POINT_BFS])
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 8)
        result = [{'boundary_point_id': f['boundary_point_id'], 'boundary_id': f['boundary_id']} for f in error_layer.selectedFeatures()]

        test_result = [{'boundary_point_id': 461, 'boundary_id': 377},
                       {'boundary_point_id': 463, 'boundary_id': 375},
                       {'boundary_point_id': 469, 'boundary_id': 378},
                       {'boundary_point_id': 470, 'boundary_id': 370},
                       {'boundary_point_id': 472, 'boundary_id': 370},
                       {'boundary_point_id': 455, 'boundary_id': 376},
                       {'boundary_point_id': 459, 'boundary_id': 377},
                       {'boundary_point_id': 457, 'boundary_id': 376}]

        for item in test_result:
            self.assertIn(item, result, 'Error in {}: {}'.format(item, translated_strings[ERROR_DUPLICATE_POINT_BFS]))

        exp = "\"error_type\" = '{}'".format(translated_strings[ERROR_NO_FOUND_POINT_BFS])
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 12)
        result = [{'boundary_point_id': f['boundary_point_id'], 'boundary_id': f['boundary_id']} for f in error_layer.selectedFeatures()]

        test_result = [{'boundary_point_id': 408, 'boundary_id': 362},
                       {'boundary_point_id': 437, 'boundary_id': 364},
                       {'boundary_point_id': 434, 'boundary_id': 364},
                       {'boundary_point_id': 409, 'boundary_id': 362},
                       {'boundary_point_id': 439, 'boundary_id': 365},
                       {'boundary_point_id': 440, 'boundary_id': 365},
                       {'boundary_point_id': 441, 'boundary_id': 365},
                       {'boundary_point_id': 438, 'boundary_id': 365},
                       {'boundary_point_id': 436, 'boundary_id': 364},
                       {'boundary_point_id': 435, 'boundary_id': 364},
                       {'boundary_point_id': 406, 'boundary_id': 362},
                       {'boundary_point_id': 407, 'boundary_id': 362}]

        for item in test_result:
            self.assertIn(item, result, 'Error in {}: {}'.format(item, translated_strings[ERROR_NO_FOUND_POINT_BFS]))

    def test_topology_boundary_points_must_be_covered_by_boundary_nodes(self):
        translated_strings = self.translatable_config_strings.get_translatable_config_strings()
        schema_name = 'test_ladm_validations_topology_tables'
        self.db_pg = get_pg_conn(schema_name)
        result = self.db_pg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')
        self.assertIsNotNone(self.names.OP_BOUNDARY_POINT_T, 'Names is None')

        boundary_point_layer = self.qgis_utils.get_layer(self.db_pg, self.names.OP_BOUNDARY_POINT_T, load=True)
        self.assertEqual(boundary_point_layer.featureCount(), 109)

        boundary_layer = self.qgis_utils.get_layer(self.db_pg, self.names.OP_BOUNDARY_T, load=True)
        self.assertEqual(boundary_layer.featureCount(), 22)

        plot_layer = self.qgis_utils.get_layer(self.db_pg, self.names.OP_PLOT_T, load=True)
        self.assertEqual(plot_layer.featureCount(), 17)

        point_bfs_layer = self.qgis_utils.get_layer(self.db_pg, self.names.POINT_BFS_T, load=True)
        self.assertEqual(point_bfs_layer.featureCount(), 81)

        more_bfs_layer = self.qgis_utils.get_layer(self.db_pg, self.names.MORE_BFS_T, load=True)
        self.assertEqual(more_bfs_layer.featureCount(), 18)

        less_layer = self.qgis_utils.get_layer(self.db_pg, self.names.LESS_BFS_T, load=True)
        self.assertEqual(less_layer.featureCount(), 6)

        error_layer = QgsVectorLayer("Point?crs={}".format(boundary_layer.sourceCrs().authid()), 'error layer', "memory")

        data_provider = error_layer.dataProvider()
        data_provider.addAttributes([QgsField('boundary_point_id', QVariant.Int),
                                     QgsField('boundary_id', QVariant.Int),
                                     QgsField('error_type', QVariant.String)])
        error_layer.updateFields()

        features = self.quality.get_boundary_points_features_not_covered_by_boundary_nodes(self.db_connection, boundary_point_layer, boundary_layer, point_bfs_layer, error_layer, translated_strings, self.names.T_ID_F)

        # the algorithm was successfully executed
        self.assertEqual(len(features), 54)

        error_layer.dataProvider().addFeatures(features)

        # English language is set as default for validations
        exp = "\"error_type\" = '{}'".format(translated_strings[ERROR_BOUNDARY_POINT_IS_NOT_COVERED_BY_BOUNDARY_NODE])
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 34)

        result = [{'id': f['boundary_point_id'], 'geom': f.geometry().asWkt()} for f in error_layer.selectedFeatures()]

        test_result = [{'id': 382, 'geom': 'PointZ (894639.00399999995715916 1544574.38599999994039536 0)'},
                       {'id': 383, 'geom': 'PointZ (894648.56400000001303852 1544485.16100000008009374 0)'},
                       {'id': 384, 'geom': 'PointZ (894723.67700000002514571 1544488.34799999999813735 0)'},
                       {'id': 385, 'geom': 'PointZ (894715.02700000000186265 1544590.31899999990127981 0)'},
                       {'id': 386, 'geom': 'PointZ (894715.02700000000186265 1544590.31899999990127981 0)'},
                       {'id': 389, 'geom': 'PointZ (894723.67700000002514571 1544488.34799999999813735 0)'},
                       {'id': 398, 'geom': 'PointZ (894856.60699999995995313 1544597.51000000000931323 0)'},
                       {'id': 399, 'geom': 'PointZ (894860.856000000028871 1544572.962000000057742 0)'},
                       {'id': 400, 'geom': 'PointZ (894879.26599999994505197 1544575.79499999992549419 0)'},
                       {'id': 401, 'geom': 'PointZ (894882.57099999999627471 1544602.70200000004842877 0)'},
                       {'id': 404, 'geom': 'PointZ (894837.25300000002607703 1544520.56300000008195639 0)'},
                       {'id': 405, 'geom': 'PointZ (894833.94799999997485429 1544542.75 0)'},
                       {'id': 410, 'geom': 'PointZ (894634.73699999996460974 1544430.39899999997578561 0)'},
                       {'id': 411, 'geom': 'PointZ (894638.04099999996833503 1544358.17299999995157123 0)'},
                       {'id': 412, 'geom': 'PointZ (894773.52399999997578561 1544367.14199999999254942 0)'},
                       {'id': 413, 'geom': 'PointZ (894768.33100000000558794 1544443.6159999999217689 0)'},
                       {'id': 414, 'geom': 'PointZ (894768.33100000000558794 1544443.6159999999217689 0)'},
                       {'id': 415, 'geom': 'PointZ (894696.625 1544436.52200000011362135 0)'},
                       {'id': 416, 'geom': 'PointZ (894702.99199999996926636 1544362.47299999999813735 0)'},
                       {'id': 417, 'geom': 'PointZ (894773.52399999997578561 1544367.14199999999254942 0)'},
                       {'id': 418, 'geom': 'PointZ (894702.99199999996926636 1544362.47299999999813735 0)'},
                       {'id': 419, 'geom': 'PointZ (894696.625 1544436.52200000011362135 0)'},
                       {'id': 420, 'geom': 'PointZ (894634.73699999996460974 1544430.39899999997578561 0)'},
                       {'id': 421, 'geom': 'PointZ (894638.04099999996833503 1544358.17299999995157123 0)'},
                       {'id': 422, 'geom': 'PointZ (894847.40200000000186265 1544448.57300000009126961 0)'},
                       {'id': 425, 'geom': 'PointZ (894972.97100000001955777 1544459.43100000009872019 0)'},
                       {'id': 426, 'geom': 'PointZ (894847.40200000000186265 1544448.57300000009126961 0)'},
                       {'id': 428, 'geom': 'PointZ (894914.05400000000372529 1544372.94500000006519258 0)'},
                       {'id': 431, 'geom': 'PointZ (894972.97100000001955777 1544459.43100000009872019 0)'},
                       {'id': 433, 'geom': 'PointZ (894914.05400000000372529 1544372.94500000006519258 0)'},
                       {'id': 446, 'geom': 'PointZ (894863.92399999999906868 1544306.01000000000931323 0)'},
                       {'id': 447, 'geom': 'PointZ (894862.50800000003073364 1544287.59899999992921948 0)'},
                       {'id': 448, 'geom': 'PointZ (894910.65899999998509884 1544288.07099999999627471 0)'},
                       {'id': 449, 'geom': 'PointZ (894905.93799999996554106 1544314.50699999998323619 0)'}]

        for item in test_result:
            self.assertIn(item, result, 'Error in {}: {}'.format(item, translated_strings[ERROR_BOUNDARY_POINT_IS_NOT_COVERED_BY_BOUNDARY_NODE]))

        exp = "\"error_type\" = '{}'".format(translated_strings[ERROR_DUPLICATE_POINT_BFS])
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 8)
        result = [{'boundary_point_id': f['boundary_point_id'], 'boundary_id': f['boundary_id']} for f in error_layer.selectedFeatures()]
        test_result = [{'boundary_point_id': 457, 'boundary_id': 376},
                       {'boundary_point_id': 469, 'boundary_id': 378},
                       {'boundary_point_id': 461, 'boundary_id': 377},
                       {'boundary_point_id': 455, 'boundary_id': 376},
                       {'boundary_point_id': 472, 'boundary_id': 370},
                       {'boundary_point_id': 463, 'boundary_id': 375},
                       {'boundary_point_id': 459, 'boundary_id': 377},
                       {'boundary_point_id': 470, 'boundary_id': 370}]

        for item in test_result:
            self.assertIn(item, result, 'Error in {}: {}'.format(item, translated_strings[ERROR_DUPLICATE_POINT_BFS]))

        exp = "\"error_type\" = '{}'".format(translated_strings[ERROR_NO_FOUND_POINT_BFS])
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 12)
        result = [{'boundary_point_id': f['boundary_point_id'], 'boundary_id': f['boundary_id']} for f in error_layer.selectedFeatures()]

        test_result = [{'boundary_point_id': 409, 'boundary_id': 362},
                       {'boundary_point_id': 436, 'boundary_id': 364},
                       {'boundary_point_id': 434, 'boundary_id': 364},
                       {'boundary_point_id': 407, 'boundary_id': 362},
                       {'boundary_point_id': 438, 'boundary_id': 365},
                       {'boundary_point_id': 439, 'boundary_id': 365},
                       {'boundary_point_id': 441, 'boundary_id': 365},
                       {'boundary_point_id': 435, 'boundary_id': 364},
                       {'boundary_point_id': 440, 'boundary_id': 365},
                       {'boundary_point_id': 437, 'boundary_id': 364},
                       {'boundary_point_id': 406, 'boundary_id': 362},
                       {'boundary_point_id': 408, 'boundary_id': 362}]

        for item in test_result:
            self.assertIn(item, result, 'Error in {}: {}'.format(item, translated_strings[ERROR_NO_FOUND_POINT_BFS]))

    def test_topology_plot_must_be_covered_by_boundary(self):
        translated_strings = self.translatable_config_strings.get_translatable_config_strings()
        schema_name = 'test_ladm_validations_topology_tables'
        self.db_pg = get_pg_conn(schema_name)
        result = self.db_pg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')
        self.assertIsNotNone(self.names.OP_BOUNDARY_POINT_T, 'Names is None')

        boundary_point_layer = self.qgis_utils.get_layer(self.db_pg, self.names.OP_BOUNDARY_POINT_T, load=True)
        self.assertEqual(boundary_point_layer.featureCount(), 109)

        boundary_layer = self.qgis_utils.get_layer(self.db_pg, self.names.OP_BOUNDARY_T, load=True)
        self.assertEqual(boundary_layer.featureCount(), 22)

        plot_layer = self.qgis_utils.get_layer(self.db_pg, self.names.OP_PLOT_T, load=True)
        self.assertEqual(plot_layer.featureCount(), 17)

        point_bfs_layer = self.qgis_utils.get_layer(self.db_pg, self.names.POINT_BFS_T, load=True)
        self.assertEqual(point_bfs_layer.featureCount(), 81)

        more_bfs_layer = self.qgis_utils.get_layer(self.db_pg, self.names.MORE_BFS_T, load=True)
        self.assertEqual(more_bfs_layer.featureCount(), 18)

        less_layer = self.qgis_utils.get_layer(self.db_pg, self.names.LESS_BFS_T, load=True)
        self.assertEqual(less_layer.featureCount(), 6)

        error_layer = QgsVectorLayer("MultiLineString?crs={}".format(plot_layer.sourceCrs().authid()), 'error layer', "memory")

        data_provider = error_layer.dataProvider()
        data_provider.addAttributes([QgsField('plot_id', QVariant.Int),
                                     QgsField('boundary_id', QVariant.Int),
                                     QgsField('error_type', QVariant.String)])
        error_layer.updateFields()

        features = self.quality.get_plot_features_not_covered_by_boundaries(self.db_connection, plot_layer, boundary_layer, more_bfs_layer, less_layer, error_layer, translated_strings, self.names.T_ID_F)

        # the algorithm was successfully executed
        self.assertEqual(len(features), 16)

        error_layer.dataProvider().addFeatures(features)

        # English language is set as default for validations
        exp = "\"error_type\" = '{}'".format(translated_strings[ERROR_PLOT_IS_NOT_COVERED_BY_BOUNDARY])

        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 12)

        result = [{'id': f['plot_id'], 'geom': f.geometry().asWkt()} for f in error_layer.selectedFeatures()]

        test_result = [{'id': 491, 'geom': 'MultiLineStringZ ((894639.00399999995715916 1544574.38599999994039536 0, 894648.56400000001303852 1544485.16100000008009374 0, 894723.67700000002514571 1544488.34799999999813735 0, 894715.02700000000186265 1544590.31899999990127981 0, 894639.00399999995715916 1544574.38599999994039536 0))'},
                       {'id': 492, 'geom': 'MultiLineStringZ ((894715.02700000000186265 1544590.31899999990127981 0, 894732.84299999999348074 1544594.1229999999050051 0),(894770.40800000005401671 1544602.14299999992363155 0, 894779.66099999996367842 1544604.11800000001676381 0),(894788.15800000005401671 1544496.48799999989569187 0, 894723.67700000002514571 1544488.34799999999813735 0, 894715.02700000000186265 1544590.31899999990127981 0))'},
                       {'id': 493, 'geom': 'MultiLineStringZ ((894856.60699999995995313 1544597.51000000000931323 0, 894860.856000000028871 1544572.962000000057742 0, 894879.26599999994505197 1544575.79499999992549419 0, 894882.57099999999627471 1544602.70200000004842877 0, 894856.60699999995995313 1544597.51000000000931323 0),(894810.34499999997206032 1544519.14700000011362135 0, 894837.25300000002607703 1544520.56300000008195639 0, 894833.94799999997485429 1544542.75 0, 894822.14000000001396984 1544541.38800000003539026 0))'},
                       {'id': 494, 'geom': 'MultiLineStringZ ((894634.73699999996460974 1544430.39899999997578561 0, 894638.04099999996833503 1544358.17299999995157123 0, 894773.52399999997578561 1544367.14199999999254942 0, 894768.33100000000558794 1544443.6159999999217689 0, 894634.73699999996460974 1544430.39899999997578561 0))'},
                       {'id': 495, 'geom': 'MultiLineStringZ ((894768.33100000000558794 1544443.6159999999217689 0, 894696.625 1544436.52200000011362135 0, 894702.99199999996926636 1544362.47299999999813735 0, 894773.52399999997578561 1544367.14199999999254942 0, 894768.33100000000558794 1544443.6159999999217689 0))'},
                       {'id': 496, 'geom': 'MultiLineStringZ ((894702.99199999996926636 1544362.47299999999813735 0, 894696.625 1544436.52200000011362135 0, 894634.73699999996460974 1544430.39899999997578561 0, 894638.04099999996833503 1544358.17299999995157123 0, 894702.99199999996926636 1544362.47299999999813735 0))'},
                       {'id': 497, 'geom': 'MultiLineStringZ ((894847.40200000000186265 1544448.57300000009126961 0, 894852.59499999997206032 1544369.26600000006146729 0),(894986.66099999996367842 1544377.29099999996833503 0, 894972.97100000001955777 1544459.43100000009872019 0, 894904.21900145395193249 1544453.48598809260874987 0),(894904.21900145395193249 1544453.48598809260874987 0, 894847.40200000000186265 1544448.57300000009126961 0))'},
                       {'id': 498, 'geom': 'MultiLineStringZ ((894847.40200000000186265 1544448.57300000009126961 0, 894852.59499999997206032 1544369.26600000006146729 0),(894852.59499999997206032 1544369.26600000006146729 0, 894914.05400000000372529 1544372.94500000006519258 0, 894911.74499999999534339 1544391.85100000002421439 0),(894904.21900000004097819 1544453.48600000003352761 0, 894847.40200000000186265 1544448.57300000009126961 0))'},
                       {'id': 499, 'geom': 'MultiLineStringZ ((894904.21900000004097819 1544453.48600000003352761 0, 894972.97100000001955777 1544459.43100000009872019 0, 894986.66099999996367842 1544377.29099999996833503 0),(894986.66099999996367842 1544377.29099999996833503 0, 894914.05400000000372529 1544372.94500000006519258 0, 894911.74499999999534339 1544391.85100000002421439 0))'},
                       {'id': 501, 'geom': 'MultiLineStringZ ((894863.92399999999906868 1544306.01000000000931323 0, 894862.50800000003073364 1544287.59899999992921948 0, 894910.65899999998509884 1544288.07099999999627471 0, 894905.93799999996554106 1544314.50699999998323619 0, 894863.92399999999906868 1544306.01000000000931323 0))'},
                       {'id': 502, 'geom': 'MultiLineStringZ ((895053.2219999999506399 1544435.35499999998137355 0, 895076.28099999995902181 1544438.87899999995715916 0),(895076.28099999995902181 1544438.87899999995715916 0, 895119.085573127027601 1544445.42050326871685684 0),(895119.085573127027601 1544445.42050326871685684 0, 895126.55500278458930552 1544446.56200782209634781 0),(895126.55500278458930552 1544446.56200782209634781 0, 895126.55500278470572084 1544446.56200782209634781 0),(895126.55500278470572084 1544446.56200782209634781 0, 895150.11300000001210719 1544450.162999999942258 0))'},
                       {'id': 506, 'geom': 'MultiLineStringZ ((871581.97699999995529652 1554559.162999999942258 0, 871583.06900000001769513 1554559.11199999996460974 0, 871586.15099999995436519 1554558.96699999994598329 0))'}]

        for item in test_result:
            self.assertIn(item, result, 'geometrical error in the polygon with id {}'.format(item['id']))


        exp = "\"error_type\" = '{}'".format(translated_strings[ERROR_DUPLICATE_MORE_BOUNDARY_FACE_STRING_TABLE])
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 1)
        result = [{'plot_id': f['plot_id'], 'boundary_id': f['boundary_id']} for f in error_layer.selectedFeatures()]
        test_result = [{'plot_id': 504, 'boundary_id': 376}]
        self.assertEqual(result, test_result, 'Error in: {}'.format(translated_strings[ERROR_DUPLICATE_MORE_BOUNDARY_FACE_STRING_TABLE]))

        exp = "\"error_type\" = '{}'".format(translated_strings[ERROR_DUPLICATE_LESS_TABLE])
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 1)
        result = [{'plot_id': f['plot_id'], 'boundary_id': f['boundary_id']} for f in error_layer.selectedFeatures()]
        test_result = [{'plot_id': 504, 'boundary_id': 377}]
        self.assertEqual(result, test_result, 'Error in: {}'.format(translated_strings[ERROR_DUPLICATE_LESS_TABLE]))

        exp = "\"error_type\" = '{}'".format(translated_strings[ERROR_NO_MORE_BOUNDARY_FACE_STRING_TABLE])
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 1)
        result = [{'plot_id': f['plot_id'], 'boundary_id': f['boundary_id']} for f in error_layer.selectedFeatures()]
        test_result = [{'plot_id': 505, 'boundary_id': 375}]
        self.assertEqual(result, test_result, 'Error in: {}'.format(translated_strings[ERROR_NO_MORE_BOUNDARY_FACE_STRING_TABLE]))

        exp = "\"error_type\" = '{}'".format(translated_strings[ERROR_NO_LESS_TABLE])
        error_layer.selectByExpression(exp)
        self.assertEqual(error_layer.selectedFeatureCount(), 1)
        result = [{'plot_id': f['plot_id'], 'boundary_id': f['boundary_id']} for f in error_layer.selectedFeatures()]
        test_result = [{'plot_id': 500, 'boundary_id': 365}]
        self.assertEqual(result, test_result, 'Error in: {}'.format(translated_strings[ERROR_NO_LESS_TABLE]))

    def test_topology_boundary_must_be_covered_by_plot(self):
       translated_strings = self.translatable_config_strings.get_translatable_config_strings()
       schema_name = 'test_ladm_validations_topology_tables'
       self.db_pg = get_pg_conn(schema_name)
       result = self.db_pg.test_connection()
       self.assertTrue(result[0], 'The test connection is not working')
       self.assertIsNotNone(self.names.OP_BOUNDARY_POINT_T, 'Names is None')

       boundary_point_layer = self.qgis_utils.get_layer(self.db_pg, self.names.OP_BOUNDARY_POINT_T, load=True)
       self.assertEqual(boundary_point_layer.featureCount(), 109)

       boundary_layer = self.qgis_utils.get_layer(self.db_pg, self.names.OP_BOUNDARY_T, load=True)
       self.assertEqual(boundary_layer.featureCount(), 22)

       plot_layer = self.qgis_utils.get_layer(self.db_pg, self.names.OP_PLOT_T, load=True)
       self.assertEqual(plot_layer.featureCount(), 17)

       point_bfs_layer = self.qgis_utils.get_layer(self.db_pg, self.names.POINT_BFS_T, load=True)
       self.assertEqual(point_bfs_layer.featureCount(), 81)

       more_bfs_layer = self.qgis_utils.get_layer(self.db_pg, self.names.MORE_BFS_T, load=True)
       self.assertEqual(more_bfs_layer.featureCount(), 18)

       less_layer = self.qgis_utils.get_layer(self.db_pg, self.names.LESS_BFS_T, load=True)
       self.assertEqual(less_layer.featureCount(), 6)

       error_layer = QgsVectorLayer("MultiLineString?crs={}".format(plot_layer.sourceCrs().authid()), 'error layer', "memory")

       data_provider = error_layer.dataProvider()
       data_provider.addAttributes([QgsField('plot_id', QVariant.Int),
                                    QgsField('boundary_id', QVariant.Int),
                                    QgsField('error_type', QVariant.String)])
       error_layer.updateFields()

       features = self.quality.get_boundary_features_not_covered_by_plots(self.db_connection, plot_layer, boundary_layer, more_bfs_layer, less_layer, error_layer, translated_strings, self.names.T_ID_F)

       # the algorithm was successfully executed
       self.assertEqual(len(features), 11)

       error_layer.dataProvider().addFeatures(features)

       # English language is set as default for validations
       exp = "\"error_type\" = '{}'".format(translated_strings[ERROR_BOUNDARY_IS_NOT_COVERED_BY_PLOT])
       error_layer.selectByExpression(exp)
       self.assertEqual(error_layer.selectedFeatureCount(), 3)

       result = [{'id': f['boundary_id'], 'id_plot': f['plot_id'], 'geom': f.geometry().asWkt()} for f in error_layer.selectedFeatures()]

       test_result = [
           {'id': 374, 'id_plot': None, 'geom': 'MultiLineStringZ ((895120.1720000000204891 1544364.95600000000558794 0, 895070.0779999999795109 1544331.15500000002793968 0, 895121.96699999994598329 1544243.82499999995343387 0, 895178.80000000004656613 1544283.712000000057742 0, 895120.1720000000204891 1544364.95600000000558794 0))'},
           {'id': 379, 'id_plot': 506,  'geom': 'LineStringZ (871560.6650000000372529 1554564.43599999998696148 0, 871564.08799999998882413 1554562.86700000008568168 0, 871564.11399999994318932 1554562.17299999995157123 0, 871581.97699999995529652 1554559.162999999942258 0, 871586.15099999995436519 1554558.96699999994598329 0)'},
           {'id': 368, 'id_plot': None, 'geom': 'MultiLineStringZ ((895053.2219999999506399 1544435.35499999998137355 0, 895065.96799999999348074 1544460.84700000006705523 0, 895076.28099999995902181 1544438.87899999995715916 0),(895126.55500000005122274 1544446.56199999991804361 0, 895126.55500278470572084 1544446.56200782209634781 0),(895126.55500278470572084 1544446.56200782209634781 0, 895138.19400000001769513 1544479.25699999998323619 0, 895150.11300000001210719 1544450.162999999942258 0))'}
       ]

       for item in test_result:
           self.assertIn(item, result, 'Error: Boundary is not covered by the plot.  boundary_id = {}'.format(item['id']))

       exp = "\"error_type\" = '{}'".format(translated_strings[ERROR_DUPLICATE_MORE_BOUNDARY_FACE_STRING_TABLE])
       error_layer.selectByExpression(exp)
       self.assertEqual(error_layer.selectedFeatureCount(), 2)
       result = [{'plot_id': f['plot_id'], 'boundary_id': f['boundary_id']} for f in error_layer.selectedFeatures()]
       test_result = [{'plot_id': 492, 'boundary_id': 360}, {'plot_id': 504, 'boundary_id': 376}]

       for item in test_result:
           self.assertIn(item, result, 'Error in: {}'.format(translated_strings[ERROR_DUPLICATE_MORE_BOUNDARY_FACE_STRING_TABLE]))

       exp = "\"error_type\" = '{}'".format(translated_strings[ERROR_DUPLICATE_LESS_TABLE])
       error_layer.selectByExpression(exp)
       self.assertEqual(error_layer.selectedFeatureCount(), 2)
       result = [{'plot_id': f['plot_id'], 'boundary_id': f['boundary_id']} for f in error_layer.selectedFeatures()]
       test_result = [{'plot_id': 504, 'boundary_id': 377}, {'plot_id': 493, 'boundary_id': 361}]

       for item in test_result:
           self.assertIn(item, result, 'Error in: {}'.format(translated_strings[ERROR_DUPLICATE_LESS_TABLE]))

       exp = "\"error_type\" = '{}'".format(translated_strings[ERROR_NO_MORE_BOUNDARY_FACE_STRING_TABLE])
       error_layer.selectByExpression(exp)
       self.assertEqual(error_layer.selectedFeatureCount(), 2)
       result = [{'plot_id': f['plot_id'], 'boundary_id': f['boundary_id']} for f in error_layer.selectedFeatures()]
       test_result = [{'plot_id': 505, 'boundary_id': 375}, {'plot_id': 501, 'boundary_id': 366}]

       for item in test_result:
           self.assertIn(item, result, 'Error in: {}'.format(translated_strings[ERROR_NO_MORE_BOUNDARY_FACE_STRING_TABLE]))

       exp = "\"error_type\" = '{}'".format(translated_strings[ERROR_NO_LESS_TABLE])
       error_layer.selectByExpression(exp)
       self.assertEqual(error_layer.selectedFeatureCount(), 2)
       result = [{'plot_id': f['plot_id'], 'boundary_id': f['boundary_id']} for f in error_layer.selectedFeatures()]
       test_result = [{'plot_id': 493, 'boundary_id': 362}, {'plot_id': 500, 'boundary_id': 365}]

       for item in test_result:
           self.assertIn(item, result, 'Error in: {}'.format(translated_strings[ERROR_NO_LESS_TABLE]))

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

        overlapping = self.qgis_utils.geometry.get_overlapping_points(overlapping_points_layer)
        self.assertTrue(len(overlapping), 1) # One list of overlapping ids

        for overlapping_ids in overlapping:
            self.assertTrue(len(overlapping_ids), 2) # Two points overlap
            points = []

            for feature in overlapping_points_layer.getFeatures(overlapping_ids):
                points.append(feature.geometry().asWkt())

            unique_points = set(points) # get unique values
            self.assertEqual(len(unique_points), 1, 'The intersection failed, points are not equal')
            self.assertEqual(list(unique_points)[0], list(expected_overlaps.values())[0])

    def test_get_overlapping_lines(self):
        print('\nINFO: Validating overlaps in boundaries...')
        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        uri = gpkg_path + '|layername={layername}'.format(layername='test_boundaries_overlap')
        boundary_overlap_layer = QgsVectorLayer(uri, 'test_boundaries_overlap', 'ogr')

        features = [feature for feature in boundary_overlap_layer.getFeatures()]
        self.assertEqual(len(features), 15)

        overlapping = self.qgis_utils.geometry.get_overlapping_lines(boundary_overlap_layer)

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
            insert_into_res([point[self.names.T_ID_F], point[self.names.T_ID_F+'_2']], point.geometry().asWkt())

        for line in line_features:
            insert_into_res([line[self.names.T_ID_F], line[self.names.T_ID_F+'_2']], line.geometry().asWkt())

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

        overlapping = self.qgis_utils.geometry.get_overlapping_polygons(polygons_overlap_layer)
        flat_overlapping = list(set([id for items in overlapping for id in items]))

        # checks
        self.assertEqual(len(flat_overlapping), 18)
        flat_expected_overlaps.sort()
        flat_overlapping.sort()
        self.assertEqual(flat_expected_overlaps, flat_overlapping)

    def test_find_vertices(self):
        print('\nINFO: Validating search for missing vertices...')

        gpkg_path = get_test_copy_path('geopackage/topology_cases.gpkg')

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
            clone_polygons = self.qgis_utils.geometry.clone_layer(polygon_layer)

            geom_polygon = clone_polygons.getFeature(1).geometry()
            init_vertex_geom = [vertex for vertex in geom_polygon.vertices()]

            self.qgis_utils.geometry.add_topological_vertices(clone_polygons, lines_layer, self.names.T_ID_F)

            geom_polygon = clone_polygons.getFeature(1).geometry()
            adjusted_vertex_geom = [vertex for vertex in geom_polygon.vertices()]

            num_vertices_added = len(adjusted_vertex_geom) - len(init_vertex_geom)
            self.assertEqual(num_vertices_added, vertices_test_values[i])

    def test_polygons_must_be_covered_by_lines(self):
        print('\nINFO: Validating polygons must be covered by lines...')

        gpkg_path = get_test_copy_path('geopackage/topology_cases.gpkg')

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
            diff_plot_boundary = self.qgis_utils.geometry.difference_plot_boundary(polygon_as_lines_layer, lines_layer, 'fid')

            if diff_plot_boundary is not None:
                if len(diff_plot_boundary) > 0:
                    for element in range(len(diff_plot_boundary)):
                        self.assertIn(diff_plot_boundary[element]['geometry'].asWkt(), diff_geom[i], 'case_{}, element_{}'.format(i + 1, element))
                else: # Case 6
                    self.assertEqual('', diff_geom[i], 'case_{}'.format(i + 1))

    def test_lines_must_be_covered_by_polygons(self):
        print('\nINFO: Validating lines must be covered by polygons...')

        gpkg_path = get_test_copy_path('geopackage/topology_cases.gpkg')

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
            diff_boundary_plot = self.qgis_utils.geometry.difference_boundary_plot(lines_layer, polygon_as_lines_layer, 'fid')

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
        polygon_intersection = self.qgis_utils.geometry.get_intersection_polygons(polygons_intersection_layer,
                                                                                  polygon_id,
                                                                                  overlapping_id)
        self.assertEqual(polygon_intersection, None)

    def test_get_missing_boundary_points_in_boundaries(self):
        print('\nINFO: Validating missing boundary points in boundaries...')

        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        uri = gpkg_path + '|layername={layername}'.format(layername='boundary')
        boundary_layer = QgsVectorLayer(uri, 'boundary', 'ogr')
        uri = gpkg_path + '|layername={layername}'.format(layername='boundary_points_')
        point_layer = QgsVectorLayer(uri, 'boundary_points_', 'ogr')

        boundary_features = [feature for feature in boundary_layer.getFeatures()]
        self.assertEqual(len(boundary_features), 8)

        point_features = [feature for feature in point_layer.getFeatures()]
        self.assertEqual(len(point_features), 9)

        missing_points = self.quality.get_missing_boundary_points_in_boundaries(point_layer, boundary_layer)

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
        uri = gpkg_path + '|layername={layername}'.format(layername='boundary')
        boundary_layer = QgsVectorLayer(uri, 'boundary', 'ogr')
        point_layer = QgsVectorLayer("MultiPoint?crs={}".format(boundary_layer.sourceCrs().authid()), "Boundary points", "memory")

        boundary_features = [feature for feature in boundary_layer.getFeatures()]
        self.assertEqual(len(boundary_features), 8)

        point_features = [feature for feature in point_layer.getFeatures()]
        self.assertEqual(len(point_features), 0)

        missing_points = self.quality.get_missing_boundary_points_in_boundaries(point_layer, boundary_layer)

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
        uri = gpkg_path + '|layername={layername}'.format(layername='construccion')
        building_layer = QgsVectorLayer(uri, 'construccion', 'ogr')
        uril = gpkg_path + '|layername={layername}'.format(layername='p_levantamiento')
        survey_layer = QgsVectorLayer(uril, 'p_levantamiento', 'ogr')

        building_features = [feature for feature in building_layer.getFeatures()]
        self.assertEqual(len(building_features), 4)

        survey_features = [feature for feature in survey_layer.getFeatures()]
        self.assertEqual(len(survey_features), 11)

        missing_points = self.quality.get_missing_boundary_points_in_boundaries(survey_layer, building_layer)

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
        points_selected = self.qgis_utils.geometry.join_boundary_points_with_boundary_discard_nonmatching(boundary_points_layer, boundary_layer, self.names.T_ID_F)

        for point_selected in points_selected:
            boundary_point_id = point_selected[self.names.T_ID_F]
            boundary_id = point_selected['{}_2'.format(self.names.T_ID_F)]
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
        points_selected = self.qgis_utils.geometry.join_boundary_points_with_boundary_discard_nonmatching(boundary_points_layer, boundary_layer, self.names.T_ID_F)

        for point_selected in points_selected:
            boundary_point_id = point_selected[self.names.T_ID_F]
            boundary_id = point_selected['{}_2'.format(self.names.T_ID_F)]
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

        ids, over_pol = self.qgis_utils.geometry.get_inner_intersections_between_polygons(right_of_way_layer, building_layer)

        geometries = [v.asWkt() for v in over_pol.asGeometryCollection()]

        self.assertEqual(len(geometries), 4)

        self.assertIn('Polygon ((1091354.41819027159363031 1121694.23184006474912167, 1091354.2822037145961076 1121696.81558464490808547, 1091355.59206581697799265 1121695.52748471638187766, 1091354.41819027159363031 1121694.23184006474912167))', geometries)
        self.assertIn('Polygon ((1091254.39762192475609481 1121590.49773243162781, 1091250.73030774760991335 1121597.99486360652372241, 1091259.24529790692031384 1121594.80259312898851931, 1091254.39762192475609481 1121590.49773243162781))', geometries)
        self.assertIn('Polygon ((1091236.35652560647577047 1121774.96929413848556578, 1091240.31053024088032544 1121761.7039380690548569, 1091224.81715030129998922 1121764.51856614812277257, 1091236.35652560647577047 1121774.96929413848556578))', geometries)
        self.assertIn('Polygon ((1091210.77726722555235028 1121751.80323319789022207, 1091216.81715549202635884 1121740.58629784546792507, 1091200.99485773546621203 1121742.94371541915461421, 1091210.77726722555235028 1121751.80323319789022207))', geometries)

    def test_boundary_dangles(self):
        print('\nINFO: Validating boundary_dangles...')
        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        uri = gpkg_path + '|layername={layername}'.format(layername='test_boundaries_overlap')
        boundary_layer = QgsVectorLayer(uri, 'dangles', 'ogr')

        features = [feature for feature in boundary_layer.getFeatures()]
        self.assertEqual(len(features), 15)

        end_points, dangle_ids = self.quality.get_dangle_ids(boundary_layer)
        self.assertEqual(len(dangle_ids), 19)

        boundary_ids = [feature[self.names.T_ID_F] for feature in end_points.getFeatures(dangle_ids)]
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

        end_points, dangle_ids = self.quality.get_dangle_ids(boundary_layer)
        self.assertEqual(len(dangle_ids), 0)

    def test_boundaries_are_not_split(self):
        print('\nINFO: Validating boundaries are not split...')
        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        uri_bad_boundary = gpkg_path + '|layername={layername}'.format(layername='bad_boundary')
        uri_bbox_boundary = gpkg_path + '|layername={layername}'.format(layername='bbox_intersect_boundary')
        uri_good_boundary = gpkg_path + '|layername={layername}'.format(layername='good_boundary')
        bad_boundary_layer = QgsVectorLayer(uri_bad_boundary, 'bad_boundary', 'ogr')
        bbox_boundary_layer = QgsVectorLayer(uri_bbox_boundary, 'bbox_intersect_boundary', 'ogr')
        good_boundary_layer = QgsVectorLayer(uri_good_boundary, 'good_boundary', 'ogr')

        bad_boundary_errors = self.qgis_utils.geometry.get_boundaries_connected_to_single_boundary(bad_boundary_layer)
        bad_boundary_errors_list = [item for item in bad_boundary_errors]
        self.assertEqual(len(bad_boundary_errors_list), 4)
        self.assertEqual([2, 3, 6, 7], [f['t_id'] for f in bad_boundary_errors])

        bbox_boundary_errors = self.qgis_utils.geometry.get_boundaries_connected_to_single_boundary(bbox_boundary_layer)
        bbox_boundary_errors_list = [item for item in bbox_boundary_errors]
        self.assertEqual(len(bbox_boundary_errors_list), 9)
        self.assertEqual([39185, 39193, 39207, 39209, 39210, 39231, 39232, 48767, 48768], [f['t_id'] for f in bbox_boundary_errors_list])

        good_boundary_errors = self.qgis_utils.geometry.get_boundaries_connected_to_single_boundary(good_boundary_layer)
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
        gaps = self.qgis_utils.geometry.get_gaps_in_polygon_layer(test_plots_layer, include_roads=True)
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
        gaps = self.qgis_utils.geometry.get_gaps_in_polygon_layer(test_plots_layer, include_roads=True)
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
        gaps = self.qgis_utils.geometry.get_gaps_in_polygon_layer(test_plots_layer, include_roads=False)
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
        gaps = self.qgis_utils.geometry.get_gaps_in_polygon_layer(test_plots_layer, include_roads=False)
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
        gaps = self.qgis_utils.geometry.get_gaps_in_polygon_layer(test_plots_layer, include_roads=True)
        geometries = [g.asWkt() for g in gaps]
        self.assertEqual([], geometries)
        self.assertEqual(len(geometries), 0)

        test_plots_layer.rollBack()

        print('\nINFO: Validating Gaps in Plots without using roads for only one geometry...')
        test_plots_layer.startEditing()
        test_plots_layer.deleteFeature(1)
        test_plots_layer.deleteFeature(2)
        test_plots_layer.deleteFeature(3)
        gaps = self.qgis_utils.geometry.get_gaps_in_polygon_layer(test_plots_layer, include_roads=False)
        geometries = [g.asWkt() for g in gaps]
        self.assertEqual([], geometries)
        self.assertEqual(len(geometries), 0)

        test_plots_layer.rollBack()

        print('\nINFO: Validating Gaps in Plots using roads for two geometries...')
        test_plots_layer.startEditing()
        test_plots_layer.deleteFeature(1)
        test_plots_layer.deleteFeature(3)
        gaps = self.qgis_utils.geometry.get_gaps_in_polygon_layer(test_plots_layer, include_roads=True)
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
        gaps = self.qgis_utils.geometry.get_gaps_in_polygon_layer(test_plots_layer, include_roads=False)
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

        single_parts, single_ids = self.qgis_utils.geometry.get_multipart_geoms(right_of_way)
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

        buildings_with_no_plot, buildings_not_within_plot = self.qgis_utils.geometry.get_buildings_out_of_plots(
                    building_layer,
                    plot_layer,
                    "id")

        self.assertEqual(len(buildings_with_no_plot), 1)
        self.assertEqual(len(buildings_not_within_plot), 2)

        self.assertEqual(buildings_with_no_plot[0]["id"], 5)
        self.assertEqual(buildings_not_within_plot[0]["id"], 2)
        self.assertEqual(buildings_not_within_plot[1]["id"], 6)

        expected_geometry_no_plot = 'MultiPolygon (((-75.14985606919390193 9.50028842268738671, -75.14985606919390193 9.5006630929751168, -75.14922300560428425 9.50057265531945738, -75.14921008593918828 9.5001979850317273, -75.14985606919390193 9.50028842268738671)))'
        expected_geometries_not_within_plot = [
            'MultiPolygon (((-75.14258229774588926 9.49984915407418384, -75.14198799315154531 9.49982331474399544, -75.14192339482607963 9.49898353651287586, -75.14259521741097103 9.49881558086665123, -75.14258229774588926 9.49984915407418384)))',
            'MultiPolygon (((-75.1430372948142633 9.49682077975437977, -75.14242022761496287 9.4980865586247436, -75.14136013781103429 9.49713722447197028, -75.14083800402700319 9.49791251403006953, -75.1406639594323309 9.49691571316965621, -75.1430372948142633 9.49682077975437977)))']
        self.assertEqual(buildings_with_no_plot[0].geometry().asWkt(), expected_geometry_no_plot)
        self.assertEqual(buildings_not_within_plot[0].geometry().asWkt(), expected_geometries_not_within_plot[0])
        self.assertEqual(buildings_not_within_plot[1].geometry().asWkt(), expected_geometries_not_within_plot[1])

    def tearDownClass():
        print('tearDown test_boundaries_digitizing')


if __name__ == '__main__':
    nose2.main()
