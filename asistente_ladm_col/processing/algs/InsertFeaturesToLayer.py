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
import os

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QVariant, QCoreApplication

from qgis.core import (
                       edit,
                       QgsEditError,
                       QgsGeometry,
                       QgsWkbTypes,
                       QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingOutputVectorLayer,
                       QgsProject,
                       QgsVectorLayerUtils
                       )

class InsertFeaturesToLayer(QgsProcessingAlgorithm):

    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'

    def createInstance(self):
        return type(self)()

    def group(self):
        return QCoreApplication.translate("InsertFeaturesToLayer", 'Vector table')

    def groupId(self):
        return 'vectortable'

    def tags(self):
        return (QCoreApplication.translate("InsertFeaturesToLayer", 'append,copy,insert,features,paste')).split(',')

    def __init__(self):
        super().__init__()

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(self.INPUT,
                                                              QCoreApplication.translate("InsertFeaturesToLayer", 'Input layer'),
                                                              [QgsProcessing.TypeVector]))
        self.addParameter(QgsProcessingParameterVectorLayer(self.OUTPUT,
                                                              QCoreApplication.translate("InsertFeaturesToLayer", 'Output layer'),
                                                              [QgsProcessing.TypeVector]))
        self.addOutput(QgsProcessingOutputVectorLayer(self.OUTPUT,
                                                        QCoreApplication.translate("InsertFeaturesToLayer", 'Output layer with new features')))

    def name(self):
        return 'insertfeaturestolayer'

    def displayName(self):
        return QCoreApplication.translate("InsertFeaturesToLayer", 'Insert features to layer')

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)
        target = self.parameterAsVectorLayer(parameters, self.OUTPUT, context)

        editable_before = False
        if target.isEditable():
            editable_before = True
            feedback.reportError("\nWARNING: You need to close the edit session on layer '{}' before running this algorithm.".format(
                target.name()
            ))
            return {self.OUTPUT: None}

        # Define a mapping between source and target layer
        mapping = dict()
        for target_idx in target.fields().allAttributesList():
            target_field = target.fields().field(target_idx)
            source_idx = source.fields().indexOf(target_field.name())
            if source_idx != -1:
                mapping[target_idx] = source_idx

        # Copy and Paste
        total = 100.0 / source.featureCount() if source.featureCount() else 0
        features = source.getFeatures()
        destType = target.geometryType()
        destIsMulti = QgsWkbTypes.isMultiType(target.wkbType())

        drop_coordinates = list()
        add_coordinates = list()
        #  Check if layer have Z or M values.
        if target.wkbType() == source.wkbType():
            pass
        if QgsWkbTypes().hasM(source.wkbType()):
            drop_coordinates.append("M")
        if not QgsWkbTypes().hasZ(source.wkbType()) and QgsWkbTypes().hasZ(target.wkbType()):
            add_coordinates.append("Z")
        if QgsWkbTypes().hasZ(source.wkbType()) and not QgsWkbTypes().hasZ(target.wkbType()):
            drop_coordinates.append("Z")

        new_features = []
        for current, in_feature in enumerate(features):
            if feedback.isCanceled():
                break

            attrs = {target_idx: in_feature[source_idx] for target_idx, source_idx in mapping.items()}

            geom = QgsGeometry()

            if in_feature.hasGeometry() and target.isSpatial():
                # Convert geometry to match destination layer
                # Adapted from QGIS qgisapp.cpp, pasteFromClipboard()
                geom = in_feature.geometry()

                if destType != QgsWkbTypes.UnknownGeometry:
                    newGeometry = geom.convertToType(destType, destIsMulti)
                    if newGeometry.isNull():
                        continue
                    newGeometry = self.transform_geom(newGeometry, drop_coordinates, add_coordinates)
                    geom = newGeometry

                # Avoid intersection if enabled in digitize settings
                geom.avoidIntersections(QgsProject.instance().avoidIntersectionsLayers())

            new_feature = QgsVectorLayerUtils().createFeature(target, geom, attrs)
            new_features.append(new_feature)

            feedback.setProgress(int(current * total))

        try:
            # This might print error messages... But, hey! That's what we want!
            with edit(target):
                target.beginEditCommand("Inserting features...")
                res = target.addFeatures(new_features)
                target.endEditCommand()
        except QgsEditError as e:
            if not editable_before:
                # Let's close the edit session to prepare for a next run
                target.rollBack()

            feedback.reportError("\nERROR: No features could be copied into '{}', because of the following error:\n{}\n".format(
                target.name(),
                repr(e)
            ))
            return {self.OUTPUT: None}

        if res:
            feedback.pushInfo("\nSUCCESS: {} out of {} features from input layer were successfully copied into '{}'!".format(
                len(new_features),
                source.featureCount(),
                target.name()
            ))
        else:
            feedback.reportError("\nERROR: The {} features from input layer could not be copied into '{}'. This is likely due to constraints that are not met (such as NOT NULL, LENGTH or MAX-MIN values). Check that your input data meets your target layer constraints.".format(
                source.featureCount(),
                target.name()
            ))

        return {self.OUTPUT: target}

    def transform_geom(self, geom, drop_coordinates, add_coordinates):
        """ This function put or remove Z and remove M value"""
        if "Z" in drop_coordinates:
            geom.get().dropZValue()
        if "M" in drop_coordinates:
            geom.get().dropMValue()
        if "Z" in add_coordinates:
            geom.get().addZValue()
        return geom
