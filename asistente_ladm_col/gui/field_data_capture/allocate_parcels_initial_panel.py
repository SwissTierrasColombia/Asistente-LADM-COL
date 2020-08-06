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
from qgis.gui import QgsPanelWidget

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.enums import EnumLogHandler
from asistente_ladm_col.config.general_config import NOT_ALLOCATED_PARCEL_COLOR
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('field_data_capture/allocate_parcels_initial_panel_widget.ui')


class AllocateParcelsFieldDataCapturePanelWidget(QgsPanelWidget, WIDGET_UI):
    allocate_parcels_to_surveyor_panel_requested = pyqtSignal(dict)  # {parcel_fid: parcel_number}

    STATUS_COL = 1

    def __init__(self, parent, controller):
        QgsPanelWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.controller = controller
        self.logger = Logger()
        self.app = AppInterface()

        self.setDockMode(True)
        self.setPanelTitle(QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget", "Allocate parcels"))
        self.parent.setWindowTitle(QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget", "Allocate parcels"))

        self.tbl_parcels.resizeColumnsToContents()
        self.prb_to_offline.setVisible(False)

        self.controller.convert_to_offline_progress.connect(self.update_progress)
        self.txt_search.valueChanged.connect(self.search_value_changed)
        self.tbl_parcels.itemSelectionChanged.connect(self.selection_changed)
        self.btn_configure_surveyors.clicked.connect(self.parent.show_configure_surveyors_panel)
        self.btn_allocate.clicked.connect(self.call_allocate_parcels_to_surveyor_panel)
        self.btn_generate_offline_projects.clicked.connect(self.generate_offline_projects)

        self.connect_to_plot_selection(True)

        self.__parcel_data = dict()  # {parcel_fid: (parcel_number, surveyor_name)}
        self.__selected_items = dict()  # {parcel_fid: parcel_number}

    def _parcel_data(self, refresh_parcel_data=False):
        if not self.__parcel_data or refresh_parcel_data:
            self.__parcel_data = self.controller.get_parcel_surveyor_data()

        return self.__parcel_data

    def fill_data(self, refresh_parcel_data=False):
        self.update_selected_items()  # Save selection

        self.tbl_parcels.blockSignals(True)  # We don't want to get itemSelectionChanged here
        self.tbl_parcels.clearContents()
        self.tbl_parcels.blockSignals(False)  # We don't want to get itemSelectionChanged here

        parcel_data = self._parcel_data(refresh_parcel_data)
        parcel_data = self.filter_data_by_search_string(parcel_data)

        number_of_rows = len(parcel_data)
        self.tbl_parcels.setRowCount(number_of_rows)
        self.tbl_parcels.setSortingEnabled(False)

        self.tbl_parcels.blockSignals(True)  # We don't want to get itemSelectionChanged here
        for row, data in enumerate(parcel_data.items()):
            parcel_number, surveyor = data[1]
            self.fill_row(data[0], parcel_number, surveyor, row)
        self.tbl_parcels.blockSignals(False)  # We don't want to get itemSelectionChanged here

        self.tbl_parcels.setSortingEnabled(True)
        self.tbl_parcels.resizeColumnsToContents()

    def fill_row(self, parcel_fid, parcel_number, surveyor, row):
        item = QTableWidgetItem(parcel_number)
        item.setData(Qt.UserRole, parcel_fid)
        self.tbl_parcels.setItem(row, 0, item)

        item2 = QTableWidgetItem(surveyor or '')
        if not surveyor:
            item2.setBackground(QBrush(NOT_ALLOCATED_PARCEL_COLOR))
        self.tbl_parcels.setItem(row, self.STATUS_COL, item2)

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
        self.controller.update_plot_selection(list(self.__selected_items.keys()))
        self.connect_to_plot_selection(True)

    def update_parcel_selection(self, selected, deselected, clear_and_select):
        """React upon a plot selection"""
        self.tbl_parcels.blockSignals(True)  # We don't want to get itemSelectionChanged here
        self.tbl_parcels.clearSelection()  # Reset GUI selection
        self.__selected_items = dict()  # Reset internal selection dict
        parcel_ids = self.controller.get_parcel_numbers_from_selected_plots()

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
            self.controller.plot_layer().selectionChanged.connect(self.update_parcel_selection)
        else:
            try:
                self.controller.plot_layer().selectionChanged.disconnect(self.update_parcel_selection)
            except (TypeError, RuntimeError):  # Layer in C++ could be already deleted...
                pass

    def close_panel(self):
        # Disconnect signals
        self.connect_to_plot_selection(False)

    def panel_accepted_refresh_parcel_data(self):
        """Slot for refreshing parcel data when it has changed in other panels"""
        self.fill_data(True)

    def call_allocate_parcels_to_surveyor_panel(self):
        # Make sure that all selected items are not yet allocated, otherwise, allow users to deallocate selected
        already_allocated = list()  # {parcel_fid: (item1, item2)}
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
                if self.controller.discard_parcel_allocation(already_allocated):
                    self.fill_data(True)  # Refresh parcel data and continue
                else:
                    self.logger.warning_msg(__name__, QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget", "There were troubles reallocating parcels!"))
                    return
            else:  # QMessageBox.Cancel
                return

        if self.__selected_items:
            self.allocate_parcels_to_surveyor_panel_requested.emit(self.__selected_items)
        else:
            self.logger.warning_msg(__name__, QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget", "First select some parcels to be allocated!"), 5)

    def generate_offline_projects(self):
        export_dir = QFileDialog.getExistingDirectory(self.parent,
                                                      QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget", "Select folder to store offline projects"),
                                                      self.app.settings.export_dir_offline_projects)
        if export_dir:
            self.app.settings.export_dir_offline_projects = export_dir
            self.prb_to_offline.setVisible(True)
            self.prb_to_offline.setRange(0, 100)
            self.prb_to_offline.setValue(0)

            res, msg = self.controller.convert_to_offline(export_dir)

            self.logger.success_warning(__name__, res, msg, EnumLogHandler.MESSAGE_BAR)

            self.fill_data(True)  # Refresh data in table widget, as it might be out of sync with newly added layers
            self.tbl_parcels.clearSelection()  # Selection might be remembered from the status before converting to offline

            self.prb_to_offline.setVisible(False)

    def update_progress(self, progress):
        self.prb_to_offline.setValue(progress)