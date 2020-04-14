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
                              pyqtSignal,
                              QCoreApplication)
from qgis.PyQt.QtGui import (QBrush,
                             QFont,
                             QIcon,
                             QColor)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QDialogButtonBox,
                                 QTreeWidgetItem,
                                 QTreeWidgetItemIterator)
from qgis.core import Qgis

from asistente_ladm_col.config.config_db_supported import ConfigDBsSupported
from asistente_ladm_col.config.enums import EnumQualityRule
from asistente_ladm_col.logic.quality.facade_quality_rules import FacadeQualityRules
from asistente_ladm_col.config.general_config import (LOG_QUALITY_LIST_ITEM_ERROR_OPEN,
                                                      LOG_QUALITY_LIST_ITEM_CORRECT_OPEN,
                                                      LOG_QUALITY_LIST_ITEM_ERROR_CLOSE,
                                                      LOG_QUALITY_LIST_ITEM_CORRECT_CLOSE,
                                                      LOG_QUALITY_LIST_ITEM_OPEN,
                                                      LOG_QUALITY_LIST_ITEM_CLOSE)
from asistente_ladm_col.config.layer_config import LayerConfig
from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.utils import show_plugin_help
from asistente_ladm_col.utils.utils import Utils
from asistente_ladm_col.utils.decorators import _log_quality_rules
from asistente_ladm_col.lib.quality_rule.quality_rule_manager import QualityRuleManager
from asistente_ladm_col.lib.logger import Logger

DIALOG_UI = get_ui_class('dialogs/dlg_quality.ui')


