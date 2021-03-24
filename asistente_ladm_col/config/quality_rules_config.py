from qgis.PyQt.QtCore import (QCoreApplication,
                              QVariant)
from qgis.core import QgsField

from asistente_ladm_col.config.enums import EnumQualityRule
from asistente_ladm_col.config.general_config import PREFIX_ERROR_CODE
from asistente_ladm_col.utils.utils import get_key_for_quality_rule_adjusted_layer

QUALITY_GROUP_NAME = "QUALITY_GROUP_NAME"
QUALITY_RULES = "QUALITY_RULES"
QUALITY_RULE_ID = "QUALITY_RULE_ID"
QUALITY_RULE_NAME = "QUALITY_RULE_NAME"
QUALITY_RULE_TABLE_NAME = "QUALITY_RULE_TABLE_NAME"
QUALITY_RULE_TABLE_FIELDS = "QUALITY_RULE_TABLE_FIELDS"
QUALITY_RULE_TABLE_FIELD = "QUALITY_RULE_TABLE_FIELD"
QUALITY_RULE_DOMAIN_ERROR_CODES = "QUALITY_RULE_DOMAIN_ERROR_CODES"
QUALITY_RULES_ERRORS = "QUALITY_RULES_ERRORS"
QUALITY_RULE_LAYERS = "QUALITY_RULE_LAYERS"
QUALITY_RULE_LADM_COL_LAYERS = "QUALITY_RULE_LADM_COL_LAYERS"
QUALITY_RULE_ADJUSTED_LAYERS = "QUALITY_RULE_ADJUSTED_LAYERS"
HAS_ADJUSTED_LAYERS = "HAS_ADJUSTED_LAYERS"
FIX_ADJUSTED_LAYER = "FIX_ADJUSTED_LAYER"
ADJUSTED_INPUT_LAYER = "ADJUSTED_INPUT_LAYER"
ADJUSTED_REFERENCE_LAYER = "ADJUSTED_REFERENCE_LAYER"
ADJUSTED_BEHAVIOR = "ADJUSTED_BEHAVIOR"
ADJUSTED_TOPOLOGICAL_POINTS = "ADJUSTED_TOPOLOGICAL_POINTS"

#ERROR CODES FOR POINT QUALITY RULES
QUALITY_RULE_ERROR_CODE_E100101 = PREFIX_ERROR_CODE + str(EnumQualityRule.Point.OVERLAPS_IN_BOUNDARY_POINTS.value) + '01'
QUALITY_RULE_ERROR_CODE_E100201 = PREFIX_ERROR_CODE + str(EnumQualityRule.Point.OVERLAPS_IN_CONTROL_POINTS.value) + '01'
QUALITY_RULE_ERROR_CODE_E100301 = PREFIX_ERROR_CODE + str(EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES.value) + '01'
QUALITY_RULE_ERROR_CODE_E100302 = PREFIX_ERROR_CODE + str(EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES.value) + '02'
QUALITY_RULE_ERROR_CODE_E100303 = PREFIX_ERROR_CODE + str(EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES.value) + '03'
QUALITY_RULE_ERROR_CODE_E100401 = PREFIX_ERROR_CODE + str(EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_PLOT_NODES.value) + '01'

#ERROR CODES FOR LINE QUALITY RULES
QUALITY_RULE_ERROR_CODE_E200101 = PREFIX_ERROR_CODE + str(EnumQualityRule.Line.OVERLAPS_IN_BOUNDARIES.value) + '01'
QUALITY_RULE_ERROR_CODE_E200201 = PREFIX_ERROR_CODE + str(EnumQualityRule.Line.BOUNDARIES_ARE_NOT_SPLIT.value) + '01'
QUALITY_RULE_ERROR_CODE_E200301 = PREFIX_ERROR_CODE + str(EnumQualityRule.Line.BOUNDARIES_COVERED_BY_PLOTS.value) + '01'
QUALITY_RULE_ERROR_CODE_E200302 = PREFIX_ERROR_CODE + str(EnumQualityRule.Line.BOUNDARIES_COVERED_BY_PLOTS.value) + '02'
QUALITY_RULE_ERROR_CODE_E200303 = PREFIX_ERROR_CODE + str(EnumQualityRule.Line.BOUNDARIES_COVERED_BY_PLOTS.value) + '03'
QUALITY_RULE_ERROR_CODE_E200304 = PREFIX_ERROR_CODE + str(EnumQualityRule.Line.BOUNDARIES_COVERED_BY_PLOTS.value) + '04'
QUALITY_RULE_ERROR_CODE_E200305 = PREFIX_ERROR_CODE + str(EnumQualityRule.Line.BOUNDARIES_COVERED_BY_PLOTS.value) + '05'
QUALITY_RULE_ERROR_CODE_E200401 = PREFIX_ERROR_CODE + str(EnumQualityRule.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS.value) + '01'
QUALITY_RULE_ERROR_CODE_E200402 = PREFIX_ERROR_CODE + str(EnumQualityRule.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS.value) + '02'
QUALITY_RULE_ERROR_CODE_E200403 = PREFIX_ERROR_CODE + str(EnumQualityRule.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS.value) + '03'
QUALITY_RULE_ERROR_CODE_E200501 = PREFIX_ERROR_CODE + str(EnumQualityRule.Line.DANGLES_IN_BOUNDARIES.value) + '01'

