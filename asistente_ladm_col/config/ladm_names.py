from PyQt5.QtCore import QCoreApplication, Qt

from asistente_ladm_col.utils.singleton import Singleton


class LADMNames(metaclass=Singleton):
    """
    Singleton to handle domain values ('which are not dependent on the database engine') a single point of access.
    """
    LC_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V = "Persona_Natural"
    LC_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V = "Persona_Juridica"
    LC_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V = "NIT"
    LC_RIGHT_TYPE_D_ILICODE_F_OWNERSHIP_V = "Dominio"

    TABLE_PROP_ASSOCIATION = "ASSOCIATION"
    TABLE_PROP_DOMAIN = "ENUM"
    TABLE_PROP_STRUCTURE = "STRUCTURE"

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

    RESTRICTION_TYPE_D_RIGHT_OF_WAY_ILICODE_VALUE = "Servidumbre"

    """
    LADM VARIABLES
    """
    LADM_MODEL_PREFIX = "LADM_COL"
    SNR_DATA_MODEL_PREFIX = "Submodelo_Insumos_SNR"
    SUPPLIES_MODEL_PREFIX = "Submodelo_Insumos_Gestor_Catastral"
    SUPPLIES_INTEGRATION_MODEL_PREFIX = "Submodelo_Integracion_Insumos"
    SURVEY_MODEL_PREFIX = "Modelo_Aplicacion_LADMCOL_Lev_Cat"
    ANT_MODEL_PREFIX = "ANT"
    CADASTRAL_CARTOGRAPHY_PREFIX = "Submodelo_Cartografia_Catastral"
    VALUATION_MODEL_PREFIX = "Sumodelo_Avaluos"

    """
    MODELS SUPPORTED IN LADM
    """
    # From this version on the plugin will work, a message will block prior versions
    LATEST_SURVEY_MODEL_VERSION_SUPPORTED = "1.0"
    LATEST_LADM_MODEL_VERSION_SUPPORTED = "3.0"
    VERSION_EXTENDED_MODELS = LATEST_SURVEY_MODEL_VERSION_SUPPORTED.replace('.', '_')
    VERSION_LADM_MODEL = LATEST_LADM_MODEL_VERSION_SUPPORTED.replace('.', '_')

    ISO_CARTESIAN_COORDINATES = 'ISO19107_PLANAS'

    SUPPORTED_MODEL_VERSIONS = {
        SURVEY_MODEL_PREFIX: LATEST_SURVEY_MODEL_VERSION_SUPPORTED,
        VALUATION_MODEL_PREFIX: LATEST_SURVEY_MODEL_VERSION_SUPPORTED,
        LADM_MODEL_PREFIX: LATEST_LADM_MODEL_VERSION_SUPPORTED,
        ANT_MODEL_PREFIX: LATEST_SURVEY_MODEL_VERSION_SUPPORTED,
        CADASTRAL_CARTOGRAPHY_PREFIX: LATEST_SURVEY_MODEL_VERSION_SUPPORTED,
        SNR_DATA_MODEL_PREFIX: LATEST_SURVEY_MODEL_VERSION_SUPPORTED,
        SUPPLIES_INTEGRATION_MODEL_PREFIX: LATEST_SURVEY_MODEL_VERSION_SUPPORTED,
        SUPPLIES_MODEL_PREFIX: LATEST_SURVEY_MODEL_VERSION_SUPPORTED
    }

    SUPPORTED_ISO_CARTESIAN_COORDINATES = "{}_V{}".format(ISO_CARTESIAN_COORDINATES, VERSION_LADM_MODEL)
    SUPPORTED_LADM_MODEL = "{}_V{}".format(LADM_MODEL_PREFIX, VERSION_LADM_MODEL)
    SUPPORTED_SNR_DATA_MODEL = "{}_V{}".format(SNR_DATA_MODEL_PREFIX, VERSION_EXTENDED_MODELS)
    SUPPORTED_SUPPLIES_MODEL = "{}_V{}".format(SUPPLIES_MODEL_PREFIX, VERSION_EXTENDED_MODELS)
    SUPPORTED_SUPPLIES_INTEGRATION_MODEL = "{}_V{}".format(SUPPLIES_INTEGRATION_MODEL_PREFIX, VERSION_EXTENDED_MODELS)
    SUPPORTED_SURVEY_MODEL = "{}_V{}".format(SURVEY_MODEL_PREFIX, VERSION_EXTENDED_MODELS)
    SUPPORTED_ANT_MODEL = "{}_V{}".format(ANT_MODEL_PREFIX, VERSION_EXTENDED_MODELS)
    SUPPORTED_CADASTRAL_CARTOGRAPHY = "{}_V{}".format(CADASTRAL_CARTOGRAPHY_PREFIX, VERSION_EXTENDED_MODELS)
    SUPPORTED_VALUATION_MODEL = "{}_V{}".format(VALUATION_MODEL_PREFIX, VERSION_EXTENDED_MODELS)

    DEFAULT_HIDDEN_MODELS = [SUPPORTED_LADM_MODEL, SUPPORTED_ISO_CARTESIAN_COORDINATES]

    ALIAS_FOR_ASSISTANT_SUPPORTED_MODEL = {
        LADM_MODEL_PREFIX: QCoreApplication.translate("TranslatableConfigStrings", "LADM COL"),
        SNR_DATA_MODEL_PREFIX: QCoreApplication.translate("TranslatableConfigStrings", "SNR data"),
        SUPPLIES_MODEL_PREFIX: QCoreApplication.translate("TranslatableConfigStrings", "Supplies"),
        SUPPLIES_INTEGRATION_MODEL_PREFIX: QCoreApplication.translate("TranslatableConfigStrings",
                                                                      "Supplies integration data"),
        SURVEY_MODEL_PREFIX: QCoreApplication.translate("TranslatableConfigStrings", "Survey"),
        ANT_MODEL_PREFIX: QCoreApplication.translate("TranslatableConfigStrings", "ANT"),
        CADASTRAL_CARTOGRAPHY_PREFIX: QCoreApplication.translate("TranslatableConfigStrings", "Reference cadastral cartography"),
        VALUATION_MODEL_PREFIX: QCoreApplication.translate("TranslatableConfigStrings", "Valuation")
    }

    SUPPORTED_MODELS = [SUPPORTED_LADM_MODEL,
                        SUPPORTED_SNR_DATA_MODEL,
                        SUPPORTED_SUPPLIES_MODEL,
                        SUPPORTED_SUPPLIES_INTEGRATION_MODEL,
                        SUPPORTED_SURVEY_MODEL,
                        SUPPORTED_ANT_MODEL,
                        SUPPORTED_CADASTRAL_CARTOGRAPHY,
                        SUPPORTED_VALUATION_MODEL]

    DEFAULT_MODEL_NAMES_CHECKED = {
        # SUPPORTED_ANT_MODEL: Qt.Unchecked,  #TODO: Disable until get last movel version
        SUPPORTED_VALUATION_MODEL: Qt.Unchecked,
        SUPPORTED_CADASTRAL_CARTOGRAPHY: Qt.Unchecked,
        SUPPORTED_SUPPLIES_MODEL: Qt.Unchecked,
        SUPPORTED_SUPPLIES_INTEGRATION_MODEL: Qt.Unchecked,
        SUPPORTED_SNR_DATA_MODEL: Qt.Unchecked,
        SUPPORTED_SURVEY_MODEL: Qt.Checked
    }

    DEFAULT_INHERITANCE = 'smart2'
    # Settings to create schema according to LADM-COL
    CREATE_BASKET_COL = False
    CREATE_IMPORT_TID = False
    STROKE_ARCS = True

    # For testing if an schema comes from ili2db
    INTERLIS_TEST_METADATA_TABLE_PG = 't_ili2db_table_prop'

    # TODO: Remove when LADM model version 3 is fully defined

    """
    UNIQUE CADASTRAL FORM
    """
    UNIQUE_CADASTRAL_FORM_TABLE = "fcm_formulario_unico_cm"
    UNIQUE_CADASTRAL_FORM_CONTACT_VISIT_TABLE = "fcm_contacto_visita"

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