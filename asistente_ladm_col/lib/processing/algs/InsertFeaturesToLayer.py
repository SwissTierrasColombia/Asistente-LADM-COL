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

from qgis.PyQt.QtCore import QCoreApplication

from qgis.core import (edit,
                       QgsEditError,
                       QgsGeometry,
                       QgsWkbTypes,
                       QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingOutputVectorLayer,
                       QgsProject,
                       QgsVectorLayerUtils)

class InsertFeaturesToLayer(QgsProcessingAlgorithm):

    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'

    def createInstance(self):
        return type(self)()

    def group(self):
        return QCoreApplication.translate("InsertFeaturesToLayer", "Vector table")

    def groupId(self):
        return 'vectortable'

    def tags(self):
        return (QCoreApplication.translate("InsertFeaturesToLayer", 'append,copy,insert,features,paste')).split(',')

    def __init__(self):
        super().__init__()

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(self.INPUT,
                                                              QCoreApplication.translate("InsertFeaturesToLayer", "Input layer"),
                                                              [QgsProcessing.TypeVector]))
        self.addParameter(QgsProcessingParameterVectorLayer(self.OUTPUT,
                                                              QCoreApplication.translate("InsertFeaturesToLayer", "Output layer"),
                                                              [QgsProcessing.TypeVector]))
        self.addOutput(QgsProcessingOutputVectorLayer(self.OUTPUT,
                                                        QCoreApplication.translate("InsertFeaturesToLayer", "Output layer with new features")))

    def name(self):
        return 'insertfeaturestolayer'

    def displayName(self):
        return QCoreApplication.translate("InsertFeaturesToLayer", "Insert features to layer")

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)
        target = self.parameterAsVectorLayer(parameters, self.OUTPUT, context)
        target.dataProvider().clearErrors()

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

        #  Check if layer has Z or M values.
        drop_coordinates = list()
        add_coordinates = list()
        if QgsWkbTypes().hasM(source.wkbType()):
            # In ladm we don't use M values, so drop them if present
            drop_coordinates.append("M")
        if not QgsWkbTypes().hasZ(source.wkbType()) and QgsWkbTypes().hasZ(target.wkbType()):
            add_coordinates.append("Z")
        if QgsWkbTypes().hasZ(source.wkbType()) and not QgsWkbTypes().hasZ(target.wkbType()):
            drop_coordinates.append("Z")

        new_features = []
        display_target_geometry = QgsWkbTypes.displayString(target.wkbType())
        display_source_geometry = QgsWkbTypes.displayString(source.wkbType())

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
                        feedback.reportError("\nERROR: Geometry type from the source layer ('{}') could not be converted to '{}'.".format(
                            display_source_geometry,
                            display_target_geometry
                        ))
                        return {self.OUTPUT: None}
                    newGeometry = self.transform_geom(newGeometry, drop_coordinates, add_coordinates)
                    geom = newGeometry

                # Avoid intersection if enabled in digitize settings
                geom.avoidIntersections(QgsProject.instance().avoidIntersectionsLayers())

            new_feature = QgsVectorLayerUtils().createFeature(target, geom, attrs)
            new_features.append(new_feature)

            feedback.setProgress(int(current * total))

        try:
            # This might print error messages... But, hey! That's what we want!
            res = target.dataProvider().addFeatures(new_features)
        except QgsEditError as e:
            if not editable_before:
                # Let's close the edit session to prepare for a next run
                target.rollBack()

            feedback.reportError("\nERROR: No features could be copied into '{}', because of the following error:\n{}\n".format(
                target.name(),
                repr(e)
            ))
            return {self.OUTPUT: None}

        if res[0]:
            feedback.pushInfo("\nSUCCESS: {} out of {} features from input layer were successfully copied into '{}'!".format(
                    len(new_features),
                    source.featureCount(),
                    target.name()
            ))         
        else:
            if target.dataProvider().hasErrors():
                feedback.reportError("\nERROR: The data could not be copied! Details: {}.".format(target.dataProvider().errors()[0]))
            else:
                feedback.reportError("\nERROR: The data could not be copied! No more details from the provider.")
            
        return {self.OUTPUT: target}

    def transform_geom(self, geom, drop_coordinates, add_coordinates):
        """Add/remove Z and remove M values"""
        if "Z" in drop_coordinates:
            geom.get().dropZValue()
        if "M" in drop_coordinates:
            geom.get().dropMValue()
        if "Z" in add_coordinates:
            geom.get().addZValue()
        return geom
