from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsGeometry,
                       QgsLineString,
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


class ConvertEmptyToNull(QgisFeatureBasedAlgorithm):

    def tags(self):
        return (QCoreApplication.translate("ConvertEmptyToNull", "empty,null,convert,geometry")).split(',')

    def group(self):
        return QCoreApplication.translate("ConvertEmptyToNull", "Vector geometry")

    def groupId(self):
        return 'vectorgeometry'

    def __init__(self):
        super().__init__()

    def name(self):
        return 'ConvertEmptyToNull'

    def displayName(self):
        return QCoreApplication.translate("ConvertEmptyToNull", "Convert Empty geometries to Null")

    def outputName(self):
        return QCoreApplication.translate("ConvertEmptyToNull", "Clean layer")

    def processFeature(self, feature, context, feedback):
        if feature.hasGeometry() and feature.geometry().isEmpty():
            feature.setGeometry(QgsGeometry())
        return [feature]

    def supportInPlaceEdit(self, layer):
        return False