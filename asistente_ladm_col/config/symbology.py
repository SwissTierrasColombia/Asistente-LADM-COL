from qgis.core import QgsWkbTypes

from asistente_ladm_col.config.enums import QualityRuleEnum
from asistente_ladm_col.config.translation_strings import TranslatableConfigStrings


class Symbology:
    ERROR_LAYER = 'error_layer'

    def __init__(self):
        self.translatable_config_strings = TranslatableConfigStrings()

    def get_default_style_group(self, names):
         return {
            names.OP_BOUNDARY_T: {
                QgsWkbTypes.LineGeometry: 'style_boundary'
            },
            names.OP_BOUNDARY_POINT_T: {
                QgsWkbTypes.PointGeometry: 'style_boundary_point'
            },
            names.OP_SURVEY_POINT_T: {
                QgsWkbTypes.PointGeometry: 'style_survey_point'
            },
            names.OP_CONTROL_POINT_T: {
                QgsWkbTypes.PointGeometry: 'style_control_point'
            },
            names.OP_PLOT_T: {
                QgsWkbTypes.PointGeometry: 'style_plot_point',
                QgsWkbTypes.PolygonGeometry: 'style_plot_polygon'
            },
            names.OP_BUILDING_T: {
                QgsWkbTypes.PointGeometry: 'style_building_point',
                QgsWkbTypes.PolygonGeometry: 'style_building'
            },
            names.OP_BUILDING_UNIT_T: {
                QgsWkbTypes.PointGeometry: 'style_building_unit_point',
                QgsWkbTypes.PolygonGeometry: 'style_building_unit_25'
            },
            names.OP_RIGHT_OF_WAY_T: {
                QgsWkbTypes.PointGeometry: 'style_right_of_way_point',
                QgsWkbTypes.PolygonGeometry: 'style_right_of_way'
            },
            self.ERROR_LAYER: {
                QgsWkbTypes.PointGeometry: 'style_point_error',
                QgsWkbTypes.LineGeometry: 'style_line_error',
                QgsWkbTypes.PolygonGeometry: 'style_polygon_error'
            }
        }

    def get_supplies_style_group(self, names):
        return {
            names.GC_PLOT_T: {
                QgsWkbTypes.PolygonGeometry: 'style_supplies_plot_polygon'
            }
        }

    def get_custom_error_layers(self):
        translated_strings = self.translatable_config_strings.get_translatable_config_strings()

        return {
            translated_strings[QualityRuleEnum.Line.BOUNDARIES_COVERED_BY_PLOTS]: {
                'es': 'style_boundary_should_be_covered_by_plot_es',
                'en': 'style_boundary_should_be_covered_by_plot_en'
            },
            translated_strings[QualityRuleEnum.Polygon.PLOTS_COVERED_BY_BOUNDARIES]: {
                'es': 'style_plot_should_be_covered_by_boundary_es',
                'en': 'style_plot_should_be_covered_by_boundary_en'
            },
            translated_strings[QualityRuleEnum.Point.BOUNDARY_POINTS_COVERED_BY_PLOT_NODES]: {
                'es': 'style_boundary_points_should_be_covered_by_boundary_nodes_es',
                'en': 'style_boundary_points_should_be_covered_by_boundary_nodes_en'
            },
            translated_strings[QualityRuleEnum.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS]: {
                'es': 'style_boundary_nodes_should_be_covered_by_boundary_points_es',
                'en': 'style_boundary_nodes_should_be_covered_by_boundary_points_en'
             }
        }

    def get_error_layer_name(self):
        return self.ERROR_LAYER
