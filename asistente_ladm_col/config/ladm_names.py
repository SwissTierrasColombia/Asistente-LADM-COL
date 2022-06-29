from asistente_ladm_col.utils.singleton import Singleton

SPECIAL_CHARACTERS = "special_characters"
DIGITS = "digits"

class LADMNames(metaclass=Singleton):
    """
    Singleton to handle domain values (which are not dependent on the database engine) in a single point of access.
    """
    """
    USEFUL DOMAIN VALUES
    """
    LC_CONDITION_PARCEL_TYPE_D_ILICODE_F_INFORMAL_V = "Informal"
    LC_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V = "Persona_Natural"
    LC_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V = "Persona_Juridica"
    LC_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V = "NIT"
    LC_PARTY_DOCUMENT_TYPE_D_ILICODE_F_SEQUENTIAL_V = "Secuencial"
    LC_RIGHT_TYPE_D_ILICODE_F_OWNERSHIP_V = "Dominio"
    LC_RIGHT_TYPE_D_ILICODE_F_OCCUPATION_V = "Ocupacion"
    LC_RIGHT_TYPE_D_ILICODE_F_POSSESSION_V = "Posesion"
    CI_CODE_PRESENTATION_FORM_D_DOCUMENT_V = "Documento"
    FDC_PARTY_DOCUMENT_TYPE_D_ILICODE_F_CC_V = "Cedula_ciudadania"
    FDC_PARTY_DOCUMENT_TYPE_D_ILICODE_F_DOC_ID_V = "Tarjeta_identidad"
    ERR_ERROR_STATE_D_ERROR_V = "Error"
    ERR_ERROR_STATE_D_FIXED_V = "Corregido"
    ERR_ERROR_STATE_D_EXCEPTION_V = "Excepcion"

    """
    PARCEL TYPE
    """
    PARCEL_TYPE_NO_HORIZONTAL_PROPERTY = "NPH"
    PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT = "PH.Matriz"
    PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT = "PH.Unidad_Predial"
    PARCEL_TYPE_CONDOMINIUM_PARENT = "Condominio.Matriz"
    PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT = "Condominio.Unidad_Predial"
    PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA = "Mejora.PH"
    PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA = "Mejora.NPH"
    PARCEL_TYPE_CEMETERY_PARENT = "Parque_Cementerio.Matriz"
    PARCEL_TYPE_CEMETERY_PARCEL_UNIT = "Parque_Cementerio.Unidad_Predial"
    PARCEL_TYPE_ROAD = "Via"
    PARCEL_TYPE_PUBLIC_USE = "Bien_Uso_Publico"

    """
    LADM PACKAGES
    """
    SURVEYING_AND_REPRESENTATION_PACKAGE = "Topografía y Representación"
    SPATIAL_UNIT_PACKAGE = "Unidad Espacial"
    BA_UNIT_PACKAGE = "Unidad Administrativa"
    RRR_PACKAGE = "Derechos, Restricciones y Responsabilidades"
    PARTY_PACKAGE = "Interesados"
    SOURCE_PACKAGE = "Fuentes"

    RESTRICTION_TYPE_D_RIGHT_OF_WAY_ILICODE_VALUE = "Servidumbre.Transito"

    """
    LADM VARIABLES
    """
    LADM_COL_MODEL_KEY = "LADM_COL"
    SURVEY_MODEL_KEY = "Modelo_Aplicacion_LADMCOL_Lev_Cat"
    SURVEY_1_0_MODEL_KEY = "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0"
    SUPPLIES_MODEL_KEY = "Submodelo_Insumos_Gestor_Catastral"
    SNR_DATA_SUPPLIES_MODEL_KEY = "Submodelo_Insumos_SNR"
    SUPPLIES_INTEGRATION_MODEL_KEY = "Submodelo_Integracion_Insumos"
    CADASTRAL_CARTOGRAPHY_MODEL_KEY = "Submodelo_Cartografia_Catastral"
    VALUATION_MODEL_KEY = "Submodelo_Avaluos"
    ISO19107_MODEL_KEY = "ISO19107_PLANAS"
    CATALOG_OBJECTS_MODEL_KEY = "CatalogueObjects"
    QUALITY_ERROR_MODEL_KEY = "Errores_Calidad"
    FIELD_DATA_CAPTURE_MODEL_KEY = "Captura_Geo"

    FDC_TOPIC_NAME = "Captura_Geo"

    # TODO: Remove when LADM model version 3 is fully defined
    """
    VALUATION MAPPING
    """
    VALUATION_BUILDING_UNIT_TABLE = "av_unidad_construccion"
    VALUATION_COMPONENT_BUILDING = "av_componente_construccion"
    VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE = "av_calificacion_no_convencional"
    VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE = "av_calificacion_convencional"
    VALUATION_GROUP_QUALIFICATION = "av_grupo_calificacion"
    VALUATION_BUILDING_OBJECT = "av_objeto_construccion"
    VALUATION_GEOECONOMIC_ZONE_TABLE = "zona_homogenea_geoeconomica"
    VALUATION_PHYSICAL_ZONE_TABLE = "zona_homogenea_fisica"

    AVALUOUNIDADCONSTRUCCION_TABLE = "avaluounidadconstruccion"
    AVALUOUNIDADCONSTRUCCION_TABLE_BUILDING_UNIT_VALUATION_FIELD = "aucons"
    AVALUOUNIDADCONSTRUCCION_TABLE_BUILDING_UNIT_FIELD = "ucons"

    """
    Do not use the same before attribute for 2 differente groups. The same applies
    to after attribute.

    Leave before_attr/after_attr empty to add the group at the end of the form.
    """
    FORM_GROUPS = {
        VALUATION_BUILDING_UNIT_TABLE: {
            '': {
                'show_label': True,
                'column_count': 1,
                'attr_list': ['num_habitaciones', 'num_banios', 'num_cocinas', 'num_oficinas', 'num_estudios',
                              'num_bodegas', 'num_locales', 'num_salas', 'num_comedores'],
                'visibility_expression': None,
                'before_attr': None,
                'after_attr': None
            },
            ' ': {
                'show_label': True,
                'column_count': 1,
                'attr_list': ['anio_construction', 'uso', 'destino_econo', 'puntuacion', 'tipologia',
                              'estado_conservacion', 'construccion_tipo'],
                'visibility_expression': None,
                'before_attr': None,
                'after_attr': None
            },
        },
        VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE: {
            ' ': {
                'show_label': True,
                'column_count': 1,
                'attr_list': ['sub_total_estructura', 'sub_total_acabados', 'sub_total_banio', 'sub_total_cocina',
                              'total_residencial_y_comercial', 'total_industrial'],
                'visibility_expression': None,
                'before_attr': None,
                'after_attr': None
            },
            '  ': {
                'show_label': True,
                'column_count': 1,
                'attr_list': ['armazon', 'muros', 'cubierta', 'conservacion_estructura', 'fachada', 'cubrimiento_muros',
                              'piso', 'conservacion_acabados', 'tamanio_banio', 'enchape_banio', 'mobiliario_banio',
                              'conservacion_banio', 'tamanio_cocina', 'enchape_cocina', 'mobiliario_cocina',
                              'conservacion_cocina', 'cerchas'],
                'visibility_expression': None,
                'before_attr': ' ',
                'after_attr': None
            },
            '   ': {
                'show_label': True,
                'column_count': 1,
                'attr_list': ['puntos_armazon', 'puntos_muro', 'puntos_cubierta', 'puntos_estructura_conservacion',
                              'puntos_fachada', 'puntos_cubrimiento_muros', 'puntos_piso',
                              'puntos_conservacion_acabados',
                              'puntos_tamanio_banio', 'puntos_enchape_banio', 'puntos_mobiliario_banio',
                              'puntos_conservacion_banio', 'puntos_tamanio_cocina', 'puntos_enchape_cocina',
                              'puntos_mobiliario_cocina', 'puntos_conservacion_cocina', 'puntos_cerchas'],
                'visibility_expression': None,
                'before_attr': '  ',
                'after_attr': None
            }
        }
    }
