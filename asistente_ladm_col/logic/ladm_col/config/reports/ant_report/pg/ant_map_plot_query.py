def get_ant_map_query (schema, where_id):
    query = """with
				terrenos_seleccionados AS (
					(SELECT op_terreno.t_id as ue_terreno from {schema}.op_terreno {where_id}) --12425  12424 12005 12584 13499
				),
				predios_seleccionados AS (
					SELECT col_uebaunit.baunit as t_id FROM {schema}.col_uebaunit WHERE col_uebaunit.ue_op_terreno in (SELECT op_terreno.t_id as ue_terreno from {schema}.op_terreno {where_id})
				),
				derechos_seleccionados AS (
					SELECT DISTINCT op_derecho.t_id FROM {schema}.op_derecho WHERE op_derecho.unidad IN (SELECT * FROM predios_seleccionados)
				),
				derecho_interesados AS (
					SELECT DISTINCT op_derecho.interesado_op_interesado, op_derecho.t_id, op_derecho.unidad as predio_t_id FROM {schema}.op_derecho WHERE op_derecho.t_id IN (SELECT * FROM derechos_seleccionados) AND op_derecho.interesado_op_interesado IS NOT NULL
				),
				derecho_agrupacion_interesados AS (
					SELECT DISTINCT op_derecho.interesado_op_agrupacion_interesados, col_miembros.interesado_op_interesado, col_miembros.agrupacion, op_derecho.unidad as predio_t_id
					FROM {schema}.op_derecho LEFT JOIN {schema}.col_miembros ON op_derecho.interesado_op_agrupacion_interesados = col_miembros.agrupacion
					WHERE op_derecho.t_id IN (SELECT * FROM derechos_seleccionados) AND op_derecho.interesado_op_agrupacion_interesados IS NOT NULL
				),
				info_predio as (
					select
						op_predio.numero_predial as numero_predial
						,op_predio.local_id as local_id
						,op_predio.t_id
						from {schema}.op_predio where op_predio.t_id IN (SELECT * FROM predios_seleccionados)
				),
				info_agrupacion_filter as (
						select distinct on (agrupacion) agrupacion
						,op_interesado.local_id as local_id
						,predio_t_id
						,(case when op_interesado.t_id is not null then 'agrupacion' end) as agrupacion_interesado
						,(coalesce(op_interesado.primer_nombre,'') || coalesce(' ' || op_interesado.segundo_nombre, '') || coalesce(' ' || op_interesado.primer_apellido, '') || coalesce(' ' || op_interesado.segundo_apellido, '')
								|| coalesce(op_interesado.razon_social, '') ) as nombre
						from derecho_agrupacion_interesados LEFT JOIN {schema}.op_interesado ON op_interesado.t_id = derecho_agrupacion_interesados.interesado_op_interesado order by agrupacion
				),
				info_interesado as (
						select
						op_interesado.local_id as local_id
						,predio_t_id
						,(case when op_interesado.t_id is not null then 'interesado' end) as agrupacion_interesado
						,(coalesce(op_interesado.primer_nombre,'') || coalesce(' ' || op_interesado.segundo_nombre, '') || coalesce(' ' || op_interesado.primer_apellido, '') || coalesce(' ' || op_interesado.segundo_apellido, '')
								|| coalesce(op_interesado.razon_social, '') ) as nombre
						from derecho_interesados LEFT JOIN {schema}.op_interesado ON op_interesado.t_id = derecho_interesados.interesado_op_interesado
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
												,ST_AsGeoJSON(op_terreno.geometria)::json AS geometry
								FROM info_total_interesados
								join info_predio on info_predio.t_id = info_total_interesados.predio_t_id
								join {schema}.col_uebaunit on col_uebaunit.baunit = info_total_interesados.predio_t_id
								join {schema}.op_terreno on op_terreno.t_id = col_uebaunit.ue_op_terreno
								) AS f
                             ) AS ff;""".format(schema=schema, where_id=where_id)

    return query