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
                              pyqtSignal,
                              QCoreApplication)
from qgis.core import QgsMapLayerProxyModel

from asistente_ladm_col import Logger
from asistente_ladm_col.config.general_config import (WIZARD_STRINGS,
                                                      WIZARD_HELP_PAGES,
                                                      WIZARD_HELP,
                                                      WIZARD_EDITING_LAYER_NAME,
                                                      WIZARD_LAYERS,
                                                      WIZARD_QSETTINGS,
                                                      WIZARD_TOOL_NAME,
                                                      WIZARD_FEATURE_NAME,
                                                      WIZARD_MAP_LAYER_PROXY_MODEL,
                                                      WIZARD_HELP1,
                                                      WIZARD_QSETTINGS_PATH)
from asistente_ladm_col.config.help_strings import HelpStrings
from asistente_ladm_col.gui.wizards.model.common.args.model_args import (FinishFeatureCreationArgs,
                                                                         ValidFeaturesDigitizedArgs,
                                                                         UnexpectedFeaturesDigitizedArgs)
from asistente_ladm_col.gui.wizards.model.common.args.model_enums import EnumDigitizedFeatureStatus
from asistente_ladm_col.gui.wizards.model.common.wizard_q_settings_manager import WizardQSettingsManager
from asistente_ladm_col.gui.wizards.controller.controller_args import CreateFeatureArgs
from asistente_ladm_col.gui.wizards.model.single_spatial_wizard_model import SingleSpatialWizardModel
from asistente_ladm_col.gui.wizards.view.common.view_utils import ViewUtils

from asistente_ladm_col.gui.wizards.view.single_wizard_view import SingleWizardView
from asistente_ladm_col.config.wizard_constants import (WIZARD_REFACTOR_FIELDS_RECENT_MAPPING_OPTIONS,
                                                        WIZARD_REFACTOR_FIELDS_LAYER_FILTERS,
                                                        WIZARD_FINISH_BUTTON_TEXT,
                                                        WIZARD_SELECT_SOURCE_HELP,
                                                        WIZARD_CREATION_MODE_KEY)
from asistente_ladm_col.gui.wizards.view.common.view_enum import EnumLayerCreationMode