#ERROR CODES FOR POLYGON QUALITY RULES
QUALITY_RULE_ERROR_CODE_E300101 = PREFIX_ERROR_CODE + str(EnumQualityRule.Polygon.OVERLAPS_IN_PLOTS.value) + '01'
QUALITY_RULE_ERROR_CODE_E300201 = PREFIX_ERROR_CODE + str(EnumQualityRule.Polygon.OVERLAPS_IN_BUILDINGS.value) + '01'
QUALITY_RULE_ERROR_CODE_E300301 = PREFIX_ERROR_CODE + str(EnumQualityRule.Polygon.OVERLAPS_IN_RIGHTS_OF_WAY.value) + '01'
QUALITY_RULE_ERROR_CODE_E300401 = PREFIX_ERROR_CODE + str(EnumQualityRule.Polygon.PLOTS_COVERED_BY_BOUNDARIES.value) + '01'
QUALITY_RULE_ERROR_CODE_E300402 = PREFIX_ERROR_CODE + str(EnumQualityRule.Polygon.PLOTS_COVERED_BY_BOUNDARIES.value) + '02'
QUALITY_RULE_ERROR_CODE_E300403 = PREFIX_ERROR_CODE + str(EnumQualityRule.Polygon.PLOTS_COVERED_BY_BOUNDARIES.value) + '03'
QUALITY_RULE_ERROR_CODE_E300404 = PREFIX_ERROR_CODE + str(EnumQualityRule.Polygon.PLOTS_COVERED_BY_BOUNDARIES.value) + '04'
QUALITY_RULE_ERROR_CODE_E300405 = PREFIX_ERROR_CODE + str(EnumQualityRule.Polygon.PLOTS_COVERED_BY_BOUNDARIES.value) + '05'
QUALITY_RULE_ERROR_CODE_E300501 = PREFIX_ERROR_CODE + str(EnumQualityRule.Polygon.RIGHT_OF_WAY_OVERLAPS_BUILDINGS.value) + '01'
QUALITY_RULE_ERROR_CODE_E300601 = PREFIX_ERROR_CODE + str(EnumQualityRule.Polygon.GAPS_IN_PLOTS.value) + '01'
QUALITY_RULE_ERROR_CODE_E300701 = PREFIX_ERROR_CODE + str(EnumQualityRule.Polygon.MULTIPART_IN_RIGHT_OF_WAY.value) + '01'
QUALITY_RULE_ERROR_CODE_E300801 = PREFIX_ERROR_CODE + str(EnumQualityRule.Polygon.PLOT_NODES_COVERED_BY_BOUNDARY_POINTS.value) + '01'
QUALITY_RULE_ERROR_CODE_E300901 = PREFIX_ERROR_CODE + str(EnumQualityRule.Polygon.BUILDINGS_SHOULD_BE_WITHIN_PLOTS.value) + '01'
QUALITY_RULE_ERROR_CODE_E300902 = PREFIX_ERROR_CODE + str(EnumQualityRule.Polygon.BUILDINGS_SHOULD_BE_WITHIN_PLOTS.value) + '02'
QUALITY_RULE_ERROR_CODE_E300903 = PREFIX_ERROR_CODE + str(EnumQualityRule.Polygon.BUILDINGS_SHOULD_BE_WITHIN_PLOTS.value) + '03'
QUALITY_RULE_ERROR_CODE_E301001 = PREFIX_ERROR_CODE + str(EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_PLOTS.value) + '01'
QUALITY_RULE_ERROR_CODE_E301002 = PREFIX_ERROR_CODE + str(EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_PLOTS.value) + '02'
QUALITY_RULE_ERROR_CODE_E301003 = PREFIX_ERROR_CODE + str(EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_PLOTS.value) + '03'
QUALITY_RULE_ERROR_CODE_E301101 = PREFIX_ERROR_CODE + str(EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_BUILDINGS.value) + '01'
QUALITY_RULE_ERROR_CODE_E301102 = PREFIX_ERROR_CODE + str(EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_BUILDINGS.value) + '02'
QUALITY_RULE_ERROR_CODE_E301103 = PREFIX_ERROR_CODE + str(EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_BUILDINGS.value) + '03'

