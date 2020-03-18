# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-11-13
        git sha              : :%H$
        copyright            : (C) 2020 by Jhon Galindo (BSF Swissphoto)
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
from qgis.PyQt.QtWidgets import (QMessageBox,
                                 QDialogButtonBox)
from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication)
from qgis.PyQt.QtGui import  QValidator
from qgis.core import (Qgis)

import processing

from asistente_ladm_col.config.general_config import (LAYER,
                                                      SETTINGS_CONNECTION_TAB_INDEX,
                                                      COLLECTED_DB_SOURCE,
                                                      SUPPLIES_DB_SOURCE)
from asistente_ladm_col.config.enums import EnumDbActionType
from asistente_ladm_col.gui.dialogs.dlg_settings import SettingsDialog
from asistente_ladm_col.utils.qt_utils import (OverrideCursor,
                                               FileValidator,
                                               DirValidator,
                                               Validators,
                                               make_file_selector,
                                               make_folder_selector)
from asistente_ladm_col.utils.ui import load_ui
from asistente_ladm_col.gui.supplies.dlg_etl_base import EtlBaseDialog


class ETLSNCDialog(EtlBaseDialog):
    def __init__(self, qgis_utils, db, conn_manager, parent=None):
        EtlBaseDialog.__init__(self, qgis_utils, db, conn_manager, parent)
        self.qgis_utils = qgis_utils
        self._db = db
        self.names = self._db.names
        self.conn_manager = conn_manager
        self.parent = parent
        self.progress_configuration(0, 1)  # start from: 0, number of steps: 1
        self.tool_name = QCoreApplication.translate("EtlSNCDialog", "ETL-SNC")
        self.setWindowTitle(QCoreApplication.translate("EtlSNCDialog", "ETL: SNC to Supplies model"))
        self.db_source = SUPPLIES_DB_SOURCE

        load_ui('supplies/wig_etl_supplies.ui', self.target_data)
        self.target_data.setVisible(True)

        self.rename_widgets()

        self.target_data.btn_browse_connection.clicked.connect(self.show_settings)
        self.update_connection_info()

        self.restore_settings()

        self.txt_help_page.clear()
        self.txt_help_page.insertHtml('Este diálogo permite convertir datos procedentes de SNC \
                                   al modelo de Datos Gestor Catastral, uno de los modelos \
                                   extendidos de perfil colombiano LADM-COL.')

        self.btn_browse_file_blo.clicked.disconnect()
        self.btn_browse_file_uni.clicked.disconnect()
        self.btn_browse_file_ter.clicked.disconnect()
        self.btn_browse_file_pro.clicked.disconnect()
        self.btn_browse_file_gdb.clicked.disconnect()

        self.btn_browse_file_blo.clicked.connect(
            make_file_selector(self.txt_file_path_blo, QCoreApplication.translate("EtlBaseDialog",
                        "Select the Predio sanción .csv file with SNC data "),
                        QCoreApplication.translate("EtlSNCDialog", 'CSV File (*.csv)')))

        self.btn_browse_file_uni.clicked.connect(
            make_file_selector(self.txt_file_path_uni, QCoreApplication.translate("EtlSNCDialog",
                        "Select the Predio .csv file with SNC data "),
                        QCoreApplication.translate("EtlSNCDialog", 'CSV File (*.csv)')))

        self.btn_browse_file_ter.clicked.connect(
            make_file_selector(self.txt_file_path_ter, QCoreApplication.translate("EtlSNCDialog",
                        "Select the Dirección .csv file with SNC data "),
                        QCoreApplication.translate("EtlSNCDialog", 'CSV File (*.csv)')))

        self.btn_browse_file_pro.clicked.connect(
            make_file_selector(self.txt_file_path_pro, QCoreApplication.translate("EtlSNCDialog",
                        "Select the Unidad construccion .csv file with SNC data "),
                        QCoreApplication.translate("EtlSNCDialog", 'CSV File (*.csv)')))

        self.btn_browse_file_gdb.clicked.connect(
            make_folder_selector(self.txt_file_path_gdb, title=QCoreApplication.translate(
                        'EtlSNCDialog', 'Open GDB folder'), parent=None))

        # Trigger validations right now
        self.txt_file_path_blo.textChanged.emit(self.txt_file_path_blo.text())
        self.txt_file_path_uni.textChanged.emit(self.txt_file_path_uni.text())
        self.txt_file_path_ter.textChanged.emit(self.txt_file_path_ter.text())
        self.txt_file_path_pro.textChanged.emit(self.txt_file_path_pro.text())
        self.txt_file_path_persona.textChanged.emit(self.txt_file_path_persona.text())
        self.txt_file_path_ficha_m.textChanged.emit(self.txt_file_path_ter.text())
        self.txt_file_path_ficha_m_predio.textChanged.emit(self.txt_file_path_pro.text())
        self.txt_file_path_gdb.textChanged.emit(self.txt_file_path_gdb.text())

    def accepted(self):
        self.bar.clearWidgets()
        self.save_settings()

        if self._db.test_connection()[0]:
            reply = QMessageBox.question(self,
                QCoreApplication.translate("EtlSNCDialog", "Warning"),
                QCoreApplication.translate("EtlSNCDialog", "The database <i>{}</i> already has a valid LADM_COL structure.<br/><br/>If such database has any data, loading data into it might cause invalid data.<br/><br/>Do you still want to continue?").format(self._db.get_description_conn_string()),
                QMessageBox.Yes, QMessageBox.No)

            lis_paths = {
                'blo': self.txt_file_path_blo.text().strip(),
                'uni': self.txt_file_path_uni.text().strip(),
                'ter': self.txt_file_path_ter.text().strip(),
                'pro': self.txt_file_path_pro.text().strip()
            }

            required_layers = ['R_TERRENO', 'U_TERRENO', 'R_SECTOR', 'U_SECTOR', 'R_VEREDA', 'U_MANZANA', 'U_BARRIO',
                               'R_CONSTRUCCION', 'U_CONSTRUCCION', 'U_UNIDAD', 'R_UNIDAD',
                               'U_NOMENCLATURA_DOMICILIARIA', 'R_NOMENCLATURA_DOMICILIARIA', 'U_PERIMETRO']

            if reply == QMessageBox.Yes:
                self.set_gui_controls_enabled(False)
                with OverrideCursor(Qt.WaitCursor):
                    res_lis, msg_lis = self.load_lis_files(lis_paths)
                    if res_lis:
                        res_gdb, msg_gdb = self.load_gdb_files(required_layers)
                        if res_gdb:
                            res_model, msg_model = self.load_model_layers()
                            if res_model:
                                self._running_tool = True
                                self.run_model_etl_cobol()
                                if not self.custom_feedback.isCanceled():
                                    self.progress.setValue(100)
                                    self.buttonBox.clear()
                                    self.buttonBox.setEnabled(True)
                                    self.buttonBox.addButton(QDialogButtonBox.Close)
                                    self.logger.clear_status()
                                    self._etl_result = True
                                else:
                                    self.initialize_feedback()  # Get ready for an eventual new execution
                                    self.logger.clear_status()
                                self._running_tool = False
                            else:
                                self.show_message(msg_model, Qgis.Warning)
                        else:
                            self.show_message(msg_gdb, Qgis.Warning)
                    else:
                        self.show_message(msg_lis, Qgis.Warning)

                self.set_gui_controls_enabled(True)
        else:
            with OverrideCursor(Qt.WaitCursor):
                # TODO: if an empty schema was selected, do the magic under the hood
                # self.create_model_into_database()
                # Now execute "accepted()"
                msg = QCoreApplication.translate("EtlSNCDialog", "To run the ETL, the database (schema) should have the Supplies LADM_COL structure. Choose a proper database (schema) and try again.")
                self.show_message(msg, Qgis.Warning)
                self.logger.warning(__name__, msg)

        self.on_result.emit(self._etl_result)  # Inform other classes if the execution was successful
        self._etl_result = False  # Next run?

    def run_model_etl_cobol(self):
        self.progress.setVisible(True)
        self.logger.info(__name__, "Running ETL-Cobol model...")
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
            'unomenclatura': self.gdb_paths['U_NOMENCLATURA_DOMICILIARIA']},
                       feedback=self.custom_feedback)
        self.logger.info(__name__, "ETL-Cobol model finished.")

    def validate_inputs(self):
        state_blo = self.txt_file_path_blo.validator().validate(self.txt_file_path_blo.text().strip(), 0)[0]
        state_ter = self.txt_file_path_ter.validator().validate(self.txt_file_path_ter.text().strip(), 0)[0]
        state_pro = self.txt_file_path_pro.validator().validate(self.txt_file_path_pro.text().strip(), 0)[0]

        if state_blo == QValidator.Acceptable and \
                state_ter == QValidator.Acceptable and \
                state_pro == QValidator.Acceptable and \
                self.validate_common_inputs():
            return True
        else:
            return False

    def show_settings(self):
        dlg = SettingsDialog(qgis_utils=self.qgis_utils, conn_manager=self.conn_manager)
        dlg.set_db_source(self.db_source)

        dlg.db_connection_changed.connect(self.db_connection_changed)
        if self.db_source == COLLECTED_DB_SOURCE:
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
                QCoreApplication.translate("EtlBaseDialog", "The database is not defined!"))
            self.target_data.db_connect_label.setToolTip('')

    def rename_widgets(self):
        """
        The base dialog has labels that we will change the text inside, with the objective of give a good description of the interface.
        """
        self.label_blo.setText('Predio sanción')
        self.label_uni.setText('Predio')
        self.label_ter.setText('Direccion')
        self.label_pro.setText('Unidad construccion')