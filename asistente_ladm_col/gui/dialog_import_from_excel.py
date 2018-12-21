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
                       QgsProject, QgsApplication)
from qgis.PyQt.QtCore import (Qt,
                              QSettings,
                              QCoreApplication, QFile)
from qgis.gui import QgsMessageBar
import processing

from asistente_ladm_col import PLUGIN_NAME
from asistente_ladm_col.utils.qt_utils import make_file_selector, normalize_local_url
from asistente_ladm_col.utils.utils import get_number_of_rows_in_excel_file
from ..config.help_strings import HelpStrings
from qgis.PyQt.QtGui import (QBrush,
                             QFont,
                             QIcon)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QTreeWidgetItem,
                                 QLineEdit,
                                 QTreeWidgetItemIterator,
                                 QComboBox, QSizePolicy, QGridLayout, QDialogButtonBox, QFileDialog)

from ..config.table_mapping_config import (COL_PARTY_TABLE,
                                           PARCEL_TABLE,
                                           RIGHT_TABLE,
                                           RRR_SOURCE_RELATION_TABLE,
                                           EXTFILE_TABLE,
                                           LA_GROUP_PARTY_TABLE,
                                           ADMINISTRATIVE_SOURCE_TABLE,
                                           MEMBERS_TABLE)
from ..utils import get_ui_class

DIALOG_UI = get_ui_class('dlg_import_from_excel.ui')

