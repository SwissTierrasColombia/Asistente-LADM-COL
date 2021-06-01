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
                                            get_field_values_by_key_values,
                                            get_copy_gpkg_conn)
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData


class TestLADMData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import_qgis_model_baker()
        cls.db_gpkg = get_copy_gpkg_conn('test_ladm_survey_model_gpkg')
        res, code, msg = cls.db_gpkg.test_connection()
        cls.assertTrue(res, msg)

        cls.app = AppInterface()
        cls.ladm_data = LADMData()

    def test_get_features_from_t_ids(self):
        print('\nINFO: Validating get_features_from_t_ids...')

        self.db_gpkg.test_connection()  # To build names
        names = self.db_gpkg.names

        layer = self.app.core.get_layer(self.db_gpkg, names.COL_POINT_TYPE_D, load=True)
        self.assertEqual(layer.featureCount(), 14)

        field_name = "thisClass"
        field_values = ["LADM_COL_V3_0.LADM_Nucleo.COL_PuntoTipo"]

        # We have 3 cases to test:
        # a) Single field (if no_attributes is True and only_attributes is an empty list)
        features = self.ladm_data.get_features_from_t_ids(layer, field_name, field_values, no_attributes=True,
                                                          only_attributes=list())
        self.assertEqual(len(features), 3)
        self.assertEqual(len([a for a in features[0].attributes() if a is not None]), 1)

        # b) Several fields (if only_attributes is not an empty list)
        #    We test both cases, when no_attributes is True and when it's False
        features = self.ladm_data.get_features_from_t_ids(layer, field_name, field_values, no_attributes=True,
                                                          only_attributes=[names.ILICODE_F, names.DISPLAY_NAME_F,
                                                                           "itfCode"])
        self.assertEqual(len(features), 3)
        # Note that the query field is always returned, so we get the 3 we asked for plus the query field
        self.assertEqual(len([a for a in features[0].attributes() if a is not None]), 4)

        features = self.ladm_data.get_features_from_t_ids(layer, field_name, field_values, no_attributes=False,
                                                          only_attributes=[names.ILICODE_F, names.DISPLAY_NAME_F,
                                                                           "itfCode"])
        self.assertEqual(len(features), 3)
        # Note that the query field is always returned, so we get the 3 we asked for plus the query field
        self.assertEqual(len([a for a in features[0].attributes() if a is not None]), 4)

        # c) All fields (if no_attributes is False and only_attributes is an empty list).
        features = self.ladm_data.get_features_from_t_ids(layer, field_name, field_values, no_attributes=False,
                                                          only_attributes=list())
        self.assertEqual(len(features), 3)
        attrs = features[0].attributes()
        field_count = len(attrs)
        self.assertEqual(field_count, 9)
        self.assertEqual(len([a for a in attrs if a is not None]), field_count)  # We get all 9 values

    def test_get_domain_value_from_code(self):
        print('\nINFO: Validating get domain value from code ...')

        layers = {
            self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D: None,
            self.db_gpkg.names.LC_RIGHT_TYPE_D: None
        }
        self.app.core.get_layers(self.db_gpkg, layers, load=True)
        test_t_id = get_field_values_by_key_values(layers[self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D],
                                                   self.db_gpkg.names.ILICODE_F,
                                                   [LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY],
                                                   self.db_gpkg.names.T_ID_F)[0]

        # Good parameters
        value = self.ladm_data.get_domain_value_from_code(self.db_gpkg, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, test_t_id, value_is_ilicode=True)
        self.assertEqual(value, LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY)

        value = self.ladm_data.get_domain_value_from_code(self.db_gpkg, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, test_t_id, value_is_ilicode=False)
        self.assertEqual(value, 'No propiedad horizontal')

        test_t_id = get_field_values_by_key_values(layers[self.db_gpkg.names.LC_RIGHT_TYPE_D],
                                                   self.db_gpkg.names.ILICODE_F, ['Dominio'], self.db_gpkg.names.T_ID_F)[0]
        value = self.ladm_data.get_domain_value_from_code(self.db_gpkg, layers[self.db_gpkg.names.LC_RIGHT_TYPE_D], test_t_id, value_is_ilicode=True)
        self.assertEqual(value, 'Dominio')

        # Domain value does not exist
        value = self.ladm_data.get_domain_value_from_code(self.db_gpkg, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, 99999, value_is_ilicode=True)
        self.assertIsNone(value)

        value = self.ladm_data.get_domain_value_from_code(self.db_gpkg, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, 99999, value_is_ilicode=False)
        self.assertIsNone(value)

        # Domain table does not exist
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
        test_t_id = get_field_values_by_key_values(layers[self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D], self.db_gpkg.names.ILICODE_F, [LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY], self.db_gpkg.names.T_ID_F)[0]

        # Good parameters
        value = self.ladm_data.get_domain_code_from_value(self.db_gpkg, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY, value_is_ilicode=True)
        self.assertEqual(value, test_t_id)

        value = self.ladm_data.get_domain_code_from_value(self.db_gpkg, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, 'No propiedad horizontal', value_is_ilicode=False)
        self.assertEqual(value, test_t_id)

        test_t_id = get_field_values_by_key_values(layers[self.db_gpkg.names.LC_RIGHT_TYPE_D], self.db_gpkg.names.ILICODE_F, ['Dominio'], self.db_gpkg.names.T_ID_F)[0]
        value = self.ladm_data.get_domain_code_from_value(self.db_gpkg, layers[self.db_gpkg.names.LC_RIGHT_TYPE_D], 'Dominio', value_is_ilicode=True)
        self.assertEqual(value, test_t_id)

        # Domain value does not exist
        value = self.ladm_data.get_domain_code_from_value(self.db_gpkg, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, 'value_none', value_is_ilicode=True)
        self.assertIsNone(value)

        value = self.ladm_data.get_domain_code_from_value(self.db_gpkg, self.db_gpkg.names.LC_CONDITION_PARCEL_TYPE_D, 'value_none', value_is_ilicode=False)
        self.assertIsNone(value)

        # Domain table does not exist
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
        print("\nINFO: Closing open db connections; unloading Model Baker")
        cls.db_gpkg.conn.close()
        unload_qgis_model_baker()


if __name__ == '__main__':
    nose2.main()