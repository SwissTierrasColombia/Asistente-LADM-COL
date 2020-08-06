# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin                : 2020-08-05
        git sha              : :%H$
        copyright            : (C) 2020 by Germán Carrillo (SwissTierras Colombia)
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
import os
import sys

from qgis.PyQt.QtCore import (QCoreApplication,
                              pyqtSignal,
                              QObject)
from qgis.core import (QgsOfflineEditing,
                       QgsProject,
                       QgsRectangle)

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.general_config import PLUGINS_DIR
from asistente_ladm_col.config.layer_config import LayerConfig
from asistente_ladm_col.lib.logger import Logger


class FieldDataCapture(QObject):
    total_progress_updated = pyqtSignal(int)  # percentage

    def __init__(self):
        QObject.__init__(self)
        self.logger = Logger()
        self.app = AppInterface()

    def convert_to_offline(self, db, surveyor_expression_dict, export_dir):
        sys.path.append(PLUGINS_DIR)
        from qfieldsync.core.layer import LayerSource, SyncAction
        from qfieldsync.core.offline_converter import OfflineConverter
        from qfieldsync.core.project import ProjectConfiguration

        project = QgsProject.instance()
        extent = QgsRectangle()
        offline_editing = QgsOfflineEditing()

        # Configure project
        project_configuration = ProjectConfiguration(project)
        project_configuration.create_base_map = False
        project_configuration.offline_copy_only_aoi = False
        project_configuration.use_layer_selection = True

        # Layer config
        layer_sync_action = LayerConfig.get_field_data_capture_layer_config(db.names)

        total_projects = len(surveyor_expression_dict)
        current_progress = 0

        for surveyor, layer_config in surveyor_expression_dict.items():
            export_folder = os.path.join(export_dir, surveyor)

            # Get layers (cannot be done out of this for loop because the project is closed and layers are deleted)
            layers = {layer_name: None for layer_name, _ in layer_sync_action.items()}
            self.app.core.get_layers(db, layers, True)
            if not layers:
                return False, QCoreApplication.translate("FieldDataCapture", "At least one layer could not be found.")

            # Configure layers
            for layer_name, layer in layers.items():
                layer_source = LayerSource(layer)
                layer_source.action = layer_sync_action[layer_name]
                if layer_name in layer_config:
                    layer_source.select_expression = layer_config[layer_name]
                layer_source.apply()

            offline_converter = OfflineConverter(project, export_folder, extent, offline_editing)
            offline_converter.convert()
            offline_editing.layerProgressUpdated.disconnect(offline_converter.on_offline_editing_next_layer)
            offline_editing.progressModeSet.disconnect(offline_converter.on_offline_editing_max_changed)
            offline_editing.progressUpdated.disconnect(offline_converter.offline_editing_task_progress)

            current_progress += 1
            self.total_progress_updated.emit(int(100*current_progress/total_projects))

        return True, QCoreApplication.translate("FieldDataCapture", "{} offline projects have been successfully created!").format(total_projects)