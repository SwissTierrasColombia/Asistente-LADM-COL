# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 15/01/19
        git sha              : :%H$
        copyright            : (C) 2019 by Sergio Ramírez (Incige SAS)
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
from qgis.core import (QgsProject, QgsVectorLayer, QgsEditFormConfig,
                       QgsSnappingConfig, QgsTolerance, QgsFeature, Qgis,
                       QgsMapLayerProxyModel, QgsWkbTypes, QgsApplication,
                       QgsProcessingException, QgsProcessingFeedback,
                       QgsVectorLayerUtils)
from qgis.gui import QgsMapToolIdentifyFeature, QgsMessageBar

from qgis.PyQt.QtCore import Qt, QPoint, QCoreApplication, QSettings
from qgis.PyQt.QtGui import QCursor
from qgis.PyQt.QtWidgets import QAction, QWizard, QSizePolicy, QGridLayout

import processing
from ..utils import get_ui_class
from ..utils.qt_utils import (enable_next_wizard,
                              disable_next_wizard)
from ..config.table_mapping_config import (EXTADDRESS_TABLE,
                                           BUILDING_TABLE,
                                           BUILDING_UNIT_TABLE,
                                           PLOT_TABLE)
from ..config.general_config import (DEFAULT_EPSG,
                                     PLUGIN_NAME,
                                     TranslatableConfigStrings)
from ..config.help_strings import HelpStrings
from .right_of_way import RightOfWay

WIZARD_UI = get_ui_class('wiz_associate_extaddress_cadastre.ui')

