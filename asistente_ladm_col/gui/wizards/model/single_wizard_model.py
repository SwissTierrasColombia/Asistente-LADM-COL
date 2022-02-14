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
from asistente_ladm_col.gui.wizards.model.common.args.model_args import FinishFeatureCreationArgs


class SingleManager:

    def __init__(self, db, layers, editing_layer):
        self._db = db
        self._editing_layer = editing_layer
        self._layers = layers

    def finish_feature_creation(self, layerId, features):
        fid = features[0].id()
        is_valid = False
        feature_tid = None

        if self._editing_layer.getFeature(fid).isValid():
            is_valid = True
            feature_tid = self._editing_layer.getFeature(fid)[self._db.names.T_ID_F]

        return FinishFeatureCreationArgs(is_valid, feature_tid)
