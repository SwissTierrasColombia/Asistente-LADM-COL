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
from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication)
from qgis.PyQt.QtWidgets import QTableWidgetItem
from qgis.gui import QgsPanelWidget

from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('field_data_capture/allocate_parcels_to_surveyor_panel_widget.ui')


class AllocateParcelsToSurveyorPanelWidget(QgsPanelWidget, WIDGET_UI):
    def __init__(self, parent, controller, selected_parcels):
        QgsPanelWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.controller = controller

        self.__selected_parcels = selected_parcels  # {parcel_fid: parcel_number}
        
        self.setDockMode(True)
        self.setPanelTitle(QCoreApplication.translate("AllocateParcelsToSurveyorPanelWidget", "Allocate parcels to surveyor"))

        self.panelAccepted.connect(self.deselect_plots)

        self.fill_table()
        self.fill_surveyors()
        self.tbl_parcels.resizeColumnsToContents()

    def deselect_plots(self):
        pass

    def fill_table(self):
        self.tbl_parcels.clearContents()

        number_of_rows = len(self.__selected_parcels)
        self.tbl_parcels.setRowCount(number_of_rows)
        self.tbl_parcels.setSortingEnabled(False)

        for row, (parcel_fid, parcel_number) in enumerate(self.__selected_parcels.items()):
            self.fill_row(parcel_fid, parcel_number, row)

        self.tbl_parcels.setSortingEnabled(True)

    def fill_row(self, parcel_fid, parcel_number, row):
        item = QTableWidgetItem(parcel_number)
        item.setData(Qt.UserRole, parcel_fid)
        self.tbl_parcels.setItem(row, 0, item)

        item2 = QTableWidgetItem(QCoreApplication.translate("AllocateParcelsToSurveyorPanelWidget", "To be allocated"))
        self.tbl_parcels.setItem(row, 1, item2)

    def fill_surveyors(self):
        self.cbo_surveyor.clear()
        for surveyor_id, surveyor_name in self.controller.get_surveyors_data().items():
            self.cbo_surveyor.addItem(surveyor_name, surveyor_id)

    def save_allocation(self):
        # TODO: only pass parcels where status is 'to be allocated'
        self.controller.save_allocation(list(self.__selected_parcels.keys()), self.cbo_surveyor.currentData())