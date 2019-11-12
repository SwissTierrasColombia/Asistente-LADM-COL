import nose2

from qgis.core import QgsWkbTypes, NULL
from qgis.testing import (start_app,
                          unittest)

start_app()  # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.utils.qgis_utils import QGISUtils
from asistente_ladm_col.logic.ladm_col.data.ladm_data import LADM_DATA
from asistente_ladm_col.config.general_config import LAYER
from asistente_ladm_col.config.table_mapping_config import Names
from asistente_ladm_col.tests.utils import (get_dbconn,
                                            restore_schema)


class TestLADMData(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        restore_schema('test_ladm_col_queries')

        self.db_connection = get_dbconn('test_ladm_col_queries')
        result = self.db_connection.test_connection()
        print('test_connection', result)

        if not result[1]:
            print('The test connection is not working')
            return

        self.qgis_utils = QGISUtils()
        self.ladm_data = LADM_DATA(self.qgis_utils)
        self.names = Names()

    def test_get_plots_related_to_parcels(self):
        print("\nINFO: Validating get plots related to parcels (Case: t_id)...")

        parcel_ids_tests = [list(), [939], [948, 939, 942]]
        plot_ids_tests = [list(), [1398], [1391, 1398, 1410]]

        count = 0
        for parcel_ids_test in parcel_ids_tests:
            plot_ids = self.ladm_data.get_plots_related_to_parcels(self.db_connection, parcel_ids_test, self.names.T_ID_F)
            # We use assertCountEqual to compare if two lists are the same regardless of the order of their elements.
            # https://docs.python.org/3.2/library/unittest.html#unittest.TestCase.assertCountEqual
            self.assertCountEqual(plot_ids, plot_ids_tests[count], "Failure with data set {}".format(count + 1))
            count += 1

        print("\nINFO: Validating get plots related to parcels (Case: custom field)...")
        plot_custom_field_ids_tests = [list(), [49379], [2614.3, 49379, 59108.5]]

        count = 0
        for parcel_ids_test in parcel_ids_tests:
            plot_custom_field_ids = self.ladm_data.get_plots_related_to_parcels(self.db_connection, parcel_ids_test, self.names.OP_PLOT_T_PLOT_AREA_F)
            self.assertCountEqual(plot_custom_field_ids, plot_custom_field_ids_tests[count], "Failure with data set {}".format(count + 1))
            count += 1

        print("\nINFO: Validating get plots related to parcels (Case: t_id) with preloaded tables...")

        layers = {self.names.OP_PLOT_T: {'name': self.names.OP_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
                  self.names.COL_UE_BAUNIT_T: {'name': self.names.COL_UE_BAUNIT_T, 'geometry': None, LAYER: None}}
        self.qgis_utils.get_layers(self.db_connection, layers, load=True)
        self.assertIsNotNone(layers, 'An error occurred while trying to get the layers of interest')

        count = 0
        for parcel_ids_test in parcel_ids_tests:
            plot_ids = self.ladm_data.get_plots_related_to_parcels(self.db_connection,
                                                                   parcel_ids_test,
                                                                   self.names.T_ID_F,
                                                                   plot_layer=layers[self.names.OP_PLOT_T][LAYER],
                                                                   uebaunit_table=layers[self.names.COL_UE_BAUNIT_T][LAYER])
            self.assertCountEqual(plot_ids, plot_ids_tests[count], "Failure with data set {}".format(count + 1))
            count += 1

    def test_get_parcels_related_to_plots(self):
        print("\nINFO: Validating get parcels related to plots (Case: t_id)...")

        plot_ids_tests = [list(), [1398], [1391, 1398, 1410]]
        parcel_ids_tests = [list(), [939], [948, 939, 942]]

        count = 0
        for plot_ids_test in plot_ids_tests:
            parcel_ids = self.ladm_data.get_parcels_related_to_plots(self.db_connection, plot_ids_test, self.names.T_ID_F)
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
            parcel_custom_field_ids = self.ladm_data.get_parcels_related_to_plots(self.db_connection,
                                                                                  plot_ids_test,
                                                                                  self.names.OP_PARCEL_T_PARCEL_NUMBER_F)
            self.assertCountEqual(parcel_custom_field_ids, parcel_custom_field_ids_tests[count],
                                  "Failure with data set {}".format(count + 1))
            count += 1

        print("\nINFO: Validating get parcels related to plots (Case: t_id) with preloaded tables...")

        layers = {
            self.names.OP_PARCEL_T: {'name': self.names.OP_PARCEL_T, 'geometry': None, LAYER: None},
            self.names.COL_UE_BAUNIT_T: {'name': self.names.COL_UE_BAUNIT_T, 'geometry': None, LAYER: None}
        }
        self.qgis_utils.get_layers(self.db_connection, layers, load=True)
        self.assertIsNotNone(layers, 'An error occurred while trying to get the layers of interest')

        count = 0
        for plot_ids_test in plot_ids_tests:
            parcel_ids = self.ladm_data.get_parcels_related_to_plots(self.db_connection,
                                                                     plot_ids_test,
                                                                     self.names.T_ID_F,
                                                                     parcel_table=layers[self.names.OP_PARCEL_T][LAYER],
                                                                     uebaunit_table=layers[self.names.COL_UE_BAUNIT_T][LAYER])
            self.assertCountEqual(parcel_ids, parcel_ids_tests[count], "Failure with data set {}".format(count + 1))
            count += 1

    def test_get_parcel_data_to_compare_changes(self):
        print("\nINFO: Validating get parcels data ...")

        features_test = {
            '253940000000000230097000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230097000000000',
                    'nombre': 'SIN INFO',
                    'tipo': 'NPH',
                    't_id': 307
                },
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': NULL,
                    'numero_predial': '253940000000000230097000000000',
                    'nombre': 'Santa Lucía',
                    'tipo': 'NPH',
                    't_id': 312
                }
            ],
            '253940000000000230098000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230098000000000',
                    'nombre': 'Santa Lucía',
                    'tipo': 'NPH',
                    't_id': 308
                }
            ],
            '253940000000000230072000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '167-24545',
                    'numero_predial': '253940000000000230072000000000',
                    'nombre': 'El Porvenir',
                    'tipo': 'NPH',
                    't_id': 309
                }
            ],
            '253940000000000230074000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '167-1527',
                    'numero_predial': '253940000000000230074000000000',
                    'nombre': 'Tudelita',
                    'tipo': 'NPH',
                    't_id': 310
                }
            ],
            '253940000000000230054000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '167-3652',
                    'numero_predial': '253940000000000230054000000000',
                    'nombre': 'San Pedro',
                    'tipo': 'NPH',
                    't_id': 313
                }
            ],
            '253940000000000230257000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '167-24800',
                    'numero_predial': '253940000000000230257000000000',
                    'nombre': 'Casimiro',
                    'tipo': 'NPH',
                    't_id': 314
                }
            ],
            '253940000000000230241000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '167-8620',
                    'numero_predial': '253940000000000230241000000000',
                    'nombre': 'SIN INFO',
                    'tipo': 'NPH',
                    't_id': 315
                },
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '167-8620',
                    'numero_predial': '253940000000000230241000000000',
                    'nombre': 'SIN INFO',
                    'tipo': 'NPH',
                    't_id': 316
                },
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '167-8620',
                    'numero_predial': '253940000000000230241000000000',
                    'nombre': 'SIN INFO',
                    'tipo': 'NPH',
                    't_id': 319
                },
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '167-8620',
                    'numero_predial': '253940000000000230241000000000',
                    'nombre': 'SIN INFO',
                    'tipo': 'NPH',
                    't_id': 320
                },
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '167-8620',
                    'numero_predial': '253940000000000230241000000000',
                    'nombre': 'SIN INFO',
                    'tipo': 'NPH',
                    't_id': 326
                },
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '167-8620',
                    'numero_predial': '253940000000000230241000000000',
                    'nombre': 'Tudela Juntas',
                    'tipo': 'NPH',
                    't_id': 327
                },
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '167-8620',
                    'numero_predial': '253940000000000230241000000000',
                    'nombre': 'SIN INFO',
                    'tipo': 'NPH',
                    't_id': 328
                },
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '167-8620',
                    'numero_predial': '253940000000000230241000000000',
                    'nombre': 'El Tigre',
                    'tipo': 'NPH',
                    't_id': 344
                },
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '167-8620',
                    'numero_predial': '253940000000000230241000000000',
                    'nombre': 'SIN INFO',
                    'tipo': 'NPH',
                    't_id': 345
                },
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '167-8620',
                    'numero_predial': '253940000000000230241000000000',
                    'nombre': 'Mardoqueo',
                    'tipo': 'NPH',
                    't_id': 346
                },
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '167-8620',
                    'numero_predial': '253940000000000230241000000000',
                    'nombre': 'Angel',
                    'tipo': 'NPH',
                    't_id': 347
                },
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230241000000000',
                    'nombre': 'SIN INFO',
                    'tipo': 'NPH',
                    't_id': 348
                },
                {
                    'departamento': '25',
                    'municipio': '394',
                    'zona': '00',
                    'fmi': '167-15523',
                    'numero_predial': '253940000000000230241000000000',
                    'nombre': 'Hoya Las Juntas',
                    'tipo': 'PropiedadHorizontal.Matriz',
                    't_id': 355
                }
            ],
            '253940000000000230235000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '167-15137',
                    'numero_predial': '253940000000000230235000000000',
                    'nombre': 'Los Naranjos',
                    'tipo': 'NPH',
                    't_id': 317
                }
            ],
            '253940000000000230254000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '167-18982',
                    'numero_predial': '253940000000000230254000000000',
                    'nombre': 'El Muche',
                    'tipo': 'NPH',
                    't_id': 318
                }
            ],
            '253940000000000230242000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '167-15523',
                    'numero_predial': '253940000000000230242000000000',
                    'nombre': 'El Guamal',
                    'tipo': 'NPH',
                    't_id': 321
                }
            ],
            '253940000000000230055000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '103002700241600084',
                    'numero_predial': '253940000000000230055000000000',
                    'nombre': 'El Volador',
                    'tipo': 'NPH',
                    't_id': 322
                }
            ],
            '253940000000000230056000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230056000000000',
                    'nombre': 'El Volador',
                    'tipo': 'NPH',
                    't_id': 323
                },
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230056000000000',
                    'nombre': 'El Almorzadero',
                    'tipo': 'NPH',
                    't_id': 324
                }
            ],
            '253940000000000230057000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '167-21463',
                    'numero_predial': '253940000000000230057000000000',
                    'nombre': 'SIN INFO',
                    'tipo': 'NPH',
                    't_id': 325
                }
            ],
            '253940000000000230234000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '167-15166',
                    'numero_predial': '253940000000000230234000000000',
                    'nombre': 'SIN INFO',
                    'tipo': 'NPH',
                    't_id': 329
                },
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '167-15166',
                    'numero_predial': '253940000000000230234000000000',
                    'nombre': 'SIN INFO',
                    'tipo': 'NPH',
                    't_id': 349
                }
            ],
            '253940000000000230213000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '167-9028',
                    'numero_predial': '253940000000000230213000000000',
                    'nombre': 'El Volador',
                    'tipo': 'NPH',
                    't_id': 330
                }
            ],
            '253940000000000230068000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '167-8114',
                    'numero_predial': '253940000000000230068000000000',
                    'nombre': 'Tudelita',
                    'tipo': 'NPH',
                    't_id': 331
                }
            ],
            '253940000000000230101000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230101000000000',
                    'nombre': 'Santa Lucia',
                    'tipo': 'NPH',
                    't_id': 332
                }
            ],
            '253940000000000230100000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230100000000000',
                    'nombre': 'SIN INFO',
                    'tipo': 'NPH',
                    't_id': 333
                }
            ],
            '253940000000000230099000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '10302400719A670000',
                    'numero_predial': '253940000000000230099000000000',
                    'nombre': 'Santa Lucia',
                    'tipo': 'NPH',
                    't_id': 334
                }
            ],
            '253940000000000230069000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '102042200446620144',
                    'numero_predial': '253940000000000230069000000000',
                    'nombre': 'Las Juntas',
                    'tipo': 'NPH',
                    't_id': 335
                }
            ],
            '253940000000000230070000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '201023900285580000',
                    'numero_predial': '253940000000000230070000000000',
                    'nombre': 'Bellavista',
                    'tipo': 'NPH',
                    't_id': 336
                }
            ],
            '253940000000000230082000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230082000000000',
                    'nombre': 'Santa Lucia',
                    'tipo': 'NPH',
                    't_id': 337
                }
            ],
            '253940000000000230081000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230081000000000',
                    'nombre': 'Santa Lucia',
                    'tipo': 'NPH',
                    't_id': 338
                }
            ],
            '253940000000000230080000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230080000000000',
                    'nombre': 'Santa Lucia',
                    'tipo': 'NPH',
                    't_id': 339
                }
            ],
            '253940000000000230079000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230079000000000',
                    'nombre': 'Santa Lucia',
                    'tipo': 'NPH',
                    't_id': 340
                }
            ],
            '253940000000000230078000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230078000000000',
                    'nombre': 'Santa Lucia',
                    'tipo': 'NPH',
                    't_id': 341
                }
            ],
            '253940000000000230077000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230077000000000',
                    'nombre': 'SIN INFO',
                    'tipo': 'NPH',
                    't_id': 342
                }
            ],
            '253940000000000320022000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000320022000000000',
                    'nombre': 'Escuela Alto de Izacar',
                    'tipo': 'NPH',
                    't_id': 343
                }
            ],
            '253940000000000230076000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230076000000000',
                    'nombre': 'Santa Lucia',
                    'tipo': 'NPH',
                    't_id': 350
                }
            ],
            NULL: [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': NULL,
                    'nombre': 'Camino',
                    'tipo': 'NPH',
                    't_id': 351
                },
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': NULL,
                    'nombre': 'Camino',
                    'tipo': 'NPH',
                    't_id': 352
                },
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': NULL,
                    'nombre': 'Vía Interveredal',
                    'tipo': 'NPH',
                    't_id': 353
                },
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': NULL,
                    'nombre': 'Bajo',
                    'tipo': 'NPH',
                    't_id': 354
                },
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': NULL,
                    'numero_predial': NULL,
                    'nombre': 'Apartamento 101',
                    'tipo': 'PropiedadHorizontal.UnidadPredial',
                    't_id': 356
                },
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': NULL,
                    'numero_predial': NULL,
                    'nombre': 'Apartamento 202',
                    'tipo': 'PropiedadHorizontal.UnidadPredial',
                    't_id': 357
                }
            ],
            '253940000000000230073000000000': [
                {
                    'departamento': '25',
                    'municipio': '394',
                    'zona': '00',
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230073000000000',
                    'nombre': 'El Pomarroso',
                    'tipo': 'NPH',
                    't_id': 311
                }
            ]
        }
        features = self.ladm_data.get_parcel_data_to_compare_changes(self.db_connection)
        self.assertCountEqual(features, features_test)

        print("\nINFO: Validating get parcels data using search criterion...")

        features_test = {
            '253940000000000230054000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': '167-3652',
                    'numero_predial': '253940000000000230054000000000',
                    'nombre': 'San Pedro',
                    'tipo': 'NPH',
                    't_id': 313
                }
            ]
        }
        search_criterion = {self.names.OP_PARCEL_T_FMI_F: '167-3652'}
        features = self.ladm_data.get_parcel_data_to_compare_changes(self.db_connection, search_criterion=search_criterion)
        self.assertCountEqual(features, features_test)

        features_test = {
            '253940000000000230097000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230097000000000',
                    'nombre': 'SIN INFO',
                    'tipo': 'NPH',
                    't_id': 307
                }
            ],
            '253940000000000230098000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230098000000000',
                    'nombre': 'Santa Lucía',
                    'tipo': 'NPH',
                    't_id': 308
                }
            ],
            '253940000000000230241000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230241000000000',
                    'nombre': 'SIN INFO',
                    'tipo': 'NPH',
                    't_id': 348
                }
            ],
            '253940000000000230056000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230056000000000',
                    'nombre': 'El Volador',
                    'tipo': 'NPH',
                    't_id': 323
                },
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230056000000000',
                    'nombre': 'El Almorzadero',
                    'tipo': 'NPH',
                    't_id': 324
                }
            ],
            '253940000000000230101000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230101000000000',
                    'nombre': 'Santa Lucia',
                    'tipo': 'NPH',
                    't_id': 332
                }
            ],
            '253940000000000230100000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230100000000000',
                    'nombre': 'SIN INFO',
                    'tipo': 'NPH',
                    't_id': 333
                }
            ],
            '253940000000000230082000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230082000000000',
                    'nombre': 'Santa Lucia',
                    'tipo': 'NPH',
                    't_id': 337
                }
            ],
            '253940000000000230081000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230081000000000',
                    'nombre': 'Santa Lucia',
                    'tipo': 'NPH',
                    't_id': 338
                }
            ],
            '253940000000000230080000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230080000000000',
                    'nombre': 'Santa Lucia',
                    'tipo': 'NPH',
                    't_id': 339
                }
            ],
            '253940000000000230079000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230079000000000',
                    'nombre': 'Santa Lucia',
                    'tipo': 'NPH',
                    't_id': 340
                }
            ],
            '253940000000000230078000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230078000000000',
                    'nombre': 'Santa Lucia',
                    'tipo': 'NPH',
                    't_id': 341
                }
            ],
            '253940000000000230077000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230077000000000',
                    'nombre': 'SIN INFO',
                    'tipo': 'NPH',
                    't_id': 342
                }
            ],
            '253940000000000320022000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000320022000000000',
                    'nombre': 'Escuela Alto de Izacar',
                    'tipo': 'NPH',
                    't_id': 343
                }
            ],
            '253940000000000230076000000000': [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230076000000000',
                    'nombre': 'Santa Lucia',
                    'tipo': 'NPH',
                    't_id': 350
                }
            ],
            NULL: [
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': NULL,
                    'nombre': 'Camino',
                    'tipo': 'NPH',
                    't_id': 351
                },
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': NULL,
                    'nombre': 'Camino',
                    'tipo': 'NPH',
                    't_id': 352
                },
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': NULL,
                    'nombre': 'Vía Interveredal',
                    'tipo': 'NPH',
                    't_id': 353
                },
                {
                    'departamento': NULL,
                    'municipio': NULL,
                    'zona': NULL,
                    'fmi': 'SIN INFO',
                    'numero_predial': NULL,
                    'nombre': 'Bajo',
                    'tipo': 'NPH',
                    't_id': 354
                }
            ],
            '253940000000000230073000000000': [
                {
                    'departamento': '25',
                    'municipio': '394',
                    'zona': '00',
                    'fmi': 'SIN INFO',
                    'numero_predial': '253940000000000230073000000000',
                    'nombre': 'El Pomarroso',
                    'tipo': 'NPH',
                    't_id': 311
                }
            ]
        }
        search_criterion = {self.names.OP_PARCEL_T_FMI_F: 'SIN INFO'}
        features = self.ladm_data.get_parcel_data_to_compare_changes(self.db_connection, search_criterion=search_criterion)
        self.assertCountEqual(features, features_test)

    def tearDownClass():
        print('tearDown test_ladm_data')


if __name__ == '__main__':
    nose2.main()
