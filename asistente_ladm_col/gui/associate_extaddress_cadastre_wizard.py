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
from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication,
                              QSettings)
from qgis.PyQt.QtWidgets import (QWizard,
                                 QSizePolicy,
                                 QGridLayout)
from qgis.core import (QgsEditFormConfig,
                       Qgis,
                       QgsMapLayerProxyModel,
                       QgsWkbTypes,
                       QgsApplication,
                       QgsVectorLayerUtils)
from qgis.gui import (QgsMessageBar,
                      QgsExpressionSelectionDialog)

from ..config.general_config import (PLUGIN_NAME,
                                     TranslatableConfigStrings)
from ..config.help_strings import HelpStrings
from ..config.table_mapping_config import (EXTADDRESS_TABLE,
                                           EXTADDRESS_BUILDING_FIELD,
                                           EXTADDRESS_BUILDING_UNIT_FIELD,
                                           EXTADDRESS_PLOT_FIELD,
                                           BUILDING_TABLE,
                                           BUILDING_UNIT_TABLE,
                                           ID_FIELD,
                                           OID_EXTADDRESS_ID_FIELD,
                                           OID_TABLE,
                                           PLOT_TABLE)
from ..utils import get_ui_class
from ..utils.qt_utils import (enable_next_wizard,
                              disable_next_wizard)
