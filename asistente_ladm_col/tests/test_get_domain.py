import nose2

from qgis.core import (NULL,
                       QgsVectorLayer)

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.ladm_names import LADMNames
from qgis.testing import (unittest,
                          start_app)

start_app()  # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (import_qgis_model_baker,
                                            unload_qgis_model_baker,
                                            get_field_values_by_another_field,
                                            get_copy_gpkg_conn)
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData


class TestGetDomains(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import_qgis_model_baker()
        cls.db_gpkg = get_copy_gpkg_conn('test_ladm_survey_model_gpkg')
        res, code, msg = cls.db_gpkg.test_connection()
        cls.assertTrue(res, msg)

        cls.app = AppInterface()
        cls.ladm_data = LADMData()

    def test_get_domain_value_from_code(self):
        print('\nINFO: Validating get domain value from code ...')

        layers = {
            self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D: None,
            self.db_gpkg.names.LC_RIGHT_TYPE_D: None
        }
        self.app.core.get_layers(self.db_gpkg, layers, load=True)
        test_t_id = get_field_values_by_another_field(layers[self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D],
                                                      self.db_gpkg.names.ILICODE_F,
                                                      [LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY],
                                                      self.db_gpkg.names.T_ID_F)[0]

        # Good parameters
        value = self.ladm_data.get_domain_value_from_code(self.db_gpkg, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, test_t_id, value_is_ilicode=True)
        self.assertEqual(value, LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY)

        value = self.ladm_data.get_domain_value_from_code(self.db_gpkg, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, test_t_id, value_is_ilicode=False)
        self.assertEqual(value, 'No propiedad horizontal')

        test_t_id = get_field_values_by_another_field(layers[self.db_gpkg.names.LC_RIGHT_TYPE_D],
                                                      self.db_gpkg.names.ILICODE_F, ['Dominio'], self.db_gpkg.names.T_ID_F)[0]
        value = self.ladm_data.get_domain_value_from_code(self.db_gpkg, layers[self.db_gpkg.names.LC_RIGHT_TYPE_D], test_t_id, value_is_ilicode=True)
        self.assertEqual(value, 'Dominio')

        # Domain value not exit
        value = self.ladm_data.get_domain_value_from_code(self.db_gpkg, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, 99999, value_is_ilicode=True)
        self.assertIsNone(value)

        value = self.ladm_data.get_domain_value_from_code(self.db_gpkg, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, 99999, value_is_ilicode=False)
        self.assertIsNone(value)

        # Domain table not exit
        value = self.ladm_data.get_domain_value_from_code(self.db_gpkg, 'table_none', 1, value_is_ilicode=True)
        self.assertIsNone(value)

        value = self.ladm_data.get_domain_value_from_code(self.db_gpkg, 'table_none', 1, value_is_ilicode=False)
        self.assertIsNone(value)

        # Bad parameters values
        value = self.ladm_data.get_domain_value_from_code(None, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, 1, value_is_ilicode=True)
        self.assertIsNone(value)

        value = self.ladm_data.get_domain_value_from_code(self.db_gpkg, None, 1, value_is_ilicode=True)
        self.assertIsNone(value)

        value = self.ladm_data.get_domain_value_from_code(self.db_gpkg, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, None, value_is_ilicode=True)
        self.assertIsNone(value)

        value = self.ladm_data.get_domain_value_from_code(self.db_gpkg, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, 1, None)
        self.assertIsNone(value)

        value = self.ladm_data.get_domain_value_from_code(NULL, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, 1, value_is_ilicode=True)
        self.assertIsNone(value)

        value = self.ladm_data.get_domain_value_from_code(self.db_gpkg, NULL, 1, value_is_ilicode=True)
        self.assertIsNone(value)

        value = self.ladm_data.get_domain_value_from_code(self.db_gpkg, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, NULL, value_is_ilicode=True)
        self.assertIsNone(value)

        value = self.ladm_data.get_domain_value_from_code(self.db_gpkg, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, 1, NULL)
        self.assertIsNone(value)

        domain_layer = QgsVectorLayer("NoGeometry", 'domain layer', "memory")
        value = self.ladm_data.get_domain_value_from_code(self.db_gpkg, domain_layer, 1, value_is_ilicode=True)
        self.assertIsNone(value)

    def test_get_domain_code_from_value(self):
        print('\nINFO: Validating get domain code from value...')

        layers = {
            self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D: None,
            self.db_gpkg.names.LC_RIGHT_TYPE_D: None
        }
        self.app.core.get_layers(self.db_gpkg, layers, load=True)
        test_t_id = get_field_values_by_another_field(layers[self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D], self.db_gpkg.names.ILICODE_F, [LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY], self.db_gpkg.names.T_ID_F)[0]

        # Good parameters
        value = self.ladm_data.get_domain_code_from_value(self.db_gpkg, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY, value_is_ilicode=True)
        self.assertEqual(value, test_t_id)

        value = self.ladm_data.get_domain_code_from_value(self.db_gpkg, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, 'No propiedad horizontal', value_is_ilicode=False)
        self.assertEqual(value, test_t_id)

        test_t_id = get_field_values_by_another_field(layers[self.db_gpkg.names.LC_RIGHT_TYPE_D], self.db_gpkg.names.ILICODE_F, ['Dominio'], self.db_gpkg.names.T_ID_F)[0]
        value = self.ladm_data.get_domain_code_from_value(self.db_gpkg, layers[self.db_gpkg.names.LC_RIGHT_TYPE_D], 'Dominio', value_is_ilicode=True)
        self.assertEqual(value, test_t_id)

        # Domain value not exit
        value = self.ladm_data.get_domain_code_from_value(self.db_gpkg, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, 'value_none', value_is_ilicode=True)
        self.assertIsNone(value)

        value = self.ladm_data.get_domain_code_from_value(self.db_gpkg, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, 'value_none', value_is_ilicode=False)
        self.assertIsNone(value)

        # Domain table not exit
        value = self.ladm_data.get_domain_code_from_value(self.db_gpkg, 'table_none', LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY, value_is_ilicode=True)
        self.assertIsNone(value)

        value = self.ladm_data.get_domain_code_from_value(self.db_gpkg, 'table_none', 'No propiedad horizontal', value_is_ilicode=False)
        self.assertIsNone(value)

        # Bad parameters values
        value = self.ladm_data.get_domain_code_from_value(None, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY, value_is_ilicode=True)
        self.assertIsNone(value)

        value = self.ladm_data.get_domain_code_from_value(self.db_gpkg, None, LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY, value_is_ilicode=True)
        self.assertIsNone(value)

        value = self.ladm_data.get_domain_code_from_value(self.db_gpkg, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, None, value_is_ilicode=True)
        self.assertIsNone(value)

        value = self.ladm_data.get_domain_code_from_value(self.db_gpkg, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY, None)
        self.assertIsNone(value)

        value = self.ladm_data.get_domain_code_from_value(NULL, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY, value_is_ilicode=True)
        self.assertIsNone(value)

        value = self.ladm_data.get_domain_code_from_value(self.db_gpkg, NULL, LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY, value_is_ilicode=True)
        self.assertIsNone(value)

        value = self.ladm_data.get_domain_code_from_value(self.db_gpkg, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, NULL, value_is_ilicode=True)
        self.assertIsNone(value)

        value = self.ladm_data.get_domain_code_from_value(self.db_gpkg, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY, NULL)
        self.assertIsNone(value)

        domain_layer = QgsVectorLayer("NoGeometry", 'domain layer', "memory")
        value = self.ladm_data.get_domain_code_from_value(self.db_gpkg, domain_layer, LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY, value_is_ilicode=True)
        self.assertIsNone(value)

    @classmethod
    def tearDownClass(cls):
        print("INFO: Closing open db connections; unloading Model Baker")
        cls.db_gpkg.conn.close()
        unload_qgis_model_baker()


if __name__ == '__main__':
    nose2.main()