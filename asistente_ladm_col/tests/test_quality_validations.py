import nose2

from qgis.core import (
    QgsVectorLayer,
    QgsApplication,
    QgsDataSourceUri,
    QgsField,
    QgsWkbTypes
)
from qgis.PyQt.QtCore import QVariant
from processing.core.Processing import Processing
from qgis.analysis import QgsNativeAlgorithms
from qgis.testing import unittest, start_app

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.config.general_config import QGIS_LANG
from asistente_ladm_col.config.table_mapping_config import ID_FIELD
from asistente_ladm_col.tests.utils import import_projectgenerator, get_test_copy_path, get_dbconn, restore_schema
from asistente_ladm_col.utils.qgis_utils import QGISUtils
from asistente_ladm_col.utils.quality import QualityUtils

import processing

import_projectgenerator()

class TesQualityValidations(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.qgis_utils = QGISUtils()
        self.quality = QualityUtils(self.qgis_utils)
        Processing.initialize()
        QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

        # Test connection DB
        self.db_connection = get_dbconn('test_ladm_col_topology')
        result = self.db_connection.test_connection()
        print('test_connection', result)
        if not result[1]:
            print('The test connection is not working')
            return
        restore_schema('test_ladm_col_topology')

    def test_topology_plot_must_be_covered_by_boundary(self):

        DB_HOSTNAME = "postgres"
        DB_PORT = "5432"
        DB_NAME = "ladm_col"
        DB_USER = "usuario_ladm_col"
        DB_PASSWORD = "clave_ladm_col"
        SCHEMA_NAME = 'test_ladm_col_topology'

        # Read data
        uri = QgsDataSourceUri()
        uri.setConnection(DB_HOSTNAME, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
        uri.setDataSource(SCHEMA_NAME, 'lindero', "geometria", "", "gid")
        boundary_layer = QgsVectorLayer(uri.uri(), 'lindero', "postgres")
        self.assertEqual(boundary_layer.featureCount(), 1619)

        uri = QgsDataSourceUri()
        uri.setConnection(DB_HOSTNAME, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
        uri.setDataSource(SCHEMA_NAME, 'terreno', "poligono_creado", "", "gid")
        plot_layer = QgsVectorLayer(uri.uri(), 'terreno', "postgres")
        self.assertEqual(plot_layer.featureCount(), 441)

        uri = QgsDataSourceUri()
        uri.setConnection(DB_HOSTNAME, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
        uri.setDataSource(SCHEMA_NAME, 'masccl', None, "", None)
        more_bfs_layer = QgsVectorLayer(uri.uri(), 'masccl', "postgres")
        self.assertEqual(more_bfs_layer.featureCount(), 3186)

        uri = QgsDataSourceUri()
        uri.setConnection(DB_HOSTNAME, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
        uri.setDataSource(SCHEMA_NAME, 'menos', None, "", None)
        less_layer = QgsVectorLayer(uri.uri(), 'less', "postgres")
        self.assertEqual(less_layer.featureCount(), 180)

        error_layer = QgsVectorLayer("MultiLineString?crs=EPSG:3116", 'error layer', "memory")

        data_provider = error_layer.dataProvider()
        data_provider.addAttributes([QgsField('plot_id', QVariant.Int),
                                     QgsField('boundary_id', QVariant.Int),
                                     QgsField('error_type', QVariant.String)])
        error_layer.updateFields()

        features = self.quality.get_features_plots_covered_by_boundaries(plot_layer, boundary_layer, more_bfs_layer, less_layer, error_layer)

        # this error can occur because an error occurred when executing the algorithm
        self.assertNotEqual(features, None)

        # the algorithm was successfully executed
        self.assertEqual(len(features), 45)

        error_layer.dataProvider().addFeatures(features)

        if QGIS_LANG == 'es':
            exp = "\"error_type\" = 'El terreno no esta cubierto por el lindero'"
            error_layer.selectByExpression(exp)
            self.assertEqual(error_layer.selectedFeatureCount(), 19)

            exp = "\"error_type\" = 'La relación topológica entre el lindero y el terreno no esta registrada en la tabla masccl'"
            error_layer.selectByExpression(exp)
            self.assertEqual(error_layer.selectedFeatureCount(), 24)

            exp = "\"error_type\" = 'La relación topológica entre el lindero y el terreno no esta registrada en la tabla menos'"
            error_layer.selectByExpression(exp)
            self.assertEqual(error_layer.selectedFeatureCount(), 2)

        elif QGIS_LANG == 'en':
            exp = "\"error_type\" = 'Plot is not covered by the boundary'"
            error_layer.selectByExpression(exp)
            self.assertEqual(error_layer.selectedFeatureCount(), 19)

            exp = "\"error_type\" = 'Topological relationship between boundary and plot not recorded in the table masccl'"
            error_layer.selectByExpression(exp)
            self.assertEqual(error_layer.selectedFeatureCount(), 24)

            exp = "\"error_type\" = 'Topological relationship between boundary and plot not recorded in the table menos'"
            error_layer.selectByExpression(exp)
            self.assertEqual(error_layer.selectedFeatureCount(), 2)

        else:
            print('the language is not supported, the tests are not executed')

    def test_topology_boundary_must_be_covered_by_plot(self):

        DB_HOSTNAME = "postgres"
        DB_PORT = "5432"
        DB_NAME = "ladm_col"
        DB_USER = "usuario_ladm_col"
        DB_PASSWORD = "clave_ladm_col"
        SCHEMA_NAME = 'test_ladm_col_topology'

        # Read data
        uri = QgsDataSourceUri()
        uri.setConnection(DB_HOSTNAME, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
        uri.setDataSource(SCHEMA_NAME, 'lindero', "geometria", "", "gid")
        boundary_layer = QgsVectorLayer(uri.uri(), 'lindero', "postgres")
        self.assertEqual(boundary_layer.featureCount(), 1619)

        uri = QgsDataSourceUri()
        uri.setConnection(DB_HOSTNAME, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
        uri.setDataSource(SCHEMA_NAME, 'terreno', "poligono_creado", "", "gid")
        plot_layer = QgsVectorLayer(uri.uri(), 'terreno', "postgres")
        self.assertEqual(plot_layer.featureCount(), 441)

        uri = QgsDataSourceUri()
        uri.setConnection(DB_HOSTNAME, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
        uri.setDataSource(SCHEMA_NAME, 'masccl', None, "", None)
        more_bfs_layer = QgsVectorLayer(uri.uri(), 'masccl', "postgres")
        self.assertEqual(more_bfs_layer.featureCount(), 3186)

        uri = QgsDataSourceUri()
        uri.setConnection(DB_HOSTNAME, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
        uri.setDataSource(SCHEMA_NAME, 'menos', None, "", None)
        less_layer = QgsVectorLayer(uri.uri(), 'less', "postgres")
        self.assertEqual(less_layer.featureCount(), 180)

        error_layer = QgsVectorLayer("MultiLineString?crs=EPSG:3116", 'error layer', "memory")

        data_provider = error_layer.dataProvider()
        data_provider.addAttributes([QgsField('plot_id', QVariant.Int),
                                     QgsField('boundary_id', QVariant.Int),
                                     QgsField('error_type', QVariant.String)])
        error_layer.updateFields()

        features = self.quality.get_features_boundaries_covered_by_plots(plot_layer, boundary_layer, more_bfs_layer, less_layer, error_layer)

        # this error can occur because an error occurred when executing the algorithm
        self.assertNotEqual(features, None)

        # the algorithm was successfully executed
        self.assertEqual(len(features), 29)

        error_layer.dataProvider().addFeatures(features)


        if QGIS_LANG == 'es':
            exp = "\"error_type\" = 'El lindero no esta cubierta por el terreno'"
            error_layer.selectByExpression(exp)
            self.assertEqual(error_layer.selectedFeatureCount(), 3)

            exp = "\"error_type\" = 'La relación topológica entre el lindero y el terreno no esta registrada en la tabla masccl'"
            error_layer.selectByExpression(exp)
            self.assertEqual(error_layer.selectedFeatureCount(), 24)

            exp = "\"error_type\" = 'La relación topológica entre el lindero y el terreno no esta registrada en la tabla menos'"
            error_layer.selectByExpression(exp)
            self.assertEqual(error_layer.selectedFeatureCount(), 2)
        elif QGIS_LANG == 'en':
            exp = "\"error_type\" = 'Boundary is not covered by the plot'"
            error_layer.selectByExpression(exp)
            self.assertEqual(error_layer.selectedFeatureCount(), 3)

            exp = "\"error_type\" = 'Topological relationship between boundary and plot not recorded in the table masccl'"
            error_layer.selectByExpression(exp)
            self.assertEqual(error_layer.selectedFeatureCount(), 24)

            exp = "\"error_type\" = 'Topological relationship between boundary and plot not recorded in the table menos'"
            error_layer.selectByExpression(exp)
            self.assertEqual(error_layer.selectedFeatureCount(), 2)
        else:
            print('the language is not supported, the tests are not executed fully')

    def test_get_too_long_segments_from_simple_line(self):
        print('\nINFO: Validating too long segments...')
        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        uri = gpkg_path + '|layername={layername}'.format(layername='too_long_lines')
        boundary_layer = QgsVectorLayer(uri, 'too_long_lines', 'ogr')

        tolerance = 200 # meters

        features = [feature for feature in boundary_layer.getFeatures()]
        self.assertEqual(len(features), 2)

        ### feature 1 ###
        feature = features[0]
        lines = feature.geometry()
        self.assertTrue(lines.isMultipart())
        self.assertEqual(lines.constGet().numGeometries(), 4)

        line = lines.constGet().geometryN(0)
        segments_info = self.qgis_utils.geometry.get_too_long_segments_from_simple_line(line, tolerance)
        self.assertEqual(len(segments_info), 2)
        self.validate_segments(segments_info, tolerance)

        line = lines.constGet().geometryN(1)
        segments_info = self.qgis_utils.geometry.get_too_long_segments_from_simple_line(line, tolerance)
        self.assertEqual(len(segments_info), 1)
        self.validate_segments(segments_info, tolerance)

        line = lines.constGet().geometryN(2)
        segments_info = self.qgis_utils.geometry.get_too_long_segments_from_simple_line(line, tolerance)
        self.assertEqual(len(segments_info), 0)
        self.validate_segments(segments_info, tolerance)

        line = lines.constGet().geometryN(3)
        segments_info = self.qgis_utils.geometry.get_too_long_segments_from_simple_line(line, tolerance)
        self.assertEqual(len(segments_info), 1)
        self.validate_segments(segments_info, tolerance)

        ### feature 2 ###
        feature = features[1]
        lines = feature.geometry()
        self.assertTrue(lines.isMultipart())
        self.assertEqual(lines.constGet().numGeometries(), 1)

        line = lines.constGet().geometryN(0)
        segments_info = self.qgis_utils.geometry.get_too_long_segments_from_simple_line(line, tolerance)
        self.assertEqual(len(segments_info), 1)
        self.validate_segments(segments_info, tolerance)

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
            insert_into_res([point[ID_FIELD], point[ID_FIELD+'_2']], point.geometry().asWkt())

        for line in line_features:
            insert_into_res([line[ID_FIELD], line[ID_FIELD+'_2']], line.geometry().asWkt())

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

            self.qgis_utils.geometry.add_topological_vertices(clone_polygons, lines_layer)

            geom_polygon = clone_polygons.getFeature(1).geometry()
            adjusted_vertex_geom = [vertex for vertex in geom_polygon.vertices()]

            num_vertices_added = len(adjusted_vertex_geom) - len(init_vertex_geom)
            self.assertEqual(num_vertices_added, vertices_test_values[i])

    def test_polygons_must_be_covered_by_lines(self):
        print('\nINFO: Validating polygons must be covered by lines...')

        gpkg_path = get_test_copy_path('geopackage/topology_cases.gpkg')

        diff_geom = ['MultiLineString ((780300.30731518880929798 1225605.22174088703468442, 780297.95234157983213663 1225599.8581298291683197, 780292.44514157995581627 1225602.31722982972860336, 780294.34505024075042456 1225606.57437412883155048))',
                     'MultiLineString ((780300.30731518880929798 1225605.22174088703468442, 780297.95234157983213663 1225599.8581298291683197, 780292.44514157995581627 1225602.31722982972860336, 780294.34505024075042456 1225606.57437412883155048))',
                     'MultiLineString ((780309.73902403307147324 1225602.49830744392238557, 780308.30989155941642821 1225603.05408118362538517, 780307.64825615496374667 1225603.95390533376485109),(780310.01870060083456337 1225599.16431454825215042, 780310.03014361101668328 1225598.66082209814339876, 780311.16639214521273971 1225598.61655267467722297))',
                     'MultiLineString ((780307.7805832359008491 1225598.39616793626919389, 780307.60049424471799284 1225599.58559290133416653),(780308.69099051796365529 1225598.27522822353057563, 780307.7805832359008491 1225598.39616793626919389),(780315.57867445563897491 1225608.45340170268900692, 780315.45555392769165337 1225607.63259818265214562, 780314.78905752801802009 1225607.92419035756029189),(780317.62428020488005131 1225603.16991792898625135, 780318.36674970726016909 1225602.84235785435885191, 780318.29131162946578115 1225603.45340628433041275))',
                     'MultiLineString ((780306.77080396702513099 1225605.06540775927715003, 780306.64257034030742943 1225605.91234613093547523, 780307.906158416881226 1225605.63026071945205331),(780314.52926436136476696 1225599.74590416136197746, 780312.94133939070161432 1225600.03702373942360282, 780312.34155925654340535 1225600.40004855743609369),(780312.43979134678374976 1225599.65884278574958444, 780314.52926436136476696 1225599.74590416136197746),(780318.10209554550237954 1225604.98605656484141946, 780317.2287368115503341 1225605.14484906173311174, 780316.19658558059018105 1225606.12406946043483913))',
                     '']

        for i in range(len(diff_geom)):
            uri_polygon = gpkg_path + '|layername={layername}_case{case}'.format(
                layername='polygon', case=i+1)
            uri_lines = gpkg_path + '|layername={layername}_case{case}'.format(
                layername='lines', case=i+1)
            polygon_layer = QgsVectorLayer(uri_polygon, 'polygon_layer_{}'.format(i+1), 'ogr')
            lines_layer = QgsVectorLayer(uri_lines, 'lines_layer_{}'.format(i+1), 'ogr')

            polygon_as_lines_layer = processing.run("qgis:polygonstolines", {'INPUT': polygon_layer, 'OUTPUT': 'memory:'})['OUTPUT']
            diff_plot_boundary = self.qgis_utils.geometry.difference_plot_boundary(polygon_as_lines_layer, lines_layer, 'fid')

            if diff_plot_boundary is not None:
                if len(diff_plot_boundary) > 0:
                    self.assertEqual(diff_plot_boundary[0]['geometry'].asWkt(), diff_geom[i], 'case_{}'.format(i + 1))
                else:
                    self.assertEqual('', diff_geom[i], 'case_{}'.format(i + 1))

    def test_lines_must_be_covered_by_polygons(self):
        print('\nINFO: Validating lines must be covered by polygons...')

        gpkg_path = get_test_copy_path('geopackage/topology_cases.gpkg')

        diff_geom = ['',
                     '',
                     'MultiLineString ((780309.73902403307147324 1225602.49830744392238557, 780307.83351406815927476 1225602.05170354596339166, 780307.64825615496374667 1225603.95390533376485109))',
                     '',
                     'MultiLineString ((780318.10209554550237954 1225604.98605656484141946, 780317.50662368256598711 1225605.92888701660558581, 780316.19658558059018105 1225606.12406946043483913))',
                     'MultiLineString ((780314.52926436136476696 1225599.74590416136197746, 780312.94133939070161432 1225600.03702373942360282, 780310.92996776115614921 1225601.25443288357928395, 780310.00367819482926279 1225599.82530040992423892, 780310.03014361101668328 1225598.66082209814339876, 780312.06798065674956888 1225598.5814258495811373, 780311.35341442003846169 1225599.61357708042487502, 780314.52926436136476696 1225599.74590416136197746))']

        for i in range(len(diff_geom)):
            uri_polygon = gpkg_path + '|layername={layername}_case{case}'.format(layername='polygon', case=i+1)
            uri_lines = gpkg_path + '|layername={layername}_case{case}'.format(layername='lines', case=i+1)
            polygon_layer = QgsVectorLayer(uri_polygon, 'polygon_layer_{}'.format(i+1), 'ogr')
            lines_layer = QgsVectorLayer(uri_lines, 'lines_layer_{}'.format(i+1), 'ogr')

            polygon_as_lines_layer = processing.run("qgis:polygonstolines", {'INPUT': polygon_layer, 'OUTPUT': 'memory:'})['OUTPUT']
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

    def test_find_boundary_points_not_covered_by_boundaries(self):
        print('\nINFO: Validating boundary points not covered by boundaries...')

        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        uri_boundary = gpkg_path + '|layername={layername}'.format(layername='boundary_lamd')
        uri_point_boundary = gpkg_path + '|layername={layername}'.format(layername='point_boundary_ladm')
        uri_point_boundary_fixed = gpkg_path + '|layername={layername}'.format(layername='point_boundary_ladm_fixed')

        boundary_layer = QgsVectorLayer(uri_boundary, 'boundary', 'ogr')
        point_boundary_layer = QgsVectorLayer(uri_point_boundary, 'point_boundary', 'ogr')
        point_boundary_fixed_layer = QgsVectorLayer(uri_point_boundary_fixed, 'point_boundary', 'ogr')

        boundary_points = self.qgis_utils.geometry.get_boundary_points_not_covered_by_boundary_nodes(point_boundary_layer, boundary_layer)
        self.assertEqual(len(boundary_points), 8)

        boundary_points = self.qgis_utils.geometry.get_boundary_points_not_covered_by_boundary_nodes(point_boundary_fixed_layer, boundary_layer)
        self.assertEqual(len(boundary_points), 0)

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
        point_layer = QgsVectorLayer("MultiPoint?crs=EPSG:{}".format(3116), "Boundary points", "memory")

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
        points_selected = self.qgis_utils.geometry.join_boundary_points_with_boundary_discard_nonmatching(boundary_points_layer, boundary_layer)

        for point_selected in points_selected:
            boundary_point_id = point_selected[ID_FIELD]
            boundary_id = point_selected['{}_2'.format(ID_FIELD)]
            key_query = "{}-{}".format(boundary_point_id, boundary_id)

            if key_query in dic_points_ccl:
                if dic_points_ccl[key_query] > 1:
                    duplicates_topology.append([boundary_point_id, boundary_id])
            else:
                missing_topology.append([boundary_point_id, boundary_id])

        self.assertEquals(len(missing_topology), 0)
        self.assertEquals(len(duplicates_topology), 0)

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
        points_selected = self.qgis_utils.geometry.join_boundary_points_with_boundary_discard_nonmatching(boundary_points_layer, boundary_layer)

        for point_selected in points_selected:
            boundary_point_id = point_selected[ID_FIELD]
            boundary_id = point_selected['{}_2'.format(ID_FIELD)]
            key_query = "{}-{}".format(boundary_point_id, boundary_id)

            if key_query in dic_points_ccl:
                if dic_points_ccl[key_query] > 1: # register more that once
                    duplicates_topology.append([boundary_point_id, boundary_id])
            else: # no register
                missing_topology.append([boundary_point_id, boundary_id])

        self.assertEquals(missing_topology, [[1, 1]])
        self.assertEquals(duplicates_topology, [[20, 1]])

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

        boundary_ids = [feature[ID_FIELD] for feature in end_points.getFeatures(dangle_ids)]
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
        self.assertEquals(len(bad_boundary_errors_list), 4)

        bbox_boundary_errors = self.qgis_utils.geometry.get_boundaries_connected_to_single_boundary(bbox_boundary_layer)
        bbox_boundary_errors_list = [item for item in bbox_boundary_errors]
        self.assertEquals(len(bbox_boundary_errors_list), 9)

        good_boundary_errors = self.qgis_utils.geometry.get_boundaries_connected_to_single_boundary(good_boundary_layer)
        good_boundary_errors_list = [item for item in good_boundary_errors]
        self.assertEquals(len(good_boundary_errors_list), 0)

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

    def tearDownClass():
        print('tearDown test_boundaries_digitizing')


if __name__ == '__main__':
    nose2.main()
