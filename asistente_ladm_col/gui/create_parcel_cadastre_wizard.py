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
from functools import partial

from qgis.core import QgsEditFormConfig, QgsVectorLayerUtils, Qgis, QgsWkbTypes
from qgis.PyQt.QtCore import Qt, QPoint, QCoreApplication
from qgis.PyQt.QtWidgets import QAction, QWizard

from ..utils import get_ui_class
from ..config.table_mapping_config import (
    ID_FIELD,
    LA_BAUNIT_TYPE_TABLE,
    PARCEL_TABLE,
    PLOT_TABLE,
    UEBAUNIT_TABLE,
    UEBAUNIT_TABLE_PARCEL_FIELD,
    UEBAUNIT_TABLE_PLOT_FIELD,
    VIDA_UTIL_FIELD_BOUNDARY_TABLE
)

WIZARD_UI = get_ui_class('wiz_create_parcel_cadastre.ui')

class CreateParcelCadastreWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self._plot_layer = None
        self._parcel_layer = None
        self._uebaunit_table = None
        self._db = db
        self.qgis_utils = qgis_utils

        self.button(QWizard.FinishButton).clicked.connect(self.prepare_parcel_creation)

    def prepare_parcel_creation(self):
        # Load layers
        res_layers = self.qgis_utils.get_layers(self._db, {
            PLOT_TABLE: {'name':PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            PARCEL_TABLE: {'name':PARCEL_TABLE, 'geometry':None},
            LA_BAUNIT_TYPE_TABLE: {'name':LA_BAUNIT_TYPE_TABLE, 'geometry':None}, # Domain for Parcel
            UEBAUNIT_TABLE: {'name':UEBAUNIT_TABLE, 'geometry':None}}, load=True)

        self._plot_layer = res_layers[PLOT_TABLE]
        if self._plot_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateParcelCadastreWizard",
                                           "Plot layer couldn't be found..."),
                Qgis.Warning)
            return

        self._parcel_layer = res_layers[PARCEL_TABLE]
        if self._parcel_layer is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateParcelCadastreWizard",
                                           "Parcel layer couldn't be found..."),
                Qgis.Warning)
            return

        self._uebaunit_table = res_layers[UEBAUNIT_TABLE]
        if self._uebaunit_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateParcelCadastreWizard",
                                           "UEBAUNIT table couldn't be found..."),
                Qgis.Warning)
            return

        # Configure automatic fields
        self.qgis_utils.configureAutomaticField(self._parcel_layer, VIDA_UTIL_FIELD_BOUNDARY_TABLE, "now()")

        # Don't suppress (i.e., show) feature form
        form_config = self._parcel_layer.editFormConfig()
        form_config.setSuppress(QgsEditFormConfig.SuppressOff)
        self._parcel_layer.setEditFormConfig(form_config)

        self.edit_parcel()

    def edit_parcel(self):
        if self._plot_layer.selectedFeatureCount() == 1:
            # Open Form
            self.iface.layerTreeView().setCurrentLayer(self._parcel_layer)
            self._parcel_layer.startEditing()
            self.iface.actionAddFeature().trigger()

            plot_ids = [f['t_id'] for f in self._plot_layer.selectedFeatures()]

            # Create connections to react when a feature is added to buffer and
            # when it gets stored into the DB
            self._parcel_layer.featureAdded.connect(self.call_parcel_commit)
            self._parcel_layer.committedFeaturesAdded.connect(partial(self.finish_parcel, plot_ids))

        elif self._plot_layer.selectedFeatureCount() == 0:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateParcelCadastreWizard",
                                           "Please select a Plot"),
                Qgis.Warning)
        else: # >1
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateParcelCadastreWizard",
                                           "Please select only one Plot"),
                Qgis.Warning)

    def call_parcel_commit(self, fid):
        res = self._parcel_layer.commitChanges()
        if res:
            self._parcel_layer.featureAdded.disconnect(self.call_parcel_commit)
            print("Parcel's featureAdded SIGNAL disconnected")

    def finish_parcel(self, plot_ids, layerId, features):
        if len(features) != 1:
            print("We should have got only one predio... We cannot do anything with {} predios".format(len(features)))
        else:
            fid = features[0].id()
            if not self._parcel_layer.getFeature(fid).isValid():
                print("Feature not found in layer Predio...")
            else:
                parcel_id = self._parcel_layer.getFeature(fid)[ID_FIELD]

                # Fill uebaunit table
                new_features = []
                for plot_id in plot_ids:
                    new_feature = QgsVectorLayerUtils().createFeature(self._uebaunit_table)
                    new_feature.setAttribute(UEBAUNIT_TABLE_PLOT_FIELD, plot_id)
                    new_feature.setAttribute(UEBAUNIT_TABLE_PARCEL_FIELD, parcel_id)
                    print("Saving Plot-Parcel:", plot_id, parcel_id)
                    new_features.append(new_feature)

                self._uebaunit_table.dataProvider().addFeatures(new_features)

                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("CreateParcelCadastreWizard",
                                               "The new parcel (t_id={}) was successfully created and associated with its corresponding Terreno (t_id={})!".format(parcel_id, plot_ids[0])),
                    Qgis.Info)

        self._parcel_layer.committedFeaturesAdded.disconnect()
        print("Parcel's committedFeaturesAdded SIGNAL disconnected")
