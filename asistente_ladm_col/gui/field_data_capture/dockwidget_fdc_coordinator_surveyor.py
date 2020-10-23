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
from qgis.PyQt.QtCore import QCoreApplication

from asistente_ladm_col.gui.field_data_capture.allocation.allocate_parcels_coordinator_initial_panel import AllocateParcelsCoordinatorInitialPanelWidget
from asistente_ladm_col.gui.field_data_capture.allocation.allocate_parcels_to_surveyor_panel import AllocateParcelsToSurveyorPanelWidget
from asistente_ladm_col.gui.field_data_capture.base_dockwidget_fdc import BaseDockWidgetFDC
from asistente_ladm_col.gui.field_data_capture.allocation.configure_surveyors_panel import ConfigureSurveyorsPanelWidget
from asistente_ladm_col.gui.field_data_capture.allocation.fdc_coordinator_allocation_controller import FDCCoordinatorAllocationController
from asistente_ladm_col.gui.field_data_capture.allocation.split_data_for_surveyors_panel import SplitDataForSurveyorsPanelWidget
from asistente_ladm_col.gui.field_data_capture.synchronization.fdc_coordinator_synchronization_controller import FDCCoordinatorSynchronizationController
from asistente_ladm_col.gui.field_data_capture.synchronization.synchronize_data_coordinator_initial_panel import SynchronizeDataCoordinatorInitialPanelWidget


class DockWidgetFDCCoordinatorSurveyor(BaseDockWidgetFDC):
    def __init__(self, iface, db, ladm_data, allocate_mode=True):
        BaseDockWidgetFDC.__init__(self, iface, db, ladm_data, allocate_mode)

    def _get_allocation_controller(self, iface, ladm_data):
        return FDCCoordinatorAllocationController(iface, self._db, ladm_data)

    def _get_synchronization_controller(self, iface, ladm_data):
        return FDCCoordinatorSynchronizationController(iface, self._db, ladm_data)

    def _initialize_allocate_initial_panel(self):
        self.add_allocation_layers()
        self.allocate_panel = AllocateParcelsCoordinatorInitialPanelWidget(self, self._allocation_controller)
        self.allocate_panel.allocate_parcels_to_receiver_panel_requested.connect(self.show_allocate_parcels_to_receiver_panel)
        self.allocate_panel.configure_receivers_panel_requested.connect(self.show_configure_receivers_panel)
        self.allocate_panel.split_data_for_receivers_panel_requested.connect(self.show_split_data_for_receivers_panel)
        self.widget.setMainPanel(self.allocate_panel)
        self.allocate_panel.fill_data()
        self.setWindowTitle(QCoreApplication.translate("DockWidgetFDCCoordinatorSurveyor", "Allocate parcels Coordinator-Surveyor"))

    def _initialize_synchronize_initial_panel(self):
        self.synchronize_panel = SynchronizeDataCoordinatorInitialPanelWidget(self,
                                                                              self._synchronization_controller,
                                                                              self._db)
        self.widget.setMainPanel(self.synchronize_panel)
        self.setWindowTitle(QCoreApplication.translate("DockWidgetFDCCoordinatorSurveyor", "Synchronize data from surveyor"))

    def _get_receivers_panel(self):
        return ConfigureSurveyorsPanelWidget(self, self._allocation_controller)

    def _get_allocate_to_receiver_panel(self, selected_parcels):
        return AllocateParcelsToSurveyorPanelWidget(self,
                                                    self._allocation_controller,
                                                    selected_parcels)

    def _get_split_data_for_receivers_panel(self):
        return SplitDataForSurveyorsPanelWidget(self, self._allocation_controller)

