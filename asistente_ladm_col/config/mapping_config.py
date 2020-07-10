from asistente_ladm_col.config.query_names import QueryNames
from asistente_ladm_col.lib.logger import Logger


T_ID_KEY = 't_id'
T_ILI_TID_KEY = 't_ili_tid'
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
    T_ILI_TID_F = None
    ILICODE_F = None
    DESCRIPTION_F = None
    DISPLAY_NAME_F = None

    GC_NEIGHBOURHOOD_T = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Barrio"
    GC_BUILDING_T = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion"
    GC_COPROPERTY_T = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_copropiedad"
    GC_HP_CONDOMINIUM_DATA_T = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio"
    GC_BLOCK_T = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Manzana"
    GC_PERIMETER_T = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro"
    GC_PARCEL_T = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro"
    GC_OWNER_T = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario"
    GC_RURAL_SECTOR_T = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_SectorRural"
    GC_URBAN_SECTOR_T = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_SectorUrbano"
    GC_PLOT_T = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Terreno"
    GC_BUILDING_UNIT_T = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion"
    GC_RURAL_DIVISION_T = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Vereda"
    GC_PARCEL_TYPE_D = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.GC_CondicionPredioTipo"
    GC_ADDRESS_T = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Direccion"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.GC_SistemaProcedenciaDatosTipo"
    GC_BUILDING_UNIT_TYPE_T = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.GC_UnidadConstruccionTipo"
    GC_COMMISSION_BUILDING_T = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesConstruccion"
    GC_COMMISSION_PLOT_T = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesTerreno"
    GC_COMMISSION_BUILDING_UNIT_T = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesUnidadConstruccion"
    GC_QUALIFICATION_BUILDING_UNIT_T = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_CalificacionUnidadConstruccion"
    GC_PARCEL_STATUS_T = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_EstadoPredio"
    GC_HP_TOWER_DATA_T = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosTorrePH"

    INI_PARCEL_SUPPLIES_T = None  # "Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos.INI_PredioInsumos"
    # "Submodelo_Integracion_Insumos_V1_0.INI_EmparejamientoTipo"

    SNR_RIGHT_T = None  # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Derecho"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos"
    SNR_SOURCE_BOUNDARIES_T = None  # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos"
    SNR_SOURCE_RIGHT_T = None  # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho"
    SNR_PARCEL_REGISTRY_T = None  # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro"
    SNR_TITLE_HOLDER_T = None  # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_titular_derecho"
    SNR_RIGHT_TYPE_D = None  # "Submodelo_Insumos_SNR_V1_0.SNR_CalidadDerechoTipo"
    SNR_TITLE_HOLDER_DOCUMENT_T = None  # "Submodelo_Insumos_SNR_V1_0.SNR_DocumentoTitularTipo"
    SNR_SOURCE_TYPE_D = None  # "Submodelo_Insumos_SNR_V1_0.SNR_FuenteTipo"
    SNR_TITLE_HOLDER_TYPE_D = None  # "Submodelo_Insumos_SNR_V1_0.SNR_PersonaTitularTipo"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_EstructuraMatriculaMatriz"
    # "Submodelo_Insumos_SNR_V1_0.SNR_ClasePredioRegistroTipo"

    # "LADM_COL_V3_0.LADM_Nucleo.col_baunitComoInteresado"
    COL_BAUNIT_SOURCE_T = None  # "LADM_COL_V3_0.LADM_Nucleo.col_baunitFuente"
    COL_CCL_SOURCE_T = None  # "LADM_COL_V3_0.LADM_Nucleo.col_cclFuente"
    # "LADM_COL_V3_0.LADM_Nucleo.CC_MetodoOperacion"

    CI_CODE_PRESENTATION_FORM_D = None  # "LADM_COL_V3_0.LADM_Nucleo.CI_Forma_Presentacion_Codigo"
    # "LADM_COL_V3_0.LADM_Nucleo.col_clFuente"
    # "LADM_COL_V3_0.LADM_Nucleo.COL_AreaTipo"
    # "LADM_COL_V3_0.LADM_Nucleo.COL_AreaValor"
    # "LADM_COL_V3_0.LADM_Nucleo.COL_ContenidoNivelTipo"
    COL_AVAILABILITY_TYPE_D = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_EstadoDisponibilidadTipo"
    # "LADM_COL_V3_0.LADM_Nucleo.COL_EstructuraTipo"
    COL_ADMINISTRATIVE_SOURCE_TYPE_D = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_FuenteAdministrativaTipo"
    COL_SPATIAL_SOURCE_TYPE_D = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_FuenteEspacialTipo"
    COL_INTERPOLATION_TYPE_D = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_InterpolacionTipo"
    COL_PRODUCTION_METHOD_TYPE_D = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_MetodoProduccionTipo"
    # "LADM_COL_V3_0.LADM_Nucleo.COL_RedServiciosTipo"
    # "LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEdificacionTipo"

    EXT_ADDRESS_TYPE_D = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Tipo_Direccion"
    EXT_ADDRESS_TYPE_MAIN_ROAD_CLASS_D = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Clase_Via_Principal"
    EXT_ADDRESS_TYPE_CITY_SECTOR_D = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Sector_Ciudad"
    EXT_ADDRESS_TYPE_PARCEL_SECTOR_D = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Sector_Predio"

    EXT_ARCHIVE_S = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtArchivo"
    EXT_ADDRESS_S = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtDireccion"
    EXT_PARTY_S = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtInteresado"
    # "LADM_COL_V3_0.LADM_Nucleo.ExtRedServiciosFisica"
    # "LADM_COL_V3_0.LADM_Nucleo.ExtUnidadEdificacionFisica"
    FRACTION_S = None # "LADM_COL_V3_0.LADM_Nucleo.Fraccion"
    # "LADM_COL_V3_0.LADM_Nucleo.Imagen"
    # "LADM_COL_V3_0.LADM_Nucleo.COL_ISO19125_Tipo"

    COL_GROUP_PARTY_TYPE_D = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_GrupoInteresadoTipo"
    COL_BAUNIT_TYPE_D = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_UnidadAdministrativaBasicaTipo"

    COL_DIMENSION_TYPE_D = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_DimensionTipo"
    # "LADM_COL_V3_0.LADM_Nucleo.COL_EstadoRedServiciosTipo"
    COL_POINT_TYPE_D = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_PuntoTipo"
    # "LADM_COL_V3_0.LADM_Nucleo.COL_RegistroTipo"
    COL_SURFACE_RELATION_TYPE_D = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_RelacionSuperficieTipo"
    LC_RESTRICTION_TYPE_D = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_RestriccionTipo"
    # "LADM_COL_V3_0.LADM_Nucleo.COL_Transformacion"
    # "LADM_COL_V3_0.LADM_Nucleo.COL_VolumenTipo"
    # "LADM_COL_V3_0.LADM_Nucleo.COL_VolumenValor"
    MORE_BFS_T = None  # "LADM_COL_V3_0.LADM_Nucleo.col_masCcl"
    # "LADM_COL_V3_0.LADM_Nucleo.col_masCl"
    LESS_BFS_T = None  # "LADM_COL_V3_0.LADM_Nucleo.col_menosCcl"
    # "LADM_COL_V3_0.LADM_Nucleo.col_menosCl"
    MEMBERS_T = None  # "LADM_COL_V3_0.LADM_Nucleo.col_miembros"
    POINT_BFS_T = None  # "LADM_COL_V3_0.LADM_Nucleo.col_puntoCcl"
    # "LADM_COL_V3_0.LADM_Nucleo.col_puntoCl"
    COL_POINT_SOURCE_T = None  # "LADM_COL_V3_0.LADM_Nucleo.col_puntoFuente"
    # "LADM_COL_V3_0.LADM_Nucleo.col_relacionFuente"
    # "LADM_COL_V3_0.LADM_Nucleo.col_relacionFuenteUespacial"
    # "LADM_COL_V3_0.LADM_Nucleo.col_responsableFuente"
    COL_RRR_SOURCE_T = None  # "LADM_COL_V3_0.LADM_Nucleo.col_rrrFuente"
    # "LADM_COL_V3_0.LADM_Nucleo.col_topografoFuente"
    COL_UE_BAUNIT_T = None  # "LADM_COL_V3_0.LADM_Nucleo.col_ueBaunit"
    COL_UE_SOURCE_T = None  # "LADM_COL_V3_0.LADM_Nucleo.col_ueFuente"
    # "LADM_COL_V3_0.LADM_Nucleo.col_ueUeGrupo"
    # "LADM_COL_V3_0.LADM_Nucleo.col_unidadFuente"
    LC_AGREEMENT_TYPE_D = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_AcuerdoTipo"
    LC_CONDITION_PARCEL_TYPE_D = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_CondicionPredioTipo"
    LC_RIGHT_TYPE_D = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_DerechoTipo"
    LC_GROUP_PARTY_T = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_AgrupacionInteresados"
    LC_BUILDING_T = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Construccion"
    LC_RIGHT_T = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Derecho"
    LC_ADMINISTRATIVE_SOURCE_T = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_FuenteAdministrativa"
    LC_SPATIAL_SOURCE_T = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_FuenteEspacial"
    LC_PARTY_T = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Interesado"
    LC_PARTY_CONTACT_T = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_InteresadoContacto"
    LC_BOUNDARY_T = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Lindero"
    LC_PARCEL_T = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio"
    LC_COPROPERTY_T = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.lc_predio_copropiedad"
    LC_OPERATION_SUPPLIES_T = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.lc_predio_ini_predioinsumos"
    LC_CONTROL_POINT_T = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoControl"
    LC_SURVEY_POINT_T = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoLevantamiento"
    LC_BOUNDARY_POINT_T = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoLindero"
    LC_RESTRICTION_T = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Restriccion"
    LC_RIGHT_OF_WAY_T = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ServidumbreTransito"
    LC_PLOT_T = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Terreno"
    LC_BUILDING_UNIT_T = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion"
    LC_PHOTO_IDENTIFICATION_TYPE_D = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_FotoidentificacionTipo"
    LC_ADMINISTRATIVE_SOURCE_TYPE_D = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_FuenteAdministrativaTipo"
    LC_ETHNIC_GROUP_TYPE_D = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_GrupoEtnicoTipo"
    LC_PARTY_DOCUMENT_TYPE_D = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_InteresadoDocumentoTipo"
    LC_PARTY_TYPE_D = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_InteresadoTipo"
    LC_PARCEL_TYPE_D = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_PredioTipo"
    LC_CONTROL_POINT_TYPE_D = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_PuntoControlTipo"
    LC_SURVEY_POINT_TYPE_D = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_PuntoLevTipo"
    LC_POINT_TYPE_D = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_PuntoTipo"
    LC_GENRE_D = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_SexoTipo"
    LC_BUILDING_UNIT_USE_D = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_UsoUConsTipo"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_ViaTipo"

    LC_BUILDING_FLOOR_TYPE_D = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_ConstruccionPlantaTipo"
    LC_BUILDING_TYPE_D = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_ConstruccionTipo"
    LC_DOMAIN_BUILDING_TYPE_D = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_DominioConstruccionTipo"
    LC_BUILDING_UNIT_TYPE_D = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_UnidadConstruccionTipo"

    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_DestinacionEconomicaTipo"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_ClaseSueloTipo"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosPHCondominio"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ContactoVisita"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_RelacionPredioTipo"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_EstructuraNovedadNumeroPredial"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_EstructuraNovedadNumeroPredial.Tipo_Novedad"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_EstructuraNovedadFMI"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_ClaseCalificacionTipo"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_ProcedimientoCatastralRegistralTipo"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_TipologiaTipo"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_EstadoConservacionTipo"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_OfertasMercadoInmobiliario"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_OfertaTipo"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_CalificarTipo"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosAdicionalesLevantamientoCatastral"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_CalificacionConvencional"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_AnexoTipo"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ObjetoConstruccion"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_ObjetoConstruccionTipo"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_GrupoCalificacion"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_CategoriaSueloTipo"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_TipologiaConstruccion"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_CalificacionNoConvencional"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.LC_ResultadoVisitaTipo"

    ############################################ FIELD VARIABLES ###########################################################

    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Barrio.Codigo"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Barrio.Codigo_Sector"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Barrio.Geometria"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Barrio.Nombre"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_CalificacionUnidadConstruccion.Componente"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_CalificacionUnidadConstruccion.Detalle_Calificacion"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_CalificacionUnidadConstruccion.Elemento_Calificacion"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_CalificacionUnidadConstruccion.Puntos"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesConstruccion.Geometria"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesConstruccion.Numero_Predial"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesTerreno.Geometria"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesTerreno.Numero_Predial"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesUnidadConstruccion.Geometria"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_ComisionesUnidadConstruccion.Numero_Predial"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Area_Construida"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Codigo_Edificacion"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Codigo_Terreno"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Etiqueta"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Geometria"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Identificador"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Numero_Mezanines"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Numero_Pisos"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Numero_Semisotanos"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Numero_Sotanos"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Tipo_Construccion"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion.Tipo_Dominio"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_copropiedad.Coeficiente_Copropiedad"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Area_Total_Construida_Comun"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Area_Total_Construida_Privada"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Area_Total_Terreno_Comun"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Area_Total_Terreno_Privada"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Total_Unidades_Privadas"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Total_Unidades_Sotano"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio.Valor_Total_Avaluo_Catastral"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosTorrePH.Torre"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosTorrePH.Total_Pisos_Torre"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosTorrePH.Total_Sotanos"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosTorrePH.Total_Unidades_Privadas"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosTorrePH.Total_Unidades_Sotano"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Direccion.Geometria_Referencia"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Direccion.Principal"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Direccion.Valor"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_EstadoPredio.Entidad_Emisora_Alerta"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_EstadoPredio.Estado_Alerta"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_EstadoPredio.Fecha_Alerta"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Manzana.Codigo"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Manzana.Codigo_Anterior"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Manzana.Codigo_Barrio"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Manzana.Geometria"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro.Codigo_Departamento"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro.Codigo_Municipio"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro.Codigo_Nombre"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro.Geometria"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro.Nombre_Geografico"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Perimetro.Tipo_Avaluo"

    GC_PARCEL_T_REGISTRY_OFFICE_F = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Circulo_Registral"
    GC_PARCEL_T_CONDITION_F = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Condicion_Predio"
    GC_PARCEL_T_ECONOMIC_DESTINATION_F = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Destinacion_Economica"
    GC_PARCEL_T_DATE_OF_DATA_F = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Fecha_Datos"
    GC_PARCEL_T_FMI_F = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Matricula_Inmobiliaria_Catastro"
    GC_PARCEL_T_PARCEL_NUMBER_F = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Numero_Predial"
    GC_PARCEL_T_PARCEL_NUMBER_BEFORE_F = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Numero_Predial_Anterior"
    GC_PARCEL_T_NUPRE_F = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.NUPRE"
    GC_PARCEL_T_DATA_SOURCE_F = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Sistema_Procedencia_Datos"
    GC_PARCEL_T_CADASTRAL_TYPE_F = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Tipo_Catastro"
    GC_PARCEL_T_PARCEL_TYPE_F = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Tipo_Predio"

    GC_OWNER_T_VERIFICATION_DIGIT = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Digito_Verificacion"
    GC_OWNER_T_DOCUMENT_ID_F = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Numero_Documento"
    GC_OWNER_T_PARCEL_ID_F = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_propietario_predio.gc_predio_catastro..Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro"
    GC_OWNER_T_SURNAME_1_F = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Primer_Apellido"
    GC_OWNER_T_FIRST_NAME_1_F = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Primer_Nombre"
    GC_OWNER_T_BUSINESS_NAME_F = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Razon_Social"
    GC_OWNER_T_SURNAME_2_F = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Segundo_Apellido"
    GC_OWNER_T_FIRST_NAME_2_F = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Segundo_Nombre"
    GC_OWNER_T_DOCUMENT_TYPE_F = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Propietario.Tipo_Documento"

    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_SectorRural.Codigo"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_SectorRural.Geometria"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_SectorUrbano.Codigo"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_SectorUrbano.Geometria"

    GC_PLOT_T_ALPHANUMERIC_AREA_F = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Alfanumerica"
    GC_PLOT_T_DIGITAL_PLOT_AREA_F = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Digital"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Terreno.Geometria"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Terreno.Manzana_Vereda_Codigo"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Terreno.Numero_Subterraneos"
    GC_PLOT_T_GC_PARCEL_F = None  # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_terreno_predio.gc_predio..Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Anio_Construccion"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Area_Construida"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Area_Privada"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Codigo_Terreno"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Etiqueta"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Geometria"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Identificador"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Planta"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Puntaje"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Tipo_Construccion"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Tipo_Dominio"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Total_Banios"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Total_Habitaciones"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Total_Locales"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Total_Pisos"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion.Uso"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Vereda.Codigo"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Vereda.Codigo_Anterior"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Vereda.Codigo_Sector"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Vereda.Geometria"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Vereda.Nombre"
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_construccion_predio.gc_predio..Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro"  --> gc_predio
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_construccion_unidad.gc_construccion..Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_Construccion"  --> gc_construccion
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_copropiedad.gc_matriz..Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro"  --> gc_matriz
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_copropiedad.gc_unidad..Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro"  --> gc_unidad
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_datosphcondominio_datostorreph.gc_datosphcondominio..Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_DatosPHCondominio"  --> gc_datosphcondominio
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_ph_predio.gc_predio..Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro"  --> gc_predio
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Direcciones..Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro"  --> gc_prediocatastro_direcciones
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro.Estado_Predio..Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro"  --> gc_prediocatastro_estado_predio
    # "Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.gc_unidadconstruccion_calificacionunidadconstruccion.gc_unidadconstruccion..Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_UnidadConstruccion"  --> gc_unidadconstruccion

    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Derecho.Calidad_Derecho_Registro"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Derecho.Codigo_Naturaleza_Juridica"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_EstructuraMatriculaMatriz.Codigo_ORIP"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_EstructuraMatriculaMatriz.Matricula_Inmobiliaria"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Ciudad_Emisora"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Ente_Emisor"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Fecha_Documento"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Numero_Documento"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Tipo_Documento"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho.Ciudad_Emisora"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho.Ente_Emisor"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho.Fecha_Documento"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho.Numero_Documento"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho.Tipo_Documento"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Cabida_Linderos"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Clase_Suelo_Registro"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Codigo_ORIP"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Fecha_Datos"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Matricula_Inmobiliaria"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Nomenclatura_Registro"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Numero_Predial_Anterior_en_FMI"
    SNR_PARCEL_REGISTRY_T_NEW_PARCEL_NUMBER_IN_FMI_F = None  # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Numero_Predial_Nuevo_en_FMI"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_titular_derecho.Porcentaje_Participacion"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Nombres"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Numero_Documento"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Primer_Apellido"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Razon_Social"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Segundo_Apellido"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Tipo_Documento"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular.Tipo_Persona"
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_derecho_fuente_derecho.snr_fuente_derecho..Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteDerecho"  --> snr_fuente_derecho
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_derecho_predio.snr_predio_registro..Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro"  --> snr_predio_registro
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos.Archivo..Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos"  --> snr_fuentecabidalndros_archivo
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_predio_registro_fuente_cabidalinderos.snr_fuente_cabidalinderos..Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_FuenteCabidaLinderos"  --> snr_fuente_cabidalinderos
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro.Matricula_Inmobiliaria_Matriz..Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro"  --> snr_predioregistro_matricula_inmobiliaria_matriz
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_titular_derecho.snr_derecho..Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Derecho"  --> snr_derecho
    # "Submodelo_Insumos_SNR_V1_0.Datos_SNR.snr_titular_derecho.snr_titular..Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_Titular"  --> snr_titular

    BAUNIT_SOURCE_T_SOURCE_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_baunitFuente.fuente_espacial..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_FuenteEspacial"  --> fuente_espacial
    BAUNIT_SOURCE_T_UNIT_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_baunitFuente.unidad..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio"  --> unidad
    COL_BAUNIT_RRR_T_UNIT_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_baunitRrr.unidad..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio"  --> unidad
    COL_CCL_SOURCE_T_BOUNDARY_F = None # "LADM_COL_V3_0.LADM_Nucleo.col_cclFuente.ccl..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Lindero"  --> ccl
    COL_CCL_SOURCE_T_SOURCE_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_cclFuente.fuente_espacial..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_FuenteEspacial"  --> fuente_espacial
    # "LADM_COL_V3_0.LADM_Nucleo.CC_MetodoOperacion.Ddimensiones_Objetivo"
    # "LADM_COL_V3_0.LADM_Nucleo.CC_MetodoOperacion.Dimensiones_Origen"
    # "LADM_COL_V3_0.LADM_Nucleo.CC_MetodoOperacion.Formula"
    COL_GROUP_PARTY_T_TYPE_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_AgrupacionInteresados.Tipo"
    # "LADM_COL_V3_0.LADM_Nucleo.COL_AreaValor.Area"
    # "LADM_COL_V3_0.LADM_Nucleo.COL_AreaValor.Datos_Proyeccion"
    # "LADM_COL_V3_0.LADM_Nucleo.COL_AreaValor.Tipo"
    COL_BAUNIT_T_NAME_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_UnidadAdministrativaBasica.Nombre"
    COL_BFS_T_GEOMETRY_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_CadenaCarasLimite.Geometria"
    COL_BFS_T_TEXTUAL_LOCATION_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_CadenaCarasLimite.Localizacion_Textual"
    COL_ADMINISTRATIVE_SOURCE_T_SOURCE_NUMBER_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_FuenteAdministrativa.Numero_Fuente"
    COL_ADMINISTRATIVE_SOURCE_T_OBSERVATION_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_FuenteAdministrativa.Observacion"
    COL_SOURCE_T_DESCRIPTION_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_FuenteEspacial.Descripcion"
    COL_SOURCE_T_METADATA_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_FuenteEspacial.Metadato"
    COL_SOURCE_T_NAME_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_FuenteEspacial.Nombre"
    COL_SPATIAL_SOURCE_T_TYPE_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_FuenteEspacial.Tipo"
    COL_SOURCE_T_AVAILABILITY_STATUS_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_Fuente.Estado_Disponibilidad"
    COL_SOURCE_T_DATE_DOCUMENT_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_Fuente.Fecha_Documento_Fuente"
    COL_SOURCE_T_MAIN_TYPE_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_Fuente.Tipo_Principal"
    COL_PARTY_T_NAME_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_Interesado.Nombre"
    COL_POINT_T_ORIGINAL_LOCATION_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_Punto.Geometria"
    COL_POINT_T_PRODUCTION_METHOD_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_Punto.MetodoProduccion"
    COL_POINT_T_INTERPOLATION_POSITION_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_Punto.Posicion_Interpolacion"
    COL_RRR_T_DESCRIPTION_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_DRR.Descripcion"

    # "LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Area..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Construccion"  --> lc_construccion_area
    # "LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Area..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ServidumbreTransito"  --> lc_servidumbretransito_area
    # "LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Area..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Terreno"  --> lc_terreno_area
    # "LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Area..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion"  --> lc_unidadconstruccion_area
    COL_SPATIAL_UNIT_T_DIMENSION_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Dimension"
    COL_SPATIAL_UNIT_T_LABEL_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Etiqueta"
    COL_SPATIAL_UNIT_T_GEOMETRY_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Geometria"
    COL_SPATIAL_UNIT_T_SURFACE_RELATION_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie"
    # "LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Volumen..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion"  --> lc_unidadconstruccion_volumen
    # "LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Volumen..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Terreno"  --> lc_terreno_volumen
    # "LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Volumen..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Construccion"  --> lc_construccion_volumen
    # "LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Volumen..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ServidumbreTransito"  --> lc_servidumbretransito_volumen

    EXT_ARCHIVE_S_DATA_F = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Datos"
    EXT_ARCHIVE_S_EXTRACTION_F = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Extraccion"
    EXT_ARCHIVE_S_ACCEPTANCE_DATE_F = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Fecha_Aceptacion"
    EXT_ARCHIVE_S_DELIVERY_DATE_F = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Fecha_Entrega"
    EXT_ARCHIVE_S_STORAGE_DATE_F = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Fecha_Grabacion"
    EXT_ARCHIVE_S_NAMESPACE_F = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Espacio_De_Nombres"
    EXT_ARCHIVE_S_LOCAL_ID_F = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtArchivo.Local_Id"
    EXT_ADDRESS_S_VALUE_MAIN_ROAD_F = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Valor_Via_Principal"
    EXT_ADDRESS_S_PARCEL_NUMBER_F = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Numero_Predio"
    EXT_ADDRESS_S_LOCALIZATION_F = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Localizacion"
    EXT_ADDRESS_S_MAIN_ROAD_CLASS_F = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Clase_Via_Principal"
    EXT_ADDRESS_S_PARCEL_SECTOR_F = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Sector_Predio"
    EXT_ADDRESS_S_PARCEL_NAME_F = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Nombre_Predio"
    EXT_ADDRESS_S_IS_MAIN_ADDRESS_F = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Es_Direccion_Principal"
    EXT_ADDRESS_S_LETTER_GENERATOR_ROAD_F = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Letra_Via_Generadora"
    EXT_ADDRESS_S_VALUE_GENERATOR_ROAD_F = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Valor_Via_Generadora"
    EXT_ADDRESS_S_LETTER_MAIN_ROAD_F = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Letra_Via_Principal"
    EXT_ADDRESS_S_ADDRESS_TYPE_F = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Tipo_Direccion"
    EXT_ADDRESS_S_CITY_SECTOR_F = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Sector_Ciudad"
    EXT_ADDRESS_S_POSTAL_CODE_F = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Codigo_Postal"
    EXT_ADDRESS_S_COMPLEMENT_F = None  # "LADM_COL_V3_0.LADM_Nucleo.ExtDireccion.Complemento"

    # "LADM_COL_V3_0.LADM_Nucleo.ExtInteresado.Ext_Direccion_ID..LADM_COL_V3_0.LADM_Nucleo.ExtInteresado"  --> extinteresado_ext_direccion_id
    # "LADM_COL_V3_0.LADM_Nucleo.ExtInteresado.Firma..LADM_COL_V3_0.LADM_Nucleo.ExtInteresado"  --> extinteresado_firma
    # "LADM_COL_V3_0.LADM_Nucleo.ExtInteresado.Fotografia..LADM_COL_V3_0.LADM_Nucleo.ExtInteresado"  --> extinteresado_fotografia
    # "LADM_COL_V3_0.LADM_Nucleo.ExtInteresado.Huella_Dactilar..LADM_COL_V3_0.LADM_Nucleo.ExtInteresado"  --> extinteresado_huella_dactilar
    # "LADM_COL_V3_0.LADM_Nucleo.ExtInteresado.Documento_Escaneado"
    # "LADM_COL_V3_0.LADM_Nucleo.ExtInteresado.Nombre"
    # "LADM_COL_V3_0.LADM_Nucleo.ExtRedServiciosFisica.Ext_Interesado_Administrador_ID..LADM_COL_V3_0.LADM_Nucleo.ExtRedServiciosFisica"  --> extredserviciosfisica_ext_interesado_administrador_id
    # "LADM_COL_V3_0.LADM_Nucleo.ExtRedServiciosFisica.Orientada"
    # "LADM_COL_V3_0.LADM_Nucleo.ExtUnidadEdificacionFisica.Ext_Direccion_ID..LADM_COL_V3_0.LADM_Nucleo.ExtUnidadEdificacionFisica"  --> extunidadedificcnfsica_ext_direccion_id
    FRACTION_S_DENOMINATOR_F = None  # "LADM_COL_V3_0.LADM_Nucleo.Fraccion.Denominador"
    FRACTION_S_NUMERATOR_F = None  # "LADM_COL_V3_0.LADM_Nucleo.Fraccion.Numerador"
    # "LADM_COL_V3_0.LADM_Nucleo.Imagen.uri"
    # "LADM_COL_V3_0.LADM_Nucleo.COL_Transformacion.Localizacion_Transformada"
    # "LADM_COL_V3_0.LADM_Nucleo.COL_Transformacion.Transformacion..LADM_COL_V3_0.LADM_Nucleo.COL_Transformacion"  --> col_transformacion_transformacion
    # "LADM_COL_V3_0.LADM_Nucleo.COL_VolumenValor.Tipo"
    # "LADM_COL_V3_0.LADM_Nucleo.COL_VolumenValor.Volumen_Medicion"


    # "LADM_COL_V3_0.LADM_Nucleo.col_miembros.interesado..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_AgrupacionInteresados"  --> interesado_lc_agrupacioninteresados
    MEMBERS_T_GROUP_PARTY_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_miembros.agrupacion..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_AgrupacionInteresados"  --> agrupacion
    MEMBERS_T_PARTY_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_miembros.interesado..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Interesado"  --> interesado_lc_interesado
    FRACTION_S_MEMBER_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_miembros.participacion..LADM_COL_V3_0.LADM_Nucleo.col_miembros"  --> col_miembros_participacion
    FRACTION_S_COPROPERTY_COEFFICIENT_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.lc_predio_copropiedad.coeficiente..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.lc_predio_copropiedad"  --> lc_predio_copropiedad_coeficiente

    VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F = None  # "LADM_COL_V3_0.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version"
    VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F = None  # "LADM_COL_V3_0.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version"
    COL_POINT_SOURCE_T_SOURCE_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_puntoFuente.fuente_espacial..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_FuenteEspacial"  --> fuente_espacial
    # "LADM_COL_V3_0.LADM_Nucleo.col_relacionFuente.fuente_administrativa..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_FuenteAdministrativa"  --> fuente_administrativa
    # "LADM_COL_V3_0.LADM_Nucleo.col_relacionFuenteUespacial.fuente_espacial..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_FuenteEspacial"  --> fuente_espacial
    COL_RRR_SOURCE_T_SOURCE_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_rrrFuente.fuente_administrativa..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_FuenteAdministrativa"  --> fuente_administrativa
    COL_RRR_PARTY_T_LC_PARTY_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_rrrInteresado.interesado..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Interesado"  --> interesado_lc_interesado
    COL_RRR_PARTY_T_LC_GROUP_PARTY_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_rrrInteresado.interesado..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_AgrupacionInteresados"  --> interesado_lc_agrupacioninteresados

    COL_UE_BAUNIT_T_PARCEL_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_ueBaunit.baunit..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio"  --> baunit
    COL_UE_SOURCE_T_SOURCE_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_ueFuente.fuente_espacial..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_FuenteEspacial"  --> fuente_espacial
    # "LADM_COL_V3_0.LADM_Nucleo.col_unidadFuente.fuente_administrativa..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_FuenteAdministrativa"  --> fuente_administrativa
    # "LADM_COL_V3_0.LADM_Nucleo.col_unidadFuente.unidad..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio"  --> unidad

    LC_BUILDING_T_IDENTIFIER_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Construccion.Identificador"
    LC_BUILDING_T_NUMBER_OF_MEZZANINE_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ConstruBUILDING YEARccion.Numero_Mezanines"
    LC_BUILDING_T_NUMBER_OF_LOOKOUT_BASEMENT_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Construccion.Numero_Semisotanos"
    LC_BUILDING_T_NUMBER_OF_BASEMENT_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Construccion.Numero_Sotanos"
    LC_BUILDING_T_BUILDING_TYPE_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Construccion.Tipo_Construccion"
    LC_BUILDING_T_DOMAIN_TYPE_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Construccion.Tipo_Dominio"
    LC_BUILDING_T_BUILDING_AREA_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Construccion.Area_Construccion"
    LC_BUILDING_T_BUILDING_VALUATION_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Construccion.Avaluo_Construccion"
    LC_BUILDING_T_NUMBER_OF_FLOORS_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Construccion.Numero_Pisos"
    LC_BUILDING_T_HEIGHT_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Construccion.Altura"
    LC_BUILDING_T_YEAR_OF_BUILD_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Construccion.Anio_Construccion"
    LC_BUILDING_T_OBSERVATIONS_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Construccion.Observaciones"

    LC_RIGHT_T_DATE_START_TENANCY_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Derecho.Fecha_Inicio_Tenencia"
    LC_RIGHT_T_RIGHT_FRACTION_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Derecho.Fraccion_Derecho"
    LC_RIGHT_T_TYPE_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Derecho.Tipo"

    LC_ADMINISTRATIVE_SOURCE_T_EMITTING_ENTITY_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_FuenteAdministrativa.Ente_Emisor"
    LC_ADMINISTRATIVE_SOURCE_T_TYPE_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_FuenteAdministrativa.Tipo"

    LC_PARTY_CONTACT_T_ALLOW_MAIL_NOTIFICATION_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_InteresadoContacto.Autoriza_Notificacion_Correo"
    LC_PARTY_CONTACT_T_EMAIL_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_InteresadoContacto.Correo_Electronico"
    LC_PARTY_CONTACT_T_NOTIFICATION_ADDRESS_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_InteresadoContacto.Domicilio_Notificacion"
    LC_PARTY_CONTACT_T_LC_PARTY_F = None # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.lc_interesado_interesadocontacto.lc_interesado..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Interesado"  --> lc_interesado
    LC_PARTY_CONTACT_T_TELEPHONE_NUMBER_1_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_InteresadoContacto.Telefono1"
    LC_PARTY_CONTACT_T_TELEPHONE_NUMBER_2_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_InteresadoContacto.Telefono2"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_InteresadoContacto.Corregimiento"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_InteresadoContacto.Departamento"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_InteresadoContacto.Direccion_Residencia"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_InteresadoContacto.Municipio"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_InteresadoContacto.Vereda"

    LC_PARTY_T_DOCUMENT_ID_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Interesado.Documento_Identidad"
    LC_PARTY_T_ETHNIC_GROUP_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Interesado.Grupo_Etnico"
    LC_PARTY_T_SURNAME_1_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Interesado.Primer_Apellido"
    LC_PARTY_T_FIRST_NAME_1_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Interesado.Primer_Nombre"
    LC_PARTY_T_BUSINESS_NAME_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Interesado.Razon_Social"
    LC_PARTY_T_SURNAME_2_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Interesado.Segundo_Apellido"
    LC_PARTY_T_FIRST_NAME_2_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Interesado.Segundo_Nombre"
    LC_PARTY_T_GENRE_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Interesado.Sexo"
    LC_PARTY_T_TYPE_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Interesado.Tipo"
    LC_PARTY_T_DOCUMENT_TYPE_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Interesado.Tipo_Documento"

    LC_BOUNDARY_T_LENGTH_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Lindero.Longitud"

    LC_PARCEL_T_VALUATION_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio.Avaluo_Catastral"
    LC_PARCEL_T_ORIP_CODE_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio.Codigo_ORIP"
    LC_PARCEL_T_PARCEL_TYPE_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio.Condicion_Predio"
    LC_COPROPERTY_T_COPROPERTY_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.lc_predio_copropiedad.copropiedad..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio"  --> copropiedad
    LC_COPROPERTY_T_PARCEL_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.lc_predio_copropiedad.predio..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio"  --> predio
    LC_PARCEL_T_DEPARTMENT_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio.Departamento"
    LC_PARCEL_T_ADDRESS_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio.Direccion..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio"  --> lc_predio_direccion

    # "Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos.INI_PredioInsumos.Observaciones"
    # "Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos.INI_PredioInsumos.Tipo_Emparejamiento"
    # "Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos.ini_predio_integracion_gc.gc_predio_catastro..Submodelo_Insumos_Gestor_Catastral_V1_0.Datos_Gestor_Catastral.GC_PredioCatastro" --> gc_predio_catastro
    # "Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos.ini_predio_integracion_snr.snr_predio_juridico..Submodelo_Insumos_SNR_V1_0.Datos_SNR.SNR_PredioRegistro"  --> snr_predio_juridico
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.lc_predio_ini_predioinsumos.ini_predio_insumos..Submodelo_Integracion_Insumos_V1_0.Datos_Integracion_Insumos.INI_PredioInsumos"  --> ini_predio_insumos
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.lc_predio_ini_predioinsumos.lc_predio..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio"  --> lc_predio

    LC_PARCEL_T_FMI_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio.Matricula_Inmobiliaria"
    LC_PARCEL_T_MUNICIPALITY_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio.Municipio"
    LC_PARCEL_T_PARCEL_NUMBER_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio.Numero_Predial"
    LC_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio.Numero_Predial_Anterior"
    LC_PARCEL_T_ID_OPERATION_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio.Id_Operacion"
    LC_PARCEL_T_NUPRE_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio.NUPRE"
    LC_PARCEL_T_TYPE_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio.Tipo"
    LC_PARCEL_T_HAS_FMI_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio.Tiene_FMI"

    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ContactoVisita.Autoriza_Notificaciones"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ContactoVisita.Celular"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ContactoVisita.Correo_Electronico"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ContactoVisita.Domicilio_Notificaciones"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ContactoVisita.Numero_Documento_Quien_Atendio"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ContactoVisita.Primer_Apellido_Quien_Atendio"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ContactoVisita.Primer_Nombre_Quien_Atendio"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ContactoVisita.Relacion_Con_Predio"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ContactoVisita.Segundo_Apellido_Quien_Atendio"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ContactoVisita.Segundo_Nombre_Quien_Atendio"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ContactoVisita.Tipo_Documento_Quien_Atendio"

    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosAdicionalesLevantamientoCatastral.Area_Registral_M2"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosAdicionalesLevantamientoCatastral.Categoria_Suelo"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosAdicionalesLevantamientoCatastral.Clase_Suelo"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosAdicionalesLevantamientoCatastral.Destinacion_Economica"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosAdicionalesLevantamientoCatastral.Fecha_Visita_predial"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosAdicionalesLevantamientoCatastral.Numero_Documento_Reconocedor"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosAdicionalesLevantamientoCatastral.Observaciones"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosAdicionalesLevantamientoCatastral.Primer_Apellido_Reconocedor"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosAdicionalesLevantamientoCatastral.Primer_Nombre_Reconocedor"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosAdicionalesLevantamientoCatastral.Procedimiento_Catastral_Registral"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosAdicionalesLevantamientoCatastral.Resultado_Visita"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosAdicionalesLevantamientoCatastral.Segundo_Apellido_Reconocedor"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosAdicionalesLevantamientoCatastral.Segundo_Nombre_Reconocedor"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosAdicionalesLevantamientoCatastral.Suscribe_Acta_Colindancia"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosAdicionalesLevantamientoCatastral.Tiene_Area_Registral"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosAdicionalesLevantamientoCatastral.Tipo_Documento_Reconocedor"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosAdicionalesLevantamientoCatastral.Novedad_FMI..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosAdicionalesLevantamientoCatastral"  --> lc_dtsdcnlstmntctstral_novedad_fmi
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosAdicionalesLevantamientoCatastral.Novedad_Numeros_Prediales..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosAdicionalesLevantamientoCatastral"  --> lc_dtsdcnlstmntctstral_novedad_numeros_prediales

    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosPHCondominio.Area_Total_Construida"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosPHCondominio.Area_Total_Construida_Comun"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosPHCondominio.Area_Total_Construida_Privada"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosPHCondominio.Area_Total_Terreno"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosPHCondominio.Area_Total_Terreno_Comun"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosPHCondominio.Area_Total_Terreno_Privada"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosPHCondominio.Numero_Torres"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosPHCondominio.Total_Unidades_Privadas"

    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_EstructuraNovedadFMI.Codigo_ORIP"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_EstructuraNovedadFMI.Numero_FMI"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_EstructuraNovedadNumeroPredial.Numero_Predial"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_EstructuraNovedadNumeroPredial.Tipo_Novedad"

    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_OfertasMercadoInmobiliario.Fecha_Captura_Oferta"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_OfertasMercadoInmobiliario.Nombre_Oferente"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_OfertasMercadoInmobiliario.Numero_Contacto_Oferente"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_OfertasMercadoInmobiliario.Tiempo_Oferta_Mercado"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_OfertasMercadoInmobiliario.Tipo_Oferta"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_OfertasMercadoInmobiliario.Valor_Negociado"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_OfertasMercadoInmobiliario.Valor_Pedido"

    LC_CONTROL_POINT_T_HORIZONTAL_ACCURACY_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoControl.Exactitud_Horizontal"
    LC_CONTROL_POINT_T_VERTICAL_ACCURACY_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoControl.Exactitud_Vertical"
    LC_CONTROL_POINT_T_ID_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoControl.ID_Punto_Control"
    LC_CONTROL_POINT_T_POINT_TYPE_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoControl.PuntoTipo"
    LC_CONTROL_POINT_T_CONTROL_POINT_TYPE_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoControl.Tipo_Punto_Control"

    LC_SURVEY_POINT_T_HORIZONTAL_ACCURACY_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoLevantamiento.Exactitud_Horizontal"
    LC_SURVEY_POINT_T_VERTICAL_ACCURACY_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoLevantamiento.Exactitud_Vertical"
    LC_SURVEY_POINT_T_PHOTO_IDENTIFICATION_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoLevantamiento.Fotoidentificacion"
    LC_SURVEY_POINT_T_ID_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoLevantamiento.ID_Punto_Levantamiento"
    LC_SURVEY_POINT_T_POINT_TYPE_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoLevantamiento.PuntoTipo"
    LC_SURVEY_POINT_T_SURVEY_POINT_TYPE_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoLevantamiento.Tipo_Punto_Levantamiento"

    LC_BOUNDARY_POINT_T_AGREEMENT_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoLindero.Acuerdo"
    LC_BOUNDARY_POINT_T_HORIZONTAL_ACCURACY_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoLindero.Exactitud_Horizontal"
    LC_BOUNDARY_POINT_T_VERTICAL_ACCURACY_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoLindero.Exactitud_Vertical"
    LC_BOUNDARY_POINT_T_PHOTO_IDENTIFICATION_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoLindero.Fotoidentificacion"
    LC_BOUNDARY_POINT_T_ID_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoLindero.ID_Punto_Lindero"
    LC_BOUNDARY_POINT_T_POINT_TYPE_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoLindero.PuntoTipo"

    LC_RESTRICTION_T_TYPE_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Restriccion.Tipo"
    LC_RIGHT_OF_WAY_T_RIGHT_OF_WAY_AREA_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ServidumbreTransito.Area_Servidumbre"

    LC_PLOT_T_PLOT_AREA_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Terreno.Area_Terreno"
    LC_PLOT_T_PLOT_VALUATION_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Terreno.Avaluo_Terreno"
    LC_PLOT_T_GEOMETRY_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Terreno.Geometria"
    LC_PLOT_T_BLOCK_RURAL_DIVISION_CODE_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Terreno.Manzana_Vereda_Codigo"

    LC_BUILDING_UNIT_T_BUILT_AREA_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion.Area_Construida"
    LC_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion.Area_Privada_Construida"
    LC_BUILDING_UNIT_T_BUILDING_UNIT_VALUATION_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion.Avaluo_Unidad_Construccion"
    LC_BUILDING_UNIT_T_IDENTIFICATION_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion.Identificador"
    LC_BUILDING_UNIT_T_FLOOR_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion.Planta_Ubicacion"
    LC_BUILDING_UNIT_T_TOTAL_FLOORS_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion.Total_Pisos"
    LC_BUILDING_UNIT_T_USE_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion.Uso"
    LC_BUILDING_UNIT_T_YEAR_OF_BUILDING_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion.Anio_Construccion"
    LC_BUILDING_UNIT_T_OBSERVATIONS_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion.Observaciones"
    LC_BUILDING_UNIT_T_BUILDING_TYPE_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion.Tipo_Construccion"
    LC_BUILDING_UNIT_T_DOMAIN_TYPE_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion.Tipo_Dominio"
    LC_BUILDING_UNIT_T_FLOOR_TYPE_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion.Tipo_Planta"
    LC_BUILDING_UNIT_T_BUILDING_UNIT_TYPE_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion.Tipo_Unidad_Construccion"
    LC_BUILDING_UNIT_T_TOTAL_BATHROOMS_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion.Total_Banios"
    LC_BUILDING_UNIT_T_TOTAL_ROOMS_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion.Total_Habitaciones"
    LC_BUILDING_UNIT_T_TOTAL_LOCALS_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion.Total_Locales"
    LC_BUILDING_UNIT_T_HEIGHT_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion.Altura"
    LC_BUILDING_UNIT_T_BUILDING_F = None  # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.lc_construccion_unidadconstruccion.lc_construccion..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Construccion"  --> lc_construccion
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_TipologiaConstruccion.Tipo_Tipologia"

    # Composed keys (when ilinames are duplicated because their target table is different, we
    # concatenate in the form "{key}_{target}")

    # "LADM_COL_V3_0.LADM_Nucleo.col_puntoReferencia.ue..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Construccion"  --> ue_lc_construccion
    # "LADM_COL_V3_0.LADM_Nucleo.col_puntoReferencia.ue..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ServidumbreTransito"  --> ue_lc_servidumbretransito
    # "LADM_COL_V3_0.LADM_Nucleo.col_puntoReferencia.ue..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Terreno"  --> ue_lc_terreno
    # "LADM_COL_V3_0.LADM_Nucleo.col_puntoReferencia.ue..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion"  --> ue_lc_unidadconstruccion

    # "LADM_COL_V3_0.LADM_Nucleo.col_baunitComoInteresado.unidad..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio"  --> unidad
    # "LADM_COL_V3_0.LADM_Nucleo.col_baunitComoInteresado.interesado..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_AgrupacionInteresados"  --> interesado_lc_agrupacioninteresados
    # "LADM_COL_V3_0.LADM_Nucleo.col_baunitComoInteresado.interesado..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Interesado"  --> interesado_lc_interesado
    EXT_ARCHIVE_S_LC_ADMINISTRATIVE_SOURCE_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_FuenteAdministrativa"  --> lc_fuenteadministrtiva_ext_archivo_id
    EXT_ARCHIVE_S_LC_SPATIAL_SOURCE_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_FuenteEspacial"  --> lc_fuenteespacial_ext_archivo_id
    # "LADM_COL_V3_0.LADM_Nucleo.COL_Interesado.ext_PID..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_AgrupacionInteresados"  --> lc_agrupacionintersdos_ext_pid
    # "LADM_COL_V3_0.LADM_Nucleo.COL_Interesado.ext_PID..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Interesado"  --> lc_interesado_ext_pid
    # "LADM_COL_V3_0.LADM_Nucleo.COL_Punto.Transformacion_Y_Resultado..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoControl"  --> lc_puntocontrol_transformacion_y_resultado
    # "LADM_COL_V3_0.LADM_Nucleo.COL_Punto.Transformacion_Y_Resultado..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoLevantamiento"  --> lc_puntolevantamiento_transformacion_y_resultado
    # "LADM_COL_V3_0.LADM_Nucleo.COL_Punto.Transformacion_Y_Resultado..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoLindero"  --> lc_puntolindero_transformacion_y_resultado

    EXT_ADDRESS_S_LC_BUILDING_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Construccion"  --> lc_construccion_ext_direccion_id
    EXT_ADDRESS_S_LC_RIGHT_OF_WAY_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ServidumbreTransito"  --> lc_servidumbretransito_ext_direccion_id
    EXT_ADDRESS_S_LC_PLOT_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Terreno"  --> lc_terreno_ext_direccion_id
    EXT_ADDRESS_S_LC_BUILDING_UNIT_F = None  # "LADM_COL_V3_0.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion"  --> lc_unidadconstruccion_ext_direccion_id
    MORE_BFS_T_LC_BOUNDARY_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_masCcl.ccl_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Lindero"  --> ccl_mas
    MORE_BFS_T_LC_BUILDING_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_masCcl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Construccion"  --> ue_mas_lc_construccion
    MORE_BFS_T_LC_RIGHT_OF_WAY_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_masCcl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ServidumbreTransito"  --> ue_mas_lc_servidumbretransito
    MORE_BFS_T_LC_PLOT_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_masCcl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Terreno"  --> ue_mas_lc_terreno
    MORE_BFS_T_LC_BUILDING_UNIT_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_masCcl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion"  --> ue_mas_lc_unidadconstruccion

    # "LADM_COL_V3_0.LADM_Nucleo.col_masCl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Construccion"  --> ue_mas_lc_construccion
    # "LADM_COL_V3_0.LADM_Nucleo.col_masCl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ServidumbreTransito"  --> ue_mas_lc_servidumbretransito
    # "LADM_COL_V3_0.LADM_Nucleo.col_masCl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Terreno"  --> ue_mas_lc_terreno
    # "LADM_COL_V3_0.LADM_Nucleo.col_masCl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion"  --> ue_mas_lc_unidadconstruccion

    LESS_BFS_T_LC_BOUNDARY_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_menosCcl.ccl_menos..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Lindero"  --> ccl_menos
    LESS_BFS_T_LC_BUILDING_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_menosCcl.ue_menos..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Construccion"  --> ue_menos_lc_construccion
    LESS_BFS_T_LC_RIGHT_OF_WAY_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_menosCcl.ue_menos..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ServidumbreTransito"  --> ue_menos_lc_servidumbretransito
    LESS_BFS_T_LC_PLOT_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_menosCcl.ue_menos..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Terreno"  --> ue_menos_lc_terreno
    LESS_BFS_T_LC_BUILDING_UNIT_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_menosCcl.ue_menos..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion"  --> ue_menos_lc_unidadconstruccion

    # "LADM_COL_V3_0.LADM_Nucleo.col_menosCl.ue_menos..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Construccion"  --> ue_menos_lc_construccion
    # "LADM_COL_V3_0.LADM_Nucleo.col_menosCl.ue_menos..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ServidumbreTransito"  --> ue_menos_lc_servidumbretransito
    # "LADM_COL_V3_0.LADM_Nucleo.col_menosCl.ue_menos..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Terreno"  --> ue_menos_lc_terreno
    # "LADM_COL_V3_0.LADM_Nucleo.col_menosCl.ue_menos..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion"  --> ue_menos_lc_unidadconstruccion

    POINT_BFS_T_LC_BOUNDARY_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_puntoCcl.ccl..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Lindero"  --> ccl
    POINT_BFS_T_LC_CONTROL_POINT_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_puntoCcl.punto..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoControl"  --> punto_lc_puntocontrol
    POINT_BFS_T_LC_SURVEY_POINT_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_puntoCcl.punto..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoLevantamiento"  --> punto_lc_puntolevantamiento
    POINT_BFS_T_LC_BOUNDARY_POINT_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_puntoCcl.punto..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoLindero"  --> punto_lc_puntolindero
    # "LADM_COL_V3_0.LADM_Nucleo.col_puntoCl.punto..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoControl"  --> punto_lc_puntocontrol
    # "LADM_COL_V3_0.LADM_Nucleo.col_puntoCl.punto..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoLevantamiento"  --> punto_lc_puntolevantamiento
    # "LADM_COL_V3_0.LADM_Nucleo.col_puntoCl.punto..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoLindero"  --> punto_lc_puntolindero
    COL_POINT_SOURCE_T_LC_CONTROL_POINT_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_puntoFuente.punto..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoControl"  --> punto_lc_puntocontrol
    COL_POINT_SOURCE_T_LC_SURVEY_POINT_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_puntoFuente.punto..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoLevantamiento"  --> punto_lc_puntolevantamiento
    COL_POINT_SOURCE_T_LC_BOUNDARY_POINT_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_puntoFuente.punto..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_PuntoLindero"  --> punto_lc_puntolindero
    # "LADM_COL_V3_0.LADM_Nucleo.col_responsableFuente.fuente_administrativa..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_FuenteAdministrativa"  --> fuente_administrativa
    # "LADM_COL_V3_0.LADM_Nucleo.col_responsableFuente.interesado..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_AgrupacionInteresados"  --> interesado_lc_agrupacioninteresados
    # "LADM_COL_V3_0.LADM_Nucleo.col_responsableFuente.interesado..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Interesado"  --> interesado_lc_interesado
    COL_RRR_SOURCE_T_LC_RIGHT_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_rrrFuente.rrr..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Derecho"  --> rrr_lc_derecho
    COL_RRR_SOURCE_T_LC_RESTRICTION_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_rrrFuente.rrr..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Restriccion"  --> rrr_lc_restriccion

    # "LADM_COL_V3_0.LADM_Nucleo.col_topografoFuente.fuente_espacial..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_FuenteEspacial"  --> fuente_espacial
    # "LADM_COL_V3_0.LADM_Nucleo.col_topografoFuente.topografo..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Interesado"  --> topografo_lc_interesado
    # "LADM_COL_V3_0.LADM_Nucleo.col_topografoFuente.topografo..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_AgrupacionInteresados"  --> topografo_lc_agrupacioninteresados

    COL_UE_BAUNIT_T_LC_PLOT_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_ueBaunit.ue..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Terreno"  --> ue_lc_terreno
    COL_UE_BAUNIT_T_LC_BUILDING_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_ueBaunit.ue..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Construccion"  --> ue_lc_construccion
    COL_UE_BAUNIT_T_LC_BUILDING_UNIT_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_ueBaunit.ue..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion"  --> ue_lc_unidadconstruccion
    COL_UE_BAUNIT_T_LC_RIGHT_OF_WAY_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_ueBaunit.ue..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ServidumbreTransito"  --> ue_lc_servidumbretransito

    COL_UE_SOURCE_T_LC_BUILDING_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_ueFuente.ue..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Construccion"  --> ue_lc_construccion
    COL_UE_SOURCE_T_LC_RIGHT_OF_WAY_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_ueFuente.ue..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ServidumbreTransito"  --> ue_lc_servidumbretransito
    COL_UE_SOURCE_T_LC_PLOT_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_ueFuente.ue..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Terreno"  --> ue_lc_terreno
    COL_UE_SOURCE_T_LC_BUILDING_UNIT_F = None  # "LADM_COL_V3_0.LADM_Nucleo.col_ueFuente.ue..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion"  --> ue_lc_unidadconstruccion

    # "LADM_COL_V3_0.LADM_Nucleo.col_ueUeGrupo.parte..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Construccion"  --> parte_lc_construccion
    # "LADM_COL_V3_0.LADM_Nucleo.col_ueUeGrupo.parte..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ServidumbreTransito"  --> parte_lc_servidumbretransito
    # "LADM_COL_V3_0.LADM_Nucleo.col_ueUeGrupo.parte..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Terreno"  --> parte_lc_terreno
    # "LADM_COL_V3_0.LADM_Nucleo.col_ueUeGrupo.parte..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion"  --> parte_lc_unidadconstruccion

    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_CalificacionConvencional.Tipo_Calificar"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_CalificacionConvencional.Total_Calificacion"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_CalificacionNoConvencional.Tipo_Anexo"

    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_GrupoCalificacion.Clase_Calificacion"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_GrupoCalificacion.Conservacion"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_GrupoCalificacion.Subtotal"

    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ObjetoConstruccion.Puntos"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_ObjetoConstruccion.Tipo_Objeto_Construccion"

    # "LADM_COL_V3_0.LADM_Nucleo.col_clFuente.fuente_espacial..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_FuenteEspacial"  --> fuente_espacial
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.lc_calificacion_unidadconstruccion.lc_unidad_construccion..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_UnidadConstruccion"  --> lc_unidad_construccion
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.lc_grupo_calificacionconvencional.lc_calificacion_convencional..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_CalificacionConvencional"  --> lc_calificacion_convencional
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.lc_informacion_adicional_contacto.lc_datos_adicionales..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_DatosAdicionalesLevantamientoCatastral"
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.lc_informacion_adicional_predio.lc_predio..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio"  --> lc_predio
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.lc_objetoconstruccion_grupocalificacion.lc_grupo_calificacion..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_GrupoCalificacion"  --> lc_grupo_calificacion
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.lc_ph_predio.lc_predio..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio"  --> lc_predio
    # "Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.lc_predio_ofertas_mercado_inmobiliario.lc_predio..Modelo_Aplicacion_LADMCOL_Lev_Cat_V1_0.Levantamiento_Catastral.LC_Predio"  --> lc_predio

    OID_T_NAMESPACE_F = None  # "LADM_COL_V3_0.LADM_Nucleo.Oid.Espacio_De_Nombres"
    OID_T_LOCAL_ID_F = None  # "LADM_COL_V3_0.LADM_Nucleo.Oid.Local_Id"

    TABLE_DICT = {
        "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Barrio": {VARIABLE_NAME: "GC_NEIGHBOURHOOD_T", FIELDS_DICT: {}},
        "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Construccion": {VARIABLE_NAME: "GC_BUILDING_T", FIELDS_DICT: {}},
        "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_DatosPHCondominio": {VARIABLE_NAME: "GC_HP_CONDOMINIUM_DATA_T", FIELDS_DICT: {}},
        "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.gc_copropiedad": {VARIABLE_NAME: "GC_COPROPERTY_T", FIELDS_DICT: {}},
        "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_DatosTorrePH": {VARIABLE_NAME: "GC_HP_TOWER_DATA_T", FIELDS_DICT: {}},
        "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_EstadoPredio": {VARIABLE_NAME: "GC_PARCEL_STATUS_T", FIELDS_DICT: {}},
        "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Manzana": {VARIABLE_NAME: "GC_BLOCK_T", FIELDS_DICT: {}},
        "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Perimetro": {VARIABLE_NAME: "GC_PERIMETER_T", FIELDS_DICT: {}},
        "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro": {VARIABLE_NAME: "GC_PARCEL_T", FIELDS_DICT: {
            "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Circulo_Registral": "GC_PARCEL_T_REGISTRY_OFFICE_F",
            "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Condicion_Predio": "GC_PARCEL_T_CONDITION_F",
            "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Destinacion_Economica": "GC_PARCEL_T_ECONOMIC_DESTINATION_F",
            "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Fecha_Datos": "GC_PARCEL_T_DATE_OF_DATA_F",
            "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Matricula_Inmobiliaria_Catastro": "GC_PARCEL_T_FMI_F",
            "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Numero_Predial": "GC_PARCEL_T_PARCEL_NUMBER_F",
            "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Numero_Predial_Anterior": "GC_PARCEL_T_PARCEL_NUMBER_BEFORE_F",
            "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.NUPRE": "GC_PARCEL_T_NUPRE_F",
            "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Sistema_Procedencia_Datos": "GC_PARCEL_T_DATA_SOURCE_F",
            "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Tipo_Catastro": "GC_PARCEL_T_CADASTRAL_TYPE_F",
            "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro.Tipo_Predio": "GC_PARCEL_T_PARCEL_TYPE_F"
        }},
        "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario": {VARIABLE_NAME: "GC_OWNER_T", FIELDS_DICT: {
            "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario.Digito_Verificacion": "GC_OWNER_T_VERIFICATION_DIGIT",
            "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario.Numero_Documento": "GC_OWNER_T_DOCUMENT_ID_F",
            "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.gc_propietario_predio.gc_predio_catastro..Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro": "GC_OWNER_T_PARCEL_ID_F",
            "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario.Primer_Apellido": "GC_OWNER_T_SURNAME_1_F",
            "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario.Primer_Nombre": "GC_OWNER_T_FIRST_NAME_1_F",
            "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario.Razon_Social": "GC_OWNER_T_BUSINESS_NAME_F",
            "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario.Segundo_Apellido": "GC_OWNER_T_SURNAME_2_F",
            "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario.Segundo_Nombre": "GC_OWNER_T_FIRST_NAME_2_F",
            "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Propietario.Tipo_Documento": "GC_OWNER_T_DOCUMENT_TYPE_F",
        }},
        "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_SectorRural": {VARIABLE_NAME: "GC_RURAL_SECTOR_T", FIELDS_DICT: {}},
        "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_SectorUrbano": {VARIABLE_NAME: "GC_URBAN_SECTOR_T", FIELDS_DICT: {}},
        "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno": {VARIABLE_NAME: "GC_PLOT_T", FIELDS_DICT: {
            "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.gc_terreno_predio.gc_predio..Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_PredioCatastro": "GC_PLOT_T_GC_PARCEL_F",
            "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Digital": "GC_PLOT_T_DIGITAL_PLOT_AREA_F",
            "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Terreno.Area_Terreno_Alfanumerica": "GC_PLOT_T_ALPHANUMERIC_AREA_F"
        }},
        "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_UnidadConstruccion": {VARIABLE_NAME: "GC_BUILDING_UNIT_T", FIELDS_DICT: {}},
        "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Vereda": {VARIABLE_NAME: "GC_RURAL_DIVISION_T", FIELDS_DICT: {}},
        "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_ComisionesConstruccion": {VARIABLE_NAME: "GC_COMMISSION_BUILDING_T", FIELDS_DICT: {}},
        "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_ComisionesTerreno": {VARIABLE_NAME: "GC_COMMISSION_PLOT_T", FIELDS_DICT: {}},
        "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_ComisionesUnidadConstruccion": {VARIABLE_NAME: "GC_COMMISSION_BUILDING_UNIT_T", FIELDS_DICT: {}},
        "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_CalificacionUnidadConstruccion": {VARIABLE_NAME: "GC_QUALIFICATION_BUILDING_UNIT_T", FIELDS_DICT: {}},
        
        "Submodelo_Insumos_Gestor_Catastral.GC_CondicionPredioTipo": {VARIABLE_NAME: "GC_PARCEL_TYPE_D", FIELDS_DICT: {}},
        "Submodelo_Insumos_Gestor_Catastral.Datos_Gestor_Catastral.GC_Direccion": {VARIABLE_NAME: "GC_ADDRESS_T", FIELDS_DICT: {}},
        "Submodelo_Insumos_Gestor_Catastral.GC_UnidadConstruccionTipo": {VARIABLE_NAME: "GC_BUILDING_UNIT_TYPE_T", FIELDS_DICT: {}},
        "Submodelo_Integracion_Insumos.Datos_Integracion_Insumos.INI_PredioInsumos": {VARIABLE_NAME: "INI_PARCEL_SUPPLIES_T", FIELDS_DICT: {}},
        "Submodelo_Insumos_SNR.Datos_SNR.SNR_Derecho": {VARIABLE_NAME: "SNR_RIGHT_T", FIELDS_DICT: {}},
        "Submodelo_Insumos_SNR.Datos_SNR.SNR_FuenteCabidaLinderos": {VARIABLE_NAME: "SNR_SOURCE_BOUNDARIES_T", FIELDS_DICT: {}},
        "Submodelo_Insumos_SNR.Datos_SNR.SNR_FuenteDerecho": {VARIABLE_NAME: "SNR_SOURCE_RIGHT_T", FIELDS_DICT: {}},
        "Submodelo_Insumos_SNR.Datos_SNR.SNR_PredioRegistro": {VARIABLE_NAME: "SNR_PARCEL_REGISTRY_T", FIELDS_DICT: {
            "Submodelo_Insumos_SNR.Datos_SNR.SNR_PredioRegistro.Numero_Predial_Nuevo_en_FMI": "SNR_PARCEL_REGISTRY_T_NEW_PARCEL_NUMBER_IN_FMI_F"
        }},
        "Submodelo_Insumos_SNR.Datos_SNR.SNR_Titular": {VARIABLE_NAME: "SNR_TITLE_HOLDER_T", FIELDS_DICT: {}},
        "Submodelo_Insumos_SNR.SNR_CalidadDerechoTipo": {VARIABLE_NAME: "SNR_RIGHT_TYPE_D", FIELDS_DICT: {}},
        "Submodelo_Insumos_SNR.SNR_DocumentoTitularTipo": {VARIABLE_NAME: "SNR_TITLE_HOLDER_DOCUMENT_T", FIELDS_DICT: {}},
        "Submodelo_Insumos_SNR.SNR_FuenteTipo": {VARIABLE_NAME: "SNR_SOURCE_TYPE_D", FIELDS_DICT: {}},
        "Submodelo_Insumos_SNR.SNR_PersonaTitularTipo": {VARIABLE_NAME: "SNR_TITLE_HOLDER_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.COL_EstadoDisponibilidadTipo": {VARIABLE_NAME: "COL_AVAILABILITY_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.CI_Forma_Presentacion_Codigo": {VARIABLE_NAME: "CI_CODE_PRESENTATION_FORM_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.COL_FuenteAdministrativaTipo": {VARIABLE_NAME: "COL_ADMINISTRATIVE_SOURCE_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.COL_FuenteEspacialTipo": {VARIABLE_NAME: "COL_SPATIAL_SOURCE_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.COL_GrupoInteresadoTipo": {VARIABLE_NAME: "COL_GROUP_PARTY_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.COL_InterpolacionTipo": {VARIABLE_NAME: "COL_INTERPOLATION_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.COL_MetodoProduccionTipo": {VARIABLE_NAME: "COL_PRODUCTION_METHOD_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.COL_RelacionSuperficieTipo": {VARIABLE_NAME: "COL_SURFACE_RELATION_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.ExtArchivo": {VARIABLE_NAME: "EXT_ARCHIVE_S", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.ExtArchivo.Datos": "EXT_ARCHIVE_S_DATA_F",
            "LADM_COL.LADM_Nucleo.ExtArchivo.Extraccion": "EXT_ARCHIVE_S_EXTRACTION_F",
            "LADM_COL.LADM_Nucleo.ExtArchivo.Fecha_Aceptacion": "EXT_ARCHIVE_S_ACCEPTANCE_DATE_F",
            "LADM_COL.LADM_Nucleo.ExtArchivo.Fecha_Entrega": "EXT_ARCHIVE_S_DELIVERY_DATE_F",
            "LADM_COL.LADM_Nucleo.ExtArchivo.Fecha_Grabacion": "EXT_ARCHIVE_S_STORAGE_DATE_F",
            "LADM_COL.LADM_Nucleo.ExtArchivo.Espacio_De_Nombres": "EXT_ARCHIVE_S_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.ExtArchivo.Local_Id": "EXT_ARCHIVE_S_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_FuenteAdministrativa": "EXT_ARCHIVE_S_LC_ADMINISTRATIVE_SOURCE_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Ext_Archivo_ID..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_FuenteEspacial": "EXT_ARCHIVE_S_LC_SPATIAL_SOURCE_F"
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
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Construccion": "EXT_ADDRESS_S_LC_BUILDING_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_ServidumbreTransito": "EXT_ADDRESS_S_LC_RIGHT_OF_WAY_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Terreno": "EXT_ADDRESS_S_LC_PLOT_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Ext_Direccion_ID..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion": "EXT_ADDRESS_S_LC_BUILDING_UNIT_F"
        }},
        "LADM_COL.LADM_Nucleo.ExtDireccion.Tipo_Direccion": {VARIABLE_NAME: "EXT_ADDRESS_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.ExtDireccion.Clase_Via_Principal": {VARIABLE_NAME: "EXT_ADDRESS_TYPE_MAIN_ROAD_CLASS_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.ExtDireccion.Sector_Ciudad": {VARIABLE_NAME: "EXT_ADDRESS_TYPE_CITY_SECTOR_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.ExtDireccion.Sector_Predio": {VARIABLE_NAME: "EXT_ADDRESS_TYPE_PARCEL_SECTOR_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.ExtInteresado": {VARIABLE_NAME: "EXT_PARTY_S", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.Fraccion": {VARIABLE_NAME: "FRACTION_S", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.Fraccion.Denominador": "FRACTION_S_DENOMINATOR_F",
            "LADM_COL.LADM_Nucleo.Fraccion.Numerador": "FRACTION_S_NUMERATOR_F"
        }},
        "LADM_COL.LADM_Nucleo.COL_UnidadAdministrativaBasicaTipo": {VARIABLE_NAME: "COL_BAUNIT_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.COL_DimensionTipo": {VARIABLE_NAME: "COL_DIMENSION_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.COL_PuntoTipo": {VARIABLE_NAME: "COL_POINT_TYPE_D", FIELDS_DICT: {}},
        "LADM_COL.LADM_Nucleo.col_masCcl": {VARIABLE_NAME: "MORE_BFS_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_masCcl.ccl_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Lindero": "MORE_BFS_T_LC_BOUNDARY_F",
            "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Construccion": "MORE_BFS_T_LC_BUILDING_F",
            "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_ServidumbreTransito": "MORE_BFS_T_LC_RIGHT_OF_WAY_F",
            "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Terreno": "MORE_BFS_T_LC_PLOT_F",
            "LADM_COL.LADM_Nucleo.col_masCcl.ue_mas..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion": "MORE_BFS_T_LC_BUILDING_UNIT_F"
        }},
        "LADM_COL.LADM_Nucleo.col_menosCcl": {VARIABLE_NAME: "LESS_BFS_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_menosCcl.ccl_menos..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Lindero": "LESS_BFS_T_LC_BOUNDARY_F",
            "LADM_COL.LADM_Nucleo.col_menosCcl.ue_menos..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Construccion": "LESS_BFS_T_LC_BUILDING_F",
            "LADM_COL.LADM_Nucleo.col_menosCcl.ue_menos..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_ServidumbreTransito": "LESS_BFS_T_LC_RIGHT_OF_WAY_F",
            "LADM_COL.LADM_Nucleo.col_menosCcl.ue_menos..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Terreno": "LESS_BFS_T_LC_PLOT_F",
            "LADM_COL.LADM_Nucleo.col_menosCcl.ue_menos..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion": "LESS_BFS_T_LC_BUILDING_UNIT_F",
        }},
        "LADM_COL.LADM_Nucleo.col_miembros": {VARIABLE_NAME: "MEMBERS_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_miembros.participacion..LADM_COL.LADM_Nucleo.col_miembros": "FRACTION_S_MEMBER_F",
            "LADM_COL.LADM_Nucleo.col_miembros.agrupacion..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_AgrupacionInteresados": "MEMBERS_T_GROUP_PARTY_F",
            "LADM_COL.LADM_Nucleo.col_miembros.interesado..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Interesado": "MEMBERS_T_PARTY_F"
        }},
        "LADM_COL.LADM_Nucleo.col_puntoCcl": {VARIABLE_NAME: "POINT_BFS_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_puntoCcl.ccl..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Lindero": "POINT_BFS_T_LC_BOUNDARY_F",
            "LADM_COL.LADM_Nucleo.col_puntoCcl.punto..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoControl": "POINT_BFS_T_LC_CONTROL_POINT_F",
            "LADM_COL.LADM_Nucleo.col_puntoCcl.punto..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoLevantamiento": "POINT_BFS_T_LC_SURVEY_POINT_F",
            "LADM_COL.LADM_Nucleo.col_puntoCcl.punto..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoLindero": "POINT_BFS_T_LC_BOUNDARY_POINT_F",
        }},
        "LADM_COL.LADM_Nucleo.col_puntoFuente": {VARIABLE_NAME: "COL_POINT_SOURCE_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_puntoFuente.fuente_espacial..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_FuenteEspacial": "COL_POINT_SOURCE_T_SOURCE_F",
            "LADM_COL.LADM_Nucleo.col_puntoFuente.punto..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoControl": "COL_POINT_SOURCE_T_LC_CONTROL_POINT_F",
            "LADM_COL.LADM_Nucleo.col_puntoFuente.punto..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoLevantamiento": "COL_POINT_SOURCE_T_LC_SURVEY_POINT_F",
            "LADM_COL.LADM_Nucleo.col_puntoFuente.punto..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoLindero": "COL_POINT_SOURCE_T_LC_BOUNDARY_POINT_F"
        }},
        "LADM_COL.LADM_Nucleo.col_rrrFuente": {VARIABLE_NAME: "COL_RRR_SOURCE_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_rrrFuente.fuente_administrativa..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_FuenteAdministrativa": "COL_RRR_SOURCE_T_SOURCE_F",
            "LADM_COL.LADM_Nucleo.col_rrrFuente.rrr..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Derecho": "COL_RRR_SOURCE_T_LC_RIGHT_F",
            "LADM_COL.LADM_Nucleo.col_rrrFuente.rrr..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Restriccion": "COL_RRR_SOURCE_T_LC_RESTRICTION_F"
        }},
        "LADM_COL.LADM_Nucleo.col_ueBaunit": {VARIABLE_NAME: "COL_UE_BAUNIT_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_ueBaunit.baunit..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Predio": "COL_UE_BAUNIT_T_PARCEL_F",
            "LADM_COL.LADM_Nucleo.col_ueBaunit.ue..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Terreno": "COL_UE_BAUNIT_T_LC_PLOT_F",
            "LADM_COL.LADM_Nucleo.col_ueBaunit.ue..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Construccion": "COL_UE_BAUNIT_T_LC_BUILDING_F",
            "LADM_COL.LADM_Nucleo.col_ueBaunit.ue..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion": "COL_UE_BAUNIT_T_LC_BUILDING_UNIT_F",
            "LADM_COL.LADM_Nucleo.col_ueBaunit.ue..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_ServidumbreTransito": "COL_UE_BAUNIT_T_LC_RIGHT_OF_WAY_F"
        }},
        "LADM_COL.LADM_Nucleo.col_ueFuente": {VARIABLE_NAME: "COL_UE_SOURCE_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_ueFuente.fuente_espacial..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_FuenteEspacial": "COL_UE_SOURCE_T_SOURCE_F",
            "LADM_COL.LADM_Nucleo.col_ueFuente.ue..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Construccion": "COL_UE_SOURCE_T_LC_BUILDING_F",
            "LADM_COL.LADM_Nucleo.col_ueFuente.ue..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_ServidumbreTransito": "COL_UE_SOURCE_T_LC_RIGHT_OF_WAY_F",
            "LADM_COL.LADM_Nucleo.col_ueFuente.ue..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Terreno": "COL_UE_SOURCE_T_LC_PLOT_F",
            "LADM_COL.LADM_Nucleo.col_ueFuente.ue..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion": "COL_UE_SOURCE_T_LC_BUILDING_UNIT_F"
        }},
        "LADM_COL.LADM_Nucleo.col_baunitFuente": {VARIABLE_NAME: "COL_BAUNIT_SOURCE_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_baunitFuente.fuente_espacial..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_FuenteEspacial": "BAUNIT_SOURCE_T_SOURCE_F",
            "LADM_COL.LADM_Nucleo.col_baunitFuente.unidad..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Predio": "BAUNIT_SOURCE_T_UNIT_F"
        }},
        "LADM_COL.LADM_Nucleo.col_cclFuente": {VARIABLE_NAME: "COL_CCL_SOURCE_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_cclFuente.fuente_espacial..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_FuenteEspacial": "COL_CCL_SOURCE_T_SOURCE_F",
            "LADM_COL.LADM_Nucleo.col_cclFuente.ccl..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Lindero": "COL_CCL_SOURCE_T_BOUNDARY_F"
        }},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.LC_AcuerdoTipo": {VARIABLE_NAME: "LC_AGREEMENT_TYPE_D", FIELDS_DICT: {}},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.LC_UsoUConsTipo": {VARIABLE_NAME: "LC_BUILDING_UNIT_USE_D", FIELDS_DICT: {}},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.LC_ConstruccionPlantaTipo": {VARIABLE_NAME: "LC_BUILDING_FLOOR_TYPE_D", FIELDS_DICT: {}},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.LC_ConstruccionTipo": {VARIABLE_NAME: "LC_BUILDING_TYPE_D", FIELDS_DICT: {}},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.LC_DominioConstruccionTipo": {VARIABLE_NAME: "LC_DOMAIN_BUILDING_TYPE_D", FIELDS_DICT: {}},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.LC_UnidadConstruccionTipo": {VARIABLE_NAME: "LC_BUILDING_UNIT_TYPE_D", FIELDS_DICT: {}},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.LC_CondicionPredioTipo": {VARIABLE_NAME: "LC_CONDITION_PARCEL_TYPE_D", FIELDS_DICT: {}},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.LC_DerechoTipo": {VARIABLE_NAME: "LC_RIGHT_TYPE_D", FIELDS_DICT: {}},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_AgrupacionInteresados": {VARIABLE_NAME: "LC_GROUP_PARTY_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.COL_AgrupacionInteresados.Tipo": "COL_GROUP_PARTY_T_TYPE_F",
            "LADM_COL.LADM_Nucleo.COL_Interesado.Nombre": "COL_PARTY_T_NAME_F",
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion": {VARIABLE_NAME: "LC_BUILDING_UNIT_T", FIELDS_DICT: {
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion.Area_Construida": "LC_BUILDING_UNIT_T_BUILT_AREA_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion.Area_Privada_Construida": "LC_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion.Avaluo_Unidad_Construccion": "LC_BUILDING_UNIT_T_BUILDING_UNIT_VALUATION_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion.Identificador": "LC_BUILDING_UNIT_T_IDENTIFICATION_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion.Planta_Ubicacion": "LC_BUILDING_UNIT_T_FLOOR_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion.Uso": "LC_BUILDING_UNIT_T_USE_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.lc_construccion_unidadconstruccion.lc_construccion..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Construccion": "LC_BUILDING_UNIT_T_BUILDING_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion.Anio_Construccion": "LC_BUILDING_UNIT_T_YEAR_OF_BUILDING_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion.Observaciones": "LC_BUILDING_UNIT_T_OBSERVATIONS_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion.Tipo_Construccion": "LC_BUILDING_UNIT_T_BUILDING_TYPE_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion.Tipo_Dominio": "LC_BUILDING_UNIT_T_DOMAIN_TYPE_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion.Tipo_Planta": "LC_BUILDING_UNIT_T_FLOOR_TYPE_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion.Tipo_Unidad_Construccion": "LC_BUILDING_UNIT_T_BUILDING_UNIT_TYPE_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion.Total_Banios": "LC_BUILDING_UNIT_T_TOTAL_BATHROOMS_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion.Total_Habitaciones": "LC_BUILDING_UNIT_T_TOTAL_ROOMS_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion.Total_Locales": "LC_BUILDING_UNIT_T_TOTAL_LOCALS_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion.Total_Pisos": "LC_BUILDING_UNIT_T_TOTAL_FLOORS_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_UnidadConstruccion.Altura": "LC_BUILDING_UNIT_T_HEIGHT_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Dimension": "COL_SPATIAL_UNIT_T_DIMENSION_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Etiqueta": "COL_SPATIAL_UNIT_T_LABEL_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Geometria": "COL_SPATIAL_UNIT_T_GEOMETRY_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie": "COL_SPATIAL_UNIT_T_SURFACE_RELATION_F",
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Construccion": {VARIABLE_NAME: "LC_BUILDING_T", FIELDS_DICT: {
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Construccion.Area_Construccion": "LC_BUILDING_T_BUILDING_AREA_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Construccion.Avaluo_Construccion": "LC_BUILDING_T_BUILDING_VALUATION_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Construccion.Numero_Pisos": "LC_BUILDING_T_NUMBER_OF_FLOORS_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Construccion.Altura": "LC_BUILDING_T_HEIGHT_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Construccion.Anio_Construccion": "LC_BUILDING_T_YEAR_OF_BUILD_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Construccion.Observaciones": "LC_BUILDING_T_OBSERVATIONS_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Construccion.Identificador": "LC_BUILDING_T_IDENTIFIER_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Construccion.Numero_Mezanines": "LC_BUILDING_T_NUMBER_OF_MEZZANINE_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Construccion.Numero_Semisotanos": "LC_BUILDING_T_NUMBER_OF_LOOKOUT_BASEMENT_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Construccion.Numero_Sotanos": "LC_BUILDING_T_NUMBER_OF_BASEMENT_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Construccion.Tipo_Construccion": "LC_BUILDING_T_BUILDING_TYPE_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Construccion.Tipo_Dominio": "LC_BUILDING_T_DOMAIN_TYPE_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Dimension": "COL_SPATIAL_UNIT_T_DIMENSION_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Etiqueta": "COL_SPATIAL_UNIT_T_LABEL_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Geometria": "COL_SPATIAL_UNIT_T_GEOMETRY_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie": "COL_SPATIAL_UNIT_T_SURFACE_RELATION_F",
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Derecho": {VARIABLE_NAME: "LC_RIGHT_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_baunitRrr.unidad..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Predio": "COL_BAUNIT_RRR_T_UNIT_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Derecho.Tipo": "LC_RIGHT_T_TYPE_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Derecho.Fecha_Inicio_Tenencia": "LC_RIGHT_T_DATE_START_TENANCY_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Derecho.Fraccion_Derecho": "LC_RIGHT_T_RIGHT_FRACTION_F",
            "LADM_COL.LADM_Nucleo.COL_DRR.Descripcion": "COL_RRR_T_DESCRIPTION_F",
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.col_rrrInteresado.interesado..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Interesado": "COL_RRR_PARTY_T_LC_PARTY_F",
            "LADM_COL.LADM_Nucleo.col_rrrInteresado.interesado..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_AgrupacionInteresados": "COL_RRR_PARTY_T_LC_GROUP_PARTY_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_FuenteAdministrativa": {VARIABLE_NAME: "LC_ADMINISTRATIVE_SOURCE_T", FIELDS_DICT: {
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_FuenteAdministrativa.Ente_Emisor": "LC_ADMINISTRATIVE_SOURCE_T_EMITTING_ENTITY_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_FuenteAdministrativa.Tipo": "LC_ADMINISTRATIVE_SOURCE_T_TYPE_F",
            "LADM_COL.LADM_Nucleo.COL_FuenteAdministrativa.Numero_Fuente": "COL_ADMINISTRATIVE_SOURCE_T_SOURCE_NUMBER_F",
            "LADM_COL.LADM_Nucleo.COL_FuenteAdministrativa.Observacion": "COL_ADMINISTRATIVE_SOURCE_T_OBSERVATION_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Estado_Disponibilidad": "COL_SOURCE_T_AVAILABILITY_STATUS_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Fecha_Documento_Fuente": "COL_SOURCE_T_DATE_DOCUMENT_F",
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Tipo_Principal": "COL_SOURCE_T_MAIN_TYPE_F"
        }},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_FuenteEspacial": {VARIABLE_NAME: "LC_SPATIAL_SOURCE_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.COL_FuenteEspacial.Tipo": "COL_SPATIAL_SOURCE_T_TYPE_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Estado_Disponibilidad": "COL_SOURCE_T_AVAILABILITY_STATUS_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Fecha_Documento_Fuente": "COL_SOURCE_T_DATE_DOCUMENT_F",
            "LADM_COL.LADM_Nucleo.COL_FuenteEspacial.Descripcion": "COL_SOURCE_T_DESCRIPTION_F",
            "LADM_COL.LADM_Nucleo.COL_FuenteEspacial.Metadato": "COL_SOURCE_T_METADATA_F",
            "LADM_COL.LADM_Nucleo.COL_FuenteEspacial.Nombre": "COL_SOURCE_T_NAME_F",
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.COL_Fuente.Tipo_Principal": "COL_SOURCE_T_MAIN_TYPE_F"
        }},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Interesado": {VARIABLE_NAME: "LC_PARTY_T", FIELDS_DICT: {
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Interesado.Documento_Identidad": "LC_PARTY_T_DOCUMENT_ID_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Interesado.Grupo_Etnico": "LC_PARTY_T_ETHNIC_GROUP_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Interesado.Primer_Apellido": "LC_PARTY_T_SURNAME_1_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Interesado.Primer_Nombre": "LC_PARTY_T_FIRST_NAME_1_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Interesado.Razon_Social": "LC_PARTY_T_BUSINESS_NAME_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Interesado.Segundo_Apellido": "LC_PARTY_T_SURNAME_2_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Interesado.Segundo_Nombre": "LC_PARTY_T_FIRST_NAME_2_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Interesado.Sexo": "LC_PARTY_T_GENRE_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Interesado.Tipo": "LC_PARTY_T_TYPE_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Interesado.Tipo_Documento": "LC_PARTY_T_DOCUMENT_TYPE_F",
            "LADM_COL.LADM_Nucleo.COL_Interesado.Nombre": "COL_PARTY_T_NAME_F",
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Lindero": {VARIABLE_NAME: "LC_BOUNDARY_T", FIELDS_DICT: {
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Lindero.Longitud": "LC_BOUNDARY_T_LENGTH_F",
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.COL_CadenaCarasLimite.Geometria": "COL_BFS_T_GEOMETRY_F",
            "LADM_COL.LADM_Nucleo.COL_CadenaCarasLimite.Localizacion_Textual": "COL_BFS_T_TEXTUAL_LOCATION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Predio": {VARIABLE_NAME: "LC_PARCEL_T", FIELDS_DICT: {
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Predio.Avaluo_Catastral": "LC_PARCEL_T_VALUATION_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Predio.Codigo_ORIP": "LC_PARCEL_T_ORIP_CODE_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Predio.Condicion_Predio": "LC_PARCEL_T_PARCEL_TYPE_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Predio.Departamento": "LC_PARCEL_T_DEPARTMENT_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Predio.Direccion..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Predio": "LC_PARCEL_T_ADDRESS_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Predio.Matricula_Inmobiliaria": "LC_PARCEL_T_FMI_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Predio.Tiene_FMI": "LC_PARCEL_T_HAS_FMI_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Predio.Municipio": "LC_PARCEL_T_MUNICIPALITY_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Predio.Numero_Predial": "LC_PARCEL_T_PARCEL_NUMBER_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Predio.Numero_Predial_Anterior": "LC_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Predio.Id_Operacion": "LC_PARCEL_T_ID_OPERATION_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Predio.NUPRE": "LC_PARCEL_T_NUPRE_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Predio.Tipo": "LC_PARCEL_T_TYPE_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadAdministrativaBasica.Nombre": "COL_BAUNIT_T_NAME_F",
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.lc_predio_copropiedad": {VARIABLE_NAME: "LC_COPROPERTY_T", FIELDS_DICT: {
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.lc_predio_copropiedad.coeficiente..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.lc_predio_copropiedad": "FRACTION_S_COPROPERTY_COEFFICIENT_F"
        }},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.lc_predio_ini_predioinsumos": {VARIABLE_NAME: "LC_OPERATION_SUPPLIES_T", FIELDS_DICT: {}},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoControl": {VARIABLE_NAME: "LC_CONTROL_POINT_T", FIELDS_DICT: {
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoControl.Exactitud_Horizontal": "LC_CONTROL_POINT_T_HORIZONTAL_ACCURACY_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoControl.Exactitud_Vertical": "LC_CONTROL_POINT_T_VERTICAL_ACCURACY_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoControl.ID_Punto_Control": "LC_CONTROL_POINT_T_ID_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoControl.PuntoTipo": "LC_CONTROL_POINT_T_POINT_TYPE_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoControl.Tipo_Punto_Control": "LC_CONTROL_POINT_T_CONTROL_POINT_TYPE_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.Posicion_Interpolacion": "COL_POINT_T_INTERPOLATION_POSITION_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.Geometria": "COL_POINT_T_ORIGINAL_LOCATION_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.MetodoProduccion": "COL_POINT_T_PRODUCTION_METHOD_F",
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoLevantamiento": {VARIABLE_NAME: "LC_SURVEY_POINT_T", FIELDS_DICT: {
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoLevantamiento.Exactitud_Horizontal": "LC_SURVEY_POINT_T_HORIZONTAL_ACCURACY_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoLevantamiento.Exactitud_Vertical": "LC_SURVEY_POINT_T_VERTICAL_ACCURACY_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoLevantamiento.Fotoidentificacion": "LC_SURVEY_POINT_T_PHOTO_IDENTIFICATION_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoLevantamiento.ID_Punto_Levantamiento": "LC_SURVEY_POINT_T_ID_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoLevantamiento.PuntoTipo": "LC_SURVEY_POINT_T_POINT_TYPE_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoLevantamiento.Tipo_Punto_Levantamiento": "LC_SURVEY_POINT_T_SURVEY_POINT_TYPE_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.Posicion_Interpolacion": "COL_POINT_T_INTERPOLATION_POSITION_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.Geometria": "COL_POINT_T_ORIGINAL_LOCATION_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.MetodoProduccion": "COL_POINT_T_PRODUCTION_METHOD_F",
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoLindero": {VARIABLE_NAME: "LC_BOUNDARY_POINT_T", FIELDS_DICT: {
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoLindero.Acuerdo": "LC_BOUNDARY_POINT_T_AGREEMENT_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoLindero.Exactitud_Horizontal": "LC_BOUNDARY_POINT_T_HORIZONTAL_ACCURACY_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoLindero.Exactitud_Vertical": "LC_BOUNDARY_POINT_T_VERTICAL_ACCURACY_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoLindero.Fotoidentificacion": "LC_BOUNDARY_POINT_T_PHOTO_IDENTIFICATION_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoLindero.ID_Punto_Lindero": "LC_BOUNDARY_POINT_T_ID_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_PuntoLindero.PuntoTipo": "LC_BOUNDARY_POINT_T_POINT_TYPE_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.Posicion_Interpolacion": "COL_POINT_T_INTERPOLATION_POSITION_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.Geometria": "COL_POINT_T_ORIGINAL_LOCATION_F",
            "LADM_COL.LADM_Nucleo.COL_Punto.MetodoProduccion": "COL_POINT_T_PRODUCTION_METHOD_F",
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Restriccion": {VARIABLE_NAME: "LC_RESTRICTION_T", FIELDS_DICT: {
            "LADM_COL.LADM_Nucleo.col_baunitRrr.unidad..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Predio": "COL_BAUNIT_RRR_T_UNIT_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Restriccion.Tipo": "LC_RESTRICTION_T_TYPE_F",
            "LADM_COL.LADM_Nucleo.COL_DRR.Descripcion": "COL_RRR_T_DESCRIPTION_F",
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.col_rrrInteresado.interesado..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Interesado": "COL_RRR_PARTY_T_LC_PARTY_F",
            "LADM_COL.LADM_Nucleo.col_rrrInteresado.interesado..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_AgrupacionInteresados": "COL_RRR_PARTY_T_LC_GROUP_PARTY_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_ServidumbreTransito": {VARIABLE_NAME: "LC_RIGHT_OF_WAY_T", FIELDS_DICT: {
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_ServidumbreTransito.Area_Servidumbre": "LC_RIGHT_OF_WAY_T_RIGHT_OF_WAY_AREA_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Dimension": "COL_SPATIAL_UNIT_T_DIMENSION_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Etiqueta": "COL_SPATIAL_UNIT_T_LABEL_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Geometria": "COL_SPATIAL_UNIT_T_GEOMETRY_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie": "COL_SPATIAL_UNIT_T_SURFACE_RELATION_F",
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Terreno": {VARIABLE_NAME: "LC_PLOT_T", FIELDS_DICT: {
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Terreno.Area_Terreno": "LC_PLOT_T_PLOT_AREA_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Terreno.Avaluo_Terreno": "LC_PLOT_T_PLOT_VALUATION_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Terreno.Geometria": "LC_PLOT_T_GEOMETRY_F",
            "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Terreno.Manzana_Vereda_Codigo": "LC_PLOT_T_BLOCK_RURAL_DIVISION_CODE_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Dimension": "COL_SPATIAL_UNIT_T_DIMENSION_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Etiqueta": "COL_SPATIAL_UNIT_T_LABEL_F",
            "LADM_COL.LADM_Nucleo.COL_UnidadEspacial.Relacion_Superficie": "COL_SPATIAL_UNIT_T_SURFACE_RELATION_F",
            "LADM_COL.LADM_Nucleo.Oid.Local_Id": "OID_T_LOCAL_ID_F",
            "LADM_COL.LADM_Nucleo.Oid.Espacio_De_Nombres": "OID_T_NAMESPACE_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Comienzo_Vida_Util_Version": "VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F",
            "LADM_COL.LADM_Nucleo.ObjetoVersionado.Fin_Vida_Util_Version": "VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F"
        }},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_InteresadoContacto": {VARIABLE_NAME: "LC_PARTY_CONTACT_T", FIELDS_DICT: {
            'Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_InteresadoContacto.Autoriza_Notificacion_Correo': 'LC_PARTY_CONTACT_T_ALLOW_MAIL_NOTIFICATION_F',
            'Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_InteresadoContacto.Correo_Electronico': 'LC_PARTY_CONTACT_T_EMAIL_F',
            'Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_InteresadoContacto.Domicilio_Notificacion': 'LC_PARTY_CONTACT_T_NOTIFICATION_ADDRESS_F',
            'Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_InteresadoContacto.Telefono1': 'LC_PARTY_CONTACT_T_TELEPHONE_NUMBER_1_F',
            'Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_InteresadoContacto.Telefono2': 'LC_PARTY_CONTACT_T_TELEPHONE_NUMBER_2_F',
            'Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.lc_interesado_interesadocontacto.lc_interesado..Modelo_Aplicacion_LADMCOL_Lev_Cat.Levantamiento_Catastral.LC_Interesado': 'LC_PARTY_CONTACT_T_LC_PARTY_F'
        }},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.LC_FuenteAdministrativaTipo": {VARIABLE_NAME: "LC_ADMINISTRATIVE_SOURCE_TYPE_D", FIELDS_DICT: {}},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.LC_FotoidentificacionTipo": {VARIABLE_NAME: "LC_PHOTO_IDENTIFICATION_TYPE_D", FIELDS_DICT: {}},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.LC_GrupoEtnicoTipo": {VARIABLE_NAME: "LC_ETHNIC_GROUP_TYPE_D", FIELDS_DICT: {}},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.LC_InteresadoDocumentoTipo": {VARIABLE_NAME: "LC_PARTY_DOCUMENT_TYPE_D", FIELDS_DICT: {}},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.LC_InteresadoTipo": {VARIABLE_NAME: "LC_PARTY_TYPE_D", FIELDS_DICT: {}},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.LC_PredioTipo": {VARIABLE_NAME: "LC_PARCEL_TYPE_D", FIELDS_DICT: {}},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.LC_PuntoControlTipo": {VARIABLE_NAME: "LC_CONTROL_POINT_TYPE_D", FIELDS_DICT: {}},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.LC_PuntoLevTipo": {VARIABLE_NAME: "LC_SURVEY_POINT_TYPE_D", FIELDS_DICT: {}},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.LC_PuntoTipo": {VARIABLE_NAME: "LC_POINT_TYPE_D", FIELDS_DICT: {}},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.LC_RestriccionTipo": {VARIABLE_NAME: "LC_RESTRICTION_TYPE_D", FIELDS_DICT: {}},
        "Modelo_Aplicacion_LADMCOL_Lev_Cat.LC_SexoTipo": {VARIABLE_NAME: "LC_GENRE_D", FIELDS_DICT: {}}
    }

    def __init__(self):
        self.logger = Logger()
        self._cached_domain_values = dict()  # Right cache: queries that actually return a domain value/code
        self._cached_wrong_domain_queries = {  # Wrong cache: queries that do not return anything from the domain
            QueryNames.VALUE_KEY: dict(),
            QueryNames.CODE_KEY: dict()
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
        self.reset_table_and_field_names()  # We will start mapping from scratch, so reset any previous mapping.

        any_update = False
        table_names_count = 0
        field_names_count = 0
        if dict_names:
            if T_ID_KEY not in dict_names \
                    or T_ILI_TID_KEY not in dict_names \
                    or DISPLAY_NAME_KEY not in dict_names \
                    or ILICODE_KEY not in dict_names \
                    or DESCRIPTION_KEY not in dict_names:
                self.logger.error(__name__, "dict_names is not properly built, at least one of these required fields was not found T_ID, T_ILI_TID, DISPLAY_NAME, ILICODE and DESCRIPTION.")
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
            self.T_ILI_TID_F = dict_names[T_ILI_TID_KEY] if T_ILI_TID_KEY in dict_names else None
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
        self.T_ILI_TID_F = None
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

    def cache_wrong_query(self, query_type, domain_table, code, value, value_is_ilicode):
        """
        If query was by value, then use value in key and code in the corresponding value pair, and viceversa

        :param query_type: QueryNames.VALUE_KEY (search by value) or QueryNames.CODE_KEY (search by code)
        :param domain_table: name of the table being searched
        :param code: t_id
        :param value: iliCode or dispName value
        :param value_is_ilicode: whether the value to be searched is iliCode or not
        """
        key = "{}..{}".format('ilicode' if value_is_ilicode else 'dispname', value if query_type == QueryNames.VALUE_KEY else code)
        if domain_table in self._cached_wrong_domain_queries[query_type]:
            self._cached_wrong_domain_queries[query_type][domain_table][key] = code if query_type == QueryNames.VALUE_KEY else value
        else:
            self._cached_wrong_domain_queries[query_type][domain_table] = {key: code if query_type == QueryNames.VALUE_KEY else value}

    def get_domain_value(self, domain_table, t_id, value_is_ilicode):
        """
        Get a domain value from the cache. First, attempt to get it from the 'right' cache, then from the 'wrong' cache.

        :param domain_table: Domain table name.
        :param t_id: t_id to be searched.
        :param value_is_ilicode: Whether the value is iliCode (True) or dispName (False)
        :return: iliCode of the corresponding t_id.
        """
        # Search in 'right' cache
        field_name = 'ilicode' if value_is_ilicode else 'dispname'
        if domain_table in self._cached_domain_values:
            for k,v in self._cached_domain_values[domain_table].items():
                if v == t_id:
                    key = k.split("..")
                    if key[0] == field_name:
                        return True, key[1]  # Compound key: ilicode..value or dispname..value

        # Search in 'wrong' cache
        if domain_table in self._cached_wrong_domain_queries[QueryNames.CODE_KEY]:
            key = "{}..{}".format('ilicode' if value_is_ilicode else 'dispname', t_id)
            if key in self._cached_wrong_domain_queries[QueryNames.CODE_KEY][domain_table]:
                return True, self._cached_wrong_domain_queries[QueryNames.CODE_KEY][domain_table][key]

        return False, None

    def get_domain_code(self, domain_table, value, value_is_ilicode):
        """
        Get a domain code from the cache. First, attempt to get it from the 'right' cache, then from the 'wrong' cache.

        :param domain_table: Domain table name.
        :param value: value to be searched.
        :param value_is_ilicode: Whether the value is iliCode (True) or dispName (False)
        :return: tuple (found, t_id)
                        found: boolean, whether the value was found in cache or not
                        t_id: t_id of the corresponding ilicode
        """
        # Search in 'right' cache
        key = "{}..{}".format('ilicode' if value_is_ilicode else 'dispname', value)
        if domain_table in self._cached_domain_values:
            if key in self._cached_domain_values[domain_table]:
                return True, self._cached_domain_values[domain_table][key]

        # Search in 'wrong' cache
        if domain_table in self._cached_wrong_domain_queries[QueryNames.VALUE_KEY]:
            if key in self._cached_wrong_domain_queries[QueryNames.VALUE_KEY][domain_table]:
                return True, self._cached_wrong_domain_queries[QueryNames.VALUE_KEY][domain_table][key]

        return False, None

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

