from asistente_ladm_col.config.query_names import QueryNames
from asistente_ladm_col.lib.logger import Logger


T_ID_KEY = 't_id'
DESCRIPTION_KEY = 'description'
ILICODE_KEY = 'ilicode'
DISPLAY_NAME_KEY = 'display_name'
    

class TableAndFieldNames:
    """
    Note: Names are dynamic because different DB engines handle different names, and because even in a single DB engine,
          one could shorten table and field names via ili2db.
    """
    VARIABLE_NAME = 'variable'
    FIELDS_DICT = 'FIELDS_DICT'

    ############################################ TABLE VARIABLES ###########################################################
    T_ID_F = None
    ILICODE_F = None
    DESCRIPTION_F = None
    DISPLAY_NAME_F = None

    OID_T = None  # "LADM_COL.LADM_Nucleo.Oid"

    GC_NEIGHBOURHOOD_T = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Barrio"
    GC_BUILDING_T = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Construccion"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.gc_construccion_predio"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.gc_construccion_unidad"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.gc_copropiedad"
    GC_HP_CONDOMINIUM_DATA_T = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio"
    GC_BLOCK_T = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Manzana"
    GC_PERIMETER_T = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Perimetro"
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
    GC_COMMISSION_BUILDING_T = None  # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Construccion"
    GC_COMMISSION_PLOT_T = None  # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Terreno"
    GC_COMMISSION_BUILDING_UNIT_T = None  # "Datos_Gestor_Catastral_V2_9_6.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion"

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
    COL_PRODUCTION_METHOD_TYPE_D = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_MetodoProduccionTipo"
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
    OP_CONDITION_PARCEL_TYPE_D = None  # "Operacion_V2_9_5.OP_CondicionPredioTipo"
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

    OP_BUILDING_FLOOR_TYPE_D = None  # "Operacion_V2_9_6.OP_ConstruccionPlantaTipo"
    OP_BUILDING_TYPE_D = None  # "Operacion_V2_9_6.OP_ConstruccionTipo"
    OP_DOMAIN_BUILDING_TYPE_D = None  # "Operacion_V2_9_6.OP_DominioConstruccionTipo"
    OP_BUILDING_UNIT_TYPE_D = None  # "Operacion_V2_9_6.OP_UnidadConstruccionTipo"

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
    GC_PARCEL_T_REGISTRY_OFFICE_F = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Predio_Catastro.Circulo_Registral"
    GC_PARCEL_T_CONDITION_F = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Predio_Catastro.Condicion_Predio"
    GC_PARCEL_T_ECONOMIC_DESTINATION_F = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Predio_Catastro.Destinacion_Economica"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Predio_Catastro.Direcciones"
    GC_PARCEL_T_DATE_OF_DATA_F = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Predio_Catastro.Fecha_Datos"
    GC_PARCEL_T_FMI_F = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Predio_Catastro.Matricula_Inmobiliaria_Catastro"
    GC_PARCEL_T_PARCEL_NUMBER_F = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Predio_Catastro.Numero_Predial"
    GC_PARCEL_T_PARCEL_NUMBER_BEFORE_F = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Predio_Catastro.Numero_Predial_Anterior"
    GC_PARCEL_T_DATA_SOURCE_F = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Predio_Catastro.Sistema_Procedencia_Datos"
    GC_PARCEL_T_CADASTRAL_TYPE_F = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Predio_Catastro.Tipo_Catastro"
    GC_PARCEL_T_PARCEL_TYPE_F = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Predio_Catastro.Tipo_Predio"
    GC_OWNER_T_VERIFICATION_DIGIT = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Propietario.Digito_Verificacion"
    GC_OWNER_T_DOCUMENT_ID_F = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Propietario.Numero_Documento"
    GC_OWNER_T_PARCEL_ID_F = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.gc_propietario_predio.gc_predio_catastro"
    GC_OWNER_T_SURNAME_1_F = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Propietario.Primer_Apellido"
    GC_OWNER_T_FIRST_NAME_1_F = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Propietario.Primer_Nombre"
    GC_OWNER_T_BUSINESS_NAME_F = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Propietario.Razon_Social"
    GC_OWNER_T_SURNAME_2_F = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Propietario.Segundo_Apellido"
    GC_OWNER_T_FIRST_NAME_2_F = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Propietario.Segundo_Nombre"
    GC_OWNER_T_DOCUMENT_TYPE_F = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Propietario.Tipo_Documento"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Sector_Rural.Codigo"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Sector_Rural.Geometria"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Sector_Urbano.Codigo"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Sector_Urbano.Geometria"
    GC_PLOT_T_ALPHANUMERIC_AREA_F = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Alfanumerica"
    GC_PLOT_T_DIGITAL_PLOT_AREA_F = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Digital"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Terreno.Geometria"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Terreno.Manzana_Vereda_Codigo"
    # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.GC_Terreno.Numero_Subterraneos"
    GC_PLOT_T_GC_PARCEL_F = None  # "Datos_Gestor_Catastral_V2_9_5.Datos_Gestor_Catastral.gc_terreno_predio.gc_predio"
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
    SNR_PARCEL_REGISTRY_T_NEW_PARCEL_NUMBER_IN_FMI_F = None  # "Datos_SNR_V2_9_5.Datos_SNR.SNR_Predio_Registro.Numero_Predial_Nuevo_en_FMI"
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
    BAUNIT_SOURCE_T_SOURCE_F = None  # LADM_COL.LADM_Nucleo.col_baunitFuente.fuente_espacial..Operacion.Operacion.OP_FuenteEspacial --> fuente_espacial
    BAUNIT_SOURCE_T_UNIT_F = None  # LADM_COL.LADM_Nucleo.col_baunitFuente.unidad..Operacion.Operacion.OP_Predio --> unidad
    COL_BAUNIT_RRR_T_UNIT_F = None  # "LADM_COL_V1_2.LADM_Nucleo.col_baunitRrr.unidad"
    COL_CCL_SOURCE_T_BOUNDARY_F = None # LADM_COL.LADM_Nucleo.col_cclFuente.ccl..Operacion.Operacion.OP_Lindero --> ccl_op_lindero
                                       # "LADM_COL.LADM_Nucleo.col_cclFuente.ccl_Operacion.Operacion.OP_Lindero" --> ccl_op_lindero
    COL_CCL_SOURCE_T_SOURCE_F = None  # LADM_COL.LADM_Nucleo.col_cclFuente.fuente_espacial..Operacion.Operacion.OP_FuenteEspacial --> fuente_espacial
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
    COL_BFS_T_GEOMETRY_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_CadenaCarasLimite.Geometria"
    COL_BFS_T_TEXTUAL_LOCATION_F = None  # "LADM_COL.LADM_Nucleo.COL_CadenaCarasLimite.Localizacion_Textual"
    COL_ADMINISTRATIVE_SOURCE_T_SOURCE_NUMBER_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_FuenteAdministrativa.Numero_Fuente"
    COL_ADMINISTRATIVE_SOURCE_T_OBSERVATION_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_FuenteAdministrativa.Observacion"
    COL_SPATIAL_SOURCE_T_MEASUREMENTS_F = None  # LADM_COL.LADM_Nucleo.COL_FuenteEspacial.Mediciones..Operacion.Operacion.OP_FuenteEspacial --> op_fuenteespacial_mediciones
    COL_SPATIAL_SOURCE_T_TYPE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_FuenteEspacial.Tipo"
    # COL_SOURCE_T_QUALITY_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Calidad"
    COL_SOURCE_T_AVAILABILITY_STATUS_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Estado_Disponibilidad"
    COL_SOURCE_T_EXT_ARCHIVE_ID_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID"
    COL_SOURCE_T_DATE_DOCUMENT_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Fecha_Documento_Fuente"
    COL_SOURCE_T_OFFICIAL_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Oficialidad"
    # COL_SOURCE_T_PROVENANCE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Procedencia"
    COL_SOURCE_T_MAIN_TYPE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Tipo_Principal"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_FuncionInteresadoTipo_.value"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Interesado.ext_PID"
    COL_PARTY_T_NAME_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Interesado.Nombre"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Interesado.Tarea"
    COL_POINT_T_ORIGINAL_LOCATION_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Geometria"
    COL_POINT_T_PRODUCTION_METHOD_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.MetodoProduccion"
    COL_POINT_T_MONUMENTATION_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Monumentacion"
    COL_POINT_T_INTERPOLATION_POSITION_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Posicion_Interpolacion"
    # COL_POINT_T_TRANSFORMATION_AND_RESULT_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Transformacion_Y_Resultado"
    COL_RRR_T_SHARE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_RRR.Compartido"
    COL_RRR_T_SHARE_CHECK_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_RRR.Comprobacion_Comparte"
    COL_RRR_T_DESCRIPTION_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_RRR.Descripcion"
    COL_RRR_T_EFFECTIVE_USAGE_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_RRR.Uso_Efectivo"

    # COL_SPATIAL_UNIT_T_AREA_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Area"
    COL_SPATIAL_UNIT_T_DIMENSION_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Dimension"
    COL_SPATIAL_UNIT_T_LABEL_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Etiqueta"
    # COL_SPATIAL_UNIT_T_EXT_ADDRESS_ID_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID"
    COL_SPATIAL_UNIT_T_GEOMETRY_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Geometria"
    COL_SPATIAL_UNIT_T_SURFACE_RELATION_F = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie"
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
    # "LADM_COL_V1_2.LADM_Nucleo.col_masCcl.ue_mas"
    # "LADM_COL_V1_2.LADM_Nucleo.col_masCl.ue_mas"
    # "LADM_COL_V1_2.LADM_Nucleo.col_menosCcl.ue_menos"
    # "LADM_COL_V1_2.LADM_Nucleo.col_menosCl.ue_menos"
    MEMBERS_T_GROUP_PARTY_F = None  # LADM_COL.LADM_Nucleo.col_miembros.agrupacion..Operacion.Operacion.OP_Agrupacion_Interesados --> agrupacion
    MEMBERS_T_PARTY_F = None  # LADM_COL.LADM_Nucleo.col_miembros.interesado..Operacion.Operacion.OP_Interesado --> interesado_op_interesado
    FRACTION_S_MEMBER_F = None  # "LADM_COL_V1_2.LADM_Nucleo.col_miembros.participacion"
    FRACTION_S_COPROPERTY_COEFFICIENT_F = None  # "Operacion.Operacion.op_predio_copropiedad.coeficiente"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F = None  # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F = None  # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL_V1_2.LADM_Nucleo.OM_Observacion.Resultado_Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.col_puntoCcl.punto"
    # "LADM_COL_V1_2.LADM_Nucleo.col_puntoCl.punto"
    COL_POINT_SOURCE_T_SOURCE_F = None  # LADM_COL.LADM_Nucleo.col_puntoFuente.fuente_espacial..Operacion.Operacion.OP_FuenteEspacial --> fuente_espacial
    # "LADM_COL_V1_2.LADM_Nucleo.col_puntoFuente.punto"
    # "LADM_COL_V1_2.LADM_Nucleo.col_puntoReferencia.ue"
    # "LADM_COL_V1_2.LADM_Nucleo.col_relacionFuente.fuente_administrativa"
    # "LADM_COL_V1_2.LADM_Nucleo.col_relacionFuenteUespacial.fuente_espacial"
    # "LADM_COL_V1_2.LADM_Nucleo.col_responsableFuente.fuente_administrativa"
    # "LADM_COL_V1_2.LADM_Nucleo.col_responsableFuente.interesado"
    COL_RRR_SOURCE_T_SOURCE_F = None  # LADM_COL.LADM_Nucleo.col_rrrFuente.fuente_administrativa..Operacion.Operacion.OP_FuenteAdministrativa --> fuente_administrativa
    # "LADM_COL_V1_2.LADM_Nucleo.col_rrrFuente.rrr"
    COL_RRR_PARTY_T_OP_PARTY_F = None  # "LADM_COL.LADM_Nucleo.col_rrrInteresado.interesado_Operacion.Operacion.OP_Interesado"
    COL_RRR_PARTY_T_OP_GROUP_PARTY_F = None  # "LADM_COL.LADM_Nucleo.col_rrrInteresado.interesado_Operacion.Operacion.OP_Agrupacion_Interesados"
    # "LADM_COL_V1_2.LADM_Nucleo.col_topografoFuente.fuente_espacial"
    # "LADM_COL_V1_2.LADM_Nucleo.col_topografoFuente.topografo"
    COL_UE_BAUNIT_T_PARCEL_F = None  # "LADM_COL_V1_2.LADM_Nucleo.col_ueBaunit.baunit..Operacion.Operacion.OP_Predio" -->  baunit
    # "LADM_COL_V1_2.LADM_Nucleo.col_ueBaunit.ue"
    COL_UE_SOURCE_T_SOURCE_F = None  # LADM_COL.LADM_Nucleo.col_ueFuente.fuente_espacial..Operacion.Operacion.OP_FuenteEspacial --> fuente_espacial
    # "LADM_COL_V1_2.LADM_Nucleo.col_ueFuente.ue"
    # "LADM_COL_V1_2.LADM_Nucleo.col_ueUeGrupo.parte"
    # "LADM_COL_V1_2.LADM_Nucleo.col_unidadFuente.fuente_administrativa"
    # "LADM_COL_V1_2.LADM_Nucleo.col_unidadFuente.unidad"
    #
    #
    OP_BUILDING_T_BUILDING_CODE_F = None  # "Operacion_V2_9_6.Operacion.OP_Construccion.Codigo_Edificacion"
    OP_BUILDING_T_IDENTIFIER_F = None  # "Operacion_V2_9_6.Operacion.OP_Construccion.Identificador"
    OP_BUILDING_T_NUMBER_OF_MEZZANINE_F = None  # "Operacion_V2_9_6.Operacion.OP_Construccion.Numero_Mezanines"
    OP_BUILDING_T_NUMBER_OF_LOOKOUT_BASEMENT_F = None  # "Operacion_V2_9_6.Operacion.OP_Construccion.Numero_Semisotanos"
    OP_BUILDING_T_NUMBER_OF_BASEMENT_F = None  # "Operacion_V2_9_6.Operacion.OP_Construccion.Numero_Sotanos"
    OP_BUILDING_T_BUILDING_TYPE_F = None  # "Operacion_V2_9_6.Operacion.OP_Construccion.Tipo_Construccion"
    OP_BUILDING_T_DOMAIN_TYPE_F = None  # "Operacion_V2_9_6.Operacion.OP_Construccion.Tipo_Dominio"
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
    OP_PLOT_T_BLOCK_RURAL_DIVISION_CODE_F = None  # "Operacion_V2_9_6.Operacion.OP_Terreno.Manzana_Vereda_Codigo"
    OP_PLOT_T_NUMBER_OF_UNDERGROUND_ROOMS_F = None  # "Operacion_V2_9_6.Operacion.OP_Terreno.Numero_Subterraneos"
    OP_BUILDING_UNIT_T_BUILT_AREA_F = None  # "Operacion_V2_9_5.Operacion.OP_UnidadConstruccion.Area_Construida"
    OP_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F = None  # "Operacion_V2_9_5.Operacion.OP_UnidadConstruccion.Area_Privada_Construida"
    OP_BUILDING_UNIT_T_BUILDING_VALUATION_F = None  # "Operacion_V2_9_6.Operacion.OP_UnidadConstruccion.Avaluo_Construccion"
    OP_BUILDING_UNIT_T_IDENTIFICATION_F = None  # "Operacion_V2_9_5.Operacion.OP_UnidadConstruccion.Identificador"
    OP_BUILDING_UNIT_T_FLOOR_F = None  # "Operacion_V2_9_6.Operacion.OP_UnidadConstruccion.Planta_Ubicacion"
    OP_BUILDING_UNIT_T_TOTAL_FLOORS_F = None  # "Operacion_V2_9_6.Operacion.OP_UnidadConstruccion.Total_Pisos"
    OP_BUILDING_UNIT_T_USE_F = None  # "Operacion_V2_9_5.Operacion.OP_UnidadConstruccion.Uso"
    OP_BUILDING_UNIT_T_YEAR_OF_BUILDING_F = None  # "Operacion_V2_9_6.Operacion.OP_UnidadConstruccion.Anio_Construccion"
    OP_BUILDING_UNIT_T_OBSERVATIONS_F = None  # "Operacion_V2_9_6.Operacion.OP_UnidadConstruccion.Observaciones"
    OP_BUILDING_UNIT_T_BUILDING_TYPE_F = None  # "Operacion_V2_9_6.Operacion.OP_UnidadConstruccion.Tipo_Construccion"
    OP_BUILDING_UNIT_T_DOMAIN_TYPE_F = None  # "Operacion_V2_9_6.Operacion.OP_UnidadConstruccion.Tipo_Dominio"
    OP_BUILDING_UNIT_T_FLOOR_TYPE_F = None  # "Operacion_V2_9_6.Operacion.OP_UnidadConstruccion.Tipo_Planta"
    OP_BUILDING_UNIT_T_BUILDING_UNIT_TYPE_F = None  # "Operacion_V2_9_6.Operacion.OP_UnidadConstruccion.Tipo_Unidad_Construccion"
    OP_BUILDING_UNIT_T_TOTAL_BATHROOMS_F = None  # "Operacion_V2_9_6.Operacion.OP_UnidadConstruccion.Total_Banios"
    OP_BUILDING_UNIT_T_TOTAL_ROOMS_F = None  # "Operacion_V2_9_6.Operacion.OP_UnidadConstruccion.Total_Habitaciones"
    OP_BUILDING_UNIT_T_TOTAL_LOCALS_F = None  # "Operacion_V2_9_6.Operacion.OP_UnidadConstruccion.Total_Locales"

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
    MORE_BFS_T_CRF_LINEAR_STRUCTURE_F = None  # "LADM_COL.LADM_Nucleo.col_masCcl.ccl_mas_Cartografia_Referencia.Auxiliares.CRF_EstructuraLineal" --> ccl_mas_crf_estructuralineal
    MORE_BFS_T_OP_BOUNDARY_F = None  # "LADM_COL.LADM_Nucleo.col_masCcl.ccl_mas_Operacion.Operacion.OP_Lindero" --> ccl_mas_op_lindero
    MORE_BFS_T_OP_BUILDING_F = None  # "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas_Operacion.Operacion.OP_Construccion" --> ue_mas_op_construccion
    MORE_BFS_T_OP_RIGHT_OF_WAY_F = None  # "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas_Operacion.Operacion.OP_ServidumbrePaso" --> ue_mas_op_servidumbrepaso
    MORE_BFS_T_OP_PLOT_F = None  # "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas_Operacion.Operacion.OP_Terreno" --> ue_mas_op_terreno
    MORE_BFS_T_OP_BUILDING_UNIT_F = None  # "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas_Operacion.Operacion.OP_UnidadConstruccion" --> ue_mas_op_unidadconstruccion
    # "LADM_COL.LADM_Nucleo.col_masCl.ue_mas_Operacion.Operacion.OP_Construccion" --> ue_mas_op_construccion
    # "LADM_COL.LADM_Nucleo.col_masCl.ue_mas_Operacion.Operacion.OP_ServidumbrePaso" --> ue_mas_op_servidumbrepaso
    # "LADM_COL.LADM_Nucleo.col_masCl.ue_mas_Operacion.Operacion.OP_Terreno" --> ue_mas_op_terreno
    # "LADM_COL.LADM_Nucleo.col_masCl.ue_mas_Operacion.Operacion.OP_UnidadConstruccion" --> ue_mas_op_unidadconstruccion
    LESS_BFS_T_OP_BOUNDARY_F = None  # "LADM_COL.LADM_Nucleo.col_menosCcl.ccl_menos_Operacion.Operacion.OP_Lindero" --> ccl_menos_op_lindero
    LESS_BFS_T_CRF_LINEAR_STRUCTURE_F = None  # "LADM_COL.LADM_Nucleo.col_menosCcl.ccl_menos_Cartografia_Referencia.Auxiliares.CRF_EstructuraLineal" --> ccl_menos_crf_estructuralineal
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
    POINT_BFS_T_OP_BOUNDARY_F = None  # "LADM_COL.LADM_Nucleo.col_puntoCcl.ccl..Operacion.Operacion.OP_Lindero" --> ccl_op_lindero
    POINT_BFS_T_CRF_LINEAR_STRUCTURE_F = None  # "LADM_COL.LADM_Nucleo.col_puntoCcl.ccl..Cartografia_Referencia.Auxiliares.CRF_EstructuraLineal" --> ccl_crf_estructuralineal
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

    OID_T_NAMESPACE_F = None  # "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres"
    OID_T_LOCAL_ID_F = None  # "LADM_COL.LADM_Nucleo.Oid.Local_Id"

    TABLE_DICT = {
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Barrio": {VARIABLE_NAME: "GC_NEIGHBOURHOOD_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Construccion": {VARIABLE_NAME: "GC_BUILDING_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio": {VARIABLE_NAME: "GC_HP_CONDOMINIUM_DATA_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Manzana": {VARIABLE_NAME: "GC_BLOCK_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Perimetro": {VARIABLE_NAME: "GC_PERIMETER_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro": {VARIABLE_NAME: "GC_PARCEL_T", FIELDS_DICT: {
            "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Circulo_Registral": "GC_PARCEL_T_REGISTRY_OFFICE_F",
            "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Condicion_Predio": "GC_PARCEL_T_CONDITION_F",
            "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Destinacion_Economica": "GC_PARCEL_T_ECONOMIC_DESTINATION_F",
            "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Fecha_Datos": "GC_PARCEL_T_DATE_OF_DATA_F",
            "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Matricula_Inmobiliaria_Catastro": "GC_PARCEL_T_FMI_F",
            "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Numero_Predial": "GC_PARCEL_T_PARCEL_NUMBER_F",
            "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Numero_Predial_Anterior": "GC_PARCEL_T_PARCEL_NUMBER_BEFORE_F",
            "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Sistema_Procedencia_Datos": "GC_PARCEL_T_DATA_SOURCE_F",
            "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Tipo_Catastro": "GC_PARCEL_T_CADASTRAL_TYPE_F",
            "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Tipo_Predio": "GC_PARCEL_T_PARCEL_TYPE_F"
        }},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario": {VARIABLE_NAME: "GC_OWNER_T", FIELDS_DICT: {
            "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario.Digito_Verificacion": "GC_OWNER_T_VERIFICATION_DIGIT",
            "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario.Numero_Documento": "GC_OWNER_T_DOCUMENT_ID_F",
            "Datos_Gestor_Catastral.Datos_Gestor_Catastral.gc_propietario_predio.gc_predio_catastro..Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro": "GC_OWNER_T_PARCEL_ID_F",
            "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario.Primer_Apellido": "GC_OWNER_T_SURNAME_1_F",
            "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario.Primer_Nombre": "GC_OWNER_T_FIRST_NAME_1_F",
            "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario.Razon_Social": "GC_OWNER_T_BUSINESS_NAME_F",
            "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario.Segundo_Apellido": "GC_OWNER_T_SURNAME_2_F",
            "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario.Segundo_Nombre": "GC_OWNER_T_FIRST_NAME_2_F",
            "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario.Tipo_Documento": "GC_OWNER_T_DOCUMENT_TYPE_F",
        }},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Sector_Rural": {VARIABLE_NAME: "GC_RURAL_SECTOR_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Sector_Urbano": {VARIABLE_NAME: "GC_URBAN_SECTOR_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno": {VARIABLE_NAME: "GC_PLOT_T", FIELDS_DICT: {
            "Datos_Gestor_Catastral.Datos_Gestor_Catastral.gc_terreno_predio.gc_predio..Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro": "GC_PLOT_T_GC_PARCEL_F",
            "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Digital": "GC_PLOT_T_DIGITAL_PLOT_AREA_F",
            "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Alfanumerica": "GC_PLOT_T_ALPHANUMERIC_AREA"
        }},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Unidad_Construccion": {VARIABLE_NAME: "GC_BUILDING_UNIT_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Vereda": {VARIABLE_NAME: "GC_RURAL_DIVISION_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Comisiones_Construccion": {VARIABLE_NAME: "GC_COMMISSION_BUILDING_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Comisiones_Terreno": {VARIABLE_NAME: "GC_COMMISSION_PLOT_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Comisiones_Unidad_Construccion": {VARIABLE_NAME: "GC_COMMISSION_BUILDING_UNIT_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.GC_CondicionPredioTipo": {VARIABLE_NAME: "GC_PARCEL_TYPE_D", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.GC_Direccion": {VARIABLE_NAME: "GC_ADDRESS_T", FIELDS_DICT: {}},
        "Datos_Gestor_Catastral.GC_UnidadConstruccionTipo": {VARIABLE_NAME: "GC_BUILDING_UNIT_TYPE_T", FIELDS_DICT: {}},
        "Datos_Integracion_Insumos.Datos_Integracion_Insumos.INI_Predio_Insumos": {VARIABLE_NAME: "INI_PARCEL_SUPPLIES_T", FIELDS_DICT: {}},
        "Datos_SNR.Datos_SNR.SNR_Derecho": {VARIABLE_NAME: "SNR_RIGHT_T", FIELDS_DICT: {}},
        "Datos_SNR.Datos_SNR.SNR_Fuente_CabidaLinderos": {VARIABLE_NAME: "SNR_SOURCE_BOUNDARIES_T", FIELDS_DICT: {}},
        "Datos_SNR.Datos_SNR.SNR_Fuente_Derecho": {VARIABLE_NAME: "SNR_SOURCE_RIGHT_T", FIELDS_DICT: {}},
        "Datos_SNR.Datos_SNR.SNR_Predio_Registro": {VARIABLE_NAME: "SNR_PARCEL_REGISTRY_T", FIELDS_DICT: {
            "Datos_SNR.Datos_SNR.SNR_Predio_Registro.Numero_Predial_Nuevo_en_FMI": "SNR_PARCEL_REGISTRY_T_NEW_PARCEL_NUMBER_IN_FMI_F"
        }},
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
        "LADM_COL.LADM_Nucleo.COL_MetodoProduccionTipo": {VARIABLE_NAME: "COL_PRODUCTION_METHOD_TYPE_D", FIELDS_DICT: {}},
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
            "LADM_COL.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID..Operacion.Operacion.OP_FuenteAdministrativa": "EXT_ARCHIVE_S_OP_ADMINISTRATIVE_SOURCE_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID..Operacion.Operacion.OP_FuenteEspacial": "EXT_ARCHIVE_S_OP_SPATIAL_SOURCE_F"
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
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID..Operacion.Operacion.OP_Construccion": "EXT_ADDRESS_S_OP_BUILDING_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID..Operacion.Operacion.OP_ServidumbrePaso": "EXT_ADDRESS_S_OP_RIGHT_OF_WAY_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID..Operacion.Operacion.OP_Terreno": "EXT_ADDRESS_S_OP_PLOT_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID..Operacion.Operacion.OP_UnidadConstruccion": "EXT_ADDRESS_S_OP_BUILDING_UNIT_F"
        }},
        "LADM_COL.LADM_Nucleo.ExtInteresado": {VARIABLE_NAME: "EXT_PARTY_S", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.Fraccion": {VARIABLE_NAME: "FRACTION_S", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.Fraccion.Denominador": "FRACTION_S_DENOMINATOR_F",
            "LADM_COL.LADM_Nucleo.Fraccion.Numerador": "FRACTION_S_NUMERATOR_F",
            "LADM_COL.LADM_Nucleo.COL_RRR.Compartido..Operacion.Operacion.OP_Derecho": "FRACTION_S_OP_RIGHT_F",
            "LADM_COL.LADM_Nucleo.COL_RRR.Compartido..Operacion.Operacion.OP_Restriccion": "FRACTION_S_OP_RESTRICTION_F"
        }},
        "LADM_COL.LADM_Nucleo.COL_BAUnitTipo": {VARIABLE_NAME: "COL_BAUNIT_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.COL_DimensionTipo": {VARIABLE_NAME: "COL_DIMENSION_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.COL_PuntoTipo": {VARIABLE_NAME: "COL_POINT_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.col_masCcl": {VARIABLE_NAME: "MORE_BFS_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_masCcl.ccl_mas..Operacion.Operacion.OP_Lindero": "MORE_BFS_T_OP_BOUNDARY_F",
            "LADM_COL.LADM_Nucleo.col_masCcl.ccl_mas..Cartografia_Referencia.Auxiliares.CRF_EstructuraLineal": "MORE_BFS_T_CRF_LINEAR_STRUCTURE_F",
            "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_Construccion": "MORE_BFS_T_OP_BUILDING_F",
            "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_ServidumbrePaso": "MORE_BFS_T_OP_RIGHT_OF_WAY_F",
            "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_Terreno": "MORE_BFS_T_OP_PLOT_F",
            "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Operacion.Operacion.OP_UnidadConstruccion": "MORE_BFS_T_OP_BUILDING_UNIT_F"
        }},
        "LADM_COL.LADM_Nucleo.col_menosCcl": {VARIABLE_NAME: "LESS_BFS_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_menosCcl.ccl_menos..Operacion.Operacion.OP_Lindero": "LESS_BFS_T_OP_BOUNDARY_F",
            "LADM_COL.LADM_Nucleo.col_menosCcl.ccl_menos..Cartografia_Referencia.Auxiliares.CRF_EstructuraLineal": "LESS_BFS_T_CRF_LINEAR_STRUCTURE_F",
            "LADM_COL.LADM_Nucleo.col_menosCcl.ue_menos..Operacion.Operacion.OP_Construccion": "LESS_BFS_T_OP_BUILDING_F",
            "LADM_COL.LADM_Nucleo.col_menosCcl.ue_menos..Operacion.Operacion.OP_ServidumbrePaso": "LESS_BFS_T_OP_RIGHT_OF_WAY_F",
            "LADM_COL.LADM_Nucleo.col_menosCcl.ue_menos..Operacion.Operacion.OP_Terreno": "LESS_BFS_T_OP_PLOT_F",
            "LADM_COL.LADM_Nucleo.col_menosCcl.ue_menos..Operacion.Operacion.OP_UnidadConstruccion": "LESS_BFS_T_OP_BUILDING_UNIT_F",
        }},
        "LADM_COL.LADM_Nucleo.col_miembros": {VARIABLE_NAME: "MEMBERS_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_miembros.participacion..LADM_COL.LADM_Nucleo.col_miembros": "FRACTION_S_MEMBER_F",
            "LADM_COL.LADM_Nucleo.col_miembros.agrupacion..Operacion.Operacion.OP_Agrupacion_Interesados": "MEMBERS_T_GROUP_PARTY_F",
            "LADM_COL.LADM_Nucleo.col_miembros.interesado..Operacion.Operacion.OP_Interesado": "MEMBERS_T_PARTY_F"
        }},
        "LADM_COL.LADM_Nucleo.col_puntoCcl": {VARIABLE_NAME: "POINT_BFS_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_puntoCcl.ccl..Operacion.Operacion.OP_Lindero": "POINT_BFS_T_OP_BOUNDARY_F",
            "LADM_COL.LADM_Nucleo.col_puntoCcl.ccl..Cartografia_Referencia.Auxiliares.CRF_EstructuraLineal": "POINT_BFS_T_CRF_LINEAR_STRUCTURE_F",
            "LADM_COL.LADM_Nucleo.col_puntoCcl.punto..Operacion.Operacion.OP_PuntoControl": "POINT_BFS_T_OP_CONTROL_POINT_F",
            "LADM_COL.LADM_Nucleo.col_puntoCcl.punto..Operacion.Operacion.OP_PuntoLevantamiento": "POINT_BFS_T_OP_SURVEY_POINT_F",
            "LADM_COL.LADM_Nucleo.col_puntoCcl.punto..Operacion.Operacion.OP_PuntoLindero": "POINT_BFS_T_OP_BOUNDARY_POINT_F",
        }},
        "LADM_COL.LADM_Nucleo.col_puntoFuente": {VARIABLE_NAME: "COL_POINT_SOURCE_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_puntoFuente.fuente_espacial..Operacion.Operacion.OP_FuenteEspacial": "COL_POINT_SOURCE_T_SOURCE_F",
            "LADM_COL.LADM_Nucleo.col_puntoFuente.punto..Operacion.Operacion.OP_PuntoControl": "COL_POINT_SOURCE_T_OP_CONTROL_POINT_F",
            "LADM_COL.LADM_Nucleo.col_puntoFuente.punto..Operacion.Operacion.OP_PuntoLevantamiento": "COL_POINT_SOURCE_T_OP_SURVEY_POINT_F",
            "LADM_COL.LADM_Nucleo.col_puntoFuente.punto..Operacion.Operacion.OP_PuntoLindero": "COL_POINT_SOURCE_T_OP_BOUNDARY_POINT_F"
        }},
        "LADM_COL.LADM_Nucleo.col_rrrFuente": {VARIABLE_NAME: "COL_RRR_SOURCE_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_rrrFuente.fuente_administrativa..Operacion.Operacion.OP_FuenteAdministrativa": "COL_RRR_SOURCE_T_SOURCE_F",
            "LADM_COL.LADM_Nucleo.col_rrrFuente.rrr..Operacion.Operacion.OP_Derecho": "COL_RRR_SOURCE_T_OP_RIGHT_F",
            "LADM_COL.LADM_Nucleo.col_rrrFuente.rrr..Operacion.Operacion.OP_Restriccion": "COL_RRR_SOURCE_T_OP_RESTRICTION_F"
        }},
        "LADM_COL.LADM_Nucleo.col_ueBaunit": {VARIABLE_NAME: "COL_UE_BAUNIT_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_ueBaunit.baunit..Operacion.Operacion.OP_Predio": "COL_UE_BAUNIT_T_PARCEL_F",
            "LADM_COL.LADM_Nucleo.col_ueBaunit.ue..Operacion.Operacion.OP_Terreno": "COL_UE_BAUNIT_T_OP_PLOT_F",
            "LADM_COL.LADM_Nucleo.col_ueBaunit.ue..Operacion.Operacion.OP_Construccion": "COL_UE_BAUNIT_T_OP_BUILDING_F",
            "LADM_COL.LADM_Nucleo.col_ueBaunit.ue..Operacion.Operacion.OP_UnidadConstruccion": "COL_UE_BAUNIT_T_OP_BUILDING_UNIT_F",
            "LADM_COL.LADM_Nucleo.col_ueBaunit.ue..Operacion.Operacion.OP_ServidumbrePaso": "COL_UE_BAUNIT_T_OP_RIGHT_OF_WAY_F"
        }},
        "LADM_COL.LADM_Nucleo.col_ueFuente": {VARIABLE_NAME: "COL_UE_SOURCE_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_ueFuente.fuente_espacial..Operacion.Operacion.OP_FuenteEspacial": "COL_UE_SOURCE_T_SOURCE_F",
            "LADM_COL.LADM_Nucleo.col_ueFuente.ue..Operacion.Operacion.OP_Construccion": "COL_UE_SOURCE_T_OP_BUILDING_F",
            "LADM_COL.LADM_Nucleo.col_ueFuente.ue..Operacion.Operacion.OP_ServidumbrePaso": "COL_UE_SOURCE_T_OP_RIGHT_OF_WAY_F",
            "LADM_COL.LADM_Nucleo.col_ueFuente.ue..Operacion.Operacion.OP_Terreno": "COL_UE_SOURCE_T_OP_PLOT_F",
            "LADM_COL.LADM_Nucleo.col_ueFuente.ue..Operacion.Operacion.OP_UnidadConstruccion": "COL_UE_SOURCE_T_OP_BUILDING_UNIT_F"
        }},
        "LADM_COL.LADM_Nucleo.col_baunitFuente": {VARIABLE_NAME: "COL_BAUNIT_SOURCE_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_baunitFuente.fuente_espacial..Operacion.Operacion.OP_FuenteEspacial": "BAUNIT_SOURCE_T_SOURCE_F",
            "LADM_COL.LADM_Nucleo.col_baunitFuente.unidad..Operacion.Operacion.OP_Predio": "BAUNIT_SOURCE_T_UNIT_F"
        }},
        "LADM_COL.LADM_Nucleo.col_cclFuente": {VARIABLE_NAME: "COL_CCL_SOURCE_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_cclFuente.fuente_espacial..Operacion.Operacion.OP_FuenteEspacial": "COL_CCL_SOURCE_T_SOURCE_F",
            "LADM_COL.LADM_Nucleo.col_cclFuente.ccl..Operacion.Operacion.OP_Lindero": "COL_CCL_SOURCE_T_BOUNDARY_F"
        }},
        "Operacion.OP_AcuerdoTipo": {VARIABLE_NAME: "OP_AGREEMENT_TYPE_D", FIELDS_DICT: {}},
        "Operacion.OP_UbicacionPuntoTipo": {VARIABLE_NAME: "OP_LOCATION_POINT_TYPE_D", FIELDS_DICT: {}},
        "Operacion.OP_ConstruccionPlantaTipo": {VARIABLE_NAME: "OP_BUILDING_FLOOR_TYPE_D", FIELDS_DICT: {}},
        "Operacion.OP_ConstruccionTipo": {VARIABLE_NAME: "OP_BUILDING_TYPE_D", FIELDS_DICT: {}},
        "Operacion.OP_DominioConstruccionTipo": {VARIABLE_NAME: "OP_DOMAIN_BUILDING_TYPE_D", FIELDS_DICT: {}},
        "Operacion.OP_UnidadConstruccionTipo": {VARIABLE_NAME: "OP_BUILDING_UNIT_TYPE_D", FIELDS_DICT: {}},
        "Operacion.OP_CondicionPredioTipo": {VARIABLE_NAME: "OP_CONDITION_PARCEL_TYPE_D", FIELDS_DICT: {}},
        "Operacion.OP_DerechoTipo": {VARIABLE_NAME: "OP_RIGHT_TYPE_D", FIELDS_DICT: {}},
        "Operacion.Operacion.OP_Agrupacion_Interesados": {VARIABLE_NAME: "OP_GROUP_PARTY_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.COL_Agrupacion_Interesados.Tipo": "COL_GROUP_PARTY_T_TYPE_F",
            "LADM_COL.LADM_Nucleo.COL_Interesado.Nombre": "COL_PARTY_T_NAME_F",
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Operacion.Operacion.OP_UnidadConstruccion": {VARIABLE_NAME: "OP_BUILDING_UNIT_T", FIELDS_DICT: {
            "Operacion.Operacion.OP_UnidadConstruccion.Area_Construida": "OP_BUILDING_UNIT_T_BUILT_AREA_F",
            "Operacion.Operacion.OP_UnidadConstruccion.Area_Privada_Construida": "OP_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F",
            "Operacion.Operacion.OP_UnidadConstruccion.Avaluo_Construccion": "OP_BUILDING_UNIT_T_BUILDING_VALUATION_F",
            "Operacion.Operacion.OP_UnidadConstruccion.Identificador": "OP_BUILDING_UNIT_T_IDENTIFICATION_F",
            "Operacion.Operacion.OP_UnidadConstruccion.Planta_Ubicacion": "OP_BUILDING_UNIT_T_FLOOR_F",
            "Operacion.Operacion.OP_UnidadConstruccion.Uso": "OP_BUILDING_UNIT_T_USE_F",
            "Operacion.Operacion.op_construccion_unidadconstruccion.op_construccion..Operacion.Operacion.OP_Construccion": "OP_BUILDING_UNIT_T_BUILDING_F",
            "Operacion.Operacion.OP_UnidadConstruccion.Anio_Construccion": "OP_BUILDING_UNIT_T_YEAR_OF_BUILDING_F",
            "Operacion.Operacion.OP_UnidadConstruccion.Observaciones": "OP_BUILDING_UNIT_T_OBSERVATIONS_F",
            "Operacion.Operacion.OP_UnidadConstruccion.Tipo_Construccion": "OP_BUILDING_UNIT_T_BUILDING_TYPE_F",
            "Operacion.Operacion.OP_UnidadConstruccion.Tipo_Dominio": "OP_BUILDING_UNIT_T_DOMAIN_TYPE_F",
            "Operacion.Operacion.OP_UnidadConstruccion.Tipo_Planta": "OP_BUILDING_UNIT_T_FLOOR_TYPE_F",
            "Operacion.Operacion.OP_UnidadConstruccion.Tipo_Unidad_Construccion": "OP_BUILDING_UNIT_T_BUILDING_UNIT_TYPE_F",
            "Operacion.Operacion.OP_UnidadConstruccion.Total_Banios": "OP_BUILDING_UNIT_T_TOTAL_BATHROOMS_F",
            "Operacion.Operacion.OP_UnidadConstruccion.Total_Habitaciones": "OP_BUILDING_UNIT_T_TOTAL_ROOMS_F",
            "Operacion.Operacion.OP_UnidadConstruccion.Total_Locales": "OP_BUILDING_UNIT_T_TOTAL_LOCALS_F",
            "Operacion.Operacion.OP_UnidadConstruccion.Total_Pisos": "OP_BUILDING_UNIT_T_TOTAL_FLOORS_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Dimension": "COL_SPATIAL_UNIT_T_DIMENSION_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Etiqueta": "COL_SPATIAL_UNIT_T_LABEL_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Geometria": "COL_SPATIAL_UNIT_T_GEOMETRY_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie": "COL_SPATIAL_UNIT_T_SURFACE_RELATION_F",
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Operacion.Operacion.OP_Construccion": {VARIABLE_NAME: "OP_BUILDING_T", FIELDS_DICT: {
            "Operacion.Operacion.OP_Construccion.Area_Construccion": "OP_BUILDING_T_BUILDING_AREA_F",
            "Operacion.Operacion.OP_Construccion.Avaluo_Construccion": "OP_BUILDING_T_BUILDING_VALUATION_F",
            "Operacion.Operacion.OP_Construccion.Numero_Pisos": "OP_BUILDING_T_NUMBER_OF_FLOORS_F",
            "Operacion.Operacion.OP_Construccion.Codigo_Edificacion": "OP_BUILDING_T_BUILDING_CODE_F",
            "Operacion.Operacion.OP_Construccion.Identificador": "OP_BUILDING_T_IDENTIFIER_F",
            "Operacion.Operacion.OP_Construccion.Numero_Mezanines": "OP_BUILDING_T_NUMBER_OF_MEZZANINE_F",
            "Operacion.Operacion.OP_Construccion.Numero_Semisotanos": "OP_BUILDING_T_NUMBER_OF_LOOKOUT_BASEMENT_F",
            "Operacion.Operacion.OP_Construccion.Numero_Sotanos": "OP_BUILDING_T_NUMBER_OF_BASEMENT_F",
            "Operacion.Operacion.OP_Construccion.Tipo_Construccion": "OP_BUILDING_T_BUILDING_TYPE_F",
            "Operacion.Operacion.OP_Construccion.Tipo_Dominio": "OP_BUILDING_T_DOMAIN_TYPE_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Dimension": "COL_SPATIAL_UNIT_T_DIMENSION_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Etiqueta": "COL_SPATIAL_UNIT_T_LABEL_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Geometria": "COL_SPATIAL_UNIT_T_GEOMETRY_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie": "COL_SPATIAL_UNIT_T_SURFACE_RELATION_F",
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Operacion.Operacion.OP_Derecho": {VARIABLE_NAME: "OP_RIGHT_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_baunitRrr.unidad..Operacion.Operacion.OP_Predio": "COL_BAUNIT_RRR_T_UNIT_F",
            "Operacion.Operacion.OP_Derecho.Tipo": "OP_RIGHT_T_TYPE_F",
            "LADM_COL.LADM_Nucleo.COL_RRR.Comprobacion_Comparte": "COL_RRR_T_SHARE_CHECK_F",
            "LADM_COL.LADM_Nucleo.COL_RRR.Descripcion": "COL_RRR_T_DESCRIPTION_F",
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.COL_RRR.Uso_Efectivo": "COL_RRR_T_EFFECTIVE_USAGE_F",
            "LADM_COL.LADM_Nucleo.col_rrrInteresado.interesado..Operacion.Operacion.OP_Interesado": "COL_RRR_PARTY_T_OP_PARTY_F",
            "LADM_COL.LADM_Nucleo.col_rrrInteresado.interesado..Operacion.Operacion.OP_Agrupacion_Interesados": "COL_RRR_PARTY_T_OP_GROUP_PARTY_F",
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
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Tipo_Principal": "COL_SOURCE_T_MAIN_TYPE_F"
        }},
        "Operacion.Operacion.OP_FuenteEspacial": {VARIABLE_NAME: "OP_SPATIAL_SOURCE_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.COL_FuenteEspacial.Tipo": "COL_SPATIAL_SOURCE_T_TYPE_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Estado_Disponibilidad": "COL_SOURCE_T_AVAILABILITY_STATUS_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Fecha_Documento_Fuente": "COL_SOURCE_T_DATE_DOCUMENT_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Oficialidad": "COL_SOURCE_T_OFFICIAL_F",
            # "LADM_COL.LADM_Nucleo.COL_Fuente.Procedencia": "COL_SOURCE_T_PROVENANCE_F",
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
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
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Operacion.Operacion.OP_Lindero": {VARIABLE_NAME: "OP_BOUNDARY_T", FIELDS_DICT: {
            "Operacion.Operacion.OP_Lindero.Longitud": "OP_BOUNDARY_T_LENGTH_F",
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
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
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Operacion.Operacion.op_predio_copropiedad": {VARIABLE_NAME: "OP_COPROPERTY_T", FIELDS_DICT: {
            "Operacion.Operacion.op_predio_copropiedad.coeficiente..Operacion.Operacion.op_predio_copropiedad": "FRACTION_S_COPROPERTY_COEFFICIENT_F"
        }},
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
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
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
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
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
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Operacion.Operacion.OP_Restriccion": {VARIABLE_NAME: "OP_RESTRICTION_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_baunitRrr.unidad..Operacion.Operacion.OP_Predio": "COL_BAUNIT_RRR_T_UNIT_F",
            "Operacion.Operacion.OP_Restriccion.Tipo": "OP_RESTRICTION_T_TYPE_F",
            "LADM_COL.LADM_Nucleo.COL_RRR.Comprobacion_Comparte": "COL_RRR_T_SHARE_CHECK_F",
            "LADM_COL.LADM_Nucleo.COL_RRR.Descripcion": "COL_RRR_T_DESCRIPTION_F",
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.COL_RRR.Uso_Efectivo": "COL_RRR_T_EFFECTIVE_USAGE_F",
            "LADM_COL.LADM_Nucleo.col_rrrInteresado.interesado..Operacion.Operacion.OP_Interesado": "COL_RRR_PARTY_T_OP_PARTY_F",
            "LADM_COL.LADM_Nucleo.col_rrrInteresado.interesado..Operacion.Operacion.OP_Agrupacion_Interesados": "COL_RRR_PARTY_T_OP_GROUP_PARTY_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Operacion.Operacion.OP_ServidumbrePaso": {VARIABLE_NAME: "OP_RIGHT_OF_WAY_T", FIELDS_DICT: {
            "Operacion.Operacion.OP_ServidumbrePaso.Area_Servidumbre": "OP_RIGHT_OF_WAY_T_RIGHT_OF_WAY_AREA_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Dimension": "COL_SPATIAL_UNIT_T_DIMENSION_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Etiqueta": "COL_SPATIAL_UNIT_T_LABEL_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Geometria": "COL_SPATIAL_UNIT_T_GEOMETRY_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie": "COL_SPATIAL_UNIT_T_SURFACE_RELATION_F",
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Operacion.Operacion.OP_Terreno": {VARIABLE_NAME: "OP_PLOT_T", FIELDS_DICT: {
            "Operacion.Operacion.OP_Terreno.Area_Terreno": "OP_PLOT_T_PLOT_AREA_F",
            "Operacion.Operacion.OP_Terreno.Avaluo_Terreno": "OP_PLOT_T_PLOT_VALUATION_F",
            "Operacion.Operacion.OP_Terreno.Geometria": "OP_PLOT_T_GEOMETRY_F",
            "Operacion.Operacion.OP_Terreno.Manzana_Vereda_Codigo": "OP_PLOT_T_BLOCK_RURAL_DIVISION_CODE_F",
            "Operacion.Operacion.OP_Terreno.Numero_Subterraneos": "OP_PLOT_T_NUMBER_OF_UNDERGROUND_ROOMS_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Dimension": "COL_SPATIAL_UNIT_T_DIMENSION_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Etiqueta": "COL_SPATIAL_UNIT_T_LABEL_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie": "COL_SPATIAL_UNIT_T_SURFACE_RELATION_F",
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Operacion.OP_FuenteAdministrativaTipo": {VARIABLE_NAME: "OP_ADMINISTRATIVE_SOURCE_TYPE_D", FIELDS_DICT: {}},
        "Operacion.OP_FotoidentificacionTipo": {VARIABLE_NAME: "OP_PHOTO_IDENTIFICATION_TYPE_D", FIELDS_DICT: {}},
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
            "LADM_COL.LADM_Nucleo.COL_FuenteEspacial.Mediciones..Operacion.Operacion.OP_FuenteEspacial": "COL_SPATIAL_SOURCE_T_MEASUREMENTS_F"
        }}
    }

    def __init__(self):
        self.logger = Logger()
        self._cached_domain_values = dict()

    def initialize_table_and_field_names(self, dict_names):
        """
        Update class variables (table and field names) according to a dictionary of names coming from a DB connection.
        This function should be called when a new DB connection is established for making all classes in the plugin able
        to access current DB connection names.

        :param dict_names: Expected dict with key as iliname (fully qualified object name in the model) with no version
                           info, and value as sqlname (produced by ili2db).
        :return: True if anything is updated, False otherwise.
        """
        self.reset_table_and_field_names()  # We will start mapping from scratch, so reset any previous mapping.

        any_update = False
        table_names_count = 0
        field_names_count = 0
        if dict_names:
            if T_ID_KEY not in dict_names or DISPLAY_NAME_KEY not in dict_names or ILICODE_KEY not in dict_names or DESCRIPTION_KEY not in dict_names:
                self.logger.error(__name__, "dict_names is not properly built, at least one of these required fields was not found T_ID, DISPLAY_NAME, ILICODE and DESCRIPTION.")
                return False

            for table_key, attrs in self.TABLE_DICT.items():
                if table_key in dict_names:
                    setattr(self, attrs[self.VARIABLE_NAME], dict_names[table_key][QueryNames.TABLE_NAME])
                    table_names_count += 1
                    any_update = True
                    for field_key, field_variable in attrs[self.FIELDS_DICT].items():
                        if field_key in dict_names[table_key]:
                            setattr(self, field_variable, dict_names[table_key][field_key])
                            field_names_count += 1

            # Required fields mapped in a custom way
            self.T_ID_F = dict_names[T_ID_KEY] if T_ID_KEY in dict_names else None
            self.ILICODE_F = dict_names[ILICODE_KEY] if ILICODE_KEY in dict_names else None
            self.DESCRIPTION_F = dict_names[DESCRIPTION_KEY] if DESCRIPTION_KEY in dict_names else None
            self.DISPLAY_NAME_F = dict_names[DISPLAY_NAME_KEY] if DISPLAY_NAME_KEY in dict_names else None

        self.logger.info(__name__, "Table and field names have been set!")
        self.logger.debug(__name__, "Number of table names set: {}".format(table_names_count))
        self.logger.debug(__name__, "Number of field names set: {}".format(field_names_count))
        return any_update

    def reset_table_and_field_names(self):
        """
        Make all table and field variables None again to prepare the next mapping.
        """
        for table_key, attrs in self.TABLE_DICT.items():
            setattr(self, attrs[self.VARIABLE_NAME], None)
            for field_key, field_variable in attrs[self.FIELDS_DICT].items():
                setattr(self, field_variable, None)

        self.T_ID_F = None
        self.ILICODE_F = None
        self.DESCRIPTION_F = None
        self.DISPLAY_NAME_F = None

        # Clear cache
        self._cached_domain_values = dict()

        self.logger.info(__name__, "Names (DB mapping) have been reset to prepare the next mapping.")

    def cache_domain_value(self, domain_table, t_id, value, value_is_ilicode):
        key = "{}..{}".format('ilicode' if value_is_ilicode else 'dispname', value)

        if domain_table in self._cached_domain_values:
            self._cached_domain_values[domain_table][key] = t_id
        else:
            self._cached_domain_values[domain_table] = {key: t_id}

    def get_domain_value(self, domain_table, t_id):
        """
        Get a domain value from the cache.

        :param domain_table: Domain table name.
        :param t_id: t_id to be searched.
        :return: iliCode of the corresponding t_id.
        """
        if domain_table in self._cached_domain_values:
            for k,v in self._cached_domain_values[domain_table].items():
                if v == t_id:
                    return True, k.split("..")[1]  # Compound key: ilicode..value or dispname..value

        return False, None

    def get_domain_code(self, domain_table, value, value_is_ilicode):
        """
        Get a domain code from the cache.

        :param domain_table: Domain table name.
        :param value: value to be searched.
        :param value_is_ilicode: Whether the value is iliCode (True) or dispName (False)
        :return: tuple (found, t_id)
                        found: boolean, whether the value was found in cache or not
                        t_id: t_id of the corresponding ilicode
        """
        key = "{}..{}".format('ilicode' if value_is_ilicode else 'dispname', value)
        if domain_table in self._cached_domain_values:
            if key in self._cached_domain_values[domain_table]:
                return True, self._cached_domain_values[domain_table][key]

        return  False, None

    def test_names(self, table_and_field_names):
        """
        Test whether required table/field names are present.

        :param table_and_field_names: List of table and field names present in the db
        :return: Tuple (bool: Names are valid or not, string: Message to indicate what exactly failed)
        """
        # Names that are mapped in the code
        mapped_names = dict()
        for k, v in self.TABLE_DICT.items():
            mapped_names[k] = v[self.VARIABLE_NAME]
            for k1, v1 in v[self.FIELDS_DICT].items():
                mapped_names[k1] = v1

        # Iterate names from DB and add to a list to check only those that coming from the DB are also mapped in code
        required_names = list(set([mapped_names[name] for name in table_and_field_names if name in mapped_names]))
        if not required_names:
            return (False, "The DB has no table or field names to check! As is, the plugin cannot get tables or fields from it!")
        not_mapped = list(set([name for name in table_and_field_names if not name in mapped_names]))
        self.logger.debug(__name__, "DB names not mapped in code ({}): First 10 --> {}".format(len(not_mapped), not_mapped[:10]))
        self.logger.debug(__name__, "Number of required names: {}".format(len(required_names)))
        required_names.extend(["T_ID_F",
                               "ILICODE_F",
                               "DESCRIPTION_F",
                               "DISPLAY_NAME_F"])

        names_not_found = list()
        for required_name in required_names:
            if getattr(self, required_name) is None:
                names_not_found.append(required_name)

        self.logger.debug(__name__, "Variable names not properly set: {}".format(names_not_found))
        if names_not_found:
            return (False, "Name '{}' was not found!".format(names_not_found[0]))

        return (True, "")
