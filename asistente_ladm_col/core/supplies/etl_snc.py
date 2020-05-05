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

from asistente_ladm_col.config.general_config import PREDIO_SANCION_FILE_PATH
from asistente_ladm_col.core.supplies.etl_supplies import ETLSupplies


class ETLSNC(ETLSupplies):
    CLASS_NAME = "ETLSNC"

    def __init__(self, names, data_source_widget):
        ETLSupplies.__init__(self, names, data_source_widget)

    def initialize_layers(self):
        self.layers = {
            self.names.GC_PARCEL_T: None,
            self.names.GC_OWNER_T: None,
            self.names.GC_HP_CONDOMINIUM_DATA_T: None,
            self.names.GC_COPROPERTY_T: None,
            self.names.GC_ADDRESS_T: None,
            self.names.GC_BUILDING_UNIT_T: None,
            self.names.GC_BUILDING_T: None,
            self.names.GC_PLOT_T: None,
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
            'predio_sancion': self.data_source_widget.txt_file_path_predio_sancion.text().strip(),
            'predio': self.data_source_widget.txt_file_path_predio.text().strip(),
            'direccion': self.data_source_widget.txt_file_path_direccion.text().strip(),
            'unidad_construccion': self.data_source_widget.txt_file_path_uni.text().strip(),
            'persona': self.data_source_widget.txt_file_path_persona.text().strip(),
            'ficha_matriz': self.data_source_widget.txt_file_path_ficha_m.text().strip(),
            'ficha_matriz_predio': self.data_source_widget.txt_file_path_ficha_m_predio.text().strip(),
        }

        root = QgsProject.instance().layerTreeRoot()
        alphanumeric_group = root.addGroup(QCoreApplication.translate(self.CLASS_NAME, "SNC Alphanumeric Supplies"))

        for name in self.alphanumeric_file_paths:
            layer = QgsVectorLayer(self.alphanumeric_file_paths[name], name, 'ogr')
            if layer.isValid():
                self.alphanumeric_file_paths[name] = layer
                QgsProject.instance().addMapLayer(layer, False)
                alphanumeric_group.addLayer(layer)
            else:
                if name == 'predio_sancion':
                    # predio_sancion is kind of optional, if it is not given, we pass a default one
                    layer = QgsVectorLayer(PREDIO_SANCION_FILE_PATH, name, 'ogr')
                    self.alphanumeric_file_paths[name] = layer
                    if layer.isValid():
                        QgsProject.instance().addMapLayer(layer, False)
                        alphanumeric_group.addLayer(layer)
                else:
                    return False, QCoreApplication.translate(self.CLASS_NAME, "There were troubles loading the CSV file called '{}'.".format(name))

        return True, ''

    def run_etl_model(self, custom_feedback):
        self.logger.info(__name__, "Running ETL-SNC model...")
        processing.run("model:ETL_SNC",
                       {'barrio': self.gdb_layer_paths['U_BARRIO'],
                        'fichamatriz': self.alphanumeric_file_paths['ficha_matriz'],
                        'fichamatrizpredio': self.alphanumeric_file_paths['ficha_matriz_predio'],
                        'gcbarrio': self.layers[self.names.GC_NEIGHBOURHOOD_T],
                        'gccomisionesconstruccion': self.layers[self.names.GC_COMMISSION_BUILDING_T],
                        'gccomisionesterreno': self.layers[self.names.GC_COMMISSION_PLOT_T],
                        'gccomisionesunidadconstruccion': self.layers[self.names.GC_COMMISSION_BUILDING_UNIT_T],
                        'gcconstruccion': self.layers[self.names.GC_BUILDING_T],
                        'gccopropiedad': self.layers[self.names.GC_COPROPERTY_T],
                        'gcdireccion': self.layers[self.names.GC_ADDRESS_T],
                        'gcmanzana': self.layers[self.names.GC_BLOCK_T],
                        'gcperimetro': self.layers[self.names.GC_PERIMETER_T],
                        'gcpredio': self.layers[self.names.GC_PARCEL_T],
                        'gcpropiedadhorizontal': self.layers[self.names.GC_HP_CONDOMINIUM_DATA_T],
                        'gcpropietario': self.layers[self.names.GC_OWNER_T],
                        'gcsectorrural': self.layers[self.names.GC_RURAL_SECTOR_T],
                        'gcsectorurbano': self.layers[self.names.GC_URBAN_SECTOR_T],
                        'gcterreno': self.layers[self.names.GC_PLOT_T],
                        'gcunidadconstruccion': self.layers[self.names.GC_BUILDING_UNIT_T],
                        'gcvereda': self.layers[self.names.GC_RURAL_DIVISION_T],
                        'manzana': self.gdb_layer_paths['U_MANZANA'],
                        'persona': self.alphanumeric_file_paths['persona'],
                        'predio': self.alphanumeric_file_paths['predio'],
                        'prediodireccion': self.alphanumeric_file_paths['direccion'],
                        'rconstruccion': self.gdb_layer_paths['R_CONSTRUCCION'],
                        'rnomemclatura': self.gdb_layer_paths['R_NOMENCLATURA_DOMICILIARIA'],
                        'rperimetro': self.gdb_layer_paths['U_PERIMETRO'],
                        'rsector': self.gdb_layer_paths['R_SECTOR'],
                        'rterreno': self.gdb_layer_paths['R_TERRENO'],
                        'runidad': self.gdb_layer_paths['R_UNIDAD'],
                        'uconstruccion': self.gdb_layer_paths['U_CONSTRUCCION'],
                        'unidadconstruccion': self.alphanumeric_file_paths['unidad_construccion'],
                        'unomenclatura': self.gdb_layer_paths['U_NOMENCLATURA_DOMICILIARIA'],
                        'usector': self.gdb_layer_paths['U_SECTOR'],
                        'uterreno': self.gdb_layer_paths['U_TERRENO'],
                        'uunidad': self.gdb_layer_paths['U_UNIDAD'],
                        'vereda': self.gdb_layer_paths['R_VEREDA']},
                        feedback=custom_feedback)
        self.logger.info(__name__, "ETL-SNC model finished.")