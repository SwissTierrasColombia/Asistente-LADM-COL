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

from asistente_ladm_col.config.general_config import FDC_COORDINATOR_DATASET_NAME
from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.gui.field_data_capture.base_fdc_synchronization_controller import BaseFDCSynchronizationController
from asistente_ladm_col.lib.db.gpkg_connector import GPKGConnector
from asistente_ladm_col.lib.qgis_model_baker.ili2db import Ili2DB


class FDCCoordinatorSynchronizationController(BaseFDCSynchronizationController):
    def __init__(self, iface, db, ladm_data):
        BaseFDCSynchronizationController.__init__(self, iface, db, ladm_data)

        self.receiver_ilicode = LADMNames.FDC_ROLE_TYPE_D_SURVEYOR_V
        self.receiver_type = self._ladm_data.get_domain_code_from_value(self._db,
                                                                        self._db.names.FDC_ROLE_TYPE_D,
                                                                        self.receiver_ilicode)

    def _validate_single_receiver_in_source_db(self, db):
        """
        Validate that we have a single surveyor and that she is in the coordinator's database

        :param db: Surveyor's database (different from self._db, which is from the coordinator!)
        :return: bool result, t_basket, basket_uuid, msg
        """
        fdc_user_layer = self.app.core.get_layer(db, db.names.FDC_USER_T, load=False)
        if not fdc_user_layer:
            return False, None, None, QCoreApplication.translate("FDCCoordinatorSynchronizationController",
                                                           "Invalid database! User table not found in surveyor's database!")

        # Get {t_basket: (name, role), ...} for ALL receivers
        receivers_source_db = self._ladm_data.get_fdc_receivers_data(db.names,
                                                                     fdc_user_layer,
                                                                     db.names.T_BASKET_F,
                                                                     None, True, db.names.FDC_USER_T_ROLE_F)

        if len(receivers_source_db) > 1:
            return False, None, None, QCoreApplication.translate("FDCCoordinatorSynchronizationController",
                                                           "Invalid database! There are more users than we expect in the surveyor's database.")
        if len(receivers_source_db) == 0:
            return False, None, None, QCoreApplication.translate("FDCCoordinatorSynchronizationController",
                                                           "Invalid database! There are no users in the surveyor's database.")

        t_basket = list(receivers_source_db.keys())[0]
        role = receivers_source_db[t_basket][1]

        # Check that role is surveyor
        surveyor_role = self._ladm_data.get_domain_code_from_value(db,
                                                                   db.names.FDC_ROLE_TYPE_D,
                                                                   self.receiver_ilicode)
        if role != surveyor_role:
            return False, None, None, QCoreApplication.translate("FDCCoordinatorSynchronizationController",
                                                     "Invalid database! The only user in the database must be a surveyor, but it is not (it is {}).").format(role)

        # Check that the surveyor (t_ili_tid) in the surveyor's DB is in the coordinator's DB.
        # Otherwise, it could be an attempt to import a DB from a surveyor of another coordinator.
        res, msg = self._validate_source_receiver_in_target_db(db, fdc_user_layer, t_basket)
        if not res:
            return False, None, None, msg

        basket_uuid = self._ladm_data.get_basket_uuid(db, t_basket)

        return True, t_basket, basket_uuid, "Success!"

    def synchronize_data(self, db, file_path):
        self.app.gui.clear_message_bar()

        # Validate db structure
        db_tmp = GPKGConnector(file_path)
        res, code, msg = db_tmp.test_connection()
        self.app.settings.fdc_surveyor_gpkg_path = file_path

        if not res:
            return False, QCoreApplication.translate("SynchronizeDataCoordinatorInitialPanelWidget",
                                                     "There was an error validating the GeoPackage database. Details: {}").format(
                msg)

        # Validate that we have a single user, and it's a surveyor. Also, get his t_basket
        res, t_basket, basket_uuid, msg = self._validate_single_receiver_in_source_db(db_tmp)
        if not res:
            return False, QCoreApplication.translate("SynchronizeDataCoordinatorInitialPanelWidget", msg)

        # Set surveyor's t_basket and write it in all DB classes
        res = self._set_receiver_t_basket_to_layers(db_tmp, t_basket)
        if not res:
            return False, QCoreApplication.translate("SynchronizeDataCoordinatorInitialPanelWidget",
                                                     "There was an error preparing the GeoPackage database. See QGIS log for details")

        # Generate XTF
        ili2db = Ili2DB()
        xtf_path = tempfile.mktemp() + '.xtf'
        res, msg = ili2db.export(db_tmp, xtf_path, baskets=[basket_uuid])
        if not res:
            return False, QCoreApplication.translate("SynchronizeDataCoordinatorInitialPanelWidget",
                                                     "Error synchronizing surveyor's database. Details: {}").format(msg)

        # Run update
        res, msg = ili2db.update(db, xtf_path, FDC_COORDINATOR_DATASET_NAME)
        if not res:
            return False, QCoreApplication.translate("SynchronizeDataCoordinatorInitialPanelWidget",
                                                     "Error synchronizing surveyor's database. Details: {}").format(msg)

        return True, QCoreApplication.translate("SynchronizeDataCoordinatorInitialPanelWidget",
                                                "Surveyor's data have been synchronized successfully!")
