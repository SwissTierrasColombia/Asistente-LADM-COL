def get_ant_map_neighbouring_change_query(names, schema, plot_id):
    query = """WITH
                parametros AS (
                  SELECT
                    {plot_id} 	AS terreno_t_id
                ),
                t AS (
                    SELECT {T_ID_F}, ST_ForceRHR({LC_PLOT_T_GEOMETRY_F}) AS geometria FROM {schema}.{LC_PLOT_T} WHERE {T_ID_F} = (SELECT terreno_t_id FROM parametros)
                ),
                linderos AS (
                    SELECT {LC_BOUNDARY_T}.{T_ID_F}, {LC_BOUNDARY_T}.{COL_BFS_T_GEOMETRY_F} AS geom  FROM {schema}.{LC_BOUNDARY_T} JOIN {schema}.{MORE_BFS_T} ON {MORE_BFS_T}.{MORE_BFS_T_LC_PLOT_F} = (SELECT terreno_t_id FROM parametros) AND {LC_BOUNDARY_T}.{T_ID_F} = {MORE_BFS_T}.{MORE_BFS_T_LC_BOUNDARY_F}
                ),
                terrenos_asociados_linderos AS (
                    SELECT DISTINCT {MORE_BFS_T}.{MORE_BFS_T_LC_PLOT_F} AS t_id_terreno, {MORE_BFS_T}.{MORE_BFS_T_LC_BOUNDARY_F} AS t_id_lindero FROM {schema}.{MORE_BFS_T} WHERE {MORE_BFS_T}.{MORE_BFS_T_LC_BOUNDARY_F} IN (SELECT {T_ID_F} FROM linderos) AND {MORE_BFS_T}.{MORE_BFS_T_LC_PLOT_F} != (SELECT terreno_t_id FROM parametros)
                ),
                lineas_colindancia AS (
                    SELECT t_id_terreno AS {T_ID_F}, linderos.geom FROM linderos JOIN terrenos_asociados_linderos ON linderos.{T_ID_F} = terrenos_asociados_linderos.t_id_lindero
                )
                SELECT array_to_json(array_agg(features)) AS features
                FROM (
                    SELECT f AS features
                    FROM (
                        SELECT 'Feature' AS type,
                        row_to_json((SELECT l FROM (SELECT ROUND(st_length(lineas_colindancia.geom)::numeric, 2) AS longitud) AS l)) AS properties,
                        ST_AsGeoJSON(lineas_colindancia.geom)::json AS geometry
                        FROM lineas_colindancia
                    ) as f)
                as ff;""".format(**vars(names),  # Custom keys are searched in Table And Field Names object
                                 schema=schema,
                                 plot_id=plot_id)

    return query
