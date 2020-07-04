from qgis.core import QgsWkbTypes

from asistente_ladm_col.config.enums import EnumQualityRule
from asistente_ladm_col.config.quality_rules_config import (QUALITY_RULE_TABLE_NAME,
                                                            QUALITY_RULES,
                                                            QualityRuleConfig)


class Symbology:

    @staticmethod
    def get_default_style_group(names):
         return {
             names.LC_BOUNDARY_T: 'style_boundary',
             names.LC_BOUNDARY_POINT_T: 'style_boundary_point',
             names.LC_SURVEY_POINT_T: 'style_survey_point',
             names.LC_CONTROL_POINT_T: 'style_control_point',
             names.LC_PLOT_T: 'style_plot_polygon',
             names.LC_BUILDING_T: 'style_building',
             names.LC_BUILDING_UNIT_T: 'style_building_unit_25',
             names.LC_RIGHT_OF_WAY_T: 'style_right_of_way'
        }

    @staticmethod
    def get_style_group_layer_modifiers(names):
        return {
            names.GC_PLOT_T: 'style_supplies_plot_polygon'
        }

    @staticmethod
    def get_default_error_style_layer():
        return {
            QgsWkbTypes.PointGeometry: 'style_point_error',
            QgsWkbTypes.LineGeometry: 'style_line_error',
            QgsWkbTypes.PolygonGeometry: 'style_polygon_error'
        }

    @staticmethod
    def get_custom_error_layers():
        quality_rules_data = QualityRuleConfig.get_quality_rules_config()
        return {
            quality_rules_data[EnumQualityRule.Line][QUALITY_RULES][EnumQualityRule.Line.BOUNDARIES_COVERED_BY_PLOTS][QUALITY_RULE_TABLE_NAME]: 'style_boundary_should_be_covered_by_plot',
            quality_rules_data[EnumQualityRule.Polygon][QUALITY_RULES][EnumQualityRule.Polygon.PLOTS_COVERED_BY_BOUNDARIES][QUALITY_RULE_TABLE_NAME]: 'style_plot_should_be_covered_by_boundary',
            quality_rules_data[EnumQualityRule.Point][QUALITY_RULES][EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES][QUALITY_RULE_TABLE_NAME]: 'style_boundary_points_should_be_covered_by_boundary_nodes',
            quality_rules_data[EnumQualityRule.Line][QUALITY_RULES][EnumQualityRule.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS][QUALITY_RULE_TABLE_NAME]: 'style_boundary_nodes_should_be_covered_by_boundary_points'
        }
