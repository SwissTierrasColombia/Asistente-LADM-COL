from asistente_ladm_col.logic.quality.point_quality_rules import PointQualityRules
from asistente_ladm_col.logic.quality.line_quality_rules import LineQualityRules
from asistente_ladm_col.logic.quality.polygon_quality_rules import PolygonQualityRules
from asistente_ladm_col.logic.quality.logic_quality_rules import LogicQualityRules
from asistente_ladm_col.config.translation_strings import TranslatableConfigStrings


class FacadeQualityRules:
    def __init__(self, qgis_utils):
        self.qgis_utils = qgis_utils
        self.translated_strings = TranslatableConfigStrings().get_translatable_config_strings()
        self.point_quality_rules = PointQualityRules(self.qgis_utils, self.translated_strings)
        self.line_quality_rules = LineQualityRules(self.qgis_utils, self.translated_strings)
        self.polygon_quality_rules = PolygonQualityRules(self.qgis_utils, self.translated_strings)
        self.logic_quality_rules = LogicQualityRules(self.qgis_utils, self.translated_strings)

    # POINTS QUALITY RULES
    def validate_overlaps_in_boundary_points(self, db, point_layer_name):
        return self.point_quality_rules.check_overlapping_points(db, point_layer_name)

    def validate_overlaps_in_control_points(self, db, point_layer_name):
        return self.point_quality_rules.check_overlapping_points(db, point_layer_name)

    def validate_boundary_points_covered_by_boundary_nodes(self, db):
        return self.point_quality_rules.check_boundary_points_covered_by_boundary_nodes(db)

    def validate_boundary_points_covered_by_plot_nodes(self, db):
        return self.point_quality_rules.check_boundary_points_covered_by_plot_nodes(db)

    # LINES QUALITY RULES
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

    # POLYGONS QUALITY RULES
    def validate_overlaps_in_plots(self, db, polygon_layer_name):
        return self.polygon_quality_rules.check_overlapping_polygons(db, polygon_layer_name)

    def validate_overlaps_in_buildings(self, db, polygon_layer_name):
        return self.polygon_quality_rules.check_overlapping_polygons(db, polygon_layer_name)

    def validate_overlaps_in_rights_of_way(self, db, polygon_layer_name):
        return self.polygon_quality_rules.check_overlapping_polygons(db, polygon_layer_name)

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
