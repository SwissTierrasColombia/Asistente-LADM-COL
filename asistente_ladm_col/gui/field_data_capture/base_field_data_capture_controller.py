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


class BaseFieldDataCaptureController(QObject):
    field_data_capture_layer_removed = pyqtSignal()
    export_field_data_progress = pyqtSignal(int)  # total progress (percentage)

    def __init__(self, iface, db, ladm_data):
        QObject.__init__(self)
        self.iface = iface
        self._db = db
        self._ladm_data = ladm_data

        self.app = AppInterface()

        self._layers = dict()
        self.initialize_layers()

        self.__parcel_data = dict()  # {t_id: {parcel_number: t_id_receiver}}

    def initialize_layers(self):
        raise NotImplementedError

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

    def get_parcel_receiver_data(self):
        receivers_dict = self.get_receivers_data(False)  # Just first letter of each name part

        for fid, pair in self._ladm_data.get_parcel_data_field_data_capture(self._db.names, self.parcel_layer()).items():
            # pair: parcel_number, receiver_t_id
            self.__parcel_data[fid] = (pair[0], receivers_dict[pair[1]][0] if pair[1] else None)

        return self.__parcel_data

    def db(self):
        return self._db

    def plot_layer(self):
        return self._layers[self._db.names.FDC_PLOT_T]

    def parcel_layer(self):
        return self._layers[self._db.names.FDC_PARCEL_T]

    def user_layer(self):
        return self._layers[self._db.names.FDC_USER_T]

    def update_plot_selection(self, parcel_ids):
        plot_ids = self._ladm_data.get_plots_related_to_parcels_field_data_capture(self._db.names,
                                                                                   self.parcel_layer(),
                                                                                   self.plot_layer(),
                                                                                   fids=parcel_ids)
        self.plot_layer().selectByIds(plot_ids)

    def get_parcel_numbers_from_selected_plots(self):
        plot_ids = self.plot_layer().selectedFeatureIds()
        return self._ladm_data.get_parcels_related_to_plots_field_data_capture(self._db.names,
                                                                               plot_ids,
                                                                               self.plot_layer(),
                                                                               self.parcel_layer())

    def save_allocation_for_receiver(self, parcel_ids, receiver_t_id):
        raise NotImplementedError

    def get_already_allocated_parcels_for_receiver(self, receiver_t_id):
        raise NotImplementedError

    def discard_parcel_allocation(self, parcel_ids):
        raise NotImplementedError

    def export_field_data(self, export_dir):
        raise NotImplementedError

    def get_receivers_data(self, full_name=True):
        raise NotImplementedError

    def save_receiver(self, receiver_data):
        raise NotImplementedError

    def delete_receiver(self, receiver_t_id):
        raise NotImplementedError

    def get_summary_data(self):
        raise NotImplementedError

    def get_count_of_not_allocated_parcels(self):
        raise NotImplementedError