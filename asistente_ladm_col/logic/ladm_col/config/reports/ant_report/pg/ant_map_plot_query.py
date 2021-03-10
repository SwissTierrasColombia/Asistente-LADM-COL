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
            limite_municipio AS (SELECT {CC_MUNICIPALITY_BOUNDARY_T_GEOMETRY_F} AS geom , {CC_MUNICIPALITY_BOUNDARY_T_NAME_MUNICIPALITY_F} as nombre_municipio FROM {schema}.{CC_MUNICIPALITY_BOUNDARY_T}
                                 WHERE {CC_MUNICIPALITY_BOUNDARY_T_GEOMETRY_F} && (SELECT ST_Expand(ST_Envelope({LC_PLOT_T_GEOMETRY_F}), {scale_zoom}) FROM {schema}.{LC_PLOT_T} WHERE {T_ID_F} = {plot_id}))
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


def get_map_boundaries(names, schema, plot_id):
    """
    Return road nomenclature info from reference cadastral cartography model
    :param names: Table and field mapping object
    :param schema: db schema name
    :param plot_id: t_id field from select plot
    :return: sql query
    """
    query = """
            WITH
            -- Se definen los parametos de la consulta
            parametros AS (
              SELECT
                {plot_id} 	AS terreno_t_id,
                 1 		AS criterio_punto_inicial, --tipo de criterio para seleccionar el punto inicial de la enumeración del terreno, valores posibles: 1 (punto mas cercano al noroeste), 2 (punto mas cercano al noreste)
                 4		AS criterio_observador, --1: Centroide, 2: Centro del extent, 3: punto en la superficie, 4: Punto mas cercano al centroide dentro del poligono
                true	AS incluir_tipo_derecho --Mostrar el tipo de derecho de cada interesado (booleano)
            ),
            -- Se orienta en terreno en el sentido de las manecillas del reloj
            t AS (
                SELECT {T_ID_F}, ST_ForceRHR({LC_PLOT_T_GEOMETRY_F}) AS geometria FROM {schema}.{LC_PLOT_T} WHERE {T_ID_F} = (SELECT terreno_t_id FROM parametros)
            ),
            -- Se obtienen los vertices del bbox del terreno general (multiparte)
            punto_nw_g AS (
                SELECT ST_SetSRID(ST_MakePoint(st_xmin(t.geometria), st_ymax(t.geometria)), ST_SRID(t.geometria)) AS p FROM t
            ),
            punto_ne_g AS (
                SELECT ST_SetSRID(ST_MakePoint(st_xmax(t.geometria), st_ymax(t.geometria)), ST_SRID(t.geometria)) AS p FROM t
            ),
            punto_se_g AS (
                SELECT ST_SetSRID(ST_MakePoint(st_xmax(t.geometria), st_ymin(t.geometria)), ST_SRID(t.geometria)) AS p FROM t
            ),
            punto_sw_g AS (
                SELECT ST_SetSRID(ST_MakePoint(st_xmin(t.geometria), st_ymin(t.geometria)), ST_SRID(t.geometria)) AS p FROM t
            ),
            -- Se obtiene el punto medio (ubicación del observador para la definicion de las cardinalidades) del terreno general (multiparte)
            punto_medio_g AS (
              SELECT
                CASE WHEN criterio_observador = 1 THEN  --centroide del poligono
                  ( SELECT ST_SetSRID(ST_MakePoint(st_x(ST_centroid(t.geometria)), st_y(ST_centroid(t.geometria))), ST_SRID(t.geometria)) AS p FROM t )
                WHEN criterio_observador = 2 THEN   --Centro del extent
                  ( SELECT ST_SetSRID(ST_MakePoint(st_x(ST_centroid(st_envelope(t.geometria))), st_y(ST_centroid(st_envelope(t.geometria)))), ST_SRID(t.geometria)) AS p FROM t )
                WHEN criterio_observador = 3 THEN  --Punto en la superficie
                  ( SELECT ST_SetSRID(ST_PointOnSurface(geometria), ST_SRID(t.geometria)) AS p FROM t )
                WHEN criterio_observador = 4 THEN  --Punto mas cercano al centroide pero que se intersecte el poligono si esta fuera
                  ( SELECT ST_SetSRID(ST_MakePoint(st_x( ST_ClosestPoint( geometria, ST_centroid(t.geometria))), st_y( ST_ClosestPoint( geometria,ST_centroid(t.geometria)))), ST_SRID(t.geometria)) AS p FROM t )
                ELSE  --defecto: Centro del extent
                  ( SELECT ST_SetSRID(ST_MakePoint(st_x(ST_centroid(st_envelope(t.geometria))), st_y(ST_centroid(st_envelope(t.geometria)))), ST_SRID(t.geometria)) AS p FROM t )
                END AS p
                FROM parametros
            ),
            -- Se cuadrantes del terreno general (multiparte)
            cuadrante_norte_g AS (
                SELECT ST_SetSRID(ST_MakePolygon(ST_MakeLine(ARRAY [punto_nw_g.p, punto_ne_g.p, punto_medio_g.p, punto_nw_g.p])), ST_SRID(t.geometria)) geom FROM t, punto_nw_g, punto_ne_g, punto_medio_g
            ),
            cuadrante_este_g AS (
                SELECT ST_SetSRID(ST_MakePolygon(ST_MakeLine(ARRAY [punto_medio_g.p, punto_ne_g.p, punto_se_g.p, punto_medio_g.p])), ST_SRID(t.geometria)) geom FROM t, punto_ne_g, punto_se_g, punto_medio_g
            ),
            cuadrante_sur_g AS (
                SELECT ST_SetSRID(ST_MakePolygon(ST_MakeLine(ARRAY [punto_medio_g.p, punto_se_g.p, punto_sw_g.p, punto_medio_g.p])), ST_SRID(t.geometria)) geom FROM t, punto_medio_g, punto_se_g, punto_sw_g
            ),
            cuadrante_oeste_g AS (
                SELECT ST_SetSRID(ST_MakePolygon(ST_MakeLine(ARRAY [punto_nw_g.p, punto_medio_g.p, punto_sw_g.p, punto_nw_g.p])), ST_SRID(t.geometria)) geom FROM t, punto_nw_g, punto_medio_g, punto_sw_g
            ),
            cuadrantes_g AS (
                SELECT 'Norte' ubicacion, geom AS cuadrante FROM cuadrante_norte_g
                UNION
                SELECT 'Este' ubicacion, geom AS cuadrante FROM cuadrante_este_g
                UNION
                SELECT 'Sur' ubicacion, geom AS cuadrante FROM cuadrante_sur_g
                UNION
                SELECT 'Oeste' ubicacion, geom AS cuadrante FROM cuadrante_oeste_g
            ),
            -- Se convierte la geometria multipoligono del terreno a partes simples
            t_simple AS (
                SELECT {T_ID_F}, (ST_Dump({LC_PLOT_T_GEOMETRY_F})).path[1] AS parte, ST_ForceRHR((ST_Dump({LC_PLOT_T_GEOMETRY_F})).geom) AS geom FROM {schema}.{LC_PLOT_T} WHERE {T_ID_F} = (SELECT terreno_t_id FROM parametros)
            ),
            -- Se ordenan las partes del terreno empezando por la más cercana a la esquina noroeste del terreno general
            t_simple_ordenado AS (
                SELECT row_number() OVER () AS parte, {T_ID_F}, geom
                FROM (
                    SELECT {T_ID_F}, geom, st_distance(t_simple.geom, punto_nw_g.p) AS dist FROM t_simple, punto_nw_g ORDER BY dist
                ) AS l
            ),
            -- Se obtienen los vertices del bbox de cada parte del terreno
            vertices_bbox_partes AS (
                SELECT t_simple_ordenado.*,
                   ST_SetSRID(ST_MakePoint(st_xmin(geom), st_ymax(geom)), ST_SRID(geom)) AS p_nw,
                   ST_SetSRID(ST_MakePoint(st_xmax(geom), st_ymax(geom)), ST_SRID(geom)) AS p_ne,
                   ST_SetSRID(ST_MakePoint(st_xmax(geom), st_ymin(geom)), ST_SRID(geom)) AS p_se,
                   ST_SetSRID(ST_MakePoint(st_xmin(geom), st_ymin(geom)), ST_SRID(geom)) AS p_sw,
                   CASE WHEN criterio_observador = 1 THEN  --centroide del poligono
                        ST_SetSRID(ST_MakePoint(st_x(ST_centroid(geom)), st_y(ST_centroid(geom))), ST_SRID(geom))
                    WHEN criterio_observador = 2 THEN  --Centro del extent
                        ST_SetSRID(ST_MakePoint(st_x(ST_centroid(st_envelope(geom))), st_y(ST_centroid(st_envelope(geom)))), ST_SRID(geom))
                    WHEN criterio_observador = 3 THEN  --Punto en la superficie
                        ST_SetSRID(ST_PointOnSurface(geom), ST_SRID(geom))
                    WHEN criterio_observador = 4 THEN  --Punto mas cercano al centroide pero que se intersecte el poligono si esta fuera
                        ST_SetSRID(ST_MakePoint(st_x(ST_ClosestPoint(geom, ST_centroid(geom))), st_y( ST_ClosestPoint(geom,ST_centroid(geom)))), ST_SRID(geom))
                    ELSE  --defecto: Centro del extent
                        ST_SetSRID(ST_MakePoint(st_x(ST_centroid(st_envelope(geom))), st_y(ST_centroid(st_envelope(geom)))), ST_SRID(geom))
                    END AS p_medio
                   FROM t_simple_ordenado, parametros
            ),
            -- Cuadrantes para cada una de las partes
            cuadrantes_partes AS (
                SELECT parte, 'Norte' AS ubicacion, ST_SetSRID(ST_MakePolygon(ST_MakeLine(ARRAY [p_nw, p_ne, p_medio, p_nw])), ST_SRID(geom)) AS cuadrante FROM vertices_bbox_partes
                union
                SELECT parte, 'Este' AS ubicacion, ST_SetSRID(ST_MakePolygon(ST_MakeLine(ARRAY [p_medio, p_ne, p_se, p_medio])), ST_SRID(geom)) AS cuadrante FROM vertices_bbox_partes
                union
                SELECT parte, 'Sur' AS ubicacion, ST_SetSRID(ST_MakePolygon(ST_MakeLine(ARRAY [p_medio, p_se, p_sw, p_medio])), ST_SRID(geom)) AS cuadrante FROM vertices_bbox_partes
                union
                SELECT parte, 'Oeste' AS ubicacion, ST_SetSRID(ST_MakePolygon(ST_MakeLine(ARRAY [p_nw, p_medio, p_sw, p_nw])), ST_SRID(geom)) AS cuadrante FROM vertices_bbox_partes
            ),
            -- Se obtienen linderos asociados a los linderos se utilizan las tablas topologicas
            linderos AS (
                SELECT {LC_BOUNDARY_T}.{T_ID_F}, {LC_BOUNDARY_T}.{COL_BFS_T_GEOMETRY_F} AS geom  FROM {schema}.{LC_BOUNDARY_T} JOIN {schema}.{MORE_BFS_T} ON {MORE_BFS_T}.{MORE_BFS_T_LC_PLOT_F} = (SELECT terreno_t_id FROM parametros) AND {LC_BOUNDARY_T}.{T_ID_F} = {MORE_BFS_T}.{MORE_BFS_T_LC_BOUNDARY_F}
            ),
            -- Se obtienen los terrenos asociados a los linderos del terreno seleccionado (Terrenos vecinos)
            terrenos_asociados_linderos AS (
                SELECT DISTINCT {MORE_BFS_T}.{MORE_BFS_T_LC_PLOT_F} AS t_id_terreno, {MORE_BFS_T}.{MORE_BFS_T_LC_BOUNDARY_F} AS t_id_lindero FROM {schema}.{MORE_BFS_T} WHERE {MORE_BFS_T}.{MORE_BFS_T_LC_BOUNDARY_F} IN (SELECT {T_ID_F} FROM linderos) AND {MORE_BFS_T}.{MORE_BFS_T_LC_PLOT_F} != (SELECT terreno_t_id FROM parametros)
            ),
            -- Puntos linderos asociados al terreno
            puntos_lindero AS (
                SELECT DISTINCT {LC_BOUNDARY_POINT_T}.{T_ID_F}, {LC_BOUNDARY_POINT_T}.{COL_POINT_T_ORIGINAL_LOCATION_F} AS geom FROM {schema}.{LC_BOUNDARY_POINT_T} JOIN {schema}.{POINT_BFS_T} ON {POINT_BFS_T}.{POINT_BFS_T_LC_BOUNDARY_F} IN (SELECT {T_ID_F} FROM linderos) AND {LC_BOUNDARY_POINT_T}.{T_ID_F} = {POINT_BFS_T}.{POINT_BFS_T_LC_BOUNDARY_POINT_F}
            ),
            puntos_terrenos_simple AS (
                SELECT DISTINCT ON (geom) geom, parte, orden, total
                FROM (
                    SELECT (ST_DumpPoints(geom)).geom geom, parte, (ST_DumpPoints(geom)).path[2] orden, ST_NPoints(geom) total FROM t_simple_ordenado ORDER BY geom, parte, orden
                ) AS puntos_terrenos_unicos
                ORDER BY geom, parte, orden
            ),
            -- Criterios para seleccionar el punto a partir del cual empiza la enumeración de los terrenos
            punto_inicial_por_lindero_con_punto_nw AS (
                SELECT DISTINCT ON (parte) parte, dist, orden AS punto_inicial, geom, 1 AS criterio FROM (
                    SELECT 	pts.geom, pts.parte, pts.orden, pts.total,
                            st_distance(pts.geom, vbp.p_nw) AS dist
                    FROM puntos_terrenos_simple AS pts JOIN vertices_bbox_partes AS vbp ON pts.parte = vbp.parte
                    ORDER BY dist
                ) punto_inicial_parte_nw ORDER BY parte, dist
            ),
            punto_inicial_por_lindero_con_punto_ne AS (
                SELECT DISTINCT ON (parte) parte, dist, orden AS punto_inicial, geom, 2 AS criterio FROM (
                    SELECT 	pts.geom, pts.parte, pts.orden, pts.total,
                            st_distance(pts.geom, vbp.p_ne) AS dist
                    FROM puntos_terrenos_simple AS pts JOIN vertices_bbox_partes AS vbp ON pts.parte = vbp.parte
                    ORDER BY dist
                ) punto_inicial_parte_ne ORDER BY parte, dist
            ),
            punto_inicial AS (
                SELECT *
                FROM (
                    SELECT *
                    FROM punto_inicial_por_lindero_con_punto_nw
                    UNION SELECT * FROM punto_inicial_por_lindero_con_punto_ne
                ) AS union_puntos_inicio
                WHERE criterio = (SELECT criterio_punto_inicial FROM parametros)
            ),
            -- Preordenación de los puntos terreno
            pre_puntos_terreno_ordenados AS (
                SELECT row_number() OVER (ORDER BY parte, reordenar) AS id, geom, parte FROM (
                    SELECT puntos_terrenos_simple.*, punto_inicial, CASE WHEN orden - punto_inicial >=0 THEN orden - punto_inicial +1 ELSE total - punto_inicial  + orden END AS reordenar
                    FROM puntos_terrenos_simple JOIN punto_inicial
                    ON puntos_terrenos_simple.parte = punto_inicial.parte
                    ORDER BY puntos_terrenos_simple.parte, puntos_terrenos_simple.orden
                ) AS puntos_ordenados_inicio ORDER BY parte, reordenar
            )
            ,
            -- Se define el punto inicial y final para cada parte
            punto_inicial_final_parte AS (
                SELECT parte, min(id) punto_inicial, max(id) punto_final FROM pre_puntos_terreno_ordenados GROUP BY parte
            ),
            -- Puntos terrenos ordenados
            puntos_terreno_ordenados AS (
                SELECT t1.*, t2.punto_inicial, punto_final FROM pre_puntos_terreno_ordenados AS t1 JOIN punto_inicial_final_parte AS t2 ON t1.parte = t2.parte
            ),
            puntos_lindero_ordenados AS (
                SELECT * FROM (
                    SELECT DISTINCT ON ({T_ID_F}) {T_ID_F}, id, st_distance(puntos_lindero.geom, puntos_terreno_ordenados.geom) AS distance, puntos_lindero.geom, round(st_x(puntos_lindero.geom)::numeric,2) x, round(st_y(puntos_lindero.geom)::numeric, 3) y, parte, punto_inicial, punto_final
                    FROM puntos_lindero, puntos_terreno_ordenados ORDER BY {T_ID_F}, distance
                    LIMIT (SELECT count({T_ID_F}) FROM puntos_lindero)
                ) tmp_puntos_lindero_ordenados ORDER BY id
            ),
            -- Se orientan cada uno de los linderos que conforman el terreno en el sentido de las manecillas del reloj
            nodo_inicial_lindero AS (
                SELECT {T_ID_F}, ST_PointN(geom, 1) AS geom FROM linderos
            ),
            nodo_inicial_mas_uno_lindero AS (
                SELECT {T_ID_F}, ST_PointN(geom, 2) AS geom FROM linderos
            ),
            dist_nodo_punto_lindero AS (
                SELECT DISTINCT ON(n_il.{T_ID_F}) n_il.{T_ID_F}, plo.id AS pn1, plo.parte, plo.punto_inicial, plo.punto_final
                FROM puntos_lindero_ordenados AS plo, nodo_inicial_lindero n_il
                ORDER BY n_il.{T_ID_F}, st_distance(plo.geom, n_il.geom)
            ),
            dist_nodo_punto_mas_uno_lindero AS (
                SELECT DISTINCT ON(nimul.{T_ID_F}) nimul.{T_ID_F}, plo.id AS pn2, plo.parte, plo.punto_inicial, plo.punto_final
                FROM puntos_lindero_ordenados AS plo, nodo_inicial_mas_uno_lindero nimul
                ORDER BY nimul.{T_ID_F}, st_distance(plo.geom, nimul.geom)
            ),
            pre_order_lindero AS (
                SELECT dn1.*, pn2 FROM dist_nodo_punto_lindero AS dn1 JOIN dist_nodo_punto_mas_uno_lindero AS dn2 ON dn1.{T_ID_F} = dn2.{T_ID_F}
            ),
            linderos_orientados AS (
                SELECT l.{T_ID_F},
                        CASE WHEN pn1=punto_final AND pn2=punto_inicial THEN geom
                             WHEN pn1=punto_inicial AND pn2=punto_final AND pn1 + 1 != pn2 THEN ST_Reverse(geom)
                             WHEN pn1 < pn2 THEN geom
                             ELSE ST_Reverse(geom)
                        END AS geom
                FROM pre_order_lindero pol JOIN linderos l ON pol.{T_ID_F} = l.{T_ID_F}
            ),
            -- Se obtienen la secuencia de nodos que conforman cada uno de los linderos
            nodos_lindero_ubicacion AS (
                SELECT DISTINCT ON (code) code, nl.{T_ID_F}, nl.path, x, y, id, parte FROM (
                    SELECT {T_ID_F} ||''|| (ST_DumpPoints(geom)).path[1] AS code,  {T_ID_F},
                       (ST_DumpPoints(geom)).path[1], (ST_DumpPoints(geom)).geom, ST_NumPoints(geom) AS numpoints FROM linderos_orientados
                ) AS nl, puntos_lindero_ordenados AS plo
                WHERE nl.path != 1 AND nl.path != numpoints
                ORDER BY code, st_distance(nl.geom, plo.geom)
            ),
            secuencia_nodos AS (
                SELECT {T_ID_F}, array_to_string(array_agg(nlu.id || ': N=' || round(y::numeric,2) || ', E=' || round(x::numeric,2) ), '; ') AS nodos
                FROM nodos_lindero_ubicacion AS nlu
                GROUP BY {T_ID_F}
            ),
            -- Se obtiene el punto incial de cada uno de los linderos
            -- Los linderos ya estan orientados siguiendo la orientación del terreno en el sentido de las manecillas del reloj
            linderos_punto_inicial AS (
                SELECT {T_ID_F}, st_startpoint(geom) AS geom FROM linderos_orientados
            ),
            linderos_punto_final AS (
                SELECT {T_ID_F}, st_endpoint(geom) AS geom FROM linderos_orientados
            ),
            lindero_punto_inicio_fin AS (
                SELECT lindero_punto_desde.{T_ID_F},  lindero_punto_desde.parte, desde, hasta  FROM (
                    SELECT DISTINCT ON(lpi.{T_ID_F}) lpi.{T_ID_F}, plo.id AS "desde", plo.parte FROM puntos_lindero_ordenados AS plo, linderos_punto_inicial lpi ORDER BY lpi.{T_ID_F}, st_distance(plo.geom, lpi.geom)
                ) AS lindero_punto_desde JOIN
                (
                    SELECT DISTINCT ON(lpf.{T_ID_F}) lpf.{T_ID_F}, plo.id AS "hasta" FROM puntos_lindero_ordenados AS plo, linderos_punto_final lpf ORDER BY lpf.{T_ID_F}, st_distance(plo.geom, lpf.geom)
                ) AS lindero_punto_hasta ON lindero_punto_desde.{T_ID_F} = lindero_punto_hasta.{T_ID_F}
                ORDER BY parte, desde, hasta
            ),
            linderos_desde_hasta AS (
                SELECT lpif.{T_ID_F}, geom, parte, desde, hasta FROM lindero_punto_inicio_fin AS lpif JOIN linderos_orientados AS lo ON lpif.{T_ID_F} = lo.{T_ID_F}
            ),
            linderos_colindantes AS (
                SELECT row_number() OVER (ORDER BY desde) AS id, {T_ID_F} AS t_id_linderos, desde, hasta, ubicacion, geom, parte FROM
                (
                    SELECT desde
                        ,{T_ID_F}
                        , hasta
                        , ubicacion
                        , geom
                        , ldh.parte
                        ,st_length(st_intersection(geom,cuadrante))/st_length(geom) AS porcentaje
                        ,max(st_length(st_intersection(geom,cuadrante))/st_length(geom)) OVER (partition BY geom) AS max_porce
                    FROM linderos_desde_hasta AS ldh JOIN cuadrantes_partes AS cp ON ldh.parte = cp.parte AND st_intersects(geom,  cuadrante)
                ) a
                WHERE porcentaje = max_porce
            ),
            colindantes AS (
                SELECT linderos_colindantes.*, terrenos_asociados_linderos.t_id_terreno  FROM linderos_colindantes LEFT JOIN terrenos_asociados_linderos ON linderos_colindantes.t_id_linderos = terrenos_asociados_linderos.t_id_lindero
            )
            SELECT array_to_json(array_agg(features)) AS features
            FROM (
                SELECT f AS features
                FROM (
                    SELECT 'Feature' AS type,
                    row_to_json((SELECT l FROM (SELECT id) AS l)) AS properties,
                    ST_AsGeoJSON(geom, 4, 0)::json AS geometry
                    FROM colindantes ORDER BY parte, id
                ) AS f)
            AS ff;
            """.format(**vars(names),  # Custom keys are searched in Table And Field Names object
                       schema=schema,
                       plot_id=plot_id)
    return query
