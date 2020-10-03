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
import os
import shutil

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessingException,
                       QgsProject,
                       QgsVectorLayer,
                       Qgis)
import processing

from asistente_ladm_col.config.general_config import (PREDIO_BLOQUEO_FILE_PATH,
                                                      FICHA_MATRIZ_FILE_PATH,
                                                      FICHA_MATRIZ_PREDIO_FILE_PATH,
                                                      FICHA_MATRIZ_TORRE_FILE_PATH,
                                                      BUILDING_UNIT_CSVT_FILE_PATH)
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
            self.names.GC_HP_TOWER_DATA_T: None,
            self.names.GC_QUALIFICATION_BUILDING_UNIT_T: None,
            self.names.GC_PARCEL_STATUS_T: None,
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
            'predio_bloqueo': self.data_source_widget.txt_file_path_predio_bloqueo.text().strip(),
            'predio': self.data_source_widget.txt_file_path_predio.text().strip(),
            'direccion': self.data_source_widget.txt_file_path_direccion.text().strip(),
            'unidad_construccion': self.data_source_widget.txt_file_path_uni.text().strip(),
            'unidad_construccion_comp': self.data_source_widget.txt_file_path_uni_comp.text().strip(),
            'persona': self.data_source_widget.txt_file_path_persona.text().strip(),
            'persona_predio': self.data_source_widget.txt_file_path_persona_predio.text().strip(),
            'ficha_matriz': self.data_source_widget.txt_file_path_ficha_m.text().strip(),
            'ficha_matriz_predio': self.data_source_widget.txt_file_path_ficha_m_predio.text().strip(),
            'ficha_matriz_torre': self.data_source_widget.txt_file_path_ficha_m_torre.text().strip()
        }

        filename, file_extension = os.path.splitext(self.data_source_widget.txt_file_path_uni.text().strip())
        shutil.copyfile(BUILDING_UNIT_CSVT_FILE_PATH, '{}.{}'.format(filename, 'csvt'))
        
        root = QgsProject.instance().layerTreeRoot()
        alphanumeric_group = root.addGroup(QCoreApplication.translate(self.CLASS_NAME, "SNC Alphanumeric Supplies"))

        optional_layers = {'predio_bloqueo':PREDIO_BLOQUEO_FILE_PATH,
                           'ficha_matriz':FICHA_MATRIZ_FILE_PATH,
                           'ficha_matriz_predio':FICHA_MATRIZ_PREDIO_FILE_PATH,
                           'ficha_matriz_torre':FICHA_MATRIZ_TORRE_FILE_PATH,}

        for name in self.alphanumeric_file_paths:
            layer = QgsVectorLayer(self.alphanumeric_file_paths[name], name, 'ogr')
            if layer.isValid():
                self.alphanumeric_file_paths[name] = layer
                QgsProject.instance().addMapLayer(layer, False)
                alphanumeric_group.addLayer(layer)
            else:
                if name in optional_layers.keys():
                    # predio_bloqueo, ficha_matriz, ficha_matriz_predio and ficha_matriz_torre
                    # are optional, if they are not given, we pass default values
                    layer = QgsVectorLayer(optional_layers[name], name, 'ogr')
                    self.alphanumeric_file_paths[name] = layer
                    if layer.isValid():
                        QgsProject.instance().addMapLayer(layer, False)
                        alphanumeric_group.addLayer(layer)
                else:
                    return False, QCoreApplication.translate(self.CLASS_NAME, "There were troubles loading the CSV file called '{}'.".format(name))

        try:
            os.remove('{}.{}'.format(filename, 'csvt'))
        except:
            pass

        return True, ''

    def run_etl_model(self, custom_feedback):
        self.logger.info(__name__, "Running ETL-SNC model...")
        try:
            processing.run("model:ETL_SNC",
                           {'ubarrio': self.gdb_layer_paths['U_BARRIO'],
                            'fichamatriz': self.alphanumeric_file_paths['ficha_matriz'],
                            'fichamatrizpredio': self.alphanumeric_file_paths['ficha_matriz_predio'],
                            'fichamatriztorre': self.alphanumeric_file_paths['ficha_matriz_torre'],
                            'gcbarrio': self.layers[self.names.GC_NEIGHBOURHOOD_T],
                            'gccomisionesconstruccion': self.layers[self.names.GC_COMMISSION_BUILDING_T],
                            'gccomisionesterreno': self.layers[self.names.GC_COMMISSION_PLOT_T],
                            'gccomisionesunidadconstruccion': self.layers[self.names.GC_COMMISSION_BUILDING_UNIT_T],
                            'gcconstruccion': self.layers[self.names.GC_BUILDING_T],
                            'gccopropiedad': self.layers[self.names.GC_COPROPERTY_T],
                            'gcdatostorreph': self.layers[self.names.GC_HP_TOWER_DATA_T],
                            'gcdireccion': self.layers[self.names.GC_ADDRESS_T],
                            'gccalificacionuconstruccion': self.layers[self.names.GC_QUALIFICATION_BUILDING_UNIT_T],
                            'gcestadopredio': self.layers[self.names.GC_PARCEL_STATUS_T],
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
                            'umanzana': self.gdb_layer_paths['U_MANZANA'],
                            'persona': self.alphanumeric_file_paths['persona'],
                            'personapredio': self.alphanumeric_file_paths['persona_predio'],
                            'prediobloqueo': self.alphanumeric_file_paths['predio_bloqueo'],
                            'predio': self.alphanumeric_file_paths['predio'],
                            'prediodireccion': self.alphanumeric_file_paths['direccion'],
                            'rconstruccion': self.gdb_layer_paths['R_CONSTRUCCION'],
                            'rnomenclatura': self.gdb_layer_paths['R_NOMENCLATURA_DOMICILIARIA'],
                            'uperimetro': self.gdb_layer_paths['U_PERIMETRO'],
                            'rsector': self.gdb_layer_paths['R_SECTOR'],
                            'rterreno': self.gdb_layer_paths['R_TERRENO'],
                            'runidad': self.gdb_layer_paths['R_UNIDAD'],
                            'uconstruccion': self.gdb_layer_paths['U_CONSTRUCCION'],
                            'unidadconstruccion': self.alphanumeric_file_paths['unidad_construccion'],
                            'unidadconstrucioncomp': self.alphanumeric_file_paths['unidad_construccion_comp'],
                            'unomenclatura': self.gdb_layer_paths['U_NOMENCLATURA_DOMICILIARIA'],
                            'usector': self.gdb_layer_paths['U_SECTOR'],
                            'uterreno': self.gdb_layer_paths['U_TERRENO'],
                            'uunidad': self.gdb_layer_paths['U_UNIDAD'],
                            'rvereda': self.gdb_layer_paths['R_VEREDA']},
                            feedback=custom_feedback)
        except QgsProcessingException as e:
            msg = "QgsProcessingException (ETL-SNC): {} Details in the QGIS log.".format(str(e))
            self.logger.critical_msg(__name__, msg)
            return False

        self.logger.info(__name__, "ETL-SNC model finished.")
        return True