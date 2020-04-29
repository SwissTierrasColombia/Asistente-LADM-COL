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
from asistente_ladm_col.config.enums import EnumQualityRule
from asistente_ladm_col.config.layer_config import LayerConfig
from asistente_ladm_col.logic.quality.point_quality_rules import PointQualityRules
from asistente_ladm_col.logic.quality.line_quality_rules import LineQualityRules
from asistente_ladm_col.logic.quality.polygon_quality_rules import PolygonQualityRules
from asistente_ladm_col.logic.quality.logic_quality_rules import LogicQualityRules


class QualityRules:
    """
    This facade class provides a simple interface to several quality rules.
    The facade delegates client requests to appropriate quality rule classes.
    """
    def __init__(self, qgis_utils):
        self.qgis_utils = qgis_utils
        self.point_quality_rules = PointQualityRules(self.qgis_utils)
        self.line_quality_rules = LineQualityRules(self.qgis_utils)
        self.polygon_quality_rules = PolygonQualityRules(self.qgis_utils)
        self.logic_quality_rules = LogicQualityRules(self.qgis_utils)

    # POINT QUALITY RULES
    def validate_overlaps_in_boundary_points(self, db):
        return self.point_quality_rules.check_overlapping_boundary_point(db)

    def validate_overlaps_in_control_points(self, db):
        return self.point_quality_rules.check_overlapping_control_point(db)

    def validate_boundary_points_covered_by_boundary_nodes(self, db):
        return self.point_quality_rules.check_boundary_points_covered_by_boundary_nodes(db)

    def validate_boundary_points_covered_by_plot_nodes(self, db):
        return self.point_quality_rules.check_boundary_points_covered_by_plot_nodes(db)

    # LINE QUALITY RULES
    def validate_overlaps_in_boundaries(self, db):
        return self.line_quality_rules.check_overlaps_in_boundaries(db)

    def validate_boundaries_are_not_split(self, db):
        return self.line_quality_rules.check_boundaries_are_not_split(db)

    def validate_boundaries_covered_by_plots(self, db):
        return self.line_quality_rules.check_boundaries_covered_by_plots(db)

    def validate_boundary_nodes_covered_by_boundary_points(self, db):
        return self.line_quality_rules.check_boundary_nodes_covered_by_boundary_points(db)

    def validate_dangles_in_boundaries(self, db):
        return self.line_quality_rules.check_dangles_in_boundaries(db)

    # POLYGON QUALITY RULES
    def validate_overlaps_in_plots(self, db):
        return self.polygon_quality_rules.check_overlapping_plots(db)

    def validate_overlaps_in_buildings(self, db):
        return self.polygon_quality_rules.check_overlapping_buildings(db)

    def validate_overlaps_in_rights_of_way(self, db):
        return self.polygon_quality_rules.check_overlapping_right_of_way(db)

    def validate_plots_covered_by_boundaries(self, db):
        return self.polygon_quality_rules.check_plots_covered_by_boundaries(db)

    def validate_right_of_way_overlaps_buildings(self, db):
        return self.polygon_quality_rules.check_right_of_way_overlaps_buildings(db)

    def validate_gaps_in_plots(self, db):
        return self.polygon_quality_rules.check_gaps_in_plots(db)

    def validate_multipart_in_right_of_way(self, db):
        return self.polygon_quality_rules.check_multiparts_in_right_of_way(db)

    def validate_plot_nodes_covered_by_boundary_points(self, db):
        return self.polygon_quality_rules.check_plot_nodes_covered_by_boundary_points(db)

    def validate_buildings_should_be_within_plots(self, db):
        return self.polygon_quality_rules.check_building_within_plots(db)

    def validate_building_units_should_be_within_plots(self, db):
        return self.polygon_quality_rules.check_building_unit_within_plots(db)

    # LOGIC QUALITY RULES
    def validate_parcel_right_relationship(self, db, query_manager):
        return self.logic_quality_rules.check_parcel_right_relationship(db, query_manager)

    def validate_duplicate_records_in_a_table(self, db, query_manager, table, fields):
        return self.logic_quality_rules.check_duplicate_records_in_a_table(db, query_manager, table, fields)

    def validate_fraction_sum_for_party_groups(self, db, query_manager):
        return self.logic_quality_rules.check_group_party_fractions_that_do_not_add_one(db, query_manager)

    def validate_department_code_has_two_numerical_characters(self, db, query_manager):
        return self.logic_quality_rules.check_parcels_with_invalid_department_code(db, query_manager)

    def validate_municipality_code_has_three_numerical_characters(self, db, query_manager):
        return self.logic_quality_rules.check_parcels_with_invalid_municipality_code(db, query_manager)

    def validate_parcel_number_has_30_numerical_characters(self, db, query_manager):
        return self.logic_quality_rules.check_parcels_with_invalid_parcel_number(db, query_manager)

    def validate_parcel_number_before_has_20_numerical_characters(self, db, query_manager):
        return self.logic_quality_rules.check_parcels_with_invalid_previous_parcel_number(db, query_manager)

    def validate_col_party_natural_type(self, db, query_manager):
        return self.logic_quality_rules.check_invalid_col_party_type_natural(db, query_manager)

    def validate_col_party_no_natural_type(self, db, query_manager):
        return self.logic_quality_rules.check_invalid_col_party_type_no_natural(db, query_manager)

    def validate_parcel_type_and_22_position_of_parcel_number(self, db, query_manager):
        return self.logic_quality_rules.check_parcels_with_invalid_parcel_type_and_22_position_number(db, query_manager)

    def validate_uebaunit_parcel(self, db, query_manager):
        return self.logic_quality_rules.check_uebaunit_parcel(db, query_manager)

    def validate_quality_rule(self, db, ladm_queries, id_quality_rule):
        """
        Single point of access to execute quality rules. It dispatches calls to
        the appropriate quality rule classes.

        :param db: DB Connector object
        :param id_quality_rule: id of the quality rule
        :return: A list of tuples. When the rule is check for duplicate records, the list has
                 several tuples, otherwise it returns a single tuple.
                 res = [(msg, Qgis.Success|Warning|Critical)), ...]
        """
        res = list()

        # POINT QUALITY RULES
        if id_quality_rule == EnumQualityRule.Point.OVERLAPS_IN_BOUNDARY_POINTS:
            res.append(self.validate_overlaps_in_boundary_points(db))
        elif id_quality_rule == EnumQualityRule.Point.OVERLAPS_IN_CONTROL_POINTS:
            res.append(self.validate_overlaps_in_control_points(db))
        elif id_quality_rule == EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES:
            res.append(self.validate_boundary_points_covered_by_boundary_nodes(db))
        elif id_quality_rule == EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_PLOT_NODES:
            res.append(self.validate_boundary_points_covered_by_plot_nodes(db))

        # LINE QUALITY RULES
        elif id_quality_rule == EnumQualityRule.Line.OVERLAPS_IN_BOUNDARIES:
            res.append(self.validate_overlaps_in_boundaries(db))
        elif id_quality_rule == EnumQualityRule.Line.BOUNDARIES_ARE_NOT_SPLIT:
            res.append(self.validate_boundaries_are_not_split(db))
        elif id_quality_rule == EnumQualityRule.Line.BOUNDARIES_COVERED_BY_PLOTS:
            res.append(self.validate_boundaries_covered_by_plots(db))
        elif id_quality_rule == EnumQualityRule.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS:
            res.append(self.validate_boundary_nodes_covered_by_boundary_points(db))
        elif id_quality_rule == EnumQualityRule.Line.DANGLES_IN_BOUNDARIES:
            res.append(self.validate_dangles_in_boundaries(db))

        # POLYGON QUALITY RULES
        elif id_quality_rule == EnumQualityRule.Polygon.OVERLAPS_IN_PLOTS:
            res.append(self.validate_overlaps_in_plots(db))
        elif id_quality_rule == EnumQualityRule.Polygon.OVERLAPS_IN_BUILDINGS:
            res.append(self.validate_overlaps_in_buildings(db))
        elif id_quality_rule == EnumQualityRule.Polygon.OVERLAPS_IN_RIGHTS_OF_WAY:
            res.append(self.validate_overlaps_in_rights_of_way(db))
        elif id_quality_rule == EnumQualityRule.Polygon.PLOTS_COVERED_BY_BOUNDARIES:
            res.append(self.validate_plots_covered_by_boundaries(db))
        elif id_quality_rule == EnumQualityRule.Polygon.RIGHT_OF_WAY_OVERLAPS_BUILDINGS:
            res.append(self.validate_right_of_way_overlaps_buildings(db))
        elif id_quality_rule == EnumQualityRule.Polygon.GAPS_IN_PLOTS:
            res.append(self.validate_gaps_in_plots(db))
        elif id_quality_rule == EnumQualityRule.Polygon.MULTIPART_IN_RIGHT_OF_WAY:
            res.append(self.validate_multipart_in_right_of_way(db))
        elif id_quality_rule == EnumQualityRule.Polygon.PLOT_NODES_COVERED_BY_BOUNDARY_POINTS:
            res.append(self.validate_plot_nodes_covered_by_boundary_points(db))
        elif id_quality_rule == EnumQualityRule.Polygon.BUILDINGS_SHOULD_BE_WITHIN_PLOTS:
            res.append(self.validate_buildings_should_be_within_plots(db))
        elif id_quality_rule == EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_PLOTS:
            res.append(self.validate_building_units_should_be_within_plots(db))

        # LOGIC QUALITY RULES
        elif id_quality_rule == EnumQualityRule.Logic.PARCEL_RIGHT_RELATIONSHIP:
            res.append(self.validate_parcel_right_relationship(db, ladm_queries))
        elif id_quality_rule == EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_A_TABLE:
            # Check a predefined list of tables (and fields that define a duplicate record)
            for table, fields in LayerConfig.get_logic_consistency_tables(db.names):
                res.append(self.validate_duplicate_records_in_a_table(db, ladm_queries, table, fields))
        elif id_quality_rule == EnumQualityRule.Logic.FRACTION_SUM_FOR_PARTY_GROUPS:
            res.append(self.validate_fraction_sum_for_party_groups(db, ladm_queries))
        elif id_quality_rule == EnumQualityRule.Logic.DEPARTMENT_CODE_HAS_TWO_NUMERICAL_CHARACTERS:
            res.append(self.validate_department_code_has_two_numerical_characters(db, ladm_queries))
        elif id_quality_rule == EnumQualityRule.Logic.MUNICIPALITY_CODE_HAS_THREE_NUMERICAL_CHARACTERS:
            res.append(self.validate_municipality_code_has_three_numerical_characters(db, ladm_queries))
        elif id_quality_rule == EnumQualityRule.Logic.PARCEL_NUMBER_HAS_30_NUMERICAL_CHARACTERS:
            res.append(self.validate_parcel_number_has_30_numerical_characters(db, ladm_queries))
        elif id_quality_rule == EnumQualityRule.Logic.PARCEL_NUMBER_BEFORE_HAS_20_NUMERICAL_CHARACTERS:
            res.append(self.validate_parcel_number_before_has_20_numerical_characters(db, ladm_queries))
        elif id_quality_rule == EnumQualityRule.Logic.COL_PARTY_NATURAL_TYPE:
            res.append(self.validate_col_party_natural_type(db, ladm_queries))
        elif id_quality_rule == EnumQualityRule.Logic.COL_PARTY_NOT_NATURAL_TYPE:
            res.append(self.validate_col_party_no_natural_type(db, ladm_queries))
        elif id_quality_rule == EnumQualityRule.Logic.PARCEL_TYPE_AND_22_POSITION_OF_PARCEL_NUMBER:
            res.append(self.validate_parcel_type_and_22_position_of_parcel_number(db, ladm_queries))
        elif id_quality_rule == EnumQualityRule.Logic.UEBAUNIT_PARCEL:
            res.append(self.validate_uebaunit_parcel(db, ladm_queries))

        return res
