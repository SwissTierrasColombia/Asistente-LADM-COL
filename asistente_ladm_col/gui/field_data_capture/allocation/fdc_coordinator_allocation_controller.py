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

from asistente_ladm_col.config.general_config import FDC_COORDINATOR_DATASET_NAME
from asistente_ladm_col.gui.field_data_capture.base_fdc_allocation_controller import BaseFDCAllocationController
from asistente_ladm_col.utils.qt_utils import normalize_local_url


class FDCCoordinatorAllocationController(BaseFDCAllocationController):
    def __init__(self, iface, db, ladm_data):
        BaseFDCAllocationController.__init__(self, iface, db, ladm_data)

        self.receiver_type = self.surveyor_type  # Coordinator allocates parcels to surveyors

        self._with_offline_project = True

    def area_layer(self):
        return self._layers[self._db.names.FDC_SPECIFIC_AREA_T]

    def _get_parcel_field_referencing_receiver(self):
        return self._db.names.T_BASKET_F

    def _get_receiver_referenced_field(self):
        return self._db.names.T_BASKET_F

    def get_basket_id_for_new_receiver(self):
        res, msg = self._get_basket_id_for_new_receiver(FDC_COORDINATOR_DATASET_NAME)
        if not res:
            msg_prefix = QCoreApplication.translate("FDCCoordinatorAllocationController", "No surveyor can be created.")
            msg = msg_prefix + " " + msg

        return res, msg

    def get_coordinator_basket_id_for_new_receiver(self):
        # At this point, the user table should only have 1 coordinator (remember that we have a subset of admin's data),
        # so we are safe getting the unique basket value for the role coordinator.
        coordinators_dict = self._ladm_data.get_fdc_receivers_data(self.db().names,
                                                                   self.user_layer(),
                                                                   self._db.names.T_BASKET_F,
                                                                   self.coordinator_type)
        basket_ids = list(coordinators_dict.keys())
        basket_id = False  # We use False intentionally, as None might be a valid value for the coordinator's basket id!
        msg = "Success!"

        if len(basket_ids) < 1:
            msg = QCoreApplication.translate("FDCCoordinatorAllocationController",
                                             "The field coordinator was not found in the user table, but it is required! No surveyor can be created.")
        elif len(basket_ids) > 1:
            msg = QCoreApplication.translate("FDCCoordinatorAllocationController",
                                             "The user table has more than one basket value, but only one is required! No surveyor can be created. (Hint: Is there more than one coordinator? It shouldn't!)")
        else:  # Eureka!
            basket_id = basket_ids.pop()

        return basket_id, msg

    def delete_receiver(self, receiver_id):
        return self._ladm_data.delete_surveyor(self.db().names, receiver_id, self.user_layer())

    def _successful_export_message(self, count, export_dir):
        return QCoreApplication.translate("FDCCoordinatorAllocationController",
                                          "{count} offline projects were succcessfully generated in <a href='file:///{normalized_path}'>{path}</a>!").format(
            count=count,
            normalized_path=normalize_local_url(export_dir),
            path=export_dir
        )