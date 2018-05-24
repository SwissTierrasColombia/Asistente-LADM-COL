# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-04-16
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

from qgis.core import (
    QgsFillSymbol,
    QgsLineSymbol,
    QgsMarkerSymbol,
    QgsSingleSymbolRenderer,
    QgsVectorLayerSimpleLabeling,
    QgsTextFormat,
    QgsTextBufferSettings,
    QgsPalLayerSettings,
    QgsMapLayer,
    QgsEffectStack,
    QgsDrawSourceEffect,
    QgsDropShadowEffect,
    QgsInnerShadowEffect,
    QgsSimpleMarkerSymbolLayer,
    QgsOuterGlowEffect,
    QgsOuterGlowEffect,
    QgsSimpleLineSymbolLayer,
    QgsWkbTypes,
    QgsFeatureRenderer,
    QgsAbstractVectorLayerLabeling,
    QgsReadWriteContext
)
from qgis.PyQt.QtCore import QObject, pyqtSignal, QFile, QIODevice
from qgis.PyQt.QtXml import QDomDocument

from ..config.general_config import STYLES_DIR
from ..config.symbology import LAYER_QML_STYLE

class SymbologyUtils(QObject):

    layer_symbology_changed = pyqtSignal(str) # layer id

    def __init__(self):
        QObject.__init__(self)

    def set_layer_style_from_qml(self, layer, emit=True):
        if layer.name() in LAYER_QML_STYLE:
            renderer, labeling = self.get_style_from_qml(LAYER_QML_STYLE[layer.name()][layer.geometryType()])
            if renderer:
                layer.setRenderer(renderer)
                if emit:
                    self.layer_symbology_changed.emit(layer.id())
            if labeling:
                layer.setLabeling(labeling)
                layer.setLabelsEnabled(True)

    def get_style_from_qml(self, qml_name):
        renderer = None
        labeling = None

        style_path = os.path.join(STYLES_DIR, qml_name + '.qml')
        file = QFile(style_path)
        if not file.open(QIODevice.ReadOnly | QIODevice.Text):
            print("Unable to read style file from", style_path)

        doc = QDomDocument()
        doc.setContent(file)
        file.close()
        doc_elem = doc.documentElement()

        nodes = doc_elem.elementsByTagName("renderer-v2")
        if nodes.count():
            renderer_elem = nodes.at(0).toElement()
            renderer = QgsFeatureRenderer.load(renderer_elem, QgsReadWriteContext())

        nodes = doc_elem.elementsByTagName("labeling")
        if nodes.count():
            labeling_elem = nodes.at(0).toElement()
            labeling = QgsAbstractVectorLayerLabeling.create(labeling_elem, QgsReadWriteContext())

        return (renderer, labeling)

    def set_point_error_symbol(self, layer):
        if not(layer.isSpatial() and layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QgsWkbTypes.PointGeometry):
            return None

        draw_source_effect_properties = {'enabled': '1', 'opacity': '1', 'draw_mode': '2', 'blend_mode': '0'}
        drop_shadow_effect_properties = {'enabled': '1', 'opacity': '1', 'draw_mode': '2', 'blend_mode': '0', 'offset_unit': 'MM', 'offset_angle': '135', 'offset_unit_scale': '3x:0,0,0,0,0,0', 'offset_distance': '2', 'blur_level': '10', 'color': '0,0,0,255'}

        draw_source_effect_0 = QgsDrawSourceEffect().create(draw_source_effect_properties)
        draw_source_effect_1 = draw_source_effect_0.clone()
        drop_shadow_effect = QgsDropShadowEffect().create(drop_shadow_effect_properties)

        effect_stack_0 = QgsEffectStack()
        effect_stack_0.appendEffect(drop_shadow_effect)
        effect_stack_0.appendEffect(draw_source_effect_0)
        effect_stack_1 = QgsEffectStack()
        effect_stack_1.appendEffect(draw_source_effect_1)

        simple_point_symbol_layer_properties_0 = {'vertical_anchor_point': '1', 'outline_width_unit': 'MM', 'offset_map_unit_scale': '3x:0,0,0,0,0,0', 'outline_width': '0.2', 'size': '3.4', 'angle': '0', 'joinstyle': 'bevel', 'outline_style': 'solid', 'scale_method': 'area', 'outline_width_map_unit_scale': '3x:0,0,0,0,0,0', 'name': 'circle', 'horizontal_anchor_point': '1', 'size_map_unit_scale': '3x:0,0,0,0,0,0', 'offset_unit': 'MM', 'color': '255,0,0,255', 'outline_color': '255,0,0,255', 'size_unit': 'MM', 'offset': '0,0'}
        simple_point_symbol_layer_properties_1 = {'vertical_anchor_point': '1', 'outline_width_unit': 'MM', 'offset_map_unit_scale': '3x:0,0,0,0,0,0', 'outline_width': '0.2', 'size': '2.4', 'angle': '34', 'joinstyle': 'bevel', 'outline_style': 'solid', 'scale_method': 'area', 'outline_width_map_unit_scale': '3x:0,0,0,0,0,0', 'name': 'circle', 'horizontal_anchor_point': '1', 'size_map_unit_scale': '3x:0,0,0,0,0,0', 'offset_unit': 'MM', 'color': '255,0,0,255', 'outline_color': '255,0,0,255', 'size_unit': 'MM', 'offset': '0,0'}
        simple_point_symbol_layer_0 = QgsSimpleMarkerSymbolLayer().create(simple_point_symbol_layer_properties_0)
        simple_point_symbol_layer_0.setPaintEffect(effect_stack_0)
        simple_point_symbol_layer_1 = QgsSimpleMarkerSymbolLayer().create(simple_point_symbol_layer_properties_1)
        simple_point_symbol_layer_1.setPaintEffect(effect_stack_1)

        point_symbol = QgsMarkerSymbol()
        point_symbol.appendSymbolLayer(simple_point_symbol_layer_0)
        point_symbol.appendSymbolLayer(simple_point_symbol_layer_1)
        layer.setRenderer(QgsSingleSymbolRenderer(point_symbol))
        self.layer_symbology_changed.emit(layer.id())

    def set_line_error_symbol(self, layer):
        if not(layer.isSpatial() and layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QgsWkbTypes.LineGeometry):
            return None

        outer_glow_effect_properties = {'blend_mode': '0', 'blur_level': '3', 'draw_mode': '2', 'color2': '0,255,0,255', 'discrete': '0', 'spread_unit_scale': '3x:0,0,0,0,0,0', 'color_type': '0', 'spread_unit': 'MM', 'spread': '2', 'color1': '0,0,255,255', 'rampType': 'gradient', 'single_color': '239,41,41,255', 'opacity': '0.5', 'enabled': '1'}
        draw_source_effect_properties = {'blend_mode': '0', 'draw_mode': '2', 'enabled': '1', 'opacity': '1'}
        inner_shadow_effect_properties = {'offset_angle': '135', 'blend_mode': '13', 'blur_level': '10', 'draw_mode': '2', 'color': '0,0,0,255', 'offset_distance': '2', 'offset_unit': 'MM', 'offset_unit_scale': '3x:0,0,0,0,0,0', 'opacity': '0.146', 'enabled': '1'}

        outer_glow_effect = QgsOuterGlowEffect().create(outer_glow_effect_properties)
        draw_source_effect = QgsDrawSourceEffect().create(draw_source_effect_properties)
        inner_shadow_effect = QgsInnerShadowEffect().create(inner_shadow_effect_properties)

        effect_stack = QgsEffectStack()
        effect_stack.appendEffect(outer_glow_effect)
        effect_stack.appendEffect(draw_source_effect)
        effect_stack.appendEffect(inner_shadow_effect)

        simple_line_symbol_layer_properties = {'draw_inside_polygon': '0', 'line_color': '227,26,28,255', 'customdash_map_unit_scale': '3x:0,0,0,0,0,0', 'joinstyle': 'round', 'width_map_unit_scale': '3x:0,0,0,0,0,0', 'customdash': '5;2', 'capstyle': 'round', 'offset': '0', 'offset_map_unit_scale': '3x:0,0,0,0,0,0', 'customdash_unit': 'MM', 'use_custom_dash': '0', 'offset_unit': 'MM', 'line_width_unit': 'MM', 'line_width': '1.46', 'line_style': 'solid'}
        simple_line_symbol_layer = QgsSimpleLineSymbolLayer().create(simple_line_symbol_layer_properties)
        simple_line_symbol_layer.setPaintEffect(effect_stack)

        line_symbol = QgsLineSymbol()
        line_symbol.appendSymbolLayer(simple_line_symbol_layer)
        layer.setRenderer(QgsSingleSymbolRenderer(line_symbol))
        self.layer_symbology_changed.emit(layer.id())
