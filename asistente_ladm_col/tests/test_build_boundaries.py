import nose2

from qgis.testing import start_app, unittest

from qgis.core import (QgsVectorLayer,
                       QgsGeometry)

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.gui.toolbar import ToolBar
from asistente_ladm_col.tests.utils import (import_qgis_model_baker,
                                            import_processing,
                                            import_asistente_ladm_col,
                                            get_iface,
                                            get_gpkg_conn,
                                            get_copy_gpkg_conn,
                                            get_test_copy_path,
                                            unload_qgis_model_baker)

start_app()  # need to start before asistente_ladm_col.tests.utils

import_processing()
import processing


class TestBuildBoundaries(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import_qgis_model_baker()
        import_asistente_ladm_col()  # Import plugin
        cls.app = AppInterface()
        cls.toolbar = ToolBar(get_iface())

    def test_build_boundaries(self):
        print('\nINFO: Validating build boundaries...')
        db_gpkg = get_copy_gpkg_conn('test_build_boundaries_gpkg')
        res, code, msg = db_gpkg.test_connection()
        self.assertTrue(res, msg)

        layers = {db_gpkg.names.LC_BOUNDARY_POINT_T: None,
                  db_gpkg.names.LC_BOUNDARY_T: None,
                  db_gpkg.names.LC_PLOT_T: None,
                  db_gpkg.names.MORE_BFS_T: None,
                  db_gpkg.names.LESS_BFS_T: None,
                  db_gpkg.names.POINT_BFS_T: None}
        self.app.core.get_layers(db_gpkg, layers, load=True)

        print('\nINFO: Check initial data...')
        layers_feature_count = {db_gpkg.names.LC_BOUNDARY_POINT_T: 12,
                                db_gpkg.names.LC_BOUNDARY_T: 21,
                                db_gpkg.names.LC_PLOT_T: 14,
                                db_gpkg.names.MORE_BFS_T: 42,
                                db_gpkg.names.LESS_BFS_T: 0,
                                db_gpkg.names.POINT_BFS_T: 46}

        for layer_name, feature_count in layers_feature_count.items():
            self.assertEqual(layers[layer_name].featureCount(),
                             feature_count,
                             'Features count does not match for the layer {}'.format(layer_name))

        print('\nINFO: Check build boundaries using a selection...')
        boundary_ids = ['c1a08287-4fd5-4504-a6b7-cd029bd0d352', 'e7db709f-f9ef-4d83-b59b-692f1c4f7942',
                        'db813999-3e1e-4539-99b6-7b797b1a3a72', '9831e428-040b-48e1-960a-5546fa47b99e',
                        '9a009adf-6e87-4b04-aeb6-5d0830a848a7', '25509907-7cbc-4c7d-ab76-153898205f80',
                        '1ef74b53-46fa-4dc5-9d85-c25db94f3dcd', '5b7194f2-54d8-4352-a47d-fac7f270a4a1']

        exp = "{} in ('{}')".format(db_gpkg.names.T_ILI_TID_F,
                                    "', '".join(boundary_ids))
        layers[db_gpkg.names.LC_BOUNDARY_T].selectByExpression(exp)

        self.toolbar.build_boundaries(db_gpkg)

        layers_feature_count = {db_gpkg.names.LC_BOUNDARY_POINT_T: 12,
                                db_gpkg.names.LC_BOUNDARY_T: 22,
                                db_gpkg.names.LC_PLOT_T: 14,
                                db_gpkg.names.MORE_BFS_T: 43,
                                db_gpkg.names.LESS_BFS_T: 0,
                                db_gpkg.names.POINT_BFS_T: 47}

        for layer_name, feature_count in layers_feature_count.items():
            self.assertEqual(layers[layer_name].featureCount(),
                             feature_count,
                             'Features count does not match for the layer {}'.format(layer_name))

        print('\nINFO: Check build boundaries for all features...')
        self.toolbar.build_boundaries(db_gpkg, True)

        layers_feature_count = {db_gpkg.names.LC_BOUNDARY_POINT_T: 12,
                                db_gpkg.names.LC_BOUNDARY_T: 25,
                                db_gpkg.names.LC_PLOT_T: 14,
                                db_gpkg.names.MORE_BFS_T: 44,
                                db_gpkg.names.LESS_BFS_T: 0,
                                db_gpkg.names.POINT_BFS_T: 50}

        for layer_name, feature_count in layers_feature_count.items():
            self.assertEqual(layers[layer_name].featureCount(),
                             feature_count,
                             'Features count does not match for the layer {}'.format(layer_name))

    def test_build_boundaries_with_empty_geom(self):
        print('\nINFO: Validating build boundaries, null geometries of the input layer are removed...')
        db_gpkg = get_copy_gpkg_conn('test_build_boundaries_empty_geom_gpkg')
        res, code, msg = db_gpkg.test_connection()
        self.assertTrue(res, msg)

        boundary_layer = self.app.core.get_layer(db_gpkg, db_gpkg.names.LC_BOUNDARY_T, load=True)
        self.assertEqual(boundary_layer.featureCount(), 3, 'Features count does not match for the layer boundary layer')

        exp = "is_empty_or_null($geometry)"
        boundary_layer.selectByExpression(exp)
        self.assertEqual(boundary_layer.selectedFeatureCount(), 1,
                         'Null features count does not match for the layer boundary layer')

        self.toolbar.build_boundaries(db_gpkg, True)

        self.assertEqual(boundary_layer.featureCount(), 6, 'Features count does not match for the layer boundary layer')

        exp = "is_empty_or_null($geometry)"
        boundary_layer.selectByExpression(exp)
        self.assertEqual(boundary_layer.selectedFeatureCount(), 0,
                         'Null features count does not match for the layer boundary layer')

    def test_build_boundaries_with_invalid_geom(self):
        print('\nINFO: Validating build boundaries, invalid geometry of the input layer are removed...')
        db_gpkg = get_copy_gpkg_conn('test_build_boundaries_invalid_geom_gpkg')
        res, code, msg = db_gpkg.test_connection()
        self.assertTrue(res, msg)

        boundary_layer = self.app.core.get_layer(db_gpkg, db_gpkg.names.LC_BOUNDARY_T, load=True)
        self.assertEqual(boundary_layer.featureCount(), 16, 'Features count does not match for the layer boundary layer')

        self.toolbar.build_boundaries(db_gpkg, True)

        self.assertEqual(boundary_layer.featureCount(), 1, 'Features count does not match for the layer boundary layer')

        exp = "is_empty_or_null($geometry)"
        boundary_layer.selectByExpression(exp)
        self.assertEqual(boundary_layer.selectedFeatureCount(), 0,
                         'Null features count does not match for the layer boundary layer')


    def test_build_boundaries_with_invalid_geom_in_processing(self):
        print('\nINFO: Validating build boundaries, invalid geometries generated when running the processing algorithm are fixed...')
        db_gpkg = get_copy_gpkg_conn('test_build_boundaries_fix_geoms_gpkg')
        res, code, msg = db_gpkg.test_connection()
        self.assertTrue(res, msg)

        boundary_layer = self.app.core.get_layer(db_gpkg, db_gpkg.names.LC_BOUNDARY_T, load=True)
        self.assertEqual(boundary_layer.featureCount(), 7, 'Features count does not match for the layer boundary layer')

        self.toolbar.build_boundaries(db_gpkg, True)

        self.assertEqual(boundary_layer.featureCount(), 17, 'Features count does not match for the layer boundary layer')

        exp = "is_empty_or_null($geometry)"
        boundary_layer.selectByExpression(exp)
        self.assertEqual(boundary_layer.selectedFeatureCount(), 0,
                         'Null features count does not match for the layer boundary layer')

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
            params = {'boundaries': boundary_layer, 'native:refactorfields_2:built_boundaries': 'TEMPORARY_OUTPUT'}
            built_boundaries_layer = processing.run("model:Build_Boundaries", params)['native:refactorfields_2:built_boundaries']
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
                self.assertTrue(found, 'The geometries are invalid: case {case}. Geometry in WKT: {geometry}'.format(case=case, geometry=boundary_geom.asWkt()))

    @classmethod
    def tearDownClass(cls):
        print("INFO: Unloading Model Baker...")
        unload_qgis_model_baker()


if __name__ == '__main__':
    nose2.main()
