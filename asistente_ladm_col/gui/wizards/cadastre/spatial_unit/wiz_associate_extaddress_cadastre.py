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
from functools import partial

from qgis.PyQt.QtCore import (QCoreApplication,
                              QSettings)
from qgis.PyQt.QtWidgets import (QWizard,
                                 QMessageBox)

from qgis.core import (Qgis,
                       QgsMapLayerProxyModel,
                       QgsWkbTypes,
                       QgsApplication,
                       QgsVectorLayerUtils)
from qgis.gui import QgsExpressionSelectionDialog

from .....config.general_config import (PLUGIN_NAME,
                                        LAYER,
                                        TranslatableConfigStrings,
                                        CSS_COLOR_ERROR_LABEL,
                                        CSS_COLOR_OKAY_LABEL,
                                        CSS_COLOR_INACTIVE_LABEL)
from .....config.help_strings import HelpStrings
from .....config.table_mapping_config import (EXTADDRESS_TABLE,
                                              EXTADDRESS_BUILDING_FIELD,
                                              EXTADDRESS_BUILDING_UNIT_FIELD,
                                              EXTADDRESS_PLOT_FIELD,
                                              BUILDING_TABLE,
                                              BUILDING_UNIT_TABLE,
                                              ID_FIELD,
                                              OID_EXTADDRESS_ID_FIELD,
                                              OID_TABLE,
                                              PLOT_TABLE)
from .....utils import get_ui_class
from .....utils.qt_utils import (enable_next_wizard,
                                 disable_next_wizard)
from .....utils.select_map_tool import SelectMapTool

WIZARD_UI = get_ui_class('wizards/cadastre/spatial_unit/wiz_associate_extaddress_cadastre.ui')


