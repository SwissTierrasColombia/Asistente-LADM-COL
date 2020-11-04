# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin                : 2020-08-21
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

from asistente_ladm_col.gui.field_data_capture.allocation.allocate_parcels_admin_initial_panel import AllocateParcelsAdminInitialPanelWidget
from asistente_ladm_col.gui.field_data_capture.allocation.allocate_parcels_to_coordinator_panel import AllocateParcelsToCoordinatorPanelWidget
from asistente_ladm_col.gui.field_data_capture.base_dockwidget_fdc import BaseDockWidgetFDC
from asistente_ladm_col.gui.field_data_capture.allocation.configure_coordinators_panel import ConfigureCoordinatorsPanelWidget
from asistente_ladm_col.gui.field_data_capture.allocation.fdc_admin_allocation_controller import FDCAdminAllocationController
from asistente_ladm_col.gui.field_data_capture.allocation.split_data_for_coordinators_panel import SplitDataForCoordinatorsPanelWidget
from asistente_ladm_col.gui.field_data_capture.synchronization.fdc_admin_synchronization_controller import FDCAdminSynchronizationController
from asistente_ladm_col.gui.field_data_capture.synchronization.synchronize_data_admin_initial_panel import SynchronizeDataAdminInitialPanelWidget


class DockWidgetFDCAdminCoordinator(BaseDockWidgetFDC):
    def __init__(self, iface, db, ladm_data, allocate_mode=True):
        BaseDockWidgetFDC.__init__(self, iface, db, ladm_data, allocate_mode)

    def _get_allocation_controller(self, iface, ladm_data):
        return FDCAdminAllocationController(iface, self._db, ladm_data)

    def _get_synchronization_controller(self, iface, ladm_data):
        return FDCAdminSynchronizationController(iface, self._db, ladm_data)

    def _initialize_allocate_initial_panel(self):
        if not self.add_allocation_layers():
            return False

        self.allocate_panel = AllocateParcelsAdminInitialPanelWidget(self, self._allocation_controller)
        self.allocate_panel.allocate_parcels_to_receiver_panel_requested.connect(self.show_allocate_parcels_to_receiver_panel)
        self.allocate_panel.configure_receivers_panel_requested.connect(self.show_configure_receivers_panel)
        self.allocate_panel.split_data_for_receivers_panel_requested.connect(self.show_split_data_for_receivers_panel)
        self.widget.setMainPanel(self.allocate_panel)
        self.allocate_panel.fill_data()
        self.setWindowTitle(QCoreApplication.translate("DockWidgetFDCAdminCoordinator", "Allocate parcels Admin-Coordinator"))

        return True

    def _initialize_synchronize_initial_panel(self):
        if not self.add_synchronization_layers():
            return False

        self.synchronize_panel = SynchronizeDataAdminInitialPanelWidget(self,
                                                                        self._synchronization_controller,
                                                                        self._db)
        self.widget.setMainPanel(self.synchronize_panel)
        self.setWindowTitle(QCoreApplication.translate("DockWidgetFDCAdminCoordinator", "Synchronize data from coordinator"))

        return True

    def _get_receivers_panel(self):
        return ConfigureCoordinatorsPanelWidget(self, self._allocation_controller)

    def _get_allocate_to_receiver_panel(self, selected_parcels):
        return AllocateParcelsToCoordinatorPanelWidget(self,
                                                       self._allocation_controller,
                                                       selected_parcels)

    def _get_split_data_for_receivers_panel(self):
        return SplitDataForCoordinatorsPanelWidget(self, self._allocation_controller)


