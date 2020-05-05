# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-03-19
        git sha              : :%H$
        copyright            : (C) 2020 by Germán Carrillo (BSF Swissphoto)
                               (C) 2020 by Jhon Galindo (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
                               jhonsigpjc@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication)
from qgis.core import (QgsVectorLayer,
                       QgsProject)

from asistente_ladm_col import Logger


class ETLSupplies(QObject):
    CLASS_NAME = ""

    def __init__(self, names, data_source_widget):
        QObject.__init__(self)
        self.names = names
        self.data_source_widget = data_source_widget
        self.logger = Logger()

        self.gdb_path = self.data_source_widget.txt_file_path_gdb.log_quality_validation_text()

        self.alphanumeric_file_paths = {}
        self.gdb_layer_paths = dict()
        self.layers = dict()

        self.initialize_layers()

    def initialize_layers(self):
        raise NotImplementedError

    def load_alphanumeric_layers(self):
        raise NotImplementedError

    def load_spatial_layers(self):
        required_layers = ['R_TERRENO', 'U_TERRENO', 'R_SECTOR', 'U_SECTOR', 'R_VEREDA', 'U_MANZANA', 'U_BARRIO',
                           'R_CONSTRUCCION', 'U_CONSTRUCCION', 'U_UNIDAD', 'R_UNIDAD',
                           'U_NOMENCLATURA_DOMICILIARIA', 'R_NOMENCLATURA_DOMICILIARIA', 'U_PERIMETRO']

        layer = QgsVectorLayer(self.gdb_path, 'layer name', 'ogr')

        if not layer.isValid():
            return False, QCoreApplication.translate(self.CLASS_NAME, "There were troubles loading the GDB.")

        sublayers = layer.dataProvider().subLayers()

        root = QgsProject.instance().layerTreeRoot()
        gdb_group = root.addGroup(QCoreApplication.translate(self.CLASS_NAME, "GDB Supplies"))

        for data in sublayers:
            sublayer = data.split('!!::!!')[1]
            if sublayer in required_layers:
                layer = QgsVectorLayer(self.gdb_path + '|layername=' + sublayer, sublayer, 'ogr')
                self.gdb_layer_paths[sublayer] = layer
                QgsProject.instance().addMapLayer(layer, False)
                gdb_group.addLayer(layer)

        if len(self.gdb_layer_paths) != len(required_layers):
            return False, QCoreApplication.translate(self.CLASS_NAME, "The GDB does not have the required layers!")

        return True, ''

    def run_etl_model(self, custom_feedback):
        raise NotImplementedError