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
from asistente_ladm_col.config.general_config import WIZARD_STRINGS
from asistente_ladm_col.gui.wizards.view.common.select_source import (SelectSource,
                                                                      SelectSourceExt)
from asistente_ladm_col.gui.wizards.view.single_wizard_view import SingleWizardView
from asistente_ladm_col.gui.wizards.wizard_constants import (WIZARD_REFACTOR_RECENT_MAPPING_OPTIONS,
                                                             WIZARD_REFACTOR_LAYER_FILTERS)


class CreateRightOfWayView(SingleWizardView):

    def __init__(self, controller, view_config):
        self.__view_config = view_config
        super().__init__(controller, view_config)

    def _create_select_source(self) -> SelectSource:
        self.__wp_select_source = SelectSourceExt(self.__view_config[WIZARD_REFACTOR_RECENT_MAPPING_OPTIONS],
                                                  self.__view_config[WIZARD_REFACTOR_LAYER_FILTERS],
                                                  self.__view_config[WIZARD_STRINGS])

        return self.__wp_select_source

    def get_with_line_edit(self):
        return self.__wp_select_source.get_with_line_edit()
