# -*- coding: utf-8 -*-

"""
***************************************************************************
    PolygonsToLines.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""
# https://github.com/qgis/QGIS/blob/master/python/plugins/processing/algs/qgis/PolygonsToLines.py
# customization of PolygonsToLines algorithm due to bug.
#   File "/usr/share/qgis/python/plugins/processing/algs/qgis/PolygonsToLines.py", line 85, in processFeature
#     feature.setGeometry(QgsGeometry(self.convertToLines(feature.geometry())))
#   File "/usr/share/qgis/python/plugins/processing/algs/qgis/PolygonsToLines.py", line 102, in convertToLines
#     rings = self.getRings(geometry.constGet())
#   File "/usr/share/qgis/python/plugins/processing/algs/qgis/PolygonsToLines.py", line 120, in getRings
#     rings.extend(self.getRings(geometry.geometryN(i)))
#   File "/usr/share/qgis/python/plugins/processing/algs/qgis/PolygonsToLines.py", line 123, in getRings
#     rings.append(geometry.exteriorRing().clone())
# AttributeError: 'QgsPoint' object has no attribute 'exteriorRing

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsGeometry,
                       QgsPoint,
                       QgsPolygon,
                       QgsMultiPolygon,
                       QgsCurvePolygon,
                       QgsGeometryCollection,
                       QgsMultiLineString,
                       QgsMultiCurve,
                       QgsWkbTypes,
                       QgsProcessing)

from processing.algs.qgis.QgisAlgorithm import QgisFeatureBasedAlgorithm


class PolygonsToLines(QgisFeatureBasedAlgorithm):

    def tags(self):
        return (QCoreApplication.translate("PolygonsToLines", 'line,polygon,convert')).split(',')

    def group(self):
        return QCoreApplication.translate("PolygonsToLines", 'Vector geometry')

    def groupId(self):
        return 'vectorgeometry'

    def __init__(self):
        super().__init__()

    def name(self):
        return 'polygonstolines'

    def displayName(self):
        return QCoreApplication.translate("PolygonsToLines", 'Polygons to lines')

    def outputName(self):
        return QCoreApplication.translate("PolygonsToLines", 'Lines')

    def outputType(self):
        return QgsProcessing.TypeVectorLine

    def inputLayerTypes(self):
        return [QgsProcessing.TypeVectorPolygon]

    def outputWkbType(self, input_wkb_type):
        return self.convertWkbToLines(input_wkb_type)

    def processFeature(self, feature, context, feedback):
        if feature.hasGeometry():
            feature.setGeometry(QgsGeometry(self.convertToLines(feature.geometry())))
        return [feature]

    def supportInPlaceEdit(self, layer):
        return False

    def convertWkbToLines(self, wkb):
        multi_wkb = QgsWkbTypes.NoGeometry
        if QgsWkbTypes.singleType(QgsWkbTypes.flatType(wkb)) == QgsWkbTypes.Polygon:
            multi_wkb = QgsWkbTypes.MultiLineString
        elif QgsWkbTypes.singleType(QgsWkbTypes.flatType(wkb)) == QgsWkbTypes.CurvePolygon:
            multi_wkb = QgsWkbTypes.MultiCurve
        if QgsWkbTypes.hasM(wkb):
            multi_wkb = QgsWkbTypes.addM(multi_wkb)
        if QgsWkbTypes.hasZ(wkb):
            multi_wkb = QgsWkbTypes.addZ(multi_wkb)

        return multi_wkb

    def convertToLines(self, geometry):
        rings = self.getRings(geometry.constGet())
        output_wkb = self.convertWkbToLines(geometry.wkbType())
        out_geom = None
        if QgsWkbTypes.flatType(output_wkb) == QgsWkbTypes.MultiLineString:
            out_geom = QgsMultiLineString()
        else:
            out_geom = QgsMultiCurve()

        for ring in rings:
            out_geom.addGeometry(ring)

        return out_geom

    def getRings(self, geometry):
        rings = []

        # TODO: remove when the error is resolved
        # Error: The expected object type is a QgsCurvePolygon but it receives a QgsPoint, however the WKT of the
        #        QgsPoint corresponds to either a QgsPolygon or QgsMultiPolygon (yeap, it must be a bug in QGIS)
        if type(geometry) == type(QgsPoint()):
            geom = QgsGeometry().fromWkt(geometry.asWkt())
            curve = None
            if geom.isMultipart():
                curve = QgsMultiPolygon()
                curve.fromWkt(geom.asWkt())
            else:
                curve = QgsPolygon()
                curve.fromWkt(geom.asWkt())

            geometry = curve.toCurveType()

        if isinstance(geometry, QgsGeometryCollection):
            # collection
            for i in range(geometry.numGeometries()):
                if QgsWkbTypes.geometryType(geometry.geometryN(i).wkbType()) == QgsWkbTypes.PolygonGeometry:
                    rings.extend(self.getRings(geometry.geometryN(i)))
        else:
            # Converts geometry to curve, because exteriorRing is a method from curve polygons
            if isinstance(geometry, QgsPolygon):
                geom = geometry.toCurveType()
                geometry = geom

            # not collection
            rings.append(geometry.exteriorRing().clone())
            for i in range(geometry.numInteriorRings()):
                rings.append(geometry.interiorRing(i).clone())

        return rings