class QualityDialog(QDialog, DIALOG_UI):
    log_quality_show_message_emitted = pyqtSignal(str, int)
    log_quality_show_button_emitted = pyqtSignal()
    log_quality_set_initial_progress_emitted = pyqtSignal(str)
    log_quality_set_final_progress_emitted = pyqtSignal(str)

    def __init__(self, db, qgis_utils, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self._db = db
        self.qgis_utils = qgis_utils
        self.quality_rules_manager = QualityRuleManager()
        self._ladm_queries = ConfigDBsSupported().get_db_factory(self._db.engine).get_ladm_queries(self.qgis_utils)
        self.utils = Utils()
        self.facade_quality_rules = FacadeQualityRules(self.qgis_utils)
        self.names = self._db.names
        self.log_dialog_quality_text = ""
        self.log_dialog_quality_text_content = ""
        self.total_time = 0

        self.trw_quality_rules.setItemsExpandable(False)
        self.trw_quality_rules.itemSelectionChanged.connect(self.validate_selection_rules)
        self.trw_quality_rules.itemSelectionChanged.emit()

        # Set connections
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.rejected)
        self.buttonBox.helpRequested.connect(self.show_help)
        self.btn_select_all.clicked.connect(self.select_all)
        self.btn_clear_selection.clicked.connect(self.clear_selection)
        Logger().clear_message_bar()

        self.items_dict = collections.OrderedDict()
        for quality_rule_group_code, quality_rule_group_name in self.quality_rules_manager.quality_rule_groups.items():
            self.items_dict[quality_rule_group_name] = {
                'rules': [{'id': rule_k, 'text': rule_v} for rule_k, rule_v in self.quality_rules_manager.get_rules(quality_rule_group_code).items()]
            }

            if quality_rule_group_code == EnumQualityRule.Point:
                self.items_dict[quality_rule_group_name]['icon'] = 'points'
            elif quality_rule_group_code == EnumQualityRule.Line:
                self.items_dict[quality_rule_group_name]['icon'] = 'lines'
            elif quality_rule_group_code == EnumQualityRule.Polygon:
                self.items_dict[quality_rule_group_name]['icon'] = 'polygons'
            elif quality_rule_group_code == EnumQualityRule.Logic:
                self.items_dict[quality_rule_group_name]['icon'] = 'tables'

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
        self.initialize_log_dialog_quality()
        selected_count = len(self.trw_quality_rules.selectedItems())

        if selected_count > 0:
            self.set_count_topology_rules(selected_count)

        iterator = QTreeWidgetItemIterator(self.trw_quality_rules, QTreeWidgetItemIterator.Selectable)
        while iterator.value():
            item = iterator.value()

            if item.isSelected():
                id = item.data(0, Qt.UserRole)
                rule_name = item.text(0)
                self.execute_quality_rule(id, rule_name=rule_name)
            iterator += 1

        if selected_count > 0:
            self.generate_log_button()

        if self.qgis_utils.error_group_exists():
            group = self.qgis_utils.get_error_layers_group()
            # # Check if group layer is empty
            if group.findLayers():
                self.qgis_utils.set_error_group_visibility(True)
            else:
                self.qgis_utils.remove_error_group_requested.emit()

    @_log_quality_rules
    def execute_quality_rule(self, id, rule_name):
        # NOTE: Do not remove the named parameters, this is needed for making a decorator that thinks they are
        # optional happy!
        # POINTS QUALITY RULES
        if id == EnumQualityRule.Point.OVERLAPS_IN_BOUNDARY_POINTS:
            result = self.facade_quality_rules.validate_overlaps_in_boundary_points(self._db)
        elif id == EnumQualityRule.Point.OVERLAPS_IN_CONTROL_POINTS:
            result = self.facade_quality_rules.validate_overlaps_in_control_points(self._db)
        elif id == EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES:
            result = self.facade_quality_rules.validate_boundary_points_covered_by_boundary_nodes(self._db)
        elif id == EnumQualityRule.Point.BOUNDARY_POINTS_COVERED_BY_PLOT_NODES:
            result = self.facade_quality_rules.validate_boundary_points_covered_by_plot_nodes(self._db)
        # LINES QUALITY RULES
        elif id == EnumQualityRule.Line.OVERLAPS_IN_BOUNDARIES:
            result = self.facade_quality_rules.validate_overlaps_in_boundaries(self._db)
        elif id == EnumQualityRule.Line.BOUNDARIES_ARE_NOT_SPLIT:
            result = self.facade_quality_rules.validate_boundaries_are_not_split(self._db)
        elif id == EnumQualityRule.Line.BOUNDARIES_COVERED_BY_PLOTS:
            result = self.facade_quality_rules.validate_boundaries_covered_by_plots(self._db)
        elif id == EnumQualityRule.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS:
            result = self.facade_quality_rules.validate_boundary_nodes_covered_by_boundary_points(self._db)
        elif id == EnumQualityRule.Line.DANGLES_IN_BOUNDARIES:
            result = self.facade_quality_rules.validate_dangles_in_boundaries(self._db)
        # POLYGONS QUALITY RULES
        elif id == EnumQualityRule.Polygon.OVERLAPS_IN_PLOTS:
            result = self.facade_quality_rules.validate_overlaps_in_plots(self._db)
        elif id == EnumQualityRule.Polygon.OVERLAPS_IN_BUILDINGS:
            result = self.facade_quality_rules.validate_overlaps_in_buildings(self._db)
        elif id == EnumQualityRule.Polygon.OVERLAPS_IN_RIGHTS_OF_WAY:
            result = self.facade_quality_rules.validate_overlaps_in_rights_of_way(self._db)
        elif id == EnumQualityRule.Polygon.PLOTS_COVERED_BY_BOUNDARIES:
            result = self.facade_quality_rules.validate_plots_covered_by_boundaries(self._db)
        # elif id == 'check_missing_survey_points_in_buildings':
        #    self.facade_quality_rules.check_missing_survey_points_in_buildings(self._db)
        elif id == EnumQualityRule.Polygon.RIGHT_OF_WAY_OVERLAPS_BUILDINGS:
            result = self.facade_quality_rules.validate_right_of_way_overlaps_buildings(self._db)
        elif id == EnumQualityRule.Polygon.GAPS_IN_PLOTS:
            result = self.facade_quality_rules.validate_gaps_in_plots(self._db)
        elif id == EnumQualityRule.Polygon.MULTIPART_IN_RIGHT_OF_WAY:
            result = self.facade_quality_rules.validate_multipart_in_right_of_way(self._db)
        elif id == EnumQualityRule.Polygon.PLOT_NODES_COVERED_BY_BOUNDARY_POINTS:
            result = self.facade_quality_rules.validate_plot_nodes_covered_by_boundary_points(self._db)
        elif id == EnumQualityRule.Polygon.BUILDINGS_SHOULD_BE_WITHIN_PLOTS:
            result = self.facade_quality_rules.validate_buildings_should_be_within_plots(self._db)
        elif id == EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_PLOTS:
            result = self.facade_quality_rules.validate_building_units_should_be_within_plots(self._db)
        # LOGIC QUALITY RULES
        elif id == EnumQualityRule.Logic.PARCEL_RIGHT_RELATIONSHIP:
            result = self.facade_quality_rules.validate_parcel_right_relationship(self._db, self._ladm_queries)
        elif id == EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_A_TABLE:

            # Check a predifene list of tables   list of define table with
            logic_consistency_tables = LayerConfig.get_logic_consistency_tables(self._db.names)
            for table in logic_consistency_tables:
                fields = logic_consistency_tables[table]
                result = self.facade_quality_rules.validate_duplicate_records_in_a_table(self._db, self._ladm_queries, table, fields)
                self.log_message(result[0], result[1])  # message, Qgis::MessageLevel

        elif id == EnumQualityRule.Logic.FRACTION_SUM_FOR_PARTY_GROUPS:
            result = self.facade_quality_rules.validate_fraction_sum_for_party_groups(self._db, self._ladm_queries)
        elif id == EnumQualityRule.Logic.DEPARTMENT_CODE_HAS_TWO_NUMERICAL_CHARACTERS:
            result = self.facade_quality_rules.validate_department_code_has_two_numerical_characters(self._db, self._ladm_queries)
        elif id == EnumQualityRule.Logic.MUNICIPALITY_CODE_HAS_THREE_NUMERICAL_CHARACTERS:
            result = self.facade_quality_rules.validate_municipality_code_has_three_numerical_characters(self._db, self._ladm_queries)
        elif id == EnumQualityRule.Logic.PARCEL_NUMBER_HAS_30_NUMERICAL_CHARACTERS:
            result = self.facade_quality_rules.validate_parcel_number_has_30_numerical_characters(self._db, self._ladm_queries)
        elif id == EnumQualityRule.Logic.PARCEL_NUMBER_BEFORE_HAS_20_NUMERICAL_CHARACTERS:
            result = self.facade_quality_rules.validate_parcel_number_before_has_20_numerical_characters(self._db, self._ladm_queries)
        elif id == EnumQualityRule.Logic.COL_PARTY_NATURAL_TYPE:
            result = self.facade_quality_rules.validate_col_party_natural_type(self._db, self._ladm_queries)
        elif id == EnumQualityRule.Logic.COL_PARTY_NOT_NATURAL_TYPE:
            result = self.facade_quality_rules.validate_col_party_no_natural_type(self._db, self._ladm_queries)
        elif id == EnumQualityRule.Logic.PARCEL_TYPE_AND_22_POSITION_OF_PARCEL_NUMBER:
            result = self.facade_quality_rules.validate_parcel_type_and_22_position_of_parcel_number(self._db, self._ladm_queries)
        elif id == EnumQualityRule.Logic.UEBAUNIT_PARCEL:
            result = self.facade_quality_rules.validate_uebaunit_parcel(self._db, self._ladm_queries)

        # It does not apply for duplicate table records because it was done before
        if id != EnumQualityRule.Logic.DUPLICATE_RECORDS_IN_A_TABLE:
            self.log_message(result[0], result[1])  # message, Qgis::MessageLevel

    def set_count_topology_rules(self, count):
        self.log_quality_show_message_emitted.emit(QCoreApplication.translate("QualityDialog", ""), count)

    def generate_log_button(self):
        self.log_quality_show_button_emitted.emit()

    def get_log_dialog_quality_text(self):
        return self.log_dialog_quality_text, self.total_time

    def initialize_log_dialog_quality(self):
        self.log_dialog_quality_text = ""
        self.total_time = 0

    def log_message(self, msg, level):
        if level == Qgis.Critical:
            prefix = LOG_QUALITY_LIST_ITEM_ERROR_OPEN
            suffix = LOG_QUALITY_LIST_ITEM_ERROR_CLOSE
        elif level == Qgis.Success:
            prefix = LOG_QUALITY_LIST_ITEM_CORRECT_OPEN
            suffix = LOG_QUALITY_LIST_ITEM_CORRECT_CLOSE
        else: # Qgis.Info
            prefix = LOG_QUALITY_LIST_ITEM_OPEN
            suffix = LOG_QUALITY_LIST_ITEM_CLOSE

        self.log_dialog_quality_text_content += "{}{}{}".format(prefix, msg, suffix)

    def rejected(self):
        pass

    def select_all(self):
        self.trw_quality_rules.selectAll()

    def clear_selection(self):
        self.trw_quality_rules.clearSelection()

    def show_help(self):
        show_plugin_help("quality_rules")
