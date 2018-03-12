# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-03-06
        git sha              : :%H$
        copyright            : (C) 2018 by Sergio Ramírez (Incige SAS)
        email                : seralra96@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.core import QgsEditFormConfig, QgsVectorLayerUtils, Qgis, QgsWkbTypes
from qgis.gui import QgsMessageBar
from qgis.PyQt.QtCore import Qt, QPoint, QCoreApplication
from qgis.PyQt.QtWidgets import QAction, QWizard

from ..utils import get_ui_class
#from ..utils.qt_utils import enable_next_wizard, disable_next_wizard
from ..config.table_mapping_config import (
    ADMINISTRATIVE_SOURCE_TABLE,
    AVAILABILITY_STATE_TABLE,
    ADMINISTRATIVE_SOURCE_TYPE_TABLE,
    VIDA_UTIL_FIELD_BOUNDARY_TABLE
)

WIZARD_UI = get_ui_class('wiz_create_administrative_source_cadastre.ui')

class CreateAdministrativeSourceCadastreWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self._administrative_source_layer = None
        self._db = db
        self.qgis_utils = qgis_utils

        self.button(QWizard.FinishButton).clicked.connect(self.prepare_administrative_source_creation)

    def prepare_administrative_source_creation(self):
        # Load layers
        res_layers = self.qgis_utils.get_layers(self._db, {
            ADMINISTRATIVE_SOURCE_TABLE: {'name': ADMINISTRATIVE_SOURCE_TABLE, 'geometry': None},
            ADMINISTRATIVE_SOURCE_TYPE_TABLE: {'name': ADMINISTRATIVE_SOURCE_TYPE_TABLE, 'geometry': None},
            AVAILABILITY_STATE_TABLE: {'name': AVAILABILITY_STATE_TABLE, 'geometry': None}}, load=True)

        self._administrative_source_layer = res_layers[ADMINISTRATIVE_SOURCE_TABLE]
        if self._administrative_source_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateAdministrativeSourceCadastreWizard",
                                           "Administrative Source layer couldn't be found..."),
                Qgis.Warning)
            return

        # Configure automatic fields
        self.qgis_utils.set_automatic_fields(self._administrative_source_layer, "s")

        # Don't suppress (i.e., show) feature form
        form_config = self._administrative_source_layer.editFormConfig()
        form_config.setSuppress(QgsEditFormConfig.SuppressOff)
        self._administrative_source_layer.setEditFormConfig(form_config)

        self.edit_administrative_source()

    def edit_administrative_source(self):
        # Open Form
        self.iface.layerTreeView().setCurrentLayer(self._administrative_source_layer)
        self._administrative_source_layer.startEditing()
        self.iface.actionAddFeature().trigger()
