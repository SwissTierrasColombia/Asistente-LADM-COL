import nose2

from qgis.core import QgsVectorLayer, QgsApplication, QgsField
from qgis.testing import unittest
from processing.core.Processing import Processing
from qgis.analysis import QgsNativeAlgorithms
from qgis.PyQt.QtCore import QVariant

from asistente_ladm_col.config.general_config import (
    TRUSTWORTHY_FIELD_NAME,
    GROUP_FIELD_NAME
)
from asistente_ladm_col.tests.utils import get_test_copy_path
from asistente_ladm_col.gui.controlled_measurement_dialog import ControlledMeasurementDialog
from asistente_ladm_col.utils.qgis_utils import QGISUtils


class TestExport(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.qgis_utils = QGISUtils()
        Processing.initialize()
        QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
        self.TestClass = ControlledMeasurementDialog(self.qgis_utils)

    def test_get_point_groups(self):
        print('\nINFO: Validating controlled measurement (Point Grouping)...')
        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        uri = gpkg_path + '|layername={layername}'.format(layername='tests_controlled_measurement')
        measure_layer = QgsVectorLayer(uri, 'tests_controlled_measurement', 'ogr')

        self.assertEqual(measure_layer.featureCount(), 38)

        bdef = [i.id() for i in measure_layer.getFeatures("\"def_type\"='Bien_Definido'")]
        self.assertEqual(len(bdef), 20)

        nbdef = [i.id() for i in measure_layer.getFeatures("\"def_type\"='No_Bien_Definido'")]
        self.assertEqual(len(nbdef), 18)

        # Test model with distance of 0.5 meters
        res, msg = self.TestClass.run_group_points_model(measure_layer, 0.5, 'def_type')

        self.assertIsNotNone(res) # Model not found

        res_layer = res['native:mergevectorlayers_1:output']
        self.assertEqual(res_layer.featureCount(), 38)
        for g in range(1,10):
            dt = [f.id() for f in res_layer.getFeatures("\"{}\"={}".format(GROUP_FIELD_NAME, g))]
            self.assertEqual(len(dt), 2) # All groups have 2 features

        features = res_layer.getFeatures("\"{}\"=4".format(GROUP_FIELD_NAME))
        features = [f for f in features]
        self.assertEqual(sorted([f.attributes()[0] for f in features]) , [191, 192])

        # Test model with distance of 5 meters
        res, msg = self.TestClass.run_group_points_model(measure_layer, 5.0, 'def_type')

        self.assertIsNotNone(res) # Model not found

        res_layer = res['native:mergevectorlayers_1:output']
        self.assertEqual(res_layer.featureCount(), 38)
        for g in [3, 8]:
            dt = [f.id() for f in res_layer.getFeatures("\"{}\"={}".format(GROUP_FIELD_NAME, g))]
            self.assertEqual(len(dt), 4)
        features = res_layer.getFeatures("\"{}\"=3".format(GROUP_FIELD_NAME))
        features = [f for f in features]
        self.assertEqual(sorted([f.attributes()[0] for f in features]), [189, 190, 191, 192])

    def test_time_groups_validation(self):
        print('\nINFO: Validating controlled measurement (Time Group Validation)...')
        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        uri = gpkg_path + '|layername={layername}'.format(layername='tests_controlled_measurement')
        measure_layer = QgsVectorLayer(uri, 'tests_controlled_measurement', 'ogr')

        self.assertEqual(measure_layer.featureCount(), 38)

        bdef = [i.id() for i in measure_layer.getFeatures("\"def_type\"='Bien_Definido'")]
        self.assertEqual(len(bdef), 20)

        nbdef = [i.id() for i in measure_layer.getFeatures("\"def_type\"='No_Bien_Definido'")]
        self.assertEqual(len(nbdef), 18)

        # Test to check time validation with 0.5 meters of distance
        res, msg = self.TestClass.run_group_points_model(
             measure_layer, 0.5, 'def_type')
        res_layer = res['native:mergevectorlayers_1:output']

        res_layer.dataProvider().addAttributes([QgsField(TRUSTWORTHY_FIELD_NAME, QVariant.String)])
        res_layer.updateFields()

        for i in [10, 6, 3]:
            features, no_features = self.TestClass.time_filter(
                layer=res_layer,
                features=res_layer.getFeatures("\"{}\"={}".format(GROUP_FIELD_NAME, i)),
                idx=res_layer.fields().indexFromName("timestamp"),
                time_tolerance=30) # minutes

            feat = {10: 1, 6: 1, 3: 2}
            no_feat = {10: 1, 6: 1, 3: 0}
            self.assertEqual(len([feat for feat in features]), feat[i])
            self.assertEqual(len([feat for feat in no_features]), no_feat[i])

        new_layer = self.TestClass.validate_trustworthy(res_layer, 30, "timestamp")

        null_group_count = [i.id() for i in new_layer.getFeatures("\"{}\" IS NULL".format(GROUP_FIELD_NAME))]
        self.assertEqual(len(null_group_count), 21)

        group_count = [i.id() for i in new_layer.getFeatures("\"{}\" IS NOT NULL".format(GROUP_FIELD_NAME))]
        self.assertEqual(len(group_count), 17)

        not_trustworthy_count = [i.id() for i in new_layer.getFeatures("\"{}\" = 'False'".format(TRUSTWORTHY_FIELD_NAME))]
        self.assertEqual(len(not_trustworthy_count), 24)

        trustworthy_count = [i.id() for i in new_layer.getFeatures("\"{}\" = 'True'".format(TRUSTWORTHY_FIELD_NAME))]
        self.assertEqual(len(trustworthy_count), 14)

        # Test to check time validation with 5 meters of distance.
        res, msg = self.TestClass.run_group_points_model(measure_layer, 5, 'def_type')

        res_layer = res['native:mergevectorlayers_1:output']
        res_layer.dataProvider().addAttributes([QgsField(TRUSTWORTHY_FIELD_NAME, QVariant.String)])
        res_layer.updateFields()

        for i in [8, 4, 3]:
            features, no_features = self.TestClass.time_filter(
                res_layer,
                res_layer.getFeatures("\"{}\"={}".format(GROUP_FIELD_NAME, i)),
                idx=res_layer.fields().indexFromName("timestamp"),
                time_tolerance=30)

            feat = {8: 2, 4: 1, 3: 4}
            no_feat = {8: 2, 4: 1, 3: 0}
            self.assertEqual(len([feat for feat in features]), feat[i])
            self.assertEqual(len([feat for feat in no_features]), no_feat[i])

        new_layer = self.TestClass.validate_trustworthy(res_layer, 30, "timestamp")

        null_group_count = [i.id() for i in new_layer.getFeatures("\"{}\" IS NULL".format(GROUP_FIELD_NAME))]
        self.assertEqual(len(null_group_count), 19)

        group_count = [i.id() for i in new_layer.getFeatures("\"{}\" IS NOT NULL".format(GROUP_FIELD_NAME))]
        self.assertEqual(len(group_count), 19)

        not_trustworthy_count = [i.id() for i in new_layer.getFeatures("\"{}\" = 'False'".format(TRUSTWORTHY_FIELD_NAME))]
        self.assertEqual(len(not_trustworthy_count), 22)

        trustworthy_count = [i.id() for i in new_layer.getFeatures("\"{}\" = 'True'".format(TRUSTWORTHY_FIELD_NAME))]
        self.assertEqual(len(trustworthy_count), 16)


if __name__ == '__main__':
    nose2.main()
