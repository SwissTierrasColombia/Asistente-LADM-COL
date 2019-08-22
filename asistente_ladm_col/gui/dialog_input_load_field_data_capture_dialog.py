# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-07-17
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
import psycopg2

from ..gui.qgis_model_baker.dlg_import_schema import DialogImportSchema
from ..gui.log_excel_dialog import LogExcelDialog
from ..lib.db.pg_connector import PGConnector

from qgis.PyQt.QtCore import QVariant

from asistente_ladm_col.utils.qt_utils import (make_file_selector,
                                               make_folder_selector)

from ..utils.qfield_utils import (run_etl_model_input_load_data,
                                  join_layers,
                                  create_virtual_field,
                                  delete_virtual_field,
                                  fix_spatial_layer,
                                  get_directions,
                                  extract_by_expresion)

from ..utils.qt_utils import OverrideCursor

from qgis.core import (QgsProject,
                       QgsField,
                       QgsVectorLayer,
                       QgsVectorLayerJoinInfo)

from ..config.table_mapping_config import (PARCEL_TABLE,
                                           COL_PARTY_TABLE,
                                           RIGHT_TABLE,
                                           ADMINISTRATIVE_SOURCE_TABLE,
                                           RRR_SOURCE_RELATION_TABLE,
                                           UEBAUNIT_TABLE,
                                           UEBAUNIT_TABLE_BUILDING_FIELD, 
                                           UEBAUNIT_TABLE_PLOT_FIELD, 
                                           UEBAUNIT_TABLE_PLOT_FIELD,
                                           PLOT_TABLE, 
                                           FDC_SECTOR,
                                           FDC_VILLAGE,
                                           FDC_BLOCK,
                                           FDC_NEIGHBOURHOOD,
                                           BUILDING_TABLE,
                                           VALUATION_BUILDING_TABLE,
                                           VALUATION_BUILDING_UNIT_TABLE,
                                           BUILDING_UNIT_TABLE,
                                           AVALUOUNIDADCONSTRUCCION_TABLE,
                                           FDC_VALUATION_BUILDING_CONNECTION,
                                           EXTADDRESS_TABLE,
                                           VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE,
                                           VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE,
                                           CODIGO_R1_GDB,
                                           DEPARTAMENTO_R1_GDB,
                                           MUNICIPIO_R1_GDB,
                                           NO_PREDIAL_R1_GDB)

from qgis.PyQt.QtCore import (Qt,
                              QSettings,
                              QCoreApplication,
                              QFile)

from qgis.PyQt.QtWidgets import (QDialog,
                                 QFileDialog,
                                 QMessageBox,
                                 QSizePolicy,
                                 QGridLayout,
                                 QDialogButtonBox,
                                 QTextEdit,
                                 QVBoxLayout,
                                 QRadioButton)

from qgis.core import (Qgis,
                       QgsMapLayerProxyModel,
                       QgsApplication,
                       QgsCoordinateReferenceSystem,
                       QgsWkbTypes)
from qgis.gui import QgsMessageBar

from ..config.help_strings import HelpStrings

from ..config.general_config import (DEFAULT_MODEL_NAMES_CHECKED,
                                    OFFICIAL_DB_PREFIX,
                                    OFFICIAL_DB_SUFFIX,
                                    PREFIX_LAYER_MODIFIERS,
                                    SUFFIX_LAYER_MODIFIERS,
                                    STYLE_GROUP_LAYER_MODIFIERS)

from ..config.symbology import OFFICIAL_STYLE_GROUP

from ..utils import get_ui_class

WIZARD_UI = get_ui_class('dlg_input_load_field_data_capture.ui')

