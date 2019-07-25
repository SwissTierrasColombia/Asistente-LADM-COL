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

from ..gui.qgis_model_baker.dlg_import_schema import DialogImportSchema
from ..gui.log_excel_dialog import LogExcelDialog

from qgis.PyQt.QtCore import QVariant

from asistente_ladm_col.utils.qt_utils import (make_file_selector,
                                               make_folder_selector)

from ..utils.qfield_utils import (run_etl_model_input_load_data,
                                  join_layers,
                                  create_column,
                                  fix_polygon_layers,
                                  get_directions)

from qgis.core import (QgsProject,
                       QgsField,
                       QgsVectorLayer,
                       QgsVectorLayerJoinInfo)

from ..config.table_mapping_config import (FDC_PARCEL,
                                           FDC_PARTY,
                                           FDC_RIGHT,
                                           FDC_ADMINISTRATIVE_SOURCE,
                                           FDC_RRRSOURCE,
                                           FDC_UEBAUNIT,
                                           FDC_UEBAUNIT_BUILDING, 
                                           FDC_UEBAUNIT_PLOT, 
                                           FDC_UEBAUNIT_BUILDING_UNIT,
                                           FDC_PLOT, 
                                           FDC_SECTOR,
                                           FDC_VILLAGE,
                                           FDC_BLOCK,
                                           FDC_NEIGHBOURHOOD,
                                           FDC_BUILDING,
                                           FDC_VALUATION_BUILDING,
                                           FDC_BUILDING_UNIT_VALUATION_TABLE,
                                           FDC_BUILDING_UNIT_CADASTRE_TABLE,
                                           FDC_VALUATION_UNIT_BUILDING_CONNECTION,
                                           FDC_VALUATION_BUILDING_CONNECTION,
                                           FDC_EXTADDRESS,
                                           FDC_QUALIFICATION_CONVENTIONAL,
                                           FDC_QUALIFICATION_NO_CONVENTIONAL)

from qgis.PyQt.QtCore import (Qt,
                              QSettings,
                              QCoreApplication,
                              QFile)

