def get_ant_map_query(names, schema, where_id):
    query = """WITH
				_terrenos_seleccionados AS (
					(SELECT lc_terreno.{T_ID_F} AS ue_terreno FROM {schema}.{LC_PLOT_T} {where_id})
				),
				_predios_seleccionados AS (
					SELECT {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_PARCEL_F} AS {T_ID_F} FROM {schema}.{COL_UE_BAUNIT_T} WHERE {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F} IN (SELECT {LC_PLOT_T}.{T_ID_F} AS ue_terreno FROM {schema}.{LC_PLOT_T} {where_id})
				),
				_derechos_seleccionados AS (
					SELECT DISTINCT {LC_RIGHT_T}.{T_ID_F} FROM {schema}.{LC_RIGHT_T} WHERE {LC_RIGHT_T}.{COL_BAUNIT_RRR_T_UNIT_F} IN (SELECT * FROM _predios_seleccionados)
				),
				_derecho_interesados AS (
					SELECT DISTINCT {LC_RIGHT_T}.{COL_RRR_PARTY_T_LC_PARTY_F}, {LC_RIGHT_T}.{T_ID_F}, {LC_RIGHT_T}.{COL_BAUNIT_RRR_T_UNIT_F} AS predio_t_id FROM {schema}.{LC_RIGHT_T} WHERE {LC_RIGHT_T}.{T_ID_F} IN (SELECT * FROM _derechos_seleccionados) AND {LC_RIGHT_T}.{COL_RRR_PARTY_T_LC_PARTY_F} IS NOT NULL
				),
				_derecho_agrupacion_interesados AS (
					SELECT DISTINCT {LC_RIGHT_T}.{COL_RRR_PARTY_T_LC_GROUP_PARTY_F}, {MEMBERS_T}.{MEMBERS_T_PARTY_F}, {MEMBERS_T}.{MEMBERS_T_GROUP_PARTY_F}, {LC_RIGHT_T}.{COL_BAUNIT_RRR_T_UNIT_F} AS predio_t_id
					FROM {schema}.{LC_RIGHT_T} LEFT JOIN {schema}.{MEMBERS_T} ON {LC_RIGHT_T}.{COL_RRR_PARTY_T_LC_GROUP_PARTY_F} = {MEMBERS_T}.{MEMBERS_T_GROUP_PARTY_F}
					WHERE {LC_RIGHT_T}.{T_ID_F} IN (SELECT * FROM _derechos_seleccionados) AND {LC_RIGHT_T}.{COL_RRR_PARTY_T_LC_GROUP_PARTY_F} IS NOT NULL
				),
				_info_predio AS (
					SELECT
						{LC_PARCEL_T}.{LC_PARCEL_T_PARCEL_NUMBER_F}
						,{LC_PARCEL_T}.{OID_T_LOCAL_ID_F}
						,{LC_PARCEL_T}.{T_ID_F}
						FROM {schema}.{LC_PARCEL_T} WHERE {LC_PARCEL_T}.{T_ID_F} IN (SELECT * FROM _predios_seleccionados)
				),
				_info_agrupacion_filter AS (
						SELECT distinct on ({MEMBERS_T_GROUP_PARTY_F}) {MEMBERS_T_GROUP_PARTY_F}
						,{LC_PARTY_T}.{OID_T_LOCAL_ID_F}
						,predio_t_id
						,(case when {LC_PARTY_T}.{T_ID_F} is not null then 'agrupacion' end) AS agrupacion_interesado
						,(coalesce({LC_PARTY_T}.{LC_PARTY_T_FIRST_NAME_1_F},'') || coalesce(' ' || {LC_PARTY_T}.{LC_PARTY_T_FIRST_NAME_2_F}, '') || coalesce(' ' || {LC_PARTY_T}.{LC_PARTY_T_SURNAME_1_F}, '') || coalesce(' ' || {LC_PARTY_T}.{LC_PARTY_T_SURNAME_2_F}, '')
								|| coalesce({LC_PARTY_T}.{LC_PARTY_T_BUSINESS_NAME_F}, '') ) AS nombre
						FROM _derecho_agrupacion_interesados LEFT JOIN {schema}.{LC_PARTY_T} ON {LC_PARTY_T}.{T_ID_F} = _derecho_agrupacion_interesados.{MEMBERS_T_PARTY_F} order by {MEMBERS_T_GROUP_PARTY_F}
				),
				_info_interesado AS (
						SELECT
						{LC_PARTY_T}.{OID_T_LOCAL_ID_F}
						,predio_t_id
						,(case when {LC_PARTY_T}.{T_ID_F} is not null then 'interesado' end) AS agrupacion_interesado
						,(coalesce({LC_PARTY_T}.{LC_PARTY_T_FIRST_NAME_1_F},'') || coalesce(' ' || {LC_PARTY_T}.{LC_PARTY_T_FIRST_NAME_2_F}, '') || coalesce(' ' || {LC_PARTY_T}.{LC_PARTY_T_SURNAME_1_F}, '') || coalesce(' ' || {LC_PARTY_T}.{LC_PARTY_T_SURNAME_2_F}, '')
								|| coalesce({LC_PARTY_T}.{LC_PARTY_T_BUSINESS_NAME_F}, '') ) AS nombre
						FROM _derecho_interesados LEFT JOIN {schema}.{LC_PARTY_T} ON {LC_PARTY_T}.{T_ID_F} = _derecho_interesados.{COL_RRR_PARTY_T_LC_PARTY_F}
				),
				_info_agrupacion AS (
						SELECT {OID_T_LOCAL_ID_F}
						,predio_t_id
						,agrupacion_interesado
						,nombre
						FROM _info_agrupacion_filter
				),
				_info_total_interesados AS (SELECT * FROM _info_interesado union all SELECT * FROM _info_agrupacion)
				SELECT array_to_json(array_agg(features)) AS features
									FROM (
										SELECT f AS features
										FROM (
											SELECT 'Feature' AS type
												,row_to_json((
													SELECT l
													FROM (
														SELECT (left(right(_info_predio.{LC_PARCEL_T_PARCEL_NUMBER_F},15),6) ||
									(CASE WHEN _info_total_interesados.agrupacion_interesado = 'agrupacion'
									THEN COALESCE(' ' || 'AGRUPACIÓN DE ' || _info_total_interesados.nombre || ' Y OTROS', ' INDETERMINADO')
									ELSE COALESCE(' ' || _info_total_interesados.nombre, ' INDETERMINADO') END)) AS predio
														) AS l
													)) AS properties
												,ST_AsGeoJSON({LC_PLOT_T}.{LC_PLOT_T_GEOMETRY_F},4,0)::json AS geometry
								FROM _info_total_interesados
								join _info_predio on _info_predio.{T_ID_F} = _info_total_interesados.predio_t_id
								join {schema}.{COL_UE_BAUNIT_T} on {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_PARCEL_F} = _info_total_interesados.predio_t_id
								join {schema}.{LC_PLOT_T} on {LC_PLOT_T}.{T_ID_F} = {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F}
								) AS f
                             ) AS ff;""".format(**vars(names),  # Custom keys are searched in Table And Field Names object
                                                schema=schema,
                                                where_id=where_id)

    return query