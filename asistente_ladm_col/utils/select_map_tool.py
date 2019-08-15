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
from qgis.PyQt.QtGui import (QColor,
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
    selected_feature_ids = list()

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
        if e.button() & Qt.LeftButton:
            self.startPoint = self.toMapCoordinates(e.pos())
            self.endPoint = self.startPoint
            self.isEmittingPoint = True

    def canvasReleaseEvent(self, e):
        if e.button() & Qt.LeftButton:
            self.isEmittingPoint = False
            self.show_rubber_band()

            if self._multi and (e.modifiers() & Qt.ControlModifier or e.modifiers() & Qt.ShiftModifier):
                if self.rubberBand.asGeometry().type() == QgsWkbTypes.PolygonGeometry:
                    self.reset()
                    return
                else:
                    id_features_intersect = self.ids_features_intersect()

                # if Control or Shift are selected, keeps the previous selection
                for id_feature_intersect in id_features_intersect:
                    # toggle selected feature
                    if id_feature_intersect not in self.selected_feature_ids:
                        self.selected_feature_ids.append(id_feature_intersect)
                    else:
                        self.selected_feature_ids.remove(id_feature_intersect)
            else:
                id_features_intersect = self.ids_features_intersect()
                # Clear selected features if Control or Shift are not selected
                self.selected_feature_ids = id_features_intersect

            self.select_features()
        elif e.button() & Qt.RightButton:
            self.features_selected_signal.emit()
            self.reset()

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

            # Approximate polygon to point when it's too small related to the scale
            if (self.rubberBand.asGeometry().area() / self.canvas.extent().area()) * 1000000 < 50:
                self.rubberBand.reset(QgsWkbTypes.PointGeometry)
                self.rubberBand.addPoint(self.startPoint, True)  # true to update canvas

    def ids_features_intersect(self):
        index = QgsSpatialIndex(self._layer)
        bbox = self.rubberBand.asGeometry().boundingBox()

        candidate_features = self._layer.getFeatures(index.intersects(bbox))
        geom = self.rubberBand.asGeometry()
        centroid = geom

        if not self._multi and geom.type() == QgsWkbTypes.PolygonGeometry:
            centroid = geom.centroid()

        features_selected = []
        distances_features_selected = dict()
        for candidate_feature in candidate_features:
            if candidate_feature.geometry().intersects(geom):
                features_selected.append(candidate_feature.id())
                # Calculate the distance to the centroid
                distances_features_selected[candidate_feature.id()] = candidate_feature.geometry().distance(centroid)

        if not self._multi and geom.type() == QgsWkbTypes.PolygonGeometry:
            if features_selected:
                # Get the key corresponding to the minimum value within a dictionary
                features_selected = [min(distances_features_selected, key=distances_features_selected.get)]

        return features_selected

    def select_features(self):
        # show features selected
        self._layer.selectByIds(self.selected_feature_ids)
        self.reset()

    def deactivate(self):
        QgsMapTool.deactivate(self)
        self.deactivated.emit()
