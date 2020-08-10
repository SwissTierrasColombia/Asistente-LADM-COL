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
from qgis.PyQt.QtWidgets import QTableWidgetItem
from qgis.gui import QgsPanelWidget

from asistente_ladm_col.config.general_config import NOT_ALLOCATED_PARCEL_COLOR
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('field_data_capture/allocate_parcels_to_surveyor_panel_widget.ui')


class AllocateParcelsToSurveyorPanelWidget(QgsPanelWidget, WIDGET_UI):
    refresh_parcel_data_requested = pyqtSignal()

    def __init__(self, parent, controller, parcels_to_be_allocated):
        QgsPanelWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.controller = controller
        self.logger = Logger()

        self.__parcels_to_be_allocated = parcels_to_be_allocated  # {parcel_fid: parcel_number}
        self.__parcels_already_allocated = dict()  # {parcel_fid: parcel_number}
        
        self.setDockMode(True)
        self.setPanelTitle(QCoreApplication.translate("AllocateParcelsToSurveyorPanelWidget", "Allocate parcels to surveyor"))

        self.panelAccepted.connect(self.panel_accepted)
        self.btn_save_allocation.clicked.connect(self.save_allocation)
        self.btn_discard_parcels.clicked.connect(self.discard_parcels)
        self.cbo_surveyor.currentIndexChanged.connect(self.surveyor_changed)

        self.__txt_already_allocated = QCoreApplication.translate("AllocateParcelsToSurveyorPanelWidget", "{} already allocated")
        self.__txt_to_be_allocated = QCoreApplication.translate("AllocateParcelsToSurveyorPanelWidget", "{} to be allocated")

        self.fill_table()
        self.fill_surveyors()
        self.tbl_parcels.resizeColumnsToContents()

    def panel_accepted(self):
        self.refresh_parcel_data_requested.emit()

    def fill_table(self, refresh_allocated_parcels=True):
        self.tbl_parcels.clearContents()

        if refresh_allocated_parcels:
            self.__parcels_already_allocated = self.controller.get_already_allocated_parcels_for_surveyor(self.cbo_surveyor.currentData())

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

        text = QCoreApplication.translate("AllocateParcelsToSurveyorPanelWidget", "Already allocated") if allocated else QCoreApplication.translate("AllocateParcelsToSurveyorPanelWidget", "To be allocated")
        item2 = QTableWidgetItem(text)
        if not allocated:
            item2.setBackground(QBrush(NOT_ALLOCATED_PARCEL_COLOR))
        self.tbl_parcels.setItem(row, 1, item2)

    def fill_surveyors(self):
        self.cbo_surveyor.clear()
        for surveyor_t_id, surveyor_data in sorted(self.controller.get_surveyors_data().items(), key=lambda x:locale.strxfrm(str(x[1][0]))):
            self.cbo_surveyor.addItem(surveyor_data[0], surveyor_t_id)  # surveyor_data: (name, doc id)

    def surveyor_changed(self, index):
        self.fill_table()

    def update_count_labels(self):
        self.lbl_already_allocated.setText(self.__txt_already_allocated.format(len(self.__parcels_already_allocated)))
        self.lbl_to_be_allocated.setText(self.__txt_to_be_allocated.format(len(self.__parcels_to_be_allocated)))

    def discard_parcels(self):
        # Take 2 cases into account:
        # 1) an already allocated parcel is being discarded --> fill_table()
        # 2) a 'to be allocated' parcel is being discarded --> fill_table(refresh_allocated_parcels=False)
        pass

    def save_allocation(self):
        parcel_ids_to_allocate = list(self.__parcels_to_be_allocated.keys())
        res = self.controller.save_allocation_for_surveyor(parcel_ids_to_allocate,
                                                                              self.cbo_surveyor.currentData())
        if res:
            self.logger.success_msg(__name__,
                                    QCoreApplication.translate("AllocateParcelsToSurveyorPanelWidget",
                                                               "{} parcels were allocated to surveyor {}!").format(
                                        len(parcel_ids_to_allocate),
                                        self.cbo_surveyor.currentText()))
            self.__parcels_to_be_allocated = dict()
            self.fill_table()
        else:
            self.logger.warning_msg(__name__, QCoreApplication.translate("AllocateParcelsToSurveyorPanelWidget",
                                                               "There was an error allocating the parcels!"))