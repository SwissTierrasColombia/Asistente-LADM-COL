def get_ant_map_query (schema, where_id):
    query = """SELECT array_to_json(array_agg(features)) AS features
                    FROM (
                        SELECT f AS features
                        FROM (
                            SELECT 'Feature' AS type
                                ,row_to_json((
                                    SELECT l
                                    FROM (
                                        SELECT (left(right(numero_predial,15),6) || COALESCE(' ' || interesado, ' INDETERMINADO')) AS predio
                                        ) AS l
                                    )) AS properties
                                ,ST_AsGeoJSON(poligono_creado)::json AS geometry
                            FROM {schema}.terreno AS l
                            LEFT JOIN {schema}.uebaunit ON l.t_id = ue_terreno
                            LEFT JOIN {schema}.predio ON predio.t_id = baunit_predio
                            LEFT JOIN

                           (
                            SELECT t_id,
	                      array_to_string(array_agg(( coalesce(primer_nombre,'') || coalesce(' ' || segundo_nombre, '') || coalesce(' ' || primer_apellido, '') || coalesce(' ' || segundo_apellido, '') )
				                || ( coalesce(razon_social, '') )
				) , ' ')
			      as interesado
                            FROM
                           (
	                    --navegar agrupación de interesados
	                    SELECT * FROM
		                {schema}.predio
		                LEFT JOIN
		                (
			         select
			             primer_nombre
			             ,segundo_nombre
			             ,primer_apellido
			             ,segundo_apellido
			             ,razon_social
			             ,unidad_predio
			         from
			             {schema}.col_derecho
			             JOIN {schema}.la_agrupacion_interesados on la_agrupacion_interesados.t_id = interesado_la_agrupacion_interesados
			             JOIN {schema}.miembros on agrupacion = la_agrupacion_interesados.t_id
			             JOIN {schema}.col_interesado on col_interesado.t_id = miembros.interesados_col_interesado
		                 ) agrupacion  ON predio.t_id = agrupacion.unidad_predio
	                    UNION
	                    --navegar agrupación de interesados
	                    SELECT * FROM
		                {schema}.predio
		                 LEFT JOIN
		                (
			         select
			             primer_nombre
			             ,segundo_nombre
			             ,primer_apellido
			             ,segundo_apellido
			             ,razon_social
			             ,unidad_predio
			         from
			             {schema}.col_derecho
			             JOIN {schema}.col_interesado on col_interesado.t_id =interesado_col_interesado
		                 ) interesado ON predio.t_id = interesado.unidad_predio
                               ) interesados
                                   group by t_id
                            ) interesados on interesados.t_id = predio.t_id

                                {where_id}
                               ) AS f
                             ) AS ff;""".format(schema=schema, where_id=where_id)

    return query