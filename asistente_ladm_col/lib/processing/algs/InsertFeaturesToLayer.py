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
from qgis.PyQt.QtCore import (QCoreApplication,
                              QSettings)

from qgis.core import (edit,
                       QgsEditError,
                       QgsGeometry,
                       QgsWkbTypes,
                       QgsProcessing,
                       QgsProcessingFeedback,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingOutputVectorLayer,
                       QgsProject,
                       QgsVectorLayerUtils,
                       QgsVectorLayer,
                       QgsFeatureSink,
                       QgsExpressionContext,
                       QgsExpressionContextUtils)

from asistente_ladm_col.config.general_config import DEFAULT_AUTOMATIC_VALUES_IN_BATCH_MODE


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
        target_provider = target.dataProvider()
        target_provider.clearErrors()

        if target.isEditable():
            feedback.reportError("\nWARNING: You need to close the edit session on layer '{}' before running this algorithm.".format(
                target.name()
            ))
            return {self.OUTPUT: None}

        features = QgsVectorLayerUtils().makeFeaturesCompatible(source.getFeatures(), target)
        eval_context = QgsExpressionContext(QgsExpressionContextUtils.globalProjectLayerScopes(target))

        # Make sure automatic values are calculated if automatic_values_in_batch_mode
        # is enabled and that they are not calculated otherwise
        automatic_values_in_batch_mode = QSettings().value('Asistente-LADM-COL/automatic_values/automatic_values_in_batch_mode', DEFAULT_AUTOMATIC_VALUES_IN_BATCH_MODE, bool)
        list_automatic_fields = list()
        if automatic_values_in_batch_mode:
            # Get indexes that have an automatic value configured, except primary keys,
            # since we deal with PK's values  differently (namely, directly with the provider)
            list_automatic_fields = [idx for idx in target.attributeList() if target.defaultValueDefinition(idx).isValid() and idx not in target_provider.pkAttributeIndexes()]

        # Update attribute values before saving
        for feature in features:
            for idx in target_provider.pkAttributeIndexes():
                # Get the PK from the provider itself
                feature.setAttribute(idx, target_provider.defaultValue(idx))

            for idx in list_automatic_fields:
                feature.setAttribute(idx, target.defaultValue(idx, feature, eval_context))

        if self.save_features(target, features, 'provider', feedback):
            feedback.pushInfo("\nSUCCESS: {} out of {} features from input layer were successfully copied into '{}'!".format(
                    len(features),
                    source.featureCount(),
                    target.name()
            ))
        else:  # Messages are handled by save_features method
            return {self.OUTPUT: None}
            
        return {self.OUTPUT: target}

    def save_features(self, layer, features, mode='provider', feedback=QgsProcessingFeedback()):
        res = False
        if mode == 'provider':
            feedback.pushInfo("Saving features using data provider...")
            layer.dataProvider().clearErrors()
            res = layer.dataProvider().addFeatures(features, QgsFeatureSink.FastInsert)[0]
            if not res:
                if layer.dataProvider().hasErrors():
                    feedback.reportError(
                        "\nERROR: The data could not be copied! Details: {}.".format(layer.dataProvider().errors()))
                else:
                    feedback.reportError("\nERROR: The data could not be copied! No more details from the provider.")
        elif mode == 'edit_session':
            feedback.pushInfo("Saving features using edit session...")
            try:
                with edit(layer):
                    res = layer.addFeatures(features, QgsFeatureSink.FastInsert)
            except QgsEditError as e:
                # Let's close the edit session to prepare for a next run
                layer.rollBack()
                feedback.reportError(
                    "\nERROR: No features could be copied into '{}', because of the following error:\n{}\n".format(
                        layer.name(),
                        repr(e)
                    ))
                res = False

        return res