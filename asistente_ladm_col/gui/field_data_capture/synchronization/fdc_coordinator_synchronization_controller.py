# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin                : 2020-10-22
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
import tempfile

from qgis.PyQt.QtCore import QCoreApplication

from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.gui.field_data_capture.base_fdc_synchronization_controller import BaseFDCSynchronizationController
from asistente_ladm_col.lib.db.gpkg_connector import GPKGConnector
from asistente_ladm_col.lib.qgis_model_baker.ili2db import Ili2DB


class FDCCoordinatorSynchronizationController(BaseFDCSynchronizationController):
    def __init__(self, iface, db, ladm_data):
        BaseFDCSynchronizationController.__init__(self, iface, db, ladm_data)

        self.receiver_type = self._ladm_data.get_domain_code_from_value(self._db,
                                                                        self._db.names.FDC_ROLE_TYPE_D,
                                                                        LADMNames.FDC_ROLE_TYPE_D_SURVEYOR_V)

    def _validate_single_surveyor(self, db):
        receivers = self._ladm_data.get_fdc_receivers_data_any_db(db)  # {t_basket: (name, role), ...}
        if len(receivers) > 1:
            return False, None, None, QCoreApplication.translate("FDCCoordinatorSynchronizationController",
                                                           "Invalid database! There are more users than we expect in the surveyor's database.")
        elif len(receivers) == 0:
            return False, None, None, QCoreApplication.translate("FDCCoordinatorSynchronizationController",
                                                           "Invalid database! There are no users in the surveyor's database.")

        t_basket = list(receivers.keys())[0]

        # Check that role is surveyor
        role = receivers[t_basket][1]
        if role != self.receiver_type:
            return False, None, None, QCoreApplication.translate("FDCCoordinatorSynchronizationController",
                                                     "Invalid database! The only user in the database must be a surveyor, but it is not.")

        basket_uuid = self._ladm_data.get_basket_uuid(db, t_basket)

        return True, t_basket, basket_uuid, "Success!"

    def _set_surveyors_t_basket_to_layers(self, db, t_basket):
        return self._ladm_data.update_t_basket_in_layers(db, self.get_receiver_layer_list(db), t_basket)

    def synchronize_data(self, db, file_path):
        # Validate db structure
        db = GPKGConnector(file_path)
        res, code, msg = db.test_connection()
        self.app.settings.fdc_surveyor_gpkg_path = file_path

        if not res:
            return False, QCoreApplication.translate("SynchronizeDataCoordinatorInitialPanelWidget",
                                                     "There was an error validating the GeoPackage database. Details: {}").format(
                msg)

        # Validate that we have a single user, and it's a surveyor. Also, get his t_basket
        res, t_basket, basket_uuid, msg = self._validate_single_surveyor(db)
        if not res:
            return False, QCoreApplication.translate("SynchronizeDataCoordinatorInitialPanelWidget", msg)

        # Set surveyor's t_basket and write it in all DB classes
        res = self._set_surveyors_t_basket_to_layers(db, t_basket)
        if not res:
            return False, QCoreApplication.translate("SynchronizeDataCoordinatorInitialPanelWidget",
                                                     "There was an error preparing the GeoPackage database. See QGIS log for details")

        # Generate XTF
        ili2db = Ili2DB()
        xtf_path = tempfile.mktemp() + '.xtf'
        res, msg = ili2db.export(db, xtf_path, baskets=[basket_uuid])
        if not res:
            return False, QCoreApplication.translate("SynchronizeDataCoordinatorInitialPanelWidget",
                                                     "Error sinchronizing surveyor's database. Details: {}").format(msg)

        # # Run update
        # res, msg = Ili2DbLib.update(self._db, xtf_path, dataset_name, context_title)
        # if not res:
        #     self.logger.warning_msg(__name__, QCoreApplication.translate("SynchronizeDataCoordinatorInitialPanelWidget",
        #                                                                  "There was an error synchronizing the surveyor's database."))
        #     return

        return True, QCoreApplication.translate("SynchronizeDataCoordinatorInitialPanelWidget",
                                                "Surveyor's data have been synchronized successfully!")
