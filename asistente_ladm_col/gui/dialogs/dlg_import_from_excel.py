# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-12-20
        git sha              : :%H$
        copyright            : (C) 2018 by Germán Carrillo (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
import os.path
import stat

from osgeo import ogr
from qgis.core import (Qgis,
                       QgsVectorLayer,
                       QgsProject,
                       QgsFeatureRequest, 
                       QgsApplication)
from qgis.PyQt.QtCore import (Qt,
                              QSettings,
                              QCoreApplication, 
                              QFile,
                              pyqtSignal)
from qgis.gui import QgsMessageBar
import processing

from qgis.PyQt.QtWidgets import (QDialog,
                                 QSizePolicy,
                                 QGridLayout,
                                 QDialogButtonBox,
                                 QFileDialog)

from ...utils.qt_utils import make_file_selector, normalize_local_url
from ...config.help_strings import HelpStrings
from ...config.table_mapping_config import (COL_PARTY_TABLE,
                                         PARCEL_TABLE,
                                         RIGHT_TABLE,
                                         RRR_SOURCE_RELATION_TABLE,
                                         EXTFILE_TABLE,
                                         LA_GROUP_PARTY_TABLE,
                                         ADMINISTRATIVE_SOURCE_TABLE,
                                         MEMBERS_TABLE)
from ...config.general_config import (EXCEL_SHEET_TITLE_DEPARTMENT,
                                      EXCEL_SHEET_TITLE_MUNICIPALITY,
                                      EXCEL_SHEET_TITLE_ZONE,
                                      EXCEL_SHEET_TITLE_REGISTRATION_PLOT,
                                      EXCEL_SHEET_TITLE_NPN,
                                      EXCEL_SHEET_TITLE_NPV,
                                      EXCEL_SHEET_TITLE_PLOT_NAME,
                                      EXCEL_SHEET_TITLE_VALUATION,
                                      EXCEL_SHEET_TITLE_PLOT_TYPE,
                                      EXCEL_SHEET_TITLE_FIRST_NAME,
                                      EXCEL_SHEET_TITLE_MIDDLE,
                                      EXCEL_SHEET_TITLE_FIRST_SURNAME,
                                      EXCEL_SHEET_TITLE_SECOND_SURNAME,
                                      EXCEL_SHEET_TITLE_BUSINESS_NAME,
                                      EXCEL_SHEET_TITLE_SEX,
                                      EXCEL_SHEET_TITLE_DOCUMENT_TYPE,
                                      EXCEL_SHEET_TITLE_DOCUMENT_NUMBER,
                                      EXCEL_SHEET_TITLE_KIND_PERSON,
                                      EXCEL_SHEET_TITLE_ISSUING_ENTITY,
                                      EXCEL_SHEET_TITLE_DATE_ISSUE,
                                      EXCEL_SHEET_TITLE_ID_GROUP,
                                      EXCEL_SHEET_TITLE_TYPE,
                                      EXCEL_SHEET_TITLE_GROUP,
                                      EXCEL_SHEET_TITLE_SOURCE_TYPE,
                                      EXCEL_SHEET_TITLE_PARTY_DOCUMENT_NUMBER,
                                      EXCEL_SHEET_TITLE_DESCRIPTION_SOURCE,
                                      EXCEL_SHEET_TITLE_STATE_SOURCE,
                                      EXCEL_SHEET_TITLE_OFFICIALITY_SOURCE,
                                      EXCEL_SHEET_TITLE_STORAGE_PATH,
                                      LAYER,
                                      PLUGIN_NAME,
                                      LOG_QUALITY_LIST_CONTAINER_OPEN,
                                      LOG_QUALITY_LIST_ITEM_ERROR_OPEN,
                                      LOG_QUALITY_LIST_ITEM_ERROR_CLOSE,
                                      LOG_QUALITY_LIST_CONTAINER_CLOSE,
                                      LOG_QUALITY_CONTENT_SEPARATOR,
                                      EXCEL_SHEET_NAME_PLOT,
                                      EXCEL_SHEET_NAME_PARTY,
                                      EXCEL_SHEET_NAME_GROUP,
                                      EXCEL_SHEET_NAME_RIGHT)
from ...utils import get_ui_class

DIALOG_UI = get_ui_class('dialogs/dlg_import_from_excel.ui')


class DialogImportFromExcel(QDialog, DIALOG_UI):
    log_excel_show_message_emitted = pyqtSignal(str)

    def __init__(self, iface, db, qgis_utils, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self._db = db
        self.qgis_utils = qgis_utils
        self.log = QgsApplication.messageLog()
        self.help_strings = HelpStrings()
        self.log_dialog_excel_text_content = ""
        self.group_parties_exists = False

        self.fields = {EXCEL_SHEET_NAME_PLOT: [EXCEL_SHEET_TITLE_DEPARTMENT, EXCEL_SHEET_TITLE_MUNICIPALITY, EXCEL_SHEET_TITLE_ZONE, 
                            EXCEL_SHEET_TITLE_REGISTRATION_PLOT, EXCEL_SHEET_TITLE_NPN, EXCEL_SHEET_TITLE_NPV,
                            EXCEL_SHEET_TITLE_PLOT_NAME, EXCEL_SHEET_TITLE_VALUATION, EXCEL_SHEET_TITLE_PLOT_TYPE
                            ],
                        EXCEL_SHEET_NAME_PARTY: [EXCEL_SHEET_TITLE_FIRST_NAME, EXCEL_SHEET_TITLE_MIDDLE, EXCEL_SHEET_TITLE_FIRST_SURNAME,
                            EXCEL_SHEET_TITLE_SECOND_SURNAME, EXCEL_SHEET_TITLE_BUSINESS_NAME, EXCEL_SHEET_TITLE_SEX,
                            EXCEL_SHEET_TITLE_DOCUMENT_TYPE, EXCEL_SHEET_TITLE_DOCUMENT_NUMBER, EXCEL_SHEET_TITLE_KIND_PERSON,
                            EXCEL_SHEET_TITLE_ISSUING_ENTITY,EXCEL_SHEET_TITLE_DATE_ISSUE
                            ],
                        EXCEL_SHEET_NAME_GROUP: [EXCEL_SHEET_TITLE_NPN, EXCEL_SHEET_TITLE_DOCUMENT_TYPE, EXCEL_SHEET_TITLE_DOCUMENT_NUMBER,
                            EXCEL_SHEET_TITLE_ID_GROUP
                            ],
                        EXCEL_SHEET_NAME_RIGHT: [EXCEL_SHEET_TITLE_TYPE, EXCEL_SHEET_TITLE_PARTY_DOCUMENT_NUMBER, EXCEL_SHEET_TITLE_GROUP, EXCEL_SHEET_TITLE_NPN,
                            EXCEL_SHEET_TITLE_SOURCE_TYPE, EXCEL_SHEET_TITLE_DESCRIPTION_SOURCE, EXCEL_SHEET_TITLE_STATE_SOURCE,
                            EXCEL_SHEET_TITLE_OFFICIALITY_SOURCE, EXCEL_SHEET_TITLE_STORAGE_PATH
                            ]}

        self.txt_help_page.setHtml(self.help_strings.DLG_IMPORT_FROM_EXCEL)
        self.txt_help_page.anchorClicked.connect(self.save_template)

        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.rejected)
        self.buttonBox.helpRequested.connect(self.show_help)
        self.btn_browse_file.clicked.connect(
            make_file_selector(self.txt_excel_path,
                               QCoreApplication.translate("DialogImportFromExcel",
                                                          "Select the Excel file with data in the intermediate structure"),
                               QCoreApplication.translate("DialogImportFromExcel",
                                                                      'Excel File (*.xlsx *.xls)')))
        self.buttonBox.button(QDialogButtonBox.Ok).setText(QCoreApplication.translate("DialogImportFromExcel", "Import"))

        self.progress.setVisible(False)
        self.restore_settings()

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.setLayout(QGridLayout())
        # self.tabWidget.currentWidget().layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

    def accepted(self):
        self.save_settings()
        self.import_from_excel()

    def import_from_excel(self):
        steps = 18
        step = 0
        self.progress.setVisible(True)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        # Where to store the reports?
        excel_path = self.txt_excel_path.text()

        if not excel_path:
            self.show_message(
                QCoreApplication.translate("DialogImportFromExcel", "You need to select an Excel file before continuing with the import."),
                Qgis.Warning)
            self.progress.setVisible(False)
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
            return

        if not os.path.exists(excel_path):
            self.show_message(
                QCoreApplication.translate("DialogImportFromExcel", "The specified Excel file does not exist!"),
                Qgis.Warning)
            self.progress.setVisible(False)
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
            return

        self.progress.setVisible(True)
        self.txt_log.setText(QCoreApplication.translate("DialogImportFromExcel", "Loading tables from the Excel file..."))

        # Now that we have the Excel file, build vrts to load its sheets appropriately
        # Also validate each layer against a number of rules
        layer_parcel = self.check_layer_from_excel_sheet(excel_path, EXCEL_SHEET_NAME_PLOT)
        layer_party = self.check_layer_from_excel_sheet(excel_path, EXCEL_SHEET_NAME_PARTY)
        layer_group_party = self.check_layer_from_excel_sheet(excel_path, EXCEL_SHEET_NAME_GROUP)
        layer_right = self.check_layer_from_excel_sheet(excel_path, EXCEL_SHEET_NAME_RIGHT)

        if layer_parcel is None or layer_party is None or layer_group_party is None or layer_right is None:
            # A layer is None if at least an error was found
            self.group_parties_exists = False
            self.log_excel_show_message_emitted.emit(self.log_dialog_excel_text_content)
            self.done(0)
            return

        if not layer_group_party.isValid() or not layer_party.isValid() or not layer_parcel.isValid() or not layer_right.isValid():
            self.show_message(
                QCoreApplication.translate("DialogImportFromExcel", "One of the sheets of the Excel file couldn't be loaded! Check the format again."),
                Qgis.Warning)
            self.progress.setVisible(False)
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
            return

        QgsProject.instance().addMapLayers([layer_group_party, layer_party, layer_parcel, layer_right])

        self.txt_log.setText(QCoreApplication.translate("DialogImportFromExcel", "Loading LADM_COL tables..."))
        step += 1
        self.progress.setValue(step/steps * 100)

        # GET LADM LAYERS
        layers = {
            COL_PARTY_TABLE: {'name': COL_PARTY_TABLE, 'geometry': None, LAYER: None},
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None, LAYER: None},
            RIGHT_TABLE: {'name': RIGHT_TABLE, 'geometry': None, LAYER: None},
            EXTFILE_TABLE: {'name': EXTFILE_TABLE, 'geometry': None, LAYER: None},
            RRR_SOURCE_RELATION_TABLE: {'name': RRR_SOURCE_RELATION_TABLE, 'geometry': None, LAYER: None},
            LA_GROUP_PARTY_TABLE: {'name': LA_GROUP_PARTY_TABLE, 'geometry': None, LAYER: None},
            MEMBERS_TABLE: {'name': MEMBERS_TABLE, 'geometry': None, LAYER: None},
            ADMINISTRATIVE_SOURCE_TABLE: {'name': ADMINISTRATIVE_SOURCE_TABLE, 'geometry': None, LAYER: None}
        }

        self.qgis_utils.get_layers(self._db, layers, load=True)
        if not layers:
            return None

        # Get feature counts to compare after the ETL and know how many records were imported to each ladm_col table
        ladm_tables = [layers[PARCEL_TABLE][LAYER],
                       layers[COL_PARTY_TABLE][LAYER],
                       layers[RIGHT_TABLE][LAYER],
                       layers[ADMINISTRATIVE_SOURCE_TABLE][LAYER],
                       layers[RRR_SOURCE_RELATION_TABLE][LAYER],
                       layers[LA_GROUP_PARTY_TABLE][LAYER],
                       layers[MEMBERS_TABLE][LAYER]]
        ladm_tables_feature_count_before = {t.name(): t.featureCount() for t in ladm_tables}


        # Run the ETL
        # 1
        self.txt_log.setText(QCoreApplication.translate("DialogImportFromExcel", "ETL (step 1): Load col_interesado data..."))
        step += 1
        self.progress.setValue(step / steps * 100)

        processing.run("model:ETL-model",
                       {
                           'INPUT': layer_party,
                           'mapping': [
                               {'expression': '"numero de documento"', 'length': 12, 'name': 'documento_identidad',
                                'precision': -1, 'type': 10},
                               {'expression': '"tipo documento"', 'length': 255, 'name': 'tipo_documento',
                                'precision': -1, 'type': 10},
                               {'expression': '"organo_emisor"', 'length': 20, 'name': 'organo_emisor', 'precision': -1,
                                'type': 10},
                               {'expression': '"fecha_emision"', 'length': -1, 'name': 'fecha_emision', 'precision': -1,
                                'type': 14},
                               {'expression': '"apellido1"', 'length': 100, 'name': 'primer_apellido', 'precision': -1,
                                'type': 10},
                               {'expression': '"nombre1"', 'length': 100, 'name': 'primer_nombre', 'precision': -1,
                                'type': 10},
                               {'expression': '"apellido2"', 'length': 100, 'name': 'segundo_apellido', 'precision': -1,
                                'type': 10},
                               {'expression': '"nombre2"', 'length': 100, 'name': 'segundo_nombre', 'precision': -1,
                                'type': 10},
                               {'expression': '"razon social"', 'length': 250, 'name': 'razon_social', 'precision': -1,
                                'type': 10},
                               {'expression': '"sexo persona"', 'length': 255, 'name': 'genero', 'precision': -1,
                                'type': 10},
                               {'expression': '"tipo_interesado_juridico"', 'length': 255,
                                'name': 'tipo_interesado_juridico', 'precision': -1, 'type': 10},
                               {'expression': '"nombre"', 'length': 255, 'name': 'nombre', 'precision': -1, 'type': 10},
                               {'expression': '"tipo persona"', 'length': 255, 'name': 'tipo', 'precision': -1,
                                'type': 10},
                               {'expression': "'ANT_COL_INTERESADO'", 'length': 255, 'name': 'p_espacio_de_nombres',
                                'precision': -1, 'type': 10},
                               {'expression': '$id', 'length': 255, 'name': 'p_local_id', 'precision': -1, 'type': 10},
                               {'expression': 'now()', 'length': -1, 'name': 'comienzo_vida_util_version',
                                'precision': -1, 'type': 16},
                               {'expression': '"fin_vida_util_version"', 'length': -1, 'name': 'fin_vida_util_version',
                                'precision': -1, 'type': 16}],
                           'output': layers[COL_PARTY_TABLE][LAYER]
                       })

        # 2
        self.txt_log.setText(
            QCoreApplication.translate("DialogImportFromExcel", "ETL (step 2): Define group parties..."))
        step += 1
        self.progress.setValue(step / steps * 100)

        pre_group_party_layer = processing.run("qgis:statisticsbycategories",
                                   { 'CATEGORIES_FIELD_NAME': 'id agrupación',
                                      'INPUT': layer_group_party,
                                     'OUTPUT': 'memory:',
                                     'VALUES_FIELD_NAME': None })['OUTPUT']

        # 3
        self.txt_log.setText(
            QCoreApplication.translate("DialogImportFromExcel", "ETL (step 3): Load group parties..."))
        step += 1
        self.progress.setValue(step / steps * 100)

        processing.run("model:ETL-model",
                       {
                           'INPUT': pre_group_party_layer,
                           'mapping': [
                               {'expression': "'Grupo_Civil'", 'length': 255, 'name': 'ai_tipo', 'precision': -1, 'type': 10},
                               {'expression': '"nombre"', 'length': 255, 'name': 'nombre', 'precision': -1, 'type': 10},
                               {'expression': "'Otro'", 'length': 255, 'name': 'tipo', 'precision': -1, 'type': 10},
                               {'expression': "'ANT_Agrupacion_Interesados'", 'length': 255, 'name': 'p_espacio_de_nombres', 'precision': -1, 'type': 10},
                               {'expression': '"id agrupación"', 'length': 255, 'name': 'p_local_id', 'precision': -1, 'type': 10},
                               {'expression': 'now()', 'length': -1, 'name': 'comienzo_vida_util_version', 'precision': -1, 'type': 16},
                               {'expression': '"fin_vida_util_version"', 'length': -1, 'name': 'fin_vida_util_version', 'precision': -1, 'type': 16}],
                           'output': layers[LA_GROUP_PARTY_TABLE][LAYER]
                       })

        # 4
        self.txt_log.setText(
            QCoreApplication.translate("DialogImportFromExcel", "ETL (step 4): Join group parties t_id..."))
        step += 1
        self.progress.setValue(step / steps * 100)
        group_party_tid_layer = processing.run("native:joinattributestable",
                                               {  'DISCARD_NONMATCHING': False,
                                                  'FIELD': 'id agrupación',
                                                  'FIELDS_TO_COPY': 't_id',
                                                  'FIELD_2': 'p_local_id',
                                                  'INPUT': layer_group_party,
                                                  'INPUT_2': layers[LA_GROUP_PARTY_TABLE][LAYER],
                                                  'METHOD': 1,
                                                  'OUTPUT': 'memory:',
                                                  'PREFIX': 'agrupacion_' })['OUTPUT']

        # 5
        self.txt_log.setText(
            QCoreApplication.translate("DialogImportFromExcel", "ETL (step 5): Join group parties with parties..."))
        step += 1
        self.progress.setValue(step / steps * 100)
        group_party_party_tid_layer = processing.run("native:joinattributestable",
                                                     { 	'DISCARD_NONMATCHING': False,
                                                          'FIELD': 'numero de documento',
                                                          'FIELDS_TO_COPY': 't_id',
                                                          'FIELD_2': 'documento_identidad',
                                                          'INPUT': group_party_tid_layer,
                                                          'INPUT_2': layers[COL_PARTY_TABLE][LAYER],
                                                          'METHOD': 1,
                                                          'OUTPUT': 'memory:',
                                                          'PREFIX': 'interesado_' })['OUTPUT']

        # 6
        self.txt_log.setText(
            QCoreApplication.translate("DialogImportFromExcel", "ETL (step 6): Load group party members..."))
        step += 1
        self.progress.setValue(step / steps * 100)
        processing.run("model:ETL-model",
                       {
                           'INPUT': group_party_party_tid_layer,
                           'mapping': [
                               {'expression': '"interesado_t_id"', 'length': -1, 'name': 'interesados_col_interesado', 'precision': 0, 'type': 4},
                               {'expression': '"agrupacion_t_id"', 'length': -1, 'name': 'agrupacion', 'precision': 0, 'type': 4}],
                           'output': layers[MEMBERS_TABLE][LAYER]
                       })

        # 7
        self.txt_log.setText(
            QCoreApplication.translate("DialogImportFromExcel", "ETL (step 7): Load parcels..."))
        step += 1
        self.progress.setValue(step / steps * 100)
        processing.run("model:ETL-model",
                       {
                           'INPUT': layer_parcel,
                           'mapping': [
                               {'expression': '"departamento"', 'length': 2, 'name': 'departamento', 'precision': -1, 'type': 10},
                               {'expression': '"municipio"', 'length': 3, 'name': 'municipio', 'precision': -1, 'type': 10},
                               {'expression': '"zona"', 'length': 2, 'name': 'zona', 'precision': -1, 'type': 10},
                               {'expression': '$id', 'length': 20, 'name': 'nupre', 'precision': -1, 'type': 10},
                               {'expression': '"matricula predio"', 'length': 80, 'name': 'fmi', 'precision': -1, 'type': 10},
                               {'expression': '"numero predial nuevo"', 'length': 30, 'name': 'numero_predial', 'precision': -1, 'type': 10},
                               {'expression': '"numero predial viejo"', 'length': 20, 'name': 'numero_predial_anterior', 'precision': -1, 'type': 10},
                               {'expression': '"avaluo"', 'length': 16, 'name': 'avaluo_predio', 'precision': 1, 'type': 6},
                               {'expression': '"copropiedad"', 'length': -1, 'name': 'copropiedad', 'precision': 0, 'type': 4},
                               {'expression': '"nombre predio"', 'length': 255, 'name': 'nombre', 'precision': -1, 'type': 10},
                               {'expression': '"tipo predio"', 'length': 255, 'name': 'tipo', 'precision': -1, 'type': 10},
                               {'expression': "'ANT_PREDIO'", 'length': 255, 'name': 'u_espacio_de_nombres', 'precision': -1, 'type': 10},
                               {'expression': '$id', 'length': 255, 'name': 'u_local_id', 'precision': -1, 'type': 10},
                               {'expression': 'now()', 'length': -1, 'name': 'comienzo_vida_util_version', 'precision': -1, 'type': 16}],
                           'output': layers[PARCEL_TABLE][LAYER]
                       })

        # 8
        self.txt_log.setText(
            QCoreApplication.translate("DialogImportFromExcel", "ETL (step 8): Concatenate Rights and Sources fields..."))
        step += 1
        self.progress.setValue(step / steps * 100)
        concat_right_source_layer = processing.run("qgis:fieldcalculator",
                                                   { 	'FIELD_LENGTH': 100,
                                                        'FIELD_NAME': 'concat_',
                                                        'FIELD_PRECISION': 3,
                                                        'FIELD_TYPE': 2,
                                                        'FORMULA': 'concat( \"número documento interesado\" , \"agrupacion\" , \"numero predial nuevo\" , \"tipo de fuente\" , \"Descricpión de la fuente\")',
                                                        'INPUT': layer_right,
                                                        'NEW_FIELD': True,
                                                        'OUTPUT': 'memory:' })['OUTPUT']

        # 9
        self.txt_log.setText(
            QCoreApplication.translate("DialogImportFromExcel",
                                       "ETL (step 9): Load Administrative Sources..."))
        step += 1
        self.progress.setValue(step / steps * 100)
        processing.run("model:ETL-model",
                       {
                           'INPUT': concat_right_source_layer,
                           'mapping': [
                               {'expression': '"Descripción de la fuente"', 'length': 255, 'name': 'texto', 'precision': -1, 'type': 10},
                               {'expression': '"tipo de fuente"', 'length': 255, 'name': 'tipo', 'precision': -1, 'type': 10},
                               {'expression': '"codigo_registral_transaccion"', 'length': 5, 'name': 'codigo_registral_transaccion', 'precision': -1, 'type': 10},
                               {'expression': '"nombre"', 'length': 50, 'name': 'nombre', 'precision': -1, 'type': 10},
                               {'expression': '"fecha_aceptacion"', 'length': -1, 'name': 'fecha_aceptacion', 'precision': -1, 'type': 16},
                               {'expression': '"estado_disponibilidad de la fuente"', 'length': 255, 'name': 'estado_disponibilidad', 'precision': -1, 'type': 10},
                               {'expression': '"sello_inicio_validez"', 'length': -1, 'name': 'sello_inicio_validez', 'precision': -1, 'type': 16},
                               {'expression': '"tipo_principal"', 'length': 255, 'name': 'tipo_principal', 'precision': -1, 'type': 10},
                               {'expression': '"fecha_grabacion"', 'length': -1, 'name': 'fecha_grabacion', 'precision': -1, 'type': 16},
                               {'expression': '"fecha_entrega"', 'length': -1, 'name': 'fecha_entrega', 'precision': -1, 'type': 16},
                               {'expression': "'ANT_COLFUENTEADMINISTRATIVA'", 'length': 255, 'name': 's_espacio_de_nombres', 'precision': -1, 'type': 10},
                               {'expression': '"concat_"', 'length': 255, 'name': 's_local_id', 'precision': -1, 'type': 10},
                               {'expression': '"oficialidad"', 'length': -1, 'name': 'oficialidad', 'precision': -1, 'type': 1}],
                           'output': layers[ADMINISTRATIVE_SOURCE_TABLE][LAYER]
                       })

        # 10
        self.txt_log.setText(
            QCoreApplication.translate("DialogImportFromExcel",
                                       "ETL (step 10): Join concatenate source to administrative source t_id..."))
        step += 1
        self.progress.setValue(step / steps * 100)
        source_tid_layer = processing.run("native:joinattributestable",
                                          {	'DISCARD_NONMATCHING': False,
                                               'FIELD': 'concat_',
                                               'FIELDS_TO_COPY': 't_id',
                                               'FIELD_2': 's_local_id',
                                               'INPUT': concat_right_source_layer,
                                               'INPUT_2': layers[ADMINISTRATIVE_SOURCE_TABLE][LAYER],
                                               'METHOD': 1,
                                               'OUTPUT': 'memory:',
                                               'PREFIX': 'fuente_' })['OUTPUT']

        # 11
        self.txt_log.setText(
            QCoreApplication.translate("DialogImportFromExcel",
                                       "ETL (step 11): Load extarchivo..."))
        step += 1
        self.progress.setValue(step / steps * 100)
        processing.run("model:ETL-model",
                       {
                           'INPUT': source_tid_layer,
                           'mapping': [
                               {'expression': '"fecha_aceptacion"', 'length': -1, 'name': 'fecha_aceptacion', 'precision': -1, 'type': 14},
                               {'expression': '"Ruta de Almacenamiento de la fuente"', 'length': 255, 'name': 'datos', 'precision': -1, 'type': 10},
                               {'expression': '"extraccion"', 'length': -1, 'name': 'extraccion', 'precision': -1, 'type': 14},
                               {'expression': '"fecha_grabacion"', 'length': -1, 'name': 'fecha_grabacion', 'precision': -1, 'type': 14},
                               {'expression': '"fecha_entrega"', 'length': -1, 'name': 'fecha_entrega', 'precision': -1, 'type': 14},
                               {'expression': "'ANT_EXTARCHIVO'", 'length': 255, 'name': 's_espacio_de_nombres', 'precision': -1, 'type': 10},
                               {'expression': '$id', 'length': 255, 'name': 's_local_id', 'precision': -1, 'type': 10},
                               {'expression': '"fuente_t_id"', 'length': -1, 'name': 'col_fuenteadminstrtiva_ext_archivo_id', 'precision': 0, 'type': 4},
                               {'expression': '"col_fuenteespacial_ext_archivo_id"', 'length': -1, 'name': 'col_fuenteespacial_ext_archivo_id', 'precision': 0, 'type': 4}],
                           'output': EXTFILE_TABLE
                       })

        # 12
        self.txt_log.setText(
            QCoreApplication.translate("DialogImportFromExcel",
                                       "ETL (step 12): Join source and party t_id..."))
        step += 1
        self.progress.setValue(step / steps * 100)
        source_party_tid_layer = processing.run("native:joinattributestable",
                                                { 	'DISCARD_NONMATCHING': False,
                                                     'FIELD': 'número documento Interesado',
                                                     'FIELDS_TO_COPY': 't_id',
                                                     'FIELD_2': 'documento_identidad',
                                                     'INPUT': source_tid_layer,
                                                     'INPUT_2': layers[COL_PARTY_TABLE][LAYER],
                                                     'METHOD': 1,
                                                     'OUTPUT': 'memory:',
                                                     'PREFIX': 'interesado_'})['OUTPUT']

        # 13
        self.txt_log.setText(
            QCoreApplication.translate("DialogImportFromExcel",
                                       "ETL (step 13): Join source, party, group party t_id..."))
        step += 1
        self.progress.setValue(step / steps * 100)
        source_party_group_tid_layer = processing.run("native:joinattributestable",
                                                      {    'DISCARD_NONMATCHING': False,
                                                           'FIELD': 'agrupación',
                                                           'FIELDS_TO_COPY': 't_id',
                                                           'FIELD_2': 'p_local_id',
                                                           'INPUT': source_party_tid_layer,
                                                           'INPUT_2': layers[LA_GROUP_PARTY_TABLE][LAYER],
                                                           'METHOD': 1,
                                                           'OUTPUT': 'memory:',
                                                           'PREFIX': 'agrupacion_' })['OUTPUT']

        # 14
        self.txt_log.setText(
            QCoreApplication.translate("DialogImportFromExcel",
                                       "ETL (step 14): Join source, party, group party, parcel t_id..."))
        step += 1
        self.progress.setValue(step / steps * 100)
        source_party_group_parcel_tid_layer = processing.run("native:joinattributestable",
                                                             { 	'DISCARD_NONMATCHING': False,
                                                                  'FIELD': 'numero predial nuevo',
                                                                  'FIELDS_TO_COPY': 't_id',
                                                                  'FIELD_2': 'numero_predial',
                                                                  'INPUT': source_party_group_tid_layer,
                                                                  'INPUT_2': layers[PARCEL_TABLE][LAYER],
                                                                  'METHOD': 1,
                                                                  'OUTPUT': 'memory:',
                                                                  'PREFIX': 'predio_' })['OUTPUT']

        # 15
        self.txt_log.setText(
            QCoreApplication.translate("DialogImportFromExcel",
                                       "ETL (step 15): Load Rights..."))
        step += 1
        self.progress.setValue(step / steps * 100)
        processing.run("model:ETL-model",
                       {
                           'INPUT': source_party_group_parcel_tid_layer,
                           'mapping': [
                               {'expression': '"tipo"', 'length': 255, 'name': 'tipo', 'precision': -1, 'type': 10},
                               {'expression': '"codigo_registral_derecho"', 'length': 5, 'name': 'codigo_registral_derecho', 'precision': -1, 'type': 10},
                               {'expression': '"descripcion"', 'length': 255, 'name': 'descripcion', 'precision': -1, 'type': 10},
                               {'expression': '"comprobacion_comparte"', 'length': -1, 'name': 'comprobacion_comparte', 'precision': -1, 'type': 1},
                               {'expression': '"uso_efectivo"', 'length': 255, 'name': 'uso_efectivo', 'precision': -1, 'type': 10},
                               {'expression': "'ANT_Col_Derecho'", 'length': 255, 'name': 'r_espacio_de_nombres', 'precision': -1, 'type': 10},
                               {'expression': '"concat_"', 'length': 255, 'name': 'r_local_id', 'precision': -1, 'type': 10},
                               {'expression': '"agrupacion_t_id"', 'length': -1, 'name': 'interesado_la_agrupacion_interesados', 'precision': 0, 'type': 4},
                               {'expression': '"interesado_t_id"', 'length': -1, 'name': 'interesado_col_interesado', 'precision': 0, 'type': 4},
                               {'expression': '"unidad_la_baunit"', 'length': -1, 'name': 'unidad_la_baunit', 'precision': 0, 'type': 4},
                               {'expression': '"predio_t_id"', 'length': -1, 'name': 'unidad_predio', 'precision': 0, 'type': 4},
                               {'expression': 'now()', 'length': -1, 'name': 'comienzo_vida_util_version', 'precision': -1, 'type': 16},
                               {'expression': '"fin_vida_util_version"', 'length': -1, 'name': 'fin_vida_util_version', 'precision': -1, 'type': 16}],
                           'output': layers[RIGHT_TABLE][LAYER]
                       })

        # 16
        self.txt_log.setText(
            QCoreApplication.translate("DialogImportFromExcel",
                                       "ETL (step 16): Join source, party, group party, parcel, right t_id..."))
        step += 1
        self.progress.setValue(step / steps * 100)
        source_party_group_parcel_right_tid_layer = processing.run("native:joinattributestable",
                                                                   { 	'DISCARD_NONMATCHING': False,
                                                                        'FIELD': 'concat_',
                                                                        'FIELDS_TO_COPY': 't_id',
                                                                        'FIELD_2': 'r_local_id',
                                                                        'INPUT': source_party_group_parcel_tid_layer,
                                                                        'INPUT_2': layers[RIGHT_TABLE][LAYER],
                                                                        'METHOD': 1,
                                                                        'OUTPUT': 'memory:',
                                                                        'PREFIX': 'derecho_' })['OUTPUT']

        # 17
        self.txt_log.setText(
            QCoreApplication.translate("DialogImportFromExcel",
                                       "ETL (step 17): Load rrrfuente..."))
        step += 1
        self.progress.setValue(step / steps * 100)
        processing.run("model:ETL-model",
                       {
                           'INPUT': source_party_group_parcel_right_tid_layer,
                           'mapping': [
                               {'expression': '"fuente_t_id"', 'length': -1, 'name': 'rfuente', 'precision': 0, 'type': 4},
                               {'expression': '"rrr_col_responsabilidad"', 'length': -1, 'name': 'rrr_col_responsabilidad', 'precision': 0, 'type': 4},
                               {'expression': '"derecho_t_id"', 'length': -1, 'name': 'rrr_col_derecho', 'precision': 0, 'type': 4},
                               {'expression': '"rrr_col_restriccion"', 'length': -1, 'name': 'rrr_col_restriccion', 'precision': 0, 'type': 4},
                               {'expression': '"rrr_col_hipoteca"', 'length': -1, 'name': 'rrr_col_hipoteca', 'precision': 0, 'type': 4}],
                           'output': layers[RRR_SOURCE_RELATION_TABLE][LAYER]
                       })


        # Print summary getting feature count in involved LADM_COL tables...
        summary = """<html><head/><body><p>"""
        summary += QCoreApplication.translate("DialogImportFromExcel", "Import done!!!<br/>")
        for table in ladm_tables:
            summary += QCoreApplication.translate(
                        "DialogImportFromExcel",
                        "<br/><b>{count}</b> records loaded into table <b>{table}</b>").format(
                            count=table.featureCount() - ladm_tables_feature_count_before[table.name()],
                            table=table.name())

        summary += """</body></html>"""
        self.txt_log.setText(summary)
        self.qgis_utils.message_with_duration_emitted.emit(
            QCoreApplication.translate("QGISUtils",
                                       "Data successfully imported to LADM_COL from intermediate structure (Excel file: '{}')!!!").format(
                excel_path),
            Qgis.Success,
            0)

    def check_layer_from_excel_sheet(self, excel_path, sheetname):
        layer = self.get_layer_from_excel_sheet(excel_path, sheetname)
        error_counter = 0

        if layer is None and sheetname != EXCEL_SHEET_NAME_GROUP: # optional sheet
            self.generate_message_excel_error(QCoreApplication.translate("DialogImportFromExcel", 
                    "The {} sheet has not information or has another name.").format(sheetname))
            error_counter += 1
        else:
            title_validator = layer.fields().toList()

        if sheetname == EXCEL_SHEET_NAME_PLOT and layer is not None:
            if not title_validator:
                self.generate_message_excel_error(QCoreApplication.translate("DialogImportFromExcel", 
                        "The title does not match the format in the sheet {}.").format(sheetname))
                error_counter += 1
            if list(layer.getFeatures('"numero predial nuevo" is Null')):
                self.generate_message_excel_error(QCoreApplication.translate("DialogImportFromExcel", 
                        "The column numero predial nuevo has empty values in sheet {}.").format(sheetname))
                error_counter += 1    
            if not self.check_field_numeric_layer(layer, 'departamento'):
                self.generate_message_excel_error(QCoreApplication.translate("DialogImportFromExcel", 
                        "The column departamento has non-numeric values in sheet {}.").format(sheetname))
                error_counter += 1
            if not self.check_field_numeric_layer(layer, 'municipio'):
                self.generate_message_excel_error(QCoreApplication.translate("DialogImportFromExcel", 
                        "The column municipio has non-numeric values in sheet {}.").format(sheetname))
                error_counter += 1
            if not self.check_field_numeric_layer(layer, 'numero predial nuevo'):
                self.generate_message_excel_error(QCoreApplication.translate("DialogImportFromExcel", 
                        "The column numero predial nuevo has non-numeric values in sheet {}.").format(sheetname))
                error_counter += 1

        if sheetname == EXCEL_SHEET_NAME_PARTY and layer is not None:
            if not title_validator:
                self.generate_message_excel_error(QCoreApplication.translate("DialogImportFromExcel", 
                        "The title does not match the format in sheet {}.").format(sheetname))
                error_counter += 1
            if list(layer.getFeatures('"tipo documento" is Null')):
                self.generate_message_excel_error(QCoreApplication.translate("DialogImportFromExcel", 
                        "The column tipo documento has empty values in sheet {}.").format(sheetname))
                error_counter += 1
            if list(layer.getFeatures('"numero de documento" is Null')):
                self.generate_message_excel_error(QCoreApplication.translate("DialogImportFromExcel", 
                        "The column numero de documento has empty values in sheet {}.").format(sheetname))
                error_counter += 1
            if not self.check_length_attribute_value(layer, 'numero de documento', 12):
                self.generate_message_excel_error(QCoreApplication.translate("DialogImportFromExcel", 
                        "The column numero de documento has more characters than expected in sheet {}.").format(sheetname))
                error_counter += 1
            if list(layer.getFeatures('"tipo persona" is Null')):
                self.generate_message_excel_error(QCoreApplication.translate("DialogImportFromExcel", 
                        "The column tipo persona has empty values in sheet {}.").format(sheetname))
                error_counter += 1

        if sheetname == EXCEL_SHEET_NAME_GROUP and layer is not None:
            if not title_validator:
                self.generate_message_excel_error(QCoreApplication.translate("DialogImportFromExcel", 
                        "The title does not match the format in the sheet {}.").format(sheetname))
                error_counter += 1
            self.group_parties_exists = True
            if list(layer.getFeatures('"numero predial nuevo" is Null')):
                self.generate_message_excel_error(QCoreApplication.translate("DialogImportFromExcel", 
                        "The column numero predial nuevo has empty values in sheet {}.").format(sheetname))
                error_counter += 1
            if list(layer.getFeatures('"tipo documento" is Null')):
                self.generate_message_excel_error(QCoreApplication.translate("DialogImportFromExcel", 
                        "The column tipo documento has empty values in sheet {}.").format(sheetname))
                error_counter += 1
            if list(layer.getFeatures('"numero de documento" is Null')):
                self.generate_message_excel_error(QCoreApplication.translate("DialogImportFromExcel", 
                        "The column numero de documento has empty values in sheet {}.").format(sheetname))
                error_counter += 1
            if list(layer.getFeatures('"id agrupación" is Null')):
                self.generate_message_excel_error(QCoreApplication.translate("DialogImportFromExcel", 
                        "The column id agrupación has empty values in sheet {}.").format(sheetname))
                error_counter += 1
            if not self.check_length_attribute_value(layer, 'numero de documento', 12):
                self.generate_message_excel_error(QCoreApplication.translate("DialogImportFromExcel", 
                        "The column numero de documento has more characters of the permitted in sheet {}.").format(sheetname))
                error_counter += 1

        if sheetname == EXCEL_SHEET_NAME_RIGHT and layer is not None:
            if not title_validator:
                self.generate_message_excel_error(QCoreApplication.translate("DialogImportFromExcel", 
                        "The title does not match the format in sheet {}.").format(sheetname))
                error_counter += 1
            if list(layer.getFeatures('"tipo" is Null')):
                self.generate_message_excel_error(QCoreApplication.translate("DialogImportFromExcel", 
                        "The column tipo has empty values in sheet {}.").format(sheetname))
                error_counter += 1
            if list(layer.getFeatures('"tipo de fuente" is Null')):
                self.generate_message_excel_error(QCoreApplication.translate("DialogImportFromExcel", 
                        "The column tipo de fuente has empty values in sheet {}.").format(sheetname))
                error_counter += 1
            if list(layer.getFeatures('"estado_disponibilidad de la fuente" is Null')):
                self.generate_message_excel_error(QCoreApplication.translate("DialogImportFromExcel", 
                        "The column estado_disponibilidad de la fuente has empty values in sheet {}.").format(sheetname))
                error_counter += 1
            #if list(layer.getFeatures('"Ruta de Almacenamiento de la fuente" is Null')):
            #    self.generate_message_excel_error(QCoreApplication.translate("DialogImportFromExcel",
            #            "The column Ruta de Almacenamiento de la fuente has empty values in sheet {}.").format(sheetname))
            #    error_counter += 1
            if len(list(layer.getFeatures('"número documento Interesado" is Null'))) + len(list(layer.getFeatures('"agrupación" is Null'))) != layer.featureCount():
                self.generate_message_excel_error(QCoreApplication.translate("DialogImportFromExcel", 
                        "Number of non-null parties plus number of non-null group parties is not equal to number of records in sheet {}. There might be rights without party or group party associated.").format(sheetname))
                error_counter += 1
            if not self.group_parties_exists:
                if list(layer.getFeatures('"número documento Interesado" is Null')):
                    self.generate_message_excel_error(QCoreApplication.translate("DialogImportFromExcel", 
                            "The column número documento Interesado has empty values in sheet {}.").format(sheetname))
                    error_counter += 1
                if len(list(layer.getFeatures('"agrupacion" is Null'))) != layer.featureCount():
                    self.generate_message_excel_error(QCoreApplication.translate("DialogImportFromExcel", 
                        "The column agrupacion has data but the sheet does not exist in sheet {}.").format(sheetname))
                    error_counter += 1

        return layer if error_counter == 0 else None

    def check_field_numeric_layer(self, layer, name):
        id_field_idx = layer.fields().indexFromName(name)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
        features = layer.getFeatures(request)
        is_numeric = True

        for feature in features:
            try:
                int(feature[name])
            except:
                is_numeric = False
                break

        return is_numeric

    def check_length_attribute_value(self, layer, name, size):
        id_field_idx = layer.fields().indexFromName(name)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
        features = layer.getFeatures(request)
        right_length = True

        for feature in features:
            if len(str(feature[name])) > size:
                right_length = False
                break

        return right_length

    def generate_message_excel_error(self, msg):
        self.log_dialog_excel_text_content += "{}{}{}{}{}{}".format(LOG_QUALITY_LIST_CONTAINER_OPEN,
                                                                    LOG_QUALITY_LIST_ITEM_ERROR_OPEN,
                                                                    msg,
                                                                    LOG_QUALITY_LIST_ITEM_ERROR_CLOSE,
                                                                    LOG_QUALITY_LIST_CONTAINER_CLOSE,
                                                                    LOG_QUALITY_CONTENT_SEPARATOR)

    def get_layer_from_excel_sheet(self, excel_path, sheetname):
        basename = os.path.basename(excel_path)
        filename = os.path.splitext(basename)[0]
        dirname = os.path.dirname(excel_path)

        header_in_first_row, count = self.get_excel_info(excel_path, sheetname)
        if header_in_first_row is None and count is None:
            return None     

        layer_definition = "<SrcLayer>{sheetname}</SrcLayer>".format(sheetname=sheetname)
        if header_in_first_row:
            layer_definition = """<SrcSql dialect="sqlite">SELECT * FROM '{sheetname}' LIMIT {count} OFFSET 1</SrcSql>""".format(sheetname=sheetname, count=count)
        xml_text_group_party = """<?xml version="1.0" encoding="UTF-8"?>
                    <OGRVRTDataSource>
                        <OGRVRTLayer name="{filename}-{sheetname}">
                            <SrcDataSource relativeToVRT="1">{basename}</SrcDataSource>
                            <!--Header={header}-->
                            {layer_definition}
                            {fields}
                        </OGRVRTLayer>            
                    </OGRVRTDataSource>
                """.format(filename=filename,
                           basename=basename,
                           header=header_in_first_row,
                           layer_definition=layer_definition,
                           sheetname=sheetname,
                           fields=self.get_vrt_fields(sheetname, header_in_first_row))

        group_party_file_path = os.path.join(dirname, '{}.{}.vrt'.format(basename, sheetname))
        with open(group_party_file_path, 'w') as sheet:
            sheet.write(xml_text_group_party)

        uri = '{vrtfilepath}|layername={filename}-{sheetname}'.format(vrtfilepath=group_party_file_path,
                                                                      sheetname=sheetname, filename=filename)

        self.log.logMessage("Loading layer from excel with uri='{}'".format(uri), PLUGIN_NAME, Qgis.Info)
        layer = QgsVectorLayer(uri, '{}-{}'.format('excel', sheetname), 'ogr')
        layer.setProviderEncoding('UTF-8')
        return layer

    def get_excel_info(self, path, sheetname):
        data_source = ogr.Open(path, 0)
        layer = data_source.GetLayer(sheetname)

        if layer is None:
            # A sheetname couldn't be found
            return None, None

        feature = layer.GetNextFeature()

        # If ogr recognizes the header, the first row will contain data, otherwise it'll contain field names
        header_in_first_row = True
        for field in self.fields[sheetname]:
            if feature.GetField(self.fields[sheetname].index(field)) != field:
                header_in_first_row = False

        num_rows = layer.GetFeatureCount()
        return header_in_first_row, num_rows - 1 if header_in_first_row else num_rows

    def get_vrt_fields(self, sheetname, header_in_first_row):
        vrt_fields = ""
        for index, field in enumerate(self.fields[sheetname]):
            vrt_fields += """<Field name="{field}" src="{src}" type="String"/>\n""".format(
                field=field,
                src='Field{}'.format(index+1) if header_in_first_row else field)

        return vrt_fields.strip()

    def save_template(self, url):
        link = url.url()
        if link == '#template':
            self.download_excel_file('plantilla_estructura_excel.xlsx')
        elif link == '#data':
            self.download_excel_file('datos_estructura_excel.xlsx')

    def download_excel_file(self, filename):
        settings = QSettings()

        new_filename, filter = QFileDialog.getSaveFileName(self,
                                   QCoreApplication.translate("DialogImportFromExcel",
                                                              "Save File"),
                                   os.path.join(settings.value('Asistente-LADM_COL/import_from_excel_dialog/template_save_path', '.'), filename),
                                   QCoreApplication.translate("DialogImportFromExcel",
                                                              "Excel File (*.xlsx *.xls)"))

        if new_filename:
            settings.setValue('Asistente-LADM_COL/import_from_excel_dialog/template_save_path', os.path.dirname(new_filename))
            template_file = QFile(":/Asistente-LADM_COL/resources/excel/" + filename)

            if not template_file.exists():
                self.log.logMessage("Excel doesn't exist! Probably due to a missing 'make' execution to generate resources...", PLUGIN_NAME, Qgis.Critical)
                msg = QCoreApplication.translate("DialogImportFromExcel", "Excel file not found. Update your plugin. For details see log.")
                self.show_message(msg, Qgis.Warning)
                return

            if os.path.isfile(new_filename):
                self.log.logMessage('Removing existing file {}...'.format(new_filename), PLUGIN_NAME, Qgis.Info)
                os.chmod(new_filename, 0o777)
                os.remove(new_filename)

            if template_file.copy(new_filename):
                os.chmod(new_filename, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
                msg = QCoreApplication.translate("DialogImportFromExcel", """The file <a href="file:///{}">{}</a> was successfully saved!""").format(normalize_local_url(new_filename), os.path.basename(new_filename))
                self.show_message(msg, Qgis.Info)
            else:
                self.log.logMessage('There was an error copying the CSV file {}!'.format(new_filename), PLUGIN_NAME, Qgis.Info)
                msg = QCoreApplication.translate("DialogImportFromExcel", "The file couldn\'t be saved.")
                self.show_message(msg, Qgis.Warning)


    def rejected(self):
        self.selected_items_dict = dict()

    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/import_from_excel_dialog/excel_path', self.txt_excel_path.text())

    def restore_settings(self):
        settings = QSettings()
        self.txt_excel_path.setText(settings.value('Asistente-LADM_COL/import_from_excel_dialog/excel_path', ''))

    def show_message(self, message, level):
        self.bar.pushMessage(message, level, 10)

    def show_help(self):
        self.qgis_utils.show_help("import_from_excel")
