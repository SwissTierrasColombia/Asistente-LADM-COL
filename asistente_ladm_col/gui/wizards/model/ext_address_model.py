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
from asistente_ladm_col.config.enums import EnumRelatableLayers
from asistente_ladm_col.gui.wizards.model.common.args.model_args import (ExecFormAdvancedArgs,
                                                                         FinishFeatureCreationArgs)


class ExtAddressManager:

    def __init__(self, db, layers, editing_layer, iface):   # , app, logger):
        self.__db = db
        self.__layers = layers

        self.__editing_layer = editing_layer

        self.__iface = iface

        self.__relatable_layers = dict()
        self.__init_selectable_layer_by_type()
        self.type_of_selected_layer_to_associate = None

    def finish_feature_creation(self, layerId, features):
        fid = features[0].id()
        is_valid = False
        feature_tid = None

        if self.__editing_layer.getFeature(fid).isValid():
            is_valid = True
            feature_tid = self.__editing_layer.getFeature(fid)[self.__db.names.T_ID_F]

        return FinishFeatureCreationArgs(is_valid, feature_tid)

    def exec_form_advanced(self, args: ExecFormAdvancedArgs):
        layer = args.layer
        feature = None
        for f in layer.editBuffer().addedFeatures():
            feature = layer.editBuffer().addedFeatures()[f]
            break

        spatial_unit_field_idx = None

        if feature:
            # Get t_id of spatial unit to associate

            selected_layer_to_pick_features =\
                self.__relatable_layers[self.type_of_selected_layer_to_associate]

            feature_id = selected_layer_to_pick_features.selectedFeatures()[0][self.__db.names.T_ID_F]
            fid = feature.id()

            if self.type_of_selected_layer_to_associate == EnumRelatableLayers.PLOT:
                spatial_unit_field_idx = layer.getFeature(fid).fieldNameIndex(self.__db.names.EXT_ADDRESS_S_LC_PLOT_F)
            elif self.type_of_selected_layer_to_associate == EnumRelatableLayers.BUILDING:
                spatial_unit_field_idx = layer.getFeature(fid).fieldNameIndex(self.__db.names.EXT_ADDRESS_S_LC_BUILDING_F)
            elif self.type_of_selected_layer_to_associate == EnumRelatableLayers.BUILDING_UNIT:
                spatial_unit_field_idx = layer.getFeature(fid).fieldNameIndex(self.__db.names.EXT_ADDRESS_S_LC_BUILDING_UNIT_F)

        if spatial_unit_field_idx:
            # assign the relation with the spatial unit
            layer.changeAttributeValue(fid, spatial_unit_field_idx, feature_id)
        else:
            # if the field of the spatial unit does not exist
            layer.rollBack()

            # TODO Association failed
            # self.__notify_association_failed()

    def __init_selectable_layer_by_type(self):
        # TODO Change the name
        self.__relatable_layers[EnumRelatableLayers.PLOT] = self.__layers[self.__db.names.LC_PLOT_T]
        self.__relatable_layers[EnumRelatableLayers.BUILDING] = self.__layers[self.__db.names.LC_BUILDING_T]
        self.__relatable_layers[EnumRelatableLayers.BUILDING_UNIT] = self.__layers[self.__db.names.LC_BUILDING_UNIT_T]

    def get_active_layer_type(self):
        for item_type in self.__relatable_layers:
            if self.__relatable_layers[item_type] == self.__iface.activeLayer():
                return item_type

        return None

    def get_number_of_selected_features(self):
        feature_count = dict()

        for layer in self.__relatable_layers:
            feature_count[layer] = self.__relatable_layers[layer].selectedFeatureCount()

        return feature_count

    def get_layer_by_type(self, layer_type: EnumRelatableLayers):
        return self.__relatable_layers[layer_type] if layer_type in self.__relatable_layers else None
