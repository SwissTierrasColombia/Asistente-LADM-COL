def get_ant_map_query (schema, where_id):
    query = """with
				terrenos_seleccionados AS (
					(SELECT terreno.t_id as ue_terreno from {schema}.terreno {where_id}) --12425  12424 12005 12584 13499
				),
				predios_seleccionados AS (
					SELECT uebaunit.baunit_predio as t_id FROM {schema}.uebaunit WHERE uebaunit.ue_terreno in (SELECT terreno.t_id as ue_terreno from {schema}.terreno {where_id})
				),
				derechos_seleccionados AS (
					SELECT DISTINCT col_derecho.t_id FROM {schema}.col_derecho WHERE col_derecho.unidad_predio IN (SELECT * FROM predios_seleccionados)
				),
				derecho_interesados AS (
					SELECT DISTINCT col_derecho.interesado_col_interesado, col_derecho.t_id, col_derecho.unidad_predio as predio_t_id FROM {schema}.col_derecho WHERE col_derecho.t_id IN (SELECT * FROM derechos_seleccionados) AND col_derecho.interesado_col_interesado IS NOT NULL
				),
				derecho_agrupacion_interesados AS (
					SELECT DISTINCT col_derecho.interesado_la_agrupacion_interesados, miembros.interesados_col_interesado, miembros.agrupacion, col_derecho.unidad_predio as predio_t_id
					FROM {schema}.col_derecho LEFT JOIN {schema}.miembros ON col_derecho.interesado_la_agrupacion_interesados = miembros.agrupacion
					WHERE col_derecho.t_id IN (SELECT * FROM derechos_seleccionados) AND col_derecho.interesado_la_agrupacion_interesados IS NOT NULL
				),
				info_predio as (
					select
						predio.numero_predial as numero_predial
						,predio.u_local_id as local_id
						,predio.t_id
						from {schema}.predio where predio.t_id IN (SELECT * FROM predios_seleccionados)
				),
				info_agrupacion_filter as (
						select distinct on (agrupacion) agrupacion
						,col_interesado.p_local_id as local_id
						,predio_t_id
						,(case when col_interesado.t_id is not null then 'agrupacion' end) as agrupacion_interesado
						,(coalesce(col_interesado.primer_nombre,'') || coalesce(' ' || col_interesado.segundo_nombre, '') || coalesce(' ' || col_interesado.primer_apellido, '') || coalesce(' ' || col_interesado.segundo_apellido, '')
								|| coalesce(col_interesado.razon_social, '') ) as nombre
						from derecho_agrupacion_interesados LEFT JOIN {schema}.col_interesado ON col_interesado.t_id = derecho_agrupacion_interesados.interesados_col_interesado order by agrupacion
				),
				info_interesado as (
						select
						col_interesado.p_local_id as local_id
						,predio_t_id
						,(case when col_interesado.t_id is not null then 'interesado' end) as agrupacion_interesado
						,(coalesce(col_interesado.primer_nombre,'') || coalesce(' ' || col_interesado.segundo_nombre, '') || coalesce(' ' || col_interesado.primer_apellido, '') || coalesce(' ' || col_interesado.segundo_apellido, '')
								|| coalesce(col_interesado.razon_social, '') ) as nombre
						from derecho_interesados LEFT JOIN {schema}.col_interesado ON col_interesado.t_id = derecho_interesados.interesado_col_interesado
				),
				info_agrupacion as (
						select local_id
						,predio_t_id
						,agrupacion_interesado
						,nombre
						from info_agrupacion_filter
				),
				info_total_interesados as (select * from info_interesado union all select * from info_agrupacion)
				SELECT array_to_json(array_agg(features)) AS features
									FROM (
										SELECT f AS features
										FROM (
											SELECT 'Feature' AS type
												,row_to_json((
													SELECT l
													FROM (
														SELECT (left(right(info_predio.numero_predial,15),6) ||
									(CASE WHEN info_total_interesados.agrupacion_interesado = 'agrupacion'
									THEN COALESCE(' ' || 'AGRUPACIÓN DE ' || info_total_interesados.nombre || ' Y OTROS', ' INDETERMINADO')
									ELSE COALESCE(' ' || info_total_interesados.nombre, ' INDETERMINADO') END)) AS predio
														) AS l
													)) AS properties
												,ST_AsGeoJSON(terreno.poligono_creado)::json AS geometry
								FROM info_total_interesados
								join info_predio on info_predio.t_id = info_total_interesados.predio_t_id
								join {schema}.uebaunit on uebaunit.baunit_predio = info_total_interesados.predio_t_id
								join {schema}.terreno on terreno.t_id = uebaunit.ue_terreno
								) AS f
                             ) AS ff;""".format(schema=schema, where_id=where_id)

    return query