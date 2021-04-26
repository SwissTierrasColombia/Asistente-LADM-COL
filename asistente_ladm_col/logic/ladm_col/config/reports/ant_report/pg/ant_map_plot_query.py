def get_ant_map_query(names, schema, where_id):
    query = """
        WITH
        terrenos_seleccionados AS (
            SELECT {LC_PLOT_T}.{T_ID_F} AS ue_lc_terreno FROM {schema}.{LC_PLOT_T} {where_id}
        ),
        predios_seleccionados AS (
            SELECT {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_PARCEL_F} AS {T_ID_F} FROM {schema}.{COL_UE_BAUNIT_T} JOIN terrenos_seleccionados ON {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F} = terrenos_seleccionados.ue_lc_terreno
        ),
        derechos_seleccionados AS (
            SELECT DISTINCT {LC_RIGHT_T}.{T_ID_F} FROM {schema}.{LC_RIGHT_T} WHERE {LC_RIGHT_T}.{COL_BAUNIT_RRR_T_UNIT_F} IN (SELECT * FROM predios_seleccionados)
        ),
        derecho_interesados AS (
            SELECT DISTINCT {LC_RIGHT_T}.{COL_RRR_PARTY_T_LC_PARTY_F}, {LC_RIGHT_T}.{T_ID_F}, {LC_RIGHT_T}.{COL_BAUNIT_RRR_T_UNIT_F} AS predio_t_id FROM {schema}.{LC_RIGHT_T} WHERE {LC_RIGHT_T}.{T_ID_F} IN (SELECT * FROM derechos_seleccionados) AND {LC_RIGHT_T}.{COL_RRR_PARTY_T_LC_PARTY_F} IS NOT NULL 
        ),
        derecho_agrupacion_interesados AS (
            SELECT DISTINCT {LC_RIGHT_T}.{COL_RRR_PARTY_T_LC_GROUP_PARTY_F}, {MEMBERS_T}.{MEMBERS_T_PARTY_F}, {MEMBERS_T}.{MEMBERS_T_GROUP_PARTY_F}, {LC_RIGHT_T}.{COL_BAUNIT_RRR_T_UNIT_F} AS predio_t_id
            FROM {schema}.{LC_RIGHT_T} LEFT JOIN {schema}.{MEMBERS_T} ON {LC_RIGHT_T}.{COL_RRR_PARTY_T_LC_GROUP_PARTY_F} = {MEMBERS_T}.{MEMBERS_T_GROUP_PARTY_F}
            WHERE {LC_RIGHT_T}.{T_ID_F} IN (SELECT * FROM derechos_seleccionados) AND {LC_RIGHT_T}.{COL_RRR_PARTY_T_LC_GROUP_PARTY_F} IS NOT NULL 
        ),
        info_predio AS (
            SELECT
                {LC_PARCEL_T}.{LC_PARCEL_T_PARCEL_NUMBER_F} AS numero_predial
                ,{LC_PARCEL_T}.{T_ID_F}
                FROM {schema}.{LC_PARCEL_T} WHERE {LC_PARCEL_T}.{T_ID_F} IN (SELECT * FROM predios_seleccionados)
        ),
        info_agrupacion_filter AS (
            SELECT distinct on ({MEMBERS_T_GROUP_PARTY_F}) {MEMBERS_T_GROUP_PARTY_F}
            ,predio_t_id
            ,(case when {LC_PARTY_T}.{T_ID_F} is not null then 'agrupacion' end) AS agrupacion_interesado
            ,(coalesce({LC_PARTY_T}.{LC_PARTY_T_FIRST_NAME_1_F},'') || coalesce(' ' || {LC_PARTY_T}.{LC_PARTY_T_FIRST_NAME_2_F}, '') || coalesce(' ' || {LC_PARTY_T}.{LC_PARTY_T_SURNAME_1_F}, '') || coalesce(' ' || {LC_PARTY_T}.{LC_PARTY_T_SURNAME_2_F}, '')
                    || coalesce({LC_PARTY_T}.{LC_PARTY_T_BUSINESS_NAME_F}, '') ) AS nombre
            FROM derecho_agrupacion_interesados LEFT JOIN {schema}.{LC_PARTY_T} ON {LC_PARTY_T}.{T_ID_F} = derecho_agrupacion_interesados.{MEMBERS_T_PARTY_F} order by {MEMBERS_T_GROUP_PARTY_F}
        ),
        info_interesado AS (
            SELECT DISTINCT
            predio_t_id
            ,(case when {LC_PARTY_T}.{T_ID_F} is not null then 'interesado' end) AS agrupacion_interesado
            ,(coalesce({LC_PARTY_T}.{LC_PARTY_T_FIRST_NAME_1_F},'') || coalesce(' ' || {LC_PARTY_T}.{LC_PARTY_T_FIRST_NAME_2_F}, '') || coalesce(' ' || {LC_PARTY_T}.{LC_PARTY_T_SURNAME_1_F}, '') || coalesce(' ' || {LC_PARTY_T}.{LC_PARTY_T_SURNAME_2_F}, '')
                    || coalesce({LC_PARTY_T}.{LC_PARTY_T_BUSINESS_NAME_F}, '') ) AS nombre
            FROM derecho_interesados LEFT JOIN {schema}.{LC_PARTY_T} ON {LC_PARTY_T}.{T_ID_F} = derecho_interesados.{COL_RRR_PARTY_T_LC_PARTY_F} 
        ),
        info_agrupacion AS (
                SELECT predio_t_id
                ,agrupacion_interesado
                ,nombre
                FROM info_agrupacion_filter
        ),
        info_total_interesados AS (
            SELECT * FROM info_interesado
            UNION ALL
            SELECT * FROM info_agrupacion
        )
        SELECT array_to_json(array_agg(features)) AS features
        FROM (
        SELECT f AS features
        FROM (
            SELECT 'Feature' AS type ,row_to_json((
                SELECT l
                    FROM (
                        SELECT (left(right(info_predio.numero_predial,15),6) ||
                        (CASE WHEN info_total_interesados.agrupacion_interesado = 'agrupacion'
                        THEN COALESCE(' ' || info_total_interesados.nombre || ' Y OTROS', ' INDETERMINADO')
                        ELSE COALESCE(' ' || info_total_interesados.nombre, ' INDETERMINADO') END)) AS predio
                    ) AS l)) AS properties
                    ,ST_AsGeoJSON(terrenos.{LC_PLOT_T_GEOMETRY_F}, 4, 0)::json AS geometry
                FROM (SELECT * FROM {schema}.{LC_PLOT_T} where {T_ID_F} in (select ue_lc_terreno from terrenos_seleccionados)) AS terrenos
                LEFT JOIN {schema}.{COL_UE_BAUNIT_T} ON terrenos.{T_ID_F} = {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F}
                LEFT JOIN info_predio ON {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_PARCEL_F} = info_predio.{T_ID_F}
                LEFT JOIN info_total_interesados ON info_predio.{T_ID_F} = info_total_interesados.predio_t_id
            ) AS f
        ) AS ff;
    """.format(**vars(names),  # Custom keys are searched in Table And Field Names object
               schema=schema,
               where_id=where_id)

    return query