#ERROR CODES FOR LOGIC QUALITY RULES
QUALITY_RULE_ERROR_CODE_E400101 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.PARCEL_RIGHT_RELATIONSHIP.value) + '01'
QUALITY_RULE_ERROR_CODE_E400102 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.PARCEL_RIGHT_RELATIONSHIP.value) + '02'
QUALITY_RULE_ERROR_CODE_E400201 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.FRACTION_SUM_FOR_PARTY_GROUPS.value) + '01'
QUALITY_RULE_ERROR_CODE_E400301 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.DEPARTMENT_CODE_HAS_TWO_NUMERICAL_CHARACTERS.value) + '01'
QUALITY_RULE_ERROR_CODE_E400401 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.MUNICIPALITY_CODE_HAS_THREE_NUMERICAL_CHARACTERS.value) + '01'
QUALITY_RULE_ERROR_CODE_E400501 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.PARCEL_NUMBER_HAS_30_NUMERICAL_CHARACTERS.value) + '01'
QUALITY_RULE_ERROR_CODE_E400601 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.PARCEL_NUMBER_BEFORE_HAS_20_NUMERICAL_CHARACTERS.value) + '01'
QUALITY_RULE_ERROR_CODE_E400701 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.COL_PARTY_NATURAL_TYPE.value) + '01'
QUALITY_RULE_ERROR_CODE_E400702 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.COL_PARTY_NATURAL_TYPE.value) + '02'
QUALITY_RULE_ERROR_CODE_E400703 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.COL_PARTY_NATURAL_TYPE.value) + '03'
QUALITY_RULE_ERROR_CODE_E400704 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.COL_PARTY_NATURAL_TYPE.value) + '04'
QUALITY_RULE_ERROR_CODE_E400801 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.COL_PARTY_NOT_NATURAL_TYPE.value) + '01'
QUALITY_RULE_ERROR_CODE_E400802 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.COL_PARTY_NOT_NATURAL_TYPE.value) + '02'
QUALITY_RULE_ERROR_CODE_E400803 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.COL_PARTY_NOT_NATURAL_TYPE.value) + '03'
QUALITY_RULE_ERROR_CODE_E400804 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.COL_PARTY_NOT_NATURAL_TYPE.value) + '04'
QUALITY_RULE_ERROR_CODE_E400901 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.PARCEL_TYPE_AND_22_POSITION_OF_PARCEL_NUMBER.value) + '01'
QUALITY_RULE_ERROR_CODE_E400902 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.PARCEL_TYPE_AND_22_POSITION_OF_PARCEL_NUMBER.value) + '02'
QUALITY_RULE_ERROR_CODE_E400903 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.PARCEL_TYPE_AND_22_POSITION_OF_PARCEL_NUMBER.value) + '03'
QUALITY_RULE_ERROR_CODE_E400904 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.PARCEL_TYPE_AND_22_POSITION_OF_PARCEL_NUMBER.value) + '04'
QUALITY_RULE_ERROR_CODE_E400905 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.PARCEL_TYPE_AND_22_POSITION_OF_PARCEL_NUMBER.value) + '05'
QUALITY_RULE_ERROR_CODE_E400906 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.PARCEL_TYPE_AND_22_POSITION_OF_PARCEL_NUMBER.value) + '06'
QUALITY_RULE_ERROR_CODE_E400907 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.PARCEL_TYPE_AND_22_POSITION_OF_PARCEL_NUMBER.value) + '07'
QUALITY_RULE_ERROR_CODE_E400908 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.PARCEL_TYPE_AND_22_POSITION_OF_PARCEL_NUMBER.value) + '08'
QUALITY_RULE_ERROR_CODE_E401001 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.UEBAUNIT_PARCEL.value) + '01'
QUALITY_RULE_ERROR_CODE_E401002 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.UEBAUNIT_PARCEL.value) + '02'
QUALITY_RULE_ERROR_CODE_E401003 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.UEBAUNIT_PARCEL.value) + '03'
QUALITY_RULE_ERROR_CODE_E401004 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.UEBAUNIT_PARCEL.value) + '04'
QUALITY_RULE_ERROR_CODE_E401005 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.UEBAUNIT_PARCEL.value) + '05'
QUALITY_RULE_ERROR_CODE_E401006 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.UEBAUNIT_PARCEL.value) + '06'
QUALITY_RULE_ERROR_CODE_E401007 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.UEBAUNIT_PARCEL.value) + '07'
QUALITY_RULE_ERROR_CODE_E401008 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.UEBAUNIT_PARCEL.value) + '08'
QUALITY_RULE_ERROR_CODE_E401009 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.UEBAUNIT_PARCEL.value) + '09'
QUALITY_RULE_ERROR_CODE_E401010 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.UEBAUNIT_PARCEL.value) + '10'
QUALITY_RULE_ERROR_CODE_E401011 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.UEBAUNIT_PARCEL.value) + '11'
QUALITY_RULE_ERROR_CODE_E401101 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_BOUNDARY_POINT.value) + '01'
QUALITY_RULE_ERROR_CODE_E401201 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_SURVEY_POINT.value) + '01'
QUALITY_RULE_ERROR_CODE_E401301 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_CONTROL_POINT.value) + '01'
QUALITY_RULE_ERROR_CODE_E401401 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_BOUNDARY.value) + '01'
QUALITY_RULE_ERROR_CODE_E401501 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_PLOT.value) + '01'
QUALITY_RULE_ERROR_CODE_E401601 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_BUILDING.value) + '01'
QUALITY_RULE_ERROR_CODE_E401701 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_BUILDING_UNIT.value) + '01'
QUALITY_RULE_ERROR_CODE_E401801 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_PARCEL.value) + '01'
QUALITY_RULE_ERROR_CODE_E401901 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_PARTY.value) + '01'
QUALITY_RULE_ERROR_CODE_E402001 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_RIGHT.value) + '01'
QUALITY_RULE_ERROR_CODE_E402101 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_RESTRICTION.value) + '01'
QUALITY_RULE_ERROR_CODE_E402201 = PREFIX_ERROR_CODE + str(EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_ADMINISTRATIVE_SOURCE.value) + '01'


