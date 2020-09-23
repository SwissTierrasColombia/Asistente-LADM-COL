from asistente_ladm_col.config.enums import EnumQualityRule
from asistente_ladm_col.config.ladm_names import LADMNames

ROLE_ACTIONS = 'role_actions'
ROLE_NAME = 'role_name'
ROLE_ENABLED = 'role_enabled'
ROLE_DESCRIPTION = 'role_description'
ROLE_GUI_CONFIG = 'role_gui_config'
ROLE_MODELS = 'role_models'
ROLE_MODEL_ILI2DB_PARAMETERS = 'role_model_ili2db_parameters'
ROLE_QUALITY_RULES = 'rule_quality_rules'
BASIC_ROLE = 'basic_role'
SUPPLIES_PROVIDER_ROLE = 'supplies_provider_role'
FIELD_ADMIN_ROLE = 'field_admin_role'
FIELD_COORDINATOR_ROLE = 'field_coordinator_role'
OPERATOR_ROLE = 'operator_role'
MANAGER_ROLE = 'manager_role'
ADVANCED_ROLE = 'advanced_role'
ADMINISTRATOR_ROLE = 'administrator_role'

ROLE_SUPPORTED_MODELS = "role_supported_models"
ROLE_HIDDEN_MODELS = "role_hidden_models"
ROLE_CHECKED_MODELS = "role_checked_models"
COMMON_SUPPORTED_MODELS = [LADMNames.LADM_COL_MODEL_KEY,
                           LADMNames.SURVEY_MODEL_KEY,
                           LADMNames.SUPPLIES_MODEL_KEY,
                           LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY,
                           LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY,
                           LADMNames.CADASTRAL_CARTOGRAPHY_MODEL_KEY,
                           LADMNames.VALUATION_MODEL_KEY,
                           LADMNames.ISO19107_MODEL_KEY]
COMMON_HIDDEN_MODELS = [LADMNames.LADM_COL_MODEL_KEY,
                        LADMNames.ISO19107_MODEL_KEY]
COMMON_CHECKED_MODELS = [LADMNames.SURVEY_MODEL_KEY]
COMMON_ROLE_MODELS = {ROLE_SUPPORTED_MODELS: COMMON_SUPPORTED_MODELS,
                      ROLE_HIDDEN_MODELS: COMMON_HIDDEN_MODELS,
                      ROLE_CHECKED_MODELS: COMMON_CHECKED_MODELS}

COMMON_QUALITY_RULES = [
    EnumQualityRule.Point.OVERLAPS_IN_BOUNDARY_POINTS,
    EnumQualityRule.Point.OVERLAPS_IN_CONTROL_POINTS,
    EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES,
    EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_PLOT_NODES,
    EnumQualityRule.Line.OVERLAPS_IN_BOUNDARIES,
    EnumQualityRule.Line.BOUNDARIES_ARE_NOT_SPLIT,
    EnumQualityRule.Line.BOUNDARIES_COVERED_BY_PLOTS,
    EnumQualityRule.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS,
    EnumQualityRule.Line.DANGLES_IN_BOUNDARIES,
    EnumQualityRule.Polygon.OVERLAPS_IN_PLOTS,
    EnumQualityRule.Polygon.OVERLAPS_IN_BUILDINGS,
    EnumQualityRule.Polygon.OVERLAPS_IN_RIGHTS_OF_WAY,
    EnumQualityRule.Polygon.PLOTS_COVERED_BY_BOUNDARIES,
    EnumQualityRule.Polygon.RIGHT_OF_WAY_OVERLAPS_BUILDINGS,
    EnumQualityRule.Polygon.GAPS_IN_PLOTS,
    EnumQualityRule.Polygon.MULTIPART_IN_RIGHT_OF_WAY,
    EnumQualityRule.Polygon.PLOT_NODES_COVERED_BY_BOUNDARY_POINTS,
    EnumQualityRule.Polygon.BUILDINGS_SHOULD_BE_WITHIN_PLOTS,
    EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_PLOTS,
    EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_BUILDINGS,
    EnumQualityRule.Logic.PARCEL_RIGHT_RELATIONSHIP,
    EnumQualityRule.Logic.FRACTION_SUM_FOR_PARTY_GROUPS,
    EnumQualityRule.Logic.DEPARTMENT_CODE_HAS_TWO_NUMERICAL_CHARACTERS,
    EnumQualityRule.Logic.MUNICIPALITY_CODE_HAS_THREE_NUMERICAL_CHARACTERS,
    EnumQualityRule.Logic.PARCEL_NUMBER_HAS_30_NUMERICAL_CHARACTERS,
    EnumQualityRule.Logic.PARCEL_NUMBER_BEFORE_HAS_20_NUMERICAL_CHARACTERS,
    EnumQualityRule.Logic.COL_PARTY_NATURAL_TYPE,
    EnumQualityRule.Logic.COL_PARTY_NOT_NATURAL_TYPE,
    EnumQualityRule.Logic.PARCEL_TYPE_AND_22_POSITION_OF_PARCEL_NUMBER,
    EnumQualityRule.Logic.UEBAUNIT_PARCEL,
    EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_BOUNDARY_POINT,
    EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_SURVEY_POINT,
    EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_CONTROL_POINT,
    EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_BOUNDARY,
    EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_PLOT,
    EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_BUILDING,
    EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_BUILDING_UNIT,
    EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_PARCEL,
    EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_PARTY,
    EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_RIGHT,
    EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_RESTRICTION,
    EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_ADMINISTRATIVE_SOURCE]

ALL_ROLES = 'all_roles'