class DialogImportFromExcel(QDialog, DIALOG_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self._db = db
        self.qgis_utils = qgis_utils
        self.log = QgsApplication.messageLog()
        self.help_strings = HelpStrings()

        self.fields = {'interesado': ['nombre1', 'nombre2', 'apellido1', 'apellido2', 'razon social', 'sexo persona',
                                 'tipo documento', 'numero de documento', 'tipo persona', 'organo emisor del documento',
                                 'fecha emision del documento'
                                 ],
                  'predio': ['departamento', 'municipio', 'zona', 'matricula predio', 'numero predial nuevo',
                             'numero predial viejo', 'nombre predio', 'avaluo', 'tipo predio'
                             ],
                  'agrupacion': ['numero predial nuevo', 'tipo documento', 'numero de documento', 'id agrupación'
                                 ],
                  'derecho': ['tipo', 'número documento Interesado', 'agrupación', 'numero predial nuevo',
                              'tipo de fuente', 'Descripción de la fuente', 'estado_disponibilidad de la fuente',
                              'Es oficial la fuente', 'Ruta de Almacenamiento de la fuente'
                              ]}

        self.txt_help_page.setHtml(self.help_strings.DLG_IMPORT_FROM_EXCEL)
        self.txt_help_page.anchorClicked.connect(self.save_template)

        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.rejected)
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
        layer_group_party = self.get_layer_from_excel_sheet(excel_path, 'agrupacion')
        layer_party = self.get_layer_from_excel_sheet(excel_path, 'interesado')
        layer_parcel = self.get_layer_from_excel_sheet(excel_path, 'predio')
        layer_right = self.get_layer_from_excel_sheet(excel_path, 'derecho')

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
        res_layers = self.qgis_utils.get_layers(self._db, {
            COL_PARTY_TABLE: {'name': COL_PARTY_TABLE, 'geometry': None},
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None},
            RIGHT_TABLE: {'name': RIGHT_TABLE, 'geometry': None},
            EXTFILE_TABLE: {'name': EXTFILE_TABLE, 'geometry': None},
            RRR_SOURCE_RELATION_TABLE: {'name': RRR_SOURCE_RELATION_TABLE, 'geometry': None},
            LA_GROUP_PARTY_TABLE: {'name': LA_GROUP_PARTY_TABLE, 'geometry': None},
            MEMBERS_TABLE: {'name': MEMBERS_TABLE, 'geometry': None},
            ADMINISTRATIVE_SOURCE_TABLE: {'name': ADMINISTRATIVE_SOURCE_TABLE, 'geometry': None}}, load=True)

        col_party_table = res_layers[COL_PARTY_TABLE]
        if col_party_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("QGISUtils",
                                                                           "Col_Party table couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return

        parcel_table = res_layers[PARCEL_TABLE]
        if parcel_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("QGISUtils",
                                                                           "Parcel table couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return

        right_table = res_layers[RIGHT_TABLE]
        if right_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("QGISUtils",
                                                                           "Right table couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return

        extfile_table = res_layers[EXTFILE_TABLE]
        if extfile_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("QGISUtils",
                                                                           "EXT_FILE table couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return

        rrr_source_table = res_layers[RRR_SOURCE_RELATION_TABLE]
        if rrr_source_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("QGISUtils",
                                                                           "RRR-SOURCE table couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return

        group_party_table = res_layers[LA_GROUP_PARTY_TABLE]
        if group_party_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("QGISUtils",
                                                                           "Group party table couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return

        members_table = res_layers[MEMBERS_TABLE]
        if members_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("QGISUtils",
                                                                           "Members table couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return

        administrative_source_table = res_layers[ADMINISTRATIVE_SOURCE_TABLE]
        if administrative_source_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("QGISUtils",
                                                                           "Administrative Source table couldn't be found... {}").format(
                                                    self._db.get_description()),
                                                Qgis.Warning)
            return


        # Get feature counts to compare after the ETL and know how many records were imported to each ladm_col table
        ladm_tables = [parcel_table,
                       col_party_table,
                       right_table,
                       administrative_source_table,
                       rrr_source_table,
                       group_party_table,
                       members_table]
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
                               {'expression': '"razon_social"', 'length': 250, 'name': 'razon_social', 'precision': -1,
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
                           'output': col_party_table
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
                           'output': group_party_table
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
                                                  'INPUT_2': group_party_table,
                                                  'METHOD': 1,
                                                  'OUTPUT': 'memory:',
                                                  'PREFIX': 'agrupacion_' })['OUTPUT']
        QgsProject.instance().addMapLayer(group_party_tid_layer)

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
                                                          'INPUT_2': col_party_table,
                                                          'METHOD': 1,
                                                          'OUTPUT': 'memory:',
                                                          'PREFIX': 'interesado_' })['OUTPUT']
        QgsProject.instance().addMapLayer(group_party_party_tid_layer)

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
                           'output': members_table
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
                           'output': parcel_table
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
                               {'expression': '"descripcion de la fuente"', 'length': 255, 'name': 'texto', 'precision': -1, 'type': 10},
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
                           'output': administrative_source_table
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
                                               'INPUT_2': administrative_source_table,
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
                                                     'INPUT_2': col_party_table,
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
                                                           'INPUT_2': group_party_table,
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
                                                                  'INPUT_2': parcel_table,
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
                           'output': right_table
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
                                                                        'INPUT_2': right_table,
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
                           'output': rrr_source_table
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

    def get_layer_from_excel_sheet(self, excel_path, sheetname):
        basename = os.path.basename(excel_path)
        filename = os.path.splitext(basename)[0]
        dirname = os.path.dirname(excel_path)

        header_in_first_row, count = self.get_excel_info(excel_path, sheetname)
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
            print(field, feature.GetField(self.fields[sheetname].index(field)) == field)
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
                                   QCoreApplication.translate('DialogImportFromExcel',
                                                              'Save File'),
                                   os.path.join(settings.value('Asistente-LADM_COL/import_from_excel_dialog/template_save_path', '.'), filename),
                                   QCoreApplication.translate('DialogImportFromExcel',
                                                              'Excel File (*.xlsx *.xls)'))

        if new_filename:
            settings.setValue('Asistente-LADM_COL/import_from_excel_dialog/template_save_path', os.path.dirname(new_filename))
            template_file = QFile(":/Asistente-LADM_COL/resources/excel/" + filename)

            if not template_file.exists():
                self.log.logMessage("Excel doesn't exist! Probably due to a missing 'make' execution to generate resources...", PLUGIN_NAME, Qgis.Critical)
                msg = QCoreApplication.translate('DialogImportFromExcel', 'Excel file not found. Update your plugin. For details see log.')
                self.show_message(msg, Qgis.Warning)
                return

            if os.path.isfile(new_filename):
                self.log.logMessage('Removing existing file {}...'.format(new_filename), PLUGIN_NAME, Qgis.Info)
                os.chmod(new_filename, 0o777)
                os.remove(new_filename)

            if template_file.copy(new_filename):
                os.chmod(new_filename, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
                msg = QCoreApplication.translate('DialogImportFromExcel', 'The file <a href="file:///{}">{}</a> was successfully saved!').format(normalize_local_url(new_filename), os.path.basename(new_filename))
                self.show_message(msg, Qgis.Info)
            else:
                self.log.logMessage('There was an error copying the CSV file {}!'.format(new_filename), PLUGIN_NAME, Qgis.Info)
                msg = QCoreApplication.translate('DialogImportFromExcel', 'The file couldn\'t be saved.')
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
