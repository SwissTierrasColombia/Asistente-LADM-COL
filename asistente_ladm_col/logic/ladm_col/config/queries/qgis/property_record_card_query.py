from asistente_ladm_col.logic.ladm_col.config.queries.queries_config_utils import get_full_alias
from asistente_ladm_col.config.mapping_config import QueryNames
from asistente_ladm_col.logic.ladm_col.ladm_query_objects import (OwnField,
                                                                  DomainOwnField,
                                                                  FilterSubLevel)


def get_igac_property_record_card_query(names, ladm_units):
    query = {
        QueryNames.LEVEL_TABLE: {
            QueryNames.LEVEL_TABLE_NAME: names.LC_PLOT_T,
            QueryNames.LEVEL_TABLE_ALIAS: names.LC_PLOT_T,
            QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.T_ID_F, names.LC_PLOT_T, names.T_ID_F),
            QueryNames.TABLE_FIELDS: [OwnField(names.LC_PLOT_T_PLOT_AREA_F, get_full_alias('Área', ladm_units, names.LC_PLOT_T, names.LC_PLOT_T_PLOT_AREA_F))],
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
                    DomainOwnField(names.LC_PARCEL_T_TYPE_F, "Tipo", names.LC_PARCEL_TYPE_D)
                ]
            }
        }
    }

    return query