class AssociateExtAddressWizard(QWizard, WIZARD_UI):
    WIZARD_NAME = "AssociateExtAddressWizard"
    WIZARD_TOOL_NAME = QCoreApplication.translate(WIZARD_NAME, "Create ExtAddress")

    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()
        self.translatable_config_strings = TranslatableConfigStrings()

        # Necessary to control featureAdded bug (crash QGIS)
        # https://gis.stackexchange.com/a/229949/120426
        self.added_features = None
        self.rollback_changes = False

        self.canvas = self.iface.mapCanvas()
        self.maptool = self.canvas.mapTool()
        self.select_maptool = None
        self._current_layer = None

        self._layers = {
            EXTADDRESS_TABLE: {'name': EXTADDRESS_TABLE, 'geometry': QgsWkbTypes.PointGeometry, LAYER: None},
            OID_TABLE: {'name': OID_TABLE, 'geometry': None, LAYER: None},
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            BUILDING_TABLE: {'name': BUILDING_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            BUILDING_UNIT_TABLE: {'name': BUILDING_UNIT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None}
        }

        self.restore_settings()
        self.rad_spatial_unit.toggled.connect(self.adjust_page_1_controls)
        self.adjust_page_1_controls()

        self.button(QWizard.NextButton).clicked.connect(self.adjust_page_2_controls)
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)
        self.rejected.connect(self.close_wizard)
        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.PolygonLayer)

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
            self.wizardPage1.setFinalPage(True)
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(EXTADDRESS_TABLE, True))
            finish_button_text = QCoreApplication.translate(self.WIZARD_NAME, "Import")
            self.wizardPage1.setButtonText(QWizard.FinishButton, finish_button_text)
        elif self.rad_spatial_unit.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            self.wizardPage1.setFinalPage(False)
            enable_next_wizard(self)
            self.wizardPage1.setFinalPage(False)
            finish_button_text = QCoreApplication.translate(self.WIZARD_NAME, "Associate address with spatial unit")
            self.txt_help_page_1.setHtml(self.help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_1)

        self.wizardPage2.setButtonText(QWizard.FinishButton, finish_button_text)

    def adjust_page_2_controls(self):
        self.button(self.FinishButton).setDisabled(True)
        self.disconnect_signals()

        # Load layers
        result = self.prepare_feature_creation_layers()
        if result is None:
            self.close_wizard(show_message=False)

        # Check if a previous features are selected
        self.check_selected_features()

        self.btn_plot_map.clicked.connect(partial(self.select_features_on_map, self._layers[PLOT_TABLE][LAYER]))
        self.btn_building_map.clicked.connect(partial(self.select_features_on_map, self._layers[BUILDING_TABLE][LAYER]))
        self.btn_building_unit_map.clicked.connect(partial(self.select_features_on_map, self._layers[BUILDING_UNIT_TABLE][LAYER]))

        self.btn_plot_expression.clicked.connect(partial(self.select_feature_by_expression, self._layers[PLOT_TABLE][LAYER]))
        self.btn_building_expression.clicked.connect(partial(self.select_feature_by_expression, self._layers[BUILDING_TABLE][LAYER]))
        self.btn_building_unit_expression.clicked.connect(partial(self.select_feature_by_expression, self._layers[BUILDING_UNIT_TABLE][LAYER]))

        self.rad_to_plot.toggled.connect(self.toggle_spatial_unit)
        self.rad_to_building.toggled.connect(self.toggle_spatial_unit)
        self.rad_to_building_unit.toggled.connect(self.toggle_spatial_unit)
        self.toggle_spatial_unit()

    def toggle_spatial_unit(self):

        self.btn_plot_map.setEnabled(False)
        self.btn_building_map.setEnabled(False)
        self.btn_building_unit_map.setEnabled(False)

        self.btn_plot_expression.setEnabled(False)
        self.btn_building_expression.setEnabled(False)
        self.btn_building_unit_expression.setEnabled(False)

        if self.rad_to_plot.isChecked():
            self.txt_help_page_2.setHtml(self.help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_2_OPTION_1)
            self._current_layer = self._layers[PLOT_TABLE][LAYER]

            self.btn_plot_map.setEnabled(True)
            self.btn_plot_expression.setEnabled(True)

        elif self.rad_to_building.isChecked():
            self.txt_help_page_2.setHtml(self.help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_2_OPTION_2)
            self._current_layer = self._layers[BUILDING_TABLE][LAYER]

            self.btn_building_map.setEnabled(True)
            self.btn_building_expression.setEnabled(True)

        elif self.rad_to_building_unit.isChecked():
            self.txt_help_page_2.setHtml(self.help_strings.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_2_OPTION_3)
            self._current_layer = self._layers[BUILDING_UNIT_TABLE][LAYER]

            self.btn_building_unit_map.setEnabled(True)
            self.btn_building_unit_expression.setEnabled(True)

        self.iface.setActiveLayer(self._current_layer)
        self.check_selected_features()

    def disconnect_signals(self):
        # GUI Wizard
        signals = [self.btn_plot_map.clicked,
                   self.btn_building_map.clicked,
                   self.btn_building_unit_map.clicked,
                   self.btn_plot_expression.clicked,
                   self.btn_building_expression.clicked,
                   self.btn_building_unit_expression.clicked]

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

        try:
            self._layers[EXTADDRESS_TABLE][LAYER].featureAdded.disconnect(self.exec_form)
        except:
            pass

        try:
            self._layers[EXTADDRESS_TABLE][LAYER].editCommandEnded.disconnect(self.confirm_commit)
        except:
            pass

        try:
            self._layers[EXTADDRESS_TABLE][LAYER].committedFeaturesAdded.disconnect(self.finish_feature_creation)
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
                                     QCoreApplication.translate(self.WIZARD_NAME, "Stop address creation?"),
                                     QCoreApplication.translate(self.WIZARD_NAME, "The map tool is about to change. Do you want to stop creating addresses?"),
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Disconnect signal that check if map tool change
            message = QCoreApplication.translate(self.WIZARD_NAME,
                                                 "'{}' tool has been closed because the map tool change.").format(self.WIZARD_TOOL_NAME)
            self.close_wizard(message)
        else:
            # Continue creating the ExtAddress
            self.canvas.setMapTool(old_tool)
            self.canvas.mapToolSet.connect(self.map_tool_changed)

    def select_features_on_map(self, layer):
        self._current_layer = layer
        self.iface.setActiveLayer(self._current_layer)
        self.setVisible(False)  # Make wizard disappear

        # Enable Select Map Tool
        self.select_maptool = SelectMapTool(self.canvas, self._current_layer, multi=False)

        self.canvas.setMapTool(self.select_maptool)
        # Connect signal that check if map tool change
        # This is necessary after select the maptool
        self.canvas.mapToolSet.connect(self.map_tool_changed)

        # Connect signal that checks a feature was selected
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

    def select_feature_by_expression(self, layer):
        self._current_layer = layer
        self.iface.setActiveLayer(self._current_layer)
        dlg_expression_selection = QgsExpressionSelectionDialog(self._current_layer)
        self._current_layer.selectionChanged.connect(self.check_selected_features)
        dlg_expression_selection.exec()
        self._current_layer.selectionChanged.disconnect(self.check_selected_features)

    def check_selected_features(self):

        self.rad_to_plot.setText(QCoreApplication.translate(self.WIZARD_NAME, "Plot(s): {count} Feature(s) Selected").format(count=self._layers[PLOT_TABLE][LAYER].selectedFeatureCount()))
        self.rad_to_building.setText(QCoreApplication.translate(self.WIZARD_NAME, "Building(s): {count} Feature(s) Selected").format(count=self._layers[BUILDING_TABLE][LAYER].selectedFeatureCount()))
        self.rad_to_building_unit.setText(QCoreApplication.translate(self.WIZARD_NAME, "Building unit(s): {count} Feature(s) Selected").format(count=self._layers[BUILDING_UNIT_TABLE][LAYER].selectedFeatureCount()))

        if self._current_layer is None:
            if self._db.get_ladm_layer_name(self.iface.activeLayer()) == PLOT_TABLE:
                self.rad_to_plot.setChecked(True)
                self._current_layer = self._layers[PLOT_TABLE][LAYER]
            elif self._db.get_ladm_layer_name(self.iface.activeLayer()) == BUILDING_TABLE:
                self.rad_to_building.setChecked(True)
                self._current_layer = self._layers[BUILDING_TABLE][LAYER]
            elif self._db.get_ladm_layer_name(self.iface.activeLayer()) == BUILDING_UNIT_TABLE:
                self.rad_to_building_unit.setChecked(True)
                self._current_layer = self._layers[BUILDING_UNIT_TABLE][LAYER]
            else:
                # Select layer that have least one feature selected
                # as current layer when current layer is not defined
                if self._layers[PLOT_TABLE][LAYER].selectedFeatureCount():
                    self.rad_to_plot.setChecked(True)
                    self._current_layer = self._layers[PLOT_TABLE][LAYER]
                elif self._layers[BUILDING_TABLE][LAYER].selectedFeatureCount():
                    self.rad_to_building.setChecked(True)
                    self._current_layer = self._layers[BUILDING_TABLE][LAYER]
                elif self._layers[BUILDING_UNIT_TABLE][LAYER].selectedFeatureCount():
                    self.rad_to_building_unit.setChecked(True)
                    self._current_layer = self._layers[BUILDING_UNIT_TABLE][LAYER]
                else:
                    # By default current_layer will be plot layer
                    self.rad_to_plot.setChecked(True)
                    self._current_layer = self._layers[PLOT_TABLE][LAYER]

        if self.rad_to_plot.isChecked():
            self.rad_to_building.setStyleSheet(CSS_COLOR_INACTIVE_LABEL)
            self.rad_to_building_unit.setStyleSheet(CSS_COLOR_INACTIVE_LABEL)

            # Check selected features in plot layer
            if self._layers[PLOT_TABLE][LAYER].selectedFeatureCount() == 1:
                self.rad_to_plot.setStyleSheet(CSS_COLOR_OKAY_LABEL)
            elif self._layers[PLOT_TABLE][LAYER].selectedFeatureCount() > 1:
                # the color of the text is changed to highlight when there are more than one feature selected
                self.rad_to_plot.setStyleSheet(CSS_COLOR_ERROR_LABEL)
            else:
                # the color of the text is changed to highlight that there is no selection
                self.rad_to_plot.setStyleSheet(CSS_COLOR_ERROR_LABEL)

        elif self.rad_to_building.isChecked():
            self.rad_to_plot.setStyleSheet(CSS_COLOR_INACTIVE_LABEL)
            self.rad_to_building_unit.setStyleSheet(CSS_COLOR_INACTIVE_LABEL)

            # Check selected features in building layer
            if self._layers[BUILDING_TABLE][LAYER].selectedFeatureCount() == 1:
                self.rad_to_building.setStyleSheet(CSS_COLOR_OKAY_LABEL)
            elif self._layers[BUILDING_TABLE][LAYER].selectedFeatureCount() > 1:
                # the color of the text is changed to highlight when there are more than one feature selected
                self.rad_to_building.setStyleSheet(CSS_COLOR_ERROR_LABEL)
            else:
                # the color of the text is changed to highlight that there is no selection
                self.rad_to_building.setStyleSheet(CSS_COLOR_ERROR_LABEL)

        elif self.rad_to_building_unit.isChecked():
            self.rad_to_plot.setStyleSheet(CSS_COLOR_INACTIVE_LABEL)
            self.rad_to_building.setStyleSheet(CSS_COLOR_INACTIVE_LABEL)

            # Check selected features in building unit layer
            if self._layers[BUILDING_UNIT_TABLE][LAYER].selectedFeatureCount() == 1:
                self.rad_to_building_unit.setStyleSheet(CSS_COLOR_OKAY_LABEL)
            elif self._layers[BUILDING_UNIT_TABLE][LAYER].selectedFeatureCount() > 1:
                # the color of the text is changed to highlight when there are more than one features selected
                self.rad_to_building_unit.setStyleSheet(CSS_COLOR_ERROR_LABEL)
            else:
                # the color of the text is changed to highlight that there is no selection
                self.rad_to_building_unit.setStyleSheet(CSS_COLOR_ERROR_LABEL)

        # Zoom to selected feature
        self.canvas.zoomToSelected(self._current_layer)

        # Condition for enabling the finish button
        if self.rad_to_plot.isChecked() and self._layers[PLOT_TABLE][LAYER].selectedFeatureCount() == 1:
            self.button(self.FinishButton).setDisabled(False)
        elif self.rad_to_building.isChecked() and self._layers[BUILDING_TABLE][LAYER].selectedFeatureCount() == 1:
            self.button(self.FinishButton).setDisabled(False)
        elif self.rad_to_building_unit.isChecked() and self._layers[BUILDING_UNIT_TABLE][LAYER].selectedFeatureCount() == 1:
            self.button(self.FinishButton).setDisabled(False)
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
                self.qgis_utils.message_emitted.emit(
                    QCoreApplication.translate(self.WIZARD_NAME,
                                               "Select a source layer to set the field mapping to '{}'.").format(
                        EXTADDRESS_TABLE),
                    Qgis.Warning)
        else:
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
        self.close()

    def init_map_tool(self):
        try:
            self.canvas.mapToolSet.disconnect(self.map_tool_changed)
        except:
            pass
        self.canvas.setMapTool(self.maptool)

    def edit_feature(self):
        if self._current_layer.selectedFeatureCount() == 1:
            # Open Form
            self.iface.layerTreeView().setCurrentLayer(self._layers[EXTADDRESS_TABLE][LAYER])
            self._layers[EXTADDRESS_TABLE][LAYER].committedFeaturesAdded.connect(self.finish_feature_creation)
            self.qgis_utils.active_snapping_all_layers()
            self.open_form(self._layers[EXTADDRESS_TABLE][LAYER])

            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate(self.WIZARD_NAME,
                                           "Now you can click on the map to locate the new address..."),
                Qgis.Info)
        else:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate(self.WIZARD_NAME,
                                           "First select a {}.").format(self._db.get_ladm_layer_name(self._current_layer)),
                Qgis.Warning)

    def finish_feature_creation(self, layerId, features):
        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because an error occurred while trying to save the data.").format(self.WIZARD_TOOL_NAME)

        if len(features) != 1:
            message = QCoreApplication.translate(self.WIZARD_NAME,
                                                 "'{}' tool has been closed. We should have got only one spatial unit... We cannot do anything with {} spatials units").format(self.WIZARD_TOOL_NAME, len(features))
            self.log.logMessage("We should have got only one spatial unit... We cannot do anything with {} spatials units".format(len(features)), PLUGIN_NAME, Qgis.Warning)
        else:
            fid = features[0].id()

            if not self._layers[EXTADDRESS_TABLE][LAYER].getFeature(fid).isValid():
                message = QCoreApplication.translate(self.WIZARD_NAME,
                                                     "'{}' tool has been closed. Feature not found in layer {}... It's not posible create a ExtAddress. ").format(self.WIZARD_TOOL_NAME, EXTADDRESS_TABLE)
                self.log.logMessage("Feature not found in layer {} ...".format(EXTADDRESS_TABLE), PLUGIN_NAME, Qgis.Warning)
            else:
                extaddress_tid = self._layers[EXTADDRESS_TABLE][LAYER].getFeature(fid)[ID_FIELD]

                # Suppress (i.e., hide) feature form
                self.qgis_utils.suppress_form(self._layers[OID_TABLE][LAYER], True)

                # Add OID record
                self._layers[OID_TABLE][LAYER].startEditing()
                feature = QgsVectorLayerUtils().createFeature(self._layers[OID_TABLE][LAYER])
                feature.setAttribute(OID_EXTADDRESS_ID_FIELD, extaddress_tid)
                self._layers[OID_TABLE][LAYER].addFeature(feature)
                self._layers[OID_TABLE][LAYER].commitChanges()

                # Don't suppress (i.e., show) feature form
                self.qgis_utils.suppress_form(self._layers[OID_TABLE][LAYER], False)

                message = QCoreApplication.translate(self.WIZARD_NAME,
                                                     "The new extaddress (t_id={}) was successfully created ").format(extaddress_tid)

        self._layers[EXTADDRESS_TABLE][LAYER].committedFeaturesAdded.disconnect(self.finish_feature_creation)
        self.log.logMessage("ExtAddress's committedFeaturesAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        self.close_wizard(message)

    def open_form(self, layer):
        if not layer.isEditable():
            layer.startEditing()

        # action add ExtAddress feature
        self.qgis_utils.suppress_form(layer, True)
        self.iface.actionAddFeature().trigger()

        # Shows the form when the feature is created
        layer.featureAdded.connect(self.exec_form)
        layer.editCommandEnded.connect(self.confirm_commit)

    def exec_form(self, f_id):

        layer = self.sender()  # Get the layer that has sent the signal

        """
        This method only stores featIds in a class variable.
        It's required to avoid a bug with SLOTS connected to featureAdded.
        """
        self.added_features = f_id

        feature = self.qgis_utils.get_new_feature(layer)
        dialog = self.iface.getFeatureForm(layer, feature)
        dialog.setModal(True)

        if dialog.exec_():
            self.rollback_changes = False
        else:
            self.rollback_changes = True

    def confirm_commit(self):

        layer = self.sender() # Get the layer that has sent the signal

        try:
            layer.featureAdded.disconnect(self.exec_form)
            self.log.logMessage("ExtAddress's featureAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        except:
            pass

        if not self.rollback_changes:

            for f in layer.editBuffer().addedFeatures():
                feature = layer.editBuffer().addedFeatures()[f]
                break

            spatial_unit_field_idx = None
            if feature:

                # Get t_id of spatial unit to associate
                feature_id = self._current_layer.selectedFeatures()[0][ID_FIELD]
                fid = feature.id()

                # TODO: Update way to obtain the layer name when master merge with branch "change_detection"
                if self._db.get_ladm_layer_name(self._current_layer) == PLOT_TABLE:
                    spatial_unit_field_idx = layer.getFeature(fid).fieldNameIndex(EXTADDRESS_PLOT_FIELD)
                elif self._db.get_ladm_layer_name(self._current_layer) == BUILDING_TABLE:
                    spatial_unit_field_idx = layer.getFeature(fid).fieldNameIndex(EXTADDRESS_BUILDING_FIELD)
                elif self._db.get_ladm_layer_name(self._current_layer) == BUILDING_UNIT_TABLE:
                    spatial_unit_field_idx = layer.getFeature(fid).fieldNameIndex(EXTADDRESS_BUILDING_UNIT_FIELD)

            if spatial_unit_field_idx:
                # assign the relation with the spatial unit
                layer.changeAttributeValue(fid, spatial_unit_field_idx, feature_id)
            else:
                # if the field of the spatial unit does not exist
                layer.rollBack()
                message = QCoreApplication.translate(self.WIZARD_NAME,
                                                     "'{}' tool has been closed because when try to create ExtAddress it was not possible to associate a space unit.").format(
                    self.WIZARD_TOOL_NAME)
                self.close_wizard(message)

            saved = layer.commitChanges()

            if not saved:
                layer.rollBack()
                self.qgis_utils.message_emitted.emit(
                    QCoreApplication.translate(self.WIZARD_NAME,
                                               "Error while saving changes. ExtAddress could not be created."),
                    Qgis.Warning)
                for e in layer.commitErrors():
                    self.log.logMessage("Commit error: {}".format(e), PLUGIN_NAME, Qgis.Warning)
        else:
            layer.rollBack()
            self.form_rejected()

        self.iface.mapCanvas().refresh()
        self.added_features = None

    def form_rejected(self):
        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because you just closed the form.").format(self.WIZARD_TOOL_NAME)
        self.close_wizard(message)

    def save_settings(self):
        settings = QSettings()

        load_data_type = 'refactor'
        if self.rad_spatial_unit.isChecked():
            load_data_type = 'to_spatial_unit'

        settings.setValue('Asistente-LADM_COL/wizards/ext_address_load_data_type', load_data_type)

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value('Asistente-LADM_COL/wizards/ext_address_load_data_type', 'to_plot')
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_spatial_unit.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help("associate_ext_address")
