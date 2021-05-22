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
from asistente_ladm_col.config.general_config import (WIZARD_FEATURE_NAME,
                                                      WIZARD_LAYERS)
from asistente_ladm_col.config.layer_config import LayerConfig
from asistente_ladm_col.gui.wizards.model.common.args.model_args import ExecFormAdvancedArgs
from asistente_ladm_col.gui.wizards.model.common.create_manually import (FeatureCreator,
                                                                         AlphaFeatureCreator)
from asistente_ladm_col.gui.wizards.model.common.feature_selector_manager import FeatureSelectorManager
from asistente_ladm_col.gui.wizards.model.creator_model import CreatorModel
from asistente_ladm_col.gui.wizards.view.common.view_enum import EnumOptionType


class ParcelCreatorModel(CreatorModel, FeatureSelectorManager):

    def __init__(self, iface, db, wiz_config):
        CreatorModel.__init__(self, iface, db, wiz_config)

        self._layers = wiz_config[WIZARD_LAYERS]

        self.__selectable_layers_by_type = dict()
        self.__init_selectable_layer_by_type()

        # parent constructor
        FeatureSelectorManager.__init__(self, self.__selectable_layers_by_type, iface, self._logger)

    def __init_selectable_layer_by_type(self):
        # TODO Change the name
        self.__selectable_layers_by_type[EnumOptionType.PLOT] = self._layers[self._db.names.LC_PLOT_T]
        self.__selectable_layers_by_type[EnumOptionType.BUILDING] = self._layers[self._db.names.LC_BUILDING_T]
        self.__selectable_layers_by_type[EnumOptionType.BUILDING_UNIT] = self._layers[self._db.names.LC_BUILDING_UNIT_T]

    def _create_feature_creator(self) -> FeatureCreator:
        return AlphaFeatureCreator(self._iface, self.app, self._logger,
                                   self._editing_layer, self._wizard_config[WIZARD_FEATURE_NAME])

    def exec_form_advanced(self, args: ExecFormAdvancedArgs):
        fid = args.feature.id()

        # assigns the type of parcel before to creating it
        parcel_condition_field_idx = args.layer.getFeature(fid).fieldNameIndex(self._db.names.LC_PARCEL_T_PARCEL_TYPE_F)
        #args.layer.changeAttributeValue(fid, parcel_condition_field_idx,
         #                          self.cb_parcel_type.itemData(self.cb_parcel_type.currentIndex()))

    def finish_feature_creation(self, layerId, features):
        pass

    # parcel
    def get_type_parcel_conditions(self):
        result = dict()
        constraint_types_of_parcels = LayerConfig.get_constraint_types_of_parcels(self._db.names)
        for feature in self._layers[self._db.names.LC_CONDITION_PARCEL_TYPE_D].getFeatures():
            if feature[self._db.names.ILICODE_F] in constraint_types_of_parcels:
                result[feature[self._db.names.T_ID_F]] = feature[self._db.names.DISPLAY_NAME_F]
        return result

