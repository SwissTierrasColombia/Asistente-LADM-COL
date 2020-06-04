def get_annex17_building_data_query (names, schema):
    query = """SELECT array_to_json(array_agg(features)) AS features
                    FROM (
                    	SELECT f AS features
                    	FROM (
                    		SELECT 'Feature' AS type
                                ,ST_AsGeoJSON({COL_SPATIAL_UNIT_T_GEOMETRY_F})::json AS geometry
                    			,row_to_json((
                    					SELECT l
                    					FROM (
                                            SELECT {T_ID_F} AS t_id
                    						) AS l
                    					)) AS properties
                            FROM {schema}.{LC_BUILDING_T} AS c
                    		) AS f
                        ) AS ff;""".format(**vars(names),  # Custom keys are search in Table And Field Names object
                                           schema=schema)

    return query