def get_annex17_plot_data_query (schema, where_id):
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
                                ,ST_AsGeoJSON(poligono_creado)::json AS geometry
                            FROM {schema}.terreno AS l
                            LEFT JOIN {schema}.uebaunit ON l.t_id = ue_terreno
                            LEFT JOIN {schema}.predio ON predio.t_id = baunit_predio
                            {where_id}
                            ) AS f
                        ) AS ff;""".format(schema=schema, where_id=where_id)

    return query