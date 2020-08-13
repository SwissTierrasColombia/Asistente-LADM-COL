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
from PyQt5.QtCore import QObject, pyqtSignal

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.lib.field_data_capture import FieldDataCapture


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
            self.__parcel_data[fid] = (pair[0], surveyors_dict[pair[1]][0] if pair[1] else None)

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

    def _get_surveyors_data(self, full_name=True):
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

    def get_surveyors_data(self, full_name=True):
        return self.ladm_data.get_surveyors_data(self.db().names, self.surveyor_layer(), full_name)

    def save_surveyor(self, surveyor_data):
        return self.ladm_data.save_surveyor(self.db(), surveyor_data, self.surveyor_layer())

    def delete_surveyor(self, surveyor_t_id):
        return self.ladm_data.delete_surveyor(self.db().names, surveyor_t_id, self.surveyor_layer())

    def get_summary_data(self):
        return self.ladm_data.get_summary_of_allocation_field_data_capture(self.db().names,
                                                                           self.parcel_layer(),
                                                                           self.surveyor_layer())

    def get_count_of_not_allocated_parcels(self):
        return self.ladm_data.get_count_of_not_allocated_parcels_field_data_capture(self.db().names,
                                                                                    self.parcel_layer())