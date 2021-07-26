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
from asistente_ladm_col.config.general_config import WIZARD_LAYERS
from asistente_ladm_col.gui.wizards.model.common.args.model_args import SpacialSourceFinishFeatureCreationArgs
from asistente_ladm_col.gui.wizards.model.common.association_utils import AssociationUtils
from asistente_ladm_col.gui.wizards.model.common.layer_remove_signals_manager import LayerRemovedSignalsManager
from asistente_ladm_col.gui.wizards.model.common.select_features_by_expression_dialog_wrapper import \
    SelectFeatureByExpressionDialogWrapper
from asistente_ladm_col.gui.wizards.model.common.select_features_on_map_wrapper import SelectFeaturesOnMapWrapper
from asistente_ladm_col.gui.wizards.model.single_wizard_model import SingleWizardModel
from asistente_ladm_col.gui.wizards.view.common.view_enum import EnumRelatableLayers


class SpatialSourceModel(SingleWizardModel):

    def __init__(self, iface, db, wiz_config):
        super().__init__(iface, db, wiz_config)

        self.__features_on_map_observer_list = list()
        self.__feature_selector_by_expression_observers = list()
        self.__layer_removed_observers = list()

        self._layers = wiz_config[WIZARD_LAYERS]
        self.names = db.names

        self.__iface = iface

        self.__feature_selector_on_map = SelectFeaturesOnMapWrapper(self.__iface, self._logger)
        self.__feature_selector_on_map.register_observer(self)

        self.__feature_selector_by_expression = SelectFeatureByExpressionDialogWrapper(self.__iface)
        self.__feature_selector_by_expression.register_observer(self)

        self.__relatable_layers = dict()
        self.__init_selectable_layer_by_type()

        self.__layer_remove_manager = LayerRemovedSignalsManager(self._layers, self)

    def __init_selectable_layer_by_type(self):
        # TODO Change the name
        self.__relatable_layers[EnumRelatableLayers.PLOT] = self._layers[self.names.LC_PLOT_T]
        self.__relatable_layers[EnumRelatableLayers.BOUNDARY] = self._layers[self.names.LC_BOUNDARY_T]
        self.__relatable_layers[EnumRelatableLayers.BOUNDARY_POINT] = self._layers[self.names.LC_BOUNDARY_POINT_T]
        self.__relatable_layers[EnumRelatableLayers.SURVEY_POINT] = self._layers[self.names.LC_SURVEY_POINT_T]
        self.__relatable_layers[EnumRelatableLayers.CONTROL_POINT] = self._layers[self.names.LC_CONTROL_POINT_T]

    def select_features_on_map(self, option_type: EnumRelatableLayers):
        # TODO is this execution right?
        self.__layer_remove_manager.reconnect_signals()
        # TODO Exception if layer does not exist
        layer = self.__relatable_layers[option_type]
        self.__feature_selector_on_map.select_features_on_map(layer)

    def select_features_by_expression(self, option_type: EnumRelatableLayers):
        # TODO Check if layer exists in self._layers
        layer = self.__relatable_layers[option_type]
        self.__feature_selector_by_expression.select_features_by_expression(layer)

    def map_tool_changed(self):
        self.__notify_map_tool_changed()

    def features_selected(self):
        self.__notify_features_selected()

    def feature_selection_by_expression_changed(self):
        self.__notify_feature_selection_by_expression_changed()

    def dispose(self):
        self.__layer_remove_manager.disconnect_signals()
        self.__feature_selector_on_map.init_map_tool()
        super().dispose()
        self.__feature_selector_on_map.disconnect_signals()

    def finish_feature_creation(self, layerId, features):
        if len(features) != 1:
            # TODO send this info to controller
            # message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed. We should have got only one {} by we have {}").format(self.WIZARD_TOOL_NAME, self.WIZARD_FEATURE_NAME, len(features))
            # self.logger.warning(__name__, "We should have got only one {}, but we have {}".format(self.WIZARD_FEATURE_NAME, len(features)))
            self._notify_finish_feature_creation(
                SpacialSourceFinishFeatureCreationArgs(added_features_amount=len(features)))
            return

        feature = features[0]

        if not feature.isValid():
            # TODO send this info to controller
            # self.logger.warning(__name__, "Feature not found in layer Spatial Source...")
            self._notify_finish_feature_creation(
                SpacialSourceFinishFeatureCreationArgs(is_valid=False))
            return

        feature_tid = feature[self.names.T_ID_F]

        feature_ids = AssociationUtils.get_list_of_features_ids(self._layers[self.names.LC_PLOT_T], self.names.T_ID_F)
        new_features = AssociationUtils.save_relations(self._layers[self.names.COL_UE_SOURCE_T],
                                                       self.names.COL_UE_SOURCE_T_LC_PLOT_F, feature_ids,
                                                       self.names.COL_UE_SOURCE_T_SOURCE_F, feature_tid)
        # all_new_features.extend(new_features)
        feature_ids = AssociationUtils.get_list_of_features_ids(self._layers[self.names.LC_BOUNDARY_T], self.names.T_ID_F)

        new_features = AssociationUtils.save_relations(self._layers[self.names.COL_CCL_SOURCE_T],
                                                       self.names.COL_CCL_SOURCE_T_BOUNDARY_F, feature_ids,
                                                       self.names.COL_CCL_SOURCE_T_SOURCE_F, feature_tid)

        feature_ids = AssociationUtils.get_list_of_features_ids(self._layers[self.names.LC_BOUNDARY_POINT_T], self.names.T_ID_F)
        new_features = AssociationUtils.save_relations(self._layers[self.names.COL_POINT_SOURCE_T],
                                                       self.names.COL_POINT_SOURCE_T_LC_BOUNDARY_POINT_F, feature_ids,
                                                       self.names.COL_POINT_SOURCE_T_SOURCE_F, feature_tid)

        feature_ids = AssociationUtils.get_list_of_features_ids(self._layers[self.names.LC_SURVEY_POINT_T], self.names.T_ID_F)
        new_features = AssociationUtils.save_relations(self._layers[self.names.COL_POINT_SOURCE_T],
                                                       self.names.COL_POINT_SOURCE_T_LC_SURVEY_POINT_F, feature_ids,
                                                       self.names.COL_POINT_SOURCE_T_SOURCE_F, feature_tid)

        feature_ids = AssociationUtils.get_list_of_features_ids(self._layers[self.names.LC_CONTROL_POINT_T], self.names.T_ID_F)

        new_features = AssociationUtils.save_relations(self._layers[self.names.COL_POINT_SOURCE_T],
                                                       self.names.COL_POINT_SOURCE_T_LC_CONTROL_POINT_F, feature_ids,
                                                       self.names.COL_POINT_SOURCE_T_SOURCE_F, feature_tid)

        self._notify_finish_feature_creation(
            # TODO associated features is missing
            SpacialSourceFinishFeatureCreationArgs(True, feature_tid, 1, None)
        )
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

    #       OBSERVERS
    # on map ---
    def register_features_on_map_observer(self, observer):
        self.__features_on_map_observer_list.append(observer)

    def remove_features_on_map_observer(self, observer):
        self.__features_on_map_observer_list.remove(observer)

    def __notify_features_selected(self):
        for item in self.__features_on_map_observer_list:
            item.features_selected()

    def __notify_map_tool_changed(self):
        for item in self.__features_on_map_observer_list:
            item.map_tool_changed()

    # by expression ---
    def register_feature_selection_by_expression_observer(self, observer):
        self.__feature_selector_by_expression_observers.append(observer)

    def remove_feature_selection_by_expression_observer(self, observer):
        self.__feature_selector_by_expression_observers.remove(observer)

    def __notify_feature_selection_by_expression_changed(self):
        for item in self.__feature_selector_by_expression_observers:
            item.feature_selection_by_expression_changed()
