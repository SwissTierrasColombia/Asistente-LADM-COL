"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin           : 2022-01-18
        git sha         : :%H$
        copyright       : (C) 2022 by Germán Carrillo (SwissTierras Colombia)
        email           : gcarrillo@linuxmail.org
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from functools import partial

from PyQt5.uic import loadUi
from qgis.PyQt.QtGui import (QFont,
                             QIcon)
from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication)
from qgis.PyQt.QtWidgets import (QTreeWidgetItem,
                                 QLineEdit,
                                 QTreeWidgetItemIterator,
                                 QComboBox,
                                 QHeaderView,
                                 QLabel)
from qgis.core import Qgis
from qgis.gui import QgsPanelWidget

from asistente_ladm_col.gui.transitional_system.tasks_widget import TasksWidget
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.transitional_system.st_session.st_session import STSession
from asistente_ladm_col.utils.ui import (get_ui_class,
                                         get_ui_file_path)
from asistente_ladm_col.utils.utils import show_plugin_help

WIDGET_UI = get_ui_class('quality_rules/quality_rules_general_results_panel_widget.ui')
QR_COLUMN = 0
RESULT_COLUMN = 1


class QualityRulesGeneralResultsPanelWidget(QgsPanelWidget, WIDGET_UI):

    def __init__(self, controller, parent=None):
        QgsPanelWidget.__init__(self, parent)
        self.setupUi(self)
        self.__controller = controller
        self.parent = parent
        self.logger = Logger()

        self.__selected_item = None  # qr_key
        self.__icon_names = ['schema.png', 'points.png', 'lines.png', 'polygons.png', 'relationships.svg']

        self.txt_search.addAction(QIcon(":/Asistente-LADM-COL/resources/images/search.png"), QLineEdit.LeadingPosition)

        self.setDockMode(True)
        self.setPanelTitle(QCoreApplication.translate("QualityRulesGeneralResultsPanelWidget", "Validation results"))
        self.trw_qrs.header().setStretchLastSection(False)
        self.trw_qrs.setColumnWidth(RESULT_COLUMN, 50)
        self.trw_qrs.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.pbr_total_progress.setValue(0)

        self.txt_search.textChanged.connect(self.__search_text_changed)
        self.btn_open_report.clicked.connect(self.__controller.open_report)
        #self.btn_save_gpkg.clicked.connect(self.__view_details_clicked)
        self.btn_view_details.clicked.connect(self.__view_details_clicked)
        self.btn_help.clicked.connect(self.__show_help)
        self.trw_qrs.itemSelectionChanged.connect(self.__selection_changed)

        # Load available rules for current role and current db models
        self.__load_available_rules()

    def __load_available_rules(self):
        self.__controller.load_general_results_tree_data()
        self.__update_available_rules()

    def __update_available_rules(self):
        self.trw_qrs.setUpdatesEnabled(False)  # Don't render until we're ready

        # Grab some context data
        top_level_items_expanded_info = dict()
        for i in range(self.trw_qrs.topLevelItemCount()):
            top_level_items_expanded_info[self.trw_qrs.topLevelItem(i).text(QR_COLUMN)] = self.trw_qrs.topLevelItem(i).isExpanded()

        # Save selection before clearing tree to restate it later (if needed)
        self.__update_selected_item()

        # Iterate qr types adding children
        self.trw_qrs.blockSignals(True)  # We don't want to get itemSelectionChanged here
        self.trw_qrs.clear()
        self.trw_qrs.blockSignals(False)

        bold_font = QFont()
        bold_font.setBold(True)

        sorted_types = sorted(self.__controller.get_general_results_tree_data().keys())
        for type_enum in sorted_types:
            type = type_enum.name  # Get the type text from the enum
            children = []
            type_item = QTreeWidgetItem([type])

            # Filter by search text
            list_qrs = self.__filter_by_search_text(type_enum, self.txt_search.text())

            for qr in list_qrs:
                qr_item = QTreeWidgetItem([qr.name(), ''])
                qr_item.setData(QR_COLUMN, Qt.UserRole, qr.id())
                qr_item.setData(QR_COLUMN, Qt.ToolTipRole, "{}\n{}".format(qr.name(), qr.id()))

                # Let's listen some QR's relevant signals to update our view when needed
                qr.progress_changed.connect(partial(self.__set_qr_progress, qr.id()))
                qr.validation_finished.connect(partial(self.__set_qr_validation_result, qr))

                children.append(qr_item)

            if children:
                icon_name = self.__icon_names[type_enum.value]
                icon = QIcon(":/Asistente-LADM-COL/resources/images/{}".format(icon_name))
                type_item.setData(0, Qt.DecorationRole, icon)
                type_item.setData(0, Qt.FontRole, bold_font)
                type_item.addChildren(children)
                self.trw_qrs.addTopLevelItem(type_item)

                # After we've set the children, we can set custom item widgets
                self.__set_children_custom_widget(type_enum, type_item, list_qrs)
            else:
                type_item = None

        # Set selection
        self.trw_qrs.blockSignals(True)  # We don't want to get itemSelectionChanged here
        item = self.__get_item_by_qr_key(self.__selected_item)
        if item:
            item.setSelected(True)
        self.trw_qrs.blockSignals(False)

        # Make type items non selectable
        # Set expand taking previous states into account
        for i in range(self.trw_qrs.topLevelItemCount()):
            self.trw_qrs.topLevelItem(i).setFlags(Qt.ItemIsEnabled)  # Not selectable
            self.trw_qrs.topLevelItem(i).setExpanded(
                top_level_items_expanded_info.get(self.trw_qrs.topLevelItem(i).text(QR_COLUMN), True))

        self.trw_qrs.setUpdatesEnabled(True)  # Now render!

    def __set_children_custom_widget(self, type_enum, type_item, filtered_qrs):
        dict_filtered_qrs = {qr.id(): qr for qr in filtered_qrs}
        for i in range(type_item.childCount()):
            item = type_item.child(i)
            qr_key = item.data(QR_COLUMN, Qt.UserRole)
            qr_result = self.__controller.get_general_results_tree_data()[type_enum][dict_filtered_qrs[qr_key]]
            self.__set_style_for_validation_result(item, qr_result)

    def __filter_by_search_text(self, type, search_text):
        res = list(self.__controller.get_general_results_tree_data()[type].keys())  # qr_objs

        search_text = search_text.lower().strip()
        if len(search_text) > 1:
            to_delete = list()
            for qr_obj in res:
                # First check in QR id
                found = search_text in qr_obj.id().lower()

                if not found:
                    # Now search in QR tags
                    for tag in qr_obj.tags():
                        if search_text in tag:
                            found = True
                            continue

                    if not found:
                        to_delete.append(qr_obj)

            for qr_obj in to_delete:
                res.remove(qr_obj)

        return res

    def __get_item_by_qr_key(self, qr_key):
        iterator = QTreeWidgetItemIterator(self.trw_qrs, QTreeWidgetItemIterator.Selectable)
        while iterator.value():
            item = iterator.value()
            if item.data(QR_COLUMN, Qt.UserRole) == qr_key:
                return item

            iterator += 1

        return None

    def __update_selected_item(self):
        self.__selected_item = None
        iterator = QTreeWidgetItemIterator(self.trw_qrs, QTreeWidgetItemIterator.Selectable)
        while iterator.value():
            item = iterator.value()
            qr_key = item.data(QR_COLUMN, Qt.UserRole)

            if item.isSelected():
                self.__selected_item = qr_key
                break

            iterator += 1

    def __search_text_changed(self, text):
        self.__update_available_rules()

    def __view_details_clicked(self):
        self.__save_settings()

        if self.trw_qrs.selectedItems():
            print(self.trw_qrs.selectedItems()[0].data(QR_COLUMN, Qt.UserRole))
            self.show_detailed_results_panel()

    def __save_settings(self):
        pass

    def __restore_settings(self):
        pass

    def __select_predefined_changed(self, index):
        pass

    def __selection_changed(self):
        self.__update_controls_after_selection_update()

    def __update_controls_after_selection_update(self):
        # Custom slot to refresh labels and button state
        self.btn_view_details.setEnabled(len(self.trw_qrs.selectedItems()))

    def __set_qr_progress(self, qr_key, value):
        item = self.__get_item_by_qr_key(qr_key)
        if item:
            self.trw_qrs.itemWidget(item, RESULT_COLUMN).setText("{}%".format(value))
            QCoreApplication.processEvents()

    def __set_qr_validation_result(self, qr, qr_result):
        self.__controller.set_qr_validation_result(qr, qr_result)
        item = self.__get_item_by_qr_key(qr.id())
        if item:
            self.__set_style_for_validation_result(item, qr_result)

    def __set_style_for_validation_result(self, item, qr_result):
        # Note this method considers when qr_result hasn't been set
        if qr_result:
            item.setData(RESULT_COLUMN, Qt.ToolTipRole, qr_result.msg)

        self.trw_qrs.setItemWidget(item, RESULT_COLUMN, self.__get_custom_widget_item_for_result(qr_result))

    def __get_custom_widget_item_for_result(self, qr_result):
        if not qr_result:
            backcolor = "#fcde87"
        elif qr_result.level == Qgis.Warning:
            backcolor = "red"
        elif qr_result.level == Qgis.Success:
            backcolor = "green"
        elif qr_result.level == Qgis.Critical:
            backcolor = "#d611ac"
        else:  # Qgis.NoLevel
            backcolor = "#949494"

        label = QLabel("0%" if not qr_result else "8")
        label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        label.setStyleSheet("QLabel{{background-color: {}; color {};}}".format(backcolor, "black"))

        return label

    def update_total_progress(self, value):
        self.pbr_total_progress.setValue(value)
        print("T:", value)

    def show_detailed_results_panel(self):
        """
        Slot called to show the task panel based on a selected task.

        :param task_id: Id of the task that will be used to show the task panel.
        """
        self.parent.show_detailed_results_panel()

    def __show_help(self):
        show_plugin_help("quality_rules")
