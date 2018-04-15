import qgis
import nose2
import psycopg2
import os

from sys import platform
from qgis.core import QgsVectorLayer, QgsWkbTypes
from qgis.testing import unittest, start_app

start_app() # need to start before asistente_ladm_col.tests.utils

#from asistente_ladm_col.gui.point_spa_uni_cadastre_wizard import PointsSpatialUnitCadastreWizard
from asistente_ladm_col.tests.utils import import_projectgenerator, get_test_path
from asistente_ladm_col.utils.qgis_utils import QGISUtils

import_projectgenerator()

class TesQualityValidations(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.qgis_utils = QGISUtils()

    def test_get_too_long_segments_from_simple_line(self):
        print('Validating too long segments')
        gpkg_path = get_test_path('geopackage/tests_data.gpkg')
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
        segments_info = self.qgis_utils.get_too_long_segments_from_simple_line(line, tolerance)
        self.assertEqual(len(segments_info), 2)
        self.validate_segments(segments_info, tolerance)

        line = lines.constGet().geometryN(1)
        segments_info = self.qgis_utils.get_too_long_segments_from_simple_line(line, tolerance)
        self.assertEqual(len(segments_info), 1)
        self.validate_segments(segments_info, tolerance)

        line = lines.constGet().geometryN(2)
        segments_info = self.qgis_utils.get_too_long_segments_from_simple_line(line, tolerance)
        self.assertEqual(len(segments_info), 0)
        self.validate_segments(segments_info, tolerance)

        line = lines.constGet().geometryN(3)
        segments_info = self.qgis_utils.get_too_long_segments_from_simple_line(line, tolerance)
        self.assertEqual(len(segments_info), 1)
        self.validate_segments(segments_info, tolerance)

        ### feature 2 ###
        feature = features[1]
        lines = feature.geometry()
        self.assertTrue(lines.isMultipart())
        self.assertEqual(lines.constGet().numGeometries(), 1)

        line = lines.constGet().geometryN(0)
        segments_info = self.qgis_utils.get_too_long_segments_from_simple_line(line, tolerance)
        self.assertEqual(len(segments_info), 1)
        self.validate_segments(segments_info, tolerance)

    def test_get_overlapping_lines(self):
        print('Validating overlaps in boundary face strings')
        gpkg_path = get_test_path('geopackage/tests_data.gpkg')
        uri = gpkg_path + '|layername={layername}'.format(layername='test_boundaries_overlap')
        boundary_overlap_layer = QgsVectorLayer(uri, 'test_boundaries_overlap', 'ogr')

        features = [feature for feature in boundary_overlap_layer.getFeatures()]
        self.assertEqual(len(features), 12)

        overlapping = self.qgis_utils.get_overlapping_lines((boundary_overlap_layer))

        line_overlap = dict()
        point_overlap = dict()

        for pair, geometry in overlapping.items():
            print(pair, geometry.asWkt())
            if geometry.type() == QgsWkbTypes.PointGeometry:
                point_overlap[pair] = geometry.asWkt()
            elif geometry.type() == QgsWkbTypes.LineGeometry:
                line_overlap[pair] = geometry.asWkt()
            elif geometry.wkbType() == QgsWkbTypes.GeometryCollection:
                overlaps = geometry.asGeometryCollection()
                print(overlaps)
                for o in overlaps:
                    if o.type() == QgsWkbTypes.PointGeometry:
                        point_overlap[pair] = o.asWkt()
                    elif o.type() == QgsWkbTypes.LineGeometry:
                        line_overlap[pair] = o.asWkt()

        ### lines ###
        expected_line_overlap = {'4-6': 'MultiLineString ((963980.77503829856868833 1077802.31638198206201196, 963926.86899802810512483 1077925.5301883143838495))', '10-12': 'MultiLineString ((963643.395574557245709 1077747.43814651435241103, 963543.5341855603037402 1077760.18016819190233946))', '1-6': 'MultiLineString ((963905.69162506482098252 1077713.75645868084393442, 964144.41837483353447169 1077577.06614228105172515),(964144.41837483353447169 1077577.06614228105172515, 964309.98692709254100919 1077617.49567248369567096))'}
        self.assertEqual(line_overlap, expected_line_overlap)

        ### points ###
        expected_point_overlap = {'3-10': 'MultiPoint ((963643.395574557245709 1077747.43814651435241103))', '5-6': 'MultiPoint ((963850.90352329798042774 1077652.23999353917315602),(963880.39959512907080352 1077685.35838998109102249))', '4-6': 'MultiPoint ((964081.01700186752714217 1077722.2743631626944989),(964211.2347710223402828 1077618.29701916221529245))', '1-8': 'MultiPoint ((963750.28136727144010365 1077824.19025488453917205))', '6-11': 'MultiPoint ((964079.46952913235872984 1077829.37777462997473776))', '4-7': 'MultiPoint ((963849.37875852338038385 1077949.20776149653829634))', '3-9': 'MultiPoint ((963662.21440408274065703 1077708.90435272408649325))'}
        self.assertEqual(point_overlap, expected_point_overlap)

    def validate_segments(self, segments_info, tolerance):
        for segment_info in segments_info:
            #print(segment_info[0].asWkt(), segment_info[1])
            self.assertEqual(segment_info[0].length(), segment_info[1])
            self.assertTrue(segment_info[1] >= tolerance)

    def tearDownClass():
        print('tearDown test_boundaries_digitizing')


if __name__ == '__main__':
    nose2.main()
