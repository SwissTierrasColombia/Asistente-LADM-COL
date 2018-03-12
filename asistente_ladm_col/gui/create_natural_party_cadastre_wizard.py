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
from qgis.PyQt.QtCore import Qt, QPoint, QCoreApplication, QSettings
from qgis.PyQt.QtWidgets import QAction, QWizard

from ..utils import get_ui_class
#from ..utils.qt_utils import enable_next_wizard, disable_next_wizard
from ..config.table_mapping_config import (
    GENDER_TYPE_TABLE,
    NATURAL_PARTY_TABLE,
    PARTY_DOCUMENT_TYPE_TABLE,
    PARTY_TYPE_TABLE)

WIZARD_UI = get_ui_class('wiz_create_natural_party_cadastre.ui')

class CreateNaturalPartyCadastreWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self._natural_party_layer = None
        self._db = db
        self.qgis_utils = qgis_utils

        self.button(QWizard.FinishButton).clicked.connect(self.prepare_natural_party_creation)

    def prepare_natural_party_creation(self):
        # Load layers
        res_layers = self.qgis_utils.get_layers(self._db, {
            NATURAL_PARTY_TABLE: {'name': NATURAL_PARTY_TABLE, 'geometry': None},
            PARTY_DOCUMENT_TYPE_TABLE: {'name': PARTY_DOCUMENT_TYPE_TABLE, 'geometry': None},
            PARTY_TYPE_TABLE: {'name': PARTY_TYPE_TABLE, 'geometry': None},
            GENDER_TYPE_TABLE: {'name': GENDER_TYPE_TABLE, 'geometry': None}}, load=True)

        self._natural_party_layer = res_layers[NATURAL_PARTY_TABLE]
        if self._natural_party_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateNaturalPartyCadastreWizard",
                                           "Natural Party layer couldn't be found..."),
                Qgis.Warning)
            return

        # Configure automatic fields
        self.qgis_utils.set_automatic_fields(self._natural_party_layer, "p")

        # Don't suppress (i.e., show) feature form
        form_config = self._natural_party_layer.editFormConfig()
        form_config.setSuppress(QgsEditFormConfig.SuppressOff)
        self._natural_party_layer.setEditFormConfig(form_config)

        self.edit_natural_party()

    def edit_natural_party(self):
        # Open Form
        self.iface.layerTreeView().setCurrentLayer(self._natural_party_layer)
        self._natural_party_layer.startEditing()
        self.iface.actionAddFeature().trigger()
