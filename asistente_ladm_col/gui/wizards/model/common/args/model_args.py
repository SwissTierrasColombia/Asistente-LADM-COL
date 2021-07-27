# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2021-05-21
        git sha              : :%H$
        copyright            : (C) 2021 by Yesid Polanía (BFS Swissphoto)
        email                : yesidpol.3@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
 """
from qgis.core import QgsVectorLayer

from asistente_ladm_col.config.enums import EnumDigitizedFeatureStatus


class FinishFeatureCreationArgs:
    def __init__(self, is_valid, feature_tid):
        self.is_valid = is_valid
        self.feature_tid = feature_tid


class SpacialSourceFinishFeatureCreationArgs(FinishFeatureCreationArgs):
    def __init__(self, is_valid=None, feature_tid=None, added_features_amount=None, associated_features_amount=None):
        super().__init__(is_valid, feature_tid)
        self.added_features_amount = added_features_amount
        self.associated_features_amount = associated_features_amount


class ParcelFinishFeatureCreationArgs(FinishFeatureCreationArgs):
    def __init__(self, is_valid=None, feature_tid=None, added_features_amount=None,
                 associated_features_amount=None, valid_constraints=False):
        super().__init__(is_valid, feature_tid)
        self.added_features_amount = added_features_amount
        self.associated_features_amount = associated_features_amount
        self.valid_constraints = valid_constraints


class UnexpectedFeaturesDigitizedArgs:
    def __init__(self, layer: QgsVectorLayer, status: EnumDigitizedFeatureStatus, features_count: int):
        self.layer = layer
        self.status = status
        self.features_count = features_count


class ValidFeaturesDigitizedArgs:
    def __init__(self, layer: QgsVectorLayer, feature):
        self.layer = layer
        self.feature = feature


class ExecFormAdvancedArgs:
    def __init__(self, layer: QgsVectorLayer, feature):
        self.layer = layer
        self.feature = feature