class DialogInputLoadFieldDataCapture(QDialog, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()
        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.accepted)
        self.progress.setVisible(False)
        self.restore_settings()

        self.txt_file_path_r2.setDisabled(True)
        self.txt_file_path_registry.setDisabled(True)
        self.btn_browse_file_r2.setDisabled(True)
        self.btn_browse_file_registry.setDisabled(True)

        self.btn_browse_connection.clicked.connect(self.show_settings)
        self.update_connection_info()

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
        self.save_settings()
        if self._db.test_connection()[0]:
            reply = QMessageBox.question(self,
                                     QCoreApplication.translate("DialogImportFromExcel", "Warning"),
                                     QCoreApplication.translate("DialogImportFromExcel",
                                                                "The schema <i>{schema}</i> already has a valid LADM_COL structure.<br/><br/>If such schema has any data, loading data into it might cause invalid data.<br/><br/>Do you still want to continue?".format(schema=self._db.schema)),
                                     QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                with OverrideCursor(Qt.WaitCursor):
                    self.manage_process_load_data()
        else:
            with OverrideCursor(Qt.WaitCursor):
                self.create_model_into_database()
                if self._db.test_connection()[0]:
                    self.manage_process_load_data()

    def load_data_for_etl(self):
        self.progress.setVisible(True)
        self.progress.setValue(1)
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading R1 tables..."))
        self.layer_r1 = QgsVectorLayer(self.txt_file_path_r1.text(), 'R1_IGAC', 'ogr')
        QgsProject.instance().addMapLayer(self.layer_r1)

        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading GDB tables..."))
        gdb_path = self.txt_file_path_gdb.text()
        layer = QgsVectorLayer(gdb_path, 'layer name', 'ogr')
        sublayers = layer.dataProvider().subLayers()

        root = QgsProject.instance().layerTreeRoot()
        gdb_group = root.addGroup("GDB")
        self.gdb_layer_list = []

        for data in sublayers:
            vlayer = QgsVectorLayer(gdb_path + '|layername=' + data.split('!!::!!')[1], data.split('!!::!!')[1], 'ogr')
            self.gdb_layer_list.append(vlayer)
            QgsProject.instance().addMapLayer(vlayer, False)
            gdb_group.addLayer(vlayer)

        layer_modifiers = {
                PREFIX_LAYER_MODIFIERS: OFFICIAL_DB_PREFIX,
                SUFFIX_LAYER_MODIFIERS: OFFICIAL_DB_SUFFIX,
                STYLE_GROUP_LAYER_MODIFIERS: OFFICIAL_STYLE_GROUP
            }

        self.res_layers = self.qgis_utils.get_layers(self._db, {
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None},
            COL_PARTY_TABLE: {'name': COL_PARTY_TABLE, 'geometry': None},
            RIGHT_TABLE: {'name': RIGHT_TABLE, 'geometry': None},
            ADMINISTRATIVE_SOURCE_TABLE: {'name': ADMINISTRATIVE_SOURCE_TABLE, 'geometry': None},
            RRR_SOURCE_RELATION_TABLE: {'name': RRR_SOURCE_RELATION_TABLE, 'geometry': None},
            UEBAUNIT_TABLE: {'name': UEBAUNIT_TABLE, 'geometry': None},
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            FDC_SECTOR: {'name': FDC_SECTOR, 'geometry': None},
            FDC_VILLAGE: {'name': FDC_VILLAGE, 'geometry': None},
            FDC_NEIGHBOURHOOD: {'name': FDC_NEIGHBOURHOOD, 'geometry': None},
            BUILDING_TABLE: {'name': BUILDING_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            VALUATION_BUILDING_TABLE: {'name': VALUATION_BUILDING_TABLE, 'geometry': None},
            VALUATION_BUILDING_UNIT_TABLE: {'name': VALUATION_BUILDING_UNIT_TABLE, 'geometry': None},
            BUILDING_UNIT_TABLE: {'name': BUILDING_UNIT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            AVALUOUNIDADCONSTRUCCION_TABLE: {'name': AVALUOUNIDADCONSTRUCCION_TABLE, 'geometry': None},
            FDC_VALUATION_BUILDING_CONNECTION: {'name': FDC_VALUATION_BUILDING_CONNECTION, 'geometry': None},
            VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE: {'name': VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE, 'geometry': None},
            VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE: {'name': VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE, 'geometry': None},
            EXTADDRESS_TABLE: {'name': EXTADDRESS_TABLE, 'geometry': QgsWkbTypes.PointGeometry}
        }, load=True, layer_modifiers=layer_modifiers)

    def mapping_fields_r1(self):
        steps = 29
        step = 0

        #This section of code allow import data from R1 in excel to Parcel table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(PARCEL_TABLE)))
        query = "select * from {} group by NoPredial&nogeometry".format(self.layer_r1.name())
        input_data = QgsVectorLayer( "?query={}".format(query), "vlayer", "virtual")
        run_etl_model_input_load_data(input_data, self.res_layers[PARCEL_TABLE], PARCEL_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data from R1 in excel to Party table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(COL_PARTY_TABLE)))
        run_etl_model_input_load_data(self.layer_r1, self.res_layers[COL_PARTY_TABLE], COL_PARTY_TABLE, self.qgis_utils)
        create_virtual_field(self.res_layers[COL_PARTY_TABLE], 'Codigo', 'concat({}, {}, {})'.format(DEPARTAMENTO_R1_GDB, MUNICIPIO_R1_GDB, NO_PREDIAL_R1_GDB))
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data from  Party table to Right table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(RIGHT_TABLE)))
        join_layers(self.res_layers[COL_PARTY_TABLE], self.res_layers[PARCEL_TABLE], 'Codigo', 'numero_predial')
        run_etl_model_input_load_data(self.res_layers[COL_PARTY_TABLE], self.res_layers[RIGHT_TABLE], RIGHT_TABLE, self.qgis_utils)
        delete_virtual_field(self.res_layers[COL_PARTY_TABLE], 'Codigo')
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data from  Right table to Administrative Source table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(ADMINISTRATIVE_SOURCE_TABLE)))
        run_etl_model_input_load_data(self.res_layers[RIGHT_TABLE], self.res_layers[ADMINISTRATIVE_SOURCE_TABLE], ADMINISTRATIVE_SOURCE_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)        

        #This section of code allow import data from  Administrative Source table to RRR Source table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(RRR_SOURCE_RELATION_TABLE)))
        run_etl_model_input_load_data(self.res_layers[ADMINISTRATIVE_SOURCE_TABLE], self.res_layers[RRR_SOURCE_RELATION_TABLE], RRR_SOURCE_RELATION_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

    def mapping_fields_gbb(self):
        steps = 29
        step = 5

        #This section of code allow import data R_TERRENO from GDB to Plot table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(PLOT_TABLE)))
        run_etl_model_input_load_data('R_TERRENO', self.res_layers[PLOT_TABLE], PLOT_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data U_TERRENO from GDB to Plot table in LADM structure.
        run_etl_model_input_load_data('U_TERRENO', self.res_layers[PLOT_TABLE], PLOT_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data R_SECTOR from GDB to Sector table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(FDC_SECTOR)))
        run_etl_model_input_load_data('R_SECTOR', self.res_layers[FDC_SECTOR], FDC_SECTOR, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data U_SECTOR from GDB to Sector table in LADM structure.
        run_etl_model_input_load_data('U_SECTOR', self.res_layers[FDC_SECTOR], FDC_SECTOR, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data R_VEREDA from GDB to village table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(FDC_VILLAGE)))
        run_etl_model_input_load_data('R_VEREDA', self.res_layers[FDC_VILLAGE], FDC_VILLAGE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data U_MANZANA from GDB to village table in LADM structure.
        run_etl_model_input_load_data('U_MANZANA', self.res_layers[FDC_VILLAGE], FDC_BLOCK, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data U_BARRIO from GDB to Neighbourhood table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(FDC_NEIGHBOURHOOD)))
        run_etl_model_input_load_data('U_BARRIO', self.res_layers[FDC_NEIGHBOURHOOD], FDC_NEIGHBOURHOOD, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data R_CONSTRUCCION from GDB to Building table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(BUILDING_TABLE)))
        run_etl_model_input_load_data('R_CONSTRUCCION', self.res_layers[BUILDING_TABLE], BUILDING_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data U_CONSTRUCCION from GDB to Building table in LADM structure.
        run_etl_model_input_load_data('U_CONSTRUCCION', self.res_layers[BUILDING_TABLE], BUILDING_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data R_CONSTRUCCION from GDB to Valuation Building table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(VALUATION_BUILDING_TABLE)))
        run_etl_model_input_load_data('R_CONSTRUCCION', self.res_layers[VALUATION_BUILDING_TABLE], VALUATION_BUILDING_TABLE, self.qgis_utils)
        create_virtual_field(self.res_layers[VALUATION_BUILDING_TABLE], 'identificador', '$id')
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data R_CONSTRUCCION from GDB to Valuation Building table in LADM structure.
        run_etl_model_input_load_data('U_CONSTRUCCION', self.res_layers[VALUATION_BUILDING_TABLE], VALUATION_BUILDING_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #Select layers to make the join.
        uunidad = QgsProject.instance().mapLayersByName('U_UNIDAD')[0]
        runidad = QgsProject.instance().mapLayersByName('R_UNIDAD')[0]
        #Generate join between U_Unidad GDB and Building table in LADM structure.
        join_layers(uunidad, self.res_layers[BUILDING_TABLE], CODIGO_R1_GDB, 'etiqueta')
        #Generate join between R_Unidad GDB and Building table in LADM structure.
        join_layers(runidad, self.res_layers[BUILDING_TABLE], CODIGO_R1_GDB, 'etiqueta')
        #Fix geometries.
        uunidad_filter = fix_spatial_layer(uunidad)
        runidad_filter = fix_spatial_layer(runidad)
        #Filter by expresion , the result of the process.
        uunidad_filter = extract_by_expresion(uunidad_filter, "construccion_oficial_t_id != 'NULL'")
        runidad_filter = extract_by_expresion(runidad_filter, "construccion_oficial_t_id != 'NULL'")

        #This section of code allow import data uunidad_filter from the previous process to Valuation Building unit table in LADM structure. 
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(VALUATION_BUILDING_UNIT_TABLE)))
        run_etl_model_input_load_data(uunidad_filter, self.res_layers[VALUATION_BUILDING_UNIT_TABLE], VALUATION_BUILDING_UNIT_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data runidad_filter from the previous process to Valuation Building unit table in LADM structure. 
        run_etl_model_input_load_data(runidad_filter, self.res_layers[VALUATION_BUILDING_UNIT_TABLE], VALUATION_BUILDING_UNIT_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data uunidad_filter from the previous process to Building unit table in LADM structure. 
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(BUILDING_UNIT_TABLE)))
        run_etl_model_input_load_data(uunidad_filter, self.res_layers[BUILDING_UNIT_TABLE], BUILDING_UNIT_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data runidad_filter from the previous process to Building unit table in LADM structure. 
        run_etl_model_input_load_data(runidad_filter, self.res_layers[BUILDING_UNIT_TABLE], BUILDING_UNIT_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)
        
        #Join between Building unit table and Valuation Building Unit Table in LADM structure.
        join_layers(self.res_layers[BUILDING_UNIT_TABLE], 
                        self.res_layers[VALUATION_BUILDING_UNIT_TABLE], 'area_construida', 'puntuacion')
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(AVALUOUNIDADCONSTRUCCION_TABLE)))
        #This section of code allow import data Building unit table from LADM structure to Valuation Building unit table in LADM structure.
        run_etl_model_input_load_data(self.res_layers[BUILDING_UNIT_TABLE], self.res_layers[AVALUOUNIDADCONSTRUCCION_TABLE],
                                                                 AVALUOUNIDADCONSTRUCCION_TABLE, self.qgis_utils)                
        step += 1
        self.progress.setValue(step/steps * 100)

        #Join between Building unit table and Valuation Building Table in LADM structure.
        join_layers(self.res_layers[BUILDING_TABLE], 
                        self.res_layers[VALUATION_BUILDING_TABLE], 'avaluo_construccion', 'identificador')
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(FDC_VALUATION_BUILDING_CONNECTION)))
        #This section of code allow import data Building unit table from LADM structure to Valuation Building connection table in LADM structure
        run_etl_model_input_load_data(self.res_layers[BUILDING_TABLE], self.res_layers[FDC_VALUATION_BUILDING_CONNECTION],
                                                                 FDC_VALUATION_BUILDING_CONNECTION, self.qgis_utils) 
        delete_virtual_field(self.res_layers[VALUATION_BUILDING_TABLE], 'identificador')
        step += 1
        self.progress.setValue(step/steps * 100)

        #Fix and  extract by expresion the data who if Convencional type.
        layer_filter = fix_spatial_layer(self.res_layers[VALUATION_BUILDING_UNIT_TABLE])
        layer_filter.setSubsetString("construccion_tipo = 'Convencional'")
        #This section of code allow import data layer_filter from the previous process to Valuation Building unit qualification conventional table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE)))
        run_etl_model_input_load_data(layer_filter, self.res_layers[VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE], VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #Fix and  extract by expresion the data who if No Convencional type.
        layer_filter = fix_spatial_layer(self.res_layers[VALUATION_BUILDING_UNIT_TABLE])
        layer_filter.setSubsetString("construccion_tipo = 'noConvencional'")
        #This section of code allow import data layer_filter from the previous process to Valuation Building unit qualification no conventional table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE)))
        run_etl_model_input_load_data(layer_filter, self.res_layers[VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE], VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        unomen = QgsProject.instance().mapLayersByName('U_NOMENCLATURA_DOMICILIARIA')[0]
        rnomen = QgsProject.instance().mapLayersByName('R_NOMENCLATURA_DOMICILIARIA')[0]

        #This section of code allow import data U_NOMENCLATURA_DOMICILIARIA from GDB to Building table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(EXTADDRESS_TABLE)))
        run_etl_model_input_load_data(get_directions(unomen, self.res_layers[BUILDING_TABLE]), self.res_layers[EXTADDRESS_TABLE], EXTADDRESS_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data R_NOMENCLATURA_DOMICILIARIA from GDB to Building table in LADM structure.
        run_etl_model_input_load_data(get_directions(rnomen, self.res_layers[PLOT_TABLE]), self.res_layers[EXTADDRESS_TABLE], EXTADDRESS_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import join between building table and parcel table to Uebaunit table in LADM structure.
        join_layers(self.res_layers[PARCEL_TABLE], self.res_layers[BUILDING_TABLE], 'numero_predial', 'su_local_id')
        vlayer = extract_by_expresion(self.res_layers[PARCEL_TABLE], "construccion_oficial_t_id != 'NULL'")
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(UEBAUNIT_TABLE_BUILDING_FIELD)))
        run_etl_model_input_load_data(vlayer, self.res_layers[UEBAUNIT_TABLE], UEBAUNIT_TABLE_BUILDING_FIELD, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import join between plot table and parcel table to Uebaunit table in LADM structure.
        join_layers(self.res_layers[PARCEL_TABLE], self.res_layers[PLOT_TABLE], 'numero_predial', 'etiqueta')
        vlayer = extract_by_expresion(self.res_layers[PARCEL_TABLE], "terreno_oficial_t_id != 'NULL'")
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(UEBAUNIT_TABLE_PLOT_FIELD)))
        run_etl_model_input_load_data(vlayer, self.res_layers[UEBAUNIT_TABLE], UEBAUNIT_TABLE_PLOT_FIELD, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import join between building unit table and parcel table to Uebaunit table in LADM structure.
        join_layers(self.res_layers[PARCEL_TABLE], self.res_layers[BUILDING_UNIT_TABLE], 'numero_predial', 'su_local_id')
        vlayer = extract_by_expresion(self.res_layers[PARCEL_TABLE], "unidadconstruccion_oficial_t_id != 'NULL'")
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(UEBAUNIT_TABLE_PLOT_FIELD)))
        run_etl_model_input_load_data(vlayer, self.res_layers[UEBAUNIT_TABLE], UEBAUNIT_TABLE_PLOT_FIELD, self.qgis_utils) 
        step += 1
        self.progress.setValue(step/steps * 100)

    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/input_load_field_data_capture/r1_path', self.txt_file_path_r1.text())
        settings.setValue('Asistente-LADM_COL/input_load_field_data_capture/gdb_path', self.txt_file_path_gdb.text())

    def restore_settings(self):
        settings = QSettings()
        self.txt_file_path_r1.setText(settings.value('Asistente-LADM_COL/input_load_field_data_capture/r1_path', ''))
        self.txt_file_path_gdb.setText(settings.value('Asistente-LADM_COL/input_load_field_data_capture/gdb_path', ''))

    def show_settings(self):
        dlg = self.qgis_utils.get_official_data_settings_dialog()
        
        if dlg.exec_():
            self._db = dlg.get_db_connection()
            self.update_connection_info()

    def update_connection_info(self):
        db_description = self._db.get_description_conn_string()
        if db_description:
            self.db_connect_label.setText(db_description)
            self.db_connect_label.setToolTip(self._db.get_display_conn_string())
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.db_connect_label.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "The database is not defined!"))
            self.db_connect_label.setToolTip('')
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

    def ladm_tables_feature_count_before(self):
        layers_name_summary = [FDC_NEIGHBOURHOOD, BUILDING_TABLE, RIGHT_TABLE, EXTADDRESS_TABLE, ADMINISTRATIVE_SOURCE_TABLE, COL_PARTY_TABLE, 
                            FDC_VILLAGE, PARCEL_TABLE, PLOT_TABLE, BUILDING_UNIT_TABLE]

        features_count_before = {}

        for layer in layers_name_summary:
            features_count_before[layer] = self.res_layers[layer].featureCount()

        return features_count_before

    def show_log_data(self, ladm_count_before):
        self.summary = ""
        self.label_r1.setVisible(False)
        self.label_r2.setVisible(False)
        self.label_gdb.setVisible(False)
        self.label_registry.setVisible(False)
        
        self.txt_file_path_r1.setVisible(False)
        self.txt_file_path_r2.setVisible(False)
        self.txt_file_path_gdb.setVisible(False)
        self.txt_file_path_registry.setVisible(False)

        self.btn_browse_file_r1.setVisible(False)
        self.btn_browse_file_r2.setVisible(False)
        self.btn_browse_file_gdb.setVisible(False)
        self.btn_browse_file_registry.setVisible(False)

        self.progress.setVisible(False)

        layers_name_summary = [FDC_NEIGHBOURHOOD, BUILDING_TABLE, RIGHT_TABLE, EXTADDRESS_TABLE, ADMINISTRATIVE_SOURCE_TABLE, COL_PARTY_TABLE, 
                            FDC_VILLAGE, PARCEL_TABLE, PLOT_TABLE, BUILDING_UNIT_TABLE]

        for name in layers_name_summary:
            layer = QgsProject.instance().mapLayersByName('{}_oficial'.format(name))[0]
            layer.featureCount()
            self.summary += QCoreApplication.translate("DialogInputLoadFieldDataCapture",
                        "<b>{count}</b> records loaded into table <b>{table}</b><br/>").format(
                            count=layer.featureCount() - ladm_count_before[name],
                            table=layer.name())

        self.txt_log.setText(self.summary)

    def create_model_into_database(self):
        get_import_schema_dialog = DialogImportSchema(self.iface, self._db, self.qgis_utils)
        for modelname in DEFAULT_MODEL_NAMES_CHECKED:
            item = get_import_schema_dialog.import_models_list_widget.findItems(modelname, Qt.MatchExactly)
            item[0].setCheckState(Qt.Checked)
        
        get_import_schema_dialog.accepted()

        if not self._db.test_connection()[0]:
            dlg = LogExcelDialog(self.qgis_utils, get_import_schema_dialog.txtStdout.toHtml())
            dlg.buttonBox.button(QDialogButtonBox.Save).setVisible(False)
            dlg.setFixedSize(dlg.size()) 
            dlg.setWindowTitle(QCoreApplication.translate("DialogInputLoadFieldDataCapture","Log error structure LADM"))
            dlg.exec_()
            return

    def set_gui_enabled(self, enabled):
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(enabled)
        self.label_r1.setEnabled(enabled)
        self.label_r2.setEnabled(enabled)
        self.label_gdb.setEnabled(enabled)
        self.label_registry.setEnabled(enabled)
        
        self.txt_file_path_r1.setEnabled(enabled)
        self.txt_file_path_r2.setEnabled(enabled)
        self.txt_file_path_gdb.setEnabled(enabled)
        self.txt_file_path_registry.setEnabled(enabled)

        self.btn_browse_file_r1.setEnabled(enabled)
        self.btn_browse_file_r2.setEnabled(enabled)
        self.btn_browse_file_gdb.setEnabled(enabled)
        self.btn_browse_file_registry.setEnabled(enabled)

    def clean_layer_joins(self, layers):
        for layer in layers:
            if isinstance(layer, str):
                layer = layers[layer]
            joins_info = layer.vectorJoins()
            for join_info in joins_info:
                layer.removeJoin(join_info.joinLayerId())    

    def manage_process_load_data(self):
        """
        Workflow for loading official data
        """
        # We need a temporary cache for official relations. Store current cache if any, and build a new cache...
        cached_layers, cached_relations, cached_bags_of_enum = self.qgis_utils._layers, self.qgis_utils._relations, self.qgis_utils._bags_of_enum
        self.qgis_utils.cache_layers_and_relations(self._db, True)

        self.set_gui_enabled(False)
        self.load_data_for_etl()
        features_count_before = self.ladm_tables_feature_count_before()
        self.mapping_fields_r1()
        self.mapping_fields_gbb()
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.show_log_data(features_count_before)

        # When finish the etl process, we need remove all joins in the layers, so we delete all joins in r1, gdb and LADM_COL layers 
        self.clean_layer_joins(self.gdb_layer_list)
        self.clean_layer_joins([self.layer_r1])
        self.clean_layer_joins(self.res_layers)

        # No one else needs the official cache, so go back to initial state
        self.qgis_utils._layers, self.qgis_utils._relations, self.qgis_utils._bags_of_enum = cached_layers, cached_relations, cached_bags_of_enum

