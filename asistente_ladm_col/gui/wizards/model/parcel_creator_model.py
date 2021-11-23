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
from qgis.PyQt.QtCore import (QObject,
                             pyqtSignal)

from asistente_ladm_col.config.enums import EnumRelatableLayers
from asistente_ladm_col.config.general_config import (WIZARD_FEATURE_NAME,
                                                      WIZARD_LAYERS)
from asistente_ladm_col.config.layer_config import (LayerConfig,
                                                    EnumRelationshipType)
from asistente_ladm_col.gui.wizards.model.common.args.model_args import (ExecFormAdvancedArgs,
                                                                         ParcelFinishFeatureCreationArgs)
from asistente_ladm_col.gui.wizards.model.common.association_utils import AssociationUtils
from asistente_ladm_col.gui.wizards.model.common.manual_feature_creator import (ManualFeatureCreator,
                                                                                AlphaFeatureCreator)
from asistente_ladm_col.gui.wizards.model.common.feature_selector_manager import FeatureSelectorManager
from asistente_ladm_col.gui.wizards.model.common.select_features_by_expression_dialog_wrapper import \
    SelectFeatureByExpressionDialogWrapper
from asistente_ladm_col.gui.wizards.model.common.select_features_on_map_wrapper import SelectFeaturesOnMapWrapper
from asistente_ladm_col.gui.wizards.model.creator_model import CreatorModel


