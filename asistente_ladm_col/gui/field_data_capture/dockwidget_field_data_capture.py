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
from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication)
from qgis.gui import QgsDockWidget

from asistente_ladm_col.gui.field_data_capture.allocate_parcels_initial_panel import AllocateParcelsFieldDataCapturePanelWidget
from asistente_ladm_col.gui.field_data_capture.allocate_parcels_to_surveyor_panel import AllocateParcelsToSurveyorPanelWidget
from asistente_ladm_col.gui.field_data_capture.configure_surveyors_panel import ConfigureSurveyorsPanelWidget
from asistente_ladm_col.gui.field_data_capture.convert_to_offline_panel import ConvertToOfflinePanelWidget
from asistente_ladm_col.gui.field_data_capture.field_data_capture_controller import FieldDataCaptureController
from asistente_ladm_col.utils import get_ui_class

from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.qt_utils import OverrideCursor

DOCKWIDGET_UI = get_ui_class('field_data_capture/dockwidget_field_data_capture.ui')


class DockWidgetFieldDataCapture(QgsDockWidget, DOCKWIDGET_UI):
    def __init__(self, iface, db, ladm_data, allocate_mode=True):
        super(DockWidgetFieldDataCapture, self).__init__(None)
        self.setupUi(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.logger = Logger()
        self.logger.clear_message_bar()  # Clear QGIS message bar

        self.controller = FieldDataCaptureController(iface, db, ladm_data)
        self.controller.field_data_capture_layer_removed.connect(self.layer_removed)

        # Configure panels
        self.configure_surveyors_panel = None
        self.lst_configure_surveyors_panel = list()

        self.allocate_parcels_to_surveyor_panel = None
        self.lst_allocate_parcels_to_surveyor_panel = list()

        self.convert_to_offline_panel = None
        self.lst_convert_to_offline_panel = list()

        if allocate_mode:
            self.add_layers()
            self.allocate_panel = AllocateParcelsFieldDataCapturePanelWidget(self, self.controller)
            self.allocate_panel.allocate_parcels_to_surveyor_panel_requested.connect(self.show_allocate_parcels_to_surveyor_panel)
            self.allocate_panel.convert_to_offline_panel_requested.connect(self.show_convert_to_offline_panel)
            self.widget.setMainPanel(self.allocate_panel)
            self.allocate_panel.fill_data()
        else:  # Synchronize mode
            # self.synchronize_panel = ChangesPerParcelPanelWidget(self, self.utils)
            # self.widget.setMainPanel(self.synchronize_panel)
            # self.lst_parcel_panels.append(self.synchronize_panel)
            pass

    def show_configure_surveyors_panel(self):
        with OverrideCursor(Qt.WaitCursor):
            if self.lst_configure_surveyors_panel:
                for panel in self.lst_configure_surveyors_panel:
                    try:
                        self.widget.closePanel(panel)
                    except RuntimeError as e:  # Panel in C++ could be already closed...
                        pass

                self.lst_configure_surveyors_panel = list()
                self.configure_surveyors_panel = None

            self.configure_surveyors_panel = ConfigureSurveyorsPanelWidget(self, self.controller)
            self.configure_surveyors_panel.clear_message_bar_requested.connect(self.allocate_panel.panel_accepted_clear_message_bar)
            self.widget.showPanel(self.configure_surveyors_panel)
            self.lst_configure_surveyors_panel.append(self.configure_surveyors_panel)

    def show_allocate_parcels_to_surveyor_panel(self, selected_parcels):
        with OverrideCursor(Qt.WaitCursor):
            if self.lst_allocate_parcels_to_surveyor_panel:
                for panel in self.lst_allocate_parcels_to_surveyor_panel:
                    try:
                        self.widget.closePanel(panel)
                    except RuntimeError as e:  # Panel in C++ could be already closed...
                        pass

                self.lst_allocate_parcels_to_surveyor_panel = list()
                self.allocate_parcels_to_surveyor_panel = None

            self.allocate_parcels_to_surveyor_panel = AllocateParcelsToSurveyorPanelWidget(self,
                                                                                           self.controller,
                                                                                           selected_parcels)
            self.allocate_parcels_to_surveyor_panel.refresh_parcel_data_requested.connect(self.allocate_panel.panel_accepted_refresh_parcel_data)
            self.widget.showPanel(self.allocate_parcels_to_surveyor_panel)
            self.lst_allocate_parcels_to_surveyor_panel.append(self.allocate_parcels_to_surveyor_panel)

    def show_convert_to_offline_panel(self):
        with OverrideCursor(Qt.WaitCursor):
            if self.lst_convert_to_offline_panel:
                for panel in self.lst_convert_to_offline_panel:
                    try:
                        self.widget.closePanel(panel)
                    except RuntimeError as e:  # Panel in C++ could be already closed...
                        pass

                self.lst_convert_to_offline_panel = list()
                self.convert_to_offline_panel = None

            self.convert_to_offline_panel = ConvertToOfflinePanelWidget(self, self.controller)
            self.convert_to_offline_panel.refresh_parcel_data_clear_selection_requested.connect(self.allocate_panel.panel_accepted_refresh_and_clear_selection)
            self.widget.showPanel(self.convert_to_offline_panel)
            self.lst_convert_to_offline_panel.append(self.convert_to_offline_panel)

    def closeEvent(self, event):
        # Close here open signals in other panels (if needed)
        if self.allocate_panel:
            self.allocate_panel.close_panel()

        self.close_dock_widget()

    def add_layers(self):
        self.controller.add_layers()

    def layer_removed(self):
        self.logger.info_msg(__name__, QCoreApplication.translate("DockWidgetFieldDataCapture",
                                                                  "'Field data capture' has been closed because you just removed a required layer."))
        self.close_dock_widget()

    def update_db_connection(self, db, ladm_col_db, db_source):
        self.close_dock_widget()  # New DB: the user needs to use the menus again, which will start FDC from scratch

    def close_dock_widget(self):
        try:
            self.controller.field_data_capture_layer_removed.disconnect()  # disconnect layer signals
        except:
            pass

        self.close()  # The user needs to use the menus again, which will start everything from scratch

    def initialize_layers(self):
        self.controller.initialize_layers()
