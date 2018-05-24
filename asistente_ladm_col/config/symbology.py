from qgis.core import QgsWkbTypes

from .table_mapping_config import (
    BOUNDARY_TABLE,
    BOUNDARY_POINT_TABLE,
    SURVEY_POINT_TABLE,
    PLOT_TABLE,
    BUILDING_TABLE,
    BUILDING_UNIT_TABLE
)

ERROR_LAYER = 'error_layer'

LAYER_QML_STYLE = {
    BOUNDARY_TABLE: {
        QgsWkbTypes.LineGeometry: 'style_boundary'
    },
    BOUNDARY_POINT_TABLE: {
        QgsWkbTypes.PointGeometry: 'style_boundary_point'
    },
    SURVEY_POINT_TABLE: {
        QgsWkbTypes.PointGeometry: 'style_survey_point'
    },
    PLOT_TABLE: {
        QgsWkbTypes.PointGeometry: 'style_plot_point',
        QgsWkbTypes.PolygonGeometry: 'style_plot_polygon'
    },
    BUILDING_TABLE: {
        QgsWkbTypes.PointGeometry: 'style_building_point',
        QgsWkbTypes.PolygonGeometry: 'style_building_25'
    },
    BUILDING_UNIT_TABLE: {
        QgsWkbTypes.PointGeometry: 'style_building_unit_point',
        QgsWkbTypes.PolygonGeometry: 'style_building_unit_25'
    },
    ERROR_LAYER: {
        QgsWkbTypes.PointGeometry: 'style_point_error',
        QgsWkbTypes.LineGeometry: 'style_line_error',
        QgsWkbTypes.PolygonGeometry: 'style_polygon_error'
    }
}
