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
from asistente_ladm_col.config.general_config import (WIZARD_HELP_PAGES,
                                                      WIZARD_HELP2,
                                                      WIZARD_FINISH_BUTTON_TEXT,
                                                      WIZARD_SELECT_SOURCE_HELP)
from asistente_ladm_col.gui.wizards.controller.controller_args import CreateFeatureArgs
from asistente_ladm_col.gui.wizards.controller.single_spatial_wizard_controller import SingleSpatialWizardController
from asistente_ladm_col.gui.wizards.model.create_right_of_way_model import CreateRightOfWayModel
from asistente_ladm_col.gui.wizards.view.create_right_of_way_view import CreateRightOfWayView


class CreateRightOfWayController(SingleSpatialWizardController):

    def __init__(self, model: CreateRightOfWayModel, iface, db, wizard_settings):
        super().__init__(model, iface, db, wizard_settings)
        self.__model = model

    def _create_view(self):
        self.__view = CreateRightOfWayView(self, self._get_view_config())
        return self.__view

    def create_feature(self, args: CreateFeatureArgs):
        if args.layer_creation_mode == EnumLayerCreationMode.MANUALLY:
            self.__model.digitizing_polygon = True

        if args.layer_creation_mode == EnumLayerCreationMode.DIGITIZING_LINE:
            self.__feature_digitizing_line()

        # TODO this implicit execute create_manually
        super().create_feature(args)

    def __feature_digitizing_line(self):
        self.__model.width_line = self.__view.get_with_line_edit()
        self.__model.digitizing_polygon = False

    def _get_view_config(self):
        view_config = super()._get_view_config()
        view_config[WIZARD_FINISH_BUTTON_TEXT][EnumLayerCreationMode.DIGITIZING_LINE] = \
            view_config[WIZARD_FINISH_BUTTON_TEXT][EnumLayerCreationMode.MANUALLY]
        view_config[WIZARD_SELECT_SOURCE_HELP][EnumLayerCreationMode.DIGITIZING_LINE] = \
            self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP2]

        return view_config
