# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-05-16
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
import processing

from QgisModelBaker.libili2db import iliimporter
from QgisModelBaker.libili2db.ili2dbconfig import BaseConfiguration
from QgisModelBaker.libqgsprojectgen.dataobjects import Project
from QgisModelBaker.libqgsprojectgen.generator.generator import Generator

from qgis.core import (QgsProject,
                       QgsEditorWidgetSetup,
                       QgsDefaultValue,
                       QgsApplication,
                       NULL)

from .symbology import SymbologyUtils
from ..config.refactor_fields_mappings import get_refactor_fields_mapping_field_data_capture_to_ladm
              
def import_capture_model(tool_name, model_name, gpkg_path):
    if model_name == 'Captura_Geografica_V0_3':
        ili_path = '/home/shade/.local/share/QGIS/QGIS3/profiles/default/python/plugins/asistente_ladm_col/resources/ili/Captura_Geografica_V0_3.ili'
    elif model_name == 'Captura_Alfanumerica_V0_3':
        ili_path = '/home/shade/.local/share/QGIS/QGIS3/profiles/default/python/plugins/asistente_ladm_col/resources/ili/Captura_Alfanumerica_V0_3.ili'

    importer = iliimporter.Importer()
    importer.tool_name = tool_name
    base_config = BaseConfiguration()
    base_config.custom_model_directories_enabled = False
    importer.configuration.tool_name = tool_name
    importer.configuration.ilifile = ili_path
    importer.configuration.ilimodels = model_name
    importer.configuration.dbfile = gpkg_path
    importer.configuration.epsg = 3116
    importer.configuration.inheritance = 'smart2'
    importer.run()

    generator = Generator(importer.configuration.tool_name, importer.configuration.uri,
                                    importer.configuration.inheritance, importer.configuration.dbschema)

    available_layers = generator.layers()
    relations, _ = generator.relations(available_layers)
    legend = generator.legend(available_layers)

    project = Project()
    project.layers = available_layers
    project.relations = relations
    project.legend = legend
    project.post_generate()

    qgis_project = QgsProject.instance()
    project.create(None, qgis_project)

def organize_legend(model_name):
    if model_name == 'Captura_Geografica_V0_3':
        root = QgsProject.instance().layerTreeRoot()
        group = root.findGroup('tables')

        if group is not None:
            layers = group.findLayers()

            for l in layers:
                if l.name() == 'fuente_espacial':
                    root.insertLayer(4, l.layer())
                    group.removeLayer(l.layer())
            if group.findLayers() == []:
                root.removeChildNode(group)
                
        group = root.findGroup('domains')
        group.setExpanded(False)
    elif model_name == 'Captura_Alfanumerica_V0_3':
        root = QgsProject.instance().layerTreeRoot()
        group = root.findGroup('tables')
        group.setExpanded(False)

def change_multimedia_suppord():
    for k, layer in QgsProject.instance().mapLayers().items():
        for field in layer.fields().names():
            if field == 'soporte_multimedia':
                CUSTOM_WIDGET_CONFIGURATION = {
                    layer.name(): {
                        'type': 'ExternalResource',
                        'config': {
                            'PropertyCollection': {
                                'properties': {},
                                'name': NULL,
                                'type': 'collection'
                            },
                            'FileWidget': True,
                            'DocumentViewer': 0,
                            'RelativeStorage': 0,
                            'StorageMode': 0,
                            'DocumentViewerHeight': 0,
                            'FileWidgetButton': True,
                            'DocumentViewerWidth': 0,
                            'FileWidgetFilter': ''
                        }
                    }
                }
                editor_widget_setup = QgsEditorWidgetSetup(
                        CUSTOM_WIDGET_CONFIGURATION[layer.name()]['type'],
                        CUSTOM_WIDGET_CONFIGURATION[layer.name()]['config'])
                index = layer.fields().indexFromName('soporte_multimedia')
                layer.setEditorWidgetSetup(index, editor_widget_setup)

def load_default_value():
    for k, layer in QgsProject.instance().mapLayers().items():
        for field in layer.fields().names():
            if field == 'area_poligono':
                id_field = layer.fields().indexFromName('area_poligono')
                layer.setDefaultValueDefinition(id_field, QgsDefaultValue("$area"))
            if field == 'exactitud_vertical':
                id_field = layer.fields().indexFromName('exactitud_vertical')
                layer.setDefaultValueDefinition(id_field, QgsDefaultValue("@position_vertical_accuracy"))
            if field == 'exactitud_horizontal':
                id_field = layer.fields().indexFromName('exactitud_horizontal')
                layer.setDefaultValueDefinition(id_field, QgsDefaultValue("@position_horizontal_accuracy"))

def load_simbology():
    for k, layer in QgsProject.instance().mapLayers().items():
        SymbologyUtils().set_layer_style_from_qml(layer)

def run_etl_model_input_load_data(input_layer, out_layer, ladm_col_layer_name, qgis_utils):

    model = QgsApplication.processingRegistry().algorithmById("model:ETL-model")

    if model:
        mapping = get_refactor_fields_mapping_field_data_capture_to_ladm(ladm_col_layer_name, qgis_utils)
        params = {
            'INPUT': input_layer,
            'mapping': mapping,
            'output': out_layer
        }
        res = processing.run("model:ETL-model", params)
        print (res)

    else:
        print("Error: Model ETL-model was not found and cannot be opened!")
        return

    return out_layer