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
import os

from qgis.core import QgsProject, QgsVectorLayer, Qgis, QgsWkbTypes
from qgis.gui import QgsMessageBar
from qgis.PyQt.QtCore import Qt, QSettings, QCoreApplication
from qgis.PyQt.QtGui import QBrush, QFont, QIcon
from qgis.PyQt.QtWidgets import (QAction, QDialog, QTreeWidgetItem, QLineEdit,
                                 QTreeWidgetItemIterator)

from ..config.table_mapping_config import (
    TABLE_PROP_ASSOCIATION,
    TABLE_PROP_DOMAIN,
    TABLE_PROP_STRUCTURE
)
from ..lib.dbconnector.gpkg_connector import GPKGConnector
from ..lib.dbconnector.pg_connector import PGConnector
from ..utils import get_ui_class
from ..utils.project_generator_utils import ProjectGeneratorUtils
from ..utils.qt_utils import make_file_selector

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
        self.selected_items = dict()
        self.project_generator_utils = ProjectGeneratorUtils()
        self.icon_names = ['points', 'lines', 'polygons', 'tables', 'domains', 'structures', 'associations']

        self.cbo_select_predefined_tables.clear()
        self.cbo_select_predefined_tables.addItem(self.tr('Spatial data'), 'spatial_data')
        self.cbo_select_predefined_tables.addItem(self.tr('Legal data'), 'legal_data')
        self.cbo_select_predefined_tables.currentIndexChanged.connect(self.select_predefined_changed)
        self.txt_search_text.addAction(QIcon(":/Asistente-LADM_COL/images/search.png"), QLineEdit.LeadingPosition)

        # Load layers from the db
        self.load_available_layers()

        # Set connections
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.rejected)
        self.txt_search_text.textChanged.connect(self.search_text_changed)
        self.chk_show_domains.toggled.connect(self.show_table_type_changed)
        self.chk_show_structures.toggled.connect(self.show_table_type_changed)
        self.chk_show_associations.toggled.connect(self.show_table_type_changed)

        # Trigger some default behaviours
        self.restore_settings()

    def load_available_layers(self):
        # Call project generator tables_info and fill the layer tree
        tables_info = self.project_generator_utils.get_tables_info_without_ignored_tables(self._db)
        self.models_tree = dict()
        for record in tables_info:
            if record['model'] not in self.models_tree:
                self.models_tree[record['model']] = {
                    record['table_alias'] or record['tablename']: record}
            else:
                if (record['table_alias'] or record['tablename']) in self.models_tree[record['model']]: # Multiple geometry columns
                    # First geometry
                    tmp_record = self.models_tree[record['model']][record['table_alias'] or record['tablename']]
                    del self.models_tree[record['model']][record['table_alias'] or record['tablename']]
                    tmp_name = "{} ({})".format((tmp_record['table_alias'] or tmp_record['tablename']), tmp_record['geometry_column'])
                    self.models_tree[record['model']][tmp_name] = tmp_record

                    # Second geometry
                    tmp_name = "{} ({})".format((record['table_alias'] or record['tablename']), record['geometry_column'])
                    self.models_tree[record['model']][tmp_name] = record
                else:
                    self.models_tree[record['model']][record['table_alias'] or record['tablename']] = record

        self.update_available_layers()

    def update_available_layers(self):
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
        self.trw_layers.clear()
        sorted_models = sorted(self.models_tree.keys())
        for model in sorted_models:
            children = []
            model_item = QTreeWidgetItem([model])

            # Filter by search text
            list_tables = self.filter_tables_by_search_text(self.models_tree[model].keys(), self.txt_search_text.text())
            sorted_tables = sorted(list_tables)

            for table in sorted_tables:
                current_table_info = self.models_tree[model][table]
                if current_table_info['is_domain'] == TABLE_PROP_DOMAIN and not show_domains \
                   or current_table_info['is_domain'] == TABLE_PROP_STRUCTURE and not show_structures \
                   or current_table_info['is_domain'] == TABLE_PROP_ASSOCIATION and not show_associations:
                    continue

                table_item = QTreeWidgetItem([table])
                table_item.setData(0, Qt.UserRole, self.models_tree[model][table])
                geometry_type = QgsWkbTypes().geometryType(QgsWkbTypes().parseType(current_table_info['type'])) if current_table_info['type'] else None
                icon_name = self.icon_names[3 if geometry_type is None else geometry_type]

                # Is the layer already loaded?
                if self.qgis_utils.get_layer_from_layer_tree(current_table_info['tablename'],
                         self._db.schema,
                         geometry_type) is not None:
                    table_item.setText(0, table + QCoreApplication.translate("DialogLoadLayers",
                                               " [already loaded]"))
                    table_item.setData(0, Qt.ForegroundRole, QBrush(Qt.lightGray))
                    table_item.setFlags(Qt.ItemIsEnabled) # Not selectable
                else: # Laye not in QGIS Layer Tree
                    if not current_table_info['is_domain']: # This is a class
                        font = QFont()
                        font.setBold(True)
                        table_item.setData(0, Qt.FontRole, font)

                if current_table_info['is_domain'] == TABLE_PROP_DOMAIN:
                    icon_name = self.icon_names[4]
                elif current_table_info['is_domain'] == TABLE_PROP_STRUCTURE:
                    icon_name = self.icon_names[5]
                elif current_table_info['is_domain'] == TABLE_PROP_ASSOCIATION:
                    icon_name = self.icon_names[6]
                icon = QIcon(":/Asistente-LADM_COL/images/{}.png".format(icon_name))
                table_item.setData(0, Qt.DecorationRole, icon)

                children.append(table_item)

            model_item.addChildren(children)
            self.trw_layers.addTopLevelItem(model_item)

        # Set selection
        iterator = QTreeWidgetItemIterator(self.trw_layers, QTreeWidgetItemIterator.Selectable)
        while iterator.value():
            item = iterator.value()
            if item.text(0) in self.selected_items:
                item.setSelected(True)

            iterator += 1

        # Make mode items non selectable
        # Set expand taking previous states into account
        for i in range(self.trw_layers.topLevelItemCount()):
            self.trw_layers.topLevelItem(i).setFlags(Qt.ItemIsEnabled) # Not selectable
            self.trw_layers.topLevelItem(i).setExpanded(top_level_items_expanded_info[i] if top_level_items_expanded_info else True)

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
                self.selected_items[item.text(0)] = item.data(0, Qt.UserRole)
            else:
                if item.text(0) in self.selected_items:
                    # It was selected before, but not anymore
                    del self.selected_items[item.text(0)]

            iterator += 1

    def search_text_changed(self, text):
        self.update_available_layers()

    def show_table_type_changed(self, state):
        self.update_available_layers()

    def accepted(self):
        self.save_settings()
        self.update_selected_items() # Take latest selection into account

        # Load selected layers
        layers_dict = {}
        for item_text, data in self.selected_items.items():
            layers_dict[data['tablename']] = {'name': data['tablename'], 'geometry': None}

        self.selected_items = dict() # Reset
        self.qgis_utils.get_layers(self._db, layers_dict, load=True)

    def rejected(self):
        self.selected_items = dict()

    def save_settings(self):
        # Save QSettings
        # settings = QSettings(
        pass

    def restore_settings(self):
        # Restore QSettings
        # settings = QSettings()
        pass

    def select_predefined_changed(self):
        pass
