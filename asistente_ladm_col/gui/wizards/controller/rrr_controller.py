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
from qgis.PyQt.QtCore import QCoreApplication

from asistente_ladm_col.gui.wizards.controller.single_wizard_controller import SingleWizardController
from asistente_ladm_col.gui.wizards.model.rrr_model import RrrModel
from asistente_ladm_col.gui.wizards.view.common.enum_feature_selection_type import EnumFeatureSelectionType
from asistente_ladm_col.gui.wizards.view.common.view_args import PickFeaturesSelectedArgs
from asistente_ladm_col.gui.wizards.view.pages.features_selector_view import RrrSelectorView
from asistente_ladm_col.gui.wizards.view.spatial_source_view import SpatialSourceView


class RrrController(SingleWizardController):

    def __init__(self, model: RrrModel, db, wizard_settings):
        super().__init__(model, db, wizard_settings)
        self.__model = model

        self.__model.register_feature_selection_by_expression_observer(self)

    def _create_view(self):
        wizard_page2 = RrrSelectorView(self, self._get_view_config())
        self.__view = SpatialSourceView(self, self._get_view_config(), wizard_page2)
        return self.__view

    # events notified from VIEW
    def next_clicked(self):
        self.__update_selected_feature_info_view()

    def pick_features_selected(self, args: PickFeaturesSelectedArgs):
        if args.feature_selection_type == EnumFeatureSelectionType.SELECTION_BY_EXPRESSION:
            self.__model.select_features_by_expression(args.selected_type)

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
