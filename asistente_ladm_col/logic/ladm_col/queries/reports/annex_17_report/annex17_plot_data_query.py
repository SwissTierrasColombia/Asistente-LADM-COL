def get_annex17_plot_data_query(schema, where_id):
    query = """SELECT array_to_json(array_agg(features)) AS features
                    FROM (
                        SELECT f AS features
                        FROM (
                            SELECT 'Feature' AS type
                                ,row_to_json((
                                    SELECT l
                                    FROM (
                                        SELECT left(right(numero_predial,15),6) AS predio
                                        ) AS l
                                    )) AS properties
                                ,ST_AsGeoJSON(geometria)::json AS geometry
                            FROM {schema}.op_terreno AS l
                            LEFT JOIN {schema}.col_uebaunit ON l.t_id = ue_op_terreno
                            LEFT JOIN {schema}.op_predio ON op_predio.t_id = baunit
                            {where_id}
                            ) AS f
                        ) AS ff;""".format(schema=schema, where_id=where_id)

    return query