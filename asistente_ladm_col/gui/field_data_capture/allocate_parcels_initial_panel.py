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
                              Qt)
from qgis.PyQt.QtWidgets import QTableWidgetItem
from qgis.gui import QgsPanelWidget

from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('field_data_capture/allocate_parcels_initial_panel_widget.ui')


class AllocateParcelsFieldDataCapturePanelWidget(QgsPanelWidget, WIDGET_UI):
    def __init__(self, parent, controller):
        QgsPanelWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.controller = controller

        self.setDockMode(True)
        self.setPanelTitle(QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget", "Allocate parcels"))
        self.parent.setWindowTitle(QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget", "Allocate parcels"))

        self.tbl_parcels.resizeColumnsToContents()
        self.prb_to_offline.setVisible(False)

        self.txt_search.valueChanged.connect(self.search_value_changed)
        self.tbl_parcels.itemSelectionChanged.connect(self.selection_changed)
        self.btn_configure_surveyors.clicked.connect(self.parent.show_configure_surveyors_panel)
        self.btn_allocate.clicked.connect(self.parent.show_allocate_parcels_to_surveyor_panel)

        self.connect_to_plot_selection(True)

        self.__parcel_data = dict()
        self.__selected_items = dict()  # {parcel_fid: parcel_number}

    def _parcel_data(self):
        if not self.__parcel_data:
            self.__parcel_data = self.controller.get_parcel_surveyor_data()

        return self.__parcel_data

    def fill_data(self):
        self.update_selected_items()  # Save selection

        self.tbl_parcels.blockSignals(True)  # We don't want to get itemSelectionChanged here
        self.tbl_parcels.clearContents()
        self.tbl_parcels.blockSignals(False)  # We don't want to get itemSelectionChanged here

        parcel_data = self._parcel_data()
        parcel_data = self.filter_data_by_search_string(parcel_data)

        number_of_rows = len(parcel_data)
        self.tbl_parcels.setRowCount(number_of_rows)
        self.tbl_parcels.setSortingEnabled(False)

        self.tbl_parcels.blockSignals(True)  # We don't want to get itemSelectionChanged here
        for row, data in enumerate(parcel_data.items()):
            parcel_number, role_fid = data[1]
            self.fill_row(data[0], parcel_number, role_fid, row)
        self.tbl_parcels.blockSignals(False)  # We don't want to get itemSelectionChanged here

        self.tbl_parcels.setSortingEnabled(True)

    def fill_row(self, parcel_fid, parcel_number, role_fid, row):
        item = QTableWidgetItem(parcel_number)
        item.setData(Qt.UserRole, parcel_fid)
        self.tbl_parcels.setItem(row, 0, item)

        item2 = QTableWidgetItem(
            QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget", "Allocated") if role_fid is not None else QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget", "Not allocated"))
        self.tbl_parcels.setItem(row, 1, item2)

        if parcel_fid in self.__selected_items:
            item.setSelected(True)
            item2.setSelected(True)

    def filter_data_by_search_string(self, parcel_data):
        res = parcel_data.copy()
        value = self.txt_search.value().strip()
        if value and len(value) > 1:
            res = {k:v for k,v in res.items() if value in v[0]}

        return res

    def search_value_changed(self, value):
        self.fill_data()

    def update_selected_items(self):
        selected_items = [item.data(Qt.UserRole) for item in self.tbl_parcels.selectedItems()]
        for row in range(self.tbl_parcels.rowCount()):
            item = self.tbl_parcels.item(row, 0)
            fid = item.data(Qt.UserRole)
            if fid in selected_items:
                self.__selected_items[fid] = item.text()
            else:
                if fid in self.__selected_items:
                    # It was selected before, but not anymore
                    del self.__selected_items[fid]

    def selection_changed(self):
        self.update_selected_items()

        self.connect_to_plot_selection(False)  # This plot selection should not trigger a table view selection refresh
        self.controller.update_plot_selection(list(self.__selected_items.keys()))
        self.connect_to_plot_selection(True)

    def update_parcel_selection(self, selected, deselected, clear_and_select):
        """React upon a plot selection"""
        self.tbl_parcels.blockSignals(True)  # We don't want to get itemSelectionChanged here
        self.tbl_parcels.clearSelection()
        parcel_numbers = self.controller.get_parcel_numbers_from_selected_plots()

        for parcel_number in parcel_numbers:
            items = self.tbl_parcels.findItems(parcel_number, Qt.MatchExactly)
            if items:
                items[0].setSelected(True)  # Select item in column 0
                self.tbl_parcels.item(items[0].row(), 1).setSelected(True)  # Select item in column 1

        self.tbl_parcels.blockSignals(False)
        self.update_selected_items()  # Update the internal selection dict

    def connect_to_plot_selection(self, connect):
        if connect:
            self.controller.plot_layer().selectionChanged.connect(self.update_parcel_selection)
        else:
            self.controller.plot_layer().selectionChanged.disconnect(self.update_parcel_selection)

    def close_panel(self):
        # Disconnect signals
        try:
            self.connect_to_plot_selection(False)
        except TypeError:
            pass
