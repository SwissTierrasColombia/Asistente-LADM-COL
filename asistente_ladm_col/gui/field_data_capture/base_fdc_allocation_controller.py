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
from asistente_ladm_col.lib.logger import Logger
from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject,
                              pyqtSignal)

from qgis.core import QgsProcessingFeatureSourceDefinition
import processing

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.gui.field_data_capture.allocation.fdc_data_exporter import FieldDataCaptureDataExporter
from asistente_ladm_col.lib.ladm_col_models import LADMColModelRegistry


class BaseFDCAllocationController(QObject):
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

        self.admin_type = self._ladm_data.get_domain_code_from_value(self._db,
                                                                        self._db.names.FDC_ROLE_TYPE_D,
                                                                        LADMNames.FDC_ROLE_TYPE_D_ADMIN_V)

        self.coordinator_type = self._ladm_data.get_domain_code_from_value(self._db,
                                                                           self._db.names.FDC_ROLE_TYPE_D,
                                                                           LADMNames.FDC_ROLE_TYPE_D_COORDINATOR_V)

        self.surveyor_type = self._ladm_data.get_domain_code_from_value(self._db,
                                                                        self._db.names.FDC_ROLE_TYPE_D,
                                                                        LADMNames.FDC_ROLE_TYPE_D_SURVEYOR_V)

        # Variables to configure (extend) the data export process (useful for Coord-Surveyor scenario)
        self._with_offline_project = False
        self.template_project_path = ''
        self.raster_layer = None

    def initialize_layers(self):
        # A dict of layers that we'll use for the allocation process.
        # Note: all of them will be loaded into QGIS and we'll use them either to filter their features to set specific
        # t_baskets or to set the t_basket for all of their features (and thus, pass them completely to all receivers).
        self._layers = {
            self._db.names.FDC_GENERAL_AREA_T: None,
            self._db.names.FDC_SPECIFIC_AREA_T: None,
            self._db.names.FDC_PLOT_T: None,
            self._db.names.FDC_PARCEL_T: None,
            self._db.names.FDC_USER_T: None,
            self._db.names.FDC_PARTY_DOCUMENT_TYPE_D: None,
            self._db.names.FDC_BUILDING_T: None,
            self._db.names.FDC_BUILDING_UNIT_T: None,
            self._db.names.FDC_CONTROL_POINT_T: None,
            self._db.names.FDC_SURVEY_POINT_T: None,
            self._db.names.FDC_BOUNDARY_POINT_T: None,
            self._db.names.FDC_CONVENTIONAL_QUALIFICATION_T: None,
            self._db.names.FDC_RIGHT_T: None,
            self._db.names.FDC_PARTY_T: None,
            self._db.names.FDC_ADMINISTRATIVE_SOURCE_RIGHT_T: None,
            self._db.names.FDC_ADMINISTRATIVE_SOURCE_T: None,
            self._db.names.FDC_HOUSING_MARKET_OFFERS_T: None,
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

            self.iface.setActiveLayer(self._layers[self._db.names.FDC_LEGACY_PLOT_T])
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

    def legacy_plot_layer(self):
        return self._layers[self._db.names.FDC_LEGACY_PLOT_T]

    def parcel_layer(self):
        return self._layers[self._db.names.FDC_PARCEL_T]

    def control_point_layer(self):
        return self._layers[self._db.names.FDC_CONTROL_POINT_T]

    def survey_point_layer(self):
        return self._layers[self._db.names.FDC_SURVEY_POINT_T]

    def boundary_point_layer(self):
        return self._layers[self._db.names.FDC_BOUNDARY_POINT_T]

    def user_layer(self):
        return self._layers[self._db.names.FDC_USER_T]

    def _layers_to_pass_complete(self):
        """
        A list of layers that should be passed complete (i.e., with no feature filter) to the receivers.

        :return: List of QgsVectorLayers
        """
        return [self.area_layer(), self.boundary_point_layer(), self.survey_point_layer(), self.control_point_layer()]

    def area_layer(self):
        raise NotImplementedError

    def area_layer_display_expression(self):
        return "concat('{} ', {})".format(
            QCoreApplication.translate("BaseFDCAllocationController", "Area"),
            self._db.names.FDC_GENERAL_AREA_T_ID_F)

    def area_layer_identifier_fields(self):
        return [self._db.names.T_ID_F]

    def document_types_table(self):
        return self._layers[self._db.names.FDC_PARTY_DOCUMENT_TYPE_D]

    def update_plot_selection(self, parcel_ids):
        # Note that here we use legacy plots
        plot_ids = self._ladm_data.get_referencing_features(self._db.names,
                                                            self.parcel_layer(),
                                                            self.legacy_plot_layer(),
                                                            self._db.names.FDC_LEGACY_PLOT_T_PARCEL_F,
                                                            fids=parcel_ids)
        self.legacy_plot_layer().selectByIds(plot_ids)

    def get_parcel_numbers_from_selected_plots(self):
        # Note that here we use legacy plots
        plot_ids = self.legacy_plot_layer().selectedFeatureIds()
        return self._ladm_data.get_parcels_related_to_plots_field_data_capture(self._db.names,
                                                                               plot_ids,
                                                                               self.legacy_plot_layer(),
                                                                               self.parcel_layer(),
                                                                               self._db.names.FDC_LEGACY_PLOT_T_PARCEL_F)

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
        return self._ladm_data.discard_parcel_allocation_field_data_capture(self._db, parcel_ids, self.parcel_layer())

    def export_field_data(self, export_dir):
        names = self._db.names

        # 1) Get receivers' t_basket that actually have at least one parcel assigned (basically, an INNER JOIN)
        # For that: Go to parcel layer and get uniques, then filter that list comparing it with receiver ids from users
        receivers_dict = self._ladm_data.get_fdc_receivers_data(names, self.user_layer(),
                                                                self._get_receiver_referenced_field(),  # t_basket
                                                                self.receiver_type, full_name=False)
        receiver_field_idx = self.parcel_layer().fields().indexOf(self._get_parcel_field_referencing_receiver())
        receiver_ids_in_parcels = self.parcel_layer().uniqueValues(receiver_field_idx)

        # Only t_basket of receivers with allocated parcels (remember that keys are receiver's t_baskets)
        basket_t_ids = [k for k in receivers_dict.keys() if k in receiver_ids_in_parcels]

        # 2) Get baskets info to export XTFs via ili2db (basically, an INNER JOIN)
        #    basket_receiver_dict: {t_basket: {t_ili_tid: receiver_name}}
        basket_table = self._ladm_data.get_basket_table(self._db)
        basket_receiver_dict = {f[names.T_ID_F]: {'t_ili_tid': f[names.T_ILI_TID_F],
                                                  'name': receivers_dict[f[names.T_ID_F]][0]}
                                for f in basket_table.getFeatures() if f[names.T_ID_F] in basket_t_ids}

        if not basket_receiver_dict:
            return False, QCoreApplication.translate("BaseFDCAllocationController",
                                                     "First allocate at least one parcel.")

        # 3) IMPORTANT: Before setting receiver's t_basket to objects related to allocated parcels,
        #               let's reset t_basket in all tables, setting them to the default basket.
        default_basket_id, msg = self._ladm_data.get_or_create_default_ili2db_basket(self._db)
        if default_basket_id is None:
            return False, msg

        # Keep parcel and user tables untouched, because there we have the allocation info! Domains don't have baskets!
        domains = [k for k,v in self._layers.items() if v.fields().indexOf(names.T_BASKET_F) < 0]
        layers_to_not_reset = domains + [names.FDC_PARCEL_T, names.FDC_USER_T]
        layers_to_reset = [v for k, v in self._layers.items() if k not in layers_to_not_reset]
        res_reset = self._ladm_data.update_t_basket_in_layers(self._db, layers_to_reset, default_basket_id)
        if not res_reset:
            return False, QCoreApplication.translate("BaseFDCAllocationController",
                                                     "Could not write default basket id ({}) in field data layers.").format(default_basket_id)

        # 4) Now that we've reset t_baskets in all tables, proceed writing
        #    each receiver's t_basket only to his associated DB objects.
        Logger().info(__name__, "Setting basket ids to db objects related to {} receivers...".format(len(basket_t_ids)))

        # Prepare basket exporter
        basket_exporter = FieldDataCaptureDataExporter(self._db,
                                                       len(basket_receiver_dict),
                                                       export_dir,
                                                       self._with_offline_project,
                                                       self.template_project_path,
                                                       self.raster_layer)
        basket_exporter.total_progress_updated.connect(self.export_field_data_progress)  # Signal chaining
        self.export_field_data_progress.emit(1)  # Let users know we started already

        for t_basket, data in basket_receiver_dict.items():
            # Now set basket id for allocated parcels' related features
            res, msg = self._ladm_data.set_basket_for_features_related_to_allocated_parcels_field_data_capture(
                self._db,
                t_basket,
                data['name'],
                self._get_parcel_field_referencing_receiver(),
                self._layers,
                self._layers_to_pass_complete())
            if not res:
                return False, msg

            # Now, export the current basket to XTF
            res_xtf, msg_xtf = basket_exporter.export_basket(data['t_ili_tid'], data['name'])
            if not res_xtf:
                return res, msg_xtf

        return True, self._successful_export_message(len(basket_receiver_dict), export_dir)

    def _successful_export_message(self, count, export_dir):
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

    def _get_fdc_dataset(self, dataset_name):
        return self._ladm_data.get_or_create_ili2db_dataset_t_id(self._db, dataset_name)  # t_id, msg

    def get_basket_id_for_new_receiver(self):
        """
        Get the basket id for the new receiver.

        For the admin-coord allocation, the basket id will always be a new one.
        For the coord-surveyor allocation, the basket id will be the unique value of the user.t_basket field.

        :return: Tuple --> basket_id, msg (useful in case of failure, e.g., because there are several t_basket values
                                           in a coord-surveyor scenario)
        """
        raise NotImplementedError

    def _get_basket_id_for_new_receiver(self, dataset_name):
        # 1. Make sure we've got the FDC dataset (varies depending on role: admin or coordinator)
        dataset_t_id, msg = self._get_fdc_dataset(dataset_name)
        if dataset_t_id is None:
            return None, QCoreApplication.translate("BaseFDCAllocationController", "Details: The Field Data Capture dataset does not exist and couldn't be created!")

        # 2. Get a new basket for such dataset
        fdc_model = LADMColModelRegistry().model(LADMNames.FIELD_DATA_CAPTURE_MODEL_KEY).full_name()
        topic_name = "{}.{}".format(fdc_model, LADMNames.FDC_TOPIC_NAME)
        basket_feature, msg = self._ladm_data.create_ili2db_basket(self._db, dataset_t_id, topic_name)

        if basket_feature is None:
            return None, QCoreApplication.translate("BaseFDCAllocationController", "Details: Basket could not be created!")

        basket_t_id = basket_feature[self._db.names.T_ID_F]

        return basket_t_id, "Success!"

    def get_coordinator_basket_id_for_new_receiver(self):
        """
        Get the basket id of the new receiver's coordinator.

        For the admin-coord allocation, the coordinator basket id will always be NULL (we don't store the admin info).
        For the coord-surveyor allocation, the basket id will be the coordinator's basket_id (role: coordinator).

        :return: Tuple --> coordinator_basket_id, msg (useful in case of failure, e.g., because there are several
                                                       coordinator in a coord-surveyor scenario)
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
        return self._ladm_data.get_count_of_not_allocated_parcels_to_receivers_field_data_capture(self.db().names,
                                                                                                  self.receiver_type,
                                                                                                  self.parcel_layer(),
                                                                                                  self.user_layer())
    def get_document_types(self):
        return self._ladm_data.get_document_types(self._db.names, self.document_types_table())

    def zoom_to_area(self, t_ids):
        self.app.gui.zoom_to_features(self.area_layer(), t_ids={self._db.names.T_ID_F: t_ids})

    def select_by_area(self, t_id):
        """
        Select legacy plots by area.

        :param t_id: Area's t_id
        """
        self.area_layer().selectByExpression("{} = {}".format(self._db.names.T_ID_F, t_id))
        processing.run("native:selectbylocation", {'INPUT': self.legacy_plot_layer(),
                                                   'PREDICATE': [0],  # intersects
                                                   'INTERSECT': QgsProcessingFeatureSourceDefinition(self.area_layer().id(), True),
                                                   'METHOD': 0})  # New selection
        self.area_layer().removeSelection()