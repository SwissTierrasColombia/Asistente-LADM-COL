from asistente_ladm_col.logic.ladm_col.config.queries.queries_config_utils import get_full_alias
from asistente_ladm_col.config.mapping_config import QueryNames
from asistente_ladm_col.logic.ladm_col.ladm_query_objects import (OwnField,
                                                                  DomainOwnField,
                                                                  FilterSubLevel)


def get_igac_economic_query(names, ladm_units):
    query = {
        QueryNames.LEVEL_TABLE: {
            QueryNames.LEVEL_TABLE_NAME: names.LC_PLOT_T,
            QueryNames.LEVEL_TABLE_ALIAS: names.LC_PLOT_T,
            QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.T_ID_F, names.LC_PLOT_T, names.T_ID_F),
            QueryNames.TABLE_FIELDS: [OwnField(names.LC_PLOT_T_PLOT_VALUATION_F, get_full_alias("Avalúo", ladm_units, names.LC_PLOT_T, names.LC_PLOT_T_PLOT_VALUATION_F)),
                                      OwnField(names.LC_PLOT_T_PLOT_AREA_F, get_full_alias("Área", ladm_units, names.LC_PLOT_T, names.LC_PLOT_T_PLOT_AREA_F))],
            QueryNames.LEVEL_TABLE: {
                QueryNames.LEVEL_TABLE_NAME: names.LC_PARCEL_T,
                QueryNames.LEVEL_TABLE_ALIAS: names.LC_PARCEL_T,
                QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_UE_BAUNIT_T_PARCEL_F,
                                                            names.COL_UE_BAUNIT_T,
                                                            names.COL_UE_BAUNIT_T_LC_PLOT_F),
                QueryNames.TABLE_FIELDS: [
                    OwnField(names.COL_BAUNIT_T_NAME_F, "Nombre"),
                    OwnField(names.LC_PARCEL_T_DEPARTMENT_F, "Departamento"),
                    OwnField(names.LC_PARCEL_T_MUNICIPALITY_F, "Municipio"),
                    OwnField(names.LC_PARCEL_T_ID_OPERATION_F, "Id operación"),
                    OwnField(names.LC_PARCEL_T_FMI_F, "FMI"),
                    OwnField(names.LC_PARCEL_T_PARCEL_NUMBER_F, "Número predial"),
                    OwnField(names.LC_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F, "Número predial anterior"),
                    OwnField(names.LC_PARCEL_T_VALUATION_F, get_full_alias("Avalúo predio", ladm_units, names.LC_PARCEL_T, names.LC_PARCEL_T_VALUATION_F)),
                    DomainOwnField(names.LC_PARCEL_T_TYPE_F, "Tipo", names.LC_PARCEL_TYPE_D)
                ],
                QueryNames.LEVEL_TABLE: {
                    QueryNames.LEVEL_TABLE_NAME: names.LC_BUILDING_T,
                    QueryNames.LEVEL_TABLE_ALIAS: names.LC_BUILDING_T,
                    QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_UE_BAUNIT_T_LC_BUILDING_F,
                                                                names.COL_UE_BAUNIT_T,
                                                                names.COL_UE_BAUNIT_T_PARCEL_F),
                    QueryNames.TABLE_FIELDS: [
                        OwnField(names.LC_BUILDING_T_BUILDING_VALUATION_F, get_full_alias("Avalúo", ladm_units, names.LC_BUILDING_T, names.LC_BUILDING_T_BUILDING_VALUATION_F)),
                        OwnField(names.LC_BUILDING_T_BUILDING_AREA_F, "Área construcción")
                    ],
                    QueryNames.LEVEL_TABLE: {
                        QueryNames.LEVEL_TABLE_NAME: names.LC_BUILDING_UNIT_T,
                        QueryNames.LEVEL_TABLE_ALIAS: names.LC_BUILDING_UNIT_T,
                        QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.T_ID_F, names.LC_BUILDING_UNIT_T,
                                                                    names.LC_BUILDING_UNIT_T_BUILDING_F),
                        QueryNames.TABLE_FIELDS: [
                            OwnField(names.LC_BUILDING_UNIT_T_BUILDING_UNIT_VALUATION_F, "Avalúo"),
                            OwnField(names.LC_BUILDING_UNIT_T_BUILT_AREA_F, get_full_alias("Área construida", ladm_units, names.LC_BUILDING_UNIT_T, names.LC_BUILDING_UNIT_T_BUILT_AREA_F)),
                            OwnField(names.LC_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F,
                                     get_full_alias("Área privada construida", ladm_units, names.LC_BUILDING_UNIT_T, names.LC_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F)),
                            OwnField(names.LC_BUILDING_UNIT_T_TOTAL_FLOORS_F, "Número de pisos"),
                            OwnField(names.LC_BUILDING_UNIT_T_FLOOR_F, "Ubicación en el piso"),
                            DomainOwnField(names.LC_BUILDING_UNIT_T_USE_F, "Uso",
                                           names.LC_BUILDING_UNIT_USE_D),
                            OwnField(names.LC_BUILDING_UNIT_T_YEAR_OF_BUILDING_F, "Año construcción")
                        ]
                    }
                }
            }
        }
    }

    return query
