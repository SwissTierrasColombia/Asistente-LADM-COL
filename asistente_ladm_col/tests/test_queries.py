import nose2
import json

from qgis.testing import (start_app,
                          unittest)

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.tests.utils import (get_dbconn,
                                            restore_schema)


class TestQueries(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        restore_schema('test_ladm_col_queries')

        self.db_connection = get_dbconn('test_ladm_col_queries')
        result = self.db_connection.test_connection()
        print('test_connection', result)

        if not result[1]:
            print('The test connection is not working')
            return

    def test_igac_basic_info_query(self):
        print("\nINFO: Validating basic info query from IGAC...")

        plot_t_id = 774
        records = self.db_connection.get_igac_basic_info(plot_t_id=plot_t_id)
        self.assertTrue(1 == len(records), 'The number of records obtained is not as expected')

        json_result = json.loads('[{"id":774,"attributes":{"Área de terreno [m2]":7307.3,"extdireccion":[{"id":775,"attributes":{"País":"Colombia","Departamento":"Cundinamarca","Ciudad":"La Palma","Código postal":null,"Apartado correo":null,"Nombre calle":"Hoya Las Juntas"}}],"predio":[{"id":355,"attributes":{"Nombre":"Hoya Las Juntas","Departamento":"25","Municipio":"394","Zona":"00","NUPRE":"0022","FMI":"167-15523","Número predial":"253940000000000230241000000000","Número predial anterior":"25394000000230242000","Tipo":"PropiedadHorizontal.Matriz","Destinación económica":null,"construccion":[{"id":148,"attributes":{"Área construcción":null,"extdireccion":[],"unidadconstruccion":[{"id":882,"attributes":{"Número de pisos":1,"Área construida [m2]":50.8,"Número de habitaciones":null,"Número de baños":null,"Número de locales":null,"Uso":null,"Puntuación":null,"extdireccion":[]}},{"id":876,"attributes":{"Número de pisos":1,"Área construida [m2]":50.8,"Número de habitaciones":null,"Número de baños":null,"Número de locales":null,"Uso":null,"Puntuación":null,"extdireccion":[]}}]}}]}}]}}]')
        self.assertTrue(ordered(json_result) == ordered(records[0]['terreno']), 'The result obtained is not as expected: {} {}'.format(json_result , records[0]['terreno']))

    def test_igac_legal_info_query(self):
        print("\nINFO: Validating legal info query from IGAC...")

        plot_t_id = 774
        records = self.db_connection.get_igac_legal_info(plot_t_id=plot_t_id)
        self.assertTrue(1 == len(records), 'The number of records obtained is not as expected')

        json_result = json.loads("""[{"id":774,"attributes":{"Área de terreno [m2]":7307.3,"predio":[{"id":355,"attributes":{"Nombre":"Hoya Las Juntas","NUPRE":"0022","FMI":"167-15523","Número predial":"253940000000000230241000000000","Número predial anterior":"25394000000230242000","col_derecho":[{"id":1940,"attributes":{"Tipo de derecho":"Dominio","Código registral":null,"Descripción":null,"col_fuenteadministrativa":[{"id":54,"attributes":{"Tipo de fuente administrativa":"Contrato","Estado disponibilidad":"Desconocido","Archivo fuente":"E:\\\\fuentes\\\\Tecnica_Societaria_36_Junio-2009_-_art2_Imagen_01-a3b2d.jpg"}}],"la_agrupacion_interesados":[{"id":106,"attributes":{"Tipo de agrupación de interesados":"Grupo_Civil","Nombre":"1","col_interesado":[{"id":121,"attributes":{"Cédula de ciudadanía":"14","Nombre":"14 14primer apellido 14segundo apellido 14primer nombre 14segundo nombre","Género":"Masculino","interesado_contacto":[],"fraccion":null}},{"id":109,"attributes":{"Cédula de ciudadanía":"2","Nombre":"2 2primer apellido 2segundo apellido 2primer nombre 2segundo nombre","Género":"Femenino","interesado_contacto":[],"fraccion":null}}]}}]}}],"col_restriccion":[],"col_responsabilidad":[],"col_hipoteca":[]}}]}}]""")
        self.assertTrue(ordered(json_result) == ordered(records[0]['terreno']),
                        'The result obtained is not as expected: {} {}'.format(json_result, records[0]['terreno']))

    def test_igac_property_record_card_info_query(self):
        print("\nINFO: Validating property record card info query from IGAC...")

        plot_t_id = 774
        records = self.db_connection.get_igac_property_record_card_info(plot_t_id=plot_t_id)
        self.assertTrue(1 == len(records), 'The number of records obtained is not as expected')

        json_result = json.loads('[{"id":774,"attributes":{"Área de terreno [m2]":7307.3,"predio":[{"id":355,"attributes":{"Nombre":"Hoya Las Juntas","Departamento":"25","Municipio":"394","Zona":"00","NUPRE":"0022","FMI":"167-15523","Número predial":"253940000000000230241000000000","Número predial anterior":"25394000000230242000","Tipo":"PropiedadHorizontal.Matriz","Localidad/Comuna":null,"Barrio":null,"Manzana/Vereda":null,"Terreno":null,"Condición propiedad":null,"Edificio":null,"Piso":null,"Unidad":null,"Estado NUPRE":null,"Destinación económica":null,"Tipo de predio":"Privado.Individual","Tipo predio público":null,"Formalidad":"Formal","Estrato":"Estrato_1","Clase suelo POT":"Rural","Categoría suelo POT":"Suburbano","Derecho FMI":"Propiedad","Inscrito RUPTA":null,"Fecha medida RUPTA":null,"Anotación FMI RUPTA":null,"Inscrito protección colectiva":null,"Fecha protección colectiva":null,"Anotación FMI protección colectiva":null,"Inscrito proteccion Ley 1448":null,"Fecha protección ley 1448":null,"Anotación FDM Ley 1448":null,"Inscripción URT":null,"Fecha de inscripción URT":null,"Anotación FMI URT":null,"Vigencia fiscal":null,"Observaciones":"32 observaciones","Fecha visita predial":"2017-04-23","Nombre quien atendio":"32 nombre_quien_atendio","Número de documento de quien atendio":"Cc","Categoría quien atendio":null,"Tipo de documento de quien atendio":"Cedula_Ciudadania","Nombre encuestador":"32 nombre encuestador","Número de documento encuestador":"Cc","Tipo de documento encuestador":"Cedula_Ciudadania","nucleofamiliar":[{"id":2048,"attributes":{"Documento de identidad":"30","Tipo de documento":"Cedula_Ciudadania","Organo emisor":null,"Fecha de emisión":null,"Primer nombre":"30primer nombre","Segundo nombre":"30segundo nombre","Primer apellido":"30primer apellido","Segundo apellido":"30segundo apellido","Fecha de nacimiento":null,"Lugar de nacimiento":null,"Nacionalidad":"30colombiano","Discapacidad":null,"Género":null,"Habita predio":null,"Parentesco":null,"Etnia":null,"Dirección":"30direccion","Celular":"30celular"}}],"investigacionmercado":[]}}]}}]')
        self.assertTrue(ordered(json_result) == ordered(records[0]['terreno']),
                        'The result obtained is not as expected: {} {}'.format(json_result, records[0]['terreno']))

    def test_igac_physical_info_query(self):
        print("\nINFO: Validating physical info query from IGAC...")

        plot_t_id = 774
        records = self.db_connection.get_igac_physical_info(plot_t_id=plot_t_id)
        self.assertTrue(1 == len(records), 'The number of records obtained is not as expected')

        json_result = json.loads('[{"id":774,"attributes":{"Área registral [m2]":7307.0,"Área calculada [m2]":7307.3,"predio":[{"id":355,"attributes":{"Nombre":"Hoya Las Juntas","NUPRE":"0022","FMI":"167-15523","Número predial":"253940000000000230241000000000","Número predial anterior":"25394000000230242000","construccion":[{"id":148,"attributes":{"Área construcción":null,"Ńúmero de pisos":null,"col_fuenteespacial":[],"unidadconstruccion":[{"id":882,"attributes":{"Número de pisos":1,"Uso":null,"Puntuación":null,"Tipología":null,"Destino económico":null,"Tipo de construcción":null,"Área privada construida [m2]":null,"Área construida [m2]":50.8,"col_fuenteespacial":[]}},{"id":876,"attributes":{"Número de pisos":1,"Uso":null,"Puntuación":null,"Tipología":null,"Destino económico":null,"Tipo de construcción":null,"Área privada construida [m2]":null,"Área construida [m2]":50.8,"col_fuenteespacial":[]}}]}}]}}],"col_territorioagricola_terreno_territorio_agricola":[],"col_bosqueareasemi_terreno_bosque_area_seminaturale":[],"col_cuerpoagua_terreno_evidencia_cuerpo_agua":[],"col_explotaciontipo_terreno_explotacion":[],"col_afectacion_terreno_afectacion":[],"col_servidumbretipo_terreno_servidumbre":[],"Linderos externos":{"lindero":[{"id":208,"attributes":{"Longitud [m]":10.4}},{"id":176,"attributes":{"Longitud [m]":53.8}},{"id":179,"attributes":{"Longitud [m]":88.4}},{"id":263,"attributes":{"Longitud [m]":127.9}},{"id":180,"attributes":{"Longitud [m]":71.0}}],"puntolindero":[{"id":438,"attributes":{"Nombre":"159","coordenadas":"963584.207 1077451.685"}},{"id":439,"attributes":{"Nombre":"158","coordenadas":"963621.476 1077426.21"}},{"id":476,"attributes":{"Nombre":"160","coordenadas":"963565.552 1077469.653"}},{"id":666,"attributes":{"Nombre":"123","coordenadas":"963485.877 1077390.939"}},{"id":673,"attributes":{"Nombre":"124","coordenadas":"963500.46 1077410.171"}},{"id":688,"attributes":{"Nombre":"108","coordenadas":"963527.536 1077431.216"}},{"id":725,"attributes":{"Nombre":"54","coordenadas":"963506.085 1077369.163"}},{"id":730,"attributes":{"Nombre":"57","coordenadas":"963554.02 1077366.511"}},{"id":731,"attributes":{"Nombre":"56","coordenadas":"963516.161 1077366.597"}}]},"Linderos internos":{"lindero":[],"puntolindero":[]},"puntolevantamiento":[{"id":841,"attributes":{"coordenadas":"963548.26 1077404.264"}},{"id":842,"attributes":{"coordenadas":"963540.808 1077415.143"}},{"id":843,"attributes":{"coordenadas":"963543.76 1077417.646"}},{"id":864,"attributes":{"coordenadas":"963551.212 1077406.767"}}],"col_fuenteespacial":[]}}]')
        self.assertTrue(ordered(json_result) == ordered(records[0]['terreno']),
                        'The result obtained is not as expected: {} {}'.format(json_result, records[0]['terreno']))

    def test_igac_economic_info_query(self):
        print("\nINFO: Validating economic info query from IGAC...")

        plot_t_id = 774
        records = self.db_connection.get_igac_economic_info(plot_t_id=plot_t_id)
        self.assertTrue(1 == len(records), 'The number of records obtained is not as expected')

        json_result = json.loads('[{"id":774,"attributes":{"Área de terreno [m2]":7307.3,"Avalúo terreno [COP]":1,"zona_homogenea_geoeconomica":[{"id":74,"attributes":{"Porcentaje":41.66,"Valor":2,"Identificador":"2"}},{"id":27,"attributes":{"Porcentaje":58.34,"Valor":2,"Identificador":"2"}}],"zona_homogenea_fisica":[{"id":74,"attributes":{"Porcentaje":41.66,"Identificador":"2"}},{"id":27,"attributes":{"Porcentaje":58.34,"Identificador":"2"}}],"predio":[{"id":355,"attributes":{"Nombre":"Hoya Las Juntas","Departamento":"25","Municipio":"394","Zona":"00","NUPRE":"0022","FMI":"167-15523","Número predial":"253940000000000230241000000000","Número predial anterior":"25394000000230242000","Avalúo predio [COP]":null,"Tipo":"PropiedadHorizontal.Matriz","Destinación económica":null,"construccion":[{"id":148,"attributes":{"Área construcción":null,"unidadconstruccion":[{"id":882,"attributes":{"Número de pisos":1,"Área construida [m2]":50.8,"Uso":null,"Destino económico":null,"Tipología":null,"Puntuación":null,"Valor m2 construcción [COP]":null,"Año construcción":null,"Estado conservación":null,"Número de habitaciones":null,"Número de baños":null,"Número de cocinas":null,"Número de oficinas":null,"Número de estudios":null,"Número de bodegas":null,"Numero de locales":null,"Número de salas":null,"Número de comedores":null,"Material":null,"Estilo":null,"Acceso":null,"nivel de acceso":null,"Ubicación en copropiedad":null,"Disposición":null,"Funcionalidad":null,"Tipo de construcción":null,"Calificación":[]}},{"id":876,"attributes":{"Número de pisos":1,"Área construida [m2]":50.8,"Uso":null,"Destino económico":null,"Tipología":null,"Puntuación":null,"Valor m2 construcción [COP]":null,"Año construcción":null,"Estado conservación":null,"Número de habitaciones":null,"Número de baños":null,"Número de cocinas":null,"Número de oficinas":null,"Número de estudios":null,"Número de bodegas":null,"Numero de locales":null,"Número de salas":null,"Número de comedores":null,"Material":null,"Estilo":null,"Acceso":null,"nivel de acceso":null,"Ubicación en copropiedad":null,"Disposición":null,"Funcionalidad":null,"Tipo de construcción":null,"Calificación":[]}}]}}]}}]}}]')
        self.assertTrue(ordered(json_result) == ordered(records[0]['terreno']),
                        'The result obtained is not as expected: {} {}'.format(json_result, records[0]['terreno']))

    def tearDownClass():
        print('tearDown test_queries')

def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj

if __name__ == '__main__':
    nose2.main()

