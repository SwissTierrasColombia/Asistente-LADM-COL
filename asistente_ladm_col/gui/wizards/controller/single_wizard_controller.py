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
from asistente_ladm_col.config.enums import EnumLayerCreationMode
from asistente_ladm_col.gui.wizards.controller.controller_args import CreateFeatureArgs
from asistente_ladm_col.gui.wizards.model.common.args.model_args import ExecFormAdvancedArgs
from asistente_ladm_col.gui.wizards.model.common.manual_feature_creator import AlphaFeatureCreator
from asistente_ladm_col.gui.wizards.model.common.select_features_by_expression_dialog_wrapper import \
    NullSelectorByExpression
from asistente_ladm_col.gui.wizards.model.common.select_features_on_map_wrapper import NullFeatureSelectorOnMap
from asistente_ladm_col.gui.wizards.controller.common.abstract_wizard_controller import AbstractWizardController, \
    ProductFactory
from asistente_ladm_col.gui.wizards.controller.common.wizard_messages_manager import WizardMessagesManager
from asistente_ladm_col.gui.wizards.model.single_wizard_model import SingleManager
from asistente_ladm_col.gui.wizards.view.single_wizard_view import SingleWizardView


class SingleProductFactory(ProductFactory):

    def create_feature_manager(self, db, layers, editing_layer):
        return SingleManager(db, layers, editing_layer)

    def create_manual_feature_creator(self, iface, app, logger, layer, feature_name):
        return AlphaFeatureCreator(iface, app, logger, layer, feature_name)

    def create_feature_selector_on_map(self, iface, logger, multiple_features=True):
        return NullFeatureSelectorOnMap()

    def create_feature_selector_by_expression(self, iface):
        return NullSelectorByExpression()

    def create_wizard_messages_manager(self, wizard_tool_name, editing_layer_name, logger):
        return WizardMessagesManager(wizard_tool_name, editing_layer_name, logger)


class SingleController(AbstractWizardController):

    def __init__(self, iface, db, wizard_config):
        AbstractWizardController.__init__(self, iface, db, wizard_config, SingleProductFactory())
        self.__manual_feature_creator = None

        self._initialize()

    def create_feature(self, args: CreateFeatureArgs):
        self._save_settings()
        if args.layer_creation_mode == EnumLayerCreationMode.REFACTOR_FIELDS:
            self.create_feature_from_refactor_fields()
        else:
            self._manual_feature_creator.create()

    # ok
    def exec_form_advanced(self, args: ExecFormAdvancedArgs):
        pass

    # NA
    def features_selected(self):
        pass

    # NA
    def feature_selection_by_expression_changed(self):
        pass

    # Single wizard view
    def _create_view(self):
        self.__view = SingleWizardView(self, self._get_view_config())
        return self.__view

    # TODO se puede implementar como un default
    def close_wizard(self):
        self.dispose()
        self.update_wizard_is_open_flag.emit(False)
        self.__view.close()
