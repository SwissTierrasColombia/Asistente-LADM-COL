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
from qgis.core import QgsVectorLayerUtils


class AssociationUtils:

    @staticmethod
    def get_list_of_features_ids(layer, t_id_f):
        result = []
        if layer is not None and layer.selectedFeatureCount() > 0:
            result = [f[t_id_f] for f in layer.selectedFeatures()]
        return result

    @staticmethod
    def save_relations(layer, attr_fkey_1, id_list, attr_fkey_2, spatial_source_id):
        new_features = list()
        for feature_id in id_list:
            new_feature = QgsVectorLayerUtils().createFeature(layer)
            new_feature.setAttribute(attr_fkey_1, feature_id)
            new_feature.setAttribute(attr_fkey_2, spatial_source_id)
            # TODO self.logger.info(__name__, "Saving Plot-SpatialSource: {}-{}".format(feature_id, spatial_source_id))
            new_features.append(new_feature)

        layer.dataProvider().addFeatures(new_features)

        return new_features
