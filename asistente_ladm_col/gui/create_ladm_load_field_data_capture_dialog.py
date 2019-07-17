# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-07-03
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

from qgis.PyQt.QtCore import QVariant

from asistente_ladm_col.utils.qt_utils import (make_file_selector,
                                               make_folder_selector)

from ..utils.qfield_utils import (run_etl_model_input_load_data_to_ladm,
                                  join_layers,
                                  fix_polygon_layers)

from qgis.core import (QgsProject,
                       QgsField,
                       QgsVectorLayer,
                       QgsVectorLayerJoinInfo)

from ..config.table_mapping_config import (FDC_LADM_CONTROL_POINT,
                                           FDC_LADM_BOUNDARY_POINT,
                                           FDC_LADM_SURVEY_POINT,
                                           FDC_LADM_RIGHT_OF_WAY,
                                           FDC_LADM_PLOT,
                                           FDC_LADM_BUILDING,
                                           FDC_LADM_SPATIAL_SOURCE,
                                           FDC_LADM_EXTFILE,
                                           FDC_LADM_COL_PARTY, 
                                           FDC_LADM_ADMINISTRATIVE_SOURCE, 
                                           FDC_LADM_EXTFILE_AD
)

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

WIZARD_UI = get_ui_class('wiz_ladm_load_field_data_capture.ui')


