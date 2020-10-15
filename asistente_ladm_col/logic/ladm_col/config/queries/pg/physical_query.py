from asistente_ladm_col.logic.ladm_col.config.queries.pg.pg_queries_config_utils import (get_custom_filter_parcels,
                                                                                         get_custom_filter_plots)


def get_igac_physical_query(names, schema, plot_t_ids, parcel_fmi, parcel_number, previous_parcel_number):
    custom_filter_plots = get_custom_filter_plots(names, schema, plot_t_ids)
    custom_filter_parcels = get_custom_filter_parcels(names, schema, plot_t_ids)

    query = """
            WITH
             _unidad_area_terreno AS (
                 SELECT ' [' || setting || ']' FROM {schema}.t_ili2db_column_prop WHERE tablename = '{LC_PLOT_T}' AND columnname = '{LC_PLOT_T_PLOT_AREA_F}' LIMIT 1
             ),
             _unidad_area_construida_uc AS (
                 SELECT ' [' || setting || ']' FROM {schema}.t_ili2db_column_prop WHERE tablename = '{LC_BUILDING_UNIT_T}' AND columnname = '{LC_BUILDING_UNIT_T_BUILT_AREA_F}' LIMIT 1
             ),
             _unidad_area_privada_construida_uc AS (
                 SELECT ' [' || setting || ']' FROM {schema}.t_ili2db_column_prop WHERE tablename = '{LC_BUILDING_UNIT_T}' AND columnname = '{LC_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F}' LIMIT 1
             ),
             _unidad_longitud_lindero AS (
                 SELECT ' [' || setting || ']' FROM {schema}.t_ili2db_column_prop WHERE tablename = '{LC_BOUNDARY_T}' AND columnname = '{LC_BOUNDARY_T_LENGTH_F}' LIMIT 1
             ),
             _terrenos_seleccionados AS (
                {custom_filter_plots}
                SELECT {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F} FROM {schema}.{LC_PARCEL_T} LEFT JOIN {schema}.{COL_UE_BAUNIT_T} ON {LC_PARCEL_T}.{T_ID_F} = {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_PARCEL_F}  WHERE {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F} IS NOT NULL AND CASE WHEN '{parcel_fmi}' = 'NULL' THEN  1 = 2 ELSE ({LC_PARCEL_T}.{LC_PARCEL_T_ORIP_CODE_F} || '-'|| {LC_PARCEL_T}.{LC_PARCEL_T_FMI_F}) = '{parcel_fmi}' END
                    UNION
                SELECT {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F} FROM {schema}.{LC_PARCEL_T} LEFT JOIN {schema}.{COL_UE_BAUNIT_T} ON {LC_PARCEL_T}.{T_ID_F} = {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_PARCEL_F}  WHERE {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F} IS NOT NULL AND CASE WHEN '{parcel_number}' = 'NULL' THEN  1 = 2 ELSE {LC_PARCEL_T}.{LC_PARCEL_T_PARCEL_NUMBER_F} = '{parcel_number}' END
                    UNION
                SELECT {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F} FROM {schema}.{LC_PARCEL_T} LEFT JOIN {schema}.{COL_UE_BAUNIT_T} ON {LC_PARCEL_T}.{T_ID_F} = {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_PARCEL_F}  WHERE {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F} IS NOT NULL AND CASE WHEN '{previous_parcel_number}' = 'NULL' THEN  1 = 2 ELSE {LC_PARCEL_T}.{LC_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F} = '{previous_parcel_number}' END
             ),
             _predios_seleccionados AS (
                {custom_filter_parcels}
                SELECT {T_ID_F} FROM {schema}.{LC_PARCEL_T} WHERE CASE WHEN '{parcel_fmi}' = 'NULL' THEN  1 = 2 ELSE ({LC_PARCEL_T}.{LC_PARCEL_T_ORIP_CODE_F} || '-'|| {LC_PARCEL_T}.{LC_PARCEL_T_FMI_F}) = '{parcel_fmi}' END
                    UNION
                SELECT {T_ID_F} FROM {schema}.{LC_PARCEL_T} WHERE CASE WHEN '{parcel_number}' = 'NULL' THEN  1 = 2 ELSE {LC_PARCEL_T}.{LC_PARCEL_T_PARCEL_NUMBER_F} = '{parcel_number}' END
                    UNION
                SELECT {T_ID_F} FROM {schema}.{LC_PARCEL_T} WHERE CASE WHEN '{previous_parcel_number}' = 'NULL' THEN  1 = 2 ELSE {LC_PARCEL_T}.{LC_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F} = '{previous_parcel_number}' END
             ),
             _construcciones_seleccionadas AS (
                 SELECT {COL_UE_BAUNIT_T_LC_BUILDING_F} FROM {schema}.{COL_UE_BAUNIT_T} WHERE {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_PARCEL_F} IN (SELECT _predios_seleccionados.{T_ID_F} FROM _predios_seleccionados WHERE _predios_seleccionados.{T_ID_F} IS NOT NULL) AND {COL_UE_BAUNIT_T_LC_BUILDING_F} IS NOT NULL
             ),
             _unidadesconstruccion_seleccionadas AS (
                 SELECT {LC_BUILDING_UNIT_T}.{T_ID_F} FROM {schema}.{LC_BUILDING_UNIT_T} WHERE {LC_BUILDING_UNIT_T}.{LC_BUILDING_UNIT_T_BUILDING_F} IN (SELECT {COL_UE_BAUNIT_T_LC_BUILDING_F} FROM _construcciones_seleccionadas)
             ),
            _punto_lindero_externos_seleccionados AS (
                 SELECT DISTINCT {MORE_BFS_T}.{MORE_BFS_T_LC_PLOT_F}, {LC_BOUNDARY_POINT_T}.{T_ID_F}
                 FROM {schema}.{LC_BOUNDARY_POINT_T} JOIN {schema}.{POINT_BFS_T} ON {LC_BOUNDARY_POINT_T}.{T_ID_F} = {POINT_BFS_T}.{POINT_BFS_T_LC_BOUNDARY_POINT_F}
                 JOIN {schema}.{LC_BOUNDARY_T} ON {POINT_BFS_T}.{POINT_BFS_T_LC_BOUNDARY_F} = {LC_BOUNDARY_T}.{T_ID_F}
                 JOIN {schema}.{MORE_BFS_T} ON {LC_BOUNDARY_T}.{T_ID_F} = {MORE_BFS_T}.{MORE_BFS_T_LC_BOUNDARY_F}
                 WHERE {MORE_BFS_T}.{MORE_BFS_T_LC_PLOT_F} IN (SELECT * FROM _terrenos_seleccionados)
                 ORDER BY {MORE_BFS_T}.{MORE_BFS_T_LC_PLOT_F}, {LC_BOUNDARY_POINT_T}.{T_ID_F}
            ),
            _punto_lindero_internos_seleccionados AS (
                SELECT DISTINCT {LESS_BFS_T}.{LESS_BFS_T_LC_PLOT_F}, {LC_BOUNDARY_POINT_T}.{T_ID_F}
                FROM {schema}.{LC_BOUNDARY_POINT_T} JOIN {schema}.{POINT_BFS_T} ON {LC_BOUNDARY_POINT_T}.{T_ID_F} = {POINT_BFS_T}.{POINT_BFS_T_LC_BOUNDARY_POINT_F}
                JOIN {schema}.{LC_BOUNDARY_T} ON {POINT_BFS_T}.{POINT_BFS_T_LC_BOUNDARY_F} = {LC_BOUNDARY_T}.{T_ID_F}
                JOIN {schema}.{LESS_BFS_T} ON {LC_BOUNDARY_T}.{T_ID_F} = {LESS_BFS_T}.{LESS_BFS_T_LC_BOUNDARY_F}
                WHERE {LESS_BFS_T}.{LESS_BFS_T_LC_PLOT_F} IN (SELECT * FROM _terrenos_seleccionados)
              ORDER BY {LESS_BFS_T}.{LESS_BFS_T_LC_PLOT_F}, {LC_BOUNDARY_POINT_T}.{T_ID_F}
            ),
             _uc_fuente_espacial AS (
                SELECT {COL_UE_SOURCE_T}.{COL_UE_SOURCE_T_LC_BUILDING_UNIT_F},
                    JSON_AGG(
                            JSON_BUILD_OBJECT('id', {LC_SPATIAL_SOURCE_T}.{T_ID_F},
                                                   'attributes', JSON_BUILD_OBJECT('Tipo de fuente espacial', (SELECT {DISPLAY_NAME_F} FROM {schema}.{COL_SPATIAL_SOURCE_TYPE_D} WHERE {T_ID_F} = {LC_SPATIAL_SOURCE_T}.{COL_SPATIAL_SOURCE_T_TYPE_F}),
                                                                                   'Estado disponibilidad', (SELECT {DISPLAY_NAME_F} FROM {schema}.{COL_AVAILABILITY_TYPE_D} WHERE {T_ID_F} = {LC_SPATIAL_SOURCE_T}.{COL_SOURCE_T_AVAILABILITY_STATUS_F}),
                                                                                   'Tipo principal', (SELECT {DISPLAY_NAME_F} FROM {schema}.{CI_CODE_PRESENTATION_FORM_D} WHERE {T_ID_F} = {LC_SPATIAL_SOURCE_T}.{COL_SOURCE_T_MAIN_TYPE_F}),
                                                                                   'Fecha documento', {LC_SPATIAL_SOURCE_T}.{COL_SOURCE_T_DATE_DOCUMENT_F},
                                                                                   'Archivo fuente', {EXT_ARCHIVE_S}.{EXT_ARCHIVE_S_DATA_F}))
                    ORDER BY {LC_SPATIAL_SOURCE_T}.{T_ID_F}) FILTER(WHERE {COL_UE_SOURCE_T}.{COL_UE_SOURCE_T_SOURCE_F} IS NOT NULL) AS _fuenteespacial_
                FROM {schema}.{COL_UE_SOURCE_T} LEFT JOIN {schema}.{LC_SPATIAL_SOURCE_T} ON {COL_UE_SOURCE_T}.{COL_UE_SOURCE_T_SOURCE_F} = {LC_SPATIAL_SOURCE_T}.{T_ID_F}
                LEFT JOIN {schema}.{EXT_ARCHIVE_S} ON {EXT_ARCHIVE_S}.{EXT_ARCHIVE_S_LC_SPATIAL_SOURCE_F} = {LC_SPATIAL_SOURCE_T}.{T_ID_F}
                WHERE {COL_UE_SOURCE_T}.{COL_UE_SOURCE_T_LC_BUILDING_UNIT_F} IN (SELECT * FROM _unidadesconstruccion_seleccionadas)
                GROUP BY {COL_UE_SOURCE_T}.{COL_UE_SOURCE_T_LC_BUILDING_UNIT_F}
             ),
            _info_uc AS (
                 SELECT {LC_BUILDING_UNIT_T}.{LC_BUILDING_UNIT_T_BUILDING_F},
                        JSON_AGG(JSON_BUILD_OBJECT('id', {LC_BUILDING_UNIT_T}.{T_ID_F},
                                          'attributes', JSON_BUILD_OBJECT('Número de pisos', {LC_BUILDING_UNIT_T}.{LC_BUILDING_UNIT_T_TOTAL_FLOORS_F},
                                                                          'Uso', (SELECT {DISPLAY_NAME_F} FROM {schema}.{LC_BUILDING_UNIT_USE_D} WHERE {T_ID_F} = {LC_BUILDING_UNIT_T}.{LC_BUILDING_UNIT_T_USE_F}),
                                                                          'Tipo construcción', (SELECT {DISPLAY_NAME_F} FROM {schema}.{LC_BUILDING_TYPE_D} WHERE {T_ID_F} = {LC_BUILDING_UNIT_T}.{LC_BUILDING_UNIT_T_BUILDING_TYPE_F}),
                                                                          'Tipo unidad de construcción', (SELECT {DISPLAY_NAME_F} FROM {schema}.{LC_BUILDING_UNIT_TYPE_D} WHERE {T_ID_F} = {LC_BUILDING_UNIT_T}.{LC_BUILDING_UNIT_T_BUILDING_UNIT_TYPE_F}),
                                                                          CONCAT('Área privada construida' , (SELECT * FROM _unidad_area_privada_construida_uc)), {LC_BUILDING_UNIT_T}.{LC_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F},
                                                                          CONCAT('Área construida' , (SELECT * FROM _unidad_area_construida_uc)), {LC_BUILDING_UNIT_T}.{LC_BUILDING_UNIT_T_BUILT_AREA_F},
                                                                          '{LC_SPATIAL_SOURCE_T}', COALESCE(_uc_fuente_espacial._fuenteespacial_, '[]')
                                                                         )) ORDER BY {LC_BUILDING_UNIT_T}.{T_ID_F}) FILTER(WHERE {LC_BUILDING_UNIT_T}.{T_ID_F} IS NOT NULL) AS _unidadconstruccion_
                 FROM {schema}.{LC_BUILDING_UNIT_T} LEFT JOIN _uc_fuente_espacial ON {LC_BUILDING_UNIT_T}.{T_ID_F} = _uc_fuente_espacial.{COL_UE_SOURCE_T_LC_BUILDING_UNIT_F}
                 WHERE {LC_BUILDING_UNIT_T}.{T_ID_F} IN (SELECT * FROM _unidadesconstruccion_seleccionadas)
                 GROUP BY {LC_BUILDING_UNIT_T}.{LC_BUILDING_UNIT_T_BUILDING_F}
             ),
             _c_fuente_espacial AS (
                SELECT {COL_UE_SOURCE_T}.{COL_UE_SOURCE_T_LC_BUILDING_F},
                    JSON_AGG(
                            JSON_BUILD_OBJECT('id', {LC_SPATIAL_SOURCE_T}.{T_ID_F},
                                                   'attributes', JSON_BUILD_OBJECT('Tipo de fuente espacial', (SELECT {DISPLAY_NAME_F} FROM {schema}.{COL_SPATIAL_SOURCE_TYPE_D} WHERE {T_ID_F} = {LC_SPATIAL_SOURCE_T}.{COL_SPATIAL_SOURCE_T_TYPE_F}),
                                                                                   'Estado disponibilidad', (SELECT {DISPLAY_NAME_F} FROM {schema}.{COL_AVAILABILITY_TYPE_D} WHERE {T_ID_F} = {LC_SPATIAL_SOURCE_T}.{COL_SOURCE_T_AVAILABILITY_STATUS_F}),
                                                                                   'Tipo principal', (SELECT {DISPLAY_NAME_F} FROM {schema}.{CI_CODE_PRESENTATION_FORM_D} WHERE {T_ID_F} = {LC_SPATIAL_SOURCE_T}.{COL_SOURCE_T_MAIN_TYPE_F}),
                                                                                   'Fecha documento', {LC_SPATIAL_SOURCE_T}.{COL_SOURCE_T_DATE_DOCUMENT_F},
                                                                                   'Archivo fuente', {EXT_ARCHIVE_S}.{EXT_ARCHIVE_S_DATA_F}))
                    ORDER BY {LC_SPATIAL_SOURCE_T}.{T_ID_F}) FILTER(WHERE {COL_UE_SOURCE_T}.{COL_UE_SOURCE_T_SOURCE_F} IS NOT NULL) AS _fuenteespacial_
                FROM {schema}.{COL_UE_SOURCE_T} LEFT JOIN {schema}.{LC_SPATIAL_SOURCE_T} ON {COL_UE_SOURCE_T}.{COL_UE_SOURCE_T_SOURCE_F} = {LC_SPATIAL_SOURCE_T}.{T_ID_F}
                LEFT JOIN {schema}.{EXT_ARCHIVE_S} ON {EXT_ARCHIVE_S}.{EXT_ARCHIVE_S_LC_SPATIAL_SOURCE_F} = {LC_SPATIAL_SOURCE_T}.{T_ID_F}
                WHERE {COL_UE_SOURCE_T}.{COL_UE_SOURCE_T_LC_BUILDING_F} IN (SELECT * FROM _construcciones_seleccionadas)
                GROUP BY {COL_UE_SOURCE_T}.{COL_UE_SOURCE_T_LC_BUILDING_F}
             ),
             _info_construccion AS (
              SELECT {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_PARCEL_F},
                    JSON_AGG(JSON_BUILD_OBJECT('id', {LC_BUILDING_T}.{T_ID_F},
                                      'attributes', JSON_BUILD_OBJECT('Área construcción', {LC_BUILDING_T}.{LC_BUILDING_T_BUILDING_AREA_F},
                                                                      'Número de pisos', {LC_BUILDING_T}.{LC_BUILDING_T_NUMBER_OF_FLOORS_F},
                                                                      '{LC_BUILDING_UNIT_T}', COALESCE(_info_uc._unidadconstruccion_, '[]'),
                                                                      '{LC_SPATIAL_SOURCE_T}', COALESCE(_c_fuente_espacial._fuenteespacial_, '[]')
                                                                     )) ORDER BY {LC_BUILDING_T}.{T_ID_F}) FILTER(WHERE {LC_BUILDING_T}.{T_ID_F} IS NOT NULL) AS _construccion_
              FROM {schema}.{LC_BUILDING_T} LEFT JOIN _c_fuente_espacial ON {LC_BUILDING_T}.{T_ID_F} = _c_fuente_espacial.{COL_UE_SOURCE_T_LC_BUILDING_F}
              LEFT JOIN _info_uc ON {LC_BUILDING_T}.{T_ID_F} = _info_uc.{LC_BUILDING_UNIT_T_BUILDING_F}
              LEFT JOIN {schema}.{COL_UE_BAUNIT_T} ON {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_BUILDING_F} = {LC_BUILDING_T}.{T_ID_F}
              WHERE {LC_BUILDING_T}.{T_ID_F} IN (SELECT * FROM _construcciones_seleccionadas)
              GROUP BY {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_PARCEL_F}
             ),
             _info_predio AS (
                 SELECT {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F},
                        JSON_AGG(JSON_BUILD_OBJECT('id', {LC_PARCEL_T}.{T_ID_F},
                                          'attributes', JSON_BUILD_OBJECT('Nombre', {LC_PARCEL_T}.{COL_BAUNIT_T_NAME_F},
                                                                          'NUPRE', {LC_PARCEL_T}.{LC_PARCEL_T_NUPRE_F},
                                                                          'Id operación', {LC_PARCEL_T}.{LC_PARCEL_T_ID_OPERATION_F},
                                                                          'FMI', ({LC_PARCEL_T}.{LC_PARCEL_T_ORIP_CODE_F} || '-'|| {LC_PARCEL_T}.{LC_PARCEL_T_FMI_F}),
                                                                          'Número predial', {LC_PARCEL_T}.{LC_PARCEL_T_PARCEL_NUMBER_F},
                                                                          'Número predial anterior', {LC_PARCEL_T}.{LC_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F},
                                                                          '{LC_BUILDING_T}', COALESCE(_info_construccion._construccion_, '[]')
                                                                         )) ORDER BY {LC_PARCEL_T}.{T_ID_F}) FILTER(WHERE {LC_PARCEL_T}.{T_ID_F} IS NOT NULL) AS _predio_
                 FROM {schema}.{LC_PARCEL_T} LEFT JOIN _info_construccion ON {LC_PARCEL_T}.{T_ID_F} = _info_construccion.{COL_UE_BAUNIT_T_PARCEL_F}
                 LEFT JOIN {schema}.{COL_UE_BAUNIT_T} ON {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_PARCEL_F} = _info_construccion.{COL_UE_BAUNIT_T_PARCEL_F}
                 WHERE {LC_PARCEL_T}.{T_ID_F} = _info_construccion.{COL_UE_BAUNIT_T_PARCEL_F}
                 AND {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F} IS NOT NULL
                 AND {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_BUILDING_F} IS NULL
                 AND {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_BUILDING_UNIT_F} IS NULL
                 GROUP BY {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F}
             ),
             _t_fuente_espacial AS (
                SELECT {COL_UE_SOURCE_T}.{COL_UE_SOURCE_T_LC_PLOT_F},
                    JSON_AGG(
                            JSON_BUILD_OBJECT('id', {LC_SPATIAL_SOURCE_T}.{T_ID_F},
                                                   'attributes', JSON_BUILD_OBJECT('Tipo de fuente espacial', (SELECT {DISPLAY_NAME_F} FROM {schema}.{COL_SPATIAL_SOURCE_TYPE_D} WHERE {T_ID_F} = {LC_SPATIAL_SOURCE_T}.{COL_SPATIAL_SOURCE_T_TYPE_F}),
                                                                                   'Estado disponibilidad', (SELECT {DISPLAY_NAME_F} FROM {schema}.{COL_AVAILABILITY_TYPE_D} WHERE {T_ID_F} = {LC_SPATIAL_SOURCE_T}.{COL_SOURCE_T_AVAILABILITY_STATUS_F}),
                                                                                   'Tipo principal', (SELECT {DISPLAY_NAME_F} FROM {schema}.{CI_CODE_PRESENTATION_FORM_D} WHERE {T_ID_F} = {LC_SPATIAL_SOURCE_T}.{COL_SOURCE_T_MAIN_TYPE_F}),
                                                                                   'Fecha documento', {LC_SPATIAL_SOURCE_T}.{COL_SOURCE_T_DATE_DOCUMENT_F},
                                                                                   'Archivo fuente', {EXT_ARCHIVE_S}.{EXT_ARCHIVE_S_DATA_F}))
                    ORDER BY {LC_SPATIAL_SOURCE_T}.{T_ID_F}) FILTER(WHERE {COL_UE_SOURCE_T}.{COL_UE_SOURCE_T_SOURCE_F} IS NOT NULL) AS _fuenteespacial_
                FROM {schema}.{COL_UE_SOURCE_T} LEFT JOIN {schema}.{LC_SPATIAL_SOURCE_T} ON {COL_UE_SOURCE_T}.{COL_UE_SOURCE_T_SOURCE_F} = {LC_SPATIAL_SOURCE_T}.{T_ID_F}
                LEFT JOIN {schema}.{EXT_ARCHIVE_S} ON {EXT_ARCHIVE_S}.{EXT_ARCHIVE_S_LC_SPATIAL_SOURCE_F} = {LC_SPATIAL_SOURCE_T}.{T_ID_F}
                WHERE {COL_UE_SOURCE_T}.{COL_UE_SOURCE_T_LC_PLOT_F} IN (SELECT * FROM _terrenos_seleccionados)
                GROUP BY {COL_UE_SOURCE_T}.{COL_UE_SOURCE_T_LC_PLOT_F}
             ),
             _info_linderos_externos AS (
                SELECT {MORE_BFS_T}.{MORE_BFS_T_LC_PLOT_F},
                    JSON_AGG(
                            JSON_BUILD_OBJECT('id', {LC_BOUNDARY_T}.{T_ID_F},
                                                   'attributes', JSON_BUILD_OBJECT(CONCAT('Longitud' , (SELECT * FROM _unidad_longitud_lindero)), {LC_BOUNDARY_T}.{LC_BOUNDARY_T_LENGTH_F}))
                    ORDER BY {LC_BOUNDARY_T}.{T_ID_F}) FILTER(WHERE {LC_BOUNDARY_T}.{T_ID_F} IS NOT NULL) AS _lindero_
                FROM {schema}.{LC_BOUNDARY_T} JOIN {schema}.{MORE_BFS_T} ON {LC_BOUNDARY_T}.{T_ID_F} = {MORE_BFS_T}.{MORE_BFS_T_LC_BOUNDARY_F}
                WHERE {MORE_BFS_T}.{MORE_BFS_T_LC_PLOT_F} IN (SELECT * FROM _terrenos_seleccionados)
                GROUP BY {MORE_BFS_T}.{MORE_BFS_T_LC_PLOT_F}
             ),
             _info_linderos_internos AS (
                SELECT {LESS_BFS_T}.{LESS_BFS_T_LC_PLOT_F},
                    JSON_AGG(
                            JSON_BUILD_OBJECT('id', {LC_BOUNDARY_T}.{T_ID_F},
                                                   'attributes', JSON_BUILD_OBJECT(CONCAT('Longitud' , (SELECT * FROM _unidad_longitud_lindero)), {LC_BOUNDARY_T}.{LC_BOUNDARY_T_LENGTH_F}))
                    ORDER BY {LC_BOUNDARY_T}.{T_ID_F}) FILTER(WHERE {LC_BOUNDARY_T}.{T_ID_F} IS NOT NULL) AS _lindero_
                FROM {schema}.{LC_BOUNDARY_T} JOIN {schema}.{LESS_BFS_T} ON {LC_BOUNDARY_T}.{T_ID_F} = {LESS_BFS_T}.{LESS_BFS_T_LC_BOUNDARY_F}
                WHERE {LESS_BFS_T}.{LESS_BFS_T_LC_PLOT_F} IN (SELECT * FROM _terrenos_seleccionados)
                GROUP BY {LESS_BFS_T}.{LESS_BFS_T_LC_PLOT_F}
             ),
            _info_punto_lindero_externos AS (
                SELECT _punto_lindero_externos_seleccionados.{MORE_BFS_T_LC_PLOT_F},
                        JSON_AGG(
                            JSON_BUILD_OBJECT('id', {LC_BOUNDARY_POINT_T}.{T_ID_F},
                                                   'attributes', JSON_BUILD_OBJECT('Nombre', {LC_BOUNDARY_POINT_T}.{LC_BOUNDARY_POINT_T_ID_F},
                                                                                   'Coordenadas', concat(st_x({LC_BOUNDARY_POINT_T}.{COL_POINT_T_ORIGINAL_LOCATION_F}),
                                                                                                 ' ', st_y({LC_BOUNDARY_POINT_T}.{COL_POINT_T_ORIGINAL_LOCATION_F}),
                                                                                                 CASE WHEN st_z({LC_BOUNDARY_POINT_T}.{COL_POINT_T_ORIGINAL_LOCATION_F}) IS NOT NULL THEN concat(' ', st_z({LC_BOUNDARY_POINT_T}.{COL_POINT_T_ORIGINAL_LOCATION_F})) END))
                        ) ORDER BY {LC_BOUNDARY_POINT_T}.{T_ID_F}) FILTER(WHERE {LC_BOUNDARY_POINT_T}.{T_ID_F} IS NOT NULL) AS _puntolindero_
                FROM {schema}.{LC_BOUNDARY_POINT_T} JOIN _punto_lindero_externos_seleccionados ON {LC_BOUNDARY_POINT_T}.{T_ID_F} = _punto_lindero_externos_seleccionados.{T_ID_F}
                WHERE _punto_lindero_externos_seleccionados.{MORE_BFS_T_LC_PLOT_F} IS NOT NULL
                GROUP BY _punto_lindero_externos_seleccionados.{MORE_BFS_T_LC_PLOT_F}
             ),
             _info_punto_lindero_internos AS (
                 SELECT _punto_lindero_internos_seleccionados.{LESS_BFS_T_LC_PLOT_F},
                        JSON_AGG(
                            JSON_BUILD_OBJECT('id', {LC_BOUNDARY_POINT_T}.{T_ID_F},
                                                   'attributes', JSON_BUILD_OBJECT('Nombre', {LC_BOUNDARY_POINT_T}.{LC_BOUNDARY_POINT_T_ID_F},
                                                                                   'Coordenadas', concat(st_x({LC_BOUNDARY_POINT_T}.{COL_POINT_T_ORIGINAL_LOCATION_F}),
                                                                                                 ' ', st_y({LC_BOUNDARY_POINT_T}.{COL_POINT_T_ORIGINAL_LOCATION_F}),
                                                                                                 CASE WHEN st_z({LC_BOUNDARY_POINT_T}.{COL_POINT_T_ORIGINAL_LOCATION_F}) IS NOT NULL THEN concat(' ', st_z({LC_BOUNDARY_POINT_T}.{COL_POINT_T_ORIGINAL_LOCATION_F})) END))
                        ) ORDER BY {LC_BOUNDARY_POINT_T}.{T_ID_F}) FILTER(WHERE {LC_BOUNDARY_POINT_T}.{T_ID_F} IS NOT NULL) AS _puntolindero_
                 FROM {schema}.{LC_BOUNDARY_POINT_T} JOIN _punto_lindero_internos_seleccionados ON {LC_BOUNDARY_POINT_T}.{T_ID_F} = _punto_lindero_internos_seleccionados.{T_ID_F}
                 WHERE _punto_lindero_internos_seleccionados.{LESS_BFS_T_LC_PLOT_F} IS NOT NULL
                 GROUP BY _punto_lindero_internos_seleccionados.{LESS_BFS_T_LC_PLOT_F}
             ),
            _info_puntolevantamiento AS (
                SELECT _t_id_terreno_,
                        JSON_AGG(
                                JSON_BUILD_OBJECT('id', _puntoslevantamiento_seleccionados._t_id_puntolevantamiento_,
                                                       'attributes', JSON_BUILD_OBJECT('Coordenadas', concat(st_x(_puntoslevantamiento_seleccionados._geometria_),
                                                                                                 ' ', st_y(_puntoslevantamiento_seleccionados._geometria_),
                                                                                                 CASE WHEN st_z(_puntoslevantamiento_seleccionados._geometria_) IS NOT NULL THEN concat(' ', st_z(_puntoslevantamiento_seleccionados._geometria_)) END)
                                                                                      ))
                        ORDER BY _puntoslevantamiento_seleccionados._t_id_puntolevantamiento_) FILTER(WHERE _puntoslevantamiento_seleccionados._t_id_puntolevantamiento_ IS NOT NULL) AS _puntolevantamiento_
                FROM
                (
                    SELECT {LC_SURVEY_POINT_T}.{T_ID_F} AS _t_id_puntolevantamiento_, {LC_SURVEY_POINT_T}.{COL_POINT_T_ORIGINAL_LOCATION_F} AS _geometria_, {LC_PLOT_T}.{T_ID_F} AS _t_id_terreno_
                    FROM {schema}.{LC_PLOT_T}, {schema}.{LC_SURVEY_POINT_T}
                    WHERE ST_Intersects({LC_PLOT_T}.{LC_PLOT_T_GEOMETRY_F}, {LC_SURVEY_POINT_T}.{COL_POINT_T_ORIGINAL_LOCATION_F}) AND {LC_PLOT_T}.{T_ID_F} IN (SELECT * FROM _terrenos_seleccionados)
                ) AS _puntoslevantamiento_seleccionados
                GROUP BY _t_id_terreno_
            ),
             _info_terreno AS (
                SELECT {LC_PLOT_T}.{T_ID_F},
                  JSON_BUILD_OBJECT('id', {LC_PLOT_T}.{T_ID_F},
                                    'attributes', JSON_BUILD_OBJECT(CONCAT('Área' , (SELECT * FROM _unidad_area_terreno)), {LC_PLOT_T}.{LC_PLOT_T_PLOT_AREA_F},
                                                                    '{LC_PARCEL_T}', COALESCE(_info_predio._predio_, '[]'),
                                                                    '{LC_BOUNDARY_T} externos', COALESCE(_info_linderos_externos._lindero_, '[]'),
                                                                    '{LC_BOUNDARY_POINT_T} externos', COALESCE(_info_punto_lindero_externos._puntolindero_, '[]'),
                                                                    '{LC_BOUNDARY_T} internos', COALESCE(_info_linderos_internos._lindero_, '[]'),
                                                                    '{LC_BOUNDARY_POINT_T} internos', COALESCE(_info_punto_lindero_internos._puntolindero_, '[]'),
                                                                    '{LC_SURVEY_POINT_T}', COALESCE(_info_puntolevantamiento._puntolevantamiento_, '[]'),
                                                                    '{LC_SPATIAL_SOURCE_T}', COALESCE(_t_fuente_espacial._fuenteespacial_, '[]')
                                                                   )) AS _terreno_
                FROM {schema}.{LC_PLOT_T} LEFT JOIN _info_predio ON _info_predio.{COL_UE_BAUNIT_T_LC_PLOT_F} = {LC_PLOT_T}.{T_ID_F}
                LEFT JOIN _t_fuente_espacial ON {LC_PLOT_T}.{T_ID_F} = _t_fuente_espacial.{COL_UE_SOURCE_T_LC_PLOT_F}
                LEFT JOIN _info_linderos_externos ON {LC_PLOT_T}.{T_ID_F} = _info_linderos_externos.{MORE_BFS_T_LC_PLOT_F}
                LEFT JOIN _info_linderos_internos ON {LC_PLOT_T}.{T_ID_F} = _info_linderos_internos.{LESS_BFS_T_LC_PLOT_F}
                LEFT JOIN _info_punto_lindero_externos ON {LC_PLOT_T}.{T_ID_F} = _info_punto_lindero_externos.{MORE_BFS_T_LC_PLOT_F}
                LEFT JOIN _info_punto_lindero_internos ON {LC_PLOT_T}.{T_ID_F} = _info_punto_lindero_internos.{LESS_BFS_T_LC_PLOT_F}
                LEFT JOIN _info_puntolevantamiento ON {LC_PLOT_T}.{T_ID_F} = _info_puntolevantamiento._t_id_terreno_
                WHERE {LC_PLOT_T}.{T_ID_F} IN (SELECT * FROM _terrenos_seleccionados)
              ORDER BY {LC_PLOT_T}.{T_ID_F}
             )
             SELECT JSON_BUILD_OBJECT('{LC_PLOT_T}', COALESCE(JSON_AGG(_info_terreno._terreno_), '[]')) FROM _info_terreno
    """

    query = query.format(**vars(names),  # Custom keys are searched in Table And Field Names object
                         schema=schema,
                         custom_filter_plots=custom_filter_plots,
                         custom_filter_parcels=custom_filter_parcels,
                         parcel_fmi=parcel_fmi,
                         parcel_number=parcel_number,
                         previous_parcel_number=previous_parcel_number)
    return query
