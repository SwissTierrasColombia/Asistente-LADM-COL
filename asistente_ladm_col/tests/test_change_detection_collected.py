import nose2

from qgis.core import QgsWkbTypes, NULL
from qgis.testing import (start_app,
                          unittest)

start_app()  # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.utils.qgis_utils import QGISUtils
from asistente_ladm_col.logic.ladm_col.ladm_data import LADM_DATA
from asistente_ladm_col.config.general_config import (LAYER,
                                                      LAYER_NAME)
from asistente_ladm_col.tests.utils import (get_pg_conn,
                                            normalize_response,
                                            restore_schema)


class TestChangeDetectionsCollected(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("INFO: Restoring databases to be used")
        restore_schema('test_ladm_col_queries')
        cls.db_pg = get_pg_conn('test_ladm_col_queries')
        result = cls.db_pg.test_connection()
        print('test_connection', result)

        if not result[1]:
            print('The test connection is not working')
            return

        cls.qgis_utils = QGISUtils()
        cls.ladm_data = LADM_DATA(cls.qgis_utils)
        cls.names = cls.db_pg.names

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
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'Hoya Las Juntas',
                    't_id': 950,
                    'area_terreno': 7307.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963516.16099999996367842 1077366.59700000006705523 0, 963506.0849999999627471 1077369.162999999942258 0, 963485.87699999997857958 1077390.93900000001303852 0, 963500.4599999999627471 1077410.17100000008940697 0, 963527.53599999996367842 1077431.21600000001490116 0, 963565.55200000002514571 1077469.65299999993294477 0, 963584.20700000005308539 1077451.68500000005587935 0, 963621.47600000002421439 1077426.2099999999627471 0, 963554.02000000001862645 1077366.51099999994039536 0, 963516.16099999996367842 1077366.59700000006705523 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '14',
                            'nombre': '14 14primer apellido 14segundo apellido 14primer nombre 14segundo nombre',
                            'derecho': 'Dominio'
                        },
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '2',
                            'nombre': '2 2primer apellido 2segundo apellido 2primer nombre 2segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'SIN INFO',
                    't_id': 953,
                    'area_terreno': 4283.7,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963546.46100000001024455 1077303.26099999994039536 0, 963614.23899999994318932 1077313.6720000000204891 0, 963631.17900000000372529 1077251.375 0, 963599.68200000002980232 1077224.26600000006146729 0, 963568.8279999999795109 1077265.58799999998882413 0, 963546.46100000001024455 1077303.26099999994039536 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '14',
                            'nombre': '14 14primer apellido 14segundo apellido 14primer nombre 14segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'Tudela Juntas',
                    't_id': 954,
                    'area_terreno': 30777.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963614.21100000001024455 1077128.07300000009126961 0, 963621.731000000028871 1077122.64299999992363155 0, 963636.30599999998230487 1077091.95699999993667006 0, 963646.0779999999795109 1077074.34799999999813735 0, 963722.36800000001676381 1077109.49200000008568168 0, 963746.39000000001396984 1077120.55799999996088445 0, 963779.01500000001396984 1077150.40100000007078052 0, 963775.98699999996460974 1077246.03000000002793968 0, 963728.30599999998230487 1077270.02099999994970858 0, 963713.56299999996554106 1077292.69299999997019768 0, 963680.36800000001676381 1077320.8279999999795109 0, 963675.40200000000186265 1077331.09499999997206032 0, 963614.23899999994318932 1077313.6720000000204891 0, 963631.17900000000372529 1077251.375 0, 963599.68200000002980232 1077224.26600000006146729 0, 963543.20499999995809048 1077199.95500000007450581 0, 963559.68099999998230487 1077171.38700000010430813 0, 963575.67700000002514571 1077153.21299999998882413 0, 963580.79899999999906868 1077147.70200000004842877 0, 963624.64899999997578561 1077205.93399999989196658 0, 963655.29200000001583248 1077187.44900000002235174 0, 963671.17500000004656613 1077163.80899999989196658 0, 963659.34199999994598329 1077146.59199999994598329 0, 963614.21100000001024455 1077128.07300000009126961 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '28',
                            'nombre': '28 28primer apellido 28segundo apellido 28primer nombre 28segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'Mardoqueo',
                    't_id': 967,
                    'area_terreno': 877.9,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963372.00699999998323619 1077487.31899999990127981 0, 963408.11999999999534339 1077525.30600000009872019 0, 963397.95700000005308539 1077538.45399999991059303 0, 963361.71600000001490116 1077499.76399999996647239 0, 963365.61999999999534339 1077490.59400000004097819 0, 963372.00699999998323619 1077487.31899999990127981 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '35',
                            'nombre': '35 35primer apellido 35segundo apellido 35primer nombre 35segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'SIN INFO',
                    't_id': 980,
                    'area_terreno': 818.8,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963361.71600000001490116 1077499.76399999996647239 0, 963397.95700000005308539 1077538.45399999991059303 0, 963387.60900000005494803 1077549.35599999991245568 0, 963376.43999999994412065 1077537.31899999990127981 0, 963350.61800000001676381 1077510.51300000003539026 0, 963357.74899999995250255 1077501.35599999991245568 0, 963361.71600000001490116 1077499.76399999996647239 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '26',
                            'nombre': '26 26primer apellido 26segundo apellido 26primer nombre 26segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'SIN INFO',
                    't_id': 981,
                    'area_terreno': 967.1,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963350.61800000001676381 1077510.51300000003539026 0, 963376.43999999994412065 1077537.31899999990127981 0, 963366.17900000000372529 1077551.52399999997578561 0, 963326.04799999995157123 1077528.81300000008195639 0, 963350.61800000001676381 1077510.51300000003539026 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '25',
                            'nombre': '25 25primer apellido 25segundo apellido 25primer nombre 25segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'SIN INFO',
                    't_id': 984,
                    'area_terreno': 2614.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963500.4599999999627471 1077410.17100000008940697 0, 963527.53599999996367842 1077431.21600000001490116 0, 963565.55200000002514571 1077469.65299999993294477 0, 963547.99399999994784594 1077479.15400000009685755 0, 963503.45900000003166497 1077453.82899999991059303 0, 963468.768999999971129 1077434.62100000004284084 0, 963500.4599999999627471 1077410.17100000008940697 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '9',
                            'nombre': '9 9primer apellido 9segundo apellido 9primer nombre 9segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'SIN INFO',
                    't_id': 985,
                    'area_terreno': 11087.8,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963376.43999999994412065 1077537.31899999990127981 0, 963387.60900000005494803 1077549.35599999991245568 0, 963381.56999999994877726 1077567.29799999995157123 0, 963429.6530000000493601 1077597.34000000008381903 0, 963351.8349999999627471 1077674.02700000000186265 0, 963319.83799999998882413 1077633.80499999993480742 0, 963301.96100000001024455 1077606.56499999994412065 0, 963279.78099999995902181 1077578.49699999997392297 0, 963290.25899999996181577 1077565.4150000000372529 0, 963305.4220000000204891 1077553.60199999995529652 0, 963308.26800000004004687 1077549.42999999993480742 0, 963310.42399999999906868 1077542.57000000006519258 0, 963319.70100000000093132 1077531.6720000000204891 0, 963326.04799999995157123 1077528.81300000008195639 0, 963366.17900000000372529 1077551.52399999997578561 0, 963376.43999999994412065 1077537.31899999990127981 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '27',
                            'nombre': '27 27primer apellido 27segundo apellido 27primer nombre 27segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'SIN INFO',
                    't_id': 986,
                    'area_terreno': 15073.7,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963722.36800000001676381 1077109.49200000008568168 0, 963740.38399999996181577 1077099.46900000004097819 0, 963766.875 1077090.20900000003166497 0, 963776.40000000002328306 1077088.09199999994598329 0, 963792.01000000000931323 1077089.28300000005401671 0, 963805.37199999997392297 1077094.04600000008940697 0, 963815.55799999996088445 1077099.46900000004097819 0, 963840.69400000001769513 1077119.7099999999627471 0, 963854.31999999994877726 1077127.91200000001117587 0, 963871.58299999998416752 1077130.39400000008754432 0, 963900.98300000000745058 1077206.71800000010989606 0, 963858.20100000000093132 1077230.7479999999050051 0, 963775.98699999996460974 1077246.03000000002793968 0, 963779.01500000001396984 1077150.40100000007078052 0, 963746.39000000001396984 1077120.55799999996088445 0, 963722.36800000001676381 1077109.49200000008568168 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '13',
                            'nombre': '13 13primer apellido 13segundo apellido 13primer nombre 13segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'SIN INFO',
                    't_id': 987,
                    'area_terreno': 2234.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963279.78099999995902181 1077578.49699999997392297 0, 963301.96100000001024455 1077606.56499999994412065 0, 963285.63100000005215406 1077621.23699999996460974 0, 963264.13800000003539026 1077649.62100000004284084 0, 963235.52300000004470348 1077621.91599999996833503 0, 963242.00500000000465661 1077610.7590000000782311 0, 963264.23600000003352761 1077593.90999999991618097 0, 963279.78099999995902181 1077578.49699999997392297 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '34',
                            'nombre': '34 34primer apellido 34segundo apellido 34primer nombre 34segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'El Tigre',
                    't_id': 988,
                    'area_terreno': 4200.0,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963479.16000000003259629 1077351.29499999992549419 0, 963506.0849999999627471 1077369.162999999942258 0, 963485.87699999997857958 1077390.93900000001303852 0, 963500.4599999999627471 1077410.17100000008940697 0, 963468.768999999971129 1077434.62100000004284084 0, 963418.89699999999720603 1077419.45200000004842877 0, 963428.88600000005681068 1077398.67800000007264316 0, 963438.72800000000279397 1077382.81899999990127981 0, 963458.00300000002607703 1077360.37400000006891787 0, 963479.16000000003259629 1077351.29499999992549419 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '20',
                            'nombre': '20 20primer apellido 20segundo apellido 20primer nombre 20segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'SIN INFO',
                    't_id': 992,
                    'area_terreno': 4814.4,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963479.16000000003259629 1077351.29499999992549419 0, 963492.73300000000745058 1077318.97299999999813735 0, 963498.00300000002607703 1077309.83799999998882413 0, 963502.98400000005494803 1077297.89400000008754432 0, 963508.81099999998696148 1077274.89100000006146729 0, 963519.10400000005029142 1077256.44800000009126961 0, 963568.8279999999795109 1077265.58799999998882413 0, 963546.46100000001024455 1077303.26099999994039536 0, 963516.16099999996367842 1077366.59700000006705523 0, 963506.0849999999627471 1077369.162999999942258 0, 963479.16000000003259629 1077351.29499999992549419 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '22',
                            'nombre': '22 22primer apellido 22segundo apellido 22primer nombre 22segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'Angel',
                    't_id': 993,
                    'area_terreno': 10495.1,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963418.89699999999720603 1077419.45200000004842877 0, 963468.768999999971129 1077434.62100000004284084 0, 963503.45900000003166497 1077453.82899999991059303 0, 963547.99399999994784594 1077479.15400000009685755 0, 963523.76100000005681068 1077504.57199999992735684 0, 963494.36399999994318932 1077519.02499999990686774 0, 963428.65200000000186265 1077489.20200000004842877 0, 963408.11999999999534339 1077525.30600000009872019 0, 963372.00699999998323619 1077487.31899999990127981 0, 963386.11399999994318932 1077448.76699999999254942 0, 963414.26300000003539026 1077422.27300000004470348 0, 963418.89699999999720603 1077419.45200000004842877 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '21',
                            'nombre': '21 21primer apellido 21segundo apellido 21primer nombre 21segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230072000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230072000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'El Porvenir',
                    't_id': 951,
                    'area_terreno': 21907.6,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963424.84900000004563481 1077377.26900000008754432 0, 963449.61999999999534339 1077352.06000000005587935 0, 963400.06099999998696148 1077310.90299999993294477 0, 963434.03000000002793968 1077254.76900000008754432 0, 963495.65800000005401671 1077274.45900000003166497 0, 963496.32099999999627471 1077252.37199999997392297 0, 963497 1077239.97500000009313226 0, 963504.01000000000931323 1077221.72799999988637865 0, 963420.13100000005215406 1077187.15599999995902181 0, 963400.52099999994970858 1077215.42699999990873039 0, 963378.57999999995809048 1077281.69500000006519258 0, 963343.66099999996367842 1077330.41599999996833503 0, 963424.84900000004563481 1077377.26900000008754432 0)),((963376.02899999998044223 1077279.62599999993108213 0, 963396.74800000002142042 1077213.01600000006146729 0, 963415.96799999999348074 1077184.47699999995529652 0, 963368.31900000001769513 1077155.28499999991618097 0, 963355.23300000000745058 1077168.81099999998696148 0, 963247.04200000001583248 1077094.51699999999254942 0, 963239.31900000001769513 1077113.19900000002235174 0, 963257.85199999995529652 1077132.22600000002421439 0, 963259.08299999998416752 1077133.05600000009872019 0, 963329.412999999942258 1077175.15400000009685755 0, 963304.04799999995157123 1077221.2590000000782311 0, 963376.02899999998044223 1077279.62599999993108213 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '24',
                            'nombre': '24 24primer apellido 24segundo apellido 24primer nombre 24segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230234000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230234000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'SIN INFO',
                    't_id': 952,
                    'area_terreno': 3902.1,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963614.21100000001024455 1077128.07300000009126961 0, 963659.34199999994598329 1077146.59199999994598329 0, 963671.17500000004656613 1077163.80899999989196658 0, 963655.29200000001583248 1077187.44900000002235174 0, 963624.64899999997578561 1077205.93399999989196658 0, 963580.79899999999906868 1077147.70200000004842877 0, 963586.19900000002235174 1077146.11000000010244548 0, 963614.21100000001024455 1077128.07300000009126961 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '18',
                            'nombre': '18 18primer apellido 18segundo apellido 18primer nombre 18segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230234000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'SIN INFO',
                    't_id': 991,
                    'area_terreno': 3056.5,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963543.20499999995809048 1077199.95500000007450581 0, 963519.10400000005029142 1077256.44800000009126961 0, 963568.8279999999795109 1077265.58799999998882413 0, 963599.68200000002980232 1077224.26600000006146729 0, 963543.20499999995809048 1077199.95500000007450581 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '34',
                            'nombre': '34 34primer apellido 34segundo apellido 34primer nombre 34segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230099000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230099000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'Santa Lucia',
                    't_id': 955,
                    'area_terreno': 2301.5,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963166.65599999995902181 1077249.80199999990873039 0, 963170.24699999997392297 1077250.36299999989569187 0, 963198.3349999999627471 1077258.8840000000782311 0, 963203.76399999996647239 1077262.1720000000204891 0, 963228.04099999996833503 1077278.587000000057742 0, 963247.5659999999916181 1077294.32899999991059303 0, 963236.87800000002607703 1077314.79399999999441206 0, 963163.49899999995250255 1077270.92699999990873039 0, 963166.65599999995902181 1077249.80199999990873039 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '16',
                            'nombre': '16 16primer apellido 16segundo apellido 16primer nombre 16segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230100000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230100000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'SIN INFO',
                    't_id': 956,
                    'area_terreno': 1210.6,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963163.49899999995250255 1077270.92699999990873039 0, 963236.87800000002607703 1077314.79399999999441206 0, 963230.50699999998323619 1077324.55300000007264316 0, 963163.99199999996926636 1077292.59700000006705523 0, 963163.49899999995250255 1077270.92699999990873039 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '29',
                            'nombre': '29 29primer apellido 29segundo apellido 29primer nombre 29segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230101000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230101000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'Santa Lucia',
                    't_id': 957,
                    'area_terreno': 749.7,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963163.99199999996926636 1077292.59700000006705523 0, 963230.50699999998323619 1077324.55300000007264316 0, 963223.85800000000745058 1077331.60000000009313226 0, 963167.14199999999254942 1077308.31899999990127981 0, 963163.99199999996926636 1077292.59700000006705523 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '9',
                            'nombre': '9 9primer apellido 9segundo apellido 9primer nombre 9segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230068000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230068000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'Tudelita',
                    't_id': 958,
                    'GEOMETRY_PLOT': None,
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '3',
                            'nombre': '3 3primer apellido 3segundo apellido 3primer nombre 3segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230081000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230081000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'Santa Lucia',
                    't_id': 959,
                    'area_terreno': 2267.4,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963438.18200000002980232 1077161.11199999996460974 0, 963461.71299999998882413 1077144.55099999997764826 0, 963528.16599999996833503 1077177.04399999999441206 0, 963529.96400000003632158 1077195.14199999999254942 0, 963517.43099999998230487 1077202.15400000009685755 0, 963438.18200000002980232 1077161.11199999996460974 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '17',
                            'nombre': '17 17primer apellido 17segundo apellido 17primer nombre 17segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230082000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230082000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'Santa Lucia',
                    't_id': 960,
                    'area_terreno': 2455.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963438.18200000002980232 1077161.11199999996460974 0, 963517.43099999998230487 1077202.15400000009685755 0, 963504.01000000000931323 1077221.72799999988637865 0, 963420.13100000005215406 1077187.15599999995902181 0, 963438.18200000002980232 1077161.11199999996460974 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '30',
                            'nombre': '30 30primer apellido 30segundo apellido 30primer nombre 30segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230070000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230070000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'Bellavista',
                    't_id': 961,
                    'area_terreno': 5375.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963319.42000000004190952 1077382.33199999993667006 0, 963343.66099999996367842 1077330.41599999996833503 0, 963424.84900000004563481 1077377.26900000008754432 0, 963424.43500000005587935 1077378.12199999997392297 0, 963393.06000000005587935 1077424.39999999990686774 0, 963388.79500000004190952 1077427.97399999992921948 0, 963325.14500000001862645 1077388.14400000008754432 0, 963319.42000000004190952 1077382.33199999993667006 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '16',
                            'nombre': '16 16primer apellido 16segundo apellido 16primer nombre 16segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230069000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230069000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'Las Juntas',
                    't_id': 962,
                    'area_terreno': 1808.1,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963314.14300000004004687 1077404.88899999996647239 0, 963319.42000000004190952 1077382.33199999993667006 0, 963325.14500000001862645 1077388.14400000008754432 0, 963388.79500000004190952 1077427.97399999992921948 0, 963368.18799999996554106 1077447.75499999988824129 0, 963314.14300000004004687 1077404.88899999996647239 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '9',
                            'nombre': '9 9primer apellido 9segundo apellido 9primer nombre 9segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230077000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230077000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'SIN INFO',
                    't_id': 963,
                    'area_terreno': 6068.6,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963534.88600000005681068 1077096.61000000010244548 0, 963534.17700000002514571 1077051.04399999999441206 0, 963615.58600000001024455 1077041.22999999998137355 0, 963617.96400000003632158 1077045.1159999999217689 0, 963630.4409999999916181 1077094.90200000000186265 0, 963608.10100000002421439 1077128.76000000000931323 0, 963534.88600000005681068 1077096.61000000010244548 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '19',
                            'nombre': '19 19primer apellido 19segundo apellido 19primer nombre 19segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230078000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230078000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'Santa Lucia',
                    't_id': 964,
                    'area_terreno': 1974.4,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963512.12300000002142042 1077118.00499999988824129 0, 963534.88600000005681068 1077096.61000000010244548 0, 963608.10100000002421439 1077128.76000000000931323 0, 963585.72699999995529652 1077142.15500000002793968 0, 963581.11499999999068677 1077142.33199999993667006 0, 963512.12300000002142042 1077118.00499999988824129 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '33',
                            'nombre': '33 33primer apellido 33segundo apellido 33primer nombre 33segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230079000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230079000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'Santa Lucia',
                    't_id': 965,
                    'area_terreno': 1453.9,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963512.12300000002142042 1077118.00499999988824129 0, 963581.11499999999068677 1077142.33199999993667006 0, 963571.89300000004004687 1077151.575999999884516 0, 963556.67299999995157123 1077158.74300000001676381 0, 963493.62899999995715916 1077125.93299999996088445 0, 963512.12300000002142042 1077118.00499999988824129 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '32',
                            'nombre': '32 32primer apellido 32segundo apellido 32primer nombre 32segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230080000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230080000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'Santa Lucia',
                    't_id': 966,
                    'area_terreno': 2330.8,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963528.16599999996833503 1077177.04399999999441206 0, 963554.77399999997578561 1077165.78000000002793968 0, 963556.67299999995157123 1077158.74300000001676381 0, 963493.62899999995715916 1077125.93299999996088445 0, 963474.51599999994505197 1077133.38100000005215406 0, 963470.2900000000372529 1077135.93800000008195639 0, 963461.71299999998882413 1077144.55099999997764826 0, 963528.16599999996833503 1077177.04399999999441206 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '31',
                            'nombre': '31 31primer apellido 31segundo apellido 31primer nombre 31segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230057000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230057000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'SIN INFO',
                    't_id': 968,
                    'area_terreno': 7691.6,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963871.58299999998416752 1077130.39400000008754432 0, 963900.98300000000745058 1077206.71800000010989606 0, 963914.53700000001117587 1077209.08000000007450581 0, 963997.61699999996926636 1077228.95500000007450581 0, 963999.02899999998044223 1077160.7520000000949949 0, 963871.58299999998416752 1077130.39400000008754432 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '13',
                            'nombre': '13 13primer apellido 13segundo apellido 13primer nombre 13segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230056000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230056000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'El Almorzadero',
                    't_id': 969,
                    'area_terreno': 7983.2,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963999.02899999998044223 1077160.7520000000949949 0, 964018.56400000001303852 1077137.9599999999627471 0, 964056.16200000001117587 1077103.8279999999795109 0, 964092.58600000001024455 1077149.2970000000204891 0, 964093.67799999995622784 1077151.54600000008940697 0, 964095.81000000005587935 1077172.89899999997578561 0, 964098.30200000002514571 1077196.3840000000782311 0, 964057.53200000000651926 1077205.07199999992735684 0, 964023.76100000005681068 1077222.39599999994970858 0, 963997.61699999996926636 1077228.95500000007450581 0, 963999.02899999998044223 1077160.7520000000949949 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '13',
                            'nombre': '13 13primer apellido 13segundo apellido 13primer nombre 13segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230056000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'El Volador',
                    't_id': 970,
                    'area_terreno': 8103.5,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((964060.35499999998137355 1077209.47299999999813735 0, 964063.02099999994970858 1077213.79199999989941716 0, 964049.44900000002235174 1077233.55099999997764826 0, 964041.35199999995529652 1077238.9529999999795109 0, 964006.30599999998230487 1077272.12899999995715916 0, 963989.03700000001117587 1077276.12000000011175871 0, 963981.22900000005029142 1077286.68100000009872019 0, 963965.03300000005401671 1077283.20500000007450581 0, 963952.28599999996367842 1077303.86199999996460974 0, 963936.19400000001769513 1077299.07099999999627471 0, 963930.37100000004284084 1077313.76300000003539026 0, 963923.97400000004563481 1077315.69200000003911555 0, 963911.41899999999441206 1077312.82400000002235174 0, 963916.75399999995715916 1077288.6270000000949949 0, 963896.32900000002700835 1077224.11499999999068677 0, 963913.16200000001117587 1077217.32700000004842877 0, 963953.34900000004563481 1077225.72299999999813735 0, 963997.83900000003632158 1077232.80000000004656613 0, 964024.32099999999627471 1077226.37400000006891787 0, 964060.35499999998137355 1077209.47299999999813735 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '12',
                            'nombre': '12 12primer apellido 12segundo apellido 12primer nombre 12segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230213000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230213000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'El Volador',
                    't_id': 971,
                    'area_terreno': 11157.6,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963516.16099999996367842 1077366.59700000006705523 0, 963546.46100000001024455 1077303.26099999994039536 0, 963614.23899999994318932 1077313.6720000000204891 0, 963675.40200000000186265 1077331.09499999997206032 0, 963665.60499999998137355 1077381.68299999996088445 0, 963621.47600000002421439 1077426.2099999999627471 0, 963554.02000000001862645 1077366.51099999994039536 0, 963516.16099999996367842 1077366.59700000006705523 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '23',
                            'nombre': '23 23primer apellido 23segundo apellido 23primer nombre 23segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230098000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230098000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'Santa Lucía',
                    't_id': 972,
                    'area_terreno': 1320.4,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963247.5659999999916181 1077294.32899999991059303 0, 963254.89899999997578561 1077285.69999999995343387 0, 963203.15000000002328306 1077248.26300000003539026 0, 963184.77000000001862645 1077229.55400000000372529 0, 963174.71299999998882413 1077227.43399999989196658 0, 963166.65599999995902181 1077249.80199999990873039 0, 963170.24699999997392297 1077250.36299999989569187 0, 963198.3349999999627471 1077258.8840000000782311 0, 963203.76399999996647239 1077262.1720000000204891 0, 963228.04099999996833503 1077278.587000000057742 0, 963247.5659999999916181 1077294.32899999991059303 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '1',
                            'nombre': '1 1primer apellido 1segundo apellido 1primer nombre 1segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230097000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230097000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'SIN INFO',
                    't_id': 973,
                    'area_terreno': 25178.2,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963254.89899999997578561 1077285.69999999995343387 0, 963265.26000000000931323 1077293.62199999997392297 0, 963304.04799999995157123 1077221.2590000000782311 0, 963329.412999999942258 1077175.15400000009685755 0, 963259.08299999998416752 1077133.05600000009872019 0, 963257.85199999995529652 1077132.22600000002421439 0, 963239.31900000001769513 1077113.19900000002235174 0, 963111.81099999998696148 1077092.34400000004097819 0, 963102.07200000004377216 1077126.28600000008009374 0, 963105.52700000000186265 1077174.69500000006519258 0, 963155.87699999997857958 1077190.41800000006332994 0, 963145.54399999999441206 1077218.64599999994970858 0, 963174.71299999998882413 1077227.43399999989196658 0, 963184.77000000001862645 1077229.55400000000372529 0, 963203.15000000002328306 1077248.26300000003539026 0, 963254.89899999997578561 1077285.69999999995343387 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '23',
                            'nombre': '23 23primer apellido 23segundo apellido 23primer nombre 23segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230097000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'Santa Lucía',
                    't_id': 976,
                    'area_terreno': 904.8,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963236.74699999997392297 1077236.07499999995343387 0, 963271.35100000002421439 1077259.19500000006519258 0, 963279.6720000000204891 1077250.14599999994970858 0, 963252.46900000004097819 1077210.84599999990314245 0, 963236.74699999997392297 1077236.07499999995343387 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '2',
                            'nombre': '2 2primer apellido 2segundo apellido 2primer nombre 2segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230257000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230257000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'Casimiro',
                    't_id': 974,
                    'area_terreno': 10986.0,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963224.99300000001676381 1077789.93299999996088445 0, 963238.74199999996926636 1077799.87199999997392297 0, 963294.10900000005494803 1077723.28399999998509884 0, 963224.99300000001676381 1077789.93299999996088445 0)),((963235.52300000004470348 1077621.91599999996833503 0, 963214.84799999999813735 1077650.3770000000949949 0, 963200.18299999996088445 1077679.35800000000745058 0, 963180.26399999996647239 1077705.22299999999813735 0, 963163.48999999999068677 1077729.76699999999254942 0, 963217.97999999998137355 1077784.86299999989569187 0, 963288.55500000005122274 1077715.87199999997392297 0, 963260.4409999999916181 1077686.07899999991059303 0, 963268.41000000003259629 1077671.37199999997392297 0, 963264.43700000003445894 1077659.64599999994970858 0, 963268.18099999998230487 1077652.43800000008195639 0, 963264.13800000003539026 1077649.62100000004284084 0, 963235.52300000004470348 1077621.91599999996833503 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '7',
                            'nombre': '7 7primer apellido 7segundo apellido 7primer nombre 7segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230054000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230054000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'San Pedro',
                    't_id': 975,
                    'area_terreno': 49379.0,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963322.17500000004656613 1077706.7099999999627471 0, 963294.10900000005494803 1077723.28399999998509884 0, 963238.74199999996926636 1077799.87199999997392297 0, 963231.84199999994598329 1077814.80799999996088445 0, 963227.35199999995529652 1077834.82400000002235174 0, 963173.25 1077894.79099999996833503 0, 963340.68700000003445894 1078024.52000000001862645 0, 963381.93099999998230487 1077954.86499999999068677 0, 963402.92500000004656613 1077934.5090000000782311 0, 963420.82099999999627471 1077909.42599999997764826 0, 963438.48300000000745058 1077883.48200000007636845 0, 963461.43000000005122274 1077875.79199999989941716 0, 963491.84600000001955777 1077855.12599999993108213 0, 963322.17500000004656613 1077706.7099999999627471 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '6',
                            'nombre': '6 6primer apellido 6segundo apellido 6primer nombre 6segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230074000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230074000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'Tudelita',
                    't_id': 977,
                    'area_terreno': 10006.6,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963316.69499999994877726 1077380.85599999991245568 0, 963340.90700000000651926 1077328.9979999999050051 0, 963376.02899999998044223 1077279.62599999993108213 0, 963304.04799999995157123 1077221.2590000000782311 0, 963254.89899999997578561 1077285.69999999995343387 0, 963247.5659999999916181 1077294.32899999991059303 0, 963316.69499999994877726 1077380.85599999991245568 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '3',
                            'nombre': '3 3primer apellido 3segundo apellido 3primer nombre 3segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230254000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230254000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'El Muche',
                    't_id': 978,
                    'area_terreno': 59108.5,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963351.8349999999627471 1077674.02700000000186265 0, 963364.45400000002700835 1077665.63599999994039536 0, 963374.95799999998416752 1077655.55499999993480742 0, 963379.53300000005401671 1077651.16400000010617077 0, 963384.79799999995157123 1077646.29600000008940697 0, 963403.65599999995902181 1077628.13199999998323619 0, 963403.91000000003259629 1077627.88800000003539026 0, 963406.65099999995436519 1077625.24699999997392297 0, 963421.37199999997392297 1077614.59000000008381903 0, 963436.44799999997485429 1077603.29099999996833503 0, 963438.90500000002793968 1077601.44900000002235174 0, 963447.39300000004004687 1077594.96600000001490116 0, 963448.43000000005122274 1077594.17299999995157123 0, 963457.29399999999441206 1077587.69100000010803342 0, 963462.84999999997671694 1077581.20800000010058284 0, 963464.18000000005122274 1077579.29799999995157123 0, 963472.24300000001676381 1077567.71399999991990626 0, 963476.80700000002980232 1077563.4150000000372529 0, 963481.37100000004284084 1077559.11499999999068677 0, 963487.98600000003352761 1077551.83899999991990626 0, 963497.24600000004284084 1077543.77000000001862645 0, 963510.162999999942258 1077534.63999999989755452 0, 963514.84100000001490116 1077531.33400000003166497 0, 963522.11699999996926636 1077524.32300000009126961 0, 963522.93700000003445894 1077523.79099999996833503 0, 963529.08600000001024455 1077519.80099999997764826 0, 963523.76100000005681068 1077504.57199999992735684 0, 963494.36399999994318932 1077519.02499999990686774 0, 963458.98600000003352761 1077559.13599999994039536 0, 963429.6530000000493601 1077597.34000000008381903 0, 963351.8349999999627471 1077674.02700000000186265 0)),((963532.79200000001583248 1077522.98399999993853271 0, 963523.15899999998509884 1077532.80499999993480742 0, 963511.93999999994412065 1077541.69500000006519258 0, 963510.74300000001676381 1077542.71600000001490116 0, 963504.74399999994784594 1077547.83300000010058284 0, 963493.41700000001583248 1077557.11700000008568168 0, 963491.83200000005308539 1077558.41699999989941716 0, 963489.80099999997764826 1077560.4909999999217689 0, 963482.09499999997206032 1077568.36499999999068677 0, 963472.78200000000651926 1077577.25499999988824129 0, 963464.94999999995343387 1077588.89700000011362135 0, 963456.06000000005587935 1077595.45800000010058284 0, 963445.05000000004656613 1077602.83799999998882413 0, 963439.88399999996181577 1077606.30000000004656613 0, 963410.07400000002235174 1077628.28700000001117587 0, 963401.24800000002142042 1077637.55099999997764826 0, 963374.96799999999348074 1077665.13599999994039536 0, 963368.28500000003259629 1077670.45200000004842877 0, 963367.51500000001396984 1077671.06400000001303852 0, 963361.61100000003352761 1077675.76099999994039536 0, 963356.09900000004563481 1077680.14599999994970858 0, 963322.17500000004656613 1077706.7099999999627471 0, 963491.84600000001955777 1077855.12599999993108213 0, 963516.67000000004190952 1077825.98500000010244548 0, 963557.90800000005401671 1077757.82099999999627471 0, 963654.3090000000083819 1077682.68599999998696148 0, 963683.5400000000372529 1077652.43100000009872019 0, 963532.79200000001583248 1077522.98399999993853271 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '10',
                            'nombre': '10 10primer apellido 10segundo apellido 10primer nombre 10segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230235000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230235000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'Los Naranjos',
                    't_id': 979,
                    'area_terreno': 5473.0,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963301.96100000001024455 1077606.56499999994412065 0, 963285.63100000005215406 1077621.23699999996460974 0, 963264.13800000003539026 1077649.62100000004284084 0, 963268.18099999998230487 1077652.43800000008195639 0, 963264.43700000003445894 1077659.64599999994970858 0, 963268.41000000003259629 1077671.37199999997392297 0, 963260.4409999999916181 1077686.07899999991059303 0, 963288.55500000005122274 1077715.87199999997392297 0, 963311.33400000003166497 1077703.05400000000372529 0, 963351.8349999999627471 1077674.02700000000186265 0, 963319.83799999998882413 1077633.80499999993480742 0, 963301.96100000001024455 1077606.56499999994412065 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '1',
                            'nombre': '1 1primer apellido 1segundo apellido 1primer nombre 1segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230055000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230055000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'El Volador',
                    't_id': 982,
                    'area_terreno': 70502.4,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963523.76100000005681068 1077504.57199999992735684 0, 963529.08600000001024455 1077519.80099999997764826 0, 963538.23400000005494803 1077515.712000000057742 0, 963543.63100000005215406 1077509.67999999993480742 0, 963554.42599999997764826 1077495.86800000001676381 0, 963565.22100000001955777 1077487.61299999989569187 0, 963574.58799999998882413 1077477.29499999992549419 0, 963591.4150000000372529 1077463.32499999995343387 0, 963592.96799999999348074 1077462.00300000002607703 0, 963595.2900000000372529 1077460.02799999993294477 0, 963602.05099999997764826 1077454.27600000007078052 0, 963614.4340000000083819 1077444.27399999997578561 0, 963624.59400000004097819 1077436.97200000006705523 0, 963634.912999999942258 1077433.16200000001117587 0, 963641.26300000003539026 1077428.39899999997578561 0, 963647.61300000001210719 1077419.98600000003352761 0, 963650.31099999998696148 1077411.09599999990314245 0, 963650.75600000005215406 1077410.28600000008009374 0, 963657.45499999995809048 1077398.0779999999795109 0, 963665.60499999998137355 1077381.68299999996088445 0, 963621.47600000002421439 1077426.2099999999627471 0, 963584.20700000005308539 1077451.68500000005587935 0, 963565.55200000002514571 1077469.65299999993294477 0, 963547.99399999994784594 1077479.15400000009685755 0, 963523.76100000005681068 1077504.57199999992735684 0)),((963916.75399999995715916 1077288.6270000000949949 0, 963896.32900000002700835 1077224.11499999999068677 0, 963860.60499999998137355 1077239.7029999999795109 0, 963775.34900000004563481 1077253.23399999993853271 0, 963734.01100000005681068 1077272.81400000001303852 0, 963718.33799999998882413 1077296.33899999991990626 0, 963684.52599999995436519 1077323.9220000000204891 0, 963669.84600000001955777 1077384.62599999993108213 0, 963669.84499999997206032 1077384.62599999993108213 0, 963668.03000000002793968 1077388.27600000007078052 0, 963667.92099999997299165 1077388.49600000004284084 0, 963661.69400000001769513 1077401.02300000004470348 0, 963656.90200000000186265 1077409.75499999988824129 0, 963654.55000000004656613 1077414.0400000000372529 0, 963654.37300000002142042 1077414.6229999999050051 0, 963651.85199999995529652 1077422.92999999993480742 0, 963645.50199999997857958 1077431.34400000004097819 0, 963639.15099999995436519 1077436.10700000007636845 0, 963631.86899999994784594 1077438.79499999992549419 0, 963628.83299999998416752 1077439.91699999989941716 0, 963628.07600000000093132 1077440.46099999989382923 0, 963619.05700000002980232 1077446.94299999997019768 0, 963618.67299999995157123 1077447.21900000004097819 0, 963606.2900000000372529 1077457.21999999997206032 0, 963600.9719999999506399 1077461.74500000011175871 0, 963595.65399999998044223 1077466.26900000008754432 0, 963578.82600000000093132 1077480.23900000005960464 0, 963576.48199999995995313 1077482.82199999992735684 0, 963571.70400000002700835 1077488.08599999989382923 0, 963569.4599999999627471 1077490.55799999996088445 0, 963560.89199999999254942 1077497.11000000010244548 0, 963558.6650000000372529 1077498.81300000008195639 0, 963555.64500000001862645 1077502.67599999997764826 0, 963547.86999999999534339 1077512.62400000006891787 0, 963542.47299999999813735 1077518.65699999989010394 0, 963537.89899999997578561 1077520.700999999884516 0, 963532.79200000001583248 1077522.98399999993853271 0, 963683.5400000000372529 1077652.43100000009872019 0, 963746.5280000000493601 1077563.51399999996647239 0, 963783.58100000000558794 1077497.82000000006519258 0, 963825.93599999998696148 1077393.0470000000204891 0, 963844.19499999994877726 1077361.89100000006146729 0, 963865.99699999997392297 1077355.64999999990686774 0, 963878.93999999994412065 1077348.74300000001676381 0, 963911.41899999999441206 1077312.82400000002235174 0, 963916.75399999995715916 1077288.6270000000949949 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '11',
                            'nombre': '11 11primer apellido 11segundo apellido 11primer nombre 11segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230242000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230242000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'El Guamal',
                    't_id': 983,
                    'area_terreno': 6085.7,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963428.65200000000186265 1077489.20200000004842877 0, 963408.11999999999534339 1077525.30600000009872019 0, 963397.95700000005308539 1077538.45399999991059303 0, 963387.60900000005494803 1077549.35599999991245568 0, 963381.56999999994877726 1077567.29799999995157123 0, 963429.6530000000493601 1077597.34000000008381903 0, 963458.98600000003352761 1077559.13599999994039536 0, 963494.36399999994318932 1077519.02499999990686774 0, 963428.65200000000186265 1077489.20200000004842877 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '10',
                            'nombre': '10 10primer apellido 10segundo apellido 10primer nombre 10segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000320022000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000320022000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'Escuela Alto de Izacar',
                    't_id': 989,
                    'area_terreno': 1377.2,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((964049.44900000002235174 1077233.55099999997764826 0, 964063.02099999994970858 1077213.79199999989941716 0, 964060.35499999998137355 1077209.47299999999813735 0, 964092.30299999995622784 1077207.74699999997392297 0, 964098.231000000028871 1077211.20800000010058284 0, 964100.34400000004097819 1077222.03300000005401671 0, 964095.125 1077244.7029999999795109 0, 964077.49699999997392297 1077242.10000000009313226 0, 964051.52700000000186265 1077236.58899999991990626 0, 964049.44900000002235174 1077233.55099999997764826 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '13',
                            'nombre': '13 13primer apellido 13segundo apellido 13primer nombre 13segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230076000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230076000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'Santa Lucia',
                    't_id': 990,
                    'area_terreno': 12960.6,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963247.04200000001583248 1077094.51699999999254942 0, 963325.6650000000372529 1077104.76900000008754432 0, 963383.32099999999627471 1077094.08100000000558794 0, 963430.59400000004097819 1077090.79399999999441206 0, 963466.44900000002235174 1077086.97399999992921948 0, 963530.28200000000651926 1077096.25799999991431832 0, 963509.643999999971129 1077116.61299999989569187 0, 963473.43099999998230487 1077131.84499999997206032 0, 963458.83200000005308539 1077139.48600000003352761 0, 963434.04200000001583248 1077158.66699999989941716 0, 963415.96799999999348074 1077184.47699999995529652 0, 963368.31900000001769513 1077155.28499999991618097 0, 963355.23300000000745058 1077168.81099999998696148 0, 963247.04200000001583248 1077094.51699999999254942 0)))',
                    'Interesados': NULL
                }
            ],
            '253940000000000230241000000994': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000994',
                    'condicion_predio': 'NPH',
                    'nombre': 'Bajo',
                    't_id': 994,
                    'area_terreno': 12095.4,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963630.4409999999916181 1077094.90200000000186265 0, 963633.32900000002700835 1077093.29199999989941716 0, 963636.30599999998230487 1077091.95699999993667006 0, 963621.731000000028871 1077122.64299999992363155 0, 963614.21100000001024455 1077128.07300000009126961 0, 963586.19900000002235174 1077146.11000000010244548 0, 963580.79899999999906868 1077147.70200000004842877 0, 963575.67700000002514571 1077153.21299999998882413 0, 963559.68099999998230487 1077171.38700000010430813 0, 963543.20499999995809048 1077199.95500000007450581 0, 963519.10400000005029142 1077256.44800000009126961 0, 963508.81099999998696148 1077274.89100000006146729 0, 963502.98400000005494803 1077297.89400000008754432 0, 963498.00300000002607703 1077309.83799999998882413 0, 963492.73300000000745058 1077318.97299999999813735 0, 963479.16000000003259629 1077351.29499999992549419 0, 963458.00300000002607703 1077360.37400000006891787 0, 963438.72800000000279397 1077382.81899999990127981 0, 963428.88600000005681068 1077398.67800000007264316 0, 963418.89699999999720603 1077419.45200000004842877 0, 963414.26300000003539026 1077422.27300000004470348 0, 963386.11399999994318932 1077448.76699999999254942 0, 963372.00699999998323619 1077487.31899999990127981 0, 963365.61999999999534339 1077490.59400000004097819 0, 963361.71600000001490116 1077499.76399999996647239 0, 963357.74899999995250255 1077501.35599999991245568 0, 963350.61800000001676381 1077510.51300000003539026 0, 963326.04799999995157123 1077528.81300000008195639 0, 963319.70100000000093132 1077531.6720000000204891 0, 963310.42399999999906868 1077542.57000000006519258 0, 963308.26800000004004687 1077549.42999999993480742 0, 963305.4220000000204891 1077553.60199999995529652 0, 963290.25899999996181577 1077565.4150000000372529 0, 963279.78099999995902181 1077578.49699999997392297 0, 963264.23600000003352761 1077593.90999999991618097 0, 963242.00500000000465661 1077610.7590000000782311 0, 963235.52300000004470348 1077621.91599999996833503 0, 963214.84799999999813735 1077650.3770000000949949 0, 963200.18299999996088445 1077679.35800000000745058 0, 963180.26399999996647239 1077705.22299999999813735 0, 963163.48999999999068677 1077729.76699999999254942 0, 963157.64699999999720603 1077729.14800000004470348 0, 963225.60900000005494803 1077612.40800000005401671 0, 963312.337000000057742 1077513.68299999996088445 0, 963313.09400000004097819 1077509.02399999997578561 0, 963360.37100000004284084 1077475.44399999990127981 0, 963368.18799999996554106 1077447.75499999988824129 0, 963388.79500000004190952 1077427.97399999992921948 0, 963393.06000000005587935 1077424.39999999990686774 0, 963424.43500000005587935 1077378.12199999997392297 0, 963424.84900000004563481 1077377.26900000008754432 0, 963449.61999999999534339 1077352.06000000005587935 0, 963495.65800000005401671 1077274.45900000003166497 0, 963496.32099999999627471 1077252.37199999997392297 0, 963497 1077239.97500000009313226 0, 963504.01000000000931323 1077221.72799999988637865 0, 963517.43099999998230487 1077202.15400000009685755 0, 963529.96400000003632158 1077195.14199999999254942 0, 963528.16599999996833503 1077177.04399999999441206 0, 963554.77399999997578561 1077165.78000000002793968 0, 963556.67299999995157123 1077158.74300000001676381 0, 963571.89300000004004687 1077151.575999999884516 0, 963581.11499999999068677 1077142.33199999993667006 0, 963585.72699999995529652 1077142.15500000002793968 0, 963608.10100000002421439 1077128.76000000000931323 0, 963630.4409999999916181 1077094.90200000000186265 0)))',
                    'Interesados': NULL
                }
            ],
            '253940000000000230241000000995': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000995',
                    'condicion_predio': 'NPH',
                    'nombre': 'Vía Interveredal',
                    't_id': 995,
                    'area_terreno': 7520.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963217.97999999998137355 1077784.86299999989569187 0, 963288.55500000005122274 1077715.87199999997392297 0, 963311.33400000003166497 1077703.05400000000372529 0, 963351.8349999999627471 1077674.02700000000186265 0, 963364.45400000002700835 1077665.63599999994039536 0, 963374.95799999998416752 1077655.55499999993480742 0, 963379.53300000005401671 1077651.16400000010617077 0, 963384.79799999995157123 1077646.29600000008940697 0, 963403.65599999995902181 1077628.13199999998323619 0, 963403.91000000003259629 1077627.88800000003539026 0, 963406.65099999995436519 1077625.24699999997392297 0, 963421.37199999997392297 1077614.59000000008381903 0, 963436.44799999997485429 1077603.29099999996833503 0, 963438.90500000002793968 1077601.44900000002235174 0, 963447.39300000004004687 1077594.96600000001490116 0, 963448.43000000005122274 1077594.17299999995157123 0, 963457.29399999999441206 1077587.69100000010803342 0, 963462.84999999997671694 1077581.20800000010058284 0, 963464.18000000005122274 1077579.29799999995157123 0, 963472.24300000001676381 1077567.71399999991990626 0, 963476.80700000002980232 1077563.4150000000372529 0, 963481.37100000004284084 1077559.11499999999068677 0, 963487.98600000003352761 1077551.83899999991990626 0, 963497.24600000004284084 1077543.77000000001862645 0, 963510.162999999942258 1077534.63999999989755452 0, 963514.84100000001490116 1077531.33400000003166497 0, 963522.11699999996926636 1077524.32300000009126961 0, 963522.93700000003445894 1077523.79099999996833503 0, 963529.08600000001024455 1077519.80099999997764826 0, 963538.23400000005494803 1077515.712000000057742 0, 963543.63100000005215406 1077509.67999999993480742 0, 963554.42599999997764826 1077495.86800000001676381 0, 963565.22100000001955777 1077487.61299999989569187 0, 963574.58799999998882413 1077477.29499999992549419 0, 963591.4150000000372529 1077463.32499999995343387 0, 963592.96799999999348074 1077462.00300000002607703 0, 963595.2900000000372529 1077460.02799999993294477 0, 963602.05099999997764826 1077454.27600000007078052 0, 963614.4340000000083819 1077444.27399999997578561 0, 963624.59400000004097819 1077436.97200000006705523 0, 963634.912999999942258 1077433.16200000001117587 0, 963641.26300000003539026 1077428.39899999997578561 0, 963647.61300000001210719 1077419.98600000003352761 0, 963650.31099999998696148 1077411.09599999990314245 0, 963650.75600000005215406 1077410.28600000008009374 0, 963657.45499999995809048 1077398.0779999999795109 0, 963665.60499999998137355 1077381.68299999996088445 0, 963675.40200000000186265 1077331.09499999997206032 0, 963680.36800000001676381 1077320.8279999999795109 0, 963713.56299999996554106 1077292.69299999997019768 0, 963728.30599999998230487 1077270.02099999994970858 0, 963775.98699999996460974 1077246.03000000002793968 0, 963858.20100000000093132 1077230.7479999999050051 0, 963900.98300000000745058 1077206.71800000010989606 0, 963914.53700000001117587 1077209.08000000007450581 0, 963997.61699999996926636 1077228.95500000007450581 0, 964023.76100000005681068 1077222.39599999994970858 0, 964057.53200000000651926 1077205.07199999992735684 0, 964098.30200000002514571 1077196.3840000000782311 0, 964098.231000000028871 1077211.20800000010058284 0, 964092.30299999995622784 1077207.74699999997392297 0, 964060.35499999998137355 1077209.47299999999813735 0, 964024.32099999999627471 1077226.37400000006891787 0, 963997.83900000003632158 1077232.80000000004656613 0, 963953.34900000004563481 1077225.72299999999813735 0, 963913.16200000001117587 1077217.32700000004842877 0, 963896.32900000002700835 1077224.11499999999068677 0, 963860.60499999998137355 1077239.7029999999795109 0, 963775.34900000004563481 1077253.23399999993853271 0, 963734.01100000005681068 1077272.81400000001303852 0, 963718.33799999998882413 1077296.33899999991990626 0, 963684.52599999995436519 1077323.9220000000204891 0, 963669.84600000001955777 1077384.62599999993108213 0, 963669.84499999997206032 1077384.62599999993108213 0, 963668.03000000002793968 1077388.27600000007078052 0, 963667.92099999997299165 1077388.49600000004284084 0, 963661.69400000001769513 1077401.02300000004470348 0, 963656.90200000000186265 1077409.75499999988824129 0, 963654.55000000004656613 1077414.0400000000372529 0, 963654.37300000002142042 1077414.6229999999050051 0, 963651.85199999995529652 1077422.92999999993480742 0, 963645.50199999997857958 1077431.34400000004097819 0, 963639.15099999995436519 1077436.10700000007636845 0, 963631.86899999994784594 1077438.79499999992549419 0, 963628.83299999998416752 1077439.91699999989941716 0, 963628.07600000000093132 1077440.46099999989382923 0, 963619.05700000002980232 1077446.94299999997019768 0, 963618.67299999995157123 1077447.21900000004097819 0, 963606.2900000000372529 1077457.21999999997206032 0, 963600.9719999999506399 1077461.74500000011175871 0, 963595.65399999998044223 1077466.26900000008754432 0, 963578.82600000000093132 1077480.23900000005960464 0, 963576.48199999995995313 1077482.82199999992735684 0, 963571.70400000002700835 1077488.08599999989382923 0, 963569.4599999999627471 1077490.55799999996088445 0, 963560.89199999999254942 1077497.11000000010244548 0, 963558.6650000000372529 1077498.81300000008195639 0, 963555.64500000001862645 1077502.67599999997764826 0, 963547.86999999999534339 1077512.62400000006891787 0, 963542.47299999999813735 1077518.65699999989010394 0, 963537.89899999997578561 1077520.700999999884516 0, 963532.79200000001583248 1077522.98399999993853271 0, 963523.15899999998509884 1077532.80499999993480742 0, 963511.93999999994412065 1077541.69500000006519258 0, 963510.74300000001676381 1077542.71600000001490116 0, 963504.74399999994784594 1077547.83300000010058284 0, 963493.41700000001583248 1077557.11700000008568168 0, 963491.83200000005308539 1077558.41699999989941716 0, 963489.80099999997764826 1077560.4909999999217689 0, 963482.09499999997206032 1077568.36499999999068677 0, 963472.78200000000651926 1077577.25499999988824129 0, 963464.94999999995343387 1077588.89700000011362135 0, 963456.06000000005587935 1077595.45800000010058284 0, 963445.05000000004656613 1077602.83799999998882413 0, 963439.88399999996181577 1077606.30000000004656613 0, 963410.07400000002235174 1077628.28700000001117587 0, 963401.24800000002142042 1077637.55099999997764826 0, 963374.96799999999348074 1077665.13599999994039536 0, 963368.28500000003259629 1077670.45200000004842877 0, 963367.51500000001396984 1077671.06400000001303852 0, 963361.61100000003352761 1077675.76099999994039536 0, 963356.09900000004563481 1077680.14599999994970858 0, 963322.17500000004656613 1077706.7099999999627471 0, 963294.10900000005494803 1077723.28399999998509884 0, 963224.99300000001676381 1077789.93299999996088445 0, 963217.97999999998137355 1077784.86299999989569187 0)))',
                    'Interesados': NULL
                }
            ],
            '253940000000000230241000000996': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000996',
                    'condicion_predio': 'NPH',
                    'nombre': 'Camino',
                    't_id': 996,
                    'area_terreno': 2032.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963530.28200000000651926 1077096.25799999991431832 0, 963534.88600000005681068 1077096.61000000010244548 0, 963512.12300000002142042 1077118.00499999988824129 0, 963493.62899999995715916 1077125.93299999996088445 0, 963474.51599999994505197 1077133.38100000005215406 0, 963470.2900000000372529 1077135.93800000008195639 0, 963461.71299999998882413 1077144.55099999997764826 0, 963438.18200000002980232 1077161.11199999996460974 0, 963420.13100000005215406 1077187.15599999995902181 0, 963400.52099999994970858 1077215.42699999990873039 0, 963378.57999999995809048 1077281.69500000006519258 0, 963343.66099999996367842 1077330.41599999996833503 0, 963319.42000000004190952 1077382.33199999993667006 0, 963314.14300000004004687 1077404.88899999996647239 0, 963252.98400000005494803 1077464.47699999995529652 0, 963247.77700000000186265 1077461.75600000005215406 0, 963308.61199999996460974 1077399.01799999992363155 0, 963316.69499999994877726 1077380.85599999991245568 0, 963340.90700000000651926 1077328.9979999999050051 0, 963376.02899999998044223 1077279.62599999993108213 0, 963396.74800000002142042 1077213.01600000006146729 0, 963415.96799999999348074 1077184.47699999995529652 0, 963434.04200000001583248 1077158.66699999989941716 0, 963458.83200000005308539 1077139.48600000003352761 0, 963473.43099999998230487 1077131.84499999997206032 0, 963509.643999999971129 1077116.61299999989569187 0, 963530.28200000000651926 1077096.25799999991431832 0)))',
                    'Interesados': NULL
                }
            ],
            '253940000000000230241000000997': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000997',
                    'condicion_predio': 'NPH',
                    'nombre': 'Camino',
                    't_id': 997,
                    'area_terreno': 3291.9,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963340.68700000003445894 1078024.52000000001862645 0, 963381.93099999998230487 1077954.86499999999068677 0, 963402.92500000004656613 1077934.5090000000782311 0, 963420.82099999999627471 1077909.42599999997764826 0, 963438.48300000000745058 1077883.48200000007636845 0, 963461.43000000005122274 1077875.79199999989941716 0, 963491.84600000001955777 1077855.12599999993108213 0, 963516.67000000004190952 1077825.98500000010244548 0, 963557.90800000005401671 1077757.82099999999627471 0, 963654.3090000000083819 1077682.68599999998696148 0, 963683.5400000000372529 1077652.43100000009872019 0, 963746.5280000000493601 1077563.51399999996647239 0, 963783.58100000000558794 1077497.82000000006519258 0, 963825.93599999998696148 1077393.0470000000204891 0, 963844.19499999994877726 1077361.89100000006146729 0, 963865.99699999997392297 1077355.64999999990686774 0, 963878.93999999994412065 1077348.74300000001676381 0, 963911.41899999999441206 1077312.82400000002235174 0, 963923.97400000004563481 1077315.69200000003911555 0, 963930.37100000004284084 1077313.76300000003539026 0, 963936.19400000001769513 1077299.07099999999627471 0, 963952.28599999996367842 1077303.86199999996460974 0, 963965.03300000005401671 1077283.20500000007450581 0, 963981.22900000005029142 1077286.68100000009872019 0, 963989.03700000001117587 1077276.12000000011175871 0, 964006.30599999998230487 1077272.12899999995715916 0, 964041.35199999995529652 1077238.9529999999795109 0, 964049.44900000002235174 1077233.55099999997764826 0, 964051.52700000000186265 1077236.58899999991990626 0, 964043.43000000005122274 1077241.9909999999217689 0, 964008.38399999996181577 1077275.16699999989941716 0, 963991.11499999999068677 1077279.15800000005401671 0, 963983.30700000002980232 1077289.71900000004097819 0, 963967.11100000003352761 1077286.24300000001676381 0, 963954.36399999994318932 1077306.89999999990686774 0, 963938.27199999999720603 1077302.10899999993853271 0, 963932.44900000002235174 1077316.80099999997764826 0, 963926.05200000002514571 1077318.72999999998137355 0, 963913.49699999997392297 1077315.86199999996460974 0, 963880.70499999995809048 1077350.48399999993853271 0, 963866.65599999995902181 1077358.13899999996647239 0, 963847.6840000000083819 1077365.77600000007078052 0, 963828.64300000004004687 1077394.46999999997206032 0, 963786.5470000000204891 1077499.4529999999795109 0, 963748.4719999999506399 1077564.61800000001676381 0, 963685.82600000000093132 1077654.50300000002607703 0, 963656.00199999997857958 1077685.14299999992363155 0, 963559.268999999971129 1077760.87000000011175871 0, 963518.64500000001862645 1077827.60800000000745058 0, 963494.70100000000093132 1077857.44800000009126961 0, 963462.12100000004284084 1077879.72399999992921948 0, 963439.63899999996647239 1077885.91100000008009374 0, 963423.37300000002142042 1077911.44100000010803342 0, 963404.56299999996554106 1077935.83400000003166497 0, 963383.91399999998975545 1077955.58400000003166497 0, 963341.912999999942258 1078026.26099999994039536 0, 963340.68700000003445894 1078024.52000000001862645 0)))',
                    'Interesados': NULL
                }
            ],
            '253940000000000230073000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230073000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'El Pomarroso',
                    't_id': 998,
                    'area_terreno': 4934.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963449.61999999999534339 1077352.06000000005587935 0, 963495.65800000005401671 1077274.45900000003166497 0, 963434.03000000002793968 1077254.76900000008754432 0, 963400.06099999998696148 1077310.90299999993294477 0, 963449.61999999999534339 1077352.06000000005587935 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '4',
                            'nombre': '4 4primer apellido 4segundo apellido 4primer nombre 4segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230241000000998': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000998',
                    'condicion_predio': 'NPH',
                    'nombre': 'Apartamento 202',
                    't_id': 999,
                    'GEOMETRY_PLOT': None,
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '17',
                            'nombre': '17 17primer apellido 17segundo apellido 17primer nombre 17segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ],
            '253940000000000230241000000999': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000999',
                    'condicion_predio': 'NPH',
                    'nombre': 'Apartamento 101',
                    't_id': 1000,
                    'GEOMETRY_PLOT': None,
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '22',
                            'nombre': '22 22primer apellido 22segundo apellido 22primer nombre 22segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                }
            ]
        }

        features = self.ladm_data.get_parcel_data_to_compare_changes(self.db_pg)
        normalize_response(features)
        self.assertEqual(features, features_test)

        print("\nINFO: Validating get parcels data using search criterion...")

        features_test = {
            '253940000000000230055000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230055000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'El Volador',
                    't_id': 982,
                    'area_terreno': 70502.4,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963523.76100000005681068 1077504.57199999992735684 0, 963529.08600000001024455 1077519.80099999997764826 0, 963538.23400000005494803 1077515.712000000057742 0, 963543.63100000005215406 1077509.67999999993480742 0, 963554.42599999997764826 1077495.86800000001676381 0, 963565.22100000001955777 1077487.61299999989569187 0, 963574.58799999998882413 1077477.29499999992549419 0, 963591.4150000000372529 1077463.32499999995343387 0, 963592.96799999999348074 1077462.00300000002607703 0, 963595.2900000000372529 1077460.02799999993294477 0, 963602.05099999997764826 1077454.27600000007078052 0, 963614.4340000000083819 1077444.27399999997578561 0, 963624.59400000004097819 1077436.97200000006705523 0, 963634.912999999942258 1077433.16200000001117587 0, 963641.26300000003539026 1077428.39899999997578561 0, 963647.61300000001210719 1077419.98600000003352761 0, 963650.31099999998696148 1077411.09599999990314245 0, 963650.75600000005215406 1077410.28600000008009374 0, 963657.45499999995809048 1077398.0779999999795109 0, 963665.60499999998137355 1077381.68299999996088445 0, 963621.47600000002421439 1077426.2099999999627471 0, 963584.20700000005308539 1077451.68500000005587935 0, 963565.55200000002514571 1077469.65299999993294477 0, 963547.99399999994784594 1077479.15400000009685755 0, 963523.76100000005681068 1077504.57199999992735684 0)),((963916.75399999995715916 1077288.6270000000949949 0, 963896.32900000002700835 1077224.11499999999068677 0, 963860.60499999998137355 1077239.7029999999795109 0, 963775.34900000004563481 1077253.23399999993853271 0, 963734.01100000005681068 1077272.81400000001303852 0, 963718.33799999998882413 1077296.33899999991990626 0, 963684.52599999995436519 1077323.9220000000204891 0, 963669.84600000001955777 1077384.62599999993108213 0, 963669.84499999997206032 1077384.62599999993108213 0, 963668.03000000002793968 1077388.27600000007078052 0, 963667.92099999997299165 1077388.49600000004284084 0, 963661.69400000001769513 1077401.02300000004470348 0, 963656.90200000000186265 1077409.75499999988824129 0, 963654.55000000004656613 1077414.0400000000372529 0, 963654.37300000002142042 1077414.6229999999050051 0, 963651.85199999995529652 1077422.92999999993480742 0, 963645.50199999997857958 1077431.34400000004097819 0, 963639.15099999995436519 1077436.10700000007636845 0, 963631.86899999994784594 1077438.79499999992549419 0, 963628.83299999998416752 1077439.91699999989941716 0, 963628.07600000000093132 1077440.46099999989382923 0, 963619.05700000002980232 1077446.94299999997019768 0, 963618.67299999995157123 1077447.21900000004097819 0, 963606.2900000000372529 1077457.21999999997206032 0, 963600.9719999999506399 1077461.74500000011175871 0, 963595.65399999998044223 1077466.26900000008754432 0, 963578.82600000000093132 1077480.23900000005960464 0, 963576.48199999995995313 1077482.82199999992735684 0, 963571.70400000002700835 1077488.08599999989382923 0, 963569.4599999999627471 1077490.55799999996088445 0, 963560.89199999999254942 1077497.11000000010244548 0, 963558.6650000000372529 1077498.81300000008195639 0, 963555.64500000001862645 1077502.67599999997764826 0, 963547.86999999999534339 1077512.62400000006891787 0, 963542.47299999999813735 1077518.65699999989010394 0, 963537.89899999997578561 1077520.700999999884516 0, 963532.79200000001583248 1077522.98399999993853271 0, 963683.5400000000372529 1077652.43100000009872019 0, 963746.5280000000493601 1077563.51399999996647239 0, 963783.58100000000558794 1077497.82000000006519258 0, 963825.93599999998696148 1077393.0470000000204891 0, 963844.19499999994877726 1077361.89100000006146729 0, 963865.99699999997392297 1077355.64999999990686774 0, 963878.93999999994412065 1077348.74300000001676381 0, 963911.41899999999441206 1077312.82400000002235174 0, 963916.75399999995715916 1077288.6270000000949949 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
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
        normalize_response(features)
        self.assertEqual(features, features_test)

        features_test = {
            '253940000000000230241000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'Hoya Las Juntas',
                    't_id': 950,
                    'area_terreno': 7307.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963516.16099999996367842 1077366.59700000006705523 0, 963506.0849999999627471 1077369.162999999942258 0, 963485.87699999997857958 1077390.93900000001303852 0, 963500.4599999999627471 1077410.17100000008940697 0, 963527.53599999996367842 1077431.21600000001490116 0, 963565.55200000002514571 1077469.65299999993294477 0, 963584.20700000005308539 1077451.68500000005587935 0, 963621.47600000002421439 1077426.2099999999627471 0, 963554.02000000001862645 1077366.51099999994039536 0, 963516.16099999996367842 1077366.59700000006705523 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '14',
                            'nombre': '14 14primer apellido 14segundo apellido 14primer nombre 14segundo nombre',
                            'derecho': 'Dominio'
                        },
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '2',
                            'nombre': '2 2primer apellido 2segundo apellido 2primer nombre 2segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'SIN INFO',
                    't_id': 953,
                    'area_terreno': 4283.7,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963546.46100000001024455 1077303.26099999994039536 0, 963614.23899999994318932 1077313.6720000000204891 0, 963631.17900000000372529 1077251.375 0, 963599.68200000002980232 1077224.26600000006146729 0, 963568.8279999999795109 1077265.58799999998882413 0, 963546.46100000001024455 1077303.26099999994039536 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '14',
                            'nombre': '14 14primer apellido 14segundo apellido 14primer nombre 14segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'Tudela Juntas',
                    't_id': 954,
                    'area_terreno': 30777.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963614.21100000001024455 1077128.07300000009126961 0, 963621.731000000028871 1077122.64299999992363155 0, 963636.30599999998230487 1077091.95699999993667006 0, 963646.0779999999795109 1077074.34799999999813735 0, 963722.36800000001676381 1077109.49200000008568168 0, 963746.39000000001396984 1077120.55799999996088445 0, 963779.01500000001396984 1077150.40100000007078052 0, 963775.98699999996460974 1077246.03000000002793968 0, 963728.30599999998230487 1077270.02099999994970858 0, 963713.56299999996554106 1077292.69299999997019768 0, 963680.36800000001676381 1077320.8279999999795109 0, 963675.40200000000186265 1077331.09499999997206032 0, 963614.23899999994318932 1077313.6720000000204891 0, 963631.17900000000372529 1077251.375 0, 963599.68200000002980232 1077224.26600000006146729 0, 963543.20499999995809048 1077199.95500000007450581 0, 963559.68099999998230487 1077171.38700000010430813 0, 963575.67700000002514571 1077153.21299999998882413 0, 963580.79899999999906868 1077147.70200000004842877 0, 963624.64899999997578561 1077205.93399999989196658 0, 963655.29200000001583248 1077187.44900000002235174 0, 963671.17500000004656613 1077163.80899999989196658 0, 963659.34199999994598329 1077146.59199999994598329 0, 963614.21100000001024455 1077128.07300000009126961 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '28',
                            'nombre': '28 28primer apellido 28segundo apellido 28primer nombre 28segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'Mardoqueo',
                    't_id': 967,
                    'area_terreno': 877.9,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963372.00699999998323619 1077487.31899999990127981 0, 963408.11999999999534339 1077525.30600000009872019 0, 963397.95700000005308539 1077538.45399999991059303 0, 963361.71600000001490116 1077499.76399999996647239 0, 963365.61999999999534339 1077490.59400000004097819 0, 963372.00699999998323619 1077487.31899999990127981 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '35',
                            'nombre': '35 35primer apellido 35segundo apellido 35primer nombre 35segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'SIN INFO',
                    't_id': 980,
                    'area_terreno': 818.8,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963361.71600000001490116 1077499.76399999996647239 0, 963397.95700000005308539 1077538.45399999991059303 0, 963387.60900000005494803 1077549.35599999991245568 0, 963376.43999999994412065 1077537.31899999990127981 0, 963350.61800000001676381 1077510.51300000003539026 0, 963357.74899999995250255 1077501.35599999991245568 0, 963361.71600000001490116 1077499.76399999996647239 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '26',
                            'nombre': '26 26primer apellido 26segundo apellido 26primer nombre 26segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'SIN INFO',
                    't_id': 981,
                    'area_terreno': 967.1,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963350.61800000001676381 1077510.51300000003539026 0, 963376.43999999994412065 1077537.31899999990127981 0, 963366.17900000000372529 1077551.52399999997578561 0, 963326.04799999995157123 1077528.81300000008195639 0, 963350.61800000001676381 1077510.51300000003539026 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '25',
                            'nombre': '25 25primer apellido 25segundo apellido 25primer nombre 25segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'SIN INFO',
                    't_id': 984,
                    'area_terreno': 2614.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963500.4599999999627471 1077410.17100000008940697 0, 963527.53599999996367842 1077431.21600000001490116 0, 963565.55200000002514571 1077469.65299999993294477 0, 963547.99399999994784594 1077479.15400000009685755 0, 963503.45900000003166497 1077453.82899999991059303 0, 963468.768999999971129 1077434.62100000004284084 0, 963500.4599999999627471 1077410.17100000008940697 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '9',
                            'nombre': '9 9primer apellido 9segundo apellido 9primer nombre 9segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'SIN INFO',
                    't_id': 985,
                    'area_terreno': 11087.8,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963376.43999999994412065 1077537.31899999990127981 0, 963387.60900000005494803 1077549.35599999991245568 0, 963381.56999999994877726 1077567.29799999995157123 0, 963429.6530000000493601 1077597.34000000008381903 0, 963351.8349999999627471 1077674.02700000000186265 0, 963319.83799999998882413 1077633.80499999993480742 0, 963301.96100000001024455 1077606.56499999994412065 0, 963279.78099999995902181 1077578.49699999997392297 0, 963290.25899999996181577 1077565.4150000000372529 0, 963305.4220000000204891 1077553.60199999995529652 0, 963308.26800000004004687 1077549.42999999993480742 0, 963310.42399999999906868 1077542.57000000006519258 0, 963319.70100000000093132 1077531.6720000000204891 0, 963326.04799999995157123 1077528.81300000008195639 0, 963366.17900000000372529 1077551.52399999997578561 0, 963376.43999999994412065 1077537.31899999990127981 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '27',
                            'nombre': '27 27primer apellido 27segundo apellido 27primer nombre 27segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'SIN INFO',
                    't_id': 986,
                    'area_terreno': 15073.7,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963722.36800000001676381 1077109.49200000008568168 0, 963740.38399999996181577 1077099.46900000004097819 0, 963766.875 1077090.20900000003166497 0, 963776.40000000002328306 1077088.09199999994598329 0, 963792.01000000000931323 1077089.28300000005401671 0, 963805.37199999997392297 1077094.04600000008940697 0, 963815.55799999996088445 1077099.46900000004097819 0, 963840.69400000001769513 1077119.7099999999627471 0, 963854.31999999994877726 1077127.91200000001117587 0, 963871.58299999998416752 1077130.39400000008754432 0, 963900.98300000000745058 1077206.71800000010989606 0, 963858.20100000000093132 1077230.7479999999050051 0, 963775.98699999996460974 1077246.03000000002793968 0, 963779.01500000001396984 1077150.40100000007078052 0, 963746.39000000001396984 1077120.55799999996088445 0, 963722.36800000001676381 1077109.49200000008568168 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '13',
                            'nombre': '13 13primer apellido 13segundo apellido 13primer nombre 13segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'SIN INFO',
                    't_id': 987,
                    'area_terreno': 2234.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963279.78099999995902181 1077578.49699999997392297 0, 963301.96100000001024455 1077606.56499999994412065 0, 963285.63100000005215406 1077621.23699999996460974 0, 963264.13800000003539026 1077649.62100000004284084 0, 963235.52300000004470348 1077621.91599999996833503 0, 963242.00500000000465661 1077610.7590000000782311 0, 963264.23600000003352761 1077593.90999999991618097 0, 963279.78099999995902181 1077578.49699999997392297 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '34',
                            'nombre': '34 34primer apellido 34segundo apellido 34primer nombre 34segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'El Tigre',
                    't_id': 988,
                    'area_terreno': 4200.0,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963479.16000000003259629 1077351.29499999992549419 0, 963506.0849999999627471 1077369.162999999942258 0, 963485.87699999997857958 1077390.93900000001303852 0, 963500.4599999999627471 1077410.17100000008940697 0, 963468.768999999971129 1077434.62100000004284084 0, 963418.89699999999720603 1077419.45200000004842877 0, 963428.88600000005681068 1077398.67800000007264316 0, 963438.72800000000279397 1077382.81899999990127981 0, 963458.00300000002607703 1077360.37400000006891787 0, 963479.16000000003259629 1077351.29499999992549419 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '20',
                            'nombre': '20 20primer apellido 20segundo apellido 20primer nombre 20segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'SIN INFO',
                    't_id': 992,
                    'area_terreno': 4814.4,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963479.16000000003259629 1077351.29499999992549419 0, 963492.73300000000745058 1077318.97299999999813735 0, 963498.00300000002607703 1077309.83799999998882413 0, 963502.98400000005494803 1077297.89400000008754432 0, 963508.81099999998696148 1077274.89100000006146729 0, 963519.10400000005029142 1077256.44800000009126961 0, 963568.8279999999795109 1077265.58799999998882413 0, 963546.46100000001024455 1077303.26099999994039536 0, 963516.16099999996367842 1077366.59700000006705523 0, 963506.0849999999627471 1077369.162999999942258 0, 963479.16000000003259629 1077351.29499999992549419 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
                            'documento_identidad': '22',
                            'nombre': '22 22primer apellido 22segundo apellido 22primer nombre 22segundo nombre',
                            'derecho': 'Dominio'
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': NULL,
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': 'Angel',
                    't_id': 993,
                    'area_terreno': 10495.1,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((963418.89699999999720603 1077419.45200000004842877 0, 963468.768999999971129 1077434.62100000004284084 0, 963503.45900000003166497 1077453.82899999991059303 0, 963547.99399999994784594 1077479.15400000009685755 0, 963523.76100000005681068 1077504.57199999992735684 0, 963494.36399999994318932 1077519.02499999990686774 0, 963428.65200000000186265 1077489.20200000004842877 0, 963408.11999999999534339 1077525.30600000009872019 0, 963372.00699999998323619 1077487.31899999990127981 0, 963386.11399999994318932 1077448.76699999999254942 0, 963414.26300000003539026 1077422.27300000004470348 0, 963418.89699999999720603 1077419.45200000004842877 0)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cedula_Ciudadania',
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
        normalize_response(features)
        self.assertEqual(features, features_test)

    @classmethod
    def tearDownClass(cls):
        print("INFO: Closing open connections to databases")
        cls.db_pg.conn.close()


if __name__ == '__main__':
    nose2.main()
