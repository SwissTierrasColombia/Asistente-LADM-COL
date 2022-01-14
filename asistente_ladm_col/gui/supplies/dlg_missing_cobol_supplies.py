"""
/***************************************************************************
                              Asistente LADM-COL
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

from qgis.PyQt.QtWidgets import (QMessageBox,
                                 QDialogButtonBox)
from qgis.PyQt.QtCore import (Qt,
                              QSettings,
                              QCoreApplication)
from qgis.PyQt.QtGui import  QValidator
from qgis.core import (Qgis,
                       QgsProject,
                       QgsVectorLayer,
                       QgsProcessingException)

import processing

from asistente_ladm_col.utils.qt_utils import (OverrideCursor,
                                               normalize_local_url)

from asistente_ladm_col.config.help_strings import HelpStrings
from asistente_ladm_col.utils.utils import show_plugin_help
from asistente_ladm_col.gui.supplies.dlg_missing_supplies_base import MissingSuppliesBaseDialog


class MissingCobolSuppliesDialog(MissingSuppliesBaseDialog):
    def __init__(self, db, conn_manager, parent=None):
        MissingSuppliesBaseDialog.__init__(self, db, conn_manager, parent)
        self._db = db
        self.conn_manager = conn_manager
        self.parent = parent

        self.names_gpkg = ''
        self.help_strings = HelpStrings()
        self.progress_configuration(0, 2)  # Start from: 0, number of steps: 2
        self._running_tool = False
        self.tool_name = QCoreApplication.translate("MissingCobolSuppliesDialog", "Missing Supplies")
        self.setWindowTitle(QCoreApplication.translate("MissingCobolSuppliesDialog", "Find missing Cobol supplies"))
        self.txt_help_page.setHtml(self.help_strings.DLG_MISSING_COBOL_SUPPLIES)
        self.data_system = 'cobol'

        # Trigger validations right now
        self.txt_file_path_uni.textChanged.emit(self.txt_file_path_uni.text())
        self.txt_file_path_gdb.textChanged.emit(self.txt_file_path_gdb.text())
        self.txt_file_path_folder_supplies.textChanged.emit(self.txt_file_path_folder_supplies.text())
        self.txt_file_names_supplies.textChanged.emit(self.txt_file_names_supplies.text())
        self.buttonBox.helpRequested.connect(self.show_help)

        # Initialize
        self.disable_widgets()
        self.restore_settings(self.data_system)

    def accepted(self):
        self.bar.clearWidgets()
        self.save_settings(self.data_system)
        etl_result = False

        self.folder_path = self.txt_file_path_folder_supplies.text()
        self.file_names = self.txt_file_names_supplies.text().strip()
        self.gpkg_path = os.path.join(self.folder_path, '{}.gpkg'.format(self.file_names))
        self.xlsx_path = os.path.join(self.folder_path, '{}.xlsx'.format(self.file_names))

        reply = self.validate_files_in_folder()

        alphanumeric_file_paths = {'uni': self.txt_file_path_uni.text().strip()}

        required_layers = ['R_TERRENO',
                           'U_TERRENO',
                           'R_VEREDA',
                           'U_MANZANA',
                           'R_CONSTRUCCION',
                           'U_CONSTRUCCION',
                           'U_UNIDAD',
                           'R_UNIDAD']

        if reply == QMessageBox.Yes:
            with OverrideCursor(Qt.WaitCursor):
                self.set_gui_controls_enabled(False)
                res_lis, msg_lis = self.load_lis_files(alphanumeric_file_paths)
                if res_lis:
                    res_gdb, msg_gdb = self.load_gdb_files(required_layers)
                    if res_gdb:
                        self._running_tool = True
                        res_etl, msg_etl = self.run_model_missing_cobol_supplies()
                        self.progress_base = 100  # We start counting a second step from 100

                        if res_etl:
                            # Since we have two steps, we need to check at this point if the user already canceled
                            if not self.custom_feedback.isCanceled():
                                self.logger.clear_status()
                                res_gpkg, msg_gpkg = self.package_results(self.output_etl_missing_cobol)
                                if res_gpkg:
                                    self.generate_excel_report()
                                    if not self.custom_feedback.isCanceled():
                                        self.progress.setValue(self.progress_maximum)
                                        self.buttonBox.clear()
                                        self.buttonBox.setEnabled(True)
                                        self.buttonBox.addButton(QDialogButtonBox.Close)

                                        msg = QCoreApplication.translate("Asistente-LADM-COL",
                                            "Missing supplies report successfully generated in folder <a href='file:///{normalized_path1}'>{path1}</a>! The output Geopackage database can be found in <a href='file:///{normalized_path2}'>{path2}</a>").format(
                                            normalized_path1=normalize_local_url(self.xlsx_path),
                                            path1=self.xlsx_path,
                                            normalized_path2=normalize_local_url(self.gpkg_path),
                                            path2=self.gpkg_path)
                                        self.logger.clear_status()
                                        self.logger.success_msg(__name__, msg)
                                        etl_result = True
                                    else:
                                        self.initialize_feedback()  # Get ready for an eventual new execution
                                        self.progress_base = 0
                                        self.logger.clear_status()

                                    self._running_tool = False
                                else:
                                    # User could have canceled while running the second algorithm
                                    if self.custom_feedback.isCanceled():
                                        self.initialize_feedback()  # Get ready for an eventual new execution
                                        self.progress_base = 0
                                        self._running_tool = False
                                    else:
                                        self.show_message(msg_gpkg, Qgis.Warning)
                            else:  # User canceled in the first algorithm
                                self.initialize_feedback()
                                self.progress_base = 0
                                self._running_tool = False
                                self.logger.clear_status()
                        else:
                            self.show_message(msg_etl, Qgis.Warning)
                    else:
                        self.show_message(msg_gdb, Qgis.Warning)
                else:
                    self.show_message(msg_lis, Qgis.Warning)

            self.set_gui_controls_enabled(True)

        self.on_result.emit(etl_result)  # Inform other classes if the execution was successful

    def validate_files_in_folder(self):
        """
        Verify that both GPKG and XLSX paths exist.
        """
        if os.path.isfile(self.gpkg_path) and os.path.isfile(self.xlsx_path):
            reply = QMessageBox.question(self,
                QCoreApplication.translate("MissingCobolSuppliesDialog", "Warning"),
                QCoreApplication.translate("MissingCobolSuppliesDialog", "The <b>xlsx</b> and the <b>gpkg</b> already exist in the folder"
                                                                   ".<br/><br/>If you run the function, the data will be overwritten.<br/><br/>Do you still want to continue?"),
                QMessageBox.Yes, QMessageBox.No)

            return reply
        else:
            reply = QMessageBox.Yes

        if reply == QMessageBox.Yes and os.path.isfile(self.gpkg_path):
            reply = QMessageBox.question(self,
                QCoreApplication.translate("MissingCobolSuppliesDialog", "Warning"),
                QCoreApplication.translate("MissingCobolSuppliesDialog", "The <b>gpkg</b> already exist in the folder"
                                                                   ".<br/><br/>If you run the function, the data will be overwritten.<br/><br/>Do you still want to continue?"),
                QMessageBox.Yes, QMessageBox.No)

            return reply
        else:
            reply = QMessageBox.Yes

        if reply == QMessageBox.Yes and os.path.isfile(self.xlsx_path):
            reply = QMessageBox.question(self,
                QCoreApplication.translate("MissingCobolSuppliesDialog", "Warning"),
                QCoreApplication.translate("MissingCobolSuppliesDialog", "The <b>xlsx</b> already exist in the folder"
                                                                   ".<br/><br/>If you run the function, the data will be overwritten.<br/><br/>Do you still want to continue?"),
                QMessageBox.Yes, QMessageBox.No)

            return reply
        else:
            reply = QMessageBox.Yes

        return reply

    def run_model_missing_cobol_supplies(self):
        self.progress.setVisible(True)
        self.logger.info(__name__, "Running Missing Cobol Supplies model...")

        try:
            self.output_etl_missing_cobol = processing.run("model:ETL_O_M_Cobol",
                {'rconstruccion': self.gdb_layer_paths['R_CONSTRUCCION'],
                'rterreno': self.gdb_layer_paths['R_TERRENO'],
                'runidad': self.gdb_layer_paths['R_UNIDAD'],
                'rvereda': self.gdb_layer_paths['R_VEREDA'],
                'uconstruccion': self.gdb_layer_paths['U_CONSTRUCCION'],
                'umanzana': self.gdb_layer_paths['U_MANZANA'],
                'uni':self.alphanumeric_file_paths['uni'],
                'uterreno': self.gdb_layer_paths['U_TERRENO'],
                'uunidad': self.gdb_layer_paths['U_UNIDAD'],
                'native:removeduplicatesbyattribute_2:COMISIONES_MZ':'TEMPORARY_OUTPUT',
                'native:removeduplicatesbyattribute_3:OMISIONES_MZ':'TEMPORARY_OUTPUT',
                'native:removeduplicatesbyattribute_4:COMISIONES_VR':'TEMPORARY_OUTPUT',
                'native:removeduplicatesbyattribute_5:OMISIONES_VR':'TEMPORARY_OUTPUT',
                'native:removeduplicatesbyattribute_6:COMISIONES_UNID_PH':'TEMPORARY_OUTPUT',
                'native:removeduplicatesbyattribute_7:OMISIONES_UNID_PH':'TEMPORARY_OUTPUT',
                'native:removeduplicatesbyattribute_8:COMISIONES_TERRENO':'TEMPORARY_OUTPUT',
                'native:removeduplicatesbyattribute_9:OMISIONES_TERRENO':'TEMPORARY_OUTPUT',
                'native:removeduplicatesbyattribute_10:COMISIONES_MEJORAS':'TEMPORARY_OUTPUT',
                'native:removeduplicatesbyattribute_11:OMISIONES_MEJORAS':'TEMPORARY_OUTPUT',
                'qgis:aggregate_12:TABLA_RESUMEN':'TEMPORARY_OUTPUT'},
                feedback=self.custom_feedback)
        except QgsProcessingException as e:
            if self.custom_feedback.isCanceled():
                # The algorithm can throw errors even if canceled, so catch them and if we canceled, silent them.
                return False, 'Missing cobol supplies algorithm canceled!'
            else:
                msg = "QgsProcessingException (Missing cobol supplies): {}".format(str(e))
                self.logger.critical(__name__, msg)
                self.show_message(msg, Qgis.Critical)
                return False, QCoreApplication.translate("MissingCobolSuppliesDialog", "Errors in the 'ETL Omissions-Commissions' model. See QGIS log for details.")

        self.logger.info(__name__, "Missing Cobol Supplies model finished.")
        return True, ''

    def package_results(self, output):  
        keys_deleted = []

        for name in output.keys():
            if isinstance(output[name], QgsVectorLayer):
                output[name].setName(name.split(':')[2])
            else:
                keys_deleted.append(name)

        for key_deleted in keys_deleted:
            output.pop(key_deleted, None)

        try:
            output_geopackage = processing.run("native:package", {'LAYERS': list(output.values()),
                                                                  'OUTPUT': self.gpkg_path,
                                                                  'OVERWRITE': True,
                                                                  'SAVE_STYLES': True},
                                               feedback=self.custom_feedback)
        except QgsProcessingException as e:
            if self.custom_feedback.isCanceled():
                # The algorithm can throw errors even if canceled, so catch them and if we canceled, silent them.
                return False, 'Package results canceled!'
            else:
                msg = "QgsProcessingException (Package layers): {}".format(str(e))
                self.logger.critical(__name__, msg)
                return False, QCoreApplication.translate("MissingCobolSuppliesDialog", "Errors in the 'Package layers' algorithm. See QGIS log for details.")

        root = QgsProject.instance().layerTreeRoot()
        results_group = root.addGroup(QCoreApplication.translate("MissingCobolSuppliesDialog", "Results missing supplies"))

        for layer_path in output_geopackage['OUTPUT_LAYERS']:
            layer = QgsVectorLayer(layer_path, layer_path.split('layername=')[1], 'ogr')
            self.names_gpkg += '{} '.format(layer_path.split('layername=')[1])
            if not layer.isValid():
                return False, QCoreApplication.translate("MissingCobolSuppliesDialog", "There were troubles loading {} layer.").format(layer_path.split('layername=')[1])
            QgsProject.instance().addMapLayer(layer, False)
            results_group.addLayer(layer)
            node = root.findLayer(layer.id())
            node.setCustomProperty("showFeatureCount", True)

        return True, ''

    def generate_excel_report(self):
        gdal.VectorTranslate(self.xlsx_path,
                             self.gpkg_path,
                             options='-f XLSX {}'.format(self.spreadsheet_structure))

    def disable_widgets(self):
        """
        Hide widgets that we don need in this class.
        """
        self.label_predio.setVisible(False)
        self.txt_file_path_predio.setVisible(False)
        self.btn_browse_file_predio.setVisible(False)

    def validate_inputs(self):
        """
        The dialog has inputs that are necessary for the model to work. So, validate that the file exists and has the correct extension.
        """
        
        uni_path = self.txt_file_path_uni.validator().validate(self.txt_file_path_uni.text().strip(), 0)[0]
        folder_path = self.txt_file_path_folder_supplies.validator().validate(self.txt_file_path_folder_supplies.text().strip(), 0)[0]
        file_names = self.txt_file_names_supplies.validator().validate(self.txt_file_names_supplies.text().strip(), 0)[0]
        
        if uni_path == QValidator.Acceptable and folder_path == QValidator.Acceptable and file_names == QValidator.Acceptable and self.validate_common_inputs():
            return True
        else:
            return False

    def show_help(self):
        show_plugin_help('omission_commission_cobol')
