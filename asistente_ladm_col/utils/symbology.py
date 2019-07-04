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

from qgis.PyQt.QtCore import (QObject,
                              pyqtSignal,
                              QFile,
                              QIODevice)
from qgis.PyQt.QtXml import QDomDocument
from qgis.core import (QgsFeatureRenderer,
                       QgsAbstractVectorLayerLabeling,
                       QgsReadWriteContext)

from ..config.translator import QGIS_LANG, DEFAULT_LANGUAGE
from ..config.general_config import (STYLES_DIR,
                                     STYLE_GROUP_LAYER_MODIFIERS)
from ..config.symbology import (DEFAULT_STYLE_GROUP,
                                CUSTOM_ERROR_LAYERS,
                                ERROR_LAYER)


class SymbologyUtils(QObject):

    layer_symbology_changed = pyqtSignal(str) # layer id

    def __init__(self):
        QObject.__init__(self)

    def set_layer_style_from_qml(self, db, layer, is_error_layer=False, emit=False, layer_modifiers=dict()):
        style_group = DEFAULT_STYLE_GROUP
        if STYLE_GROUP_LAYER_MODIFIERS in layer_modifiers:
            if layer_modifiers[STYLE_GROUP_LAYER_MODIFIERS]:
                style_group = layer_modifiers[STYLE_GROUP_LAYER_MODIFIERS]

        qml_name = None
        if is_error_layer:
            if layer.name() in CUSTOM_ERROR_LAYERS:
                # Symbology is selected according to the language
                if QGIS_LANG in CUSTOM_ERROR_LAYERS[layer.name()]:
                    qml_name = CUSTOM_ERROR_LAYERS[layer.name()][QGIS_LANG]
                else:
                    qml_name = CUSTOM_ERROR_LAYERS[layer.name()][DEFAULT_LANGUAGE]
            else:
                qml_name = DEFAULT_STYLE_GROUP[ERROR_LAYER][layer.geometryType()]
        else:
            if db is None:
                return

            layer_name = db.get_ladm_layer_name(layer)

            if layer_name in style_group:
                if layer.geometryType() in style_group[layer_name]:
                    qml_name = style_group[layer_name][layer.geometryType()]

            # If style not in style group then we use default simbology
            if qml_name is None:
                if layer_name in DEFAULT_STYLE_GROUP:
                    if layer.geometryType() in DEFAULT_STYLE_GROUP[layer_name]:
                        qml_name = DEFAULT_STYLE_GROUP[layer_name][layer.geometryType()]

        if qml_name is not None:
            renderer, labeling = self.get_style_from_qml(qml_name)
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
