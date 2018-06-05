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
        else:
            print("Model not found!!!", msg)


if __name__ == '__main__':
    nose2.main()
