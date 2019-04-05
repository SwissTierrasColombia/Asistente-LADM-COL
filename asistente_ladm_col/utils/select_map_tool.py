# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-04-04
        git sha              : :%H$
        copyright            : (C) 2018 by Leo Cardona (BSF Swissphoto)
        email                : leo.cardona.p@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt5.QtGui import (QColor,
                         QCursor)
from qgis.PyQt.QtCore import (Qt,
                              pyqtSignal)
from qgis.gui import (QgsMapTool,
                      QgsMapToolEmitPoint,
                      QgsRubberBand)
from qgis.core import (QgsPointXY,
                       QgsSpatialIndex,
                       QgsWkbTypes)


class SelectMapTool(QgsMapToolEmitPoint):

    features_selected_signal = pyqtSignal()

    def __init__(self, canvas, layer, multi=True):
        self.canvas = canvas
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self._multi = multi
        self._layer = layer

        # Cursor
        cursor = QCursor()
        cursor.setShape(Qt.CrossCursor)
        self.setCursor(cursor)

        # RubberBand Style
        self.rubberBand = QgsRubberBand(self.canvas, True)
        self.rubberBand.setBrushStyle(Qt.Dense4Pattern)
        self.rubberBand.setColor(QColor(255, 181, 92))
        self.rubberBand.setStrokeColor(QColor(232, 137, 72))
        self.rubberBand.setWidth(0.2)
        self.reset()

    def reset(self):
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        self.rubberBand.reset(True)

    def canvasPressEvent(self, e):
        self.startPoint = self.toMapCoordinates(e.pos())
        self.endPoint = self.startPoint
        self.isEmittingPoint = True

    def canvasReleaseEvent(self, e):
        self.isEmittingPoint = False
        self.show_rubber_band()
        self.intersection()

    def canvasDoubleClickEvent(self, e):
        self.canvasPressEvent(e)

    def canvasMoveEvent(self, e):
        if not self.isEmittingPoint:
            return
        self.endPoint = self.toMapCoordinates(e.pos())
        self.show_rubber_band()

    def show_rubber_band(self):
        self.create_rubber_band()
        if self.rubberBand:
            self.rubberBand.show()

    def create_rubber_band(self):
        self.rubberBand.reset(True)

        if self.startPoint is None and self.endPoint is None:
            return None
        elif self.startPoint.x() == self.endPoint.x() or self.startPoint.y() == self.endPoint.y():
            self.rubberBand.reset(QgsWkbTypes.PointGeometry)
            self.rubberBand.addPoint(self.startPoint, True)  # true to update canvas
        else:
            self.rubberBand.reset(QgsWkbTypes.PolygonGeometry)

            point1 = QgsPointXY(self.startPoint.x(), self.startPoint.y())
            point2 = QgsPointXY(self.startPoint.x(), self.endPoint.y())
            point3 = QgsPointXY(self.endPoint.x(), self.endPoint.y())
            point4 = QgsPointXY(self.endPoint.x(), self.startPoint.y())

            self.rubberBand.addPoint(point1, False)
            self.rubberBand.addPoint(point2, False)
            self.rubberBand.addPoint(point3, False)
            self.rubberBand.addPoint(point4, True)  # true to update canvas

    def intersection(self):
        index = QgsSpatialIndex(self._layer)
        bbox = self.rubberBand.asGeometry().boundingBox()

        cadidate_features = self._layer.getFeatures(index.intersects(bbox))
        geom = self.rubberBand.asGeometry()
        centroid = geom

        if not self._multi and geom.type() == QgsWkbTypes.PolygonGeometry:
            centroid = geom.centroid()

        features_selected = []
        distances_features_selected = dict()
        for cadidate_feature in cadidate_features:
            if cadidate_feature.geometry().intersects(geom):
                features_selected.append(cadidate_feature.id())
                # Calculate the distance to the centroid
                distances_features_selected[cadidate_feature.id()] = cadidate_feature.geometry().distance(centroid)

        if not self._multi and geom.type() == QgsWkbTypes.PolygonGeometry:
            if features_selected:
                # Get the key corresponding to the minimum value within a dictionary
                features_selected = [min(distances_features_selected, key=distances_features_selected.get)]

        # show features selected
        self._layer.selectByIds(features_selected)

        # emit the signal when at least one element has been selected
        if len(self._layer.selectedFeatures()):
            self.features_selected_signal.emit()

        self.reset()

    def deactivate(self):
        QgsMapTool.deactivate(self)
        self.deactivated.emit()
