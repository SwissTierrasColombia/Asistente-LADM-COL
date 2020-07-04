def get_annex17_plot_data_query(names, schema, where_id):
    query = """SELECT array_to_json(array_agg(features)) AS features
                    FROM (
                        SELECT f AS features
                        FROM (
                            SELECT 'Feature' AS type
                                ,row_to_json((
                                    SELECT l
                                    FROM (
                                        SELECT left(right({LC_PARCEL_T_PARCEL_NUMBER_F},15),6) AS predio
                                        ) AS l
                                    )) AS properties
                                ,ST_AsGeoJSON({LC_PLOT_T_GEOMETRY_F})::json AS geometry
                            FROM {schema}.{LC_PLOT_T} AS l
                            LEFT JOIN {schema}.{COL_UE_BAUNIT_T} ON l.{T_ID_F} = {COL_UE_BAUNIT_T_LC_PLOT_F}
                            LEFT JOIN {schema}.{LC_PARCEL_T} ON {LC_PARCEL_T}.{T_ID_F} = {COL_UE_BAUNIT_T_PARCEL_F}
                            {where_id}
                            ) AS f
                        ) AS ff;""".format(**vars(names),  # Custom keys are searched in Table And Field Names object
                                           schema=schema,
                                           where_id=where_id)

    return query