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
                             pyqtSignal)
from asistente_ladm_col.config.general_config import WIZARD_FEATURE_NAME
from asistente_ladm_col.gui.wizards.model.common.args.model_args import (UnexpectedFeaturesDigitizedArgs,
                                                                         ExecFormAdvancedArgs,
                                                                         FinishFeatureCreationArgs,
                                                                         ValidFeaturesDigitizedArgs)
from asistente_ladm_col.gui.wizards.model.common.manual_feature_creator import (SpatialFeatureCreator,
                                                                                ManualFeatureCreator)
from asistente_ladm_col.gui.wizards.model.creator_model import CreatorModel


class SingleSpatialWizardModel(CreatorModel):
    valid_features_digitized = pyqtSignal(ValidFeaturesDigitizedArgs)
    unexpected_features_digitized = pyqtSignal(UnexpectedFeaturesDigitizedArgs)

    def __init__(self, iface, db, wiz_config):
        CreatorModel.__init__(self, iface, db, wiz_config)

    def _create_feature_creator(self) -> ManualFeatureCreator:
        self._manual_feature_creator = SpatialFeatureCreator(self._iface, self.app, self._logger,
                                                             self._editing_layer, self._wizard_config[WIZARD_FEATURE_NAME], 9)
        self._manual_feature_creator.valid_features_digitized.connect(self._valid_features_digitized_invoker)
        self._manual_feature_creator.unexpected_features_digitized.connect(self.unexpected_features_digitized)

        return self._manual_feature_creator

    def exec_form_advanced(self, args: ExecFormAdvancedArgs):
        pass

    #   spatial methods
    def save_created_geometry(self):
        self._manual_feature_creator.save_created_geometry()

    def rollback_layer(self, layer):
        # stop edition in close_wizard crash qgis
        if layer.isEditable():
            layer.rollBack()

    def _valid_features_digitized_invoker(self, args: ValidFeaturesDigitizedArgs):
        self.valid_features_digitized.emit(args)
