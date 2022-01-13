# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-06-07
        git sha              : :%H$
        copyright            : (C) 2019 by Leo Cardona (BSF Swissphoto)
                               (C) 2021 by Yesid Polania (BSF Swissphoto)
        email                : leo.cardona.p@gmail.com
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


class SpatialSourceCreatorManager:

    def __init__(self, db, layers, editing_layer):
        self.__db = db
        self.__layers = layers

        self.__editing_layer = editing_layer
        self.names = db.names

        self.__relatable_layers = dict()
        self.__init_selectable_layer_by_type()

    def __init_selectable_layer_by_type(self):
        # TODO Change the name
        self.__relatable_layers[EnumRelatableLayers.PLOT] = self.__layers[self.names.LC_PLOT_T]
        self.__relatable_layers[EnumRelatableLayers.BOUNDARY] = self.__layers[self.names.LC_BOUNDARY_T]
        self.__relatable_layers[EnumRelatableLayers.BOUNDARY_POINT] = self.__layers[self.names.LC_BOUNDARY_POINT_T]
        self.__relatable_layers[EnumRelatableLayers.SURVEY_POINT] = self.__layers[self.names.LC_SURVEY_POINT_T]
        self.__relatable_layers[EnumRelatableLayers.CONTROL_POINT] = self.__layers[self.names.LC_CONTROL_POINT_T]

    def get_layer_by_type(self, layer_type: EnumRelatableLayers):
        return self.__relatable_layers[layer_type] if layer_type in self.__relatable_layers else None

    def finish_feature_creation(self, layerId, features):
        if len(features) != 1:
            # TODO send this info to controller
            # message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed. We should have got only one {} by we have {}").format(self.WIZARD_TOOL_NAME, self.WIZARD_FEATURE_NAME, len(features))
            # self.logger.warning(__name__, "We should have got only one {}, but we have {}".format(self.WIZARD_FEATURE_NAME, len(features)))
            return SpacialSourceFinishFeatureCreationArgs(added_features_amount=len(features))

        feature = features[0]

        if not feature.isValid():
            # TODO send this info to controller
            # self.logger.warning(__name__, "Feature not found in layer Spatial Source...")
            return SpacialSourceFinishFeatureCreationArgs(is_valid=False)

        feature_tid = feature[self.names.T_ID_F]

        feature_ids = LADMData.get_list_of_features_ids(self.__layers[self.names.LC_PLOT_T], self.names.T_ID_F)
        new_features = LADMData.save_relations(self.__layers[self.names.COL_UE_SOURCE_T],
                                                       self.names.COL_UE_SOURCE_T_LC_PLOT_F, feature_ids,
                                                       self.names.COL_UE_SOURCE_T_SOURCE_F, feature_tid)
        # all_new_features.extend(new_features)
        feature_ids = LADMData.get_list_of_features_ids(self.__layers[self.names.LC_BOUNDARY_T], self.names.T_ID_F)

        new_features = LADMData.save_relations(self.__layers[self.names.COL_CCL_SOURCE_T],
                                                       self.names.COL_CCL_SOURCE_T_BOUNDARY_F, feature_ids,
                                                       self.names.COL_CCL_SOURCE_T_SOURCE_F, feature_tid)

        feature_ids = LADMData.get_list_of_features_ids(self.__layers[self.names.LC_BOUNDARY_POINT_T], self.names.T_ID_F)
        new_features = LADMData.save_relations(self.__layers[self.names.COL_POINT_SOURCE_T],
                                                       self.names.COL_POINT_SOURCE_T_LC_BOUNDARY_POINT_F, feature_ids,
                                                       self.names.COL_POINT_SOURCE_T_SOURCE_F, feature_tid)

        feature_ids = LADMData.get_list_of_features_ids(self.__layers[self.names.LC_SURVEY_POINT_T], self.names.T_ID_F)
        new_features = LADMData.save_relations(self.__layers[self.names.COL_POINT_SOURCE_T],
                                                       self.names.COL_POINT_SOURCE_T_LC_SURVEY_POINT_F, feature_ids,
                                                       self.names.COL_POINT_SOURCE_T_SOURCE_F, feature_tid)

        feature_ids = LADMData.get_list_of_features_ids(self.__layers[self.names.LC_CONTROL_POINT_T], self.names.T_ID_F)

        new_features = LADMData.save_relations(self.__layers[self.names.COL_POINT_SOURCE_T],
                                                       self.names.COL_POINT_SOURCE_T_LC_CONTROL_POINT_F, feature_ids,
                                                       self.names.COL_POINT_SOURCE_T_SOURCE_F, feature_tid)

        return SpacialSourceFinishFeatureCreationArgs(True, feature_tid, 1, None)
        # TODO These message
        # if all_new_features:
        #    message = QCoreApplication.translate("WizardTranslations",
        #                                   "The new spatial source (t_id={}) was successfully created and associated with the following features: {}").format(spatial_source_id, feature_ids_dict)
        # else:
        #    message = QCoreApplication.translate("WizardTranslations",
        #                                   "The new spatial source (t_id={}) was successfully created and it wasn't associated with a spatial unit").format(spatial_source_id)

    def get_number_of_selected_features(self):
        feature_count = dict()

        for layer in self.__relatable_layers:
            feature_count[layer] = self.__relatable_layers[layer].selectedFeatureCount()

        return feature_count
