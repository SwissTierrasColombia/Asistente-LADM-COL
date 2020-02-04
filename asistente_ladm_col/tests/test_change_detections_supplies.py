import nose2

from qgis.core import (QgsWkbTypes,
                       NULL)
from qgis.testing import (start_app,
                          unittest)

start_app()  # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.utils.qgis_utils import QGISUtils
from asistente_ladm_col.logic.ladm_col.data.ladm_data import LADM_DATA
from asistente_ladm_col.config.general_config import LAYER
from asistente_ladm_col.tests.utils import (get_pg_conn,
                                            normalize_responce,
                                            restore_schema)


class TestChangeDetectionsSupplies(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("INFO: Restoring databases to be used")
        restore_schema('test_change_detections')
        cls.db_pg = get_pg_conn('test_change_detections')
        result = cls.db_pg.test_connection()
        print('test_connection', result)

        if not result[1]:
            print('The test connection is not working')
            return

        cls.qgis_utils = QGISUtils()
        cls.ladm_data = LADM_DATA(cls.qgis_utils)

    def test_get_plots_related_to_parcels_supplies(self):
        print("\nINFO: Validating get plots related to parcels in supplies model (Case: t_id)...")

        result = self.db_pg.test_connection()
        self.assertTrue(result[0], 'The test connection is not working')
        self.assertIsNotNone(self.db_pg.names.OP_BOUNDARY_POINT_T, 'Names is None')

        parcel_ids_tests = [list(), [1000], [1000, 1001, 1002]]
        plot_ids_tests = [list(), [1112], [1112, 1102, 1086]]

        count = 0
        for parcel_ids_test in parcel_ids_tests:
            plot_ids = self.ladm_data.get_plots_related_to_parcels_supplies(self.db_pg, parcel_ids_test, self.db_pg.names.T_ID_F)
            # We use assertCountEqual to compare if two lists are the same regardless of the order of their elements.
            # https://docs.python.org/3.2/library/unittest.html#unittest.TestCase.assertCountEqual
            self.assertEqual(sorted(plot_ids), sorted(plot_ids_tests[count]), "Failure with data set {}".format(count + 1))
            count += 1

        print("\nINFO: Validating get plots related to parcels in supplies model (Case: custom field)...")
        plot_custom_field_ids_tests = [list(), [967.13], [967.13, 4200.03, 25178.2]]

        count = 0
        for parcel_ids_test in parcel_ids_tests:
            plot_custom_field_ids = self.ladm_data.get_plots_related_to_parcels_supplies(self.db_pg, parcel_ids_test, self.db_pg.names.GC_PLOT_T_DIGITAL_PLOT_AREA_F)
            self.assertEqual(sorted(plot_custom_field_ids), sorted(plot_custom_field_ids_tests[count]), "Failure with data set {}".format(count + 1))
            count += 1

        print("\nINFO: Validating get plots related to parcels in supplies model (Case: t_id) with preloaded tables...")

        layers = {self.db_pg.names.GC_PLOT_T: {'name': self.db_pg.names.GC_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None}}
        self.qgis_utils.get_layers(self.db_pg, layers, load=True)
        self.assertIsNotNone(layers, 'An error occurred while trying to get the layers of interest')

        count = 0
        for parcel_ids_test in parcel_ids_tests:
            plot_ids = self.ladm_data.get_plots_related_to_parcels_supplies(self.db_pg,
                                                                            parcel_ids_test,
                                                                            self.db_pg.names.T_ID_F,
                                                                            gc_plot_layer=layers[self.db_pg.names.GC_PLOT_T][LAYER])
            self.assertEqual(sorted(plot_ids), sorted(plot_ids_tests[count]), "Failure with data set {}".format(count + 1))
            count += 1

    def test_get_parcels_related_to_plots_supplies(self):
        print("\nINFO: Validating get parcels related to plots in supplies model (Case: t_id)...")

        parcel_ids_tests = [list(), [1000], [1000, 1001, 1002]]
        plot_ids_tests = [list(), [1112], [1112, 1102, 1086]]

        count = 0
        for plot_ids_test in plot_ids_tests:
            parcel_ids = self.ladm_data.get_parcels_related_to_plots_supplies(self.db_pg, plot_ids_test, self.db_pg.names.T_ID_F)
            # We use assertCountEqual to compare if two lists are the same regardless of the order of their elements.
            # https://docs.python.org/3.2/library/unittest.html#unittest.TestCase.assertCountEqual
            self.assertEqual(sorted(parcel_ids), sorted(parcel_ids_tests[count]), "Failure with data set {}".format(count + 1))
            count += 1

        print("\nINFO: Validating get parcels related to plots in supplies model (Case: custom field)...")
        parcel_custom_field_ids_tests = [list(),
                                         ['253940000000000230241000000000'],
                                         ['253940000000000230241000000000', '253940000000000230241000000994', '253940000000000230241000000995']]

        count = 0
        for plot_ids_test in plot_ids_tests:
            parcel_custom_field_ids = self.ladm_data.get_parcels_related_to_plots_supplies(self.db_pg,
                                                                                           plot_ids_test,
                                                                                           self.db_pg.names.GC_PARCEL_T_PARCEL_NUMBER_F)
            self.assertEqual(sorted(parcel_custom_field_ids), sorted(parcel_custom_field_ids_tests[count]), "Failure with data set {}".format(count + 1))
            count += 1

        print("\nINFO: Validating get parcels related to plots in supplies model (Case: t_id) with preloaded tables...")

        layers = {
            self.db_pg.names.GC_PARCEL_T: {'name': self.db_pg.names.GC_PARCEL_T, 'geometry': None, LAYER: None}
        }
        self.qgis_utils.get_layers(self.db_pg, layers, load=True)
        self.assertIsNotNone(layers, 'An error occurred while trying to get the layers of interest')

        count = 0
        for plot_ids_test in plot_ids_tests:
            parcel_ids = self.ladm_data.get_parcels_related_to_plots_supplies(self.db_pg,
                                                                              plot_ids_test,
                                                                              self.db_pg.names.T_ID_F,
                                                                              gc_parcel_table=layers[self.db_pg.names.GC_PARCEL_T][LAYER])
            self.assertEqual(sorted(parcel_ids), sorted(parcel_ids_tests[count]), "Failure with data set {}".format(count + 1))
            count += 1

    def test_get_parcel_data_to_compare_changes_supplies(self):
        print("\nINFO: Validating get parcels data ...")

        features_test = {
            '253940000000000230241000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '760ab38',
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 971,
                    'area_terreno': 5375.26,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963319.42000000004190952 1077382.33199999993667006, 963343.66099999996367842 1077330.41599999996833503, 963424.84900000004563481 1077377.26900000008754432, 963424.43500000005587935 1077378.12199999997392297, 963393.06000000005587935 1077424.39999999990686774, 963388.79500000004190952 1077427.97399999992921948, 963325.14500000001862645 1077388.14400000008754432, 963319.42000000004190952 1077382.33199999993667006)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '1',
                            'nombre': '1primer nombre 1segundo nombre 1primero apellido 1segundo apellido',
                            'derecho': NULL
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': 'b3fabeb',
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 973,
                    'area_terreno': 10006.6,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963316.69499999994877726 1077380.85599999991245568, 963340.90700000000651926 1077328.9979999999050051, 963376.02899999998044223 1077279.62599999993108213, 963304.04799999995157123 1077221.2590000000782311, 963254.89899999997578561 1077285.69999999995343387, 963247.5659999999916181 1077294.32899999991059303, 963316.69499999994877726 1077380.85599999991245568)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '4',
                            'nombre': '4primer nombre 4segundo nombre 4primero apellido 4segundo apellido',
                            'derecho': NULL
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '2b97646',
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 980,
                    'area_terreno': 6068.56,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963534.88600000005681068 1077096.61000000010244548, 963534.17700000002514571 1077051.04399999999441206, 963615.58600000001024455 1077041.22999999998137355, 963617.96400000003632158 1077045.1159999999217689, 963630.4409999999916181 1077094.90200000000186265, 963608.10100000002421439 1077128.76000000000931323, 963534.88600000005681068 1077096.61000000010244548)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '18',
                            'nombre': '18primer nombre 18segundo nombre 18primero apellido 18segundo apellido',
                            'derecho': NULL
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': 'fc286c8',
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 991,
                    'area_terreno': 3902.12,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963614.21100000001024455 1077128.07300000009126961, 963659.34199999994598329 1077146.59199999994598329, 963671.17500000004656613 1077163.80899999989196658, 963655.29200000001583248 1077187.44900000002235174, 963624.64899999997578561 1077205.93399999989196658, 963580.79899999999906868 1077147.70200000004842877, 963586.19900000002235174 1077146.11000000010244548, 963614.21100000001024455 1077128.07300000009126961)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '32',
                            'nombre': '32primer nombre 32segundo nombre 32primero apellido 32segundo apellido',
                            'derecho': NULL
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '5a49adb',
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 992,
                    'area_terreno': 2455.26,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963438.18200000002980232 1077161.11199999996460974, 963517.43099999998230487 1077202.15400000009685755, 963504.01000000000931323 1077221.72799999988637865, 963420.13100000005215406 1077187.15599999995902181, 963438.18200000002980232 1077161.11199999996460974)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '33',
                            'nombre': '33primer nombre 33segundo nombre 33primero apellido 33segundo apellido',
                            'derecho': NULL
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '640b220',
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 995,
                    'area_terreno': 904.82,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963236.74699999997392297 1077236.07499999995343387, 963271.35100000002421439 1077259.19500000006519258, 963279.6720000000204891 1077250.14599999994970858, 963252.46900000004097819 1077210.84599999990314245, 963236.74699999997392297 1077236.07499999995343387)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '36',
                            'nombre': '36primer nombre 36segundo nombre 36primero apellido 36segundo apellido',
                            'derecho': NULL
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '1eee7a1',
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 996,
                    'area_terreno': 8103.5,
                    'GEOMETRY_PLOT': 'MultiPolygon (((964060.35499999998137355 1077209.47299999999813735, 964063.02099999994970858 1077213.79199999989941716, 964049.44900000002235174 1077233.55099999997764826, 964041.35199999995529652 1077238.9529999999795109, 964006.30599999998230487 1077272.12899999995715916, 963989.03700000001117587 1077276.12000000011175871, 963981.22900000005029142 1077286.68100000009872019, 963965.03300000005401671 1077283.20500000007450581, 963952.28599999996367842 1077303.86199999996460974, 963936.19400000001769513 1077299.07099999999627471, 963930.37100000004284084 1077313.76300000003539026, 963923.97400000004563481 1077315.69200000003911555, 963911.41899999999441206 1077312.82400000002235174, 963916.75399999995715916 1077288.6270000000949949, 963896.32900000002700835 1077224.11499999999068677, 963913.16200000001117587 1077217.32700000004842877, 963953.34900000004563481 1077225.72299999999813735, 963997.83900000003632158 1077232.80000000004656613, 964024.32099999999627471 1077226.37400000006891787, 964060.35499999998137355 1077209.47299999999813735)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '38',
                            'nombre': '38primer nombre 38segundo nombre 38primero apellido 38segundo apellido',
                            'derecho': NULL
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': 'cb0dbdc',
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 997,
                    'GEOMETRY_PLOT': None,
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '39',
                            'nombre': '39primer nombre 39segundo nombre 39primero apellido 39segundo apellido',
                            'derecho': NULL
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': 'efa6c49',
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 998,
                    'area_terreno': 70502.47,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963523.76100000005681068 1077504.57199999992735684, 963529.08600000001024455 1077519.80099999997764826, 963538.23400000005494803 1077515.712000000057742, 963543.63100000005215406 1077509.67999999993480742, 963554.42599999997764826 1077495.86800000001676381, 963565.22100000001955777 1077487.61299999989569187, 963574.58799999998882413 1077477.29499999992549419, 963591.4150000000372529 1077463.32499999995343387, 963592.96799999999348074 1077462.00300000002607703, 963595.2900000000372529 1077460.02799999993294477, 963602.05099999997764826 1077454.27600000007078052, 963614.4340000000083819 1077444.27399999997578561, 963624.59400000004097819 1077436.97200000006705523, 963634.912999999942258 1077433.16200000001117587, 963641.26300000003539026 1077428.39899999997578561, 963647.61300000001210719 1077419.98600000003352761, 963650.31099999998696148 1077411.09599999990314245, 963650.75600000005215406 1077410.28600000008009374, 963657.45499999995809048 1077398.0779999999795109, 963665.60499999998137355 1077381.68299999996088445, 963621.47600000002421439 1077426.2099999999627471, 963584.20700000005308539 1077451.68500000005587935, 963565.55200000002514571 1077469.65299999993294477, 963547.99399999994784594 1077479.15400000009685755, 963523.76100000005681068 1077504.57199999992735684)),((963916.75399999995715916 1077288.6270000000949949, 963896.32900000002700835 1077224.11499999999068677, 963860.60499999998137355 1077239.7029999999795109, 963775.34900000004563481 1077253.23399999993853271, 963734.01100000005681068 1077272.81400000001303852, 963718.33799999998882413 1077296.33899999991990626, 963684.52599999995436519 1077323.9220000000204891, 963669.84600000001955777 1077384.62599999993108213, 963669.84499999997206032 1077384.62599999993108213, 963668.03000000002793968 1077388.27600000007078052, 963667.92099999997299165 1077388.49600000004284084, 963661.69400000001769513 1077401.02300000004470348, 963656.90200000000186265 1077409.75499999988824129, 963654.55000000004656613 1077414.0400000000372529, 963654.37300000002142042 1077414.6229999999050051, 963651.85199999995529652 1077422.92999999993480742, 963645.50199999997857958 1077431.34400000004097819, 963639.15099999995436519 1077436.10700000007636845, 963631.86899999994784594 1077438.79499999992549419, 963628.83299999998416752 1077439.91699999989941716, 963628.07600000000093132 1077440.46099999989382923, 963619.05700000002980232 1077446.94299999997019768, 963618.67299999995157123 1077447.21900000004097819, 963606.2900000000372529 1077457.21999999997206032, 963600.9719999999506399 1077461.74500000011175871, 963595.65399999998044223 1077466.26900000008754432, 963578.82600000000093132 1077480.23900000005960464, 963576.48199999995995313 1077482.82199999992735684, 963571.70400000002700835 1077488.08599999989382923, 963569.4599999999627471 1077490.55799999996088445, 963560.89199999999254942 1077497.11000000010244548, 963558.6650000000372529 1077498.81300000008195639, 963555.64500000001862645 1077502.67599999997764826, 963547.86999999999534339 1077512.62400000006891787, 963542.47299999999813735 1077518.65699999989010394, 963537.89899999997578561 1077520.700999999884516, 963532.79200000001583248 1077522.98399999993853271, 963683.5400000000372529 1077652.43100000009872019, 963746.5280000000493601 1077563.51399999996647239, 963783.58100000000558794 1077497.82000000006519258, 963825.93599999998696148 1077393.0470000000204891, 963844.19499999994877726 1077361.89100000006146729, 963865.99699999997392297 1077355.64999999990686774, 963878.93999999994412065 1077348.74300000001676381, 963911.41899999999441206 1077312.82400000002235174, 963916.75399999995715916 1077288.6270000000949949)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '40',
                            'nombre': '40primer nombre 40segundo nombre 40primero apellido 40segundo apellido',
                            'derecho': NULL
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '81d29bf',
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 1000,
                    'area_terreno': 967.13,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963350.61800000001676381 1077510.51300000003539026, 963376.43999999994412065 1077537.31899999990127981, 963366.17900000000372529 1077551.52399999997578561, 963326.04799999995157123 1077528.81300000008195639, 963350.61800000001676381 1077510.51300000003539026)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '43',
                            'nombre': '43primer nombre 43segundo nombre 43primero apellido 43segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230234000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': 'd05ca21',
                    'numero_predial': '253940000000000230234000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 972,
                    'area_terreno': 2234.27,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963279.78099999995902181 1077578.49699999997392297, 963301.96100000001024455 1077606.56499999994412065, 963285.63100000005215406 1077621.23699999996460974, 963264.13800000003539026 1077649.62100000004284084, 963235.52300000004470348 1077621.91599999996833503, 963242.00500000000465661 1077610.7590000000782311, 963264.23600000003352761 1077593.90999999991618097, 963279.78099999995902181 1077578.49699999997392297)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '3',
                            'nombre': '3primer nombre 3segundo nombre 3primero apellido 3segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230100000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '6918b54',
                    'numero_predial': '253940000000000230100000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 974,
                    'area_terreno': 11087.81,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963376.43999999994412065 1077537.31899999990127981, 963387.60900000005494803 1077549.35599999991245568, 963381.56999999994877726 1077567.29799999995157123, 963429.6530000000493601 1077597.34000000008381903, 963351.8349999999627471 1077674.02700000000186265, 963319.83799999998882413 1077633.80499999993480742, 963301.96100000001024455 1077606.56499999994412065, 963279.78099999995902181 1077578.49699999997392297, 963290.25899999996181577 1077565.4150000000372529, 963305.4220000000204891 1077553.60199999995529652, 963308.26800000004004687 1077549.42999999993480742, 963310.42399999999906868 1077542.57000000006519258, 963319.70100000000093132 1077531.6720000000204891, 963326.04799999995157123 1077528.81300000008195639, 963366.17900000000372529 1077551.52399999997578561, 963376.43999999994412065 1077537.31899999990127981)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '7',
                            'nombre': '7primer nombre 7segundo nombre 7primero apellido 7segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230068000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '363db4f',
                    'numero_predial': '253940000000000230068000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 975,
                    'area_terreno': 1453.95,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963512.12300000002142042 1077118.00499999988824129, 963581.11499999999068677 1077142.33199999993667006, 963571.89300000004004687 1077151.575999999884516, 963556.67299999995157123 1077158.74300000001676381, 963493.62899999995715916 1077125.93299999996088445, 963512.12300000002142042 1077118.00499999988824129)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '9',
                            'nombre': '9primer nombre 9segundo nombre 9primero apellido 9segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230081000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '345e748',
                    'numero_predial': '253940000000000230081000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 976,
                    'area_terreno': 5472.99,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963301.96100000001024455 1077606.56499999994412065, 963285.63100000005215406 1077621.23699999996460974, 963264.13800000003539026 1077649.62100000004284084, 963268.18099999998230487 1077652.43800000008195639, 963264.43700000003445894 1077659.64599999994970858, 963268.41000000003259629 1077671.37199999997392297, 963260.4409999999916181 1077686.07899999991059303, 963288.55500000005122274 1077715.87199999997392297, 963311.33400000003166497 1077703.05400000000372529, 963351.8349999999627471 1077674.02700000000186265, 963319.83799999998882413 1077633.80499999993480742, 963301.96100000001024455 1077606.56499999994412065)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '10',
                            'nombre': '10primer nombre 10segundo nombre 10primero apellido 10segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230082000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '9f0eade',
                    'numero_predial': '253940000000000230082000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 977,
                    'area_terreno': 59108.43,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963351.8349999999627471 1077674.02700000000186265, 963364.45400000002700835 1077665.63599999994039536, 963374.95799999998416752 1077655.55499999993480742, 963379.53300000005401671 1077651.16400000010617077, 963384.79799999995157123 1077646.29600000008940697, 963403.65599999995902181 1077628.13199999998323619, 963403.91000000003259629 1077627.88800000003539026, 963406.65099999995436519 1077625.24699999997392297, 963421.37199999997392297 1077614.59000000008381903, 963436.44799999997485429 1077603.29099999996833503, 963438.90500000002793968 1077601.44900000002235174, 963447.39300000004004687 1077594.96600000001490116, 963448.43000000005122274 1077594.17299999995157123, 963457.29399999999441206 1077587.69100000010803342, 963462.84999999997671694 1077581.20800000010058284, 963464.18000000005122274 1077579.29799999995157123, 963472.24300000001676381 1077567.71399999991990626, 963476.80700000002980232 1077563.4150000000372529, 963481.37100000004284084 1077559.11499999999068677, 963487.98600000003352761 1077551.83899999991990626, 963497.24600000004284084 1077543.77000000001862645, 963510.162999999942258 1077534.63999999989755452, 963514.84100000001490116 1077531.33400000003166497, 963522.11699999996926636 1077524.32300000009126961, 963522.93700000003445894 1077523.79099999996833503, 963529.08600000001024455 1077519.80099999997764826, 963523.76100000005681068 1077504.57199999992735684, 963494.36399999994318932 1077519.02499999990686774, 963458.98600000003352761 1077559.13599999994039536, 963429.6530000000493601 1077597.34000000008381903, 963351.8349999999627471 1077674.02700000000186265)),((963532.79200000001583248 1077522.98399999993853271, 963523.15899999998509884 1077532.80499999993480742, 963511.93999999994412065 1077541.69500000006519258, 963510.74300000001676381 1077542.71600000001490116, 963504.74399999994784594 1077547.83300000010058284, 963493.41700000001583248 1077557.11700000008568168, 963491.83200000005308539 1077558.41699999989941716, 963489.80099999997764826 1077560.4909999999217689, 963482.09499999997206032 1077568.36499999999068677, 963472.78200000000651926 1077577.25499999988824129, 963464.94999999995343387 1077588.89700000011362135, 963456.06000000005587935 1077595.45800000010058284, 963445.05000000004656613 1077602.83799999998882413, 963439.88399999996181577 1077606.30000000004656613, 963410.07400000002235174 1077628.28700000001117587, 963401.24800000002142042 1077637.55099999997764826, 963374.96799999999348074 1077665.13599999994039536, 963368.28500000003259629 1077670.45200000004842877, 963367.51500000001396984 1077671.06400000001303852, 963361.61100000003352761 1077675.76099999994039536, 963356.09900000004563481 1077680.14599999994970858, 963322.17500000004656613 1077706.7099999999627471, 963491.84600000001955777 1077855.12599999993108213, 963516.67000000004190952 1077825.98500000010244548, 963557.90800000005401671 1077757.82099999999627471, 963654.3090000000083819 1077682.68599999998696148, 963683.5400000000372529 1077652.43100000009872019, 963532.79200000001583248 1077522.98399999993853271)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '11',
                            'nombre': '11primer nombre 11segundo nombre 11primero apellido 11segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230069000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': 'aab6849',
                    'numero_predial': '253940000000000230069000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 978,
                    'area_terreno': 28125.31,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963105.46600000001490116 1077266.95600000000558794, 963121.11399999994318932 1077286.72999999998137355, 963125.37600000004749745 1077299.02200000011362135, 963106.92099999997299165 1077371.54799999995157123, 963130.39899999997578561 1077377.34300000010989606, 963133.31700000003911555 1077377.40100000007078052, 963247.77700000000186265 1077461.75600000005215406, 963308.61199999996460974 1077399.01799999992363155, 963316.69499999994877726 1077380.85599999991245568, 963247.5659999999916181 1077294.32899999991059303, 963236.87800000002607703 1077314.79399999999441206, 963230.50699999998323619 1077324.55300000007264316, 963223.85800000000745058 1077331.60000000009313226, 963167.14199999999254942 1077308.31899999990127981, 963163.99199999996926636 1077292.59700000006705523, 963163.49899999995250255 1077270.92699999990873039, 963166.65599999995902181 1077249.80199999990873039, 963105.46600000001490116 1077266.95600000000558794)),((963252.98400000005494803 1077464.47699999995529652, 963313.09400000004097819 1077509.02399999997578561, 963360.37100000004284084 1077475.44399999990127981, 963368.18799999996554106 1077447.75499999988824129, 963314.14300000004004687 1077404.88899999996647239, 963252.98400000005494803 1077464.47699999995529652)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '13',
                            'nombre': '13primer nombre 13segundo nombre 13primero apellido 13segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230079000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': 'c955757',
                    'numero_predial': '253940000000000230079000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 979,
                    'area_terreno': 15073.75,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963722.36800000001676381 1077109.49200000008568168, 963740.38399999996181577 1077099.46900000004097819, 963766.875 1077090.20900000003166497, 963776.40000000002328306 1077088.09199999994598329, 963792.01000000000931323 1077089.28300000005401671, 963805.37199999997392297 1077094.04600000008940697, 963815.55799999996088445 1077099.46900000004097819, 963840.69400000001769513 1077119.7099999999627471, 963854.31999999994877726 1077127.91200000001117587, 963871.58299999998416752 1077130.39400000008754432, 963900.98300000000745058 1077206.71800000010989606, 963858.20100000000093132 1077230.7479999999050051, 963775.98699999996460974 1077246.03000000002793968, 963779.01500000001396984 1077150.40100000007078052, 963746.39000000001396984 1077120.55799999996088445, 963722.36800000001676381 1077109.49200000008568168)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '16',
                            'nombre': '16primer nombre 16segundo nombre 16primero apellido 16segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230057000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '97e281a',
                    'numero_predial': '253940000000000230057000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 981,
                    'area_terreno': 818.82,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963361.71600000001490116 1077499.76399999996647239, 963397.95700000005308539 1077538.45399999991059303, 963387.60900000005494803 1077549.35599999991245568, 963376.43999999994412065 1077537.31899999990127981, 963350.61800000001676381 1077510.51300000003539026, 963357.74899999995250255 1077501.35599999991245568, 963361.71600000001490116 1077499.76399999996647239)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '19',
                            'nombre': '19primer nombre 19segundo nombre 19primero apellido 19segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230056000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '7d6dad4',
                    'numero_predial': '253940000000000230056000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 982,
                    'area_terreno': 4814.39,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963479.16000000003259629 1077351.29499999992549419, 963492.73300000000745058 1077318.97299999999813735, 963498.00300000002607703 1077309.83799999998882413, 963502.98400000005494803 1077297.89400000008754432, 963508.81099999998696148 1077274.89100000006146729, 963519.10400000005029142 1077256.44800000009126961, 963568.8279999999795109 1077265.58799999998882413, 963546.46100000001024455 1077303.26099999994039536, 963516.16099999996367842 1077366.59700000006705523, 963506.0849999999627471 1077369.162999999942258, 963479.16000000003259629 1077351.29499999992549419)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '20',
                            'nombre': '20primer nombre 20segundo nombre 20primero apellido 20segundo apellido',
                            'derecho': NULL
                        }
                    ]
                },
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '83d1096',
                    'numero_predial': '253940000000000230056000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 983,
                    'area_terreno': 2330.82,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963528.16599999996833503 1077177.04399999999441206, 963554.77399999997578561 1077165.78000000002793968, 963556.67299999995157123 1077158.74300000001676381, 963493.62899999995715916 1077125.93299999996088445, 963474.51599999994505197 1077133.38100000005215406, 963470.2900000000372529 1077135.93800000008195639, 963461.71299999998882413 1077144.55099999997764826, 963528.16599999996833503 1077177.04399999999441206)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '21',
                            'nombre': '21primer nombre 21segundo nombre 21primero apellido 21segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230213000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': 'f4251a9',
                    'numero_predial': '253940000000000230213000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 984,
                    'area_terreno': 7307.28,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963516.16099999996367842 1077366.59700000006705523, 963506.0849999999627471 1077369.162999999942258, 963485.87699999997857958 1077390.93900000001303852, 963500.4599999999627471 1077410.17100000008940697, 963527.53599999996367842 1077431.21600000001490116, 963565.55200000002514571 1077469.65299999993294477, 963584.20700000005308539 1077451.68500000005587935, 963621.47600000002421439 1077426.2099999999627471, 963554.02000000001862645 1077366.51099999994039536, 963516.16099999996367842 1077366.59700000006705523)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '22',
                            'nombre': '22primer nombre 22segundo nombre 22primero apellido 22segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230098000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': 'd2e5624',
                    'numero_predial': '253940000000000230098000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 985,
                    'area_terreno': 1808.06,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963314.14300000004004687 1077404.88899999996647239, 963319.42000000004190952 1077382.33199999993667006, 963325.14500000001862645 1077388.14400000008754432, 963388.79500000004190952 1077427.97399999992921948, 963368.18799999996554106 1077447.75499999988824129, 963314.14300000004004687 1077404.88899999996647239)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '23',
                            'nombre': '23primer nombre 23segundo nombre 23primero apellido 23segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230097000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '9698161',
                    'numero_predial': '253940000000000230097000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 986,
                    'area_terreno': 749.75,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963163.99199999996926636 1077292.59700000006705523, 963230.50699999998323619 1077324.55300000007264316, 963223.85800000000745058 1077331.60000000009313226, 963167.14199999999254942 1077308.31899999990127981, 963163.99199999996926636 1077292.59700000006705523)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '24',
                            'nombre': '24primer nombre 24segundo nombre 24primero apellido 24segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230054000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '3544b9b',
                    'numero_predial': '253940000000000230054000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 987,
                    'area_terreno': 2301.52,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963166.65599999995902181 1077249.80199999990873039, 963170.24699999997392297 1077250.36299999989569187, 963198.3349999999627471 1077258.8840000000782311, 963203.76399999996647239 1077262.1720000000204891, 963228.04099999996833503 1077278.587000000057742, 963247.5659999999916181 1077294.32899999991059303, 963236.87800000002607703 1077314.79399999999441206, 963163.49899999995250255 1077270.92699999990873039, 963166.65599999995902181 1077249.80199999990873039)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '26',
                            'nombre': '26primer nombre 26segundo nombre 26primero apellido 26segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230074000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '40f62d8',
                    'numero_predial': '253940000000000230074000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 988,
                    'area_terreno': 7520.37,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963217.97999999998137355 1077784.86299999989569187, 963288.55500000005122274 1077715.87199999997392297, 963311.33400000003166497 1077703.05400000000372529, 963351.8349999999627471 1077674.02700000000186265, 963364.45400000002700835 1077665.63599999994039536, 963374.95799999998416752 1077655.55499999993480742, 963379.53300000005401671 1077651.16400000010617077, 963384.79799999995157123 1077646.29600000008940697, 963403.65599999995902181 1077628.13199999998323619, 963403.91000000003259629 1077627.88800000003539026, 963406.65099999995436519 1077625.24699999997392297, 963421.37199999997392297 1077614.59000000008381903, 963436.44799999997485429 1077603.29099999996833503, 963438.90500000002793968 1077601.44900000002235174, 963447.39300000004004687 1077594.96600000001490116, 963448.43000000005122274 1077594.17299999995157123, 963457.29399999999441206 1077587.69100000010803342, 963462.84999999997671694 1077581.20800000010058284, 963464.18000000005122274 1077579.29799999995157123, 963472.24300000001676381 1077567.71399999991990626, 963476.80700000002980232 1077563.4150000000372529, 963481.37100000004284084 1077559.11499999999068677, 963487.98600000003352761 1077551.83899999991990626, 963497.24600000004284084 1077543.77000000001862645, 963510.162999999942258 1077534.63999999989755452, 963514.84100000001490116 1077531.33400000003166497, 963522.11699999996926636 1077524.32300000009126961, 963522.93700000003445894 1077523.79099999996833503, 963529.08600000001024455 1077519.80099999997764826, 963538.23400000005494803 1077515.712000000057742, 963543.63100000005215406 1077509.67999999993480742, 963554.42599999997764826 1077495.86800000001676381, 963565.22100000001955777 1077487.61299999989569187, 963574.58799999998882413 1077477.29499999992549419, 963591.4150000000372529 1077463.32499999995343387, 963592.96799999999348074 1077462.00300000002607703, 963595.2900000000372529 1077460.02799999993294477, 963602.05099999997764826 1077454.27600000007078052, 963614.4340000000083819 1077444.27399999997578561, 963624.59400000004097819 1077436.97200000006705523, 963634.912999999942258 1077433.16200000001117587, 963641.26300000003539026 1077428.39899999997578561, 963647.61300000001210719 1077419.98600000003352761, 963650.31099999998696148 1077411.09599999990314245, 963650.75600000005215406 1077410.28600000008009374, 963657.45499999995809048 1077398.0779999999795109, 963665.60499999998137355 1077381.68299999996088445, 963675.40200000000186265 1077331.09499999997206032, 963680.36800000001676381 1077320.8279999999795109, 963713.56299999996554106 1077292.69299999997019768, 963728.30599999998230487 1077270.02099999994970858, 963775.98699999996460974 1077246.03000000002793968, 963858.20100000000093132 1077230.7479999999050051, 963900.98300000000745058 1077206.71800000010989606, 963914.53700000001117587 1077209.08000000007450581, 963997.61699999996926636 1077228.95500000007450581, 964023.76100000005681068 1077222.39599999994970858, 964057.53200000000651926 1077205.07199999992735684, 964098.30200000002514571 1077196.3840000000782311, 964098.231000000028871 1077211.20800000010058284, 964092.30299999995622784 1077207.74699999997392297, 964060.35499999998137355 1077209.47299999999813735, 964024.32099999999627471 1077226.37400000006891787, 963997.83900000003632158 1077232.80000000004656613, 963953.34900000004563481 1077225.72299999999813735, 963913.16200000001117587 1077217.32700000004842877, 963896.32900000002700835 1077224.11499999999068677, 963860.60499999998137355 1077239.7029999999795109, 963775.34900000004563481 1077253.23399999993853271, 963734.01100000005681068 1077272.81400000001303852, 963718.33799999998882413 1077296.33899999991990626, 963684.52599999995436519 1077323.9220000000204891, 963669.84600000001955777 1077384.62599999993108213, 963669.84499999997206032 1077384.62599999993108213, 963668.03000000002793968 1077388.27600000007078052, 963667.92099999997299165 1077388.49600000004284084, 963661.69400000001769513 1077401.02300000004470348, 963656.90200000000186265 1077409.75499999988824129, 963654.55000000004656613 1077414.0400000000372529, 963654.37300000002142042 1077414.6229999999050051, 963651.85199999995529652 1077422.92999999993480742, 963645.50199999997857958 1077431.34400000004097819, 963639.15099999995436519 1077436.10700000007636845, 963631.86899999994784594 1077438.79499999992549419, 963628.83299999998416752 1077439.91699999989941716, 963628.07600000000093132 1077440.46099999989382923, 963619.05700000002980232 1077446.94299999997019768, 963618.67299999995157123 1077447.21900000004097819, 963606.2900000000372529 1077457.21999999997206032, 963600.9719999999506399 1077461.74500000011175871, 963595.65399999998044223 1077466.26900000008754432, 963578.82600000000093132 1077480.23900000005960464, 963576.48199999995995313 1077482.82199999992735684, 963571.70400000002700835 1077488.08599999989382923, 963569.4599999999627471 1077490.55799999996088445, 963560.89199999999254942 1077497.11000000010244548, 963558.6650000000372529 1077498.81300000008195639, 963555.64500000001862645 1077502.67599999997764826, 963547.86999999999534339 1077512.62400000006891787, 963542.47299999999813735 1077518.65699999989010394, 963537.89899999997578561 1077520.700999999884516, 963532.79200000001583248 1077522.98399999993853271, 963523.15899999998509884 1077532.80499999993480742, 963511.93999999994412065 1077541.69500000006519258, 963510.74300000001676381 1077542.71600000001490116, 963504.74399999994784594 1077547.83300000010058284, 963493.41700000001583248 1077557.11700000008568168, 963491.83200000005308539 1077558.41699999989941716, 963489.80099999997764826 1077560.4909999999217689, 963482.09499999997206032 1077568.36499999999068677, 963472.78200000000651926 1077577.25499999988824129, 963464.94999999995343387 1077588.89700000011362135, 963456.06000000005587935 1077595.45800000010058284, 963445.05000000004656613 1077602.83799999998882413, 963439.88399999996181577 1077606.30000000004656613, 963410.07400000002235174 1077628.28700000001117587, 963401.24800000002142042 1077637.55099999997764826, 963374.96799999999348074 1077665.13599999994039536, 963368.28500000003259629 1077670.45200000004842877, 963367.51500000001396984 1077671.06400000001303852, 963361.61100000003352761 1077675.76099999994039536, 963356.09900000004563481 1077680.14599999994970858, 963322.17500000004656613 1077706.7099999999627471, 963294.10900000005494803 1077723.28399999998509884, 963224.99300000001676381 1077789.93299999996088445, 963217.97999999998137355 1077784.86299999989569187)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '28',
                            'nombre': '28primer nombre 28segundo nombre 28primero apellido 28segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000320022000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '757ec82',
                    'numero_predial': '253940000000000320022000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 989,
                    'GEOMETRY_PLOT': None,
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '29',
                            'nombre': '29primer nombre 29segundo nombre 29primero apellido 29segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230235000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '3b1296d',
                    'numero_predial': '253940000000000230235000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 990,
                    'area_terreno': 7691.6,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963871.58299999998416752 1077130.39400000008754432, 963900.98300000000745058 1077206.71800000010989606, 963914.53700000001117587 1077209.08000000007450581, 963997.61699999996926636 1077228.95500000007450581, 963999.02899999998044223 1077160.7520000000949949, 963871.58299999998416752 1077130.39400000008754432)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '31',
                            'nombre': '31primer nombre 31segundo nombre 31primero apellido 31segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230055000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': 'b7b500c',
                    'numero_predial': '253940000000000230055000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 993,
                    'area_terreno': 12095.39,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963630.4409999999916181 1077094.90200000000186265, 963633.32900000002700835 1077093.29199999989941716, 963636.30599999998230487 1077091.95699999993667006, 963621.731000000028871 1077122.64299999992363155, 963614.21100000001024455 1077128.07300000009126961, 963586.19900000002235174 1077146.11000000010244548, 963580.79899999999906868 1077147.70200000004842877, 963575.67700000002514571 1077153.21299999998882413, 963559.68099999998230487 1077171.38700000010430813, 963543.20499999995809048 1077199.95500000007450581, 963519.10400000005029142 1077256.44800000009126961, 963508.81099999998696148 1077274.89100000006146729, 963502.98400000005494803 1077297.89400000008754432, 963498.00300000002607703 1077309.83799999998882413, 963492.73300000000745058 1077318.97299999999813735, 963479.16000000003259629 1077351.29499999992549419, 963458.00300000002607703 1077360.37400000006891787, 963438.72800000000279397 1077382.81899999990127981, 963428.88600000005681068 1077398.67800000007264316, 963418.89699999999720603 1077419.45200000004842877, 963414.26300000003539026 1077422.27300000004470348, 963386.11399999994318932 1077448.76699999999254942, 963372.00699999998323619 1077487.31899999990127981, 963365.61999999999534339 1077490.59400000004097819, 963361.71600000001490116 1077499.76399999996647239, 963357.74899999995250255 1077501.35599999991245568, 963350.61800000001676381 1077510.51300000003539026, 963326.04799999995157123 1077528.81300000008195639, 963319.70100000000093132 1077531.6720000000204891, 963310.42399999999906868 1077542.57000000006519258, 963308.26800000004004687 1077549.42999999993480742, 963305.4220000000204891 1077553.60199999995529652, 963290.25899999996181577 1077565.4150000000372529, 963279.78099999995902181 1077578.49699999997392297, 963264.23600000003352761 1077593.90999999991618097, 963242.00500000000465661 1077610.7590000000782311, 963235.52300000004470348 1077621.91599999996833503, 963214.84799999999813735 1077650.3770000000949949, 963200.18299999996088445 1077679.35800000000745058, 963180.26399999996647239 1077705.22299999999813735, 963163.48999999999068677 1077729.76699999999254942, 963131.37699999997857958 1077725.60899999993853271, 963144.32099999999627471 1077599.59700000006705523, 963312.337000000057742 1077513.68299999996088445, 963313.09400000004097819 1077509.02399999997578561, 963360.37100000004284084 1077475.44399999990127981, 963368.18799999996554106 1077447.75499999988824129, 963388.79500000004190952 1077427.97399999992921948, 963393.06000000005587935 1077424.39999999990686774, 963424.43500000005587935 1077378.12199999997392297, 963424.84900000004563481 1077377.26900000008754432, 963449.61999999999534339 1077352.06000000005587935, 963495.65800000005401671 1077274.45900000003166497, 963496.32099999999627471 1077252.37199999997392297, 963497 1077239.97500000009313226, 963504.01000000000931323 1077221.72799999988637865, 963517.43099999998230487 1077202.15400000009685755, 963529.96400000003632158 1077195.14199999999254942, 963528.16599999996833503 1077177.04399999999441206, 963554.77399999997578561 1077165.78000000002793968, 963556.67299999995157123 1077158.74300000001676381, 963571.89300000004004687 1077151.575999999884516, 963581.11499999999068677 1077142.33199999993667006, 963585.72699999995529652 1077142.15500000002793968, 963608.10100000002421439 1077128.76000000000931323, 963630.4409999999916181 1077094.90200000000186265)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '34',
                            'nombre': '34primer nombre 34segundo nombre 34primero apellido 34segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230242000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': 'cd9718f',
                    'numero_predial': '253940000000000230242000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 994,
                    'area_terreno': 10986.03,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963224.99300000001676381 1077789.93299999996088445, 963238.74199999996926636 1077799.87199999997392297, 963294.10900000005494803 1077723.28399999998509884, 963224.99300000001676381 1077789.93299999996088445)),((963235.52300000004470348 1077621.91599999996833503, 963214.84799999999813735 1077650.3770000000949949, 963200.18299999996088445 1077679.35800000000745058, 963180.26399999996647239 1077705.22299999999813735, 963163.48999999999068677 1077729.76699999999254942, 963144.32099999999627471 1077802.22799999988637865, 963217.97999999998137355 1077784.86299999989569187, 963288.55500000005122274 1077715.87199999997392297, 963260.4409999999916181 1077686.07899999991059303, 963268.41000000003259629 1077671.37199999997392297, 963264.43700000003445894 1077659.64599999994970858, 963268.18099999998230487 1077652.43800000008195639, 963264.13800000003539026 1077649.62100000004284084, 963235.52300000004470348 1077621.91599999996833503)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '35',
                            'nombre': '35primer nombre 35segundo nombre 35primero apellido 35segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230076000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '7b3c311',
                    'numero_predial': '253940000000000230076000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 999,
                    'area_terreno': 1210.57,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963163.49899999995250255 1077270.92699999990873039, 963236.87800000002607703 1077314.79399999999441206, 963230.50699999998323619 1077324.55300000007264316, 963163.99199999996926636 1077292.59700000006705523, 963163.49899999995250255 1077270.92699999990873039)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '41',
                            'nombre': '41primer nombre 41segundo nombre 41primero apellido 41segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230241000000994': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '528b942',
                    'numero_predial': '253940000000000230241000000994',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 1001,
                    'area_terreno': 4200.03,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963479.16000000003259629 1077351.29499999992549419, 963506.0849999999627471 1077369.162999999942258, 963485.87699999997857958 1077390.93900000001303852, 963500.4599999999627471 1077410.17100000008940697, 963468.768999999971129 1077434.62100000004284084, 963418.89699999999720603 1077419.45200000004842877, 963428.88600000005681068 1077398.67800000007264316, 963438.72800000000279397 1077382.81899999990127981, 963458.00300000002607703 1077360.37400000006891787, 963479.16000000003259629 1077351.29499999992549419)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '45',
                            'nombre': '45primer nombre 45segundo nombre 45primero apellido 45segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230241000000995': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '4144e2b',
                    'numero_predial': '253940000000000230241000000995',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 1002,
                    'area_terreno': 25178.2,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963254.89899999997578561 1077285.69999999995343387, 963265.26000000000931323 1077293.62199999997392297, 963304.04799999995157123 1077221.2590000000782311, 963329.412999999942258 1077175.15400000009685755, 963259.08299999998416752 1077133.05600000009872019, 963257.85199999995529652 1077132.22600000002421439, 963239.31900000001769513 1077113.19900000002235174, 963208.73999999999068677 1077026.23699999996460974, 963060.56000000005587935 1077061.94299999997019768, 962999.85999999998603016 1077150.61299999989569187, 963011.76199999998789281 1077181.55799999996088445, 963047.46799999999348074 1077206.55199999990873039, 963145.54399999999441206 1077218.64599999994970858, 963174.71299999998882413 1077227.43399999989196658, 963184.77000000001862645 1077229.55400000000372529, 963203.15000000002328306 1077248.26300000003539026, 963254.89899999997578561 1077285.69999999995343387)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '46',
                            'nombre': '46primer nombre 46segundo nombre 46primero apellido 46segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230241000000996': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': 'b6f7ca6',
                    'numero_predial': '253940000000000230241000000996',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 1003,
                    'area_terreno': 1377.2,
                    'GEOMETRY_PLOT': 'MultiPolygon (((964049.44900000002235174 1077233.55099999997764826, 964063.02099999994970858 1077213.79199999989941716, 964060.35499999998137355 1077209.47299999999813735, 964092.30299999995622784 1077207.74699999997392297, 964098.231000000028871 1077211.20800000010058284, 964100.34400000004097819 1077222.03300000005401671, 964095.125 1077244.7029999999795109, 964077.49699999997392297 1077242.10000000009313226, 964051.52700000000186265 1077236.58899999991990626, 964049.44900000002235174 1077233.55099999997764826)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '47',
                            'nombre': '47primer nombre 47segundo nombre 47primero apellido 47segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230241000000997': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '5d1413f',
                    'numero_predial': '253940000000000230241000000997',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 1004,
                    'area_terreno': 7983.14,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963999.02899999998044223 1077160.7520000000949949, 964018.56400000001303852 1077137.9599999999627471, 964056.16200000001117587 1077103.8279999999795109, 964095.587000000057742 1077117.93800000008195639, 964122.96100000001024455 1077129.98900000005960464, 964169.88100000005215406 1077129.24500000011175871, 964098.30200000002514571 1077196.3840000000782311, 964057.53200000000651926 1077205.07199999992735684, 964023.76100000005681068 1077222.39599999994970858, 963997.61699999996926636 1077228.95500000007450581, 963999.02899999998044223 1077160.7520000000949949)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '48',
                            'nombre': '48primer nombre 48segundo nombre 48primero apellido 48segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230073000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '97f8fbe',
                    'numero_predial': '253940000000000230073000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 1005,
                    'area_terreno': 4283.74,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963546.46100000001024455 1077303.26099999994039536, 963614.23899999994318932 1077313.6720000000204891, 963631.17900000000372529 1077251.375, 963599.68200000002980232 1077224.26600000006146729, 963568.8279999999795109 1077265.58799999998882413, 963546.46100000001024455 1077303.26099999994039536)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '49',
                            'nombre': '49primer nombre 49segundo nombre 49primero apellido 49segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230241000000998': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '658fd65',
                    'numero_predial': '253940000000000230241000000998',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 1006,
                    'area_terreno': 2614.27,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963500.4599999999627471 1077410.17100000008940697, 963527.53599999996367842 1077431.21600000001490116, 963565.55200000002514571 1077469.65299999993294477, 963547.99399999994784594 1077479.15400000009685755, 963503.45900000003166497 1077453.82899999991059303, 963468.768999999971129 1077434.62100000004284084, 963500.4599999999627471 1077410.17100000008940697)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '50',
                            'nombre': '50primer nombre 50segundo nombre 50primero apellido 50segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230241000000999': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '166a1b6',
                    'numero_predial': '253940000000000230241000000999',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 1007,
                    'area_terreno': 21907.65,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963424.84900000004563481 1077377.26900000008754432, 963449.61999999999534339 1077352.06000000005587935, 963400.06099999998696148 1077310.90299999993294477, 963434.03000000002793968 1077254.76900000008754432, 963495.65800000005401671 1077274.45900000003166497, 963496.32099999999627471 1077252.37199999997392297, 963497 1077239.97500000009313226, 963504.01000000000931323 1077221.72799999988637865, 963420.13100000005215406 1077187.15599999995902181, 963400.52099999994970858 1077215.42699999990873039, 963378.57999999995809048 1077281.69500000006519258, 963343.66099999996367842 1077330.41599999996833503, 963424.84900000004563481 1077377.26900000008754432)),((963376.02899999998044223 1077279.62599999993108213, 963396.74800000002142042 1077213.01600000006146729, 963415.96799999999348074 1077184.47699999995529652, 963368.31900000001769513 1077155.28499999991618097, 963355.23300000000745058 1077168.81099999998696148, 963247.04200000001583248 1077094.51699999999254942, 963239.31900000001769513 1077113.19900000002235174, 963257.85199999995529652 1077132.22600000002421439, 963259.08299999998416752 1077133.05600000009872019, 963329.412999999942258 1077175.15400000009685755, 963304.04799999995157123 1077221.2590000000782311, 963376.02899999998044223 1077279.62599999993108213)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '51',
                            'nombre': '51primer nombre 51segundo nombre 51primero apellido 51segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230072000000002': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '264c43a',
                    'numero_predial': '253940000000000230072000000002',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 1008,
                    'area_terreno': 6085.67,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963428.65200000000186265 1077489.20200000004842877, 963408.11999999999534339 1077525.30600000009872019, 963397.95700000005308539 1077538.45399999991059303, 963387.60900000005494803 1077549.35599999991245568, 963381.56999999994877726 1077567.29799999995157123, 963429.6530000000493601 1077597.34000000008381903, 963458.98600000003352761 1077559.13599999994039536, 963494.36399999994318932 1077519.02499999990686774, 963428.65200000000186265 1077489.20200000004842877)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '2',
                            'nombre': '2primer nombre 2segundo nombre 2primero apellido 2segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230241000000005': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': 'a6a81fc',
                    'numero_predial': '253940000000000230241000000005',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 1009,
                    'area_terreno': 3291.88,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963340.68700000003445894 1078024.52000000001862645, 963381.93099999998230487 1077954.86499999999068677, 963402.92500000004656613 1077934.5090000000782311, 963420.82099999999627471 1077909.42599999997764826, 963438.48300000000745058 1077883.48200000007636845, 963461.43000000005122274 1077875.79199999989941716, 963491.84600000001955777 1077855.12599999993108213, 963516.67000000004190952 1077825.98500000010244548, 963557.90800000005401671 1077757.82099999999627471, 963654.3090000000083819 1077682.68599999998696148, 963683.5400000000372529 1077652.43100000009872019, 963746.5280000000493601 1077563.51399999996647239, 963783.58100000000558794 1077497.82000000006519258, 963825.93599999998696148 1077393.0470000000204891, 963844.19499999994877726 1077361.89100000006146729, 963865.99699999997392297 1077355.64999999990686774, 963878.93999999994412065 1077348.74300000001676381, 963911.41899999999441206 1077312.82400000002235174, 963923.97400000004563481 1077315.69200000003911555, 963930.37100000004284084 1077313.76300000003539026, 963936.19400000001769513 1077299.07099999999627471, 963952.28599999996367842 1077303.86199999996460974, 963965.03300000005401671 1077283.20500000007450581, 963981.22900000005029142 1077286.68100000009872019, 963989.03700000001117587 1077276.12000000011175871, 964006.30599999998230487 1077272.12899999995715916, 964041.35199999995529652 1077238.9529999999795109, 964049.44900000002235174 1077233.55099999997764826, 964051.52700000000186265 1077236.58899999991990626, 964054.74800000002142042 1077257.2099999999627471, 964027.07600000000093132 1077279.82400000002235174, 964017.92599999997764826 1077291.35400000005029142, 964003.34600000001955777 1077302.51200000010430813, 963977.60800000000745058 1077305.78499999991618097, 963968.60699999995995313 1077315.53000000002793968, 963960.12699999997857958 1077320.36499999999068677, 963949.04399999999441206 1077322.37400000006891787, 963945.62199999997392297 1077333.23399999993853271, 963930.81900000001769513 1077341.86299999989569187, 963908.50199999997857958 1077350.49200000008568168, 963901.06400000001303852 1077362.69200000003911555, 963896.89800000004470348 1077379.05700000002980232, 963873.98699999996460974 1077405.2409999999217689, 963836.49499999999534339 1077513.549000000115484, 963784.12699999997857958 1077581.39100000006146729, 963719.26100000005681068 1077667.67999999993480742, 963676.41399999998975545 1077704.575999999884516, 963596.67000000004190952 1077781.34400000004097819, 963546.68200000002980232 1077842.04399999999441206, 963517.22499999997671694 1077870.31099999998696148, 963487.46999999997206032 1077888.462000000057742, 963477.05500000005122274 1077903.63700000010430813, 963461.28500000003259629 1077925.9529999999795109, 963438.37399999995250255 1077952.13700000010430813, 963412.48699999996460974 1077972.66800000006332994, 963352.8279999999795109 1078037.98099999991245568, 963340.68700000003445894 1078024.52000000001862645)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '5',
                            'nombre': '5primer nombre 5segundo nombre 5primero apellido 5segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230101000000011': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '31dad9e',
                    'numero_predial': '253940000000000230101000000011',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 1010,
                    'area_terreno': 11157.65,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963516.16099999996367842 1077366.59700000006705523, 963546.46100000001024455 1077303.26099999994039536, 963614.23899999994318932 1077313.6720000000204891, 963675.40200000000186265 1077331.09499999997206032, 963665.60499999998137355 1077381.68299999996088445, 963621.47600000002421439 1077426.2099999999627471, 963554.02000000001862645 1077366.51099999994039536, 963516.16099999996367842 1077366.59700000006705523)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '8',
                            'nombre': '8primer nombre 8segundo nombre 8primero apellido 8segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230070000000011': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': 'dbe0b75',
                    'numero_predial': '253940000000000230070000000011',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 1011,
                    'area_terreno': 2032.36,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963530.28200000000651926 1077096.25799999991431832, 963534.88600000005681068 1077096.61000000010244548, 963512.12300000002142042 1077118.00499999988824129, 963493.62899999995715916 1077125.93299999996088445, 963474.51599999994505197 1077133.38100000005215406, 963470.2900000000372529 1077135.93800000008195639, 963461.71299999998882413 1077144.55099999997764826, 963438.18200000002980232 1077161.11199999996460974, 963420.13100000005215406 1077187.15599999995902181, 963400.52099999994970858 1077215.42699999990873039, 963378.57999999995809048 1077281.69500000006519258, 963343.66099999996367842 1077330.41599999996833503, 963319.42000000004190952 1077382.33199999993667006, 963314.14300000004004687 1077404.88899999996647239, 963252.98400000005494803 1077464.47699999995529652, 963247.77700000000186265 1077461.75600000005215406, 963308.61199999996460974 1077399.01799999992363155, 963316.69499999994877726 1077380.85599999991245568, 963340.90700000000651926 1077328.9979999999050051, 963376.02899999998044223 1077279.62599999993108213, 963396.74800000002142042 1077213.01600000006146729, 963415.96799999999348074 1077184.47699999995529652, 963434.04200000001583248 1077158.66699999989941716, 963458.83200000005308539 1077139.48600000003352761, 963473.43099999998230487 1077131.84499999997206032, 963509.643999999971129 1077116.61299999989569187, 963530.28200000000651926 1077096.25799999991431832)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '12',
                            'nombre': '12primer nombre 12segundo nombre 12primero apellido 12segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230077000000665': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '962b494',
                    'numero_predial': '253940000000000230077000000665',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 1012,
                    'area_terreno': 1974.4,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963512.12300000002142042 1077118.00499999988824129, 963534.88600000005681068 1077096.61000000010244548, 963608.10100000002421439 1077128.76000000000931323, 963585.72699999995529652 1077142.15500000002793968, 963581.11499999999068677 1077142.33199999993667006, 963512.12300000002142042 1077118.00499999988824129)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '14',
                            'nombre': '14primer nombre 14segundo nombre 14primero apellido 14segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230078000000010': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': 'dc4c738',
                    'numero_predial': '253940000000000230078000000010',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 1013,
                    'area_terreno': 1320.35,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963247.5659999999916181 1077294.32899999991059303, 963254.89899999997578561 1077285.69999999995343387, 963203.15000000002328306 1077248.26300000003539026, 963184.77000000001862645 1077229.55400000000372529, 963174.71299999998882413 1077227.43399999989196658, 963166.65599999995902181 1077249.80199999990873039, 963170.24699999997392297 1077250.36299999989569187, 963198.3349999999627471 1077258.8840000000782311, 963203.76399999996647239 1077262.1720000000204891, 963228.04099999996833503 1077278.587000000057742, 963247.5659999999916181 1077294.32899999991059303)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '15',
                            'nombre': '15primer nombre 15segundo nombre 15primero apellido 15segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230257000000005': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '8c8d901',
                    'numero_predial': '253940000000000230257000000005',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 1014,
                    'area_terreno': 877.88,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963372.00699999998323619 1077487.31899999990127981, 963408.11999999999534339 1077525.30600000009872019, 963397.95700000005308539 1077538.45399999991059303, 963361.71600000001490116 1077499.76399999996647239, 963365.61999999999534339 1077490.59400000004097819, 963372.00699999998323619 1077487.31899999990127981)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '25',
                            'nombre': '25primer nombre 25segundo nombre 25primero apellido 25segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230241000000011': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': 'a662c27',
                    'numero_predial': '253940000000000230241000000011',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 1015,
                    'area_terreno': 30777.21,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963614.21100000001024455 1077128.07300000009126961, 963621.731000000028871 1077122.64299999992363155, 963636.30599999998230487 1077091.95699999993667006, 963646.0779999999795109 1077074.34799999999813735, 963722.36800000001676381 1077109.49200000008568168, 963746.39000000001396984 1077120.55799999996088445, 963779.01500000001396984 1077150.40100000007078052, 963775.98699999996460974 1077246.03000000002793968, 963728.30599999998230487 1077270.02099999994970858, 963713.56299999996554106 1077292.69299999997019768, 963680.36800000001676381 1077320.8279999999795109, 963675.40200000000186265 1077331.09499999997206032, 963614.23899999994318932 1077313.6720000000204891, 963631.17900000000372529 1077251.375, 963599.68200000002980232 1077224.26600000006146729, 963543.20499999995809048 1077199.95500000007450581, 963559.68099999998230487 1077171.38700000010430813, 963575.67700000002514571 1077153.21299999998882413, 963580.79899999999906868 1077147.70200000004842877, 963624.64899999997578561 1077205.93399999989196658, 963655.29200000001583248 1077187.44900000002235174, 963671.17500000004656613 1077163.80899999989196658, 963659.34199999994598329 1077146.59199999994598329, 963614.21100000001024455 1077128.07300000009126961)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '44',
                            'nombre': '44primer nombre 44segundo nombre 44primero apellido 44segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230080000001651': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '0c4e185',
                    'numero_predial': '253940000000000230080000001651',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 1016,
                    'area_terreno': 2267.45,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963438.18200000002980232 1077161.11199999996460974, 963461.71299999998882413 1077144.55099999997764826, 963528.16599999996833503 1077177.04399999999441206, 963529.96400000003632158 1077195.14199999999254942, 963517.43099999998230487 1077202.15400000009685755, 963438.18200000002980232 1077161.11199999996460974)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '17',
                            'nombre': '17primer nombre 17segundo nombre 17primero apellido 17segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230097000131854': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': 'ca366db',
                    'numero_predial': '253940000000000230097000131854',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 1017,
                    'area_terreno': 3056.48,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963543.20499999995809048 1077199.95500000007450581, 963519.10400000005029142 1077256.44800000009126961, 963568.8279999999795109 1077265.58799999998882413, 963599.68200000002980232 1077224.26600000006146729, 963543.20499999995809048 1077199.95500000007450581)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '27',
                            'nombre': '27primer nombre 27segundo nombre 27primero apellido 27segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230254000001354': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': 'c3ae78c',
                    'numero_predial': '253940000000000230254000001354',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 1018,
                    'area_terreno': 4934.25,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963449.61999999999534339 1077352.06000000005587935, 963495.65800000005401671 1077274.45900000003166497, 963434.03000000002793968 1077254.76900000008754432, 963400.06099999998696148 1077310.90299999993294477, 963449.61999999999534339 1077352.06000000005587935)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '30',
                            'nombre': '30primer nombre 30segundo nombre 30primero apellido 30segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230241000000163': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '5743f48',
                    'numero_predial': '253940000000000230241000000163',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 1019,
                    'area_terreno': 10495.07,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963418.89699999999720603 1077419.45200000004842877, 963468.768999999971129 1077434.62100000004284084, 963503.45900000003166497 1077453.82899999991059303, 963547.99399999994784594 1077479.15400000009685755, 963523.76100000005681068 1077504.57199999992735684, 963494.36399999994318932 1077519.02499999990686774, 963428.65200000000186265 1077489.20200000004842877, 963408.11999999999534339 1077525.30600000009872019, 963372.00699999998323619 1077487.31899999990127981, 963386.11399999994318932 1077448.76699999999254942, 963414.26300000003539026 1077422.27300000004470348, 963418.89699999999720603 1077419.45200000004842877)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '37',
                            'nombre': '37primer nombre 37segundo nombre 37primero apellido 37segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230234000005646': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '0035944',
                    'numero_predial': '253940000000000230234000005646',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 1020,
                    'GEOMETRY_PLOT': None,
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '42',
                            'nombre': '42primer nombre 42segundo nombre 42primero apellido 42segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ],
            '253940000000000230099335131315': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '1fae15c',
                    'numero_predial': '253940000000000230099335131315',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 1021,
                    'area_terreno': 12960.6,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963247.04200000001583248 1077094.51699999999254942, 963316.60199999995529652 1077064.30499999993480742, 963379.38500000000931323 1077047.93999999994412065, 963437.40700000000651926 1077039.31099999998696148, 963500.18999999994412065 1077059.24699999997392297, 963530.28200000000651926 1077096.25799999991431832, 963509.643999999971129 1077116.61299999989569187, 963473.43099999998230487 1077131.84499999997206032, 963458.83200000005308539 1077139.48600000003352761, 963434.04200000001583248 1077158.66699999989941716, 963415.96799999999348074 1077184.47699999995529652, 963368.31900000001769513 1077155.28499999991618097, 963355.23300000000745058 1077168.81099999998696148, 963247.04200000001583248 1077094.51699999999254942)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '6',
                            'nombre': '6primer nombre 6segundo nombre 6primero apellido 6segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ]
        }
        features = self.ladm_data.get_parcel_data_to_compare_changes_supplies(self.db_pg)
        normalize_responce(features)
        self.assertEqual(features, features_test)

        print("\nINFO: Validating get parcels data using search criterion...")

        features_test = {
            '253940000000000230099335131315': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '1fae15c',
                    'numero_predial': '253940000000000230099335131315',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 1021,
                    'area_terreno': 12960.6,
                    'GEOMETRY_PLOT': 'MultiPolygon (((963247.04200000001583248 1077094.51699999999254942, 963316.60199999995529652 1077064.30499999993480742, 963379.38500000000931323 1077047.93999999994412065, 963437.40700000000651926 1077039.31099999998696148, 963500.18999999994412065 1077059.24699999997392297, 963530.28200000000651926 1077096.25799999991431832, 963509.643999999971129 1077116.61299999989569187, 963473.43099999998230487 1077131.84499999997206032, 963458.83200000005308539 1077139.48600000003352761, 963434.04200000001583248 1077158.66699999989941716, 963415.96799999999348074 1077184.47699999995529652, 963368.31900000001769513 1077155.28499999991618097, 963355.23300000000745058 1077168.81099999998696148, 963247.04200000001583248 1077094.51699999999254942)))',
                    'Interesados': [
                        {
                            'tipo_documento': 'Cédula de ciudadanía',
                            'documento_identidad': '6',
                            'nombre': '6primer nombre 6segundo nombre 6primero apellido 6segundo apellido',
                            'derecho': NULL
                        }
                    ]
                }
            ]
        }
        search_criterion = {self.db_pg.names.GC_PARCEL_T_PARCEL_NUMBER_F: '253940000000000230099335131315'}
        features = self.ladm_data.get_parcel_data_to_compare_changes_supplies(self.db_pg, search_criterion=search_criterion)
        normalize_responce(features)
        self.assertEqual(features, features_test)

        features_test = {
            '253940000000000230241000000000': [
                {
                    'departamento': '25',
                    'matricula_inmobiliaria': '760ab38',
                    'numero_predial': '253940000000000230241000000000',
                    'condicion_predio': 'NPH',
                    'nombre': NULL,
                    't_id': 971,
                    'area_terreno': 5375.26,
                    'GEOMETRY_PLOT': "MultiPolygon (((963319.42000000004190952 1077382.33199999993667006, 963343.66099999996367842 1077330.41599999996833503, 963424.84900000004563481 1077377.26900000008754432, 963424.43500000005587935 1077378.12199999997392297, 963393.06000000005587935 1077424.39999999990686774, 963388.79500000004190952 1077427.97399999992921948, 963325.14500000001862645 1077388.14400000008754432, 963319.42000000004190952 1077382.33199999993667006)))",
                    'Interesados': [
                        {'tipo_documento': 'Cédula de ciudadanía',
                         'documento_identidad': '1',
                         'nombre': '1primer nombre 1segundo nombre 1primero apellido 1segundo apellido',
                         'derecho': NULL
                         }
                    ]
                }
            ]
        }
        search_criterion = {self.db_pg.names.GC_PARCEL_T_FMI_F: '760ab38'}
        features = self.ladm_data.get_parcel_data_to_compare_changes_supplies(self.db_pg, search_criterion=search_criterion)
        normalize_responce(features)
        self.assertEqual(features, features_test)

    @classmethod
    def tearDownClass(cls):
        print("INFO: Closing open connections to databases")
        cls.db_pg.conn.close()


if __name__ == '__main__':
    nose2.main()
