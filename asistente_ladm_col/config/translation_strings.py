from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication)
from asistente_ladm_col.config.enums import EnumQualityRule
from asistente_ladm_col.config.quality_rules_config import (QUALITY_RULE_ERROR_CODE_E1001,
                                                            QUALITY_RULE_ERROR_CODE_E1002,
                                                            QUALITY_RULE_ERROR_CODE_E100301,
                                                            QUALITY_RULE_ERROR_CODE_E100302,
                                                            QUALITY_RULE_ERROR_CODE_E100303,
                                                            QUALITY_RULE_ERROR_CODE_E1004,
                                                            QUALITY_RULE_ERROR_CODE_E2001,
                                                            QUALITY_RULE_ERROR_CODE_E2002,
                                                            QUALITY_RULE_ERROR_CODE_E200301,
                                                            QUALITY_RULE_ERROR_CODE_E200302,
                                                            QUALITY_RULE_ERROR_CODE_E200303,
                                                            QUALITY_RULE_ERROR_CODE_E200304,
                                                            QUALITY_RULE_ERROR_CODE_E200305,
                                                            QUALITY_RULE_ERROR_CODE_E200401,
                                                            QUALITY_RULE_ERROR_CODE_E200402,
                                                            QUALITY_RULE_ERROR_CODE_E200403,
                                                            QUALITY_RULE_ERROR_CODE_E2005,
                                                            QUALITY_RULE_ERROR_CODE_E3001,
                                                            QUALITY_RULE_ERROR_CODE_E3002,
                                                            QUALITY_RULE_ERROR_CODE_E3003,
                                                            QUALITY_RULE_ERROR_CODE_E300401,
                                                            QUALITY_RULE_ERROR_CODE_E300402,
                                                            QUALITY_RULE_ERROR_CODE_E300403,
                                                            QUALITY_RULE_ERROR_CODE_E300404,
                                                            QUALITY_RULE_ERROR_CODE_E300405,
                                                            QUALITY_RULE_ERROR_CODE_E3005,
                                                            QUALITY_RULE_ERROR_CODE_E3006,
                                                            QUALITY_RULE_ERROR_CODE_E3007,
                                                            QUALITY_RULE_ERROR_CODE_E3008,
                                                            QUALITY_RULE_ERROR_CODE_E300901,
                                                            QUALITY_RULE_ERROR_CODE_E300902,
                                                            QUALITY_RULE_ERROR_CODE_E300903,
                                                            QUALITY_RULE_ERROR_CODE_E301001,
                                                            QUALITY_RULE_ERROR_CODE_E301002,
                                                            QUALITY_RULE_ERROR_CODE_E301003,
                                                            QUALITY_RULE_ERROR_CODE_E301004,
                                                            QUALITY_RULE_ERROR_CODE_E301005,
                                                            QUALITY_RULE_ERROR_CODE_E301006,
                                                            QUALITY_RULE_ERROR_CODE_E400101,
                                                            QUALITY_RULE_ERROR_CODE_E400102,
                                                            QUALITY_RULE_ERROR_CODE_E4002,
                                                            QUALITY_RULE_ERROR_CODE_E4003,
                                                            QUALITY_RULE_ERROR_CODE_E4004,
                                                            QUALITY_RULE_ERROR_CODE_E4005,
                                                            QUALITY_RULE_ERROR_CODE_E4006,
                                                            QUALITY_RULE_ERROR_CODE_E4007,
                                                            QUALITY_RULE_ERROR_CODE_E400801,
                                                            QUALITY_RULE_ERROR_CODE_E400802,
                                                            QUALITY_RULE_ERROR_CODE_E400803,
                                                            QUALITY_RULE_ERROR_CODE_E400804,
                                                            QUALITY_RULE_ERROR_CODE_E400901,
                                                            QUALITY_RULE_ERROR_CODE_E400902,
                                                            QUALITY_RULE_ERROR_CODE_E400903,
                                                            QUALITY_RULE_ERROR_CODE_E400904,
                                                            QUALITY_RULE_ERROR_CODE_E401001,
                                                            QUALITY_RULE_ERROR_CODE_E401002,
                                                            QUALITY_RULE_ERROR_CODE_E401003,
                                                            QUALITY_RULE_ERROR_CODE_E401004,
                                                            QUALITY_RULE_ERROR_CODE_E401005,
                                                            QUALITY_RULE_ERROR_CODE_E401006,
                                                            QUALITY_RULE_ERROR_CODE_E401007,
                                                            QUALITY_RULE_ERROR_CODE_E401008,
                                                            QUALITY_RULE_ERROR_CODE_E401101,
                                                            QUALITY_RULE_ERROR_CODE_E401102,
                                                            QUALITY_RULE_ERROR_CODE_E401103,
                                                            QUALITY_RULE_ERROR_CODE_E401104,
                                                            QUALITY_RULE_ERROR_CODE_E401105,
                                                            QUALITY_RULE_ERROR_CODE_E401106,
                                                            QUALITY_RULE_ERROR_CODE_E401107,
                                                            QUALITY_RULE_ERROR_CODE_E401108,
                                                            QUALITY_RULE_ERROR_CODE_E401109,
                                                            QUALITY_RULE_ERROR_CODE_E401110,
                                                            QUALITY_RULE_ERROR_CODE_E401111)

