# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-11-13
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
from osgeo import gdal

from qgis.PyQt.QtWidgets import (QDialog,
                                 QMessageBox,
                                 QDialogButtonBox,
                                 QSizePolicy)
from qgis.PyQt.QtCore import (Qt,
                              QSettings,
                              QCoreApplication)
from qgis.PyQt.QtGui import  QValidator
from qgis.core import (Qgis,
                       QgsProject,
                       QgsWkbTypes,
                       QgsVectorLayer,
                       QgsProcessingFeedback,
                       QgsVectorLayerJoinInfo,
                       QgsProcessingException)

import processing

from asistente_ladm_col.config.general_config import SETTINGS_CONNECTION_TAB_INDEX

from asistente_ladm_col.config.enums import EnumDbActionType
from asistente_ladm_col.gui.dialogs.dlg_settings import SettingsDialog
from asistente_ladm_col.utils.qt_utils import (OverrideCursor,
                                               DirValidator,
                                               make_folder_selector,
                                               normalize_local_url)

from asistente_ladm_col.utils.ui import load_ui
from asistente_ladm_col.gui.dialogs.dlg_cobol_base import CobolBaseDialog


class MissingCobolSupplies(CobolBaseDialog):
    def __init__(self, qgis_utils, db, conn_manager, parent=None):
        CobolBaseDialog.__init__(self, qgis_utils, db, conn_manager, parent)
        self.qgis_utils = qgis_utils
        self._db = db
        self.conn_manager = conn_manager
        self.parent = parent
        self.names_gpkg = ''
        self.progress_configuration(0, 2)  # Start from: 0, number of steps: 2
        self._running_missing_supplies = False

        load_ui('dialogs/wig_missing_cobol_supplies_export.ui', self.target_data)
        self.target_data.setVisible(True)

        self.disable_widgets()

        self.target_data.btn_browse_file_folder_supplies.clicked.connect(
                make_folder_selector(self.target_data.txt_file_path_folder_supplies, title=QCoreApplication.translate(
                'MissingCobolSupplies', 'Select folder to save data'), parent=None))

        dir_validator_folder = DirValidator(pattern=None, allow_empty_dir=True)
        self.target_data.txt_file_path_folder_supplies.setValidator(dir_validator_folder)
        self.target_data.txt_file_path_folder_supplies.textChanged.connect(self.validators.validate_line_edits)
        self.target_data.txt_file_path_folder_supplies.textChanged.connect(self.input_data_changed)

        self.restore_settings()
        self.target_data.txt_file_path_folder_supplies.setText(QSettings().value('Asistente-LADM_COL/etl_cobol/folder_path', ''))

        # Trigger validations right now
        self.txt_file_path_uni.textChanged.emit(self.txt_file_path_uni.text())
        self.txt_file_path_ter.textChanged.emit(self.txt_file_path_ter.text())
        self.txt_file_path_pro.textChanged.emit(self.txt_file_path_pro.text())
        self.txt_file_path_gdb.textChanged.emit(self.txt_file_path_gdb.text())
        self.target_data.txt_file_path_folder_supplies.textChanged.emit(self.target_data.txt_file_path_folder_supplies.text())

    def accepted(self):
        self.save_settings()
        QSettings().setValue('Asistente-LADM_COL/etl_cobol/folder_path', self.target_data.txt_file_path_folder_supplies.text())

        self.folder_path = self.target_data.txt_file_path_folder_supplies.text()
        self.gpkg_path = os.path.join(self.folder_path, QCoreApplication.translate(
                'MissingCobolSupplies', 'missing_supplies_cobol.gpkg'))
        self.xlsx_path = os.path.join(self.folder_path, QCoreApplication.translate(
                'MissingCobolSupplies', 'missing_supplies_cobol.xlsx'))

        reply = self.validate_files_in_folder()

        lis_paths = {'uni': self.txt_file_path_uni.text().strip()}

        required_layers = ['R_TERRENO','U_TERRENO','R_VEREDA','U_MANZANA','R_CONSTRUCCION'
                            ,'U_CONSTRUCCION','U_UNIDAD','R_UNIDAD']

        if reply == QMessageBox.Yes:
            with OverrideCursor(Qt.WaitCursor):
                self.set_gui_controls_enabled(False)
                res_lis, msg_lis = self.load_lis_files(lis_paths)
                if res_lis:
                    res_gdb, msg_gdb = self.load_gdb_files(required_layers)
                    if res_gdb:
                        self._running_missing_supplies = True
                        self.run_model_missing_cobol_supplies()
                        self.progress_base = 100  # We start counting a second step from 100

                        # Since we have two steps, we need to check at this point if the user already canceled
                        if not self.feedback.isCanceled():
                            res_gpkg, msg_gpkg = self.package_results(self.output_etl_missing_cobol)
                            if res_gpkg:
                                self.generate_excel_report()
                                if not self.feedback.isCanceled():
                                    self.progress.setValue(self.progress_maximum)
                                    self.buttonBox.clear()
                                    self.buttonBox.setEnabled(True)
                                    self.buttonBox.addButton(QDialogButtonBox.Close)

                                    msg = QCoreApplication.translate("Asistente-LADM_COL",
                                        "Missing supplies report successfully generated in folder <a href='file:///{normalized_path1}'>{path1}</a>! The output Geopackage database can be found in <a href='file:///{normalized_path2}'>{path2}</a>").format(
                                        normalized_path1=normalize_local_url(self.xlsx_path),
                                        path1=self.xlsx_path,
                                        normalized_path2=normalize_local_url(self.gpkg_path),
                                        path2=self.gpkg_path)
                                    self.logger.success_msg(__name__, msg)
                                else:
                                    self.initialize_feedback()  # Get ready for an eventual new execution
                                    self.progress_base = 0

                                self._running_missing_supplies = False
                            else:
                                # User could have canceled while running the second algorithm
                                if self.feedback.isCanceled():
                                    self.initialize_feedback()  # Get ready for an eventual new execution
                                    self.progress_base = 0
                                    self._running_missing_supplies = False
                                else:
                                    self.show_message(msg_gpkg, Qgis.Warning)
                        else:  # User canceled in the first algorithm
                            self.initialize_feedback()
                            self.progress_base = 0
                            self._running_missing_supplies = False
                    else:
                        self.show_message(msg_gdb, Qgis.Warning)
                else:
                    self.show_message(msg_lis, Qgis.Warning)

            self.set_gui_controls_enabled(True)

    def validate_files_in_folder(self):
        if os.path.isfile(self.gpkg_path) and os.path.isfile(self.xlsx_path):
            reply = QMessageBox.question(self,
                QCoreApplication.translate("MissingCobolSupplies", "Warning"),
                QCoreApplication.translate("MissingCobolSupplies","The <b>xlsx</b> and the <b>gpkg</b> already exist in the folder" \
                    ".<br/><br/>If you run the function, the data will be overwritten.<br/><br/>Do you still want to continue?"),
                QMessageBox.Yes, QMessageBox.No)

            return reply
        else:
            reply = QMessageBox.Yes

        if reply == QMessageBox.Yes and os.path.isfile(self.gpkg_path):
            reply = QMessageBox.question(self,
                QCoreApplication.translate("MissingCobolSupplies", "Warning"),
                QCoreApplication.translate("MissingCobolSupplies","The <b>gpkg</b> already exist in the folder" \
                    ".<br/><br/>If you run the function, the data will be overwritten.<br/><br/>Do you still want to continue?"),
                QMessageBox.Yes, QMessageBox.No)

            return reply
        else:
            reply = QMessageBox.Yes

        if reply == QMessageBox.Yes and os.path.isfile(self.xlsx_path):
            reply = QMessageBox.question(self,
                QCoreApplication.translate("MissingCobolSupplies", "Warning"),
                QCoreApplication.translate("MissingCobolSupplies","The <b>xlsx</b> already exist in the folder" \
                    ".<br/><br/>If you run the function, the data will be overwritten.<br/><br/>Do you still want to continue?"),
                QMessageBox.Yes, QMessageBox.No)

            return reply
        else:
            reply = QMessageBox.Yes

        return reply

    def run_model_missing_cobol_supplies(self):
        self.progress.setVisible(True)
        self.logger.info(__name__, "Running ETL-Missing Cobol model...")

        try:
            self.output_etl_missing_cobol = processing.run("model:ETL_O_M_Cobol",
                {'rconstruccion': self.gdb_paths['R_CONSTRUCCION'],
                'rterreno': self.gdb_paths['R_TERRENO'],
                'runidad': self.gdb_paths['R_UNIDAD'],
                'rvereda': self.gdb_paths['R_VEREDA'],
                'uconstruccion': self.gdb_paths['U_CONSTRUCCION'],
                'umanzana': self.gdb_paths['U_MANZANA'],
                'uni':self.lis_paths['uni'],
                'uterreno': self.gdb_paths['U_TERRENO'],
                'uunidad': self.gdb_paths['U_UNIDAD'],
                'qgis:refactorfields_1:COMISIONES_TERRENO':'TEMPORARY_OUTPUT',
                'qgis:refactorfields_2:OMISIONES_TERRENO':'TEMPORARY_OUTPUT',
                'qgis:refactorfields_3:COMISIONES_MEJORAS':'TEMPORARY_OUTPUT',
                'qgis:refactorfields_4:OMISIONES_MEJORAS':'TEMPORARY_OUTPUT',
                'qgis:refactorfields_5:COMISIONES_UNID_PH':'TEMPORARY_OUTPUT',
                'qgis:refactorfields_6:OMISIONES_UNID_PH':'TEMPORARY_OUTPUT',
                'qgis:refactorfields_7:COMISIONES_MZ':'TEMPORARY_OUTPUT',
                'qgis:refactorfields_8:OMISIONES_MZ':'TEMPORARY_OUTPUT',
                'qgis:refactorfields_9:COMISIONES_VR':'TEMPORARY_OUTPUT',
                'qgis:refactorfields_10:OMISIONES_VR':'TEMPORARY_OUTPUT'},
                feedback=self.feedback)
        except QgsProcessingException as e:
            if self.feedback.isCanceled():
                # The algorithm can throw errors even if canceled, so catch them and if we canceled, silent them.
                return False, 'Missing cobol supplies algorithm canceled!'
            else:
                msg = "QgsProcessingException (Missing cobol supplies): {}".format(str(e))
                self.logger.critical(__name__, msg)
                self.show_message(msg, Qgis.Critical)

        self.logger.info(__name__, "ETL-Missing Cobol model finished.")

    def package_results(self, output):  
        for name in output.keys():
            output[name].setName(name.split(':')[2])

        try:
            output_geopackage = processing.run("native:package", {'LAYERS': [
                        output['qgis:refactorfields_1:COMISIONES_TERRENO'],
                        output['qgis:refactorfields_2:OMISIONES_TERRENO'],
                        output['qgis:refactorfields_3:COMISIONES_MEJORAS'],
                        output['qgis:refactorfields_4:OMISIONES_MEJORAS'],
                        output['qgis:refactorfields_5:COMISIONES_UNID_PH'],
                        output['qgis:refactorfields_6:OMISIONES_UNID_PH'],
                        output['qgis:refactorfields_7:COMISIONES_MZ'],
                        output['qgis:refactorfields_8:OMISIONES_MZ'],
                        output['qgis:refactorfields_9:COMISIONES_VR'],
                        output['qgis:refactorfields_10:OMISIONES_VR']],
                    'OUTPUT': self.gpkg_path,
                    'OVERWRITE': True,
                    'SAVE_STYLES': True},
                feedback=self.feedback)
        except QgsProcessingException as e:
            if self.feedback.isCanceled():
                # The algorithm can throw errors even if canceled, so catch them and if we canceled, silent them.
                return False, 'Package results canceled!'
            else:
                msg = "QgsProcessingException (Package layers): {}".format(str(e))
                self.logger.critical(__name__, msg)
                self.show_message(msg, Qgis.Critical)

        root = QgsProject.instance().layerTreeRoot()
        results_group = root.addGroup(QCoreApplication.translate("MissingCobolSupplies", "Results missing supplies"))

        for layer_path in output_geopackage['OUTPUT_LAYERS']:
            layer = QgsVectorLayer(layer_path, layer_path.split('layername=')[1], 'ogr')
            self.names_gpkg += '{} '.format(layer_path.split('layername=')[1])
            if not layer.isValid():
                return False, QCoreApplication.translate("MissingCobolSupplies", "There were troubles loading {} layer.".format(layer_path.split('layername=')[1]))
            QgsProject.instance().addMapLayer(layer, False)
            results_group.addLayer(layer)
            LayerNode = root.findLayer(layer.id())
            LayerNode.setCustomProperty("showFeatureCount", True)

        return True, ''

    def generate_excel_report(self):
        gdal.VectorTranslate(self.xlsx_path,
                             self.gpkg_path,
                             options='-f XLSX {}'.format(self.names_gpkg.strip()))
    
    def show_settings(self):
        dlg = SettingsDialog(qgis_utils=self.qgis_utils, conn_manager=self.conn_manager)

        dlg.db_connection_changed.connect(self.db_connection_changed)
        dlg.db_connection_changed.connect(self.qgis_utils.cache_layers_and_relations)

        # We only need those tabs related to Model Baker/ili2db operations
        for i in reversed(range(dlg.tabWidget.count())):
            if i not in [SETTINGS_CONNECTION_TAB_INDEX]:
                dlg.tabWidget.removeTab(i)

        dlg.set_action_type(EnumDbActionType.SCHEMA_IMPORT)  # To avoid unnecessary validations (LADM compliance)

        if dlg.exec_():
            self._db = dlg.get_db_connection()
            self.update_connection_info()

    def update_connection_info(self):
        db_description = self._db.get_description_conn_string()
        if db_description:
            self.target_data.db_connect_label.setText(db_description)
            self.target_data.db_connect_label.setToolTip(self._db.get_display_conn_string())
        else:
            self.target_data.db_connect_label.setText(
                QCoreApplication.translate("MissingCobolSupplies", "The database is not defined!"))
            self.target_data.db_connect_label.setToolTip('')

    def additional_validations(self):
        if hasattr(self.target_data, "txt_file_path_folder_supplies"):
            state_folder = self.target_data.txt_file_path_folder_supplies.validator().validate(
                self.target_data.txt_file_path_folder_supplies.text().strip(), 0)[0]
        else:
            state_folder = QValidator.Acceptable

        return state_folder

    def disable_widgets(self):
        """
        The base dialog has widgets that we don't need in this subclass. so hide them.
        """
        self.label_blo.setVisible(False)
        self.label_ter.setVisible(False)
        self.label_pro.setVisible(False)

        self.txt_file_path_blo.setVisible(False)
        self.txt_file_path_ter.setVisible(False)
        self.txt_file_path_pro.setVisible(False)

        self.btn_browse_file_blo.setVisible(False)
        self.btn_browse_file_ter.setVisible(False)
        self.btn_browse_file_pro.setVisible(False)

    def validate_inputs(self):
        state_path = self.target_data.txt_file_path_folder_supplies.validator().validate(self.target_data.txt_file_path_folder_supplies.text().strip(), 0)[0]

        if state_path == QValidator.Acceptable and self.validate_common_inputs():
            return True
        else:
            return False

    def reject(self):
        if self._running_missing_supplies:
            reply = QMessageBox.question(self,
                                         QCoreApplication.translate("MissingCobolSupplies", "Warning"),
                                         QCoreApplication.translate("MissingCobolSupplies",
                                                                    "The 'Missing Supplies' tool is still running. Do you want to cancel it? If you cancel, the data might be incomplete in the target database."),
                                         QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.feedback.cancel()
                self._running_missing_supplies = False
                msg = QCoreApplication.translate("MissingCobolSupplies", QCoreApplication.translate("MissingCobolSupplies", "The 'Missing Supplies' tool was cancelled."))
                self.logger.info(__name__, msg)
                self.show_message(msg, Qgis.Info)
        else:
            if self._db_was_changed:
                self.conn_manager.db_connection_changed.emit(self._db, self._db.test_connection()[0])
            self.logger.info(__name__, "Dialog closed.")
            self.done(1)