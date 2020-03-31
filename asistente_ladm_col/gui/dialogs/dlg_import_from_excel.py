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
                       QgsProcessingFeedback)
from qgis.PyQt.QtCore import (Qt,
                              QSettings,
                              QCoreApplication,
                              QFile,
                              pyqtSignal)
from qgis.gui import QgsMessageBar
import processing

from qgis.PyQt.QtWidgets import (QDialog,
                                 QSizePolicy,
                                 QDialogButtonBox,
                                 QMessageBox,
                                 QFileDialog)

from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.qt_utils import make_file_selector, normalize_local_url
from asistente_ladm_col.config.help_strings import HelpStrings
from asistente_ladm_col.config.general_config import (LOG_QUALITY_LIST_CONTAINER_OPEN,
                                                      LOG_QUALITY_LIST_ITEM_ERROR_OPEN,
                                                      LOG_QUALITY_LIST_ITEM_ERROR_CLOSE,
                                                      LOG_QUALITY_LIST_CONTAINER_CLOSE,
                                                      LOG_QUALITY_CONTENT_SEPARATOR)
from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.utils import show_plugin_help

DIALOG_UI = get_ui_class('dialogs/dlg_import_from_excel.ui')

# Excel titles
EXCEL_SHEET_NAME_PLOT = 'predio'
EXCEL_SHEET_NAME_PARTY = 'interesado'
EXCEL_SHEET_NAME_GROUP = 'agrupacion'
EXCEL_SHEET_NAME_RIGHT = 'derecho'
EXCEL_SHEET_TITLE_DEPARTMENT = 'departamento'
EXCEL_SHEET_TITLE_MUNICIPALITY = 'municipio'
EXCEL_SHEET_TITLE_ZONE = 'zona'
EXCEL_SHEET_TITLE_REGISTRATION_PLOT = 'matricula predio'
EXCEL_SHEET_TITLE_NPN = 'numero predial nuevo'
EXCEL_SHEET_TITLE_NPV = 'numero predial viejo'
EXCEL_SHEET_TITLE_PLOT_NAME = 'nombre predio'
EXCEL_SHEET_TITLE_VALUATION = 'avaluo'
EXCEL_SHEET_TITLE_PLOT_CONDITION = 'condicion predio'
EXCEL_SHEET_TITLE_PLOT_TYPE = 'tipo predio'
EXCEL_SHEET_TITLE_ADDRESS = 'direccion'
EXCEL_SHEET_TITLE_FIRST_NAME = 'nombre1'
EXCEL_SHEET_TITLE_MIDDLE = 'nombre2'
EXCEL_SHEET_TITLE_FIRST_SURNAME = 'apellido1'
EXCEL_SHEET_TITLE_SECOND_SURNAME = 'apellido2'
EXCEL_SHEET_TITLE_BUSINESS_NAME = 'razon social'
EXCEL_SHEET_TITLE_SEX = 'sexo persona'
EXCEL_SHEET_TITLE_DOCUMENT_TYPE = 'tipo documento'
EXCEL_SHEET_TITLE_DOCUMENT_NUMBER = 'numero de documento'
EXCEL_SHEET_TITLE_KIND_PERSON = 'tipo persona'
EXCEL_SHEET_TITLE_ISSUING_ENTITY = 'organo emisor del documento'
EXCEL_SHEET_TITLE_DATE_ISSUE = 'fecha emision del documento'
EXCEL_SHEET_TITLE_ID_GROUP = 'id agrupación'
EXCEL_SHEET_TITLE_TYPE = 'tipo'
EXCEL_SHEET_TITLE_PARTY_DOCUMENT_NUMBER = 'número documento Interesado'
EXCEL_SHEET_TITLE_GROUP = 'agrupación'
EXCEL_SHEET_TITLE_SOURCE_TYPE = 'tipo de fuente'
EXCEL_SHEET_TITLE_DESCRIPTION_SOURCE = 'Descripción de la fuente'
EXCEL_SHEET_TITLE_STATE_SOURCE = 'estado_disponibilidad de la fuente'
EXCEL_SHEET_TITLE_OFFICIALITY_SOURCE = 'Es oficial la fuente'
EXCEL_SHEET_TITLE_STORAGE_PATH = 'Ruta de Almacenamiento de la fuente'


