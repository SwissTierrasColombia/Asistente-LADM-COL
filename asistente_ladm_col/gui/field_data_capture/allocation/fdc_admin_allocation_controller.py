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

from asistente_ladm_col.config.general_config import FDC_ADMIN_DATASET_NAME
from asistente_ladm_col.gui.field_data_capture.base_fdc_allocation_controller import BaseFDCAllocationController
from asistente_ladm_col.utils.qt_utils import normalize_local_url


class FDCAdminAllocationController(BaseFDCAllocationController):
    def __init__(self, iface, db, ladm_data):
        BaseFDCAllocationController.__init__(self, iface, db, ladm_data)

        self.receiver_type = self.coordinator_type  # Admin allocates parcels to coordinators

    def area_layer(self):
        return self._layers[self._db.names.FDC_GENERAL_AREA_T]

    def area_layer_user_field(self):
        return self._db.names.FDC_GENERAL_AREA_T_USER_F

    def _get_parcel_field_referencing_receiver(self):
        return self._db.names.T_BASKET_F

    def _get_receiver_referenced_field(self):
        return self._db.names.T_BASKET_F

    def get_basket_id_for_new_receiver(self):
        res, msg = self._get_basket_id_for_new_receiver(FDC_ADMIN_DATASET_NAME)
        if not res:
            msg_prefix = QCoreApplication.translate("FDCAdminAllocationController", "No coordinator can be created.")
            msg = msg_prefix + " " + msg

        return res, msg

    def get_coordinator_t_ili_tid_for_new_receiver(self):
        return None, "Success!"  # Since we don't store admin info, we pass a None (NULL) here.

    def delete_receiver(self, receiver_id):
        return self._ladm_data.delete_coordinator(self.db(), receiver_id, self.surveyor_type, self.user_layer())

    def _successful_export_message(self, count, export_dir):
        return QCoreApplication.translate("FDCAdminAllocationController",
                                          "{count} XTF files were succcessfully generated in <a href='file:///{normalized_path}'>{path}</a>!").format(
            count=count,
            normalized_path=normalize_local_url(export_dir),
            path=export_dir
        )