# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-02-06
        git sha              : :%H$
        copyright            : (C) 2019 by Jhon Galindo (Incige SAS)
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
import glob
import processing

from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.PyQt.QtCore import (Qt,
                              QSettings,
                              QCoreApplication)

from qgis.PyQt.QtGui import (QStandardItemModel,
                             QStandardItem)

from qgis.core import (Qgis,
                       QgsProject,
                       QgsWkbTypes,
                       QgsVectorLayer,
                       QgsVectorLayerJoinInfo)

from ...config.general_config import (DEFAULT_HIDDEN_MODELS,
                                      SETTINGS_CONNECTION_TAB_INDEX,
                                      SETTINGS_MODELS_TAB_INDEX)

from ...config.enums import EnumDbActionType
from ...utils.qt_utils import OverrideCursor
from ...utils import get_ui_class
from ...gui.dialogs.dlg_settings import SettingsDialog

from asistente_ladm_col.utils.qt_utils import (make_file_selector,
                                               make_folder_selector)
from asistente_ladm_col.config.table_mapping_config import Names
from asistente_ladm_col.config.general_config import LAYER

DIALOG_LOG_EXCEL_UI = get_ui_class('dialogs/dlg_etl_cobol.ui')


class EtlCobolDialog(QDialog, DIALOG_LOG_EXCEL_UI):
    def __init__(self, qgis_utils, db, conn_manager, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.qgis_utils = qgis_utils
        self._db = db
        self.conn_manager = conn_manager
        self.names = Names()
        self.buttonBox.accepted.connect(self.accepted)

        self.btn_browse_connection.clicked.connect(self.show_settings)
        self.update_connection_info()

        self._layers = dict()
        self.initialize_layers()

        self.progress.setVisible(False)
        self.restore_settings()

        self.btn_browse_file_blo.clicked.connect(
            make_file_selector(self.txt_file_path_blo, QCoreApplication.translate("DialogExportData",
                        "Select the .lis file with Cobol data "), 
                        QCoreApplication.translate("DialogExportData", 'lis File (*.lis)')))

        self.btn_browse_file_uni.clicked.connect(
            make_file_selector(self.txt_file_path_uni, QCoreApplication.translate("DialogExportData",
                        "Select the .lis file with Cobol data "), 
                        QCoreApplication.translate("DialogExportData", 'lis File (*.lis)')))

        self.btn_browse_file_ter.clicked.connect(
            make_file_selector(self.txt_file_path_ter, QCoreApplication.translate("DialogExportData",
                        "Select the .lis file with Cobol data "), 
                        QCoreApplication.translate("DialogExportData", 'lis File (*.lis)')))

        self.btn_browse_file_pro.clicked.connect(
            make_file_selector(self.txt_file_path_pro, QCoreApplication.translate("DialogExportData",
                        "Select the .lis file with Cobol data "), 
                        QCoreApplication.translate("DialogExportData", 'lis File (*.lis)')))

        self.btn_browse_file_gdb.clicked.connect(
                make_folder_selector(self.txt_file_path_gdb, title=QCoreApplication.translate(
                'SettingsDialog', 'Open Folder with GDB'), parent=None))

    def initialize_layers(self):
        self._layers = {
            self.names.GC_PARCEL_T: {'name': self.names.GC_PARCEL_T, 'geometry': None, LAYER: None},
            self.names.GC_OWNER_T: {'name': self.names.GC_OWNER_T, 'geometry': None, LAYER: None},
            self.names.GC_ADDRESS_T: {'name': self.names.GC_ADDRESS_T, 'geometry': QgsWkbTypes.LineGeometry, LAYER: None},
            self.names.GC_BUILDING_UNIT_T: {'name': self.names.GC_BUILDING_UNIT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.GC_BUILDING_T: {'name': self.names.GC_BUILDING_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.GC_PLOT_T: {'name': self.names.GC_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.GC_RURAL_DIVISION_T: {'name': self.names.GC_RURAL_DIVISION_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.GC_URBAN_SECTOR_T: {'name': self.names.GC_URBAN_SECTOR_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.GC_RURAL_SECTOR_T: {'name': self.names.GC_RURAL_SECTOR_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.GC_PERIMETER_T: {'name': self.names.GC_PERIMETER_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.GC_BLOCK_T: {'name': self.names.GC_BLOCK_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.GC_NEIGHBOURHOOD_T: {'name': self.names.GC_NEIGHBOURHOOD_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.GC_COMMISSION_BUILDING_T: {'name': self.names.GC_COMMISSION_BUILDING_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.GC_COMMISSION_PLOT_T: {'name': self.names.GC_COMMISSION_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.GC_COMMISSION_BUILDING_UNIT_T: {'name': self.names.GC_COMMISSION_BUILDING_UNIT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
        }

    def accepted(self):
        self.save_settings()

        if self._db.test_connection()[0]:
            reply = QMessageBox.question(self,
                QCoreApplication.translate("EtlCobolDialog", "Warning"),
                QCoreApplication.translate("EtlCobolDialog","The schema <i>{schema}</i> already has a valid LADM_COL structure.<br/><br/>If such schema has any data, loading data into it might cause invalid data.<br/><br/>Do you still want to continue?".format(schema=self._db.schema)),
                QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                with OverrideCursor(Qt.WaitCursor):
                    self.load_lis_files()
                    self.load_gdb_files()
                    self.load_model_files(self._layers)
                    self.run_model_etl_cobol()
        else:
            with OverrideCursor(Qt.WaitCursor):
                self.create_model_into_database()
                if self._db.test_connection()[0]:
                    self.remove_group('GDB')
                    self.manage_process_load_data()

    def show_settings(self):
        dlg = SettingsDialog(qgis_utils=self.qgis_utils, conn_manager=self.conn_manager)

        # Connect signals (DBUtils, QgisUtils)
        dlg.db_connection_changed.connect(self.db_connection_changed)
        dlg.db_connection_changed.connect(self.qgis_utils.cache_layers_and_relations)

        # We only need those tabs related to Model Baker/ili2db operations
        for i in reversed(range(dlg.tabWidget.count())):
            if i not in [SETTINGS_CONNECTION_TAB_INDEX, SETTINGS_MODELS_TAB_INDEX]:
                dlg.tabWidget.removeTab(i)

        dlg.set_action_type(EnumDbActionType.EXPORT)

        if dlg.exec_():
            self._db = dlg.get_db_connection()
            self.update_connection_info()

    def db_connection_changed(self, db, ladm_col_db):
        self._db_was_changed = True

    def update_connection_info(self):
        db_description = self._db.get_description_conn_string()
        if db_description:
            self.db_connect_label.setText(db_description)
            self.db_connect_label.setToolTip(self._db.get_display_conn_string())
        else:
            self.db_connect_label.setText(
                QCoreApplication.translate("DialogExportData", "The database is not defined!"))
            self.db_connect_label.setToolTip('')

    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/etl_cobol/blo_path', self.txt_file_path_blo.text())
        settings.setValue('Asistente-LADM_COL/etl_cobol/uni_path', self.txt_file_path_uni.text())
        settings.setValue('Asistente-LADM_COL/etl_cobol/ter_path', self.txt_file_path_ter.text())
        settings.setValue('Asistente-LADM_COL/etl_cobol/pro_path', self.txt_file_path_pro.text())
        settings.setValue('Asistente-LADM_COL/etl_cobol/gdb_path', self.txt_file_path_gdb.text())

    def restore_settings(self):
        settings = QSettings()
        self.txt_file_path_blo.setText(settings.value('Asistente-LADM_COL/etl_cobol/blo_path', ''))
        self.txt_file_path_uni.setText(settings.value('Asistente-LADM_COL/etl_cobol/uni_path', ''))
        self.txt_file_path_ter.setText(settings.value('Asistente-LADM_COL/etl_cobol/ter_path', ''))
        self.txt_file_path_pro.setText(settings.value('Asistente-LADM_COL/etl_cobol/pro_path', ''))
        self.txt_file_path_gdb.setText(settings.value('Asistente-LADM_COL/etl_cobol/gdb_path', ''))

    def load_lis_files(self):
        self.lis_paths = {
            'blo':self.txt_file_path_blo.text(), 
            'uni':self.txt_file_path_uni.text(), 
            'ter':self.txt_file_path_ter.text(), 
            'pro':self.txt_file_path_pro.text()
            } 

        root = QgsProject.instance().layerTreeRoot()
        lis_group = root.addGroup("Lis_Supplies")

        for name in self.lis_paths:
            uri = 'file:///{}?type=csv&delimiter=;&detectTypes=yes&geomType=none&subsetIndex=no&watchFile=no'.format(self.lis_paths[name])
            layer = QgsVectorLayer(uri, name, 'delimitedtext')
            if layer.isValid():
                self.lis_paths[name] = layer
                QgsProject.instance().addMapLayer(layer, False)
                lis_group.addLayer(layer)

    def load_gdb_files(self):
        self.gdb_paths = {}

        required_layers = ['R_TERRENO','U_TERRENO','R_SECTOR','U_SECTOR','R_VEREDA','U_MANZANA','U_BARRIO'
                            ,'R_CONSTRUCCION','U_CONSTRUCCION','U_UNIDAD','R_UNIDAD','U_NOMENCLATURA_DOMICILIARIA',
                            'R_NOMENCLATURA_DOMICILIARIA', 'U_PERIMETRO']

        gdb_path = self.txt_file_path_gdb.text()
        layer = QgsVectorLayer(gdb_path, 'layer name', 'ogr')
        sublayers = layer.dataProvider().subLayers()

        root = QgsProject.instance().layerTreeRoot()
        gdb_group = root.addGroup("GDB_Supplies")

        for data in sublayers:
            if data.split('!!::!!')[1] in required_layers:    
                layer = QgsVectorLayer(gdb_path + '|layername=' + data.split('!!::!!')[1], data.split('!!::!!')[1], 'ogr')
                self.gdb_paths[data.split('!!::!!')[1]] = layer
                QgsProject.instance().addMapLayer(layer, False)
                gdb_group.addLayer(layer)

    def load_model_files(self, layers):
        self.qgis_utils.get_layers(self._db, self._layers, load=True)
        if not self._layers:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("DialogExportData",
                                           "'{}' tool has been closed because there was a problem loading the requeries layers.").format(
                    "Input load dialog"),
                Qgis.Warning)
            return False

    def run_model_etl_cobol(self):
        processing.run("model:ETL-model-supplies", 
            {'barrio': self.gdb_paths['U_BARRIO'],
            'gcbarrio': self._layers[self.names.GC_NEIGHBOURHOOD_T][LAYER],
            'gccomisionconstruccion': self._layers[self.names.GC_COMMISSION_BUILDING_T][LAYER],
            'gccomisionterreno': self._layers[self.names.GC_COMMISSION_PLOT_T][LAYER],
            'gcconstruccion': self._layers[self.names.GC_BUILDING_T][LAYER],
            'gcdireccion': self._layers[self.names.GC_ADDRESS_T][LAYER],
            'gcmanzana': self._layers[self.names.GC_BLOCK_T][LAYER],
            'gcperimetro': self._layers[self.names.GC_PERIMETER_T][LAYER],
            'gcpropietario': self._layers[self.names.GC_OWNER_T][LAYER],
            'gcsector': self._layers[self.names.GC_RURAL_SECTOR_T][LAYER],
            'gcsectorurbano': self._layers[self.names.GC_URBAN_SECTOR_T][LAYER],
            'gcterreno': self._layers[self.names.GC_PLOT_T][LAYER],
            'gcunidad': self._layers[self.names.GC_BUILDING_UNIT_T][LAYER],
            'gcunidadconstruccioncomision': self._layers[self.names.GC_COMMISSION_BUILDING_UNIT_T][LAYER],
            'gcvereda': self._layers[self.names.GC_RURAL_DIVISION_T][LAYER],
            'inputblo': self.lis_paths['blo'],
            'inputconstruccion': self.gdb_paths['R_CONSTRUCCION'],
            'inputmanzana': self.gdb_paths['U_MANZANA'],
            'inputperimetro': self.gdb_paths['U_PERIMETRO'],
            'inputpro': self.lis_paths['pro'],
            'inputrunidad': self.gdb_paths['R_UNIDAD'],
            'inputsector': self.gdb_paths['R_SECTOR'],
            'inputter': self.lis_paths['ter'],
            'inputterreno': self.gdb_paths['R_TERRENO'],
            'inputuconstruccion': self.gdb_paths['U_CONSTRUCCION'],
            'inputuni': self.lis_paths['uni'],
            'inputusector': self.gdb_paths['U_SECTOR'],
            'inpututerreno': self.gdb_paths['U_TERRENO'],
            'inputuunidad': self.gdb_paths['U_UNIDAD'],
            'inputvereda': self.gdb_paths['R_VEREDA'],
            'ouputlayer': self._layers[self.names.GC_PARCEL_T][LAYER],
            'rnomenclatura': self.gdb_paths['R_NOMENCLATURA_DOMICILIARIA'],
            'unomenclatura': self.gdb_paths['U_NOMENCLATURA_DOMICILIARIA']})
