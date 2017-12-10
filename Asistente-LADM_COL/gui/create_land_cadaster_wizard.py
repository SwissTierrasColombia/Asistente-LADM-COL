# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2017-12-09
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
from qgis.core import (QgsProject, QgsVectorLayer, QgsVectorLayerUtils,
                       QgsFeature, QgsMapLayerProxyModel, QgsWkbTypes)
from qgis.gui import QgsMessageBar
from qgis.PyQt.QtCore import Qt, QPoint
from qgis.PyQt.QtWidgets import QAction, QWizard

from ..utils import get_ui_class
from ..config.table_mapping_config import (
    LAND_TABLE,
    VIDA_UTIL_FIELD_BOUNDARY_TABLE
)

WIZARD_UI = get_ui_class('wiz_create_land_cadaster.ui')

class CreateLandCadasterWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self._land_layer = None
        self._db = db
        self.qgis_utils = qgis_utils

        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.PolygonLayer)

        self.button(QWizard.FinishButton).clicked.connect(self.create_land)

    def create_land(self):
        # Load layers
        self._land_layer = self.qgis_utils.get_layer(self._db, LAND_TABLE, QgsWkbTypes.PolygonGeometry, True)
        if self._land_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                self.tr("Land layer couldn't be found..."),
                QgsMessageBar.WARNING)
            return

        refactored_layer = self.mMapLayerComboBox.currentLayer()
        if refactored_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                self.tr("Refactored layer couldn't be found..."),
                QgsMessageBar.WARNING)
            return
        refactored_features = [f for f in refactored_layer.getFeatures()]

        features = []
        for f in refactored_features:
            attrs_list = f.attributes()
            attrs = {i:j for i,j in enumerate(attrs_list) if j != None and i!=0} # Exclude NULLs and t_id
            new_feature = QgsVectorLayerUtils().createFeature(self._land_layer, f.geometry(), attrs)
            features.append(new_feature)

        self._land_layer.startEditing()
        self._land_layer.addFeatures(features)
        self._land_layer.commitChanges()

        self.iface.messageBar().pushMessage("Asistente LADM_COL",
            self.tr("{} new land(s) has(have) been created!".format(len(features))),
            QgsMessageBar.INFO)
