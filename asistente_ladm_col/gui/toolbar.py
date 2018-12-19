# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-08-09
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

from qgis.PyQt.QtCore import QCoreApplication, QSettings
from qgis.PyQt.QtWidgets import QDialog, QFileDialog
from qgis.core import (QgsProject,
                       Qgis,
                       QgsVectorLayer)

import processing

from ..config.table_mapping_config import (COL_PARTY_TABLE,
                                           PARCEL_TABLE,
                                           RIGHT_TABLE,
                                           EXTFILE_TABLE,
                                           RRR_SOURCE_RELATION_TABLE,
                                           EXTFILE_TABLE,
                                           LA_GROUP_PARTY_TABLE,
                                           ADMINISTRATIVE_SOURCE_TABLE,
                                           MEMBERS_TABLE)
from .dlg_topological_edition import LayersForTopologicalEdition
from ..utils.utils import get_number_of_rows_in_excel_file


class ToolBar():
    def __init__(self, iface, qgis_utils):
        self.iface = iface
        self.qgis_utils = qgis_utils

    def enable_topological_editing(self, db):
        # Enable Topological Editing
        QgsProject.instance().setTopologicalEditing(True)

        dlg = LayersForTopologicalEdition()
        if dlg.exec_() == QDialog.Accepted:
            # Load layers selected in the dialog
            res_layers = self.qgis_utils.get_layers(db, dlg.selected_layers_info, load=True)

            layers = list()
            # Open edit session in all layers
            for layer_name, layer_info in dlg.selected_layers_info.items():
                layer = res_layers[layer_name]
                if layer is None:
                    self.qgis_utils.message_emitted.emit(
                        QCoreApplication.translate("QGISUtils", "{} layer couldn't be found... {}").format(layer_name, db.get_description()),
                        Qgis.Warning)
                    return

                layer.startEditing()
                layers.append(layer)

            # Activate "Vertex Tool (All Layers)"
            self.qgis_utils.activate_layer_requested.emit(layers[0])
            self.qgis_utils.action_vertex_tool_requested.emit()

            self.qgis_utils.message_with_duration_emitted.emit(
                QCoreApplication.translate("QGISUtils", "You can start moving nodes in layers {} and {}, simultaneously!").format(
                    ", ".join(layer.name() for layer in layers[:-1]), layers[-1].name()),
                Qgis.Info, 30)

    def import_from_intermediate_structure(self, db):
        # Where to store the reports?
        previous_file_path = QSettings().value("Asistente-LADM_COL/import/latest_excel_file_path", ".")
        save_into_file = QFileDialog.getOpenFileName(
            None,
            QCoreApplication.translate("QGISUtils", "Select the Excel file with data in the intermediate structure"),
            previous_file_path,
            'Excel files (*.xls *.xlsx)',
            'Excel files (*.xls *.xlsx)')[0]

        if not save_into_file:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "You need to select an Excel file before continuing with the import."),
                Qgis.Warning)
            return
        QSettings().setValue("Asistente-LADM_COL/import/latest_excel_file_path", save_into_file)

        basename = os.path.basename(save_into_file)
        filename = os.path.splitext(basename)[0]
        dirname = os.path.dirname(save_into_file)

        # Now that we have the Excel file, build vrts to load its sheets appropriately

        # GROUP PARTY
        sheetname = 'agrupacion'
        count = get_number_of_rows_in_excel_file(save_into_file, sheetname)
        if count is None:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "It was not possible to get the number or rows in sheet '{sheet}' from file '{file}'.").format(sheet=sheetname, file=save_into_file),
                Qgis.Warning)
            return

        xml_text_group_party = """<?xml version="1.0" encoding="UTF-8"?>
            <OGRVRTDataSource>
                <OGRVRTLayer name="{filename}-agrupacion">
                    <SrcDataSource relativeToVRT="1">{basename}</SrcDataSource>
                    <!--Header=True-->
                    <SrcSql dialect="sqlite">SELECT * FROM 'agrupacion' LIMIT {count} OFFSET 1</SrcSql>
                    <Field name="numero predial nuevo" src="Field1" type="String"/>
                    <Field name="tipo documento" src="Field2" type="String"/>
                    <Field name="numero de documento" src="Field3" type="String"/>
                    <Field name="id agrupación" src="Field4" type="String"/>               
                </OGRVRTLayer>            
            </OGRVRTDataSource>
        """.format(filename=filename, basename=basename, count=count)

        group_party_file_path = os.path.join(dirname, '{}.{}.vrt'.format(basename, sheetname))
        with open(group_party_file_path, 'w') as sheet:
            sheet.write(xml_text_group_party)

        uri = '{vrtfilepath}|layername={filename}-{sheetname}'.format(vrtfilepath=group_party_file_path, sheetname=sheetname, filename=filename)
        layer_group_party = QgsVectorLayer(uri, '{}-{}'.format('excel', sheetname), 'ogr')
        layer_group_party.setProviderEncoding('UTF-8')
        print(uri, layer_group_party.isValid())

        # COL_PARTY
        sheetname = 'interesado'
        count = get_number_of_rows_in_excel_file(save_into_file, sheetname)
        if count is None:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "It was not possible to get the number or rows in sheet '{sheet}' from file '{file}'.").format(sheet=sheetname, file=save_into_file),
                Qgis.Warning)
            return
        xml_text_party = """<?xml version="1.0" encoding="UTF-8"?>
            <OGRVRTDataSource>
                <OGRVRTLayer name="{filename}-interesado">
                    <SrcDataSource relativeToVRT="1">{basename}</SrcDataSource>
                    <!--Header=False-->
                    <SrcLayer>interesado</SrcLayer>
                    <Field name="nombre1" src="Field1" type="String"/>
                    <Field name="nombre2" src="Field2" type="String"/>
                    <Field name="apellido1" src="Field3" type="String"/>
                    <Field name="apellido2" src="Field4" type="String"/>
                    <Field name="razon social" src="Field5" type="String"/>
                    <Field name="sexo persona" src="Field6" type="String"/>
                    <Field name="tipo documento" src="Field7" type="String"/>
                    <Field name="numero de documento" src="Field8" type="String"/>
                    <Field name="tipo persona" src="Field9" type="String"/>
                    <Field name="organo emisor del documento" src="Field10" type="String"/>
                    <Field name="fecha emision del documento" src="Field11" type="String"/>
                    <Field name="numero predial nuevo" src="Field12" type="String"/>
                </OGRVRTLayer>
            </OGRVRTDataSource>
        """.format(filename=filename, basename=basename)

        party_file_path = os.path.join(dirname, '{}.{}.vrt'.format(basename, sheetname))
        with open(party_file_path, 'w') as sheet:
            sheet.write(xml_text_party)

        uri = '{vrtfilepath}|layername={filename}-{sheetname}'.format(vrtfilepath=party_file_path, sheetname=sheetname, filename=filename)
        layer_party = QgsVectorLayer(uri, '{}-{}'.format('excel', sheetname), 'ogr')
        layer_party.setProviderEncoding('UTF-8')
        print(uri, layer_party.isValid())

        # PARCEL
        sheetname = 'predio'
        count = get_number_of_rows_in_excel_file(save_into_file, sheetname)
        if count is None:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "It was not possible to get the number or rows in sheet '{sheet}' from file '{file}'.").format(sheet=sheetname, file=save_into_file),
                Qgis.Warning)
            return
        xml_text_parcel = """<?xml version="1.0" encoding="UTF-8"?>
            <OGRVRTDataSource>
                <OGRVRTLayer name="{filename}-predio">
                    <SrcDataSource relativeToVRT="1">{basename}</SrcDataSource>
                    <!--Header=False-->
                    <SrcSql dialect="sqlite">SELECT * FROM 'predio' LIMIT {count} OFFSET 0</SrcSql>
                    <Field name="departamento" src="departamento" type="Integer"/>
                    <Field name="municipio" src="municipio" type="Integer"/>
                    <Field name="zona" src="zona" type="String"/>
                    <Field name="matricula predio" src="matricula predio" type="String"/>
                    <Field name="numero predial nuevo" src="numero predial nuevo" type="String"/>
                    <Field name="numero predial viejo" src="numero predial viejo" type="String"/>
                    <Field name="nombre predio" src="nombre predio" type="String"/>
                    <Field name="avaluo" src="avaluo" type="String"/>
                    <Field name="tipo predio" src="tipo predio" type="String"/>
                </OGRVRTLayer>
            </OGRVRTDataSource>
        """.format(filename=filename, basename=basename, count=count)

        parcel_file_path = os.path.join(dirname, '{}.{}.vrt'.format(basename, sheetname))
        with open(parcel_file_path, 'w') as sheet:
            sheet.write(xml_text_parcel)

        uri = '{vrtfilepath}|layername={filename}-{sheetname}'.format(vrtfilepath=parcel_file_path, sheetname=sheetname, filename=filename)
        layer_parcel = QgsVectorLayer(uri, '{}-{}'.format('excel', sheetname), 'ogr')
        layer_parcel.setProviderEncoding('UTF-8')
        print(uri, layer_parcel.isValid())

        # RIGHT
        sheetname = 'derecho'
        count = get_number_of_rows_in_excel_file(save_into_file, sheetname)
        if count is None:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("QGISUtils",
                                           "It was not possible to get the number or rows in sheet '{sheet}' from file '{file}'.").format(sheet=sheetname, file=save_into_file),
                Qgis.Warning)
            return
        xml_text_right = """<?xml version="1.0" encoding="UTF-8"?>
            <OGRVRTDataSource>
                <OGRVRTLayer name="{filename}-derecho">
                    <SrcDataSource relativeToVRT="1">{basename}</SrcDataSource>
                    <!--Header=False-->
                    <SrcLayer>derecho</SrcLayer>
                    <Field name="tipo" src="tipo" type="String"/>
                    <Field name="número documento Interesado" src="número documento Interesado" type="String"/>
                    <Field name="agrupación" src="agrupación" type="String"/>
                    <Field name="numero predial nuevo" src="numero predial nuevo" type="String"/>
                    <Field name="tipo de fuente" src="tipo de fuente" type="String"/>
                    <Field name="Descripción de la fuente" src="Descripción de la fuente" type="Integer"/>
                    <Field name="estado_disponibilidad de la fuente" src="estado_disponibilidad de la fuente" type="String"/>
                    <Field name="Es oficial la fuente" src="Es oficial la fuente" type="String"/>
                    <Field name="Ruta de Almacenamiento de la fuente" src="Ruta de Almacenamiento de la fuente" type="String"/>
                </OGRVRTLayer>
            </OGRVRTDataSource>
        """.format(filename=filename, basename=basename, count=count)

        right_file_path = os.path.join(dirname, '{}.{}.vrt'.format(basename, sheetname))
        with open(right_file_path, 'w') as sheet:
            sheet.write(xml_text_right)

        uri = '{vrtfilepath}|layername={filename}-{sheetname}'.format(vrtfilepath=right_file_path, sheetname=sheetname, filename=filename)
        layer_right = QgsVectorLayer(uri, '{}-{}'.format('excel', sheetname), 'ogr')
        layer_right.setProviderEncoding('UTF-8')
        print(uri, layer_right.isValid())
        QgsProject.instance().addMapLayers([layer_group_party, layer_party, layer_parcel, layer_right])


        # GET LADM LAYERS
        res_layers = self.qgis_utils.get_layers(db, {
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
                                                    db.get_description()),
                                                Qgis.Warning)
            return

        parcel_table = res_layers[PARCEL_TABLE]
        if parcel_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("QGISUtils",
                                                                           "Parcel table couldn't be found... {}").format(
                                                    db.get_description()),
                                                Qgis.Warning)
            return

        right_table = res_layers[RIGHT_TABLE]
        if right_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("QGISUtils",
                                                                           "Right table couldn't be found... {}").format(
                                                    db.get_description()),
                                                Qgis.Warning)
            return

        extfile_table = res_layers[EXTFILE_TABLE]
        if extfile_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("QGISUtils",
                                                                           "EXT_FILE table couldn't be found... {}").format(
                                                    db.get_description()),
                                                Qgis.Warning)
            return

        rrr_source_table = res_layers[RRR_SOURCE_RELATION_TABLE]
        if rrr_source_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("QGISUtils",
                                                                           "RRR-SOURCE table couldn't be found... {}").format(
                                                    db.get_description()),
                                                Qgis.Warning)
            return

        group_party_table = res_layers[LA_GROUP_PARTY_TABLE]
        if group_party_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("QGISUtils",
                                                                           "Group party table couldn't be found... {}").format(
                                                    db.get_description()),
                                                Qgis.Warning)
            return

        members_table = res_layers[MEMBERS_TABLE]
        if members_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("QGISUtils",
                                                                           "Members table couldn't be found... {}").format(
                                                    db.get_description()),
                                                Qgis.Warning)
            return

        administrative_source_table = res_layers[ADMINISTRATIVE_SOURCE_TABLE]
        if administrative_source_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("QGISUtils",
                                                                           "Administrative Source table couldn't be found... {}").format(
                                                    db.get_description()),
                                                Qgis.Warning)
            return


        # Run the ETL

        print('1. Load col_interesado data')
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

        print('2. Define group parties')
        pre_group_party_layer = processing.run("qgis:statisticsbycategories",
                                   { 'CATEGORIES_FIELD_NAME': 'id agrupación',
                                      'INPUT': layer_group_party,
                                     'OUTPUT': 'memory:',
                                     'VALUES_FIELD_NAME': None })['OUTPUT']

        print('3. Load group parties')
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

        print('4. Join group parties t_id')
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

        print('5. Join group parties with parties')
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

        print('6. Load group party members')
        processing.run("model:ETL-model",
                       {
                           'INPUT': group_party_party_tid_layer,
                           'mapping': [
                               {'expression': '"interesado_t_id"', 'length': -1, 'name': 'interesados_col_interesado', 'precision': 0, 'type': 4},
                               {'expression': '"agrupacion_t_id"', 'length': -1, 'name': 'agrupacion', 'precision': 0, 'type': 4}],
                           'output': members_table
                       })

        print('7. Load parcels')
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

        print('8. Concatenate Rights and Sources fields')
        concat_right_source_layer = processing.run("qgis:fieldcalculator",
                                                   { 	'FIELD_LENGTH': 100,
                                                        'FIELD_NAME': 'concat_',
                                                        'FIELD_PRECISION': 3,
                                                        'FIELD_TYPE': 2,
                                                        'FORMULA': 'concat( \"número documento interesado\" , \"agrupacion\" , \"numero predial nuevo\" , \"tipo de fuente\" , \"Descricpión de la fuente\")',
                                                        'INPUT': layer_right,
                                                        'NEW_FIELD': True,
                                                        'OUTPUT': 'memory:' })['OUTPUT']

        print('9. Load Administrative sources')
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

        print('10. Join concatenate source to administrative source t_id')
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

        print('11. Load extarchivo')
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

        print('12. Join source and party t_id')
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

        print('13. Join source, party, group party t_id')
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

        print('14. Join source, party, group party, parcel t_id')
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

        print('15. Load Rights')
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

        print('16. Join source, party, group party, parcel, right t_id')
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

        print('17. Load rrrfuente')
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


        self.qgis_utils.message_emitted.emit(
            QCoreApplication.translate("QGISUtils",
                                       "Data successfully imported to LADM_COL from intermediate structure (Excel file: '{}')!!!").format(
                                            save_into_file),
            Qgis.Success)