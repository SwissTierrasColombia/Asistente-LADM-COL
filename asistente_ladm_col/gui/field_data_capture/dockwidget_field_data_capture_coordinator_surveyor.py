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

from asistente_ladm_col.gui.field_data_capture.allocate_parcels_coordinator_initial_panel import AllocateParcelsCoordinatorInitialPanelWidget
from asistente_ladm_col.gui.field_data_capture.allocate_parcels_to_surveyor_panel import AllocateParcelsToSurveyorPanelWidget
from asistente_ladm_col.gui.field_data_capture.base_dockwidget_field_data_capture import BaseDockWidgetFieldDataCapture
from asistente_ladm_col.gui.field_data_capture.configure_surveyors_panel import ConfigureSurveyorsPanelWidget
from asistente_ladm_col.gui.field_data_capture.field_data_capture_coordinator_controller import FieldDataCaptureCoordinatorController
from asistente_ladm_col.gui.field_data_capture.split_data_for_surveyors_panel import SplitDataForSurveyorsPanelWidget


class DockWidgetFieldDataCaptureCoordinatorSurveyor(BaseDockWidgetFieldDataCapture):
    def __init__(self, iface, db, ladm_data, allocate_mode=True):
        BaseDockWidgetFieldDataCapture.__init__(self, iface, db, ladm_data, allocate_mode)
        self.setWindowTitle(QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget", "Allocate parcels Coordinator-Surveyor"))

    def _get_controller(self, iface, db, ladm_data):
        return FieldDataCaptureCoordinatorController(iface, db, ladm_data)

    def _initialize_allocate_initial_panel(self):
        self.add_layers()
        self.allocate_panel = AllocateParcelsCoordinatorInitialPanelWidget(self, self._controller)
        self.allocate_panel.allocate_parcels_to_receiver_panel_requested.connect(self.show_allocate_parcels_to_receiver_panel)
        self.allocate_panel.configure_receivers_panel_requested.connect(self.show_configure_receivers_panel)
        self.allocate_panel.split_data_for_receivers_panel_requested.connect(self.show_split_data_for_receivers_panel)
        self.widget.setMainPanel(self.allocate_panel)
        self.allocate_panel.fill_data()

    def _initialize_synchronize_initial_panel(self):
        pass

    def _get_receivers_panel(self):
        return ConfigureSurveyorsPanelWidget(self, self._controller)

    def _get_allocate_to_receiver_panel(self, selected_parcels):
        return AllocateParcelsToSurveyorPanelWidget(self,
                                                    self._controller,
                                                    selected_parcels)

    def _get_split_data_for_receivers_panel(self):
        return SplitDataForSurveyorsPanelWidget(self, self._controller)

