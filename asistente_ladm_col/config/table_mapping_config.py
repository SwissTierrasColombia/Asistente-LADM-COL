from qgis.core import NULL

TABLE_NAME = 'table_name'
VARIABLE_NAME = 'variable'
FIELDS_DICT = 'fields_dict'

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Names(metaclass=Singleton):
    """
    Singleton to handle table and field names in a single point of access
    """

    ############################################ TABLE VARIABLES ###########################################################
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

    # "LADM_COL_V1_2.LADM_Nucleo.baunitComoInteresado"
    # "LADM_COL_V1_2.LADM_Nucleo.baunitFuente"
    # "LADM_COL_V1_2.LADM_Nucleo.baunitRrr"
    # "LADM_COL_V1_2.LADM_Nucleo.cclFuente"
    # "LADM_COL_V1_2.LADM_Nucleo.CC_MetodoOperacion"
    #
    # "LADM_COL_V1_2.LADM_Nucleo.CI_CodigoTarea"
    # "LADM_COL_V1_2.LADM_Nucleo.CI_Contacto"
    # "LADM_COL_V1_2.LADM_Nucleo.CI_Forma_Presentacion_Codigo"
    # "LADM_COL_V1_2.LADM_Nucleo.CI_ParteResponsable"
    #
    # "LADM_COL_V1_2.LADM_Nucleo.clFuente"

    COL_GROUP_PARTY_T = None  # "LADM_COL_V1_2.LADM_Nucleo.COL_Agrupacion_Interesados"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_AgrupacionUnidadesEspaciales"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_AreaTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_AreaValor"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_BAUnit"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_CadenaCarasLimite"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_CarasLindero"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_ContenidoNivelTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_EspacioJuridicoRedServicios"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_EspacioJuridicoUnidadEdificacion"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_EstadoDisponibilidadTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_EstructuraTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_FuenteAdministrativa"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_FuenteAdministrativaTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_FuenteEspacial"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_FuenteEspacialTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_FuncionInteresadoTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_FuncionInteresadoTipo_"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_GrupoInteresadoTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Interesado"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_InterpolacionTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_MetodoProduccionTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_MonumentacionTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Nivel"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_RedServiciosTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_RRR"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEdificacionTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial"

    # "LADM_COL_V1_2.LADM_Nucleo.DQ_AbsoluteExternalPositionalAccuracy"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Metodo_Evaluacion_Codigo_Tipo"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_PositionalAccuracy"

    EXT_FILE_S = None  # "LADM_COL_V1_2.LADM_Nucleo.ExtArchivo"
    EXT_ADDRESS_S = None  # "LADM_COL_V1_2.LADM_Nucleo.ExtDireccion"
    EXT_PARTY_S = None  # "LADM_COL_V1_2.LADM_Nucleo.ExtInteresado"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtRedServiciosFisica"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtUnidadEdificacionFisica"
    FRACTION_S = None  # "LADM_COL_V1_2.LADM_Nucleo.Fraccion"
    # "LADM_COL_V1_2.LADM_Nucleo.Imagen"
    # "LADM_COL_V1_2.LADM_Nucleo.ISO19125_Tipo"

    LA_GROUP_PARTY_TYPE_D = None  # "LADM_COL_V1_2.LADM_Nucleo.LA_Agrupacion_Interesados_Tipo"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_BAUnitTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_ContenidoNivelTipo"
    LA_RIGHT_TYPE_D = None  # "LADM_COL_V1_2.LADM_Nucleo.LA_DerechoTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_DimensionTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_EstadoDisponibilidadTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_EstadoRedServiciosTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_EstructuraTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_FuenteAdministrativaTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_FuenteEspacialTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_HipotecaTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_InterpolacionTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_MonumentacionTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_PuntoTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_RedServiciosTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_RegistroTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_RelacionNecesariaBAUnits"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_RelacionNecesariaUnidadesEspaciales"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_RelacionSuperficieTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_ResponsabilidadTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_RestriccionTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_TareaInteresadoTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_TareaInteresadoTipo.Tipo"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_Transformacion"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_UnidadEdificacionTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_VolumenTipo"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_VolumenValor"
    # "LADM_COL_V1_2.LADM_Nucleo.LI_Lineaje"
    MORE_BFS_T = "LADM_COL_V1_2.LADM_Nucleo.masCcl"
    # "LADM_COL_V1_2.LADM_Nucleo.masCl"
    LESS_BFS_T = None  # "LADM_COL_V1_2.LADM_Nucleo.menosCcl"
    # "LADM_COL_V1_2.LADM_Nucleo.menosCl"
    MEMBERS_T = None  # "LADM_COL_V1_2.LADM_Nucleo.miembros"
    # VERSIONED_OBJECT_T = "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado"
    # OID_T = "LADM_COL_V1_2.LADM_Nucleo.Oid"
    # "LADM_COL_V1_2.LADM_Nucleo.OM_Observacion"
    # "LADM_COL_V1_2.LADM_Nucleo.OM_Proceso"
    POINT_BFS_T = None  # "LADM_COL_V1_2.LADM_Nucleo.puntoCcl"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoCl"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoFuente"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoReferencia"
    # "LADM_COL_V1_2.LADM_Nucleo.relacionFuente"
    # "LADM_COL_V1_2.LADM_Nucleo.relacionFuenteUespacial"
    # "LADM_COL_V1_2.LADM_Nucleo.responsableFuente"
    RRR_SOURCE_T = None  # "LADM_COL_V1_2.LADM_Nucleo.rrrFuente"
    # "LADM_COL_V1_2.LADM_Nucleo.rrrInteresado"
    # "LADM_COL_V1_2.LADM_Nucleo.topografoFuente"
    UE_BAUNIT_T = None  # "LADM_COL_V1_2.LADM_Nucleo.ueBaunit"
    # "LADM_COL_V1_2.LADM_Nucleo.ueFuente"
    # "LADM_COL_V1_2.LADM_Nucleo.ueJerarquiaGrupo"
    # "LADM_COL_V1_2.LADM_Nucleo.ueNivel"
    # "LADM_COL_V1_2.LADM_Nucleo.ueUeGrupo"
    # "LADM_COL_V1_2.LADM_Nucleo.unidadFuente"
    # "Operacion_V2_9_5.OP_AcuerdoTipo"
    OP_PARCEL_TYPE_T = None  # "Operacion_V2_9_5.OP_CondicionPredioTipo"
    OP_RIGHT_TYPE_T = None  # "Operacion_V2_9_5.OP_DerechoTipo"
    OP_GROUP_TYPE_T = None  # "Operacion_V2_9_5.Operacion.OP_Agrupacion_Interesados"
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
    # "Operacion_V2_9_5.Operacion.op_predio_copropiedad"
    # "Operacion_V2_9_5.Operacion.op_predio_insumos_operacion"
    OP_CONTROL_POINT_T = None  # "Operacion_V2_9_5.Operacion.OP_PuntoControl"
    OP_SURVEY_POINT_T = None  # "Operacion_V2_9_5.Operacion.OP_PuntoLevantamiento"
    OP_BOUNDARY_POINT_T = None  # "Operacion_V2_9_5.Operacion.OP_PuntoLindero"
    OP_RESTRICTION_T = None  # "Operacion_V2_9_5.Operacion.OP_Restriccion"
    OP_RIGHT_OF_WAY_T = None  # "Operacion_V2_9_5.Operacion.OP_ServidumbrePaso"
    OP_PLOT_T = None  # "Operacion_V2_9_5.Operacion.OP_Terreno"
    OP_BUILDING_TYPE = None  # "Operacion_V2_9_5.Operacion.OP_UnidadConstruccion"
    # "Operacion_V2_9_5.OP_FotoidentificacionTipo"
    OP_ADMINISTRATIVE_SOURCE_TYPE_D = None  # "Operacion_V2_9_5.OP_FuenteAdministrativaTipo"
    # "Operacion_V2_9_5.OP_GrupoEtnicoTipo"
    # "Operacion_V2_9_5.OP_InstitucionTipo"
    OP_PARTY_DOCUMENT_TYPE_D = None  # "Operacion_V2_9_5.OP_InteresadoDocumentoTipo"
    OP_PARTY_TYPE_D = None  # "Operacion_V2_9_5.OP_InteresadoTipo"
    OP_PARCEL_TYPE_D = None  # "Operacion_V2_9_5.OP_PredioTipo"
    OP_CONTROL_POINT_TYPE_D = None  # "Operacion_V2_9_5.OP_PuntoControlTipo"
    OP_SURVEY_POINT_TYPE_D = None  # "Operacion_V2_9_5.OP_PuntoLevTipo"
    OP_POINT_TYPE_D = None  # "Operacion_V2_9_5.OP_PuntoTipo"
    OP_RESTRICTION_TYPE = None  # "Operacion_V2_9_5.OP_RestriccionTipo"
    OP_GENRE_D = None  # "Operacion_V2_9_5.OP_SexoTipo"
    # "Operacion_V2_9_5.OP_UbicacionPuntoTipo"
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
    # "LADM_COL_V1_2.LADM_Nucleo.baunitComoInteresado.interesado"
    # "LADM_COL_V1_2.LADM_Nucleo.baunitComoInteresado.interesado"
    # "LADM_COL_V1_2.LADM_Nucleo.baunitComoInteresado.unidad"
    # "LADM_COL_V1_2.LADM_Nucleo.baunitFuente.bfuente"
    # "LADM_COL_V1_2.LADM_Nucleo.baunitFuente.unidad"
    # "LADM_COL_V1_2.LADM_Nucleo.baunitRrr.unidad"
    # "LADM_COL_V1_2.LADM_Nucleo.baunitRrr.unidad"
    # "LADM_COL_V1_2.LADM_Nucleo.cclFuente.ccl"
    # "LADM_COL_V1_2.LADM_Nucleo.cclFuente.lfuente"
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
    # "LADM_COL_V1_2.LADM_Nucleo.clFuente.cfuente"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Agrupacion_Interesados.Tipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_AreaValor.areaSize"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_AreaValor.type"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_BAUnit.Nombre"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_BAUnit.u_Espacio_De_Nombres"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_BAUnit.u_Local_Id"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_CadenaCarasLimite.ccl_Espacio_De_Nombres"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_CadenaCarasLimite.ccl_Local_Id"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_CadenaCarasLimite.Geometria"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_CadenaCarasLimite.Localizacion_Textual"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_FuenteAdministrativa.Numero_Fuente"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_FuenteAdministrativa.Observacion"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_FuenteEspacial.Mediciones"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_FuenteEspacial.Procedimiento"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_FuenteEspacial.Tipo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Estado_Disponibilidad"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Estado_Disponibilidad"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Fecha_Documento_Fuente"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Fecha_Documento_Fuente"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Oficialidad"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Oficialidad"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Procedencia"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Procedencia"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.s_Espacio_De_Nombres"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.s_Espacio_De_Nombres"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.s_Local_Id"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.s_Local_Id"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Tipo_Principal"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Fuente.Tipo_Principal"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_FuncionInteresadoTipo_.value"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Interesado.ext_PID"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Interesado.ext_PID"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Interesado.Nombre"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Interesado.Nombre"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Interesado.p_Espacio_De_Nombres"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Interesado.p_Espacio_De_Nombres"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Interesado.p_Local_Id"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Interesado.p_Local_Id"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Interesado.Tarea"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Interesado.Tarea"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Exactitud_Estimada"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Exactitud_Estimada"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Exactitud_Estimada"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Exactitud_Estimada"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Exactitud_Estimada"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Exactitud_Estimada"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Localizacion_Original"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Localizacion_Original"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Localizacion_Original"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.MetodoProduccion"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.MetodoProduccion"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.MetodoProduccion"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Monumentacion"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Monumentacion"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Monumentacion"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.p_Espacio_De_Nombres"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.p_Espacio_De_Nombres"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.p_Espacio_De_Nombres"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.p_Local_Id"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.p_Local_Id"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.p_Local_Id"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Posicion_Interpolacion"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Posicion_Interpolacion"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Posicion_Interpolacion"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Transformacion_Y_Resultado"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Transformacion_Y_Resultado"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_Punto.Transformacion_Y_Resultado"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_RRR.Compartido"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_RRR.Compartido"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_RRR.Comprobacion_Comparte"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_RRR.Comprobacion_Comparte"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_RRR.Descripcion"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_RRR.Descripcion"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_RRR.r_Espacio_De_Nombres"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_RRR.r_Espacio_De_Nombres"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_RRR.r_Local_Id"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_RRR.r_Local_Id"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_RRR.Uso_Efectivo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_RRR.Uso_Efectivo"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Area"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Area"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Area"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Area"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Dimension"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Dimension"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Dimension"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Dimension"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Etiqueta"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Etiqueta"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Etiqueta"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Etiqueta"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.poligono_creado"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.poligono_creado"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.poligono_creado"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.poligono_creado"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.su_Espacio_De_Nombres"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.su_Espacio_De_Nombres"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.su_Espacio_De_Nombres"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.su_Espacio_De_Nombres"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.su_Local_Id"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.su_Local_Id"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.su_Local_Id"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.su_Local_Id"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Volumen"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Volumen"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Volumen"
    # "LADM_COL_V1_2.LADM_Nucleo.COL_UnidadEspacial.Volumen"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_AbsoluteExternalPositionalAccuracy.atributo1"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element.Descripcion_Medida"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element.Descripcion_Medida"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element.Descripcion_Medida"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element.Descripcion_Metodo_Evaluacion"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element.Descripcion_Metodo_Evaluacion"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element.Descripcion_Metodo_Evaluacion"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element.Fecha_Hora"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element.Fecha_Hora"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element.Fecha_Hora"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element.Identificacion_Medida"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element.Identificacion_Medida"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element.Identificacion_Medida"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element.Metodo_Evaluacion"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element.Metodo_Evaluacion"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element.Metodo_Evaluacion"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element.Nombre_Medida"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element.Nombre_Medida"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element.Nombre_Medida"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element.Procedimiento_Evaluacion"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element.Procedimiento_Evaluacion"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element.Procedimiento_Evaluacion"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element.Resultado"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element.Resultado"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_Element.Resultado"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_PositionalAccuracy.atributo21"
    # "LADM_COL_V1_2.LADM_Nucleo.DQ_PositionalAccuracy.atributo21"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtArchivo.Datos"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtArchivo.Extraccion"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtArchivo.Fecha_Aceptacion"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtArchivo.Fecha_Entrega"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtArchivo.Fecha_Grabacion"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtArchivo.s_Espacio_De_Nombres"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtArchivo.s_Local_Id"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtDireccion.Apartado_Correo"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtDireccion.Ciudad"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtDireccion.Codigo_Postal"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtDireccion.Coordenada_Direccion"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtDireccion.Departamento"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtDireccion.Direccion_ID"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtDireccion.Nombre_Area_Direccion"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtDireccion.Nombre_Calle"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtDireccion.Nombre_Edificio"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtDireccion.Numero_Edificio"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtDireccion.Pais"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtInteresado.Ext_Direccion_ID"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtInteresado.Firma"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtInteresado.Fotografia"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtInteresado.Huella_Dactilar"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtInteresado.Interesado_ID"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtInteresado.Nombre"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtRedServiciosFisica.Ext_Interesado_Administrador_ID"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtRedServiciosFisica.Orientada"
    # "LADM_COL_V1_2.LADM_Nucleo.ExtUnidadEdificacionFisica.Ext_Direccion_ID"
    # "LADM_COL_V1_2.LADM_Nucleo.Fraccion.Denominador"
    # "LADM_COL_V1_2.LADM_Nucleo.Fraccion.Numerador"
    # "LADM_COL_V1_2.LADM_Nucleo.Imagen.uri"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_TareaInteresadoTipo.Tipo"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_Transformacion.Localizacion_Transformada"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_Transformacion.Transformacion"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_VolumenValor.Tipo"
    # "LADM_COL_V1_2.LADM_Nucleo.LA_VolumenValor.Volumen_Medicion"
    # "LADM_COL_V1_2.LADM_Nucleo.LI_Lineaje.Statement"
    # "LADM_COL_V1_2.LADM_Nucleo.masCcl.ccl_mas"
    # "LADM_COL_V1_2.LADM_Nucleo.masCcl.ue_mas"
    # "LADM_COL_V1_2.LADM_Nucleo.masCcl.ue_mas"
    # "LADM_COL_V1_2.LADM_Nucleo.masCcl.ue_mas"
    # "LADM_COL_V1_2.LADM_Nucleo.masCcl.ue_mas"
    # "LADM_COL_V1_2.LADM_Nucleo.masCl.ue_mas"
    # "LADM_COL_V1_2.LADM_Nucleo.masCl.ue_mas"
    # "LADM_COL_V1_2.LADM_Nucleo.masCl.ue_mas"
    # "LADM_COL_V1_2.LADM_Nucleo.masCl.ue_mas"
    # "LADM_COL_V1_2.LADM_Nucleo.menosCcl.ccl_menos"
    # "LADM_COL_V1_2.LADM_Nucleo.menosCcl.ue_menos"
    # "LADM_COL_V1_2.LADM_Nucleo.menosCcl.ue_menos"
    # "LADM_COL_V1_2.LADM_Nucleo.menosCcl.ue_menos"
    # "LADM_COL_V1_2.LADM_Nucleo.menosCcl.ue_menos"
    # "LADM_COL_V1_2.LADM_Nucleo.menosCl.ue_menos"
    # "LADM_COL_V1_2.LADM_Nucleo.menosCl.ue_menos"
    # "LADM_COL_V1_2.LADM_Nucleo.menosCl.ue_menos"
    # "LADM_COL_V1_2.LADM_Nucleo.menosCl.ue_menos"
    # "LADM_COL_V1_2.LADM_Nucleo.miembros.agrupacion"
    # "LADM_COL_V1_2.LADM_Nucleo.miembros.interesados"
    # "LADM_COL_V1_2.LADM_Nucleo.miembros.interesados"
    # "LADM_COL_V1_2.LADM_Nucleo.miembros.participacion"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL_V1_2.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL_V1_2.LADM_Nucleo.Oid.espacioDeNombres"
    # "LADM_COL_V1_2.LADM_Nucleo.Oid.localId"
    # "LADM_COL_V1_2.LADM_Nucleo.OM_Observacion.Resultado_Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.OM_Observacion.Resultado_Calidad"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoCcl.ccl"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoCcl.punto"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoCcl.punto"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoCcl.punto"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoCl.punto"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoCl.punto"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoCl.punto"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoFuente.pfuente"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoFuente.punto"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoFuente.punto"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoFuente.punto"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoReferencia.ue"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoReferencia.ue"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoReferencia.ue"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoReferencia.ue"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoReferencia.ue"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoReferencia.ue"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoReferencia.ue"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoReferencia.ue"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoReferencia.ue"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoReferencia.ue"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoReferencia.ue"
    # "LADM_COL_V1_2.LADM_Nucleo.puntoReferencia.ue"
    # "LADM_COL_V1_2.LADM_Nucleo.relacionFuente.refuente"
    # "LADM_COL_V1_2.LADM_Nucleo.relacionFuenteUespacial.rfuente"
    # "LADM_COL_V1_2.LADM_Nucleo.responsableFuente.cfuente"
    # "LADM_COL_V1_2.LADM_Nucleo.responsableFuente.notario"
    # "LADM_COL_V1_2.LADM_Nucleo.responsableFuente.notario"
    # "LADM_COL_V1_2.LADM_Nucleo.rrrFuente.rfuente"
    # "LADM_COL_V1_2.LADM_Nucleo.rrrFuente.rrr"
    # "LADM_COL_V1_2.LADM_Nucleo.rrrFuente.rrr"
    # "LADM_COL_V1_2.LADM_Nucleo.rrrInteresado.interesado"
    # "LADM_COL_V1_2.LADM_Nucleo.rrrInteresado.interesado"
    # "LADM_COL_V1_2.LADM_Nucleo.rrrInteresado.interesado"
    # "LADM_COL_V1_2.LADM_Nucleo.rrrInteresado.interesado"
    # "LADM_COL_V1_2.LADM_Nucleo.topografoFuente.sfuente"
    # "LADM_COL_V1_2.LADM_Nucleo.topografoFuente.topografo"
    # "LADM_COL_V1_2.LADM_Nucleo.topografoFuente.topografo"
    # "LADM_COL_V1_2.LADM_Nucleo.ueBaunit.baunit"
    # "LADM_COL_V1_2.LADM_Nucleo.ueBaunit.ue"
    # "LADM_COL_V1_2.LADM_Nucleo.ueBaunit.ue"
    # "LADM_COL_V1_2.LADM_Nucleo.ueBaunit.ue"
    # "LADM_COL_V1_2.LADM_Nucleo.ueBaunit.ue"
    # "LADM_COL_V1_2.LADM_Nucleo.ueFuente.pfuente"
    # "LADM_COL_V1_2.LADM_Nucleo.ueFuente.ue"
    # "LADM_COL_V1_2.LADM_Nucleo.ueFuente.ue"
    # "LADM_COL_V1_2.LADM_Nucleo.ueFuente.ue"
    # "LADM_COL_V1_2.LADM_Nucleo.ueFuente.ue"
    # "LADM_COL_V1_2.LADM_Nucleo.ueUeGrupo.parte"
    # "LADM_COL_V1_2.LADM_Nucleo.ueUeGrupo.parte"
    # "LADM_COL_V1_2.LADM_Nucleo.ueUeGrupo.parte"
    # "LADM_COL_V1_2.LADM_Nucleo.ueUeGrupo.parte"
    # "LADM_COL_V1_2.LADM_Nucleo.unidadFuente.ufuente"
    # "LADM_COL_V1_2.LADM_Nucleo.unidadFuente.unidad"
    #
    #
    # "Operacion_V2_9_5.Operacion.OP_Construccion.Area_Construccion"
    # "Operacion_V2_9_5.Operacion.OP_Construccion.Avaluo_Construccion"
    # "Operacion_V2_9_5.Operacion.OP_Construccion.Numero_Pisos"
    # "Operacion_V2_9_5.Operacion.op_construccion_unidadconstruccion.op_construccion"
    # "Operacion_V2_9_5.Operacion.OP_Derecho.Tipo"
    # "Operacion_V2_9_5.Operacion.OP_FuenteAdministrativa.Ente_Emisor"
    # "Operacion_V2_9_5.Operacion.OP_FuenteAdministrativa.Tipo"
    # "Operacion_V2_9_5.Operacion.OP_Interesado_Contacto.Autoriza_Notificacion_Correo"
    # "Operacion_V2_9_5.Operacion.OP_Interesado_Contacto.Correo_Electronico"
    # "Operacion_V2_9_5.Operacion.OP_Interesado_Contacto.Domicilio_Notificacion"
    # "Operacion_V2_9_5.Operacion.op_interesado_contacto.op_interesado"
    # "Operacion_V2_9_5.Operacion.OP_Interesado_Contacto.Origen_Datos"
    # "Operacion_V2_9_5.Operacion.OP_Interesado_Contacto.Telefono1"
    # "Operacion_V2_9_5.Operacion.OP_Interesado_Contacto.Telefono2"
    # "Operacion_V2_9_5.Operacion.OP_Interesado.Documento_Identidad"
    # "Operacion_V2_9_5.Operacion.OP_Interesado.Grupo_Etnico"
    # "Operacion_V2_9_5.Operacion.OP_Interesado.Primer_Apellido"
    # "Operacion_V2_9_5.Operacion.OP_Interesado.Primer_Nombre"
    # "Operacion_V2_9_5.Operacion.OP_Interesado.Razon_Social"
    # "Operacion_V2_9_5.Operacion.OP_Interesado.Segundo_Apellido"
    # "Operacion_V2_9_5.Operacion.OP_Interesado.Segundo_Nombre"
    # "Operacion_V2_9_5.Operacion.OP_Interesado.Sexo"
    # "Operacion_V2_9_5.Operacion.OP_Interesado.Tipo"
    # "Operacion_V2_9_5.Operacion.OP_Interesado.Tipo_Documento"
    # "Operacion_V2_9_5.Operacion.OP_Lindero.Longitud"
    OP_PARCEL_T_VALUATION_F = None  # "Operacion_V2_9_5.Operacion.OP_Predio.Avaluo_Predio"
    OP_PARCEL_T_ORIP_CODE_F = None  # "Operacion_V2_9_5.Operacion.OP_Predio.Codigo_ORIP"
    OP_PARCEL_T_PARCEL_TYPE_F = None  # "Operacion_V2_9_5.Operacion.OP_Predio.Condicion_Predio"
    # "Operacion_V2_9_5.Operacion.op_predio_copropiedad.coeficiente"
    # "Operacion_V2_9_5.Operacion.op_predio_copropiedad.copropiedad"
    # "Operacion_V2_9_5.Operacion.op_predio_copropiedad.predio"
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
    # "Operacion_V2_9_5.Operacion.OP_PuntoControl.Exactitud_Horizontal"
    # "Operacion_V2_9_5.Operacion.OP_PuntoControl.Exactitud_Vertical"
    # "Operacion_V2_9_5.Operacion.OP_PuntoControl.ID_Punto_Control"
    # "Operacion_V2_9_5.Operacion.OP_PuntoControl.PuntoTipo"
    # "Operacion_V2_9_5.Operacion.OP_PuntoControl.Tipo_Punto_Control"
    # "Operacion_V2_9_5.Operacion.OP_PuntoLevantamiento.Exactitud_Horizontal"
    # "Operacion_V2_9_5.Operacion.OP_PuntoLevantamiento.Exactitud_Vertical"
    # "Operacion_V2_9_5.Operacion.OP_PuntoLevantamiento.Fotoidentificacion"
    # "Operacion_V2_9_5.Operacion.OP_PuntoLevantamiento.ID_Punto_Levantamiento"
    # "Operacion_V2_9_5.Operacion.OP_PuntoLevantamiento.PuntoTipo"
    # "Operacion_V2_9_5.Operacion.OP_PuntoLevantamiento.Tipo_Punto_Levantamiento"
    # "Operacion_V2_9_5.Operacion.OP_PuntoLindero.Acuerdo"
    # "Operacion_V2_9_5.Operacion.OP_PuntoLindero.Exactitud_Horizontal"
    # "Operacion_V2_9_5.Operacion.OP_PuntoLindero.Exactitud_Vertical"
    # "Operacion_V2_9_5.Operacion.OP_PuntoLindero.Fotoidentificacion"
    # "Operacion_V2_9_5.Operacion.OP_PuntoLindero.ID_Punto_Lindero"
    # "Operacion_V2_9_5.Operacion.OP_PuntoLindero.PuntoTipo"
    # "Operacion_V2_9_5.Operacion.OP_PuntoLindero.Ubicacion_Punto"
    # "Operacion_V2_9_5.Operacion.OP_Restriccion.Tipo"
    # "Operacion_V2_9_5.Operacion.OP_ServidumbrePaso.Area_Servidumbre"
    # "Operacion_V2_9_5.Operacion.OP_Terreno.Area_Terreno"
    # "Operacion_V2_9_5.Operacion.OP_Terreno.Avaluo_Terreno"
    # "Operacion_V2_9_5.Operacion.OP_Terreno.poligono_creado"
    # "Operacion_V2_9_5.Operacion.OP_UnidadConstruccion.Area_Construida"
    # "Operacion_V2_9_5.Operacion.OP_UnidadConstruccion.Area_Privada_Construida"
    # "Operacion_V2_9_5.Operacion.OP_UnidadConstruccion.Avaluo_Unidad_Construccion"
    # "Operacion_V2_9_5.Operacion.OP_UnidadConstruccion.Identificador"
    # "Operacion_V2_9_5.Operacion.OP_UnidadConstruccion.Numero_Pisos"
    # "Operacion_V2_9_5.Operacion.OP_UnidadConstruccion.Piso_Ubicacion"
    # "Operacion_V2_9_5.Operacion.OP_UnidadConstruccion.Uso"

    ####################################################### TABLE KEYS #####################################################

    K_GC_NEIGHBOURHOOD_T = "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Barrio"
    K_GC_BUILDING_T = "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Construccion"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.gc_construccion_predio"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.gc_construccion_unidad"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.gc_copropiedad"
    K_GC_HP_CONDOMINIUM_DATA_T = "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio"
    K_GC_BLOCK_T = "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Manzana"
    K_GC_PERIMETER_T = "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Perimetro"
    K_GC_HP_PARCEL_T = "Datos_Gestor_Catastral.Datos_Gestor_Catastral.gc_ph_predio"
    K_GC_PARCEL_T = "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro"
    K_GC_OWNER_T = "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietaio"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.gc_propietario_predio"
    K_GC_RURAL_SECTOR_T = "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Sector_Rural"
    K_GC_URBAN_SECTOR_T = "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Sector_Urbano"
    K_GC_PLOT_T = "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.gc_terreno_predio"
    K_GC_BUILDING_UNIT_T = "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Unidad_Construccion"
    K_GC_RURAL_DIVISION_T = "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Vereda"
    K_GC_PARCEL_TYPE_D = "Datos_Gestor_Catastral.GC_CondicionPredioTipo"
    K_GC_ADDRESS_T = "Datos_Gestor_Catastral.GC_Direccion"
    # "Datos_Gestor_Catastral.GC_SistemaProcedenciaDatosTipo"
    K_GC_BUILDING_UNIT_TYPE_T = "Datos_Gestor_Catastral.GC_UnidadConstruccionTipo"

    K_INI_PARCEL_SUPPLIES_T = "Datos_Integracion_Insumos.Datos_Integracion_Insumos.INI_Predio_Insumos"
    # "Datos_Integracion_Insumos.Datos_Integracion_Insumos.ini_predio_integracion_gc"
    # "Datos_Integracion_Insumos.Datos_Integracion_Insumos.ini_predio_integracion_snr"

    K_SNR_RIGHT_T = "Datos_SNR.Datos_SNR.SNR_Derecho"
    # "Datos_SNR.Datos_SNR.snr_derecho_predio"
    # "Datos_SNR.Datos_SNR.snr_fuente_cabidalinderos"
    K_SNR_SOURCE_BOUNDARIES_T = "Datos_SNR.Datos_SNR.SNR_Fuente_CabidaLinderos"
    # "Datos_SNR.Datos_SNR.snr_fuente_derecho"
    K_SNR_SOURCE_RIGHT_T = "Datos_SNR.Datos_SNR.SNR_Fuente_Derecho"
    K_SNR_PARCEL_REGISTRY_T = "Datos_SNR.Datos_SNR.SNR_Predio_Registro"
    K_SNR_TITLE_HOLDER_T = "Datos_SNR.Datos_SNR.SNR_Titular"
    # "Datos_SNR.Datos_SNR.snr_titular_derecho"
    K_SNR_RIGHT_TYPE_D = "Datos_SNR.SNR_CalidadDerechoTipo"
    K_SNR_TITLE_HOLDER_DOCUMENT_T = "Datos_SNR.SNR_DocumentoTitularTipo"
    K_SNR_SOURCE_TYPE_D = "Datos_SNR.SNR_FuenteTipo"
    K_SNR_TITLE_HOLDER_TYPE_D = "Datos_SNR.SNR_PersonaTitularTipo"

    # "LADM_COL.LADM_Nucleo.baunitComoInteresado"
    # "LADM_COL.LADM_Nucleo.baunitFuente"
    # "LADM_COL.LADM_Nucleo.baunitRrr"
    # "LADM_COL.LADM_Nucleo.cclFuente"
    # "LADM_COL.LADM_Nucleo.CC_MetodoOperacion"
    #
    # "LADM_COL.LADM_Nucleo.CI_CodigoTarea"
    # "LADM_COL.LADM_Nucleo.CI_Contacto"
    # "LADM_COL.LADM_Nucleo.CI_Forma_Presentacion_Codigo"
    # "LADM_COL.LADM_Nucleo.CI_ParteResponsable"
    #
    # "LADM_COL.LADM_Nucleo.clFuente"

    K_COL_GROUP_PARTY_T = "LADM_COL.LADM_Nucleo.COL_Agrupacion_Interesados"
    # "LADM_COL.LADM_Nucleo.COL_AgrupacionUnidadesEspaciales"
    # "LADM_COL.LADM_Nucleo.COL_AreaTipo"
    # "LADM_COL.LADM_Nucleo.COL_AreaValor"
    # "LADM_COL.LADM_Nucleo.COL_BAUnit"
    # "LADM_COL.LADM_Nucleo.COL_CadenaCarasLimite"
    # "LADM_COL.LADM_Nucleo.COL_CarasLindero"
    # "LADM_COL.LADM_Nucleo.COL_ContenidoNivelTipo"
    # "LADM_COL.LADM_Nucleo.COL_EspacioJuridicoRedServicios"
    # "LADM_COL.LADM_Nucleo.COL_EspacioJuridicoUnidadEdificacion"
    # "LADM_COL.LADM_Nucleo.COL_EstadoDisponibilidadTipo"
    # "LADM_COL.LADM_Nucleo.COL_EstructuraTipo"
    # "LADM_COL.LADM_Nucleo.COL_Fuente"
    # "LADM_COL.LADM_Nucleo.COL_FuenteAdministrativa"
    # "LADM_COL.LADM_Nucleo.COL_FuenteAdministrativaTipo"
    # "LADM_COL.LADM_Nucleo.COL_FuenteEspacial"
    # "LADM_COL.LADM_Nucleo.COL_FuenteEspacialTipo"
    # "LADM_COL.LADM_Nucleo.COL_FuncionInteresadoTipo"
    # "LADM_COL.LADM_Nucleo.COL_FuncionInteresadoTipo_"
    # "LADM_COL.LADM_Nucleo.COL_GrupoInteresadoTipo"
    # "LADM_COL.LADM_Nucleo.COL_Interesado"
    # "LADM_COL.LADM_Nucleo.COL_InterpolacionTipo"
    # "LADM_COL.LADM_Nucleo.COL_MetodoProduccionTipo"
    # "LADM_COL.LADM_Nucleo.COL_MonumentacionTipo"
    # "LADM_COL.LADM_Nucleo.COL_Nivel"
    # "LADM_COL.LADM_Nucleo.COL_Punto"
    # "LADM_COL.LADM_Nucleo.COL_RedServiciosTipo"
    # "LADM_COL.LADM_Nucleo.COL_RRR"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEdificacionTipo"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial"

    # "LADM_COL.LADM_Nucleo.DQ_AbsoluteExternalPositionalAccuracy"
    # "LADM_COL.LADM_Nucleo.DQ_Element"
    # "LADM_COL.LADM_Nucleo.DQ_Metodo_Evaluacion_Codigo_Tipo"
    # "LADM_COL.LADM_Nucleo.DQ_PositionalAccuracy"

    K_EXT_FILE_S = "LADM_COL.LADM_Nucleo.ExtArchivo"
    K_EXT_ADDRESS_S = "LADM_COL.LADM_Nucleo.ExtDireccion"
    K_EXT_PARTY_S = "LADM_COL.LADM_Nucleo.ExtInteresado"
    # "LADM_COL.LADM_Nucleo.ExtRedServiciosFisica"
    # "LADM_COL.LADM_Nucleo.ExtUnidadEdificacionFisica"
    K_FRACTION_S = "LADM_COL.LADM_Nucleo.Fraccion"
    # "LADM_COL.LADM_Nucleo.Imagen"
    # "LADM_COL.LADM_Nucleo.ISO19125_Tipo"

    K_LA_GROUP_PARTY_TYPE_D = "LADM_COL.LADM_Nucleo.LA_Agrupacion_Interesados_Tipo"
    # "LADM_COL.LADM_Nucleo.LA_BAUnitTipo"
    # "LADM_COL.LADM_Nucleo.LA_ContenidoNivelTipo"
    K_LA_RIGHT_TYPE_D = "LADM_COL.LADM_Nucleo.LA_DerechoTipo"
    # "LADM_COL.LADM_Nucleo.LA_DimensionTipo"
    # "LADM_COL.LADM_Nucleo.LA_EstadoDisponibilidadTipo"
    # "LADM_COL.LADM_Nucleo.LA_EstadoRedServiciosTipo"
    # "LADM_COL.LADM_Nucleo.LA_EstructuraTipo"
    # "LADM_COL.LADM_Nucleo.LA_FuenteAdministrativaTipo"
    # "LADM_COL.LADM_Nucleo.LA_FuenteEspacialTipo"
    # "LADM_COL.LADM_Nucleo.LA_HipotecaTipo"
    # "LADM_COL.LADM_Nucleo.LA_InterpolacionTipo"
    # "LADM_COL.LADM_Nucleo.LA_MonumentacionTipo"
    # "LADM_COL.LADM_Nucleo.LA_PuntoTipo"
    # "LADM_COL.LADM_Nucleo.LA_RedServiciosTipo"
    # "LADM_COL.LADM_Nucleo.LA_RegistroTipo"
    # "LADM_COL.LADM_Nucleo.LA_RelacionNecesariaBAUnits"
    # "LADM_COL.LADM_Nucleo.LA_RelacionNecesariaUnidadesEspaciales"
    # "LADM_COL.LADM_Nucleo.LA_RelacionSuperficieTipo"
    # "LADM_COL.LADM_Nucleo.LA_ResponsabilidadTipo"
    # "LADM_COL.LADM_Nucleo.LA_RestriccionTipo"
    # "LADM_COL.LADM_Nucleo.LA_TareaInteresadoTipo"
    # "LADM_COL.LADM_Nucleo.LA_TareaInteresadoTipo.Tipo"
    # "LADM_COL.LADM_Nucleo.LA_Transformacion"
    # "LADM_COL.LADM_Nucleo.LA_UnidadEdificacionTipo"
    # "LADM_COL.LADM_Nucleo.LA_VolumenTipo"
    # "LADM_COL.LADM_Nucleo.LA_VolumenValor"
    # "LADM_COL.LADM_Nucleo.LI_Lineaje"
    K_MORE_BFS_T = "LADM_COL.LADM_Nucleo.masCcl"
    # "LADM_COL.LADM_Nucleo.masCl"
    K_LESS_BFS_T = "LADM_COL.LADM_Nucleo.menosCcl"
    # "LADM_COL.LADM_Nucleo.menosCl"
    K_MEMBERS_T = "LADM_COL.LADM_Nucleo.miembros"
    # VERSIONED_OBJECT_T = "LADM_COL.LADM_Nucleo.ObjetoVersionado"
    # OID_T = "LADM_COL.LADM_Nucleo.Oid"
    # "LADM_COL.LADM_Nucleo.OM_Observacion"
    # "LADM_COL.LADM_Nucleo.OM_Proceso"
    K_POINT_BFS_T = "LADM_COL.LADM_Nucleo.puntoCcl"
    # "LADM_COL.LADM_Nucleo.puntoCl"
    # "LADM_COL.LADM_Nucleo.puntoFuente"
    # "LADM_COL.LADM_Nucleo.puntoReferencia"
    # "LADM_COL.LADM_Nucleo.relacionFuente"
    # "LADM_COL.LADM_Nucleo.relacionFuenteUespacial"
    # "LADM_COL.LADM_Nucleo.responsableFuente"
    K_RRR_SOURCE_T = "LADM_COL.LADM_Nucleo.rrrFuente"
    # "LADM_COL.LADM_Nucleo.rrrInteresado"
    # "LADM_COL.LADM_Nucleo.topografoFuente"
    K_UE_BAUNIT_T = "LADM_COL.LADM_Nucleo.ueBaunit"
    # "LADM_COL.LADM_Nucleo.ueFuente"
    # "LADM_COL.LADM_Nucleo.ueJerarquiaGrupo"
    # "LADM_COL.LADM_Nucleo.ueNivel"
    # "LADM_COL.LADM_Nucleo.ueUeGrupo"
    # "LADM_COL.LADM_Nucleo.unidadFuente"
    # "Operacion.OP_AcuerdoTipo"
    K_OP_PARCEL_TYPE_T = "Operacion.OP_CondicionPredioTipo"
    K_OP_RIGHT_TYPE_T = "Operacion.OP_DerechoTipo"
    K_OP_GROUP_TYPE_T = "Operacion.Operacion.OP_Agrupacion_Interesados"
    K_OP_BUILDING_T = "Operacion.Operacion.OP_Construccion"
    # "Operacion.Operacion.op_construccion_unidadconstruccion"
    K_OP_RIGHT_T = "Operacion.Operacion.OP_Derecho"
    K_OP_ADMINISTRATIVE_SOURCE_T = "Operacion.Operacion.OP_FuenteAdministrativa"
    K_OP_SPATIAL_SOURCE_T = "Operacion.Operacion.OP_FuenteEspacial"
    K_OP_PARTY_T = "Operacion.Operacion.OP_Interesado"
    # "Operacion.Operacion.op_interesado_contacto"
    # "Operacion.Operacion.OP_Interesado_Contacto"
    K_OP_BOUNDARY_T = "Operacion.Operacion.OP_Lindero"
    K_OP_PARCEL_T = "Operacion.Operacion.OP_Predio"
    # "Operacion.Operacion.op_predio_copropiedad"
    # "Operacion.Operacion.op_predio_insumos_operacion"
    K_OP_CONTROL_POINT_T = "Operacion.Operacion.OP_PuntoControl"
    K_OP_SURVEY_POINT_T = "Operacion.Operacion.OP_PuntoLevantamiento"
    K_OP_BOUNDARY_POINT_T = "Operacion.Operacion.OP_PuntoLindero"
    K_OP_RESTRICTION_T = "Operacion.Operacion.OP_Restriccion"
    K_OP_RIGHT_OF_WAY_T = "Operacion.Operacion.OP_ServidumbrePaso"
    K_OP_PLOT_T = "Operacion.Operacion.OP_Terreno"
    K_OP_BUILDING_TYPE = "Operacion.Operacion.OP_UnidadConstruccion"
    # "Operacion.OP_FotoidentificacionTipo"
    K_OP_ADMINISTRATIVE_SOURCE_TYPE_D = "Operacion.OP_FuenteAdministrativaTipo"
    # "Operacion.OP_GrupoEtnicoTipo"
    # "Operacion.OP_InstitucionTipo"
    K_OP_PARTY_DOCUMENT_TYPE_D = "Operacion.OP_InteresadoDocumentoTipo"
    K_OP_PARTY_TYPE_D = "Operacion.OP_InteresadoTipo"
    K_OP_PARCEL_TYPE_D = "Operacion.OP_PredioTipo"
    K_OP_CONTROL_POINT_TYPE_D = "Operacion.OP_PuntoControlTipo"
    K_OP_SURVEY_POINT_TYPE_D = "Operacion.OP_PuntoLevTipo"
    K_OP_POINT_TYPE_D = "Operacion.OP_PuntoTipo"
    K_OP_RESTRICTION_TYPE = "Operacion.OP_RestriccionTipo"
    K_OP_GENRE_D = "Operacion.OP_SexoTipo"
    # "Operacion.OP_UbicacionPuntoTipo"
    # "Operacion.OP_UsoUConsTipo"
    # "Operacion.OP_ViaTipo"

    ###################################################### FIELD KEYS ######################################################

    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Barrio.Codigo"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Barrio.Geometria"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Barrio.Nombre"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Barrio.Sector_Codigo"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Construccion.Area_Construida"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Construccion.Codigo_Edificacion"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Construccion.Codigo_Terreno"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Construccion.Etiqueta"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Construccion.Geometria"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Construccion.Identificador"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Construccion.Numero_Mezanines"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Construccion.Numero_Pisos"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Construccion.Numero_Semisotanos"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Construccion.Numero_Sotanos"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.gc_construccion_predio.gc_predio"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Construccion.Tipo_Construccion"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Construccion.Tipo_Dominio"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.gc_construccion_unidad.gc_construccion"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.gc_copropiedad.Coeficiente_Copropiedad"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.gc_copropiedad.gc_matriz"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.gc_copropiedad.gc_unidad"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Area_Total_Construida"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Area_Total_Construida_Comun"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Area_Total_Construida_Privada"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Area_Total_Terreno"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Area_Total_Terreno_Comun"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Area_Total_Terreno_Privada"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Torre_No"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Total_Pisos_Torre"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Total_Sotanos"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Total_Unidades_Privadas"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Datos_PH_Condiminio.Total_Unidades_Sotano"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Manzana.Barrio_Codigo"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Manzana.Codigo"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Manzana.Codigo_Anterior"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Manzana.Geometria"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Perimetro.Codigo_Nombre"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Perimetro.Departamento_Codigo"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Perimetro.Geometria"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Perimetro.Municipio_Codigo"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Perimetro.Nombre_Geografico"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Perimetro.Tipo_Avaluo"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.gc_ph_predio.gc_predio"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Circulo_Registral"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Condicion_Predio"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Destinacion_Economica"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Direcciones"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Fecha_Datos"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Matricula_Inmobiliaria_Catastro"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Numero_Predial"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Numero_Predial_Anterior"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Sistema_Procedencia_Datos"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Tipo_Catastro"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Predio_Catastro.Tipo_Predio"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario.Digito_Verificacion"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario.Numero_Documento"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.gc_propietario_predio.gc_predio_catastro"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario.Primer_Apellido"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario.Primer_Nombre"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario.Razon_Social"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario.Segundo_Apellido"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario.Segundo_Nombre"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario.Tipo_Documento"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Sector_Rural.Codigo"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Sector_Rural.Geometria"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Sector_Urbano.Codigo"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Sector_Urbano.Geometria"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Alfanumerica"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Digital"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno.Geometria"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno.Manzana_Vereda_Codigo"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno.Numero_Subterraneos"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.gc_terreno_predio.gc_predio"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Unidad_Construccion.Anio"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Unidad_Construccion.Area_Construida"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Unidad_Construccion.Area_Privada"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Unidad_Construccion.Codigo_Terreno"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Unidad_Construccion.Etiqueta"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Unidad_Construccion.Geometria"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Unidad_Construccion.Identificador"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Unidad_Construccion.Planta"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Unidad_Construccion.Puntaje"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Unidad_Construccion.Tipo_Construccion"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Unidad_Construccion.Tipo_Dominio"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Unidad_Construccion.Total_Banios"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Unidad_Construccion.Total_Habitaciones"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Unidad_Construccion.Total_Locales"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Unidad_Construccion.Total_Pisos"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Unidad_Construccion.Uso"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Vereda.Codigo"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Vereda.Codigo_Anterior"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Vereda.Geometria"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Vereda.Nombre"
    # "Datos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Vereda.Sector_Codigo"
    # "Datos_Gestor_Catastral.GC_Direccion.Geometria_Referencia"
    # "Datos_Gestor_Catastral.GC_Direccion.Principal"
    # "Datos_Gestor_Catastral.GC_Direccion.Valor"
    #
    #
    # "Datos_Integracion_Insumos.Datos_Integracion_Insumos.ini_predio_integracion_gc.gc_predio_catastro"
    # "Datos_Integracion_Insumos.Datos_Integracion_Insumos.ini_predio_integracion_snr.snr_predio_juridico"
    #
    # "Datos_SNR.Datos_SNR.SNR_Derecho.Calidad_Derecho_Registro"
    # "Datos_SNR.Datos_SNR.SNR_Derecho.Codigo_Naturaleza_Juridica"
    # "Datos_SNR.Datos_SNR.snr_derecho_predio.snr_predio_registro"
    # "Datos_SNR.Datos_SNR.SNR_Fuente_CabidaLinderos.Archivo"
    # "Datos_SNR.Datos_SNR.SNR_Fuente_CabidaLinderos.Ciudad_Emisora"
    # "Datos_SNR.Datos_SNR.SNR_Fuente_CabidaLinderos.Ente_Emisor"
    # "Datos_SNR.Datos_SNR.SNR_Fuente_CabidaLinderos.Fecha_Documento"
    # "Datos_SNR.Datos_SNR.SNR_Fuente_CabidaLinderos.Numero_Documento"
    # "Datos_SNR.Datos_SNR.snr_fuente_cabidalinderos.snr_fuente_cabidalinderos"
    # "Datos_SNR.Datos_SNR.SNR_Fuente_CabidaLinderos.Tipo_Documento"
    # "Datos_SNR.Datos_SNR.SNR_Fuente_Derecho.Ciudad_Emisora"
    # "Datos_SNR.Datos_SNR.SNR_Fuente_Derecho.Ente_Emisor"
    # "Datos_SNR.Datos_SNR.SNR_Fuente_Derecho.Fecha_Documento"
    # "Datos_SNR.Datos_SNR.SNR_Fuente_Derecho.Numero_Documento"
    # "Datos_SNR.Datos_SNR.snr_fuente_derecho.snr_fuente_derecho"
    # "Datos_SNR.Datos_SNR.SNR_Fuente_Derecho.Tipo_Documento"
    # "Datos_SNR.Datos_SNR.SNR_Predio_Registro.Cabida_Linderos"
    # "Datos_SNR.Datos_SNR.SNR_Predio_Registro.Codigo_ORIP"
    # "Datos_SNR.Datos_SNR.SNR_Predio_Registro.Fecha_Datos"
    # "Datos_SNR.Datos_SNR.SNR_Predio_Registro.Matricula_Inmobiliaria"
    # "Datos_SNR.Datos_SNR.SNR_Predio_Registro.Matricula_Inmobiliaria_Matriz"
    # "Datos_SNR.Datos_SNR.SNR_Predio_Registro.Numero_Predial_Anterior_en_FMI"
    # "Datos_SNR.Datos_SNR.SNR_Predio_Registro.Numero_Predial_Nuevo_en_FMI"
    # "Datos_SNR.Datos_SNR.SNR_Predio_Registro.NUPRE_en_FMI"
    # "Datos_SNR.Datos_SNR.snr_titular_derecho.Porcentaje_Participacion"
    # "Datos_SNR.Datos_SNR.snr_titular_derecho.snr_derecho"
    # "Datos_SNR.Datos_SNR.snr_titular_derecho.snr_titular"
    # "Datos_SNR.Datos_SNR.SNR_Titular.Nombres"
    # "Datos_SNR.Datos_SNR.SNR_Titular.Numero_Documento"
    # "Datos_SNR.Datos_SNR.SNR_Titular.Primer_Apellido"
    # "Datos_SNR.Datos_SNR.SNR_Titular.Razon_Social"
    # "Datos_SNR.Datos_SNR.SNR_Titular.Segundo_Apellido"
    # "Datos_SNR.Datos_SNR.SNR_Titular.Tipo_Documento"
    # "Datos_SNR.Datos_SNR.SNR_Titular.Tipo_Persona"
    #
    # "LADM_COL.LADM_Nucleo.baunitComoInteresado.interesado"
    # "LADM_COL.LADM_Nucleo.baunitComoInteresado.interesado"
    # "LADM_COL.LADM_Nucleo.baunitComoInteresado.unidad"
    # "LADM_COL.LADM_Nucleo.baunitFuente.bfuente"
    # "LADM_COL.LADM_Nucleo.baunitFuente.unidad"
    # "LADM_COL.LADM_Nucleo.baunitRrr.unidad"
    # "LADM_COL.LADM_Nucleo.baunitRrr.unidad"
    # "LADM_COL.LADM_Nucleo.cclFuente.ccl"
    # "LADM_COL.LADM_Nucleo.cclFuente.lfuente"
    # "LADM_COL.LADM_Nucleo.CC_MetodoOperacion.Ddimensiones_Objetivo"
    # "LADM_COL.LADM_Nucleo.CC_MetodoOperacion.Dimensiones_Origen"
    # "LADM_COL.LADM_Nucleo.CC_MetodoOperacion.Formula"
    # "LADM_COL.LADM_Nucleo.CI_Contacto.Direccion"
    # "LADM_COL.LADM_Nucleo.CI_Contacto.Fuente_En_Linea"
    # "LADM_COL.LADM_Nucleo.CI_Contacto.Horario_De_Atencion"
    # "LADM_COL.LADM_Nucleo.CI_Contacto.Instrucciones_Contacto"
    # "LADM_COL.LADM_Nucleo.CI_Contacto.Telefono"
    # "LADM_COL.LADM_Nucleo.CI_ParteResponsable.Funcion"
    # "LADM_COL.LADM_Nucleo.CI_ParteResponsable.Informacion_Contacto"
    # "LADM_COL.LADM_Nucleo.CI_ParteResponsable.Nombre_Individual"
    # "LADM_COL.LADM_Nucleo.CI_ParteResponsable.Nombre_Organizacion"
    # "LADM_COL.LADM_Nucleo.CI_ParteResponsable.Posicion"
    # "LADM_COL.LADM_Nucleo.clFuente.cfuente"
    # "LADM_COL.LADM_Nucleo.COL_Agrupacion_Interesados.Tipo"
    # "LADM_COL.LADM_Nucleo.COL_AreaValor.areaSize"
    # "LADM_COL.LADM_Nucleo.COL_AreaValor.type"
    # "LADM_COL.LADM_Nucleo.COL_BAUnit.Nombre"
    # "LADM_COL.LADM_Nucleo.COL_BAUnit.u_Espacio_De_Nombres"
    # "LADM_COL.LADM_Nucleo.COL_BAUnit.u_Local_Id"
    # "LADM_COL.LADM_Nucleo.COL_CadenaCarasLimite.ccl_Espacio_De_Nombres"
    # "LADM_COL.LADM_Nucleo.COL_CadenaCarasLimite.ccl_Local_Id"
    # "LADM_COL.LADM_Nucleo.COL_CadenaCarasLimite.Geometria"
    # "LADM_COL.LADM_Nucleo.COL_CadenaCarasLimite.Localizacion_Textual"
    # "LADM_COL.LADM_Nucleo.COL_FuenteAdministrativa.Numero_Fuente"
    # "LADM_COL.LADM_Nucleo.COL_FuenteAdministrativa.Observacion"
    # "LADM_COL.LADM_Nucleo.COL_Fuente.Calidad"
    # "LADM_COL.LADM_Nucleo.COL_Fuente.Calidad"
    # "LADM_COL.LADM_Nucleo.COL_Fuente.Calidad"
    # "LADM_COL.LADM_Nucleo.COL_Fuente.Calidad"
    # "LADM_COL.LADM_Nucleo.COL_FuenteEspacial.Mediciones"
    # "LADM_COL.LADM_Nucleo.COL_FuenteEspacial.Procedimiento"
    # "LADM_COL.LADM_Nucleo.COL_FuenteEspacial.Tipo"
    # "LADM_COL.LADM_Nucleo.COL_Fuente.Estado_Disponibilidad"
    # "LADM_COL.LADM_Nucleo.COL_Fuente.Estado_Disponibilidad"
    # "LADM_COL.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID"
    # "LADM_COL.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID"
    # "LADM_COL.LADM_Nucleo.COL_Fuente.Fecha_Documento_Fuente"
    # "LADM_COL.LADM_Nucleo.COL_Fuente.Fecha_Documento_Fuente"
    # "LADM_COL.LADM_Nucleo.COL_Fuente.Oficialidad"
    # "LADM_COL.LADM_Nucleo.COL_Fuente.Oficialidad"
    # "LADM_COL.LADM_Nucleo.COL_Fuente.Procedencia"
    # "LADM_COL.LADM_Nucleo.COL_Fuente.Procedencia"
    # "LADM_COL.LADM_Nucleo.COL_Fuente.s_Espacio_De_Nombres"
    # "LADM_COL.LADM_Nucleo.COL_Fuente.s_Espacio_De_Nombres"
    # "LADM_COL.LADM_Nucleo.COL_Fuente.s_Local_Id"
    # "LADM_COL.LADM_Nucleo.COL_Fuente.s_Local_Id"
    # "LADM_COL.LADM_Nucleo.COL_Fuente.Tipo_Principal"
    # "LADM_COL.LADM_Nucleo.COL_Fuente.Tipo_Principal"
    # "LADM_COL.LADM_Nucleo.COL_FuncionInteresadoTipo_.value"
    # "LADM_COL.LADM_Nucleo.COL_Interesado.ext_PID"
    # "LADM_COL.LADM_Nucleo.COL_Interesado.ext_PID"
    # "LADM_COL.LADM_Nucleo.COL_Interesado.Nombre"
    # "LADM_COL.LADM_Nucleo.COL_Interesado.Nombre"
    # "LADM_COL.LADM_Nucleo.COL_Interesado.p_Espacio_De_Nombres"
    # "LADM_COL.LADM_Nucleo.COL_Interesado.p_Espacio_De_Nombres"
    # "LADM_COL.LADM_Nucleo.COL_Interesado.p_Local_Id"
    # "LADM_COL.LADM_Nucleo.COL_Interesado.p_Local_Id"
    # "LADM_COL.LADM_Nucleo.COL_Interesado.Tarea"
    # "LADM_COL.LADM_Nucleo.COL_Interesado.Tarea"
    # "LADM_COL.LADM_Nucleo.COL_Punto.Exactitud_Estimada"
    # "LADM_COL.LADM_Nucleo.COL_Punto.Exactitud_Estimada"
    # "LADM_COL.LADM_Nucleo.COL_Punto.Exactitud_Estimada"
    # "LADM_COL.LADM_Nucleo.COL_Punto.Exactitud_Estimada"
    # "LADM_COL.LADM_Nucleo.COL_Punto.Exactitud_Estimada"
    # "LADM_COL.LADM_Nucleo.COL_Punto.Exactitud_Estimada"
    # "LADM_COL.LADM_Nucleo.COL_Punto.Localizacion_Original"
    # "LADM_COL.LADM_Nucleo.COL_Punto.Localizacion_Original"
    # "LADM_COL.LADM_Nucleo.COL_Punto.Localizacion_Original"
    # "LADM_COL.LADM_Nucleo.COL_Punto.MetodoProduccion"
    # "LADM_COL.LADM_Nucleo.COL_Punto.MetodoProduccion"
    # "LADM_COL.LADM_Nucleo.COL_Punto.MetodoProduccion"
    # "LADM_COL.LADM_Nucleo.COL_Punto.Monumentacion"
    # "LADM_COL.LADM_Nucleo.COL_Punto.Monumentacion"
    # "LADM_COL.LADM_Nucleo.COL_Punto.Monumentacion"
    # "LADM_COL.LADM_Nucleo.COL_Punto.p_Espacio_De_Nombres"
    # "LADM_COL.LADM_Nucleo.COL_Punto.p_Espacio_De_Nombres"
    # "LADM_COL.LADM_Nucleo.COL_Punto.p_Espacio_De_Nombres"
    # "LADM_COL.LADM_Nucleo.COL_Punto.p_Local_Id"
    # "LADM_COL.LADM_Nucleo.COL_Punto.p_Local_Id"
    # "LADM_COL.LADM_Nucleo.COL_Punto.p_Local_Id"
    # "LADM_COL.LADM_Nucleo.COL_Punto.Posicion_Interpolacion"
    # "LADM_COL.LADM_Nucleo.COL_Punto.Posicion_Interpolacion"
    # "LADM_COL.LADM_Nucleo.COL_Punto.Posicion_Interpolacion"
    # "LADM_COL.LADM_Nucleo.COL_Punto.Transformacion_Y_Resultado"
    # "LADM_COL.LADM_Nucleo.COL_Punto.Transformacion_Y_Resultado"
    # "LADM_COL.LADM_Nucleo.COL_Punto.Transformacion_Y_Resultado"
    # "LADM_COL.LADM_Nucleo.COL_RRR.Compartido"
    # "LADM_COL.LADM_Nucleo.COL_RRR.Compartido"
    # "LADM_COL.LADM_Nucleo.COL_RRR.Comprobacion_Comparte"
    # "LADM_COL.LADM_Nucleo.COL_RRR.Comprobacion_Comparte"
    # "LADM_COL.LADM_Nucleo.COL_RRR.Descripcion"
    # "LADM_COL.LADM_Nucleo.COL_RRR.Descripcion"
    # "LADM_COL.LADM_Nucleo.COL_RRR.r_Espacio_De_Nombres"
    # "LADM_COL.LADM_Nucleo.COL_RRR.r_Espacio_De_Nombres"
    # "LADM_COL.LADM_Nucleo.COL_RRR.r_Local_Id"
    # "LADM_COL.LADM_Nucleo.COL_RRR.r_Local_Id"
    # "LADM_COL.LADM_Nucleo.COL_RRR.Uso_Efectivo"
    # "LADM_COL.LADM_Nucleo.COL_RRR.Uso_Efectivo"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Area"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Area"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Area"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Area"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Dimension"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Dimension"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Dimension"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Dimension"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Etiqueta"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Etiqueta"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Etiqueta"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Etiqueta"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.poligono_creado"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.poligono_creado"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.poligono_creado"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.poligono_creado"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.su_Espacio_De_Nombres"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.su_Espacio_De_Nombres"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.su_Espacio_De_Nombres"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.su_Espacio_De_Nombres"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.su_Local_Id"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.su_Local_Id"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.su_Local_Id"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.su_Local_Id"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Volumen"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Volumen"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Volumen"
    # "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Volumen"
    # "LADM_COL.LADM_Nucleo.DQ_AbsoluteExternalPositionalAccuracy.atributo1"
    # "LADM_COL.LADM_Nucleo.DQ_Element.Descripcion_Medida"
    # "LADM_COL.LADM_Nucleo.DQ_Element.Descripcion_Medida"
    # "LADM_COL.LADM_Nucleo.DQ_Element.Descripcion_Medida"
    # "LADM_COL.LADM_Nucleo.DQ_Element.Descripcion_Metodo_Evaluacion"
    # "LADM_COL.LADM_Nucleo.DQ_Element.Descripcion_Metodo_Evaluacion"
    # "LADM_COL.LADM_Nucleo.DQ_Element.Descripcion_Metodo_Evaluacion"
    # "LADM_COL.LADM_Nucleo.DQ_Element.Fecha_Hora"
    # "LADM_COL.LADM_Nucleo.DQ_Element.Fecha_Hora"
    # "LADM_COL.LADM_Nucleo.DQ_Element.Fecha_Hora"
    # "LADM_COL.LADM_Nucleo.DQ_Element.Identificacion_Medida"
    # "LADM_COL.LADM_Nucleo.DQ_Element.Identificacion_Medida"
    # "LADM_COL.LADM_Nucleo.DQ_Element.Identificacion_Medida"
    # "LADM_COL.LADM_Nucleo.DQ_Element.Metodo_Evaluacion"
    # "LADM_COL.LADM_Nucleo.DQ_Element.Metodo_Evaluacion"
    # "LADM_COL.LADM_Nucleo.DQ_Element.Metodo_Evaluacion"
    # "LADM_COL.LADM_Nucleo.DQ_Element.Nombre_Medida"
    # "LADM_COL.LADM_Nucleo.DQ_Element.Nombre_Medida"
    # "LADM_COL.LADM_Nucleo.DQ_Element.Nombre_Medida"
    # "LADM_COL.LADM_Nucleo.DQ_Element.Procedimiento_Evaluacion"
    # "LADM_COL.LADM_Nucleo.DQ_Element.Procedimiento_Evaluacion"
    # "LADM_COL.LADM_Nucleo.DQ_Element.Procedimiento_Evaluacion"
    # "LADM_COL.LADM_Nucleo.DQ_Element.Resultado"
    # "LADM_COL.LADM_Nucleo.DQ_Element.Resultado"
    # "LADM_COL.LADM_Nucleo.DQ_Element.Resultado"
    # "LADM_COL.LADM_Nucleo.DQ_PositionalAccuracy.atributo21"
    # "LADM_COL.LADM_Nucleo.DQ_PositionalAccuracy.atributo21"
    # "LADM_COL.LADM_Nucleo.ExtArchivo.Datos"
    # "LADM_COL.LADM_Nucleo.ExtArchivo.Extraccion"
    # "LADM_COL.LADM_Nucleo.ExtArchivo.Fecha_Aceptacion"
    # "LADM_COL.LADM_Nucleo.ExtArchivo.Fecha_Entrega"
    # "LADM_COL.LADM_Nucleo.ExtArchivo.Fecha_Grabacion"
    # "LADM_COL.LADM_Nucleo.ExtArchivo.s_Espacio_De_Nombres"
    # "LADM_COL.LADM_Nucleo.ExtArchivo.s_Local_Id"
    # "LADM_COL.LADM_Nucleo.ExtDireccion.Apartado_Correo"
    # "LADM_COL.LADM_Nucleo.ExtDireccion.Ciudad"
    # "LADM_COL.LADM_Nucleo.ExtDireccion.Codigo_Postal"
    # "LADM_COL.LADM_Nucleo.ExtDireccion.Coordenada_Direccion"
    # "LADM_COL.LADM_Nucleo.ExtDireccion.Departamento"
    # "LADM_COL.LADM_Nucleo.ExtDireccion.Direccion_ID"
    # "LADM_COL.LADM_Nucleo.ExtDireccion.Nombre_Area_Direccion"
    # "LADM_COL.LADM_Nucleo.ExtDireccion.Nombre_Calle"
    # "LADM_COL.LADM_Nucleo.ExtDireccion.Nombre_Edificio"
    # "LADM_COL.LADM_Nucleo.ExtDireccion.Numero_Edificio"
    # "LADM_COL.LADM_Nucleo.ExtDireccion.Pais"
    # "LADM_COL.LADM_Nucleo.ExtInteresado.Ext_Direccion_ID"
    # "LADM_COL.LADM_Nucleo.ExtInteresado.Firma"
    # "LADM_COL.LADM_Nucleo.ExtInteresado.Fotografia"
    # "LADM_COL.LADM_Nucleo.ExtInteresado.Huella_Dactilar"
    # "LADM_COL.LADM_Nucleo.ExtInteresado.Interesado_ID"
    # "LADM_COL.LADM_Nucleo.ExtInteresado.Nombre"
    # "LADM_COL.LADM_Nucleo.ExtRedServiciosFisica.Ext_Interesado_Administrador_ID"
    # "LADM_COL.LADM_Nucleo.ExtRedServiciosFisica.Orientada"
    # "LADM_COL.LADM_Nucleo.ExtUnidadEdificacionFisica.Ext_Direccion_ID"
    # "LADM_COL.LADM_Nucleo.Fraccion.Denominador"
    # "LADM_COL.LADM_Nucleo.Fraccion.Numerador"
    # "LADM_COL.LADM_Nucleo.Imagen.uri"
    # "LADM_COL.LADM_Nucleo.LA_TareaInteresadoTipo.Tipo"
    # "LADM_COL.LADM_Nucleo.LA_Transformacion.Localizacion_Transformada"
    # "LADM_COL.LADM_Nucleo.LA_Transformacion.Transformacion"
    # "LADM_COL.LADM_Nucleo.LA_VolumenValor.Tipo"
    # "LADM_COL.LADM_Nucleo.LA_VolumenValor.Volumen_Medicion"
    # "LADM_COL.LADM_Nucleo.LI_Lineaje.Statement"
    # "LADM_COL.LADM_Nucleo.masCcl.ccl_mas"
    # "LADM_COL.LADM_Nucleo.masCcl.ue_mas"
    # "LADM_COL.LADM_Nucleo.masCcl.ue_mas"
    # "LADM_COL.LADM_Nucleo.masCcl.ue_mas"
    # "LADM_COL.LADM_Nucleo.masCcl.ue_mas"
    # "LADM_COL.LADM_Nucleo.masCl.ue_mas"
    # "LADM_COL.LADM_Nucleo.masCl.ue_mas"
    # "LADM_COL.LADM_Nucleo.masCl.ue_mas"
    # "LADM_COL.LADM_Nucleo.masCl.ue_mas"
    # "LADM_COL.LADM_Nucleo.menosCcl.ccl_menos"
    # "LADM_COL.LADM_Nucleo.menosCcl.ue_menos"
    # "LADM_COL.LADM_Nucleo.menosCcl.ue_menos"
    # "LADM_COL.LADM_Nucleo.menosCcl.ue_menos"
    # "LADM_COL.LADM_Nucleo.menosCcl.ue_menos"
    # "LADM_COL.LADM_Nucleo.menosCl.ue_menos"
    # "LADM_COL.LADM_Nucleo.menosCl.ue_menos"
    # "LADM_COL.LADM_Nucleo.menosCl.ue_menos"
    # "LADM_COL.LADM_Nucleo.menosCl.ue_menos"
    # "LADM_COL.LADM_Nucleo.miembros.agrupacion"
    # "LADM_COL.LADM_Nucleo.miembros.interesados"
    # "LADM_COL.LADM_Nucleo.miembros.interesados"
    # "LADM_COL.LADM_Nucleo.miembros.participacion"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Calidad"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL.LADM_Nucleo.ObjetoVersionado.Procedencia"
    # "LADM_COL.LADM_Nucleo.Oid.espacioDeNombres"
    # "LADM_COL.LADM_Nucleo.Oid.localId"
    # "LADM_COL.LADM_Nucleo.OM_Observacion.Resultado_Calidad"
    # "LADM_COL.LADM_Nucleo.OM_Observacion.Resultado_Calidad"
    # "LADM_COL.LADM_Nucleo.puntoCcl.ccl"
    # "LADM_COL.LADM_Nucleo.puntoCcl.punto"
    # "LADM_COL.LADM_Nucleo.puntoCcl.punto"
    # "LADM_COL.LADM_Nucleo.puntoCcl.punto"
    # "LADM_COL.LADM_Nucleo.puntoCl.punto"
    # "LADM_COL.LADM_Nucleo.puntoCl.punto"
    # "LADM_COL.LADM_Nucleo.puntoCl.punto"
    # "LADM_COL.LADM_Nucleo.puntoFuente.pfuente"
    # "LADM_COL.LADM_Nucleo.puntoFuente.punto"
    # "LADM_COL.LADM_Nucleo.puntoFuente.punto"
    # "LADM_COL.LADM_Nucleo.puntoFuente.punto"
    # "LADM_COL.LADM_Nucleo.puntoReferencia.ue"
    # "LADM_COL.LADM_Nucleo.puntoReferencia.ue"
    # "LADM_COL.LADM_Nucleo.puntoReferencia.ue"
    # "LADM_COL.LADM_Nucleo.puntoReferencia.ue"
    # "LADM_COL.LADM_Nucleo.puntoReferencia.ue"
    # "LADM_COL.LADM_Nucleo.puntoReferencia.ue"
    # "LADM_COL.LADM_Nucleo.puntoReferencia.ue"
    # "LADM_COL.LADM_Nucleo.puntoReferencia.ue"
    # "LADM_COL.LADM_Nucleo.puntoReferencia.ue"
    # "LADM_COL.LADM_Nucleo.puntoReferencia.ue"
    # "LADM_COL.LADM_Nucleo.puntoReferencia.ue"
    # "LADM_COL.LADM_Nucleo.puntoReferencia.ue"
    # "LADM_COL.LADM_Nucleo.relacionFuente.refuente"
    # "LADM_COL.LADM_Nucleo.relacionFuenteUespacial.rfuente"
    # "LADM_COL.LADM_Nucleo.responsableFuente.cfuente"
    # "LADM_COL.LADM_Nucleo.responsableFuente.notario"
    # "LADM_COL.LADM_Nucleo.responsableFuente.notario"
    # "LADM_COL.LADM_Nucleo.rrrFuente.rfuente"
    # "LADM_COL.LADM_Nucleo.rrrFuente.rrr"
    # "LADM_COL.LADM_Nucleo.rrrFuente.rrr"
    # "LADM_COL.LADM_Nucleo.rrrInteresado.interesado"
    # "LADM_COL.LADM_Nucleo.rrrInteresado.interesado"
    # "LADM_COL.LADM_Nucleo.rrrInteresado.interesado"
    # "LADM_COL.LADM_Nucleo.rrrInteresado.interesado"
    # "LADM_COL.LADM_Nucleo.topografoFuente.sfuente"
    # "LADM_COL.LADM_Nucleo.topografoFuente.topografo"
    # "LADM_COL.LADM_Nucleo.topografoFuente.topografo"
    # "LADM_COL.LADM_Nucleo.ueBaunit.baunit"
    # "LADM_COL.LADM_Nucleo.ueBaunit.ue"
    # "LADM_COL.LADM_Nucleo.ueBaunit.ue"
    # "LADM_COL.LADM_Nucleo.ueBaunit.ue"
    # "LADM_COL.LADM_Nucleo.ueBaunit.ue"
    # "LADM_COL.LADM_Nucleo.ueFuente.pfuente"
    # "LADM_COL.LADM_Nucleo.ueFuente.ue"
    # "LADM_COL.LADM_Nucleo.ueFuente.ue"
    # "LADM_COL.LADM_Nucleo.ueFuente.ue"
    # "LADM_COL.LADM_Nucleo.ueFuente.ue"
    # "LADM_COL.LADM_Nucleo.ueUeGrupo.parte"
    # "LADM_COL.LADM_Nucleo.ueUeGrupo.parte"
    # "LADM_COL.LADM_Nucleo.ueUeGrupo.parte"
    # "LADM_COL.LADM_Nucleo.ueUeGrupo.parte"
    # "LADM_COL.LADM_Nucleo.unidadFuente.ufuente"
    # "LADM_COL.LADM_Nucleo.unidadFuente.unidad"
    #
    #
    # "Operacion.Operacion.OP_Construccion.Area_Construccion"
    # "Operacion.Operacion.OP_Construccion.Avaluo_Construccion"
    # "Operacion.Operacion.OP_Construccion.Numero_Pisos"
    # "Operacion.Operacion.op_construccion_unidadconstruccion.op_construccion"
    # "Operacion.Operacion.OP_Derecho.Tipo"
    # "Operacion.Operacion.OP_FuenteAdministrativa.Ente_Emisor"
    # "Operacion.Operacion.OP_FuenteAdministrativa.Tipo"
    # "Operacion.Operacion.OP_Interesado_Contacto.Autoriza_Notificacion_Correo"
    # "Operacion.Operacion.OP_Interesado_Contacto.Correo_Electronico"
    # "Operacion.Operacion.OP_Interesado_Contacto.Domicilio_Notificacion"
    # "Operacion.Operacion.op_interesado_contacto.op_interesado"
    # "Operacion.Operacion.OP_Interesado_Contacto.Origen_Datos"
    # "Operacion.Operacion.OP_Interesado_Contacto.Telefono1"
    # "Operacion.Operacion.OP_Interesado_Contacto.Telefono2"
    # "Operacion.Operacion.OP_Interesado.Documento_Identidad"
    # "Operacion.Operacion.OP_Interesado.Grupo_Etnico"
    # "Operacion.Operacion.OP_Interesado.Primer_Apellido"
    # "Operacion.Operacion.OP_Interesado.Primer_Nombre"
    # "Operacion.Operacion.OP_Interesado.Razon_Social"
    # "Operacion.Operacion.OP_Interesado.Segundo_Apellido"
    # "Operacion.Operacion.OP_Interesado.Segundo_Nombre"
    # "Operacion.Operacion.OP_Interesado.Sexo"
    # "Operacion.Operacion.OP_Interesado.Tipo"
    # "Operacion.Operacion.OP_Interesado.Tipo_Documento"
    # "Operacion.Operacion.OP_Lindero.Longitud"
    K_OP_PARCEL_T_VALUATION_F = "Operacion.Operacion.OP_Predio.Avaluo_Predio"
    K_OP_PARCEL_T_ORIP_CODE_F = "Operacion.Operacion.OP_Predio.Codigo_ORIP"
    K_OP_PARCEL_T_PARCEL_TYPE_F = "Operacion.Operacion.OP_Predio.Condicion_Predio"
    # "Operacion.Operacion.op_predio_copropiedad.coeficiente"
    # "Operacion.Operacion.op_predio_copropiedad.copropiedad"
    # "Operacion.Operacion.op_predio_copropiedad.predio"
    K_OP_PARCEL_T_DEPARTMENT_F = "Operacion.Operacion.OP_Predio.Departamento"
    K_OP_PARCEL_T_ADDRESS_F = "Operacion.Operacion.OP_Predio.Direccion"
    # "Operacion.Operacion.op_predio_insumos_operacion.ini_predio_insumos"
    # "Operacion.Operacion.op_predio_insumos_operacion.op_predio"
    K_OP_PARCEL_T_FMI_F = "Operacion.Operacion.OP_Predio.Matricula_Inmobiliaria"
    K_OP_PARCEL_T_MUNICIPALITY_F = "Operacion.Operacion.OP_Predio.Municipio"
    K_OP_PARCEL_T_PARCEL_NUMBER_F = "Operacion.Operacion.OP_Predio.Numero_Predial"
    K_OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F = "Operacion.Operacion.OP_Predio.Numero_Predial_Anterior"
    K_OP_PARCEL_T_NUPRE_F = "Operacion.Operacion.OP_Predio.NUPRE"
    K_OP_PARCEL_T_TYPE_F = "Operacion.Operacion.OP_Predio.Tipo"
    # "Operacion.Operacion.OP_PuntoControl.Exactitud_Horizontal"
    # "Operacion.Operacion.OP_PuntoControl.Exactitud_Vertical"
    # "Operacion.Operacion.OP_PuntoControl.ID_Punto_Control"
    # "Operacion.Operacion.OP_PuntoControl.PuntoTipo"
    # "Operacion.Operacion.OP_PuntoControl.Tipo_Punto_Control"
    # "Operacion.Operacion.OP_PuntoLevantamiento.Exactitud_Horizontal"
    # "Operacion.Operacion.OP_PuntoLevantamiento.Exactitud_Vertical"
    # "Operacion.Operacion.OP_PuntoLevantamiento.Fotoidentificacion"
    # "Operacion.Operacion.OP_PuntoLevantamiento.ID_Punto_Levantamiento"
    # "Operacion.Operacion.OP_PuntoLevantamiento.PuntoTipo"
    # "Operacion.Operacion.OP_PuntoLevantamiento.Tipo_Punto_Levantamiento"
    # "Operacion.Operacion.OP_PuntoLindero.Acuerdo"
    # "Operacion.Operacion.OP_PuntoLindero.Exactitud_Horizontal"
    # "Operacion.Operacion.OP_PuntoLindero.Exactitud_Vertical"
    # "Operacion.Operacion.OP_PuntoLindero.Fotoidentificacion"
    # "Operacion.Operacion.OP_PuntoLindero.ID_Punto_Lindero"
    # "Operacion.Operacion.OP_PuntoLindero.PuntoTipo"
    # "Operacion.Operacion.OP_PuntoLindero.Ubicacion_Punto"
    # "Operacion.Operacion.OP_Restriccion.Tipo"
    # "Operacion.Operacion.OP_ServidumbrePaso.Area_Servidumbre"
    # "Operacion.Operacion.OP_Terreno.Area_Terreno"
    # "Operacion.Operacion.OP_Terreno.Avaluo_Terreno"
    # "Operacion.Operacion.OP_Terreno.poligono_creado"
    # "Operacion.Operacion.OP_UnidadConstruccion.Area_Construida"
    # "Operacion.Operacion.OP_UnidadConstruccion.Area_Privada_Construida"
    # "Operacion.Operacion.OP_UnidadConstruccion.Avaluo_Unidad_Construccion"
    # "Operacion.Operacion.OP_UnidadConstruccion.Identificador"
    # "Operacion.Operacion.OP_UnidadConstruccion.Numero_Pisos"
    # "Operacion.Operacion.OP_UnidadConstruccion.Piso_Ubicacion"
    # "Operacion.Operacion.OP_UnidadConstruccion.Uso"

    TABLE_DICT = {
        K_OP_PARCEL_T: {VARIABLE_NAME: "OP_PARCEL_T", FIELDS_DICT: {
            K_OP_PARCEL_T_DEPARTMENT_F: "OP_PARCEL_T_DEPARTMENT_F"
            }}
    }

    def initialize_table_and_field_names(self, dict_names):
        if dict_names:
            print(self.OP_PARCEL_T, self.OP_PARCEL_T_DEPARTMENT_F)

            for table_key, attrs in self.TABLE_DICT.items():
                if table_key in dict_names:
                    setattr(self, attrs[VARIABLE_NAME], dict_names[table_key][TABLE_NAME])
                    for field_key, field_variable in attrs[FIELDS_DICT].items():
                        if field_key in dict_names[table_key]:
                            setattr(self, field_variable, dict_names[table_key][field_key])
            print(self.OP_PARCEL_T, self.OP_PARCEL_T_DEPARTMENT_F)

            # self.OP_PARCEL_T = dict_names[self.K_OP_PARCEL_T][TABLE_NAME]
            # self.OP_PARCEL_T_DEPARTMENT_F = dict_names[self.K_OP_PARCEL_T][self.K_OP_PARCEL_T_DEPARTMENT_F]
            # self.OP_PARCEL_T_ADDRESS_F = dict_names[self.K_OP_PARCEL_T][self.K_OP_PARCEL_T_ADDRESS_F]
            # self.OP_PARCEL_T_FMI_F = dict_names[self.K_OP_PARCEL_T][self.K_OP_PARCEL_T_FMI_F]
            # self.OP_PARCEL_T_MUNICIPALITY_F = dict_names[self.K_OP_PARCEL_T][self.K_OP_PARCEL_T_MUNICIPALITY_F]
            # self.OP_PARCEL_T_PARCEL_NUMBER_F = dict_names[self.K_OP_PARCEL_T][self.K_OP_PARCEL_T_PARCEL_NUMBER_F]
            # self.OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F = dict_names[self.K_OP_PARCEL_T][self.K_OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F]
            # self.OP_PARCEL_T_NUPRE_F = dict_names[self.K_OP_PARCEL_T][self.K_OP_PARCEL_T_NUPRE_F]
            # self.OP_PARCEL_T_TYPE_F = dict_names[self.K_OP_PARCEL_T][self.K_OP_PARCEL_T_TYPE_F]

    def get_layer_sets(self):
        """
        Configure layer sets to appear in the load layers dialog
        Each layer set is a key-value pair where key is the name of the layer set
        and the value is a list of layers to load
        """
        return {
            'Datos de Interesados': [
                self.OP_GENRE_D,
                self.OP_PARTY_T,
                self.OP_PARTY_DOCUMENT_TYPE_D,
                self.OP_PARTY_TYPE_D
            ],
            'Derechos': [
                self.OP_PARTY_T,
                self.OP_PARCEL_T,
                self.OP_ADMINISTRATIVE_SOURCE_T,
                self.EXT_FILE_S,
                self.COL_GROUP_PARTY_T,
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


"""
CADASTRE MAPPING
"""
ADMINISTRATIVE_SOURCE_TABLE = "col_fuenteadministrativa"
ADMINISTRATIVE_SOURCE_TYPE_TABLE = "col_fuenteadministrativatipo"
AVAILABILITY_STATE_TABLE = "col_estadodisponibilidadtipo"
POINT_BFS_TABLE_BOUNDARY_FIELD = "ccl_lindero"
BFS_TABLE_BOUNDARY_POINT_FIELD = "punto_puntolindero"
BOUNDARY_POINT_TABLE = "op_puntolindero"
BOUNDARY_TABLE = "op_lindero"
BUILDING_TABLE = "op_construccion"
BUILDING_AREA_FIELD = "area_construccion"
BUILDING_VALUATION_FIELD = "avaluo_construccion"
BUILDING_UNIT_AREA_FIELD = "area_construida"
BUILDING_UNIT_PRIVATE_AREA_FIELD = "area_privada_construida"
BUILDING_UNIT_VALUATION_FIELD = "avaluo_unidad_construccion"
BUILDING_UNIT_TABLE = "op_unidadconstruccion"
USE_BUILDING_UNIT_TABLE_TYPE = "op_usouconstipo"
BUSINESS_NAME_FIELD = "razon_social"
CCLSOURCE_TABLE = "cclfuente"
CCLSOURCE_TABLE_BOUNDARY_FIELD = "ccl_lindero"
CCLSOURCE_TABLE_SOURCE_FIELD = "lfuente"
COL_PARTY_DOCUMENT_ID_FIELD = "documento_identidad"
COL_PARTY_TABLE = "op_interesado"
COL_PARTY_TYPE_FIELD = "tipo"
COL_PARTY_DOC_TYPE_FIELD = "tipo_documento"
COL_PARTY_FIRST_NAME_FIELD = "primer_nombre"
COL_PARTY_SURNAME_FIELD = "primer_apellido"
COL_PARTY_BUSINESS_NAME_FIELD = "razon_social"
COL_PARTY_LEGAL_PARTY_FIELD = "tipo_interesado_juridico"
COL_PARTY_NAME_FIELD = "nombre"
COL_RESTRICTION_TYPE_RIGHT_OF_WAY_VALUE = "Servidumbre"
CONTROL_POINT_TABLE = "puntocontrol"
DEPARTMENT_FIELD = "departamento"
DOCUMENT_ID_FIELD = "documento_identidad"
DOMAIN_KEY_FIELD = {
    "pg": "ilicode",
    "gpkg": "iliCode"
}
EXTADDRESS_TABLE = "extdireccion"
EXTADDRESS_PLOT_FIELD = "terreno_ext_direccion_id"
EXTADDRESS_BUILDING_FIELD = "construccion_ext_direccion_id"
EXTADDRESS_BUILDING_UNIT_FIELD = "unidadconstruccion_ext_direccion_id"
EXTFILE_TABLE = "extarchivo"
EXTFILE_DATA_FIELD = "datos"
FIRST_NAME_FIELD = "primer_nombre"
FIRST_SURNAME_FIELD = "primer_apellido"
FMI_FIELD = "fmi"
FRACTION_TABLE = "fraccion"
FRACTION_DENOMINATOR_FIELD = "denominador"
FRACTION_MEMBER_FIELD = "miembros_participacion"
FRACTION_NUMERATOR_FIELD = "numerador"
GENDER_TYPE_TABLE = "col_generotipo"
ID_FIELD = "t_id"
LA_GROUP_PARTY_TABLE = "op_agrupacion_interesados"
LA_GROUP_PARTY_NAME_FIELD = "nombre"
LA_GROUP_PARTY_GPTYPE_FIELD = "ai_tipo"
LA_GROUP_PARTY_TYPE_FIELD = "tipo"
LA_GROUP_PARTY_TYPE_TABLE = "col_grupointeresadotipo"
LA_GROUP_PARTY_TYPE_VALUE = "Otro"
LA_BAUNIT_NAME_FIELD = "nombre"
LA_BAUNIT_TABLE = "la_baunit"
LA_BAUNIT_TYPE_TABLE = "la_baunittipo"
LA_DIMENSION_TYPE_TABLE = "la_dimensiontipo"
LA_BUILDING_UNIT_TYPE_TABLE = "la_unidadedificaciontipo"
LA_INTERPOLATION_TYPE_TABLE = "la_interpolaciontipo"
LA_MONUMENTATION_TYPE_TABLE = "la_monumentaciontipo"
LA_POINT_TABLE = "la_punto"
LA_POINT_TYPE_TABLE = "la_puntotipo"
LA_SURFACE_RELATION_TYPE_TABLE = "la_relacionsuperficietipo"
LENGTH_FIELD_BOUNDARY_TABLE = "longitud"
LESS_TABLE = "menos"
LESS_TABLE_BOUNDARY_FIELD = "ccl_lindero"
LESS_TABLE_PLOT_FIELD = "eu_terreno"
LOCAL_ID_FIELD = "_local_id"
MEMBERS_GROUP_PARTY_FIELD = "agrupacion"
MEMBERS_PARTY_FIELD = "interesados_col_interesado"
MEMBERS_TABLE = "col_miembros"
MORE_BOUNDARY_FACE_STRING_TABLE = "masccl"
MOREBFS_TABLE_BOUNDARY_FIELD = "cclp_lindero"
MOREBFS_TABLE_PLOT_FIELD = "uep_terreno"
MORTGAGE_TABLE = "col_hipoteca"
MUNICIPALITY_FIELD = "municipio"
NAMESPACE_FIELD = "_espacio_de_nombres"
NIT_NUMBER_FIELD = "numero_nit"
NUMBER_OF_FLOORS = "numero_pisos"
NUPRE_FIELD = "nupre"
OID_EXTADDRESS_ID_FIELD = "extdireccion_direccion_id"
OID_TABLE = "oid"
PARCEL_NAME_FIELD = "nombre"
PARCEL_NUMBER_FIELD = "numero_predial"
PARCEL_NUMBER_BEFORE_FIELD = "numero_predial_anterior"
PARCEL_TABLE = "op_predio"
PARCEL_TYPE_FIELD = "tipo"
PARCEL_TYPE_PH_OPTION = "PropiedadHorizontal.UnidadPredial"
PARCEL_VALUATION_FIELD = "avaluo_predio"
PARTY_DOCUMENT_TYPE_TABLE = "col_interesadodocumentotipo"
PARTY_TYPE_TABLE = "la_interesadotipo"
PLOT_TABLE = "op_terreno"
PLOT_AREA_FIELD = "area_terreno"
PLOT_CALCULATED_AREA_FIELD = "area_calculada"
PLOT_REGISTRY_AREA_FIELD = "area_registral"
PLOT_VALUATION_FIELD = "avaluo_terreno"
POINT_AGREEMENT_TYPE_TABLE = "op_acuerdotipo"
PHOTO_IDENTIFICATION_TYPE_TABLE = "op_fotoidentificaciontipo"
PRODUCTION_METHOD_TYPE_TABLE = "col_metodoproducciontipo"
POINT_LOCATION_POINT_TYPE_TABLE = "op_ubicacionpuntotipo"
POINT_TYPE_TABLE = "op_puntotipo"
SURFACE_RELATION_TYPE_TABLE = "col_relacionsuperficietipo"
DIMENSION_TYPE_TABLE = "col_dimensiontipo"
POINT_BOUNDARY_FACE_STRING_TABLE = "puntoccl"
POINT_DESCRIPTION_TYPE_TABLE = "col_descripcionpuntotipo"
POINT_DEFINITION_TYPE_TABLE = "col_defpuntotipo"
POINT_INTERPOLATION_TYPE_TABLE = "col_interpolaciontipo"
POINT_MONUMENTATION_TYPE_TABLE = "col_monumentaciontipo"
POINTSOURCE_TABLE = "puntofuente"
POINTSOURCE_TABLE_BOUNDARYPOINT_FIELD = "punto_puntolindero"
POINTSOURCE_TABLE_SURVEYPOINT_FIELD = "punto_puntolevantamiento"
POINTSOURCE_TABLE_CONTROLPOINT_FIELD = "punto_puntocontrol"
POINTSOURCE_TABLE_SOURCE_FIELD = "pfuente"
RESPONSIBILITY_TABLE = "col_responsabilidad"
RESPONSIBILITY_TYPE_TABLE = "col_responsabilidadtipo"
RESTRICTION_TABLE_DESCRIPTION_FIELD = "descripcion"
RESTRICTION_TABLE = "col_restriccion"
RESTRICTION_TABLE_PARCEL_FIELD = "unidad_predio"
RESTRICTION_TYPE_TABLE = "col_restricciontipo"
RRR_SOURCE_RELATION_TABLE = "rrrfuente"
RRR_SOURCE_RESPONSIBILITY_FIELD = "rrr_col_responsabilidad"
RRR_SOURCE_RESTRICTION_FIELD = "rrr_col_restriccion"
RRR_SOURCE_RIGHT_FIELD = "rrr_col_derecho"
RRR_SOURCE_SOURCE_FIELD = "rfuente"
RIGHT_TABLE = "op_derecho"
RIGHT_TABLE_PARCEL_FIELD = "unidad_predio"
RIGHT_TABLE_PARTY_FIELD = "interesado_col_interesado"
RIGHT_TABLE_GROUP_PARTY_FIELD = "interesado_la_agrupacion_interesados"
RIGHT_TABLE_TYPE_FIELD = "tipo"
RIGHT_TYPE_TABLE = "col_derechotipo"
RIGHT_OF_WAY_TABLE="servidumbrepaso"
RIGHT_OF_WAY_TABLE_IDENTIFICATOR_FIELD = "identificador"
REFERENCE_POINT_FIELD = "punto_referencia"
SECOND_NAME_FIELD = "segundo_nombre"
SECOND_SURNAME_FIELD = "segundo_apellido"
SPATIAL_SOURCE_TABLE = "col_fuenteespacial"
SPATIAL_SOURCE_TYPE_TABLE = "col_fuenteespacialtipo"
SURVEY_POINT_TABLE = "op_puntolevantamiento"
SURVEY_POINT_TYPE_TABLE = "col_puntolevtipo"
TABLE_PROP_ASSOCIATION = "ASSOCIATION"
TABLE_PROP_DOMAIN = "ENUM"
TABLE_PROP_STRUCTURE = "STRUCTURE"
TYPE_BUILDING_TYPE_TABLE = "col_tipoconstrucciontipo"
TYPE_FIELD = "tipo"
UEBAUNIT_TABLE = "col_uebaunit"
UEBAUNIT_TABLE_BUILDING_FIELD = "ue_op_construccion"
UEBAUNIT_TABLE_BUILDING_UNIT_FIELD = "ue_op_unidadconstruccion"
UEBAUNIT_TABLE_PARCEL_FIELD = "baunit"
UEBAUNIT_TABLE_PLOT_FIELD = "ue_op_terreno"
UEBAUNIT_TABLE_RIGHT_OF_WAY_FIELD = "ue_op_servidumbrepaso"
UESOURCE_TABLE = "uefuente"
UESOURCE_TABLE_PLOT_FIELD = "ue_terreno"
UESOURCE_TABLE_SOURCE_FIELD = "pfuente"
VIDA_UTIL_FIELD = "comienzo_vida_util_version"
ZONE_FIELD = "zona"

"""
PROPERTY RECORD CARD MAPPING
"""
PROPERTY_RECORD_CARD_TABLE = "predio_ficha"
PROPERTY_RECORD_CARD_PARCEL_ID_FIELD = "crpredio"
PROPERTY_RECORD_CARD_SECTOR_FIELD = "sector"
PROPERTY_RECORD_CARD_BLOCK_TOWN_FIELD = "manzana_vereda"
PROPERTY_RECORD_CARD_ECONOMIC_DESTINATION_FIELD = "destinacion_economica"
PROPERTY_RECORD_CARD_LOCALITY_FIELD = "localidad_comuna"
PRC_PUBLIC_PARCEL_TYPE_FIELD = "tipo_predio_publico"
PRC_PARCEL_TYPE_FIELD = "predio_tipo"
MARKET_RESEARCH_TABLE = "investigacionmercado"
NUCLEAR_FAMILY_TABLE = "nucleofamiliar"
NATURAL_PARTY_TABLE = "interesado_natural"
LEGAL_PARTY_TABLE = "interesado_juridico"

"""
VALUATION MAPPING
"""
AVALUOUNIDADCONSTRUCCION_TABLE = "avaluounidadconstruccion"
AVALUOUNIDADCONSTRUCCION_TABLE_BUILDING_UNIT_VALUATION_FIELD = "aucons"
AVALUOUNIDADCONSTRUCCION_TABLE_BUILDING_UNIT_FIELD = "ucons"
VALUATION_PARCEL_TABLE = "avaluos_v2_2_1avaluos_predio"
VALUATION_HORIZONTAL_PROPERTY_TABLE = "predio_matriz_ph"
VALUATION_COMMON_EQUIPMENT_TABLE = "equipamiento_comunal"
VALUATION_BUILDING_TABLE = "avaluos_v2_2_1avaluos_construccion"
VALUATION_BUILDING_UNIT_TABLE = "unidad_construccion"
VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE = "calificacion_no_convencional"
VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE = "calificacion_convencional"
VALUATION_GEOECONOMIC_ZONE_TABLE = "zona_homogenea_geoeconomica"
VALUATION_PHYSICAL_ZONE_TABLE = "zona_homogenea_fisica"



"""
PLURAL WORDS, FOR DISPLAY PURPOSES
"""
DICT_PLURAL = {
    PLOT_TABLE: "Terrenos",
    PARCEL_TABLE: "Predios",
    BUILDING_TABLE: "Construcciones",
    BUILDING_UNIT_TABLE: "Unidades de Construcción",
    EXTADDRESS_TABLE: "Direcciones",
    COL_PARTY_TABLE: "Interesados",
    LA_GROUP_PARTY_TABLE: "Agrupación de interesados",
    RIGHT_TABLE: "Derechos",
    RESTRICTION_TABLE: "Restricciones",
    RESPONSIBILITY_TABLE: "Responsabilidades",
    MORTGAGE_TABLE: "Hipotecas",
    ADMINISTRATIVE_SOURCE_TABLE: "Fuentes Administrativas",
    SPATIAL_SOURCE_TABLE: "Fuentes Espaciales",
    NUCLEAR_FAMILY_TABLE: "Núcleo Familiar",
    MARKET_RESEARCH_TABLE: "Investigaciones de Mercado",
    PROPERTY_RECORD_CARD_TABLE: "Ficha Predial",
    BOUNDARY_TABLE: "Linderos",
    BOUNDARY_POINT_TABLE: "Puntos de Lindero",
    SURVEY_POINT_TABLE: "Puntos de Levantamiento"
}


"""
LADM PACKAGES
"""
SURVEYING_AND_REPRESENTATION_PACKAGE = "Topografía y Representación"
SPATIAL_UNIT_PACKAGE = "Unidad Espacial"
BA_UNIT_PACKAGE = "Unidad Administrativa"
RRR_PACKAGE = "Derechos, Restricciones y Responsabilidades"
PARTY_PACKAGE = "Interesados"
SOURCE_PACKAGE = "Fuentes"

"""
LADM PACKAGE ICONS
"""
DICT_PACKAGE_ICON = { # Resources don't seem to be initialized at this point, so return path and build icon when needed
    SURVEYING_AND_REPRESENTATION_PACKAGE: ":/Asistente-LADM_COL/resources/images/surveying.png",
    SPATIAL_UNIT_PACKAGE: ":/Asistente-LADM_COL/resources/images/spatial_unit.png",
    BA_UNIT_PACKAGE: ":/Asistente-LADM_COL/resources/images/ba_unit.png",
    RRR_PACKAGE: ":/Asistente-LADM_COL/resources/images/rrr.png",
    PARTY_PACKAGE: ":/Asistente-LADM_COL/resources/images/party.png",
    SOURCE_PACKAGE: ":/Asistente-LADM_COL/resources/images/source.png"
}

DICT_TABLE_PACKAGE = {
    PARCEL_TABLE: BA_UNIT_PACKAGE,
    PLOT_TABLE: SPATIAL_UNIT_PACKAGE,
    BUILDING_TABLE: SPATIAL_UNIT_PACKAGE,
    BUILDING_UNIT_TABLE: SPATIAL_UNIT_PACKAGE,
    RIGHT_OF_WAY_TABLE: SPATIAL_UNIT_PACKAGE,
    COL_PARTY_TABLE: PARTY_PACKAGE,
    LA_GROUP_PARTY_TABLE: PARTY_PACKAGE,
    RIGHT_TABLE: RRR_PACKAGE,
    RESTRICTION_TABLE: RRR_PACKAGE,
    RESPONSIBILITY_TABLE: RRR_PACKAGE,
    MORTGAGE_TABLE: RRR_PACKAGE,
    ADMINISTRATIVE_SOURCE_TABLE: SOURCE_PACKAGE,
    SPATIAL_SOURCE_TABLE: SOURCE_PACKAGE,
    BOUNDARY_POINT_TABLE: SURVEYING_AND_REPRESENTATION_PACKAGE,
    SURVEY_POINT_TABLE: SURVEYING_AND_REPRESENTATION_PACKAGE,
    BOUNDARY_TABLE: SURVEYING_AND_REPRESENTATION_PACKAGE
}


NAMESPACE_PREFIX = {
    ADMINISTRATIVE_SOURCE_TABLE: 's',
    BOUNDARY_POINT_TABLE: 'p',
    BOUNDARY_TABLE: 'ccl',
    BUILDING_TABLE: 'su',
    BUILDING_UNIT_TABLE: 'su',
    COL_PARTY_TABLE: 'p',
    CONTROL_POINT_TABLE: 'p',
    EXTFILE_TABLE: 's',
    LA_GROUP_PARTY_TABLE: 'p',
    PARCEL_TABLE: 'u',
    PLOT_TABLE: 'su',
    RESPONSIBILITY_TABLE: 'r',
    RESTRICTION_TABLE: 'r',
    RIGHT_OF_WAY_TABLE: 'su',
    RIGHT_TABLE: 'r',
    SPATIAL_SOURCE_TABLE: 's',
    SURVEY_POINT_TABLE: 'p'
}

DICT_AUTOMATIC_VALUES = {
    BOUNDARY_TABLE: [{LENGTH_FIELD_BOUNDARY_TABLE: "$length"}],
    COL_PARTY_TABLE: [{COL_PARTY_NAME_FIELD: "regexp_replace(regexp_replace(regexp_replace(concat({}, ' ', {}, ' ', {}, ' ', {}, ' ', {}, ' ', {}), '\\\\s+', ' '), '^\\\\s+', ''), '\\\\s+$', '')".format(
        DOCUMENT_ID_FIELD,
        FIRST_SURNAME_FIELD,
        SECOND_SURNAME_FIELD,
        FIRST_NAME_FIELD,
        SECOND_NAME_FIELD,
        BUSINESS_NAME_FIELD)}],
    PARCEL_TABLE: [{DEPARTMENT_FIELD: 'substr("numero_predial", 0, 2)'},
                   {MUNICIPALITY_FIELD: 'substr("numero_predial", 3, 3)'},
                   {ZONE_FIELD: 'substr("numero_predial", 6, 2)'}],
    OID_TABLE: [{"localid": "$id"},
                {"espaciodenombres": "\'OID\'"}]
}

DICT_DISPLAY_EXPRESSIONS = {
    COL_PARTY_TABLE: "regexp_replace(regexp_replace(regexp_replace(concat({}, ' ', {}, ' ', {}, ' ', {}, ' ', {}, ' ', {}), '\\\\s+', ' '), '^\\\\s+', ''), '\\\\s+$', '')".format(
        DOCUMENT_ID_FIELD,
        FIRST_SURNAME_FIELD,
        SECOND_SURNAME_FIELD,
        FIRST_NAME_FIELD,
        SECOND_NAME_FIELD,
        BUSINESS_NAME_FIELD),
    PARCEL_TABLE: "concat({}, ' - ', {}, ' - ', {})".format(ID_FIELD, PARCEL_NUMBER_FIELD, FMI_FIELD),
    LA_BAUNIT_TABLE: "{} || ' ' || {} || ' ' || {}".format(ID_FIELD, LA_BAUNIT_NAME_FIELD, TYPE_FIELD),
    LA_GROUP_PARTY_TABLE: "concat({}, ' - ', {})".format(ID_FIELD, LA_GROUP_PARTY_NAME_FIELD),
    BUILDING_TABLE: '"{}{}"  || \' \' ||  "{}"'.format(NAMESPACE_PREFIX[BUILDING_UNIT_TABLE],
                                                                    NAMESPACE_FIELD,
                                                                    ID_FIELD)
}

LAYER_VARIABLES = {
    BUILDING_TABLE: {
        "qgis_25d_angle": 90,
        "qgis_25d_height": 1
    },
    BUILDING_UNIT_TABLE: {
        "qgis_25d_angle": 90,
        "qgis_25d_height": '"{}" * 2.5'.format(NUMBER_OF_FLOORS)
    }
}

# Read only fields might be declared in two scenarios:
#   1. As soon as the layer is loaded (e.g., DEPARTMENT_FIELD)
#   2. Only for a wizard (e.g., PARCEL_TYPE)
# WARNING: Both modes are exclusive, if you list a field in 1, DO NOT do it in 2. and viceversa!
CUSTOM_READ_ONLY_FIELDS = {
    PARCEL_TABLE: [DEPARTMENT_FIELD, MUNICIPALITY_FIELD, ZONE_FIELD]  # list of fields of the layer to block its edition
}

CUSTOM_WIDGET_CONFIGURATION = {
    EXTFILE_TABLE: {
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

LAYER_CONSTRAINTS = {
    PROPERTY_RECORD_CARD_TABLE: {
        PRC_PUBLIC_PARCEL_TYPE_FIELD: {
            'expression': 'CASE WHEN "{prc_ptf}" IS NOT NULL THEN\n(strpos("{prc_ptf}", \'Privado.\') != 0 AND "{prc_pptf}" IS NULL) OR (strpos("{prc_ptf}", \'Publico.\') != 0 AND "{prc_pptf}" IS NOT NULL)\nELSE True\nEND'.format(prc_ptf=PRC_PARCEL_TYPE_FIELD, prc_pptf=PRC_PUBLIC_PARCEL_TYPE_FIELD),
            'description': 'Si el tipo de predio es Público, debes elegir un valor de este listado; pero si el tipo de predio es Privado, no debes seleccionar ningún valor de este listado.'
        }
    },
    PARCEL_TABLE: {
        PARCEL_TYPE_FIELD: {
            'expression': """
                            CASE
                                WHEN  "{parcel_type}" =  'NPH' THEN
                                    num_selected('{plot_layer}') = 1 AND num_selected('{building_unit_layer}') = 0
                                WHEN  "{parcel_type}" IN  ('PropiedadHorizontal.Matriz', 'Condominio.Matriz', 'ParqueCementerio.Matriz', 'BienUsoPublico', 'Condominio.UnidadPredial') THEN
                                    num_selected('{plot_layer}') = 1 AND num_selected('{building_unit_layer}') = 0
                                WHEN  "{parcel_type}" IN  ('Via', 'ParqueCementerio.UnidadPrivada') THEN
                                    num_selected('{plot_layer}') = 1 AND num_selected('{building_unit_layer}') = 0 AND num_selected('{building_layer}') = 0
                                WHEN  "{parcel_type}" =   'PropiedadHorizontal.UnidadPredial' THEN
                                    num_selected('{plot_layer}') = 0 AND num_selected('{building_unit_layer}') != 0 AND num_selected('{building_layer}') = 0
                                WHEN  "{parcel_type}" =  'Mejora' THEN
                                    num_selected('{plot_layer}') = 0 AND num_selected('{building_unit_layer}') = 0 AND num_selected('{building_layer}') = 1
                                ELSE
                                    TRUE
                            END""".format(parcel_type=PARCEL_TYPE_FIELD, plot_layer=PLOT_TABLE, building_layer=BUILDING_TABLE, building_unit_layer=BUILDING_UNIT_TABLE),
            'description': 'La parcela debe tener una o varias unidades espaciales asociadas. Verifique las reglas ' #''Parcel must have one or more spatial units associated with it. Check the rules.'
        },
        PARCEL_NUMBER_FIELD: {
            'expression': """CASE
                                WHEN  "{parcel_number}" IS NOT NULL THEN
                                    CASE
                                        WHEN length("{parcel_number}") != 30 OR regexp_match(to_string("{parcel_number}"), '^[0-9]*$') = 0  THEN
                                            FALSE
                                        WHEN "{parcel_type}" = 'NPH' THEN
                                            substr("{parcel_number}", 22,1) = 0
                                        WHEN strpos( "{parcel_type}", 'PropiedadHorizontal.') != 0 THEN
                                            substr("{parcel_number}", 22,1) = 9
                                        WHEN strpos( "{parcel_type}", 'Condominio.') != 0 THEN
                                            substr("{parcel_number}", 22,1) = 8
                                        WHEN strpos("{parcel_type}", 'ParqueCementerio.') != 0 THEN
                                            substr("{parcel_number}", 22,1) = 7
                                        WHEN "{parcel_type}" = 'Mejora' THEN
                                            substr("{parcel_number}", 22,1) = 5
                                        WHEN "{parcel_type}" = 'Via' THEN
                                            substr("{parcel_number}", 22,1) = 4
                                        WHEN "{parcel_type}" = 'BienUsoPublico' THEN
                                            substr("{parcel_number}", 22,1) = 3
                                        ELSE
                                            TRUE
                                    END
                                ELSE
                                    TRUE
                            END""".format(parcel_type=PARCEL_TYPE_FIELD, parcel_number=PARCEL_NUMBER_FIELD),
            'description': 'El campo debe tener 30 caracteres numéricos y la posición 22 debe coincidir con el tipo de predio.'
        }, PARCEL_NUMBER_BEFORE_FIELD: {
            'expression': """CASE
                                WHEN  "{parcel_number_before}" IS NULL THEN
                                    TRUE
                                WHEN length("{parcel_number_before}") != 20 OR regexp_match(to_string("{parcel_number_before}"), '^[0-9]*$') = 0 THEN
                                    FALSE
                                ELSE
                                    TRUE
                            END""".format(parcel_number_before=PARCEL_NUMBER_BEFORE_FIELD),
            'description': 'El campo debe tener 20 caracteres numéricos.'
        }, PARCEL_VALUATION_FIELD:{
            'expression': """
                            CASE
                                WHEN  "{parcel_valuation}" IS NULL THEN
                                    TRUE
                                WHEN  "{parcel_valuation}" = 0 THEN
                                    FALSE
                                ELSE
                                    TRUE
                            END""".format(parcel_valuation=PARCEL_VALUATION_FIELD),
            'description': 'El valor debe ser mayor a cero (0).'
        }
    },
    COL_PARTY_TABLE: {
        COL_PARTY_DOC_TYPE_FIELD: {
            'expression': """
                            CASE
                                WHEN  "{col_party_type}" = 'Persona_Natural' THEN
                                     "{col_party_doc_type}" !=  'NIT'
                                WHEN  "{col_party_type}" = 'Persona_No_Natural' THEN
                                     "{col_party_doc_type}" = 'NIT' OR "{col_party_doc_type}" = 'Secuencial_IGAC' OR "{col_party_doc_type}" = 'Secuencial_SNR'
                                ELSE
                                    TRUE
                            END""".format(col_party_type=COL_PARTY_TYPE_FIELD, col_party_doc_type=COL_PARTY_DOC_TYPE_FIELD),
            'description': 'Si el tipo de interesado es "Persona Natural" entonces el tipo de documento debe ser diferente de \'NIT\'. Pero si el tipo de interesado es "Persona No Natural" entonces el tipo de documento debe ser \'NIT\' o \'Secuencial IGAC\' o \'Secuencial SNR\'. '
        }, COL_PARTY_FIRST_NAME_FIELD:{
            'expression': """
                        CASE
                            WHEN  "{col_party_type}" = 'Persona_Natural'  THEN
                                 "{col_party_first_name}" IS NOT NULL AND length(trim("{col_party_first_name}")) != 0
                            WHEN  "{col_party_type}" = 'Persona_No_Natural'  THEN
                                 "{col_party_first_name}" IS NULL
                            ELSE
                                TRUE
                        END""".format(col_party_type=COL_PARTY_TYPE_FIELD, col_party_first_name=COL_PARTY_FIRST_NAME_FIELD),
            'description': 'Si el tipo de interesado es "Persona Natural" este campo se debe diligenciar, si el tipo de interesado es "Persona No Natural" este campo debe ser NULL.'
        }, COL_PARTY_SURNAME_FIELD: {
            'expression': """
                CASE
                    WHEN  "{col_party_type}" = 'Persona_Natural' THEN
                         "{col_party_surname}" IS NOT NULL AND length(trim("{col_party_surname}")) != 0
                    WHEN  "{col_party_type}" = 'Persona_No_Natural' THEN
                         "{col_party_surname}" IS NULL
                    ELSE
                        TRUE
                END""".format(col_party_type=COL_PARTY_TYPE_FIELD, col_party_surname=COL_PARTY_SURNAME_FIELD),
            'description': 'Si el tipo de interesado es "Persona Natural" este campo se debe diligenciar, si el tipo de interesado es "Persona No Natural" este campo debe ser NULL.'
        }, COL_PARTY_BUSINESS_NAME_FIELD:{
            'expression': """
                            CASE
                                WHEN  "{col_party_type}" =  'Persona_No_Natural' THEN
                                     "{col_party_business_name}" IS NOT NULL AND  length(trim( "{col_party_business_name}")) != 0
                                WHEN  "{col_party_type}" =  'Persona_Natural' THEN
                                     "{col_party_business_name}" IS NULL
                                ELSE
                                    TRUE
                            END""".format(col_party_type=COL_PARTY_TYPE_FIELD, col_party_business_name=COL_PARTY_BUSINESS_NAME_FIELD),
            'description': 'Si el tipo de interesado es "Persona No Natural" este campo se debe diligenciar, si el tipo de interesado es "Persona Natural" este campo debe ser NULL.'

        }, COL_PARTY_LEGAL_PARTY_FIELD:{
            'expression': """
                            CASE
                                WHEN  "{col_party_type}" =  'Persona_No_Natural' THEN
                                     "{col_party_legal_party}" IS NOT NULL
                                WHEN  "{col_party_type}" =  'Persona_Natural' THEN
                                     "{col_party_legal_party}" IS NULL
                                ELSE
                                    TRUE
                            END""".format(col_party_type=COL_PARTY_TYPE_FIELD, col_party_legal_party=COL_PARTY_LEGAL_PARTY_FIELD),
            'description': 'Si el tipo de interesado es "Persona No Natural" este campo se debe diligenciar, si el tipo de interesado es "Persona Natural" este campo debe ser NULL.'

        }, COL_PARTY_DOCUMENT_ID_FIELD:{
            'expression': """
                            CASE
                                WHEN  "{col_party_document_id}"  IS NULL THEN
                                    FALSE
                                WHEN length(trim("{col_party_document_id}")) = 0 THEN
                                    FALSE
                                ELSE
                                    TRUE
                            END""".format(col_party_document_id=COL_PARTY_DOCUMENT_ID_FIELD),
            'description': 'El campo es obligatorio.'

        }
    },
    PLOT_TABLE: {
        PLOT_CALCULATED_AREA_FIELD: {
            'expression': """
                            CASE
                                WHEN  "{plot_calculated_area}" IS NULL THEN
                                    FALSE
                                WHEN  "{plot_calculated_area}" = 0 THEN
                                    FALSE
                                ELSE
                                    TRUE
                            END""".format(plot_calculated_area = PLOT_CALCULATED_AREA_FIELD),
            'description': 'El valor debe ser mayor a cero (0).'
        }, PLOT_VALUATION_FIELD: {
            'expression': """
                            CASE
                                WHEN  "{plot_valuation_field}" IS NULL THEN
                                    FALSE
                                WHEN  "{plot_valuation_field}" = 0 THEN
                                    FALSE
                                ELSE
                                    TRUE
                            END""".format(plot_valuation_field = PLOT_VALUATION_FIELD),
            'description': 'El valor debe ser mayor a cero (0).'
        }
    },
    BUILDING_TABLE: {
        BUILDING_AREA_FIELD: {
            'expression': """
                    CASE
                        WHEN  "{building_area}" IS NULL THEN
                            TRUE
                        WHEN  "{building_area}" = 0 THEN
                            FALSE
                        ELSE
                            TRUE
                    END""".format(building_area=BUILDING_AREA_FIELD),
            'description': 'El valor debe ser mayor a cero (0).'
        }, BUILDING_VALUATION_FIELD: {
            'expression': """
                    CASE
                        WHEN  "{building_valuation_field}" IS NULL THEN
                            FALSE
                        WHEN  "{building_valuation_field}" = 0 THEN
                            FALSE
                        ELSE
                            TRUE
                    END""".format(building_valuation_field=BUILDING_VALUATION_FIELD),
            'description': 'El valor debe ser mayor a cero (0).'
        }
    },
    BUILDING_UNIT_TABLE: {
        BUILDING_UNIT_AREA_FIELD: {
            'expression': """
                    CASE
                        WHEN  "{building_unit_area}" IS NULL THEN
                            TRUE
                        WHEN  "{building_unit_area}" = 0 THEN
                            FALSE
                        ELSE
                            TRUE
                    END""".format(building_unit_area=BUILDING_UNIT_AREA_FIELD),
            'description': 'El valor debe ser mayor a cero (0).'
        }, BUILDING_UNIT_PRIVATE_AREA_FIELD: {
            'expression': """
                    CASE
                        WHEN  "{building_unit_private_area}" IS NULL THEN
                            TRUE
                        WHEN  "{building_unit_private_area}" = 0 THEN
                            FALSE
                        ELSE
                            TRUE
                    END""".format(building_unit_private_area=BUILDING_UNIT_PRIVATE_AREA_FIELD),
            'description': 'El valor debe ser mayor a cero (0).'
        }, BUILDING_UNIT_VALUATION_FIELD: {
            'expression': """
                    CASE
                        WHEN  "{building_unit_valuation_field}" IS NULL THEN
                            TRUE
                        WHEN  "{building_unit_valuation_field}" = 0 THEN
                            FALSE
                        ELSE
                            TRUE
                    END""".format(building_unit_valuation_field=BUILDING_UNIT_VALUATION_FIELD),
            'description': 'El valor debe ser mayor a cero (0).'
        }
    }
}

"""
Do not use the same before attribute for 2 differente groups. The same applies
to after attribute.

Leave before_attr/after_attr empty to add the group at the end of the form.
"""
FORM_GROUPS = {
    PROPERTY_RECORD_CARD_TABLE: {
        'Código Predial Nacional': {
            'show_label': True,
            'column_count': 1,
            'attr_list': ['sector', 'barrio', 'localidad_comuna', 'manzana_vereda', 'terreno', 'condicion_propiedad', 'edificio', 'piso', 'unidad'],
            'visibility_expression': None,
            'before_attr': 'estado_nupre',
            'after_attr': None
        },
        'Tipo predio público': {
            'show_label': False,
            'column_count':  1,
            'attr_list':  ['tipo_predio_publico'],
            'visibility_expression': '"predio_tipo" IS NOT NULL AND strpos("predio_tipo", \'Publico.\') != 0',
            'before_attr': None,
            'after_attr': 'predio_tipo'
        }
    },
    VALUATION_PARCEL_TABLE: {
        ' ': {
            'show_label': True,
            'column_count':  1,
            'attr_list':  ['num_balcones', 'num_terrazas', 'num_mezanines'],
            'visibility_expression': None,
            'before_attr': None,
            'after_attr': None
        },
        '  ': {
            'show_label': True,
            'column_count':  1,
            'attr_list':  ['frente', 'fondo'],
            'visibility_expression': None,
            'before_attr': None,
            'after_attr': 'comun_uso_exclusivo'
        }
        },
    VALUATION_HORIZONTAL_PROPERTY_TABLE: {
        '': {
            'show_label': True,
            'column_count': 1,
            'attr_list': ['tipologia_constructiva_copropiedad', 'anio_construccion_etapa',
                          'estado_conservacion_copropiedad', 'materiales_construccion_areas_comunes',
                          'disenio_funcionalidad_copropiedad'],
            'visibility_expression': None,
            'before_attr': None,
            'after_attr': None
        },
        ' ': {
            'show_label': True,
            'column_count': 1,
            'attr_list': ['num_etapas', 'num_interiores', 'num_torres', 'num_pisos_por_torre', 'num_unidades_privadas',
                          'num_sotanos'],
            'visibility_expression': None,
            'before_attr': None,
            'after_attr': None
        }
    },
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


"""
we define the minimum structure of a table to validate that there are no repeated records
"""
LOGIC_CONSISTENCY_TABLES = {
    # Geometric tables
    BOUNDARY_POINT_TABLE: ['acuerdo',
                           'fotoidentificacion',
                           'ubicacion_punto',
                           'exactitud_vertical',
                           'exactitud_horizontal',
                           'posicion_interpolacion',
                           'monumentacion',
                           'metodoproduccion',
                           'puntotipo',
                           'localizacion_original'],
    SURVEY_POINT_TABLE: ['tipo_punto_levantamiento',
                         'fotoidentificacion',
                         'exactitud_vertical',
                         'exactitud_horizontal',
                         'posicion_interpolacion',
                         'metodoproduccion',
                         'monumentacion',
                         'puntotipo',
                         'localizacion_original'],
    CONTROL_POINT_TABLE: ['nombre_punto',
                          'exactitud_vertical',
                          'exactitud_horizontal',
                          'tipo_punto_control',
                          'confiabilidad',
                          'posicion_interpolacion',
                          'monumentacion',
                          'puntotipo',
                          'localizacion_original'],
    BOUNDARY_TABLE: [LENGTH_FIELD_BOUNDARY_TABLE,
                     'localizacion_textual',
                     'geometria'],
    PLOT_TABLE: ['area_terreno',
                 'avaluo_terreno',
                 'dimension',
                 'etiqueta',
                 'relacion_superficie',
                 'poligono_creado'],
    BUILDING_TABLE: ['avaluo_construccion',
                     'area_construccion',
                     'dimension',
                     'etiqueta',
                     'relacion_superficie',
                     'poligono_creado'],
    BUILDING_UNIT_TABLE: ['avaluo_unidad_construccion',
                          'numero_pisos',
                          'area_construida',
                          'area_privada_construida',
                          'op_construccion',
                          'dimension',
                          'etiqueta',
                          'relacion_superficie',
                          'poligono_creado'],
    # Alphanumeric tables
    COL_PARTY_TABLE: ['documento_identidad',
                      'tipo_documento'],
    PARCEL_TABLE: ['departamento',
                   'municipio',
                   'zona',
                   'nupre',
                   'fmi',
                   'numero_predial',
                   'numero_predial_anterior',
                   'avaluo_predio',
                   'copropiedad',
                   'nombre',
                   'tipo'],
    RIGHT_TABLE: ['tipo',
                  'codigo_registral_derecho',
                  'descripcion',
                  'comprobacion_comparte',
                  'uso_efectivo',
                  'r_espacio_de_nombres',
                  'interesado_la_agrupacion_interesados',
                  'interesado_col_interesado',
                  'unidad_la_baunit',
                  'unidad_predio'],
    RESTRICTION_TABLE: ['interesado_requerido',
                        'tipo',
                        'codigo_registral_restriccion',
                        'descripcion',
                        'comprobacion_comparte',
                        'uso_efectivo',
                        'interesado_la_agrupacion_interesados',
                        'interesado_col_interesado',
                        'unidad_la_baunit',
                        'unidad_predio'],
    RESPONSIBILITY_TABLE: ['tipo',
                           'codigo_registral_responsabilidad',
                           'descripcion',
                           'comprobacion_comparte',
                           'uso_efectivo',
                           'interesado_la_agrupacion_interesados',
                           'interesado_col_interesado',
                           'unidad_la_baunit',
                           'unidad_predio'],
    ADMINISTRATIVE_SOURCE_TABLE: ['texto',
                                  'tipo',
                                  'codigo_registral_transaccion',
                                  'nombre',
                                  'fecha_aceptacion',
                                  'estado_disponibilidad',
                                  'sello_inicio_validez',
                                  'tipo_principal',
                                  'fecha_grabacion',
                                  'fecha_entrega',
                                  'oficialidad']
}



"""
Constrains for wizard create parcel
"""

# Types of parcels
PARCEL_TYPE_NO_HORIZONTAL_PROPERTY = "NPH"
PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT = "PropiedadHorizontal.Matriz"
PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT = "PropiedadHorizontal.UnidadPredial"
PARCEL_TYPE_CONDOMINIUM_PARENT = "Condominio.Matriz"
PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT = "Condominio.UnidadPredial"
PARCEL_TYPE_MEJORA = "Mejora"
PARCEL_TYPE_CEMETERY_PARENT = "ParqueCementerio.Matriz"
PARCEL_TYPE_CEMETERY_PRIVATE_UNIT = "ParqueCementerio.UnidadPrivada"
PARCEL_TYPE_ROAD = "Via"
PARCEL_TYPE_PUBLIC_USE = "BienUsoPublico"
PARCEL_TYPE_STORE = "Deposito"
PARCEL_TYPE_PARKING = "Parqueadero"
PARCEL_TYPE_WAREHOUSE = "Bodega"

# Operations:
# 1 = One and only one feature must be selected
# + = One or more features must be selected
# * = Optional, i.e., zero or more features could be selected
# None = Won't be stored as a related feature (selected features will be ignored)
CONSTRAINT_TYPES_OF_PARCEL = {
    PARCEL_TYPE_NO_HORIZONTAL_PROPERTY: {
        PLOT_TABLE: 1,
        BUILDING_TABLE: '*',
        BUILDING_UNIT_TABLE: '*'
    },
    PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT: {
        PLOT_TABLE: 1,
        BUILDING_TABLE: '*',
        BUILDING_UNIT_TABLE: None
    },
    PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT: {
        PLOT_TABLE: None,
        BUILDING_TABLE: None,
        BUILDING_UNIT_TABLE: '+'
    },
    PARCEL_TYPE_CONDOMINIUM_PARENT: {
        PLOT_TABLE: 1,
        BUILDING_TABLE: '*',
        BUILDING_UNIT_TABLE: None
    },
    PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT: {
        PLOT_TABLE: 1,
        BUILDING_TABLE: '*',
        BUILDING_UNIT_TABLE: None
    },
    PARCEL_TYPE_MEJORA: {
        PLOT_TABLE: None,
        BUILDING_TABLE: '*',
        BUILDING_UNIT_TABLE: '+'
    },
    PARCEL_TYPE_CEMETERY_PARENT: {
        PLOT_TABLE: 1,
        BUILDING_TABLE: '*',
        BUILDING_UNIT_TABLE: None
    },
    PARCEL_TYPE_CEMETERY_PRIVATE_UNIT: {
        PLOT_TABLE: 1,
        BUILDING_TABLE: None,
        BUILDING_UNIT_TABLE: None
    },
    PARCEL_TYPE_ROAD: {
        PLOT_TABLE: 1,
        BUILDING_TABLE: None,
        BUILDING_UNIT_TABLE: None
    },
    PARCEL_TYPE_PUBLIC_USE: {
        PLOT_TABLE: 1,
        BUILDING_TABLE: '*',
        BUILDING_UNIT_TABLE: None
    },
    PARCEL_TYPE_STORE: {
        PLOT_TABLE: '*',
        BUILDING_TABLE: '*',
        BUILDING_UNIT_TABLE: '*'
    },
    PARCEL_TYPE_PARKING: {
        PLOT_TABLE: '*',
        BUILDING_TABLE: '*',
        BUILDING_UNIT_TABLE: '*'
    },
    PARCEL_TYPE_WAREHOUSE: {
        PLOT_TABLE: '*',
        BUILDING_TABLE: '*',
        BUILDING_UNIT_TABLE: '*'
    }
}
