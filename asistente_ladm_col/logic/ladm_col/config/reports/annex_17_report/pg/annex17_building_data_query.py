def get_annex17_building_data_query (schema):
    query = """SELECT array_to_json(array_agg(features)) AS features
                    FROM (
                    	SELECT f AS features
                    	FROM (
                    		SELECT 'Feature' AS type
                    			,ST_AsGeoJSON(geometria)::json AS geometry
                    			,row_to_json((
                    					SELECT l
                    					FROM (
                    						SELECT t_id AS t_id
                    						) AS l
                    					)) AS properties
                            FROM {schema}.op_construccion AS c
                    		) AS f
                        ) AS ff;""".format(schema=schema)

    return query