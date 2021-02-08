from asistente_ladm_col.logic.ladm_col.config.queries.queries_config_utils import get_full_alias
from asistente_ladm_col.config.query_names import QueryNames
from asistente_ladm_col.logic.ladm_col.ladm_query_objects import (OwnField,
                                                                  DomainOwnField,
                                                                  EvalExpressionOwnField,
                                                                  RelatedOwnFieldObject,
                                                                  FilterSubLevel)
from qgis.core import QgsExpression


def get_igac_basic_query(names, ladm_units):
    required_address_fields = [
        DomainOwnField(names.EXT_ADDRESS_S_ADDRESS_TYPE_F, "Tipo dirección", names.EXT_ADDRESS_TYPE_D),
        OwnField(names.EXT_ADDRESS_S_POSTAL_CODE_F, 'Código postal'),
        EvalExpressionOwnField("Dirección",
                               QgsExpression("""trim(
                                coalesce(get_domain_value_from_code( '{dominio_clase_via_principal}',  "{clase_via_principal}" , False, False)||' ', '') ||
                                coalesce({valor_via_principal} || ' ', '') ||
                                coalesce({letra_via_principal} || ' ', '') ||
                                coalesce(get_domain_value_from_code( '{dominio_sector_ciudad}',  "{sector_ciudad}", False, False)||' ', '') ||
                                coalesce({valor_via_generadora} || ' ', '') ||
                                coalesce({letra_via_generadora} || ' ', '') ||
                                coalesce({numero_predio} || ' ', '') ||
                                coalesce(get_domain_value_from_code( '{dominio_sector_predio}',  "{sector_predio}", False, False)||' ', '') ||
                                coalesce({complemento} || ' ', '') ||
                                coalesce({nombre_predio}, '')
                            )""".format(
                             dominio_clase_via_principal=names.EXT_ADDRESS_TYPE_MAIN_ROAD_CLASS_D,
                             clase_via_principal=names.EXT_ADDRESS_S_MAIN_ROAD_CLASS_F,
                             valor_via_principal=names.EXT_ADDRESS_S_VALUE_MAIN_ROAD_F,
                             letra_via_principal=names.EXT_ADDRESS_S_LETTER_MAIN_ROAD_F,
                             dominio_sector_ciudad=names.EXT_ADDRESS_TYPE_CITY_SECTOR_D,
                             sector_ciudad=names.EXT_ADDRESS_S_CITY_SECTOR_F,
                             valor_via_generadora=names.EXT_ADDRESS_S_VALUE_GENERATOR_ROAD_F,
                             letra_via_generadora=names.EXT_ADDRESS_S_LETTER_GENERATOR_ROAD_F,
                             numero_predio=names.EXT_ADDRESS_S_PARCEL_NUMBER_F,
                             dominio_sector_predio=names.EXT_ADDRESS_TYPE_PARCEL_SECTOR_D,
                             sector_predio=names.EXT_ADDRESS_S_PARCEL_SECTOR_F,
                             complemento=names.EXT_ADDRESS_S_COMPLEMENT_F,
                             nombre_predio=names.EXT_ADDRESS_S_PARCEL_NAME_F)))]

    query = {
        QueryNames.LEVEL_TABLE: {
            QueryNames.LEVEL_TABLE_NAME: names.LC_PLOT_T,
            QueryNames.LEVEL_TABLE_ALIAS: names.LC_PLOT_T,
            QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.T_ID_F, names.LC_PLOT_T, names.T_ID_F),
            QueryNames.TABLE_FIELDS: [OwnField(names.LC_PLOT_T_PLOT_AREA_F, get_full_alias("Área", ladm_units, names.LC_PLOT_T, names.LC_PLOT_T_PLOT_AREA_F)),
                                      RelatedOwnFieldObject(names.EXT_ADDRESS_S, names.EXT_ADDRESS_S,
                                                            required_address_fields,
                                                            names.EXT_ADDRESS_S_LC_PLOT_F)],
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
                    OwnField(names.LC_PARCEL_T_NUPRE_F, "NUPRE"),
                    OwnField(names.LC_PARCEL_T_ID_OPERATION_F, "Id operación"),
                    OwnField(names.LC_PARCEL_T_FMI_F, "FMI"),
                    OwnField(names.LC_PARCEL_T_PARCEL_NUMBER_F, "Número predial"),
                    OwnField(names.LC_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F, "Número predial anterior"),
                    DomainOwnField(names.LC_PARCEL_T_TYPE_F, "Tipo", names.COL_BAUNIT_TYPE_D)
                ],
                QueryNames.LEVEL_TABLE: {
                    QueryNames.LEVEL_TABLE_NAME: names.LC_BUILDING_T,
                    QueryNames.LEVEL_TABLE_ALIAS: names.LC_BUILDING_T,
                    QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.COL_UE_BAUNIT_T_LC_BUILDING_F,
                                                                names.COL_UE_BAUNIT_T,
                                                                names.COL_UE_BAUNIT_T_PARCEL_F),
                    QueryNames.TABLE_FIELDS: [
                        OwnField(names.LC_BUILDING_T_BUILDING_AREA_F, "Área"),
                        RelatedOwnFieldObject(names.EXT_ADDRESS_S, names.EXT_ADDRESS_S,
                                              required_address_fields, names.EXT_ADDRESS_S_LC_BUILDING_F)
                    ],
                    QueryNames.LEVEL_TABLE: {
                        QueryNames.LEVEL_TABLE_NAME: names.LC_BUILDING_UNIT_T,
                        QueryNames.LEVEL_TABLE_ALIAS: names.LC_BUILDING_UNIT_T,
                        QueryNames.FILTER_SUB_LEVEL: FilterSubLevel(names.T_ID_F, names.LC_BUILDING_UNIT_T,
                                                                    names.LC_BUILDING_UNIT_T_BUILDING_F),
                        QueryNames.TABLE_FIELDS: [
                            OwnField(names.LC_BUILDING_UNIT_T_TOTAL_FLOORS_F, "Número de pisos"),
                            OwnField(names.LC_BUILDING_UNIT_T_TOTAL_ROOMS_F, "Número de habitaciones"),
                            OwnField(names.LC_BUILDING_UNIT_T_TOTAL_BATHROOMS_F, "Número de baños"),
                            OwnField(names.LC_BUILDING_UNIT_T_TOTAL_LOCALS_F, "Número de locales"),
                            DomainOwnField(names.LC_BUILDING_UNIT_T_BUILDING_TYPE_F, "Tipo construcción",
                                           names.LC_BUILDING_TYPE_D),
                            DomainOwnField(names.LC_BUILDING_UNIT_T_BUILDING_UNIT_TYPE_F,
                                           "Tipo unidad de construcción", names.LC_BUILDING_UNIT_TYPE_D),
                            DomainOwnField(names.LC_BUILDING_UNIT_T_FLOOR_TYPE_F, "Tipo de planta",
                                           names.LC_BUILDING_FLOOR_TYPE_D),
                            DomainOwnField(names.LC_BUILDING_UNIT_T_DOMAIN_TYPE_F, "Tipo dominio",
                                           names.LC_DOMAIN_BUILDING_TYPE_D),
                            OwnField(names.LC_BUILDING_UNIT_T_FLOOR_F, "Ubicación en el piso"),
                            OwnField(names.LC_BUILDING_UNIT_T_BUILT_AREA_F, get_full_alias("Área construida", ladm_units, names.LC_BUILDING_UNIT_T, names.LC_BUILDING_UNIT_T_BUILT_AREA_F)),
                            DomainOwnField(names.LC_BUILDING_UNIT_T_USE_F, "Uso",
                                           names.LC_BUILDING_UNIT_USE_D),
                            RelatedOwnFieldObject(names.EXT_ADDRESS_S, names.EXT_ADDRESS_S,
                                                  required_address_fields, names.EXT_ADDRESS_S_LC_BUILDING_UNIT_F)
                        ]
                    }
                }
            }
        }
    }

    return query

