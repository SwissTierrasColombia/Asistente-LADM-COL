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
from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication)

from asistente_ladm_col.gui.field_data_capture.allocate_parcels_admin_initial_panel import AllocateParcelsAdminInitialPanelWidget
from asistente_ladm_col.gui.field_data_capture.allocate_parcels_to_surveyor_panel import AllocateParcelsToSurveyorPanelWidget
from asistente_ladm_col.gui.field_data_capture.base_dockwidget_field_data_capture import BaseDockWidgetFieldDataCapture
from asistente_ladm_col.gui.field_data_capture.configure_coordinators_panel import ConfigureCoordinatorsPanelWidget
from asistente_ladm_col.gui.field_data_capture.convert_to_offline_panel import ConvertToOfflinePanelWidget
from asistente_ladm_col.utils.qt_utils import OverrideCursor


class DockWidgetFieldDataCaptureAdminCoordinator(BaseDockWidgetFieldDataCapture):
    def __init__(self, iface, db, ladm_data, allocate_mode=True):
        BaseDockWidgetFieldDataCapture.__init__(self, iface, db, ladm_data, allocate_mode)
        self.setWindowTitle(QCoreApplication.translate("DockWidgetFieldDataCaptureAdminCoordinator", "Allocate parcels Admin-Coordinator"))

    def _initialize_allocate_initial_panel(self):
        self.add_layers()
        self.allocate_panel = AllocateParcelsAdminInitialPanelWidget(self, self._controller)
        self.allocate_panel.allocate_parcels_to_receiver_panel_requested.connect(self.show_allocate_parcels_to_receiver_panel)
        self.allocate_panel.configure_receivers_panel_requested.connect(self.show_configure_receivers_panel)
        self.allocate_panel.split_data_for_receivers_panel_requested.connect(self.show_split_data_for_receivers_panel)
        self.widget.setMainPanel(self.allocate_panel)
        self.allocate_panel.fill_data()

    def _initialize_synchronize_initial_panel(self):
        pass

    def _get_receivers_panel(self):
        return ConfigureCoordinatorsPanelWidget(self, self._controller)

    def show_allocate_parcels_to_receiver_panel(self, selected_parcels):
        with OverrideCursor(Qt.WaitCursor):
            self._reset_allocate_parcels_to_receiver_panel_vars()

            self.allocate_parcels_to_receiver_panel = AllocateParcelsToSurveyorPanelWidget(self,
                                                                                           self._controller,
                                                                                           selected_parcels)
            self.allocate_parcels_to_receiver_panel.refresh_parcel_data_requested.connect(
                self.allocate_panel.panel_accepted_refresh_parcel_data)
            self.widget.showPanel(self.allocate_parcels_to_receiver_panel)
            self.lst_allocate_parcels_to_receiver_panel.append(self.allocate_parcels_to_receiver_panel)

    def show_split_data_for_receivers_panel(self):
        with OverrideCursor(Qt.WaitCursor):
            self._reset_split_data_for_receivers_panel_vars()

            self.split_data_for_receivers_panel = ConvertToOfflinePanelWidget(self, self._controller)
            self.split_data_for_receivers_panel.refresh_parcel_data_clear_selection_requested.connect(
                self.allocate_panel.panel_accepted_refresh_and_clear_selection)
            self.widget.showPanel(self.split_data_for_receivers_panel)
            self.lst_split_data_for_receivers_panel.append(self.split_data_for_receivers_panel)

