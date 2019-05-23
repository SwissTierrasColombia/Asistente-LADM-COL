def get_annex17_point_data_query (schema, plot_id):
    query = """WITH parametros
                    AS (
                    	SELECT {id} AS poligono_t_id
                    		,2 AS criterio_punto_inicial
                    		,4 AS criterio_observador
                    		,true AS incluir_tipo_derecho
                    	)
                    	,t
                    AS (
                    	SELECT t_id
                    		,ST_ForceRHR(poligono_creado) AS poligono_creado
                    	FROM {schema}.terreno AS t
                    		,parametros
                    	WHERE t.t_id = poligono_t_id
                    	)
                    	,a
                    AS (
                    	SELECT ST_SetSRID(ST_MakePoint(st_xmin(t.poligono_creado), st_ymax(t.poligono_creado)), ST_SRID(t.poligono_creado)) AS p
                    	FROM t
                    	)
                    	,b
                    AS (
                    	SELECT ST_SetSRID(ST_MakePoint(st_xmax(t.poligono_creado), st_ymax(t.poligono_creado)), ST_SRID(t.poligono_creado)) AS p
                    	FROM t
                    	)
                    	,c
                    AS (
                    	SELECT ST_SetSRID(ST_MakePoint(st_xmax(t.poligono_creado), st_ymin(t.poligono_creado)), ST_SRID(t.poligono_creado)) AS p
                    	FROM t
                    	)
                    	,d
                    AS (
                    	SELECT ST_SetSRID(ST_MakePoint(st_xmin(t.poligono_creado), st_ymin(t.poligono_creado)), ST_SRID(t.poligono_creado)) AS p
                    	FROM t
                    	)
                    	,m
                    AS (
                    	SELECT CASE
                    			WHEN criterio_observador = 1
                    				THEN (
                    						SELECT ST_SetSRID(ST_MakePoint(st_x(ST_centroid(t.poligono_creado)), st_y(ST_centroid(t.poligono_creado))), ST_SRID(t.poligono_creado)) AS p
                    						FROM t
                    						)
                    			WHEN criterio_observador = 2
                    				THEN (
                    						SELECT ST_SetSRID(ST_MakePoint(st_x(ST_centroid(st_envelope(t.poligono_creado))), st_y(ST_centroid(st_envelope(t.poligono_creado)))), ST_SRID(t.poligono_creado)) AS p
                    						FROM t
                    						)
                    			WHEN criterio_observador = 3
                    				THEN (
                    						SELECT ST_SetSRID(ST_PointOnSurface(poligono_creado), ST_SRID(t.poligono_creado)) AS p
                    						FROM t
                    						)
                    			WHEN criterio_observador = 4
                    				THEN (
                    						SELECT ST_SetSRID(ST_MakePoint(st_x(ST_ClosestPoint(poligono_creado, ST_centroid(t.poligono_creado))), st_y(ST_ClosestPoint(poligono_creado, ST_centroid(t.poligono_creado)))), ST_SRID(t.poligono_creado)) AS p
                    						FROM t
                    						)
                    			ELSE (
                    					SELECT ST_SetSRID(ST_MakePoint(st_x(ST_centroid(st_envelope(t.poligono_creado))), st_y(ST_centroid(st_envelope(t.poligono_creado)))), ST_SRID(t.poligono_creado)) AS p
                    					FROM t
                    					)
                    			END AS p
                    	FROM parametros
                    	)
                    	,norte
                    AS (
                    	SELECT ST_SetSRID(ST_MakePolygon(ST_MakeLine(ARRAY [a.p, b.p, m.p, a.p])), ST_SRID(t.poligono_creado)) geom
                    	FROM t
                    		,a
                    		,b
                    		,m
                    	)
                    	,este
                    AS (
                    	SELECT ST_SetSRID(ST_MakePolygon(ST_MakeLine(ARRAY [m.p, b.p, c.p, m.p])), ST_SRID(t.poligono_creado)) geom
                    	FROM t
                    		,b
                    		,c
                    		,m
                    	)
                    	,sur
                    AS (
                    	SELECT ST_SetSRID(ST_MakePolygon(ST_MakeLine(ARRAY [m.p, c.p, d.p, m.p])), ST_SRID(t.poligono_creado)) geom
                    	FROM t
                    		,m
                    		,c
                    		,d
                    	)
                    	,oeste
                    AS (
                    	SELECT ST_SetSRID(ST_MakePolygon(ST_MakeLine(ARRAY [a.p, m.p, d.p, a.p])), ST_SRID(t.poligono_creado)) geom
                    	FROM t
                    		,a
                    		,m
                    		,d
                    	)
                    	,limite_poligono
                    AS (
                    	SELECT t_id
                    		,ST_Boundary(poligono_creado) geom
                    	FROM t
                    	)
                    	,limite_vecinos
                    AS (
                    	SELECT o.t_id
                    		,ST_Boundary(o.poligono_creado) geom
                    	FROM t
                    		,{schema}.terreno o
                    	WHERE o.poligono_creado && st_envelope(t.poligono_creado)
                    		AND t.t_id <> o.t_id
                    	)
                    	,pre_colindancias
                    AS (
                    	SELECT limite_vecinos.t_id
                    		,st_intersection(limite_poligono.geom, limite_vecinos.geom) geom
                    	FROM limite_poligono
                    		,limite_vecinos
                    	WHERE st_intersects(limite_poligono.geom, limite_vecinos.geom)
                    		AND limite_poligono.t_id <> limite_vecinos.t_id

                    	UNION

                    	SELECT NULL AS t_id
                    		,ST_Difference(limite_poligono.geom, a.geom) geom
                    	FROM limite_poligono
                    		,(
                    			SELECT ST_LineMerge(ST_Union(geom)) geom
                    			FROM limite_vecinos
                    			) a
                    	)
                    	,tmp_colindantes
                    AS (
                    	SELECT t_id
                    		,ST_LineMerge(ST_Union(geom)) geom
                    	FROM (
                    		SELECT SIMPLE.t_id
                    			,SIMPLE.simple_geom AS geom
                    			,ST_GeometryType(SIMPLE.simple_geom) AS geom_type
                    			,ST_AsEWKT(SIMPLE.simple_geom) AS geom_wkt
                    		FROM (
                    			SELECT dumped.*
                    				,(dumped.geom_dump).geom AS simple_geom
                    				,(dumped.geom_dump).path AS path
                    			FROM (
                    				SELECT *
                    					,ST_Dump(geom) AS geom_dump
                    				FROM pre_colindancias
                    				) AS dumped
                    			) AS SIMPLE
                    		) a
                    	GROUP BY t_id
                    	)
                    	,lineas_colindancia
                    AS (
                    	SELECT *
                    	FROM (
                    		SELECT SIMPLE.t_id
                    			,SIMPLE.simple_geom AS geom
                    		FROM (
                    			SELECT dumped.*
                    				,(dumped.geom_dump).geom AS simple_geom
                    				,(dumped.geom_dump).path AS path
                    			FROM (
                    				SELECT *
                    					,ST_Dump(geom) AS geom_dump
                    				FROM (
                    					SELECT *
                    					FROM tmp_colindantes
                    					WHERE ST_GeometryType(geom) = 'ST_MultiLineString'
                    					) a
                    				) AS dumped
                    			) AS SIMPLE
                    		) a

                    	UNION

                    	SELECT *
                    	FROM tmp_colindantes
                    	WHERE ST_GeometryType(geom) <> 'ST_MultiLineString'
                    	)
                    	,puntos_terreno
                    AS (
                    	SELECT (ST_DumpPoints(poligono_creado)).* AS dp
                    	FROM t
                    	)
                    	,punto_nw
                    AS (
                    	SELECT geom
                    		,st_distance(geom, nw) AS dist
                    	FROM puntos_terreno
                    		,(
                    			SELECT ST_SetSRID(ST_MakePoint(st_xmin(st_envelope(poligono_creado)), st_ymax(st_envelope(poligono_creado))), ST_SRID(poligono_creado)) AS nw
                    			FROM t
                    			) a
                    	ORDER BY dist limit 1
                    	)
                    	,punto_inicial_por_lindero_con_punto_nw
                    AS (
                    	SELECT st_startpoint(lineas_colindancia.geom) geom
                    	FROM lineas_colindancia
                    		,punto_nw
                    	WHERE st_intersects(lineas_colindancia.geom, punto_nw.geom)
                    		AND NOT st_intersects(st_endpoint(lineas_colindancia.geom), punto_nw.geom) limit 1
                    	)
                    	,punto_inicial_por_lindero_porcentaje_n
                    AS (
                    	SELECT round((st_length(st_intersection(lineas_colindancia.geom, norte.geom)) / st_length(lineas_colindancia.geom))::NUMERIC, 2) dist
                    		,st_startpoint(lineas_colindancia.geom) geom
                    		,st_distance(lineas_colindancia.geom, nw) distance_to_nw
                    	FROM lineas_colindancia
                    		,norte
                    		,(
                    			SELECT ST_SetSRID(ST_MakePoint(st_xmin(st_envelope(poligono_creado)), st_ymax(st_envelope(poligono_creado))), ST_SRID(poligono_creado)) AS nw
                    			FROM t
                    			) a
                    	WHERE st_intersects(lineas_colindancia.geom, norte.geom)
                    	ORDER BY dist DESC
                    		,distance_to_nw limit 1
                    	)
                    	,punto_inicial
                    AS (
                    	SELECT CASE
                    			WHEN criterio_punto_inicial = 1
                    				THEN (
                    						SELECT geom
                    						FROM punto_inicial_por_lindero_con_punto_nw
                    						)
                    			WHEN criterio_punto_inicial = 2
                    				THEN (
                    						SELECT geom
                    						FROM punto_inicial_por_lindero_porcentaje_n
                    						)
                    			END AS geom
                    	FROM parametros
                    	)
                    	,puntos_ordenados
                    AS (
                    	SELECT CASE
                    			WHEN id - m + 1 <= 0
                    				THEN total + id - m
                    			ELSE id - m + 1
                    			END AS id
                    		,geom
                    		,st_x(geom) x
                    		,st_y(geom) y
                    	FROM (
                    		SELECT row_number() OVER (
                    				ORDER BY path
                    				) AS id
                    			,m
                    			,path
                    			,geom
                    			,total
                    		FROM (
                    			SELECT (ST_DumpPoints(ST_ForceRHR(poligono_creado))).* AS dp
                    				,ST_NPoints(poligono_creado) total
                    				,poligono_creado
                    			FROM t
                    			) AS a
                    			,(
                    				SELECT row_number() OVER (
                    						ORDER BY path
                    						) AS m
                    					,st_distance(puntos_terreno.geom, punto_inicial.geom) AS dist
                    				FROM puntos_terreno
                    					,punto_inicial
                    				ORDER BY dist limit 1
                    				) b
                    		) t
                    	WHERE id <> total
                    	ORDER BY id
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
                    		FROM puntos_ordenados
                    		) AS f
                    	) AS ff;""".format(schema=schema, id=plot_id)

    return query