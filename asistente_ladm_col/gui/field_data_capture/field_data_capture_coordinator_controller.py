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
from asistente_ladm_col.gui.field_data_capture.base_field_data_capture_controller import BaseFieldDataCaptureController
from asistente_ladm_col.lib.field_data_capture import FieldDataCapture


class FieldDataCaptureCoordinatorController(BaseFieldDataCaptureController):
    def __init__(self, iface, db, ladm_data):
        BaseFieldDataCaptureController.__init__(self, iface, db, ladm_data)

    def initialize_layers(self):
        self._layers = {
            self._db.names.FDC_PLOT_T: None,
            self._db.names.FDC_PARCEL_T: None,
            self._db.names.FDC_USER_T: None
        }

    def _get_parcel_field_referencing_receiver(self):
        return self._db.names.FDC_PARCEL_T_SURVEYOR_F

    def _get_receiver_referenced_field(self):
        return self._db.names.T_ID_F

    def discard_parcel_allocation(self, parcel_ids):
        return self._ladm_data.discard_parcel_allocation_field_data_capture(self._db.names, parcel_ids, self.parcel_layer())

    def export_field_data(self, export_dir):
        surveyor_expressions_dict = self._ladm_data.get_layer_expressions_per_receiver_field_data_capture(self._db.names,
                                                                                                          self._get_parcel_field_referencing_receiver(),
                                                                                                          self._get_receiver_referenced_field(),
                                                                                                          self.parcel_layer(),
                                                                                                          self.plot_layer(),
                                                                                                          self.user_layer())

        # Disconnect so that we don't close the panel while converting to offline
        for layer_name in self._layers:
            if self._layers[layer_name]:
                try:
                    self._layers[layer_name].willBeDeleted.disconnect(self.field_data_capture_layer_removed)
                except:
                    pass

        field_data_capture = FieldDataCapture()
        field_data_capture.total_progress_updated.connect(self.export_field_data_progress)  # Signal chaining
        res, msg = field_data_capture.convert_to_offline(self._db, surveyor_expressions_dict, export_dir)

        if res:
            self.add_layers(True)  # Update self._layers with the newly loaded layers

        return res, msg

    def save_receiver(self, receiver_data):
        return self._ladm_data.save_surveyor(self.db(), receiver_data, self.user_layer())

    def delete_receiver(self, receiver_t_id):
        return self._ladm_data.delete_surveyor(self.db().names, receiver_t_id, self.user_layer())

    def get_count_of_not_allocated_parcels(self):
        return self._ladm_data.get_count_of_not_allocated_parcels_to_surveyors_field_data_capture(self.db().names,
                                                                                                  self.parcel_layer())