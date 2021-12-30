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
from asistente_ladm_col.config.enums import EnumFeatureSelectionType, EnumLayerCreationMode
from asistente_ladm_col.config.general_config import WIZARD_EDITING_LAYER_NAME
from asistente_ladm_col.gui.wizards.controller.common.abstract_wizard_controller import ProductFactory, \
    AbstractWizardController
from asistente_ladm_col.gui.wizards.controller.common.wizard_messages_manager import WizardMessagesManager
from asistente_ladm_col.gui.wizards.controller.controller_args import CreateFeatureArgs
from asistente_ladm_col.gui.wizards.model.common.args.model_args import ExecFormAdvancedArgs
from asistente_ladm_col.gui.wizards.model.common.manual_feature_creator import AlphaFeatureCreator
from asistente_ladm_col.gui.wizards.model.common.select_features_by_expression_dialog_wrapper import \
    SelectFeatureByExpressionDialogWrapper
from asistente_ladm_col.gui.wizards.model.common.select_features_on_map_wrapper import NullFeatureSelectorOnMap
from asistente_ladm_col.gui.wizards.model.rrr_model import RrrCreatorManager
from asistente_ladm_col.gui.wizards.view.common.view_args import PickFeaturesSelectedArgs
from asistente_ladm_col.gui.wizards.view.pages.features_selector_view import RrrSelectorView
from asistente_ladm_col.gui.wizards.view.spatial_source_view import SpatialSourceView


class RrrProductFactory(ProductFactory):

    def __init__(self, editing_layer_name):
        self.__editing_layer_name = editing_layer_name

    def create_feature_manager(self, db, layers, editing_layer):
        return RrrCreatorManager(db, layers, editing_layer, self.__editing_layer_name)

    def create_manual_feature_creator(self, iface, app, logger, layer, feature_name):
        return AlphaFeatureCreator(iface, app, logger, layer, feature_name)

    def create_feature_selector_on_map(self, iface, logger, multiple_features=True):
        return NullFeatureSelectorOnMap()

    def create_feature_selector_by_expression(self, iface):
        return SelectFeatureByExpressionDialogWrapper(iface)

    def create_wizard_messages_manager(self, wizard_tool_name, editing_layer_name, logger):
        return WizardMessagesManager(wizard_tool_name, editing_layer_name, logger)


class RrrController(AbstractWizardController):

    def __init__(self, iface, db, wizard_config):
        product_factory = RrrProductFactory(wizard_config[WIZARD_EDITING_LAYER_NAME])
        AbstractWizardController.__init__(self, iface, db, wizard_config, product_factory)
        self.__manual_feature_creator = None

        self._initialize()

    def create_feature(self, args: CreateFeatureArgs):
        self._save_settings()
        if args.layer_creation_mode == EnumLayerCreationMode.REFACTOR_FIELDS:
            self.create_feature_from_refactor_fields()
        else:
            self._manual_feature_creator.create()

    # TODO OK
    def exec_form_advanced(self, args: ExecFormAdvancedArgs):
        pass

    # NA
    def features_selected(self):
        pass

    def feature_selection_by_expression_changed(self):
        self.__update_selected_feature_info_view()

    def _create_view(self):
        wizard_page2 = RrrSelectorView(self, self._get_view_config())
        self.__view = SpatialSourceView(self, self._get_view_config(), wizard_page2)
        return self.__view

    def close_wizard(self):
        self.dispose()
        self.update_wizard_is_open_flag.emit(False)
        self.__view.close()

    # events notified from VIEW
    def next_clicked(self):
        self.__update_selected_feature_info_view()

    def pick_features_selected(self, args: PickFeaturesSelectedArgs):
        if args.feature_selection_type == EnumFeatureSelectionType.SELECTION_BY_EXPRESSION:
            layer = self._feature_manager.get_layer_by_type(args.selected_type)
            self._feature_selector_by_expression.select_features_by_expression(layer)

    def __update_selected_feature_info_view(self):
        feature_count = self._feature_manager.get_number_of_selected_features()
        self.__view.show_number_of_selected_features(feature_count)

        enable_finish_button = self.__is_any_feature_selected(feature_count)
        self.__view.enable_finish_button(enable_finish_button)

    @staticmethod
    def __is_any_feature_selected(feature_count):
        for item_type in feature_count:
            if feature_count[item_type] > 0:
                return True

        return False
