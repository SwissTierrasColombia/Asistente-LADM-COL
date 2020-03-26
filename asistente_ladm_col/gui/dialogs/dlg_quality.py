# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-06-11
        git sha              : :%H$
        copyright            : (C) 2018 by Germán Carrillo (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
import collections
from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication)
from qgis.PyQt.QtGui import (QBrush,
                             QFont,
                             QIcon,
                             QColor)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QDialogButtonBox,
                                 QTreeWidgetItem,
                                 QTreeWidgetItemIterator)
from asistente_ladm_col.config.translation_strings import (TranslatableConfigStrings,
                                                           CHECK_OVERLAPS_IN_BOUNDARY_POINTS,
                                                           CHECK_OVERLAPS_IN_CONTROL_POINTS,
                                                           CHECK_BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES,
                                                           CHECK_BOUNDARY_POINTS_COVERED_BY_PLOT_NODES,
                                                           CHECK_OVERLAPS_IN_BOUNDARIES,
                                                           CHECK_BOUNDARIES_ARE_NOT_SPLIT,
                                                           CHECK_BOUNDARIES_COVERED_BY_PLOTS,
                                                           CHECK_BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS,
                                                           CHECK_DANGLES_IN_BOUNDARIES,
                                                           CHECK_OVERLAPS_IN_PLOTS,
                                                           CHECK_OVERLAPS_IN_BUILDINGS,
                                                           CHECK_OVERLAPS_IN_RIGHTS_OF_WAY,
                                                           CHECK_PLOTS_COVERED_BY_BOUNDARIES,
                                                           CHECK_RIGHT_OF_WAY_OVERLAPS_BUILDINGS,
                                                           CHECK_GAPS_IN_PLOTS,
                                                           CHECK_MULTIPART_IN_RIGHT_OF_WAY,
                                                           CHECK_BUILDING_WITHIN_PLOTS,
                                                           CHECK_BUILDING_UNIT_WITHIN_PLOTS,
                                                           CHECK_PARCEL_RIGHT_RELATIONSHIP,
                                                           CHECK_FRACTION_SUM_FOR_PARTY_GROUPS,
                                                           FIND_DUPLICATE_RECORDS_IN_A_TABLE,
                                                           CHECK_DEPARMENT_CODE_HAS_TWO_NUMERICAL_CHARACTERS,
                                                           CHECK_MUNICIPALITY_CODE_HAS_THREE_NUMERICAL_CHARACTERS,
                                                           CHECK_PARCEL_NUMBER_HAS_30_NUMERICAL_CHARACTERS,
                                                           CHECK_PARCEL_NUMBER_BEFORE_HAS_20_NUMERICAL_CHARACTERS,
                                                           CHECK_COL_PARTY_NATURAL_TYPE,
                                                           CHECK_COL_PARTY_LEGAL_TYPE,
                                                           CHECK_PARCEL_TYPE_AND_22_POSITON_OF_PARCEL_NUMBER,
                                                           CHECK_UEBAUNIT_PARCEL,
                                                           CHECK_PLOT_NODES_COVERED_BY_BOUNDARY_POINTS)
from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.utils import show_plugin_help

DIALOG_UI = get_ui_class('dialogs/dlg_quality.ui')


