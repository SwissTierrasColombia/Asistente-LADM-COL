def get_ant_map_neighbouring_change_query(names, schema, where_id):
    query = """WITH
                    parametros AS (
                        SELECT
                            1 		AS criterio_punto_inicial, --tipo de criterio para seleccionar el punto inicial del terreno, valores posibles: 1,2
                            4		AS criterio_observador, --1: Centroide, 2: Centro del extent, 3: punto en la superficie, 4: Punto mas cercano al centroide dentro del poligono
                            15		as tolerancia_sentidos --tolerancia en grados para la definicion del sentido de una linea
                            ),
                            t AS ( --Orienta los vertices del terreno en sentido horario
	                        SELECT t_id, ST_ForceRHR(geometria) as geometria FROM {schema}.lc_terreno AS t, parametros {where_id}
                                ),
                            --bordes de la extension del poligono
                            a AS (
	                        SELECT ST_SetSRID(ST_MakePoint(st_xmin(t.geometria), st_ymax(t.geometria)), ST_SRID(t.geometria)) AS p FROM t
                            ),
                            b AS (
                                SELECT ST_SetSRID(ST_MakePoint(st_xmax(t.geometria), st_ymax(t.geometria)), ST_SRID(t.geometria)) AS p FROM t
                            ),
                            c AS (
                                SELECT ST_SetSRID(ST_MakePoint(st_xmax(t.geometria), st_ymin(t.geometria)), ST_SRID(t.geometria)) AS p FROM t
                            ),
                            d AS (
                                SELECT ST_SetSRID(ST_MakePoint(st_xmin(t.geometria), st_ymin(t.geometria)), ST_SRID(t.geometria)) AS p FROM t
                            ),
                            --Punto medio (ubicación del observador para la definicion de las cardinalidades)
                            m AS (
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
                                END as p
                                FROM parametros
                            ),
                            --Cuadrantes del polígono desde el observador a cada una de las esquinas de la extensión del polígono
                            norte AS (
                                SELECT ST_SetSRID(ST_MakePolygon(ST_MakeLine(ARRAY [a.p, b.p, m.p, a.p])), ST_SRID(t.geometria)) geom FROM t,a,b,m
                            ),
                            este AS (
                                SELECT ST_SetSRID(ST_MakePolygon(ST_MakeLine(ARRAY [m.p, b.p, c.p, m.p])), ST_SRID(t.geometria)) geom FROM t,b,c,m
                            ),
                            sur AS (
                                SELECT ST_SetSRID(ST_MakePolygon(ST_MakeLine(ARRAY [m.p, c.p, d.p, m.p])), ST_SRID(t.geometria)) geom FROM t,m,c,d
                            ),
                            oeste AS (
                                SELECT ST_SetSRID(ST_MakePolygon(ST_MakeLine(ARRAY [a.p, m.p, d.p, a.p])), ST_SRID(t.geometria)) geom FROM t,a,m,d
                            )
                            ,limite_poligono as(
                                SELECT t_id, ST_Boundary(geometria) geom FROM t
                            )
                            ,limite_vecinos as (  --obtiene el limite de los terrenos colindantes, filtrados por bounding box
                                select o.t_id, ST_Boundary(o.geometria) geom from t, {schema}.lc_terreno o where o.geometria && st_envelope(t.geometria) and t.t_id <> o.t_id
                            )
                            ,pre_colindancias as ( --inteseccion entre el limite del poligono y los terrenos cercanos, añade la geometria de los limites sin adjacencia
                                SELECT limite_vecinos.t_id, st_intersection(limite_poligono.geom,limite_vecinos.geom) geom  FROM limite_poligono,limite_vecinos where st_intersects(limite_poligono.geom,limite_vecinos.geom) and limite_poligono.t_id <> limite_vecinos.t_id
                                union
                                SELECT null as t_id, ST_Difference(limite_poligono.geom, a.geom) geom
                                FROM limite_poligono,
                                (
                                    select ST_LineMerge(ST_Union(geom)) geom from limite_vecinos
                                ) a
                            )
                            , tmp_colindantes as (
                                select  t_id,ST_LineMerge(ST_Union(geom)) geom from
                                (
                                    SELECT
                                    simple.t_id,
                                    simple.simple_geom as geom,
                                    ST_GeometryType(simple.simple_geom) as geom_type,
                                    ST_AsEWKT(simple.simple_geom) as geom_wkt
                                    FROM (
                                    SELECT
                                        dumped.*,
                                        (dumped.geom_dump).geom as simple_geom,
                                        (dumped.geom_dump).path as path
                                    FROM (
                                        SELECT *, ST_Dump(geom) AS geom_dump FROM pre_colindancias
                                    ) as dumped
                                    ) AS simple

                                ) a
                                group by t_id
                            )
                            , lineas_colindancia as ( --contiene las lineas de cambio de colindancia todas las lineas son parte simple
                                SELECT * FROM
                                (
                                    SELECT
                                    simple.t_id,
                                    simple.simple_geom as geom
                                    FROM (
                                    SELECT
                                        dumped.*,
                                        (dumped.geom_dump).geom as simple_geom,
                                        (dumped.geom_dump).path as path
                                    FROM (
                                        SELECT *, ST_Dump(geom) AS geom_dump FROM (select * from tmp_colindantes where ST_GeometryType(geom) = 'ST_MultiLineString') a
                                    ) as dumped
                                    ) AS simple
                                ) a
                                UNION
                                select * from tmp_colindantes where ST_GeometryType(geom) <> 'ST_MultiLineString'
                            )
                            , puntos_terreno as (
                                SELECT (ST_DumpPoints(geometria)).* AS dp
                                FROM t
                            )
                            --Criterio 1: el punto inicial del terreno es el primer punto del lindero que intersecte con el punto ubicado mas cerca de la esquina nw del polígono
                            , punto_nw as (
                                SELECT 	geom
                                    ,st_distance(geom, nw) AS dist
                                FROM 	puntos_terreno,
                                    (SELECT ST_SetSRID(ST_MakePoint(st_xmin(st_envelope(geometria)), st_ymax(st_envelope(geometria))), ST_SRID(geometria)) as nw FROM t ) a
                                ORDER BY dist limit 1
                            )
                            , punto_inicial_por_lindero_con_punto_nw as (
                                select st_startpoint(lineas_colindancia.geom) geom from lineas_colindancia, punto_nw where st_intersects(lineas_colindancia.geom, punto_nw.geom ) and not st_intersects(st_endpoint(lineas_colindancia.geom), punto_nw.geom )  limit 1
                            )

                            --Criterio 2: el punto inicial del terreno es el primer punto del lindero que tenga mayor porcentaje de su longitud sobre el cuadrante norte del poligono
                            , punto_inicial_por_lindero_porcentaje_n as(
                                select 	round((st_length(st_intersection(lineas_colindancia.geom, norte.geom))/st_length(lineas_colindancia.geom))::numeric,2) dist,
                                    st_startpoint(lineas_colindancia.geom) geom
                                    ,st_distance(lineas_colindancia.geom,nw) distance_to_nw
                                    from lineas_colindancia
                                        ,norte
                                        ,(SELECT ST_SetSRID(ST_MakePoint(st_xmin(st_envelope(geometria)), st_ymax(st_envelope(geometria))), ST_SRID(geometria)) as nw FROM t ) a
                                    where st_intersects(lineas_colindancia.geom, norte.geom)  order by dist desc, distance_to_nw
                                    limit 1
                            )
                            --Criterio para definir el punto inicial del terreno
                            ,punto_inicial as (
                                SELECT
                                    CASE WHEN criterio_punto_inicial = 1 THEN (select geom from punto_inicial_por_lindero_con_punto_nw)
                                    WHEN criterio_punto_inicial = 2 THEN (select geom from punto_inicial_por_lindero_porcentaje_n)
                                END as geom
                                FROM parametros
                            )
                            , puntos_ordenados as (
                                SELECT case when id-m+1 <= 0 then total + id-m else id-m+1 end as id, geom , st_x(geom) x, st_y(geom) y FROM
                                    (
                                    SELECT row_number() OVER (ORDER BY path) AS id
                                        ,m
                                        ,path
                                        ,geom
                                        ,total
                                    FROM (
                                        SELECT (ST_DumpPoints(ST_ForceRHR(geometria))).* AS dp
                                            ,ST_NPoints(geometria) total
                                            ,geometria
                                        FROM t
                                        ) AS a
                                        ,(
                                            SELECT row_number() OVER (ORDER BY path) AS m
                                                ,st_distance(puntos_terreno.geom, punto_inicial.geom) AS dist
                                            FROM puntos_terreno,punto_inicial
                                            ORDER BY dist limit 1
                                        ) b
                                    ) t
                                    where id <> total
                                order by id
                            )
                            , cuadrantes as (
                                SELECT '1_Norte' ubicacion,norte.geom as cuadrante FROM norte
                                UNION
                                SELECT '2_Este' ubicacion,este.geom as cuadrante FROM este
                                UNION
                                SELECT '3_Sur' ubicacion,sur.geom as cuadrante FROM sur
                                UNION
                                SELECT '4_Oeste' ubicacion,oeste.geom as cuadrante FROM oeste
                            )
                            , lineas_colindancia_desde_hasta as (
                                select *
                                    ,(SELECT id from puntos_ordenados WHERE st_intersects(puntos_ordenados.geom, st_startpoint(lineas_colindancia.geom))) desde
                                    ,(SELECT id from puntos_ordenados WHERE st_intersects(puntos_ordenados.geom, st_endpoint(lineas_colindancia.geom))) hasta
                                from lineas_colindancia
                                order by desde
                            )
                            , colindantes as (
                                SELECT row_number() OVER (ORDER BY desde) AS id, t_id,desde,hasta,ubicacion,geom FROM
                                (
                                    select *
                                        ,st_length(st_intersection(geom,cuadrante))/st_length(geom) as porcentaje
                                        ,max(st_length(st_intersection(geom,cuadrante))/st_length(geom)) over (partition by geom) as max_porce
                                    from lineas_colindancia_desde_hasta, cuadrantes where st_intersects(geom,cuadrante)
                                ) a
                                where porcentaje = max_porce
                            )
                            SELECT array_to_json(array_agg(features)) AS features
                                                FROM (
                                                    SELECT f AS features
                                                FROM (
                                        SELECT 'Feature' AS type
                                                            ,row_to_json((
                                                                SELECT l
                                                                FROM (
                                                                    SELECT ROUND(st_length(lineas_colindancia.geom)::numeric, 2) AS longitud
                                                                    ) AS l
                                                                )) AS properties

                            ,ST_AsGeoJSON(lineas_colindancia.geom)::json AS geometry FROM lineas_colindancia) as f) as ff""".format(**vars(names),  # Custom keys are searched in Table And Field Names object
                                                                                                                                    schema=schema,
                                                                                                                                    where_id=where_id)
    return query