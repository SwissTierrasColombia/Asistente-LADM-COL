# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-09-10
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BSF Swissphoto)
                               (C) 2018 by Sergio Ramírez (Incige SAS)
                               (C) 2018 by Jorge Useche (Incige SAS)
                               (C) 2018 by Jhon Galindo (Incige SAS)
                               (C) 2019 by Leo Cardona (BSF Swissphoto)
                               (C) 2021 by Yesid Polania (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
                               sergio.ramirez@incige.com
                               naturalmentejorge@gmail.com
                               jhonsigpjc@gmail.com
                               leo.cardona.p@gmail.com
                               yesidpol.3@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
 """
from asistente_ladm_col.config.enums import (EnumRelatableLayers,
                                             EnumRelationshipType)
from asistente_ladm_col.config.layer_config import LayerConfig
from asistente_ladm_col.gui.wizards.model.common.args.model_args import (FeatureFormArgs,
                                                                         ParcelFinishFeatureCreationArgs)
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData


class ParcelCreatorManager:

    def __init__(self, db, layers, editing_layer):
        self.__db = db
        self.__layers = layers

        self.__editing_layer = editing_layer

        self.__constraint_types_of_parcels = LayerConfig.get_constraint_types_of_parcels(self.__db.names)

        self.parcel_type_ili_code = None

        self.__relatable_layers = dict()
        self.__init_selectable_layer_by_type()

    # TODO ref2 Cambiar el nombre
    def exec_form_advanced(self, args: FeatureFormArgs):
        fid = args.feature.id()

        # assigns the type of parcel before to creating it
        parcel_condition_field_idx = args.layer.getFeature(fid).fieldNameIndex(
            self.__db.names.LC_PARCEL_T_PARCEL_TYPE_F)
        args.layer.changeAttributeValue(fid, parcel_condition_field_idx,
                                        self.__get_ili_code_id_dict()[self.parcel_type_ili_code])

    def set_parcel_type(self, feature):
        parcel_conditions = self.get_type_parcel_conditions()
        value = parcel_conditions[self.parcel_type_ili_code]
        feature[self.__db.names.LC_PARCEL_T_PARCEL_TYPE_F] = value

    # TODO ref2 Cambiar el nombre
    def finish_feature_creation(self, layerId, features):
        if len(features) != 1:
            # TODO send this info to controller
            # message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed. We should have got only one {} by we have {}").format(self.WIZARD_TOOL_NAME, self.WIZARD_FEATURE_NAME, len(features))
            # self.logger.warning(__name__, "We should have got only one {}, but we have {}".format(self.WIZARD_FEATURE_NAME, len(features)))
            return ParcelFinishFeatureCreationArgs(added_features_amount=len(features))

        if not self.is_each_layer_valid():
            return ParcelFinishFeatureCreationArgs(valid_constraints=False)

        feature = features[0]

        if not feature.isValid():
            # TODO send this info to controller
            # self.logger.warning(__name__, "Feature not found in layer Spatial Source...")
            return ParcelFinishFeatureCreationArgs(is_valid=False)

        # TODO What is the difference?
        # feature_tid = feature[self.__db.names.T_ID_F]
        feature_tid = self.__editing_layer.getFeature(feature.id())[self.__db.names.T_ID_F]

        plot_ids = list()
        building_ids = list()
        building_unit_ids = list()

        # Apply restriction to the selection

        # add plot associated
        if self.__db.names.LC_PLOT_T in self.__constraint_types_of_parcels[self.parcel_type_ili_code]:
            add_features = self.__constraint_types_of_parcels[self.parcel_type_ili_code][
                               self.__db.names.LC_PLOT_T] is not None
        else:
            add_features = True

        if add_features:
            plot_ids = LADMData.get_list_of_features_ids(self.__layers[self.__db.names.LC_PLOT_T],
                                                                 self.__db.names.T_ID_F)

        new_features = LADMData.save_relations(self.__layers[self.__db.names.COL_UE_BAUNIT_T],
                                                       self.__db.names.COL_UE_BAUNIT_T_LC_PLOT_F, plot_ids,
                                                       self.__db.names.COL_UE_BAUNIT_T_PARCEL_F, feature_tid)

        # add building associated
        if self.__db.names.LC_BUILDING_T in self.__constraint_types_of_parcels[self.parcel_type_ili_code]:
            add_features = self.__constraint_types_of_parcels[self.parcel_type_ili_code][
                               self.__db.names.LC_BUILDING_T] is not None
        else:
            add_features = True

        if add_features:
            building_ids = LADMData.get_list_of_features_ids(self.__layers[self.__db.names.LC_BUILDING_T],
                                                                     self.__db.names.T_ID_F)

        new_features = LADMData.save_relations(self.__layers[self.__db.names.COL_UE_BAUNIT_T],
                                                       self.__db.names.COL_UE_BAUNIT_T_LC_BUILDING_F, building_ids,
                                                       self.__db.names.COL_UE_BAUNIT_T_PARCEL_F, feature_tid)

        # add building unit associated
        if self.__db.names.LC_BUILDING_UNIT_T in self.__constraint_types_of_parcels[self.parcel_type_ili_code]:
            add_features = self.__constraint_types_of_parcels[self.parcel_type_ili_code][
                               self.__db.names.LC_BUILDING_UNIT_T] is not None
        else:
            add_features = True

        if add_features:
            building_unit_ids = LADMData.get_list_of_features_ids(
                self.__layers[self.__db.names.LC_BUILDING_UNIT_T],
                self.__db.names.T_ID_F)

        new_features = LADMData.save_relations(self.__layers[self.__db.names.COL_UE_BAUNIT_T],
                                                       self.__db.names.COL_UE_BAUNIT_T_LC_BUILDING_UNIT_F,
                                                       building_unit_ids, self.__db.names.COL_UE_BAUNIT_T_PARCEL_F,
                                                       feature_tid)

        return ParcelFinishFeatureCreationArgs(True, feature_tid, 1, None)

    def get_type_parcel_conditions(self):
        result = dict()

        for feature in self.__layers[self.__db.names.LC_CONDITION_PARCEL_TYPE_D].getFeatures():
            if feature[self.__db.names.ILICODE_F] in self.__constraint_types_of_parcels:
                result[feature[self.__db.names.ILICODE_F]] = feature[self.__db.names.DISPLAY_NAME_F]
        return result

    def __get_ili_code_id_dict(self):
        result = dict()
        for feature in self.__layers[self.__db.names.LC_CONDITION_PARCEL_TYPE_D].getFeatures():
            if feature[self.__db.names.ILICODE_F] in self.__constraint_types_of_parcels:
                result[feature[self.__db.names.ILICODE_F]] = feature[self.__db.names.T_ID_F]

        return result

    # TODO name is not clear
    def get_layer_status(self):
        result = dict()

        for spatial_unit in self.__relatable_layers:
            is_layer_valid = self.__is_layer_valid(spatial_unit)
            if is_layer_valid is not None:
                result[spatial_unit] = is_layer_valid

        return result

    def __is_layer_valid(self, spatial_unit_enum: EnumRelatableLayers):
        constraint = \
            self.__constraint_types_of_parcels[self.parcel_type_ili_code][
                spatial_unit_enum.get_db_name(self.__db.names)]
        layer = self.__relatable_layers[spatial_unit_enum]
        is_valid = None

        if constraint == EnumRelationshipType.ONE:
            is_valid = layer.selectedFeatureCount() == 1
        elif constraint == EnumRelationshipType.ONE_OR_MANY:
            is_valid = layer.selectedFeatureCount() >= 1
        elif constraint == EnumRelationshipType.MANY:
            is_valid = True

        return is_valid

    def get_number_of_selected_features(self):
        feature_count = dict()

        for layer in self.__relatable_layers:
            feature_count[layer] = self.__relatable_layers[layer].selectedFeatureCount()

        return feature_count

    def __init_selectable_layer_by_type(self):
        # TODO Change the name
        self.__relatable_layers[EnumRelatableLayers.PLOT] = self.__layers[self.__db.names.LC_PLOT_T]
        self.__relatable_layers[EnumRelatableLayers.BUILDING] = self.__layers[self.__db.names.LC_BUILDING_T]
        self.__relatable_layers[EnumRelatableLayers.BUILDING_UNIT] = self.__layers[self.__db.names.LC_BUILDING_UNIT_T]

    def is_each_layer_valid(self):
        result = True
        for key, layer_status in self.get_layer_status().items():
            if not layer_status:
                result = False
                break
        return result

    def get_layer_by_type(self, layer_type: EnumRelatableLayers):
        return self.__relatable_layers[layer_type] if layer_type in self.__relatable_layers else None
