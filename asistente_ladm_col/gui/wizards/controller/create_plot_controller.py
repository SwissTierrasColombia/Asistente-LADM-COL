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
from qgis.core import QgsMapLayerProxyModel

from asistente_ladm_col import Logger
from asistente_ladm_col.config.general_config import (WIZARD_STRINGS,
                                                      WIZARD_HELP_PAGES,
                                                      WIZARD_HELP,
                                                      WIZARD_HELP1,
                                                      WIZARD_QSETTINGS,
                                                      WIZARD_QSETTINGS_LOAD_DATA_TYPE,
                                                      WIZARD_LAYERS,
                                                      WIZARD_EDITING_LAYER_NAME,
                                                      WIZARD_TOOL_NAME,
                                                      WIZARD_HELP2)
from asistente_ladm_col.config.help_strings import HelpStrings
from asistente_ladm_col.gui.wizards.controller.controller_args import CreateFeatureArgs
from asistente_ladm_col.gui.wizards.model.common.wizard_q_settings_manager import WizardQSettingsManager
from asistente_ladm_col.gui.wizards.model.create_plot_model import (CreatePlot,
                                                                    EnumPlotCreationResult)
from asistente_ladm_col.gui.wizards.view.common.enum_feature_selection_type import EnumFeatureSelectionType
from asistente_ladm_col.gui.wizards.view.pages.features_selector_view import PlotSelectorView
from asistente_ladm_col.gui.wizards.view.spatial_source_view import SpatialSourceView
from asistente_ladm_col.gui.wizards.wizard_constants import (WIZARD_REFACTOR_RECENT_MAPPING_OPTIONS,
                                                             WIZARD_FINISH_BUTTON_TEXT,
                                                             WIZARD_SELECT_SOURCE_HELP,
                                                             WIZARD_REFACTOR_LAYER_FILTERS)
from asistente_ladm_col.gui.wizards.view.common.view_enum import EnumLayerCreationMode
from asistente_ladm_col.gui.wizards.view.common.view_args import PickFeaturesSelectedArgs


