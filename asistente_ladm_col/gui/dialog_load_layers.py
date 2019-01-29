# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-03-08
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

from qgis.PyQt.QtCore import (Qt,
                              QSettings,
                              QCoreApplication)
from qgis.PyQt.QtGui import (QBrush,
                             QFont,
                             QIcon)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QTreeWidgetItem,
                                 QLineEdit,
                                 QTreeWidgetItemIterator,
                                 QComboBox)
from qgis.core import QgsWkbTypes

from ..config.general_config import (TABLE_NAME,
                                     GEOMETRY_COLUMN,
                                     GEOMETRY_TYPE,
                                     KIND_SETTINGS,
                                     TABLE_ALIAS,
                                     MODEL)
from ..config.layer_sets import LAYER_SETS
from ..config.table_mapping_config import (TABLE_PROP_ASSOCIATION,
                                           TABLE_PROP_DOMAIN,
                                           TABLE_PROP_STRUCTURE)
from ..utils import get_ui_class
from ..resources_rc import *

DIALOG_UI = get_ui_class('dlg_load_layers.ui')

class DialogLoadLayers(QDialog, DIALOG_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self._db = db
        self.qgis_utils = qgis_utils
        self.models_tree = dict()
        self.selected_items_dict = dict()
        self.icon_names = ['points', 'lines', 'polygons', 'tables', 'domains', 'structures', 'associations']

        self.txt_search_text.addAction(QIcon(":/Asistente-LADM_COL/resources/images/search.png"), QLineEdit.LeadingPosition)

        # Fill predefined tables combobox
        self.cbo_select_predefined_tables.clear()
        self.cbo_select_predefined_tables.setInsertPolicy(QComboBox.InsertAlphabetically)
        self.cbo_select_predefined_tables.addItem("", []) # By default

        for name, layer_list in LAYER_SETS.items():
            self.cbo_select_predefined_tables.addItem(name, layer_list)

        self.cbo_select_predefined_tables.currentIndexChanged.connect(self.select_predefined_changed)

        # Set connections
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.rejected)
        self.buttonBox.helpRequested.connect(self.show_help)
        self.txt_search_text.textChanged.connect(self.search_text_changed)
        self.chk_show_domains.toggled.connect(self.show_table_type_changed)
        self.chk_show_structures.toggled.connect(self.show_table_type_changed)
        self.chk_show_associations.toggled.connect(self.show_table_type_changed)
        self.trw_layers.itemSelectionChanged.connect(self.selection_changed)

        # Reload latest settings
        self.restore_settings()

        # Load layers from the db
        self.load_available_layers()

    def load_available_layers(self):
        # Call qgis model baker tables_info and fill the tree
        tables_info = self.qgis_utils._layers
        self.models_tree = dict()

        for record in tables_info:
            if record[MODEL] is not None:
                if record[MODEL] not in self.models_tree:
                    self.models_tree[record[MODEL]] = {
                        record[TABLE_ALIAS] or record[TABLE_NAME]: record}
                else:
                    if (record[TABLE_ALIAS] or record[TABLE_NAME]) in self.models_tree[record[MODEL]]: # Multiple geometry columns
                        # First geometry
                        tmp_record = self.models_tree[record[MODEL]][record[TABLE_ALIAS] or record[TABLE_NAME]]
                        del self.models_tree[record[MODEL]][record[TABLE_ALIAS] or record[TABLE_NAME]]
                        tmp_name = "{} ({})".format((tmp_record[TABLE_ALIAS] or tmp_record[TABLE_NAME]), tmp_record[GEOMETRY_COLUMN])
                        self.models_tree[record[MODEL]][tmp_name] = tmp_record

                        # Second geometry
                        tmp_name = "{} ({})".format((record[TABLE_ALIAS] or record[TABLE_NAME]), record[GEOMETRY_COLUMN])
                        self.models_tree[record[MODEL]][tmp_name] = record
                    else:
                        self.models_tree[record[MODEL]][record[TABLE_ALIAS] or record[TABLE_NAME]] = record

        self.update_available_layers()

    def update_available_layers(self):
        self.trw_layers.setUpdatesEnabled(False) # Don't render until we're ready

        # Grab some context data
        show_domains = self.chk_show_domains.isChecked()
        show_structures = self.chk_show_structures.isChecked()
        show_associations = self.chk_show_associations.isChecked()
        top_level_items_expanded_info = []
        for i in range(self.trw_layers.topLevelItemCount()):
            top_level_items_expanded_info.append(self.trw_layers.topLevelItem(i).isExpanded())

        # Save selection
        self.update_selected_items()

        # Iterate models adding children
        self.trw_layers.blockSignals(True) # We don't want to get itemSelectionChanged here
        self.trw_layers.clear()
        self.trw_layers.blockSignals(False)

        sorted_models = sorted(self.models_tree.keys())
        for model in sorted_models:
            children = []
            model_item = QTreeWidgetItem([model])

            # Filter by search text
            list_tables = self.filter_tables_by_search_text(self.models_tree[model].keys(), self.txt_search_text.text())
            sorted_tables = sorted(list_tables)

            for table in sorted_tables:
                current_table_info = self.models_tree[model][table]
                if current_table_info[KIND_SETTINGS] == TABLE_PROP_DOMAIN and not show_domains \
                   or current_table_info[KIND_SETTINGS] == TABLE_PROP_STRUCTURE and not show_structures \
                   or current_table_info[KIND_SETTINGS] == TABLE_PROP_ASSOCIATION and not show_associations:
                    continue

                table_item = QTreeWidgetItem([table])
                table_item.setData(0, Qt.UserRole, self.models_tree[model][table])
                geometry_type = QgsWkbTypes().geometryType(QgsWkbTypes().parseType(current_table_info[GEOMETRY_TYPE])) if current_table_info[GEOMETRY_TYPE] else None
                icon_name = self.icon_names[3 if geometry_type is None else geometry_type]

                # Is the layer already loaded?
                if self.qgis_utils.get_layer_from_layer_tree(current_table_info[TABLE_NAME],
                         self._db.schema,
                         geometry_type) is not None:
                    table_item.setText(0, table + QCoreApplication.translate("DialogLoadLayers",
                                               " [already loaded]"))
                    table_item.setData(0, Qt.ForegroundRole, QBrush(Qt.lightGray))
                    table_item.setFlags(Qt.ItemIsEnabled) # Not selectable
                else: # Laye not in QGIS Layer Tree
                    if not current_table_info[KIND_SETTINGS]: # This is a class
                        font = QFont()
                        font.setBold(True)
                        table_item.setData(0, Qt.FontRole, font)

                if current_table_info[KIND_SETTINGS] == TABLE_PROP_DOMAIN:
                    icon_name = self.icon_names[4]
                elif current_table_info[KIND_SETTINGS] == TABLE_PROP_STRUCTURE:
                    icon_name = self.icon_names[5]
                elif current_table_info[KIND_SETTINGS] == TABLE_PROP_ASSOCIATION:
                    icon_name = self.icon_names[6]
                icon = QIcon(":/Asistente-LADM_COL/resources/images/{}.png".format(icon_name))
                table_item.setData(0, Qt.DecorationRole, icon)

                children.append(table_item)

            model_item.addChildren(children)
            self.trw_layers.addTopLevelItem(model_item)

        # Set selection
        iterator = QTreeWidgetItemIterator(self.trw_layers, QTreeWidgetItemIterator.Selectable)
        self.trw_layers.blockSignals(True) # We don't want to get itemSelectionChanged here
        while iterator.value():
            item = iterator.value()
            if item.text(0) in self.selected_items_dict:
                item.setSelected(True)

            iterator += 1

        self.trw_layers.blockSignals(False)

        # Make model items non selectable
        # Set expand taking previous states into account
        for i in range(self.trw_layers.topLevelItemCount()):
            self.trw_layers.topLevelItem(i).setFlags(Qt.ItemIsEnabled) # Not selectable
            self.trw_layers.topLevelItem(i).setExpanded(top_level_items_expanded_info[i] if top_level_items_expanded_info else True)

        self.trw_layers.setUpdatesEnabled(True) # Now render!

    def filter_tables_by_search_text(self, list_tables, search_text):
        res = list(list_tables)[:]
        search_text = search_text.lower()
        if search_text:
            if len(search_text) == 1:
                for table in list_tables:
                    if not table.lower().startswith(search_text):
                        res.remove(table)
            elif len(search_text) > 1:
                for table in list_tables:
                    if search_text not in table.lower():
                        res.remove(table)

        return res

    def update_selected_items(self):
        iterator = QTreeWidgetItemIterator(self.trw_layers, QTreeWidgetItemIterator.Selectable)
        while iterator.value():
            item = iterator.value()

            if item.isSelected():
                self.selected_items_dict[item.text(0)] = item.data(0, Qt.UserRole)
            else:
                if item.text(0) in self.selected_items_dict:
                    # It was selected before, but not anymore
                    del self.selected_items_dict[item.text(0)]

            iterator += 1

    def search_text_changed(self, text):
        self.update_available_layers()

    def show_table_type_changed(self, state):
        self.update_available_layers()

    def accepted(self):
        self.save_settings()
        self.update_selected_items() # Take latest selection into account

        if len(self.selected_items_dict):
            # Load selected layers
            layers_dict = {}
            for item_text, data in self.selected_items_dict.items():
                layers_dict[item_text] = {
                    'name': data[TABLE_NAME],
                    'geometry': QgsWkbTypes().geometryType(QgsWkbTypes().parseType(data[GEOMETRY_TYPE])) if data[GEOMETRY_TYPE] else None
                }

            self.selected_items_dict = dict() # Reset
            self.qgis_utils.get_layers(self._db, layers_dict, load=True)

    def rejected(self):
        self.selected_items_dict = dict()

    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/load_layers_dialog/show_domains', self.chk_show_domains.isChecked())
        settings.setValue('Asistente-LADM_COL/load_layers_dialog/show_structures', self.chk_show_structures.isChecked())
        settings.setValue('Asistente-LADM_COL/load_layers_dialog/show_associations', self.chk_show_associations.isChecked())

    def restore_settings(self):
        settings = QSettings()
        self.chk_show_domains.setChecked(settings.value('Asistente-LADM_COL/load_layers_dialog/show_domains', False, bool))
        self.chk_show_structures.setChecked(settings.value('Asistente-LADM_COL/load_layers_dialog/show_structures', False, bool))
        self.chk_show_associations.setChecked(settings.value('Asistente-LADM_COL/load_layers_dialog/show_associations', False, bool))

    def select_predefined_changed(self, index):
        layer_list = self.cbo_select_predefined_tables.currentData()

        # Clear layer selection
        self.trw_layers.blockSignals(True) # We don't want to get itemSelectionChanged here
        self.trw_layers.clearSelection()
        self.trw_layers.blockSignals(False)
        self.selected_items_dict = dict()

        # First find corresponding unique names in tree, since for
        # tables with multiple geometry columns, the tree has as much
        # tables as geometry columns are, but the table name is the same
        select_layers_list = list()
        for model, tables in self.models_tree.items():
            for table_name_in_tree, record in tables.items():
                if record[TABLE_NAME] in layer_list:
                    select_layers_list.append(table_name_in_tree)
                    self.selected_items_dict[table_name_in_tree] = record

        self.update_selected_count_label()

        # Select predefined layers in the view (some layers might not be visible)
        if select_layers_list:
            self.trw_layers.blockSignals(True) # We don't want to get itemSelectionChanged here
            count = len(select_layers_list) # We can stop before iterating all layers
            iterator = QTreeWidgetItemIterator(self.trw_layers, QTreeWidgetItemIterator.Selectable)
            while iterator.value():
                item = iterator.value()
                if item.text(0) in select_layers_list:
                    item.setSelected(True)
                    count -= 1
                    if count == 0:
                        break

                iterator += 1

            self.trw_layers.blockSignals(False)

    def update_selected_count_label(self):
        selected_count = len(self.selected_items_dict)
        if selected_count == 0:
            text = QCoreApplication.translate("DialogLoadLayers",
                        "There are no selected layers to load")
        elif selected_count == 1:
            text = QCoreApplication.translate("DialogLoadLayers",
                        "There is 1 selected layer ready to be loaded")
        else:
            text = QCoreApplication.translate("DialogLoadLayers",
                        "There are {} selected layers ready to be loaded").format(selected_count)

        self.lbl_selected_count.setText(text)

    def selection_changed(self):
        # Update internal dict and dialog label
        self.update_selected_items()
        self.update_selected_count_label()

    def show_help(self):
        self.qgis_utils.show_help("load_layers")
