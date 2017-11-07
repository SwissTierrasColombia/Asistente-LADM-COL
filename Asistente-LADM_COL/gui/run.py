import os

from qgis.core import QgsVectorLayer
from qgis.PyQt.QtCore import QObject

class Run(QObject):

    def __init__(self, iface):
        QObject.__init__(self)
        self.iface = iface

    def doRun(self):
        # TODO Read CSV
        # TODO Validate it
        # TODO Create QGIS layer from CSV
        txtFile = "/docs/tr/ai/insumos/puntos.csv"
        uri = "file:///{}?delimiter={}&xField={}&yField={}&crs=EPSG:3116".format(
                      txtFile,
                      ";",
                      "x",
                      "y"
                   )
        csvLayer = QgsVectorLayer( uri, os.path.basename( txtFile ), "delimitedtext" )
        if not csvLayer.isValid():
            print("Layer not valid!")
            return

        QgsProject.instance().addMapLayer(csvLayer)
        # TODO Set PG connection
        # TODO Import CSVLayer into PG Model based on ili
        ##csvLayer.copy()
        ##pgLayer.startSession()
        ##pgLayer.paste()
        ##pgLayer.endSession()
