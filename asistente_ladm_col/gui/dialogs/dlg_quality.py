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


from asistente_ladm_col.config.enums import QualityRuleEnum
from asistente_ladm_col.logic.quality.facade_quality_rules import FacadeQualityRules
from asistente_ladm_col.config.general_config import (LOG_QUALITY_LIST_ITEM_ERROR_OPEN,
                                                      LOG_QUALITY_LIST_ITEM_CORRECT_OPEN,
                                                      LOG_QUALITY_LIST_ITEM_ERROR_CLOSE,
                                                      LOG_QUALITY_LIST_ITEM_CORRECT_CLOSE,
                                                      LOG_QUALITY_LIST_ITEM_OPEN,
                                                      LOG_QUALITY_LIST_ITEM_CLOSE)
from asistente_ladm_col.config.translation_strings import TranslatableConfigStrings
from asistente_ladm_col.config.layer_config import LayerConfig
from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.utils import Utils
from asistente_ladm_col.utils.decorators import _log_quality_rules
from asistente_ladm_col.lib.logger import Logger

DIALOG_UI = get_ui_class('dialogs/dlg_quality.ui')


class QualityDialog(QDialog, DIALOG_UI):
    log_quality_show_message_emitted = pyqtSignal(str, int)
    log_quality_show_button_emitted = pyqtSignal()
    log_quality_set_initial_progress_emitted = pyqtSignal(str)
    log_quality_set_final_progress_emitted = pyqtSignal(str)

    def __init__(self, db, query_manager, qgis_utils, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self._db = db
        self._query_manager = query_manager
        self.qgis_utils = qgis_utils
        self.utils = Utils()
        self.facade_quality_rules = FacadeQualityRules(self.qgis_utils)
        self.names = self._db.names
        self.translatable_config_strings = TranslatableConfigStrings()
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

        translated_strings = self.translatable_config_strings.get_translatable_config_strings()

        self.items_dict = collections.OrderedDict()
        self.items_dict[QCoreApplication.translate("QualityDialog", "Rules for Points")] = {
                'icon': 'points',
                'rules': [{
                    'id' : QualityRuleEnum.Point.OVERLAPS_IN_BOUNDARY_POINTS,
                    'text': translated_strings[QualityRuleEnum.Point.OVERLAPS_IN_BOUNDARY_POINTS]
                },{
                    'id' : QualityRuleEnum.Point.OVERLAPS_IN_CONTROL_POINTS,
                    'text': translated_strings[QualityRuleEnum.Point.OVERLAPS_IN_CONTROL_POINTS]
                },{
                    'id' : QualityRuleEnum.Point.BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES,
                    'text': translated_strings[QualityRuleEnum.Point.BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES]
                },{
                    'id' : QualityRuleEnum.Point.BOUNDARY_POINTS_COVERED_BY_PLOT_NODES,
                    'text': translated_strings[QualityRuleEnum.Point.BOUNDARY_POINTS_COVERED_BY_PLOT_NODES]
                }]
            }
        self.items_dict[QCoreApplication.translate("QualityDialog", "Rules for Lines")] = {
                'icon' : 'lines',
                'rules': [{
                    'id': QualityRuleEnum.Line.OVERLAPS_IN_BOUNDARIES,
                    'text': translated_strings[QualityRuleEnum.Line.OVERLAPS_IN_BOUNDARIES]
                }, {
                    'id': QualityRuleEnum.Line.BOUNDARIES_ARE_NOT_SPLIT,
                    'text': translated_strings[QualityRuleEnum.Line.BOUNDARIES_ARE_NOT_SPLIT]
                }, {
                    'id': QualityRuleEnum.Line.BOUNDARIES_COVERED_BY_PLOTS,
                    'text': translated_strings[QualityRuleEnum.Line.BOUNDARIES_COVERED_BY_PLOTS]
                }, {
                    'id': QualityRuleEnum.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS,
                    'text': translated_strings[QualityRuleEnum.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS]
                }, {
                    'id': QualityRuleEnum.Line.DANGLES_IN_BOUNDARIES,
                    'text': translated_strings[QualityRuleEnum.Line.DANGLES_IN_BOUNDARIES]
                }]
            }
        self.items_dict[QCoreApplication.translate("QualityDialog", "Rules for Polygons")] = {
                'icon': 'polygons',
                'rules': [{
                    'id': QualityRuleEnum.Polygon.OVERLAPS_IN_PLOTS,
                    'text': translated_strings[QualityRuleEnum.Polygon.OVERLAPS_IN_PLOTS]
                },{
                    'id': QualityRuleEnum.Polygon.OVERLAPS_IN_BUILDINGS,
                    'text': translated_strings[QualityRuleEnum.Polygon.OVERLAPS_IN_BUILDINGS]
                },{
                    'id': QualityRuleEnum.Polygon.OVERLAPS_IN_RIGHTS_OF_WAY,
                    'text': translated_strings[QualityRuleEnum.Polygon.OVERLAPS_IN_RIGHTS_OF_WAY]
                },{
                    'id': QualityRuleEnum.Polygon.PLOTS_COVERED_BY_BOUNDARIES,
                    'text': translated_strings[QualityRuleEnum.Polygon.PLOTS_COVERED_BY_BOUNDARIES]
                #}, {
                #    'id': 'check_missing_survey_points_in_buildings',
                #    'text': QCoreApplication.translate("QualityDialog", "Buildings nodes should be covered by Survey Points")
                }, {
                    'id': QualityRuleEnum.Polygon.RIGHT_OF_WAY_OVERLAPS_BUILDINGS,
                    'text': translated_strings[QualityRuleEnum.Polygon.RIGHT_OF_WAY_OVERLAPS_BUILDINGS]
                }, {
                    'id': QualityRuleEnum.Polygon.GAPS_IN_PLOTS,
                    'text': translated_strings[QualityRuleEnum.Polygon.GAPS_IN_PLOTS]
                }, {
                    'id': QualityRuleEnum.Polygon.MULTIPART_IN_RIGHT_OF_WAY,
                    'text': translated_strings[QualityRuleEnum.Polygon.MULTIPART_IN_RIGHT_OF_WAY]
                }, {
                    'id': QualityRuleEnum.Polygon.PLOT_NODES_COVERED_BY_BOUNDARY_POINTS,
                    'text': translated_strings[QualityRuleEnum.Polygon.PLOT_NODES_COVERED_BY_BOUNDARY_POINTS]
                },{
                    'id': QualityRuleEnum.Polygon.BUILDINGS_SHOULD_BE_WITHIN_PLOTS,
                    'text': translated_strings[QualityRuleEnum.Polygon.BUILDINGS_SHOULD_BE_WITHIN_PLOTS]
                },{
                    'id': QualityRuleEnum.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_PLOTS,
                    'text': translated_strings[QualityRuleEnum.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_PLOTS]
                }]
            }

        self.items_dict[QCoreApplication.translate("QualityDialog", "Logic consistency rules")] = {
                'icon': 'tables',
                'rules': [{
                    'id': QualityRuleEnum.Logic.PARCEL_RIGHT_RELATIONSHIP,
                    'text': translated_strings[QualityRuleEnum.Logic.PARCEL_RIGHT_RELATIONSHIP]
                }, {
                    'id': QualityRuleEnum.Logic.DUPLICATE_RECORDS_IN_A_TABLE,
                    'text': translated_strings[QualityRuleEnum.Logic.DUPLICATE_RECORDS_IN_A_TABLE]
                }, {
                    'id': QualityRuleEnum.Logic.FRACTION_SUM_FOR_PARTY_GROUPS,
                    'text': translated_strings[QualityRuleEnum.Logic.FRACTION_SUM_FOR_PARTY_GROUPS]
                }, {
                    'id': QualityRuleEnum.Logic.DEPARTMENT_CODE_HAS_TWO_NUMERICAL_CHARACTERS,
                    'text': translated_strings[QualityRuleEnum.Logic.DEPARTMENT_CODE_HAS_TWO_NUMERICAL_CHARACTERS]
                }, {
                    'id': QualityRuleEnum.Logic.MUNICIPALITY_CODE_HAS_THREE_NUMERICAL_CHARACTERS,
                    'text': translated_strings[QualityRuleEnum.Logic.MUNICIPALITY_CODE_HAS_THREE_NUMERICAL_CHARACTERS]
                }, {
                    'id': QualityRuleEnum.Logic.PARCEL_NUMBER_HAS_30_NUMERICAL_CHARACTERS,
                    'text': translated_strings[QualityRuleEnum.Logic.PARCEL_NUMBER_HAS_30_NUMERICAL_CHARACTERS]
                }, {
                    'id': QualityRuleEnum.Logic.PARCEL_NUMBER_BEFORE_HAS_20_NUMERICAL_CHARACTERS,
                    'text': translated_strings[QualityRuleEnum.Logic.PARCEL_NUMBER_BEFORE_HAS_20_NUMERICAL_CHARACTERS]
                }, {
                    'id': QualityRuleEnum.Logic.COL_PARTY_NATURAL_TYPE,
                    'text': translated_strings[QualityRuleEnum.Logic.COL_PARTY_NATURAL_TYPE]
                }, {
                    'id': QualityRuleEnum.Logic.COL_PARTY_NOT_NATURAL_TYPE,
                    'text': translated_strings[QualityRuleEnum.Logic.COL_PARTY_NOT_NATURAL_TYPE]
                }, {
                    'id': QualityRuleEnum.Logic.PARCEL_TYPE_AND_22_POSITION_OF_PARCEL_NUMBER,
                    'text': translated_strings[QualityRuleEnum.Logic.PARCEL_TYPE_AND_22_POSITION_OF_PARCEL_NUMBER]
                }, {
                    'id': QualityRuleEnum.Logic.UEBAUNIT_PARCEL,
                    'text': translated_strings[QualityRuleEnum.Logic.UEBAUNIT_PARCEL]
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
        translated_strings = self.translatable_config_strings.get_translatable_config_strings()
        # NOTE: Do not remove the named parameters, this is needed for making a decorator that thinks they are
        # optional happy!
        # POINTS QUALITY RULES
        if id == QualityRuleEnum.Point.OVERLAPS_IN_BOUNDARY_POINTS:
            result = self.facade_quality_rules.validate_overlaps_in_boundary_points(self._db, point_layer_name=self.names.OP_BOUNDARY_POINT_T)
        elif id == QualityRuleEnum.Point.OVERLAPS_IN_CONTROL_POINTS:
            result = self.facade_quality_rules.validate_overlaps_in_control_points(self._db, point_layer_name=self.names.OP_CONTROL_POINT_T)
        elif id == QualityRuleEnum.Point.BOUNDARY_POINTS_COVERED_BY_BOUNDARY_NODES:
            result = self.facade_quality_rules.validate_boundary_points_covered_by_boundary_nodes(self._db)
        elif id == QualityRuleEnum.Point.BOUNDARY_POINTS_COVERED_BY_PLOT_NODES:
            result = self.facade_quality_rules.validate_boundary_points_covered_by_plot_nodes(self._db)
        # LINES QUALITY RULES
        elif id == QualityRuleEnum.Line.OVERLAPS_IN_BOUNDARIES:
            result = self.facade_quality_rules.validate_overlaps_in_boundaries(self._db)
        elif id == QualityRuleEnum.Line.BOUNDARIES_ARE_NOT_SPLIT:
            result = self.facade_quality_rules.validate_boundaries_are_not_split(self._db)
        elif id == QualityRuleEnum.Line.BOUNDARIES_COVERED_BY_PLOTS:
            result = self.facade_quality_rules.validate_boundaries_covered_by_plots(self._db)
        elif id == QualityRuleEnum.Line.BOUNDARY_NODES_COVERED_BY_BOUNDARY_POINTS:
            result = self.facade_quality_rules.validate_boundary_nodes_covered_by_boundary_points(self._db)
        elif id == QualityRuleEnum.Line.DANGLES_IN_BOUNDARIES:
            result = self.facade_quality_rules.validate_dangles_in_boundaries(self._db)
        # POLYGONS QUALITY RULES
        elif id == QualityRuleEnum.Polygon.OVERLAPS_IN_PLOTS:
            result = self.facade_quality_rules.validate_overlaps_in_plots(self._db, self.names.OP_PLOT_T)
        elif id == QualityRuleEnum.Polygon.OVERLAPS_IN_BUILDINGS:
            result = self.facade_quality_rules.validate_overlaps_in_buildings(self._db, self.names.OP_BUILDING_T)
        elif id == QualityRuleEnum.Polygon.OVERLAPS_IN_RIGHTS_OF_WAY:
            result = self.facade_quality_rules.validate_overlaps_in_rights_of_way(self._db, self.names.OP_RIGHT_OF_WAY_T)
        elif id == QualityRuleEnum.Polygon.PLOTS_COVERED_BY_BOUNDARIES:
            result = self.facade_quality_rules.validate_plots_covered_by_boundaries(self._db)
        # elif id == 'check_missing_survey_points_in_buildings':
        #    self.facade_quality_rules.check_missing_survey_points_in_buildings(self._db)
        elif id == QualityRuleEnum.Polygon.RIGHT_OF_WAY_OVERLAPS_BUILDINGS:
            result = self.facade_quality_rules.validate_right_of_way_overlaps_buildings(self._db)
        elif id == QualityRuleEnum.Polygon.GAPS_IN_PLOTS:
            result = self.facade_quality_rules.validate_gaps_in_plots(self._db)
        elif id == QualityRuleEnum.Polygon.MULTIPART_IN_RIGHT_OF_WAY:
            result = self.facade_quality_rules.validate_multipart_in_right_of_way(self._db)
        elif id == QualityRuleEnum.Polygon.PLOT_NODES_COVERED_BY_BOUNDARY_POINTS:
            result = self.facade_quality_rules.validate_plot_nodes_covered_by_boundary_points(self._db)
        elif id == QualityRuleEnum.Polygon.BUILDINGS_SHOULD_BE_WITHIN_PLOTS:
            result = self.facade_quality_rules.validate_buildings_should_be_within_plots(self._db)
        elif id == QualityRuleEnum.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_PLOTS:
            result = self.facade_quality_rules.validate_building_units_should_be_within_plots(self._db)
        # LOGIC QUALITY RULES
        elif id == QualityRuleEnum.Logic.PARCEL_RIGHT_RELATIONSHIP:
            result = self.facade_quality_rules.validate_parcel_right_relationship(self._db, self._query_manager)
        elif id == QualityRuleEnum.Logic.DUPLICATE_RECORDS_IN_A_TABLE:

            # Check a predifene list of tables   list of define table with
            logic_consistency_tables = LayerConfig.get_logic_consistency_tables(self._db.names)
            for table in logic_consistency_tables:
                fields = logic_consistency_tables[table]
                result = self.facade_quality_rules.validate_duplicate_records_in_a_table(self._db, self._query_manager, table, fields)
                self.log_message(result[0], result[1])  # message, Qgis::MessageLevel

        elif id == QualityRuleEnum.Logic.FRACTION_SUM_FOR_PARTY_GROUPS:
            result = self.facade_quality_rules.validate_fraction_sum_for_party_groups(self._db, self._query_manager)
        elif id == QualityRuleEnum.Logic.DEPARTMENT_CODE_HAS_TWO_NUMERICAL_CHARACTERS:
            result = self.facade_quality_rules.validate_department_code_has_two_numerical_characters(self._db, self._query_manager)
        elif id == QualityRuleEnum.Logic.MUNICIPALITY_CODE_HAS_THREE_NUMERICAL_CHARACTERS:
            result = self.facade_quality_rules.validate_municipality_code_has_three_numerical_characters(self._db, self._query_manager)
        elif id == QualityRuleEnum.Logic.PARCEL_NUMBER_HAS_30_NUMERICAL_CHARACTERS:
            result = self.facade_quality_rules.validate_parcel_number_has_30_numerical_characters(self._db, self._query_manager)
        elif id == QualityRuleEnum.Logic.PARCEL_NUMBER_BEFORE_HAS_20_NUMERICAL_CHARACTERS:
            result = self.facade_quality_rules.validate_parcel_number_before_has_20_numerical_characters(self._db, self._query_manager)
        elif id == QualityRuleEnum.Logic.COL_PARTY_NATURAL_TYPE:
            result = self.facade_quality_rules.validate_col_party_natural_type(self._db, self._query_manager)
        elif id == QualityRuleEnum.Logic.COL_PARTY_NOT_NATURAL_TYPE:
            result = self.facade_quality_rules.validate_col_party_no_natural_type(self._db, self._query_manager)
        elif id == QualityRuleEnum.Logic.PARCEL_TYPE_AND_22_POSITION_OF_PARCEL_NUMBER:
            result = self.facade_quality_rules.validate_parcel_type_and_22_position_of_parcel_number(self._db, self._query_manager)
        elif id == QualityRuleEnum.Logic.UEBAUNIT_PARCEL:
            result = self.facade_quality_rules.validate_uebaunit_parcel(self._db, self._query_manager)

        # It does not apply for duplicate table records because it was done before
        if id != QualityRuleEnum.Logic.DUPLICATE_RECORDS_IN_A_TABLE:
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
        self.qgis_utils.show_help("quality_rules")
