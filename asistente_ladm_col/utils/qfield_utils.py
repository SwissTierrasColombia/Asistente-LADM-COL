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

def run_etl_model_input_load_data(input_layer, out_layer, ladm_col_layer_name, qgis_utils):

    if isinstance(input_layer, str):
        input_layer = QgsProject.instance().mapLayersByName(input_layer)[0]
        input_layer = fix_polygon_layers(input_layer)

    model = QgsApplication.processingRegistry().algorithmById("model:ETL-model")

    if model:
        mapping = get_refactor_fields_mapping_r1_gdb_to_ladm(ladm_col_layer_name, qgis_utils)
        params = {
            'INPUT': input_layer,
            'mapping': mapping,
            'output': out_layer
        }
        print (input_layer.name())
        res = processing.run("model:ETL-model", params)

    else:
        return

    return out_layer

def fix_polygon_layers(layer):
    params = {'INPUT': layer, 'OUTPUT':'memory:'}
    multipart = processing.run("native:multiparttosingleparts", params)
    params = {'INPUT': multipart['OUTPUT'], 'OUTPUT':'memory:'}
    fix = processing.run("native:fixgeometries", params)

    return fix['OUTPUT']

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

def get_directions(layer, reference):
    reference = fix_polygon_layers(reference)
    params = {'INPUT':layer,'ALL_PARTS':False,'OUTPUT':'TEMPORARY_OUTPUT'}
    centroids = processing.run("native:centroids", params)
    params = {'INPUT':centroids['OUTPUT'],'REFERENCE_LAYER':reference,'TOLERANCE':10,'BEHAVIOR':0,'OUTPUT':'TEMPORARY_OUTPUT'}
    direction = processing.run("qgis:snapgeometries", params)

    return direction['OUTPUT'] 