def get_municipality_boundary(names, schema, plot_id, overview):
    """
    Return municipality boundary info from reference cadastral cartography model
    :param names: Table and field mapping object
    :param schema: db schema name
    :param plot_id: t_id field from select plot
    :param overview: True if you want the info for the overview map or false for the general map.
                    Zoom level: 1000 overview map
                                100 map
    :return:
    """
    scale_zoom = 1000 if overview else 100
    query = """
            WITH
            limite_municipio AS (SELECT {CC_MUNICIPALITY_BOUNDARY_T_GEOMETRY_F} AS geom , {CC_MUNICIPALITY_BOUNDARY_T_CODE_MUNICIPALITY_F} || ' ' || {CC_MUNICIPALITY_BOUNDARY_T_NAME_MUNICIPALITY_F} as nombre_municipio FROM {schema}.{CC_MUNICIPALITY_BOUNDARY_T}
                                 WHERE {CC_MUNICIPALITY_BOUNDARY_T_GEOMETRY_F} && (SELECT ST_Expand(ST_Envelope({LC_PLOT_T_GEOMETRY_F}), {scale_zoom}) FROM {schema}.{LC_PLOT_T} WHERE {T_ID_F} = {plot_id}) AND
                                 NOT ST_Contains({CC_MUNICIPALITY_BOUNDARY_T_GEOMETRY_F}, (SELECT {LC_PLOT_T_GEOMETRY_F} FROM {schema}.{LC_PLOT_T} WHERE {T_ID_F} = {plot_id})))
            SELECT array_to_json(array_agg(features)) AS features
            FROM (
                SELECT f AS features
                FROM (
                    SELECT 'Feature' AS type,
                    row_to_json((SELECT l FROM (SELECT nombre_municipio) AS l)) AS properties,
                    ST_AsGeoJSON(geom, 4, 0)::json AS geometry
                    FROM limite_municipio
                ) AS f)
            AS ff;
            """.format(**vars(names),  # Custom keys are searched in Table And Field Names object
                       schema=schema,
                       scale_zoom=scale_zoom,
                       plot_id=plot_id)

    return query


