from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication)
from asistente_ladm_col.config.enums import QualityRuleEnum

ERROR_LAYER_GROUP = "ERROR_LAYER_GROUP"
RIGHT_OF_WAY_LINE_LAYER = "RIGHT_OF_WAY_LINE_LAYER"

# Logic consistency errors
ERROR_PARCEL_WITH_NO_RIGHT = "ERROR_PARCEL_WITH_NO_RIGHT"
ERROR_PARCEL_WITH_REPEATED_DOMAIN_RIGHT = "ERROR_PARCEL_WITH_REPEATED_DOMAIN_RIGHT"

# Specific topology errors
ERROR_PLOT_IS_NOT_COVERED_BY_BOUNDARY = "ERROR_PLOT_IS_NOT_COVERED_BY_BOUNDARY"
ERROR_BOUNDARY_IS_NOT_COVERED_BY_PLOT = "ERROR_BOUNDARY_IS_NOT_COVERED_BY_PLOT"
ERROR_NO_MORE_BOUNDARY_FACE_STRING_TABLE = "ERROR_NO_MORE_BOUNDARY_FACE_STRING_TABLE"
ERROR_DUPLICATE_MORE_BOUNDARY_FACE_STRING_TABLE = "ERROR_DUPLICATE_MORE_BOUNDARY_FACE_STRING_TABLE"
ERROR_NO_LESS_TABLE = "ERROR_NO_LESS_TABLE"
ERROR_DUPLICATE_LESS_TABLE = "ERROR_DUPLICATE_LESS_TABLE"
ERROR_NO_FOUND_POINT_BFS = "ERROR_NO_FOUND_POINT_BFS"
ERROR_DUPLICATE_POINT_BFS = "ERROR_DUPLICATE_POINT_BFS"
ERROR_BOUNDARY_POINT_IS_NOT_COVERED_BY_BOUNDARY_NODE = "ERROR_BOUNDARY_POINT_IS_NOT_COVERED_BY_BOUNDARY_NODE"
ERROR_BOUNDARY_NODE_IS_NOT_COVERED_BY_BOUNDARY_POINT = "ERROR_BOUNDARY_NODE_IS_NOT_COVERED_BY_BOUNDARY_POINT"
ERROR_BUILDING_IS_NOT_OVER_A_PLOT = "ERROR_BUILDING_IS_NOT_OVER_A_PLOT"
ERROR_BUILDING_CROSSES_A_PLOT_LIMIT = "ERROR_BUILDING_CROSSES_A_PLOT_LIMIT"
ERROR_BUILDING_UNIT_IS_NOT_OVER_A_PLOT = "ERROR_BUILDING_UNIT_IS_NOT_OVER_A_PLOT"
ERROR_BUILDING_UNIT_CROSSES_A_PLOT_LIMIT = "ERROR_BUILDING_UNIT_CROSSES_A_PLOT_LIMIT"


TOOLBAR_BUILD_BOUNDARY = QCoreApplication.translate("TranslatableConfigStrings", "Build boundaries...")
TOOLBAR_MOVE_NODES = QCoreApplication.translate("TranslatableConfigStrings", "Move nodes...")
TOOLBAR_FILL_POINT_BFS = QCoreApplication.translate("TranslatableConfigStrings", "Fill Point BFS")
TOOLBAR_FILL_MORE_BFS_LESS = QCoreApplication.translate("TranslatableConfigStrings", "Fill More BFS and Less")
TOOLBAR_FILL_RIGHT_OF_WAY_RELATIONS = QCoreApplication.translate("TranslatableConfigStrings", "Fill Right of Way Relations")
TOOLBAR_IMPORT_FROM_INTERMEDIATE_STRUCTURE = QCoreApplication.translate("TranslatableConfigStrings", "Import from intermediate structure")
TOOLBAR_FINALIZE_GEOMETRY_CREATION = QCoreApplication.translate("TranslatableConfigStrings", "Finalize geometry creation")


