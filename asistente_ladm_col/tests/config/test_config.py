TEST_SCHEMAS_MAPPING = {
    # TEST DB POSTGRES
    'test_ladm_col': 'ladm/pg/ladm_col_v1_1.sql',
    'test_ladm_col_empty': 'ladm/pg/test_ladm_col_empty_v1_1.sql',
    'test_change_detections': 'ladm/pg/test_change_detections_v1_1.sql',
    'test_distinct_geoms': 'ladm/pg/test_distinct_geoms_v1_1.sql',
    'interlis_no_ladm': 'static/pg/interlis_no_ladm.sql',
    'empty_no_interlis_no_ladm': 'static/pg/empty_no_interlis_no_ladm.sql',
    'interlis_ili2db3_ladm': 'static/pg/interlis_ili2db3_ladm_col_221.sql',
    'ladm_col_210': 'static/pg/ladm_col_operation_v_210.sql',
    # TEST DB MSSQL
    'empty_no_interlis_no_ladm_mssql': 'static/mssql/empty_no_interlis_no_ladm_mssql.sql',
    'interlis_ili2db3_ladm_mssql': 'static/mssql/interlis_ili2db3_ladm_mssql.sql',
    'interlis_no_ladm_mssql': 'static/mssql/interlis_no_ladm_mssql.sql',
    'ladm_col_211_mssql': 'static/mssql/ladm_col_211_mssql.sql',
    'test_ladm_col_queries_mssql': 'ladm/mssql/test_ladm_col_queries_v1_1.sql',
    'test_ladm_col_mssql': 'ladm/mssql/test_ladm_col_v1_1.sql',
    # TEST DB GEOPACKAGE
    'test_ladm_multiple_child_domains_gpkg': 'ladm/gpkg/test_multiple_models_ambiente_y_lc.gpkg',
    'tests_geometry_util_gpkg': 'static/gpkg/geometry_utils.gpkg',
    'tests_quality_validations_gpkg': 'static/gpkg/quality_validations.gpkg',
    'tests_quality_rules_tolerance_gpkg': 'ladm/gpkg/test_quality_rules_tolerance.gpkg',
    'topology_cases_gpkg': 'static/gpkg/topology_cases.gpkg',
    'adjust_boundaries_cases_gpkg': 'static/gpkg/adjust_boundaries_cases.gpkg',
    'no_interlis_gpkg': 'static/gpkg/no_interlis.gpkg',
    'interlis_no_ladm_col_models_gpkg': 'static/gpkg/interlis_no_ladm_col_models.gpkg'
}
