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

from asistente_ladm_col.gui.field_data_capture.base_allocate_parcels_initial_panel import BaseAllocateParcelsInitialPanelWidget
from asistente_ladm_col.gui.field_data_capture.allocate_parcels_to_surveyor_panel import AllocateParcelsToSurveyorPanelWidget
from asistente_ladm_col.gui.field_data_capture.configure_surveyors_panel import ConfigureSurveyorsPanelWidget
from asistente_ladm_col.gui.field_data_capture.convert_to_offline_panel import ConvertToOfflinePanelWidget
from asistente_ladm_col.gui.field_data_capture.field_data_capture_controller import FieldDataCaptureController
from asistente_ladm_col.utils import get_ui_class

from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.qt_utils import OverrideCursor

DOCKWIDGET_UI = get_ui_class('field_data_capture/dockwidget_field_data_capture.ui')


class BaseDockWidgetFieldDataCapture(QgsDockWidget, DOCKWIDGET_UI):
    def __init__(self, iface, db, ladm_data, allocate_mode=True):
        super(BaseDockWidgetFieldDataCapture, self).__init__(None)
        self.setupUi(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.logger = Logger()
        self.logger.clear_message_bar()  # Clear QGIS message bar

        self._controller = FieldDataCaptureController(iface, db, ladm_data)
        self._controller.field_data_capture_layer_removed.connect(self.layer_removed)

        # Configure panels
        self.configure_receivers_panel = None
        self.lst_configure_receivers_panel = list()

        self.allocate_parcels_to_receiver_panel = None
        self.lst_allocate_parcels_to_receiver_panel = list()

        self.split_data_for_receivers_panel = None
        self.lst_split_data_for_receivers_panel = list()

        self.allocate_panel = None

        if allocate_mode:
            self._initialize_allocate_initial_panel()
        else:  # Synchronize mode
            # self.synchronize_panel = ChangesPerParcelPanelWidget(self, self.utils)
            # self.widget.setMainPanel(self.synchronize_panel)
            # self.lst_parcel_panels.append(self.synchronize_panel)
            self._initialize_synchronize_initial_panel()

    def _initialize_allocate_initial_panel(self):
        raise NotImplementedError

    def _initialize_synchronize_initial_panel(self):
        raise NotImplementedError

    def show_configure_receivers_panel(self):
        raise NotImplementedError

    def _reset_receivers_panel_vars(self):
        if self.lst_configure_receivers_panel:
            for panel in self.lst_configure_receivers_panel:
                try:
                    self.widget.closePanel(panel)
                except RuntimeError as e:  # Panel in C++ could be already closed...
                    pass

            self.lst_configure_receivers_panel = list()
            self.configure_receivers_panel = None

    def show_allocate_parcels_to_receiver_panel(self, selected_parcels):
        raise NotImplementedError

    def _reset_allocate_parcels_to_receiver_panel_vars(self):
        if self.lst_allocate_parcels_to_receiver_panel:
            for panel in self.lst_allocate_parcels_to_receiver_panel:
                try:
                    self.widget.closePanel(panel)
                except RuntimeError as e:  # Panel in C++ could be already closed...
                    pass

            self.lst_allocate_parcels_to_receiver_panel = list()
            self.allocate_parcels_to_receiver_panel = None

    def show_split_data_for_receivers_panel(self):
        raise NotImplementedError

    def _reset_split_data_for_receivers_panel_vars(self):
        if self.lst_split_data_for_receivers_panel:
            for panel in self.lst_split_data_for_receivers_panel:
                try:
                    self.widget.closePanel(panel)
                except RuntimeError as e:  # Panel in C++ could be already closed...
                    pass

            self.lst_split_data_for_receivers_panel = list()
            self.split_data_for_receivers_panel = None

    def closeEvent(self, event):
        # Close here open signals in other panels (if needed)
        if self.allocate_panel:
            self.allocate_panel.close_panel()

        self.close_dock_widget()

    def add_layers(self):
        self._controller.add_layers()

    def layer_removed(self):
        self.logger.info_msg(__name__, QCoreApplication.translate("DockWidgetFieldDataCapture",
                                                                  "'Field data capture' has been closed because you just removed a required layer."))
        self.close_dock_widget()

    def update_db_connection(self, db, ladm_col_db, db_source):
        self.close_dock_widget()  # New DB: the user needs to use the menus again, which will start FDC from scratch

    def close_dock_widget(self):
        try:
            self._controller.field_data_capture_layer_removed.disconnect()  # disconnect layer signals
        except:
            pass

        self.close()  # The user needs to use the menus again, which will start everything from scratch

    def initialize_layers(self):
        self._controller.initialize_layers()