class ImportFromExcelDialog(QDialog, DIALOG_UI):
    log_excel_show_message_emitted = pyqtSignal(str)

    def __init__(self, iface, db, qgis_utils, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self._db = db
        self.qgis_utils = qgis_utils
        self.logger = Logger()
        self.help_strings = HelpStrings()
        self.log_dialog_excel_text_content = ""
        self.group_parties_exists = False
        self.names = self._db.names
        self._running_tool = False
        self.tool_name = QCoreApplication.translate("ImportFromExcelDialog", "Import intermediate structure")

        self.fields = {EXCEL_SHEET_NAME_PLOT: [EXCEL_SHEET_TITLE_DEPARTMENT, EXCEL_SHEET_TITLE_MUNICIPALITY, EXCEL_SHEET_TITLE_ZONE, 
                            EXCEL_SHEET_TITLE_REGISTRATION_PLOT, EXCEL_SHEET_TITLE_NPN, EXCEL_SHEET_TITLE_NPV,
                            EXCEL_SHEET_TITLE_PLOT_NAME, EXCEL_SHEET_TITLE_VALUATION, EXCEL_SHEET_TITLE_PLOT_CONDITION, 
                            EXCEL_SHEET_TITLE_PLOT_TYPE, EXCEL_SHEET_TITLE_ADDRESS
                            ],
                        EXCEL_SHEET_NAME_PARTY: [EXCEL_SHEET_TITLE_FIRST_NAME, EXCEL_SHEET_TITLE_MIDDLE, EXCEL_SHEET_TITLE_FIRST_SURNAME,
                            EXCEL_SHEET_TITLE_SECOND_SURNAME, EXCEL_SHEET_TITLE_BUSINESS_NAME, EXCEL_SHEET_TITLE_SEX,
                            EXCEL_SHEET_TITLE_DOCUMENT_TYPE, EXCEL_SHEET_TITLE_DOCUMENT_NUMBER, EXCEL_SHEET_TITLE_KIND_PERSON,
                            EXCEL_SHEET_TITLE_ISSUING_ENTITY,EXCEL_SHEET_TITLE_DATE_ISSUE, EXCEL_SHEET_TITLE_NPN
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
        #self.buttonBox.rejected.connect(self.rejected)
        self.buttonBox.helpRequested.connect(self.show_help)
        self.btn_browse_file.clicked.connect(
            make_file_selector(self.txt_excel_path,
                               QCoreApplication.translate("ImportFromExcelDialog",
                                                          "Select the Excel file with data in the intermediate structure"),
                               QCoreApplication.translate("ImportFromExcelDialog",
                                                                      'Excel File (*.xlsx *.xls)')))
        self.buttonBox.button(QDialogButtonBox.Ok).setText(QCoreApplication.translate("ImportFromExcelDialog", "Import"))

        self.initialize_feedback()
        self.restore_settings()

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        # self.tabWidget.currentWidget().layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

    def accepted(self):
        self.save_settings()
        self.import_from_excel()

    def import_from_excel(self):
        self._running_tool = True
        steps = 18
        step = 0
        self.progress.setVisible(True)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        # Where to store the reports?
        excel_path = self.txt_excel_path.text()

        if not excel_path:
            self.show_message(
                QCoreApplication.translate("ImportFromExcelDialog", "You need to select an Excel file before continuing with the import."),
                Qgis.Warning)
            self.progress.setVisible(False)
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
            return

        if not os.path.exists(excel_path):
            self.show_message(
                QCoreApplication.translate("ImportFromExcelDialog", "The specified Excel file does not exist!"),
                Qgis.Warning)
            self.progress.setVisible(False)
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
            return

        self.progress.setVisible(True)
        self.txt_log.setText(QCoreApplication.translate("ImportFromExcelDialog", "Loading tables from the Excel file..."))

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
                QCoreApplication.translate("ImportFromExcelDialog", "One of the sheets of the Excel file couldn't be loaded! Check the format again."),
                Qgis.Warning)
            self.progress.setVisible(False)
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
            return

        QgsProject.instance().addMapLayers([layer_group_party, layer_party, layer_parcel, layer_right])

        # GET LADM LAYERS
        layers = {
            self.names.OP_PARTY_T: None,
            self.names.OP_PARCEL_T: None,
            self.names.OP_RIGHT_T: None,
            self.names.EXT_ARCHIVE_S: None,
            self.names.COL_RRR_SOURCE_T: None,
            self.names.OP_GROUP_PARTY_T: None,
            self.names.MEMBERS_T: None,
            self.names.OP_ADMINISTRATIVE_SOURCE_T: None
        }

        self.qgis_utils.get_layers(self._db, layers, load=True)
        if not layers:
            return None

        # Get feature counts to compare after the ETL and know how many records were imported to each ladm_col table
        ladm_tables = [layers[self.names.OP_PARCEL_T],
                       layers[self.names.OP_PARTY_T],
                       layers[self.names.OP_RIGHT_T],
                       layers[self.names.OP_ADMINISTRATIVE_SOURCE_T],
                       layers[self.names.COL_RRR_SOURCE_T],
                       layers[self.names.OP_GROUP_PARTY_T],
                       layers[self.names.MEMBERS_T]]
        ladm_tables_feature_count_before = {t.name(): t.featureCount() for t in ladm_tables}


        # Run the ETL
        params = {'agrupacion': layers[self.names.OP_GROUP_PARTY_T],
                  'colmiembros': layers[self.names.MEMBERS_T],
                  'colrrrsourcet': layers[self.names.COL_RRR_SOURCE_T],
                  'extarchivo': layers[self.names.EXT_ARCHIVE_S],
                  'interesado': layers[self.names.OP_PARTY_T],
                  'layergroupparty': layer_group_party,
                  'layerparcel': layer_parcel,
                  'layerparty': layer_party,
                  'layerright': layer_right,
                  'opderecho': layers[self.names.OP_RIGHT_T],
                  'opfuenteadministrativatipo': layers[self.names.OP_ADMINISTRATIVE_SOURCE_T],
                  'parcel': layers[self.names.OP_PARCEL_T]}

        self.qgis_utils.disable_automatic_fields(self._db, self.names.OP_GROUP_PARTY_T)
        self.qgis_utils.disable_automatic_fields(self._db, self.names.OP_RIGHT_T)
        self.qgis_utils.disable_automatic_fields(self._db, self.names.OP_ADMINISTRATIVE_SOURCE_T)

        processing.run("model:ETL_intermediate_structure", params, feedback=self.feedback)

        if not self.feedback.isCanceled():
            self.progress.setValue(100)
            self.buttonBox.clear()
            self.buttonBox.setEnabled(True)
            self.buttonBox.addButton(QDialogButtonBox.Close)
        else:
            self.initialize_feedback() 

        # Print summary getting feature count in involved LADM_COL tables...
        summary = """<html><head/><body><p>"""
        summary += QCoreApplication.translate("ImportFromExcelDialog", "Import done!!!<br/>")
        for table in ladm_tables:
            summary += QCoreApplication.translate(
                        "ImportFromExcelDialog",
                        "<br/><b>{count}</b> records loaded into table <b>{table}</b>").format(
                            count=table.featureCount() - ladm_tables_feature_count_before[table.name()],
                            table=table.name())

        summary += """</body></html>"""
        self.txt_log.setText(summary)
        self.logger.success_msg(__name__, QCoreApplication.translate("ImportFromExcelDialog",
            "Data successfully imported to LADM_COL from intermediate structure (Excel file: '{}')!!!").format(excel_path))
        self._running_tool = False

    def check_layer_from_excel_sheet(self, excel_path, sheetname):
        layer = self.get_layer_from_excel_sheet(excel_path, sheetname)
        error_counter = 0

        if layer is None and sheetname != EXCEL_SHEET_NAME_GROUP: # optional sheet
            self.generate_message_excel_error(QCoreApplication.translate("ImportFromExcelDialog",
                    "The {} sheet has not information or has another name.").format(sheetname))
            error_counter += 1
        else:
            title_validator = layer.fields().toList()

        if sheetname == EXCEL_SHEET_NAME_PLOT and layer is not None:
            if not title_validator:
                self.generate_message_excel_error(QCoreApplication.translate("ImportFromExcelDialog",
                        "The title does not match the format in the sheet {}.").format(sheetname))
                error_counter += 1
            if list(layer.getFeatures('"numero predial nuevo" is Null')):
                self.generate_message_excel_error(QCoreApplication.translate("ImportFromExcelDialog",
                        "The column numero predial nuevo has empty values in sheet {}.").format(sheetname))
                error_counter += 1    
            if not self.check_field_numeric_layer(layer, 'departamento'):
                self.generate_message_excel_error(QCoreApplication.translate("ImportFromExcelDialog",
                        "The column departamento has non-numeric values in sheet {}.").format(sheetname))
                error_counter += 1
            if not self.check_field_numeric_layer(layer, 'municipio'):
                self.generate_message_excel_error(QCoreApplication.translate("ImportFromExcelDialog",
                        "The column municipio has non-numeric values in sheet {}.").format(sheetname))
                error_counter += 1
            if not self.check_field_numeric_layer(layer, 'numero predial nuevo'):
                self.generate_message_excel_error(QCoreApplication.translate("ImportFromExcelDialog",
                        "The column numero predial nuevo has non-numeric values in sheet {}.").format(sheetname))
                error_counter += 1

        if sheetname == EXCEL_SHEET_NAME_PARTY and layer is not None:
            if not title_validator:
                self.generate_message_excel_error(QCoreApplication.translate("ImportFromExcelDialog",
                        "The title does not match the format in sheet {}.").format(sheetname))
                error_counter += 1
            if list(layer.getFeatures('"tipo documento" is Null')):
                self.generate_message_excel_error(QCoreApplication.translate("ImportFromExcelDialog",
                        "The column tipo documento has empty values in sheet {}.").format(sheetname))
                error_counter += 1
            if list(layer.getFeatures('"numero de documento" is Null')):
                self.generate_message_excel_error(QCoreApplication.translate("ImportFromExcelDialog",
                        "The column numero de documento has empty values in sheet {}.").format(sheetname))
                error_counter += 1
            if not self.check_length_attribute_value(layer, 'numero de documento', 12):
                self.generate_message_excel_error(QCoreApplication.translate("ImportFromExcelDialog",
                        "The column numero de documento has more characters than expected in sheet {}.").format(sheetname))
                error_counter += 1
            if list(layer.getFeatures('"tipo persona" is Null')):
                self.generate_message_excel_error(QCoreApplication.translate("ImportFromExcelDialog",
                        "The column tipo persona has empty values in sheet {}.").format(sheetname))
                error_counter += 1

        if sheetname == EXCEL_SHEET_NAME_GROUP and layer is not None:
            if not title_validator:
                self.generate_message_excel_error(QCoreApplication.translate("ImportFromExcelDialog",
                        "The title does not match the format in the sheet {}.").format(sheetname))
                error_counter += 1
            self.group_parties_exists = True
            if list(layer.getFeatures('"numero predial nuevo" is Null')):
                self.generate_message_excel_error(QCoreApplication.translate("ImportFromExcelDialog",
                        "The column numero predial nuevo has empty values in sheet {}.").format(sheetname))
                error_counter += 1
            if list(layer.getFeatures('"tipo documento" is Null')):
                self.generate_message_excel_error(QCoreApplication.translate("ImportFromExcelDialog",
                        "The column tipo documento has empty values in sheet {}.").format(sheetname))
                error_counter += 1
            if list(layer.getFeatures('"numero de documento" is Null')):
                self.generate_message_excel_error(QCoreApplication.translate("ImportFromExcelDialog",
                        "The column numero de documento has empty values in sheet {}.").format(sheetname))
                error_counter += 1
            if list(layer.getFeatures('"id agrupación" is Null')):
                self.generate_message_excel_error(QCoreApplication.translate("ImportFromExcelDialog",
                        "The column id agrupación has empty values in sheet {}.").format(sheetname))
                error_counter += 1
            if not self.check_length_attribute_value(layer, 'numero de documento', 12):
                self.generate_message_excel_error(QCoreApplication.translate("ImportFromExcelDialog",
                        "The column numero de documento has more characters of the permitted in sheet {}.").format(sheetname))
                error_counter += 1

        if sheetname == EXCEL_SHEET_NAME_RIGHT and layer is not None:
            if not title_validator:
                self.generate_message_excel_error(QCoreApplication.translate("ImportFromExcelDialog",
                        "The title does not match the format in sheet {}.").format(sheetname))
                error_counter += 1
            if list(layer.getFeatures('"tipo" is Null')):
                self.generate_message_excel_error(QCoreApplication.translate("ImportFromExcelDialog",
                        "The column tipo has empty values in sheet {}.").format(sheetname))
                error_counter += 1
            if list(layer.getFeatures('"tipo de fuente" is Null')):
                self.generate_message_excel_error(QCoreApplication.translate("ImportFromExcelDialog",
                        "The column tipo de fuente has empty values in sheet {}.").format(sheetname))
                error_counter += 1
            if list(layer.getFeatures('"estado_disponibilidad de la fuente" is Null')):
                self.generate_message_excel_error(QCoreApplication.translate("ImportFromExcelDialog",
                        "The column estado_disponibilidad de la fuente has empty values in sheet {}.").format(sheetname))
                error_counter += 1
            #if list(layer.getFeatures('"Ruta de Almacenamiento de la fuente" is Null')):
            #    self.generate_message_excel_error(QCoreApplication.translate("ImportFromExcelDialog",
            #            "The column Ruta de Almacenamiento de la fuente has empty values in sheet {}.").format(sheetname))
            #    error_counter += 1
            if len(list(layer.getFeatures('"número documento Interesado" is Null'))) + len(list(layer.getFeatures('"agrupación" is Null'))) != layer.featureCount():
                self.generate_message_excel_error(QCoreApplication.translate("ImportFromExcelDialog",
                        "Number of non-null parties plus number of non-null group parties is not equal to number of records in sheet {}. There might be rights without party or group party associated.").format(sheetname))
                error_counter += 1
            if not self.group_parties_exists:
                if list(layer.getFeatures('"número documento Interesado" is Null')):
                    self.generate_message_excel_error(QCoreApplication.translate("ImportFromExcelDialog",
                            "The column número documento Interesado has empty values in sheet {}.").format(sheetname))
                    error_counter += 1
                if len(list(layer.getFeatures('"agrupacion" is Null'))) != layer.featureCount():
                    self.generate_message_excel_error(QCoreApplication.translate("ImportFromExcelDialog",
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

        self.logger.info(__name__, "Loading layer from excel with uri='{}'".format(uri))
        layer = QgsVectorLayer(uri, '{}-{}'.format('excel', sheetname), 'ogr')
        layer.setProviderEncoding('UTF-8')
        return layer

    def get_excel_info(self, path, sheetname):
        data_source = ogr.Open(path, 0)
        layer = data_source.GetLayerByName(sheetname)

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
                                   QCoreApplication.translate("ImportFromExcelDialog",
                                                              "Save File"),
                                   os.path.join(settings.value('Asistente-LADM_COL/import_from_excel_dialog/template_save_path', '.'), filename),
                                   QCoreApplication.translate("ImportFromExcelDialog",
                                                              "Excel File (*.xlsx *.xls)"))

        if new_filename:
            settings.setValue('Asistente-LADM_COL/import_from_excel_dialog/template_save_path', os.path.dirname(new_filename))
            template_file = QFile(":/Asistente-LADM_COL/resources/excel/" + filename)

            if not template_file.exists():
                self.logger.critical(__name__, "Excel doesn't exist! Probably due to a missing 'make' execution to generate resources...")
                msg = QCoreApplication.translate("ImportFromExcelDialog", "Excel file not found. Update your plugin. For details see log.")
                self.show_message(msg, Qgis.Warning)
                return

            if os.path.isfile(new_filename):
                self.logger.info(__name__, 'Removing existing file {}...'.format(new_filename))
                os.chmod(new_filename, 0o777)
                os.remove(new_filename)

            if template_file.copy(new_filename):
                os.chmod(new_filename, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
                msg = QCoreApplication.translate("ImportFromExcelDialog", """The file <a href="file:///{}">{}</a> was successfully saved!""").format(normalize_local_url(new_filename), os.path.basename(new_filename))
                self.show_message(msg, Qgis.Info)
            else:
                self.logger.info(__name__, 'There was an error copying the CSV file {}!'.format(new_filename))
                msg = QCoreApplication.translate("ImportFromExcelDialog", "The file couldn\'t be saved.")
                self.show_message(msg, Qgis.Warning)


    def reject(self):
        self.selected_items_dict = dict()
            
        if self._running_tool:
            reply = QMessageBox.question(self,
                                         QCoreApplication.translate("import_from_excel", "Warning"),
                                         QCoreApplication.translate("import_from_excel",
                                                                    "The '{}' tool is still running. Do you want to cancel it? If you cancel, the data might be incomplete in the target database.").format(self.tool_name),
                                         QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.feedback.cancel()
                self._running_tool = False
                msg = QCoreApplication.translate("import_from_excel", "The '{}' tool was cancelled.").format(self.tool_name)
                self.logger.info(__name__, msg)
                self.show_message(msg, Qgis.Info)
        else:
            self.logger.info(__name__, "Dialog closed.")
            self.done(1)

    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/import_from_excel_dialog/excel_path', self.txt_excel_path.text())

    def restore_settings(self):
        settings = QSettings()
        self.txt_excel_path.setText(settings.value('Asistente-LADM_COL/import_from_excel_dialog/excel_path', ''))

    def show_message(self, message, level):
        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.bar.pushMessage(message, level, 10)

    def show_help(self):
        show_plugin_help("import_from_excel")

    def progress_changed(self):
        QCoreApplication.processEvents()  # Listen to cancel from the user
        self.progress.setValue(self.feedback.progress())

    def initialize_feedback(self):
        self.progress.setValue(0)
        self.progress.setVisible(False)
        self.feedback = QgsProcessingFeedback()         
        self.feedback.progressChanged.connect(self.progress_changed)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)