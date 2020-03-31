# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2017-11-14
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BSF Swissphoto)
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
import ast
import datetime
import glob
import json
import os

from qgis.PyQt.QtCore import (Qt,
                              QObject,
                              pyqtSignal,
                              QCoreApplication,
                              QSettings,
                              QEventLoop,
                              QTextStream,
                              QIODevice,
                              QUrl)
from qgis.PyQt.QtWidgets import (QProgressBar,
                                 QDialog)
from qgis.PyQt.QtNetwork import (QNetworkAccessManager,
                                 QNetworkRequest)
from qgis.core import (Qgis,
                       QgsApplication,
                       QgsEditFormConfig,
                       QgsAttributeEditorContainer,
                       QgsAttributeEditorElement,
                       QgsDefaultValue,
                       QgsEditorWidgetSetup,
                       QgsExpression,
                       QgsExpressionContextUtils,
                       QgsFieldConstraints,
                       QgsLayerTreeGroup,
                       QgsLayerTreeNode,
                       QgsMapLayer,
                       QgsOptionalExpression,
                       QgsProject,
                       QgsTolerance,
                       QgsSnappingConfig,
                       QgsProperty,
                       QgsRelation,
                       QgsVectorLayer)

import processing

from asistente_ladm_col.gui.dialogs.dlg_topological_edition import LayersForTopologicalEditionDialog
from asistente_ladm_col.utils.decorators import _activate_processing_plugin
from asistente_ladm_col.lib.geometry import GeometryUtils
from asistente_ladm_col.utils.qgis_model_baker_utils import QgisModelBakerUtils
from asistente_ladm_col.utils.qt_utils import (OverrideCursor,
                                               ProcessWithStatus)
from asistente_ladm_col.utils.utils import is_connected
from asistente_ladm_col.utils.symbology import SymbologyUtils
from asistente_ladm_col.config.general_config import (DEFAULT_EPSG,
                                                      FIELD_MAPPING_PATH,
                                                      MAXIMUM_FIELD_MAPPING_FILES_PER_TABLE,
                                                      TEST_SERVER,
                                                      DEFAULT_ENDPOINT_SOURCE_SERVICE,
                                                      SOURCE_SERVICE_EXPECTED_ID)
from asistente_ladm_col.config.enums import EnumLayerRegistryType
from asistente_ladm_col.config.transitional_system_config import TransitionalSystemConfig
from asistente_ladm_col.config.layer_config import LayerConfig
from asistente_ladm_col.config.refactor_fields_mappings import RefactorFieldsMappings
from asistente_ladm_col.config.query_names import QueryNames
from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.config.translation_strings import (TranslatableConfigStrings,
                                                           ERROR_LAYER_GROUP)
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.source_handler import SourceHandler


class QGISUtils(QObject):
    action_add_feature_requested = pyqtSignal()
    action_vertex_tool_requested = pyqtSignal()
    activate_layer_requested = pyqtSignal(QgsMapLayer)
    create_progress_message_bar_emitted = pyqtSignal(str, QProgressBar)
    layer_symbology_changed = pyqtSignal(str) # layer id
    map_refresh_requested = pyqtSignal()
    map_freeze_requested = pyqtSignal(bool)
    zoom_full_requested = pyqtSignal()
    zoom_to_selected_requested = pyqtSignal()
    set_node_visibility_requested = pyqtSignal(QgsLayerTreeNode, bool)

    def __init__(self):
        QObject.__init__(self)
        self.logger = Logger()
        self.qgis_model_baker_utils = QgisModelBakerUtils()
        self.symbology = SymbologyUtils()
        self.geometry = GeometryUtils()
        self.translatable_config_strings = TranslatableConfigStrings()
        self.refactor_fields = RefactorFieldsMappings()