class SingleSpatialWizardController(QObject):
    update_wizard_is_open_flag = pyqtSignal(bool)
    enable_save_geometry_button = pyqtSignal(bool)

    def __init__(self, model: SingleSpatialWizardModel, iface, db, wizard_settings):
        QObject.__init__(self)

        self.wizard_config = wizard_settings
        self.__iface = iface
        self.__layers = self.wizard_config[WIZARD_LAYERS]
        self.__db = db
        self.EDITING_LAYER_NAME = self.wizard_config[WIZARD_EDITING_LAYER_NAME]
        self.WIZARD_TOOL_NAME = self.wizard_config[WIZARD_TOOL_NAME]
        self.logger = Logger()

        # ----- model section
        self.__model = model
        self.__model.register_finish_feature_creation_observer(self)
        self.__model.register_form_rejected_observer(self)
        self.__model.register_unexpected_features_digitized_observer(self)
        self.__model.register_valid_features_digitized_observer(self)
        self.__model.register_layer_removed_observer(self)

        self.__model.set_ready_only_fields(True)

        # ------ view section
        self.__view = self._create_view()

        ViewUtils.enable_digitize_actions(self.__iface, False)
        # QSetings
        self.__settings_manager = WizardQSettingsManager(self.wizard_config[WIZARD_QSETTINGS][WIZARD_QSETTINGS_PATH])

    def _create_view(self):
        return SingleWizardView(self, self._get_view_config())

    def exec_(self):
        self._restore_settings()
        self.__view.exec_()

    #  view
    def _get_view_config(self):
        # TODO Load help_strings from wizard_config
        help_strings = HelpStrings()
        return {
            WIZARD_STRINGS: self.wizard_config[WIZARD_STRINGS],
            WIZARD_REFACTOR_FIELDS_RECENT_MAPPING_OPTIONS: self.__model.refactor_field_mapping,
            WIZARD_REFACTOR_FIELDS_LAYER_FILTERS: QgsMapLayerProxyModel.Filter(self.wizard_config[WIZARD_MAP_LAYER_PROXY_MODEL]),
            WIZARD_HELP_PAGES: self.wizard_config[WIZARD_HELP_PAGES],
            WIZARD_HELP: self.wizard_config[WIZARD_HELP],
            WIZARD_FINISH_BUTTON_TEXT: {
                EnumLayerCreationMode.REFACTOR_FIELDS: QCoreApplication.translate("WizardTranslations", "Import"),
                EnumLayerCreationMode.MANUALLY: QCoreApplication.translate("WizardTranslations", "Create")
            },
            WIZARD_SELECT_SOURCE_HELP: {
                EnumLayerCreationMode.REFACTOR_FIELDS:
                    help_strings.get_refactor_help_string(self.__db, self.__layers[self.EDITING_LAYER_NAME]),
                EnumLayerCreationMode.MANUALLY:
                    self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP1]
            }
        }

    # QSettings
    def _restore_settings(self):
        settings = self.__settings_manager.get_settings()

        if WIZARD_CREATION_MODE_KEY not in settings or settings[WIZARD_CREATION_MODE_KEY] is None:
            settings[WIZARD_CREATION_MODE_KEY] = EnumLayerCreationMode.MANUALLY

        self.__view.restore_settings(settings)

    def __save_settings(self):
        self.__settings_manager.save_settings(self.__view.get_settings())

    def wizard_rejected(self):
        message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed.").format(self.WIZARD_TOOL_NAME)
        self.logger.info_msg(__name__, message)
        self.close_wizard()

    #  TODO name?
    def close_wizard(self):
        self.__model.dispose()
        self.update_wizard_is_open_flag.emit(False)
        ViewUtils.enable_digitize_actions(self.__iface, True)
        self.enable_save_geometry_button.emit(False)
        self.__view.close()

    def create_feature(self, args: CreateFeatureArgs):
        self.__save_settings()
        if args.layer_creation_mode == EnumLayerCreationMode.REFACTOR_FIELDS:
            self.__feature_from_refactor()
        else:
            self.__feature_manual()

    def __feature_manual(self):
        self.enable_save_geometry_button.emit(True)
        self.__model.create_feature_manually()

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

    def finish_feature_creation(self, args: FinishFeatureCreationArgs):
        if not args.is_valid:
            message = QCoreApplication.translate("WizardTranslations",
                                                 "'{}' tool has been closed. Feature not found in layer {}... It's not posible create it.").format(
                self.WIZARD_TOOL_NAME, self.EDITING_LAYER_NAME)
            self.logger.warning(__name__, "Feature not found in layer {} ...".format(self.EDITING_LAYER_NAME))
        else:
            feature_tid = args.feature_tid
            message = QCoreApplication.translate("WizardTranslations",
                                                 "The new {} (t_id={}) was successfully created ").format(
                self.wizard_config[WIZARD_FEATURE_NAME], feature_tid)

        self.logger.info_msg(__name__, message)
        self.close_wizard()

    def form_rejected(self):
        message = QCoreApplication.translate("WizardTranslations",
                                       "'{}' tool has been closed because you just closed the form.").format(
            self.WIZARD_TOOL_NAME)
        self.logger.info_msg(__name__, message)
        self.close_wizard()

    # spatial
    def unexpected_features_digitized(self, args: UnexpectedFeaturesDigitizedArgs):
        message = ""
        if args.status == EnumDigitizedFeatureStatus.INVALID:
            message = QCoreApplication.translate("WizardTranslations",
                                                 "The geometry is invalid. Do you want to return to the edit session?")
        elif args.status == EnumDigitizedFeatureStatus.ZERO_FEATURES:
            message = QCoreApplication.translate("WizardTranslations",
                                                 "No geometry has been created. Do you want to return to the edit session?")
        elif args.status == EnumDigitizedFeatureStatus.OTHER:
            message = QCoreApplication.translate("WizardTranslations",
                                                 "Several geometries were created but only one was expected. Do you want to return to the edit session?")

        if not ViewUtils.show_message_associate_geometry_creation(message):
            self.__model.rollback_layer(args.layer)

            message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed.").format(
                self.WIZARD_TOOL_NAME)

            self.logger.info_msg(__name__, message)
            self.close_wizard()

    def valid_features_digitized(self, args: ValidFeaturesDigitizedArgs):
        self.enable_save_geometry_button.emit(False)

    def layer_removed(self):
        message = QCoreApplication.translate("WizardTranslations",
                                             "'{}' tool has been closed because you just removed a required layer.").format(self.WIZARD_TOOL_NAME)
        self.logger.info_msg(__name__, message)
        self.close_wizard()
