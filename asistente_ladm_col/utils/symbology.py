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

from asistente_ladm_col.config.general_config import STYLES_DIR
from asistente_ladm_col.config.layer_config import LayerConfig
from asistente_ladm_col.config.symbology import Symbology
from asistente_ladm_col.lib.logger import Logger


class SymbologyUtils(QObject):

    layer_symbology_changed = pyqtSignal(str) # layer id

    def __init__(self):
        QObject.__init__(self)
        self.logger = Logger()

    def set_layer_style_from_qml(self, db, layer, is_error_layer=False, emit=False, layer_modifiers=dict()):
        style_group = Symbology().get_default_style_group(db.names)
        style_group_const = Symbology().get_default_style_group(db.names)
        style_custom_error_layers = Symbology().get_custom_error_layers()

        if LayerConfig.STYLE_GROUP_LAYER_MODIFIERS in layer_modifiers:
            if layer_modifiers[LayerConfig.STYLE_GROUP_LAYER_MODIFIERS]:
                # By default symbology layer user default style group
                # but it could be update if a layer modifiers it send
                # e.g STYLE_GROUP_LAYER_MODIFIERS could be Symbology().get_supplies_style_group()
                style_group = layer_modifiers[LayerConfig.STYLE_GROUP_LAYER_MODIFIERS]

        qml_name = None
        if is_error_layer:
            if layer.name() in style_custom_error_layers:
                qml_name = style_custom_error_layers.get(layer.name())
            else:
                qml_name = Symbology().get_default_error_style_layer().get(layer.geometryType())
        else:
            if db is None:
                return

            layer_name = db.get_ladm_layer_name(layer)
            qml_name = style_group.get(layer_name)

            # If style not in style group then we use default symbology
            if qml_name is None:
                qml_name = style_group_const.get(layer_name)

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
            self.logger.warning(__name__, "Unable to read style file from {}".format(style_path))

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
