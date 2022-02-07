"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin           : 2022-01-31
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
                             QIcon,
                             QBrush,
                             QColor)
from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication,
                              QSize)
from qgis.PyQt.QtWidgets import (QTableWidgetItem,
                                 QLineEdit,
                                 QComboBox,
                                 QHeaderView,
                                 QLabel,
                                 QWidget,
                                 QCheckBox,
                                 QHBoxLayout)
from qgis.gui import QgsPanelWidget

from asistente_ladm_col.config.enums import EnumQualityRuleResult
from asistente_ladm_col.config.general_config import (WIDGET_STYLE_QUALITY_RULE_SUCCESS,
                                                      WIDGET_STYLE_QUALITY_RULE_ERRORS,
                                                      WIDGET_STYLE_QUALITY_RULE_UNDEFINED,
                                                      WIDGET_STYLE_QUALITY_RULE_CRITICAL,
                                                      WIDGET_STYLE_QUALITY_RULE_INITIAL_STATE,
                                                      TABLE_ITEM_COLOR_ERROR,
                                                      TABLE_ITEM_COLOR_EXCEPTION,
                                                      TABLE_ITEM_COLOR_FIXED_ERROR)
from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.gui.transitional_system.tasks_widget import TasksWidget
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.transitional_system.st_session.st_session import STSession
from asistente_ladm_col.utils.ui import (get_ui_class,
                                         get_ui_file_path)
from asistente_ladm_col.utils.utils import show_plugin_help

WIDGET_UI = get_ui_class('quality_rules/quality_rules_error_results_panel_widget.ui')
CHECK_COLUMN = 0
UUIDS_COLUMN = 1
QRE_COLUMN = 2
DETAILS_COLUMN = 3


