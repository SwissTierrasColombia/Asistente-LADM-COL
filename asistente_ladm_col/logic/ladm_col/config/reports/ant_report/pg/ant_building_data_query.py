def get_ant_building_data_query(names, schema, plot_id):
    query = """
            WITH
            predio as (
                select {COL_UE_BAUNIT_T_PARCEL_F} from {schema}.{COL_UE_BAUNIT_T}
                where {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F} = {plot_id}
            ),
            construcciones_predio as (
                select {COL_UE_BAUNIT_T_LC_BUILDING_F} from {schema}.{COL_UE_BAUNIT_T}
                where {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_PARCEL_F} in (select * from predio) and {COL_UE_BAUNIT_T_LC_BUILDING_F} is not Null
            )
            SELECT array_to_json(array_agg(features)) AS features
            FROM (
            SELECT f AS features
                FROM (
                    SELECT 'Feature' AS type
                        ,ST_AsGeoJSON({COL_SPATIAL_UNIT_T_GEOMETRY_F}, 4, 0)::json AS geometry --Parametrizar geometria
                        ,row_to_json((SELECT l FROM (SELECT {T_ID_F} AS t_id) AS l)) AS properties
                    FROM {schema}.{LC_BUILDING_T} 
                    WHERE {T_ID_F} in (select * from construcciones_predio)
                ) AS f
            ) AS ff;""".format(**vars(names),  # Custom keys are searched in Table And Field Names object
                               plot_id=plot_id,
                               schema=schema)

    return query

