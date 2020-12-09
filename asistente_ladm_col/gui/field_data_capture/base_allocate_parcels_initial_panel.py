# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin                : 2020-07-22
        git sha              : :%H$
        copyright            : (C) 2020 by Germán Carrillo (SwissTierras Colombia)
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
from qgis.PyQt.QtCore import (QCoreApplication,
                              Qt,
                              pyqtSignal)
from qgis.PyQt.QtGui import QBrush
from qgis.PyQt.QtWidgets import (QTableWidgetItem,
                                 QMessageBox,
                                 QFileDialog)
from qgis.core import NULL
from qgis.gui import QgsPanelWidget

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.general_config import NOT_ALLOCATED_PARCEL_COLOR
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('field_data_capture/base_allocate_parcels_initial_panel_widget.ui')


class BaseAllocateParcelsInitialPanelWidget(QgsPanelWidget, WIDGET_UI):
    allocate_parcels_to_receiver_panel_requested = pyqtSignal(dict)  # {parcel_fid: parcel_number}
    configure_receivers_panel_requested = pyqtSignal()
    split_data_for_receivers_panel_requested = pyqtSignal()

    STATUS_COL = 1

    def __init__(self, parent, controller):
        QgsPanelWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self._controller = controller
        self.logger = Logger()
        self.app = AppInterface()

        self.setDockMode(True)
        self.setPanelTitle(QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget", "Allocate parcels"))
        self.parent.setWindowTitle(QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget", "Allocate parcels"))

        self.cbo_areas.setSourceLayer(self._controller.area_layer())
        self.cbo_areas.setDisplayExpression(self._controller.area_layer_display_expression())
        self.cbo_areas.setAllowNull(True)
        self.cbo_areas.setIdentifierFields(self._controller.area_layer_identifier_fields())
        self.cbo_areas.setIdentifierValuesToNull()
        self.selected_area_changed()

        self.tbl_parcels.resizeColumnsToContents()

        self.txt_search.valueChanged.connect(self.search_value_changed)
        self.tbl_parcels.itemSelectionChanged.connect(self.selection_changed)
        self.btn_allocate.clicked.connect(self.call_allocate_parcels_to_receiver_panel)
        self.btn_configure_receivers.clicked.connect(self.configure_receivers_panel_requested)
        self.btn_show_summary.clicked.connect(self.split_data_for_receivers_panel_requested)
        self.chk_show_only_not_allocated.stateChanged.connect(self.chk_check_state_changed)
        self.btn_reallocate.clicked.connect(self.reallocate_clicked)
        self.btn_select_by_area.clicked.connect(self.select_by_area)
        self.cbo_areas.identifierValueChanged.connect(self.selected_area_changed)

        self.connect_to_plot_selection(True)

        self.__parcel_data = dict()  # {parcel_fid: (parcel_number, surveyor_name)}
        self.__selected_items = dict()  # {parcel_fid: parcel_number}

    def _parcel_data(self, refresh_parcel_data=False):
        if not self.__parcel_data or refresh_parcel_data:
            self.__parcel_data = self._controller.get_parcel_receiver_data()

        return self.__parcel_data

    def fill_data(self, refresh_parcel_data=False):
        self.update_selected_items()  # Save selection

        self.tbl_parcels.blockSignals(True)  # We don't want to get itemSelectionChanged here
        self.tbl_parcels.clearContents()
        self.tbl_parcels.blockSignals(False)  # We don't want to get itemSelectionChanged here

        # Build the parcel_data dict taking configuration (search string, chk filter) into account
        parcel_data = self._parcel_data(refresh_parcel_data).copy()
        if self.chk_show_only_not_allocated.isChecked():
            parcel_data = {k:v for k,v in parcel_data.items() if not v[1]}  # v: (parcel_number, surveyor)
        parcel_data = self.filter_data_by_search_string(parcel_data)

        self.tbl_parcels.setRowCount(len(parcel_data))
        self.tbl_parcels.setSortingEnabled(False)

        self.tbl_parcels.blockSignals(True)  # We don't want to get itemSelectionChanged here
        for row, data in enumerate(parcel_data.items()):
            parcel_number, receiver = data[1]
            self.fill_row(data[0], parcel_number, receiver, row)
        self.tbl_parcels.blockSignals(False)  # We don't want to get itemSelectionChanged here

        self.tbl_parcels.setSortingEnabled(True)
        self.tbl_parcels.resizeColumnsToContents()

    def fill_row(self, parcel_fid, parcel_number, receiver, row):
        item = QTableWidgetItem(parcel_number)
        item.setData(Qt.UserRole, parcel_fid)
        self.tbl_parcels.setItem(row, 0, item)

        item2 = QTableWidgetItem(receiver or '')
        if not receiver:
            item2.setBackground(QBrush(NOT_ALLOCATED_PARCEL_COLOR))
        self.tbl_parcels.setItem(row, self.STATUS_COL, item2)

        if parcel_fid in self.__selected_items:
            item.setSelected(True)
            item2.setSelected(True)

    def filter_data_by_search_string(self, parcel_data):
        value = self.txt_search.value().strip()
        if value and len(value) > 1:
            parcel_data = {k:v for k,v in parcel_data.items() if value in v[0]}

        return parcel_data

    def search_value_changed(self, value):
        self.fill_data()

    def chk_check_state_changed(self, state):
        self.fill_data()

    def update_selected_items(self):
        """Update the internal selected_items dict"""
        selected_gui_items = [item.data(Qt.UserRole) for item in self.tbl_parcels.selectedItems()]
        for row in range(self.tbl_parcels.rowCount()):
            item = self.tbl_parcels.item(row, 0)
            fid = item.data(Qt.UserRole)
            if fid in selected_gui_items:
                self.__selected_items[fid] = item.text()
            else:
                if fid in self.__selected_items:
                    # It was selected before, but not anymore
                    del self.__selected_items[fid]

    def selection_changed(self):
        """React upon manual selection in the table widget"""
        self.update_selected_items()

        self.connect_to_plot_selection(False)  # This plot selection should not trigger a table view selection refresh
        self._controller.update_plot_selection(list(self.__selected_items.keys()))
        self.connect_to_plot_selection(True)

    def update_parcel_selection(self, selected, deselected, clear_and_select):
        """React upon a plot selection"""
        self.tbl_parcels.blockSignals(True)  # We don't want to get itemSelectionChanged here
        self.tbl_parcels.clearSelection()  # Reset GUI selection
        self.__selected_items = dict()  # Reset internal selection dict
        parcel_ids = self._controller.get_parcel_numbers_from_selected_plots()

        for parcel_id in parcel_ids:
            if parcel_id in self._parcel_data():
                parcel_number = self._parcel_data()[parcel_id][0]
                items = self.tbl_parcels.findItems(parcel_number, Qt.MatchExactly)
                if items:
                    items[0].setSelected(True)  # Select item in column 0
                    self.tbl_parcels.item(items[0].row(), self.STATUS_COL).setSelected(True)  # Select item in column 1
                else:  # parcel is not currently shown, so select it in internal dict
                    if parcel_id in self._parcel_data():
                        self.__selected_items[parcel_id] = parcel_number

        self.tbl_parcels.blockSignals(False)
        self.update_selected_items()  # Update the internal selection dict

    def connect_to_plot_selection(self, connect):
        if connect:
            self._controller.legacy_plot_layer().selectionChanged.connect(self.update_parcel_selection)
        else:
            try:
                self._controller.legacy_plot_layer().selectionChanged.disconnect(self.update_parcel_selection)
            except (TypeError, RuntimeError):  # Layer in C++ could be already deleted...
                pass

    def close_panel(self):
        # Disconnect signals
        self.connect_to_plot_selection(False)

    def panel_accepted_clear_message_bar(self):
        self.logger.clear_message_bar()

    def panel_accepted_refresh_parcel_data(self):
        """Slot for refreshing parcel data when it has changed in other panels"""
        self.panel_accepted_clear_message_bar()
        self.fill_data(True)

    def panel_accepted_refresh_and_clear_selection(self):
        self.panel_accepted_refresh_parcel_data()  # Refresh data in table widget, as it might be out of sync with newly added layers
        self.tbl_parcels.clearSelection()  # Selection might be remembered from the status before converting to offline

    def call_allocate_parcels_to_receiver_panel(self):
        # Make sure that all selected items are not yet allocated, otherwise, allow users to deallocate selected
        already_allocated = list()  # [parcel_fid1, ...]
        for parcel_fid, parcel_number in self.__selected_items.items():
            if parcel_fid in self._parcel_data():
                if self._parcel_data()[parcel_fid][1]:  # surveyor_name
                    already_allocated.append(parcel_fid)

        if already_allocated:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Question)
            msg.setText(QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget",
                                                   "Some selected parcels are already allocated!\n\nWhat would you like to do with selected parcels that are already allocated?"))
            msg.setWindowTitle(QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget", "Warning"))
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            msg.button(QMessageBox.Yes).setText(
                QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget", "Deselect them and continue"))
            msg.button(QMessageBox.No).setText(
                QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget", "Reallocate and continue"))
            reply = msg.exec_()

            if reply == QMessageBox.Yes:  # Ignore
                # Remove selection of allocated parcels, reload table widget data and continue
                for allocated_parcel_id in already_allocated:
                    if allocated_parcel_id in self._parcel_data():
                        items = self.tbl_parcels.findItems(self._parcel_data()[allocated_parcel_id][0], Qt.MatchExactly)
                        if items:  # Item is currently shown, so deselect it in GUI
                            items[0].setSelected(False)  # Deselect item in column 0
                            self.tbl_parcels.item(items[0].row(), self.STATUS_COL).setSelected(False)  # Deselect item in column 1
                        else:  # Item is not currently shown, deselected in internal selection dict
                            if allocated_parcel_id in self.__selected_items:
                                del self.__selected_items[allocated_parcel_id]

                self.fill_data()

                if not self.__selected_items:
                    self.logger.warning_msg(__name__, QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget",
                                                                       "Ignoring selected parcels, there are none to be allocated! First select some!"), 10)
                    return

            elif reply == QMessageBox.No:  # Reallocate
                # Preserve the selected_items dict, but remove allocation before continuing
                if not self.discard_parcel_allocation(already_allocated):
                    return
            else:  # QMessageBox.Cancel
                return

        if self.__selected_items:
            self.allocate_parcels_to_receiver_panel_requested.emit(self.__selected_items)
        else:
            self.logger.warning_msg(__name__, QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget", "First select some parcels to be allocated."), 5)

    def discard_parcel_allocation(self, parcel_fids):
        res = self._controller.discard_parcel_allocation(parcel_fids)
        if res:
            self.fill_data(True)  # Refresh parcel data
            self.logger.success_msg(__name__, QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget",
                                                                         "Selected parcels are now not allocated!"))
        else:
            self.logger.warning_msg(__name__, QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget",
                                                                         "There were troubles reallocating parcels!"))
        return res

    def reallocate_clicked(self):
        if not self.__selected_items:
            self.logger.warning_msg(__name__, QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget",
                                                                         "First select some parcels."), 5)
            return

        # Get selected parcels that are already allocated
        already_allocated = list()  # [parcel_fid1, ...]
        for parcel_fid, parcel_number in self.__selected_items.items():
            if parcel_fid in self._parcel_data():
                if self._parcel_data()[parcel_fid][1]:  # surveyor_name
                    already_allocated.append(parcel_fid)

        if already_allocated:
            # Ask for confirmation
            reply = QMessageBox.question(self,
                                         QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget", "Do you confirm?"),
                                         QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget",
                                                                    "Are you sure you want to remove the allocation of selected parcels?"),
                                         QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.discard_parcel_allocation(already_allocated)
        else:
            self.logger.info_msg(__name__, QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget", "Selected parcels are not yet allocated, so we cannot reallocate them."))

    def selected_area_changed(self):
        values = self.cbo_areas.identifierValues()
        valid = values and values[0] != NULL
        self.btn_select_by_area.setEnabled(valid)
        if valid:
            self._controller.zoom_to_area(values)

    def select_by_area(self):
        self._controller.select_by_area(self.cbo_areas.identifierValues()[0])
