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
from asistente_ladm_col import Logger
from asistente_ladm_col.config.general_config import WIZARD_LAYERS
from asistente_ladm_col.gui.wizards.model.common.args.model_args import ExecFormAdvancedArgs
from asistente_ladm_col.gui.wizards.model.common.select_features_by_expression_dialog_wrapper import \
    SelectFeatureByExpressionDialogWrapper
from asistente_ladm_col.gui.wizards.model.common.select_features_on_map_wrapper import SelectFeaturesOnMapWrapper
from asistente_ladm_col.gui.wizards.model.single_spatial_wizard_model import SingleSpatialWizardModel
from asistente_ladm_col.gui.wizards.view.common.view_enum import EnumRelatableLayers


class ExtAddressModel(SingleSpatialWizardModel):

    def __init__(self, iface, db, wiz_config):
        super().__init__(iface, db, wiz_config)

        self.__features_on_map_observer_list = list()
        self.__feature_selector_by_expression_observers = list()

        self.__association_failed_observers = list()

        self.__relatable_layers = dict()

        self._layers = wiz_config[WIZARD_LAYERS]
        self.__iface = iface

        self._logger = Logger()

        self.__feature_selector_on_map = SelectFeaturesOnMapWrapper(self.__iface, self._logger)
        self.__feature_selector_on_map.register_observer(self)

        self.__feature_selector_by_expression = SelectFeatureByExpressionDialogWrapper(self.__iface)
        self.__feature_selector_by_expression.register_observer(self)

        self.type_of_selected_layer_to_associate = None
        self.__init_selectable_layer_by_type()

    def __init_selectable_layer_by_type(self):
        # TODO Change the name
        self.__relatable_layers[EnumRelatableLayers.PLOT] = self._layers[self._db.names.LC_PLOT_T]
        self.__relatable_layers[EnumRelatableLayers.BUILDING] = self._layers[self._db.names.LC_BUILDING_T]
        self.__relatable_layers[EnumRelatableLayers.BUILDING_UNIT] = self._layers[self._db.names.LC_BUILDING_UNIT_T]

    def get_active_layer_type(self):
        for item_type in self.__relatable_layers:
            if self.__relatable_layers[item_type] == self.__iface.activeLayer():
                return item_type

        return None

    def select_features_on_map(self):
        # TODO is this execution right?
        self.__layer_remove_manager.reconnect_signals()
        # TODO Exception if layer does not exist
        layer = self.__relatable_layers[self.type_of_selected_layer_to_associate]
        self.__feature_selector_on_map.select_features_on_map(layer)

    def select_features_by_expression(self):
        # TODO Check if layer exists in self._layers
        layer = self.__relatable_layers[self.type_of_selected_layer_to_associate]
        self.__feature_selector_by_expression.select_features_by_expression(layer)

    def map_tool_changed(self):
        self.__notify_map_tool_changed()

    def features_selected(self):
        self.__notify_features_selected()

    def feature_selection_by_expression_changed(self):
        self.__notify_feature_selection_by_expression_changed()

    def dispose(self):
        self.__feature_selector_on_map.init_map_tool()
        super().dispose()
        self.__feature_selector_on_map.disconnect_signals()

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

            feature_id = selected_layer_to_pick_features.selectedFeatures()[0][self._db.names.T_ID_F]
            fid = feature.id()

            if self.type_of_selected_layer_to_associate == EnumRelatableLayers.PLOT:
                spatial_unit_field_idx = layer.getFeature(fid).fieldNameIndex(self._db.names.EXT_ADDRESS_S_LC_PLOT_F)
            elif self.type_of_selected_layer_to_associate == EnumRelatableLayers.BUILDING:
                spatial_unit_field_idx = layer.getFeature(fid).fieldNameIndex(self._db.names.EXT_ADDRESS_S_LC_BUILDING_F)
            elif self.type_of_selected_layer_to_associate == EnumRelatableLayers.BUILDING_UNIT:
                spatial_unit_field_idx = layer.getFeature(fid).fieldNameIndex(self._db.names.EXT_ADDRESS_S_LC_BUILDING_UNIT_F)

        if spatial_unit_field_idx:
            # assign the relation with the spatial unit
            layer.changeAttributeValue(fid, spatial_unit_field_idx, feature_id)
        else:
            # if the field of the spatial unit does not exist
            layer.rollBack()

            self.__notify_association_failed()

    def get_number_of_selected_features(self):
        feature_count = dict()

        for layer in self.__relatable_layers:
            feature_count[layer] = self.__relatable_layers[layer].selectedFeatureCount()

        return feature_count

    #       OBSERVERS
    def register_association_failed_observer(self, observer):
        self.__association_failed_observers.append(observer)

    def remove_association_failed_observer(self, observer):
        self.__association_failed_observers.remove(observer)

    def __notify_association_failed(self):
        for item in self.__association_failed_observers:
           item.association_failed()

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
