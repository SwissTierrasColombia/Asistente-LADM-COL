"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin           : 2022-01-13
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
import os.path

from PyQt5.uic import loadUi
from qgis.PyQt.QtGui import (QFont,
                             QIcon)
from qgis.PyQt.QtCore import (Qt,
                              pyqtSignal,
                              QCoreApplication)
from qgis.PyQt.QtWidgets import (QTreeWidgetItem,
                                 QLineEdit,
                                 QTreeWidgetItemIterator,
                                 QComboBox)
from qgis.gui import QgsPanelWidget

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.enums import EnumQualityRulePanelMode
from asistente_ladm_col.gui.transitional_system.tasks_widget import TasksWidget
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.transitional_system.st_session.st_session import STSession
from asistente_ladm_col.utils.qt_utils import (make_file_selector,
                                               make_folder_selector)
from asistente_ladm_col.utils.ui import (get_ui_class,
                                         get_ui_file_path)
from asistente_ladm_col.utils.utils import show_plugin_help

WIDGET_UI = get_ui_class('quality_rules/quality_rules_initial_panel_widget.ui')

TAB_VALIDATE_INDEX = 0
TAB_READ_INDEX = 1


class QualityRulesInitialPanelWidget(QgsPanelWidget, WIDGET_UI):

    def __init__(self, controller, parent=None):
        QgsPanelWidget.__init__(self, None)
        self.setupUi(self)
        self.__controller = controller
        self.parent = parent
        self.app = AppInterface()
        self.logger = Logger()
        self.__mode = EnumQualityRulePanelMode.VALIDATE

        self.__selected_items_list = list()
        self.__icon_names = ['schema.png', 'points.png', 'lines.png', 'polygons.png', 'relationships.svg']

        self.txt_search.addAction(QIcon(":/Asistente-LADM-COL/resources/images/search.png"), QLineEdit.LeadingPosition)

        self.setDockMode(True)
        self.setPanelTitle(QCoreApplication.translate("QualityRulesInitialPanelWidget", "Quality Rules"))

        self.__restore_settings()

        self.txt_search.textChanged.connect(self.__search_text_changed)
        self.btn_validate.clicked.connect(self.__validate_clicked)
        self.btn_read.clicked.connect(self.__read_clicked)
        self.btn_help.clicked.connect(self.__show_help)
        self.trw_qrs.itemSelectionChanged.connect(self.__selection_changed)
        self.tab.currentChanged.connect(self.__tab_changed)

        dir_selector = make_folder_selector(self.txt_dir_path,
                                            title=QCoreApplication.translate("QualityRulesInitialPanelWidget",
                                                                             "Select a folder to store quality errors"),
                                            parent=None,
                                            setting_property="qr_results_dir_path")
        self.btn_dir_path.clicked.connect(dir_selector)

        db_file_selector = make_file_selector(self.txt_db_path,
                                              title=QCoreApplication.translate("QualityRulesInitialPanelWidget",
                                                                               "Open GeoPackage database file with quality errors"),
                                              file_filter=QCoreApplication.translate("QualityRulesInitialPanelWidget",
                                                                                     "GeoPackage Database (*.gpkg)"),
                                              setting_property="qr_db_file_path")

        self.btn_db_path.clicked.connect(db_file_selector)

        self.__tab_changed(self.tab.currentIndex())  # Direct call to initialize controls

    def __tab_changed(self, index):
        self.__activate_mode(
            EnumQualityRulePanelMode.VALIDATE if index == TAB_VALIDATE_INDEX else EnumQualityRulePanelMode.READ)

    def __activate_mode(self, mode):
        self.__mode = mode
        validate_mode = mode == EnumQualityRulePanelMode.VALIDATE

        # First reset both search and selection
        self.txt_search.setText('')
        self.trw_qrs.clearSelection()
        self.__selected_items_list = list()

        self.trw_qrs.setEnabled(validate_mode)

        self.btn_validate.setVisible(validate_mode)
        self.lbl_selected_count.setVisible(validate_mode)
        self.btn_read.setVisible(not validate_mode)

        self.lbl_presets.setVisible(validate_mode)
        self.cbo_presets.setVisible(validate_mode)
        self.btn_save_selection.setVisible(validate_mode)
        self.btn_delete_selection.setVisible(validate_mode)

        # Load available rules for current role and current db models
        self.__load_available_rules()

    def __load_available_rules(self):
        self.__controller.load_tree_data(self.__mode)
        self.__update_available_rules()

    def __update_available_rules(self):
        self.trw_qrs.setUpdatesEnabled(False)  # Don't render until we're ready

        # Grab some context data
        top_level_items_expanded_info = dict()
        for i in range(self.trw_qrs.topLevelItemCount()):
            top_level_items_expanded_info[self.trw_qrs.topLevelItem(i).text(0)] = self.trw_qrs.topLevelItem(i).isExpanded()

        # Save selection
        self.__update_selected_items()

        # Iterate qr types adding children
        self.trw_qrs.blockSignals(True)  # We don't want to get itemSelectionChanged here
        self.trw_qrs.clear()
        self.trw_qrs.blockSignals(False)

        bold_font = QFont()
        bold_font.setBold(True)

        sorted_types = sorted(self.__controller.get_qrs_tree_data().keys())
        for type_enum in sorted_types:
            children = []
            type_item = QTreeWidgetItem([self.__controller.get_tr_string(type_enum)])

            # Filter by search text
            list_qrs = self.__filter_by_search_text(type_enum, self.txt_search.text())

            for qr in list_qrs:
                qr_item = QTreeWidgetItem([qr.name()])
                qr_item.setData(0, Qt.UserRole, qr.id())
                qr_item.setData(0, Qt.ToolTipRole, "{}\n{}".format(qr.name(), qr.id()))
                children.append(qr_item)

            if children:
                icon_name = self.__icon_names[type_enum.value]
                icon = QIcon(":/Asistente-LADM-COL/resources/images/{}".format(icon_name))
                type_item.setData(0, Qt.DecorationRole, icon)
                type_item.setData(0, Qt.FontRole, bold_font)
                type_item.addChildren(children)
                self.trw_qrs.addTopLevelItem(type_item)

        # Set selection
        iterator = QTreeWidgetItemIterator(self.trw_qrs, QTreeWidgetItemIterator.Selectable)
        self.trw_qrs.blockSignals(True)  # We don't want to get itemSelectionChanged here
        while iterator.value():
            item = iterator.value()
            if item.data(0, Qt.UserRole) in self.__selected_items_list:
                item.setSelected(True)

            iterator += 1

        self.trw_qrs.blockSignals(False)

        # Make type items non selectable
        # Set expand taking previous states into account
        for i in range(self.trw_qrs.topLevelItemCount()):
            self.trw_qrs.topLevelItem(i).setFlags(Qt.ItemIsEnabled)  # Not selectable
            self.trw_qrs.topLevelItem(i).setExpanded(top_level_items_expanded_info.get(self.trw_qrs.topLevelItem(i).text(0), True))

        self.trw_qrs.setUpdatesEnabled(True)  # Now render!

    def __filter_by_search_text(self, type, search_text):
        res = list(self.__controller.get_qrs_tree_data()[type].values())

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

    def __update_selected_items(self):
        iterator = QTreeWidgetItemIterator(self.trw_qrs, QTreeWidgetItemIterator.Selectable)
        while iterator.value():
            item = iterator.value()
            qr_key = item.data(0, Qt.UserRole)

            if item.isSelected():
                if qr_key not in self.__selected_items_list:
                    self.__selected_items_list.append(qr_key)
            else:
                if qr_key in self.__selected_items_list:
                    # It was selected before, but not anymore
                    self.__selected_items_list.remove(qr_key)

            iterator += 1

        self.__update_controls_after_selection_update()

    def __search_text_changed(self, text):
        self.__update_available_rules()

    def __validate_clicked(self):
        self.__save_settings()
        self.__update_selected_items() # Take latest selection into account

        dir_path = self.txt_dir_path.text().strip()
        if not os.path.isdir(dir_path):
            self.logger.warning_msg(__name__, QCoreApplication.translate("QualityRulesInitialPanelWidget",
                                                                         "The dir '{}' does not exist! Select a valid dir to store quality validation results.").format(
                dir_path), 15)
            return

        if len(self.__selected_items_list):
            self.__controller.set_qr_dir_path(dir_path)
            self.__controller.set_selected_qrs(self.__selected_items_list.copy())
            self.__selected_items_list = list()  # Reset
            self.show_general_results_panel()

    def __read_clicked(self):
        self.__save_settings()
        self.show_general_results_panel()

    def __save_settings(self):
        self.app.settings.qr_results_dir_path = self.txt_dir_path.text().strip()
        self.app.settings.qr_db_file_path = self.txt_db_path.text().strip()

    def __restore_settings(self):
        self.txt_dir_path.setText(self.app.settings.qr_results_dir_path)
        self.txt_db_path.setText(self.app.settings.qr_db_file_path)

    def __select_predefined_changed(self, index):
        pass

    def __update_selected_count_label(self):
        selected_count = len(self.__selected_items_list)
        if selected_count == 0:
            text = QCoreApplication.translate("QualityRules", "There are no selected rules to validate")
            btn_text = QCoreApplication.translate("QualityRules", "Validate")
        elif selected_count == 1:
            text = QCoreApplication.translate("QualityRules", "There is 1 selected rule to validate")
            btn_text = QCoreApplication.translate("QualityRules", "Validate 1 rule")
        else:
            text = QCoreApplication.translate("QualityRules",
                                              "There are {} selected rules to validate").format(selected_count)
            btn_text = QCoreApplication.translate("QualityRules", "Validate {} rules").format(selected_count)

        self.lbl_selected_count.setText(text)
        self.btn_validate.setText(btn_text)

    def __selection_changed(self):
        # Update internal dict and dialog label
        self.__update_selected_items()

    def __update_controls_after_selection_update(self):
        # Custom slot to refresh labels and button state
        self.btn_validate.setEnabled(len(self.__selected_items_list))
        self.__update_selected_count_label()

    def show_general_results_panel(self):
        self.parent.show_general_results_panel(self.__mode)

    def __show_help(self):
        show_plugin_help("quality_rules")