class QualityRuleConfig:
    @staticmethod
    def get_quality_rules_config():
        from asistente_ladm_col.config.translation_strings import TranslatableConfigStrings  # To avoid circularity
        translated_strings = TranslatableConfigStrings().get_translatable_config_strings()

        return {
            EnumQualityRule.Point: {
                QUALITY_GROUP_NAME: QCoreApplication.translate("QualityDialog", "Rules for Points"),
                QUALITY_RULES: {
                    EnumQualityRule.Point.OVERLAPS_IN_BOUNDARY_POINTS: {
                        QUALITY_RULE_ID: EnumQualityRule.Point.OVERLAPS_IN_BOUNDARY_POINTS,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Point.OVERLAPS_IN_BOUNDARY_POINTS],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "punto_lindero_superposicion"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "ids_punto_lindero"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "conteo"), QVariant.Int)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E100101
                        ]
                    },
                    EnumQualityRule.Point.OVERLAPS_IN_CONTROL_POINTS: {
                        QUALITY_RULE_ID: EnumQualityRule.Point.OVERLAPS_IN_CONTROL_POINTS,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Point.OVERLAPS_IN_CONTROL_POINTS],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "punto_control_superposicion"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "ids_punto_control"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "conteo"), QVariant.Int)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E100201
                        ]
                    },
                    EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES: {
                        QUALITY_RULE_ID: EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "punto_lindero_no_cubierto_por_nodo_lindero"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_punto_lindero"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_lindero"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E100301,
                            QUALITY_RULE_ERROR_CODE_E100302,
                            QUALITY_RULE_ERROR_CODE_E100303
                        ]
                    },
                    EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_PLOT_NODES: {
                        QUALITY_RULE_ID: EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_PLOT_NODES,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_PLOT_NODES],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "punto_lindero_no_cubierto_por_nodo_terreno"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_punto_lindero"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E100401
                        ]
                    }
                }
            },
            EnumQualityRule.Line: {
                QUALITY_GROUP_NAME: QCoreApplication.translate("QualityDialog", "Rules for Lines"),
                QUALITY_RULES: {
                    EnumQualityRule.Line.OVERLAPS_IN_BOUNDARIES: {
                        QUALITY_RULE_ID: EnumQualityRule.Line.OVERLAPS_IN_BOUNDARIES,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Line.OVERLAPS_IN_BOUNDARIES],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "lindero_superposicion"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_lindero"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_lindero_superpone"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E200101
                        ]
                    },
                    EnumQualityRule.Line.BOUNDARIES_ARE_NOT_SPLIT: {
                        QUALITY_RULE_ID: EnumQualityRule.Line.BOUNDARIES_ARE_NOT_SPLIT,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Line.BOUNDARIES_ARE_NOT_SPLIT],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "lindero_no_cambio_colindancia"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_lindero"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E200201
                        ]
                    },
                    EnumQualityRule.Line.BOUNDARIES_COVERED_BY_PLOTS: {
                        QUALITY_RULE_ID: EnumQualityRule.Line.BOUNDARIES_COVERED_BY_PLOTS,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Line.BOUNDARIES_COVERED_BY_PLOTS],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "lindero_no_cubierto_por_limite_terreno"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_lindero"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_terreno"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E200301,
                            QUALITY_RULE_ERROR_CODE_E200302,
                            QUALITY_RULE_ERROR_CODE_E200303,
                            QUALITY_RULE_ERROR_CODE_E200304,
                            QUALITY_RULE_ERROR_CODE_E200305
                        ]
                    },
                    EnumQualityRule.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS: {
                        QUALITY_RULE_ID: EnumQualityRule.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "nodo_lindero_no_cubierto_por_punto_lindero"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_lindero"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_punto_lindero"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E200401,
                            QUALITY_RULE_ERROR_CODE_E200402,
                            QUALITY_RULE_ERROR_CODE_E200403
                        ]
                    },
                    EnumQualityRule.Line.DANGLES_IN_BOUNDARIES: {
                        QUALITY_RULE_ID: EnumQualityRule.Line.DANGLES_IN_BOUNDARIES,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Line.DANGLES_IN_BOUNDARIES],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "lindero_nodos_no_conectados"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_lindero"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E200501
                        ]
                    }

                }
            },
            EnumQualityRule.Polygon: {
                QUALITY_GROUP_NAME: QCoreApplication.translate("QualityDialog", "Rules for Polygons"),
                QUALITY_RULES: {
                    EnumQualityRule.Polygon.OVERLAPS_IN_PLOTS: {
                        QUALITY_RULE_ID: EnumQualityRule.Polygon.OVERLAPS_IN_PLOTS,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Polygon.OVERLAPS_IN_PLOTS],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "terreno_superposicion"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_terreno"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_terreno_superpone"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E300101
                        ]
                    },
                    EnumQualityRule.Polygon.OVERLAPS_IN_BUILDINGS: {
                        QUALITY_RULE_ID: EnumQualityRule.Polygon.OVERLAPS_IN_BUILDINGS,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Polygon.OVERLAPS_IN_BUILDINGS],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "construccion_superposicion"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_construccion"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_construccion_superpone"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E300201
                        ]
                    },
                    EnumQualityRule.Polygon.OVERLAPS_IN_RIGHTS_OF_WAY: {
                        QUALITY_RULE_ID: EnumQualityRule.Polygon.OVERLAPS_IN_RIGHTS_OF_WAY,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Polygon.OVERLAPS_IN_RIGHTS_OF_WAY],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "servidumbre_de_paso_superposicion"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_servidumbre"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_servidumbre_superpone"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E300301
                        ]
                    },
                    EnumQualityRule.Polygon.PLOTS_COVERED_BY_BOUNDARIES: {
                        QUALITY_RULE_ID: EnumQualityRule.Polygon.PLOTS_COVERED_BY_BOUNDARIES,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Polygon.PLOTS_COVERED_BY_BOUNDARIES],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "limite_terreno_no_cubierto_por_lindero"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_terreno"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_lindero"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E300401,
                            QUALITY_RULE_ERROR_CODE_E300402,
                            QUALITY_RULE_ERROR_CODE_E300403,
                            QUALITY_RULE_ERROR_CODE_E300404,
                            QUALITY_RULE_ERROR_CODE_E300405
                        ]
                    },
                    EnumQualityRule.Polygon.RIGHT_OF_WAY_OVERLAPS_BUILDINGS: {
                        QUALITY_RULE_ID: EnumQualityRule.Polygon.RIGHT_OF_WAY_OVERLAPS_BUILDINGS,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Polygon.RIGHT_OF_WAY_OVERLAPS_BUILDINGS],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "servidumbre_de_paso_no_superposicion_construccion"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_servidumbre_paso"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_construccion"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E300501
                        ]
                    },
                    EnumQualityRule.Polygon.GAPS_IN_PLOTS: {
                        QUALITY_RULE_ID: EnumQualityRule.Polygon.GAPS_IN_PLOTS,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Polygon.GAPS_IN_PLOTS],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "terrenos_huecos_entre_ellos"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_hueco"), QVariant.Int),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "ids_terrenos"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E300601
                        ]
                    },
                    EnumQualityRule.Polygon.MULTIPART_IN_RIGHT_OF_WAY: {
                        QUALITY_RULE_ID: EnumQualityRule.Polygon.MULTIPART_IN_RIGHT_OF_WAY,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Polygon.MULTIPART_IN_RIGHT_OF_WAY],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "servidumbre_de_paso_multiparte"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_servidumbre_paso"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E300701
                        ]
                    },
                    EnumQualityRule.Polygon.PLOT_NODES_COVERED_BY_BOUNDARY_POINTS: {
                        QUALITY_RULE_ID: EnumQualityRule.Polygon.PLOT_NODES_COVERED_BY_BOUNDARY_POINTS,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Polygon.PLOT_NODES_COVERED_BY_BOUNDARY_POINTS],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "nodo_terreno_no_cubierto_por_punto_lindero"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_terreno"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E300801
                        ]
                    },
                    EnumQualityRule.Polygon.BUILDINGS_SHOULD_BE_WITHIN_PLOTS: {
                        QUALITY_RULE_ID: EnumQualityRule.Polygon.BUILDINGS_SHOULD_BE_WITHIN_PLOTS,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Polygon.BUILDINGS_SHOULD_BE_WITHIN_PLOTS],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "construccion_no_contenida_por_terreno_asociado"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_construccion"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E300901,
                            QUALITY_RULE_ERROR_CODE_E300902
                        ]
                    },
                    EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_PLOTS: {
                        QUALITY_RULE_ID: EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_PLOTS,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_PLOTS],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "unidades_construccion_no_contenida_por_terreno_asociado"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_unidad_construccion"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E301001,
                            QUALITY_RULE_ERROR_CODE_E301002,
                            QUALITY_RULE_ERROR_CODE_E301003
                        ]
                    },
                    EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_BUILDINGS: {
                        QUALITY_RULE_ID: EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_BUILDINGS,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_BUILDINGS],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "unidades_construccion_no_contenida_por_construccion_asociada"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_unidad_construccion"),
                                     QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E301101,
                            QUALITY_RULE_ERROR_CODE_E301102,
                            QUALITY_RULE_ERROR_CODE_E301103
                        ]
                    }
                }
            },
            EnumQualityRule.Logic: {
                QUALITY_GROUP_NAME: QCoreApplication.translate("QualityDialog", "Logic consistency rules"),
                QUALITY_RULES: {
                    EnumQualityRule.Logic.PARCEL_RIGHT_RELATIONSHIP: {
                        QUALITY_RULE_ID: EnumQualityRule.Logic.PARCEL_RIGHT_RELATIONSHIP,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Logic.PARCEL_RIGHT_RELATIONSHIP],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "predio_error_derecho"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_predio"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E400101,
                            QUALITY_RULE_ERROR_CODE_E400102
                        ]
                    },
                    # 4002 could be taken if needed, we used it in early stages of the model, but then discarded it
                    EnumQualityRule.Logic.FRACTION_SUM_FOR_PARTY_GROUPS: {
                        QUALITY_RULE_ID: EnumQualityRule.Logic.FRACTION_SUM_FOR_PARTY_GROUPS,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Logic.FRACTION_SUM_FOR_PARTY_GROUPS],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "participaciones_agrupacion_no_suman_1"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_agrupacion"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "miembros"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "suma_participaciones"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E400201
                        ]
                    },
                    EnumQualityRule.Logic.DEPARTMENT_CODE_HAS_TWO_NUMERICAL_CHARACTERS: {
                        QUALITY_RULE_ID: EnumQualityRule.Logic.DEPARTMENT_CODE_HAS_TWO_NUMERICAL_CHARACTERS,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Logic.DEPARTMENT_CODE_HAS_TWO_NUMERICAL_CHARACTERS],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "predio_error_codigo_departamento"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_predio"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E400301
                        ]
                    },
                    EnumQualityRule.Logic.MUNICIPALITY_CODE_HAS_THREE_NUMERICAL_CHARACTERS: {
                        QUALITY_RULE_ID: EnumQualityRule.Logic.MUNICIPALITY_CODE_HAS_THREE_NUMERICAL_CHARACTERS,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Logic.MUNICIPALITY_CODE_HAS_THREE_NUMERICAL_CHARACTERS],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "predio_error_codigo_municipio"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_predio"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E400401
                        ]
                    },
                    EnumQualityRule.Logic.PARCEL_NUMBER_HAS_30_NUMERICAL_CHARACTERS: {
                        QUALITY_RULE_ID: EnumQualityRule.Logic.PARCEL_NUMBER_HAS_30_NUMERICAL_CHARACTERS,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Logic.PARCEL_NUMBER_HAS_30_NUMERICAL_CHARACTERS],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "predio_error_numero_predial"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_predio"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E400501
                        ]
                    },
                    EnumQualityRule.Logic.PARCEL_NUMBER_BEFORE_HAS_20_NUMERICAL_CHARACTERS: {
                        QUALITY_RULE_ID: EnumQualityRule.Logic.PARCEL_NUMBER_BEFORE_HAS_20_NUMERICAL_CHARACTERS,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Logic.PARCEL_NUMBER_BEFORE_HAS_20_NUMERICAL_CHARACTERS],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "predio_error_numero_predial_anterior"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_predio"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E400601
                        ]
                    },
                    EnumQualityRule.Logic.COL_PARTY_NATURAL_TYPE: {
                        QUALITY_RULE_ID: EnumQualityRule.Logic.COL_PARTY_NATURAL_TYPE,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Logic.COL_PARTY_NATURAL_TYPE],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "interesado_natural_inconsistente"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_interesado"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E400701,
                            QUALITY_RULE_ERROR_CODE_E400702,
                            QUALITY_RULE_ERROR_CODE_E400703,
                            QUALITY_RULE_ERROR_CODE_E400704
                        ]
                    },
                    EnumQualityRule.Logic.COL_PARTY_NOT_NATURAL_TYPE: {
                        QUALITY_RULE_ID: EnumQualityRule.Logic.COL_PARTY_NOT_NATURAL_TYPE,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Logic.COL_PARTY_NOT_NATURAL_TYPE],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "interesado_juridico_inconsistente"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_interesado"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E400801,
                            QUALITY_RULE_ERROR_CODE_E400802,
                            QUALITY_RULE_ERROR_CODE_E400803,
                            QUALITY_RULE_ERROR_CODE_E400804
                        ]
                    },
                    EnumQualityRule.Logic.PARCEL_TYPE_AND_22_POSITION_OF_PARCEL_NUMBER: {
                        QUALITY_RULE_ID: EnumQualityRule.Logic.PARCEL_TYPE_AND_22_POSITION_OF_PARCEL_NUMBER,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Logic.PARCEL_TYPE_AND_22_POSITION_OF_PARCEL_NUMBER],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "predio_error_condicion_predio"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_predio"), QVariant.String)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E400901,
                            QUALITY_RULE_ERROR_CODE_E400902,
                            QUALITY_RULE_ERROR_CODE_E400903,
                            QUALITY_RULE_ERROR_CODE_E400904,
                            QUALITY_RULE_ERROR_CODE_E400905,
                            QUALITY_RULE_ERROR_CODE_E400906,
                            QUALITY_RULE_ERROR_CODE_E400907,
                            QUALITY_RULE_ERROR_CODE_E400908
                        ]
                    },
                    EnumQualityRule.Logic.UEBAUNIT_PARCEL: {
                        QUALITY_RULE_ID: EnumQualityRule.Logic.UEBAUNIT_PARCEL,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Logic.UEBAUNIT_PARCEL],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "unidad_espacial_no_corresponde_a_predio"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "id_predio"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "numero_terrenos_asociados"), QVariant.Int),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "numero_construcciones_asociadas"), QVariant.Int),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "numero_unidades_construccion_asociadas"), QVariant.Int)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E401001,
                            QUALITY_RULE_ERROR_CODE_E401002,
                            QUALITY_RULE_ERROR_CODE_E401003,
                            QUALITY_RULE_ERROR_CODE_E401004,
                            QUALITY_RULE_ERROR_CODE_E401005,
                            QUALITY_RULE_ERROR_CODE_E401006,
                            QUALITY_RULE_ERROR_CODE_E401007,
                            QUALITY_RULE_ERROR_CODE_E401008,
                            QUALITY_RULE_ERROR_CODE_E401009,
                            QUALITY_RULE_ERROR_CODE_E401010,
                            QUALITY_RULE_ERROR_CODE_E401011
                        ]
                    },
                    EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_BOUNDARY_POINT: {
                        QUALITY_RULE_ID: EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_BOUNDARY_POINT,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_BOUNDARY_POINT],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "punto_lindero_con_registro_repetido"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "ids_duplicados"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "conteo"), QVariant.Int)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E401101
                        ]
                    },
                    EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_SURVEY_POINT: {
                        QUALITY_RULE_ID: EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_SURVEY_POINT,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_SURVEY_POINT],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "punto_levantamiento_con_registro_repetido"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "ids_duplicados"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "conteo"), QVariant.Int)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E401201
                        ]
                    },
                    EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_CONTROL_POINT: {
                        QUALITY_RULE_ID: EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_CONTROL_POINT,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_CONTROL_POINT],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "punto_control_con_registro_repetido"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "ids_duplicados"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "conteo"), QVariant.Int)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E401301
                        ]
                    },
                    EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_BOUNDARY: {
                        QUALITY_RULE_ID: EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_BOUNDARY,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_BOUNDARY],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "lindero_con_registro_repetido"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "ids_duplicados"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "conteo"), QVariant.Int)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E401401
                        ]
                    },
                    EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_PLOT: {
                        QUALITY_RULE_ID: EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_PLOT,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_PLOT],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "terreno_con_registro_repetido"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "ids_duplicados"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "conteo"), QVariant.Int)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E401501
                        ]
                    },
                    EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_BUILDING: {
                        QUALITY_RULE_ID: EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_BUILDING,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_BUILDING],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "construccion_con_registro_repetido"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "ids_duplicados"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "conteo"), QVariant.Int)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E401601
                        ]
                    },
                    EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_BUILDING_UNIT: {
                        QUALITY_RULE_ID: EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_BUILDING_UNIT,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_BUILDING_UNIT],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "unidad_construccion_con_registro_repetido"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "ids_duplicados"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "conteo"), QVariant.Int)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E401701
                        ]
                    },
                    EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_PARCEL: {
                        QUALITY_RULE_ID: EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_PARCEL,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_PARCEL],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "predio_con_registro_repetido"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "ids_duplicados"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "conteo"), QVariant.Int)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E401801
                        ]
                    },
                    EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_PARTY: {
                        QUALITY_RULE_ID: EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_PARTY,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_PARTY],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "interesado_con_registro_repetido"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "ids_duplicados"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "conteo"), QVariant.Int)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E401901
                        ]
                    },
                    EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_RIGHT: {
                        QUALITY_RULE_ID: EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_RIGHT,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_RIGHT],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "derecho_con_registro_repetido"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "ids_duplicados"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "conteo"), QVariant.Int)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E402001
                        ]
                    },
                    EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_RESTRICTION: {
                        QUALITY_RULE_ID: EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_RESTRICTION,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_RESTRICTION],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "restriccion_con_registro_repetido"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "ids_duplicados"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "conteo"), QVariant.Int)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E402101
                        ]
                    },
                    EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_ADMINISTRATIVE_SOURCE: {
                        QUALITY_RULE_ID: EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_ADMINISTRATIVE_SOURCE,
                        QUALITY_RULE_NAME: translated_strings[EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_ADMINISTRATIVE_SOURCE],
                        QUALITY_RULE_TABLE_NAME: QCoreApplication.translate("QualityRulesConfig", "fuente_administrativa_con_registro_repetido"),
                        QUALITY_RULE_TABLE_FIELDS: [
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "ids_duplicados"), QVariant.String),
                            QgsField(QCoreApplication.translate("QualityRulesConfig", "conteo"), QVariant.Int)
                        ],
                        QUALITY_RULE_DOMAIN_ERROR_CODES: [
                            QUALITY_RULE_ERROR_CODE_E402201
                        ]
                    },
                }
            }
        }

    @staticmethod
    def get_quality_rules_layer_config(names):
        return {
            EnumQualityRule.Point.OVERLAPS_IN_BOUNDARY_POINTS: {
                QUALITY_RULE_LADM_COL_LAYERS: [names.LC_BOUNDARY_POINT_T],
                QUALITY_RULE_ADJUSTED_LAYERS: {
                    names.LC_BOUNDARY_POINT_T: {
                        ADJUSTED_INPUT_LAYER: names.LC_BOUNDARY_POINT_T,
                        ADJUSTED_REFERENCE_LAYER: names.LC_BOUNDARY_POINT_T}
                }
            }, EnumQualityRule.Point.OVERLAPS_IN_CONTROL_POINTS: {
                QUALITY_RULE_LADM_COL_LAYERS: [names.LC_CONTROL_POINT_T],
                QUALITY_RULE_ADJUSTED_LAYERS: {
                    names.LC_CONTROL_POINT_T: {
                        ADJUSTED_INPUT_LAYER: names.LC_CONTROL_POINT_T,
                        ADJUSTED_REFERENCE_LAYER: names.LC_CONTROL_POINT_T}
                }
            }, EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES: {
                QUALITY_RULE_LADM_COL_LAYERS: [names.LC_BOUNDARY_T,
                                      names.POINT_BFS_T,
                                      names.LC_BOUNDARY_POINT_T],
                QUALITY_RULE_ADJUSTED_LAYERS: {
                    names.LC_BOUNDARY_T: {
                        ADJUSTED_INPUT_LAYER: names.LC_BOUNDARY_T,
                        ADJUSTED_REFERENCE_LAYER: names.LC_BOUNDARY_POINT_T}
                }
            }, EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_PLOT_NODES: {
                QUALITY_RULE_LADM_COL_LAYERS: [names.LC_PLOT_T,
                                      names.LC_BOUNDARY_POINT_T],
                QUALITY_RULE_ADJUSTED_LAYERS: {
                    names.LC_PLOT_T: {
                        ADJUSTED_INPUT_LAYER: names.LC_PLOT_T,
                        ADJUSTED_REFERENCE_LAYER: names.LC_BOUNDARY_POINT_T
                    }
                }
            }, EnumQualityRule.Line.OVERLAPS_IN_BOUNDARIES: {
                QUALITY_RULE_LADM_COL_LAYERS: [names.LC_BOUNDARY_T],
                QUALITY_RULE_ADJUSTED_LAYERS: {
                    names.LC_BOUNDARY_T: {
                        ADJUSTED_INPUT_LAYER: names.LC_BOUNDARY_T,
                        ADJUSTED_REFERENCE_LAYER: names.LC_BOUNDARY_T,
                        FIX_ADJUSTED_LAYER: True
                    }
                }
            }, EnumQualityRule.Line.BOUNDARIES_ARE_NOT_SPLIT: {
                QUALITY_RULE_LADM_COL_LAYERS: [names.LC_BOUNDARY_T],
                QUALITY_RULE_ADJUSTED_LAYERS: {
                    names.LC_BOUNDARY_T: {
                        ADJUSTED_INPUT_LAYER: names.LC_BOUNDARY_T,
                        ADJUSTED_REFERENCE_LAYER: names.LC_BOUNDARY_T
                    }
                }
            }, EnumQualityRule.Line.BOUNDARIES_COVERED_BY_PLOTS: {
                QUALITY_RULE_LADM_COL_LAYERS: [names.LC_PLOT_T,
                                      names.LC_BOUNDARY_T,
                                      names.LESS_BFS_T,
                                      names.MORE_BFS_T],
                QUALITY_RULE_ADJUSTED_LAYERS: {
                    names.LC_PLOT_T: {
                        ADJUSTED_INPUT_LAYER: names.LC_PLOT_T,
                        ADJUSTED_REFERENCE_LAYER: names.LC_BOUNDARY_T
                    }
                }
            }, EnumQualityRule.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS: {
                QUALITY_RULE_LADM_COL_LAYERS: [names.LC_BOUNDARY_POINT_T,
                                      names.POINT_BFS_T,
                                      names.LC_BOUNDARY_T],
                QUALITY_RULE_ADJUSTED_LAYERS: {
                    names.LC_BOUNDARY_T: {
                        ADJUSTED_INPUT_LAYER: names.LC_BOUNDARY_T,
                        ADJUSTED_REFERENCE_LAYER: names.LC_BOUNDARY_POINT_T
                    }
                }
            }, EnumQualityRule.Line.DANGLES_IN_BOUNDARIES: {
                QUALITY_RULE_LADM_COL_LAYERS: [names.LC_BOUNDARY_T],
                QUALITY_RULE_ADJUSTED_LAYERS: {
                    names.LC_BOUNDARY_T: {
                        ADJUSTED_INPUT_LAYER: names.LC_BOUNDARY_T,
                        ADJUSTED_REFERENCE_LAYER: names.LC_BOUNDARY_T
                    }
                }
            }, EnumQualityRule.Polygon.OVERLAPS_IN_PLOTS: {
                QUALITY_RULE_LADM_COL_LAYERS: [names.LC_PLOT_T],
                QUALITY_RULE_ADJUSTED_LAYERS: {
                    names.LC_PLOT_T: {
                        ADJUSTED_INPUT_LAYER: names.LC_PLOT_T,
                        ADJUSTED_REFERENCE_LAYER: names.LC_PLOT_T,
                        FIX_ADJUSTED_LAYER: True
                    }
                }
            }, EnumQualityRule.Polygon.OVERLAPS_IN_BUILDINGS: {
                QUALITY_RULE_LADM_COL_LAYERS: [names.LC_BUILDING_T],
                QUALITY_RULE_ADJUSTED_LAYERS: {
                    names.LC_BUILDING_T: {
                        ADJUSTED_INPUT_LAYER: names.LC_BUILDING_T,
                        ADJUSTED_REFERENCE_LAYER: names.LC_BUILDING_T
                    }
                }
            }, EnumQualityRule.Polygon.OVERLAPS_IN_RIGHTS_OF_WAY: {
                QUALITY_RULE_LADM_COL_LAYERS: [names.LC_RIGHT_OF_WAY_T],
                QUALITY_RULE_ADJUSTED_LAYERS: {
                    names.LC_RIGHT_OF_WAY_T: {
                        ADJUSTED_INPUT_LAYER: names.LC_RIGHT_OF_WAY_T,
                        ADJUSTED_REFERENCE_LAYER: names.LC_RIGHT_OF_WAY_T
                    }
                }
            }, EnumQualityRule.Polygon.PLOTS_COVERED_BY_BOUNDARIES: {
                QUALITY_RULE_LADM_COL_LAYERS: [names.LC_PLOT_T,
                                      names.LC_BOUNDARY_T,
                                      names.LESS_BFS_T,
                                      names.MORE_BFS_T],
                QUALITY_RULE_ADJUSTED_LAYERS: {
                    names.LC_PLOT_T: {
                        ADJUSTED_INPUT_LAYER: names.LC_PLOT_T,
                        ADJUSTED_REFERENCE_LAYER: names.LC_PLOT_T,
                        FIX_ADJUSTED_LAYER: True
                    }, names.LC_BOUNDARY_T: {  # This one uses an adjusted layer as reference layer!
                        ADJUSTED_INPUT_LAYER: names.LC_BOUNDARY_T,
                        ADJUSTED_REFERENCE_LAYER: get_key_for_quality_rule_adjusted_layer(names.LC_PLOT_T, names.LC_PLOT_T, True),
                        FIX_ADJUSTED_LAYER: True
                    }
                }
            }, EnumQualityRule.Polygon.RIGHT_OF_WAY_OVERLAPS_BUILDINGS: {
                QUALITY_RULE_LADM_COL_LAYERS: [names.LC_RIGHT_OF_WAY_T,
                                      names.LC_BUILDING_T],
                QUALITY_RULE_ADJUSTED_LAYERS: {
                    names.LC_RIGHT_OF_WAY_T: {
                        ADJUSTED_INPUT_LAYER: names.LC_RIGHT_OF_WAY_T,
                        ADJUSTED_REFERENCE_LAYER: names.LC_BUILDING_T
                    }
                }
            }, EnumQualityRule.Polygon.GAPS_IN_PLOTS: {
                QUALITY_RULE_LADM_COL_LAYERS: [names.LC_PLOT_T],
                QUALITY_RULE_ADJUSTED_LAYERS: {
                    names.LC_PLOT_T: {
                        ADJUSTED_INPUT_LAYER: names.LC_PLOT_T,
                        ADJUSTED_REFERENCE_LAYER: names.LC_PLOT_T,
                        FIX_ADJUSTED_LAYER: True
                    }
                }
            }, EnumQualityRule.Polygon.MULTIPART_IN_RIGHT_OF_WAY: {
                QUALITY_RULE_LADM_COL_LAYERS: [names.LC_RIGHT_OF_WAY_T]
            }, EnumQualityRule.Polygon.PLOT_NODES_COVERED_BY_BOUNDARY_POINTS: {
                QUALITY_RULE_LADM_COL_LAYERS: [names.LC_PLOT_T,
                                               names.LC_BOUNDARY_POINT_T],
                QUALITY_RULE_ADJUSTED_LAYERS: {
                    names.LC_PLOT_T: {
                        ADJUSTED_INPUT_LAYER: names.LC_PLOT_T,
                        ADJUSTED_REFERENCE_LAYER: names.LC_BOUNDARY_POINT_T
                    }
                }
            }, EnumQualityRule.Polygon.BUILDINGS_SHOULD_BE_WITHIN_PLOTS: {
                QUALITY_RULE_LADM_COL_LAYERS: [names.LC_BUILDING_T,
                                               names.LC_PLOT_T,
                                               names.LC_PARCEL_T,
                                               names.COL_UE_BAUNIT_T,
                                               names.LC_CONDITION_PARCEL_TYPE_D],
                QUALITY_RULE_ADJUSTED_LAYERS: {
                    names.LC_BUILDING_T: {
                        ADJUSTED_INPUT_LAYER: names.LC_BUILDING_T,
                        ADJUSTED_REFERENCE_LAYER: names.LC_PLOT_T,
                        ADJUSTED_BEHAVIOR: 0,
                        ADJUSTED_TOPOLOGICAL_POINTS: True
                    }
                }
            }, EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_PLOTS: {
                QUALITY_RULE_LADM_COL_LAYERS: [names.LC_BUILDING_UNIT_T,
                                               names.LC_PLOT_T,
                                               names.LC_PARCEL_T,
                                               names.COL_UE_BAUNIT_T,
                                               names.LC_CONDITION_PARCEL_TYPE_D],
                QUALITY_RULE_ADJUSTED_LAYERS: {
                    names.LC_BUILDING_UNIT_T: {
                        ADJUSTED_INPUT_LAYER: names.LC_BUILDING_UNIT_T,
                        ADJUSTED_REFERENCE_LAYER: names.LC_PLOT_T,
                        ADJUSTED_BEHAVIOR: 0,
                        ADJUSTED_TOPOLOGICAL_POINTS: True
                    }
                }
            }, EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_BUILDINGS: {
                QUALITY_RULE_LADM_COL_LAYERS: [names.LC_BUILDING_T,
                                               names.LC_BUILDING_UNIT_T,
                                               names.LC_PARCEL_T,
                                               names.COL_UE_BAUNIT_T,
                                               names.LC_CONDITION_PARCEL_TYPE_D],
                QUALITY_RULE_ADJUSTED_LAYERS: {
                    names.LC_BUILDING_UNIT_T: {
                        ADJUSTED_INPUT_LAYER: names.LC_BUILDING_UNIT_T,
                        ADJUSTED_REFERENCE_LAYER: names.LC_BUILDING_T,
                        ADJUSTED_BEHAVIOR: 0,
                        ADJUSTED_TOPOLOGICAL_POINTS: True
                    }
                }
            }
        }
