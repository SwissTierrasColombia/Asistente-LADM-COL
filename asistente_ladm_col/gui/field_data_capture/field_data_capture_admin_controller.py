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

from asistente_ladm_col.gui.field_data_capture.base_field_data_capture_controller import BaseFieldDataCaptureController
from asistente_ladm_col.gui.field_data_capture.basket_exporter import BasketExporter


class FieldDataCaptureAdminController(BaseFieldDataCaptureController):
    def __init__(self, iface, db, ladm_data):
        BaseFieldDataCaptureController.__init__(self, iface, db, ladm_data)

    def initialize_layers(self):
        self._layers = {
            self._db.names.FDC_PLOT_T: None,
            self._db.names.FDC_PARCEL_T: None,
            self._db.names.FDC_USER_T: None
        }

    def _get_parcel_field_referencing_receiver(self):
        return self._db.names.T_BASKET_F

    def _get_receiver_referenced_field(self):
        return self._db.names.T_BASKET_F

    def discard_parcel_allocation(self, parcel_ids):
        return self._ladm_data.discard_parcel_allocation_field_data_capture(self._db.names, parcel_ids, self.parcel_layer())

    def export_field_data(self, export_dir):
        names = self._db.names

        # Get list of basket t_ili_tids to export
        receivers_data = self._ladm_data.get_fdc_receivers_data(names, self.user_layer(), self._get_receiver_referenced_field())
        receiver_idx = self.parcel_layer().fields().indexOf(self._get_parcel_field_referencing_receiver())
        receiver_ids = self.parcel_layer().uniqueValues(receiver_idx)
        # Only t_basket of receivers with allocated parcels
        basket_t_ids = [k for k in receivers_data.keys() if k in receiver_ids]
        basket_table = self._ladm_data.get_basket_table(self._db)
        basket_dict = {f[names.T_ILI_TID_F]: receivers_data[f[names.T_ID_F]][0] for f in basket_table.getFeatures() if f[self._db.names.T_ID_F] in basket_t_ids}

        if not basket_dict:
            return False, QCoreApplication.translate("FieldDataCaptureAdminController", "First allocate parcels to at least one coordinator.")

        # Now set basket id for allocated parcels' related features
        res = self._ladm_data.set_basket_for_features_related_to_allocated_parcels_field_data_capture(
            self._db,
            self._get_parcel_field_referencing_receiver(),
            self._get_receiver_referenced_field(),
            self.parcel_layer(),
            self.plot_layer(),
            self.user_layer())

        # Finally, export each basket to XTF
        basket_exporter = BasketExporter(self._db, basket_dict, export_dir)
        basket_exporter.total_progress_updated.connect(self.export_field_data_progress)  # Signal chaining
        all_res = basket_exporter.export_baskets()

        for basket,res in all_res.items():
            if not res[0]:  # res: (bool, msg)
                return res

        return True, QCoreApplication.translate("FieldDataCaptureAdminController", "{} XTFs were succcessfully generated!").format(len(basket_dict))

    def save_receiver(self, receiver_data):
        return self._ladm_data.save_surveyor(self.db(), receiver_data, self.user_layer())

    def delete_receiver(self, receiver_t_id):
        return self._ladm_data.delete_surveyor(self.db().names, receiver_t_id, self.user_layer())

    def get_count_of_not_allocated_parcels(self):
        return self._ladm_data.get_count_of_not_allocated_parcels_to_coordinators_field_data_capture(self.db().names,
                                                                                                     self.parcel_layer(),
                                                                                                     self.user_layer())