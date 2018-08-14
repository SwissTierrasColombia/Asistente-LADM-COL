import nose2

from qgis.core import QgsVectorLayer, QgsApplication
from qgis.testing import unittest, start_app

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.config.table_mapping_config import ID_FIELD
from asistente_ladm_col.tests.utils import import_projectgenerator, get_test_copy_path
from asistente_ladm_col.utils.qgis_utils import QGISUtils
from asistente_ladm_col.utils.quality import QualityUtils

from processing.core.Processing import Processing
from qgis.analysis import QgsNativeAlgorithms
from qgis.core import QgsWkbTypes
import processing

import_projectgenerator()

class TesQualityValidations(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.qgis_utils = QGISUtils()
        self.quality = QualityUtils(self.qgis_utils)
        Processing.initialize()
        QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

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
        segments_info = self.quality.get_too_long_segments_from_simple_line(line, tolerance)
        self.assertEqual(len(segments_info), 2)
        self.validate_segments(segments_info, tolerance)

        line = lines.constGet().geometryN(1)
        segments_info = self.quality.get_too_long_segments_from_simple_line(line, tolerance)
        self.assertEqual(len(segments_info), 1)
        self.validate_segments(segments_info, tolerance)

        line = lines.constGet().geometryN(2)
        segments_info = self.quality.get_too_long_segments_from_simple_line(line, tolerance)
        self.assertEqual(len(segments_info), 0)
        self.validate_segments(segments_info, tolerance)

        line = lines.constGet().geometryN(3)
        segments_info = self.quality.get_too_long_segments_from_simple_line(line, tolerance)
        self.assertEqual(len(segments_info), 1)
        self.validate_segments(segments_info, tolerance)

        ### feature 2 ###
        feature = features[1]
        lines = feature.geometry()
        self.assertTrue(lines.isMultipart())
        self.assertEqual(lines.constGet().numGeometries(), 1)

        line = lines.constGet().geometryN(0)
        segments_info = self.quality.get_too_long_segments_from_simple_line(line, tolerance)
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
        print('\nINFO: Validating find missing vertices...')

        gpkg_path = get_test_copy_path('geopackage/topology_cases.gpkg')

        vertices_test_values = [2,2,2,6,4,0]

        for i in range(len(vertices_test_values)):
            case = "_case"+str(i+1)
            uri_polygon = gpkg_path + '|layername={layername}'.format(layername='polygon'+case)
            uri_lines = gpkg_path + '|layername={layername}'.format(layername='lines'+case)
            polygon_layer = QgsVectorLayer(uri_polygon, 'polygon_layer'+case, 'ogr')
            lines_layer = QgsVectorLayer(uri_lines, 'lines_layer'+case, 'ogr')
            vertices = self.qgis_utils.geometry.find_missing_vertices_polygon_line(polygon_layer, lines_layer)
            self.assertEqual(vertices.featureCount(), vertices_test_values[i])

    def test_position_vertices(self):
        print('\nINFO: validating the position of the vertices...')

        gpkg_path = get_test_copy_path('geopackage/topology_cases.gpkg')

        position_vertices = [[{'part': 0, 'ring': 1, 'vertex': 1}],
                             [{'part': 0, 'ring': 1, 'vertex': 4}],
                             [{'part': 1, 'ring': 1, 'vertex': 3}],
                             [{'part': 1, 'ring': 1, 'vertex': 4}],
                             [{'part': 2, 'ring': 1, 'vertex': 3}],
                             [{'part': 2, 'ring': 1, 'vertex': 4}]]

        uri_polygon = gpkg_path + '|layername={layername}'.format(layername='polygon_case4')
        uri_lines = gpkg_path + '|layername={layername}'.format(layername='lines_case4')
        polygon_layer = QgsVectorLayer(uri_polygon, 'polygon_layer_case4', 'ogr')
        lines_layer = QgsVectorLayer(uri_lines, 'lines_layer_case4', 'ogr')
        vertices = self.qgis_utils.geometry.find_missing_vertices_polygon_line(polygon_layer, lines_layer)
        polygonGeom = polygon_layer.getFeature(1).geometry()

        for vertice in vertices.getFeatures():
            position = self.qgis_utils.geometry.getVertexPositionGeom(polygonGeom, vertice.geometry())
            self.assertEqual(position in position_vertices, True)


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

    def validate_segments(self, segments_info, tolerance):
        for segment_info in segments_info:
            #print(segment_info[0].asWkt(), segment_info[1])
            self.assertEqual(segment_info[0].length(), segment_info[1])
            self.assertTrue(segment_info[1] >= tolerance)

    def tearDownClass():
        print('tearDown test_boundaries_digitizing')


if __name__ == '__main__':
    nose2.main()
