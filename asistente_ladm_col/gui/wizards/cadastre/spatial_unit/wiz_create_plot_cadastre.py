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

from qgis.PyQt.QtCore import (QCoreApplication,
                              QSettings)
from qgis.PyQt.QtWidgets import (QWizard,
                                 QMessageBox)
from qgis.core import (QgsApplication,
                       QgsMapLayerProxyModel,
                       QgsWkbTypes,
                       QgsVectorLayerUtils,
                       QgsGeometry,
                       Qgis)
from qgis.gui import QgsExpressionSelectionDialog

from .....config.general_config import (LAYER,
                                        CSS_COLOR_ERROR_LABEL,
                                        CSS_COLOR_OKAY_LABEL,
                                        PLUGIN_NAME)
from .....config.help_strings import HelpStrings
from .....config.table_mapping_config import (PLOT_TABLE,
                                              PLOT_REGISTRY_AREA_FIELD,
                                              PLOT_CALCULATED_AREA_FIELD,
                                              BOUNDARY_TABLE)
from .....utils import get_ui_class
from .....utils.qt_utils import (enable_next_wizard,
                                 disable_next_wizard)
from .....utils.select_map_tool import SelectMapTool

WIZARD_UI = get_ui_class('wizards/cadastre/spatial_unit/wiz_create_plot_cadastre.ui')


