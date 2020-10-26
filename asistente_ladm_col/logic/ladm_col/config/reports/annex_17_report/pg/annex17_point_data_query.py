def get_annex17_point_data_query(names, schema, plot_id):
    query = """WITH
        parametros AS (
          SELECT
            {plot_id} 	AS terreno_t_id,
             2 		AS criterio_punto_inicial, --tipo de criterio para seleccionar el punto inicial del terreno, valores posibles: 1,2 parametrizar
             4		AS criterio_observador --1: Centroide, 2: Centro del extent, 3: punto en la superficie, 4: Punto mas cercano al centroide dentro del poligono
        ),
        t AS (
            SELECT {T_ID_F}, ST_ForceRHR({LC_PLOT_T_GEOMETRY_F}) AS geometria FROM {schema}.{LC_PLOT_T} WHERE {T_ID_F} = (SELECT terreno_t_id FROM parametros)
        ),
        linderos AS (
            SELECT {LC_BOUNDARY_T}.{T_ID_F}, {LC_BOUNDARY_T}.{COL_BFS_T_GEOMETRY_F} AS geom  FROM {schema}.{LC_BOUNDARY_T} JOIN {schema}.{MORE_BFS_T} ON {MORE_BFS_T}.{MORE_BFS_T_LC_PLOT_F} = (SELECT terreno_t_id FROM parametros) AND {LC_BOUNDARY_T}.{T_ID_F} = {MORE_BFS_T}.{MORE_BFS_T_LC_BOUNDARY_F}
        ),
        puntos_lindero AS (
            SELECT {LC_BOUNDARY_POINT_T}.{T_ID_F}, {LC_BOUNDARY_POINT_T}.{COL_POINT_T_ORIGINAL_LOCATION_F} AS geom FROM {schema}.{LC_BOUNDARY_POINT_T} JOIN {schema}.{POINT_BFS_T} ON {POINT_BFS_T}.{POINT_BFS_T_LC_BOUNDARY_F} IN (SELECT {T_ID_F} FROM linderos) AND {LC_BOUNDARY_POINT_T}.{T_ID_F} = {POINT_BFS_T}.{POINT_BFS_T_LC_BOUNDARY_POINT_F}
        ),
        puntos_terreno AS (
            SELECT (ST_DumpPoints(geometria)).* AS dp,
                    ST_NPoints(geometria) total
            FROM t
        ),
        --bordes de la extension del poligono
        punto_nw AS (
            SELECT ST_SetSRID(ST_MakePoint(st_xmin(t.geometria), st_ymax(t.geometria)), ST_SRID(t.geometria)) AS p FROM t
        ),
        punto_ne AS (
            SELECT ST_SetSRID(ST_MakePoint(st_xmax(t.geometria), st_ymax(t.geometria)), ST_SRID(t.geometria)) AS p FROM t
        ),
        --Punto medio (ubicación del observador para la definicion de las cardinalidades)
        punto_medio AS (
          SELECT
            CASE WHEN criterio_observador = 1 THEN --centroide del poligono
              ( SELECT ST_SetSRID(ST_MakePoint(st_x(ST_centroid(t.geometria)), st_y(ST_centroid(t.geometria))), ST_SRID(t.geometria)) AS p FROM t )
            WHEN criterio_observador = 2 THEN --Centro del extent
              ( SELECT ST_SetSRID(ST_MakePoint(st_x(ST_centroid(st_envelope(t.geometria))), st_y(ST_centroid(st_envelope(t.geometria)))), ST_SRID(t.geometria)) AS p FROM t )
            WHEN criterio_observador = 3 THEN --Punto en la superficie
              ( SELECT ST_SetSRID(ST_PointOnSurface(geometria), ST_SRID(t.geometria)) AS p FROM t )
            WHEN criterio_observador = 4 THEN --Punto mas cercano al centroide pero que se intersecte el poligono si esta fuera
              ( SELECT ST_SetSRID(ST_MakePoint(st_x( ST_ClosestPoint( geometria, ST_centroid(t.geometria))), st_y( ST_ClosestPoint( geometria,ST_centroid(t.geometria)))), ST_SRID(t.geometria)) AS p FROM t )
            ELSE --defecto: Centro del extent
              ( SELECT ST_SetSRID(ST_MakePoint(st_x(ST_centroid(st_envelope(t.geometria))), st_y(ST_centroid(st_envelope(t.geometria)))), ST_SRID(t.geometria)) AS p FROM t )
            END AS p
            FROM parametros
        ),
        cuadrante_norte AS (
            SELECT ST_SetSRID(ST_MakePolygon(ST_MakeLine(ARRAY [punto_nw.p, punto_ne.p, punto_medio.p, punto_nw.p])), ST_SRID(t.geometria)) geom FROM t, punto_nw, punto_ne, punto_medio
        ),
        punto_inicial_por_lindero_porcentaje_n AS(
            SELECT 	round((st_length(st_intersection(linderos.geom, cuadrante_norte.geom))/st_length(linderos.geom))::numeric,2) dist,
                st_startpoint(linderos.geom) geom
                ,st_distance(linderos.geom, punto_nw.p) distance_to_nw
                FROM linderos
                    ,cuadrante_norte
                    , punto_nw
                WHERE st_intersects(linderos.geom, cuadrante_norte.geom)  ORDER BY dist DESC, distance_to_nw
                LIMIT 1
        ),
        punto_inicial_por_lindero_con_punto_nw AS (
            SELECT 	geom,
                    st_distance(geom, nw) AS dist
            FROM puntos_terreno,
                (SELECT ST_SetSRID(ST_MakePoint(st_xmin(st_envelope(geometria)), st_ymax(st_envelope(geometria))), ST_SRID(geometria)) AS nw FROM t) a
            ORDER BY dist LIMIT 1
        ),
        punto_inicial AS (
            SELECT
                CASE WHEN criterio_punto_inicial = 1 THEN (SELECT geom FROM punto_inicial_por_lindero_con_punto_nw)
                WHEN criterio_punto_inicial = 2 THEN (SELECT geom FROM punto_inicial_por_lindero_porcentaje_n)
            END AS geom
            FROM parametros
        ),
        puntos_terreno_ordenados AS (
            SELECT CASE WHEN id-m+1 <= 0 THEN total + id-m ELSE id-m+1 END AS id, geom  FROM
                (
                SELECT row_number() OVER (ORDER BY path) AS id
                    ,m
                    ,path
                    ,geom
                    ,total
                FROM (
                    SELECT (ST_DumpPoints(geometria)).* AS dp
                        ,ST_NPoints(geometria) total
                        ,geometria
                    FROM t
                    ) AS a
                    ,(
                        SELECT row_number() OVER (ORDER BY path) AS m
                            ,st_distance(puntos_terreno.geom, punto_inicial.geom) AS dist
                        FROM puntos_terreno,punto_inicial
                        ORDER BY dist LIMIT 1
                    ) b
                ) t
                WHERE id <> total
            ORDER BY id
        ),
        puntos_lindero_ordenados AS (
            SELECT * FROM (
                SELECT DISTINCT ON ({T_ID_F}) {T_ID_F}, id, st_distance(puntos_lindero.geom, puntos_terreno_ordenados.geom) AS distance, puntos_lindero.geom, st_x(puntos_lindero.geom) x, st_y(puntos_lindero.geom) y
                FROM puntos_lindero, puntos_terreno_ordenados ORDER BY {T_ID_F}, distance
                LIMIT (SELECT count(DISTINCT {T_ID_F}) FROM puntos_lindero)
            ) tmp_puntos_lindero_ordenados ORDER BY id
        )
        SELECT array_to_json(array_agg(features)) AS features
        FROM (
            SELECT f AS features
            FROM (
                SELECT 'Feature' AS type
                ,ST_AsGeoJSON(geom)::json AS geometry
                ,row_to_json((
                        SELECT l
                        FROM (
                            SELECT id AS point_number
                            ) AS l
                        )) AS properties
            FROM puntos_lindero_ordenados order by id
            ) AS f
        ) AS ff;""".format(**vars(names),  # Custom keys are searched in Table And Field Names object
                           schema=schema,
                           plot_id=plot_id)

    return query
