from qgis.core import QgsWkbTypes

from .general_config import translated_strings
from .table_mapping_config import (BOUNDARY_TABLE,
                                   BOUNDARY_POINT_TABLE,
                                   CONTROL_POINT_TABLE,
                                   SURVEY_POINT_TABLE,
                                   PLOT_TABLE,
                                   OFFICIAL_PLOT_TABLE,
                                   BUILDING_TABLE,
                                   BUILDING_UNIT_TABLE,
                                   RIGHT_OF_WAY_TABLE)

ERROR_LAYER = 'error_layer'

DEFAULT_GROUP_STYLE = {
    BOUNDARY_TABLE: {
        QgsWkbTypes.LineGeometry: 'style_boundary'
    },
    BOUNDARY_POINT_TABLE: {
        QgsWkbTypes.PointGeometry: 'style_boundary_point'
    },
    SURVEY_POINT_TABLE: {
        QgsWkbTypes.PointGeometry: 'style_survey_point'
    },
    CONTROL_POINT_TABLE: {
        QgsWkbTypes.PointGeometry: 'style_control_point'
    },
    PLOT_TABLE: {
        QgsWkbTypes.PointGeometry: 'style_plot_point',
        QgsWkbTypes.PolygonGeometry: 'style_plot_polygon'
    },
    BUILDING_TABLE: {
        QgsWkbTypes.PointGeometry: 'style_building_point',
        QgsWkbTypes.PolygonGeometry: 'style_building'
    },
    BUILDING_UNIT_TABLE: {
        QgsWkbTypes.PointGeometry: 'style_building_unit_point',
        QgsWkbTypes.PolygonGeometry: 'style_building_unit_25'
    },
    RIGHT_OF_WAY_TABLE: {
        QgsWkbTypes.PointGeometry: 'style_right_of_way_point',
        QgsWkbTypes.PolygonGeometry: 'style_right_of_way'
    },
    ERROR_LAYER: {
        QgsWkbTypes.PointGeometry: 'style_point_error',
        QgsWkbTypes.LineGeometry: 'style_line_error',
        QgsWkbTypes.PolygonGeometry: 'style_polygon_error'
    }
}

OFFICIAL_GROUP_STYLE = {
    PLOT_TABLE: {
        QgsWkbTypes.PolygonGeometry: 'style_official_plot_polygon'
    }
}

CUSTOM_ERROR_LAYERS = {
    translated_strings.CHECK_BOUNDARIES_COVERED_BY_PLOTS: {
        'es': 'style_boundary_should_be_covered_by_plot_es',
        'en': 'style_boundary_should_be_covered_by_plot_en'
    },
    translated_strings.CHECK_PLOTS_COVERED_BY_BOUNDARIES: {
        'es': 'style_plot_should_be_covered_by_boundary_es',
        'en': 'style_plot_should_be_covered_by_boundary_en'
    },
    translated_strings.CHECK_BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES: {
        'es': 'style_boundary_points_should_be_covered_by_boundary_nodes_es',
        'en': 'style_boundary_points_should_be_covered_by_boundary_nodes_en'
    },
    translated_strings.CHECK_BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS: {
        'es': 'style_boundary_nodes_should_be_covered_by_boundary_points_es',
        'en': 'style_boundary_nodes_should_be_covered_by_boundary_points_en'
     }
}
