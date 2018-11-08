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

from .dlg_topological_edition import LayersForTopologicalEdition


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