class AssociateExtAddressWizard(QWizard, WIZARD_UI):

    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._db = db
        self.qgis_utils = qgis_utils
        self.canvas = self.iface.mapCanvas()
        self.maptool = self.iface.mapCanvas().mapTool()
        self.maptool_id = None
        self.help_strings = HelpStrings()
        self.translatable_config_strings = TranslatableConfigStrings()
        self._ext_address_layer = None
        self._plot_layer = None

        self.restore_settings()

        self.rad_to_plot.toggled.connect(self.adjust_page_1_controls)
        self.rad_to_building.toggled.connect(self.adjust_page_1_controls)
        self.rad_to_building_unit.toggled.connect(self.adjust_page_1_controls)
        self.adjust_page_1_controls()
        self.button(QWizard.NextButton).clicked.connect(self.prepare_selection)
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)

        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.PolygonLayer)

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.setLayout(QGridLayout())
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

    def adjust_page_1_controls(self):
        self.cbo_mapping.clear()
        self.cbo_mapping.addItem("")
        self.cbo_mapping.addItems(self.qgis_utils.get_field_mappings_file_names(EXTADDRESS_TABLE))

        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            self.lbl_field_mapping.setEnabled(True)
            self.cbo_mapping.setEnabled(True)
            disable_next_wizard(self)
            finish_button_text = QCoreApplication.translate("AssociateExtAddressWizard", "Import")
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(EXTADDRESS_TABLE, True))
            self.wizardPage1.setFinalPage(True)
            self.wizardPage1.setButtonText(QWizard.FinishButton,
                                           QCoreApplication.translate("AssociateExtAddressWizard",
                                           finish_button_text))

        elif self.rad_to_plot.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            self.wizardPage1.setFinalPage(False)
            enable_next_wizard(self)
            finish_button_text = QCoreApplication.translate("AssociateExtAddressWizard", "Associate Plot ExtAddress")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_1_OPTION_POINTS)

        elif self.rad_to_building.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            self.wizardPage1.setFinalPage(False)
            enable_next_wizard(self)
            finish_button_text = QCoreApplication.translate("AssociateExtAddressWizard", "Associate Building ExtAddress")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_1_OPTION2_POINTS)

        elif self.rad_to_building_unit.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            self.wizardPage1.setFinalPage(False)
            enable_next_wizard(self)
            finish_button_text = QCoreApplication.translate("AssociateExtAddressWizard", "Associate Building Unit ExtAddress")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_1_OPTION3_POINTS)

        self.wizardPage2.setButtonText(QWizard.FinishButton,
                                       QCoreApplication.translate('AssociateExtAddressWizard',
                                       finish_button_text))

    def prepare_selection(self):
        if self.rad_to_plot.isChecked():
            # Load layers
            res_layers = self.qgis_utils.get_layers(self._db, {
            EXTADDRESS_TABLE: {'name': EXTADDRESS_TABLE, 'geometry': QgsWkbTypes.PointGeometry},
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry}
            }, load=True)

            self._ext_address_layer = res_layers[EXTADDRESS_TABLE]
            self._plot_layer = res_layers[PLOT_TABLE]

            self.check_selected_features(self._plot_layer)
            self.btn_select.setText(QCoreApplication.translate("AssociateExtAddressWizard",
                                    "Select Plot"))
            self.btn_select.clicked.connect(self.select_plot)
        elif self.rad_to_building.isChecked():
            self.btn_select.setText(QCoreApplication.translate("AssociateExtAddressWizard",
                                    "Select Building"))
            self.btn_select.clicked.connect(self.select_building)
        elif self.rad_to_building_unit.isChecked():
            self.btn_select.setText(QCoreApplication.translate("AssociateExtAddressWizard",
                                    "Select Building Unit"))
            self.btn_select.clicked.connect(self.select_building_unit)

    def check_selected_features(self, layer):

        if layer.selectedFeatureCount() == 1:
            self.lbl_selected.setText(QCoreApplication.translate("AssociateExtAddressWizard",
                                          str(layer.selectedFeatureCount()) + " Feature(s) Selected"))
            self.button(self.FinishButton).setDisabled(False)
        elif layer.selectedFeatureCount() > 1:
            self.show_message(QCoreApplication.translate("AssociateExtAddressWizard",
                                          "Please select just one feature"), Qgis.Warning)
            self.lbl_selected.setText(QCoreApplication.translate("AssociateExtAddressWizard",
                                          str(layer.selectedFeatureCount()) + " Feature(s) Selected"))
            self.button(self.FinishButton).setDisabled(True)
        else:
            self.button(self.FinishButton).setDisabled(True)


    def finished_dialog(self):
        self.save_settings()

        if self.rad_refactor.isChecked():
            if self.mMapLayerComboBox.currentLayer() is not None:
                field_mapping = self.cbo_mapping.currentText()
                res_etl_model = self.qgis_utils.show_etl_model(self._db,
                                               self.mMapLayerComboBox.currentLayer(),
                                               EXTADDRESS_TABLE,
                                               field_mapping=field_mapping)

                if res_etl_model:
                    if field_mapping:
                        self.qgis_utils.delete_old_field_mapping(field_mapping)

                    self.qgis_utils.save_field_mapping(EXTADDRESS_TABLE)

            else:
                self.iface.messageBar().pushMessage('Asistente LADM_COL',
                    QCoreApplication.translate("AssociateExtAddressWizard",
                                               "Select a source layer to set the field mapping to '{}'.").format(EXTADDRESS_TABLE),
                    Qgis.Warning)

        elif self.rad_to_plot.isChecked():
            self.prepare_extdirection_plot_creation()

        elif self.rad_to_building.isChecked():
            self.prepare_extdirection_building_creation()

        elif self.rad_to_building_unit.isChecked():
            self.prepare_extdirection_building_unit_creation()


    def select_plot(self):

        self.setVisible(False)
        self.maptool_id = QgsMapToolIdentifyFeature(self.canvas)
        self.maptool_id.setLayer(self._plot_layer)
        cursor = QCursor()
        cursor.setShape(Qt.CrossCursor)
        self.maptool_id.setCursor(cursor)
        self.iface.mapCanvas().setMapTool(self.maptool_id)
        self.maptool_id.featureIdentified.connect(self.get_feature_id)


    def get_feature_id(self, feature):
        print("El id del terreno es " + str(feature.id()))
        self.setVisible(True)
        if feature:
            self.lbl_selected.setText(QCoreApplication.translate("AssociateExtAddressWizard",
                                    "1 Plot Selected"))
            self._plot_layer.selectByIds([feature.id()])

        self.iface.mapCanvas().setMapTool(self.maptool)

        self.check_selected_features(self._plot_layer)

        self.maptool_id.featureIdentified.disconnect(self.get_feature_id)
        self.log.logMessage("Parcel's featureIdentified SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)

    def select_building(self):
        print("Aun no estoy listo para asociar construcciones")
        self.maptool_id.featureIdentified.disconnect(self.get_feature_id)
        self.log.logMessage("Parcel's featureIdentified SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        pass

    def select_building_unit(self):
        print("Aun no estoy listo para asociar unidades de construccion")
        self.maptool_id.featureIdentified.disconnect(self.get_feature_id)
        self.log.logMessage("Parcel's featureIdentified SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        pass

    def activate_wizard(self):
        self.setVisible(True)
        self.iface.mapCanvas().setMapTool(self.maptool)

    def prepare_extdirection_plot_creation(self):
        # Load layers
        res_layers = self.qgis_utils.get_layers(self._db, {
            EXTADDRESS_TABLE: {'name': EXTADDRESS_TABLE, 'geometry': QgsWkbTypes.PointGeometry},
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry}
            }, load=True)

        self._ext_address_layer = res_layers[EXTADDRESS_TABLE]
        self._plot_layer = res_layers[PLOT_TABLE]


    def prepare_extdirection_building_creation(self):
        # Load layers
        res_layers = self.qgis_utils.get_layers(self._db, {
            EXTADDRESS_TABLE: {'name': EXTADDRESS_TABLE, 'geometry': QgsWkbTypes.PointGeometry},
            BUILDING_TABLE: {'name': BUILDING_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry}
            }, load=True)

    def prepare_extdirection_building_unit_creation(self):
        # Load layers
        res_layers = self.qgis_utils.get_layers(self._db, {
            EXTADDRESS_TABLE: {'name': EXTADDRESS_TABLE, 'geometry': QgsWkbTypes.PointGeometry},
            BUILDING_UNIT_TABLE: {'name': BUILDING_UNIT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry}
            }, load=True)

    def show_message(self, message, level):
        self.bar.pushMessage(message, level, 3)

    def save_settings(self):
        settings = QSettings()

        load_data_type = 'refactor'
        if self.rad_to_plot.isChecked():
            load_data_type = 'to_plot'
        elif self.rad_to_building.isChecked():
            load_data_type = 'to_building'
        elif self.rad_to_building_unit.isChecked():
            load_data_type = 'to_building_unit'

        settings.setValue('Asistente-LADM_COL/wizards/ext_address_load_data_type', load_data_type)

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value('Asistente-LADM_COL/wizards/ext_address_load_data_type') or 'to_plot'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        elif load_data_type == 'to_plot':
            self.rad_to_plot.setChecked(True)
        elif load_data_type == 'to_building':
            self.rad_to_building.setChecked(True)
        else:
            self.rad_to_building_unit.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help("associate_ext_address")