class QualityDialog(QDialog, DIALOG_UI):
    def __init__(self, db, qgis_utils, quality, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self._db = db
        self.qgis_utils = qgis_utils
        self.quality = quality
        self.names = self._db.names
        self.translatable_config_strings = TranslatableConfigStrings()

        self.trw_quality_rules.setItemsExpandable(False)
        self.trw_quality_rules.itemSelectionChanged.connect(self.validate_selection_rules)
        self.trw_quality_rules.itemSelectionChanged.emit()

        # Set connections
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.rejected)
        self.buttonBox.helpRequested.connect(self.show_help)
        self.btn_select_all.clicked.connect(self.select_all)
        self.btn_clear_selection.clicked.connect(self.clear_selection)

        translated_strings = self.translatable_config_strings.get_translatable_config_strings()

        self.items_dict = collections.OrderedDict()
        self.items_dict[QCoreApplication.translate("QualityDialog", "Rules for Points")] = {
                'icon': 'points',
                'rules': [{
                    'id' : 'check_overlaps_in_boundary_points',
                    'text': translated_strings[CHECK_OVERLAPS_IN_BOUNDARY_POINTS]
                },{
                    'id' : 'check_overlaps_in_control_points',
                    'text': translated_strings[CHECK_OVERLAPS_IN_CONTROL_POINTS]
                },{
                    'id' : 'check_boundary_points_covered_by_boundary_nodes',
                    'text': translated_strings[CHECK_BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES]
                },{
                    'id' : 'check_boundary_points_covered_by_plot_nodes',
                    'text': translated_strings[CHECK_BOUNDARY_POINTS_COVERED_BY_PLOT_NODES]
                }]
            }
        self.items_dict[QCoreApplication.translate("QualityDialog", "Rules for Lines")] = {
                'icon' : 'lines',
                'rules': [{
                    'id': 'check_overlaps_in_boundaries',
                    'text': translated_strings[CHECK_OVERLAPS_IN_BOUNDARIES]
                }, {
                    'id': 'check_boundaries_are_not_split',
                    'text': translated_strings[CHECK_BOUNDARIES_ARE_NOT_SPLIT]
                }, {
                    'id': 'check_boundaries_covered_by_plots',
                    'text': translated_strings[CHECK_BOUNDARIES_COVERED_BY_PLOTS]
                }, {
                    'id': 'check_boundary_nodes_covered_by_boundary_points',
                    'text': translated_strings[CHECK_BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS]
                }, {
                    'id': 'check_dangles_in_boundaries',
                    'text': translated_strings[CHECK_DANGLES_IN_BOUNDARIES]
                }]
            }
        self.items_dict[QCoreApplication.translate("QualityDialog", "Rules for Polygons")] = {
                'icon': 'polygons',
                'rules': [{
                    'id': 'check_overlaps_in_plots',
                    'text': translated_strings[CHECK_OVERLAPS_IN_PLOTS]
                },{
                    'id': 'check_overlaps_in_buildings',
                    'text': translated_strings[CHECK_OVERLAPS_IN_BUILDINGS]
                },{
                    'id': 'check_overlaps_in_rights_of_way',
                    'text': translated_strings[CHECK_OVERLAPS_IN_RIGHTS_OF_WAY]
                },{
                    'id': 'check_plots_covered_by_boundaries',
                    'text': translated_strings[CHECK_PLOTS_COVERED_BY_BOUNDARIES]
                #}, {
                #    'id': 'check_missing_survey_points_in_buildings',
                #    'text': QCoreApplication.translate("QualityDialog", "Buildings nodes should be covered by Survey Points")
                }, {
                    'id': 'check_right_of_way_overlaps_buildings',
                    'text': translated_strings[CHECK_RIGHT_OF_WAY_OVERLAPS_BUILDINGS]
                }, {
                    'id': 'check_gaps_in_plots',
                    'text': translated_strings[CHECK_GAPS_IN_PLOTS]
                }, {
                    'id': 'check_multipart_in_right_of_way',
                    'text': translated_strings[CHECK_MULTIPART_IN_RIGHT_OF_WAY]
                }, {
                    'id': 'check_plot_nodes_covered_by_boundary_points',
                    'text': translated_strings[CHECK_PLOT_NODES_COVERED_BY_BOUNDARY_POINTS]
                },{
                    'id': 'check_buildings_should_be_within_plots',
                    'text': translated_strings[CHECK_BUILDING_WITHIN_PLOTS]
                },{
                    'id': 'check_building_units_should_be_within_plots',
                    'text': translated_strings[CHECK_BUILDING_UNIT_WITHIN_PLOTS]
                }]
            }

        self.items_dict[QCoreApplication.translate("QualityDialog", "Logic consistency rules")] = {
                'icon': 'tables',
                'rules': [{
                    'id': 'check_parcel_right_relationship',
                    'text': translated_strings[CHECK_PARCEL_RIGHT_RELATIONSHIP]
                }, {
                    'id': 'find_duplicate_records_in_a_table',
                    'text': translated_strings[FIND_DUPLICATE_RECORDS_IN_A_TABLE]
                }, {
                    'id': 'check_fraction_sum_for_party_groups',
                    'text': translated_strings[CHECK_FRACTION_SUM_FOR_PARTY_GROUPS]
                }, {
                    'id': 'check_department_code_has_two_numerical_characters',
                    'text': translated_strings[CHECK_DEPARMENT_CODE_HAS_TWO_NUMERICAL_CHARACTERS]
                }, {
                    'id': 'check_municipality_code_has_three_numerical_characters',
                    'text': translated_strings[CHECK_MUNICIPALITY_CODE_HAS_THREE_NUMERICAL_CHARACTERS]
                }, {
                    'id': 'check_parcel_number_has_30_numerical_characters',
                    'text': translated_strings[CHECK_PARCEL_NUMBER_HAS_30_NUMERICAL_CHARACTERS]
                }, {
                    'id': 'check_parcel_number_before_has_20_numerical_characters',
                    'text': translated_strings[CHECK_PARCEL_NUMBER_BEFORE_HAS_20_NUMERICAL_CHARACTERS]
                }, {
                    'id': 'check_col_party_natural_type',
                    'text': translated_strings[CHECK_COL_PARTY_NATURAL_TYPE]
                }, {
                    'id': 'check_col_party_legal_type',
                    'text': translated_strings[CHECK_COL_PARTY_LEGAL_TYPE]
                }, {
                    'id': 'check_parcel_type_and_22_position_of_parcel_number',
                    'text': translated_strings[CHECK_PARCEL_TYPE_AND_22_POSITON_OF_PARCEL_NUMBER]
                }, {
                    'id': 'check_uebaunit_parcel',
                    'text': translated_strings[CHECK_UEBAUNIT_PARCEL]
                }]
            }

        self.load_items()

    def validate_selection_rules(self):
        # At least one quality rule must have been selected
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(bool(self.trw_quality_rules.selectedItems()))

    def load_items(self):
        self.trw_quality_rules.setUpdatesEnabled(False) # Don't render until we're ready
        self.trw_quality_rules.clear()

        font = QFont()
        font.setBold(True)

        for group, items in self.items_dict.items():
            children = []
            group_item = QTreeWidgetItem([group])
            group_item.setData(0, Qt.BackgroundRole, QBrush(QColor(219, 219, 219, 255)))
            group_item.setData(0, Qt.FontRole, font)
            icon = QIcon(":/Asistente-LADM_COL/resources/images/{}.png".format(items['icon']))
            group_item.setData(0, Qt.DecorationRole, icon)

            for rule in items['rules']:
                rule_item = QTreeWidgetItem([rule['text']])
                rule_item.setData(0, Qt.UserRole, rule['id'])

                children.append(rule_item)

            group_item.addChildren(children)
            self.trw_quality_rules.addTopLevelItem(group_item)

        # Make group items non selectable and expanded
        for i in range(self.trw_quality_rules.topLevelItemCount()):
            self.trw_quality_rules.topLevelItem(i).setFlags(Qt.ItemIsEnabled) # Not selectable
            self.trw_quality_rules.topLevelItem(i).setExpanded(True)

        self.trw_quality_rules.setUpdatesEnabled(True) # Now render!

    def accepted(self):
        # we erase the group error layer every time it runs because we assume that data set changes.
        self.qgis_utils.remove_error_group_requested.emit()
        self.quality.initialize_log_dialog_quality()
        selected_count = len(self.trw_quality_rules.selectedItems())

        if selected_count > 0:
            self.quality.set_count_topology_rules(selected_count)
        translated_strings = self.translatable_config_strings.get_translatable_config_strings()

        iterator = QTreeWidgetItemIterator(self.trw_quality_rules, QTreeWidgetItemIterator.Selectable)
        while iterator.value():
            item = iterator.value()

            if item.isSelected():
                id = item.data(0, Qt.UserRole)
                rule_name = item.text(0)

                # NOTE: Do not remove the named parameters, this is needed for making a decorator that thinks they are
                # optional happy!
                if id == 'check_overlaps_in_boundary_points':
                    self.quality.check_overlapping_points(self._db, point_layer_name=self.names.OP_BOUNDARY_POINT_T, rule_name=rule_name, translated_strings=translated_strings)
                elif id == 'check_overlaps_in_control_points':
                    self.quality.check_overlapping_points(self._db, point_layer_name=self.names.OP_CONTROL_POINT_T, rule_name=rule_name, translated_strings=translated_strings)
                elif id == 'check_boundary_points_covered_by_boundary_nodes':
                    self.quality.check_boundary_points_covered_by_boundary_nodes(self._db, rule_name=rule_name, translated_strings=translated_strings)
                elif id == 'check_boundary_points_covered_by_plot_nodes':
                    self.quality.check_boundary_points_covered_by_plot_nodes(self._db, rule_name=rule_name, translated_strings=translated_strings)
                elif id == 'check_overlaps_in_boundaries':
                    self.quality.check_overlaps_in_boundaries(self._db, rule_name=rule_name, translated_strings=translated_strings)
                elif id == 'check_boundaries_are_not_split':
                    self.quality.check_boundaries_are_not_split(self._db, rule_name=rule_name, translated_strings=translated_strings)
                elif id == 'check_boundaries_covered_by_plots':
                    self.quality.check_boundaries_covered_by_plots(self._db, rule_name=rule_name, translated_strings=translated_strings)
                elif id == 'check_boundary_nodes_covered_by_boundary_points':
                    self.quality.check_boundary_nodes_covered_by_boundary_points(self._db, rule_name=rule_name, translated_strings=translated_strings)
                elif id == 'check_dangles_in_boundaries':
                    self.quality.check_dangles_in_boundaries(self._db, rule_name=rule_name, translated_strings=translated_strings)
                elif id == 'check_overlaps_in_plots':
                    self.quality.check_overlapping_polygons(self._db, polygon_layer_name=self.names.OP_PLOT_T, rule_name=rule_name, translated_strings=translated_strings)
                elif id == 'check_overlaps_in_buildings':
                    self.quality.check_overlapping_polygons(self._db, polygon_layer_name=self.names.OP_BUILDING_T, rule_name=rule_name, translated_strings=translated_strings)
                elif id == 'check_overlaps_in_rights_of_way':
                    self.quality.check_overlapping_polygons(self._db, polygon_layer_name=self.names.OP_RIGHT_OF_WAY_T, rule_name=rule_name, translated_strings=translated_strings)
                elif id == 'check_plots_covered_by_boundaries':
                    self.quality.check_plots_covered_by_boundaries(self._db, rule_name=rule_name, translated_strings=translated_strings)
                #elif id == 'check_missing_survey_points_in_buildings':
                #    self.quality.check_missing_survey_points_in_buildings(self._db)
                elif id == 'check_right_of_way_overlaps_buildings':
                    self.quality.check_right_of_way_overlaps_buildings(self._db, rule_name=rule_name, translated_strings=translated_strings)
                elif id == 'check_gaps_in_plots':
                    self.quality.check_gaps_in_plots(self._db, rule_name=rule_name, translated_strings=translated_strings)
                elif id == 'check_multipart_in_right_of_way':
                    self.quality.check_multiparts_in_right_of_way(self._db, rule_name=rule_name, translated_strings=translated_strings)
                elif id == 'check_plot_nodes_covered_by_boundary_points':
                    self.quality.check_plot_nodes_covered_by_boundary_points(self._db, rule_name=rule_name, translated_strings=translated_strings)
                elif id == 'check_buildings_should_be_within_plots':
                    self.quality.check_building_within_plots(self._db, rule_name=rule_name, translated_strings=translated_strings)
                elif id == 'check_building_units_should_be_within_plots':
                    self.quality.check_building_unit_within_plots(self._db, rule_name=rule_name, translated_strings=translated_strings)
                elif id == 'check_parcel_right_relationship':
                    self.quality.check_parcel_right_relationship(self._db, rule_name=rule_name, translated_strings=translated_strings)
                elif id == 'find_duplicate_records_in_a_table':
                    self.quality.find_duplicate_records_in_a_table(self._db, rule_name=rule_name)
                elif id == 'check_fraction_sum_for_party_groups':
                    self.quality.check_fraction_sum_for_party_groups(self._db, rule_name=rule_name)
                elif id == 'check_department_code_has_two_numerical_characters':
                    self.quality.basic_logic_validations(self._db, rule='DEPARTMENT_CODE_VALIDATION', rule_name=rule_name)
                elif id == 'check_municipality_code_has_three_numerical_characters':
                    self.quality.basic_logic_validations(self._db, rule='MUNICIPALITY_CODE_VALIDATION', rule_name=rule_name)
                elif id == 'check_parcel_number_has_30_numerical_characters':
                    self.quality.basic_logic_validations(self._db, rule='PARCEL_NUMBER_VALIDATION', rule_name=rule_name)
                elif id == 'check_parcel_number_before_has_20_numerical_characters':
                    self.quality.basic_logic_validations(self._db, rule='PARCEL_NUMBER_BEFORE_VALIDATION', rule_name=rule_name)
                elif id == 'check_col_party_natural_type':
                    self.quality.advanced_logic_validations(self._db, rule='COL_PARTY_TYPE_NATURAL_VALIDATION', rule_name=rule_name)
                elif id == 'check_col_party_legal_type':
                    self.quality.advanced_logic_validations(self._db, rule='COL_PARTY_TYPE_NO_NATURAL_VALIDATION', rule_name=rule_name)
                elif id == 'check_parcel_type_and_22_position_of_parcel_number':
                    self.quality.advanced_logic_validations(self._db, rule='PARCEL_TYPE_AND_22_POSITION_OF_PARCEL_NUMBER_VALIDATION', rule_name=rule_name)
                elif id == 'check_uebaunit_parcel':
                    self.quality.advanced_logic_validations(self._db, rule='UEBAUNIT_PARCEL_VALIDATION', rule_name=rule_name)

            iterator += 1

        if selected_count > 0:
            self.quality.generate_log_button()

        if self.qgis_utils.error_group_exists():
            group = self.qgis_utils.get_error_layers_group()
            # # Check if group layer is empty
            if group.findLayers():
                self.qgis_utils.set_error_group_visibility(True)
            else:
                self.qgis_utils.remove_error_group_requested.emit()

    def rejected(self):
        pass

    def select_all(self):
        self.trw_quality_rules.selectAll()

    def clear_selection(self):
        self.trw_quality_rules.clearSelection()

    def show_help(self):
        show_plugin_help("quality_rules")
