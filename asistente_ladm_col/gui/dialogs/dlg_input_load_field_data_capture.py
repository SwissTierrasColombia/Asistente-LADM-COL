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

from ...gui.qgis_model_baker.dlg_import_schema import DialogImportSchema
from ...gui.dialogs.dlg_log_excel import LogExcelDialog
from ...gui.dialogs.dlg_official_data_settings import OfficialDataSettingsDialog
from ...lib.db.db_connector import EnumTestLevel
from ...lib.db.db_connection_manager import ConnectionManager

from qgis.PyQt.QtCore import QVariant

from asistente_ladm_col.utils.qt_utils import (make_file_selector,
                                               make_folder_selector)

from ...utils.qfield_utils import (run_etl_model_input_load_data,
                                  join_layers,
                                  create_virtual_field,
                                  delete_virtual_field,
                                  fix_spatial_layer,
                                  get_directions,
                                  extract_by_expresion)

from ...utils.qt_utils import OverrideCursor

from qgis.core import (QgsProject,
                       QgsField,
                       QgsVectorLayer,
                       QgsVectorLayerJoinInfo)

from ...config.table_mapping_config import (PARCEL_TABLE,
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

from ...config.help_strings import HelpStrings

from ...config.general_config import (LAYER,
                                     DEFAULT_MODEL_NAMES_CHECKED,
                                     OFFICIAL_DB_PREFIX,
                                     OFFICIAL_DB_SUFFIX,
                                     PREFIX_LAYER_MODIFIERS,
                                     SUFFIX_LAYER_MODIFIERS,
                                     STYLE_GROUP_LAYER_MODIFIERS,
                                     OFFICIAL_DB_SOURCE)

from ...config.symbology import OFFICIAL_STYLE_GROUP

from ...utils import get_ui_class

WIZARD_UI = get_ui_class('dialogs/dlg_input_load_field_data_capture.ui')

class InputLoadFieldDataCaptureDialog(QDialog, WIZARD_UI):
    def __init__(self, iface, conn_manager, qgis_utils, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.conn_manager = conn_manager
        self._db = None
        self.log = QgsApplication.messageLog()
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()
        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.accepted)
        self.progress.setVisible(False)
        self.restore_settings()

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

        self._layers = {
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None, LAYER: None},
            COL_PARTY_TABLE: {'name': COL_PARTY_TABLE, 'geometry': None, LAYER: None},
            RIGHT_TABLE: {'name': RIGHT_TABLE, 'geometry': None, LAYER: None},
            ADMINISTRATIVE_SOURCE_TABLE: {'name': ADMINISTRATIVE_SOURCE_TABLE, 'geometry': None, LAYER: None},
            RRR_SOURCE_RELATION_TABLE: {'name': RRR_SOURCE_RELATION_TABLE, 'geometry': None, LAYER: None},
            UEBAUNIT_TABLE: {'name': UEBAUNIT_TABLE, 'geometry': None, LAYER: None},
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            FDC_SECTOR: {'name': FDC_SECTOR, 'geometry': None, LAYER: None},
            FDC_VILLAGE: {'name': FDC_VILLAGE, 'geometry': None, LAYER: None},
            FDC_NEIGHBOURHOOD: {'name': FDC_NEIGHBOURHOOD, 'geometry': None, LAYER: None},
            BUILDING_TABLE: {'name': BUILDING_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            VALUATION_BUILDING_TABLE: {'name': VALUATION_BUILDING_TABLE, 'geometry': None, LAYER: None},
            VALUATION_BUILDING_UNIT_TABLE: {'name': VALUATION_BUILDING_UNIT_TABLE, 'geometry': None, LAYER: None},
            BUILDING_UNIT_TABLE: {'name': BUILDING_UNIT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            AVALUOUNIDADCONSTRUCCION_TABLE: {'name': AVALUOUNIDADCONSTRUCCION_TABLE, 'geometry': None, LAYER: None},
            FDC_VALUATION_BUILDING_CONNECTION: {'name': FDC_VALUATION_BUILDING_CONNECTION, 'geometry': None, LAYER: None},
            VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE: {'name': VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE, 'geometry': None, LAYER: None},
            VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE: {'name': VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE, 'geometry': None, LAYER: None},
            EXTADDRESS_TABLE: {'name': EXTADDRESS_TABLE, 'geometry': QgsWkbTypes.PointGeometry, LAYER: None}
        }

        self.txt_file_path_r2.setDisabled(True)
        self.txt_file_path_registry.setDisabled(True)
        self.btn_browse_file_r2.setDisabled(True)
        self.btn_browse_file_registry.setDisabled(True)

        self.btn_browse_connection.clicked.connect(self.show_settings)
        self.update_connection_info()

        self.btn_browse_file_r1.clicked.connect(
            make_file_selector(self.txt_file_path_r1, QCoreApplication.translate("InputLoadFieldDataCaptureDialog",
                        "Select the Excel file with data in the intermediate structure"), 
                        QCoreApplication.translate("InputLoadFieldDataCaptureDialog", 'Excel File (*.xlsx *.xls)')))

        self.btn_browse_file_gdb.clicked.connect(
                make_folder_selector(self.txt_file_path_gdb, title=QCoreApplication.translate(
                'SettingsDialog', 'Open Folder with GDB'), parent=None))

    def show_help(self):
        self.qgis_utils.show_help("create_points")

    def show_message(self, message, level):
        self.bar.pushMessage(message, level, 10)

    def accepted(self):
        self.save_settings()
        
        if self._db.test_connection()[0]:
            reply = QMessageBox.question(self,
                                     QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "Warning"),
                                     QCoreApplication.translate("InputLoadFieldDataCaptureDialog",
                                                                "The schema <i>{schema}</i> already has a valid LADM_COL structure.<br/><br/>If such schema has any data, loading data into it might cause invalid data.<br/><br/>Do you still want to continue?".format(schema=self._db.schema)),
                                     QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                with OverrideCursor(Qt.WaitCursor):
                    self.remove_layer('R1_IGAC')
                    self.remove_group('GDB')
                    self.manage_process_load_data()
        else:
            with OverrideCursor(Qt.WaitCursor):
                self.create_model_into_database()
                if self._db.test_connection()[0]:
                    self.remove_group('GDB')
                    self.manage_process_load_data()

    def load_data_for_etl(self):
        self.progress.setVisible(True)
        self.progress.setValue(1)
        self.txt_log.setText(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "Loading R1 tables..."))
        self.layer_r1 = QgsVectorLayer(self.txt_file_path_r1.text(), 'R1_IGAC', 'ogr')
        QgsProject.instance().addMapLayer(self.layer_r1)

        self.txt_log.setText(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "Loading GDB tables..."))
        gdb_path = self.txt_file_path_gdb.text()
        layer = QgsVectorLayer(gdb_path, 'layer name', 'ogr')
        if not layer.isValid():
            self.show_message(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "Select a valid GDB"), Qgis.Warning)
            return False

        sublayers = layer.dataProvider().subLayers()

        root = QgsProject.instance().layerTreeRoot()
        gdb_group = root.addGroup("GDB")
        self.gdb_layer_list = []
        validating_layers = ['R_TERRENO','U_TERRENO','R_SECTOR','U_SECTOR','R_VEREDA','U_MANZANA','U_BARRIO','R_CONSTRUCCION','U_CONSTRUCCION','U_UNIDAD','R_UNIDAD','U_NOMENCLATURA_DOMICILIARIA','R_NOMENCLATURA_DOMICILIARIA']

        for data in sublayers:
            if data.split('!!::!!')[1] in validating_layers:
                validating_layers.remove(data.split('!!::!!')[1])

            vlayer = QgsVectorLayer(gdb_path + '|layername=' + data.split('!!::!!')[1], data.split('!!::!!')[1], 'ogr')
            self.gdb_layer_list.append(vlayer)
            QgsProject.instance().addMapLayer(vlayer, False)
            gdb_group.addLayer(vlayer)

        if validating_layers != []:
            self.show_message(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "The GDB doesn't have all the layers that ETL function needs"), Qgis.Warning)
            return False

        layer_modifiers = {
                PREFIX_LAYER_MODIFIERS: OFFICIAL_DB_PREFIX,
                SUFFIX_LAYER_MODIFIERS: OFFICIAL_DB_SUFFIX,
                STYLE_GROUP_LAYER_MODIFIERS: OFFICIAL_STYLE_GROUP
            }

        self.qgis_utils.get_layers(self._db, self._layers, load=True, layer_modifiers=layer_modifiers)
        if not self._layers:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("InputLoadFieldDataCaptureDialog",
                                           "'{}' tool has been closed because there was a problem loading the requeries layers.").format(
                    "Input load dialog"),
                Qgis.Warning)
            return False

        return True

    def mapping_fields_r1(self):
        steps = 29
        step = 0

        create_virtual_field(self.layer_r1, 'id', '$id')
        create_virtual_field(self.layer_r1, 'Numero_predial', "concat(Departamento , Municipio, NoPredial)")

        #This section of code allow import data from R1 in excel to Parcel table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "Loading data to {} table...".format(PARCEL_TABLE)))
        query = "select * from {} group by NoPredial&nogeometry".format(self.layer_r1.name())
        input_data = QgsVectorLayer( "?query={}".format(query), "vlayer", "virtual")
        run_etl_model_input_load_data(input_data, self._layers[PARCEL_TABLE][LAYER], PARCEL_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data from R1 in excel to Party table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "Loading data to {} table...".format(COL_PARTY_TABLE)))
        run_etl_model_input_load_data(self.layer_r1, self._layers[COL_PARTY_TABLE][LAYER], COL_PARTY_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data from  Party table to Right table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "Loading data to {} table...".format(RIGHT_TABLE)))
        join_layers(self._layers[COL_PARTY_TABLE][LAYER], self.layer_r1, 'organo_emisor', 'id')
        join_layers(self._layers[COL_PARTY_TABLE][LAYER], self._layers[PARCEL_TABLE][LAYER], 'R1_IGAC_Numero_predial', 'numero_predial')

        run_etl_model_input_load_data(self._layers[COL_PARTY_TABLE][LAYER], self._layers[RIGHT_TABLE][LAYER], RIGHT_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        delete_virtual_field(self.layer_r1, 'id')
        delete_virtual_field(self.layer_r1, 'Numero_predial')

        #This section of code allow import data from  Right table to Administrative Source table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "Loading data to {} table...".format(ADMINISTRATIVE_SOURCE_TABLE)))
        run_etl_model_input_load_data(self._layers[RIGHT_TABLE][LAYER], self._layers[ADMINISTRATIVE_SOURCE_TABLE][LAYER], ADMINISTRATIVE_SOURCE_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)        

        #This section of code allow import data from  Administrative Source table to RRR Source table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "Loading data to {} table...".format(RRR_SOURCE_RELATION_TABLE)))
        run_etl_model_input_load_data(self._layers[ADMINISTRATIVE_SOURCE_TABLE][LAYER], self._layers[RRR_SOURCE_RELATION_TABLE][LAYER], RRR_SOURCE_RELATION_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

    def mapping_fields_gbb(self):
        steps = 29
        step = 5

        #This section of code allow import data R_TERRENO from GDB to Plot table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "Loading data to {} table...".format(PLOT_TABLE)))
        run_etl_model_input_load_data('R_TERRENO', self._layers[PLOT_TABLE][LAYER], PLOT_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data U_TERRENO from GDB to Plot table in LADM structure.
        run_etl_model_input_load_data('U_TERRENO', self._layers[PLOT_TABLE][LAYER], PLOT_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data R_SECTOR from GDB to Sector table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "Loading data to {} table...".format(FDC_SECTOR)))
        run_etl_model_input_load_data('R_SECTOR', self._layers[FDC_SECTOR][LAYER], FDC_SECTOR, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data U_SECTOR from GDB to Sector table in LADM structure.
        run_etl_model_input_load_data('U_SECTOR', self._layers[FDC_SECTOR][LAYER], FDC_SECTOR, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data R_VEREDA from GDB to village table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "Loading data to {} table...".format(FDC_VILLAGE)))
        run_etl_model_input_load_data('R_VEREDA', self._layers[FDC_VILLAGE][LAYER], FDC_VILLAGE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data U_MANZANA from GDB to village table in LADM structure.
        run_etl_model_input_load_data('U_MANZANA', self._layers[FDC_VILLAGE][LAYER], FDC_BLOCK, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data U_BARRIO from GDB to Neighbourhood table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "Loading data to {} table...".format(FDC_NEIGHBOURHOOD)))
        run_etl_model_input_load_data('U_BARRIO', self._layers[FDC_NEIGHBOURHOOD][LAYER], FDC_NEIGHBOURHOOD, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data R_CONSTRUCCION from GDB to Building table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "Loading data to {} table...".format(BUILDING_TABLE)))
        run_etl_model_input_load_data('R_CONSTRUCCION', self._layers[BUILDING_TABLE][LAYER], BUILDING_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data U_CONSTRUCCION from GDB to Building table in LADM structure.
        run_etl_model_input_load_data('U_CONSTRUCCION', self._layers[BUILDING_TABLE][LAYER], BUILDING_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data R_CONSTRUCCION from GDB to Valuation Building table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "Loading data to {} table...".format(VALUATION_BUILDING_TABLE)))
        run_etl_model_input_load_data('R_CONSTRUCCION', self._layers[VALUATION_BUILDING_TABLE][LAYER], VALUATION_BUILDING_TABLE, self.qgis_utils)
        create_virtual_field(self._layers[VALUATION_BUILDING_TABLE][LAYER], 'identificador', '$id')
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data R_CONSTRUCCION from GDB to Valuation Building table in LADM structure.
        run_etl_model_input_load_data('U_CONSTRUCCION', self._layers[VALUATION_BUILDING_TABLE][LAYER], VALUATION_BUILDING_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #Select layers to make the join.
        uunidad = QgsProject.instance().mapLayersByName('U_UNIDAD')[0]
        runidad = QgsProject.instance().mapLayersByName('R_UNIDAD')[0]
        #Generate join between U_Unidad GDB and Building table in LADM structure.
        join_layers(uunidad, self._layers[BUILDING_TABLE][LAYER], CODIGO_R1_GDB, 'etiqueta')
        #Generate join between R_Unidad GDB and Building table in LADM structure.
        join_layers(runidad, self._layers[BUILDING_TABLE][LAYER], CODIGO_R1_GDB, 'etiqueta')
        #Fix geometries.
        uunidad_filter = fix_spatial_layer(uunidad)
        runidad_filter = fix_spatial_layer(runidad)
        #Filter by expresion , the result of the process.
        uunidad_filter = extract_by_expresion(uunidad_filter, "construccion_oficial_t_id != 'NULL'")
        runidad_filter = extract_by_expresion(runidad_filter, "construccion_oficial_t_id != 'NULL'")

        #This section of code allow import data uunidad_filter from the previous process to Valuation Building unit table in LADM structure. 
        self.txt_log.setText(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "Loading data to {} table...".format(VALUATION_BUILDING_UNIT_TABLE)))
        run_etl_model_input_load_data(uunidad_filter, self._layers[VALUATION_BUILDING_UNIT_TABLE][LAYER], VALUATION_BUILDING_UNIT_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data runidad_filter from the previous process to Valuation Building unit table in LADM structure. 
        run_etl_model_input_load_data(runidad_filter, self._layers[VALUATION_BUILDING_UNIT_TABLE][LAYER], VALUATION_BUILDING_UNIT_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data uunidad_filter from the previous process to Building unit table in LADM structure. 
        self.txt_log.setText(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "Loading data to {} table...".format(BUILDING_UNIT_TABLE)))
        run_etl_model_input_load_data(uunidad_filter, self._layers[BUILDING_UNIT_TABLE][LAYER], BUILDING_UNIT_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data runidad_filter from the previous process to Building unit table in LADM structure. 
        run_etl_model_input_load_data(runidad_filter, self._layers[BUILDING_UNIT_TABLE][LAYER], BUILDING_UNIT_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)
        
        #Join between Building unit table and Valuation Building Unit Table in LADM structure.
        join_layers(self._layers[BUILDING_UNIT_TABLE][LAYER], 
                        self._layers[VALUATION_BUILDING_UNIT_TABLE][LAYER], 'area_construida', 'puntuacion')
        self.txt_log.setText(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "Loading data to {} table...".format(AVALUOUNIDADCONSTRUCCION_TABLE)))
        #This section of code allow import data Building unit table from LADM structure to Valuation Building unit table in LADM structure.
        run_etl_model_input_load_data(self._layers[BUILDING_UNIT_TABLE][LAYER], self._layers[AVALUOUNIDADCONSTRUCCION_TABLE][LAYER],
                                                                 AVALUOUNIDADCONSTRUCCION_TABLE, self.qgis_utils)                
        step += 1
        self.progress.setValue(step/steps * 100)

        #Join between Building unit table and Valuation Building Table in LADM structure.
        join_layers(self._layers[BUILDING_TABLE][LAYER], 
                        self._layers[VALUATION_BUILDING_TABLE][LAYER], 'avaluo_construccion', 'identificador')
        self.txt_log.setText(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "Loading data to {} table...".format(FDC_VALUATION_BUILDING_CONNECTION)))
        #This section of code allow import data Building unit table from LADM structure to Valuation Building connection table in LADM structure
        run_etl_model_input_load_data(self._layers[BUILDING_TABLE][LAYER], self._layers[FDC_VALUATION_BUILDING_CONNECTION][LAYER],
                                                                 FDC_VALUATION_BUILDING_CONNECTION, self.qgis_utils) 
        delete_virtual_field(self._layers[VALUATION_BUILDING_TABLE][LAYER], 'identificador')
        step += 1
        self.progress.setValue(step/steps * 100)

        #Fix and  extract by expresion the data who if Convencional type.
        layer_filter = fix_spatial_layer(self._layers[VALUATION_BUILDING_UNIT_TABLE][LAYER])
        layer_filter.setSubsetString("construccion_tipo = 'Convencional'")
        #This section of code allow import data layer_filter from the previous process to Valuation Building unit qualification conventional table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "Loading data to {} table...".format(VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE)))
        run_etl_model_input_load_data(layer_filter, self._layers[VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE][LAYER], VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #Fix and  extract by expresion the data who if No Convencional type.
        layer_filter = fix_spatial_layer(self._layers[VALUATION_BUILDING_UNIT_TABLE][LAYER])
        layer_filter.setSubsetString("construccion_tipo = 'noConvencional'")
        #This section of code allow import data layer_filter from the previous process to Valuation Building unit qualification no conventional table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "Loading data to {} table...".format(VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE)))
        run_etl_model_input_load_data(layer_filter, self._layers[VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE][LAYER], VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        unomen = QgsProject.instance().mapLayersByName('U_NOMENCLATURA_DOMICILIARIA')[0]
        rnomen = QgsProject.instance().mapLayersByName('R_NOMENCLATURA_DOMICILIARIA')[0]

        #This section of code allow import data U_NOMENCLATURA_DOMICILIARIA from GDB to Building table in LADM structure.
        self.txt_log.setText(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "Loading data to {} table...".format(EXTADDRESS_TABLE)))
        run_etl_model_input_load_data(get_directions(unomen, self._layers[BUILDING_TABLE][LAYER]), self._layers[EXTADDRESS_TABLE][LAYER], EXTADDRESS_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import data R_NOMENCLATURA_DOMICILIARIA from GDB to Building table in LADM structure.
        run_etl_model_input_load_data(get_directions(rnomen, self._layers[PLOT_TABLE][LAYER]), self._layers[EXTADDRESS_TABLE][LAYER], EXTADDRESS_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import join between building table and parcel table to Uebaunit table in LADM structure.
        join_layers(self._layers[PARCEL_TABLE][LAYER], self._layers[BUILDING_TABLE][LAYER], 'numero_predial', 'su_local_id')
        vlayer = extract_by_expresion(self._layers[PARCEL_TABLE][LAYER], "construccion_oficial_t_id != 'NULL'")
        self.txt_log.setText(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "Loading data to {} table...".format(UEBAUNIT_TABLE_BUILDING_FIELD)))
        run_etl_model_input_load_data(vlayer, self._layers[UEBAUNIT_TABLE][LAYER], UEBAUNIT_TABLE_BUILDING_FIELD, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import join between plot table and parcel table to Uebaunit table in LADM structure.
        join_layers(self._layers[PARCEL_TABLE][LAYER], self._layers[PLOT_TABLE][LAYER], 'numero_predial', 'etiqueta')
        vlayer = extract_by_expresion(self._layers[PARCEL_TABLE][LAYER], "terreno_oficial_t_id != 'NULL'")
        self.txt_log.setText(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "Loading data to {} table...".format(UEBAUNIT_TABLE_PLOT_FIELD)))
        run_etl_model_input_load_data(vlayer, self._layers[UEBAUNIT_TABLE][LAYER], UEBAUNIT_TABLE_PLOT_FIELD, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        #This section of code allow import join between building unit table and parcel table to Uebaunit table in LADM structure.
        join_layers(self._layers[PARCEL_TABLE][LAYER], self._layers[BUILDING_UNIT_TABLE][LAYER], 'numero_predial', 'su_local_id')
        vlayer = extract_by_expresion(self._layers[PARCEL_TABLE][LAYER], "unidadconstruccion_oficial_t_id != 'NULL'")
        self.txt_log.setText(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "Loading data to {} table...".format(UEBAUNIT_TABLE_PLOT_FIELD)))
        run_etl_model_input_load_data(vlayer, self._layers[UEBAUNIT_TABLE][LAYER], UEBAUNIT_TABLE_PLOT_FIELD, self.qgis_utils) 
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
        dlg = OfficialDataSettingsDialog(qgis_utils=self.qgis_utils, conn_manager=self.conn_manager)
        dlg.set_action_type(EnumTestLevel.DB_SCHEMA)
        dlg.official_db_connection_changed.connect(self.conn_manager.official_db_connection_changed)
        if dlg.exec_():
            self.update_connection_info()

    def update_connection_info(self):
        self._db = self.conn_manager.get_db_connector_from_source(db_source=OFFICIAL_DB_SOURCE)
        db_description = self._db.get_description_conn_string()
        if db_description:
            self.db_connect_label.setText(db_description)
            self.db_connect_label.setToolTip(self._db.get_display_conn_string())
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.db_connect_label.setText(QCoreApplication.translate("InputLoadFieldDataCaptureDialog", "The database is not defined!"))
            self.db_connect_label.setToolTip('')
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

    def ladm_tables_feature_count_before(self):
        layers_name_summary = [FDC_NEIGHBOURHOOD, BUILDING_TABLE, RIGHT_TABLE, EXTADDRESS_TABLE, ADMINISTRATIVE_SOURCE_TABLE, COL_PARTY_TABLE, 
                            FDC_VILLAGE, PARCEL_TABLE, PLOT_TABLE, BUILDING_UNIT_TABLE]

        features_count_before = {}

        for layer in layers_name_summary:
            features_count_before[layer] = self._layers[layer][LAYER].featureCount()

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
            self.summary += QCoreApplication.translate("InputLoadFieldDataCaptureDialog",
                        "<b>{count}</b> records loaded into table <b>{table}</b><br/>").format(
                            count=layer.featureCount() - ladm_count_before[name],
                            table=layer.name())

        self.txt_log.setText(self.summary)

    def create_model_into_database(self):
        get_import_schema_dialog = DialogImportSchema(self.iface, self.qgis_utils, self.conn_manager, db_source=OFFICIAL_DB_SOURCE)
        for modelname in DEFAULT_MODEL_NAMES_CHECKED:
            item = get_import_schema_dialog.import_models_list_widget.findItems(modelname, Qt.MatchExactly)
            item[0].setCheckState(Qt.Checked)
        
        get_import_schema_dialog.accepted()

        if not self._db.test_connection(test_level=EnumTestLevel.LADM)[0]:
            dlg = LogExcelDialog(self.qgis_utils, get_import_schema_dialog.txtStdout.toHtml())
            dlg.buttonBox.button(QDialogButtonBox.Save).setVisible(False)
            dlg.setFixedSize(dlg.size()) 
            dlg.setWindowTitle(QCoreApplication.translate("InputLoadFieldDataCaptureDialog","Log error structure LADM"))
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
                layer = self._layers[layer][LAYER]
            joins_info = layer.vectorJoins()
            for join_info in joins_info:
                layer.removeJoin(join_info.joinLayerId())    

    def remove_layer(self, layer_name):
        layer = QgsProject.instance().mapLayersByName(layer_name)
        print (QgsProject.instance().mapLayersByName(layer_name))
        if layer != []:
            QgsProject.instance().removeMapLayer(layer[0].id())

    def remove_group(self, group_name):
        root = QgsProject.instance().layerTreeRoot()
        group = root.findGroup(group_name)
        if group is not None:
            for child in group.children():
                QgsProject.instance().removeMapLayer(child.layerId())
            root.removeChildNode(group)

    def manage_process_load_data(self):
        """
        Workflow for loading official data
        """
        # We need a temporary cache for official relations. Store current cache if any, and build a new cache...
        cached_layers, cached_relations, cached_bags_of_enum = self.qgis_utils._layers, self.qgis_utils._relations, self.qgis_utils._bags_of_enum
        self.qgis_utils.cache_layers_and_relations(self._db, True)

        self.set_gui_enabled(False)
        is_loaded = self.load_data_for_etl()

        if is_loaded:
            features_count_before = self.ladm_tables_feature_count_before()
            #self.mapping_fields_r1()
            #self.mapping_fields_gbb()
            #self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            #self.show_log_data(features_count_before)

            # When finish the etl process, we need remove all joins in the layers, so we delete all joins in r1, gdb and LADM_COL layers 
            #self.clean_layer_joins(self.gdb_layer_list)
            #self.clean_layer_joins([self.layer_r1])
            #self.clean_layer_joins(self._layers)
        else:
            self.set_gui_enabled(True)

        # No one else needs the official cache, so go back to initial state
        self.qgis_utils._layers, self.qgis_utils._relations, self.qgis_utils._bags_of_enum = cached_layers, cached_relations, cached_bags_of_enum