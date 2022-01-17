# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-09-10
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BSF Swissphoto)
                               (C) 2018 by Sergio Ramírez (Incige SAS)
                               (C) 2019 by Leo Cardona (BSF Swissphoto)
                               (C) 2021 by Yesid Polania (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
                               sergio.ramirez@incige.com
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
from asistente_ladm_col.gui.wizards.model.common.args.model_args import SpacialSourceFinishFeatureCreationArgs
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData


class RrrCreatorManager:

    def __init__(self, db, layers, editing_layer, editing_layer_name):
        self.__db = db
        self.__layers = layers

        self.__editing_layer = editing_layer
        self.__editing_layer_name = editing_layer_name

        self.names = db.names

        self.__relatable_layers = dict()
        self.__init_selectable_layer_by_type()

    def __init_selectable_layer_by_type(self):
        self.__relatable_layers[EnumRelatableLayers.ADMINISTRATIVE_SOURCE] = \
            self.__layers[self.names.LC_ADMINISTRATIVE_SOURCE_T]

    def get_layer_by_type(self, layer_type: EnumRelatableLayers):
        return self.__relatable_layers[layer_type] if layer_type in self.__relatable_layers else None

    def finish_feature_creation(self, layerId, features):
        if len(features) != 1:
            return SpacialSourceFinishFeatureCreationArgs(added_features_amount=len(features))

        fid = features[0].id()

        # editing layer Name?
        if not self.__editing_layer.getFeature(fid).isValid():
            # self.logger.warning(__name__, "Feature not found in layer {}...".format(self.__editing_layer_name))
            # TODO send this info to controller
            return SpacialSourceFinishFeatureCreationArgs(SpacialSourceFinishFeatureCreationArgs(is_valid=False))

        # feature_rrr_id: generic name used for represent id for right, restriction
        # feature_rrr_id = self._layers[self.EDITING_LAYER_NAME].getFeature(fid)[self.names.T_ID_F]
        feature_tid = self.__editing_layer.getFeature(fid)[self.__db.names.T_ID_F]

        administrative_source_ids = LADMData.get_list_of_features_ids(self.__layers[self.names.LC_ADMINISTRATIVE_SOURCE_T], self.names.T_ID_F)

        # Fill rrrfuente table
        new_features = []
        attr_fk = None

        if self.__editing_layer_name == self.names.LC_RIGHT_T:
            attr_fk = self.names.COL_RRR_SOURCE_T_LC_RIGHT_F
        elif self.__editing_layer_name == self.names.LC_RESTRICTION_T:
            attr_fk = self.names.COL_RRR_SOURCE_T_LC_RESTRICTION_F

        new_features = LADMData.save_relations(self.__layers[self.names.COL_RRR_SOURCE_T],
                                               self.names.COL_RRR_SOURCE_T_SOURCE_F,
                                               administrative_source_ids, attr_fk, feature_tid)
        return SpacialSourceFinishFeatureCreationArgs(True, feature_tid, 1, None)
        # TODO log messages is missing

    def get_number_of_selected_features(self):
        feature_count = dict()

        for layer in self.__relatable_layers:
            feature_count[layer] = self.__relatable_layers[layer].selectedFeatureCount()

        return feature_count
