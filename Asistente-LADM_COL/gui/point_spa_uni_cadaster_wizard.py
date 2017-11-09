import os

from qgis.core import QgsProject, QgsVectorLayer
from qgis.PyQt.QtWidgets import QWizard

from ..utils.qt_utils import make_file_selector
from ..utils import get_ui_class
from ..config.table_mapping_config import *

WIZARD_UI = get_ui_class('wiz_add_points_cadaster.ui')

class PointsSpatialUnitCadasterWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface

        # Set connections
        self.btn_browse_file.clicked.connect(
            make_file_selector(self.txt_file_path,
                               file_filter=self.tr('CSV Comma Separated Value (*.csv)')))
        self.txt_file_path.textChanged.connect(self.fill_long_lat_combos)
        self.button(QWizard.FinishButton).hide()
        self.button(QWizard.CommitButton).show()
        self.button(QWizard.CommitButton).clicked.connect(self.copy_csv_points_to_db)

    def copy_csv_points_to_db(self):
        csv_path = self.txt_file_path.text().strip()

        # Create QGIS vector layer
        uri = "file:///{}?delimiter={}&xField={}&yField={}&crs=EPSG:3116".format(
              csv_path,
              self.txt_delimiter.text(),
              self.cbo_longitude.currentText(),
              self.cbo_latitude.currentText()
           )
        csv_layer = QgsVectorLayer(uri, os.path.basename(csv_path), "delimitedtext")
        if not csv_layer.isValid():
            print("CSV layer not valid!")

        uri = 'dbname=\'test3\' host=localhost port=5432 user=\'postgres\' password=\'postgres\' sslmode=disable key=\'t_id\' srid=3116 type=Point checkPrimaryKeyUnicity=\'1\' table="ladm_col_02"."puntolindero" (localizacion_original) sql='
        # options = dict()
        # options['update'] = True
        # options['addlist'] = True
        # _writer = QgsVectorLayerExporter.exportLayer(csv_layer,
        #                                              uri,
        #                                              "postgres",
        #                                              QgsCoordinateReferenceSystem(3116, QgsCoordinateReferenceSystem.EpsgCrsId),
        #                                              False,
        #                                              options)

        target_point_layer = QgsVectorLayer(uri, "target", "postgres")
        QgsProject.instance().addMapLayers([csv_layer, target_point_layer])
        self.iface.setActiveLayer(csv_layer)
        self.iface.actionCopyFeatures().trigger() # Copy!
        self.iface.setActiveLayer(target_point_layer)
        target_point_layer.startEditing()
        res = self.iface.actionPasteFeatures().trigger() # Paste
        target_point_layer.commitChanges()

        # After a while figuring out how to append to a PostGIS table with current
        # QGIS master, no option has been found. I'll see if I can propose something
        # upstream that makes that easier in this plugin
        
        # RollBack if num features in target layer is different from CSV layer

        # Progress QgsMessageBar

    def fill_long_lat_combos(self, text):
        csv_path = self.txt_file_path.text().strip()
        self.cbo_longitude.clear()
        self.cbo_latitude.clear()
        if os.path.exists(csv_path):
            fields = self.get_fields_from_csv_file(csv_path)
            self.cbo_longitude.addItems(fields)
            self.cbo_latitude.addItems(fields)

    def get_fields_from_csv_file(self, csv_path):
        errorReading = False
        try:
            reader  = open(csv_path, "r")
        except IOError:
            errorReading = True
        line = reader.readline().replace("\n", "")
        reader.close()
        if not line:
            errorReading = True
        else:
            return line.split(self.txt_delimiter.text().strip())

        return []
