import nose2

from qgis.core import QgsVectorLayer
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


class TesQualityValidations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import_qgis_model_baker()
        cls.app = AppInterface()
        cls.geometry = GeometryUtils()

    def test_validate_topology_relation_between_point_boundary_boundary(self):
        print('\nINFO: Validating that the relation between point boundary and boundary is registered in the topology table ...')

        gpkg_path = get_test_copy_path('db/static/gpkg/quality_validations.gpkg')
        self.db_gpkg = get_gpkg_conn('tests_quality_validations_gpkg')
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

        gpkg_path = get_test_copy_path('db/static/gpkg/quality_validations.gpkg')
        uri = gpkg_path + '|layername={layername}'.format(layername='construccion')
        building_layer = QgsVectorLayer(uri, 'construccion', 'ogr')
        uri = gpkg_path + '|layername={layername}'.format(layername='servidumbre_transito')
        right_of_way_layer = QgsVectorLayer(uri, 'servidumbre_transito', 'ogr')

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
        gpkg_path = get_test_copy_path('db/static/gpkg/geometry_utils.gpkg')
        self.db_gpkg = get_gpkg_conn('tests_geometry_util_gpkg')
        names = self.db_gpkg.names
        names.T_ID_F = 't_id'  # Static label is set because the database does not have the ladm structure

        uri = gpkg_path + '|layername={layername}'.format(layername='overlapping_lines')
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
        gpkg_path = get_test_copy_path('db/static/gpkg/quality_validations.gpkg')
        uri = gpkg_path + '|layername={layername}'.format(layername='boundary')
        boundary_layer = QgsVectorLayer(uri, 'dangles', 'ogr')

        features = [feature for feature in boundary_layer.getFeatures()]
        self.assertEqual(len(features), 8)

        end_points, dangle_ids = self.geometry.get_dangle_ids(boundary_layer)
        self.assertEqual(len(dangle_ids), 0)

    def test_boundaries_are_not_split(self):
        print('\nINFO: Validating boundaries are not split...')
        gpkg_path = get_test_copy_path('db/static/gpkg/quality_validations.gpkg')
        self.db_gpkg = get_gpkg_conn('tests_quality_validations_gpkg')
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

    def test_check_gaps_in_plots(self):
        gpkg_path = get_test_copy_path('db/static/gpkg/quality_validations.gpkg')
        uri = gpkg_path + '|layername={layername}'.format(layername='check_gaps_in_plots')
        test_plots_layer = QgsVectorLayer(uri, 'check_gaps_in_plots', 'ogr')

        print('\nINFO: Validating Gaps in Plots using roads and multiple geometries...')
        gaps = GeometryUtils.get_gaps_in_polygon_layer(test_plots_layer, True)
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
        gaps = GeometryUtils.get_gaps_in_polygon_layer(test_plots_layer, True)
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
        gaps = GeometryUtils.get_gaps_in_polygon_layer(test_plots_layer, False)
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
        gaps = GeometryUtils.get_gaps_in_polygon_layer(test_plots_layer, False)
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
        gaps = GeometryUtils.get_gaps_in_polygon_layer(test_plots_layer, True)
        geometries = [g.asWkt() for g in gaps]
        self.assertEqual([], geometries)
        self.assertEqual(len(geometries), 0)

        test_plots_layer.rollBack()

        print('\nINFO: Validating Gaps in Plots without using roads for only one geometry...')
        test_plots_layer.startEditing()
        test_plots_layer.deleteFeature(1)
        test_plots_layer.deleteFeature(2)
        test_plots_layer.deleteFeature(3)
        gaps = GeometryUtils.get_gaps_in_polygon_layer(test_plots_layer, False)
        geometries = [g.asWkt() for g in gaps]
        self.assertEqual([], geometries)
        self.assertEqual(len(geometries), 0)

        test_plots_layer.rollBack()

        print('\nINFO: Validating Gaps in Plots using roads for two geometries...')
        test_plots_layer.startEditing()
        test_plots_layer.deleteFeature(1)
        test_plots_layer.deleteFeature(3)
        gaps = GeometryUtils.get_gaps_in_polygon_layer(test_plots_layer, True)
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
        gaps = GeometryUtils.get_gaps_in_polygon_layer(test_plots_layer, False)
        geometries = [g.asWkt() for g in gaps]
        self.assertEqual([], geometries)
        self.assertEqual(len(geometries), 0)

        test_plots_layer.rollBack()

    def test_multiparts_in_right_of_way(self):
        print('\nINFO: Validating right_of_way for no multipart geometries...')
        gpkg_path = get_test_copy_path('db/static/gpkg/quality_validations.gpkg')
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

        gpkg_path = get_test_copy_path('db/static/gpkg/quality_validations.gpkg')
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

    @classmethod
    def tearDownClass(cls):
        print("INFO: Unloading Model Baker...")
        unload_qgis_model_baker()


if __name__ == '__main__':
    nose2.main()
