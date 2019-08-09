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
import processing

from QgisModelBaker.libili2db import iliimporter
from QgisModelBaker.libili2db.ili2dbconfig import BaseConfiguration
from QgisModelBaker.libqgsprojectgen.dataobjects import Project
from QgisModelBaker.libqgsprojectgen.generator.generator import Generator

from qgis.PyQt.QtCore import QVariant

from qgis.core import (QgsProject,
                       QgsEditorWidgetSetup,
                       QgsDefaultValue,
                       QgsApplication,
                       NULL,
                       QgsField,
                       QgsVectorLayer,
                       QgsVectorLayerJoinInfo)

from .symbology import SymbologyUtils
from ..config.refactor_fields_mappings import get_refactor_fields_mapping_r1_gdb_to_ladm

def run_etl_model_input_load_data(input_layer, output_layer, ladm_col_layer_name, qgis_utils):

    if isinstance(input_layer, str):
        input_layer = QgsProject.instance().mapLayersByName(input_layer)[0]
        input_layer = fix_spatial_layer(input_layer)

    model = QgsApplication.processingRegistry().algorithmById("model:ETL-model")

    if model:
        mapping = get_refactor_fields_mapping_r1_gdb_to_ladm(ladm_col_layer_name, qgis_utils)
        params = {
            'INPUT': input_layer,
            'mapping': mapping,
            'output': output_layer
        }

        res = processing.run("model:ETL-model", params)

    else:
        return

    return output_layer

def fix_spatial_layer(layer):
    params = {'INPUT': layer, 'OUTPUT':'memory:'}
    single_parts = processing.run("native:multiparttosingleparts", params)
    params = {'INPUT': single_parts['OUTPUT'], 'OUTPUT':'memory:'}
    fixed = processing.run("native:fixgeometries", params)

    return fixed['OUTPUT']

def join_layers(initial, target, join_name, target_name):
    joinObject = QgsVectorLayerJoinInfo()
    joinObject.setJoinLayerId(target.id())
    joinObject.setJoinFieldName(target_name)
    joinObject.setTargetFieldName(join_name)
    joinObject.setJoinLayer(target)
    initial.addJoin(joinObject)

def create_column(layer, name):
    layer.dataProvider().addAttributes([QgsField(name, QVariant.String, "VARCHAR")])
    layer.updateFields()

def get_directions(layer, reference_layers):
    reference_layers = fix_spatial_layer(reference_layers)
    params = {'INPUT':layer,'ALL_PARTS':False,'OUTPUT':'TEMPORARY_OUTPUT'}
    centroids = processing.run("native:centroids", params)
    params = {'INPUT':centroids['OUTPUT'],'REFERENCE_LAYER':reference_layers,'TOLERANCE':10,'BEHAVIOR':0,'OUTPUT':'TEMPORARY_OUTPUT'}
    direction = processing.run("qgis:snapgeometries", params)

    return direction['OUTPUT'] 