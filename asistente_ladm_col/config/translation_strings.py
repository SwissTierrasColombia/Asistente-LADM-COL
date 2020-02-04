from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication)

ERROR_LAYER_GROUP = "ERROR_LAYER_GROUP"
CHECK_OVERLAPS_IN_BOUNDARY_POINTS = "CHECK_OVERLAPS_IN_BOUNDARY_POINTS"
CHECK_OVERLAPS_IN_CONTROL_POINTS = "CHECK_OVERLAPS_IN_CONTROL_POINTS"
CHECK_BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES = "CHECK_BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES"
RIGHT_OF_WAY_LINE_LAYER = "RIGHT_OF_WAY_LINE_LAYER"
CHECK_BOUNDARY_POINTS_COVERED_BY_PLOT_NODES = "CHECK_BOUNDARY_POINTS_COVERED_BY_PLOT_NODES"
CHECK_OVERLAPS_IN_BOUNDARIES = "CHECK_OVERLAPS_IN_BOUNDARIES"
CHECK_BOUNDARIES_ARE_NOT_SPLIT = "CHECK_BOUNDARIES_ARE_NOT_SPLIT"
CHECK_BOUNDARIES_COVERED_BY_PLOTS = "CHECK_BOUNDARIES_COVERED_BY_PLOTS"
CHECK_BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS = "CHECK_BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS"
CHECK_DANGLES_IN_BOUNDARIES = "CHECK_DANGLES_IN_BOUNDARIES"
CHECK_OVERLAPS_IN_PLOTS = "CHECK_OVERLAPS_IN_PLOTS"
CHECK_OVERLAPS_IN_BUILDINGS = "CHECK_OVERLAPS_IN_BUILDINGS"
CHECK_OVERLAPS_IN_RIGHTS_OF_WAY = "CHECK_OVERLAPS_IN_RIGHTS_OF_WAY"
CHECK_PLOTS_COVERED_BY_BOUNDARIES = "CHECK_PLOTS_COVERED_BY_BOUNDARIES"
CHECK_RIGHT_OF_WAY_OVERLAPS_BUILDINGS = "CHECK_RIGHT_OF_WAY_OVERLAPS_BUILDINGS"
CHECK_GAPS_IN_PLOTS = "CHECK_GAPS_IN_PLOTS"
CHECK_MULTIPART_IN_RIGHT_OF_WAY = "CHECK_MULTIPART_IN_RIGHT_OF_WAY"
CHECK_BUILDING_WITHIN_PLOTS = "CHECK_BUILDING_WITHIN_PLOTS"
CHECK_BUILDING_UNIT_WITHIN_PLOTS = "CHECK_BUILDING_UNIT_WITHIN_PLOTS"

# Logic consistency checks
CHECK_PARCEL_RIGHT_RELATIONSHIP = "CHECK_PARCEL_RIGHT_RELATIONSHIP"
CHECK_FRACTION_SUM_FOR_PARTY_GROUPS = "CHECK_FRACTION_SUM_FOR_PARTY_GROUPS"
FIND_DUPLICATE_RECORDS_IN_A_TABLE = "FIND_DUPLICATE_RECORDS_IN_A_TABLE"
CHECK_DEPARMENT_CODE_HAS_TWO_NUMERICAL_CHARACTERS = "CHECK_DEPARMENT_CODE_HAS_TWO_NUMERICAL_CHARACTERS"
CHECK_MUNICIPALITY_CODE_HAS_THREE_NUMERICAL_CHARACTERS = "CHECK_MUNICIPALITY_CODE_HAS_THREE_NUMERICAL_CHARACTERS"
CHECK_PARCEL_NUMBER_HAS_30_NUMERICAL_CHARACTERS = "CHECK_PARCEL_NUMBER_HAS_30_NUMERICAL_CHARACTERS"
CHECK_PARCEL_NUMBER_BEFORE_HAS_20_NUMERICAL_CHARACTERS = "CHECK_PARCEL_NUMBER_BEFORE_HAS_20_NUMERICAL_CHARACTERS"
CHECK_COL_PARTY_NATURAL_TYPE = "CHECK_COL_PARTY_NATURAL_TYPE"
CHECK_COL_PARTY_LEGAL_TYPE = "CHECK_COL_PARTY_LEGAL_TYPE"
CHECK_PARCEL_TYPE_AND_22_POSITON_OF_PARCEL_NUMBER = "CHECK_PARCEL_TYPE_AND_22_POSITON_OF_PARCEL_NUMBER"
CHECK_UEBAUNIT_PARCEL = "CHECK_UEBAUNIT_PARCEL"

# Logic consistency errors
ERROR_PARCEL_WITH_NO_RIGHT = "ERROR_PARCEL_WITH_NO_RIGHT"
ERROR_PARCEL_WITH_REPEATED_DOMAIN_RIGHT = "ERROR_PARCEL_WITH_REPEATED_DOMAIN_RIGHT"

