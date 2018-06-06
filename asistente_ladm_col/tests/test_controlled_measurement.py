import nose2

from qgis.core import QgsVectorLayer, QgsApplication
from asistente_ladm_col.tests.utils import get_test_copy_path
from qgis.testing import unittest
from asistente_ladm_col.gui.controlled_measurement_dialog import ControlledMeasurementDialog

from processing.core.Processing import Processing
from qgis.analysis import QgsNativeAlgorithms


class TestExport(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        Processing.initialize()
        QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

    def test_to_get_point_groups(self):
        print('\nINFO: Validating controlled measurement...')
        gpkg_path = get_test_copy_path('geopackage/tests_data.gpkg')
        uri = gpkg_path + '|layername={layername}'.format(layername='tests_controlled_measurement')
        measure_layer = QgsVectorLayer(uri, 'tests_controlled_measurement', 'ogr')

        self.assertEqual(measure_layer.featureCount(), 38)

        bdef = [i.id() for i in measure_layer.getFeatures("\"tipe_def\"='Bien_Definido'")]
        self.assertEqual(len(bdef), 20)

        nbdef = [i.id() for i in measure_layer.getFeatures("\"tipe_def\"='No_Bien_Definido'")]
        self.assertEqual(len(nbdef), 18)
        print(type(measure_layer))
        res, msg = ControlledMeasurementDialog.run_group_points_model(
            ControlledMeasurementDialog, measure_layer, 0.5, 'tipe_def')
        if res is not None:
            self.assertEqual(res['native:mergevectorlayers_1:output'].featureCount(), 38)
            for r in range(1,10):
                dt = [i.id() for i in res['native:mergevectorlayers_1:output'].getFeatures("\"belongs_to_group\"={}".format(r))]
                self.assertEqual(len(dt), 2)
            features = res['native:mergevectorlayers_1:output'].getFeatures("\"belongs_to_group\"=4")
            features = [f for f in features]
            self.assertEqual(sorted([f.attributes()[0] for f in features]) , [191, 192])
        else:
            print("Model not found!!!", msg)

        res, msg = ControlledMeasurementDialog.run_group_points_model(
            ControlledMeasurementDialog, measure_layer, 5.0, 'tipe_def')
        if res is not None:
            self.assertEqual(res['native:mergevectorlayers_1:output'].featureCount(), 38)
            for r in [3, 8]:
                dt = [i.id() for i in res['native:mergevectorlayers_1:output'].getFeatures("\"belongs_to_group\"={}".format(r))]
                self.assertEqual(len(dt), 4)
            features = res['native:mergevectorlayers_1:output'].getFeatures("\"belongs_to_group\"=3")
            features = [f for f in features]
            self.assertEqual(sorted([f.attributes()[0] for f in features]), [189, 190, 191, 192])
        else:
            print("Model not found!!!", msg)


if __name__ == '__main__':
    nose2.main()
