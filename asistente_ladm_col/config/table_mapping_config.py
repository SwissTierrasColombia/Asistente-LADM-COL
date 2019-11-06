from qgis.core import NULL

TABLE_NAME = 'table_name'
VARIABLE_NAME = 'variable'
FIELDS_DICT = 'fields_dict'
T_ID = 't_id'
DESCRIPTION = 'description'
ILICODE = 'ilicode'
DISPLAY_NAME = 'display_name'


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Names(metaclass=Singleton):
    """
    Singleton to handle table and field names in a single point of access.
    Note: Names are dynamic because different DB engines handle different names, and because even in a single DB engine,
          one could shorten table and field names via ili2db.
    """

    ############################################ TABLE VARIABLES ###########################################################
    T_ID_F = None
    ILICODE_F = None
    DESCRIPTION_F = None
    DISPLAY_NAME_F = None

    GC_NEIGHBOURHOOD_T = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Barrio"
    GC_BUILDING_T = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Construccion"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.gc_construccion_predio"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.gc_construccion_unidad"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.gc_copropiedad"
    GC_HP_CONDOMINIUM_DATA_T = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio"
    GC_BLOCK_T = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Manzana"
    GC_PERIMETER_T = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Perimetro"
    GC_HP_PARCEL_T = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.gc_ph_predio"
    GC_PARCEL_T = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Predio_Catastro"
    GC_OWNER_T = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Propietaio"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.gc_propietario_predio"
    GC_RURAL_SECTOR_T = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Sector_Rural"
    GC_URBAN_SECTOR_T = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Sector_Urbano"
    GC_PLOT_T = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Terreno"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.gc_terreno_predio"
    GC_BUILDING_UNIT_T = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Unidad_Construccion"
    GC_RURAL_DIVISION_T = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Vereda"
    GC_PARCEL_TYPE_D = None  # "Datos_Gestor_Catastral_V2_9_5.GC_CondicionPredioTipo"
    GC_ADDRESS_T = None  # "Datos_Gestor_Catastral_V2_9_5.GC_Direccion"
    # "Datos_Gestor_Catastral_V2_9_5.GC_SistemaProcedenciaDatosTipo"
    GC_BUILDING_UNIT_TYPE_T = None  # "Datos_Gestor_Catastral_V2_9_5.GC_UnidadConstruccionTipo"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Construccion"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Terreno"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion"

    INI_PARCEL_SUPPLIES_T = None  # "Datos_Integracion_Insumos_V2_9_5.Datos_Integracion_Insumos.INI_Predio_Insumos"
    # "Datos_Integracion_Insumos_V2_9_5.Datos_Integracion_Insumos.ini_predio_integracion_gc"
    # "Datos_Integracion_Insumos_V2_9_5.Datos_Integracion_Insumos.ini_predio_integracion_snr"

    SNR_RIGHT_T = None  # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Derecho"
    # "Datos_SNR_V2_9_5.Datos_SNR.snr_derecho_predio"
    # "Datos_SNR_V2_9_5.Datos_SNR.snr_fuente_cabidalinderos"
    SNR_SOURCE_BOUNDARIES_T = None  # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Fuente_CabidaLinderos"
    # "Datos_SNR_V2_9_5.Datos_SNR.snr_fuente_derecho"
    SNR_SOURCE_RIGHT_T = None  # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Fuente_Derecho"
    SNR_PARCEL_REGISTRY_T = None  # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Predio_Registro"
    SNR_TITLE_HOLDER_T = None  # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Titular"
    # "Datos_SNR_V2_9_5.Datos_SNR.snr_titular_derecho"
    SNR_RIGHT_TYPE_D = None  # "Datos_SNR_V2_9_5.SNR_CalidadDerechoTipo"
    SNR_TITLE_HOLDER_DOCUMENT_T = None  # "Datos_SNR_V2_9_5.SNR_DocumentoTitularTipo"
    SNR_SOURCE_TYPE_D = None  # "Datos_SNR_V2_9_5.SNR_FuenteTipo"
    SNR_TITLE_HOLDER_TYPE_D = None  # "Datos_SNR_V2_9_5.SNR_PersonaTitularTipo"

    # "LADM_COL_V1_2.LADM_Nucleo.col_baunitComoInteresado"
    COL_BAUNIT_SOURCE_T = None  # "LADM_COL_V1_2.LADM_Nucleo.col_baunitFuente"
    COL_CCL_SOURCE_T = None # "LADM_COL_V1_2.LADM_Nucleo.col_cclFuente"
    # "LADM_COL_V1_2.LADM_Nucleo.CC_MetodoOperacion"
    #
    # "LADM_COL_V1_2.LADM_Nucleo.CI_CodigoTarea"
    # "LADM_COL_V1_2.LADM_Nucleo.CI_Contacto"
    # "LADM_COL_V1_2.LADM_Nucleo.CI_Forma_Presentacion_Codigo"
    # "LADM_COL_V1_2.LADM_Nucleo.CI_ParteResponsable"
    #
    # "LADM_COL_V1_2.LADM_Nucleo.col_clFuente"

    # "LADM_COL_V1_2.LADM_Nucleo.COL_AgrupacionUnidadesEspaciales"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_AreaTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_AreaValor"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_CarasLindero"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_ContenidoNivelTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_EspacioJuridicoRedServicios"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_EspacioJuridicoUnidadEdificacion"
    COL_AVAILABILITY_TYPE_D = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_EstadoDisponibilidadTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_EstructuraTipo"
    COL_ADMINISTRATIVE_SOURCE_T = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_FuenteAdministrativa"
    COL_ADMINISTRATIVE_SOURCE_TYPE_D = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_FuenteAdministrativaTipo"
    COL_SPATIAL_SOURCE_T = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_FuenteEspacial"
    COL_SPATIAL_SOURCE_TYPE_D = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_FuenteEspacialTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_FuncionInteresadoTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_FuncionInteresadoTipo_"
    COL_INTERPOLATION_TYPE_D = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_InterpolacionTipo"
    COL_PRODUCTION_METHOD = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_MetodoProduccionTipo"
    COL_MONUMENTATION_TYPE_D = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_MonumentacionTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Nivel"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_RedServiciosTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEdificacionTipo"

    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Metodo_Evaluacion_Codigo_Tipo"

    EXT_ARCHIVE_S = None  # "LADM_COL_V1_2.LADM_Nucleo.ExtArchivo"
    EXT_ADDRESS_S = None  # "LADM_COL_V1_2.LADM_Nucleo.ExtDireccion"
    EXT_PARTY_S = None  # "LADM_COL_V1_2.LADM_Nucleo.ExtInteresado"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtRedServiciosFisica"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtUnidadEdificacionFisica"
    FRACTION_S = None  # "LADM_COL_V1_2.LADM_Nucleo.Fraccion"
    # "LADM_COL_V1_2.LADM_Nucleo.Imagen"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_ISO19125_Tipo"

    COL_GROUP_PARTY_TYPE_D = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_GrupoInteresadoTipo"
    COL_BAUNIT_TYPE_D = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_BAUnitTipo"

    COL_DIMENSION_TYPE_D = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_DimensionTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_EstadoRedServiciosTipo"
    COL_POINT_TYPE_D = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_PuntoTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_RegistroTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_RelacionNecesariaBAUnits"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_RelacionNecesariaUnidadesEspaciales"
    COL_SURFACE_RELATION_TYPE_D = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_RelacionSuperficieTipo"
    OP_RESTRICTION_TYPE_D = None  # "Operacion_V2_9_6.OP_RestriccionTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Transformacion"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_VolumenTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_VolumenValor"
    MORE_BFS_T = None  # "LADM_COL_V1_2.LADM_Nucleo.col_masCcl"
    # "LADM_COL_V1_2.LADM_Nucleo.col_masCl"
    LESS_BFS_T = None  # "LADM_COL_V1_2.LADM_Nucleo.col_menosCcl"
    # "LADM_COL_V1_2.LADM_Nucleo.col_menosCl"
    MEMBERS_T = None  # "LADM_COL_V1_2.LADM_Nucleo.col_miembros"
    OM_OBSERVATION_T = None  # "LADM_COL_V1_2.LADM_Nucleo.OM_Observacion"
    POINT_BFS_T = None  # "LADM_COL_V1_2.LADM_Nucleo.col_puntoCcl"
    # "LADM_COL_V1_2.LADM_Nucleo.col_puntoCl"
    COL_POINT_SOURCE_T = None # "LADM_COL_V1_2.LADM_Nucleo.col_puntoFuente"
    # "LADM_COL_V1_2.LADM_Nucleo.col_puntoReferencia"
    # "LADM_COL_V1_2.LADM_Nucleo.col_relacionFuente"
    # "LADM_COL_V1_2.LADM_Nucleo.col_relacionFuenteUespacial"
    # "LADM_COL_V1_2.LADM_Nucleo.col_responsableFuente"
    COL_RRR_SOURCE_T = None  # "LADM_COL_V1_2.LADM_Nucleo.col_rrrFuente"
    # "LADM_COL_V1_2.LADM_Nucleo.col_topografoFuente"
    COL_UE_BAUNIT_T = None  # "LADM_COL_V1_2.LADM_Nucleo.col_ueBaunit"
    COL_UE_SOURCE_T = None  # "LADM_COL_V1_2.LADM_Nucleo.col_ueFuente"
    # "LADM_COL_V1_2.LADM_Nucleo.col_ueJerarquiaGrupo"
    # "LADM_COL_V1_2.LADM_Nucleo.col_ueNivel"
    # "LADM_COL_V1_2.LADM_Nucleo.col_ueUeGrupo"
    # "LADM_COL_V1_2.LADM_Nucleo.col_unidadFuente"
    OP_AGREEMENT_TYPE_D = None  # "Operacion_V2_9_5.OP_AcuerdoTipo"
    OP_PARCEL_TYPE_T = None  # "Operacion_V2_9_5.OP_CondicionPredioTipo"
    OP_RIGHT_TYPE_D = None  # "Operacion_V2_9_5.OP_DerechoTipo"
    OP_GROUP_PARTY_T = None  # "Operacion_V2_9_6.Operacion.OP_Agrupacion_Interesados"
    OP_BUILDING_T = None  # "Operacion_V2_9_5.Operacion.OP_Construccion"
    # "Operacion_V2_9_5.Operacion.op_construccion_unidadconstruccion"
    OP_RIGHT_T = None  # "Operacion_V2_9_5.Operacion.OP_Derecho"
    OP_ADMINISTRATIVE_SOURCE_T = None  # "Operacion_V2_9_5.Operacion.OP_FuenteAdministrativa"
    OP_SPATIAL_SOURCE_T = None  # "Operacion_V2_9_5.Operacion.OP_FuenteEspacial"
    OP_PARTY_T = None  # "Operacion_V2_9_5.Operacion.OP_Interesado"
    # "Operacion_V2_9_5.Operacion.op_interesado_contacto"
    # "Operacion_V2_9_5.Operacion.OP_Interesado_Contacto"
    OP_BOUNDARY_T = None  # "Operacion_V2_9_5.Operacion.OP_Lindero"
    OP_PARCEL_T = None  # "Operacion_V2_9_5.Operacion.OP_Predio"
    OP_COPROPERTY_T = None  # "Operacion_V2_9_5.Operacion.op_predio_copropiedad"
    OP_OPERATION_SUPPLIES_T = None  # "Operacion_V2_9_5.Operacion.op_predio_insumos_operacion"
    OP_CONTROL_POINT_T = None  # "Operacion_V2_9_5.Operacion.OP_PuntoControl"
    OP_SURVEY_POINT_T = None  # "Operacion_V2_9_5.Operacion.OP_PuntoLevantamiento"
    OP_BOUNDARY_POINT_T = None  # "Operacion_V2_9_5.Operacion.OP_PuntoLindero"
    OP_RESTRICTION_T = None  # "Operacion_V2_9_5.Operacion.OP_Restriccion"
    OP_RIGHT_OF_WAY_T = None  # "Operacion_V2_9_5.Operacion.OP_ServidumbrePaso"
    OP_PLOT_T = None  # "Operacion_V2_9_5.Operacion.OP_Terreno"
    OP_BUILDING_UNIT_T = None  # "Operacion_V2_9_5.Operacion.OP_UnidadConstruccion"
    OP_PHOTO_IDENTIFICATION_TYPE_D = None  # "Operacion_V2_9_5.OP_FotoidentificacionTipo"
    OP_ADMINISTRATIVE_SOURCE_TYPE_D = None  # "Operacion_V2_9_5.OP_FuenteAdministrativaTipo"
    OP_ETHNIC_GROUP_TYPE = None  # "Operacion_V2_9_5.OP_GrupoEtnicoTipo"
    # "Operacion_V2_9_5.OP_InstitucionTipo"
    OP_PARTY_DOCUMENT_TYPE_D = None  # "Operacion_V2_9_5.OP_InteresadoDocumentoTipo"
    OP_PARTY_TYPE_D = None  # "Operacion_V2_9_5.OP_InteresadoTipo"
    OP_PARCEL_TYPE_D = None  # "Operacion_V2_9_5.OP_PredioTipo"
    OP_CONTROL_POINT_TYPE_D = None  # "Operacion_V2_9_5.OP_PuntoControlTipo"
    OP_SURVEY_POINT_TYPE_D = None  # "Operacion_V2_9_5.OP_PuntoLevTipo"
    OP_POINT_TYPE_D = None  # "Operacion_V2_9_5.OP_PuntoTipo"
    OP_GENRE_D = None  # "Operacion_V2_9_5.OP_SexoTipo"
    OP_LOCATION_POINT_TYPE_D = None  # "Operacion_V2_9_5.OP_UbicacionPuntoTipo"
    # "Operacion_V2_9_5.OP_UsoUConsTipo"
    # "Operacion_V2_9_5.OP_ViaTipo"

    ############################################ FIELD VARIABLES ###########################################################

    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Barrio.Codigo"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Barrio.Geometria"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Barrio.Nombre"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Barrio.Sector_Codigo"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Construccion.Area_Construida"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Construccion.Codigo_Edificacion"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Construccion.Codigo_Terreno"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Construccion.Etiqueta"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Construccion.Geometria"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Construccion.Identificador"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Construccion.Numero_Mezanines"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Construccion.Numero_Pisos"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Construccion.Numero_Semisotanos"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Construccion.Numero_Sotanos"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.gc_construccion_predio.gc_predio"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Construccion.Tipo_Construccion"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Construccion.Tipo_Dominio"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.gc_construccion_unidad.gc_construccion"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.gc_copropiedad.Coeficiente_Copropiedad"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.gc_copropiedad.gc_matriz"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.gc_copropiedad.gc_unidad"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Area_Total_Construida"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Area_Total_Construida_Comun"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Area_Total_Construida_Privada"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Area_Total_Terreno"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Area_Total_Terreno_Comun"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Area_Total_Terreno_Privada"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Torre_No"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Total_Pisos_Torre"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Total_Sotanos"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Total_Unidades_Privadas"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Total_Unidades_Sotano"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Manzana.Barrio_Codigo"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Manzana.Codigo"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Manzana.Codigo_Anterior"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Manzana.Geometria"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Perimetro.Codigo_Nombre"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Perimetro.Departamento_Codigo"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Perimetro.Geometria"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Perimetro.Municipio_Codigo"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Perimetro.Nombre_Geografico"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Perimetro.Tipo_Avaluo"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.gc_ph_predio.gc_predio"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Predio_Catastro.Circulo_Registral"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Predio_Catastro.Condicion_Predio"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Predio_Catastro.Destinacion_Economica"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Predio_Catastro.Direcciones"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Predio_Catastro.Fecha_Datos"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Predio_Catastro.Matricula_Inmobiliaria_Catastro"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Predio_Catastro.Numero_Predial"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Predio_Catastro.Numero_Predial_Anterior"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Predio_Catastro.Sistema_Procedencia_Datos"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Predio_Catastro.Tipo_Catastro"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Predio_Catastro.Tipo_Predio"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Propietario.Digito_Verificacion"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Propietario.Numero_Documento"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.gc_propietario_predio.gc_predio_catastro"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Propietario.Primer_Apellido"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Propietario.Primer_Nombre"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Propietario.Razon_Social"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Propietario.Segundo_Apellido"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Propietario.Segundo_Nombre"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Propietario.Tipo_Documento"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Sector_Rural.Codigo"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Sector_Rural.Geometria"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Sector_Urbano.Codigo"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Sector_Urbano.Geometria"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Alfanumerica"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Digital"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Terreno.Geometria"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Terreno.Manzana_Vereda_Codigo"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Terreno.Numero_Subterraneos"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.gc_terreno_predio.gc_predio"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Unidad_Construccion.Anio"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Unidad_Construccion.Area_Construida"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Unidad_Construccion.Area_Privada"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Unidad_Construccion.Codigo_Terreno"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Unidad_Construccion.Etiqueta"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Unidad_Construccion.Geometria"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Unidad_Construccion.Identificador"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Unidad_Construccion.Planta"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Unidad_Construccion.Puntaje"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Unidad_Construccion.Tipo_Construccion"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Unidad_Construccion.Tipo_Dominio"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Unidad_Construccion.Total_Banios"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Unidad_Construccion.Total_Habitaciones"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Unidad_Construccion.Total_Locales"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Unidad_Construccion.Total_Pisos"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Unidad_Construccion.Uso"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Vereda.Codigo"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Vereda.Codigo_Anterior"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Vereda.Geometria"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Vereda.Nombre"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Vereda.Sector_Codigo"
    # "Datos_Gestor_Catastral_V2_9_5.GC_Direccion.Geometria_Referencia"
    # "Datos_Gestor_Catastral_V2_9_5.GC_Direccion.Principal"
    # "Datos_Gestor_Catastral_V2_9_5.GC_Direccion.Valor"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Construccion.Area_Construida"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Construccion.Codigo_Edificacion"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Construccion.Codigo_Terreno"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Construccion.Etiqueta"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Construccion.Geometria"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Construccion.Identificador"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Construccion.Numero_Mezanines"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Construccion.Numero_Pisos"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Construccion.Numero_Semisotanos"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Construccion.Tipo_Construccion"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Construccion.Tipo_Dominio"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Terreno.Area_Terreno_Alfanumerica"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Terreno.Area_Terreno_Digital"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Terreno.Geometria"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Terreno.Manzana_Vereda_Codigo"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Terreno.Numero_Subterraneos"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion.Anio"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion.Area_Construida"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion.Area_Privada"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion.Codigo_Terreno"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion.Etiqueta"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion.Geometria"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion.Identificador"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion.Planta"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion.Puntaje"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion.Tipo_Construccion"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion.Tipo_Dominio"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion.Total_Banios"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion.Total_Habitaciones"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion.Total_Locales"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion.Total_Pisos"
    # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion.Uso"
    #
    #
    #
    # "Datos_Integracion_Insumos_V2_9_5.Datos_Integracion_Insumos.ini_predio_integracion_gc.gc_predio_catastro"
    # "Datos_Integracion_Insumos_V2_9_5.Datos_Integracion_Insumos.ini_predio_integracion_snr.snr_predio_juridico"
    #
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Derecho.Calidad_Derecho_Registro"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Derecho.Codigo_Naturaleza_Juridica"
    # "Datos_SNR_V2_9_5.Datos_SNR.snr_derecho_predio.snr_predio_registro"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Fuente_CabidaLinderos.Archivo"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Fuente_CabidaLinderos.Ciudad_Emisora"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Fuente_CabidaLinderos.Ente_Emisor"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Fuente_CabidaLinderos.Fecha_Documento"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Fuente_CabidaLinderos.Numero_Documento"
    # "Datos_SNR_V2_9_5.Datos_SNR.snr_fuente_cabidalinderos.snr_fuente_cabidalinderos"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Fuente_CabidaLinderos.Tipo_Documento"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Fuente_Derecho.Ciudad_Emisora"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Fuente_Derecho.Ente_Emisor"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Fuente_Derecho.Fecha_Documento"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Fuente_Derecho.Numero_Documento"
    # "Datos_SNR_V2_9_5.Datos_SNR.snr_fuente_derecho.snr_fuente_derecho"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Fuente_Derecho.Tipo_Documento"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Predio_Registro.Cabida_Linderos"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Predio_Registro.Codigo_ORIP"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Predio_Registro.Fecha_Datos"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Predio_Registro.Matricula_Inmobiliaria"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Predio_Registro.Matricula_Inmobiliaria_Matriz"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Predio_Registro.Numero_Predial_Anterior_en_FMI"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Predio_Registro.Numero_Predial_Nuevo_en_FMI"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Predio_Registro.NUPRE_en_FMI"
    # "Datos_SNR_V2_9_5.Datos_SNR.snr_titular_derecho.Porcentaje_Participacion"
    # "Datos_SNR_V2_9_5.Datos_SNR.snr_titular_derecho.snr_derecho"
    # "Datos_SNR_V2_9_5.Datos_SNR.snr_titular_derecho.snr_titular"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Titular.Nombres"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Titular.Numero_Documento"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Titular.Primer_Apellido"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Titular.Razon_Social"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Titular.Segundo_Apellido"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Titular.Tipo_Documento"
    # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Titular.Tipo_Persona"
    #
    # "LADM_COL_V1_2.LADM_Nucleo.col_baunitComoInteresado.interesado"
    # "LADM_COL_V1_2.LADM_Nucleo.col_baunitComoInteresado.unidad"
    BAUNIT_SOURCE_T_SOURCE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.col_baunitFuente.bfuente"
    BAUNIT_SOURCE_T_UNIT_F = None  # "LADM_COL_V1_2.LADM_Nucleo.col_baunitFuente.unidad"
    COL_BAUNIT_RRR_T_UNIT_F = None  # "LADM_COL_V1_2.LADM_Nucleo.col_baunitRrr.unidad"
    COL_CCL_SOURCE_T_BOUNDARY_F = None # "LADM_COL_V1_2.LADM_Nucleo.col_cclFuente.ccl"
                                       # "LADM_COL.LADM_Nucleo.col_cclFuente.ccl_Operacion.Operacion.OP_Lindero" --> ccl_op_lindero
    COL_CCL_SOURCE_T_SOURCE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.col_cclFuente.fuente_espacial"
    # "LADM_COL_V1_2.LADM_Nucleo.CC_MetodoOperacion.Ddimensiones_Objetivo"
    # "LADM_COL_V1_2.LADM_Nucleo.CC_MetodoOperacion.Dimensiones_Origen"
    # "LADM_COL_V1_2.LADM_Nucleo.CC_MetodoOperacion.Formula"
    # "LADM_COL_V1_2.LADM_Nucleo.CI_Contacto.Direccion"
    # "LADM_COL_V1_2.LADM_Nucleo.CI_Contacto.Fuente_En_Linea"
    # "LADM_COL_V1_2.LADM_Nucleo.CI_Contacto.Horario_De_Atencion"
    # "LADM_COL_V1_2.LADM_Nucleo.CI_Contacto.Instrucciones_Contacto"
    # "LADM_COL_V1_2.LADM_Nucleo.CI_Contacto.Telefono"
    # "LADM_COL_V1_2.LADM_Nucleo.CI_ParteResponsable.Funcion"
    # "LADM_COL_V1_2.LADM_Nucleo.CI_ParteResponsable.Informacion_Contacto"
    # "LADM_COL_V1_2.LADM_Nucleo.CI_ParteResponsable.Nombre_Individual"
    # "LADM_COL_V1_2.LADM_Nucleo.CI_ParteResponsable.Nombre_Organizacion"
    # "LADM_COL_V1_2.LADM_Nucleo.CI_ParteResponsable.Posicion"
    # "LADM_COL_V1_2.LADM_Nucleo.col_clFuente.fuente_espacial"
    COL_GROUP_PARTY_T_TYPE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Agrupacion_Interesados.Tipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_AreaValor.areaSize"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_AreaValor.type"
    COL_BAUNIT_T_NAME_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_BAUnit.Nombre"
    COL_BAUNIT_T_NAMESPACE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_BAUnit.Espacio_De_Nombres"
    COL_BAUNIT_T_LOCAL_ID_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_BAUnit.Local_Id"
    COL_BFS_T_NAMESPACE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_CadenaCarasLimite.Espacio_De_Nombres"
    COL_BFS_T_LOCAL_ID_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_CadenaCarasLimite.Local_Id"
    COL_BFS_T_GEOMETRY_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_CadenaCarasLimite.Geometria"
    COL_BFS_T_TEXTUAL_LOCATION_F = None  # "LADM_COL.LADM_Nucleo.COL_CadenaCarasLimite.Localizacion_Textual"
    COL_ADMINISTRATIVE_SOURCE_T_SOURCE_NUMBER_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_FuenteAdministrativa.Numero_Fuente"
    COL_ADMINISTRATIVE_SOURCE_T_OBSERVATION_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_FuenteAdministrativa.Observacion"
    COL_SPATIAL_SOURCE_T_MEASUREMENTS_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_FuenteEspacial.Mediciones"
    COL_SPATIAL_SOURCE_T_TYPE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_FuenteEspacial.Tipo"
    # COL_SOURCE_T_QUALITY_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Calidad"
    COL_SOURCE_T_AVAILABILITY_STATUS_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Estado_Disponibilidad"
    COL_SOURCE_T_EXT_ARCHIVE_ID_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID"
    COL_SOURCE_T_DATE_DOCUMENT_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Fecha_Documento_Fuente"
    COL_SOURCE_T_OFFICIAL_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Oficialidad"
    # COL_SOURCE_T_PROVENANCE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Procedencia"
    COL_SOURCE_T_NAMESPACE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Espacio_De_Nombres"
    COL_SOURCE_T_LOCAL_ID_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Local_Id"
    COL_SOURCE_T_MAIN_TYPE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Tipo_Principal"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_FuncionInteresadoTipo_.value"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Interesado.ext_PID"
    COL_PARTY_T_NAME_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Interesado.Nombre"
    COL_PARTY_T_NAMESPACE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Interesado.Espacio_De_Nombres"
    COL_PARTY_T_LOCAL_ID_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Interesado.Local_Id"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Interesado.Tarea"
    COL_POINT_T_ORIGINAL_LOCATION_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Geometria"
    COL_POINT_T_PRODUCTION_METHOD_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.MetodoProduccion"
    COL_POINT_T_MONUMENTATION_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Monumentacion"
    COL_POINT_T_NAMESPACE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Espacio_De_Nombres"
    COL_POINT_T_LOCAL_ID_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Local_Id"
    COL_POINT_T_INTERPOLATION_POSITION_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Posicion_Interpolacion"
    # COL_POINT_T_TRANSFORMATION_AND_RESULT_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Transformacion_Y_Resultado"
    COL_RRR_T_SHARE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_RRR.Compartido"
    COL_RRR_T_SHARE_CHECK_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_RRR.Comprobacion_Comparte"
    COL_RRR_T_DESCRIPTION_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_RRR.Descripcion"
    COL_RRR_T_NAMESPACE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_RRR.Espacio_De_Nombres"
    COL_RRR_T_LOCAL_ID_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_RRR.Local_Id"
    COL_RRR_T_EFFECTIVE_USAGE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_RRR.Uso_Efectivo"

    # COL_SPATIAL_UNIT_T_AREA_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Area"
    COL_SPATIAL_UNIT_T_DIMENSION_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Dimension"
    COL_SPATIAL_UNIT_T_LABEL_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Etiqueta"
    # COL_SPATIAL_UNIT_T_EXT_ADDRESS_ID_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID"
    COL_SPATIAL_UNIT_T_GEOMETRY_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Geometria"
    COL_SPATIAL_UNIT_T_SURFACE_RELATION_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie"
    COL_SPATIAL_UNIT_T_NAMESPACE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Espacio_De_Nombres"
    COL_SPATIAL_UNIT_T_LOCAL_ID_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Local_Id"
    # COL_SPATIAL_UNIT_T_VOLUME_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Volumen"

    EXT_ARCHIVE_S_DATA_F = None  # "LADM_COL_V1_2.LADM_Nucleo.ExtArchivo.Datos"
    EXT_ARCHIVE_S_EXTRACTION_F = None  # "LADM_COL_V1_2.LADM_Nucleo.ExtArchivo.Extraccion"
    EXT_ARCHIVE_S_ACCEPTANCE_DATE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.ExtArchivo.Fecha_Aceptacion"
    EXT_ARCHIVE_S_DELIVERY_DATE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.ExtArchivo.Fecha_Entrega"
    EXT_ARCHIVE_S_STORAGE_DATE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.ExtArchivo.Fecha_Grabacion"
    EXT_ARCHIVE_S_NAMESPACE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.ExtArchivo.Espacio_De_Nombres"
    EXT_ARCHIVE_S_LOCAL_ID_F = None  # "LADM_COL_V1_2.LADM_Nucleo.ExtArchivo.Local_Id"
    EXT_ADDRESS_S_VALUE_MAIN_ROAD_F = None  # "LADM_COL.LADM_Nucleo.ExtDireccion.Valor_Via_Principal"
    EXT_ADDRESS_S_PARCEL_NUMBER_F = None  # "LADM_COL.LADM_Nucleo.ExtDireccion.Numero_Predio"
    EXT_ADDRESS_S_LOCALIZATION_F = None  # "LADM_COL.LADM_Nucleo.ExtDireccion.Localizacion"
    EXT_ADDRESS_S_MAIN_ROAD_CLASS_F = None  # "LADM_COL.LADM_Nucleo.ExtDireccion.Clase_Via_Principal"
    EXT_ADDRESS_S_PARCEL_SECTOR_F = None  # "LADM_COL.LADM_Nucleo.ExtDireccion.Sector_Predio"
    EXT_ADDRESS_S_PARCEL_NAME_F = None  # "LADM_COL.LADM_Nucleo.ExtDireccion.Nombre_Predio"
    EXT_ADDRESS_S_IS_MAIN_ADDRESS_F = None  # "LADM_COL.LADM_Nucleo.ExtDireccion.Es_Direccion_Principal"
    EXT_ADDRESS_S_LETTER_GENERATOR_ROAD_F = None  # "LADM_COL.LADM_Nucleo.ExtDireccion.Letra_Via_Generadora"
    EXT_ADDRESS_S_VALUE_GENERATOR_ROAD_F = None  # "LADM_COL.LADM_Nucleo.ExtDireccion.Valor_Via_Generadora"
    EXT_ADDRESS_S_LETTER_MAIN_ROAD_F = None  # "LADM_COL.LADM_Nucleo.ExtDireccion.Letra_Via_Principal"
    EXT_ADDRESS_S_ADDRESS_TYPE_F = None  # "LADM_COL.LADM_Nucleo.ExtDireccion.Tipo_Direccion"
    EXT_ADDRESS_S_CITY_SECTOR_F = None  # "LADM_COL.LADM_Nucleo.ExtDireccion.Sector_Ciudad"
    EXT_ADDRESS_S_POSTAL_CODE_F = None  # "LADM_COL.LADM_Nucleo.ExtDireccion.Codigo_Postal"
    EXT_ADDRESS_S_COMPLEMENT_F = None  # "LADM_COL.LADM_Nucleo.ExtDireccion.Complemento"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtInteresado.Ext_Direccion_ID"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtInteresado.Firma"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtInteresado.Fotografia"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtInteresado.Huella_Dactilar"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtInteresado.Interesado_ID"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtInteresado.Nombre"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtRedServiciosFisica.Ext_Interesado_Administrador_ID"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtRedServiciosFisica.Orientada"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtUnidadEdificacionFisica.Ext_Direccion_ID"
    FRACTION_S_DENOMINATOR_F = None  # "LADM_COL_V1_2.LADM_Nucleo.Fraccion.Denominador"
    FRACTION_S_NUMERATOR_F = None  # "LADM_COL_V1_2.LADM_Nucleo.Fraccion.Numerador"
    # "LADM_COL_V1_2.LADM_Nucleo.Imagen.uri"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Transformacion.Localizacion_Transformada"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Transformacion.Transformacion"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_VolumenValor.Tipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_VolumenValor.Volumen_Medicion"
    MORE_BFS_T_BOUNDARY_F = None  # "LADM_COL_V1_2.LADM_Nucleo.col_masCcl.ccl_mas"
    # "LADM_COL_V1_2.LADM_Nucleo.col_masCcl.ue_mas"
    # "LADM_COL_V1_2.LADM_Nucleo.col_masCl.ue_mas"
    LESS_BFS_T_OP_BOUNDARY_F = None # "LADM_COL_V1_2.LADM_Nucleo.col_menosCcl.ccl_menos"
                                    # "LADM_COL.LADM_Nucleo.col_menosCcl.ccl_menos_Operacion.Operacion.OP_Lindero" --> ccl_menos_op_lindero
    # "LADM_COL_V1_2.LADM_Nucleo.col_menosCcl.ue_menos"
    # "LADM_COL_V1_2.LADM_Nucleo.col_menosCl.ue_menos"
    MEMBERS_T_GROUP_PARTY_F = None  # "LADM_COL_V1_2.LADM_Nucleo.col_miembros.agrupacion"
    MEMBERS_T_PARTY_F = None  # "LADM_COL_V1_2.LADM_Nucleo.col_miembros.interesado"
    FRACTION_S_MEMBER_F = None  # "LADM_COL_V1_2.LADM_Nucleo.col_miembros.participacion"
    FRACTION_S_COPROPERTY_COEFFICIENT_F = None  # "Operacion.Operacion.op_predio_copropiedad.coeficiente"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F = None  # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F = None  # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL_V1_2.LADM_Nucleo.OM_Observacion.Resultado_Calidad"
    POINT_BFS_T_BOUNDARY_F = None  # "LADM_COL_V1_2.LADM_Nucleo.col_puntoCcl.ccl"
    # "LADM_COL_V1_2.LADM_Nucleo.col_puntoCcl.punto"
    # "LADM_COL_V1_2.LADM_Nucleo.col_puntoCl.punto"
    COL_POINT_SOURCE_T_SOURCE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.col_puntoFuente.fuente_espacial"
    # "LADM_COL_V1_2.LADM_Nucleo.col_puntoFuente.punto"
    # "LADM_COL_V1_2.LADM_Nucleo.col_puntoReferencia.ue"
    # "LADM_COL_V1_2.LADM_Nucleo.col_relacionFuente.fuente_administrativa"
    # "LADM_COL_V1_2.LADM_Nucleo.col_relacionFuenteUespacial.fuente_espacial"
    # "LADM_COL_V1_2.LADM_Nucleo.col_responsableFuente.fuente_administrativa"
    # "LADM_COL_V1_2.LADM_Nucleo.col_responsableFuente.interesado"
    COL_RRR_SOURCE_T_SOURCE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.col_rrrFuente.fuente_administrativa"
    # "LADM_COL_V1_2.LADM_Nucleo.col_rrrFuente.rrr"
    COL_RRR_PARTY_T_OP_PARTY_F = None  # "LADM_COL.LADM_Nucleo.col_rrrInteresado.interesado_Operacion.Operacion.OP_Interesado"
    COL_RRR_PARTY_T_OP_GROUP_PARTY_F = None  # "LADM_COL.LADM_Nucleo.col_rrrInteresado.interesado_Operacion.Operacion.OP_Agrupacion_Interesados"
    # "LADM_COL_V1_2.LADM_Nucleo.col_topografoFuente.fuente_espacial"
    # "LADM_COL_V1_2.LADM_Nucleo.col_topografoFuente.topografo"
    COL_UE_BAUNIT_T_PARCEL_F = None  # "LADM_COL_V1_2.LADM_Nucleo.col_ueBaunit.baunit"
    # "LADM_COL_V1_2.LADM_Nucleo.col_ueBaunit.ue"
    COL_UE_SOURCE_T_SOURCE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.col_ueFuente.fuente_espacial"
    # "LADM_COL_V1_2.LADM_Nucleo.col_ueFuente.ue"
    # "LADM_COL_V1_2.LADM_Nucleo.col_ueUeGrupo.parte"
    # "LADM_COL_V1_2.LADM_Nucleo.col_unidadFuente.fuente_administrativa"
    # "LADM_COL_V1_2.LADM_Nucleo.col_unidadFuente.unidad"
    #
    #
    OP_BUILDING_T_BUILDING_AREA_F = None  # "Operacion_V2_9_5.Operacion.OP_Construccion.Area_Construccion"
    OP_BUILDING_T_BUILDING_VALUATION_F = None  # "Operacion_V2_9_5.Operacion.OP_Construccion.Avaluo_Construccion"
    OP_BUILDING_T_NUMBER_OF_FLOORS_F = None  # "Operacion_V2_9_5.Operacion.OP_Construccion.Numero_Pisos"
    OP_BUILDING_UNIT_T_BUILDING_F = None  # "Operacion_V2_9_5.Operacion.op_construccion_unidadconstruccion.op_construccion"
    OP_RIGHT_T_TYPE_F = None  # "Operacion_V2_9_5.Operacion.OP_Derecho.Tipo"
    OP_ADMINISTRATIVE_SOURCE_T_EMITTING_ENTITY_F = None  # "Operacion_V2_9_5.Operacion.OP_FuenteAdministrativa.Ente_Emisor"
    OP_ADMINISTRATIVE_SOURCE_T_TYPE_F = None  # "Operacion_V2_9_5.Operacion.OP_FuenteAdministrativa.Tipo"
    # "Operacion_V2_9_5.Operacion.OP_Interesado_Contacto.Autoriza_Notificacion_Correo"
    # "Operacion_V2_9_5.Operacion.OP_Interesado_Contacto.Correo_Electronico"
    # "Operacion_V2_9_5.Operacion.OP_Interesado_Contacto.Domicilio_Notificacion"
    # "Operacion_V2_9_5.Operacion.op_interesado_contacto.op_interesado"
    # "Operacion_V2_9_5.Operacion.OP_Interesado_Contacto.Origen_Datos"
    # "Operacion_V2_9_5.Operacion.OP_Interesado_Contacto.Telefono1"
    # "Operacion_V2_9_5.Operacion.OP_Interesado_Contacto.Telefono2"

    OP_PARTY_T_DOCUMENT_ID_F = None  # "Operacion_V2_9_5.Operacion.OP_Interesado.Documento_Identidad"
    OP_PARTY_T_ETHNIC_GROUP_F = None  # "Operacion_V2_9_5.Operacion.OP_Interesado.Grupo_Etnico"
    OP_PARTY_T_SURNAME_1_F = None  # "Operacion_V2_9_5.Operacion.OP_Interesado.Primer_Apellido"
    OP_PARTY_T_FIRST_NAME_1_F = None  # "Operacion_V2_9_5.Operacion.OP_Interesado.Primer_Nombre"
    OP_PARTY_T_BUSINESS_NAME_F = None  # "Operacion_V2_9_5.Operacion.OP_Interesado.Razon_Social"
    OP_PARTY_T_SURNAME_2_F = None  # "Operacion_V2_9_5.Operacion.OP_Interesado.Segundo_Apellido"
    OP_PARTY_T_FIRST_NAME_2_F = None  # "Operacion_V2_9_5.Operacion.OP_Interesado.Segundo_Nombre"
    OP_PARTY_T_GENRE_F = None  # "Operacion_V2_9_5.Operacion.OP_Interesado.Sexo"
    OP_PARTY_T_TYPE_F = None  # "Operacion_V2_9_5.Operacion.OP_Interesado.Tipo"
    OP_PARTY_T_DOCUMENT_TYPE_F = None  # "Operacion_V2_9_5.Operacion.OP_Interesado.Tipo_Documento"
    OP_BOUNDARY_T_LENGTH_F = None  # "Operacion_V2_9_5.Operacion.OP_Lindero.Longitud"
    OP_PARCEL_T_VALUATION_F = None  # "Operacion_V2_9_5.Operacion.OP_Predio.Avaluo_Predio"
    OP_PARCEL_T_ORIP_CODE_F = None  # "Operacion_V2_9_5.Operacion.OP_Predio.Codigo_ORIP"
    OP_PARCEL_T_PARCEL_TYPE_F = None  # "Operacion_V2_9_5.Operacion.OP_Predio.Condicion_Predio"
    OP_COPROPERTY_T_COPROPERTY_F = None  # "Operacion_V2_9_5.Operacion.op_predio_copropiedad.copropiedad"
    OP_COPROPERTY_T_PARCEL_F = None  # "Operacion_V2_9_5.Operacion.op_predio_copropiedad.predio"
    OP_PARCEL_T_DEPARTMENT_F = None  # "Operacion_V2_9_5.Operacion.OP_Predio.Departamento"
    OP_PARCEL_T_ADDRESS_F = None  # "Operacion_V2_9_5.Operacion.OP_Predio.Direccion"
    # "Operacion_V2_9_5.Operacion.op_predio_insumos_operacion.ini_predio_insumos"
    # "Operacion_V2_9_5.Operacion.op_predio_insumos_operacion.op_predio"
    OP_PARCEL_T_FMI_F = None  # "Operacion_V2_9_5.Operacion.OP_Predio.Matricula_Inmobiliaria"
    OP_PARCEL_T_MUNICIPALITY_F = None  # "Operacion_V2_9_5.Operacion.OP_Predio.Municipio"
    OP_PARCEL_T_PARCEL_NUMBER_F = None  # "Operacion_V2_9_5.Operacion.OP_Predio.Numero_Predial"
    OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F = None  # "Operacion_V2_9_5.Operacion.OP_Predio.Numero_Predial_Anterior"
    OP_PARCEL_T_NUPRE_F = None  # "Operacion_V2_9_5.Operacion.OP_Predio.NUPRE"
    OP_PARCEL_T_TYPE_F = None  # "Operacion_V2_9_5.Operacion.OP_Predio.Tipo"
    OP_CONTROL_POINT_T_HORIZONTAL_ACCURACY_F = None  # "Operacion_V2_9_5.Operacion.OP_PuntoControl.Exactitud_Horizontal"
    OP_CONTROL_POINT_T_VERTICAL_ACCURACY_F = None  # "Operacion_V2_9_5.Operacion.OP_PuntoControl.Exactitud_Vertical"
    OP_CONTROL_POINT_T_ID_F = None  # "Operacion_V2_9_5.Operacion.OP_PuntoControl.ID_Punto_Control"
    OP_CONTROL_POINT_T_POINT_TYPE_F = None  # "Operacion_V2_9_5.Operacion.OP_PuntoControl.PuntoTipo"
    OP_CONTROL_POINT_T_CONTROL_POINT_TYPE_F = None  # "Operacion_V2_9_5.Operacion.OP_PuntoControl.Tipo_Punto_Control"
    OP_SURVEY_POINT_T_HORIZONTAL_ACCURACY_F = None  # "Operacion_V2_9_5.Operacion.OP_PuntoLevantamiento.Exactitud_Horizontal"
    OP_SURVEY_POINT_T_VERTICAL_ACCURACY_F = None  # "Operacion_V2_9_5.Operacion.OP_PuntoLevantamiento.Exactitud_Vertical"
    OP_SURVEY_POINT_T_PHOTO_IDENTIFICATION_F = None  # "Operacion_V2_9_5.Operacion.OP_PuntoLevantamiento.Fotoidentificacion"
    OP_SURVEY_POINT_T_ID_F = None  # "Operacion_V2_9_5.Operacion.OP_PuntoLevantamiento.ID_Punto_Levantamiento"
    OP_SURVEY_POINT_T_POINT_TYPE_F = None  # "Operacion_V2_9_5.Operacion.OP_PuntoLevantamiento.PuntoTipo"
    OP_SURVEY_POINT_T_SURVEY_POINT_TYPE_F = None  # "Operacion_V2_9_5.Operacion.OP_PuntoLevantamiento.Tipo_Punto_Levantamiento"
    OP_BOUNDARY_POINT_T_AGREEMENT_F = None  # "Operacion_V2_9_5.Operacion.OP_PuntoLindero.Acuerdo"
    OP_BOUNDARY_POINT_T_HORIZONTAL_ACCURACY_F = None  # "Operacion_V2_9_5.Operacion.OP_PuntoLindero.Exactitud_Horizontal"
    OP_BOUNDARY_POINT_T_VERTICAL_ACCURACY_F = None  # "Operacion_V2_9_5.Operacion.OP_PuntoLindero.Exactitud_Vertical"
    OP_BOUNDARY_POINT_T_PHOTO_IDENTIFICATION_F = None  # "Operacion_V2_9_5.Operacion.OP_PuntoLindero.Fotoidentificacion"
    OP_BOUNDARY_POINT_T_ID_F = None  # "Operacion_V2_9_5.Operacion.OP_PuntoLindero.ID_Punto_Lindero"
    OP_BOUNDARY_POINT_T_POINT_TYPE_F = None  # "Operacion_V2_9_5.Operacion.OP_PuntoLindero.PuntoTipo"
    OP_BOUNDARY_POINT_T_POINT_LOCATION_F = None  # "Operacion_V2_9_5.Operacion.OP_PuntoLindero.Ubicacion_Punto"
    OP_RESTRICTION_T_TYPE_F = None  # "Operacion_V2_9_5.Operacion.OP_Restriccion.Tipo"
    OP_RIGHT_OF_WAY_T_RIGHT_OF_WAY_AREA_F = None  # "Operacion_V2_9_5.Operacion.OP_ServidumbrePaso.Area_Servidumbre"
    OP_PLOT_T_PLOT_AREA_F = None  # "Operacion_V2_9_5.Operacion.OP_Terreno.Area_Terreno"
    OP_PLOT_T_PLOT_VALUATION_F = None  # "Operacion_V2_9_5.Operacion.OP_Terreno.Avaluo_Terreno"
    OP_PLOT_T_GEOMETRY_F = None  # "Operacion_V2_9_5.Operacion.OP_Terreno.Geometria"
    OP_BUILDING_UNIT_T_BUILT_AREA_F = None  # "Operacion_V2_9_5.Operacion.OP_UnidadConstruccion.Area_Construida"
    OP_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F = None  # "Operacion_V2_9_5.Operacion.OP_UnidadConstruccion.Area_Privada_Construida"
    OP_BUILDING_UNIT_T_BUILDING_UNIT_VALUATION_F = None  # "Operacion_V2_9_5.Operacion.OP_UnidadConstruccion.Avaluo_Unidad_Construccion"
    OP_BUILDING_UNIT_T_IDENTIFICATION_F = None  # "Operacion_V2_9_5.Operacion.OP_UnidadConstruccion.Identificador"
    OP_BUILDING_UNIT_T_NUMBER_OF_FLOORS_F = None  # "Operacion_V2_9_5.Operacion.OP_UnidadConstruccion.Numero_Pisos"
    OP_BUILDING_UNIT_T_FLOOR_F = None  # "Operacion_V2_9_5.Operacion.OP_UnidadConstruccion.Piso_Ubicacion"
    OP_BUILDING_UNIT_T_USE_F = None  # "Operacion_V2_9_5.Operacion.OP_UnidadConstruccion.Uso"

    # Composed keys (when ilinames are duplicated because their target table is different, we
    # concatenate in the form "{key}_{target}")

    # "LADM_COL.LADM_Nucleo.col_baunitComoInteresado.interesado_Operacion.Operacion.OP_Agrupacion_Interesados" --> interesado_op_agrupacion_interesados
    # "LADM_COL.LADM_Nucleo.col_baunitComoInteresado.interesado_Operacion.Operacion.OP_Interesado" --> interesado_op_interesado
    # "LADM_COL.LADM_Nucleo.col_cclFuente.ccl_Cartografia_Referencia.Auxiliares.CRF_EstructuraLineal" --> ccl_crf_estructuralineal
    # "LADM_COL.LADM_Nucleo.COL_Fuente.Calidad_Operacion.Operacion.OP_FuenteAdministrativa" --> op_fuenteadministrtiva_calidad
    # "LADM_COL.LADM_Nucleo.COL_Fuente.Calidad_Operacion.Operacion.OP_FuenteEspacial" --> op_fuenteespacial_calidad
    EXT_ARCHIVE_S_OP_ADMINISTRATIVE_SOURCE_F = None  # "LADM_COL.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID_Operacion.Operacion.OP_FuenteAdministrativa" --> op_fuenteadministrtiva_ext_archivo_id
    EXT_ARCHIVE_S_OP_SPATIAL_SOURCE_F = None  # "LADM_COL.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID_Operacion.Operacion.OP_FuenteEspacial" --> op_fuenteespacial_ext_archivo_id
    # "LADM_COL.LADM_Nucleo.COL_Fuente.Procedencia_Operacion.Operacion.OP_FuenteAdministrativa" --> op_fuenteadministrtiva_procedencia
    # "LADM_COL.LADM_Nucleo.COL_Fuente.Procedencia_Operacion.Operacion.OP_FuenteEspacial" --> op_fuenteespacial_procedencia
    # "LADM_COL.LADM_Nucleo.COL_Interesado.ext_PID_Operacion.Operacion.OP_Agrupacion_Interesados" --> op_agrupacion_intrsdos_ext_pid
    # "LADM_COL.LADM_Nucleo.COL_Interesado.ext_PID_Operacion.Operacion.OP_Interesado" --> op_interesado_ext_pid
    # "LADM_COL.LADM_Nucleo.COL_Interesado.Tarea_Operacion.Operacion.OP_Agrupacion_Interesados" --> op_agrupacion_intrsdos_tarea
    # "LADM_COL.LADM_Nucleo.COL_Interesado.Tarea_Operacion.Operacion.OP_Interesado" --> op_interesado_tarea
    # "LADM_COL.LADM_Nucleo.COL_Punto.Transformacion_Y_Resultado_Cartografia_Referencia.Auxiliares.CRF_EstructuraPuntual" --> crf_estructurapuntual_transformacion_y_resultado
    # "LADM_COL.LADM_Nucleo.COL_Punto.Transformacion_Y_Resultado_Cartografia_Referencia.LimitesPoliticoAdministrativos.CRF_PuntoLimite" --> crf_puntolimite_transformacion_y_resultado
    # "LADM_COL.LADM_Nucleo.COL_Punto.Transformacion_Y_Resultado_Operacion.Operacion.OP_PuntoControl" --> op_puntocontrol_transformacion_y_resultado
    # "LADM_COL.LADM_Nucleo.COL_Punto.Transformacion_Y_Resultado_Operacion.Operacion.OP_PuntoLevantamiento" --> op_puntolevantamiento_transformacion_y_resultado
    # "LADM_COL.LADM_Nucleo.COL_Punto.Transformacion_Y_Resultado_Operacion.Operacion.OP_PuntoLindero" --> op_puntolindero_transformacion_y_resultado
    FRACTION_S_OP_RIGHT_F = None  # "LADM_COL.LADM_Nucleo.COL_RRR.Compartido_Operacion.Operacion.OP_Derecho" --> op_derecho_compartido
    FRACTION_S_OP_RESTRICTION_F = None  # "LADM_COL.LADM_Nucleo.COL_RRR.Compartido_Operacion.Operacion.OP_Restriccion" --> op_restriccion_compartido
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Area_Operacion.Operacion.OP_Construccion" --> op_construccion_area
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Area_Operacion.Operacion.OP_ServidumbrePaso" --> op_servidumbrepaso_area
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Area_Operacion.Operacion.OP_Terreno" --> op_terreno_area
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Area_Operacion.Operacion.OP_UnidadConstruccion" --> op_unidadconstruccion_area
    EXT_ADDRESS_S_OP_BUILDING_F = None  # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID_Operacion.Operacion.OP_Construccion" --> op_construccion_ext_direccion_id
    EXT_ADDRESS_S_OP_RIGHT_OF_WAY_F = None  # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID_Operacion.Operacion.OP_ServidumbrePaso" --> op_servidumbrepaso_ext_direccion_id
    EXT_ADDRESS_S_OP_PLOT_F = None  # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID_Operacion.Operacion.OP_Terreno" --> op_terreno_ext_direccion_id
    EXT_ADDRESS_S_OP_BUILDING_UNIT_F = None  # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID_Operacion.Operacion.OP_UnidadConstruccion" --> op_unidadconstruccion_ext_direccion_id
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Volumen_Operacion.Operacion.OP_Construccion" --> op_construccion_volumen
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Volumen_Operacion.Operacion.OP_ServidumbrePaso" --> op_servidumbrepaso_volumen
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Volumen_Operacion.Operacion.OP_Terreno" --> op_terreno_volumen
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Volumen_Operacion.Operacion.OP_UnidadConstruccion" --> op_unidadconstruccion_volumen
    # "LADM_COL.LADM_Nucleo.col_masCcl.ccl_mas_Cartografia_Referencia.Auxiliares.CRF_EstructuraLineal" --> ccl_mas_crf_estructuralineal
    # "LADM_COL.LADM_Nucleo.col_masCcl.ccl_mas_Operacion.Operacion.OP_Lindero" --> ccl_mas_op_lindero
    MORE_BFS_T_OP_BUILDING_F = None  # "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas_Operacion.Operacion.OP_Construccion" --> ue_mas_op_construccion
    MORE_BFS_T_OP_RIGHT_OF_WAY_F = None  # "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas_Operacion.Operacion.OP_ServidumbrePaso" --> ue_mas_op_servidumbrepaso
    MORE_BFS_T_OP_PLOT_F = None  # "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas_Operacion.Operacion.OP_Terreno" --> ue_mas_op_terreno
    MORE_BFS_T_OP_BUILDING_UNIT_F = None  # "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas_Operacion.Operacion.OP_UnidadConstruccion" --> ue_mas_op_unidadconstruccion
    # "LADM_COL.LADM_Nucleo.col_masCl.ue_mas_Operacion.Operacion.OP_Construccion" --> ue_mas_op_construccion
    # "LADM_COL.LADM_Nucleo.col_masCl.ue_mas_Operacion.Operacion.OP_ServidumbrePaso" --> ue_mas_op_servidumbrepaso
    # "LADM_COL.LADM_Nucleo.col_masCl.ue_mas_Operacion.Operacion.OP_Terreno" --> ue_mas_op_terreno
    # "LADM_COL.LADM_Nucleo.col_masCl.ue_mas_Operacion.Operacion.OP_UnidadConstruccion" --> ue_mas_op_unidadconstruccion
    # "LADM_COL.LADM_Nucleo.col_menosCcl.ccl_menos_Cartografia_Referencia.Auxiliares.CRF_EstructuraLineal" --> ccl_menos_crf_estructuralineal
    LESS_BFS_T_OP_BUILDING_F = None  # "LADM_COL.LADM_Nucleo.col_menosCcl.ue_menos_Operacion.Operacion.OP_Construccion" --> ue_menos_op_construccion
    LESS_BFS_T_OP_RIGHT_OF_WAY_F = None  # "LADM_COL.LADM_Nucleo.col_menosCcl.ue_menos_Operacion.Operacion.OP_ServidumbrePaso" --> ue_menos_op_servidumbrepaso
    LESS_BFS_T_OP_PLOT_F = None  # "LADM_COL.LADM_Nucleo.col_menosCcl.ue_menos_Operacion.Operacion.OP_Terreno" --> ue_menos_op_terreno
    LESS_BFS_T_OP_BUILDING_UNIT_F = None  # "LADM_COL.LADM_Nucleo.col_menosCcl.ue_menos_Operacion.Operacion.OP_UnidadConstruccion" --> ue_menos_op_unidadconstruccion
    # "LADM_COL.LADM_Nucleo.col_menosCl.ue_menos_Operacion.Operacion.OP_Construccion" --> ue_menos_op_construccion
    # "LADM_COL.LADM_Nucleo.col_menosCl.ue_menos_Operacion.Operacion.OP_ServidumbrePaso" --> ue_menos_op_servidumbrepaso
    # "LADM_COL.LADM_Nucleo.col_menosCl.ue_menos_Operacion.Operacion.OP_Terreno" --> ue_menos_op_terreno
    # "LADM_COL.LADM_Nucleo.col_menosCl.ue_menos_Operacion.Operacion.OP_UnidadConstruccion" --> ue_menos_op_unidadconstruccion
    # "LADM_COL.LADM_Nucleo.col_miembros.interesados_Operacion.Operacion.OP_Agrupacion_Interesados" --> interesados_op_agrupacion_interesados
    # "LADM_COL.LADM_Nucleo.col_miembros.interesados_Operacion.Operacion.OP_Interesado" --> interesados_op_interesado
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad_Cartografia_Referencia.Auxiliares.CRF_EstructuraLineal" --> crf_estructuralineal_calidad
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad_Cartografia_Referencia.Auxiliares.CRF_EstructuraPuntual" --> crf_estructurapuntual_calidad
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad_Cartografia_Referencia.LimitesPoliticoAdministrativos.CRF_PuntoLimite" --> crf_puntolimite_calidad
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad_Operacion.Operacion.OP_Agrupacion_Interesados" --> op_agrupacion_intrsdos_calidad
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad_Operacion.Operacion.OP_Construccion" --> op_construccion_calidad
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad_Operacion.Operacion.OP_Derecho" --> op_derecho_calidad
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad_Operacion.Operacion.OP_Interesado" --> op_interesado_calidad
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad_Operacion.Operacion.OP_Lindero" --> op_lindero_calidad
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad_Operacion.Operacion.OP_Predio" --> op_predio_calidad
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad_Operacion.Operacion.OP_PuntoControl" --> op_puntocontrol_calidad
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad_Operacion.Operacion.OP_PuntoLevantamiento" --> op_puntolevantamiento_calidad
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad_Operacion.Operacion.OP_PuntoLindero" --> op_puntolindero_calidad
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad_Operacion.Operacion.OP_Restriccion" --> op_restriccion_calidad
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad_Operacion.Operacion.OP_ServidumbrePaso" --> op_servidumbrepaso_calidad
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad_Operacion.Operacion.OP_Terreno" --> op_terreno_calidad
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad_Operacion.Operacion.OP_UnidadConstruccion" --> op_unidadconstruccion_calidad
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia_Cartografia_Referencia.Auxiliares.CRF_EstructuraLineal" --> crf_estructuralineal_procedencia
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia_Cartografia_Referencia.Auxiliares.CRF_EstructuraPuntual" --> crf_estructurapuntual_procedencia
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia_Cartografia_Referencia.LimitesPoliticoAdministrativos.CRF_PuntoLimite" --> crf_puntolimite_procedencia
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia_Operacion.Operacion.OP_Agrupacion_Interesados" --> op_agrupacion_intrsdos_procedencia
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia_Operacion.Operacion.OP_Construccion" --> op_construccion_procedencia
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia_Operacion.Operacion.OP_Derecho" --> op_derecho_procedencia
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia_Operacion.Operacion.OP_Interesado" --> op_interesado_procedencia
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia_Operacion.Operacion.OP_Lindero" --> op_lindero_procedencia
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia_Operacion.Operacion.OP_Predio" --> op_predio_procedencia
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia_Operacion.Operacion.OP_PuntoControl" --> op_puntocontrol_procedencia
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia_Operacion.Operacion.OP_PuntoLevantamiento" --> op_puntolevantamiento_procedencia
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia_Operacion.Operacion.OP_PuntoLindero" --> op_puntolindero_procedencia
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia_Operacion.Operacion.OP_Restriccion" --> op_restriccion_procedencia
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia_Operacion.Operacion.OP_ServidumbrePaso" --> op_servidumbrepaso_procedencia
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia_Operacion.Operacion.OP_Terreno" --> op_terreno_procedencia
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia_Operacion.Operacion.OP_UnidadConstruccion" --> op_unidadconstruccion_procedencia
    # "LADM_COL.LADM_Nucleo.col_puntoCcl.ccl_Cartografia_Referencia.Auxiliares.CRF_EstructuraLineal" --> ccl_crf_estructuralineal
    # "LADM_COL.LADM_Nucleo.col_puntoCcl.ccl_Operacion.Operacion.OP_Lindero" --> ccl_op_lindero
    # "LADM_COL.LADM_Nucleo.col_puntoCcl.punto_Cartografia_Referencia.Auxiliares.CRF_EstructuraPuntual" --> punto_crf_estructurapuntual
    # "LADM_COL.LADM_Nucleo.col_puntoCcl.punto_Cartografia_Referencia.LimitesPoliticoAdministrativos.CRF_PuntoLimite" --> punto_crf_puntolimite
    POINT_BFS_T_OP_CONTROL_POINT_F = None  # "LADM_COL.LADM_Nucleo.col_puntoCcl.punto_Operacion.Operacion.OP_PuntoControl" --> punto_op_puntocontrol
    POINT_BFS_T_OP_SURVEY_POINT_F = None  # "LADM_COL.LADM_Nucleo.col_puntoCcl.punto_Operacion.Operacion.OP_PuntoLevantamiento" --> punto_op_puntolevantamiento
    POINT_BFS_T_OP_BOUNDARY_POINT_F = None  # "LADM_COL.LADM_Nucleo.col_puntoCcl.punto_Operacion.Operacion.OP_PuntoLindero" --> punto_op_puntolindero
    # "LADM_COL.LADM_Nucleo.col_puntoCl.punto_Cartografia_Referencia.Auxiliares.CRF_EstructuraPuntual" --> punto_crf_estructurapuntual
    # "LADM_COL.LADM_Nucleo.col_puntoCl.punto_Cartografia_Referencia.LimitesPoliticoAdministrativos.CRF_PuntoLimite" --> punto_crf_puntolimite
    # "LADM_COL.LADM_Nucleo.col_puntoCl.punto_Operacion.Operacion.OP_PuntoControl" --> punto_op_puntocontrol
    # "LADM_COL.LADM_Nucleo.col_puntoCl.punto_Operacion.Operacion.OP_PuntoLevantamiento" --> punto_op_puntolevantamiento
    # "LADM_COL.LADM_Nucleo.col_puntoCl.punto_Operacion.Operacion.OP_PuntoLindero" --> punto_op_puntolindero
    # "LADM_COL.LADM_Nucleo.col_puntoFuente.punto_Cartografia_Referencia.Auxiliares.CRF_EstructuraPuntual" --> punto_crf_estructurapuntual
    # "LADM_COL.LADM_Nucleo.col_puntoFuente.punto_Cartografia_Referencia.LimitesPoliticoAdministrativos.CRF_PuntoLimite" --> punto_crf_puntolimite
    COL_POINT_SOURCE_T_OP_CONTROL_POINT_F = None  # "LADM_COL.LADM_Nucleo.col_puntoFuente.punto_Operacion.Operacion.OP_PuntoControl" --> punto_op_puntocontrol
    COL_POINT_SOURCE_T_OP_SURVEY_POINT_F = None  # "LADM_COL.LADM_Nucleo.col_puntoFuente.punto_Operacion.Operacion.OP_PuntoLevantamiento" --> punto_op_puntolevantamiento
    COL_POINT_SOURCE_T_OP_BOUNDARY_POINT_F = None  # "LADM_COL.LADM_Nucleo.col_puntoFuente.punto_Operacion.Operacion.OP_PuntoLindero" --> punto_op_puntolindero
    # "LADM_COL.LADM_Nucleo.col_responsableFuente.notario_Operacion.Operacion.OP_Agrupacion_Interesados" --> notario_op_agrupacion_interesados
    # "LADM_COL.LADM_Nucleo.col_responsableFuente.notario_Operacion.Operacion.OP_Interesado" --> notario_op_interesado
    COL_RRR_SOURCE_T_OP_RIGHT_F = None  # "LADM_COL.LADM_Nucleo.col_rrrFuente.rrr_Operacion.Operacion.OP_Derecho" --> rrr_op_derecho
    COL_RRR_SOURCE_T_OP_RESTRICTION_F = None  # "LADM_COL.LADM_Nucleo.col_rrrFuente.rrr_Operacion.Operacion.OP_Restriccion" --> rrr_op_restriccion
    # "LADM_COL.LADM_Nucleo.col_topografoFuente.topografo_Operacion.Operacion.OP_Agrupacion_Interesados" --> topografo_op_agrupacion_interesados
    # "LADM_COL.LADM_Nucleo.col_topografoFuente.topografo_Operacion.Operacion.OP_Interesado" --> topografo_op_interesado

    COL_UE_BAUNIT_T_OP_PLOT_F = None  # "LADM_COL.LADM_Nucleo.col_ueBaunit.ue_Operacion.Operacion.OP_Terreno" --> ue_op_terreno
    COL_UE_BAUNIT_T_OP_BUILDING_F = None  # "LADM_COL.LADM_Nucleo.col_ueBaunit.ue_Operacion.Operacion.OP_Construccion" --> ue_op_construccion
    COL_UE_BAUNIT_T_OP_BUILDING_UNIT_F = None  # "LADM_COL.LADM_Nucleo.col_ueBaunit.ue_Operacion.Operacion.OP_UnidadConstruccion" --> ue_op_unidadconstruccion
    COL_UE_BAUNIT_T_OP_RIGHT_OF_WAY_F = None  # "LADM_COL.LADM_Nucleo.col_ueBaunit.ue_Operacion.Operacion.OP_ServidumbrePaso" --> ue_op_servidumbrepaso

    COL_UE_SOURCE_T_OP_BUILDING_F = None  # "LADM_COL.LADM_Nucleo.col_ueFuente.ue_Operacion.Operacion.OP_Construccion" --> ue_op_construccion
    COL_UE_SOURCE_T_OP_RIGHT_OF_WAY_F = None  # "LADM_COL.LADM_Nucleo.col_ueFuente.ue_Operacion.Operacion.OP_ServidumbrePaso" --> ue_op_servidumbrepaso
    COL_UE_SOURCE_T_OP_PLOT_F = None  # "LADM_COL.LADM_Nucleo.col_ueFuente.ue_Operacion.Operacion.OP_Terreno" --> ue_op_terreno
    COL_UE_SOURCE_T_OP_BUILDING_UNIT_F = None  # "LADM_COL.LADM_Nucleo.col_ueFuente.ue_Operacion.Operacion.OP_UnidadConstruccion" --> ue_op_unidadconstruccion
    # "LADM_COL.LADM_Nucleo.col_ueUeGrupo.parte_Operacion.Operacion.OP_Construccion" --> parte_op_construccion
    # "LADM_COL.LADM_Nucleo.col_ueUeGrupo.parte_Operacion.Operacion.OP_ServidumbrePaso" --> parte_op_servidumbrepaso
    # "LADM_COL.LADM_Nucleo.col_ueUeGrupo.parte_Operacion.Operacion.OP_Terreno" --> parte_op_terreno
    # "LADM_COL.LADM_Nucleo.col_ueUeGrupo.parte_Operacion.Operacion.OP_UnidadConstruccion" --> parte_op_unidadconstruccion


    TABLE_DICT = {
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Barrio": {VARIABLE_NAME: "GC_NEIGHBOURHOOD_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Construccion": {VARIABLE_NAME: "GC_BUILDING_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio": {VARIABLE_NAME: "GC_HP_CONDOMINIUM_DATA_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Manzana": {VARIABLE_NAME: "GC_BLOCK_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Perimetro": {VARIABLE_NAME: "GC_PERIMETER_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.gc_ph_predio": {VARIABLE_NAME: "GC_HP_PARCEL_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro": {VARIABLE_NAME: "GC_PARCEL_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietaio": {VARIABLE_NAME: "GC_OWNER_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Sector_Rural": {VARIABLE_NAME: "GC_RURAL_SECTOR_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Sector_Urbano": {VARIABLE_NAME: "GC_URBAN_SECTOR_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno": {VARIABLE_NAME: "GC_PLOT_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Unidad_Construccion": {VARIABLE_NAME: "GC_BUILDING_UNIT_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Vereda": {VARIABLE_NAME: "GC_RURAL_DIVISION_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.GC_CondicionPredioTipo": {VARIABLE_NAME: "GC_PARCEL_TYPE_D", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.GC_Direccion": {VARIABLE_NAME: "GC_ADDRESS_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.GC_UnidadConstruccionTipo": {VARIABLE_NAME: "GC_BUILDING_UNIT_TYPE_T", FIELDS_DICT: {}},
        "Datos_Integracion_Insumos.Datos_Integracion_Insumos.INI_Predio_Insumos": {VARIABLE_NAME: "INI_PARCEL_SUPPLIES_T", FIELDS_DICT: {}},
        "Datos_SNR.Datos_SNR.SNR_Derecho": {VARIABLE_NAME: "SNR_RIGHT_T", FIELDS_DICT: {}},
        "Datos_SNR.Datos_SNR.SNR_Fuente_CabidaLinderos": {VARIABLE_NAME: "SNR_SOURCE_BOUNDARIES_T", FIELDS_DICT: {}},
        "Datos_SNR.Datos_SNR.SNR_Fuente_Derecho": {VARIABLE_NAME: "SNR_SOURCE_RIGHT_T", FIELDS_DICT: {}},
        "Datos_SNR.Datos_SNR.SNR_Predio_Registro": {VARIABLE_NAME: "SNR_PARCEL_REGISTRY_T", FIELDS_DICT: {}},
        "Datos_SNR.Datos_SNR.SNR_Titular": {VARIABLE_NAME: "SNR_TITLE_HOLDER_T", FIELDS_DICT: {}},
        "Datos_SNR.SNR_CalidadDerechoTipo": {VARIABLE_NAME: "SNR_RIGHT_TYPE_D", FIELDS_DICT: {}},
        "Datos_SNR.SNR_DocumentoTitularTipo": {VARIABLE_NAME: "SNR_TITLE_HOLDER_DOCUMENT_T", FIELDS_DICT: {}},
        "Datos_SNR.SNR_FuenteTipo": {VARIABLE_NAME: "SNR_SOURCE_TYPE_D", FIELDS_DICT: {}},
        "Datos_SNR.SNR_PersonaTitularTipo": {VARIABLE_NAME: "SNR_TITLE_HOLDER_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.COL_EstadoDisponibilidadTipo": {VARIABLE_NAME: "COL_AVAILABILITY_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.COL_FuenteAdministrativaTipo": {VARIABLE_NAME: "COL_ADMINISTRATIVE_SOURCE_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.COL_FuenteEspacialTipo": {VARIABLE_NAME: "COL_SPATIAL_SOURCE_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.COL_GrupoInteresadoTipo": {VARIABLE_NAME: "COL_GROUP_PARTY_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.COL_InterpolacionTipo": {VARIABLE_NAME: "COL_INTERPOLATION_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.COL_MetodoProduccionTipo": {VARIABLE_NAME: "COL_PRODUCTION_METHOD", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.COL_RelacionSuperficieTipo": {VARIABLE_NAME: "COL_SURFACE_RELATION_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.COL_MonumentacionTipo": {VARIABLE_NAME: "COL_MONUMENTATION_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.ExtArchivo": {VARIABLE_NAME: "EXT_ARCHIVE_S", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.ExtArchivo.Datos": "EXT_ARCHIVE_S_DATA_F",
            "LADM_COL.LADM_Nucleo.ExtArchivo.Extraccion": "EXT_ARCHIVE_S_EXTRACTION_F",
            "LADM_COL.LADM_Nucleo.ExtArchivo.Fecha_Aceptacion": "EXT_ARCHIVE_S_ACCEPTANCE_DATE_F",
            "LADM_COL.LADM_Nucleo.ExtArchivo.Fecha_Entrega": "EXT_ARCHIVE_S_DELIVERY_DATE_F",
            "LADM_COL.LADM_Nucleo.ExtArchivo.Fecha_Grabacion": "EXT_ARCHIVE_S_STORAGE_DATE_F",
            "LADM_COL.LADM_Nucleo.ExtArchivo.Espacio_De_Nombres": "EXT_ARCHIVE_S_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.ExtArchivo.Local_Id": "EXT_ARCHIVE_S_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID_Operacion.Operacion.OP_FuenteAdministrativa": "EXT_ARCHIVE_S_OP_ADMINISTRATIVE_SOURCE_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID_Operacion.Operacion.OP_FuenteEspacial": "EXT_ARCHIVE_S_OP_SPATIAL_SOURCE_F"
        }},
        "LADM_COL.LADM_Nucleo.ExtDireccion": {VARIABLE_NAME: "EXT_ADDRESS_S", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.ExtDireccion.Valor_Via_Principal": "EXT_ADDRESS_S_VALUE_MAIN_ROAD_F",
            "LADM_COL.LADM_Nucleo.ExtDireccion.Numero_Predio": "EXT_ADDRESS_S_PARCEL_NUMBER_F",
            "LADM_COL.LADM_Nucleo.ExtDireccion.Localizacion": "EXT_ADDRESS_S_LOCALIZATION_F",
            "LADM_COL.LADM_Nucleo.ExtDireccion.Clase_Via_Principal": "EXT_ADDRESS_S_MAIN_ROAD_CLASS_F",
            "LADM_COL.LADM_Nucleo.ExtDireccion.Sector_Predio": "EXT_ADDRESS_S_PARCEL_SECTOR_F",
            "LADM_COL.LADM_Nucleo.ExtDireccion.Nombre_Predio": "EXT_ADDRESS_S_PARCEL_NAME_F",
            "LADM_COL.LADM_Nucleo.ExtDireccion.Es_Direccion_Principal": "EXT_ADDRESS_S_IS_MAIN_ADDRESS_F",
            "LADM_COL.LADM_Nucleo.ExtDireccion.Letra_Via_Generadora": "EXT_ADDRESS_S_LETTER_GENERATOR_ROAD_F",
            "LADM_COL.LADM_Nucleo.ExtDireccion.Valor_Via_Generadora": "EXT_ADDRESS_S_VALUE_GENERATOR_ROAD_F",
            "LADM_COL.LADM_Nucleo.ExtDireccion.Letra_Via_Principal": "EXT_ADDRESS_S_LETTER_MAIN_ROAD_F",
            "LADM_COL.LADM_Nucleo.ExtDireccion.Tipo_Direccion": "EXT_ADDRESS_S_ADDRESS_TYPE_F",
            "LADM_COL.LADM_Nucleo.ExtDireccion.Sector_Ciudad": "EXT_ADDRESS_S_CITY_SECTOR_F",
            "LADM_COL.LADM_Nucleo.ExtDireccion.Codigo_Postal": "EXT_ADDRESS_S_POSTAL_CODE_F",
            "LADM_COL.LADM_Nucleo.ExtDireccion.Complemento": "EXT_ADDRESS_S_COMPLEMENT_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID_Operacion.Operacion.OP_Construccion": "EXT_ADDRESS_S_OP_BUILDING_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID_Operacion.Operacion.OP_ServidumbrePaso": "EXT_ADDRESS_S_OP_RIGHT_OF_WAY_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID_Operacion.Operacion.OP_Terreno": "EXT_ADDRESS_S_OP_PLOT_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID_Operacion.Operacion.OP_UnidadConstruccion": "EXT_ADDRESS_S_OP_BUILDING_UNIT_F"
        }},
        "LADM_COL.LADM_Nucleo.ExtInteresado": {VARIABLE_NAME: "EXT_PARTY_S", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.Fraccion": {VARIABLE_NAME: "FRACTION_S", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.Fraccion.Denominador": "FRACTION_S_DENOMINATOR_F",
            "LADM_COL.LADM_Nucleo.Fraccion.Numerador": "FRACTION_S_NUMERATOR_F",
            "LADM_COL.LADM_Nucleo.col_miembros.participacion": "FRACTION_S_MEMBER_F",
            "Operacion.Operacion.op_predio_copropiedad.coeficiente": "FRACTION_S_COPROPERTY_COEFFICIENT_F",
            "LADM_COL.LADM_Nucleo.COL_RRR.Compartido_Operacion.Operacion.OP_Derecho": "FRACTION_S_OP_RIGHT_F",
            "LADM_COL.LADM_Nucleo.COL_RRR.Compartido_Operacion.Operacion.OP_Restriccion": "FRACTION_S_OP_RESTRICTION_F"
        }},
        "LADM_COL.LADM_Nucleo.COL_BAUnitTipo": {VARIABLE_NAME: "COL_BAUNIT_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.COL_DimensionTipo": {VARIABLE_NAME: "COL_DIMENSION_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.COL_PuntoTipo": {VARIABLE_NAME: "COL_POINT_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.col_masCcl": {VARIABLE_NAME: "MORE_BFS_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_masCcl.ccl_mas": "MORE_BFS_T_BOUNDARY_F",
            "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas_Operacion.Operacion.OP_Construccion": "MORE_BFS_T_OP_BUILDING_F",
            "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas_Operacion.Operacion.OP_ServidumbrePaso": "MORE_BFS_T_OP_RIGHT_OF_WAY_F",
            "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas_Operacion.Operacion.OP_Terreno": "MORE_BFS_T_OP_PLOT_F",
            "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas_Operacion.Operacion.OP_UnidadConstruccion": "MORE_BFS_T_OP_BUILDING_UNIT_F"
        }},
        "LADM_COL.LADM_Nucleo.col_menosCcl": {VARIABLE_NAME: "LESS_BFS_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_menosCcl.ccl_menos": "LESS_BFS_T_OP_BOUNDARY_F",
            "LADM_COL.LADM_Nucleo.col_menosCcl.ue_menos_Operacion.Operacion.OP_Construccion": "LESS_BFS_T_OP_BUILDING_F",
            "LADM_COL.LADM_Nucleo.col_menosCcl.ue_menos_Operacion.Operacion.OP_ServidumbrePaso": "LESS_BFS_T_OP_RIGHT_OF_WAY_F",
            "LADM_COL.LADM_Nucleo.col_menosCcl.ue_menos_Operacion.Operacion.OP_Terreno": "LESS_BFS_T_OP_PLOT_F",
            "LADM_COL.LADM_Nucleo.col_menosCcl.ue_menos_Operacion.Operacion.OP_UnidadConstruccion": "LESS_BFS_T_OP_BUILDING_UNIT_F",
        }},
        "LADM_COL.LADM_Nucleo.col_miembros": {VARIABLE_NAME: "MEMBERS_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_miembros.agrupacion": "MEMBERS_T_GROUP_PARTY_F",
            "LADM_COL.LADM_Nucleo.col_miembros.interesado": "MEMBERS_T_PARTY_F"
        }},
        "LADM_COL.LADM_Nucleo.col_puntoCcl": {VARIABLE_NAME: "POINT_BFS_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_puntoCcl.ccl": "POINT_BFS_T_BOUNDARY_F",
            "LADM_COL.LADM_Nucleo.col_puntoCcl.punto_Operacion.Operacion.OP_PuntoControl": "POINT_BFS_T_OP_CONTROL_POINT_F",
            "LADM_COL.LADM_Nucleo.col_puntoCcl.punto_Operacion.Operacion.OP_PuntoLevantamiento": "POINT_BFS_T_OP_SURVEY_POINT_F",
            "LADM_COL.LADM_Nucleo.col_puntoCcl.punto_Operacion.Operacion.OP_PuntoLindero": "POINT_BFS_T_OP_BOUNDARY_POINT_F",
        }},
        "LADM_COL.LADM_Nucleo.col_puntoFuente": {VARIABLE_NAME: "COL_POINT_SOURCE_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_puntoFuente.fuente_espacial": "COL_POINT_SOURCE_T_SOURCE_F",
            "LADM_COL.LADM_Nucleo.col_puntoFuente.punto_Operacion.Operacion.OP_PuntoControl": "COL_POINT_SOURCE_T_OP_CONTROL_POINT_F",
            "LADM_COL.LADM_Nucleo.col_puntoFuente.punto_Operacion.Operacion.OP_PuntoLevantamiento": "COL_POINT_SOURCE_T_OP_SURVEY_POINT_F",
            "LADM_COL.LADM_Nucleo.col_puntoFuente.punto_Operacion.Operacion.OP_PuntoLindero": "COL_POINT_SOURCE_T_OP_BOUNDARY_POINT_F"
        }},
        "LADM_COL.LADM_Nucleo.col_rrrFuente": {VARIABLE_NAME: "COL_RRR_SOURCE_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_rrrFuente.fuente_administrativa": "COL_RRR_SOURCE_T_SOURCE_F",
            "LADM_COL.LADM_Nucleo.col_rrrFuente.rrr_Operacion.Operacion.OP_Derecho": "COL_RRR_SOURCE_T_OP_RIGHT_F",
            "LADM_COL.LADM_Nucleo.col_rrrFuente.rrr_Operacion.Operacion.OP_Restriccion": "COL_RRR_SOURCE_T_OP_RESTRICTION_F"
        }},
        "LADM_COL.LADM_Nucleo.col_ueBaunit": {VARIABLE_NAME: "COL_UE_BAUNIT_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_ueBaunit.baunit": "COL_UE_BAUNIT_T_PARCEL_F",
            "LADM_COL.LADM_Nucleo.col_ueBaunit.ue_Operacion.Operacion.OP_Terreno": "COL_UE_BAUNIT_T_OP_PLOT_F",
            "LADM_COL.LADM_Nucleo.col_ueBaunit.ue_Operacion.Operacion.OP_Construccion": "COL_UE_BAUNIT_T_OP_BUILDING_F",
            "LADM_COL.LADM_Nucleo.col_ueBaunit.ue_Operacion.Operacion.OP_UnidadConstruccion": "COL_UE_BAUNIT_T_OP_BUILDING_UNIT_F",
            "LADM_COL.LADM_Nucleo.col_ueBaunit.ue_Operacion.Operacion.OP_ServidumbrePaso": "COL_UE_BAUNIT_T_OP_RIGHT_OF_WAY_F"
        }},
        "LADM_COL.LADM_Nucleo.col_ueFuente": {VARIABLE_NAME: "COL_UE_SOURCE_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_ueFuente.fuente_espacial": "COL_UE_SOURCE_T_SOURCE_F",
            "LADM_COL.LADM_Nucleo.col_ueFuente.ue_Operacion.Operacion.OP_Construccion": "COL_UE_SOURCE_T_OP_BUILDING_F",
            "LADM_COL.LADM_Nucleo.col_ueFuente.ue_Operacion.Operacion.OP_ServidumbrePaso": "COL_UE_SOURCE_T_OP_RIGHT_OF_WAY_F",
            "LADM_COL.LADM_Nucleo.col_ueFuente.ue_Operacion.Operacion.OP_Terreno": "COL_UE_SOURCE_T_OP_PLOT_F",
            "LADM_COL.LADM_Nucleo.col_ueFuente.ue_Operacion.Operacion.OP_UnidadConstruccion": "COL_UE_SOURCE_T_OP_BUILDING_UNIT_F"
        }},
        "LADM_COL.LADM_Nucleo.col_baunitFuente": {VARIABLE_NAME: "COL_BAUNIT_SOURCE_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_baunitFuente.fuente_espacial": "BAUNIT_SOURCE_T_SOURCE_F",
            "LADM_COL.LADM_Nucleo.col_baunitFuente.unidad": "BAUNIT_SOURCE_T_UNIT_F"
        }},
        "LADM_COL.LADM_Nucleo.col_cclFuente": {VARIABLE_NAME: "COL_CCL_SOURCE_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_cclFuente.fuente_espacial": "COL_CCL_SOURCE_T_SOURCE_F",
            "LADM_COL.LADM_Nucleo.col_cclFuente.ccl": "COL_CCL_SOURCE_T_BOUNDARY_F"
        }},
        "Operacion.OP_AcuerdoTipo": {VARIABLE_NAME: "OP_AGREEMENT_TYPE_D", FIELDS_DICT: {}},
        "Operacion.OP_UbicacionPuntoTipo": {VARIABLE_NAME: "OP_LOCATION_POINT_TYPE_D", FIELDS_DICT: {}},
        "Operacion.OP_CondicionPredioTipo": {VARIABLE_NAME: "OP_PARCEL_TYPE_T", FIELDS_DICT: {}},
        "Operacion.OP_DerechoTipo": {VARIABLE_NAME: "OP_RIGHT_TYPE_D", FIELDS_DICT: {}},
        "Operacion.Operacion.OP_Agrupacion_Interesados": {VARIABLE_NAME: "OP_GROUP_PARTY_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.COL_Agrupacion_Interesados.Tipo": "COL_GROUP_PARTY_T_TYPE_F",
            "LADM_COL.LADM_Nucleo.COL_Interesado.Nombre": "COL_PARTY_T_NAME_F",
            "LADM_COL.LADM_Nucleo.COL_Interesado.Espacio_De_Nombres": "COL_PARTY_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.COL_Interesado.Local_Id": "COL_PARTY_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Operacion.Operacion.OP_UnidadConstruccion": {VARIABLE_NAME: "OP_BUILDING_UNIT_T", FIELDS_DICT: {
            "Operacion.Operacion.OP_UnidadConstruccion.Area_Construida": "OP_BUILDING_UNIT_T_BUILT_AREA_F",
            "Operacion.Operacion.OP_UnidadConstruccion.Area_Privada_Construida": "OP_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F",
            "Operacion.Operacion.OP_UnidadConstruccion.Avaluo_Unidad_Construccion": "OP_BUILDING_UNIT_T_BUILDING_UNIT_VALUATION_F",
            "Operacion.Operacion.OP_UnidadConstruccion.Identificador": "OP_BUILDING_UNIT_T_IDENTIFICATION_F",
            "Operacion.Operacion.OP_UnidadConstruccion.Numero_Pisos": "OP_BUILDING_UNIT_T_NUMBER_OF_FLOORS_F",
            "Operacion.Operacion.OP_UnidadConstruccion.Piso_Ubicacion": "OP_BUILDING_UNIT_T_FLOOR_F",
            "Operacion.Operacion.OP_UnidadConstruccion.Uso": "OP_BUILDING_UNIT_T_USE_F",
            "Operacion.Operacion.op_construccion_unidadconstruccion.op_construccion": "OP_BUILDING_UNIT_T_BUILDING_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Dimension": "COL_SPATIAL_UNIT_T_DIMENSION_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Etiqueta": "COL_SPATIAL_UNIT_T_LABEL_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Geometria": "COL_SPATIAL_UNIT_T_GEOMETRY_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie": "COL_SPATIAL_UNIT_T_SURFACE_RELATION_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Espacio_De_Nombres": "COL_SPATIAL_UNIT_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Local_Id": "COL_SPATIAL_UNIT_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Operacion.Operacion.OP_Construccion": {VARIABLE_NAME: "OP_BUILDING_T", FIELDS_DICT: {
            "Operacion.Operacion.OP_Construccion.Area_Construccion": "OP_BUILDING_T_BUILDING_AREA_F",
            "Operacion.Operacion.OP_Construccion.Avaluo_Construccion": "OP_BUILDING_T_BUILDING_VALUATION_F",
            "Operacion.Operacion.OP_Construccion.Numero_Pisos": "OP_BUILDING_T_NUMBER_OF_FLOORS_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Dimension": "COL_SPATIAL_UNIT_T_DIMENSION_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Etiqueta": "COL_SPATIAL_UNIT_T_LABEL_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Geometria": "COL_SPATIAL_UNIT_T_GEOMETRY_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie": "COL_SPATIAL_UNIT_T_SURFACE_RELATION_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Espacio_De_Nombres": "COL_SPATIAL_UNIT_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Local_Id": "COL_SPATIAL_UNIT_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Operacion.Operacion.OP_Derecho": {VARIABLE_NAME: "OP_RIGHT_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_baunitRrr.unidad": "COL_BAUNIT_RRR_T_UNIT_F",
            "Operacion.Operacion.OP_Derecho.Tipo": "OP_RIGHT_T_TYPE_F",
            "LADM_COL.LADM_Nucleo.COL_RRR.Comprobacion_Comparte": "COL_RRR_T_SHARE_CHECK_F",
            "LADM_COL.LADM_Nucleo.COL_RRR.Descripcion": "COL_RRR_T_DESCRIPTION_F",
            "LADM_COL.LADM_Nucleo.COL_RRR.Espacio_De_Nombres": "COL_RRR_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.COL_RRR.Local_Id": "COL_RRR_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.COL_RRR.Uso_Efectivo": "COL_RRR_T_EFFECTIVE_USAGE_F",
            "LADM_COL.LADM_Nucleo.col_rrrInteresado.interesado_Operacion.Operacion.OP_Interesado": "COL_RRR_PARTY_T_OP_PARTY_F",
            "LADM_COL.LADM_Nucleo.col_rrrInteresado.interesado_Operacion.Operacion.OP_Agrupacion_Interesados": "COL_RRR_PARTY_T_OP_GROUP_PARTY_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Operacion.Operacion.OP_FuenteAdministrativa": {VARIABLE_NAME: "OP_ADMINISTRATIVE_SOURCE_T", FIELDS_DICT: {
            "Operacion.Operacion.OP_FuenteAdministrativa.Ente_Emisor": "OP_ADMINISTRATIVE_SOURCE_T_EMITTING_ENTITY_F",
            "Operacion.Operacion.OP_FuenteAdministrativa.Tipo": "OP_ADMINISTRATIVE_SOURCE_T_TYPE_F",
            "LADM_COL.LADM_Nucleo.COL_FuenteAdministrativa.Numero_Fuente": "COL_ADMINISTRATIVE_SOURCE_T_SOURCE_NUMBER_F",
            "LADM_COL.LADM_Nucleo.COL_FuenteAdministrativa.Observacion": "COL_ADMINISTRATIVE_SOURCE_T_OBSERVATION_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Estado_Disponibilidad": "COL_SOURCE_T_AVAILABILITY_STATUS_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Fecha_Documento_Fuente": "COL_SOURCE_T_DATE_DOCUMENT_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Oficialidad": "COL_SOURCE_T_OFFICIAL_F",
            # "LADM_COL.LADM_Nucleo.COL_Fuente.Procedencia": "COL_SOURCE_T_PROVENANCE_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Espacio_De_Nombres": "COL_SOURCE_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Local_Id": "COL_SOURCE_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Tipo_Principal": "COL_SOURCE_T_MAIN_TYPE_F"
        }},
        "Operacion.Operacion.OP_FuenteEspacial": {VARIABLE_NAME: "OP_SPATIAL_SOURCE_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.COL_FuenteEspacial.Tipo": "COL_SPATIAL_SOURCE_T_TYPE_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Estado_Disponibilidad": "COL_SOURCE_T_AVAILABILITY_STATUS_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Fecha_Documento_Fuente": "COL_SOURCE_T_DATE_DOCUMENT_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Oficialidad": "COL_SOURCE_T_OFFICIAL_F",
            # "LADM_COL.LADM_Nucleo.COL_Fuente.Procedencia": "COL_SOURCE_T_PROVENANCE_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Espacio_De_Nombres": "COL_SOURCE_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Local_Id": "COL_SOURCE_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Tipo_Principal": "COL_SOURCE_T_MAIN_TYPE_F"
        }},
        "Operacion.Operacion.OP_Interesado": {VARIABLE_NAME: "OP_PARTY_T", FIELDS_DICT: {
            "Operacion.Operacion.OP_Interesado.Documento_Identidad": "OP_PARTY_T_DOCUMENT_ID_F",
            "Operacion.Operacion.OP_Interesado.Grupo_Etnico": "OP_PARTY_T_ETHNIC_GROUP_F",
            "Operacion.Operacion.OP_Interesado.Primer_Apellido": "OP_PARTY_T_SURNAME_1_F",
            "Operacion.Operacion.OP_Interesado.Primer_Nombre": "OP_PARTY_T_FIRST_NAME_1_F",
            "Operacion.Operacion.OP_Interesado.Razon_Social": "OP_PARTY_T_BUSINESS_NAME_F",
            "Operacion.Operacion.OP_Interesado.Segundo_Apellido": "OP_PARTY_T_SURNAME_2_F",
            "Operacion.Operacion.OP_Interesado.Segundo_Nombre": "OP_PARTY_T_FIRST_NAME_2_F",
            "Operacion.Operacion.OP_Interesado.Sexo": "OP_PARTY_T_GENRE_F",
            "Operacion.Operacion.OP_Interesado.Tipo": "OP_PARTY_T_TYPE_F",
            "Operacion.Operacion.OP_Interesado.Tipo_Documento": "OP_PARTY_T_DOCUMENT_TYPE_F",
            "LADM_COL.LADM_Nucleo.COL_Interesado.Nombre": "COL_PARTY_T_NAME_F",
            "LADM_COL.LADM_Nucleo.COL_Interesado.Espacio_De_Nombres": "COL_PARTY_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.COL_Interesado.Local_Id": "COL_PARTY_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Operacion.Operacion.OP_Lindero": {VARIABLE_NAME: "OP_BOUNDARY_T", FIELDS_DICT: {
            "Operacion.Operacion.OP_Lindero.Longitud": "OP_BOUNDARY_T_LENGTH_F",
            "LADM_COL.LADM_Nucleo.COL_CadenaCarasLimite.Espacio_De_Nombres": "COL_BFS_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.COL_CadenaCarasLimite.Local_Id": "COL_BFS_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.COL_CadenaCarasLimite.Geometria": "COL_BFS_T_GEOMETRY_F",
            "LADM_COL.LADM_Nucleo.COL_CadenaCarasLimite.Localizacion_Textual": "COL_BFS_T_TEXTUAL_LOCATION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Operacion.Operacion.OP_Predio": {VARIABLE_NAME: "OP_PARCEL_T", FIELDS_DICT: {
            "Operacion.Operacion.OP_Predio.Avaluo_Predio": "OP_PARCEL_T_VALUATION_F",
            "Operacion.Operacion.OP_Predio.Codigo_ORIP": "OP_PARCEL_T_ORIP_CODE_F",
            "Operacion.Operacion.OP_Predio.Condicion_Predio": "OP_PARCEL_T_PARCEL_TYPE_F",
            "Operacion.Operacion.OP_Predio.Departamento": "OP_PARCEL_T_DEPARTMENT_F",
            "Operacion.Operacion.OP_Predio.Direccion": "OP_PARCEL_T_ADDRESS_F",
            "Operacion.Operacion.OP_Predio.Matricula_Inmobiliaria": "OP_PARCEL_T_FMI_F",
            "Operacion.Operacion.OP_Predio.Municipio": "OP_PARCEL_T_MUNICIPALITY_F",
            "Operacion.Operacion.OP_Predio.Numero_Predial": "OP_PARCEL_T_PARCEL_NUMBER_F",
            "Operacion.Operacion.OP_Predio.Numero_Predial_Anterior": "OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F",
            "Operacion.Operacion.OP_Predio.NUPRE": "OP_PARCEL_T_NUPRE_F",
            "Operacion.Operacion.OP_Predio.Tipo": "OP_PARCEL_T_TYPE_F",
            "LADM_COL.LADM_Nucleo.COL_BAUnit.Nombre": "COL_BAUNIT_T_NAME_F",
            "LADM_COL.LADM_Nucleo.COL_BAUnit.Espacio_De_Nombres": "COL_BAUNIT_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.COL_BAUnit.Local_Id": "COL_BAUNIT_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Operacion.Operacion.op_predio_copropiedad": {VARIABLE_NAME: "OP_COPROPERTY_T", FIELDS_DICT: {}},
        "Operacion.Operacion.op_predio_insumos_operacion": {VARIABLE_NAME: "OP_OPERATION_SUPPLIES_T", FIELDS_DICT: {}},
        "Operacion.Operacion.OP_PuntoControl": {VARIABLE_NAME: "OP_CONTROL_POINT_T", FIELDS_DICT: {
            "Operacion.Operacion.OP_PuntoControl.Exactitud_Horizontal": "OP_CONTROL_POINT_T_HORIZONTAL_ACCURACY_F",
            "Operacion.Operacion.OP_PuntoControl.Exactitud_Vertical": "OP_CONTROL_POINT_T_VERTICAL_ACCURACY_F",
            "Operacion.Operacion.OP_PuntoControl.ID_Punto_Control": "OP_CONTROL_POINT_T_ID_F",
            "Operacion.Operacion.OP_PuntoControl.PuntoTipo": "OP_CONTROL_POINT_T_POINT_TYPE_F",
            "Operacion.Operacion.OP_PuntoControl.Tipo_Punto_Control": "OP_CONTROL_POINT_T_CONTROL_POINT_TYPE_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.Posicion_Interpolacion": "COL_POINT_T_INTERPOLATION_POSITION_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.Geometria": "COL_POINT_T_ORIGINAL_LOCATION_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.MetodoProduccion": "COL_POINT_T_PRODUCTION_METHOD_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.Monumentacion": "COL_POINT_T_MONUMENTATION_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.Espacio_De_Nombres": "COL_POINT_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.Local_Id": "COL_POINT_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Operacion.Operacion.OP_PuntoLevantamiento": {VARIABLE_NAME: "OP_SURVEY_POINT_T", FIELDS_DICT: {
            "Operacion.Operacion.OP_PuntoLevantamiento.Exactitud_Horizontal": "OP_SURVEY_POINT_T_HORIZONTAL_ACCURACY_F",
            "Operacion.Operacion.OP_PuntoLevantamiento.Exactitud_Vertical": "OP_SURVEY_POINT_T_VERTICAL_ACCURACY_F",
            "Operacion.Operacion.OP_PuntoLevantamiento.Fotoidentificacion": "OP_SURVEY_POINT_T_PHOTO_IDENTIFICATION_F",
            "Operacion.Operacion.OP_PuntoLevantamiento.ID_Punto_Levantamiento": "OP_SURVEY_POINT_T_ID_F",
            "Operacion.Operacion.OP_PuntoLevantamiento.PuntoTipo": "OP_SURVEY_POINT_T_POINT_TYPE_F",
            "Operacion.Operacion.OP_PuntoLevantamiento.Tipo_Punto_Levantamiento": "OP_SURVEY_POINT_T_SURVEY_POINT_TYPE_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.Posicion_Interpolacion": "COL_POINT_T_INTERPOLATION_POSITION_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.Geometria": "COL_POINT_T_ORIGINAL_LOCATION_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.MetodoProduccion": "COL_POINT_T_PRODUCTION_METHOD_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.Monumentacion": "COL_POINT_T_MONUMENTATION_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.Espacio_De_Nombres": "COL_POINT_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.Local_Id": "COL_POINT_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Operacion.Operacion.OP_PuntoLindero": {VARIABLE_NAME: "OP_BOUNDARY_POINT_T", FIELDS_DICT: {
            "Operacion.Operacion.OP_PuntoLindero.Acuerdo": "OP_BOUNDARY_POINT_T_AGREEMENT_F",
            "Operacion.Operacion.OP_PuntoLindero.Exactitud_Horizontal": "OP_BOUNDARY_POINT_T_HORIZONTAL_ACCURACY_F",
            "Operacion.Operacion.OP_PuntoLindero.Exactitud_Vertical": "OP_BOUNDARY_POINT_T_VERTICAL_ACCURACY_F",
            "Operacion.Operacion.OP_PuntoLindero.Fotoidentificacion": "OP_BOUNDARY_POINT_T_PHOTO_IDENTIFICATION_F",
            "Operacion.Operacion.OP_PuntoLindero.ID_Punto_Lindero": "OP_BOUNDARY_POINT_T_ID_F",
            "Operacion.Operacion.OP_PuntoLindero.PuntoTipo": "OP_BOUNDARY_POINT_T_POINT_TYPE_F",
            "Operacion.Operacion.OP_PuntoLindero.Ubicacion_Punto": "OP_BOUNDARY_POINT_T_POINT_LOCATION_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.Posicion_Interpolacion": "COL_POINT_T_INTERPOLATION_POSITION_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.Geometria": "COL_POINT_T_ORIGINAL_LOCATION_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.MetodoProduccion": "COL_POINT_T_PRODUCTION_METHOD_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.Monumentacion": "COL_POINT_T_MONUMENTATION_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.Espacio_De_Nombres": "COL_POINT_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.Local_Id": "COL_POINT_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Operacion.Operacion.OP_Restriccion": {VARIABLE_NAME: "OP_RESTRICTION_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_baunitRrr.unidad": "COL_BAUNIT_RRR_T_UNIT_F",
            "Operacion.Operacion.OP_Restriccion.Tipo": "OP_RESTRICTION_T_TYPE_F",
            "LADM_COL.LADM_Nucleo.COL_RRR.Comprobacion_Comparte": "COL_RRR_T_SHARE_CHECK_F",
            "LADM_COL.LADM_Nucleo.COL_RRR.Descripcion": "COL_RRR_T_DESCRIPTION_F",
            "LADM_COL.LADM_Nucleo.COL_RRR.Espacio_De_Nombres": "COL_RRR_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.COL_RRR.Local_Id": "COL_RRR_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.COL_RRR.Uso_Efectivo": "COL_RRR_T_EFFECTIVE_USAGE_F",
            "LADM_COL.LADM_Nucleo.col_rrrInteresado.interesado_Operacion.Operacion.OP_Interesado": "COL_RRR_PARTY_T_OP_PARTY_F",
            "LADM_COL.LADM_Nucleo.col_rrrInteresado.interesado_Operacion.Operacion.OP_Agrupacion_Interesados": "COL_RRR_PARTY_T_OP_GROUP_PARTY_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Operacion.Operacion.OP_ServidumbrePaso": {VARIABLE_NAME: "OP_RIGHT_OF_WAY_T", FIELDS_DICT: {
            "Operacion.Operacion.OP_ServidumbrePaso.Area_Servidumbre": "OP_RIGHT_OF_WAY_T_RIGHT_OF_WAY_AREA_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Dimension": "COL_SPATIAL_UNIT_T_DIMENSION_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Etiqueta": "COL_SPATIAL_UNIT_T_LABEL_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Geometria": "COL_SPATIAL_UNIT_T_GEOMETRY_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie": "COL_SPATIAL_UNIT_T_SURFACE_RELATION_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Espacio_De_Nombres": "COL_SPATIAL_UNIT_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Local_Id": "COL_SPATIAL_UNIT_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Operacion.Operacion.OP_Terreno": {VARIABLE_NAME: "OP_PLOT_T", FIELDS_DICT: {
            "Operacion.Operacion.OP_Terreno.Area_Terreno": "OP_PLOT_T_PLOT_AREA_F",
            "Operacion.Operacion.OP_Terreno.Avaluo_Terreno": "OP_PLOT_T_PLOT_VALUATION_F",
            "Operacion.Operacion.OP_Terreno.Geometria": "OP_PLOT_T_GEOMETRY_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Dimension": "COL_SPATIAL_UNIT_T_DIMENSION_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Etiqueta": "COL_SPATIAL_UNIT_T_LABEL_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie": "COL_SPATIAL_UNIT_T_SURFACE_RELATION_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Espacio_De_Nombres": "COL_SPATIAL_UNIT_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Local_Id": "COL_SPATIAL_UNIT_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Operacion.OP_FuenteAdministrativaTipo": {VARIABLE_NAME: "OP_ADMINISTRATIVE_SOURCE_TYPE_D", FIELDS_DICT: {}},
        "Operacion.OP_GrupoEtnicoTipo": {VARIABLE_NAME: "OP_ETHNIC_GROUP_TYPE", FIELDS_DICT: {}},
        "Operacion.OP_InteresadoDocumentoTipo": {VARIABLE_NAME: "OP_PARTY_DOCUMENT_TYPE_D", FIELDS_DICT: {}},
        "Operacion.OP_InteresadoTipo": {VARIABLE_NAME: "OP_PARTY_TYPE_D", FIELDS_DICT: {}},
        "Operacion.OP_PredioTipo": {VARIABLE_NAME: "OP_PARCEL_TYPE_D", FIELDS_DICT: {}},
        "Operacion.OP_PuntoControlTipo": {VARIABLE_NAME: "OP_CONTROL_POINT_TYPE_D", FIELDS_DICT: {}},
        "Operacion.OP_PuntoLevTipo": {VARIABLE_NAME: "OP_SURVEY_POINT_TYPE_D", FIELDS_DICT: {}},
        "Operacion.OP_PuntoTipo": {VARIABLE_NAME: "OP_POINT_TYPE_D", FIELDS_DICT: {}},
        "Operacion.OP_RestriccionTipo": {VARIABLE_NAME: "OP_RESTRICTION_TYPE_D", FIELDS_DICT: {}},
        "Operacion.OP_SexoTipo": {VARIABLE_NAME: "OP_GENRE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.OM_Observacion": {VARIABLE_NAME: "OM_OBSERVATION_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.COL_FuenteEspacial.Mediciones": "COL_SPATIAL_SOURCE_T_MEASUREMENTS_F"
        }},
    }

    def initialize_table_and_field_names(self, dict_names):
        """
        Update class variables (table and field names) according to a dictionary of names coming from a DB connection.
        This function should be called when a new DB connection is established for making all classes in the plugin able
        to access current DB connection names.

        :param dict_names: Expected dict with key as iliname (fully qualified object name in the model) with no version
                           info, and value as sqlname (produced by ili2db).
        :return: True if anything is updated, False otherwise.
        """
        any_update = False
        debug = False
        if dict_names:
            if T_ID not in dict_names or DISPLAY_NAME not in dict_names or ILICODE not in dict_names or DESCRIPTION not in dict_names:
                # TODO: Logger "dict_names is not properly built, at least one of these required fields was not found T_ID, DISPLAY_NAME, ILICODE, DESCRIPTION."
                return False

            for table_key, attrs in self.TABLE_DICT.items():
                # debug = table_key == 'Operacion.Operacion.OP_UnidadConstruccion'

                if table_key in dict_names:
                    setattr(self, attrs[VARIABLE_NAME], dict_names[table_key][TABLE_NAME])
                    any_update = True
                    if debug:
                        print("Field Names: ", attrs[FIELDS_DICT])
                    for field_key, field_variable in attrs[FIELDS_DICT].items():
                        if field_key in dict_names[table_key]:
                            if debug:
                                print(field_variable, dict_names[table_key][field_key])
                            setattr(self, field_variable, dict_names[table_key][field_key])


            # Required fields mapped in a custom way
            self.T_ID_F = dict_names[T_ID] if T_ID in dict_names else None
            self.ILICODE_F = dict_names[ILICODE] if ILICODE in dict_names else None
            self.DESCRIPTION_F = dict_names[DESCRIPTION] if DESCRIPTION in dict_names else None
            self.DISPLAY_NAME_F = dict_names[DISPLAY_NAME] if DISPLAY_NAME in dict_names else None

        # set init custom variables
        self.set_custom_variables()

        return any_update

    def set_custom_variables(self):
        self.OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V = "Persona_Natural"
        self.OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V = "Persona_Juridica"
        self.OP_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V = "NIT"
        self.TABLE_PROP_ASSOCIATION = "ASSOCIATION"
        self.TABLE_PROP_DOMAIN = "ENUM"
        self.TABLE_PROP_STRUCTURE = "STRUCTURE"

        """
        PARCEL TYPE
        """
        self.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY = "NPH"
        self.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT = "PH.Matriz"
        self.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT = "PH.Unidad_Predial"
        self.PARCEL_TYPE_CONDOMINIUM_PARENT = "Condominio.Matriz"
        self.PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT = "Condominio.Unidad_Predial"
        self.PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA = "Mejora.PH"
        self.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA = "Mejora.NPH"
        self.PARCEL_TYPE_CEMETERY_PARENT = "Parque_Cementerio.Matriz"
        self.PARCEL_TYPE_CEMETERY_PARCEL_UNIT = "Parque_Cementerio.Unidad_Predial"
        self.PARCEL_TYPE_ROAD = "Via"
        self.PARCEL_TYPE_PUBLIC_USE = "Bien_Uso_Publico"

        """
        LADM PACKAGES
        """
        self.SURVEYING_AND_REPRESENTATION_PACKAGE = "Topografía y Representación"
        self.SPATIAL_UNIT_PACKAGE = "Unidad Espacial"
        self.BA_UNIT_PACKAGE = "Unidad Administrativa"
        self.RRR_PACKAGE = "Derechos, Restricciones y Responsabilidades"
        self.PARTY_PACKAGE = "Interesados"
        self.SOURCE_PACKAGE = "Fuentes"

    def test_names(self, models):
        """
        Test whether required table/field names are present.

        :param models: List of model prefixes present in the db
        :return: Tuple (bool: Names are valid or not, string: Message to indicate what exactly failed)
        """
        required_names = ["T_ID_F",
                          "ILICODE_F",
                          "DESCRIPTION_F",
                          "DISPLAY_NAME_F"]

        for k, v in self.TABLE_DICT.items():
            if k.split(".")[0] in models:
                required_names.append(v[VARIABLE_NAME])
                for k1, v1 in v[FIELDS_DICT].items():
                    if k1.split(".")[0] in models:
                        required_names.append(v1)

        print(required_names)
        names_not_found = list()
        for required_name in required_names:
            if getattr(self, required_name) is None:
                names_not_found.append(required_name)

        print("Names not found:", set(names_not_found))
        if names_not_found:
            return (False, "Name '{}' was not found!".format(names_not_found[0]))

        return (True, "")

    def get_layer_sets(self):
        """
        Configure layer sets to appear in the load layers dialog
        Each layer set is a key-value pair where key is the name of the layer set
        and the value is a list of layers to load
        """
        return {
            'Datos de Interesados': [
                self.OP_PARTY_T,
                self.OP_GENRE_D,
                self.OP_PARTY_DOCUMENT_TYPE_D,
                self.OP_PARTY_TYPE_D
            ],
            'Derechos': [
                self.OP_PARTY_T,
                self.OP_PARCEL_T,
                self.OP_ADMINISTRATIVE_SOURCE_T,
                self.EXT_ARCHIVE_S,
                self.OP_GROUP_PARTY_T,
                self.OP_RIGHT_T
            ],
            'Punto Lindero, Lindero y Terreno': [
                self.OP_BOUNDARY_POINT_T,
                self.OP_BOUNDARY_T,
                self.OP_PLOT_T,
                self.MORE_BFS_T,
                self.LESS_BFS_T,
                self.POINT_BFS_T
            ]
        }

    @staticmethod
    def get_restriction_type_d_right_of_way_ilicode_value():
        return "Servidumbre"

    def get_constraint_types_of_parcels(self):
        # Operations:
        # 1 = One and only one feature must be selected
        # + = One or more features must be selected
        # * = Optional, i.e., zero or more features could be selected
        # None = Won't be stored as a related feature (selected features will be ignored)
        return {
            self.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY: {
                self.OP_PLOT_T: 1,
                self.OP_BUILDING_T: '*',
                self.OP_BUILDING_UNIT_T: '*'
            },
            self.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT: {
                self.OP_PLOT_T: 1,
                self.OP_BUILDING_T: '*',
                self.OP_BUILDING_UNIT_T: None
            },
            self.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT: {
                self.OP_PLOT_T: None,
                self.OP_BUILDING_T: None,
                self.OP_BUILDING_UNIT_T: '+'
            },
            self.PARCEL_TYPE_CONDOMINIUM_PARENT: {
                self.OP_PLOT_T: 1,
                self.OP_BUILDING_T: '*',
                self.OP_BUILDING_UNIT_T: None
            },
            self.PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT: {
                self.OP_PLOT_T: 1,
                self.OP_BUILDING_T: '*',
                self.OP_BUILDING_UNIT_T: None
            },
            self.PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA: {
                self.OP_PLOT_T: None,
                self.OP_BUILDING_T: '*',
                self.OP_BUILDING_UNIT_T: '+'
            },
            self.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA: {
                self.OP_PLOT_T: None,
                self.OP_BUILDING_T: '*',
                self.OP_BUILDING_UNIT_T: '+'
            },
            self.PARCEL_TYPE_CEMETERY_PARENT: {
                self.OP_PLOT_T: 1,
                self.OP_BUILDING_T: '*',
                self.OP_BUILDING_UNIT_T: None
            },
            self.PARCEL_TYPE_CEMETERY_PARCEL_UNIT: {
                self.OP_PLOT_T: 1,
                self.OP_BUILDING_T: None,
                self.OP_BUILDING_UNIT_T: None
            },
            self.PARCEL_TYPE_ROAD: {
                self.OP_PLOT_T: 1,
                self.OP_BUILDING_T: None,
                self.OP_BUILDING_UNIT_T: None
            },
            self.PARCEL_TYPE_PUBLIC_USE: {
                self.OP_PLOT_T: 1,
                self.OP_BUILDING_T: '*',
                self.OP_BUILDING_UNIT_T: None
            }
        }

    def get_dict_plural(self):
        """
        PLURAL WORDS, FOR DISPLAY PURPOSES
        """
        return {
            self.OP_PLOT_T: "Terrenos",
            self.OP_PARCEL_T: "Predios",
            self.OP_BUILDING_T: "Construcciones",
            self.OP_BUILDING_UNIT_T: "Unidades de Construcción",
            self.EXT_ADDRESS_S: "Direcciones",
            self.OP_PARTY_T: "Interesados",
            self.OP_GROUP_PARTY_T: "Agrupación de interesados",
            self.OP_RIGHT_T: "Derechos",
            self.OP_RESTRICTION_T: "Restricciones",
            self.OP_ADMINISTRATIVE_SOURCE_T: "Fuentes Administrativas",
            self.OP_SPATIAL_SOURCE_T: "Fuentes Espaciales",
            self.OP_BOUNDARY_T: "Linderos",
            self.OP_BOUNDARY_POINT_T: "Puntos de Lindero",
            self.OP_SURVEY_POINT_T: "Puntos de Levantamiento"
        }

    def get_dict_package_icon(self):
        """
        LADM PACKAGE ICONS
        """
        return {
            # Resources don't seem to be initialized at this point, so return path and build icon when needed
            self.SURVEYING_AND_REPRESENTATION_PACKAGE: ":/Asistente-LADM_COL/resources/images/surveying.png",
            self.SPATIAL_UNIT_PACKAGE: ":/Asistente-LADM_COL/resources/images/spatial_unit.png",
            self.BA_UNIT_PACKAGE: ":/Asistente-LADM_COL/resources/images/ba_unit.png",
            self.RRR_PACKAGE: ":/Asistente-LADM_COL/resources/images/rrr.png",
            self.PARTY_PACKAGE: ":/Asistente-LADM_COL/resources/images/party.png",
            self.SOURCE_PACKAGE: ":/Asistente-LADM_COL/resources/images/source.png"
        }

    def get_dict_table_package(self):
        return {
            self.OP_PARCEL_T: self.BA_UNIT_PACKAGE,
            self.OP_PLOT_T: self.SPATIAL_UNIT_PACKAGE,
            self.OP_BUILDING_T: self.SPATIAL_UNIT_PACKAGE,
            self.OP_BUILDING_UNIT_T: self.SPATIAL_UNIT_PACKAGE,
            self.OP_RIGHT_OF_WAY_T: self.SPATIAL_UNIT_PACKAGE,
            self.OP_PARTY_T: self.PARTY_PACKAGE,
            self.OP_GROUP_PARTY_T: self.PARTY_PACKAGE,
            self.OP_RIGHT_T: self.RRR_PACKAGE,
            self.OP_RESTRICTION_T: self.RRR_PACKAGE,
            self.OP_ADMINISTRATIVE_SOURCE_T: self.SOURCE_PACKAGE,
            self.OP_SPATIAL_SOURCE_T: self.SOURCE_PACKAGE,
            self.OP_BOUNDARY_POINT_T: self.SURVEYING_AND_REPRESENTATION_PACKAGE,
            self.OP_SURVEY_POINT_T: self.SURVEYING_AND_REPRESENTATION_PACKAGE,
            self.OP_BOUNDARY_T: self.SURVEYING_AND_REPRESENTATION_PACKAGE
        }

    def get_logic_consistency_tables(self):
        """
        we define the minimum structure of a table to validate that there are no repeated records
        """
        return {
            # Geometric tables
            self.OP_BOUNDARY_POINT_T: [self.OP_BOUNDARY_POINT_T_AGREEMENT_F,
                                       self.OP_BOUNDARY_POINT_T_PHOTO_IDENTIFICATION_F,
                                       self.OP_BOUNDARY_POINT_T_POINT_LOCATION_F,
                                       self.OP_BOUNDARY_POINT_T_VERTICAL_ACCURACY_F,
                                       self.OP_BOUNDARY_POINT_T_HORIZONTAL_ACCURACY_F,
                                       self.COL_POINT_T_INTERPOLATION_POSITION_F,
                                       self.COL_POINT_T_MONUMENTATION_F,
                                       self.COL_POINT_T_PRODUCTION_METHOD_F,
                                       self.OP_BOUNDARY_POINT_T_POINT_TYPE_F,
                                       self.COL_POINT_T_ORIGINAL_LOCATION_F],
            self.OP_SURVEY_POINT_T: [self.OP_SURVEY_POINT_T_SURVEY_POINT_TYPE_F,
                                     self.OP_SURVEY_POINT_T_PHOTO_IDENTIFICATION_F,
                                     self.OP_SURVEY_POINT_T_VERTICAL_ACCURACY_F,
                                     self.OP_SURVEY_POINT_T_HORIZONTAL_ACCURACY_F,
                                     self.COL_POINT_T_INTERPOLATION_POSITION_F,
                                     self.COL_POINT_T_PRODUCTION_METHOD_F,
                                     self.COL_POINT_T_MONUMENTATION_F,
                                     self.OP_SURVEY_POINT_T_POINT_TYPE_F,
                                     self.COL_POINT_T_ORIGINAL_LOCATION_F],
            self.OP_CONTROL_POINT_T: [self.OP_CONTROL_POINT_T_VERTICAL_ACCURACY_F,
                                      self.OP_CONTROL_POINT_T_HORIZONTAL_ACCURACY_F,
                                      self.OP_CONTROL_POINT_T_ID_F,
                                      self.COL_POINT_T_INTERPOLATION_POSITION_F,
                                      self.COL_POINT_T_MONUMENTATION_F,
                                      self.OP_CONTROL_POINT_T_POINT_TYPE_F,
                                      self.COL_POINT_T_ORIGINAL_LOCATION_F],
            self.OP_BOUNDARY_T: [self.OP_BOUNDARY_T_LENGTH_F,
                                 self.COL_BFS_T_TEXTUAL_LOCATION_F,
                                 self.COL_BFS_T_GEOMETRY_F],
            self.OP_PLOT_T: [self.OP_PLOT_T_PLOT_AREA_F,
                             self.OP_PLOT_T_PLOT_VALUATION_F,
                             self.COL_SPATIAL_UNIT_T_DIMENSION_F,
                             self.COL_SPATIAL_UNIT_T_LABEL_F,
                             self.COL_SPATIAL_UNIT_T_SURFACE_RELATION_F,
                             self.OP_PLOT_T_GEOMETRY_F],
            self.OP_BUILDING_T: [self.OP_BUILDING_T_BUILDING_VALUATION_F,
                                 self.OP_BUILDING_T_BUILDING_AREA_F,
                                 self.COL_SPATIAL_UNIT_T_DIMENSION_F,
                                 self.COL_SPATIAL_UNIT_T_LABEL_F,
                                 self.COL_SPATIAL_UNIT_T_SURFACE_RELATION_F,
                                 self.COL_SPATIAL_UNIT_T_GEOMETRY_F],
            self.OP_BUILDING_UNIT_T: [self.OP_BUILDING_UNIT_T_BUILDING_UNIT_VALUATION_F,
                                      self.OP_BUILDING_UNIT_T_NUMBER_OF_FLOORS_F,
                                      self.OP_BUILDING_UNIT_T_BUILT_AREA_F,
                                      self.OP_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F,
                                      self.OP_BUILDING_UNIT_T_BUILDING_F,
                                      self.COL_SPATIAL_UNIT_T_DIMENSION_F,
                                      self.COL_SPATIAL_UNIT_T_LABEL_F,
                                      self.COL_SPATIAL_UNIT_T_SURFACE_RELATION_F,
                                      self.COL_SPATIAL_UNIT_T_GEOMETRY_F],
            # Alphanumeric tables
            self.OP_PARTY_T: [self.OP_PARTY_T_DOCUMENT_ID_F,
                              self.OP_PARTY_T_DOCUMENT_TYPE_F],
            self.OP_PARCEL_T: [self.OP_PARCEL_T_DEPARTMENT_F,
                               self.OP_PARCEL_T_MUNICIPALITY_F,
                               self.OP_PARCEL_T_NUPRE_F,
                               self.OP_PARCEL_T_FMI_F,
                               self.OP_PARCEL_T_PARCEL_NUMBER_F,
                               self.OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F,
                               self.OP_PARCEL_T_VALUATION_F,
                               self.COL_BAUNIT_T_NAME_F,
                               self.OP_PARCEL_T_TYPE_F],
            self.OP_RIGHT_T: [self.OP_RIGHT_T_TYPE_F,
                              self.COL_RRR_T_DESCRIPTION_F,
                              self.COL_RRR_T_SHARE_CHECK_F,
                              self.COL_RRR_T_EFFECTIVE_USAGE_F,
                              self.COL_RRR_T_NAMESPACE_F,
                              self.COL_RRR_PARTY_T_OP_GROUP_PARTY_F,
                              self.COL_RRR_PARTY_T_OP_PARTY_F,
                              self.COL_BAUNIT_RRR_T_UNIT_F],
            self.OP_RESTRICTION_T: [self.OP_RESTRICTION_T_TYPE_F,
                                    self.COL_RRR_T_DESCRIPTION_F,
                                    self.COL_RRR_T_SHARE_CHECK_F,
                                    self.COL_RRR_T_EFFECTIVE_USAGE_F,
                                    self.COL_RRR_PARTY_T_OP_GROUP_PARTY_F,
                                    self.COL_RRR_PARTY_T_OP_PARTY_F,
                                    self.COL_BAUNIT_RRR_T_UNIT_F],
            self.OP_ADMINISTRATIVE_SOURCE_T: [self.OP_ADMINISTRATIVE_SOURCE_T_EMITTING_ENTITY_F,
                                              self.COL_ADMINISTRATIVE_SOURCE_T_SOURCE_NUMBER_F,
                                              self.COL_ADMINISTRATIVE_SOURCE_T_OBSERVATION_F,
                                              self.OP_ADMINISTRATIVE_SOURCE_T_TYPE_F,
                                              self.COL_SOURCE_T_DATE_DOCUMENT_F,
                                              self.COL_SOURCE_T_AVAILABILITY_STATUS_F,
                                              self.COL_SOURCE_T_MAIN_TYPE_F,
                                              self.COL_SOURCE_T_OFFICIAL_F]
        }

    def get_custom_widget_configuration(self):
        return {
            self.EXT_ARCHIVE_S: {
                'type': 'ExternalResource',
                'config': {
                    'PropertyCollection': {
                        'properties': {},
                        'name': NULL,
                        'type': 'collection'
                    },
                    'UseLink': True,
                    'FullUrl': True,
                    'FileWidget': True,
                    'DocumentViewer': 0,
                    'RelativeStorage': 0,
                    'StorageMode': 0,
                    'FileWidgetButton': True,
                    'DocumentViewerHeight': 0,
                    'DocumentViewerWidth': 0,
                    'FileWidgetFilter': ''
                }
            }
        }

    def get_custom_read_only_fields(self):
        # Read only fields might be declared in two scenarios:
        #   1. As soon as the layer is loaded (e.g., DEPARTMENT_FIELD)
        #   2. Only for a wizard (e.g., PARCEL_TYPE)
        # WARNING: Both modes are exclusive, if you list a field in 1, DO NOT do it in 2. and viceversa!
        return {
            self.OP_PARCEL_T: [self.OP_PARCEL_T_DEPARTMENT_F,
                               self.OP_PARCEL_T_MUNICIPALITY_F]  # list of fields of the layer to block its edition
        }

    def get_layer_variables(self):
        return {
            self.OP_BUILDING_T: {
                "qgis_25d_angle": 90,
                "qgis_25d_height": 1
            },
            self.OP_BUILDING_UNIT_T: {
                "qgis_25d_angle": 90,
                "qgis_25d_height": '"{}" * 2.5'.format(self.OP_BUILDING_UNIT_T_NUMBER_OF_FLOORS_F)
            }
        }

    def get_dict_automatic_values(self):
        return {
            self.OP_BOUNDARY_T: [{self.OP_BOUNDARY_T_LENGTH_F: "$length"}],
            self.OP_PARTY_T: [{
                self.COL_PARTY_T_NAME_F: "regexp_replace(regexp_replace(regexp_replace(concat({}, ' ', {}, ' ', {}, ' ', {}, ' ', {}, ' ', {}), '\\\\s+', ' '), '^\\\\s+', ''), '\\\\s+$', '')".format(
                    self.OP_PARTY_T_DOCUMENT_ID_F,
                    self.OP_PARTY_T_SURNAME_1_F,
                    self.OP_PARTY_T_SURNAME_2_F,
                    self.OP_PARTY_T_FIRST_NAME_1_F,
                    self.OP_PARTY_T_FIRST_NAME_2_F,
                    self.OP_PARTY_T_BUSINESS_NAME_F)}],
            self.OP_PARCEL_T: [
                {self.OP_PARCEL_T_DEPARTMENT_F: 'substr("{}", 0, 2)'.format(self.OP_PARCEL_T_PARCEL_NUMBER_F)},
                {self.OP_PARCEL_T_MUNICIPALITY_F: 'substr("{}", 3, 3)'.format(self.OP_PARCEL_T_PARCEL_NUMBER_F)}]
        }

    def get_dict_display_expressions(self):
        return {
            self.COL_PARTY_T_NAME_F: "regexp_replace(regexp_replace(regexp_replace(concat({}, ' ', {}, ' ', {}, ' ', {}, ' ', {}, ' ', {}), '\\\\s+', ' '), '^\\\\s+', ''), '\\\\s+$', '')".format(
                self.OP_PARTY_T_DOCUMENT_ID_F,
                self.OP_PARTY_T_SURNAME_1_F,
                self.OP_PARTY_T_SURNAME_2_F,
                self.OP_PARTY_T_FIRST_NAME_1_F,
                self.OP_PARTY_T_FIRST_NAME_2_F,
                self.OP_PARTY_T_BUSINESS_NAME_F),
            self.OP_PARCEL_T: "concat({}, ' - ', {}, ' - ', {})".format(self.T_ID_F, self.OP_PARCEL_T_PARCEL_NUMBER_F, self.OP_PARCEL_T_FMI_F),
            self.OP_GROUP_PARTY_T: "concat({}, ' - ', {})".format(self.T_ID_F, self.COL_PARTY_T_NAME_F),
            self.OP_BUILDING_T: '"{}"  || \' \' ||  "{}"'.format(self.COL_SPATIAL_UNIT_T_NAMESPACE_F, self.T_ID_F)
        }

    def get_layer_constraints(self):
        return  {
            self.OP_PARCEL_T: {
                self.OP_PARCEL_T_TYPE_F: {
                    'expression': """
                                    CASE
                                        WHEN  "{OP_PARCEL_T_TYPE_F}" =  get_domain_code_from_value('{OP_PARCEL_TYPE_T}', '{PARCEL_TYPE_NO_HORIZONTAL_PROPERTY}', True, False) THEN
                                            num_selected('{OP_PLOT_T}') = 1 AND num_selected('{OP_BUILDING_UNIT_T}') = 0
                                        WHEN  "{OP_PARCEL_T_TYPE_F}" IN  (get_domain_code_from_value('{OP_PARCEL_TYPE_T}', '{PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT}', True, False),
                                                                          get_domain_code_from_value('{OP_PARCEL_TYPE_T}', '{PARCEL_TYPE_CONDOMINIUM_PARENT}', True, False),
                                                                          get_domain_code_from_value('{OP_PARCEL_TYPE_T}', '{PARCEL_TYPE_CEMETERY_PARENT}', True, False),
                                                                          get_domain_code_from_value('{OP_PARCEL_TYPE_T}', '{PARCEL_TYPE_PUBLIC_USE}', True, False),
                                                                          get_domain_code_from_value('{OP_PARCEL_TYPE_T}', '{PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT}', True, False)) THEN
                                            num_selected('{OP_PLOT_T}') = 1 AND num_selected('{OP_BUILDING_UNIT_T}') = 0
                                        WHEN  "{OP_PARCEL_T_TYPE_F}" IN  (get_domain_code_from_value('{OP_PARCEL_TYPE_T}', '{PARCEL_TYPE_ROAD}', True, False),
                                                                          get_domain_code_from_value('{OP_PARCEL_TYPE_T}', '{PARCEL_TYPE_CEMETERY_PARCEL_UNIT}', True, False)) THEN
                                            num_selected('{OP_PLOT_T}') = 1 AND num_selected('{OP_BUILDING_UNIT_T}') = 0 AND num_selected('{OP_BUILDING_T}') = 0
                                        WHEN  "{OP_PARCEL_T_TYPE_F}" = get_domain_code_from_value('{OP_PARCEL_TYPE_T}', '{PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT}', True, False) THEN
                                            num_selected('{OP_PLOT_T}') = 0 AND num_selected('{OP_BUILDING_UNIT_T}') != 0 AND num_selected('{OP_BUILDING_T}') = 0
                                        WHEN  "{OP_PARCEL_T_TYPE_F}" IN (get_domain_code_from_value('{OP_PARCEL_TYPE_T}', '{PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA}', True, False),
                                                                         get_domain_code_from_value('{OP_PARCEL_TYPE_T}', '{PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA}', True, False)) THEN
                                            num_selected('{OP_PLOT_T}') = 0 AND num_selected('{OP_BUILDING_UNIT_T}') = 0 AND num_selected('{OP_BUILDING_T}') = 1
                                        ELSE
                                            TRUE
                                    END""".format(OP_PARCEL_T_TYPE_F=self.OP_PARCEL_T_TYPE_F,
                                                  OP_PARCEL_TYPE_T=self.OP_PARCEL_TYPE_T,
                                                  OP_PLOT_T=self.OP_PLOT_T,
                                                  OP_BUILDING_T=self.OP_BUILDING_T,
                                                  OP_BUILDING_UNIT_T=self.OP_BUILDING_UNIT_T,
                                                  PARCEL_TYPE_NO_HORIZONTAL_PROPERTY=self.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY,
                                                  PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT=self.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT,
                                                  PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT=self.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT,
                                                  PARCEL_TYPE_CONDOMINIUM_PARENT=self.PARCEL_TYPE_CONDOMINIUM_PARENT,
                                                  PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT=self.PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT,
                                                  PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA=self.PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA,
                                                  PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA=self.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA,
                                                  PARCEL_TYPE_CEMETERY_PARENT=self.PARCEL_TYPE_CEMETERY_PARENT,
                                                  PARCEL_TYPE_CEMETERY_PARCEL_UNIT=self.PARCEL_TYPE_CEMETERY_PARCEL_UNIT,
                                                  PARCEL_TYPE_ROAD=self.PARCEL_TYPE_ROAD,
                                                  PARCEL_TYPE_PUBLIC_USE=self.PARCEL_TYPE_PUBLIC_USE),
                    'description': 'La parcela debe tener una o varias unidades espaciales asociadas. Verifique las reglas '
                    # ''Parcel must have one or more spatial units associated with it. Check the rules.'
                },
                self.OP_PARCEL_T_PARCEL_NUMBER_F: {
                    'expression': """CASE
                                        WHEN  "{OP_PARCEL_T_PARCEL_NUMBER_F}" IS NOT NULL THEN
                                            CASE
                                                WHEN length("{OP_PARCEL_T_PARCEL_NUMBER_F}") != 30 OR regexp_match(to_string("{OP_PARCEL_T_PARCEL_NUMBER_F}"), '^[0-9]*$') = 0  THEN
                                                    FALSE
                                                WHEN "{OP_PARCEL_T_TYPE_F}" = get_domain_code_from_value('{OP_PARCEL_TYPE_T}', '{PARCEL_TYPE_NO_HORIZONTAL_PROPERTY}', True, False) THEN
                                                    substr("{OP_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 0
                                                WHEN "{OP_PARCEL_T_TYPE_F}" = get_domain_code_from_value('{OP_PARCEL_TYPE_T}', '{PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT}', True, False) THEN
                                                    substr("{OP_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 9
                                                WHEN "{OP_PARCEL_T_TYPE_F}" = get_domain_code_from_value('{OP_PARCEL_TYPE_T}', '{PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT}', True, False) THEN
                                                    substr("{OP_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 9
                                                WHEN "{OP_PARCEL_T_TYPE_F}" = get_domain_code_from_value('{OP_PARCEL_TYPE_T}', '{PARCEL_TYPE_CONDOMINIUM_PARENT}', True, False) THEN
                                                    substr("{OP_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 8
                                                WHEN "{OP_PARCEL_T_TYPE_F}" = get_domain_code_from_value('{OP_PARCEL_TYPE_T}', '{PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT}', True, False) THEN
                                                    substr("{OP_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 8
                                                WHEN "{OP_PARCEL_T_TYPE_F}" = get_domain_code_from_value('{OP_PARCEL_TYPE_T}', '{PARCEL_TYPE_CEMETERY_PARENT}', True, False) THEN
                                                    substr("{OP_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 7
                                                WHEN "{OP_PARCEL_T_TYPE_F}" = get_domain_code_from_value('{OP_PARCEL_TYPE_T}', '{PARCEL_TYPE_CEMETERY_PARCEL_UNIT}', True, False) THEN
                                                    substr("{OP_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 7
                                                WHEN "{OP_PARCEL_T_TYPE_F}" = get_domain_code_from_value('{OP_PARCEL_TYPE_T}', '{PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA}', True, False) THEN
                                                    substr("{OP_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 5
                                                WHEN "{OP_PARCEL_T_TYPE_F}" = get_domain_code_from_value('{OP_PARCEL_TYPE_T}', '{PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA}', True, False) THEN
                                                    substr("{OP_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 5
                                                WHEN "{OP_PARCEL_T_TYPE_F}" = get_domain_code_from_value('{OP_PARCEL_TYPE_T}', '{PARCEL_TYPE_ROAD}', True, False) THEN
                                                    substr("{OP_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 4
                                                WHEN "{OP_PARCEL_T_TYPE_F}" = get_domain_code_from_value('{OP_PARCEL_TYPE_T}', '{PARCEL_TYPE_PUBLIC_USE}', True, False) THEN
                                                    substr("{OP_PARCEL_T_PARCEL_NUMBER_F}", 22,1) = 3
                                                ELSE
                                                    TRUE
                                            END
                                        ELSE
                                            TRUE
                                    END""".format(OP_PARCEL_T_TYPE_F=self.OP_PARCEL_T_TYPE_F,
                                                  OP_PARCEL_TYPE_T=self.OP_PARCEL_TYPE_T,
                                                  PARCEL_TYPE_NO_HORIZONTAL_PROPERTY=self.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY,
                                                  PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT=self.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT,
                                                  PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT=self.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT,
                                                  PARCEL_TYPE_CONDOMINIUM_PARENT=self.PARCEL_TYPE_CONDOMINIUM_PARENT,
                                                  PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT=self.PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT,
                                                  PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA=self.PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA,
                                                  PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA=self.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA,
                                                  PARCEL_TYPE_CEMETERY_PARENT=self.PARCEL_TYPE_CEMETERY_PARENT,
                                                  PARCEL_TYPE_CEMETERY_PARCEL_UNIT=self.PARCEL_TYPE_CEMETERY_PARCEL_UNIT,
                                                  PARCEL_TYPE_ROAD=self.PARCEL_TYPE_ROAD,
                                                  PARCEL_TYPE_PUBLIC_USE=self.PARCEL_TYPE_PUBLIC_USE,
                                                  OP_PARCEL_T_PARCEL_NUMBER_F=self.OP_PARCEL_T_PARCEL_NUMBER_F),
                    'description': 'El campo debe tener 30 caracteres numéricos y la posición 22 debe coincidir con el tipo de predio.'
                },
                self.OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F: {
                    'expression': """CASE
                                        WHEN  "{OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F}" IS NULL THEN
                                            TRUE
                                        WHEN length("{OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F}") != 20 OR regexp_match(to_string("{OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F}"), '^[0-9]*$') = 0 THEN
                                            FALSE
                                        ELSE
                                            TRUE
                                    END""".format(OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F=self.OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F),
                    'description': 'El campo debe tener 20 caracteres numéricos.'
                },
                self.OP_PARCEL_T_VALUATION_F: {
                    'expression': """
                                    CASE
                                        WHEN  "{OP_PARCEL_T_VALUATION_F}" IS NULL THEN
                                            TRUE
                                        WHEN  "{OP_PARCEL_T_VALUATION_F}" = 0 THEN
                                            FALSE
                                        ELSE
                                            TRUE
                                    END""".format(OP_PARCEL_T_VALUATION_F=self.OP_PARCEL_T_VALUATION_F),
                    'description': 'El valor debe ser mayor a cero (0).'
                }
            },
            self.OP_PARTY_T: {
                self.OP_PARTY_T_DOCUMENT_TYPE_F: {
                    'expression': """
                                    CASE
                                        WHEN  "{OP_PARTY_T_TYPE_F}" = get_domain_code_from_value('{OP_PARTY_TYPE_D}', '{OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V}', True, False) THEN
                                             "{OP_PARTY_T_DOCUMENT_TYPE_F}" !=  get_domain_code_from_value('{OP_PARTY_DOCUMENT_TYPE_D}', '{OP_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V}', True, False)
                                        WHEN  "{OP_PARTY_T_TYPE_F}" = get_domain_code_from_value('{OP_PARTY_TYPE_D}', '{OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V}', True, False) THEN
                                             "{OP_PARTY_T_DOCUMENT_TYPE_F}" = get_domain_code_from_value('{OP_PARTY_DOCUMENT_TYPE_D}', '{OP_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V}', True, False)
                                        ELSE
                                            TRUE
                                    END""".format(OP_PARTY_T_TYPE_F=self.OP_PARTY_T_TYPE_F,
                                                  OP_PARTY_TYPE_D=self.OP_PARTY_TYPE_D,
                                                  OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V=self.OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V,
                                                  OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V=self.OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V,
                                                  OP_PARTY_DOCUMENT_TYPE_D=self.OP_PARTY_DOCUMENT_TYPE_D,
                                                  OP_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V=self.OP_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V,
                                                  OP_PARTY_T_DOCUMENT_TYPE_F=self.OP_PARTY_T_DOCUMENT_TYPE_F),
                    'description': 'Si el tipo de interesado es "Persona Natural" entonces el tipo de documento debe ser diferente de \'NIT\'. Pero si el tipo de interesado es "Persona No Natural" entonces el tipo de documento debe ser \'NIT\' o \'Secuencial IGAC\' o \'Secuencial SNR\'. '
                },
                self.OP_PARTY_T_FIRST_NAME_1_F: {
                    'expression': """
                                CASE
                                    WHEN  "{OP_PARTY_T_TYPE_F}" = get_domain_code_from_value('{OP_PARTY_TYPE_D}', '{OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V}', True, False)  THEN
                                         "{OP_PARTY_T_FIRST_NAME_1_F}" IS NOT NULL AND length(trim("{OP_PARTY_T_FIRST_NAME_1_F}")) != 0
                                    WHEN  "{OP_PARTY_T_TYPE_F}" = get_domain_code_from_value('{OP_PARTY_TYPE_D}', '{OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V}', True, False)  THEN
                                         "{OP_PARTY_T_FIRST_NAME_1_F}" IS NULL
                                    ELSE
                                        TRUE
                                END""".format(OP_PARTY_T_TYPE_F=self.OP_PARTY_T_TYPE_F,
                                              OP_PARTY_TYPE_D=self.OP_PARTY_TYPE_D,
                                              OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V=self.OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V,
                                              OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V=self.OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V,
                                              OP_PARTY_T_FIRST_NAME_1_F=self.OP_PARTY_T_FIRST_NAME_1_F),
                    'description': 'Si el tipo de interesado es "Persona Natural" este campo se debe diligenciar, si el tipo de interesado es "Persona No Natural" este campo debe ser NULL.'
                },
                self.OP_PARTY_T_SURNAME_1_F: {
                    'expression': """
                        CASE
                            WHEN  "{OP_PARTY_T_TYPE_F}" = get_domain_code_from_value('{OP_PARTY_TYPE_D}', '{OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V}', True, False) THEN
                                 "{OP_PARTY_T_SURNAME_1_F}" IS NOT NULL AND length(trim("{OP_PARTY_T_SURNAME_1_F}")) != 0
                            WHEN  "{OP_PARTY_T_TYPE_F}" = get_domain_code_from_value('{OP_PARTY_TYPE_D}', '{OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V}', True, False) THEN
                                 "{OP_PARTY_T_SURNAME_1_F}" IS NULL
                            ELSE
                                TRUE
                        END""".format(OP_PARTY_T_TYPE_F=self.OP_PARTY_T_TYPE_F,
                                      OP_PARTY_TYPE_D=self.OP_PARTY_TYPE_D,
                                      OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V=self.OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V,
                                      OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V=self.OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V,
                                      OP_PARTY_T_SURNAME_1_F=self.OP_PARTY_T_SURNAME_1_F),
                    'description': 'Si el tipo de interesado es "Persona Natural" este campo se debe diligenciar, si el tipo de interesado es "Persona No Natural" este campo debe ser NULL.'
                },
                self.OP_PARTY_T_BUSINESS_NAME_F: {
                    'expression': """
                                    CASE
                                        WHEN  "{OP_PARTY_T_TYPE_F}" =  get_domain_code_from_value('{OP_PARTY_TYPE_D}', '{OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V}', True, False) THEN
                                             "{OP_PARTY_T_BUSINESS_NAME_F}" IS NOT NULL AND  length(trim( "{OP_PARTY_T_BUSINESS_NAME_F}")) != 0
                                        WHEN  "{OP_PARTY_T_TYPE_F}" =  get_domain_code_from_value('{OP_PARTY_TYPE_D}', '{OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V}', True, False) THEN
                                             "{OP_PARTY_T_BUSINESS_NAME_F}" IS NULL
                                        ELSE
                                            TRUE
                                    END""".format(OP_PARTY_T_TYPE_F=self.OP_PARTY_T_TYPE_F,
                                                  OP_PARTY_TYPE_D=self.OP_PARTY_TYPE_D,
                                                  OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V=self.OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V,
                                                  OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V=self.OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V,
                                                  OP_PARTY_T_BUSINESS_NAME_F=self.OP_PARTY_T_BUSINESS_NAME_F),
                    'description': 'Si el tipo de interesado es "Persona No Natural" este campo se debe diligenciar, si el tipo de interesado es "Persona Natural" este campo debe ser NULL.'

                },
                self.OP_PARTY_T_DOCUMENT_ID_F: {
                    'expression': """
                                    CASE
                                        WHEN  "{OP_PARTY_T_DOCUMENT_ID_F}"  IS NULL THEN
                                            FALSE
                                        WHEN length(trim("{OP_PARTY_T_DOCUMENT_ID_F}")) = 0 THEN
                                            FALSE
                                        ELSE
                                            TRUE
                                    END""".format(OP_PARTY_T_DOCUMENT_ID_F=self.OP_PARTY_T_DOCUMENT_ID_F),
                    'description': 'El campo es obligatorio.'

                }
            },
            self.OP_PLOT_T: {
                self.OP_PLOT_T_PLOT_AREA_F: {
                    'expression': """
                                    CASE
                                        WHEN  "{OP_PLOT_T_PLOT_AREA_F}" IS NULL THEN
                                            FALSE
                                        WHEN  "{OP_PLOT_T_PLOT_AREA_F}" = 0 THEN
                                            FALSE
                                        ELSE
                                            TRUE
                                    END""".format(OP_PLOT_T_PLOT_AREA_F=self.OP_PLOT_T_PLOT_AREA_F),
                    'description': 'El valor debe ser mayor a cero (0).'
                },
                self.OP_PLOT_T_PLOT_VALUATION_F: {
                    'expression': """
                                    CASE
                                        WHEN  "{OP_PLOT_T_PLOT_VALUATION_F}" IS NULL THEN
                                            FALSE
                                        WHEN  "{OP_PLOT_T_PLOT_VALUATION_F}" = 0 THEN
                                            FALSE
                                        ELSE
                                            TRUE
                                    END""".format(OP_PLOT_T_PLOT_VALUATION_F=self.OP_PLOT_T_PLOT_VALUATION_F),
                    'description': 'El valor debe ser mayor a cero (0).'
                }
            },
            self.OP_BUILDING_T: {
                self.OP_BUILDING_T_BUILDING_AREA_F: {
                    'expression': """
                            CASE
                                WHEN  "{OP_BUILDING_T_BUILDING_AREA_F}" IS NULL THEN
                                    TRUE
                                WHEN  "{OP_BUILDING_T_BUILDING_AREA_F}" = 0 THEN
                                    FALSE
                                ELSE
                                    TRUE
                            END""".format(OP_BUILDING_T_BUILDING_AREA_F=self.OP_BUILDING_T_BUILDING_AREA_F),
                    'description': 'El valor debe ser mayor a cero (0).'
                },
                self.OP_BUILDING_T_BUILDING_VALUATION_F: {
                    'expression': """
                            CASE
                                WHEN  "{OP_BUILDING_T_BUILDING_VALUATION_F}" IS NULL THEN
                                    FALSE
                                WHEN  "{OP_BUILDING_T_BUILDING_VALUATION_F}" = 0 THEN
                                    FALSE
                                ELSE
                                    TRUE
                            END""".format(OP_BUILDING_T_BUILDING_VALUATION_F=self.OP_BUILDING_T_BUILDING_VALUATION_F),
                    'description': 'El valor debe ser mayor a cero (0).'
                }
            },
            self.OP_BUILDING_UNIT_T: {
                self.OP_BUILDING_UNIT_T_BUILT_AREA_F: {
                    'expression': """
                            CASE
                                WHEN  "{OP_BUILDING_UNIT_T_BUILT_AREA_F}" IS NULL THEN
                                    TRUE
                                WHEN  "{OP_BUILDING_UNIT_T_BUILT_AREA_F}" = 0 THEN
                                    FALSE
                                ELSE
                                    TRUE
                            END""".format(OP_BUILDING_UNIT_T_BUILT_AREA_F=self.OP_BUILDING_UNIT_T_BUILT_AREA_F),
                    'description': 'El valor debe ser mayor a cero (0).'
                },
                self.OP_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F: {
                    'expression': """
                            CASE
                                WHEN  "{OP_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F}" IS NULL THEN
                                    TRUE
                                WHEN  "{OP_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F}" = 0 THEN
                                    FALSE
                                ELSE
                                    TRUE
                            END""".format(OP_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F=self.OP_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F),
                    'description': 'El valor debe ser mayor a cero (0).'
                },
                self.OP_BUILDING_UNIT_T_BUILDING_UNIT_VALUATION_F: {
                    'expression': """
                            CASE
                                WHEN  "{OP_BUILDING_UNIT_T_BUILDING_UNIT_VALUATION_F}" IS NULL THEN
                                    TRUE
                                WHEN  "{OP_BUILDING_UNIT_T_BUILDING_UNIT_VALUATION_F}" = 0 THEN
                                    FALSE
                                ELSE
                                    TRUE
                            END""".format(OP_BUILDING_UNIT_T_BUILDING_UNIT_VALUATION_F=self.OP_BUILDING_UNIT_T_BUILDING_UNIT_VALUATION_F),
                    'description': 'El valor debe ser mayor a cero (0).'
                }
            }
        }

DEPARTMENT_FIELD = "departamento"
LESS_TABLE = "menos"
MORE_BOUNDARY_FACE_STRING_TABLE = "col_masCcl"
MUNICIPALITY_FIELD = "municipio"
PARCEL_NUMBER_FIELD = "numero_predial"
PARCEL_NUMBER_BEFORE_FIELD = "numero_predial_anterior"
PARCEL_TABLE = "op_predio"
POINT_BOUNDARY_FACE_STRING_TABLE = "col_puntoCcl"

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
                          'puntos_fachada', 'puntos_cubrimiento_muros', 'puntos_piso', 'puntos_conservacion_acabados',
                          'puntos_tamanio_banio', 'puntos_enchape_banio', 'puntos_mobiliario_banio',
                          'puntos_conservacion_banio', 'puntos_tamanio_cocina', 'puntos_enchape_cocina',
                          'puntos_mobiliario_cocina', 'puntos_conservacion_cocina', 'puntos_cerchas'],
            'visibility_expression': None,
            'before_attr': '  ',
            'after_attr': None
        }
    }
}