def get_urban_limit(names, schema, plot_id, overview):
    """
    Return urban limit info from reference cadastral cartography model
    :param names: Table and field mapping object
    :param schema: db schema name
    :param plot_id: t_id field from select plot
    :param overview: True if you want the info for the overview map or false for the general map.
                    Scale Zoom level: 1000 overview map
                                      100 map
    :return:
    """
    scale_zoom = 1000 if overview else 100
    query = """
            WITH
            perimetro_urbano AS (
                SELECT {CC_URBAN_PERIMETER_T_GEOMETRY_F} AS geom, {CC_URBAN_PERIMETER_T_GEOGRAPHIC_NAME_F} as nombre_geografico FROM {schema}.{CC_URBAN_PERIMETER_T}
                WHERE {CC_URBAN_PERIMETER_T_GEOMETRY_F} && (SELECT ST_Expand(ST_Envelope({LC_PLOT_T_GEOMETRY_F}), {scale_zoom}) FROM {schema}.{LC_PLOT_T} WHERE {T_ID_F} = {plot_id})
            )
            SELECT array_to_json(array_agg(features)) AS features
            FROM (
                SELECT f AS features
                FROM (
                    SELECT 'Feature' AS type,
                    row_to_json((SELECT l FROM (SELECT nombre_geografico) AS l)) AS properties,
                    ST_AsGeoJSON(geom, 4, 0)::json AS geometry
                    FROM perimetro_urbano
                ) AS f)
            AS ff;
            """.format(**vars(names),  # Custom keys are searched in Table And Field Names object
                       schema=schema,
                       scale_zoom=scale_zoom,
                       plot_id=plot_id)
    return query


def get_road_nomenclature(names, schema, plot_id, overview):
    """
    Return road nomenclature info from reference cadastral cartography model
    :param names: Table and field mapping object
    :param schema: db schema name
    :param plot_id: t_id field from select plot
    :param overview: True if you want the info for the overview map or false for the general map.
                    Zoom level: 1000 overview map
                                100 map
    :return: sql query
    """
    scale_zoom = 1000 if overview else 100
    query = """
            WITH
            nomenclatura_vial AS (
                SELECT (SELECT {DISPLAY_NAME_F} FROM {schema}.{CC_ROAD_TYPE_D} WHERE {T_ID_F} = {CC_ROAD_NOMENCLATURE_T_ROAD_TYPE_F}) || ' ' || {CC_ROAD_NOMENCLATURE_T_ROAD_NUMBER_F} AS nombre, {CC_ROAD_NOMENCLATURE_T_GEOMETRY_F} AS geom FROM {schema}.{CC_ROAD_NOMENCLATURE_T}
                WHERE {CC_ROAD_NOMENCLATURE_T_GEOMETRY_F} && (SELECT ST_Expand(ST_Envelope({LC_PLOT_T_GEOMETRY_F}), {scale_zoom}) FROM {schema}.{LC_PLOT_T} WHERE {T_ID_F} = {plot_id})
            )
            SELECT array_to_json(array_agg(features)) AS features
            FROM (
                SELECT f AS features
                FROM (
                    SELECT 'Feature' AS type,
                    row_to_json((SELECT l FROM (SELECT nombre) AS l)) AS properties,
                    ST_AsGeoJSON(geom, 4, 0)::json AS geometry
                    FROM nomenclatura_vial
                ) AS f)
            AS ff;
            """.format(**vars(names),  # Custom keys are searched in Table And Field Names object
                       schema=schema,
                       scale_zoom=scale_zoom,
                       plot_id=plot_id)
    return query
