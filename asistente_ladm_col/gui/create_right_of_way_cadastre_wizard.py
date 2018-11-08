# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 06/09/18
        git sha              : :%H$
        copyright            : (C) 2018 by Sergio Ramírez (Incige SAS)
        email                : sergio.ramirez@incige.com
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

from qgis.core import (QgsProject, QgsVectorLayer, QgsEditFormConfig,
                       QgsSnappingConfig, QgsTolerance, QgsFeature, Qgis,
                       QgsMapLayerProxyModel, QgsWkbTypes, QgsApplication,
                       QgsProcessingException, QgsProcessingFeedback)

from qgis.PyQt.QtCore import Qt, QPoint, QCoreApplication, QSettings
from qgis.PyQt.QtWidgets import QAction, QWizard

import processing
from ..utils import get_ui_class
from ..config.table_mapping_config import RIGHT_OF_WAY_TABLE, SURVEY_POINT_TABLE
from ..config.general_config import (
    DEFAULT_EPSG,
    PLUGIN_NAME,
    TranslatableConfigStrings
)
from ..config.help_strings import HelpStrings

WIZARD_UI = get_ui_class('wiz_create_right_of_way_cadastre.ui')

class CreateRightOfWayCadastreWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._right_of_way_layer = None
        self._right_of_way_line_layer = None
        self._survey_point_layer = None
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()
        self.translatable_config_strings = TranslatableConfigStrings()


        self.restore_settings()

        self.rad_digitizing.toggled.connect(self.adjust_page_1_controls)
        self.rad_digitizing_line.toggled.connect(self.adjust_page_1_controls)
        self.adjust_page_1_controls()
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)

        self.width_line_edit.setValue(1.0)

        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.PolygonLayer)

    def adjust_page_1_controls(self):
        if self.rad_refactor.isChecked():
            self.lbl_width.setEnabled(False)
            self.width_line_edit.setEnabled(False)
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            finish_button_text = 'Import'
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(RIGHT_OF_WAY_TABLE, True))

        elif self.rad_digitizing.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_width.setEnabled(False)
            self.width_line_edit.setEnabled(False)
            finish_button_text = QCoreApplication.translate('CreateRightOfWayCadastreWizard', 'Start')
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_CREATE_RIGHT_OF_WAY_CADASTRE_PAGE_1_OPTION_POINTS)

        elif self.rad_digitizing_line.isChecked():
            self.width_line_edit.setEnabled(True)
            self.lbl_width.setEnabled(True)
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            finish_button_text = QCoreApplication.translate('CreateRightOfWayCadastreWizard', 'Start')
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_CREATE_RIGHT_OF_WAY_CADASTRE_PAGE_1_OPTION2_POINTS)

        self.wizardPage1.setButtonText(QWizard.FinishButton,
                                       QCoreApplication.translate('CreateRightOfWayCadastreWizard',
                                       finish_button_text))

    def finished_dialog(self):
        self.save_settings()

        if self.rad_refactor.isChecked():
            if self.mMapLayerComboBox.currentLayer() is not None:
                self.qgis_utils.show_etl_model(self._db,
                                               self.mMapLayerComboBox.currentLayer(),
                                               RIGHT_OF_WAY_TABLE)
            else:
                self.iface.messageBar().pushMessage('Asistente LADM_COL',
                    QCoreApplication.translate('CreateRightOfWayCadastreWizard',
                                               "Select a source layer to set the field mapping to '{}'.").format(RIGHT_OF_WAY_TABLE),
                    Qgis.Warning)

        elif self.rad_digitizing.isChecked():
            self.prepare_right_of_way_creation()

        elif self.rad_digitizing_line.isChecked():
            self.prepare_right_if_way_line_creation()

    def add_db_required_layers(self):
        # Load layers
        res_layers = self.qgis_utils.get_layers(self._db, {
            RIGHT_OF_WAY_TABLE: {'name': RIGHT_OF_WAY_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            SURVEY_POINT_TABLE: {'name': SURVEY_POINT_TABLE, 'geometry': None}
        }, load=True)

        self._right_of_way_layer = res_layers[RIGHT_OF_WAY_TABLE]
        self._survey_point_layer = res_layers[SURVEY_POINT_TABLE]

        if self._right_of_way_layer is None:
            self.iface.messageBar().pushMessage('Asistente LADM_COL',
                QCoreApplication.translate('CreateRightOfWayCadastreWizard',
                                           "Right of Way layer couldn't be found... {}").format(self._db.get_description()),
                Qgis.Warning)
            return

        if self._survey_point_layer is None:
            self.iface.messageBar().pushMessage('Asistente LADM_COL',
                QCoreApplication.translate('CreateRightOfWayCadastreWizard',
                                           "Survey Point layer couldn't be found... {}").format(self._db.get_description()),
                Qgis.Warning)
            return

    def set_layers_settings(self):
        # Disable transactions groups
        QgsProject.instance().setAutoTransaction(False)

        # Configure Snapping
        snapping = QgsProject.instance().snappingConfig()
        snapping.setEnabled(True)
        snapping.setMode(QgsSnappingConfig.AllLayers)
        snapping.setType(QgsSnappingConfig.Vertex)
        snapping.setUnits(QgsTolerance.Pixels)
        snapping.setTolerance(9)
        QgsProject.instance().setSnappingConfig(snapping)

    def prepare_right_of_way_creation(self):
        # Load layers
        self.add_db_required_layers()

        # Disable transactions groups and configure Snapping
        self.set_layers_settings()

        # Don't suppress feature form
        form_config = self._right_of_way_layer.editFormConfig()
        form_config.setSuppress(QgsEditFormConfig.SuppressOff)
        self._right_of_way_layer.setEditFormConfig(form_config)

        # Enable edition mode
        self.iface.layerTreeView().setCurrentLayer(self._right_of_way_layer)
        self._right_of_way_layer.startEditing()
        self.iface.actionAddFeature().trigger()

        self.iface.messageBar().pushMessage('Asistente LADM_COL',
            QCoreApplication.translate('CreateRightOfWayCadastreWizard',
                                       "You can now start capturing right of way digitizing on the map..."),
            Qgis.Info)

    def prepare_right_if_way_line_creation(self):
        # Load layers
        self.add_db_required_layers()

        # Add Memory line layer
        self._right_of_way_line_layer = QgsVectorLayer("MultiLineString?crs=EPSG:{}".format(DEFAULT_EPSG),
                                    self.translatable_config_strings.RIGHT_OF_WAY_LINE_LAYER, "memory")
        QgsProject.instance().addMapLayer(self._right_of_way_line_layer, True)

        # Disable transactions groups and configure Snapping
        self.set_layers_settings()

        # Suppress feature form
        form_config = self._right_of_way_line_layer.editFormConfig()
        form_config.setSuppress(QgsEditFormConfig.SuppressOn)
        self._right_of_way_line_layer.setEditFormConfig(form_config)

        # Enable edition mode
        self.iface.layerTreeView().setCurrentLayer(self._right_of_way_line_layer)
        self._right_of_way_line_layer.startEditing()
        self.iface.actionAddFeature().trigger()

        self._right_of_way_line_layer.featureAdded.connect(self.call_right_of_way_line_commit)
        self._right_of_way_line_layer.committedFeaturesAdded.connect(partial(self.finish_right_of_way_line))

        self.iface.messageBar().pushMessage('Asistente LADM_COL',
            QCoreApplication.translate('CreateRightOfWayCadastreWizard',
                                       "You can now start capturing line right of way digitizing on the map..."),
            Qgis.Info)

    def call_right_of_way_line_commit(self, fid):
        self._right_of_way_line_layer.featureAdded.disconnect(self.call_right_of_way_line_commit)
        self.log.logMessage("RigthOfWayLine's featureAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        res = self._right_of_way_line_layer.commitChanges()

    def finish_right_of_way_line(self, layerId, features):
        self._right_of_way_line_layer.committedFeaturesAdded.disconnect()
        self.log.logMessage("RigthOfWayLine's committedFeaturesAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        params = {'INPUT':self._right_of_way_line_layer,
                  'DISTANCE':self.width_line_edit.value(),
                  'SEGMENTS':5,
                  'END_CAP_STYLE':1,
                  'JOIN_STYLE':2,
                  'MITER_LIMIT':2,
                  'DISSOLVE':False,
                  'OUTPUT':'memory:'}
        buffered_right_of_way_layer = processing.run("native:buffer", params)['OUTPUT']
        QgsProject.instance().addMapLayer(buffered_right_of_way_layer, True)


    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/wizards/right_of_way_load_data_type', 'digitizing' if self.rad_digitizing.isChecked() else 'refactor')

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value('Asistente-LADM_COL/wizards/right_of_way_load_data_type') or 'digitizing'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_digitizing.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help("create_right_of_way")