class CreatePlotController(QObject):
    update_wizard_is_open_flag = pyqtSignal(bool)

    def __init__(self, model: CreatePlot, db, wizard_settings):
        QObject.__init__(self)

        self.wizard_config = wizard_settings
        self.__layers = self.wizard_config[WIZARD_LAYERS]
        self.__db = db
        self.EDITING_LAYER_NAME = self.wizard_config[WIZARD_EDITING_LAYER_NAME]
        self.WIZARD_TOOL_NAME = self.wizard_config[WIZARD_TOOL_NAME]
        self.logger = Logger()

        # ----- model section
        self.__model = model
        self.__model.register_features_on_map_observer(self)
        self.__model.register_feature_selection_by_expression_observer(self)

        self.__model.set_ready_only_fields(True)
        # ------ view section
        self.__view = self._create_view()

        # QSetings
        self.__settings_manager = WizardQSettingsManager(
            self.wizard_config[WIZARD_QSETTINGS][WIZARD_QSETTINGS_LOAD_DATA_TYPE])

    def _create_view(self):
        wizard_page2 = PlotSelectorView(self, self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP2])
        self.__view = SpatialSourceView(self, self._get_view_config(), wizard_page2)
        return self.__view

    def exec_(self):
        self.__restore_settings()
        self.__view.exec_()

    #  view
    def _get_view_config(self):
        # TODO Load help_strings from wizard_config
        help_strings = HelpStrings()
        return {
            WIZARD_STRINGS: self.wizard_config[WIZARD_STRINGS],
            WIZARD_REFACTOR_RECENT_MAPPING_OPTIONS: self.__model.refactor_field_mapping,
            WIZARD_REFACTOR_LAYER_FILTERS: QgsMapLayerProxyModel.Filter(QgsMapLayerProxyModel.NoGeometry),
            WIZARD_HELP_PAGES: self.wizard_config[WIZARD_HELP_PAGES],
            WIZARD_HELP: self.wizard_config[WIZARD_HELP],
            WIZARD_FINISH_BUTTON_TEXT: {
                EnumLayerCreationMode.REFACTOR: QCoreApplication.translate("WizardTranslations", "Import"),
                EnumLayerCreationMode.MANUALLY: QCoreApplication.translate("WizardTranslations", "Create")
            },
            WIZARD_SELECT_SOURCE_HELP: {
                EnumLayerCreationMode.REFACTOR:
                    help_strings.get_refactor_help_string(self.__db, self.__layers[self.EDITING_LAYER_NAME]),
                EnumLayerCreationMode.MANUALLY:
                    self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP1]
            }
        }

    # QSettings
    def __restore_settings(self):
        settings = self.__settings_manager.get_settings()
        self.__view.restore_settings(settings)

    def __save_settings(self):
        self.__settings_manager.save_settings(self.__view.get_settings())

    def wizard_rejected(self):
        message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed.").format(
            self.WIZARD_TOOL_NAME)
        self.logger.info_msg(__name__, message)
        self.close_wizard()

    #  TODO name?
    def close_wizard(self):
        self.__model.dispose()
        self.update_wizard_is_open_flag.emit(False)
        self.__view.close()

    def create_feature(self, args: CreateFeatureArgs):
        self.__save_settings()
        if args.layer_creation_mode == EnumLayerCreationMode.REFACTOR:
            self.__feature_from_refactor()
        else:
            edit_feature_result = self.__model.edit_feature()

            if edit_feature_result == EnumPlotCreationResult.NO_BOUNDARIES_SELECTED:
                self.logger.warning_msg(__name__, QCoreApplication.translate("WizardTranslations", "First select boundaries!"))
            elif edit_feature_result == EnumPlotCreationResult.NO_PLOTS_CREATED:
                message = QCoreApplication.translate("WizardTranslations", "No plot could be created. Make sure selected boundaries are closed!")
                self.logger.info_msg(__name__, message)
                self.close_wizard()
            elif edit_feature_result == EnumPlotCreationResult.CREATED:
                self.close_wizard()

    def __feature_from_refactor(self):
        selected_layer = self.__view.get_selected_layer_refactor()

        if selected_layer is not None:
            field_mapping = self.__view.get_field_mapping_refactor()
            self.__model.create_feature_from_refactor(selected_layer, field_mapping)
        else:
            self.logger.warning_msg(__name__, QCoreApplication.translate("WizardTranslations",
                                                                         "Select a source layer to set the field mapping to '{}'.").format(
                self.wizard_config[WIZARD_EDITING_LAYER_NAME]))

        message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed.").format(
            self.WIZARD_TOOL_NAME)
        self.logger.info_msg(__name__, message)
        self.close_wizard()

    def form_rejected(self):
        message = QCoreApplication.translate("WizardTranslations",
                                             "'{}' tool has been closed because you just closed the form.").format(
            self.WIZARD_TOOL_NAME)
        self.logger.info_msg(__name__, message)
        self.close_wizard()

    # events notified from VIEW
    def next_clicked(self):
        self.__update_selected_feature_info_view()

    def pick_features_selected(self, args: PickFeaturesSelectedArgs):
        if args.feature_selection_type == EnumFeatureSelectionType.SELECTION_ON_MAP:
            self.__view.set_visible(False)  # Make wizard disappear
            self.__model.select_features_on_map()
        elif args.feature_selection_type == EnumFeatureSelectionType.SELECTION_BY_EXPRESSION:
            self.__model.select_features_by_expression()
        elif args.feature_selection_type == EnumFeatureSelectionType.ALL_FEATURES:
            self.__model.select_all_features()
            self.__update_selected_feature_info_view()

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
                                             "'{}' tool has been closed because you just removed a required layer.").format(
            self.WIZARD_TOOL_NAME)
        self.logger.info_msg(__name__, message)
        self.close_wizard()