class ParcelCreatorModel(CreatorModel):
    features_selected = pyqtSignal()
    map_tool_changed = pyqtSignal()
    feature_selection_by_expression_changed = pyqtSignal()

    def __init__(self, iface, db, wiz_config):
        CreatorModel.__init__(self, iface, db, wiz_config)

        self.db = db
        self._layers = wiz_config[WIZARD_LAYERS]

        self.__relatable_layers = dict()
        self.__init_selectable_layer_by_type()

        # FeatureSelectorManager
        self.parcel_type_ili_code = None
        self.__constraint_types_of_parcels = LayerConfig.get_constraint_types_of_parcels(self.db.names)

        self.__features_on_map_observer_list = list()
        self.__feature_selector_by_expression_observers = list()

        self.__feature_selector_on_map = SelectFeaturesOnMapWrapper(self._iface, self._logger)
        self.__feature_selector_on_map.features_selected.connect(self.features_selected)
        self.__feature_selector_on_map.map_tool_changed.connect(self.map_tool_changed)

        self.__feature_selector_by_expression = SelectFeatureByExpressionDialogWrapper(self._iface)
        self.__feature_selector_by_expression.feature_selection_by_expression_changed.connect(
            self.feature_selection_by_expression_changed)

        self.type_of_selected_layer_to_associate = None

    def select_features_on_map(self):
        self._layer_remove_manager.reconnect_signals()
        # TODO Exception if layer does not exist
        layer = self.__relatable_layers[self.type_of_selected_layer_to_associate]
        self.__feature_selector_on_map.select_features_on_map(layer)

    def select_features_by_expression(self):
        # TODO Check if layer exists in self._layers
        layer = self.__relatable_layers[self.type_of_selected_layer_to_associate]
        self.__feature_selector_by_expression.select_features_by_expression(layer)

    def dispose(self):
        self.__feature_selector_on_map.init_map_tool()
        self.__feature_selector_on_map.disconnect_signals()

    def get_number_of_selected_features(self):
        feature_count = dict()

        for layer in self.__relatable_layers:
            feature_count[layer] = self.__relatable_layers[layer].selectedFeatureCount()

        return feature_count

    def __init_selectable_layer_by_type(self):
        # TODO Change the name
        self.__relatable_layers[EnumRelatableLayers.PLOT] = self._layers[self._db.names.LC_PLOT_T]
        self.__relatable_layers[EnumRelatableLayers.BUILDING] = self._layers[self._db.names.LC_BUILDING_T]
        self.__relatable_layers[EnumRelatableLayers.BUILDING_UNIT] = self._layers[self._db.names.LC_BUILDING_UNIT_T]

    def _create_feature_creator(self) -> ManualFeatureCreator:
        return AlphaFeatureCreator(self._iface, self.app, self._logger,
                                   self._editing_layer, self._wizard_config[WIZARD_FEATURE_NAME])

    def exec_form_advanced(self, args: ExecFormAdvancedArgs):
        fid = args.feature.id()

        # assigns the type of parcel before to creating it
        parcel_condition_field_idx = args.layer.getFeature(fid).fieldNameIndex(self._db.names.LC_PARCEL_T_PARCEL_TYPE_F)
        args.layer.changeAttributeValue(fid, parcel_condition_field_idx,
                                        self.__get_ili_code_id_dict()[self.parcel_type_ili_code])

    def _finish_feature_creation(self, layerId, features):
        if len(features) != 1:
            # TODO send this info to controller
            # message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed. We should have got only one {} by we have {}").format(self.WIZARD_TOOL_NAME, self.WIZARD_FEATURE_NAME, len(features))
            # self.logger.warning(__name__, "We should have got only one {}, but we have {}".format(self.WIZARD_FEATURE_NAME, len(features)))
            self.finish_feature_creation.emit(ParcelFinishFeatureCreationArgs(added_features_amount=len(features)))
            return

        if not self.is_each_layer_valid():
            self.finish_feature_creation.emit(ParcelFinishFeatureCreationArgs(valid_constraints=False))
            return

        feature = features[0]

        if not feature.isValid():
            # TODO send this info to controller
            # self.logger.warning(__name__, "Feature not found in layer Spatial Source...")
            self.finish_feature_creation.emit(ParcelFinishFeatureCreationArgs(is_valid=False))
            return

        # TODO What is the difference?
        # feature_tid = feature[self.db.names.T_ID_F]
        feature_tid = self._editing_layer.getFeature(feature.id())[self.db.names.T_ID_F]

        plot_ids = list()
        building_ids = list()
        building_unit_ids = list()

        # Apply restriction to the selection

        # add plot associated
        if self.db.names.LC_PLOT_T in self.__constraint_types_of_parcels[self.parcel_type_ili_code]:
            add_features = self.__constraint_types_of_parcels[self.parcel_type_ili_code][self.db.names.LC_PLOT_T] is not None
        else:
            add_features = True

        if add_features:
            plot_ids = AssociationUtils.get_list_of_features_ids(self._layers[self.db.names.LC_PLOT_T],
                                                                 self.db.names.T_ID_F)

        new_features = AssociationUtils.save_relations(self._layers[self.db.names.COL_UE_BAUNIT_T],
                                                       self.db.names.COL_UE_BAUNIT_T_LC_PLOT_F, plot_ids,
                                                       self.db.names.COL_UE_BAUNIT_T_PARCEL_F, feature_tid)

        # add building associated
        if self.db.names.LC_BUILDING_T in self.__constraint_types_of_parcels[self.parcel_type_ili_code]:
            add_features = self.__constraint_types_of_parcels[self.parcel_type_ili_code][
                               self.db.names.LC_BUILDING_T] is not None
        else:
            add_features = True

        if add_features:
            building_ids = AssociationUtils.get_list_of_features_ids(self._layers[self.db.names.LC_BUILDING_T],
                                                                     self.db.names.T_ID_F)

        new_features = AssociationUtils.save_relations(self._layers[self.db.names.COL_UE_BAUNIT_T],
                                                       self.db.names.COL_UE_BAUNIT_T_LC_BUILDING_F, building_ids,
                                                       self.db.names.COL_UE_BAUNIT_T_PARCEL_F, feature_tid)

        # add building unit associated
        if self.db.names.LC_BUILDING_UNIT_T in self.__constraint_types_of_parcels[self.parcel_type_ili_code]:
            add_features = self.__constraint_types_of_parcels[self.parcel_type_ili_code][
                               self.db.names.LC_BUILDING_UNIT_T] is not None
        else:
            add_features = True

        if add_features:
            building_unit_ids = AssociationUtils.get_list_of_features_ids(self._layers[self.db.names.LC_BUILDING_UNIT_T],
                                                                     self.db.names.T_ID_F)

        new_features = AssociationUtils.save_relations(self._layers[self.db.names.COL_UE_BAUNIT_T],
                                                       self.db.names.COL_UE_BAUNIT_T_LC_BUILDING_UNIT_F,
                                                       building_unit_ids, self.db.names.COL_UE_BAUNIT_T_PARCEL_F,
                                                       feature_tid)

        self.finish_feature_creation.emit(
            # TODO associated features is missing
            ParcelFinishFeatureCreationArgs(True, feature_tid, 1, None)
        )

    # parcel
    def get_type_parcel_conditions(self):
        result = dict()

        for feature in self._layers[self._db.names.LC_CONDITION_PARCEL_TYPE_D].getFeatures():
            if feature[self._db.names.ILICODE_F] in self.__constraint_types_of_parcels:
                result[feature[self._db.names.ILICODE_F]] = feature[self._db.names.DISPLAY_NAME_F]
        return result

    def __get_ili_code_id_dict(self):
        result = dict()
        for feature in self._layers[self._db.names.LC_CONDITION_PARCEL_TYPE_D].getFeatures():
            if feature[self._db.names.ILICODE_F] in self.__constraint_types_of_parcels:
                result[feature[self._db.names.ILICODE_F]] = feature[self._db.names.T_ID_F]

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
        constraint = self.__constraint_types_of_parcels[self.parcel_type_ili_code][spatial_unit_enum.get_db_name(self.db.names)]
        layer = self.__relatable_layers[spatial_unit_enum]
        is_valid = None
        if constraint == EnumRelationshipType.ONE:
            is_valid = layer.selectedFeatureCount() == 1
        elif constraint == EnumRelationshipType.ONE_OR_MANY:
            is_valid = layer.selectedFeatureCount() >= 1
        elif constraint == EnumRelationshipType.MANY:
            is_valid = True

        return is_valid

    def is_each_layer_valid(self):
        result = True
        for layer_status in self.get_layer_status():
            if not layer_status:
                result = False
                break
        return result