class LadmLoadFieldDataCaptureDialog(QDialog, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()
        self.buttonBox.accepted.connect(self.accepted)

        self.btn_browse_file_geo.clicked.connect(
            make_file_selector(self.txt_file_path_geo, QCoreApplication.translate("DialogImportFromExcel",
                        "Select the Excel file with data in the intermediate structure"), 
                        QCoreApplication.translate("DialogImportFromExcel", 'GeoPackage Database (*.gpkg *)')))

        self.btn_browse_file_alfa.clicked.connect(
            make_file_selector(self.txt_file_path_alfa, QCoreApplication.translate("DialogImportFromExcel",
                    "Select the Excel file with data in the intermediate structure"), 
                    QCoreApplication.translate("DialogImportFromExcel", 'GeoPackage Database (*.gpkg *)')))

    def show_help(self):
        self.qgis_utils.show_help("create_points")

    def accepted(self):
        self.load_gpkg_alfa()
        self.mapping_fields_alfa()
        self.load_gpkg_geo()
        self.mapping_fields_geo()
        
    def load_gpkg_alfa(self):
        gpkg_path = self.txt_file_path_alfa.text()
        layer = QgsVectorLayer(gpkg_path, 'layer name', 'ogr')
        info = layer.dataProvider().subLayers()

        root = QgsProject.instance().layerTreeRoot()
        gdb_group = root.addGroup("GPKG_ALFA")
        self.gdb_layer = []

        for data in info:
            vlayer = QgsVectorLayer(gpkg_path + '|layername=' + data.split('!!::!!')[1], data.split('!!::!!')[1], 'ogr')
            self.gdb_layer.append(vlayer)
            QgsProject.instance().addMapLayer(vlayer, False)
            gdb_group.addLayer(vlayer)

        self.res_layers_alfa = self.qgis_utils.get_layers(self._db, {
            FDC_LADM_COL_PARTY: {'name': FDC_LADM_COL_PARTY, 'geometry': None},
            FDC_LADM_ADMINISTRATIVE_SOURCE: {'name': FDC_LADM_ADMINISTRATIVE_SOURCE, 'geometry': None},
            FDC_LADM_EXTFILE: {'name': FDC_LADM_EXTFILE, 'geometry': None}
        }, load=True)

    def load_gpkg_geo(self):
        gpkg_path = self.txt_file_path_geo.text()
        layer = QgsVectorLayer(gpkg_path, 'layer name', 'ogr')
        info = layer.dataProvider().subLayers()

        root = QgsProject.instance().layerTreeRoot()
        gdb_group = root.addGroup("GPKG_GEO")
        self.gdb_layer = []

        for data in info:
            vlayer = QgsVectorLayer(gpkg_path + '|layername=' + data.split('!!::!!')[1], data.split('!!::!!')[1], 'ogr')
            self.gdb_layer.append(vlayer)
            QgsProject.instance().addMapLayer(vlayer, False)
            gdb_group.addLayer(vlayer)

        self.res_layers_geo = self.qgis_utils.get_layers(self._db, {
            FDC_LADM_CONTROL_POINT: {'name': FDC_LADM_CONTROL_POINT, 'geometry': QgsWkbTypes.PointGeometry},
            FDC_LADM_BOUNDARY_POINT: {'name': FDC_LADM_BOUNDARY_POINT, 'geometry': QgsWkbTypes.PointGeometry},
            FDC_LADM_SURVEY_POINT: {'name': FDC_LADM_SURVEY_POINT, 'geometry': QgsWkbTypes.PointGeometry},
            FDC_LADM_RIGHT_OF_WAY: {'name': FDC_LADM_RIGHT_OF_WAY, 'geometry': QgsWkbTypes.PolygonGeometry},
            FDC_LADM_PLOT: {'name': FDC_LADM_PLOT, 'geometry': QgsWkbTypes.PolygonGeometry},
            FDC_LADM_BUILDING: {'name': FDC_LADM_BUILDING, 'geometry': QgsWkbTypes.PolygonGeometry},
            FDC_LADM_SPATIAL_SOURCE: {'name': FDC_LADM_SPATIAL_SOURCE, 'geometry': None},
            FDC_LADM_EXTFILE: {'name': FDC_LADM_EXTFILE, 'geometry': None}
        }, load=True)

    def mapping_fields_geo(self):

        Punto = QgsProject.instance().mapLayersByName('punto')[0]
        Poligono = QgsProject.instance().mapLayersByName('poligono')[0]
        fuente_espacial = QgsProject.instance().mapLayersByName('fuente_espacial')[0]

        Punto.setSubsetString("tipo_punto = 'Punto_Control'")
        run_etl_model_input_load_data_to_ladm(Punto, self.res_layers_geo[FDC_LADM_CONTROL_POINT], FDC_LADM_CONTROL_POINT, self.qgis_utils)
        Punto.setSubsetString("tipo_punto = 'Punto_Levantamiento.Construccion' OR tipo_punto = 'Punto_Levantamiento.Servidumbre'")
        run_etl_model_input_load_data_to_ladm(Punto, self.res_layers_geo[FDC_LADM_SURVEY_POINT], FDC_LADM_SURVEY_POINT, self.qgis_utils)
        Punto.setSubsetString("tipo_punto = 'Punto_Lindero'")
        run_etl_model_input_load_data_to_ladm(Punto, self.res_layers_geo[FDC_LADM_BOUNDARY_POINT], FDC_LADM_BOUNDARY_POINT, self.qgis_utils)

        Poligono.setSubsetString("tipo_poligono = 'Servidumbre'")
        run_etl_model_input_load_data_to_ladm(Poligono, self.res_layers_geo[FDC_LADM_RIGHT_OF_WAY], FDC_LADM_RIGHT_OF_WAY, self.qgis_utils)
        Poligono.setSubsetString("tipo_poligono = 'Terreno'")
        run_etl_model_input_load_data_to_ladm(Poligono, self.res_layers_geo[FDC_LADM_PLOT], FDC_LADM_PLOT, self.qgis_utils)
        Poligono.setSubsetString("tipo_poligono = 'Construccion'")
        run_etl_model_input_load_data_to_ladm(Poligono, self.res_layers_geo[FDC_LADM_BUILDING], FDC_LADM_BUILDING, self.qgis_utils)

        run_etl_model_input_load_data_to_ladm(fuente_espacial, self.res_layers_geo[FDC_LADM_SPATIAL_SOURCE], FDC_LADM_SPATIAL_SOURCE, self.qgis_utils)
        join_layers(fuente_espacial, self.res_layers_geo[FDC_LADM_SPATIAL_SOURCE], 'T_id', 's_local_id')
        vlayer = QgsVectorLayer("?query=SELECT * FROM {}&nogeometry".format(fuente_espacial.name()), "vlayer", "virtual" )
        run_etl_model_input_load_data_to_ladm(vlayer, self.res_layers_geo[FDC_LADM_EXTFILE], FDC_LADM_EXTFILE, self.qgis_utils)
    
    def mapping_fields_alfa(self):

        titular = QgsProject.instance().mapLayersByName('titular')[0]
        fuente_administrativa = QgsProject.instance().mapLayersByName('fuente_administrativa')[0]

        run_etl_model_input_load_data_to_ladm(titular, self.res_layers_alfa[FDC_LADM_COL_PARTY], FDC_LADM_COL_PARTY, self.qgis_utils)
        run_etl_model_input_load_data_to_ladm(fuente_administrativa, self.res_layers_alfa[FDC_LADM_ADMINISTRATIVE_SOURCE], FDC_LADM_ADMINISTRATIVE_SOURCE, self.qgis_utils)

        join_layers(fuente_administrativa, self.res_layers_alfa[FDC_LADM_ADMINISTRATIVE_SOURCE], 'T_id', 's_local_id')
        vlayer = QgsVectorLayer("?query=SELECT * FROM {}&nogeometry".format(fuente_administrativa.name()), "vlayer", "virtual" )
        run_etl_model_input_load_data_to_ladm(vlayer, self.res_layers_alfa[FDC_LADM_EXTFILE], FDC_LADM_EXTFILE_AD, self.qgis_utils)


    