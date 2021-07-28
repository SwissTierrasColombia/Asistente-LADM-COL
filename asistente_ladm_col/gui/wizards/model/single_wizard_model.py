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
from asistente_ladm_col.config.general_config import WIZARD_FEATURE_NAME
from asistente_ladm_col.gui.wizards.model.common.args.model_args import ExecFormAdvancedArgs
from asistente_ladm_col.gui.wizards.model.common.muanual_feature_creator import (AlphaFeatureCreator,
                                                                                 ManualFeatureCreator)
from asistente_ladm_col.gui.wizards.model.creator_model import CreatorModel


class SingleWizardModel(CreatorModel):

    def __init__(self, iface, db, wiz_config):
        super().__init__(iface, db, wiz_config)

    def exec_form_advanced(self, args: ExecFormAdvancedArgs):
        pass

    def _create_feature_creator(self) -> ManualFeatureCreator:
        return AlphaFeatureCreator(self._iface, self.app, self._logger,
                                   self._editing_layer, self._wizard_config[WIZARD_FEATURE_NAME])
