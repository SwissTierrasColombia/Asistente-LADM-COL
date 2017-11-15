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
from qgis.core import QgsGeometry, QgsLineString, QgsDefaultValue

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
    default_value = QgsDefaultValue("$length", True)
    layer.setDefaultValueDefinition(index, default_value)
