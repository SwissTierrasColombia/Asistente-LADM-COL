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
import processing

from qgis.core import (QgsProject,
                       QgsVectorLayerUtils,
                       QgsVectorLayer)

from asistente_ladm_col.config.general_config import (WIZARD_EDITING_LAYER_NAME,
                                                      WIZARD_LAYERS)
from asistente_ladm_col.config.translation_strings import (TranslatableConfigStrings,
                                                           RIGHT_OF_WAY_LINE_LAYER)
from asistente_ladm_col.gui.wizards.model.common.args.model_args import ValidFeaturesDigitizedArgs
from asistente_ladm_col.gui.wizards.model.common.layer_remove_signals_manager import LayerRemovedSignalsManager
from asistente_ladm_col.gui.wizards.model.single_spatial_wizard_model import SingleSpatialWizardModel
from asistente_ladm_col.utils.crs_utils import get_crs_authid


class RightOfWayModel(SingleSpatialWizardModel):

    def __init__(self, iface, db, wiz_config):
        super().__init__(iface, db, wiz_config)
        self.__wizard_config = wiz_config
        self.__editing_layer_name = self.__wizard_config[WIZARD_EDITING_LAYER_NAME]
        self.__editing_layer = self.__wizard_config[WIZARD_LAYERS][self.__editing_layer_name]

        self.__temporal_layer = {"memory_line_layer": None}
        self.__translatable_config_strings = TranslatableConfigStrings()

        self.digitizing_polygon = True
        self.width_line = 1.0
        self.__layer_removed_signal_manager = None

    def create_feature_manually(self):
        if not self.digitizing_polygon:
            self.__add_memory_line_layer()
        else:
            self._manual_feature_creator.editing_layer = None

        super().create_feature_manually()

    def _valid_features_digitized_invoker(self, args: ValidFeaturesDigitizedArgs):
        super()._valid_features_digitized_invoker(args)

        if not self.digitizing_polygon:
            layer = args.layer

            # Get temporal right of way geometry
            feature = self.__get_feature_with_buffer_right_of_way(layer)
            layer.commitChanges()

            # Change target layer (temporal by db layer)
            layer = self.__editing_layer

            # Add temporal geometry create
            if not layer.isEditable():
                layer.startEditing()

            self.app.core.suppress_form(layer, True)
            args.feature = feature
            layer.addFeature(feature)

    def dispose(self):
        super().dispose()
        if self.__layer_removed_signal_manager:
            self.__layer_removed_signal_manager.disconnect_signals()
        if self.__temporal_layer["memory_line_layer"]:
            self.rollback_layer(self.__temporal_layer["memory_line_layer"])
            QgsProject.instance().removeMapLayer(self.__temporal_layer["memory_line_layer"])

    def __get_feature_with_buffer_right_of_way(self, layer):
        params = {'INPUT': layer,
                  'DISTANCE': self.width_line,
                  'SEGMENTS': 5,
                  'END_CAP_STYLE': 1,  # Flat
                  'JOIN_STYLE': 2,
                  'MITER_LIMIT': 2,
                  'DISSOLVE': False,
                  'OUTPUT': 'memory:'}
        buffered_right_of_way_layer = processing.run("native:buffer", params)['OUTPUT']
        buffer_geometry = buffered_right_of_way_layer.getFeature(1).geometry()
        feature = QgsVectorLayerUtils().createFeature(self.__editing_layer, buffer_geometry)
        return feature

    def __add_memory_line_layer(self):
        translated_strings = self.__translatable_config_strings.get_translatable_config_strings()
        # Add Memory line layer
        temporal_layer = QgsVectorLayer(
            "MultiLineString?crs={}".format(get_crs_authid(self.__editing_layer.sourceCrs())),
            translated_strings[RIGHT_OF_WAY_LINE_LAYER], "memory")
        QgsProject.instance().addMapLayer(temporal_layer, True)

        self.__temporal_layer["memory_line_layer"] = temporal_layer
        self.__layer_removed_signal_manager = LayerRemovedSignalsManager(self.__temporal_layer)
        self.__layer_removed_signal_manager.layer_removed.connect(self.layer_removed)

        self.__layer_removed_signal_manager.connect_signals()

        self._manual_feature_creator.editing_layer = temporal_layer
