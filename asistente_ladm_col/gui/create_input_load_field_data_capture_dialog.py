# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-04-11
        git sha              : :%H$
        copyright            : (C) 2019 by Jhon Galindo
        email                : jhonsigpjc@gmail.com
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
import stat
import processing

from asistente_ladm_col.utils.qt_utils import (make_file_selector,
                                               make_folder_selector)

from ..utils.qfield_utils import run_etl_model_input_load_data

from qgis.core import (QgsProject,
                       QgsVectorLayer)

from ..config.table_mapping_config import (FDC_PARCEL,
                                           FDC_PARTY,
                                           FDC_RIGHT,
                                           FDC_ADMINISTRATIVE_SOURCE,
                                           FDC_RRRSOURCE,
                                           FDC_UEBAUNIT,
                                           FDC_PLOT, 
                                           FDC_SECTOR)

from qgis.PyQt.QtCore import (Qt,
                              QSettings,
                              QCoreApplication,
                              QFile)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QFileDialog,
                                 QSizePolicy,
                                 QGridLayout)
from qgis.core import (Qgis,
                       QgsMapLayerProxyModel,
                       QgsApplication,
                       QgsCoordinateReferenceSystem,
                       QgsWkbTypes)
from qgis.gui import QgsMessageBar

from ..config.help_strings import HelpStrings

from ..utils import get_ui_class

WIZARD_UI = get_ui_class('wiz_input_load_field_data_capture.ui')


class InputLoadFieldDataCaptureDialog(QDialog, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()
        self.buttonBox.accepted.connect(self.accepted)

        self.btn_browse_file_r1.clicked.connect(
            make_file_selector(self.txt_file_path_r1, QCoreApplication.translate("DialogImportFromExcel",
                        "Select the Excel file with data in the intermediate structure"), 
                        QCoreApplication.translate("DialogImportFromExcel", 'Excel File (*.xlsx *.xls)')))

        self.btn_browse_file_gdb.clicked.connect(
                make_folder_selector(self.txt_file_path_gdb, title=QCoreApplication.translate(
                'SettingsDialog', 'Open Folder with GDB'), parent=None))

    def show_help(self):
        self.qgis_utils.show_help("create_points")

    def accepted(self):
        #self.load_r1()
        #self.mapping_fields_r1()
        self.load_gdb()
        self.mapping_fields_gbb()
        
    def load_r1(self):
        self.layer_r1 = QgsVectorLayer(self.txt_file_path_r1.text(), 'R1_IGAC', 'ogr')
        QgsProject.instance().addMapLayer(self.layer_r1)

        self.res_layers = self.qgis_utils.get_layers(self._db, {
            FDC_PARCEL: {'name': FDC_PARCEL, 'geometry': None},
            FDC_PARTY: {'name': FDC_PARTY, 'geometry': None},
            FDC_RIGHT: {'name': FDC_RIGHT, 'geometry': None},
            FDC_ADMINISTRATIVE_SOURCE: {'name': FDC_ADMINISTRATIVE_SOURCE, 'geometry': None},
            FDC_RRRSOURCE: {'name': FDC_RRRSOURCE, 'geometry': None},
            FDC_UEBAUNIT: {'name': FDC_UEBAUNIT, 'geometry': None}
        }, load=True)

    def load_gdb(self):
        gdb_path = self.txt_file_path_gdb.text()
        layer = QgsVectorLayer(gdb_path, 'layer name', 'ogr')
        info = layer.dataProvider().subLayers()

        root = QgsProject.instance().layerTreeRoot()
        gdb_group = root.addGroup("GDB")
        self.gdb_layer = []

        for data in info:
            vlayer = QgsVectorLayer(gdb_path + '|layername=' + data.split('!!::!!')[1], data.split('!!::!!')[1], 'ogr')
            self.gdb_layer.append(vlayer)
            QgsProject.instance().addMapLayer(vlayer, False)
            gdb_group.addLayer(vlayer)

        self.res_layers_gdb = self.qgis_utils.get_layers(self._db, {
            FDC_PLOT: {'name': FDC_PLOT, 'geometry': QgsWkbTypes.PolygonGeometry},
            FDC_SECTOR: {'name': FDC_SECTOR, 'geometry': None}
        }, load=True)

    def mapping_fields_r1(self):
        arreglo = [ FDC_PARCEL, FDC_PARTY, FDC_RIGHT, FDC_ADMINISTRATIVE_SOURCE, FDC_RRRSOURCE]
        for name in arreglo:
            if name == FDC_ADMINISTRATIVE_SOURCE:
                input_data = self.res_layers[FDC_RIGHT]
            else:
                if name == FDC_RRRSOURCE:
                    input_data = self.res_layers[FDC_ADMINISTRATIVE_SOURCE]
                    print (input_data.name())
                else:
                    input_data = self.layer_r1

            output_data = self.res_layers[name]
            run_etl_model_input_load_data(input_data, output_data, name, self.qgis_utils)
            print ("Ejecutando etl" + self.res_layers[name].name())

    def mapping_fields_gbb(self):

        terreno = QgsProject.instance().mapLayersByName('U_TERRENO')[0].id()
        sector = QgsProject.instance().mapLayersByName('U_SECTOR')[0].id()

        arreglo = [ FDC_PLOT, FDC_SECTOR]
        for name in arreglo:
            if name == FDC_PLOT:
                input_data = self.fix_polygon_layers(terreno)
                output_data = self.res_layers_gdb[FDC_PLOT]
            elif name == FDC_SECTOR:
                input_data = self.fix_polygon_layers(sector)
                output_data = self.res_layers_gdb[FDC_SECTOR]

            run_etl_model_input_load_data(input_data, output_data, name, self.qgis_utils)
            print ("Ejecutando etl" + self.res_layers_gdb[name].name())

    def fix_polygon_layers(self, layer):

        params = {'INPUT': layer, 'OUTPUT':'memory:'}
        multipart = processing.run("native:multiparttosingleparts", params)
        params = {'INPUT': multipart['OUTPUT'], 'OUTPUT':'memory:'}
        fix = processing.run("native:fixgeometries", params)

        return fix['OUTPUT']
