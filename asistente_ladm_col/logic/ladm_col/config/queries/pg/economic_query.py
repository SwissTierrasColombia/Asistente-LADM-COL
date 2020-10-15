from asistente_ladm_col.logic.ladm_col.config.queries.pg.pg_queries_config_utils import (get_custom_filter_parcels,
                                                                                         get_custom_filter_plots)


def get_igac_economic_query(names, schema, plot_t_ids, parcel_fmi, parcel_number, previous_parcel_number):
    custom_filter_plots = get_custom_filter_plots(names, schema, plot_t_ids)
    custom_filter_parcels = get_custom_filter_parcels(names, schema, plot_t_ids)

    query = """
        WITH
         _unidad_avaluo_predio AS (
             SELECT ' [' || setting || ']' FROM {schema}.t_ili2db_column_prop WHERE tablename LIKE '{LC_PARCEL_T}' AND columnname LIKE '{LC_PARCEL_T_VALUATION_F}' LIMIT 1
         ),
         _unidad_avaluo_terreno AS (
             SELECT ' [' || setting || ']' FROM {schema}.t_ili2db_column_prop WHERE tablename = '{LC_PLOT_T}' AND columnname = '{LC_PLOT_T_PLOT_VALUATION_F}' LIMIT 1
         ),
         _unidad_area_terreno AS (
             SELECT ' [' || setting || ']' FROM {schema}.t_ili2db_column_prop WHERE tablename = '{LC_PLOT_T}' AND columnname = '{LC_PLOT_T_PLOT_AREA_F}' LIMIT 1
         ),
         _unidad_avaluo_construccion AS (
             SELECT ' [' || setting || ']' FROM {schema}.t_ili2db_column_prop WHERE tablename = '{LC_BUILDING_T}' AND columnname = '{LC_BUILDING_T_BUILDING_VALUATION_F}' LIMIT 1
         ),
         _unidad_area_construida_uc AS (
             SELECT ' [' || setting || ']' FROM {schema}.t_ili2db_column_prop WHERE tablename = '{LC_BUILDING_UNIT_T}' AND columnname = '{LC_BUILDING_UNIT_T_BUILT_AREA_F}' LIMIT 1
         ),
         _unidad_avaluo_uc AS (
             SELECT ' [' || setting || ']' FROM {schema}.t_ili2db_column_prop WHERE tablename = '{LC_BUILDING_UNIT_T}' AND columnname = '{LC_BUILDING_UNIT_T_BUILDING_UNIT_VALUATION_F}' LIMIT 1
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
             SELECT {LC_BUILDING_UNIT_T}.{T_ID_F} FROM {schema}.{LC_BUILDING_UNIT_T} WHERE {LC_BUILDING_UNIT_T}.{LC_BUILDING_T} IN (SELECT {COL_UE_BAUNIT_T_LC_BUILDING_F} FROM _construcciones_seleccionadas)
         ),
         _info_uc AS (
             SELECT {LC_BUILDING_UNIT_T}.{LC_BUILDING_T},
                    JSON_AGG(JSON_BUILD_OBJECT('id', {LC_BUILDING_UNIT_T}.{T_ID_F},
                                      'attributes', JSON_BUILD_OBJECT(CONCAT('Avalúo' , (SELECT * FROM _unidad_avaluo_uc)), {LC_BUILDING_UNIT_T}.{LC_BUILDING_UNIT_T_BUILDING_UNIT_VALUATION_F}
                                                                      , CONCAT('Área construida' , (SELECT * FROM _unidad_area_construida_uc)), {LC_BUILDING_UNIT_T}.{LC_BUILDING_UNIT_T_BUILT_AREA_F}
                                                                      , CONCAT('Área privada construida' , (SELECT * FROM _unidad_area_construida_uc)), {LC_BUILDING_UNIT_T}.{LC_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F}
                                                                      , 'Número de pisos', {LC_BUILDING_UNIT_T}.{LC_BUILDING_UNIT_T_TOTAL_FLOORS_F}
                                                                      , 'Ubicación en el piso', {LC_BUILDING_UNIT_T}.{LC_BUILDING_UNIT_T_FLOOR_F}
                                                                      , 'Uso',  (SELECT {DISPLAY_NAME_F} FROM {schema}.{LC_BUILDING_UNIT_USE_D} WHERE {T_ID_F} = {LC_BUILDING_UNIT_T}.{LC_BUILDING_UNIT_T_USE_F})
                                                                      , 'Año construcción',  {LC_BUILDING_UNIT_T}.{LC_BUILDING_UNIT_T_YEAR_OF_BUILDING_F}
                                                                     )) ORDER BY {LC_BUILDING_UNIT_T}.{T_ID_F}) FILTER(WHERE {LC_BUILDING_UNIT_T}.{T_ID_F} IS NOT NULL)  AS _unidadconstruccion_
             FROM {schema}.{LC_BUILDING_UNIT_T}
             WHERE {LC_BUILDING_UNIT_T}.{T_ID_F} IN (SELECT * FROM _unidadesconstruccion_seleccionadas)
             GROUP BY {LC_BUILDING_UNIT_T}.{LC_BUILDING_T}
         ),
         _info_construccion AS (
             SELECT {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_PARCEL_F},
                    JSON_AGG(JSON_BUILD_OBJECT('id', {LC_BUILDING_T}.{T_ID_F},
                                      'attributes', JSON_BUILD_OBJECT(CONCAT('Avalúo' , (SELECT * FROM _unidad_avaluo_construccion)), {LC_BUILDING_T}.{LC_BUILDING_T_BUILDING_VALUATION_F},
                                                                      'Área construcción', {LC_BUILDING_T}.{LC_BUILDING_T_BUILDING_AREA_F},
                                                                      '{LC_BUILDING_UNIT_T}', COALESCE(_info_uc._unidadconstruccion_, '[]')
                                                                     )) ORDER BY {LC_BUILDING_T}.{T_ID_F}) FILTER(WHERE {LC_BUILDING_T}.{T_ID_F} IS NOT NULL) AS _construccion_
             FROM {schema}.{LC_BUILDING_T}
             LEFT JOIN _info_uc ON {LC_BUILDING_T}.{T_ID_F} = _info_uc.{LC_BUILDING_T}
             LEFT JOIN {schema}.{COL_UE_BAUNIT_T} ON {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_BUILDING_F} = {LC_BUILDING_T}.{T_ID_F}
             WHERE {LC_BUILDING_T}.{T_ID_F} IN (SELECT * FROM _construcciones_seleccionadas)
             GROUP BY {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_PARCEL_F}
         ),
        _info_predio AS (
             SELECT {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F},
                    JSON_AGG(JSON_BUILD_OBJECT('id', {LC_PARCEL_T}.{T_ID_F},
                                      'attributes', JSON_BUILD_OBJECT('Nombre', {LC_PARCEL_T}.{COL_BAUNIT_T_NAME_F},
                                                                      'Departamento', {LC_PARCEL_T}.{LC_PARCEL_T_DEPARTMENT_F},
                                                                      'Municipio', {LC_PARCEL_T}.{LC_PARCEL_T_MUNICIPALITY_F},
                                                                      'NUPRE', {LC_PARCEL_T}.{LC_PARCEL_T_NUPRE_F},
                                                                      'Id operación', {LC_PARCEL_T}.{LC_PARCEL_T_ID_OPERATION_F},
                                                                      'FMI', ({LC_PARCEL_T}.{LC_PARCEL_T_ORIP_CODE_F} || '-'|| {LC_PARCEL_T}.{LC_PARCEL_T_FMI_F}),
                                                                      'Número predial', {LC_PARCEL_T}.{LC_PARCEL_T_PARCEL_NUMBER_F},
                                                                      'Número predial anterior', {LC_PARCEL_T}.{LC_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F},
                                                                      CONCAT('Avalúo predio' , (SELECT * FROM _unidad_avaluo_predio)), {LC_PARCEL_T}.{LC_PARCEL_T_VALUATION_F},
                                                                      'Tipo', (SELECT {DISPLAY_NAME_F} FROM {schema}.{LC_PARCEL_TYPE_D} WHERE {T_ID_F} = {LC_PARCEL_T}.{LC_PARCEL_T_TYPE_F}),
                                                                      '{LC_BUILDING_T}', COALESCE(_info_construccion._construccion_, '[]')
                                                                     )) ORDER BY {LC_PARCEL_T}.{T_ID_F}) FILTER(WHERE {LC_PARCEL_T}.{T_ID_F} IS NOT NULL) AS _predio_
             FROM {schema}.{LC_PARCEL_T} LEFT JOIN {schema}.{COL_UE_BAUNIT_T} ON {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_PARCEL_F} = {LC_PARCEL_T}.{T_ID_F}
             LEFT JOIN _info_construccion ON {LC_PARCEL_T}.{T_ID_F} = _info_construccion.{COL_UE_BAUNIT_T_PARCEL_F}
             WHERE {LC_PARCEL_T}.{T_ID_F} IN (SELECT * FROM _predios_seleccionados)
             AND {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F} IS NOT NULL
             AND {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_BUILDING_F} IS NULL
             AND {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_BUILDING_UNIT_F} IS NULL
             GROUP BY {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F}
         ),
         _info_terreno AS (
            SELECT {LC_PLOT_T}.{T_ID_F},
              JSON_BUILD_OBJECT('id', {LC_PLOT_T}.{T_ID_F},
                                'attributes', JSON_BUILD_OBJECT(CONCAT('Avalúo', (SELECT * FROM _unidad_avaluo_terreno)), {LC_PLOT_T}.{LC_PLOT_T_PLOT_VALUATION_F}
                                                                , CONCAT('Área' , (SELECT * FROM _unidad_area_terreno)), {LC_PLOT_T}.{LC_PLOT_T_PLOT_AREA_F}
                                                                , '{LC_PARCEL_T}', COALESCE(_info_predio._predio_, '[]')
                                                               )) AS _terreno_
            FROM {schema}.{LC_PLOT_T} LEFT JOIN _info_predio ON _info_predio.{COL_UE_BAUNIT_T_LC_PLOT_F} = {LC_PLOT_T}.{T_ID_F}
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