class TranslatableConfigStrings(QObject):
    def __init__(self):
        pass

    def get_translatable_config_strings(self):
        return {
            QualityRuleEnum.Point.OVERLAPS_IN_BOUNDARY_POINTS: QCoreApplication.translate("TranslatableConfigStrings", "Boundary Points should not overlap"),
            QualityRuleEnum.Point.OVERLAPS_IN_CONTROL_POINTS: QCoreApplication.translate("TranslatableConfigStrings", "Control Points should not overlap"),
            QualityRuleEnum.Point.BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES: QCoreApplication.translate("TranslatableConfigStrings", "Boundary Points should be covered by Boundary nodes"),
            QualityRuleEnum.Point.BOUNDARY_POINTS_COVERED_BY_PLOT_NODES: QCoreApplication.translate("TranslatableConfigStrings", "Boundary Points should be covered by plot nodes"),
            QualityRuleEnum.Line.OVERLAPS_IN_BOUNDARIES: QCoreApplication.translate("TranslatableConfigStrings", "Boundaries should not overlap"),
            QualityRuleEnum.Line.BOUNDARIES_ARE_NOT_SPLIT: QCoreApplication.translate("TranslatableConfigStrings", "Boundaries should not be split"),
            QualityRuleEnum.Line.BOUNDARIES_COVERED_BY_PLOTS: QCoreApplication.translate("TranslatableConfigStrings", "Boundaries should be covered by Plots"),
            QualityRuleEnum.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS: QCoreApplication.translate("TranslatableConfigStrings", "Boundary nodes should be covered by Boundary Points"),
            QualityRuleEnum.Line.DANGLES_IN_BOUNDARIES: QCoreApplication.translate("TranslatableConfigStrings", "Boundaries should not have dangles"),
            QualityRuleEnum.Polygon.OVERLAPS_IN_PLOTS: QCoreApplication.translate("TranslatableConfigStrings", "Plots should not overlap"),
            QualityRuleEnum.Polygon.OVERLAPS_IN_BUILDINGS: QCoreApplication.translate("TranslatableConfigStrings", "Buildings should not overlap"),
            QualityRuleEnum.Polygon.OVERLAPS_IN_RIGHTS_OF_WAY: QCoreApplication.translate("TranslatableConfigStrings", "Rights of Way should not overlap"),
            QualityRuleEnum.Polygon.PLOTS_COVERED_BY_BOUNDARIES: QCoreApplication.translate("TranslatableConfigStrings", "Plots should be covered by Boundaries"),
            QualityRuleEnum.Polygon.PLOT_NODES_COVERED_BY_BOUNDARY_POINTS: QCoreApplication.translate("TranslatableConfigStrings", "Plot nodes should be covered by boundary points"),
            QualityRuleEnum.Polygon.RIGHT_OF_WAY_OVERLAPS_BUILDINGS: QCoreApplication.translate("TranslatableConfigStrings", "Right of Way should not overlap Buildings"),
            QualityRuleEnum.Polygon.GAPS_IN_PLOTS: QCoreApplication.translate("TranslatableConfigStrings", "Plots should not have gaps"),
            QualityRuleEnum.Polygon.MULTIPART_IN_RIGHT_OF_WAY: QCoreApplication.translate("TranslatableConfigStrings", "Right of Way should not have multipart geometries"),
            QualityRuleEnum.Polygon.BUILDINGS_SHOULD_BE_WITHIN_PLOTS: QCoreApplication.translate("TranslatableConfigStrings", "Buildings should be within Plots"),
            QualityRuleEnum.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_PLOTS: QCoreApplication.translate("TranslatableConfigStrings", "Building Units should be within Plots"),
            QualityRuleEnum.Logic.PARCEL_RIGHT_RELATIONSHIP: QCoreApplication.translate("TranslatableConfigStrings", "Parcel should have one and only one Right"),
            QualityRuleEnum.Logic.FRACTION_SUM_FOR_PARTY_GROUPS: QCoreApplication.translate("TranslatableConfigStrings", "Group Party Fractions should sum 1"),
            QualityRuleEnum.Logic.DUPLICATE_RECORDS_IN_A_TABLE: QCoreApplication.translate("TranslatableConfigStrings", "Table records should not be repeated"),
            QualityRuleEnum.Logic.DEPARTMENT_CODE_HAS_TWO_NUMERICAL_CHARACTERS: QCoreApplication.translate("TranslatableConfigStrings", "Check that the department field of the parcel table has two numerical characters"),
            QualityRuleEnum.Logic.MUNICIPALITY_CODE_HAS_THREE_NUMERICAL_CHARACTERS: QCoreApplication.translate("TranslatableConfigStrings", "Check that the municipality field of the parcel table has three numerical characters"),
            QualityRuleEnum.Logic.PARCEL_NUMBER_HAS_30_NUMERICAL_CHARACTERS: QCoreApplication.translate("TranslatableConfigStrings", "Check that the parcel number has 30 numerical characters"),
            QualityRuleEnum.Logic.PARCEL_NUMBER_BEFORE_HAS_20_NUMERICAL_CHARACTERS: QCoreApplication.translate("TranslatableConfigStrings", "Check that the parcel number before has 20 numerical characters"),
            QualityRuleEnum.Logic.COL_PARTY_NATURAL_TYPE: QCoreApplication.translate("TranslatableConfigStrings", "Check that attributes are appropriate for parties of type natural"),
            QualityRuleEnum.Logic.COL_PARTY_NOT_NATURAL_TYPE: QCoreApplication.translate("TranslatableConfigStrings", "Check that attributes are appropriate for parties of type legal"),
            QualityRuleEnum.Logic.PARCEL_TYPE_AND_22_POSITION_OF_PARCEL_NUMBER: QCoreApplication.translate("TranslatableConfigStrings", "Check that the type of parcel corresponds to position 22 of the parcel number"),
            QualityRuleEnum.Logic.UEBAUNIT_PARCEL: QCoreApplication.translate("TranslatableConfigStrings", "Check that Spatial Units associated with Parcels correspond to the parcel type"),
            ERROR_LAYER_GROUP: QCoreApplication.translate("TranslatableConfigStrings", "Validation errors"),
            ERROR_PARCEL_WITH_NO_RIGHT: QCoreApplication.translate("TranslatableConfigStrings", "Parcel does not have any Right associated"),
            RIGHT_OF_WAY_LINE_LAYER: QCoreApplication.translate("TranslatableConfigStrings", "Right of way line"),
            ERROR_PARCEL_WITH_REPEATED_DOMAIN_RIGHT: QCoreApplication.translate("TranslatableConfigStrings", "Parcel has more than one domain right associated"),
            ERROR_PLOT_IS_NOT_COVERED_BY_BOUNDARY: QCoreApplication.translate("TranslatableConfigStrings", "Plot is not covered by boundary"),
            ERROR_BOUNDARY_IS_NOT_COVERED_BY_PLOT: QCoreApplication.translate("TranslatableConfigStrings", "Boundary is not covered by plot"),
            ERROR_NO_MORE_BOUNDARY_FACE_STRING_TABLE: QCoreApplication.translate("TranslatableConfigStrings", "Topological relationship between boundary and plot is not recorded in the masccl table"),
            ERROR_DUPLICATE_MORE_BOUNDARY_FACE_STRING_TABLE: QCoreApplication.translate("TranslatableConfigStrings", "Topological relationship between boundary and plot is duplicated in the masccl table"),
            ERROR_NO_LESS_TABLE: QCoreApplication.translate("TranslatableConfigStrings", "Topological relationship between boundary and plot is not recorded in the menosccl table"),
            ERROR_DUPLICATE_LESS_TABLE: QCoreApplication.translate("TranslatableConfigStrings", "Topological relationship between boundary and plot is duplicated in the menosccl table"),
            ERROR_NO_FOUND_POINT_BFS: QCoreApplication.translate("TranslatableConfigStrings", "Topological relationship between boundary point and boundary is not recorded in the puntoccl table"),
            ERROR_DUPLICATE_POINT_BFS: QCoreApplication.translate("TranslatableConfigStrings", "Topological relationship between boundary point and boundary is duplicated in the puntoccl table"),
            ERROR_BOUNDARY_POINT_IS_NOT_COVERED_BY_BOUNDARY_NODE: QCoreApplication.translate("TranslatableConfigStrings", "Boundary point is not covered by boundary node"),
            ERROR_BOUNDARY_NODE_IS_NOT_COVERED_BY_BOUNDARY_POINT: QCoreApplication.translate("TranslatableConfigStrings", "Boundary node is not covered by boundary point"),
            ERROR_BUILDING_IS_NOT_OVER_A_PLOT: QCoreApplication.translate("TranslatableConfigStrings", "Building is not over a plot"),
            ERROR_BUILDING_CROSSES_A_PLOT_LIMIT: QCoreApplication.translate("TranslatableConfigStrings", "Building crosses a plot's limit"),
            ERROR_BUILDING_UNIT_IS_NOT_OVER_A_PLOT: QCoreApplication.translate("TranslatableConfigStrings", "Building Unit is not over a plot"),
            ERROR_BUILDING_UNIT_CROSSES_A_PLOT_LIMIT: QCoreApplication.translate("TranslatableConfigStrings", "Building Unit crosses a plot's limit")
        }
