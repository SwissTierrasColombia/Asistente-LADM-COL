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
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsWkbTypes,
                       QgsProject,
                       QgsVectorLayer)
import processing

from asistente_ladm_col.config.general_config import BLO_LIS_FILE_PATH
from asistente_ladm_col.core.supplies.etl_supplies import ETLSupplies


class ETLCobol(ETLSupplies):
    CLASS_NAME = "ETLCobol"

    def __init__(self, names, data_source_widget):
        ETLSupplies.__init__(self, names, data_source_widget)

    def initialize_layers(self):
        self.layers = {
            self.names.GC_PARCEL_T: None,
            self.names.GC_OWNER_T: None,
            self.names.GC_ADDRESS_T: None,
            self.names.GC_BUILDING_UNIT_T: None,
            self.names.GC_BUILDING_T: None,
            self.names.GC_PLOT_T: None,
            self.names.GC_PARCEL_STATUS_T: None,
            self.names.GC_RURAL_DIVISION_T: None,
            self.names.GC_URBAN_SECTOR_T: None,
            self.names.GC_RURAL_SECTOR_T: None,
            self.names.GC_PERIMETER_T: None,
            self.names.GC_BLOCK_T: None,
            self.names.GC_NEIGHBOURHOOD_T: None,
            self.names.GC_COMMISSION_BUILDING_T: None,
            self.names.GC_COMMISSION_PLOT_T: None,
            self.names.GC_COMMISSION_BUILDING_UNIT_T: None
        }

    def load_alphanumeric_layers(self):
        self.alphanumeric_file_paths = {
            'blo': self.data_source_widget.txt_file_path_blo.text().strip(),
            'uni': self.data_source_widget.txt_file_path_uni.text().strip(),
            'ter': self.data_source_widget.txt_file_path_ter.text().strip(),
            'pro': self.data_source_widget.txt_file_path_pro.text().strip()
        }

        root = QgsProject.instance().layerTreeRoot()
        lis_group = root.addGroup(QCoreApplication.translate(self.CLASS_NAME, "LIS Supplies"))

        for name in self.alphanumeric_file_paths:
            uri = 'file:///{}?type=csv&delimiter=;&detectTypes=yes&geomType=none&subsetIndex=no&watchFile=no'.format(self.alphanumeric_file_paths[name])
            layer = QgsVectorLayer(uri, name, 'delimitedtext')
            if layer.isValid():
                self.alphanumeric_file_paths[name] = layer
                QgsProject.instance().addMapLayer(layer, False)
                lis_group.addLayer(layer)
            else:
                if name == 'blo':
                    # BLO is kind of optional, if it is not given, we pass a default one
                    uri = 'file:///{}?type=csv&delimiter=;&detectTypes=yes&geomType=none&subsetIndex=no&watchFile=no'.format(BLO_LIS_FILE_PATH)
                    layer = QgsVectorLayer(uri, name, 'delimitedtext')
                    self.alphanumeric_file_paths[name] = layer
                    QgsProject.instance().addMapLayer(layer, False)
                    lis_group.addLayer(layer)
                else:
                    return False, QCoreApplication.translate(self.CLASS_NAME, "There were troubles loading the LIS file called '{}'.".format(name))

        return True, ''

    def run_etl_model(self, custom_feedback):
        self.logger.info(__name__, "Running ETL-Cobol model...")
        processing.run("model:ETL-model-supplies",
                       {'barrio': self.gdb_layer_paths['U_BARRIO'],
                        'gcbarrio': self.layers[self.names.GC_NEIGHBOURHOOD_T],
                        'gccomisionconstruccion': self.layers[self.names.GC_COMMISSION_BUILDING_T],
                        'gccomisionterreno': self.layers[self.names.GC_COMMISSION_PLOT_T],
                        'gcconstruccion': self.layers[self.names.GC_BUILDING_T],
                        'gcdireccion': self.layers[self.names.GC_ADDRESS_T],
                        'gcestadopredio': self.layers[self.names.GC_PARCEL_STATUS_T],
                        'gcmanzana': self.layers[self.names.GC_BLOCK_T],
                        'gcperimetro': self.layers[self.names.GC_PERIMETER_T],
                        'gcpropietario': self.layers[self.names.GC_OWNER_T],
                        'gcsector': self.layers[self.names.GC_RURAL_SECTOR_T],
                        'gcsectorurbano': self.layers[self.names.GC_URBAN_SECTOR_T],
                        'gcterreno': self.layers[self.names.GC_PLOT_T],
                        'gcunidad': self.layers[self.names.GC_BUILDING_UNIT_T],
                        'gcunidadconstruccioncomision': self.layers[self.names.GC_COMMISSION_BUILDING_UNIT_T],
                        'gcvereda': self.layers[self.names.GC_RURAL_DIVISION_T],
                        'inputblo': self.alphanumeric_file_paths['blo'],
                        'inputconstruccion': self.gdb_layer_paths['R_CONSTRUCCION'],
                        'inputmanzana': self.gdb_layer_paths['U_MANZANA'],
                        'inputperimetro': self.gdb_layer_paths['U_PERIMETRO'],
                        'inputpro': self.alphanumeric_file_paths['pro'],
                        'inputrunidad': self.gdb_layer_paths['R_UNIDAD'],
                        'inputsector': self.gdb_layer_paths['R_SECTOR'],
                        'inputter': self.alphanumeric_file_paths['ter'],
                        'inputterreno': self.gdb_layer_paths['R_TERRENO'],
                        'inputuconstruccion': self.gdb_layer_paths['U_CONSTRUCCION'],
                        'inputuni': self.alphanumeric_file_paths['uni'],
                        'inputusector': self.gdb_layer_paths['U_SECTOR'],
                        'inpututerreno': self.gdb_layer_paths['U_TERRENO'],
                        'inputuunidad': self.gdb_layer_paths['U_UNIDAD'],
                        'inputvereda': self.gdb_layer_paths['R_VEREDA'],
                        'ouputlayer': self.layers[self.names.GC_PARCEL_T],
                        'rnomenclatura': self.gdb_layer_paths['R_NOMENCLATURA_DOMICILIARIA'],
                        'unomenclatura': self.gdb_layer_paths['U_NOMENCLATURA_DOMICILIARIA']},
                       feedback=custom_feedback)
        self.logger.info(__name__, "ETL-Cobol model finished.")