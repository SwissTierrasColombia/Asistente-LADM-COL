import nose2

from qgis.core import NULL
from qgis.testing import (start_app,
                          unittest)

start_app()  # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.utils.qgis_utils import QGISUtils
from asistente_ladm_col.logic.ladm_col.ladm_data import LADM_DATA
from asistente_ladm_col.config.general_config import (LAYER,
                                                      LAYER_NAME)
from asistente_ladm_col.tests.utils import (get_pg_conn,
                                            restore_schema)


class TestLADMData(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        restore_schema('test_ladm_col_queries')

        self.db_pg = get_pg_conn('test_ladm_col_queries')
        result = self.db_pg.test_connection()
        print('test_connection', result)

        if not result[1]:
            print('The test connection is not working')
            return

        self.qgis_utils = QGISUtils()
        self.ladm_data = LADM_DATA(self.qgis_utils)
        self.names = self.db_pg.names

    def test_get_plots_related_to_parcels(self):
        print("\nINFO: Validating get plots related to parcels (Case: t_id)...")

        parcel_ids_tests = [list(), [975], [984, 975, 978]]
        plot_ids_tests = [list(), [1437], [1430, 1437, 1449]]

        count = 0
        for parcel_ids_test in parcel_ids_tests:
            plot_ids = self.ladm_data.get_plots_related_to_parcels(self.db_pg, parcel_ids_test, self.names.T_ID_F)
            # We use assertCountEqual to compare if two lists are the same regardless of the order of their elements.
            # https://docs.python.org/3.2/library/unittest.html#unittest.TestCase.assertCountEqual
            self.assertCountEqual(plot_ids, plot_ids_tests[count], "Failure with data set {}".format(count + 1))
            count += 1

        print("\nINFO: Validating get plots related to parcels (Case: custom field)...")
        plot_custom_field_ids_tests = [list(), [49379], [2614.3, 49379, 59108.5]]

        count = 0
        for parcel_ids_test in parcel_ids_tests:
            plot_custom_field_ids = self.ladm_data.get_plots_related_to_parcels(self.db_pg, parcel_ids_test, self.names.OP_PLOT_T_PLOT_AREA_F)
            self.assertCountEqual(plot_custom_field_ids, plot_custom_field_ids_tests[count], "Failure with data set {}".format(count + 1))
            count += 1

        print("\nINFO: Validating get plots related to parcels (Case: t_id) with preloaded tables...")

        layers = {self.names.OP_PLOT_T: {LAYER_NAME: self.names.OP_PLOT_T, LAYER: None},
                  self.names.COL_UE_BAUNIT_T: {LAYER_NAME: self.names.COL_UE_BAUNIT_T, LAYER: None}}
        self.qgis_utils.get_layers(self.db_pg, layers, load=True)
        self.assertIsNotNone(layers, 'An error occurred while trying to get the layers of interest')

        count = 0
        for parcel_ids_test in parcel_ids_tests:
            plot_ids = self.ladm_data.get_plots_related_to_parcels(self.db_pg,
                                                                   parcel_ids_test,
                                                                   self.names.T_ID_F,
                                                                   plot_layer=layers[self.names.OP_PLOT_T][LAYER],
                                                                   uebaunit_table=layers[self.names.COL_UE_BAUNIT_T][LAYER])
            self.assertCountEqual(plot_ids, plot_ids_tests[count], "Failure with data set {}".format(count + 1))
            count += 1

    def test_get_parcels_related_to_plots(self):
        print("\nINFO: Validating get parcels related to plots (Case: t_id)...")

        plot_ids_tests = [list(), [1437], [1430, 1437, 1449]]
        parcel_ids_tests = [list(), [975], [984, 975, 978]]

        count = 0
        for plot_ids_test in plot_ids_tests:
            parcel_ids = self.ladm_data.get_parcels_related_to_plots(self.db_pg, plot_ids_test, self.names.T_ID_F)
            # We use assertCountEqual to compare if two lists are the same regardless of the order of their elements.
            # https://docs.python.org/3.2/library/unittest.html#unittest.TestCase.assertCountEqual
            self.assertCountEqual(parcel_ids, parcel_ids_tests[count], "Failure with data set {}".format(count + 1))
            count += 1

        print("\nINFO: Validating get parcels related to plots (Case: custom field)...")
        parcel_custom_field_ids_tests = [list(),
                                         ['253940000000000230054000000000'],
                                         ['253940000000000230241000000000', '253940000000000230054000000000', '253940000000000230254000000000']]

        count = 0
        for plot_ids_test in plot_ids_tests:
            parcel_custom_field_ids = self.ladm_data.get_parcels_related_to_plots(self.db_pg,
                                                                                  plot_ids_test,
                                                                                  self.names.OP_PARCEL_T_PARCEL_NUMBER_F)
            self.assertCountEqual(parcel_custom_field_ids, parcel_custom_field_ids_tests[count],
                                  "Failure with data set {}".format(count + 1))
            count += 1

        print("\nINFO: Validating get parcels related to plots (Case: t_id) with preloaded tables...")

        layers = {
            self.names.OP_PARCEL_T: {LAYER_NAME: self.names.OP_PARCEL_T, LAYER: None},
            self.names.COL_UE_BAUNIT_T: {LAYER_NAME: self.names.COL_UE_BAUNIT_T, LAYER: None}
        }
        self.qgis_utils.get_layers(self.db_pg, layers, load=True)
        self.assertIsNotNone(layers, 'An error occurred while trying to get the layers of interest')

        count = 0
        for plot_ids_test in plot_ids_tests:
            parcel_ids = self.ladm_data.get_parcels_related_to_plots(self.db_pg,
                                                                     plot_ids_test,
                                                                     self.names.T_ID_F,
                                                                     parcel_table=layers[self.names.OP_PARCEL_T][LAYER],
                                                                     uebaunit_table=layers[self.names.COL_UE_BAUNIT_T][LAYER])
            self.assertCountEqual(parcel_ids, parcel_ids_tests[count], "Failure with data set {}".format(count + 1))
            count += 1

    def test_get_parcel_data_to_compare_changes(self):
        print("\nINFO: Validating get parcels data ...")

        features_test = {
            '253940000000000230241000000000': [
            {'departamento': '25',
             'matricula_inmobiliaria': NULL,
             'numero_predial': '253940000000000230241000000000',
             'condicion_predio': 'NPH',
             'nombre': 'Hoya Las Juntas',
             't_id': 950,
             'area_terreno': 7307.3,
             'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                              'documento_identidad': '14',
                              'nombre': '14 14primer apellido 14segundo apellido 14primer nombre 14segundo nombre',
                              'derecho': 'Dominio'}, {'tipo_documento': 'Cedula_Ciudadania',
                                                      'documento_identidad': '2',
                                                      'nombre': '2 2primer apellido 2segundo apellido 2primer nombre 2segundo nombre',
                                                      'derecho': 'Dominio'}]
             },
            {'departamento': '25',
             'matricula_inmobiliaria': NULL,
             'numero_predial': '253940000000000230241000000000',
             'condicion_predio': 'NPH',
             'nombre': 'SIN INFO',
             't_id': 953,
             'area_terreno': 4283.7,
             'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                              'documento_identidad': '14',
                              'nombre': '14 14primer apellido 14segundo apellido 14primer nombre 14segundo nombre',
                              'derecho': 'Dominio'}]},
            {'departamento': '25',
             'matricula_inmobiliaria': NULL,
             'numero_predial': '253940000000000230241000000000',
             'condicion_predio': 'NPH',
             'nombre': 'Tudela Juntas',
             't_id': 954,
             'area_terreno': 30777.3,
             'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                              'documento_identidad': '28',
                              'nombre': '28 28primer apellido 28segundo apellido 28primer nombre 28segundo nombre',
                              'derecho': 'Dominio'}]},
            {'departamento': '25',
             'matricula_inmobiliaria': NULL,
             'numero_predial': '253940000000000230241000000000',
             'condicion_predio': 'NPH',
             'nombre': 'Mardoqueo',
             't_id': 967,
             'area_terreno': 877.9,
             'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                              'documento_identidad': '35',
                              'nombre': '35 35primer apellido 35segundo apellido 35primer nombre 35segundo nombre',
                              'derecho': 'Dominio'}]},
            {'departamento': '25',
             'matricula_inmobiliaria': NULL,
             'numero_predial': '253940000000000230241000000000',
             'condicion_predio': 'NPH',
             'nombre': 'SIN INFO',
             't_id': 980,
             'area_terreno': 818.8,
             'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                              'documento_identidad': '26',
                              'nombre': '26 26primer apellido 26segundo apellido 26primer nombre 26segundo nombre',
                              'derecho': 'Dominio'}]},
            {'departamento': '25',
             'matricula_inmobiliaria': NULL,
             'numero_predial': '253940000000000230241000000000',
             'condicion_predio': 'NPH',
             'nombre': 'SIN INFO',
             't_id': 981,
             'area_terreno': 967.1,
             'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                              'documento_identidad': '25',
                              'nombre': '25 25primer apellido 25segundo apellido 25primer nombre 25segundo nombre',
                              'derecho': 'Dominio'}]},
            {'departamento': '25',
             'matricula_inmobiliaria': NULL,
             'numero_predial': '253940000000000230241000000000',
             'condicion_predio': 'NPH',
             'nombre': 'SIN INFO',
             't_id': 984,
             'area_terreno': 2614.3,
             'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                              'documento_identidad': '9',
                              'nombre': '9 9primer apellido 9segundo apellido 9primer nombre 9segundo nombre',
                              'derecho': 'Dominio'}]}, {'departamento': '25',
                                                        'matricula_inmobiliaria': NULL,
                                                        'numero_predial': '253940000000000230241000000000',
                                                        'condicion_predio': 'NPH',
                                                        'nombre': 'SIN INFO',
                                                        't_id': 985,
                                                        'area_terreno': 11087.8,
                                                        'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                         'documento_identidad': '27',
                                                                         'nombre': '27 27primer apellido 27segundo apellido 27primer nombre 27segundo nombre',
                                                                         'derecho': 'Dominio'}]}, {'departamento': '25',
                                                                                                   'matricula_inmobiliaria': NULL,
                                                                                                   'numero_predial': '253940000000000230241000000000',
                                                                                                   'condicion_predio': 'NPH',
                                                                                                   'nombre': 'SIN INFO',
                                                                                                   't_id': 986,
                                                                                                   'area_terreno': 15073.7,
                                                                                                   'Interesados': [{
                                                                                                                       'tipo_documento': 'Cedula_Ciudadania',
                                                                                                                       'documento_identidad': '13',
                                                                                                                       'nombre': '13 13primer apellido 13segundo apellido 13primer nombre 13segundo nombre',
                                                                                                                       'derecho': 'Dominio'}]},
            {'departamento': '25',
             'matricula_inmobiliaria': NULL,
             'numero_predial': '253940000000000230241000000000',
             'condicion_predio': 'NPH',
             'nombre': 'SIN INFO',
             't_id': 987,
             'area_terreno': 2234.3,
             'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                              'documento_identidad': '34',
                              'nombre': '34 34primer apellido 34segundo apellido 34primer nombre 34segundo nombre',
                              'derecho': 'Dominio'}]}, {'departamento': '25',
                                                        'matricula_inmobiliaria': NULL,
                                                        'numero_predial': '253940000000000230241000000000',
                                                        'condicion_predio': 'NPH',
                                                        'nombre': 'El Tigre',
                                                        't_id': 988,
                                                        'area_terreno': 4200.0,
                                                        'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                         'documento_identidad': '20',
                                                                         'nombre': '20 20primer apellido 20segundo apellido 20primer nombre 20segundo nombre',
                                                                         'derecho': 'Dominio'}]}, {'departamento': '25',
                                                                                                   'matricula_inmobiliaria': NULL,
                                                                                                   'numero_predial': '253940000000000230241000000000',
                                                                                                   'condicion_predio': 'NPH',
                                                                                                   'nombre': 'SIN INFO',
                                                                                                   't_id': 992,
                                                                                                   'area_terreno': 4814.4,
                                                                                                   'Interesados': [{
                                                                                                                       'tipo_documento': 'Cedula_Ciudadania',
                                                                                                                       'documento_identidad': '22',
                                                                                                                       'nombre': '22 22primer apellido 22segundo apellido 22primer nombre 22segundo nombre',
                                                                                                                       'derecho': 'Dominio'}]},
            {'departamento': '25',
             'matricula_inmobiliaria': NULL,
             'numero_predial': '253940000000000230241000000000',
             'condicion_predio': 'NPH',
             'nombre': 'Angel',
             't_id': 993,
             'area_terreno': 10495.1,
             'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                              'documento_identidad': '21',
                              'nombre': '21 21primer apellido 21segundo apellido 21primer nombre 21segundo nombre',
                              'derecho': 'Dominio'}]}],
            '253940000000000230072000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230072000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'El Porvenir',
                                                't_id': 951,
                                                'area_terreno': 21907.6,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '24',
                                                                 'nombre': '24 24primer apellido 24segundo apellido 24primer nombre 24segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000230234000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230234000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'SIN INFO',
                                                't_id': 952,
                                                'area_terreno': 3902.1,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '18',
                                                                 'nombre': '18 18primer apellido 18segundo apellido 18primer nombre 18segundo nombre',
                                                                 'derecho': 'Dominio'}]}, {'departamento': '25',
                                                                                           'matricula_inmobiliaria': NULL,
                                                                                           'numero_predial': '253940000000000230234000000000',
                                                                                           'condicion_predio': 'NPH',
                                                                                           'nombre': 'SIN INFO',
                                                                                           't_id': 991,
                                                                                           'area_terreno': 3056.5,
                                                                                           'Interesados': [{
                                                                                                               'tipo_documento': 'Cedula_Ciudadania',
                                                                                                               'documento_identidad': '34',
                                                                                                               'nombre': '34 34primer apellido 34segundo apellido 34primer nombre 34segundo nombre',
                                                                                                               'derecho': 'Dominio'}]}],
            '253940000000000230099000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230099000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'Santa Lucia',
                                                't_id': 955,
                                                'area_terreno': 2301.5,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '16',
                                                                 'nombre': '16 16primer apellido 16segundo apellido 16primer nombre 16segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000230100000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230100000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'SIN INFO',
                                                't_id': 956,
                                                'area_terreno': 1210.6,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '29',
                                                                 'nombre': '29 29primer apellido 29segundo apellido 29primer nombre 29segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000230101000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230101000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'Santa Lucia',
                                                't_id': 957,
                                                'area_terreno': 749.7,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '9',
                                                                 'nombre': '9 9primer apellido 9segundo apellido 9primer nombre 9segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000230068000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230068000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'Tudelita',
                                                't_id': 958,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '3',
                                                                 'nombre': '3 3primer apellido 3segundo apellido 3primer nombre 3segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000230081000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230081000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'Santa Lucia',
                                                't_id': 959,
                                                'area_terreno': 2267.4,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '17',
                                                                 'nombre': '17 17primer apellido 17segundo apellido 17primer nombre 17segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000230082000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230082000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'Santa Lucia',
                                                't_id': 960,
                                                'area_terreno': 2455.3,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '30',
                                                                 'nombre': '30 30primer apellido 30segundo apellido 30primer nombre 30segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000230070000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230070000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'Bellavista',
                                                't_id': 961,
                                                'area_terreno': 5375.3,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '16',
                                                                 'nombre': '16 16primer apellido 16segundo apellido 16primer nombre 16segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000230069000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230069000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'Las Juntas',
                                                't_id': 962,
                                                'area_terreno': 1808.1,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '9',
                                                                 'nombre': '9 9primer apellido 9segundo apellido 9primer nombre 9segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000230077000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230077000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'SIN INFO',
                                                't_id': 963,
                                                'area_terreno': 6068.6,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '19',
                                                                 'nombre': '19 19primer apellido 19segundo apellido 19primer nombre 19segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000230078000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230078000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'Santa Lucia',
                                                't_id': 964,
                                                'area_terreno': 1974.4,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '33',
                                                                 'nombre': '33 33primer apellido 33segundo apellido 33primer nombre 33segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000230079000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230079000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'Santa Lucia',
                                                't_id': 965,
                                                'area_terreno': 1453.9,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '32',
                                                                 'nombre': '32 32primer apellido 32segundo apellido 32primer nombre 32segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000230080000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230080000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'Santa Lucia',
                                                't_id': 966,
                                                'area_terreno': 2330.8,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '31',
                                                                 'nombre': '31 31primer apellido 31segundo apellido 31primer nombre 31segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000230057000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230057000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'SIN INFO',
                                                't_id': 968,
                                                'area_terreno': 7691.6,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '13',
                                                                 'nombre': '13 13primer apellido 13segundo apellido 13primer nombre 13segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000230056000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230056000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'El Almorzadero',
                                                't_id': 969,
                                                'area_terreno': 7983.2,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '13',
                                                                 'nombre': '13 13primer apellido 13segundo apellido 13primer nombre 13segundo nombre',
                                                                 'derecho': 'Dominio'}]}, {'departamento': '25',
                                                                                           'matricula_inmobiliaria': NULL,
                                                                                           'numero_predial': '253940000000000230056000000000',
                                                                                           'condicion_predio': 'NPH',
                                                                                           'nombre': 'El Volador',
                                                                                           't_id': 970,
                                                                                           'area_terreno': 8103.5,
                                                                                           'Interesados': [{
                                                                                                               'tipo_documento': 'Cedula_Ciudadania',
                                                                                                               'documento_identidad': '12',
                                                                                                               'nombre': '12 12primer apellido 12segundo apellido 12primer nombre 12segundo nombre',
                                                                                                               'derecho': 'Dominio'}]}],
            '253940000000000230213000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230213000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'El Volador',
                                                't_id': 971,
                                                'area_terreno': 11157.6,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '23',
                                                                 'nombre': '23 23primer apellido 23segundo apellido 23primer nombre 23segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000230098000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230098000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'Santa Lucía',
                                                't_id': 972,
                                                'area_terreno': 1320.4,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '1',
                                                                 'nombre': '1 1primer apellido 1segundo apellido 1primer nombre 1segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000230097000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230097000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'SIN INFO',
                                                't_id': 973,
                                                'area_terreno': 25178.2,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '23',
                                                                 'nombre': '23 23primer apellido 23segundo apellido 23primer nombre 23segundo nombre',
                                                                 'derecho': 'Dominio'}]}, {'departamento': '25',
                                                                                           'matricula_inmobiliaria': NULL,
                                                                                           'numero_predial': '253940000000000230097000000000',
                                                                                           'condicion_predio': 'NPH',
                                                                                           'nombre': 'Santa Lucía',
                                                                                           't_id': 976,
                                                                                           'area_terreno': 904.8,
                                                                                           'Interesados': [{
                                                                                                               'tipo_documento': 'Cedula_Ciudadania',
                                                                                                               'documento_identidad': '2',
                                                                                                               'nombre': '2 2primer apellido 2segundo apellido 2primer nombre 2segundo nombre',
                                                                                                               'derecho': 'Dominio'}]}],
            '253940000000000230257000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230257000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'Casimiro',
                                                't_id': 974,
                                                'area_terreno': 10986.0,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '7',
                                                                 'nombre': '7 7primer apellido 7segundo apellido 7primer nombre 7segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000230054000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230054000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'San Pedro',
                                                't_id': 975,
                                                'area_terreno': 49379.0,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '6',
                                                                 'nombre': '6 6primer apellido 6segundo apellido 6primer nombre 6segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000230074000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230074000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'Tudelita',
                                                't_id': 977,
                                                'area_terreno': 10006.6,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '3',
                                                                 'nombre': '3 3primer apellido 3segundo apellido 3primer nombre 3segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000230254000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230254000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'El Muche',
                                                't_id': 978,
                                                'area_terreno': 59108.5,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '10',
                                                                 'nombre': '10 10primer apellido 10segundo apellido 10primer nombre 10segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000230235000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230235000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'Los Naranjos',
                                                't_id': 979,
                                                'area_terreno': 5473.0,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '1',
                                                                 'nombre': '1 1primer apellido 1segundo apellido 1primer nombre 1segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000230055000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230055000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'El Volador',
                                                't_id': 982,
                                                'area_terreno': 70502.4,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '11',
                                                                 'nombre': '11 11primer apellido 11segundo apellido 11primer nombre 11segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000230242000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230242000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'El Guamal',
                                                't_id': 983,
                                                'area_terreno': 6085.7,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '10',
                                                                 'nombre': '10 10primer apellido 10segundo apellido 10primer nombre 10segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000320022000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000320022000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'Escuela Alto de Izacar',
                                                't_id': 989,
                                                'area_terreno': 1377.2,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '13',
                                                                 'nombre': '13 13primer apellido 13segundo apellido 13primer nombre 13segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000230076000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230076000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'Santa Lucia',
                                                't_id': 990,
                                                'area_terreno': 12960.6,
                                                'Interesados': NULL}],
            '253940000000000230241000000994': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230241000000994',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'Bajo',
                                                't_id': 994,
                                                'area_terreno': 12095.4,
                                                'Interesados': NULL}],
            '253940000000000230241000000995': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230241000000995',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'Vía Interveredal',
                                                't_id': 995,
                                                'area_terreno': 7520.3,
                                                'Interesados': NULL}],
            '253940000000000230241000000996': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230241000000996',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'Camino',
                                                't_id': 996,
                                                'area_terreno': 2032.3,
                                                'Interesados': NULL}],
            '253940000000000230241000000997': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230241000000997',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'Camino',
                                                't_id': 997,
                                                'area_terreno': 3291.9,
                                                'Interesados': NULL}],
            '253940000000000230073000000000': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230073000000000',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'El Pomarroso',
                                                't_id': 998,
                                                'area_terreno': 4934.3,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '4',
                                                                 'nombre': '4 4primer apellido 4segundo apellido 4primer nombre 4segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000230241000000998': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230241000000998',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'Apartamento 202',
                                                't_id': 999,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '17',
                                                                 'nombre': '17 17primer apellido 17segundo apellido 17primer nombre 17segundo nombre',
                                                                 'derecho': 'Dominio'}]}],
            '253940000000000230241000000999': [{'departamento': '25',
                                                'matricula_inmobiliaria': NULL,
                                                'numero_predial': '253940000000000230241000000999',
                                                'condicion_predio': 'NPH',
                                                'nombre': 'Apartamento 101',
                                                't_id': 1000,
                                                'Interesados': [{'tipo_documento': 'Cedula_Ciudadania',
                                                                 'documento_identidad': '22',
                                                                 'nombre': '22 22primer apellido 22segundo apellido 22primer nombre 22segundo nombre',
                                                                 'derecho': 'Dominio'}]}]}
        features = self.ladm_data.get_parcel_data_to_compare_changes(self.db_pg)
        self.assertCountEqual(features, features_test)

        print("\nINFO: Validating get parcels data using search criterion...")

        features_test = {'253940000000000230055000000000':
            [
                {'departamento': '25',
                 'matricula_inmobiliaria': NULL,
                 'numero_predial': '253940000000000230055000000000',
                 'condicion_predio': 'NPH',
                 'nombre': 'El Volador',
                 't_id': 982,
                 'area_terreno': 70502.4,
                 'Interesados': [
                     {'tipo_documento': 'Cedula_Ciudadania',
                      'documento_identidad': '11',
                      'nombre': '11 11primer apellido 11segundo apellido 11primer nombre 11segundo nombre',
                      'derecho': 'Dominio'
                      }
                 ]
                 }
            ]
        }
        search_criterion = {self.names.OP_PARCEL_T_PARCEL_NUMBER_F: '253940000000000230055000000000'}
        features = self.ladm_data.get_parcel_data_to_compare_changes(self.db_pg, search_criterion=search_criterion)
        self.assertCountEqual(features, features_test)

        features_test = {'253940000000000230241000000000':
            [
                {'departamento': '25',
                 'matricula_inmobiliaria': NULL,
                 'numero_predial': '253940000000000230241000000000',
                 'condicion_predio': 'NPH',
                 'nombre': 'Hoya Las Juntas',
                 't_id': 950,
                 'area_terreno': 7307.3,
                 'Interesados': [
                     {'tipo_documento': 'Cedula_Ciudadania',
                      'documento_identidad': '14',
                      'nombre': '14 14primer apellido 14segundo apellido 14primer nombre 14segundo nombre',
                      'derecho': 'Dominio'
                      },
                     {'tipo_documento': 'Cedula_Ciudadania',
                      'documento_identidad': '2',
                      'nombre': '2 2primer apellido 2segundo apellido 2primer nombre 2segundo nombre',
                      'derecho': 'Dominio'
                      }
                 ]
                 },
                {'departamento': '25',
                 'matricula_inmobiliaria': NULL,
                 'numero_predial': '253940000000000230241000000000',
                 'condicion_predio': 'NPH',
                 'nombre': 'SIN INFO',
                 't_id': 953,
                 'area_terreno': 4283.7,
                 'Interesados': [
                     {'tipo_documento': 'Cedula_Ciudadania',
                      'documento_identidad': '14',
                      'nombre': '14 14primer apellido 14segundo apellido 14primer nombre 14segundo nombre',
                      'derecho': 'Dominio'
                      }
                 ]
                 },
                {'departamento': '25',
                 'matricula_inmobiliaria': NULL,
                 'numero_predial': '253940000000000230241000000000',
                 'condicion_predio': 'NPH',
                 'nombre': 'Tudela Juntas',
                 't_id': 954,
                 'area_terreno': 30777.3,
                 'Interesados': [
                     {'tipo_documento': 'Cedula_Ciudadania',
                      'documento_identidad': '28',
                      'nombre': '28 28primer apellido 28segundo apellido 28primer nombre 28segundo nombre',
                      'derecho': 'Dominio'
                      }
                 ]
                 },
                {'departamento': '25',
                 'matricula_inmobiliaria': NULL,
                 'numero_predial': '253940000000000230241000000000',
                 'condicion_predio': 'NPH',
                 'nombre': 'Mardoqueo',
                 't_id': 967,
                 'area_terreno': 877.9,
                 'Interesados': [
                     {'tipo_documento': 'Cedula_Ciudadania',
                      'documento_identidad': '35',
                      'nombre': '35 35primer apellido 35segundo apellido 35primer nombre 35segundo nombre',
                      'derecho': 'Dominio'
                      }
                 ]
                 },
                {'departamento': '25',
                 'matricula_inmobiliaria': NULL,
                 'numero_predial': '253940000000000230241000000000',
                 'condicion_predio': 'NPH',
                 'nombre': 'SIN INFO',
                 't_id': 980,
                 'area_terreno': 818.8,
                 'Interesados': [
                     {'tipo_documento': 'Cedula_Ciudadania',
                      'documento_identidad': '26',
                      'nombre': '26 26primer apellido 26segundo apellido 26primer nombre 26segundo nombre',
                      'derecho': 'Dominio'
                      }
                 ]
                 },
                {'departamento': '25',
                 'matricula_inmobiliaria': NULL,
                 'numero_predial': '253940000000000230241000000000',
                 'condicion_predio': 'NPH',
                 'nombre': 'SIN INFO',
                 't_id': 981,
                 'area_terreno': 967.1,
                 'Interesados': [
                     {'tipo_documento': 'Cedula_Ciudadania',
                      'documento_identidad': '25',
                      'nombre': '25 25primer apellido 25segundo apellido 25primer nombre 25segundo nombre',
                      'derecho': 'Dominio'
                      }
                 ]
                 },
                {'departamento': '25',
                 'matricula_inmobiliaria': NULL,
                 'numero_predial': '253940000000000230241000000000',
                 'condicion_predio': 'NPH',
                 'nombre': 'SIN INFO',
                 't_id': 984,
                 'area_terreno': 2614.3,
                 'Interesados': [
                     {'tipo_documento': 'Cedula_Ciudadania',
                      'documento_identidad': '9',
                      'nombre': '9 9primer apellido 9segundo apellido 9primer nombre 9segundo nombre',
                      'derecho': 'Dominio'
                      }
                 ]
                 },
                {'departamento': '25',
                 'matricula_inmobiliaria': NULL,
                 'numero_predial': '253940000000000230241000000000',
                 'condicion_predio': 'NPH',
                 'nombre': 'SIN INFO',
                 't_id': 985,
                 'area_terreno': 11087.8,
                 'Interesados': [
                     {'tipo_documento': 'Cedula_Ciudadania',
                      'documento_identidad': '27',
                      'nombre': '27 27primer apellido 27segundo apellido 27primer nombre 27segundo nombre',
                      'derecho': 'Dominio'
                      }
                 ]
                 },
                {'departamento': '25',
                 'matricula_inmobiliaria': NULL,
                 'numero_predial': '253940000000000230241000000000',
                 'condicion_predio': 'NPH',
                 'nombre': 'SIN INFO',
                 't_id': 986,
                 'area_terreno': 15073.7,
                 'Interesados': [
                     {'tipo_documento': 'Cedula_Ciudadania',
                      'documento_identidad': '13',
                      'nombre': '13 13primer apellido 13segundo apellido 13primer nombre 13segundo nombre',
                      'derecho': 'Dominio'
                      }
                 ]
                 },
                {'departamento': '25',
                 'matricula_inmobiliaria': NULL,
                 'numero_predial': '253940000000000230241000000000',
                 'condicion_predio': 'NPH',
                 'nombre': 'SIN INFO',
                 't_id': 987,
                 'area_terreno': 2234.3,
                 'Interesados': [
                     {'tipo_documento': 'Cedula_Ciudadania',
                      'documento_identidad': '34',
                      'nombre': '34 34primer apellido 34segundo apellido 34primer nombre 34segundo nombre',
                      'derecho': 'Dominio'
                      }
                 ]
                 },
                {'departamento': '25',
                 'matricula_inmobiliaria': NULL,
                 'numero_predial': '253940000000000230241000000000',
                 'condicion_predio': 'NPH',
                 'nombre': 'El Tigre',
                 't_id': 988,
                 'area_terreno': 4200.0,
                 'Interesados': [
                     {'tipo_documento': 'Cedula_Ciudadania',
                      'documento_identidad': '20',
                      'nombre': '20 20primer apellido 20segundo apellido 20primer nombre 20segundo nombre',
                      'derecho': 'Dominio'
                      }
                 ]
                 },
                {'departamento': '25',
                 'matricula_inmobiliaria': NULL,
                 'numero_predial': '253940000000000230241000000000',
                 'condicion_predio': 'NPH',
                 'nombre': 'SIN INFO',
                 't_id': 992,
                 'area_terreno': 4814.4,
                 'Interesados': [
                     {'tipo_documento': 'Cedula_Ciudadania',
                      'documento_identidad': '22',
                      'nombre': '22 22primer apellido 22segundo apellido 22primer nombre 22segundo nombre',
                      'derecho': 'Dominio'
                      }
                 ]
                 },
                {'departamento': '25',
                 'matricula_inmobiliaria': NULL,
                 'numero_predial': '253940000000000230241000000000',
                 'condicion_predio': 'NPH',
                 'nombre': 'Angel',
                 't_id': 993,
                 'area_terreno': 10495.1,
                 'Interesados': [
                     {'tipo_documento': 'Cedula_Ciudadania',
                      'documento_identidad': '21',
                      'nombre': '21 21primer apellido 21segundo apellido 21primer nombre 21segundo nombre',
                      'derecho': 'Dominio'
                      }
                 ]
                 }
            ]
        }
        search_criterion = {self.names.OP_PARCEL_T_PARCEL_NUMBER_F: '253940000000000230241000000000'}
        features = self.ladm_data.get_parcel_data_to_compare_changes(self.db_pg, search_criterion=search_criterion)
        self.assertCountEqual(features, features_test)

    def tearDownClass():
        print('tearDown test_ladm_data')


if __name__ == '__main__':
    nose2.main()
