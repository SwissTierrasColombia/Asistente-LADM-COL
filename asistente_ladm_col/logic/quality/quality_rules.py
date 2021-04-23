# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-03-06
        git sha              : :%H$
        copyright            : (C) 2020 by Leo Cardona (BSF Swissphoto)
        email                : leo.cardona.p@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
 """
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import Qgis

from asistente_ladm_col.config.enums import EnumQualityRule
from asistente_ladm_col.config.layer_config import LayerConfig
from asistente_ladm_col.config.quality_rules_config import QUALITY_RULE_LAYERS
from asistente_ladm_col.logic.quality.point_quality_rules import PointQualityRules
from asistente_ladm_col.logic.quality.line_quality_rules import LineQualityRules
from asistente_ladm_col.logic.quality.polygon_quality_rules import PolygonQualityRules
from asistente_ladm_col.logic.quality.logic_quality_rules import LogicQualityRules
from asistente_ladm_col.logic.quality.quality_rule_execution_result import QualityRuleExecutionResult


class QualityRules:
    """
    This facade class provides a simple interface to several quality rule classes.
    """
    def __init__(self):
        self.point_quality_rules = PointQualityRules()
        self.line_quality_rules = LineQualityRules()
        self.polygon_quality_rules = PolygonQualityRules()
        self.logic_quality_rules = LogicQualityRules()

    def validate_quality_rule(self, db, id_quality_rule, layers):
        """
        Single point of access to execute quality rules. It dispatches calls to
        the appropriate quality rule classes.

        :param db: DB Connector object
        :param id_quality_rule: id of the quality rule
        :param layers: List of layers required by the quality rule.
        :return: A list of tuples. When the rule is check for duplicate records, the list has
                 several tuples, otherwise it returns a single tuple.
                 res = [(msg, Qgis.Success|Warning|Critical)), ...]
        """
        msg, level, error_layers = "Rule {} not found!".format(id_quality_rule), Qgis.Critical, list()

        # Check that we have all required layers, otherwise, return and don't even call the quality rule
        for k,v in layers[QUALITY_RULE_LAYERS].items():
            if v is None:
                return QCoreApplication.translate("", "Invalid input layer '{}'. Chances are, you're using a tolerance so high that it makes some geometries invalid.".format(k)), Qgis.Critical

        # POINT QUALITY RULES
        if id_quality_rule == EnumQualityRule.Point.OVERLAPS_IN_BOUNDARY_POINTS:
            msg, level, error_layers = self.point_quality_rules.check_overlapping_boundary_point(db, layers)
        elif id_quality_rule == EnumQualityRule.Point.OVERLAPS_IN_CONTROL_POINTS:
            msg, level, error_layers = self.point_quality_rules.check_overlapping_control_point(db, layers)
        elif id_quality_rule == EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES:
            msg, level, error_layers = self.point_quality_rules.check_boundary_points_covered_by_boundary_nodes(db, layers)
        elif id_quality_rule == EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_PLOT_NODES:
            msg, level, error_layers = self.point_quality_rules.check_boundary_points_covered_by_plot_nodes(db, layers)

        # LINE QUALITY RULES
        elif id_quality_rule == EnumQualityRule.Line.OVERLAPS_IN_BOUNDARIES:
            msg, level, error_layers = self.line_quality_rules.check_overlaps_in_boundaries(db, layers)
        elif id_quality_rule == EnumQualityRule.Line.BOUNDARIES_ARE_NOT_SPLIT:
            msg, level, error_layers = self.line_quality_rules.check_boundaries_are_not_split(db, layers)
        elif id_quality_rule == EnumQualityRule.Line.BOUNDARIES_COVERED_BY_PLOTS:
            msg, level, error_layers = self.line_quality_rules.check_boundaries_covered_by_plots(db, layers)
        elif id_quality_rule == EnumQualityRule.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS:
            msg, level, error_layers = self.line_quality_rules.check_boundary_nodes_covered_by_boundary_points(db, layers)
        elif id_quality_rule == EnumQualityRule.Line.DANGLES_IN_BOUNDARIES:
            msg, level, error_layers = self.line_quality_rules.check_dangles_in_boundaries(db, layers)

        # POLYGON QUALITY RULES
        elif id_quality_rule == EnumQualityRule.Polygon.OVERLAPS_IN_PLOTS:
            msg, level, error_layers = self.polygon_quality_rules.check_overlapping_plots(db, layers)
        elif id_quality_rule == EnumQualityRule.Polygon.OVERLAPS_IN_BUILDINGS:
            msg, level, error_layers = self.polygon_quality_rules.check_overlapping_buildings(db, layers)
        elif id_quality_rule == EnumQualityRule.Polygon.OVERLAPS_IN_RIGHTS_OF_WAY:
            msg, level, error_layers = self.polygon_quality_rules.check_overlapping_right_of_way(db, layers)
        elif id_quality_rule == EnumQualityRule.Polygon.PLOTS_COVERED_BY_BOUNDARIES:
            msg, level, error_layers = self.polygon_quality_rules.check_plots_covered_by_boundaries(db, layers)
        elif id_quality_rule == EnumQualityRule.Polygon.RIGHT_OF_WAY_OVERLAPS_BUILDINGS:
            msg, level, error_layers = self.polygon_quality_rules.check_right_of_way_overlaps_buildings(db, layers)
        elif id_quality_rule == EnumQualityRule.Polygon.GAPS_IN_PLOTS:
            msg, level, error_layers = self.polygon_quality_rules.check_gaps_in_plots(db, layers)
        elif id_quality_rule == EnumQualityRule.Polygon.MULTIPART_IN_RIGHT_OF_WAY:
            msg, level, error_layers = self.polygon_quality_rules.check_multiparts_in_right_of_way(db, layers)
        elif id_quality_rule == EnumQualityRule.Polygon.PLOT_NODES_COVERED_BY_BOUNDARY_POINTS:
            msg, level, error_layers = self.polygon_quality_rules.check_plot_nodes_covered_by_boundary_points(db, layers)
        elif id_quality_rule == EnumQualityRule.Polygon.BUILDINGS_SHOULD_BE_WITHIN_PLOTS:
            msg, level, error_layers = self.polygon_quality_rules.check_building_within_plots(db, layers)
        elif id_quality_rule == EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_PLOTS:
            msg, level, error_layers = self.polygon_quality_rules.check_building_unit_within_plots(db, layers)
        elif id_quality_rule == EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_BUILDINGS:
            msg, level, error_layers = self.polygon_quality_rules.check_building_unit_within_buildings(db, layers)

        # LOGIC QUALITY RULES
        elif id_quality_rule == EnumQualityRule.Logic.PARCEL_RIGHT_RELATIONSHIP:
            msg, level, error_layers = self.logic_quality_rules.check_parcel_right_relationship(db)
        elif id_quality_rule == EnumQualityRule.Logic.FRACTION_SUM_FOR_PARTY_GROUPS:
            msg, level, error_layers = self.logic_quality_rules.check_group_party_fractions_that_do_not_add_one(db)
        elif id_quality_rule == EnumQualityRule.Logic.DEPARTMENT_CODE_HAS_TWO_NUMERICAL_CHARACTERS:
            msg, level, error_layers = self.logic_quality_rules.check_parcels_with_invalid_department_code(db)
        elif id_quality_rule == EnumQualityRule.Logic.MUNICIPALITY_CODE_HAS_THREE_NUMERICAL_CHARACTERS:
            msg, level, error_layers = self.logic_quality_rules.check_parcels_with_invalid_municipality_code(db)
        elif id_quality_rule == EnumQualityRule.Logic.PARCEL_NUMBER_HAS_30_NUMERICAL_CHARACTERS:
            msg, level, error_layers = self.logic_quality_rules.check_parcels_with_invalid_parcel_number(db)
        elif id_quality_rule == EnumQualityRule.Logic.PARCEL_NUMBER_BEFORE_HAS_20_NUMERICAL_CHARACTERS:
            msg, level, error_layers = self.logic_quality_rules.check_parcels_with_invalid_previous_parcel_number(db)
        elif id_quality_rule == EnumQualityRule.Logic.COL_PARTY_NATURAL_TYPE:
            msg, level, error_layers = self.logic_quality_rules.check_invalid_col_party_type_natural(db)
        elif id_quality_rule == EnumQualityRule.Logic.COL_PARTY_NOT_NATURAL_TYPE:
            msg, level, error_layers = self.logic_quality_rules.check_invalid_col_party_type_no_natural(db)
        elif id_quality_rule == EnumQualityRule.Logic.PARCEL_TYPE_AND_22_POSITION_OF_PARCEL_NUMBER:
            msg, level, error_layers = self.logic_quality_rules.check_parcels_with_invalid_parcel_type_and_22_position_number(db)
        elif id_quality_rule == EnumQualityRule.Logic.UEBAUNIT_PARCEL:
            msg, level, error_layers = self.logic_quality_rules.check_uebaunit_parcel(db)
        elif id_quality_rule == EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_BOUNDARY_POINT:
            msg, level, error_layers = self.__check_duplicate_records_in_table(db, db.names.LC_BOUNDARY_POINT_T, id_quality_rule)
        elif id_quality_rule == EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_SURVEY_POINT:
            msg, level, error_layers = self.__check_duplicate_records_in_table(db, db.names.LC_SURVEY_POINT_T, id_quality_rule)
        elif id_quality_rule == EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_CONTROL_POINT:
            msg, level, error_layers = self.__check_duplicate_records_in_table(db, db.names.LC_CONTROL_POINT_T, id_quality_rule)
        elif id_quality_rule == EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_BOUNDARY:
            msg, level, error_layers = self.__check_duplicate_records_in_table(db, db.names.LC_BOUNDARY_T, id_quality_rule)
        elif id_quality_rule == EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_PLOT:
            msg, level, error_layers = self.__check_duplicate_records_in_table(db, db.names.LC_PLOT_T, id_quality_rule)
        elif id_quality_rule == EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_BUILDING:
            msg, level, error_layers = self.__check_duplicate_records_in_table(db, db.names.LC_BUILDING_T, id_quality_rule)
        elif id_quality_rule == EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_BUILDING_UNIT:
            msg, level, error_layers = self.__check_duplicate_records_in_table(db, db.names.LC_BUILDING_UNIT_T, id_quality_rule)
        elif id_quality_rule == EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_PARCEL:
            msg, level, error_layers = self.__check_duplicate_records_in_table(db, db.names.LC_PARCEL_T, id_quality_rule)
        elif id_quality_rule == EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_PARTY:
            msg, level, error_layers = self.__check_duplicate_records_in_table(db, db.names.LC_PARTY_T, id_quality_rule)
        elif id_quality_rule == EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_RIGHT:
            msg, level, error_layers = self.__check_duplicate_records_in_table(db, db.names.LC_RIGHT_T, id_quality_rule)
        elif id_quality_rule == EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_RESTRICTION:
            msg, level, error_layers = self.__check_duplicate_records_in_table(db, db.names.LC_RESTRICTION_T, id_quality_rule)
        elif id_quality_rule == EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_ADMINISTRATIVE_SOURCE:
            msg, level, error_layers = self.__check_duplicate_records_in_table(db, db.names.LC_ADMINISTRATIVE_SOURCE_T, id_quality_rule)

        # TODO: All check functions should return a QualityRuleExecutionResult object
        return QualityRuleExecutionResult(msg, level, error_layers)

    def __check_duplicate_records_in_table(self, db, table, rule_code):
        fields = LayerConfig.get_logic_consistency_tables(db.names).get(table)
        return self.logic_quality_rules.check_duplicate_records_in_a_table(db, table, fields, rule_code)