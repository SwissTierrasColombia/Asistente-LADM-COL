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
from asistente_ladm_col.gui.wizards.model.common.args.model_args import (UnexpectedFeaturesDigitizedArgs,
                                                                         ExecFormAdvancedArgs,
                                                                         FinishFeatureCreationArgs,
                                                                         ValidFeaturesDigitizedArgs)
from asistente_ladm_col.gui.wizards.model.common.muanual_feature_creator import (SpatialFeatureCreator,
                                                                                 ManualFeatureCreator)
from asistente_ladm_col.gui.wizards.model.common.observers import (ValidFeatureDigitizedObserver,
                                                                   UnexpectedFeatureDigitizedObserver)
from asistente_ladm_col.gui.wizards.model.creator_model import CreatorModel


class SingleSpatialWizardModel(CreatorModel):

    def __init__(self, iface, db, wiz_config):
        super().__init__(iface, db, wiz_config)

        self.__valid_feature_observer_list = list()
        self.__unexpected_features_digitized_observer_list = list()
        self.__layer_removed_observer_list = list()

    def _create_feature_creator(self) -> ManualFeatureCreator:
        self._manual_feature_creator = SpatialFeatureCreator(self._iface, self.app, self._logger,
                                                             self._editing_layer, self._wizard_config[WIZARD_FEATURE_NAME], 9)
        self._manual_feature_creator.register_geometry_observer(self)

        return self._manual_feature_creator

    def finish_feature_creation(self, layerId, features):
        fid = features[0].id()
        is_valid = False
        feature_tid = None

        if not self._editing_layer.getFeature(fid).isValid():
            self._logger.warning(__name__, "Feature not found in layer {} ...".format(self._editing_layer_name))
        else:
            is_valid = True
            feature_tid = self._editing_layer.getFeature(fid)[self._db.names.T_ID_F]

        args = FinishFeatureCreationArgs(is_valid, feature_tid)
        self._notify_finish_feature_creation(args)

    def exec_form_advanced(self, args: ExecFormAdvancedArgs):
        pass

    #   spatial methods
    def save_created_geometry(self):
        self._manual_feature_creator.save_created_geometry()

    def valid_features_digitized(self, args: ValidFeaturesDigitizedArgs):
        self.__notify_valid_features(args)

    def unexpected_features_digitized(self, args: UnexpectedFeaturesDigitizedArgs):
        self.__notify_unexpected_features_digitized(args)

    def __notify_valid_features(self, args: ValidFeaturesDigitizedArgs):
        for item in self.__valid_feature_observer_list:
            item.valid_features_digitized(args)

    def __notify_unexpected_features_digitized(self, args: UnexpectedFeaturesDigitizedArgs):
        for item in self.__unexpected_features_digitized_observer_list:
            item.unexpected_features_digitized(args)

    def register_valid_features_digitized_observer(self, observer: ValidFeatureDigitizedObserver):
        self.__valid_feature_observer_list.append(observer)

    def remove_valid_features_digitized_observer(self, observer: ValidFeatureDigitizedObserver):
        self.__valid_feature_observer_list.remove(observer)

    def register_unexpected_features_digitized_observer(self, observer: UnexpectedFeatureDigitizedObserver):
        self.__unexpected_features_digitized_observer_list.append(observer)

    def remove_unexpected_features_digitized_observer(self, observer: UnexpectedFeatureDigitizedObserver):
        self.__unexpected_features_digitized_observer_list.remove(observer)

    def rollback_layer(self, layer):
        # stop edition in close_wizard crash qgis
        if layer.isEditable():
            layer.rollBack()