from ..utils.select_map_tool import SelectMapTool

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
        self.maptool = self.canvas.mapTool()
        self.select_maptool = None
        self.help_strings = HelpStrings()
        self.translatable_config_strings = TranslatableConfigStrings()
        self._extaddress_layer = None
        self._plot_layer = None
        self._building_layer = None
        self._building_unit_layer = None
        self._current_layer = None

        self._feature_tid = None
        self._extaddress_tid = None

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
            FinishButton_text = QCoreApplication.translate("AssociateExtAddressWizard", "Import")
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(EXTADDRESS_TABLE, True))
            self.wizardPage1.setFinalPage(True)
            self.wizardPage1.setButtonText(QWizard.FinishButton,
                                           QCoreApplication.translate("AssociateExtAddressWizard",
                                                                      FinishButton_text))

        elif self.rad_to_plot.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            self.wizardPage1.setFinalPage(False)
            enable_next_wizard(self)
            FinishButton_text = QCoreApplication.translate("AssociateExtAddressWizard", "Associate Plot ExtAddress")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_1_OPTION_1)

        elif self.rad_to_building.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            self.wizardPage1.setFinalPage(False)
            enable_next_wizard(self)
            FinishButton_text = QCoreApplication.translate("AssociateExtAddressWizard", "Associate Building ExtAddress")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_1_OPTION_2)

        else:  # self.rad_to_building_unit.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            self.wizardPage1.setFinalPage(False)
            enable_next_wizard(self)
            FinishButton_text = QCoreApplication.translate("AssociateExtAddressWizard",
                                                           "Associate Building Unit ExtAddress")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_1_OPTION_3)

        self.wizardPage2.setButtonText(QWizard.FinishButton,
                                       QCoreApplication.translate('AssociateExtAddressWizard',
                                                                  FinishButton_text))

    def prepare_selection(self):
        self.button(self.FinishButton).setDisabled(True)
        if self.rad_to_plot.isChecked():
            self.btn_select.setText(QCoreApplication.translate("AssociateExtAddressWizard",
                                                               "Select Plot"))
            self.txt_help_page_2.setHtml(self.help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_2_OPTION_1)
            # Load layers
            res_layers = self.qgis_utils.get_layers(self._db, {
                EXTADDRESS_TABLE: {'name': EXTADDRESS_TABLE, 'geometry': QgsWkbTypes.PointGeometry},
                OID_TABLE: {'name': OID_TABLE, 'geometry': None},
                PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry}
            }, load=True)

            self._extaddress_layer = res_layers[EXTADDRESS_TABLE]
            self._oid_layer = res_layers[OID_TABLE]
            self._plot_layer = res_layers[PLOT_TABLE]
            self._current_layer = self._plot_layer

        elif self.rad_to_building.isChecked():
            self.btn_select.setText(QCoreApplication.translate("AssociateExtAddressWizard",
                                                               "Select Building"))
            self.txt_help_page_2.setHtml(self.help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_2_OPTION_2)

            # Load layers
            res_layers = self.qgis_utils.get_layers(self._db, {
                EXTADDRESS_TABLE: {'name': EXTADDRESS_TABLE, 'geometry': QgsWkbTypes.PointGeometry},
                OID_TABLE: {'name': OID_TABLE, 'geometry': None},
                BUILDING_TABLE: {'name': BUILDING_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry}
            }, load=True)

            self._extaddress_layer = res_layers[EXTADDRESS_TABLE]
            self._building_layer = res_layers[BUILDING_TABLE]
            self._oid_layer = res_layers[OID_TABLE]
            self._current_layer = self._building_layer

        else:  # self.rad_to_building_unit.isChecked():
            self.btn_select.setText(QCoreApplication.translate("AssociateExtAddressWizard",
                                                               "Select Building Unit"))
            self.txt_help_page_2.setHtml(self.help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_2_OPTION_3)

            # Load layers
            res_layers = self.qgis_utils.get_layers(self._db, {
                EXTADDRESS_TABLE: {'name': EXTADDRESS_TABLE, 'geometry': QgsWkbTypes.PointGeometry},
                OID_TABLE: {'name': OID_TABLE, 'geometry': None},
                BUILDING_UNIT_TABLE: {'name': BUILDING_UNIT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry}
            }, load=True)

            self._extaddress_layer = res_layers[EXTADDRESS_TABLE]
            self._building_unit_layer = res_layers[BUILDING_UNIT_TABLE]
            self._oid_layer = res_layers[OID_TABLE]
            self._current_layer = self._building_unit_layer

        self.iface.setActiveLayer(self._current_layer)
        self.check_selected_features()
        self.btn_select.clicked.connect(self.select_feature)
        self.btn_select_by_expression.clicked.connect(self.select_feature_by_expression)

    def check_selected_features(self):
        self.bar.clearWidgets()

        if self._current_layer.selectedFeatureCount() == 1:
            self.lbl_selected.setText(QCoreApplication.translate("AssociateExtAddressWizard",
                                                                 "1 Feature Selected"))
            self.button(self.FinishButton).setDisabled(False)
            self._feature_tid = self._current_layer.selectedFeatures()[0][ID_FIELD]
            self.canvas.zoomToSelected(self._current_layer)
        elif self._current_layer.selectedFeatureCount() > 1:
            self.show_message(QCoreApplication.translate("AssociateExtAddressWizard",
                                                         "Please select just one feature"), Qgis.Warning)
            self.lbl_selected.setText(QCoreApplication.translate("AssociateExtAddressWizard",
                                                                 "{} Feature(s) Selected".format(
                                                                     self._current_layer.selectedFeatureCount())))
            self.button(self.FinishButton).setDisabled(True)
        else:
            self.lbl_selected.setText(QCoreApplication.translate("AssociateExtAddressWizard",
                                                                 "0 Features Selected"))
            self.button(self.FinishButton).setDisabled(True)

    def select_feature_by_expression(self):
        Dlg_expression_selection = QgsExpressionSelectionDialog(self._current_layer)
        self._current_layer.selectionChanged.connect(self.check_selected_features)
        Dlg_expression_selection.exec()
        self._current_layer.selectionChanged.disconnect(self.check_selected_features)

    def select_feature(self):
        self.setVisible(False)  # Make wizard disappear

        # Create maptool
        self.select_maptool = SelectMapTool(self.canvas, self._current_layer, multi=False)
        self.canvas.setMapTool(self.select_maptool)
        self.select_maptool.features_selected_signal.connect(self.feature_selected)

        # TODO: Take into account that a user can select another tool

    def feature_selected(self):
        self.setVisible(True)  # Make wizard appear
        feature = self._current_layer.selectedFeatures()[0]  # Get selected feature

        if feature:
            self.lbl_selected.setText(QCoreApplication.translate("AssociateExtAddressWizard",
                                                                 "1 Feature Selected"))
            self._current_layer.selectByIds([feature.id()])

        self.canvas.setMapTool(self.maptool)
        self.check_selected_features()

        self.select_maptool.features_selected_signal.disconnect(self.feature_selected)
        self.log.logMessage("Spatial Unit's featureIdentified SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)

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
                                                                               "Select a source layer to set the field mapping to '{}'.").format(
                                                        EXTADDRESS_TABLE),
                                                    Qgis.Warning)

        else:
            self.prepare_extaddress_creation()

    def prepare_extaddress_creation(self):
        # Don't suppress (i.e., show) feature form
        form_config = self._extaddress_layer.editFormConfig()
        form_config.setSuppress(QgsEditFormConfig.SuppressOff)
        self._extaddress_layer.setEditFormConfig(form_config)

        # Suppress (i.e., hide) feature form
        form_config = self._oid_layer.editFormConfig()
        form_config.setSuppress(QgsEditFormConfig.SuppressOn)
        self._oid_layer.setEditFormConfig(form_config)

        self.edit_extaddress()

    def edit_extaddress(self):
        if self._current_layer.selectedFeatureCount() == 1:
            # Open Form
            self.iface.layerTreeView().setCurrentLayer(self._extaddress_layer)
            self._extaddress_layer.startEditing()
            self.iface.actionAddFeature().trigger()

            # Create connections to react when a feature is added to buffer and
            # when it gets stored into the DB
            self._extaddress_layer.featureAdded.connect(self.call_extaddress_commit)

        else:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate("AssociateExtAddressWizard",
                                                                           "Please select a feature"),
                                                Qgis.Warning)

    def call_extaddress_commit(self, fid):
        plot_field_idx = self._extaddress_layer.getFeature(fid).fieldNameIndex(EXTADDRESS_PLOT_FIELD)
        building_field_idx = self._extaddress_layer.getFeature(fid).fieldNameIndex(EXTADDRESS_BUILDING_FIELD)
        building_unit_field_idx = self._extaddress_layer.getFeature(fid).fieldNameIndex(EXTADDRESS_BUILDING_UNIT_FIELD)
        self._extaddress_tid = self._extaddress_layer.getFeature(fid)[ID_FIELD]

        if self._current_layer.name() == PLOT_TABLE:
            self._extaddress_layer.changeAttributeValue(fid, plot_field_idx, self._feature_tid)
        elif self._current_layer.name() == BUILDING_TABLE:
            self._extaddress_layer.changeAttributeValue(fid, building_field_idx, self._feature_tid)
        else:  # self._current_layer.name() == BUILDING_UNIT_TABLE:
            self._extaddress_layer.changeAttributeValue(fid, building_unit_field_idx, self._feature_tid)

        self._extaddress_layer.featureAdded.disconnect(self.call_extaddress_commit)
        self.log.logMessage("Extaddress's featureAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        res = self._extaddress_layer.commitChanges()
        self._current_layer.removeSelection()
        self.add_oid_feature()

    def add_oid_feature(self):
        # Add OID record
        self._oid_layer.startEditing()
        feature = QgsVectorLayerUtils().createFeature(self._oid_layer)
        feature.setAttribute(OID_EXTADDRESS_ID_FIELD, self._extaddress_tid)
        self._oid_layer.addFeature(feature)
        self._oid_layer.commitChanges()

    def show_message(self, message, level):
        self.bar.pushMessage(message, level, 0)

    def save_settings(self):
        settings = QSettings()

        load_data_type = 'refactor'
        if self.rad_to_plot.isChecked():
            load_data_type = 'to_plot'
        elif self.rad_to_building.isChecked():
            load_data_type = 'to_building'
        else:  # self.rad_to_building_unit.isChecked():
            load_data_type = 'to_building_unit'

        settings.setValue('Asistente-LADM_COL/wizards/ext_address_load_data_type', load_data_type)

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value('Asistente-LADM_COL/wizards/ext_address_load_data_type', 'to_plot')
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        elif load_data_type == 'to_plot':
            self.rad_to_plot.setChecked(True)
        elif load_data_type == 'to_building':
            self.rad_to_building.setChecked(True)
        else:  # load_data_type == 'to_building_unit':
            self.rad_to_building_unit.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help("associate_ext_address")
