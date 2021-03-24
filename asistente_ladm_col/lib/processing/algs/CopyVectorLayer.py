# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2021-01-27
        copyright            : (C) 2021 by Germán Carrillo (SwissTierras Colombia)
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
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterFeatureSink,
                       QgsFeatureSink)


class CopyVectorLayer(QgsProcessingAlgorithm):
    """
    Based on https://github.com/qgisco/curso-introduccion-pyqgis/blob/master/3ra_Sesi%C3%B3n_Expresiones_personalizadas_y_Algoritmos_Geoprocesamiento/05c_copy_vector_layer.py
    """

    INPUT = 'INPUT'
    SINK = 'SINK'
    OUTPUT = 'OUTPUT'

    def __init__(self):
        super().__init__()

    def createInstance(self):
        return CopyVectorLayer()

    def name(self):
        return 'copy_vector_layer'

    def displayName(self):
        return QCoreApplication.translate("CopyVectorLayer", "Copy vector layer")

    def group(self):
        return QCoreApplication.translate("CopyVectorLayer", "Vector table")

    def groupId(self):
        return 'vectortable'

    def tags(self):
        return (QCoreApplication.translate("CopyVectorLayer", 'copy,duplicate,vector,layer')).split(',')

    def shortHelpString(self):
        return QCoreApplication.translate("CopyVectorLayer", "Creates a full copy of a vector layer")

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                QCoreApplication.translate("CopyVectorLayer", "Input layer"),
                [QgsProcessing.TypeVector]
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.SINK,
                QCoreApplication.translate("CopyVectorLayer", "Copy of the vector layer")
            )
        )
        self.addOutput(
            QgsProcessingOutputVectorLayer(
                self.OUTPUT,
                QCoreApplication.translate("CopyVectorLayer", "Output layer")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsVectorLayer(
            parameters,
            self.INPUT,
            context
        )
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.SINK,
            context,
            source.fields(),
            source.wkbType(),
            source.sourceCrs())

        features = [f for f in source.getFeatures()]
        sink.addFeatures(features, QgsFeatureSink.FastInsert)

        return {self.OUTPUT: dest_id}