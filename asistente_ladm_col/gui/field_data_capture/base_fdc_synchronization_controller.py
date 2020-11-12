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
from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject,
                              pyqtSignal)

from asistente_ladm_col.app_interface import AppInterface


class BaseFDCSynchronizationController(QObject):
    field_data_capture_layer_removed = pyqtSignal()

    def __init__(self, iface, db, ladm_data):
        QObject.__init__(self)
        self.iface = iface
        self._db = db
        self._ladm_data = ladm_data

        self.app = AppInterface()

        self.receiver_ilicode = ''
        self.receiver_type = None

        self._layers = dict()
        self._receiver_layers = dict()

        self.initialize_layers()

    def initialize_layers(self):
        # A dict of layers that we'll use for the synchronization process (just as context)
        self._layers = {
            self._db.names.FDC_PLOT_T: None,
            self._db.names.FDC_PARCEL_T: None,
            self._db.names.FDC_USER_T: None,
            self._db.names.FDC_PARTY_DOCUMENT_TYPE_D: None
        }

        # A dict of layers to which we should set receiver's t_basket before synchronizing.
        # Note: These layers will get a t_basket for all their features, with no filter.
        self._receiver_layers = {
            self._db.names.FDC_ADMINISTRATIVE_SOURCE_T: None,
            self._db.names.FDC_BUILDING_T: None,
            self._db.names.FDC_BUILDING_UNIT_T: None,
            self._db.names.FDC_CONVENTIONAL_QUALIFICATION_T: None,
            self._db.names.FDC_FMI_CHANGE_T: None,
            self._db.names.FDC_HOUSING_MARKET_OFFERS_T: None,
            self._db.names.FDC_PARCEL_T: None,
            self._db.names.FDC_PARCEL_COOWNERSHIP_T: None,
            self._db.names.FDC_PARCEL_NUMBERS_CHANGE_T: None,
            self._db.names.FDC_PARTY_T: None,
            self._db.names.FDC_PLOT_T: None,
            self._db.names.FDC_BOUNDARY_POINT_T: None,
            self._db.names.FDC_CONTROL_POINT_T: None,
            self._db.names.FDC_SURVEY_POINT_T: None,
            self._db.names.FDC_RIGHT_T: None,
            self._db.names.FDC_VISIT_CONTACT_T: None,
            self._db.names.FDC_LEGACY_PLOT_T: None,
            self._db.names.FDC_LEGACY_BUILDING_T: None,
            self._db.names.FDC_LEGACY_BUILDING_UNIT_T: None
        }

    def add_layers(self, force=False):
        # We can pick any required layer, if it is None, no prior load has been done, otherwise skip...
        if self._layers[self._db.names.FDC_PLOT_T] is None or force:
            self.app.gui.freeze_map(True)

            res = self.app.core.get_layers(self._db, self._layers, load=True, emit_map_freeze=False)
            if not res:
                return False

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

        return True

    def get_receiver_layer_list(self, db):
        layers = list(self._receiver_layers.values())
        if None in layers:
            self.app.core.get_layers(db, self._receiver_layers, load=False)

        if not self._receiver_layers:
            self.logger.critical(__name__, "Receiver layers could not be obtained!")
            return dict()

        return list(self._receiver_layers.values())

    def db(self):
        return self._db

    def plot_layer(self):
        return self._layers[self._db.names.FDC_PLOT_T]

    def parcel_layer(self):
        return self._layers[self._db.names.FDC_PARCEL_T]

    def user_layer(self):
        return self._layers[self._db.names.FDC_USER_T]

    def _validate_single_receiver_in_source_db(self, db):
        raise NotImplementedError

    def _validate_source_receiver_in_target_db(self, source_db, fdc_source_user_layer, t_basket):
        field_idx = self.user_layer().fields().indexOf(self._db.names.T_ILI_TID_F)
        target_t_ili_tids = self.user_layer().uniqueValues(field_idx)

        receiver_role = self._ladm_data.get_domain_code_from_value(source_db,
                                                                   source_db.names.FDC_ROLE_TYPE_D,
                                                                   self.receiver_ilicode)

        # Get {t_basket: (name, t_ili_tid), ...} for the receiver role (we expect a single user here!)
        receivers_source_db = self._ladm_data.get_fdc_receivers_data(source_db.names,
                                                                     fdc_source_user_layer,
                                                                     source_db.names.T_BASKET_F,
                                                                     receiver_role, True, source_db.names.T_ILI_TID_F)
        receiver_name = receivers_source_db[t_basket][0]
        source_t_ili_tid = receivers_source_db[t_basket][1]

        if source_t_ili_tid not in target_t_ili_tids:
            return False, QCoreApplication.translate("BaseFDCSynchronizationController",
                                                     "Invalid database! We couldn't find the receiver '{}' ({}) in the original database. Make sure you're synchronizing the correct XTF.").format(
                receiver_name,
                source_t_ili_tid)

        return True, 'Success!'

    def _set_receiver_t_basket_to_layers(self, db, t_basket):
        return self._ladm_data.update_t_basket_in_layers(db, self.get_receiver_layer_list(db), t_basket)

    def synchronize_data(self, db, file_path):
        raise NotImplementedError