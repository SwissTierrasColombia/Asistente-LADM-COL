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
from asistente_ladm_col.config.general_config import FDC_DATASET_NAME
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

        self.receiver_type = None  # To be overwritten by children classes

        self._layers = dict()
        self.initialize_layers()

        self.__parcel_data = dict()  # {t_id: {parcel_number: t_id_receiver}}

    def initialize_layers(self):
        self._layers = {
            self._db.names.FDC_PLOT_T: None,
            self._db.names.FDC_PARCEL_T: None,
            self._db.names.FDC_USER_T: None,
            self._db.names.FDC_PARTY_DOCUMENT_TYPE_D: None
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

    def get_parcel_receiver_data(self):
        """
        Obtain parcel-receiver pairs (if no receiver is associated with the parcel, just return None in that field)

        :return: dict in the form {parcel_fid: (parcel_number, receiver_name)}
        """
        receivers_dict = self.get_receivers_data(False)  # Just first letter of each name part

        for fid, pair in self._ladm_data.get_parcel_data_field_data_capture(self._db.names,
                                                                            self.parcel_layer(),
                                                                            self._get_parcel_field_referencing_receiver()).items():
            # pair: parcel_number, parcel_field_pointing_to_receiver (either t_basket or receiver_t_id)
            self.__parcel_data[fid] = (pair[0],
                                       receivers_dict[pair[1]][0] if pair[1] and pair[1] in receivers_dict else None)

        return self.__parcel_data

    def _get_parcel_field_referencing_receiver(self):
        """
        :return: Field name in layer parcels used as FK to receivers. In mode admin-coord it is "t_basket",
                 in mode coord-surveyor, it is "reconocedor".
                 Note that t_basket is not really an FK for 2 reasons:
                  1) It could be pointing to a default basket created at the illi2db import execution.
                  2) We force (in the application level) user.t_basket to correspond with parcel.t_basket, the DB knows
                     nothing about it. It's because of the logic we need to link users-(baskets)-parcels that we use
                     t_basket as FK.
        """
        raise NotImplementedError

    def _get_receiver_referenced_field(self):
        """
        :return: Field name in receivers table referenced by parcel.
        """
        raise NotImplementedError

    def db(self):
        return self._db

    def plot_layer(self):
        return self._layers[self._db.names.FDC_PLOT_T]

    def parcel_layer(self):
        return self._layers[self._db.names.FDC_PARCEL_T]

    def user_layer(self):
        return self._layers[self._db.names.FDC_USER_T]

    def document_types_table(self):
        return self._layers[self._db.names.FDC_PARTY_DOCUMENT_TYPE_D]

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

    def save_allocation_for_receiver(self, parcel_ids, receiver_id):
        """
        :param parcel_ids: List of parcels to allocate
        :param receiver_id: Either receiver_t_id or receiver_t_basket
        :return: Whether parcels were successfully allocated or not
        """
        return self._ladm_data.save_allocation_for_receiver_field_data_capture(parcel_ids,
                                                                               receiver_id,
                                                                               self._get_parcel_field_referencing_receiver(),
                                                                               self.parcel_layer())

    def get_already_allocated_parcels_for_receiver(self, receiver_id):
        """
        :param receiver_id: Either t_id (surveyor), t_basket (coordinator)
        :return: {parcel_fid: parcel_number}
        """
        return self._ladm_data.get_parcels_for_receiver_field_data_capture(self._db.names.FDC_PARCEL_T_PARCEL_NUMBER_F,
                                                                           receiver_id,
                                                                           self._get_parcel_field_referencing_receiver(),
                                                                           self.parcel_layer())

    def discard_parcel_allocation(self, parcel_ids):
        raise NotImplementedError

    def export_field_data(self, export_dir):
        raise NotImplementedError

    def get_receivers_data(self, full_name=True):
        """
        :param receiver_type: Type of receiver that will be retrieved
        :param full_name: Whether the full name should be retrieved or only an alias
        :return: {receiver_t_id: (receiver_name, receiver_doc_id)}
        """
        return self._ladm_data.get_fdc_receivers_data(self.db().names,
                                                      self.user_layer(),
                                                      self._get_receiver_referenced_field(),
                                                      self.receiver_type,
                                                      full_name)

    def save_receiver(self, receiver_data):
        return self._ladm_data.save_receiver(receiver_data, self.user_layer())

    def delete_receiver(self, receiver_t_id):
        raise NotImplementedError

    def _get_fdc_dataset(self):
        return self._ladm_data.get_or_create_ili2db_dataset_t_id(self._db, FDC_DATASET_NAME)  # t_id, msg

    def get_basket_id_for_new_receiver(self):
        """
        Get the basket id for the new receiver.

        For the admin-coord allocation, the basket id will always be a new one.
        For the coord-surveyor allocation, the basket id will be the unique value of the user.t_basket field.

        :return: Tuple --> basket_id, msg (useful in case of failure, e.g., because there are several t_basket values
                                           in a coord-surveyor scenario)
        """
        raise NotImplementedError

    def get_summary_data(self):
        return self._ladm_data.get_summary_of_allocation_field_data_capture(self.db().names,
                                                                            self.receiver_type,
                                                                            self._get_parcel_field_referencing_receiver(),
                                                                            self._get_receiver_referenced_field(),
                                                                            self.parcel_layer(),
                                                                            self.user_layer())

    def get_count_of_not_allocated_parcels(self):
        raise NotImplementedError

    def get_document_types(self):
        return self._ladm_data.get_document_types(self._db.names, self.document_types_table())