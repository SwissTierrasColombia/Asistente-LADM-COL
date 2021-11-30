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
from qgis.PyQt.QtCore import (QObject,
                             pyqtSignal)

from asistente_ladm_col.config.enums import EnumRelatableLayers

from asistente_ladm_col.config.general_config import (WIZARD_LAYERS,
                                                      WIZARD_EDITING_LAYER_NAME,
                                                      WIZARD_FEATURE_NAME)
from asistente_ladm_col.gui.wizards.model.common.args.model_args import (SpacialSourceFinishFeatureCreationArgs,
                                                                         ExecFormAdvancedArgs)
from asistente_ladm_col.gui.wizards.model.common.association_utils import AssociationUtils
from asistente_ladm_col.gui.wizards.model.common.manual_feature_creator import (ManualFeatureCreator,
                                                                                AlphaFeatureCreator)
from asistente_ladm_col.gui.wizards.model.common.select_features_by_expression_dialog_wrapper import \
    SelectFeatureByExpressionDialogWrapper
from asistente_ladm_col.gui.wizards.model.creator_model import CreatorModel


class RrrModel(CreatorModel):
    feature_selection_by_expression_changed = pyqtSignal()

    def __init__(self, iface, db, wiz_config):
        CreatorModel.__init__(self, iface, db, wiz_config)
        self._layers = wiz_config[WIZARD_LAYERS]
        self.__wizard_config = wiz_config
        self.__iface = iface
        self.__db = db
        self.__editing_layer_name = self.__wizard_config[WIZARD_EDITING_LAYER_NAME]
        self.__editing_layer = self.__wizard_config[WIZARD_LAYERS][self.__editing_layer_name]

        self.names = db.names

        self.__feature_selector_by_expression = SelectFeatureByExpressionDialogWrapper(self.__iface)

        self.__feature_selector_by_expression.feature_selection_by_expression_changed.connect(
            self.feature_selection_by_expression_changed)

        self.__relatable_layers = dict()
        self.__init_selectable_layer_by_type()

    def __init_selectable_layer_by_type(self):
        self.__relatable_layers[EnumRelatableLayers.ADMINISTRATIVE_SOURCE] = \
            self._layers[self.names.LC_ADMINISTRATIVE_SOURCE_T]

    def _finish_feature_creation(self, layerId, features):
        if len(features) != 1:
            args = SpacialSourceFinishFeatureCreationArgs(added_features_amount=len(features))
            self.finish_feature_creation.emit(args)
            return

        fid = features[0].id()

        if not self.__editing_layer_name.getFeature(fid).isValid():
            # self.logger.warning(__name__, "Feature not found in layer {}...".format(self.__editing_layer_name))
            # TODO send this info to controller
            args = SpacialSourceFinishFeatureCreationArgs(SpacialSourceFinishFeatureCreationArgs(is_valid=False))
            self.finish_feature_creation.emit(args)
            return

        # feature_rrr_id: generic name used for represent id for right, restriction
        # feature_rrr_id = self._layers[self.EDITING_LAYER_NAME].getFeature(fid)[self.names.T_ID_F]
        feature_tid = self.__editing_layer.getFeature(fid)[self.__db.names.T_ID_F]

        administrative_source_ids = AssociationUtils.get_list_of_features_ids(self._layers[self.names.LC_ADMINISTRATIVE_SOURCE_T], self.names.T_ID_F)

        # Fill rrrfuente table
        new_features = []
        attr_fk = None

        if self.__editing_layer_name == self.names.LC_RIGHT_T:
            attr_fk = self.names.COL_RRR_SOURCE_T_LC_RIGHT_F
        elif self.__editing_layer_name == self.names.LC_RESTRICTION_T:
            attr_fk = self.names.COL_RRR_SOURCE_T_LC_RESTRICTION_F

        new_features = AssociationUtils.save_relations(self._layers[self.names.self.names.COL_RRR_SOURCE_T],
                                                       self.names.COL_POINT_SOURCE_T_LC_CONTROL_POINT_F,
                                                       administrative_source_ids, attr_fk, feature_tid)
        args = SpacialSourceFinishFeatureCreationArgs(True, feature_tid, 1, None)
        self.finish_feature_creation.emit(args)
        # TODO log messages is missing

    def exec_form_advanced(self, args: ExecFormAdvancedArgs):
        pass

    def _create_feature_creator(self) -> ManualFeatureCreator:
        return AlphaFeatureCreator(self._iface, self.app, self._logger,
                                   self._editing_layer, self._wizard_config[WIZARD_FEATURE_NAME])

    def select_features_by_expression(self, option_type: EnumRelatableLayers):
        # TODO Check if LAYER exists in self._layers
        layer = self.__relatable_layers[option_type]
        self.__feature_selector_by_expression.select_features_by_expression(layer)

    def get_number_of_selected_features(self):
        feature_count = dict()

        for layer in self.__relatable_layers:
            feature_count[layer] = self.__relatable_layers[layer].selectedFeatureCount()

        return feature_count
