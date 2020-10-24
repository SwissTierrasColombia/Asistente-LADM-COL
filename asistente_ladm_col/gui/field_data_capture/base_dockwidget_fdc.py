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
from asistente_ladm_col.gui.field_data_capture.base_allocate_parcels_to_receiver_panel import BaseAllocateParcelsToReceiverPanelWidget
from asistente_ladm_col.gui.field_data_capture.base_configure_receivers_panel import BaseConfigureReceiversPanelWidget
from asistente_ladm_col.gui.field_data_capture.base_split_data_for_receivers_panel import BaseSplitDataForReceiversPanelWidget
from asistente_ladm_col.gui.field_data_capture.base_fdc_allocation_controller import BaseFDCAllocationController
from asistente_ladm_col.utils import get_ui_class

from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.qt_utils import OverrideCursor

DOCKWIDGET_UI = get_ui_class('field_data_capture/base_dockwidget_field_data_capture.ui')


class BaseDockWidgetFDC(QgsDockWidget, DOCKWIDGET_UI):
    def __init__(self, iface, db, ladm_data, allocate_mode=True):
        super(BaseDockWidgetFDC, self).__init__(None)
        self.setupUi(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self._db = db

        self.logger = Logger()
        self.logger.clear_message_bar()  # Clear QGIS message bar

        # Configure panels
        self.configure_receivers_panel = None
        self.lst_configure_receivers_panel = list()

        self.allocate_parcels_to_receiver_panel = None
        self.lst_allocate_parcels_to_receiver_panel = list()

        self.split_data_for_receivers_panel = None
        self.lst_split_data_for_receivers_panel = list()

        self.allocate_panel = None
        self.synchronize_panel = None

        if allocate_mode:
            self._allocation_controller = self._get_allocation_controller(iface, ladm_data)
            self._allocation_controller.field_data_capture_layer_removed.connect(self.layer_removed)
            self._initialize_allocate_initial_panel()
        else:  # Synchronize mode
            self._synchronization_controller = self._get_synchronization_controller(iface, ladm_data)
            self._synchronization_controller.field_data_capture_layer_removed.connect(self.layer_removed)
            self._initialize_synchronize_initial_panel()

    def _get_allocation_controller(self, iface, ladm_data):
        raise NotImplementedError

    def _get_synchronization_controller(self, iface, ladm_data):
        raise NotImplementedError

    def _initialize_allocate_initial_panel(self):
        raise NotImplementedError

    def _initialize_synchronize_initial_panel(self):
        raise NotImplementedError

    def show_configure_receivers_panel(self):
        with OverrideCursor(Qt.WaitCursor):
            self.__reset_receivers_panel_vars()

            self.configure_receivers_panel = self._get_receivers_panel()
            self.configure_receivers_panel.clear_message_bar_requested.connect(
                self.allocate_panel.panel_accepted_clear_message_bar)
            self.widget.showPanel(self.configure_receivers_panel)
            self.lst_configure_receivers_panel.append(self.configure_receivers_panel)

    def __reset_receivers_panel_vars(self):
        if self.lst_configure_receivers_panel:
            for panel in self.lst_configure_receivers_panel:
                try:
                    self.widget.closePanel(panel)
                except RuntimeError as e:  # Panel in C++ could be already closed...
                    pass

            self.lst_configure_receivers_panel = list()
            self.configure_receivers_panel = None

    def _get_receivers_panel(self):
        raise NotImplementedError

    def show_allocate_parcels_to_receiver_panel(self, selected_parcels):
        with OverrideCursor(Qt.WaitCursor):
            self._reset_allocate_parcels_to_receiver_panel_vars()

            self.allocate_parcels_to_receiver_panel = self._get_allocate_to_receiver_panel(selected_parcels)
            self.allocate_parcels_to_receiver_panel.refresh_parcel_data_requested.connect(
                self.allocate_panel.panel_accepted_refresh_parcel_data)
            self.widget.showPanel(self.allocate_parcels_to_receiver_panel)
            self.lst_allocate_parcels_to_receiver_panel.append(self.allocate_parcels_to_receiver_panel)

    def _reset_allocate_parcels_to_receiver_panel_vars(self):
        if self.lst_allocate_parcels_to_receiver_panel:
            for panel in self.lst_allocate_parcels_to_receiver_panel:
                try:
                    self.widget.closePanel(panel)
                except RuntimeError as e:  # Panel in C++ could be already closed...
                    pass

            self.lst_allocate_parcels_to_receiver_panel = list()
            self.allocate_parcels_to_receiver_panel = None

    def _get_allocate_to_receiver_panel(self, selected_parcels):
        raise NotImplementedError

    def show_split_data_for_receivers_panel(self):
        with OverrideCursor(Qt.WaitCursor):
            self._reset_split_data_for_receivers_panel_vars()

            self.split_data_for_receivers_panel = self._get_split_data_for_receivers_panel()
            self.split_data_for_receivers_panel.refresh_parcel_data_clear_selection_requested.connect(
                self.allocate_panel.panel_accepted_refresh_and_clear_selection)
            self.widget.showPanel(self.split_data_for_receivers_panel)
            self.lst_split_data_for_receivers_panel.append(self.split_data_for_receivers_panel)

    def _get_split_data_for_receivers_panel(self):
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

        if self.synchronize_panel:
            self.synchronize_panel.close_panel()

        self.close_dock_widget()

    def add_allocation_layers(self):
        self._allocation_controller.add_layers()

    def add_synchronization_layers(self):
        self._synchronization_controller.add_layers()

    def layer_removed(self):
        self.logger.info_msg(__name__, QCoreApplication.translate("DockWidgetFDC",
                                                                  "'Field data capture' has been closed because you just removed a required layer."))
        self.close_dock_widget()

    def update_db_connection(self, db, ladm_col_db, db_source):
        self.close_dock_widget()  # New DB: the user needs to use the menus again, which will start FDC from scratch

    def close_dock_widget(self):
        try:
            self._allocation_controller.field_data_capture_layer_removed.disconnect()  # disconnect layer signals
        except:
            pass

        self.close()  # The user needs to use the menus again, which will start everything from scratch

    def initialize_layers(self):
        self._allocation_controller.initialize_layers()