ERROR_LAYER_GROUP = "ERROR_LAYER_GROUP"
RIGHT_OF_WAY_LINE_LAYER = "RIGHT_OF_WAY_LINE_LAYER"

TOOLBAR_BUILD_BOUNDARY = QCoreApplication.translate("TranslatableConfigStrings", "Build boundaries...")
TOOLBAR_MOVE_NODES = QCoreApplication.translate("TranslatableConfigStrings", "Move nodes...")
TOOLBAR_FILL_POINT_BFS = QCoreApplication.translate("TranslatableConfigStrings", "Fill Point BFS")
TOOLBAR_FILL_MORE_BFS_LESS = QCoreApplication.translate("TranslatableConfigStrings", "Fill More BFS and Less")
TOOLBAR_FILL_RIGHT_OF_WAY_RELATIONS = QCoreApplication.translate("TranslatableConfigStrings", "Fill Right of Way Relations")
TOOLBAR_IMPORT_FROM_INTERMEDIATE_STRUCTURE = QCoreApplication.translate("TranslatableConfigStrings", "Import from intermediate structure")
TOOLBAR_FINALIZE_GEOMETRY_CREATION = QCoreApplication.translate("TranslatableConfigStrings", "Finalize geometry creation")


class TranslatableConfigStrings(QObject):
    help_get_domain_code_from_value = QCoreApplication.translate("TranslatableConfigStrings", "Gets the t_id that corresponds to a domain value") + \
                                         QCoreApplication.translate("TranslatableConfigStrings", "<h4>Syntax</h4>") + \
                                         "<span class=\"functionname\">get_domain_code_from_value</span>(" \
                                         "<span class=\"argument\">domain_table</span>," \
                                         "<span class=\"argument\">value</span>," \
                                         "<span class=\"argument\">value_is_ilicode</span>," \
                                         "<span class=\"argument\">validate_conn</span>)" + \
                                         QCoreApplication.translate("TranslatableConfigStrings", "<h4>Arguments</h4>") + \
                                         "<span class=\"argument\">domain_table</span> " + QCoreApplication.translate("TranslatableConfigStrings", "Domain table name or layer obj") + \
                                         "<br><span class=\"argument\">value</span> " + QCoreApplication.translate("TranslatableConfigStrings", "Domain value to look for") + \
                                         "<br><span class=\"argument\">value_is_ilicode</span> " + QCoreApplication.translate("TranslatableConfigStrings", "Whether value is iliCode or dispName") + \
                                         "<br><span class=\"argument\">validate_conn</span> " + QCoreApplication.translate("TranslatableConfigStrings", "Whether validate connection or not") + \
                                         QCoreApplication.translate("TranslatableConfigStrings", "<h4>Examples</h4>") + \
                                         """<pre>get_domain_code_from_value( 
  'op_condicionprediotipo',
  'NPH',
  True,
  False) → {}</pre>""".format(QCoreApplication.translate("TranslatableConfigStrings", "Gets the t_id of NPH in\n  domain op_condicion_predio"))

    def __init__(self):
        pass

    def get_translatable_config_strings(self):
        return {
            EnumQualityRule.Point.OVERLAPS_IN_BOUNDARY_POINTS: QCoreApplication.translate("TranslatableConfigStrings", "Boundary Points should not overlap"),
            EnumQualityRule.Point.OVERLAPS_IN_CONTROL_POINTS: QCoreApplication.translate("TranslatableConfigStrings", "Control Points should not overlap"),
            EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES: QCoreApplication.translate("TranslatableConfigStrings", "Boundary Points should be covered by Boundary nodes"),
            EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_PLOT_NODES: QCoreApplication.translate("TranslatableConfigStrings", "Boundary Points should be covered by plot nodes"),
            EnumQualityRule.Line.OVERLAPS_IN_BOUNDARIES: QCoreApplication.translate("TranslatableConfigStrings", "Boundaries should not overlap"),
            EnumQualityRule.Line.BOUNDARIES_ARE_NOT_SPLIT: QCoreApplication.translate("TranslatableConfigStrings", "Boundaries should not be split"),
            EnumQualityRule.Line.BOUNDARIES_COVERED_BY_PLOTS: QCoreApplication.translate("TranslatableConfigStrings", "Boundaries should be covered by Plots"),
            EnumQualityRule.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS: QCoreApplication.translate("TranslatableConfigStrings", "Boundary nodes should be covered by Boundary Points"),
            EnumQualityRule.Line.DANGLES_IN_BOUNDARIES: QCoreApplication.translate("TranslatableConfigStrings", "Boundaries should not have dangles"),
            EnumQualityRule.Polygon.OVERLAPS_IN_PLOTS: QCoreApplication.translate("TranslatableConfigStrings", "Plots should not overlap"),
            EnumQualityRule.Polygon.OVERLAPS_IN_BUILDINGS: QCoreApplication.translate("TranslatableConfigStrings", "Buildings should not overlap"),
            EnumQualityRule.Polygon.OVERLAPS_IN_RIGHTS_OF_WAY: QCoreApplication.translate("TranslatableConfigStrings", "Rights of Way should not overlap"),
            EnumQualityRule.Polygon.PLOTS_COVERED_BY_BOUNDARIES: QCoreApplication.translate("TranslatableConfigStrings", "Plots should be covered by Boundaries"),
            EnumQualityRule.Polygon.PLOT_NODES_COVERED_BY_BOUNDARY_POINTS: QCoreApplication.translate("TranslatableConfigStrings", "Plot nodes should be covered by boundary points"),
            EnumQualityRule.Polygon.RIGHT_OF_WAY_OVERLAPS_BUILDINGS: QCoreApplication.translate("TranslatableConfigStrings", "Right of Way should not overlap Buildings"),
            EnumQualityRule.Polygon.GAPS_IN_PLOTS: QCoreApplication.translate("TranslatableConfigStrings", "Plots should not have gaps"),
            EnumQualityRule.Polygon.MULTIPART_IN_RIGHT_OF_WAY: QCoreApplication.translate("TranslatableConfigStrings", "Right of Way should not have multipart geometries"),
            EnumQualityRule.Polygon.BUILDINGS_SHOULD_BE_WITHIN_PLOTS: QCoreApplication.translate("TranslatableConfigStrings", "Buildings should be within Plots"),
            EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_PLOTS: QCoreApplication.translate("TranslatableConfigStrings", "Building Units should be within plots and buildings associates"),
            EnumQualityRule.Logic.PARCEL_RIGHT_RELATIONSHIP: QCoreApplication.translate("TranslatableConfigStrings", "Parcel should have one and only one Right"),
            EnumQualityRule.Logic.FRACTION_SUM_FOR_PARTY_GROUPS: QCoreApplication.translate("TranslatableConfigStrings", "Group Party Fractions should sum 1"),
            EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_A_TABLE: QCoreApplication.translate("TranslatableConfigStrings", "Table records should not be repeated"),
            EnumQualityRule.Logic.DEPARTMENT_CODE_HAS_TWO_NUMERICAL_CHARACTERS: QCoreApplication.translate("TranslatableConfigStrings", "Check that the department field of the parcel table has two numerical characters"),
            EnumQualityRule.Logic.MUNICIPALITY_CODE_HAS_THREE_NUMERICAL_CHARACTERS: QCoreApplication.translate("TranslatableConfigStrings", "Check that the municipality field of the parcel table has three numerical characters"),
            EnumQualityRule.Logic.PARCEL_NUMBER_HAS_30_NUMERICAL_CHARACTERS: QCoreApplication.translate("TranslatableConfigStrings", "Check that the parcel number has 30 numerical characters"),
            EnumQualityRule.Logic.PARCEL_NUMBER_BEFORE_HAS_20_NUMERICAL_CHARACTERS: QCoreApplication.translate("TranslatableConfigStrings", "Check that the parcel number before has 20 numerical characters"),
            EnumQualityRule.Logic.COL_PARTY_NATURAL_TYPE: QCoreApplication.translate("TranslatableConfigStrings", "Check that parties of type natural cannot include data of a legal party"),
            EnumQualityRule.Logic.COL_PARTY_NOT_NATURAL_TYPE: QCoreApplication.translate("TranslatableConfigStrings", "Check that parties of type legal cannot include data of a natural party"),
            EnumQualityRule.Logic.PARCEL_TYPE_AND_22_POSITION_OF_PARCEL_NUMBER: QCoreApplication.translate("TranslatableConfigStrings", "Check that the type of parcel corresponds to position 22 of the parcel number"),
            EnumQualityRule.Logic.UEBAUNIT_PARCEL: QCoreApplication.translate("TranslatableConfigStrings", "Check that Spatial Units associated with Parcels correspond to the parcel type"),

            # Domain errors message
            # ERROR CODES FOR POINT QUALITY RULES
            QUALITY_RULE_ERROR_CODE_E1001: QCoreApplication.translate("TranslatableConfigStrings", "Los puntos de lindero no deben superponerse"),
            QUALITY_RULE_ERROR_CODE_E1002: QCoreApplication.translate("TranslatableConfigStrings", "Los puntos de control no deben superponerse"),
            QUALITY_RULE_ERROR_CODE_E100301: QCoreApplication.translate("TranslatableConfigStrings", "Punto lindero no esta cubierto por un nodo de lindero"),
            QUALITY_RULE_ERROR_CODE_E100302: QCoreApplication.translate("TranslatableConfigStrings", "La relación topológica entre el punto lindero y el nodo de un lindero no está registra en la tabla puntoccl"),
            QUALITY_RULE_ERROR_CODE_E100303: QCoreApplication.translate("TranslatableConfigStrings", "La relación topológica entre el punto lindero y el nodo de un lindero está duplicada en la tabla puntoccl"),
            QUALITY_RULE_ERROR_CODE_E1004: QCoreApplication.translate("TranslatableConfigStrings", "El punto de lindero no está cubierto por un nodo de un terreno"),

            # ERROR CODES FOR LINE QUALITY RULES
            QUALITY_RULE_ERROR_CODE_E2001: QCoreApplication.translate("TranslatableConfigStrings", "Los linderos no deben superponerse"),
            QUALITY_RULE_ERROR_CODE_E2002: QCoreApplication.translate("TranslatableConfigStrings", "El lindero debe terminar en cambio de colindancia"),
            QUALITY_RULE_ERROR_CODE_E200301: QCoreApplication.translate("TranslatableConfigStrings", "El lindero no está cubierto por terreno"),
            QUALITY_RULE_ERROR_CODE_E200302: QCoreApplication.translate("TranslatableConfigStrings", "La relación topológica entre lindero y terreno está duplicada en la tabla masccl"),
            QUALITY_RULE_ERROR_CODE_E200303: QCoreApplication.translate("TranslatableConfigStrings", "La relación topológica entre lindero y terreno está duplicada en la tabla menosccl"),
            QUALITY_RULE_ERROR_CODE_E200304: QCoreApplication.translate("TranslatableConfigStrings", "La relación topológica entre lindero y terreno no está registrada en la tabla masccl"),
            QUALITY_RULE_ERROR_CODE_E200305: QCoreApplication.translate("TranslatableConfigStrings", "La relación topológica entre lindero y terreno no está registrada en la tabla menosccl"),
            QUALITY_RULE_ERROR_CODE_E200401: QCoreApplication.translate("TranslatableConfigStrings", "Nodo lindero no está cubierto por un punto lindero"),
            QUALITY_RULE_ERROR_CODE_E200402: QCoreApplication.translate("TranslatableConfigStrings", "La relación topológica entre el punto lindero y el nodo de un lindero no está registra en la tabla puntoccl"),
            QUALITY_RULE_ERROR_CODE_E200403: QCoreApplication.translate("TranslatableConfigStrings", "La relación topológica entre el punto lindero y el nodo de un lindero está duplicada en la tabla puntoccl"),
            QUALITY_RULE_ERROR_CODE_E2005: QCoreApplication.translate("TranslatableConfigStrings", "El lindero no debe tener nodos sin conectar"),

            # ERROR CODES FOR POLYGON QUALITY RULES
            QUALITY_RULE_ERROR_CODE_E3001: QCoreApplication.translate("TranslatableConfigStrings", "Los terrenos no deben superponerse"),
            QUALITY_RULE_ERROR_CODE_E3002: QCoreApplication.translate("TranslatableConfigStrings", "Las construcciones no deben superponerse"),
            QUALITY_RULE_ERROR_CODE_E3003: QCoreApplication.translate("TranslatableConfigStrings", "Las servidumbres de paso no deben superponerse"),
            QUALITY_RULE_ERROR_CODE_E300401: QCoreApplication.translate("TranslatableConfigStrings", "El terreno no está cubierto por linderos"),
            QUALITY_RULE_ERROR_CODE_E300402: QCoreApplication.translate("TranslatableConfigStrings", "La relación topológica entre lindero y terreno está duplicada en la tabla masccl"),
            QUALITY_RULE_ERROR_CODE_E300403: QCoreApplication.translate("TranslatableConfigStrings", "La relación topológica entre lindero y terreno está duplicada en la tabla menosccl"),
            QUALITY_RULE_ERROR_CODE_E300404: QCoreApplication.translate("TranslatableConfigStrings", "La relación topológica entre lindero y terreno no está registrada en la tabla masccl"),
            QUALITY_RULE_ERROR_CODE_E300405: QCoreApplication.translate("TranslatableConfigStrings", "La relación topológica entre lindero y terreno no está registrada en la tabla menosccl"),
            QUALITY_RULE_ERROR_CODE_E3005: QCoreApplication.translate("TranslatableConfigStrings", "La servidumbre de paso no se debe superponer con la construcción"),
            QUALITY_RULE_ERROR_CODE_E3006: QCoreApplication.translate("TranslatableConfigStrings", "No debe haber hueco entre terrenos"),
            QUALITY_RULE_ERROR_CODE_E3007: QCoreApplication.translate("TranslatableConfigStrings", "Servidumbre de paso no debe tener geometría multiparte"),
            QUALITY_RULE_ERROR_CODE_E3008: QCoreApplication.translate("TranslatableConfigStrings", "El nodo del terreno no está cubierto por un punto lindero"),
            QUALITY_RULE_ERROR_CODE_E300901: QCoreApplication.translate("TranslatableConfigStrings", "La construcción no está dentro de ningún terreno"),
            QUALITY_RULE_ERROR_CODE_E300902: QCoreApplication.translate("TranslatableConfigStrings", "La construcción cruza los límites de un terreno"),
            QUALITY_RULE_ERROR_CODE_E300903: QCoreApplication.translate("TranslatableConfigStrings", "La construcción está dentro de un terreno pero no dentro de su terreno correspondiente"),
            QUALITY_RULE_ERROR_CODE_E301001: QCoreApplication.translate("TranslatableConfigStrings", "La unidad de construcción no está dentro de ningún terreno"),
            QUALITY_RULE_ERROR_CODE_E301002: QCoreApplication.translate("TranslatableConfigStrings", "La unidad de construcción cruza los límites de un terreno"),
            QUALITY_RULE_ERROR_CODE_E301003: QCoreApplication.translate("TranslatableConfigStrings", "La unidad de construcción está dentro de un terreno pero no dentro de su terreno correspondiente"),
            QUALITY_RULE_ERROR_CODE_E301004: QCoreApplication.translate("TranslatableConfigStrings", "La unidad de construcción no está dentro de ninguna contrucción"),
            QUALITY_RULE_ERROR_CODE_E301005: QCoreApplication.translate("TranslatableConfigStrings", "La unidad de construcción cruza los límites de un construcción"),
            QUALITY_RULE_ERROR_CODE_E301006: QCoreApplication.translate("TranslatableConfigStrings", "La unidad de construcción está dentro de una construcción pero no dentro de su construcción correspondiente"),

            # ERROR CODES FOR LOGIC QUALITY RULES
            QUALITY_RULE_ERROR_CODE_E400101: QCoreApplication.translate("TranslatableConfigStrings", "El predio tiene más de un derecho de dominio asociado"),
            QUALITY_RULE_ERROR_CODE_E400102: QCoreApplication.translate("TranslatableConfigStrings", "El predio no tiene derecho asociado"),
            QUALITY_RULE_ERROR_CODE_E4002: QCoreApplication.translate("TranslatableConfigStrings", "La tabla no debe tener registros repetidos"),
            QUALITY_RULE_ERROR_CODE_E4003: QCoreApplication.translate("TranslatableConfigStrings", "Los porcentajes de participación de la agrupación de interesados deben sumar uno (1)"),
            QUALITY_RULE_ERROR_CODE_E4004: QCoreApplication.translate("TranslatableConfigStrings", "El código de departamento debe tener dos caracteres numéricos"),
            QUALITY_RULE_ERROR_CODE_E4005: QCoreApplication.translate("TranslatableConfigStrings", "El código de municipio debe tener tres caracteres numéricos"),
            QUALITY_RULE_ERROR_CODE_E4006: QCoreApplication.translate("TranslatableConfigStrings", "El número predial debe tiener 30 caracteres numéricos"),
            QUALITY_RULE_ERROR_CODE_E4007: QCoreApplication.translate("TranslatableConfigStrings", "El número predial anterior debe tener 20 caracteres numéricos"),
            QUALITY_RULE_ERROR_CODE_E400801: QCoreApplication.translate("TranslatableConfigStrings", "La razón social no debe estar diligenciada"),
            QUALITY_RULE_ERROR_CODE_E400802: QCoreApplication.translate("TranslatableConfigStrings", "El primer apellido es obligatorio y debe estar diligenciado"),
            QUALITY_RULE_ERROR_CODE_E400803: QCoreApplication.translate("TranslatableConfigStrings", "El primer nombre es obligatorio y debe estar diligenciado"),
            QUALITY_RULE_ERROR_CODE_E400804: QCoreApplication.translate("TranslatableConfigStrings", "El tipo de documento debe ser diferente de NIT"),
            QUALITY_RULE_ERROR_CODE_E400901: QCoreApplication.translate("TranslatableConfigStrings", "Razón social debe estar diligenciada"),
            QUALITY_RULE_ERROR_CODE_E400902: QCoreApplication.translate("TranslatableConfigStrings", "Primer apellido no debe estar diligenciada"),
            QUALITY_RULE_ERROR_CODE_E400903: QCoreApplication.translate("TranslatableConfigStrings", "Primer nombre no debe estar diligenciada"),
            QUALITY_RULE_ERROR_CODE_E400904: QCoreApplication.translate("TranslatableConfigStrings", "Tipo de documento debe ser NIT o Secuencial IGAC o Secuencial SNR"),
            QUALITY_RULE_ERROR_CODE_E401001: QCoreApplication.translate("TranslatableConfigStrings", "Cuando la condicion del predio es 'Bien de uso publico' la posición 22 del número predial debe ser 3"),
            QUALITY_RULE_ERROR_CODE_E401002: QCoreApplication.translate("TranslatableConfigStrings", "Cuando la condicion del predio es 'Condominio Matriz' o 'Condominio Unidad Predial' la posición 22 del número predial debe ser 8"),
            QUALITY_RULE_ERROR_CODE_E401003: QCoreApplication.translate("TranslatableConfigStrings", "Cuando la condicion del predio es 'Mejora en NPH' la posición 22 del número predial debe ser 5"),
            QUALITY_RULE_ERROR_CODE_E401004: QCoreApplication.translate("TranslatableConfigStrings", "Cuando la condicion del predio es 'Mejora en PH' la posición 22 del número predial debe ser 5"),
            QUALITY_RULE_ERROR_CODE_E401005: QCoreApplication.translate("TranslatableConfigStrings", "Cuando la condicion del predio es 'NPH' la posición 22 del número predial debe ser 0"),
            QUALITY_RULE_ERROR_CODE_E401006: QCoreApplication.translate("TranslatableConfigStrings", "Cuando la condición del predio es 'Parque Cementerio Matriz' o 'Parque Cementerio Unidad Predial' la posición 22 del número predial debe ser 7"),
            QUALITY_RULE_ERROR_CODE_E401007: QCoreApplication.translate("TranslatableConfigStrings", "Cuando la condicion del predio es 'PH Matriz' o 'PH Unidad Predial' la posición 22 del número predial debe ser 9"),
            QUALITY_RULE_ERROR_CODE_E401008: QCoreApplication.translate("TranslatableConfigStrings", "Cuando la condicion del predio es 'Vía' la posición 22 del número predial debe ser 4"),
            QUALITY_RULE_ERROR_CODE_E401101: QCoreApplication.translate("TranslatableConfigStrings", "Cuando la condición del predio es 'Bien de Uso Publico', el predio debe tener asociado 1 terreno y 0 unidades de construcción"),
            QUALITY_RULE_ERROR_CODE_E401102: QCoreApplication.translate("TranslatableConfigStrings", "Cuando la condición del predio es 'Condominio Matriz', el predio debe tener asociado 1 terreno y 0 unidades de construcción"),
            QUALITY_RULE_ERROR_CODE_E401103: QCoreApplication.translate("TranslatableConfigStrings", "Cuando la condición del predio es 'Condominio Unidad Predial', el predio debe tener asociado 1 terreno y 0 unidades de construcción"),
            QUALITY_RULE_ERROR_CODE_E401104: QCoreApplication.translate("TranslatableConfigStrings", "Cuando la condición del predio es 'Mejora en NPH', el predio debe tener asociado 0 terrenos y 1 construcción y 0 unidades de construcción"),
            QUALITY_RULE_ERROR_CODE_E401105: QCoreApplication.translate("TranslatableConfigStrings", "Cuando la condición del predio es 'Mejora en PH', el predio debe tener asociado 0 terrenos y 1 construcción y 0 unidades de construcción"),
            QUALITY_RULE_ERROR_CODE_E401106: QCoreApplication.translate("TranslatableConfigStrings", "Cuando la condición del predio es 'Parque Cementerio Matriz', el predio debe tener asociado 1 terreno y 0 unidades de construcción"),
            QUALITY_RULE_ERROR_CODE_E401107: QCoreApplication.translate("TranslatableConfigStrings", "Cuando la condición del predio es 'Parque Cementerio Unidad Predial', el predio debe tener asociado 1 terreno y 0 construcciones y 0 unidades de construcción"),
            QUALITY_RULE_ERROR_CODE_E401108: QCoreApplication.translate("TranslatableConfigStrings", "Cuando la condición del predio es 'PH Matriz', el predio debe tener asociado 1 terreno y 0 unidades de construcción"),
            QUALITY_RULE_ERROR_CODE_E401109: QCoreApplication.translate("TranslatableConfigStrings", "Cuando la condición del predio es 'PH Unidad Predial', el predio debe tener asociado 0 terrenos y 0 construcciones y 1 unidad de construcción"),
            QUALITY_RULE_ERROR_CODE_E401110: QCoreApplication.translate("TranslatableConfigStrings", "Cuando la condición del predio es 'Vía', el predio debe tener asociado 1 terreno y 0 construcciones y 0 unidades de construcción"),
            QUALITY_RULE_ERROR_CODE_E401111: QCoreApplication.translate("TranslatableConfigStrings", "Cuando la condición del predio es 'NPH', el predio debe tener asociado 1 terreno y 0 unidades de construcción"),

            ERROR_LAYER_GROUP: QCoreApplication.translate("TranslatableConfigStrings", "Validation errors"),
            RIGHT_OF_WAY_LINE_LAYER: QCoreApplication.translate("TranslatableConfigStrings", "Right of way line")
        }
