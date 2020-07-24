import nose2

from qgis.core import NULL
from qgis.testing import (start_app,
                          unittest)

from asistente_ladm_col.app_interface import AppInterface

start_app()  # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData
from asistente_ladm_col.tests.utils import (get_pg_conn,
                                            normalize_response,
                                            restore_schema,
                                            import_qgis_model_baker,
                                            unload_qgis_model_baker)


class TestChangeDetectionsCollected(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("INFO: Restoring databases to be used")
        import_qgis_model_baker()
        restore_schema('test_ladm_col_queries')
        cls.db_pg = get_pg_conn('test_ladm_col_queries')
        res, code, msg = cls.db_pg.test_connection()
        cls.assertTrue(res, msg)

        cls.app = AppInterface()
        cls.ladm_data = LADMData()
        cls.names = cls.db_pg.names

    def test_get_plots_related_to_parcels(self):
        print("\nINFO: Validating get plots related to parcels (Case: t_id)...")

        parcel_ids_tests = [list(), [959], [977, 959, 965]]
        plot_ids_tests = [list(), [1451], [1444, 1451, 1459]]

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
            plot_custom_field_ids = self.ladm_data.get_plots_related_to_parcels(self.db_pg, parcel_ids_test, self.names.LC_PLOT_T_PLOT_AREA_F)
            self.assertCountEqual(plot_custom_field_ids, plot_custom_field_ids_tests[count], "Failure with data set {}".format(count + 1))
            count += 1

        print("\nINFO: Validating get plots related to parcels (Case: t_id) with preloaded tables...")

        layers = {
            self.names.LC_PLOT_T: None,
            self.names.COL_UE_BAUNIT_T: None
        }
        self.app.core.get_layers(self.db_pg, layers, load=True)
        self.assertIsNotNone(layers, 'An error occurred while trying to get the layers of interest')

        count = 0
        for parcel_ids_test in parcel_ids_tests:
            plot_ids = self.ladm_data.get_plots_related_to_parcels(self.db_pg,
                                                                   parcel_ids_test,
                                                                   self.names.T_ID_F,
                                                                   plot_layer=layers[self.names.LC_PLOT_T],
                                                                   uebaunit_table=layers[self.names.COL_UE_BAUNIT_T])
            self.assertCountEqual(plot_ids, plot_ids_tests[count], "Failure with data set {}".format(count + 1))
            count += 1

    def test_get_parcels_related_to_plots(self):
        print("\nINFO: Validating get parcels related to plots (Case: t_id)...")

        plot_ids_tests = [list(), [1451], [1444, 1451, 1459]]
        parcel_ids_tests = [list(), [959], [977, 959, 965]]

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
                                                                                  self.names.LC_PARCEL_T_PARCEL_NUMBER_F)
            self.assertCountEqual(parcel_custom_field_ids, parcel_custom_field_ids_tests[count],
                                  "Failure with data set {}".format(count + 1))
            count += 1

        print("\nINFO: Validating get parcels related to plots (Case: t_id) with preloaded tables...")

        layers = {
            self.names.LC_PARCEL_T: None,
            self.names.COL_UE_BAUNIT_T: None
        }
        self.app.core.get_layers(self.db_pg, layers, load=True)
        self.assertIsNotNone(layers, 'An error occurred while trying to get the layers of interest')

        count = 0
        for plot_ids_test in plot_ids_tests:
            parcel_ids = self.ladm_data.get_parcels_related_to_plots(self.db_pg,
                                                                     plot_ids_test,
                                                                     self.names.T_ID_F,
                                                                     parcel_table=layers[self.names.LC_PARCEL_T],
                                                                     uebaunit_table=layers[self.names.COL_UE_BAUNIT_T])
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
                    't_id': 909,
                    'area_terreno': 7307.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844186.5580000001937151 2143347.0090000000782311 0, 4844176.49199999962002039 2143349.59100000001490116 0, 4844156.33200000040233135 2143371.39099999982863665 0, 4844170.94099999964237213 2143390.58699999982491136 0, 4844198.0400000000372529 2143411.57500000018626451 0, 4844236.10300000011920929 2143449.92599999997764826 0, 4844254.71700000017881393 2143431.93500000005587935 0, 4844291.92200000025331974 2143406.40799999982118607 0, 4844224.39800000004470348 2143346.85699999984353781 0, 4844186.5580000001937151 2143347.0090000000782311 0)))',
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
                    't_id': 915,
                    'area_terreno': 4283.7,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844216.73300000000745058 2143283.65299999993294477 0, 4844284.49399999994784594 2143293.94100000010803342 0, 4844301.3169999998062849 2143231.64699999988079071 0, 4844269.78899999987334013 2143204.60600000014528632 0, 4844239.02300000004470348 2143245.96100000012665987 0, 4844216.73300000000745058 2143283.65299999993294477 0)))',
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
                    't_id': 917,
                    'area_terreno': 30777.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844284.14400000032037497 2143108.43800000008195639 0, 4844291.65099999960511923 2143102.99800000013783574 0, 4844306.1650000000372529 2143072.30200000014156103 0, 4844315.90099999960511923 2143054.68600000021979213 0, 4844392.21300000045448542 2143089.67900000000372529 0, 4844416.24100000038743019 2143100.69799999985843897 0, 4844448.90099999960511923 2143130.46900000004097819 0, 4844446.04100000020116568 2143226.05299999983981252 0, 4844398.42599999997764826 2143250.11500000022351742 0, 4844383.73000000044703484 2143272.79999999981373549 0, 4844350.60099999979138374 2143300.97800000011920929 0, 4844345.65500000026077032 2143311.24899999983608723 0, 4844284.49399999994784594 2143293.94100000010803342 0, 4844301.3169999998062849 2143231.64699999988079071 0, 4844269.78899999987334013 2143204.60600000014528632 0, 4844213.29899999964982271 2143180.40599999995902181 0, 4844229.71700000017881393 2143151.82400000002235174 0, 4844245.67300000041723251 2143133.63200000021606684 0, 4844250.78299999982118607 2143128.11500000022351742 0, 4844294.71200000029057264 2143186.2409999999217689 0, 4844325.30700000002980232 2143167.71199999982491136 0, 4844341.13999999966472387 2143144.05700000002980232 0, 4844329.28399999998509884 2143126.86899999994784594 0, 4844284.14400000032037497 2143108.43800000008195639 0)))',
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
                    't_id': 943,
                    'area_terreno': 877.9,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844042.68800000008195639 2143467.91800000006332994 0, 4844078.84900000039488077 2143505.82299999985843897 0, 4844068.71399999968707561 2143518.98199999984353781 0, 4844032.42399999964982271 2143480.375 0, 4844036.30999999959021807 2143471.20300000021234155 0, 4844042.68800000008195639 2143467.91800000006332994 0)))',
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
                    't_id': 969,
                    'area_terreno': 818.8,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844032.42399999964982271 2143480.375 0, 4844068.71399999968707561 2143518.98199999984353781 0, 4844058.38999999966472387 2143529.89600000018253922 0, 4844047.20600000023841858 2143517.88499999977648258 0, 4844021.35099999979138374 2143491.13799999980255961 0, 4844028.46200000029057264 2143481.973000000230968 0, 4844032.42399999964982271 2143480.375 0)))',
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
                    't_id': 971,
                    'area_terreno': 967.1,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844021.35099999979138374 2143491.13799999980255961 0, 4844047.20600000023841858 2143517.88499999977648258 0, 4844036.97499999962747097 2143532.10000000009313226 0, 4843996.82500000018626451 2143509.47099999990314245 0, 4844021.35099999979138374 2143491.13799999980255961 0)))',
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
                    't_id': 977,
                    'area_terreno': 2614.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844170.94099999964237213 2143390.58699999982491136 0, 4844198.0400000000372529 2143411.57500000018626451 0, 4844236.10300000011920929 2143449.92599999997764826 0, 4844218.57000000029802322 2143459.45200000004842877 0, 4844174.01400000043213367 2143434.21799999987706542 0, 4844139.30900000035762787 2143415.08000000007450581 0, 4844170.94099999964237213 2143390.58699999982491136 0)))',
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
                    't_id': 979,
                    'area_terreno': 11087.8,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844047.20600000023841858 2143517.88499999977648258 0, 4844058.38999999966472387 2143529.89600000018253922 0, 4844052.38499999977648258 2143547.83999999985098839 0, 4844100.49600000027567148 2143577.78299999982118607 0, 4844022.85099999979138374 2143654.56499999994412065 0, 4843990.80099999997764826 2143614.41900000022724271 0, 4843972.88599999994039536 2143587.22399999992921948 0, 4843950.66799999959766865 2143559.20899999979883432 0, 4843961.11799999978393316 2143546.1159999999217689 0, 4843976.25299999956041574 2143534.28299999982118607 0, 4843979.08999999985098839 2143530.10800000000745058 0, 4843981.23300000000745058 2143523.24800000013783574 0, 4843990.4869999997317791 2143512.3390000001527369 0, 4843996.82500000018626451 2143509.47099999990314245 0, 4844036.97499999962747097 2143532.10000000009313226 0, 4844047.20600000023841858 2143517.88499999977648258 0)))',
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
                    't_id': 981,
                    'area_terreno': 15073.7,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844392.21300000045448542 2143089.67900000000372529 0, 4844410.20199999958276749 2143079.62999999988824129 0, 4844436.66299999970942736 2143070.32899999991059303 0, 4844446.17999999970197678 2143068.19599999999627471 0, 4844461.78399999998509884 2143069.35999999986961484 0, 4844475.14699999988079071 2143074.09700000006705523 0, 4844485.33700000029057264 2143079.5 0, 4844510.49500000011175871 2143099.68699999991804361 0, 4844524.12799999956041574 2143107.86100000003352761 0, 4844541.38700000010430813 2143110.31100000021979213 0, 4844570.90400000009685755 2143186.54499999992549419 0, 4844528.18599999975413084 2143210.63700000010430813 0, 4844446.04100000020116568 2143226.05299999983981252 0, 4844448.90099999960511923 2143130.46900000004097819 0, 4844416.24100000038743019 2143100.69799999985843897 0, 4844392.21300000045448542 2143089.67900000000372529 0)))',
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
                    't_id': 983,
                    'area_terreno': 2234.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4843950.66799999959766865 2143559.20899999979883432 0, 4843972.88599999994039536 2143587.22399999992921948 0, 4843956.58999999985098839 2143601.91699999989941716 0, 4843935.15699999965727329 2143630.32400000002235174 0, 4843906.50899999961256981 2143602.6830000001937151 0, 4843912.96800000034272671 2143591.52000000001862645 0, 4843935.15799999982118607 2143574.64099999982863665 0, 4843950.66799999959766865 2143559.20899999979883432 0)))',
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
                    't_id': 985,
                    'area_terreno': 4200.0,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844149.54999999981373549 2143331.77900000009685755 0, 4844176.49199999962002039 2143349.59100000001490116 0, 4844156.33200000040233135 2143371.39099999982863665 0, 4844170.94099999964237213 2143390.58699999982491136 0, 4844139.30900000035762787 2143415.08000000007450581 0, 4844089.43599999975413084 2143400.00499999988824129 0, 4844099.38399999961256981 2143379.22500000009313226 0, 4844109.19400000013411045 2143363.35699999984353781 0, 4844128.41999999992549419 2143340.89000000013038516 0, 4844149.54999999981373549 2143331.77900000009685755 0)))',
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
                    't_id': 993,
                    'area_terreno': 4814.4,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844149.54999999981373549 2143331.77900000009685755 0, 4844163.05999999959021807 2143299.45000000018626451 0, 4844168.31099999975413084 2143290.31100000021979213 0, 4844173.26900000032037497 2143278.36400000005960464 0, 4844179.0530000003054738 2143255.36299999989569187 0, 4844189.30900000035762787 2143236.91200000001117587 0, 4844239.02300000004470348 2143245.96100000012665987 0, 4844216.73300000000745058 2143283.65299999993294477 0, 4844186.5580000001937151 2143347.0090000000782311 0, 4844176.49199999962002039 2143349.59100000001490116 0, 4844149.54999999981373549 2143331.77900000009685755 0)))',
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
                    't_id': 995,
                    'area_terreno': 10495.1,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844089.43599999975413084 2143400.00499999988824129 0, 4844139.30900000035762787 2143415.08000000007450581 0, 4844174.01400000043213367 2143434.21799999987706542 0, 4844218.57000000029802322 2143459.45200000004842877 0, 4844194.39400000032037497 2143484.89900000020861626 0, 4844165.03699999954551458 2143499.39600000018253922 0, 4844099.30700000002980232 2143469.70200000004842877 0, 4844078.84900000039488077 2143505.82299999985843897 0, 4844042.68800000008195639 2143467.91800000006332994 0, 4844056.72099999990314245 2143429.36200000019744039 0, 4844084.80999999959021807 2143402.83300000010058284 0, 4844089.43599999975413084 2143400.00499999988824129 0)))',
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
                    't_id': 911,
                    'area_terreno': 21907.6,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844095.31199999991804361 2143357.83399999979883432 0, 4844120.026999999769032 2143332.59500000020489097 0, 4844070.42200000025331974 2143291.54499999992549419 0, 4844104.27599999960511923 2143235.38100000005215406 0, 4844165.90600000042468309 2143254.95399999991059303 0, 4844166.53100000042468309 2143232.87699999986216426 0, 4844167.18800000008195639 2143220.48499999986961484 0, 4844174.16199999954551458 2143202.23600000003352761 0, 4844090.26699999999254942 2143167.82700000004842877 0, 4844070.71600000001490116 2143196.11799999978393316 0, 4844048.90099999960511923 2143262.38899999996647239 0, 4844014.0849999999627471 2143311.14600000018253922 0, 4844095.31199999991804361 2143357.83399999979883432 0)),((4844046.348000000230968 2143260.325999999884516 0, 4844066.94099999964237213 2143193.7140000001527369 0, 4844086.10099999979138374 2143165.15700000012293458 0, 4844038.42599999997764826 2143136.06300000008195639 0, 4844025.37000000011175871 2143149.60399999981746078 0, 4843917.10699999984353781 2143075.5359999998472631 0, 4843909.41999999992549419 2143094.22200000006705523 0, 4843927.97599999979138374 2143113.20699999993667006 0, 4843929.20799999963492155 2143114.03399999998509884 0, 4843999.57500000018626451 2143155.98900000005960464 0, 4843974.3030000003054738 2143202.11400000005960464 0, 4844046.348000000230968 2143260.325999999884516 0)))',
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
                    't_id': 913,
                    'area_terreno': 3902.1,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844284.14400000032037497 2143108.43800000008195639 0, 4844329.28399999998509884 2143126.86899999994784594 0, 4844341.13999999966472387 2143144.05700000002980232 0, 4844325.30700000002980232 2143167.71199999982491136 0, 4844294.71200000029057264 2143186.2409999999217689 0, 4844250.78299999982118607 2143128.11500000022351742 0, 4844256.1780000003054738 2143126.51399999996647239 0, 4844284.14400000032037497 2143108.43800000008195639 0)))',
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
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844213.29899999964982271 2143180.40599999995902181 0, 4844189.30900000035762787 2143236.91200000001117587 0, 4844239.02300000004470348 2143245.96100000012665987 0, 4844269.78899999987334013 2143204.60600000014528632 0, 4844213.29899999964982271 2143180.40599999995902181 0)))',
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
                    't_id': 919,
                    'area_terreno': 2301.5,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4843837.03100000042468309 2143230.88100000005215406 0, 4843840.62200000043958426 2143231.43500000005587935 0, 4843868.7099999999627471 2143239.90299999993294477 0, 4843874.14199999999254942 2143243.18000000016763806 0, 4843898.43499999959021807 2143259.54400000022724271 0, 4843917.97699999995529652 2143275.24399999994784594 0, 4843907.33000000007450581 2143295.71700000017881393 0, 4843833.91299999970942736 2143252 0, 4843837.03100000042468309 2143230.88100000005215406 0)))',
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
                    't_id': 921,
                    'area_terreno': 1210.6,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4843833.91299999970942736 2143252 0, 4843907.33000000007450581 2143295.71700000017881393 0, 4843900.97900000028312206 2143305.48199999984353781 0, 4843834.44299999997019768 2143273.65799999982118607 0, 4843833.91299999970942736 2143252 0)))',
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
                    't_id': 923,
                    'area_terreno': 749.7,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4843834.44299999997019768 2143273.65799999982118607 0, 4843900.97900000028312206 2143305.48199999984353781 0, 4843894.34599999990314245 2143312.53700000001117587 0, 4843837.61899999994784594 2143289.3659999999217689 0, 4843834.44299999997019768 2143273.65799999982118607 0)))',
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
                    't_id': 925,
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
                    't_id': 927,
                    'area_terreno': 2267.4,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844108.2630000002682209 2143141.76500000013038516 0, 4844131.75299999956041574 2143125.17199999978765845 0, 4844198.22800000011920929 2143157.53299999982118607 0, 4844200.05700000002980232 2143175.61899999994784594 0, 4844187.54200000036507845 2143182.64900000020861626 0, 4844108.2630000002682209 2143141.76500000013038516 0)))',
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
                    't_id': 929,
                    'area_terreno': 2455.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844108.2630000002682209 2143141.76500000013038516 0, 4844187.54200000036507845 2143182.64900000020861626 0, 4844174.16199999954551458 2143202.23600000003352761 0, 4844090.26699999999254942 2143167.82700000004842877 0, 4844108.2630000002682209 2143141.76500000013038516 0)))',
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
                    't_id': 931,
                    'area_terreno': 5375.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4843989.946000000461936 2143363.07700000004842877 0, 4844014.0849999999627471 2143311.14600000018253922 0, 4844095.31199999991804361 2143357.83399999979883432 0, 4844094.90000000037252903 2143358.68699999991804361 0, 4844063.62100000027567148 2143404.99500000011175871 0, 4844059.36500000022351742 2143408.57500000018626451 0, 4843995.678999999538064 2143368.87600000016391277 0, 4843989.946000000461936 2143363.07700000004842877 0)))',
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
                    't_id': 933,
                    'area_terreno': 1808.1,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4843984.71100000012665987 2143385.63200000021606684 0, 4843989.946000000461936 2143363.07700000004842877 0, 4843995.678999999538064 2143368.87600000016391277 0, 4844059.36500000022351742 2143408.57500000018626451 0, 4844038.8030000003054738 2143428.38200000021606684 0, 4843984.71100000012665987 2143385.63200000021606684 0)))',
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
                    't_id': 935,
                    'area_terreno': 6068.6,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844204.80499999970197678 2143077.12900000018998981 0, 4844204.01800000015646219 2143031.58799999998882413 0, 4844285.36799999978393316 2143021.63799999980255961 0, 4844287.75100000016391277 2143025.51699999999254942 0, 4844300.3080000001937151 2143075.25600000005215406 0, 4844278.03799999970942736 2143109.13499999977648258 0, 4844204.80499999970197678 2143077.12900000018998981 0)))',
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
                    't_id': 937,
                    'area_terreno': 1974.4,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844182.09100000001490116 2143098.55200000014156103 0, 4844204.80499999970197678 2143077.12900000018998981 0, 4844278.03799999970942736 2143109.13499999977648258 0, 4844255.69900000002235174 2143122.56199999991804361 0, 4844251.08999999985098839 2143122.74699999997392297 0, 4844182.09100000001490116 2143098.55200000014156103 0)))',
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
                    't_id': 939,
                    'area_terreno': 1453.9,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844182.09100000001490116 2143098.55200000014156103 0, 4844251.08999999985098839 2143122.74699999997392297 0, 4844241.88900000043213367 2143132.00199999986216426 0, 4844226.68900000024586916 2143139.1919999998062849 0, 4844163.62100000027567148 2143106.50799999991431832 0, 4844182.09100000001490116 2143098.55200000014156103 0)))',
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
                    't_id': 941,
                    'area_terreno': 2330.8,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844198.22800000011920929 2143157.53299999982118607 0, 4844224.8030000003054738 2143146.22899999981746078 0, 4844226.68900000024586916 2143139.1919999998062849 0, 4844163.62100000027567148 2143106.50799999991431832 0, 4844144.53000000026077032 2143113.98600000003352761 0, 4844140.31099999975413084 2143116.549000000115484 0, 4844131.75299999956041574 2143125.17199999978765845 0, 4844198.22800000011920929 2143157.53299999982118607 0)))',
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
                    't_id': 945,
                    'area_terreno': 7691.6,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844541.38700000010430813 2143110.31100000021979213 0, 4844570.90400000009685755 2143186.54499999992549419 0, 4844584.45500000007450581 2143188.88200000021606684 0, 4844667.52599999960511923 2143208.60300000011920929 0, 4844668.81900000013411045 2143140.4330000001937151 0, 4844541.38700000010430813 2143110.31100000021979213 0)))',
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
                    't_id': 947,
                    'area_terreno': 7983.2,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844668.81900000013411045 2143140.4330000001937151 0, 4844688.303999999538064 2143117.61899999994784594 0, 4844725.82400000002235174 2143083.43899999978020787 0, 4844762.3080000001937151 2143128.82099999999627471 0, 4844763.40299999993294477 2143131.0669999998062849 0, 4844765.571000000461936 2143152.40499999979510903 0, 4844768.10199999995529652 2143175.87399999983608723 0, 4844727.36899999994784594 2143184.62800000002607703 0, 4844693.64499999955296516 2143202.00199999986216426 0, 4844667.52599999960511923 2143208.60300000011920929 0, 4844668.81900000013411045 2143140.4330000001937151 0)))',
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
                    't_id': 949,
                    'area_terreno': 8103.5,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844730.19799999985843897 2143189.02199999988079071 0, 4844732.87000000011175871 2143193.33399999979883432 0, 4844719.33899999968707561 2143213.10600000014528632 0, 4844711.25600000005215406 2143218.52000000001862645 0, 4844676.28600000031292439 2143251.73900000005960464 0, 4844659.03199999965727329 2143255.75799999991431832 0, 4844651.24700000043958426 2143266.32700000004842877 0, 4844635.0530000003054738 2143262.88100000005215406 0, 4844622.34900000039488077 2143283.549000000115484 0, 4844606.25700000021606684 2143278.78899999987334013 0, 4844600.46200000029057264 2143293.48300000000745058 0, 4844594.0719999996945262 2143295.42199999978765845 0, 4844581.51800000015646219 2143292.57800000021234155 0, 4844586.80900000035762787 2143268.3840000000782311 0, 4844566.28199999965727329 2143203.94100000010803342 0, 4844583.09499999973922968 2143197.12699999986216426 0, 4844623.27599999960511923 2143205.44900000002235174 0, 4844667.75499999988824129 2143212.44499999983236194 0, 4844694.21200000029057264 2143205.97699999995529652 0, 4844730.19799999985843897 2143189.02199999988079071 0)))',
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
                    't_id': 951,
                    'area_terreno': 11157.6,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844186.5580000001937151 2143347.0090000000782311 0, 4844216.73300000000745058 2143283.65299999993294477 0, 4844284.49399999994784594 2143293.94100000010803342 0, 4844345.65500000026077032 2143311.24899999983608723 0, 4844335.95100000035017729 2143361.82800000021234155 0, 4844291.92200000025331974 2143406.40799999982118607 0, 4844224.39800000004470348 2143346.85699999984353781 0, 4844186.5580000001937151 2143347.0090000000782311 0)))',
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
                    't_id': 953,
                    'area_terreno': 1320.4,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4843917.97699999995529652 2143275.24399999994784594 0, 4843925.29100000020116568 2143266.60699999984353781 0, 4843873.50399999972432852 2143229.27900000009685755 0, 4843855.10099999979138374 2143210.61200000019744039 0, 4843845.04499999992549419 2143208.50999999977648258 0, 4843837.03100000042468309 2143230.88100000005215406 0, 4843840.62200000043958426 2143231.43500000005587935 0, 4843868.7099999999627471 2143239.90299999993294477 0, 4843874.14199999999254942 2143243.18000000016763806 0, 4843898.43499999959021807 2143259.54400000022724271 0, 4843917.97699999995529652 2143275.24399999994784594 0)))',
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
                    't_id': 955,
                    'area_terreno': 25178.2,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4843925.29100000020116568 2143266.60699999984353781 0, 4843935.66100000031292439 2143274.50700000021606684 0, 4843974.3030000003054738 2143202.11400000005960464 0, 4843999.57500000018626451 2143155.98900000005960464 0, 4843929.20799999963492155 2143114.03399999998509884 0, 4843927.97599999979138374 2143113.20699999993667006 0, 4843909.41999999992549419 2143094.22200000006705523 0, 4843781.9419999998062849 2143073.59899999992921948 0, 4843772.26599999982863665 2143107.5400000000372529 0, 4843775.803999999538064 2143155.91800000006332994 0, 4843826.15500000026077032 2143171.54600000008940697 0, 4843815.87600000016391277 2143199.776999999769032 0, 4843845.04499999992549419 2143208.50999999977648258 0, 4843855.10099999979138374 2143210.61200000019744039 0, 4843873.50399999972432852 2143229.27900000009685755 0, 4843925.29100000020116568 2143266.60699999984353781 0)))',
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
                    't_id': 961,
                    'area_terreno': 904.8,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4843907.06199999991804361 2143217.03899999987334013 0, 4843941.68900000024586916 2143240.08699999982491136 0, 4843949.99000000022351742 2143231.02799999993294477 0, 4843922.73300000000745058 2143191.79600000008940697 0, 4843907.06199999991804361 2143217.03899999987334013 0)))',
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
                    't_id': 957,
                    'area_terreno': 10986.0,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4843896.27599999960511923 2143770.63100000005215406 0, 4843910.03500000014901161 2143780.54100000020116568 0, 4843965.24000000022351742 2143703.89699999988079071 0, 4843896.27599999960511923 2143770.63100000005215406 0)),((4843906.50899999961256981 2143602.6830000001937151 0, 4843885.89400000032037497 2143631.1650000000372529 0, 4843871.28699999954551458 2143660.15700000012293458 0, 4843851.42300000041723251 2143686.04300000006332994 0, 4843834.70000000018626451 2143710.60300000011920929 0, 4843889.25800000037997961 2143765.575999999884516 0, 4843959.67599999997764826 2143696.49800000013783574 0, 4843931.52500000037252903 2143666.76899999985471368 0, 4843939.46499999985098839 2143652.05599999986588955 0, 4843935.473000000230968 2143640.34299999987706542 0, 4843939.20299999974668026 2143633.13200000021606684 0, 4843935.15699999965727329 2143630.32400000002235174 0, 4843906.50899999961256981 2143602.6830000001937151 0)))',
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
                    't_id': 959,
                    'area_terreno': 49379.0,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4843993.2630000002682209 2143687.28299999982118607 0, 4843965.24000000022351742 2143703.89699999988079071 0, 4843910.03500000014901161 2143780.54100000020116568 0, 4843903.16399999987334013 2143795.48199999984353781 0, 4843898.71200000029057264 2143815.49500000011175871 0, 4843844.74199999962002039 2143875.52499999990686774 0, 4844012.31799999997019768 2144004.89600000018253922 0, 4844053.41899999976158142 2143935.20599999977275729 0, 4844074.36699999962002039 2143914.82400000002235174 0, 4844092.2099999999627471 2143889.723000000230968 0, 4844109.81799999997019768 2143863.76099999994039536 0, 4844132.74000000022351742 2143856.03500000014901161 0, 4844163.10400000028312206 2143835.32700000004842877 0, 4843993.2630000002682209 2143687.28299999982118607 0)))',
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
                    't_id': 963,
                    'area_terreno': 10006.6,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4843987.21999999973922968 2143361.60699999984353781 0, 4844011.33000000007450581 2143309.73300000000745058 0, 4844046.348000000230968 2143260.325999999884516 0, 4843974.3030000003054738 2143202.11400000005960464 0, 4843925.29100000020116568 2143266.60699999984353781 0, 4843917.97699999995529652 2143275.24399999994784594 0, 4843987.21999999973922968 2143361.60699999984353781 0)))',
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
                    't_id': 965,
                    'area_terreno': 59108.5,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844022.85099999979138374 2143654.56499999994412065 0, 4844035.44900000002235174 2143646.15599999995902181 0, 4844045.92999999970197678 2143636.06199999991804361 0, 4844050.49500000011175871 2143631.66600000020116568 0, 4844055.74899999983608723 2143626.79100000020116568 0, 4844074.56599999964237213 2143608.60399999981746078 0, 4844074.81900000013411045 2143608.35900000017136335 0, 4844077.553999999538064 2143605.71499999985098839 0, 4844092.24899999983608723 2143595.03800000017508864 0, 4844107.29700000025331974 2143583.71900000004097819 0, 4844109.75 2143581.87300000013783574 0, 4844118.22200000006705523 2143575.37900000018998981 0, 4844119.25700000021606684 2143574.5849999999627471 0, 4844128.10599999967962503 2143568.09100000001490116 0, 4844133.64699999988079071 2143561.60099999979138374 0, 4844134.973000000230968 2143559.68999999994412065 0, 4844143.01200000010430813 2143548.098000000230968 0, 4844147.56599999964237213 2143543.79300000006332994 0, 4844152.12100000027567148 2143539.48799999989569187 0, 4844158.71999999973922968 2143532.20399999991059303 0, 4844167.96100000012665987 2143524.12300000013783574 0, 4844180.85500000044703484 2143514.97500000009313226 0, 4844185.52500000037252903 2143511.66300000017508864 0, 4844192.78500000014901161 2143504.64300000015646219 0, 4844193.60400000028312206 2143504.10999999986961484 0, 4844199.74299999978393316 2143500.11100000003352761 0, 4844194.39400000032037497 2143484.89900000020861626 0, 4844165.03699999954551458 2143499.39600000018253922 0, 4844129.74700000043958426 2143539.54699999978765845 0, 4844100.49600000027567148 2143577.78299999982118607 0, 4844022.85099999979138374 2143654.56499999994412065 0)),((4844203.45199999958276749 2143503.2859999998472631 0, 4844193.84100000001490116 2143513.11899999994784594 0, 4844182.64400000032037497 2143522.02300000004470348 0, 4844181.44900000002235174 2143523.04600000008940697 0, 4844175.46200000029057264 2143528.17100000008940697 0, 4844164.15699999965727329 2143537.47000000020489097 0, 4844162.57500000018626451 2143538.77199999988079071 0, 4844160.54899999964982271 2143540.848000000230968 0, 4844152.86000000033527613 2143548.73100000014528632 0, 4844143.5669999998062849 2143557.63299999991431832 0, 4844135.75999999977648258 2143569.28299999982118607 0, 4844126.88599999994039536 2143575.85600000014528632 0, 4844115.89400000032037497 2143583.25100000016391277 0, 4844110.7369999997317791 2143586.72000000020489097 0, 4844080.98099999967962503 2143608.74800000013783574 0, 4844072.17499999981373549 2143618.02199999988079071 0, 4844045.95700000040233135 2143645.63799999980255961 0, 4844039.28600000031292439 2143650.96299999998882413 0, 4844038.51800000015646219 2143651.575999999884516 0, 4844032.625 2143656.28099999995902181 0, 4844027.12299999967217445 2143660.67299999995157123 0, 4843993.2630000002682209 2143687.28299999982118607 0, 4844163.10400000028312206 2143835.32700000004842877 0, 4844187.86500000022351742 2143806.15799999982118607 0, 4844228.96300000045448542 2143737.95800000010058284 0, 4844325.18400000035762787 2143662.69400000013411045 0, 4844354.34700000006705523 2143632.40400000009685755 0, 4844203.45199999958276749 2143503.2859999998472631 0)))',
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
                    't_id': 967,
                    'area_terreno': 5473.0,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4843972.88599999994039536 2143587.22399999992921948 0, 4843956.58999999985098839 2143601.91699999989941716 0, 4843935.15699999965727329 2143630.32400000002235174 0, 4843939.20299999974668026 2143633.13200000021606684 0, 4843935.473000000230968 2143640.34299999987706542 0, 4843939.46499999985098839 2143652.05599999986588955 0, 4843931.52500000037252903 2143666.76899999985471368 0, 4843959.67599999997764826 2143696.49800000013783574 0, 4843982.42100000008940697 2143683.64699999988079071 0, 4844022.85099999979138374 2143654.56499999994412065 0, 4843990.80099999997764826 2143614.41900000022724271 0, 4843972.88599999994039536 2143587.22399999992921948 0)))',
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
                    't_id': 973,
                    'area_terreno': 70502.4,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844194.39400000032037497 2143484.89900000020861626 0, 4844199.74299999978393316 2143500.11100000003352761 0, 4844208.87899999972432852 2143496.00799999991431832 0, 4844214.2630000002682209 2143489.97000000020489097 0, 4844225.02799999993294477 2143476.14600000018253922 0, 4844235.8030000003054738 2143467.87699999986216426 0, 4844245.14699999988079071 2143457.54799999995157123 0, 4844261.94099999964237213 2143443.55599999986588955 0, 4844263.49100000038743019 2143442.23199999984353781 0, 4844265.80900000035762787 2143440.25400000018998981 0, 4844272.55599999986588955 2143434.49299999978393316 0, 4844284.9150000000372529 2143424.47500000009313226 0, 4844295.05700000002980232 2143417.15899999998509884 0, 4844305.36400000005960464 2143413.33300000010058284 0, 4844311.70299999974668026 2143408.56199999991804361 0, 4844318.03500000014901161 2143400.14199999999254942 0, 4844320.71600000001490116 2143391.25199999986216426 0, 4844321.16000000014901161 2143390.4419999998062849 0, 4844327.83399999979883432 2143378.22800000011920929 0, 4844335.95100000035017729 2143361.82800000021234155 0, 4844291.92200000025331974 2143406.40799999982118607 0, 4844254.71700000017881393 2143431.93500000005587935 0, 4844236.10300000011920929 2143449.92599999997764826 0, 4844218.57000000029802322 2143459.45200000004842877 0, 4844194.39400000032037497 2143484.89900000020861626 0)),((4844586.80900000035762787 2143268.3840000000782311 0, 4844566.28199999965727329 2143203.94100000010803342 0, 4844530.60400000028312206 2143219.58300000010058284 0, 4844445.41600000020116568 2143233.25499999988824129 0, 4844404.13300000037997961 2143252.89600000018253922 0, 4844388.50899999961256981 2143276.43600000021979213 0, 4844354.76200000010430813 2143304.06399999978020787 0, 4844340.19500000029802322 2143364.76200000010430813 0, 4844340.19400000013411045 2143364.76200000010430813 0, 4844338.38599999994039536 2143368.41300000017508864 0, 4844338.27799999993294477 2143368.63299999991431832 0, 4844332.07600000035017729 2143381.16399999987334013 0, 4844327.30099999997764826 2143389.89999999990686774 0, 4844324.95799999963492155 2143394.18699999991804361 0, 4844324.78199999965727329 2143394.77000000001862645 0, 4844322.276999999769032 2143403.07700000004842877 0, 4844315.94500000029802322 2143411.49800000013783574 0, 4844309.60500000044703484 2143416.26899999985471368 0, 4844302.33200000040233135 2143418.96900000004097819 0, 4844299.29899999964982271 2143420.09500000020489097 0, 4844298.54399999976158142 2143420.64000000013038516 0, 4844289.54100000020116568 2143427.13499999977648258 0, 4844289.15699999965727329 2143427.4109999998472631 0, 4844276.79800000041723251 2143437.42799999983981252 0, 4844271.49100000038743019 2143441.9599999999627471 0, 4844266.1830000001937151 2143446.4909999999217689 0, 4844249.3880000002682209 2143460.48300000000745058 0, 4844247.04999999981373549 2143463.06900000013411045 0, 4844242.28399999998509884 2143468.33799999998882413 0, 4844240.04499999992549419 2143470.81300000008195639 0, 4844231.49299999978393316 2143477.37699999986216426 0, 4844229.26999999955296516 2143479.08300000010058284 0, 4844226.25800000037997961 2143482.94900000002235174 0, 4844218.50399999972432852 2143492.90499999979510903 0, 4844213.12100000027567148 2143498.94400000013411045 0, 4844208.5530000003054738 2143500.99500000011175871 0, 4844203.45199999958276749 2143503.2859999998472631 0, 4844354.34700000006705523 2143632.40400000009685755 0, 4844417.14800000004470348 2143543.424000000115484 0, 4844454.06799999997019768 2143477.70000000018626451 0, 4844496.21899999957531691 2143372.90700000012293458 0, 4844514.41399999987334013 2143341.73600000003352761 0, 4844536.19400000013411045 2143335.4599999999627471 0, 4844549.11899999994784594 2143328.53399999998509884 0, 4844581.51800000015646219 2143292.57800000021234155 0, 4844586.80900000035762787 2143268.3840000000782311 0)))',
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
                    't_id': 975,
                    'area_terreno': 6085.7,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844099.30700000002980232 2143469.70200000004842877 0, 4844078.84900000039488077 2143505.82299999985843897 0, 4844068.71399999968707561 2143518.98199999984353781 0, 4844058.38999999966472387 2143529.89600000018253922 0, 4844052.38499999977648258 2143547.83999999985098839 0, 4844100.49600000027567148 2143577.78299999982118607 0, 4844129.74700000043958426 2143539.54699999978765845 0, 4844165.03699999954551458 2143499.39600000018253922 0, 4844099.30700000002980232 2143469.70200000004842877 0)))',
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
                    't_id': 987,
                    'area_terreno': 1377.2,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844719.33899999968707561 2143213.10600000014528632 0, 4844732.87000000011175871 2143193.33399999979883432 0, 4844730.19799999985843897 2143189.02199999988079071 0, 4844762.12600000016391277 2143187.2409999999217689 0, 4844768.05700000002980232 2143190.68999999994412065 0, 4844770.18800000008195639 2143201.50600000005215406 0, 4844765.01099999994039536 2143224.17299999995157123 0, 4844747.3880000002682209 2143221.60199999995529652 0, 4844721.42100000008940697 2143216.13899999996647239 0, 4844719.33899999968707561 2143213.10600000014528632 0)))',
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
                    't_id': 989,
                    'area_terreno': 12960.6,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4843917.10699999984353781 2143075.5359999998472631 0, 4843995.70700000040233135 2143085.64699999988079071 0, 4844053.31400000024586916 2143074.86400000005960464 0, 4844100.55700000002980232 2143071.49699999997392297 0, 4844136.38700000010430813 2143067.61700000008568168 0, 4844200.20299999974668026 2143076.78500000014901161 0, 4844179.61099999956786633 2143097.1650000000372529 0, 4844143.44299999997019768 2143112.45200000004842877 0, 4844128.86500000022351742 2143120.11500000022351742 0, 4844104.12100000027567148 2143139.32899999991059303 0, 4844086.10099999979138374 2143165.15700000012293458 0, 4844038.42599999997764826 2143136.06300000008195639 0, 4844025.37000000011175871 2143149.60399999981746078 0, 4843917.10699999984353781 2143075.5359999998472631 0)))',
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
                    't_id': 997,
                    'area_terreno': 12095.4,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844300.3080000001937151 2143075.25600000005215406 0, 4844303.1919999998062849 2143073.64199999999254942 0, 4844306.1650000000372529 2143072.30200000014156103 0, 4844291.65099999960511923 2143102.99800000013783574 0, 4844284.14400000032037497 2143108.43800000008195639 0, 4844256.1780000003054738 2143126.51399999996647239 0, 4844250.78299999982118607 2143128.11500000022351742 0, 4844245.67300000041723251 2143133.63200000021606684 0, 4844229.71700000017881393 2143151.82400000002235174 0, 4844213.29899999964982271 2143180.40599999995902181 0, 4844189.30900000035762787 2143236.91200000001117587 0, 4844179.0530000003054738 2143255.36299999989569187 0, 4844173.26900000032037497 2143278.36400000005960464 0, 4844168.31099999975413084 2143290.31100000021979213 0, 4844163.05999999959021807 2143299.45000000018626451 0, 4844149.54999999981373549 2143331.77900000009685755 0, 4844128.41999999992549419 2143340.89000000013038516 0, 4844109.19400000013411045 2143363.35699999984353781 0, 4844099.38399999961256981 2143379.22500000009313226 0, 4844089.43599999975413084 2143400.00499999988824129 0, 4844084.80999999959021807 2143402.83300000010058284 0, 4844056.72099999990314245 2143429.36200000019744039 0, 4844042.68800000008195639 2143467.91800000006332994 0, 4844036.30999999959021807 2143471.20300000021234155 0, 4844032.42399999964982271 2143480.375 0, 4844028.46200000029057264 2143481.973000000230968 0, 4844021.35099999979138374 2143491.13799999980255961 0, 4843996.82500000018626451 2143509.47099999990314245 0, 4843990.4869999997317791 2143512.3390000001527369 0, 4843981.23300000000745058 2143523.24800000013783574 0, 4843979.08999999985098839 2143530.10800000000745058 0, 4843976.25299999956041574 2143534.28299999982118607 0, 4843961.11799999978393316 2143546.1159999999217689 0, 4843950.66799999959766865 2143559.20899999979883432 0, 4843935.15799999982118607 2143574.64099999982863665 0, 4843912.96800000034272671 2143591.52000000001862645 0, 4843906.50899999961256981 2143602.6830000001937151 0, 4843885.89400000032037497 2143631.1650000000372529 0, 4843871.28699999954551458 2143660.15700000012293458 0, 4843851.42300000041723251 2143686.04300000006332994 0, 4843834.70000000018626451 2143710.60300000011920929 0, 4843828.85900000017136335 2143709.99500000011175871 0, 4843896.58299999963492155 2143593.19700000016018748 0, 4843983.09499999973922968 2143494.37199999997392297 0, 4843983.84399999957531691 2143489.71499999985098839 0, 4844031.03799999970942736 2143456.06999999983236194 0, 4844038.8030000003054738 2143428.38200000021606684 0, 4844059.36500000022351742 2143408.57500000018626451 0, 4844063.62100000027567148 2143404.99500000011175871 0, 4844094.90000000037252903 2143358.68699999991804361 0, 4844095.31199999991804361 2143357.83399999979883432 0, 4844120.026999999769032 2143332.59500000020489097 0, 4844165.90600000042468309 2143254.95399999991059303 0, 4844166.53100000042468309 2143232.87699999986216426 0, 4844167.18800000008195639 2143220.48499999986961484 0, 4844174.16199999954551458 2143202.23600000003352761 0, 4844187.54200000036507845 2143182.64900000020861626 0, 4844200.05700000002980232 2143175.61899999994784594 0, 4844198.22800000011920929 2143157.53299999982118607 0, 4844224.8030000003054738 2143146.22899999981746078 0, 4844226.68900000024586916 2143139.1919999998062849 0, 4844241.88900000043213367 2143132.00199999986216426 0, 4844251.08999999985098839 2143122.74699999997392297 0, 4844255.69900000002235174 2143122.56199999991804361 0, 4844278.03799999970942736 2143109.13499999977648258 0, 4844300.3080000001937151 2143075.25600000005215406 0)))',
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
                    't_id': 999,
                    'area_terreno': 7520.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4843889.25800000037997961 2143765.575999999884516 0, 4843959.67599999997764826 2143696.49800000013783574 0, 4843982.42100000008940697 2143683.64699999988079071 0, 4844022.85099999979138374 2143654.56499999994412065 0, 4844035.44900000002235174 2143646.15599999995902181 0, 4844045.92999999970197678 2143636.06199999991804361 0, 4844050.49500000011175871 2143631.66600000020116568 0, 4844055.74899999983608723 2143626.79100000020116568 0, 4844074.56599999964237213 2143608.60399999981746078 0, 4844074.81900000013411045 2143608.35900000017136335 0, 4844077.553999999538064 2143605.71499999985098839 0, 4844092.24899999983608723 2143595.03800000017508864 0, 4844107.29700000025331974 2143583.71900000004097819 0, 4844109.75 2143581.87300000013783574 0, 4844118.22200000006705523 2143575.37900000018998981 0, 4844119.25700000021606684 2143574.5849999999627471 0, 4844128.10599999967962503 2143568.09100000001490116 0, 4844133.64699999988079071 2143561.60099999979138374 0, 4844134.973000000230968 2143559.68999999994412065 0, 4844143.01200000010430813 2143548.098000000230968 0, 4844147.56599999964237213 2143543.79300000006332994 0, 4844152.12100000027567148 2143539.48799999989569187 0, 4844158.71999999973922968 2143532.20399999991059303 0, 4844167.96100000012665987 2143524.12300000013783574 0, 4844180.85500000044703484 2143514.97500000009313226 0, 4844185.52500000037252903 2143511.66300000017508864 0, 4844192.78500000014901161 2143504.64300000015646219 0, 4844193.60400000028312206 2143504.10999999986961484 0, 4844199.74299999978393316 2143500.11100000003352761 0, 4844208.87899999972432852 2143496.00799999991431832 0, 4844214.2630000002682209 2143489.97000000020489097 0, 4844225.02799999993294477 2143476.14600000018253922 0, 4844235.8030000003054738 2143467.87699999986216426 0, 4844245.14699999988079071 2143457.54799999995157123 0, 4844261.94099999964237213 2143443.55599999986588955 0, 4844263.49100000038743019 2143442.23199999984353781 0, 4844265.80900000035762787 2143440.25400000018998981 0, 4844272.55599999986588955 2143434.49299999978393316 0, 4844284.9150000000372529 2143424.47500000009313226 0, 4844295.05700000002980232 2143417.15899999998509884 0, 4844305.36400000005960464 2143413.33300000010058284 0, 4844311.70299999974668026 2143408.56199999991804361 0, 4844318.03500000014901161 2143400.14199999999254942 0, 4844320.71600000001490116 2143391.25199999986216426 0, 4844321.16000000014901161 2143390.4419999998062849 0, 4844327.83399999979883432 2143378.22800000011920929 0, 4844335.95100000035017729 2143361.82800000021234155 0, 4844345.65500000026077032 2143311.24899999983608723 0, 4844350.60099999979138374 2143300.97800000011920929 0, 4844383.73000000044703484 2143272.79999999981373549 0, 4844398.42599999997764826 2143250.11500000022351742 0, 4844446.04100000020116568 2143226.05299999983981252 0, 4844528.18599999975413084 2143210.63700000010430813 0, 4844570.90400000009685755 2143186.54499999992549419 0, 4844584.45500000007450581 2143188.88200000021606684 0, 4844667.52599999960511923 2143208.60300000011920929 0, 4844693.64499999955296516 2143202.00199999986216426 0, 4844727.36899999994784594 2143184.62800000002607703 0, 4844768.10199999995529652 2143175.87399999983608723 0, 4844768.05700000002980232 2143190.68999999994412065 0, 4844762.12600000016391277 2143187.2409999999217689 0, 4844730.19799999985843897 2143189.02199999988079071 0, 4844694.21200000029057264 2143205.97699999995529652 0, 4844667.75499999988824129 2143212.44499999983236194 0, 4844623.27599999960511923 2143205.44900000002235174 0, 4844583.09499999973922968 2143197.12699999986216426 0, 4844566.28199999965727329 2143203.94100000010803342 0, 4844530.60400000028312206 2143219.58300000010058284 0, 4844445.41600000020116568 2143233.25499999988824129 0, 4844404.13300000037997961 2143252.89600000018253922 0, 4844388.50899999961256981 2143276.43600000021979213 0, 4844354.76200000010430813 2143304.06399999978020787 0, 4844340.19500000029802322 2143364.76200000010430813 0, 4844340.19400000013411045 2143364.76200000010430813 0, 4844338.38599999994039536 2143368.41300000017508864 0, 4844338.27799999993294477 2143368.63299999991431832 0, 4844332.07600000035017729 2143381.16399999987334013 0, 4844327.30099999997764826 2143389.89999999990686774 0, 4844324.95799999963492155 2143394.18699999991804361 0, 4844324.78199999965727329 2143394.77000000001862645 0, 4844322.276999999769032 2143403.07700000004842877 0, 4844315.94500000029802322 2143411.49800000013783574 0, 4844309.60500000044703484 2143416.26899999985471368 0, 4844302.33200000040233135 2143418.96900000004097819 0, 4844299.29899999964982271 2143420.09500000020489097 0, 4844298.54399999976158142 2143420.64000000013038516 0, 4844289.54100000020116568 2143427.13499999977648258 0, 4844289.15699999965727329 2143427.4109999998472631 0, 4844276.79800000041723251 2143437.42799999983981252 0, 4844271.49100000038743019 2143441.9599999999627471 0, 4844266.1830000001937151 2143446.4909999999217689 0, 4844249.3880000002682209 2143460.48300000000745058 0, 4844247.04999999981373549 2143463.06900000013411045 0, 4844242.28399999998509884 2143468.33799999998882413 0, 4844240.04499999992549419 2143470.81300000008195639 0, 4844231.49299999978393316 2143477.37699999986216426 0, 4844229.26999999955296516 2143479.08300000010058284 0, 4844226.25800000037997961 2143482.94900000002235174 0, 4844218.50399999972432852 2143492.90499999979510903 0, 4844213.12100000027567148 2143498.94400000013411045 0, 4844208.5530000003054738 2143500.99500000011175871 0, 4844203.45199999958276749 2143503.2859999998472631 0, 4844193.84100000001490116 2143513.11899999994784594 0, 4844182.64400000032037497 2143522.02300000004470348 0, 4844181.44900000002235174 2143523.04600000008940697 0, 4844175.46200000029057264 2143528.17100000008940697 0, 4844164.15699999965727329 2143537.47000000020489097 0, 4844162.57500000018626451 2143538.77199999988079071 0, 4844160.54899999964982271 2143540.848000000230968 0, 4844152.86000000033527613 2143548.73100000014528632 0, 4844143.5669999998062849 2143557.63299999991431832 0, 4844135.75999999977648258 2143569.28299999982118607 0, 4844126.88599999994039536 2143575.85600000014528632 0, 4844115.89400000032037497 2143583.25100000016391277 0, 4844110.7369999997317791 2143586.72000000020489097 0, 4844080.98099999967962503 2143608.74800000013783574 0, 4844072.17499999981373549 2143618.02199999988079071 0, 4844045.95700000040233135 2143645.63799999980255961 0, 4844039.28600000031292439 2143650.96299999998882413 0, 4844038.51800000015646219 2143651.575999999884516 0, 4844032.625 2143656.28099999995902181 0, 4844027.12299999967217445 2143660.67299999995157123 0, 4843993.2630000002682209 2143687.28299999982118607 0, 4843965.24000000022351742 2143703.89699999988079071 0, 4843896.27599999960511923 2143770.63100000005215406 0, 4843889.25800000037997961 2143765.575999999884516 0)))',
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
                    't_id': 1001,
                    'area_terreno': 2032.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844200.20299999974668026 2143076.78500000014901161 0, 4844204.80499999970197678 2143077.12900000018998981 0, 4844182.09100000001490116 2143098.55200000014156103 0, 4844163.62100000027567148 2143106.50799999991431832 0, 4844144.53000000026077032 2143113.98600000003352761 0, 4844140.31099999975413084 2143116.549000000115484 0, 4844131.75299999956041574 2143125.17199999978765845 0, 4844108.2630000002682209 2143141.76500000013038516 0, 4844090.26699999999254942 2143167.82700000004842877 0, 4844070.71600000001490116 2143196.11799999978393316 0, 4844048.90099999960511923 2143262.38899999996647239 0, 4844014.0849999999627471 2143311.14600000018253922 0, 4843989.946000000461936 2143363.07700000004842877 0, 4843984.71100000012665987 2143385.63200000021606684 0, 4843923.68699999991804361 2143445.29499999992549419 0, 4843918.47800000011920929 2143442.58399999979883432 0, 4843979.17300000041723251 2143379.77300000004470348 0, 4843987.21999999973922968 2143361.60699999984353781 0, 4844011.33000000007450581 2143309.73300000000745058 0, 4844046.348000000230968 2143260.325999999884516 0, 4844066.94099999964237213 2143193.7140000001527369 0, 4844086.10099999979138374 2143165.15700000012293458 0, 4844104.12100000027567148 2143139.32899999991059303 0, 4844128.86500000022351742 2143120.11500000022351742 0, 4844143.44299999997019768 2143112.45200000004842877 0, 4844179.61099999956786633 2143097.1650000000372529 0, 4844200.20299999974668026 2143076.78500000014901161 0)))',
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
                    't_id': 1003,
                    'area_terreno': 3291.9,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844012.31799999997019768 2144004.89600000018253922 0, 4844053.41899999976158142 2143935.20599999977275729 0, 4844074.36699999962002039 2143914.82400000002235174 0, 4844092.2099999999627471 2143889.723000000230968 0, 4844109.81799999997019768 2143863.76099999994039536 0, 4844132.74000000022351742 2143856.03500000014901161 0, 4844163.10400000028312206 2143835.32700000004842877 0, 4844187.86500000022351742 2143806.15799999982118607 0, 4844228.96300000045448542 2143737.95800000010058284 0, 4844325.18400000035762787 2143662.69400000013411045 0, 4844354.34700000006705523 2143632.40400000009685755 0, 4844417.14800000004470348 2143543.424000000115484 0, 4844454.06799999997019768 2143477.70000000018626451 0, 4844496.21899999957531691 2143372.90700000012293458 0, 4844514.41399999987334013 2143341.73600000003352761 0, 4844536.19400000013411045 2143335.4599999999627471 0, 4844549.11899999994784594 2143328.53399999998509884 0, 4844581.51800000015646219 2143292.57800000021234155 0, 4844594.0719999996945262 2143295.42199999978765845 0, 4844600.46200000029057264 2143293.48300000000745058 0, 4844606.25700000021606684 2143278.78899999987334013 0, 4844622.34900000039488077 2143283.549000000115484 0, 4844635.0530000003054738 2143262.88100000005215406 0, 4844651.24700000043958426 2143266.32700000004842877 0, 4844659.03199999965727329 2143255.75799999991431832 0, 4844676.28600000031292439 2143251.73900000005960464 0, 4844711.25600000005215406 2143218.52000000001862645 0, 4844719.33899999968707561 2143213.10600000014528632 0, 4844721.42100000008940697 2143216.13899999996647239 0, 4844713.33800000045448542 2143221.55200000014156103 0, 4844678.36799999978393316 2143254.77199999988079071 0, 4844661.11500000022351742 2143258.79100000020116568 0, 4844653.32899999991059303 2143269.35999999986961484 0, 4844637.13499999977648258 2143265.91399999987334013 0, 4844624.43099999986588955 2143286.58199999993667006 0, 4844608.33899999968707561 2143281.82200000016018748 0, 4844602.54399999976158142 2143296.51599999982863665 0, 4844596.15400000009685755 2143298.45500000007450581 0, 4844583.60099999979138374 2143295.61100000003352761 0, 4844550.88599999994039536 2143330.27199999988079071 0, 4844536.85699999984353781 2143337.94700000016018748 0, 4844517.90799999982118607 2143345.61299999989569187 0, 4844498.92700000014156103 2143374.32500000018626451 0, 4844457.03500000014901161 2143479.32700000004842877 0, 4844419.09300000034272671 2143544.52400000020861626 0, 4844356.63499999977648258 2143634.47099999990314245 0, 4844326.87999999988824129 2143665.14699999988079071 0, 4844230.32899999991059303 2143741.00300000002607703 0, 4844189.84100000001490116 2143807.776999999769032 0, 4844165.96200000029057264 2143837.64300000015646219 0, 4844133.43699999991804361 2143859.9640000001527369 0, 4844110.97800000011920929 2143866.18699999991804361 0, 4844094.76400000043213367 2143891.73199999984353781 0, 4844076.00600000005215406 2143916.14500000001862645 0, 4844055.401999999769032 2143935.92100000008940697 0, 4844013.54600000008940697 2144006.6340000000782311 0, 4844012.31799999997019768 2144004.89600000018253922 0)))',
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
                    't_id': 1005,
                    'area_terreno': 4934.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844120.026999999769032 2143332.59500000020489097 0, 4844165.90600000042468309 2143254.95399999991059303 0, 4844104.27599999960511923 2143235.38100000005215406 0, 4844070.42200000025331974 2143291.54499999992549419 0, 4844120.026999999769032 2143332.59500000020489097 0)))',
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
                    't_id': 1007,
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
                    't_id': 1009,
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
                    't_id': 973,
                    'area_terreno': 70502.4,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844194.39400000032037497 2143484.89900000020861626 0, 4844199.74299999978393316 2143500.11100000003352761 0, 4844208.87899999972432852 2143496.00799999991431832 0, 4844214.2630000002682209 2143489.97000000020489097 0, 4844225.02799999993294477 2143476.14600000018253922 0, 4844235.8030000003054738 2143467.87699999986216426 0, 4844245.14699999988079071 2143457.54799999995157123 0, 4844261.94099999964237213 2143443.55599999986588955 0, 4844263.49100000038743019 2143442.23199999984353781 0, 4844265.80900000035762787 2143440.25400000018998981 0, 4844272.55599999986588955 2143434.49299999978393316 0, 4844284.9150000000372529 2143424.47500000009313226 0, 4844295.05700000002980232 2143417.15899999998509884 0, 4844305.36400000005960464 2143413.33300000010058284 0, 4844311.70299999974668026 2143408.56199999991804361 0, 4844318.03500000014901161 2143400.14199999999254942 0, 4844320.71600000001490116 2143391.25199999986216426 0, 4844321.16000000014901161 2143390.4419999998062849 0, 4844327.83399999979883432 2143378.22800000011920929 0, 4844335.95100000035017729 2143361.82800000021234155 0, 4844291.92200000025331974 2143406.40799999982118607 0, 4844254.71700000017881393 2143431.93500000005587935 0, 4844236.10300000011920929 2143449.92599999997764826 0, 4844218.57000000029802322 2143459.45200000004842877 0, 4844194.39400000032037497 2143484.89900000020861626 0)),((4844586.80900000035762787 2143268.3840000000782311 0, 4844566.28199999965727329 2143203.94100000010803342 0, 4844530.60400000028312206 2143219.58300000010058284 0, 4844445.41600000020116568 2143233.25499999988824129 0, 4844404.13300000037997961 2143252.89600000018253922 0, 4844388.50899999961256981 2143276.43600000021979213 0, 4844354.76200000010430813 2143304.06399999978020787 0, 4844340.19500000029802322 2143364.76200000010430813 0, 4844340.19400000013411045 2143364.76200000010430813 0, 4844338.38599999994039536 2143368.41300000017508864 0, 4844338.27799999993294477 2143368.63299999991431832 0, 4844332.07600000035017729 2143381.16399999987334013 0, 4844327.30099999997764826 2143389.89999999990686774 0, 4844324.95799999963492155 2143394.18699999991804361 0, 4844324.78199999965727329 2143394.77000000001862645 0, 4844322.276999999769032 2143403.07700000004842877 0, 4844315.94500000029802322 2143411.49800000013783574 0, 4844309.60500000044703484 2143416.26899999985471368 0, 4844302.33200000040233135 2143418.96900000004097819 0, 4844299.29899999964982271 2143420.09500000020489097 0, 4844298.54399999976158142 2143420.64000000013038516 0, 4844289.54100000020116568 2143427.13499999977648258 0, 4844289.15699999965727329 2143427.4109999998472631 0, 4844276.79800000041723251 2143437.42799999983981252 0, 4844271.49100000038743019 2143441.9599999999627471 0, 4844266.1830000001937151 2143446.4909999999217689 0, 4844249.3880000002682209 2143460.48300000000745058 0, 4844247.04999999981373549 2143463.06900000013411045 0, 4844242.28399999998509884 2143468.33799999998882413 0, 4844240.04499999992549419 2143470.81300000008195639 0, 4844231.49299999978393316 2143477.37699999986216426 0, 4844229.26999999955296516 2143479.08300000010058284 0, 4844226.25800000037997961 2143482.94900000002235174 0, 4844218.50399999972432852 2143492.90499999979510903 0, 4844213.12100000027567148 2143498.94400000013411045 0, 4844208.5530000003054738 2143500.99500000011175871 0, 4844203.45199999958276749 2143503.2859999998472631 0, 4844354.34700000006705523 2143632.40400000009685755 0, 4844417.14800000004470348 2143543.424000000115484 0, 4844454.06799999997019768 2143477.70000000018626451 0, 4844496.21899999957531691 2143372.90700000012293458 0, 4844514.41399999987334013 2143341.73600000003352761 0, 4844536.19400000013411045 2143335.4599999999627471 0, 4844549.11899999994784594 2143328.53399999998509884 0, 4844581.51800000015646219 2143292.57800000021234155 0, 4844586.80900000035762787 2143268.3840000000782311 0)))',
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

        search_criterion = {self.names.LC_PARCEL_T_PARCEL_NUMBER_F: '253940000000000230055000000000'}
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
                    't_id': 909,
                    'area_terreno': 7307.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844186.5580000001937151 2143347.0090000000782311 0, 4844176.49199999962002039 2143349.59100000001490116 0, 4844156.33200000040233135 2143371.39099999982863665 0, 4844170.94099999964237213 2143390.58699999982491136 0, 4844198.0400000000372529 2143411.57500000018626451 0, 4844236.10300000011920929 2143449.92599999997764826 0, 4844254.71700000017881393 2143431.93500000005587935 0, 4844291.92200000025331974 2143406.40799999982118607 0, 4844224.39800000004470348 2143346.85699999984353781 0, 4844186.5580000001937151 2143347.0090000000782311 0)))',
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
                    't_id': 915,
                    'area_terreno': 4283.7,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844216.73300000000745058 2143283.65299999993294477 0, 4844284.49399999994784594 2143293.94100000010803342 0, 4844301.3169999998062849 2143231.64699999988079071 0, 4844269.78899999987334013 2143204.60600000014528632 0, 4844239.02300000004470348 2143245.96100000012665987 0, 4844216.73300000000745058 2143283.65299999993294477 0)))',
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
                    't_id': 917,
                    'area_terreno': 30777.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844284.14400000032037497 2143108.43800000008195639 0, 4844291.65099999960511923 2143102.99800000013783574 0, 4844306.1650000000372529 2143072.30200000014156103 0, 4844315.90099999960511923 2143054.68600000021979213 0, 4844392.21300000045448542 2143089.67900000000372529 0, 4844416.24100000038743019 2143100.69799999985843897 0, 4844448.90099999960511923 2143130.46900000004097819 0, 4844446.04100000020116568 2143226.05299999983981252 0, 4844398.42599999997764826 2143250.11500000022351742 0, 4844383.73000000044703484 2143272.79999999981373549 0, 4844350.60099999979138374 2143300.97800000011920929 0, 4844345.65500000026077032 2143311.24899999983608723 0, 4844284.49399999994784594 2143293.94100000010803342 0, 4844301.3169999998062849 2143231.64699999988079071 0, 4844269.78899999987334013 2143204.60600000014528632 0, 4844213.29899999964982271 2143180.40599999995902181 0, 4844229.71700000017881393 2143151.82400000002235174 0, 4844245.67300000041723251 2143133.63200000021606684 0, 4844250.78299999982118607 2143128.11500000022351742 0, 4844294.71200000029057264 2143186.2409999999217689 0, 4844325.30700000002980232 2143167.71199999982491136 0, 4844341.13999999966472387 2143144.05700000002980232 0, 4844329.28399999998509884 2143126.86899999994784594 0, 4844284.14400000032037497 2143108.43800000008195639 0)))',
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
                    't_id': 943,
                    'area_terreno': 877.9,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844042.68800000008195639 2143467.91800000006332994 0, 4844078.84900000039488077 2143505.82299999985843897 0, 4844068.71399999968707561 2143518.98199999984353781 0, 4844032.42399999964982271 2143480.375 0, 4844036.30999999959021807 2143471.20300000021234155 0, 4844042.68800000008195639 2143467.91800000006332994 0)))',
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
                    't_id': 969,
                    'area_terreno': 818.8,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844032.42399999964982271 2143480.375 0, 4844068.71399999968707561 2143518.98199999984353781 0, 4844058.38999999966472387 2143529.89600000018253922 0, 4844047.20600000023841858 2143517.88499999977648258 0, 4844021.35099999979138374 2143491.13799999980255961 0, 4844028.46200000029057264 2143481.973000000230968 0, 4844032.42399999964982271 2143480.375 0)))',
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
                    't_id': 971,
                    'area_terreno': 967.1,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844021.35099999979138374 2143491.13799999980255961 0, 4844047.20600000023841858 2143517.88499999977648258 0, 4844036.97499999962747097 2143532.10000000009313226 0, 4843996.82500000018626451 2143509.47099999990314245 0, 4844021.35099999979138374 2143491.13799999980255961 0)))',
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
                    't_id': 977,
                    'area_terreno': 2614.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844170.94099999964237213 2143390.58699999982491136 0, 4844198.0400000000372529 2143411.57500000018626451 0, 4844236.10300000011920929 2143449.92599999997764826 0, 4844218.57000000029802322 2143459.45200000004842877 0, 4844174.01400000043213367 2143434.21799999987706542 0, 4844139.30900000035762787 2143415.08000000007450581 0, 4844170.94099999964237213 2143390.58699999982491136 0)))',
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
                    't_id': 979,
                    'area_terreno': 11087.8,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844047.20600000023841858 2143517.88499999977648258 0, 4844058.38999999966472387 2143529.89600000018253922 0, 4844052.38499999977648258 2143547.83999999985098839 0, 4844100.49600000027567148 2143577.78299999982118607 0, 4844022.85099999979138374 2143654.56499999994412065 0, 4843990.80099999997764826 2143614.41900000022724271 0, 4843972.88599999994039536 2143587.22399999992921948 0, 4843950.66799999959766865 2143559.20899999979883432 0, 4843961.11799999978393316 2143546.1159999999217689 0, 4843976.25299999956041574 2143534.28299999982118607 0, 4843979.08999999985098839 2143530.10800000000745058 0, 4843981.23300000000745058 2143523.24800000013783574 0, 4843990.4869999997317791 2143512.3390000001527369 0, 4843996.82500000018626451 2143509.47099999990314245 0, 4844036.97499999962747097 2143532.10000000009313226 0, 4844047.20600000023841858 2143517.88499999977648258 0)))',
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
                    't_id': 981,
                    'area_terreno': 15073.7,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844392.21300000045448542 2143089.67900000000372529 0, 4844410.20199999958276749 2143079.62999999988824129 0, 4844436.66299999970942736 2143070.32899999991059303 0, 4844446.17999999970197678 2143068.19599999999627471 0, 4844461.78399999998509884 2143069.35999999986961484 0, 4844475.14699999988079071 2143074.09700000006705523 0, 4844485.33700000029057264 2143079.5 0, 4844510.49500000011175871 2143099.68699999991804361 0, 4844524.12799999956041574 2143107.86100000003352761 0, 4844541.38700000010430813 2143110.31100000021979213 0, 4844570.90400000009685755 2143186.54499999992549419 0, 4844528.18599999975413084 2143210.63700000010430813 0, 4844446.04100000020116568 2143226.05299999983981252 0, 4844448.90099999960511923 2143130.46900000004097819 0, 4844416.24100000038743019 2143100.69799999985843897 0, 4844392.21300000045448542 2143089.67900000000372529 0)))',
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
                    't_id': 983,
                    'area_terreno': 2234.3,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4843950.66799999959766865 2143559.20899999979883432 0, 4843972.88599999994039536 2143587.22399999992921948 0, 4843956.58999999985098839 2143601.91699999989941716 0, 4843935.15699999965727329 2143630.32400000002235174 0, 4843906.50899999961256981 2143602.6830000001937151 0, 4843912.96800000034272671 2143591.52000000001862645 0, 4843935.15799999982118607 2143574.64099999982863665 0, 4843950.66799999959766865 2143559.20899999979883432 0)))',
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
                    't_id': 985,
                    'area_terreno': 4200.0,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844149.54999999981373549 2143331.77900000009685755 0, 4844176.49199999962002039 2143349.59100000001490116 0, 4844156.33200000040233135 2143371.39099999982863665 0, 4844170.94099999964237213 2143390.58699999982491136 0, 4844139.30900000035762787 2143415.08000000007450581 0, 4844089.43599999975413084 2143400.00499999988824129 0, 4844099.38399999961256981 2143379.22500000009313226 0, 4844109.19400000013411045 2143363.35699999984353781 0, 4844128.41999999992549419 2143340.89000000013038516 0, 4844149.54999999981373549 2143331.77900000009685755 0)))',
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
                    't_id': 993,
                    'area_terreno': 4814.4,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844149.54999999981373549 2143331.77900000009685755 0, 4844163.05999999959021807 2143299.45000000018626451 0, 4844168.31099999975413084 2143290.31100000021979213 0, 4844173.26900000032037497 2143278.36400000005960464 0, 4844179.0530000003054738 2143255.36299999989569187 0, 4844189.30900000035762787 2143236.91200000001117587 0, 4844239.02300000004470348 2143245.96100000012665987 0, 4844216.73300000000745058 2143283.65299999993294477 0, 4844186.5580000001937151 2143347.0090000000782311 0, 4844176.49199999962002039 2143349.59100000001490116 0, 4844149.54999999981373549 2143331.77900000009685755 0)))',
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
                    't_id': 995,
                    'area_terreno': 10495.1,
                    'GEOMETRY_PLOT': 'MultiPolygonZ (((4844089.43599999975413084 2143400.00499999988824129 0, 4844139.30900000035762787 2143415.08000000007450581 0, 4844174.01400000043213367 2143434.21799999987706542 0, 4844218.57000000029802322 2143459.45200000004842877 0, 4844194.39400000032037497 2143484.89900000020861626 0, 4844165.03699999954551458 2143499.39600000018253922 0, 4844099.30700000002980232 2143469.70200000004842877 0, 4844078.84900000039488077 2143505.82299999985843897 0, 4844042.68800000008195639 2143467.91800000006332994 0, 4844056.72099999990314245 2143429.36200000019744039 0, 4844084.80999999959021807 2143402.83300000010058284 0, 4844089.43599999975413084 2143400.00499999988824129 0)))',
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

        search_criterion = {self.names.LC_PARCEL_T_PARCEL_NUMBER_F: '253940000000000230241000000000'}
        features = self.ladm_data.get_parcel_data_to_compare_changes(self.db_pg, search_criterion=search_criterion)
        normalize_response(features)
        self.assertEqual(features, features_test)

    @classmethod
    def tearDownClass(cls):
        print("INFO: Closing open connections to databases")
        cls.db_pg.conn.close()
        unload_qgis_model_baker()


if __name__ == '__main__':
    nose2.main()
