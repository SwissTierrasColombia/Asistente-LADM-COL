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

from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.gui.field_data_capture.base_field_data_capture_controller import BaseFieldDataCaptureController
from asistente_ladm_col.gui.field_data_capture.basket_exporter import BasketExporter
from asistente_ladm_col.lib.ladm_col_models import LADMColModelRegistry


class FieldDataCaptureAdminController(BaseFieldDataCaptureController):
    def __init__(self, iface, db, ladm_data):
        BaseFieldDataCaptureController.__init__(self, iface, db, ladm_data)

        self.receiver_type = self._ladm_data.get_domain_code_from_value(self._db,
                                                                        self._db.names.FDC_PARTY_DOCUMENT_TYPE_D,
                                                                        LADMNames.FDC_PARTY_DOCUMENT_TYPE_D_ILICODE_F_CC_V)

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
        return self._ladm_data.discard_parcel_allocation_for_coordinators_field_data_capture(self._db, parcel_ids, self.parcel_layer())

    def export_field_data(self, export_dir):
        names = self._db.names

        # Get list of basket t_ili_tids to export
        receivers_data = self._ladm_data.get_fdc_receivers_data(names, self.user_layer(), self._get_receiver_referenced_field(), self.receiver_type, full_name=False)
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
            self.receiver_type,
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

    def get_basket_id_for_new_receiver(self):
        # 1. Make sure we've got the FDC dataset
        dataset_t_id, msg = self._get_fdc_dataset()
        if dataset_t_id is None:
            return None, QCoreApplication.translate("FieldDataCaptureAdminController", "The Field Data Capture dataset does not exist and couldn't be created! No coordinator can be created.")

        # 2. Get a new basket for such dataset
        fdc_model = LADMColModelRegistry().model(LADMNames.FIELD_DATA_CAPTURE_MODEL_KEY).full_name()
        topic_name = "{}.{}".format(fdc_model, LADMNames.FDC_TOPIC_NAME)
        basket_feature, msg = self._ladm_data.create_ili2db_basket(self._db, dataset_t_id, topic_name)

        if basket_feature is None:
            return None, QCoreApplication.translate("FieldDataCaptureAdminController", "The new coordinator could not be created. Details: Basket could not be created!")

        basket_t_id = basket_feature[self._db.names.T_ID_F]

        return basket_t_id, "Success!"

    def delete_receiver(self, receiver_id):
        return self._ladm_data.delete_coordinator(self.db(), receiver_id, self.user_layer())

    def get_count_of_not_allocated_parcels(self):
        return self._ladm_data.get_count_of_not_allocated_parcels_to_coordinators_field_data_capture(self.db().names,
                                                                                                     self.receiver_type,
                                                                                                     self.parcel_layer(),
                                                                                                     self.user_layer())