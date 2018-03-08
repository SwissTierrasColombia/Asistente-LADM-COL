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
    RESTRICTION_TABLE,
    RESTRICTION_TYPE_TABLE,
    NATURAL_PARTY_TABLE,
    LEGAL_PARTY_TABLE,
    PARCEL_TABLE,
    LA_BAUNIT_TABLE,
    LA_GROUP_PARTY,
    VIDA_UTIL_FIELD_BOUNDARY_TABLE
)

WIZARD_UI = get_ui_class('wiz_create_restriction_cadastre.ui')

class CreateRestrictionCadastreWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self._plot_layer = None
        self._db = db
        self.qgis_utils = qgis_utils

        self.button(QWizard.FinishButton).clicked.connect(self.prepare_restriction_creation)

    def prepare_restriction_creation(self):
        # Load layers
        res_layers = self.qgis_utils.get_layers(self._db, {
            RESTRICTION_TABLE: {'name':RESTRICTION_TABLE, 'geometry':None},
            RESTRICTION_TYPE_TABLE: {'name':RESTRICTION_TYPE_TABLE, 'geometry':None},
            NATURAL_PARTY_TABLE: {'name':NATURAL_PARTY_TABLE, 'geometry':None},
            LEGAL_PARTY_TABLE:{'name':LEGAL_PARTY_TABLE, 'geometry':None},
            PARCEL_TABLE:{'name':PARCEL_TABLE, 'geometry':None},
            LA_BAUNIT_TABLE:{'name':LA_BAUNIT_TABLE, 'geometry':None},
            LA_GROUP_PARTY:{'name':LA_GROUP_PARTY, 'geometry':None}}, load=True)

        self._restriction_layer = res_layers[RESTRICTION_TABLE]
        if self._restriction_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateAdministrativeSourceCadastreWizard",
                                           "Administrative Source layer couldn't be found..."),
                Qgis.Warning)
            return

        # Configure automatic fields
        self.qgis_utils.configureAutomaticField(self._restriction_layer, VIDA_UTIL_FIELD_BOUNDARY_TABLE, "now()")

        # Configure relation fields

        # Don't suppress (i.e., show) feature form
        form_config = self._restriction_layer.editFormConfig()
        form_config.setSuppress(QgsEditFormConfig.SuppressOff)
        self._restriction_layer.setEditFormConfig(form_config)

        self.edit_spatial_source()

    def edit_spatial_source(self):
        # Open Form
        self.iface.layerTreeView().setCurrentLayer(self._restriction_layer)
        self._restriction_layer.startEditing()
        self.iface.actionAddFeature().trigger()
