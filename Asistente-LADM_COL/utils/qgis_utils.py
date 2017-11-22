# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2017-11-14
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.core import (QgsGeometry, QgsLineString, QgsDefaultValue, QgsProject,
                       QgsWkbTypes, QgsFeature, QgsDataSourceUri)

def extractAsSingleSegments(geom):
    """
    Copied from:
    https://github.com/qgis/QGIS/blob/55203a0fc2b8e35fa2909da77a84bbfde8fcba5c/python/plugins/processing/algs/qgis/Explode.py#L89
    """
    segments = []
    if geom.isMultipart():
        for part in range(geom.constGet().numGeometries()):
            segments.extend(getPolylineAsSingleSegments(geom.constGet().geometryN(part)))
    else:
        segments.extend(getPolylineAsSingleSegments(geom.constGet()))
    return segments

def getPolylineAsSingleSegments(polyline):
    """
    Copied from:
    https://github.com/qgis/QGIS/blob/55203a0fc2b8e35fa2909da77a84bbfde8fcba5c/python/plugins/processing/algs/qgis/Explode.py#L99
    """
    segments = []
    for i in range(polyline.numPoints() - 1):
        ptA = polyline.pointN(i)
        ptB = polyline.pointN(i + 1)
        segment = QgsGeometry(QgsLineString([ptA, ptB]))
        segments.append(segment)
    return segments

def configureAutomaticField(layer, field, expression):
    index = layer.fields().indexFromName(field)
    default_value = QgsDefaultValue(expression, True)
    layer.setDefaultValueDefinition(index, default_value)

def get_layer(layer_name):
    for k,layer in QgsProject.instance().mapLayers().items():
        if layer.dataProvider().name() == 'postgres':
            if QgsDataSourceUri(layer.source()).table() == layer_name.lower():
                return layer
        else:
            if '|layername=' in layer.source(): # GeoPackage layers
                if layer.source().split()[-1] == layer_name.lower():
                    return layer
    return None

def explode_boundaries(self):
    print("EXPLODE!!!")
    layer = get_layer('lindero')
    if len(layer.selectedFeatures()) == 0:
        return None

    segments = list()
    for f in layer.selectedFeatures():
        segments.extend(extractAsSingleSegments(f.geometry()))

    # Remove the selected lines, we'll add exploded segments in a while
    layer.deleteFeatures([sf.id() for sf in layer.selectedFeatures()])

    # Create features based on segment geometries
    exploded_features = list()
    for segment in segments:
        feature = QgsFeature(layer.fields())
        feature.setGeometry(segment)
        exploded_features.append(feature)

    layer.addFeatures(exploded_features)

def merge_boundaries(self):
    print("MERGE!!!")
    layer = get_layer('lindero')
    if len(layer.selectedFeatures()) < 2:
        return None

    unionGeom = layer.selectedFeatures()[0].geometry()
    for f in layer.selectedFeatures()[1:]:
        if not f.geometry().isNull():
            unionGeom = unionGeom.combine(f.geometry())

    # Remove the selected lines, we'll add exploded segments in a while
    layer.deleteFeatures([sf.id() for sf in layer.selectedFeatures()])

    # Convert to mulipart geometry if needed
    if QgsWkbTypes.isMultiType(layer.wkbType()) and not unionGeom.isMultipart():
        unionGeom.convertToMultiType()

    feature = QgsFeature(layer.fields())
    feature.setGeometry(unionGeom)
    layer.addFeature(feature)
