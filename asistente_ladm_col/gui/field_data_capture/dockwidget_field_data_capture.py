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
                              QCoreApplication,
                              QObject,
                              pyqtSignal)
from qgis.core import Qgis
from qgis.gui import QgsDockWidget

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.gui.field_data_capture.allocate_parcels_initial_panel import AllocateParcelsFieldDataCapturePanelWidget
from asistente_ladm_col.gui.field_data_capture.allocate_parcels_to_surveyor_panel import \
    AllocateParcelsToSurveyorPanelWidget
from asistente_ladm_col.gui.field_data_capture.configure_surveyors_panel import ConfigureSurveyorsPanelWidget
from asistente_ladm_col.lib.field_data_capture import FieldDataCapture
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

        if allocate_mode:
            self.add_layers()
            self.allocate_panel = AllocateParcelsFieldDataCapturePanelWidget(self, self.controller)
            self.allocate_panel.allocate_parcels_to_surveyor_panel_requested.connect(self.show_allocate_parcels_to_surveyor_panel)
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

            self.configure_surveyors_panel = ConfigureSurveyorsPanelWidget(self)
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


class FieldDataCaptureController(QObject):
    field_data_capture_layer_removed = pyqtSignal()
    convert_to_offline_progress = pyqtSignal(int)  # total progress (percentage)

    def __init__(self, iface, db, ladm_data):
        QObject.__init__(self)
        self.iface = iface
        self._db = db
        self.ladm_data = ladm_data

        self.app = AppInterface()

        self._layers = dict()
        self.initialize_layers()

        self.__parcel_data = dict()  # {t_id: {parcel_number: t_id_surveyor}}

    def initialize_layers(self):
        self._layers = {
            self._db.names.FDC_PLOT_T: None,
            self._db.names.FDC_PARCEL_T: None,
            self._db.names.FDC_SURVEYOR_T: None
        }

    def add_layers(self, force=False):
        # We can pick any required layer, if it is None, no prior load has been done, otherwise skip...
        if self._layers[self._db.names.FDC_PLOT_T] is None or force:
            self.app.gui.freeze_map(True)

            self.app.core.get_layers(self._db, self._layers, load=True, emit_map_freeze=False)
            if not self._layers:
                return None

            self.iface.setActiveLayer(self._layers[self._db.names.FDC_PLOT_T])
            self.iface.zoomToActiveLayer()

            self.app.gui.freeze_map(False)

            for layer_name in self._layers:
                if self._layers[layer_name]:  # Layer was loaded, listen to its removal so that we can react properly
                    try:
                        self._layers[layer_name].willBeDeleted.disconnect(self.field_data_capture_layer_removed)
                    except:
                        pass
                    self._layers[layer_name].willBeDeleted.connect(self.field_data_capture_layer_removed)

    def get_parcel_surveyor_data(self):
        surveyors_dict = self.get_surveyors_data(False)  # Just first letter of each name part

        for fid, pair in self.ladm_data.get_parcel_data_field_data_capture(self._db.names, self.parcel_layer()).items():
            # pair: parcel_number, surveyor_t_id
            self.__parcel_data[fid] = (pair[0], surveyors_dict[pair[1]] if pair[1] else None)

        return self.__parcel_data

    def db(self):
        return self._db

    def plot_layer(self):
        return self._layers[self._db.names.FDC_PLOT_T]

    def parcel_layer(self):
        return self._layers[self._db.names.FDC_PARCEL_T]

    def surveyor_layer(self):
        return self._layers[self._db.names.FDC_SURVEYOR_T]

    def update_plot_selection(self, parcel_ids):
        plot_ids = self.ladm_data.get_plots_related_to_parcels_field_data_capture(self._db.names,
                                                                                  self.parcel_layer(),
                                                                                  self.plot_layer(),
                                                                                  fids=parcel_ids)
        self.plot_layer().selectByIds(plot_ids)

    def get_parcel_numbers_from_selected_plots(self):
        plot_ids = self.plot_layer().selectedFeatureIds()
        return self.ladm_data.get_parcels_related_to_plots_field_data_capture(self._db.names,
                                                                              plot_ids,
                                                                              self.plot_layer(),
                                                                              self.parcel_layer())

    def save_allocation_for_surveyor(self, parcel_ids, surveyor_t_id):
        return self.ladm_data.save_allocation_for_surveyor_field_data_capture(self._db.names, parcel_ids, surveyor_t_id, self.parcel_layer())

    def get_surveyors_data(self, full_name=True):
        surveyors_data = dict()
        for feature in self.surveyor_layer().getFeatures():
            name = self.ladm_data.get_surveyor_name(self._db.names, feature, full_name)
            surveyors_data[feature[self._db.names.T_ID_F]] = name

        return surveyors_data


    def get_already_allocated_parcels_for_surveyor(self, surveyor_t_id):
        return self.ladm_data.get_parcels_for_surveyor_field_data_capture(self._db.names,
                                                                          self._db.names.FDC_PARCEL_T_PARCEL_NUMBER_F,
                                                                          surveyor_t_id,
                                                                          self.parcel_layer())

    def discard_parcel_allocation(self, parcel_ids):
        return self.ladm_data.discard_parcel_allocation_field_data_capture(self._db.names, parcel_ids, self.parcel_layer())

    def convert_to_offline(self, export_dir):
        surveyor_expressions_dict = self.ladm_data.get_layer_ids_related_to_parcels_field_data_capture(self._db.names,
                                                                                                       self.parcel_layer(),
                                                                                                       self.plot_layer(),
                                                                                                       self.surveyor_layer())

        # Disconnect so that we don't close the panel while converting to offline
        for layer_name in self._layers:
            if self._layers[layer_name]:
                try:
                    self._layers[layer_name].willBeDeleted.disconnect(self.field_data_capture_layer_removed)
                except:
                    pass

        field_data_capture = FieldDataCapture()
        field_data_capture.total_progress_updated.connect(self.convert_to_offline_progress)  # Signal chaining
        res, msg = field_data_capture.convert_to_offline(self._db, surveyor_expressions_dict, export_dir)

        if res:
            self.add_layers(True)  # Update self._layers with the newly loaded layers

        return res, msg
