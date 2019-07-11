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
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtWidgets import QDialog
from qgis.core import (QgsProject,
                       Qgis)
from ..config.general_config import LAYER
from ..gui.dialogs.dlg_topological_edition import LayersForTopologicalEdition


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

            layers = dlg.selected_layers_info
            self.qgis_utils.get_layers(db, layers, load=True)
            if not layers:
                return None

            list_layers = list()
            # Open edit session in all layers
            for layer_name, layer_info in layers.items():
                layer = layers[layer_name][LAYER]
                layer.startEditing()
                list_layers.append(layer)

            # Activate "Vertex Tool (All Layers)"
            self.qgis_utils.activate_layer_requested.emit(list_layers[0])
            self.qgis_utils.action_vertex_tool_requested.emit()

            self.qgis_utils.message_with_duration_emitted.emit(
                QCoreApplication.translate("QGISUtils", "You can start moving nodes in layers {} and {}, simultaneously!").format(
                    ", ".join(layer.name() for layer in list_layers[:-1]), list_layers[-1].name()),
                Qgis.Info, 30)
