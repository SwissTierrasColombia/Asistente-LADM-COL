"""
/***************************************************************************
                              Asistente LADM-COL
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
    def __init__(self):
        QObject.__init__(self)
        self.logger = Logger()

    def set_layer_style_from_qml(self, db, layer, emit=False, layer_modifiers=dict(), models=list()):  # TODO: Add tests
        if db is None:
            self.logger.critical(__name__, "DB connection is none. Style not set.")
            return

        qml_name = None
        if db.is_ladm_layer(layer):
            layer_name = db.get_ladm_layer_name(layer)
        else:
            layer_name = layer.name()  # we identify some error layer styles using the error table names

        # Check if we should use modifier style group
        if LayerConfig.STYLE_GROUP_LAYER_MODIFIERS in layer_modifiers:
            style_group_modifiers = layer_modifiers.get(LayerConfig.STYLE_GROUP_LAYER_MODIFIERS)

            if style_group_modifiers:
                qml_name = style_group_modifiers.get(layer_name)

        if not qml_name:  # If None or empty string, we use default styles
            qml_name = Symbology().get_default_style_group(db.names, models).get(layer_name)

        if qml_name:
            self.set_style_from_qml_name(layer, qml_name)

    @staticmethod
    def set_style_from_qml_name(layer, qml_name, force_repaint=False):
        renderer, labeling = SymbologyUtils.get_style_from_qml(qml_name)
        if renderer:
            layer.setRenderer(renderer)
        if labeling:
            layer.setLabeling(labeling)
            layer.setLabelsEnabled(True)

        if force_repaint:
            layer.triggerRepaint()

    @staticmethod
    def get_style_from_qml(qml_name):
        renderer = None
        labeling = None

        style_path = os.path.join(STYLES_DIR, qml_name + '.qml')
        file = QFile(style_path)
        if not file.open(QIODevice.ReadOnly | QIODevice.Text):
            Logger().warning(__name__, "Unable to read style file from {}".format(style_path))

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

        return renderer, labeling
