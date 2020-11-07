def get_annex17_building_data_query (names, schema, plot_id):
    query = """SELECT array_to_json(array_agg(features)) AS features
                    FROM (
                    	SELECT f AS features
                    	FROM (
                    		SELECT 'Feature' AS type
                                ,ST_AsGeoJSON({COL_SPATIAL_UNIT_T_GEOMETRY_F}, 4, 0)::json AS geometry
                    			,row_to_json((
                    					SELECT l
                    					FROM (
                                            SELECT {T_ID_F} AS t_id
                    						) AS l
                    					)) AS properties
                            FROM {schema}.{LC_BUILDING_T} AS c
                            WHERE {COL_SPATIAL_UNIT_T_GEOMETRY_F} && (SELECT ST_Expand(ST_Envelope({LC_PLOT_T}.{LC_PLOT_T_GEOMETRY_F}), 100) FROM {schema}.{LC_PLOT_T} WHERE {T_ID_F} = {plot_id})
                    		) AS f
                        ) AS ff;""".format(**vars(names),  # Custom keys are searched in Table And Field Names object
                                           plot_id=plot_id,
                                           schema=schema)

    return query