# Specific topology errors
CHECK_PLOT_NODES_COVERED_BY_BOUNDARY_POINTS = "CHECK_PLOT_NODES_COVERED_BY_BOUNDARY_POINTS"
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
            ERROR_LAYER_GROUP: QCoreApplication.translate("TranslatableConfigStrings", "Validation errors"),
            CHECK_OVERLAPS_IN_BOUNDARY_POINTS: QCoreApplication.translate("TranslatableConfigStrings", "Boundary Points should not overlap"),
            CHECK_OVERLAPS_IN_CONTROL_POINTS: QCoreApplication.translate("TranslatableConfigStrings", "Control Points should not overlap"),
            CHECK_BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES: QCoreApplication.translate("TranslatableConfigStrings", "Boundary Points should be covered by Boundary nodes"),
            RIGHT_OF_WAY_LINE_LAYER: QCoreApplication.translate("TranslatableConfigStrings", "Right of way line"),
            CHECK_BOUNDARY_POINTS_COVERED_BY_PLOT_NODES: QCoreApplication.translate("TranslatableConfigStrings", "Boundary Points should be covered by plot nodes"),
            CHECK_OVERLAPS_IN_BOUNDARIES: QCoreApplication.translate("TranslatableConfigStrings", "Boundaries should not overlap"),
            CHECK_BOUNDARIES_ARE_NOT_SPLIT: QCoreApplication.translate("TranslatableConfigStrings", "Boundaries should not be split"),
            CHECK_BOUNDARIES_COVERED_BY_PLOTS: QCoreApplication.translate("TranslatableConfigStrings", "Boundaries should be covered by Plots"),
            CHECK_BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS: QCoreApplication.translate("TranslatableConfigStrings", "Boundary nodes should be covered by Boundary Points"),
            CHECK_DANGLES_IN_BOUNDARIES: QCoreApplication.translate("TranslatableConfigStrings", "Boundaries should not have dangles"),
            CHECK_OVERLAPS_IN_PLOTS: QCoreApplication.translate("TranslatableConfigStrings", "Plots should not overlap"),
            CHECK_OVERLAPS_IN_BUILDINGS: QCoreApplication.translate("TranslatableConfigStrings", "Buildings should not overlap"),
            CHECK_OVERLAPS_IN_RIGHTS_OF_WAY: QCoreApplication.translate("TranslatableConfigStrings", "Rights of Way should not overlap"),
            CHECK_PLOTS_COVERED_BY_BOUNDARIES: QCoreApplication.translate("TranslatableConfigStrings", "Plots should be covered by Boundaries"),
            CHECK_RIGHT_OF_WAY_OVERLAPS_BUILDINGS: QCoreApplication.translate("TranslatableConfigStrings", "Right of Way should not overlap Buildings"),
            CHECK_GAPS_IN_PLOTS: QCoreApplication.translate("TranslatableConfigStrings", "Plots should not have gaps"),
            CHECK_MULTIPART_IN_RIGHT_OF_WAY: QCoreApplication.translate("TranslatableConfigStrings", "Right of Way should not have multipart geometries"),
            CHECK_BUILDING_WITHIN_PLOTS: QCoreApplication.translate("TranslatableConfigStrings", "Buildings should be within Plots"),
            CHECK_BUILDING_UNIT_WITHIN_PLOTS: QCoreApplication.translate("TranslatableConfigStrings", "Building Units should be within Plots"),
            CHECK_PARCEL_RIGHT_RELATIONSHIP: QCoreApplication.translate("TranslatableConfigStrings", "Parcel should have one and only one Right"),
            CHECK_FRACTION_SUM_FOR_PARTY_GROUPS: QCoreApplication.translate("TranslatableConfigStrings", "Group Party Fractions should sum 1"),
            FIND_DUPLICATE_RECORDS_IN_A_TABLE: QCoreApplication.translate("TranslatableConfigStrings", "Table records should not be repeated"),
            CHECK_DEPARMENT_CODE_HAS_TWO_NUMERICAL_CHARACTERS: QCoreApplication.translate("TranslatableConfigStrings", "Check that the department field of the parcel table has two numerical characters"),
            CHECK_MUNICIPALITY_CODE_HAS_THREE_NUMERICAL_CHARACTERS: QCoreApplication.translate("TranslatableConfigStrings", "Check that the municipality field of the parcel table has three numerical characters"),
            CHECK_PARCEL_NUMBER_HAS_30_NUMERICAL_CHARACTERS: QCoreApplication.translate("TranslatableConfigStrings", "Check that the parcel number has 30 numerical characters"),
            CHECK_PARCEL_NUMBER_BEFORE_HAS_20_NUMERICAL_CHARACTERS: QCoreApplication.translate("TranslatableConfigStrings", "Check that the parcel number before has 20 numerical characters"),
            CHECK_COL_PARTY_NATURAL_TYPE: QCoreApplication.translate("TranslatableConfigStrings", "Check that attributes are appropriate for parties of type natural"),
            CHECK_COL_PARTY_LEGAL_TYPE: QCoreApplication.translate("TranslatableConfigStrings", "Check that attributes are appropriate for parties of type legal"),
            CHECK_PARCEL_TYPE_AND_22_POSITON_OF_PARCEL_NUMBER: QCoreApplication.translate("TranslatableConfigStrings", "Check that the type of parcel corresponds to position 22 of the parcel number"),
            CHECK_UEBAUNIT_PARCEL: QCoreApplication.translate("TranslatableConfigStrings", "Check that Spatial Units associated with Parcels correspond to the parcel type"),
            ERROR_PARCEL_WITH_NO_RIGHT: QCoreApplication.translate("TranslatableConfigStrings", "Parcel does not have any Right associated"),
            ERROR_PARCEL_WITH_REPEATED_DOMAIN_RIGHT: QCoreApplication.translate("TranslatableConfigStrings", "Parcel has more than one domain right associated"),
            CHECK_PLOT_NODES_COVERED_BY_BOUNDARY_POINTS: QCoreApplication.translate("TranslatableConfigStrings", "Plot nodes should be covered by boundary points"),
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
