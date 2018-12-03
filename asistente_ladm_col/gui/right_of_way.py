# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 03/12/18
        git sha              : :%H$
        copyright            : (C) 2018 by Sergio Ramírez (Incige SAS)
        email                : sergio.ramirez@incige.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from functools import partial

from qgis.PyQt.QtCore import (Qt,
                              QObject,
                              pyqtSignal,
                              QCoreApplication,
                              QSettings)

from qgis.core import (
                       Qgis,
                       QgsApplication,
                       QgsProject,
                       QgsVectorLayer,
                       QgsEditFormConfig,
                       QgsWkbTypes,
                       QgsSnappingConfig,
                       QgsTolerance,
                       QgsVectorLayerUtils
)

import processing

from ..config.table_mapping_config import RIGHT_OF_WAY_TABLE, SURVEY_POINT_TABLE

from ..config.general_config import (
    DEFAULT_EPSG,
    PLUGIN_NAME,
    TranslatableConfigStrings
)

from ..utils.qgis_utils import QGISUtils

class RightOfWay(QObject):

    def __init__(self, iface, qgis_utils):
        QObject.__init__(self)
        self.qgis_utils = qgis_utils

        self._right_of_way_layer = None
        self.iface = iface
        self.addedFeatures = None

    def prepare_right_of_way_line_creation(self, db, _right_of_way_layer, tb_strings, iface, width_value):
        # Load layers
        self.add_db_required_layers(db, iface)
        # Add Memory line layer
        self._right_of_way_line_layer = QgsVectorLayer("MultiLineString?crs=EPSG:{}".format(DEFAULT_EPSG),
                                    tb_strings.RIGHT_OF_WAY_LINE_LAYER, "memory")
        QgsProject.instance().addMapLayer(self._right_of_way_line_layer, True)

        # Disable transactions groups and configure Snapping
        self.set_layers_settings()

        # Suppress feature form
        form_config = self._right_of_way_line_layer.editFormConfig()
        form_config.setSuppress(QgsEditFormConfig.SuppressOn)
        self._right_of_way_line_layer.setEditFormConfig(form_config)

        # Enable edition mode
        iface.layerTreeView().setCurrentLayer(self._right_of_way_line_layer)
        self._right_of_way_line_layer.startEditing()
        iface.actionAddFeature().trigger()

        self._right_of_way_line_layer.featureAdded.connect(self.store_features_ids)
        self._right_of_way_line_layer.editCommandEnded.connect(self.update_attributes_after_adding)
        self._right_of_way_line_layer.committedFeaturesAdded.connect(partial(self.finish_right_of_way_line, width_value, iface))

        iface.messageBar().pushMessage('Asistente LADM_COL',
            QCoreApplication.translate('CreateRightOfWayCadastreWizard',
                                       "You can now start capturing line right of way digitizing on the map..."),
            Qgis.Info)

    def set_layers_settings(self):
        # Disable transactions groups
        QgsProject.instance().setAutoTransaction(False)

        # Configure Snapping
        snapping = QgsProject.instance().snappingConfig()
        snapping.setEnabled(True)
        snapping.setMode(QgsSnappingConfig.AllLayers)
        snapping.setType(QgsSnappingConfig.Vertex)
        snapping.setUnits(QgsTolerance.Pixels)
        snapping.setTolerance(9)
        QgsProject.instance().setSnappingConfig(snapping)

    def add_db_required_layers(self, db, iface):
        # Load layers
        res_layers = self.qgis_utils.get_layers(db, {
            RIGHT_OF_WAY_TABLE: {'name': RIGHT_OF_WAY_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            SURVEY_POINT_TABLE: {'name': SURVEY_POINT_TABLE, 'geometry': None}
        }, load=True)

        self._right_of_way_layer = res_layers[RIGHT_OF_WAY_TABLE]
        self._survey_point_layer = res_layers[SURVEY_POINT_TABLE]

        if self._right_of_way_layer is None:
            iface.messageBar().pushMessage('Asistente LADM_COL',
                QCoreApplication.translate('CreateRightOfWayCadastreWizard',
                                           "Right of Way layer couldn't be found... {}").format(db.get_description()),
                Qgis.Warning)
            return

        if self._survey_point_layer is None:
            iface.messageBar().pushMessage('Asistente LADM_COL',
                QCoreApplication.translate('CreateRightOfWayCadastreWizard',
                                           "Survey Point layer couldn't be found... {}").format(db.get_description()),
                Qgis.Warning)
            return

        form_config = self._right_of_way_layer.editFormConfig()
        form_config.setSuppress(QgsEditFormConfig.SuppressOff)
        self._right_of_way_layer.setEditFormConfig(form_config)

    def store_features_ids(self, featId):
         """
         This method only stores featIds in a class variable
         """
         self.addedFeatures = featId

    def update_attributes_after_adding(self):
        layer = self.sender() #here I can get the layer that has sent the signal
        self.log = QgsApplication.messageLog()
        layer.featureAdded.disconnect(self.store_features_ids)
        self.log.logMessage("RigthOfWayLine's featureAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        res = layer.commitChanges()
        QgsProject.instance().removeMapLayer(layer)
        self.addedFeatures = None

    def finish_right_of_way_line(self, width_value, iface, layerId, features):
        self.log = QgsApplication.messageLog()
        self._right_of_way_line_layer.committedFeaturesAdded.disconnect()
        self.log.logMessage("RigthOfWayLine's committedFeaturesAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        params = {'INPUT':self._right_of_way_line_layer,
                  'DISTANCE':width_value,
                  'SEGMENTS':5,
                  'END_CAP_STYLE':1,
                  'JOIN_STYLE':2,
                  'MITER_LIMIT':2,
                  'DISSOLVE':False,
                  'OUTPUT':'memory:'}
        buffered_right_of_way_layer = processing.run("native:buffer", params)['OUTPUT']

        serv = buffered_right_of_way_layer.getFeature(1).geometry()
        feature = QgsVectorLayerUtils().createFeature(self._right_of_way_layer, serv)

        if feature:
            self._right_of_way_layer.startEditing()
            self._right_of_way_layer.addFeature(feature)
            form = iface.getFeatureForm(self._right_of_way_layer, feature)
            form.show()
