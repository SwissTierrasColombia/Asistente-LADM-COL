import nose2
from qgis.PyQt.QtCore import QSettings
from qgis.core import (QgsProject,
                       QgsVectorLayer,
                       NULL)

from qgis.testing import (unittest,
                          start_app)

from asistente_ladm_col.app_interface import AppInterface

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.lib.model_registry import LADMColModelRegistry
from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.tests.utils import (import_qgis_model_baker,
                                            unload_qgis_model_baker,
                                            restore_pg_db,
                                            get_test_path,
                                            import_processing,
                                            delete_features,
                                            get_test_copy_path)

import_processing()
import processing


class TestInsertFeaturesToLayer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import_qgis_model_baker()

        cls.app = AppInterface()
        cls.db = restore_pg_db('insert_features_to_layer', [LADMColModelRegistry().model(LADMNames.SUPPLIES_MODEL_KEY).full_name()])
        res, code, msg = cls.db.test_connection()
        cls.assertTrue(res, msg)

    def test_calculate_automatic_values_in_batch_mode(self):
        print('\nINFO: Validating automatic values in batch...')

        # Config settings
        QSettings().setValue('Asistente-LADM-COL/automatic_values/automatic_values_in_batch_mode', True)

        source_layer_path = get_test_copy_path("db/static/gpkg/insert_features_to_layer.gpkg") + "|layername=a"

        layer_cadastral_parcel = self.app.core.get_layer(self.db, self.db.names.GC_PARCEL_T, load=True)
        # self.set_automatic_fields(db, layer, layer_name)  # Since this is the first get_layer(), no need to call it
        delete_features(layer_cadastral_parcel)
        count_before = layer_cadastral_parcel.featureCount()

        res = processing.run("ladm_col:insertfeaturestolayer", {'INPUT': source_layer_path, 'OUTPUT': layer_cadastral_parcel})

        output = res['OUTPUT']
        self.assertIsNotNone(output)

        count_after = output.featureCount()
        print("New features in output: {}".format(count_after - count_before))
        self.assertGreater(count_after, count_before, "There should be new features in the output layer!")

        print("Iterating {} features in output...".format(count_after))
        for feature in output.getFeatures():
            self.assertEqual(len(feature[self.db.names.T_ILI_TID_F]), 36)

    def test_calculate_automatic_values_in_batch_mode_but_setting_is_disabled(self):
        print('\nINFO: Validating automatic values in batch, but setting is disabled...')

        # Config settings
        QSettings().setValue('Asistente-LADM-COL/automatic_values/automatic_values_in_batch_mode', True)
        QSettings().setValue('Asistente-LADM-COL/automatic_values/t_ili_tid_enabled', False)

        source_layer_path = get_test_copy_path("db/static/gpkg/insert_features_to_layer.gpkg") + "|layername=a"

        layer_cadastral_parcel = self.app.core.get_layer(self.db, self.db.names.GC_PARCEL_T, load=True)
        self.app.core.set_automatic_fields(self.db, layer_cadastral_parcel, self.db.names.GC_PARCEL_T, self.app.core.get_active_models_per_db(self.db))
        delete_features(layer_cadastral_parcel)
        count_before = layer_cadastral_parcel.featureCount()

        res = processing.run("ladm_col:insertfeaturestolayer", {'INPUT': source_layer_path, 'OUTPUT': layer_cadastral_parcel})

        output = res['OUTPUT']
        self.assertIsNotNone(output)

        count_after = output.featureCount()
        print("New features in output: {}".format(count_after - count_before))
        self.assertGreater(count_after, count_before, "There should be new features in the output layer!")

        print("Iterating {} features in output...".format(count_after))
        for feature in output.getFeatures():
            self.assertEqual(feature[self.db.names.T_ILI_TID_F], NULL)

    def test_do_not_calculate_automatic_values_in_batch_mode(self):
        print('\nINFO: Validating do not calculate automatic values in batch mode...')

        # Config settings
        QSettings().setValue('Asistente-LADM-COL/automatic_values/automatic_values_in_batch_mode', False)

        source_layer_path = get_test_copy_path("db/static/gpkg/insert_features_to_layer.gpkg") + "|layername=a"

        layer_cadastral_parcel = self.app.core.get_layer(self.db, self.db.names.GC_PARCEL_T, load=True)
        self.app.core.set_automatic_fields(self.db, layer_cadastral_parcel, self.db.names.GC_PARCEL_T, self.app.core.get_active_models_per_db(self.db))
        delete_features(layer_cadastral_parcel)
        count_before = layer_cadastral_parcel.featureCount()

        res = processing.run("ladm_col:insertfeaturestolayer", {'INPUT': source_layer_path, 'OUTPUT': layer_cadastral_parcel})

        output = res['OUTPUT']
        self.assertIsNotNone(output)

        count_after = output.featureCount()
        print("New features in output: {}".format(count_after - count_before))
        self.assertGreater(count_after, count_before, "There should be new features in the output layer!")

        print("Iterating {} features in output...".format(count_after))
        for feature in output.getFeatures():
            self.assertEqual(feature[self.db.names.T_ILI_TID_F], NULL)


    @classmethod
    def tearDownClass(cls):
        print("INFO: Unloading Model Baker")
        unload_qgis_model_baker()


if __name__ == '__main__':
    nose2.main()
