import nose2

from qgis.core import (QgsVectorLayer,
                       QgsWkbTypes,
                       QgsGeometry)
from qgis.testing import (unittest,
                          start_app)

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.lib.geometry import GeometryUtils

start_app()  # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (import_qgis_model_baker,
                                            import_processing,
                                            get_test_copy_path,
                                            get_pg_conn,
                                            get_gpkg_conn,
                                            restore_schema,
                                            unload_qgis_model_baker)

import_processing()
import processing


class TestGeometryUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import_qgis_model_baker()
        cls.app = AppInterface()
        cls.geometry = GeometryUtils()

    def test_check_build_boundaries(self):
        print('\nINFO: Validation of the definition of boundaries...')

        gpkg_path = get_test_copy_path('db/static/gpkg/adjust_boundaries_cases.gpkg')
        self.db_gpkg = get_gpkg_conn('adjust_boundaries_cases_gpkg')
        names = self.db_gpkg.names
        names.T_ID_F = 't_id'  # Static label is set because the database does not have the ladm structure

        test_results = {
            'boundary_case_1': ['LineString (882256.9922020563390106 1545352.94816972548142076, 883830.40917081397492439 1545368.68233941309154034, 885435.29447894683107734 1545352.94816972548142076, 887291.92650208086706698 1545337.21400003810413182, 888881.07764052611310035 1545463.08735753851942718)'],
            'boundary_case_2': ['LineString (882325.469107756158337 1544955.88267589989118278, 883209.64509183121845126 1544960.13352197711355984, 884510.40399148012511432 1544985.6385984409134835, 885547.61043433740269393 1544964.3843680543359369, 886822.86425752262584865 1544977.13690628623589873, 887889.82662292092572898 1544989.88944451813586056, 888612.47045605920720845 1545002.64198275003582239)'],
            'boundary_case_3': ['LineString (886476.29300758719909936 1544161.06105313077569008, 882415.14798706094734371 1544041.61561135039664805, 882407.18495760892983526 1541724.37404081481508911, 887200.92868772032670677 1541764.18918807501904666)', 'LineString (886476.29300758719909936 1544161.06105313077569008, 889390.76178702362813056 1543165.68237162916921079, 887200.92868772032670677 1541764.18918807501904666)', 'LineString (887200.92868772032670677 1541764.18918807501904666, 886476.29300758719909936 1544161.06105313077569008)'],
            'boundary_case_4': ['LineString (886476.29300758719909936 1544161.06105313077569008, 882415.14798706094734371 1544041.61561135039664805, 882407.18495760892983526 1541724.37404081481508911, 887200.92868772032670677 1541764.18918807501904666)', 'LineString (886476.29300758719909936 1544161.06105313077569008, 889390.76178702362813056 1543165.68237162916921079, 887894.38694565510377288 1542208.00247315340675414, 887200.92868772032670677 1541764.18918807501904666)', 'LineString (886476.29300758719909936 1544161.06105313077569008, 887200.92868772032670677 1541764.18918807501904666)'],
            'boundary_case_5': ['LineString (882709.45987063564825803 1543510.21952517866156995, 882696.0032627055188641 1542761.13501706859096885, 883485.45759460597764701 1543057.18039153120480478, 882709.45987063564825803 1543510.21952517866156995)', 'LineString (883485.45759460597764701 1543057.18039153120480478, 884898.40142726874910295 1543084.09360739146359265)', 'LineString (884898.40142726874910295 1543084.09360739146359265, 885629.54379147209692746 1543640.30006850324571133, 885719.25451100617647171 1542711.79412132478319108, 884898.40142726874910295 1543084.09360739146359265)'],
            'boundary_case_6': ['LineString (882696.91113005892839283 1543128.55981796747073531, 883485.45759460597764701 1543057.18039153120480478, 884898.40142726874910295 1543084.09360739146359265)', 'LineString (884898.40142726874910295 1543084.09360739146359265, 885629.54379147209692746 1543640.30006850324571133)', 'LineString (884898.40142726874910295 1543084.09360739146359265, 885719.25451100617647171 1542711.79412132478319108)'],
            'boundary_case_7': ['LineString (882376.98617732501588762 1543885.65919923176988959, 881339.55751997174229473 1543276.52677656547166407, 882234.22076576261315495 1542448.48738950374536216)', 'LineString (883128.88401155360043049 1543847.58842281508259475, 883994.99417503213044256 1543247.9736942530144006, 883043.22476461622864008 1542438.96969539951533079)'],
            'boundary_case_8': ['LineString (895937.47771990788169205 1543691.07968750013969839, 895937.47771990788169205 1543987.82934027793817222, 896479.9233217597939074 1543987.82934027793817222, 896479.9233217597939074 1543691.07968750013969839, 895937.47771990788169205 1543691.07968750013969839)'],
            'boundary_case_9': ['LineString (895922.15344387735240161 1545423.63106414745561779, 895823.74850363796576858 1545312.72245558886788785, 895753.01430986321065575 1545231.0768567833583802, 895752.70520490442868322 1545118.35534420749172568, 895755.45756576466374099 1545004.08130264561623335, 895750.58388843457214534 1544903.72545119561254978, 895751.76962125208228827 1544777.10258481604978442, 895944.93307849601842463 1544785.83842549938708544)', 'LineString (895944.93307849601842463 1544785.83842549938708544, 896159.51394954684656113 1544779.07535220449790359, 896159.22516733291558921 1545234.59747773432172835, 896065.97630945523269475 1545327.50076097156852484, 895922.15344387735240161 1545423.63106414745561779)', 'LineString (895922.15344387735240161 1545423.63106414745561779, 895944.93307849601842463 1544785.83842549938708544)']
        }

        for case in test_results:
            uri = gpkg_path + '|layername={}'.format(case)
            boundary_layer = QgsVectorLayer(uri, '{}'.format(case), 'ogr')
            params = {'boundaries': boundary_layer, 'native:multiparttosingleparts_1:built_boundaries': 'TEMPORARY_OUTPUT'}
            built_boundaries_layer = processing.run("model:Build_Boundaries", params)['native:multiparttosingleparts_1:built_boundaries']
            boundaries_geom = [f.geometry() for f in built_boundaries_layer.getFeatures()]

            self.assertEqual(built_boundaries_layer.featureCount(), len(test_results[case]), 'Invalid number of features: case {}'.format(case))

            for boundary_geom in boundaries_geom:
                found = False
                for wkt_geom in test_results[case]:
                    geom = QgsGeometry.fromWkt(wkt_geom)
                    # geometries are compared using symDifference because they may be the same but digitized in a different way
                    if boundary_geom.symDifference(geom).isEmpty():
                        found = True
                        break
                self.assertTrue(found,'The geometries are invalid: case {case}. Geometry in WKT: {geometry}'.format(case=case, geometry=boundary_geom.asWkt()))

    def test_overlapping_points(self):
        print('\nINFO: Validating overlaps in points...')
        test_layer = 'overlapping_points'
        gpkg_path = get_test_copy_path('db/static/gpkg/geometry_utils.gpkg')
        uri = gpkg_path + '|layername={}'.format(test_layer)
        overlapping_points_layer = QgsVectorLayer(uri, 'test_overlapping_points', 'ogr')
        self.assertEqual(overlapping_points_layer.featureCount(), 286, 'The number of features differs')

        expected_overlaps = {
            '286, 285': 'Point (963166.65579999983310699 1077249.80199999921023846)'
        }

        overlapping = self.geometry.get_overlapping_points(overlapping_points_layer)
        self.assertTrue(len(overlapping), 1)  # One list of overlapping ids

        for overlapping_ids in overlapping:
            self.assertTrue(len(overlapping_ids), 2)  # Two points overlap
            points = []

            for feature in overlapping_points_layer.getFeatures(overlapping_ids):
                points.append(feature.geometry().asWkt())

            unique_points = set(points)  # get unique values
            self.assertEqual(len(unique_points), 1, 'The intersection failed, points are not equal')
            self.assertEqual(list(unique_points)[0], list(expected_overlaps.values())[0])

    def test_get_overlapping_lines(self):
        print('\nINFO: Validating overlaps in boundaries...')
        gpkg_path = get_test_copy_path('db/static/gpkg/geometry_utils.gpkg')
        self.db_gpkg = get_gpkg_conn('tests_geometry_util_gpkg')
        names = self.db_gpkg.names
        names.T_ID_F = 't_id'  # Static label is set because the database does not have the ladm structure

        uri = gpkg_path + '|layername={layername}'.format(layername='overlapping_lines')
        boundary_overlap_layer = QgsVectorLayer(uri, 'test_overlapping_lines', 'ogr')
        self.assertEqual(boundary_overlap_layer.featureCount(), 15)

        overlapping_lines = self.geometry.get_overlapping_lines(boundary_overlap_layer)
        self.assertNotEqual(overlapping_lines, dict())

        error_line_layer = overlapping_lines['native:extractbyexpression_3:Intersected_Lines']
        error_point_layer = overlapping_lines['native:deleteduplicategeometries_1:Intersected_Points']

        self.assertEqual(error_point_layer.featureCount(), 20)  # 20: len(expected_point_overlaps)
        self.assertEqual(error_line_layer.featureCount(), 5)

        point_features = error_point_layer.getFeatures()
        line_features = error_line_layer.getFeatures()

        # First, check point overlaps
        # For point overlaps, we don't rely on t_id pairs, because duplicated geometries are removed randomly,
        # therefore we are only interested in geometries (as WKTs).
        expected_point_overlaps = ['Point (963384.55712854664307088 1077823.99900980317033827)',
                                   'Point (963750.28136727144010365 1077824.19025488453917205)',
                                   'Point (963662.21440408274065703 1077708.90435272408649325)',
                                   'Point (963849.37875852338038385 1077949.20776149653829634)',
                                   'Point (964211.2347710223402828 1077618.29701916221529245)',
                                   'Point (963651.61653553508222103 1077966.0537187303416431)',
                                   'Point (964079.46952913235872984 1077829.37777462997473776)',
                                   'Point (964309.98692709254100919 1077617.49567248369567096)',
                                   'Point (964144.41837483353447169 1077577.06614228105172515)',
                                   'Point (963905.69162506482098252 1077713.75645868084393442)',
                                   'Point (963850.90352329798042774 1077652.23999353917315602)',
                                   'Point (964081.01700186752714217 1077722.2743631626944989)',
                                   'Point (963880.39959512907080352 1077685.35838998109102249)',
                                   'Point (963801.72997597197536379 1077798.46595053421333432)',
                                   'Point (963255.32157539459876716 1077724.74916282831691206)',
                                   'Point (964213.72614089539274573 1077962.10928706941194832)',
                                   'Point (963759.37523004529066384 1078021.79097451153211296)',
                                   'Point (963643.395574557245709 1077747.43814651435241103)',
                                   'Point (963926.86899802810512483 1077925.5301883143838495)',
                                   'Point (963980.77503829856868833 1077802.31638198206201196)']
        for point in point_features:
            self.assertIn(point.geometry().asWkt(), expected_point_overlaps)

        # Now, check line overlaps
        line_overlaps = dict()
        def insert_into_res(ids, geometry):
            """
            Local function to append a geometry into a list for each pair of ids
            """
            pair = "{}-{}".format(min(ids), max(ids))
            if pair not in line_overlaps:
                line_overlaps[pair] = [geometry]
            else: # Pair is in dict already
                line_overlaps[pair].append(geometry)

        for line in line_features:
            insert_into_res([line[names.T_ID_F], line[names.T_ID_F+'_2']], line.geometry().asWkt())

        expected_line_overlaps = {
            '7-15': ['MultiLineString ((964213.72614089539274573 1077962.10928706941194832, 963759.37523004529066384 1078021.79097451153211296))'],
            '5-6': ['MultiLineString ((963926.86899802810512483 1077925.5301883143838495, 963980.77503829856868833 1077802.31638198206201196))'],
            '13-14': ['MultiLineString ((963210.47528458514716476 1077644.75307651958428323, 963255.32157539459876716 1077724.74916282831691206))'],
            '5-7': ['MultiLineString ((964309.98692709254100919 1077617.49567248369567096, 964144.41837483353447169 1077577.06614228105172515),(964144.41837483353447169 1077577.06614228105172515, 963905.69162506482098252 1077713.75645868084393442))'],
            '335-337': ['MultiLineString ((963643.395574557245709 1077747.43814651435241103, 963543.5341855603037402 1077760.18016819190233946))']
        }

        for pair, overlaps in line_overlaps.items():
            print("Testing pair {}...".format(pair))
            self.assertEqual(len(overlaps), len(expected_line_overlaps[pair]))
            for overlap in overlaps:
                self.assertIn(overlap, expected_line_overlaps[pair])

    def test_overlapping_polygons(self):
        print('\nINFO: Validating overlaps in polygons (plots)...')

        gpkg_path = get_test_copy_path('db/static/gpkg/geometry_utils.gpkg')
        uri = gpkg_path + '|layername={layername}'.format(layername='overlapping_polygons')
        polygons_overlap_layer = QgsVectorLayer(uri, 'overlapping_polygons', 'ogr')

        if QgsWkbTypes.isMultiType(polygons_overlap_layer.wkbType()) and \
                polygons_overlap_layer.geometryType() == QgsWkbTypes.PolygonGeometry:
            polygons_overlap_layer = processing.run("native:multiparttosingleparts",
                                           {'INPUT': polygons_overlap_layer, 'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']

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

        gpkg_path = get_test_copy_path('db/static/gpkg/topology_cases.gpkg')
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
            polygon_copy = self.app.core.get_layer_copy(polygon_layer)

            geom_polygon = polygon_copy.getFeature(1).geometry()
            init_vertex_geom = [vertex for vertex in geom_polygon.vertices()]

            self.geometry.add_topological_vertices(polygon_copy, lines_layer)

            geom_polygon = polygon_copy.getFeature(1).geometry()
            adjusted_vertex_geom = [vertex for vertex in geom_polygon.vertices()]

            num_vertices_added = len(adjusted_vertex_geom) - len(init_vertex_geom)
            self.assertEqual(num_vertices_added, vertices_test_values[i])

    def test_polygons_must_be_covered_by_lines(self):
        print('\nINFO: Validating polygons must be covered by lines...')

        gpkg_path = get_test_copy_path('db/static/gpkg/topology_cases.gpkg')
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

            polygon_as_lines_layer = processing.run("ladm_col:polygonstolines", {'INPUT': polygon_layer, 'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']
            diff_plot_boundary = self.geometry.difference_plot_boundary(names, polygon_as_lines_layer, lines_layer, 'fid')

            if diff_plot_boundary is not None:
                if len(diff_plot_boundary) > 0:
                    for element in range(len(diff_plot_boundary)):
                        self.assertIn(diff_plot_boundary[element]['geometry'].asWkt(), diff_geom[i], 'case_{}, element_{}'.format(i + 1, element))
                else: # Case 6
                    self.assertEqual('', diff_geom[i], 'case_{}'.format(i + 1))

    def test_lines_must_be_covered_by_polygons(self):
        print('\nINFO: Validating lines must be covered by polygons...')

        gpkg_path = get_test_copy_path('db/static/gpkg/topology_cases.gpkg')
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

            polygon_as_lines_layer = processing.run("ladm_col:polygonstolines", {'INPUT': polygon_layer, 'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']
            diff_boundary_plot = self.geometry.difference_boundary_plot(names, lines_layer, polygon_as_lines_layer, 'fid')

            if diff_boundary_plot is not None:
                if len(diff_boundary_plot) > 0:
                    self.assertEqual(diff_boundary_plot[0]['geometry'].asWkt(), diff_geom[i], 'case_{}'.format(i + 1))
                else:
                    self.assertEqual('', diff_geom[i], 'case_{}'.format(i + 1))

    def test_intersection_polygons_tolerance(self):
        print('\nINFO: Validating intersection in polygons (plots)...')

        gpkg_path = get_test_copy_path('db/static/gpkg/geometry_utils.gpkg')
        uri = gpkg_path + '|layername={layername}'.format(layername='overlapping_polygons')
        polygons_intersection_layer = QgsVectorLayer(uri, 'overlapping_polygons', 'ogr')

        polygon_id = 61
        overlapping_id = 62
        test_overlapping_polygon = 'MultiPolygon (((779846.53495819831732661 1225249.26543459924869239, 779783.95215819834265858 1225214.60283459979109466, 779755.42265819816384465 1225312.01313459943048656, 779751.20725819806102663 1225339.76893460075370967, 779753.92445819883141667 1225441.12693459982983768, 779750.35635819809976965 1225530.46543460036627948, 779822.77425819879863411 1225579.77523459936492145, 779989.38215819804463536 1225693.37413460086099803, 780035.07055819837842137 1225719.08503460022620857, 780048.81795819813851267 1225694.37763460050337017, 780107.8898581980029121 1225665.00753459963016212, 780145.38955819851253182 1225642.4988345995079726, 780156.81765819864813238 1225634.07963460008613765, 780178.43775819859001786 1225625.24393460038118064, 780098.00075819867197424 1225413.46203460055403411, 779976.68275819870177656 1225330.46993460017256439, 779918.56405819824431092 1225292.73203460010699928, 779846.53495819831732661 1225249.26543459924869239)))'
        polygon_intersection = self.geometry.get_intersection_polygons(polygons_intersection_layer, polygon_id, overlapping_id)
        self.assertEqual(polygon_intersection.asWkt(), test_overlapping_polygon)


    @classmethod
    def tearDownClass(cls):
        print("INFO: Unloading Model Baker...")
        unload_qgis_model_baker()


if __name__ == '__main__':
    nose2.main()