class CreatePlotCadastreWizard(QWizard, WIZARD_UI):
    WIZARD_NAME = "CreatePlotCadastreWizard"
    WIZARD_TOOL_NAME = QCoreApplication.translate(WIZARD_NAME, "Create plot")
    EDITING_LAYER_NAME = ""

    def __init__(self, iface, db, qgis_utils, plugin):
        QWizard.__init__(self)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()

        self.plugin = plugin
        self.plugin.is_wizard_open = True

        self.canvas = self.iface.mapCanvas()
        self.maptool = self.canvas.mapTool()
        self.select_maptool = None

        self.EDITING_LAYER_NAME = PLOT_TABLE
        self._layers = {
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            BOUNDARY_TABLE: {'name': BOUNDARY_TABLE, 'geometry': None, LAYER: None}
        }

        self.restore_settings()
        self.rad_plot_from_boundaries.toggled.connect(self.adjust_page_1_controls)
        self.adjust_page_1_controls()

        self.button(QWizard.NextButton).clicked.connect(self.adjust_page_2_controls)
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)
        self.rejected.connect(self.close_wizard)
        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.PolygonLayer)

    def adjust_page_1_controls(self):
        self.cbo_mapping.clear()
        self.cbo_mapping.addItem("")
        self.cbo_mapping.addItems(self.qgis_utils.get_field_mappings_file_names(self.EDITING_LAYER_NAME))

        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            self.lbl_field_mapping.setEnabled(True)
            self.cbo_mapping.setEnabled(True)
            disable_next_wizard(self)
            self.wizardPage1.setFinalPage(True)
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(self.EDITING_LAYER_NAME, True))
            finish_button_text = QCoreApplication.translate(self.WIZARD_NAME, "Import")
            self.wizardPage1.setButtonText(QWizard.FinishButton, finish_button_text)
        elif self.rad_plot_from_boundaries.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            enable_next_wizard(self)
            self.wizardPage1.setFinalPage(False)
            finish_button_text = QCoreApplication.translate(self.WIZARD_NAME, "Finish")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_CREATE_PLOT_CADASTRE_PAGE_1_OPTION_BOUNDARIES)

        self.wizardPage1.setButtonText(QWizard.FinishButton, finish_button_text)

    def adjust_page_2_controls(self):
        self.button(self.FinishButton).setDisabled(True)
        self.txt_help_page_2.setHtml(self.help_strings.WIZ_CREATE_PLOT_CADASTRE_PAGE_2)
        self.disconnect_signals()

        # Load layers
        result = self.prepare_feature_creation_layers()
        if result is None:
            self.close_wizard(show_message=False)

        # Check if a previous features are selected
        self.check_selected_features()
        self.btn_map.clicked.connect(partial(self.select_features_on_map, self._layers[BOUNDARY_TABLE][LAYER]))
        self.btn_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[BOUNDARY_TABLE][LAYER]))
        self.btn_select_all.clicked.connect(partial(self.select_all_features, self._layers[BOUNDARY_TABLE][LAYER]))

    def disconnect_signals(self):
        # GUI Wizard
        signals = [self.btn_map.clicked,
                   self.btn_expression.clicked,
                   self.btn_select_all.clicked]

        for signal in signals:
            try:
                signal.disconnect()
            except:
                pass

        # QGIS APP
        try:
            self.canvas.mapToolSet.disconnect(self.map_tool_changed)
        except:
            pass

        for layer_name in self._layers:
            try:
                self._layers[layer_name][LAYER].willBeDeleted.disconnect(self.layer_removed)
            except:
                pass

    def map_tool_changed(self, new_tool, old_tool):
        self.canvas.mapToolSet.disconnect(self.map_tool_changed)
        reply = QMessageBox.question(self,
                                     QCoreApplication.translate(self.WIZARD_NAME, "Stop plot creation?"),
                                     QCoreApplication.translate(self.WIZARD_NAME,"The map tool is about to change. Do you want to stop creating plot?"),
                                     QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            message = QCoreApplication.translate(self.WIZARD_NAME,
                                                 "'{}' tool has been closed because the map tool change.").format(self.WIZARD_TOOL_NAME)
            self.close_wizard(message)
        else:
            # Continue creating the Parcel
            self.canvas.setMapTool(old_tool)
            self.canvas.mapToolSet.connect(self.map_tool_changed)

    def select_features_on_map(self, layer):
        self.iface.setActiveLayer(layer)
        self.setVisible(False)  # Make wizard disappear

        # Enable Select Map Tool
        self.select_maptool = SelectMapTool(self.canvas, layer, multi=True)

        self.canvas.setMapTool(self.select_maptool)
        # Connect signal that check if map tool change
        # This is necessary after select the maptool
        self.canvas.mapToolSet.connect(self.map_tool_changed)

        # Connect signal that check a feature was selected
        self.select_maptool.features_selected_signal.connect(self.features_selected)

    def features_selected(self):
        self.setVisible(True)  # Make wizard appear
        self.check_selected_features()

        # Disconnect signal that check if map tool change
        # This is necessary before changing the tool to the user's previous selection
        self.canvas.mapToolSet.disconnect(self.map_tool_changed)
        self.canvas.setMapTool(self.maptool)

        self.log.logMessage("Select maptool SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        self.select_maptool.features_selected_signal.disconnect(self.features_selected)

    def select_all_features(self, layer):
        layer.selectAll()
        self.check_selected_features()

    def select_features_by_expression(self, layer):
        self.iface.setActiveLayer(layer)
        dlg_expression_selection = QgsExpressionSelectionDialog(layer)
        layer.selectionChanged.connect(self.check_selected_features)
        dlg_expression_selection.exec()
        layer.selectionChanged.disconnect(self.check_selected_features)

    def check_selected_features(self):
        self.lb_info.setText(QCoreApplication.translate(self.WIZARD_NAME, "<b>Boundary(ies)</b>: {count} Feature(s) Selected").format(count=self._layers[BOUNDARY_TABLE][LAYER].selectedFeatureCount()))
        self.lb_info.setStyleSheet(CSS_COLOR_OKAY_LABEL)  # Default color

        _color = CSS_COLOR_OKAY_LABEL
        has_selected_boundaries = self._layers[BOUNDARY_TABLE][LAYER].selectedFeatureCount() > 0
        if not has_selected_boundaries:
            _color = CSS_COLOR_ERROR_LABEL
        self.lb_info.setStyleSheet(_color)

        self.button(self.FinishButton).setEnabled(has_selected_boundaries)

    def finished_dialog(self):
        self.save_settings()

        if self.rad_refactor.isChecked():
            if self.mMapLayerComboBox.currentLayer() is not None:
                field_mapping = self.cbo_mapping.currentText()
                res_etl_model = self.qgis_utils.show_etl_model(self._db,
                                                               self.mMapLayerComboBox.currentLayer(),
                                                               self.EDITING_LAYER_NAME,
                                                               QgsWkbTypes.PolygonGeometry,
                                                               field_mapping)

                if res_etl_model:
                    if field_mapping:
                        self.qgis_utils.delete_old_field_mapping(field_mapping)

                    self.qgis_utils.save_field_mapping(self.EDITING_LAYER_NAME)
            else:
                self.qgis_utils.message_emitted.emit(
                    QCoreApplication.translate(self.WIZARD_NAME,
                                               "Select a source layer to set the field mapping to '{}'.").format(
                        self.EDITING_LAYER_NAME),
                    Qgis.Warning)

        elif self.rad_plot_from_boundaries.isChecked():
            self.prepare_feature_creation()

    def prepare_feature_creation(self):
        result = self.prepare_feature_creation_layers()
        if result:
            self.edit_feature()
        else:
            self.close_wizard(show_message=False)

    def prepare_feature_creation_layers(self):
        is_loaded = self.required_layers_are_available()
        if not is_loaded:
            return False

        # Add signal to check if a layer was removed
        self.validate_remove_layers()

        # All layers were successfully loaded
        return True

    def required_layers_are_available(self):
        # Load layers
        self.qgis_utils.get_layers(self._db, self._layers, load=True)
        if not self._layers:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate(self.WIZARD_NAME,
                                           "'{}' tool has been closed because there was a problem loading the requeries layers.").format(
                    self.WIZARD_TOOL_NAME),
                Qgis.Warning)
            return False

        # Check if layers any layer is in editing mode
        layers_name = list()
        for layer in self._layers:
            if self._layers[layer][LAYER].isEditable():
                layers_name.append(self._db.get_ladm_layer_name(self._layers[layer][LAYER]))

        if layers_name:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate(self.WIZARD_NAME,
                                           "Wizard cannot be opened until the following layers are not in edit mode '{}'.").format(
                    '; '.join([layer_name for layer_name in layers_name])),
                Qgis.Warning)
            return False

        return True

    def validate_remove_layers(self):
        for layer_name in self._layers:
            if self._layers[layer_name][LAYER]:
                # Layer was found, listen to its removal so that we can update the variable properly
                try:
                    self._layers[layer_name][LAYER].willBeDeleted.disconnect(self.layer_removed)
                except:
                    pass
                self._layers[layer_name][LAYER].willBeDeleted.connect(self.layer_removed)

    def layer_removed(self):
        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because you just removed a required layer.").format(self.WIZARD_TOOL_NAME)
        self.close_wizard(message)

    def close_wizard(self, message=None, show_message=True):
        if message is None:
            message = QCoreApplication.translate(self.WIZARD_NAME, "'{}' tool has been closed.").format(self.WIZARD_TOOL_NAME)
        if show_message:
            self.qgis_utils.message_emitted.emit(message, Qgis.Info)
        self.init_map_tool()
        self.disconnect_signals()
        self.plugin.is_wizard_open = False
        self.close()

    def init_map_tool(self):
        try:
            self.canvas.mapToolSet.disconnect(self.map_tool_changed)
        except:
            pass
        self.canvas.setMapTool(self.maptool)

    def edit_feature(self):
        if self._layers[BOUNDARY_TABLE][LAYER].selectedFeatureCount() > 0:
            # Open Form
            self.iface.layerTreeView().setCurrentLayer(self._layers[self.EDITING_LAYER_NAME][LAYER])
            self.qgis_utils.active_snapping_all_layers()
            self.create_plots_from_boundaries()
        else:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate(self.WIZARD_NAME,
                                           "First select boundaries!"),
                Qgis.Warning)

    def create_plots_from_boundaries(self):
        selected_boundaries = self._layers[BOUNDARY_TABLE][LAYER].selectedFeatures()

        boundary_geometries = [f.geometry() for f in selected_boundaries]
        collection = QgsGeometry().polygonize(boundary_geometries)
        features = list()
        for polygon in collection.asGeometryCollection():
            feature = QgsVectorLayerUtils().createFeature(self._layers[self.EDITING_LAYER_NAME][LAYER], polygon)
            features.append(feature)

        if features:
            if not self._layers[self.EDITING_LAYER_NAME][LAYER].isEditable():
                self._layers[self.EDITING_LAYER_NAME][LAYER].startEditing()

            self._layers[self.EDITING_LAYER_NAME][LAYER].addFeatures(features)
            self.iface.mapCanvas().refresh()

            message = QCoreApplication.translate("QGISUtils", "{} new plot(s) has(have) been created! To finish the creation of the plots, open its attribute table and fill in the mandatory fields.").format(len(features))
            button_text = QCoreApplication.translate("QGISUtils", "Open table of attributes")
            level = Qgis.Info
            layer = self._layers[self.EDITING_LAYER_NAME][LAYER]
            filter = '"{}" is Null and "{}" is Null'.format(PLOT_REGISTRY_AREA_FIELD, PLOT_CALCULATED_AREA_FIELD)
            self.qgis_utils.message_with_open_table_attributes_button_emitted.emit(message, button_text, level, layer, filter)
            self.close_wizard(show_message=False)
        else:
            message = QCoreApplication.translate("QGISUtils", "No plot could be created. Make sure selected boundaries are closed!")
            self.close_wizard(message)

    def form_rejected(self):
        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because you just closed the form.").format(self.WIZARD_TOOL_NAME)
        self.close_wizard(message)

    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/wizards/plot_load_data_type', 'from_boundaries' if self.rad_plot_from_boundaries.isChecked() else 'refactor')

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value('Asistente-LADM_COL/wizards/plot_load_data_type') or 'from_boundaries'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_plot_from_boundaries.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help("create_plot")
