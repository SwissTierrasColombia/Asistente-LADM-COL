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

from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtCore import (Qt,
                              QSettings,
                              QCoreApplication)

from qgis.core import (QgsProject,
                       QgsVectorLayer,
                       QgsVectorLayerJoinInfo)

from ...utils.qt_utils import OverrideCursor
from ...utils import get_ui_class

from asistente_ladm_col.utils.qt_utils import (make_file_selector,
                                               make_folder_selector)

DIALOG_LOG_EXCEL_UI = get_ui_class('dialogs/dlg_etl_cobol.ui')


class EtlCobolDialog(QDialog, DIALOG_LOG_EXCEL_UI):
    def __init__(self, qgis_utils, db, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.qgis_utils = qgis_utils
        self._db = db
        self.buttonBox.accepted.connect(self.accepted)
        self.progress.setVisible(False)
        self.restore_settings()

        self.btn_browse_file_blo.clicked.connect(
            make_file_selector(self.txt_file_path_blo, QCoreApplication.translate("InputLoadFieldDataCaptureDialog",
                        "Select the .lis file with Cobol data "), 
                        QCoreApplication.translate("InputLoadFieldDataCaptureDialog", 'lis File (*.lis)')))

        self.btn_browse_file_uni.clicked.connect(
            make_file_selector(self.txt_file_path_uni, QCoreApplication.translate("InputLoadFieldDataCaptureDialog",
                        "Select the .lis file with Cobol data "), 
                        QCoreApplication.translate("InputLoadFieldDataCaptureDialog", 'lis File (*.lis)')))

        self.btn_browse_file_ter.clicked.connect(
            make_file_selector(self.txt_file_path_ter, QCoreApplication.translate("InputLoadFieldDataCaptureDialog",
                        "Select the .lis file with Cobol data "), 
                        QCoreApplication.translate("InputLoadFieldDataCaptureDialog", 'lis File (*.lis)')))

        self.btn_browse_file_pro.clicked.connect(
            make_file_selector(self.txt_file_path_pro, QCoreApplication.translate("InputLoadFieldDataCaptureDialog",
                        "Select the .lis file with Cobol data "), 
                        QCoreApplication.translate("InputLoadFieldDataCaptureDialog", 'lis File (*.lis)')))

        self.btn_browse_file_gdb.clicked.connect(
                make_folder_selector(self.txt_file_path_gdb, title=QCoreApplication.translate(
                'SettingsDialog', 'Open Folder with GDB'), parent=None))

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
        else:
            with OverrideCursor(Qt.WaitCursor):
                self.create_model_into_database()
                if self._db.test_connection()[0]:
                    self.remove_group('GDB')
                    self.manage_process_load_data()

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