class QualityRulesErrorResultsPanelWidget(QgsPanelWidget, WIDGET_UI):

    def __init__(self, controller, parent=None):
        QgsPanelWidget.__init__(self, parent)
        self.setupUi(self)
        self.__controller = controller
        self.parent = parent
        self.logger = Logger()

        self.__selected_item = None  # t_id of the qr error

        self.txt_search.addAction(QIcon(":/Asistente-LADM-COL/resources/images/search.png"), QLineEdit.LeadingPosition)

        self.setDockMode(True)
        self.setPanelTitle(QCoreApplication.translate("QualityRulesErrorResultsPanelWidget", "Errors"))
        self.tbw_errors.setColumnCount(4)
        self.tbw_errors.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbw_errors.horizontalHeader().setSectionResizeMode(CHECK_COLUMN, QHeaderView.ResizeToContents)
        self.tbw_errors.horizontalHeader().setSectionResizeMode(QRE_COLUMN, QHeaderView.ResizeToContents)

        self.txt_search.textChanged.connect(self.__search_text_changed)
        #self.btn_open_report.clicked.connect(self.__controller.open_report)
        #self.btn_view_error_results.clicked.connect(self.__view_error_results_clicked)
        self.btn_help.clicked.connect(self.__show_help)
        self.tbw_errors.itemSelectionChanged.connect(self.__selection_changed)
        self.tbw_errors.cellChanged.connect(self.__cell_changed)

        # Set icon and QR name in the panel header
        qr = self.__controller.get_selected_qr()
        icon_names = ['schema.png', 'points.png', 'lines.png', 'polygons.png', 'relationships.svg']
        icon_name = icon_names[qr.type().value]
        icon = QIcon(":/Asistente-LADM-COL/resources/images/{}".format(icon_name))
        self.lbl_icon_type.setPixmap(icon.pixmap(QSize(24, 24)))
        self.lbl_icon_type.setToolTip(qr.type().name)
        self.lbl_qr_name.setText(qr.name())
        self.lbl_qr_name.setToolTip(qr.id())

        self.__column_labels = ["",
                                self.__controller.get_uuids_display_name(),
                                QCoreApplication.translate("QualityRulesErrorResultsPanelWidget", "Error"),
                                QCoreApplication.translate("QualityRulesErrorResultsPanelWidget", "Details")]

        # Load available rules for current role and current db models
        self.__load_available_errors()

    def __load_available_errors(self):
        self.__controller.load_error_results_data()
        self.__update_available_error_data()

    def __update_available_error_data(self):
        self.tbw_errors.setUpdatesEnabled(False)  # Don't render until we're ready
        self.tbw_errors.cellChanged.disconnect(self.__cell_changed)  # We don't want these notifications for a while

        # Save selection before clearing table to restate it later (if needed)
        self.__update_selected_item()

        self.tbw_errors.blockSignals(True)  # We don't want to get itemSelectionChanged here
        self.tbw_errors.clear()
        self.tbw_errors.blockSignals(False)

        self.tbw_errors.setHorizontalHeaderLabels(self.__column_labels)

        # Filter by search text
        list_errors = self.__filter_by_search_text(self.txt_search.text())
        self.tbw_errors.setRowCount(len(list_errors))
        row = 0

        for feature in list_errors:
            # 1) Fixed error checkbox
            widget = QWidget()
            checkbox = QCheckBox()
            checkbox.setCheckState(Qt.Checked if self.__controller.is_fixed_error(feature) else Qt.Unchecked)
            checkbox.setStyleSheet('background: white;')
            layout = QHBoxLayout(widget)
            layout.addWidget(checkbox)
            layout.setAlignment(Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            checkbox.stateChanged.connect(partial(self.__error_state_changed, row))
            self.tbw_errors.setCellWidget(row, CHECK_COLUMN, widget)

            # 2) Object UUIDs
            uuids = self.__controller.uuid_objs(feature)
            uuid_item = QTableWidgetItem(uuids)
            uuid_item.setData(Qt.UserRole, self.__controller.error_t_id(feature))
            uuid_item.setData(Qt.ToolTipRole, "UUIDs:\n{}".format(uuids))
            self.tbw_errors.setItem(row, UUIDS_COLUMN, uuid_item)

            # 3) Error type code
            error_type_code, error_type_display = self.__controller.error_type_code_and_display(feature)
            error_type_item = QTableWidgetItem(error_type_code)
            error_type_item.setData(Qt.ToolTipRole, "{}\n({})".format(error_type_display, error_type_code))
            self.tbw_errors.setItem(row, QRE_COLUMN, error_type_item)

            # 4) Details + Values
            details = self.__controller.error_details_and_values(feature)
            error_details_item = QTableWidgetItem(details)
            error_details_item.setData(Qt.ToolTipRole, details)
            self.tbw_errors.setItem(row, DETAILS_COLUMN, error_details_item)

            self.__set_row_color_by_state(row, self.__controller.error_state(feature))

            row += 1

        # Set selection
        self.tbw_errors.blockSignals(True)  # We don't want to get itemSelectionChanged here
        item = self.__get_item_by_t_id(self.__selected_item)
        if item:
            item.setSelected(True)
        self.tbw_errors.blockSignals(False)

        self.tbw_errors.cellChanged.connect(self.__cell_changed)  # We do want notifications from the user
        self.tbw_errors.setUpdatesEnabled(True)  # Now render!

    def __set_children_custom_widget(self, type_enum, type_item, filtered_qrs):
        dict_filtered_qrs = {qr.id(): qr for qr in filtered_qrs}
        for i in range(type_item.childCount()):
            item = type_item.child(i)
            qr_key = item.data(Qt.UserRole)
            qr_result = self.__controller.get_error_results_data()[type_enum][dict_filtered_qrs[qr_key]]
            self.__set_style_for_validation_result(item, qr_result)

    def __filter_by_search_text(self, search_text):
        features = list(self.__controller.get_error_results_data().values())

        search_text = search_text.lower().strip()
        if len(search_text) > 1:
            to_delete = list()
            for feature in features:
                # First check in UUID
                found = search_text in self.__controller.uuid_objs(feature)

                if not found:
                    # Now search in QR error type (code and display)
                    error_type_code, error_type_display = self.__controller.error_type_code_and_display(feature)
                    if search_text in error_type_code.lower() or search_text in error_type_display.lower():
                        found = True

                    if not found:
                        # Finally, if we search for 'errores', 'corregidos' or 'excepciones', we should find errors
                        if search_text in 'errores':
                            if self.__controller.is_error(feature):
                                found = True
                        elif search_text in 'corregidos':
                            if self.__controller.is_fixed_error(feature):
                                found = True
                        elif search_text in 'excepciones':
                            if self.__controller.is_exception(feature):
                                found = True

                        if not found:
                            to_delete.append(feature)

            for feature in to_delete:
                features.remove(feature)

        return features

    def __get_item_by_t_id(self, t_id):
        items = self.tbw_errors.selectedItems()

        for row in range(self.tbw_errors.rowCount()):
            item = self.tbw_errors.item(row, UUIDS_COLUMN)  # This item has data (t_id)
            if item.data(Qt.UserRole) == t_id:
                return item

        return None

    def __set_row_color_by_state(self, row, state):
        if state == LADMNames.ERR_ERROR_STATE_D_FIXED_V:
            color == TABLE_ITEM_COLOR_FIXED
        elif state == LADMNames.ERR_ERROR_STATE_D_EXCEPTION_V:
            color == TABLE_ITEM_COLOR_EXCEPTION
        else:  # LADMNames.ERR_ERROR_STATE_D_ERROR_V
            color = TABLE_ITEM_COLOR_ERROR

        for column in range(self.tbw_errors.columnCount()):
            item = self.tbw_errors.item(row, column)
            if item:
                item.setBackground(QBrush(QColor(color)))
            else:  # Do we have a widget there?
                widget = self.tbw_errors.cellWidget(row, column)
                if widget:
                    widget.setStyleSheet("background-color:{};".format(color))

    def __update_selected_item(self):
        self.__selected_item = None
        items = self.tbw_errors.selectedItems()
        for item in items:
            self.__selected_item = self.__get_item_data(item)  # t_id

    def __get_item_data(self, item):
        row = self.tbw_errors.row(item)
        return self.tbw_errors.item(row, UUIDS_COLUMN).data(Qt.UserRole)  # This item has data (t_id)

    def __search_text_changed(self, text):
        self.__update_available_error_data()

    def __save_settings(self):
        pass

    def __restore_settings(self):
        pass

    def __selection_changed(self):
        # Custom slot to refresh labels and button state
        t_ids = list()
        if len(self.tbw_errors.selectedItems()):
            for item in self.tbw_errors.selectedItems():
                if item.column() == UUIDS_COLUMN:  # Only get one item (cell) per row
                    t_ids.append(self.__get_item_data(item))
            #self.btn_view_error_results.setEnabled(len(self.tbw_errors.selectedItems()))

            self.__controller.highlight_geometries(t_ids)

    def __cell_changed(self, row, column):
        if column == CHECK_COLUMN:  # We have check boxes there
            item = self.tbw_errors.item(row, column)
            print(item.checkState())

    def __error_state_changed(self, row, state):
        # TODO: Save to controller's data and to DB
        print("Fixed" if state == Qt.Checked else "Still an error!")

    def __show_help(self):
        show_plugin_help("quality_rules")
