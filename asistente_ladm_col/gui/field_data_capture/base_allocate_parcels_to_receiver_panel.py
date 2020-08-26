# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-07-23
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
import locale

from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication,
                              pyqtSignal)
from qgis.PyQt.QtGui import QBrush
from qgis.PyQt.QtWidgets import (QTableWidgetItem,
                                 QMessageBox)
from qgis.gui import QgsPanelWidget

from asistente_ladm_col.config.general_config import NOT_ALLOCATED_PARCEL_COLOR
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('field_data_capture/base_allocate_parcels_to_receiver_panel_widget.ui')


class BaseAllocateParcelsToReceiverPanelWidget(QgsPanelWidget, WIDGET_UI):
    refresh_parcel_data_requested = pyqtSignal()

    def __init__(self, parent, controller, parcels_to_be_allocated):
        QgsPanelWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self._controller = controller
        self.logger = Logger()

        # Main dicts to store parcels that are not yet allocated but were selected
        # from the previous panel and parcels that are already allocated in the DB
        self.__parcels_to_be_allocated = parcels_to_be_allocated  # {parcel_fid: parcel_number}
        self.__parcels_already_allocated = dict()  # {parcel_fid: parcel_number}
        
        self.setDockMode(True)
        self.setPanelTitle(QCoreApplication.translate("BaseAllocateParcelsToReceiverPanelWidget", "Allocate parcels to receiver"))

        self.panelAccepted.connect(self.panel_accepted)
        self.btn_save_allocation.clicked.connect(self.save_allocation)
        self.btn_discard_parcels.clicked.connect(self.discard_parcels)
        self.cbo_receiver.currentIndexChanged.connect(self.receiver_changed)

        self.__txt_already_allocated = QCoreApplication.translate("BaseAllocateParcelsToReceiverPanelWidget", "{} already allocated")
        self.__txt_to_be_allocated = QCoreApplication.translate("BaseAllocateParcelsToReceiverPanelWidget", "{} to be allocated")

        self.fill_table()
        self.fill_receivers()
        self.tbl_parcels.resizeColumnsToContents()

    def panel_accepted(self):
        self.refresh_parcel_data_requested.emit()

    def fill_table(self, refresh_allocated_parcels=True):
        self.tbl_parcels.clearContents()

        if refresh_allocated_parcels:
            self.__parcels_already_allocated = self._controller.get_already_allocated_parcels_for_receiver(self.cbo_receiver.currentData())

        number_of_rows = len(self.__parcels_to_be_allocated) + len(self.__parcels_already_allocated)
        self.tbl_parcels.setRowCount(number_of_rows)
        self.tbl_parcels.setSortingEnabled(False)

        # Fill parcels to be allocated
        for row, (parcel_fid, parcel_number) in enumerate(self.__parcels_to_be_allocated.items()):
            self.fill_row(parcel_fid, parcel_number, False, row)

        # Fill already allocated parcels
        for row, (parcel_fid, parcel_number) in enumerate(self.__parcels_already_allocated.items()):
            self.fill_row(parcel_fid, parcel_number, True, row + len(self.__parcels_to_be_allocated))

        self.tbl_parcels.setSortingEnabled(True)
        self.update_count_labels()

    def fill_row(self, parcel_fid, parcel_number, allocated, row):
        item = QTableWidgetItem(parcel_number)
        item.setData(Qt.UserRole, parcel_fid)
        self.tbl_parcels.setItem(row, 0, item)

        text = QCoreApplication.translate("BaseAllocateParcelsToReceiverPanelWidget", "Already allocated") if allocated else QCoreApplication.translate("BaseAllocateParcelsToReceiverPanelWidget", "To be allocated")
        item2 = QTableWidgetItem(text)
        item2.setData(Qt.UserRole, allocated)
        if not allocated:
            item2.setBackground(QBrush(NOT_ALLOCATED_PARCEL_COLOR))
        self.tbl_parcels.setItem(row, 1, item2)

    def fill_receivers(self):
        self.cbo_receiver.clear()
        for receiver_t_id, receiver_data in sorted(self._controller.get_receivers_data().items(), key=lambda x:locale.strxfrm(str(x[1][0]))):
            self.cbo_receiver.addItem(receiver_data[0], receiver_t_id)  # receiver_data: (name, doc id)

    def receiver_changed(self, index):
        self.fill_table()

    def update_count_labels(self):
        self.lbl_already_allocated.setText(self.__txt_already_allocated.format(len(self.__parcels_already_allocated)))
        self.lbl_to_be_allocated.setText(self.__txt_to_be_allocated.format(len(self.__parcels_to_be_allocated)))

    def discard_parcels(self):
        # Take 2 cases into account:
        # 1) an already allocated parcel is being discarded --> fill_table()
        # 2) a 'to be allocated' parcel is being discarded --> fill_table(refresh_allocated_parcels=False)
        already_allocated = list()
        to_be_allocated = list()

        selected_gui_items = [item.data(Qt.UserRole) for item in self.tbl_parcels.selectedItems()]
        for row in range(self.tbl_parcels.rowCount()):
            item = self.tbl_parcels.item(row, 0)
            fid = item.data(Qt.UserRole)
            if fid in selected_gui_items:
                item2 = self.tbl_parcels.item(row, 1)
                if item2.data(Qt.UserRole):  # Allocated?
                    already_allocated.append(fid)
                else:
                    to_be_allocated.append(fid)

        if not already_allocated and not to_be_allocated:
            self.logger.warning_msg(__name__, QCoreApplication.translate("BaseAllocateParcelsToReceiverPanelWidget",
                                                                         "First select some parcels in the list."))
            return

        reply = QMessageBox.question(self,
                                     QCoreApplication.translate("BaseAllocateParcelsToReceiverPanelWidget", "Do you confirm?"),
                                     QCoreApplication.translate("BaseAllocateParcelsToReceiverPanelWidget",
                                                                "Are you sure you want to remove the allocation of selected parcels in the list?"),
                                     QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            res = False
            # 1)
            if already_allocated:
                res = self._controller.discard_parcel_allocation(already_allocated)

            # 2)
            for parcel_fid in to_be_allocated:
                del self.__parcels_to_be_allocated[parcel_fid]
                res = True

            if res:
                self.logger.success_msg(__name__, QCoreApplication.translate("BaseAllocateParcelsToReceiverPanelWidget",
                                                                             "Selected parcels were successfully discarded!"))
            else:
                self.logger.warning_msg(__name__, QCoreApplication.translate("BaseAllocateParcelsToReceiverPanelWidget",
                                                                             "There were troubles discarding parcels!"))

            # Finally, reload the table, refreshing from data source only when already-allocated parcels were discarded
            # For safety, we reload even if not res, just to make sure our data is totally in sync
            self.fill_table(bool(already_allocated))

    def save_allocation(self):
        if not self.__parcels_to_be_allocated:
            self.logger.warning_msg(__name__, QCoreApplication.translate("BaseAllocateParcelsToReceiverPanelWidget",
                                    "There are no parcels to be allocated! Go back and select some parcels first."))
            return

        parcel_ids_to_allocate = list(self.__parcels_to_be_allocated.keys())

        res = self._controller.save_allocation_for_receiver(parcel_ids_to_allocate, self.cbo_receiver.currentData())
        if res:
            self.logger.success_msg(__name__,
                                    QCoreApplication.translate("BaseAllocateParcelsToReceiverPanelWidget",
                                                               "{} parcels were allocated to user {}!").format(
                                        len(parcel_ids_to_allocate),
                                        self.cbo_receiver.currentText()))
            self.__parcels_to_be_allocated = dict()
            self.fill_table()
        else:
            self.logger.warning_msg(__name__, QCoreApplication.translate("BaseAllocateParcelsToReceiverPanelWidget",
                                                               "There was an error allocating the parcels!"))