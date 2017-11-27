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

from qgis.core import QgsProject, QgsVectorLayer
from qgis.PyQt.QtWidgets import QWizard

from ..utils.qt_utils import make_file_selector
from ..utils import qgis_utils, get_ui_class
from ..config.table_mapping_config import BOUNDARY_POINT_TABLE

WIZARD_UI = get_ui_class('wiz_add_points_cadaster.ui')

class PointsSpatialUnitCadasterWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, db, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self._db = db

        # Set connections
        self.btn_browse_file.clicked.connect(
            make_file_selector(self.txt_file_path,
                               file_filter=self.tr('CSV Comma Separated Value (*.csv)')))
        self.txt_file_path.textChanged.connect(self.fill_long_lat_combos)
        self.button(QWizard.FinishButton).clicked.connect(self.copy_csv_points_to_db)

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
        csv_layer.selectAll()

        res, uri = self._db.get_uri_for_layer(BOUNDARY_POINT_TABLE)
        if not res:
            print(uri)
            return

        target_point_layer = qgis_utils.get_layer(BOUNDARY_POINT_TABLE)
        if target_point_layer is None:
            target_point_layer = QgsVectorLayer(uri, BOUNDARY_POINT_TABLE.capitalize(), self._db.provider)
            QgsProject.instance().addMapLayer(target_point_layer)

        self.iface.copySelectionToClipboard(csv_layer)
        target_point_layer.startEditing()
        self.iface.pasteFromClipboard(target_point_layer)
        target_point_layer.commitChanges()
        QgsProject.instance().addMapLayer(target_point_layer)
        self.iface.zoomFull()

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
