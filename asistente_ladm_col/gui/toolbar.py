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
                    <!--Header=True-->
                    <SrcSql dialect="sqlite">SELECT * FROM 'interesado' LIMIT {count} OFFSET 1</SrcSql>
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
        """.format(filename=filename, basename=basename, count=count)

        party_file_path = os.path.join(dirname, '{}.{}.vrt'.format(basename, sheetname))
        with open(party_file_path, 'w') as sheet:
            sheet.write(xml_text_party)

        uri = '{vrtfilepath}|layername={filename}-{sheetname}'.format(vrtfilepath=party_file_path, sheetname=sheetname, filename=filename)
        layer_party = QgsVectorLayer(uri, '{}-{}'.format('excel', sheetname), 'ogr')
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
                    <!--Header=True-->
                    <SrcSql dialect="sqlite">SELECT * FROM 'derecho' LIMIT {count} OFFSET 1</SrcSql>
                    <Field name="tipo" src="Field1" type="String"/>
                    <Field name="número documento Interesado" src="Field2" type="String"/>
                    <Field name="agrupación" src="Field3" type="String"/>
                    <Field name="numero predial nuevo" src="Field4" type="String"/>
                    <Field name="tipo de fuente" src="Field5" type="String"/>
                    <Field name="Descripción de la fuente" src="Field6" type="String"/>
                    <Field name="estado_disponibilidad de la fuente" src="Field7" type="String"/>
                    <Field name="Es oficial la fuente" src="Field8" type="String"/>
                    <Field name="Ruta de Almacenamiento de la fuente" src="Field9" type="String"/>
                </OGRVRTLayer>
            </OGRVRTDataSource>
        """.format(filename=filename, basename=basename, count=count)

        right_file_path = os.path.join(dirname, '{}.{}.vrt'.format(basename, sheetname))
        with open(right_file_path, 'w') as sheet:
            sheet.write(xml_text_right)

        uri = '{vrtfilepath}|layername={filename}-{sheetname}'.format(vrtfilepath=right_file_path, sheetname=sheetname, filename=filename)
        layer_right = QgsVectorLayer(uri, '{}-{}'.format('excel', sheetname), 'ogr')
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

        administrtive_source_table = res_layers[ADMINISTRATIVE_SOURCE_TABLE]
        if administrtive_source_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("QGISUtils",
                                                                           "Administrative Source table couldn't be found... {}").format(
                                                    db.get_description()),
                                                Qgis.Warning)
            return


        # Run the ETL

        self.qgis_utils.message_emitted.emit(
            QCoreApplication.translate("QGISUtils",
                                       "Data successfully imported to LADM_COL from intermediate structure (Excel file: '{}')!!!").format(
                                            save_into_file),
            Qgis.Success)