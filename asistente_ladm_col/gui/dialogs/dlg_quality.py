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
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import (QBrush,
                             QFont,
                             QIcon,
                             QColor)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QDialogButtonBox,
                                 QTreeWidgetItem,
                                 QTreeWidgetItemIterator)

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.enums import EnumQualityRule
from asistente_ladm_col.logic.quality.quality_rules import QualityRules

from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.utils import show_plugin_help
from asistente_ladm_col.lib.quality_rule.quality_rule_manager import QualityRuleManager
from asistente_ladm_col.lib.logger import Logger

DIALOG_UI = get_ui_class('dialogs/dlg_quality.ui')


class QualityDialog(QDialog, DIALOG_UI):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.quality_rules_manager = QualityRuleManager()
        self.quality_rules = QualityRules()
        self.log_dialog_quality_text = ""
        self.log_dialog_quality_text_content = ""
        self.log_quality_validation_total_time = 0

        self.app = AppInterface()

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
        for group_key, rules in self.quality_rules_manager.get_quality_rules_by_group().items():
            group_name = self.quality_rules_manager.get_quality_rule_group_name(group_key)
            self.items_dict[group_name] = {
                'rules': [{'id': k_rule, 'text': v_rule.rule_name} for k_rule, v_rule in rules.items()]
            }
            if group_key == EnumQualityRule.Point:
                self.items_dict[group_name]['icon'] = 'points'
            elif group_key == EnumQualityRule.Line:
                self.items_dict[group_name]['icon'] = 'lines'
            elif group_key == EnumQualityRule.Polygon:
                self.items_dict[group_name]['icon'] = 'polygons'
            elif group_key == EnumQualityRule.Logic:
                self.items_dict[group_name]['icon'] = 'tables'

        self.load_items()

        self.selected_rules = list()

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
            icon = QIcon(":/Asistente-LADM-COL/resources/images/{}.png".format(items['icon']))
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
        self.app.gui.remove_error_group()

        iterator = QTreeWidgetItemIterator(self.trw_quality_rules, QTreeWidgetItemIterator.Selectable)
        while iterator.value():
            item = iterator.value()
            if item.isSelected():
                self.selected_rules.append(item.data(0, Qt.UserRole))
            iterator += 1

    def rejected(self):
        pass

    def select_all(self):
        self.trw_quality_rules.selectAll()

    def clear_selection(self):
        self.trw_quality_rules.clearSelection()

    def show_help(self):
        show_plugin_help("quality_rules")
