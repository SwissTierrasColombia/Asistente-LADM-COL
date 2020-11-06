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
import os
import tempfile

from qgis.PyQt.QtCore import QCoreApplication

from asistente_ladm_col.config.general_config import FDC_ADMIN_DATASET_NAME
from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.gui.field_data_capture.base_fdc_synchronization_controller import BaseFDCSynchronizationController
from asistente_ladm_col.lib.db.gpkg_connector import GPKGConnector
from asistente_ladm_col.lib.ladm_col_models import LADMColModelRegistry
from asistente_ladm_col.lib.qgis_model_baker.ili2db import Ili2DB


class FDCAdminSynchronizationController(BaseFDCSynchronizationController):
    def __init__(self, iface, db, ladm_data):
        BaseFDCSynchronizationController.__init__(self, iface, db, ladm_data)

        self.receiver_ilicode = LADMNames.FDC_ROLE_TYPE_D_COORDINATOR_V
        self.receiver_type = self._ladm_data.get_domain_code_from_value(self._db,
                                                                           self._db.names.FDC_ROLE_TYPE_D,
                                                                           self.receiver_ilicode)

    def _validate_single_receiver_in_source_db(self, db):
        """
        Validate that we have a single coordinator

        :param db: Coordinator's database (different from self._db, which is from the admin!)
        :return: bool result, t_basket, basket_uuid, msg
        """
        fdc_user_layer = self.app.core.get_layer(db, db.names.FDC_USER_T, load=False)
        if not fdc_user_layer:
            return False, None, None, QCoreApplication.translate("FDCAdminSynchronizationController",
                                                                 "Invalid database! User table not found in coordinator's database!")

        # Get {t_basket: (name, role), ...} for ALL receivers
        receivers_source_db = self._ladm_data.get_fdc_receivers_data(db.names,
                                                                     fdc_user_layer,
                                                                     db.names.T_BASKET_F,
                                                                     None, True, db.names.FDC_USER_T_ROLE_F)

        if len(receivers_source_db) == 0:
            return False, None, None, QCoreApplication.translate("FDCAdminSynchronizationController",
                                                           "Invalid database! There are no users in the coordinator's database.")

        # Go for the coordinator role
        coordinator_count = 0
        coordinator_t_basket = None
        coordinator_role = self._ladm_data.get_domain_code_from_value(db,
                                                                      db.names.FDC_ROLE_TYPE_D,
                                                                      self.receiver_ilicode)
        for t_basket, data in receivers_source_db.items():
            if data[1] == coordinator_role:  # data[1] is the user role
                coordinator_count += 1
                coordinator_t_basket = t_basket

        # Validate we have a single coordinator role
        if coordinator_count > 1:
            return False, None, None, QCoreApplication.translate("FDCAdminSynchronizationController",
                                                           "Invalid database! There are more coordinators than we expect in the coordinator's database.")
        elif coordinator_count == 0:
            return False, None, None, QCoreApplication.translate("FDCAdminSynchronizationController",
                                                           "Invalid database! There are no coordinators in the coordinator's database!")

        basket_uuid = self._ladm_data.get_basket_uuid(db, coordinator_t_basket)

        return True, coordinator_t_basket, basket_uuid, "Success!"

    def get_coordinator_basket(self, db):
        """ To be used on Coordinator DB export to XTF """
        res, t_basket, basket_uuid, msg = self._validate_single_receiver_in_source_db(db)
        if not res:
            return False, None, msg

        # Set coordinator's t_basket and write it in all DB classes
        res_set_basket = self._set_receiver_t_basket_to_layers(db, t_basket)
        if not res_set_basket:
            msg = QCoreApplication.translate("FDCAdminSynchronizationController",
                                             "There was an error preparing the coordinator's database. See QGIS log for details")
            return False, None, msg

        return res, basket_uuid, msg

    def synchronize_data(self, db, file_path):
        if file_path and os.path.isfile(file_path):
            self.app.settings.fdc_coordinator_xtf_path = file_path
        else:
            return False, QCoreApplication.translate("FDCAdminSynchronizationController",
                                                     "First, choose a valid XTF file to synchronize.")

        # Now, we validate we have a correct single coordinator in the source DB.
        # For that we need a physical DB.

        # Schema import
        ili2db = Ili2DB()
        gpkg_path = tempfile.mktemp() + '.gpkg'
        source_db = GPKGConnector(gpkg_path)
        model = LADMColModelRegistry().model(LADMNames.FIELD_DATA_CAPTURE_MODEL_KEY)
        res_schema_import, msg_schema_import = ili2db.import_schema(source_db, [model.full_name()], create_basket_col=True)
        if not res_schema_import:
            return False, msg_schema_import

        # Import data
        source_db.test_connection()  # To build names object
        res_import_data, msg_import_data = ili2db.import_data(source_db, file_path)
        if not res_import_data:
            return False, msg_import_data

        # Do some checks to the source_db (user table; single coordinator, among others)
        res, t_basket, basket_uuid, msg = self._validate_single_receiver_in_source_db(source_db)
        if not res:
            return False, msg

        # Finally, check that the coordinator in the coordinator's DB is in the admin's DB.
        # Otherwise, it could be an attempt to import a DB from a coordinator of another admin or something.
        fdc_user_layer = self.app.core.get_layer(source_db, source_db.names.FDC_USER_T, load=False)
        res, msg = self._validate_source_receiver_in_target_db(source_db, fdc_user_layer, t_basket)
        if not res:
            return False, msg

        # Run update
        ili2db = Ili2DB()  # We'll change of db, better start an ili2db object from scratch
        res, msg = ili2db.update(db, file_path, FDC_ADMIN_DATASET_NAME)
        if not res:
            return False, QCoreApplication.translate("FDCAdminSynchronizationController",
                                                     "Error synchronizing coordinator's database. Details: {}").format(
                msg)

        return True, QCoreApplication.translate("FDCAdminSynchronizationController",
                                                "Coordinator's data have been synchronized successfully!")
