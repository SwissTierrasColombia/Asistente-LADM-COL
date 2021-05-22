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
from qgis.PyQt.QtCore import QCoreApplication

from asistente_ladm_col.config.general_config import (WIZARD_HELP_PAGES,
                                                      WIZARD_HELP2)
from asistente_ladm_col.gui.wizards.controller.single_wizard_controller import SingleWizardController
from asistente_ladm_col.gui.wizards.model.spatial_source_model import SpatialSourceModel
from asistente_ladm_col.gui.wizards.view.common.enum_feature_selection_type import EnumFeatureSelectionType
from asistente_ladm_col.gui.wizards.view.common.view_args import PickFeaturesSelectedArgs
from asistente_ladm_col.gui.wizards.view.pages.features_selector_view import SpatialSourceFeaturesSelectorView
from asistente_ladm_col.gui.wizards.view.spatial_source_view import SpatialSourceView


class SpatialSourceController(SingleWizardController):

    def __init__(self, model: SpatialSourceModel, db, wizard_settings):
        super().__init__(model, db, wizard_settings)
        self.__model = model

        self.__model.register_feature_selection_by_expression_observer(self)
        self.__model.register_features_on_map_observer(self)

    def _create_view(self):
        wizard_page2 = SpatialSourceFeaturesSelectorView(self, self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP2])
        self.__view = SpatialSourceView(self, self._get_view_config(), wizard_page2)
        return self.__view

    # events notified from VIEW
    def next_clicked(self):
        self.__update_selected_feature_info_view()

    def pick_features_selected(self, args: PickFeaturesSelectedArgs):
        if args.feature_selection_type == EnumFeatureSelectionType.SELECTION_ON_MAP:
            self.__view.set_visible(False)  # Make wizard disappear
            self.__model.select_features_on_map(args.selected_type)
        elif args.feature_selection_type == EnumFeatureSelectionType.SELECTION_BY_EXPRESSION:
            self.__model.select_features_by_expression(args.selected_type)

    # events notified from MODEL
    # on map
    def map_tool_changed(self):
        message = QCoreApplication.translate("WizardTranslations",
                                             "'{}' tool has been closed because the map tool change.").format(
            self.WIZARD_TOOL_NAME)
        self.logger.info_msg(__name__, message)
        self.close_wizard()

    def features_selected(self):
        self.__view.set_visible(True)
        self.__update_selected_feature_info_view()

    # by expression
    def feature_selection_by_expression_changed(self):
        self.__update_selected_feature_info_view()

    def __update_selected_feature_info_view(self):
        feature_count = self.__model.get_number_of_selected_features()
        self.__view.show_number_of_selected_features(feature_count)

        enable_finish_button = self.__is_any_feature_selected(feature_count)
        self.__view.enable_finish_button(enable_finish_button)

    @staticmethod
    def __is_any_feature_selected(feature_count):
        for item_type in feature_count:
            if feature_count[item_type] > 0:
                return True

        return False

    def layer_removed(self):
        message = QCoreApplication.translate("WizardTranslations",
                                             "'{}' tool has been closed because you just removed a required layer.").format(self.WIZARD_TOOL_NAME)
        self.logger.info_msg(__name__, message)
        self.close_wizard()
