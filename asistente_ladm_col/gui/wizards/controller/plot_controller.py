# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-09-10
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BFS Swissphoto)
                               (C) 2019 by Leo Cardona (BFS Swissphoto)
                               (C) 2021 by Yesid Polania (BFS Swissphoto)
        email                : gcarrillo@linuxmail.org
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
                              pyqtSignal,
                              QCoreApplication)

from asistente_ladm_col import Logger
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.general_config import (WIZARD_HELP_PAGES,
                                                      WIZARD_HELP2)
from asistente_ladm_col.config.enums import (EnumLayerCreationMode,
                                             EnumFeatureSelectionType)
from asistente_ladm_col.gui.wizards.controller.common.abstract_wizard_controller import (ProductFactory,
                                                                                         AbstractWizardController)
from asistente_ladm_col.gui.wizards.controller.common.wizard_messages_manager import WizardMessagesManager
from asistente_ladm_col.gui.wizards.controller.controller_args import CreateFeatureArgs
from asistente_ladm_col.gui.wizards.model.common.manual_feature_creator import NullFeatureCreator
from asistente_ladm_col.gui.wizards.model.common.select_features_by_expression_dialog_wrapper import \
    SelectFeatureByExpressionDialogWrapper
from asistente_ladm_col.gui.wizards.model.common.select_features_on_map_wrapper import SelectFeaturesOnMapWrapper
from asistente_ladm_col.gui.wizards.model.plot_model import (EnumPlotCreationResult,
                                                             PlotCreatorManager)
from asistente_ladm_col.gui.wizards.view.pages.features_selector_view import PlotSelectorView
from asistente_ladm_col.gui.wizards.view.spatial_source_view import SpatialSourceView
from asistente_ladm_col.gui.wizards.view.common.view_args import PickFeaturesSelectedArgs


class PlotProductFactory(ProductFactory):

    def __init__(self, iface, app, logger):
        self.__iface = iface
        self.__app = app
        # TODO Logger can be moved
        self.__logger = logger

    def create_feature_manager(self, db, layers, editing_layer):
        return PlotCreatorManager(db, layers, editing_layer, self.__iface, self.__app, self.__logger)

    def create_manual_feature_creator(self, iface, app, logger, layer, feature_name):
        return NullFeatureCreator()

    def create_feature_selector_on_map(self, iface, logger, multiple_features=True):
        return SelectFeaturesOnMapWrapper(iface, logger)

    def create_feature_selector_by_expression(self, iface):
        return SelectFeatureByExpressionDialogWrapper(iface)

    def create_wizard_messages_manager(self, wizard_tool_name, editing_layer_name, logger):
        return WizardMessagesManager(wizard_tool_name, editing_layer_name, logger)


class PlotController(AbstractWizardController):
    def __init__(self, iface, db, wizard_config, observer):
        product_factory = PlotProductFactory(iface, AppInterface(), Logger())
        AbstractWizardController.__init__(self, iface, db, wizard_config, product_factory, observer)
        self.__manual_feature_creator = None

        self._initialize()

    def create_feature(self, args: CreateFeatureArgs):
        self._save_settings()
        if args.layer_creation_mode == EnumLayerCreationMode.REFACTOR_FIELDS:
            self.create_feature_from_refactor_fields()
        else:
            edit_feature_result = self._feature_manager.edit_feature()

            if edit_feature_result == EnumPlotCreationResult.NO_BOUNDARIES_SELECTED:
                self._logger.warning_msg(__name__,
                                        QCoreApplication.translate("WizardTranslations", "First select boundaries!"))
            elif edit_feature_result == EnumPlotCreationResult.NO_PLOTS_CREATED:
                message = QCoreApplication.translate("WizardTranslations",
                                                     "No plot could be created. Make sure selected boundaries are closed!")
                self._logger.info_msg(__name__, message)
                self.close_wizard()
            elif edit_feature_result == EnumPlotCreationResult.CREATED:
                self.close_wizard()

    def features_selected(self):
        self.__view.set_visible(True)
        self.__update_selected_feature_info_view()

    def feature_selection_by_expression_changed(self):
        self.__update_selected_feature_info_view()

    def _create_view(self):
        wizard_page2 = PlotSelectorView(self, self._wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP2])
        self.__view = SpatialSourceView(self, self._get_view_config(), wizard_page2)
        return self.__view

    # events notified from VIEW
    def next_clicked(self):
        self.__update_selected_feature_info_view()

    def pick_features_selected(self, args: PickFeaturesSelectedArgs):
        layer = self._feature_manager.get_layer_by_type(args.selected_type)

        if args.feature_selection_type == EnumFeatureSelectionType.SELECTION_ON_MAP:
            self.__view.set_visible(False)  # Make wizard disappear
            self._layer_remove_manager.reconnect_signals()
            self._feature_selector_on_map.select_features_on_map(layer)
        elif args.feature_selection_type == EnumFeatureSelectionType.SELECTION_BY_EXPRESSION:
            self._feature_selector_by_expression.select_features_by_expression(layer)
        elif args.feature_selection_type == EnumFeatureSelectionType.ALL_FEATURES:
            self._feature_manager.select_all_features()
            self.__update_selected_feature_info_view()

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