from qgis.PyQt.QtWidgets import (QDialog,
                                 QFileDialog,
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

from ..config.general_config import DEFAULT_MODEL_NAMES_CHECKED

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
        self.create_model_into_database()
        self.load_r1()
        self.mapping_fields_r1()
        self.load_gdb()
        self.mapping_fields_gbb()
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.show_log_data()

    def load_r1(self):
        self.progress.setVisible(True)
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading R1 tables..."))
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
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading GDB tables..."))
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
            FDC_SECTOR: {'name': FDC_SECTOR, 'geometry': None},
            FDC_VILLAGE: {'name': FDC_VILLAGE, 'geometry': None},
            FDC_NEIGHBOURHOOD: {'name': FDC_NEIGHBOURHOOD, 'geometry': None},
            FDC_BUILDING: {'name': FDC_BUILDING, 'geometry': QgsWkbTypes.PolygonGeometry},
            FDC_VALUATION_BUILDING: {'name': FDC_VALUATION_BUILDING, 'geometry': None},
            FDC_BUILDING_UNIT_VALUATION_TABLE: {'name': FDC_BUILDING_UNIT_VALUATION_TABLE, 'geometry': None},
            FDC_BUILDING_UNIT_CADASTRE_TABLE: {'name': FDC_BUILDING_UNIT_CADASTRE_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            FDC_VALUATION_UNIT_BUILDING_CONNECTION: {'name': FDC_VALUATION_UNIT_BUILDING_CONNECTION, 'geometry': None},
            FDC_VALUATION_BUILDING_CONNECTION: {'name': FDC_VALUATION_BUILDING_CONNECTION, 'geometry': None},
            FDC_QUALIFICATION_CONVENTIONAL: {'name': FDC_QUALIFICATION_CONVENTIONAL, 'geometry': None},
            FDC_QUALIFICATION_NO_CONVENTIONAL: {'name': FDC_QUALIFICATION_NO_CONVENTIONAL, 'geometry': None},
            FDC_EXTADDRESS: {'name': FDC_EXTADDRESS, 'geometry': QgsWkbTypes.PointGeometry}
        }, load=True)

    def mapping_fields_r1(self):
        steps = 29
        step = 0

        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(FDC_PARCEL)))
        query = "select * from {} group by NoPredial&nogeometry".format(self.layer_r1.name())
        input_data = QgsVectorLayer( "?query={}".format(query), "vlayer", "virtual")
        create_column(self.res_layers[FDC_PARCEL], 'Codigo')
        run_etl_model_input_load_data(input_data, self.res_layers[FDC_PARCEL], FDC_PARCEL, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(FDC_PARTY)))
        create_column(self.res_layers[FDC_PARTY], 'Codigo')
        run_etl_model_input_load_data(self.layer_r1, self.res_layers[FDC_PARTY], FDC_PARTY, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(FDC_RIGHT)))
        join_layers(self.res_layers[FDC_PARTY], self.res_layers[FDC_PARCEL], 'Codigo', 'Codigo')
        run_etl_model_input_load_data(self.res_layers[FDC_PARTY], self.res_layers[FDC_RIGHT], FDC_RIGHT, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(FDC_ADMINISTRATIVE_SOURCE)))
        run_etl_model_input_load_data(self.res_layers[FDC_RIGHT], self.res_layers[FDC_ADMINISTRATIVE_SOURCE], FDC_ADMINISTRATIVE_SOURCE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)        
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(FDC_RRRSOURCE)))
        run_etl_model_input_load_data(self.res_layers[FDC_ADMINISTRATIVE_SOURCE], self.res_layers[FDC_RRRSOURCE], FDC_RRRSOURCE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

    def mapping_fields_gbb(self):
        steps = 29
        step = 5
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(FDC_PLOT)))
        run_etl_model_input_load_data('R_TERRENO', self.res_layers_gdb[FDC_PLOT], FDC_PLOT, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)
        run_etl_model_input_load_data('U_TERRENO', self.res_layers_gdb[FDC_PLOT], FDC_PLOT, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(FDC_SECTOR)))
        run_etl_model_input_load_data('R_SECTOR', self.res_layers_gdb[FDC_SECTOR], FDC_SECTOR, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)
        run_etl_model_input_load_data('U_SECTOR', self.res_layers_gdb[FDC_SECTOR], FDC_SECTOR, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(FDC_VILLAGE)))
        run_etl_model_input_load_data('R_VEREDA', self.res_layers_gdb[FDC_VILLAGE], FDC_VILLAGE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)
        run_etl_model_input_load_data('U_MANZANA', self.res_layers_gdb[FDC_VILLAGE], FDC_BLOCK, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(FDC_NEIGHBOURHOOD)))
        run_etl_model_input_load_data('U_BARRIO', self.res_layers_gdb[FDC_NEIGHBOURHOOD], FDC_NEIGHBOURHOOD, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        create_column(self.res_layers_gdb[FDC_BUILDING], 'Codigo')
        create_column(self.res_layers_gdb[FDC_BUILDING], 'identificador')
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(FDC_BUILDING)))
        run_etl_model_input_load_data('R_CONSTRUCCION', self.res_layers_gdb[FDC_BUILDING], FDC_BUILDING, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)
        run_etl_model_input_load_data('U_CONSTRUCCION', self.res_layers_gdb[FDC_BUILDING], FDC_BUILDING, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)
        create_column(self.res_layers_gdb[FDC_VALUATION_BUILDING], 'Codigo')
        create_column(self.res_layers_gdb[FDC_VALUATION_BUILDING], 'identificador')
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(FDC_VALUATION_BUILDING)))
        run_etl_model_input_load_data('R_CONSTRUCCION', self.res_layers_gdb[FDC_VALUATION_BUILDING], FDC_VALUATION_BUILDING, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)
        run_etl_model_input_load_data('U_CONSTRUCCION', self.res_layers_gdb[FDC_VALUATION_BUILDING], FDC_VALUATION_BUILDING, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        uunidad = QgsProject.instance().mapLayersByName('U_UNIDAD')[0]
        runidad = QgsProject.instance().mapLayersByName('R_UNIDAD')[0]

        create_column(self.res_layers_gdb[FDC_BUILDING_UNIT_VALUATION_TABLE], 'identificador')
        join_layers(uunidad, self.res_layers_gdb[FDC_BUILDING], 'Codigo', 'Codigo')
        join_layers(runidad, self.res_layers_gdb[FDC_BUILDING], 'Codigo', 'Codigo')
        uunidad_filter = fix_polygon_layers(uunidad)
        runidad_filter = fix_polygon_layers(runidad)
        uunidad_filter.setSubsetString("construccion_t_id != 'NULL'")
        runidad_filter.setSubsetString("construccion_t_id != 'NULL'")
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(FDC_BUILDING_UNIT_VALUATION_TABLE)))
        run_etl_model_input_load_data(uunidad_filter, self.res_layers_gdb[FDC_BUILDING_UNIT_VALUATION_TABLE], FDC_BUILDING_UNIT_VALUATION_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)
        run_etl_model_input_load_data(runidad_filter, self.res_layers_gdb[FDC_BUILDING_UNIT_VALUATION_TABLE], FDC_BUILDING_UNIT_VALUATION_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        create_column(self.res_layers_gdb[FDC_BUILDING_UNIT_CADASTRE_TABLE], 'Codigo')
        create_column(self.res_layers_gdb[FDC_BUILDING_UNIT_CADASTRE_TABLE], 'identificador')
        join_layers(uunidad, self.res_layers_gdb[FDC_BUILDING], 'Codigo', 'Codigo')
        join_layers(runidad, self.res_layers_gdb[FDC_BUILDING], 'Codigo', 'Codigo')
        uunidad_filter = fix_polygon_layers(uunidad)
        runidad_filter = fix_polygon_layers(runidad)
        uunidad_filter.setSubsetString("construccion_t_id != 'NULL'")
        runidad_filter.setSubsetString("construccion_t_id != 'NULL'")
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(FDC_BUILDING_UNIT_CADASTRE_TABLE)))
        run_etl_model_input_load_data(uunidad_filter, self.res_layers_gdb[FDC_BUILDING_UNIT_CADASTRE_TABLE], FDC_BUILDING_UNIT_CADASTRE_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)
        run_etl_model_input_load_data(runidad_filter, self.res_layers_gdb[FDC_BUILDING_UNIT_CADASTRE_TABLE], FDC_BUILDING_UNIT_CADASTRE_TABLE, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        join_layers(self.res_layers_gdb[FDC_BUILDING_UNIT_CADASTRE_TABLE], 
                        self.res_layers_gdb[FDC_BUILDING_UNIT_VALUATION_TABLE], 'identificador', 'identificador')
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(FDC_VALUATION_UNIT_BUILDING_CONNECTION)))
        run_etl_model_input_load_data(self.res_layers_gdb[FDC_BUILDING_UNIT_CADASTRE_TABLE], self.res_layers_gdb[FDC_VALUATION_UNIT_BUILDING_CONNECTION],
                                                                 FDC_VALUATION_UNIT_BUILDING_CONNECTION, self.qgis_utils)                
        step += 1
        self.progress.setValue(step/steps * 100)
        join_layers(self.res_layers_gdb[FDC_BUILDING], 
                        self.res_layers_gdb[FDC_VALUATION_BUILDING], 'identificador', 'identificador')
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(FDC_VALUATION_BUILDING_CONNECTION)))
        run_etl_model_input_load_data(self.res_layers_gdb[FDC_BUILDING], self.res_layers_gdb[FDC_VALUATION_BUILDING_CONNECTION],
                                                                 FDC_VALUATION_BUILDING_CONNECTION, self.qgis_utils) 
        step += 1
        self.progress.setValue(step/steps * 100)

        layer_filter = fix_polygon_layers(self.res_layers_gdb[FDC_BUILDING_UNIT_VALUATION_TABLE])
        layer_filter.setSubsetString("construccion_tipo = 'Convencional'")
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(FDC_QUALIFICATION_CONVENTIONAL)))
        run_etl_model_input_load_data(layer_filter, self.res_layers_gdb[FDC_QUALIFICATION_CONVENTIONAL], FDC_QUALIFICATION_CONVENTIONAL, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)
        layer_filter = fix_polygon_layers(self.res_layers_gdb[FDC_BUILDING_UNIT_VALUATION_TABLE])
        layer_filter.setSubsetString("construccion_tipo = 'noConvencional'")
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(FDC_QUALIFICATION_NO_CONVENTIONAL)))
        run_etl_model_input_load_data(layer_filter, self.res_layers_gdb[FDC_QUALIFICATION_NO_CONVENTIONAL], FDC_QUALIFICATION_NO_CONVENTIONAL, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        unomen = QgsProject.instance().mapLayersByName('U_NOMENCLATURA_DOMICILIARIA')[0]
        rnomen = QgsProject.instance().mapLayersByName('R_NOMENCLATURA_DOMICILIARIA')[0]

        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(FDC_EXTADDRESS)))
        run_etl_model_input_load_data(get_directions(unomen, self.res_layers_gdb[FDC_BUILDING]), self.res_layers_gdb[FDC_EXTADDRESS], FDC_EXTADDRESS, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)
        run_etl_model_input_load_data(get_directions(rnomen, self.res_layers_gdb[FDC_PLOT]), self.res_layers_gdb[FDC_EXTADDRESS], FDC_EXTADDRESS, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)

        join_layers(self.res_layers[FDC_PARCEL], self.res_layers_gdb[FDC_BUILDING], 'Codigo', 'Codigo')
        vlayer = QgsVectorLayer("?query=SELECT * FROM {}&nogeometry".format(FDC_PARCEL), "vlayer", "virtual" )
        vlayer.setSubsetString("construccion_t_id != 'NULL'")
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(FDC_UEBAUNIT_BUILDING)))
        run_etl_model_input_load_data(vlayer, self.res_layers[FDC_UEBAUNIT], FDC_UEBAUNIT_BUILDING, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)
        join_layers(self.res_layers[FDC_PARCEL], self.res_layers_gdb[FDC_PLOT], 'Codigo', 'etiqueta')
        vlayer = QgsVectorLayer("?query=SELECT * FROM {}&nogeometry".format(FDC_PARCEL), "vlayer", "virtual" )
        vlayer.setSubsetString("terreno_t_id != 'NULL'")
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(FDC_UEBAUNIT_PLOT)))
        run_etl_model_input_load_data(vlayer, self.res_layers[FDC_UEBAUNIT], FDC_UEBAUNIT_PLOT, self.qgis_utils)
        step += 1
        self.progress.setValue(step/steps * 100)
        join_layers(self.res_layers[FDC_PARCEL], self.res_layers_gdb[FDC_BUILDING_UNIT_CADASTRE_TABLE], 'Codigo', 'Codigo')
        vlayer = QgsVectorLayer("?query=SELECT * FROM {}&nogeometry".format(FDC_PARCEL), "vlayer", "virtual" )
        vlayer.setSubsetString("unidadconstruccion_t_id != 'NULL'")
        self.txt_log.setText(QCoreApplication.translate("DialogInputLoadFieldDataCapture", "Loading data to {} table...".format(FDC_UEBAUNIT_BUILDING_UNIT)))
        run_etl_model_input_load_data(vlayer, self.res_layers[FDC_UEBAUNIT], FDC_UEBAUNIT_BUILDING_UNIT, self.qgis_utils) 
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
            self.db_connect_label.setText(QCoreApplication.translate("DialogImportSchema", "The database is not defined!"))
            self.db_connect_label.setToolTip('')
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

    def show_log_data(self):
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

        layers_name_summary = [FDC_NEIGHBOURHOOD, FDC_BUILDING, FDC_RIGHT, FDC_EXTADDRESS, FDC_ADMINISTRATIVE_SOURCE, FDC_PARTY, 
                            FDC_VILLAGE, FDC_PARCEL, FDC_PLOT, FDC_BUILDING_UNIT_CADASTRE_TABLE]

        for name in layers_name_summary:
            layer = QgsProject.instance().mapLayersByName(name)[0]
            layer.featureCount()
            self.summary += QCoreApplication.translate("DialogInputLoadFieldDataCapture",
                        "<b>{count}</b> records loaded into table <b>{table}</b><br/>").format(
                            count=layer.featureCount(),table=layer.name())

        self.txt_log.setText(self.summary)

    def create_model_into_database(self):
        resultado = None
        get_import_schema_dialog = DialogImportSchema(self.iface, self._db, self.qgis_utils)
        for modelname in DEFAULT_MODEL_NAMES_CHECKED:
            item = get_import_schema_dialog.import_models_list_widget.findItems(modelname, Qt.MatchExactly)
            item[0].setCheckState(Qt.Checked)
        
        get_import_schema_dialog.accepted()

        if get_import_schema_dialog.progress_bar.value() != 100:
            dlg = LogExcelDialog(self.qgis_utils, get_import_schema_dialog.txtStdout.toHtml())
            dlg.buttonBox.button(QDialogButtonBox.Save).setVisible(False)
            dlg.setFixedSize(dlg.size()) 
            dlg.setWindowTitle(QCoreApplication.translate("DialogInputLoadFieldDataCapture","Log error structure LADM"))
            dlg.exec_()