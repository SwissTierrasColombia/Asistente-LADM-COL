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

from asistente_ladm_col.config.translation_strings import (TranslatableConfigStrings,
                                                           RIGHT_OF_WAY_LINE_LAYER)
from asistente_ladm_col.gui.wizards.model.common.args.model_args import FinishFeatureCreationArgs
from asistente_ladm_col.utils.crs_utils import get_crs_authid


class RightOfWayManager:

    def __init__(self, db, layers, editing_layer):
        self._db = db
        self.__layers = layers
        self.__translatable_config_strings = TranslatableConfigStrings()
        self.width_line = 1.0

        self._editing_layer = editing_layer
        self.app = None

    def finish_feature_creation(self, layerId, features):
        fid = features[0].id()
        is_valid = False
        feature_tid = None

        if self._editing_layer.getFeature(fid).isValid():
            is_valid = True
            feature_tid = self._editing_layer.getFeature(fid)[self._db.names.T_ID_F]

        return FinishFeatureCreationArgs(is_valid, feature_tid)

    def get_memory_line_layer(self, base_layer):
        translated_strings = self.__translatable_config_strings.get_translatable_config_strings()
        # Add Memory line layer
        temporal_layer = QgsVectorLayer(
            "MultiLineString?crs={}".format(get_crs_authid(base_layer.sourceCrs())),
            translated_strings[RIGHT_OF_WAY_LINE_LAYER], "memory")

        return temporal_layer

    def get_feature_with_buffer_right_of_way(self, tmp_layer, layer):
        params = {'INPUT': tmp_layer,
                  'DISTANCE': self.width_line,
                  'SEGMENTS': 5,
                  'END_CAP_STYLE': 1,  # Flat
                  'JOIN_STYLE': 2,
                  'MITER_LIMIT': 2,
                  'DISSOLVE': False,
                  'OUTPUT': 'memory:'}
        buffered_right_of_way_layer = processing.run("native:buffer", params)['OUTPUT']
        buffer_geometry = buffered_right_of_way_layer.getFeature(1).geometry()
        feature = QgsVectorLayerUtils().createFeature(layer, buffer_geometry)
        tmp_layer.commitChanges()

        return feature

    def add_tmp_feature_to_layer(self, layer, tmp_feature):
        # Add temporal geometry create
        if not layer.isEditable():
            layer.startEditing()

        self.app.core.suppress_form(layer, True)

        layer.addFeature(tmp_feature)
