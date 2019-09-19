from functools import partial

from qgis.PyQt.QtCore import (QCoreApplication,
                              pyqtSignal)
from qgis.core import (Qgis,
                       QgsVectorLayerUtils)
from qgis.gui import QgsExpressionSelectionDialog

from .....config.general_config import (LAYER,
                                        PLUGIN_NAME,
                                        CSS_COLOR_OKAY_LABEL,
                                        CSS_COLOR_ERROR_LABEL,
                                        CSS_COLOR_INACTIVE_LABEL)
from .....config.table_mapping_config import (OID_TABLE,
                                              OID_EXTADDRESS_ID_FIELD,
                                              EXTADDRESS_BUILDING_UNIT_FIELD,
                                              EXTADDRESS_BUILDING_FIELD,
                                              EXTADDRESS_PLOT_FIELD,
                                              ID_FIELD,
                                              PLOT_TABLE,
                                              BUILDING_TABLE,
                                              BUILDING_UNIT_TABLE)
from .....config.wizards_config import WizardConfig
from .....gui.wizards.multi_page_spatial_wizard import MultiPageSpatialWizard
from .....gui.wizards.select_features_by_expression_wizard import SelectFeatureByExpressionWizard
from .....utils.select_map_tool import SelectMapTool


class CreateExtAddressCadastreWizard(MultiPageSpatialWizard,
                                     SelectFeatureByExpressionWizard):

    set_wizard_is_open_emitted = pyqtSignal(bool)
    set_finalize_geometry_creation_enabled_emitted = pyqtSignal(bool)

    def __init__(self, iface, db, qgis_utils, wizard_settings):
        MultiPageSpatialWizard.__init__(self, iface, db, qgis_utils, wizard_settings)
        SelectFeatureByExpressionWizard.__init__(self)
        self._current_layer = None

    #############################################################################
    # implement: raise NotImplementedError
    #############################################################################

    def register_select_feature_on_map(self):
        self.btn_plot_map.clicked.connect(partial(self.select_features_on_map, self._layers[PLOT_TABLE][LAYER]))
        self.btn_building_map.clicked.connect(partial(self.select_features_on_map, self._layers[BUILDING_TABLE][LAYER]))
        self.btn_building_unit_map.clicked.connect(partial(self.select_features_on_map, self._layers[BUILDING_UNIT_TABLE][LAYER]))

    def register_select_features_by_expression(self):
        self.btn_plot_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[PLOT_TABLE][LAYER]))
        self.btn_building_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[BUILDING_TABLE][LAYER]))
        self.btn_building_unit_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[BUILDING_UNIT_TABLE][LAYER]))

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

    def advance_save(self, features):
        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because an error occurred while trying to save the data.").format(self.WIZARD_TOOL_NAME)
        if len(features) != 1:
            message = QCoreApplication.translate(self.WIZARD_NAME, "'{}' tool has been closed. We should have got only one {} by we have {}").format(self.WIZARD_TOOL_NAME, self.WIZARD_FEATURE_NAME, len(features))
            self.log.logMessage("We should have got only one {}, but we have {}".format(self.WIZARD_FEATURE_NAME, len(features)), PLUGIN_NAME, Qgis.Warning)
        else:
            fid = features[0].id()

            if not self._layers[self.EDITING_LAYER_NAME][LAYER].getFeature(fid).isValid():
                message = QCoreApplication.translate(self.WIZARD_NAME,
                                                     "'{}' tool has been closed. Feature not found in layer {}... It's not posible create it. ").format(self.WIZARD_TOOL_NAME, self.EDITING_LAYER_NAME)
                self.log.logMessage("Feature not found in layer {} ...".format(self.EDITING_LAYER_NAME), PLUGIN_NAME, Qgis.Warning)
            else:
                extaddress_tid = self._layers[self.EDITING_LAYER_NAME][LAYER].getFeature(fid)[ID_FIELD]

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
                                                     "The new {} (t_id={}) was successfully created ").format(self.WIZARD_FEATURE_NAME, extaddress_tid)
        return message

    def disconnect_signals_select_features_by_expression(self):
        signals = [self.btn_plot_expression.clicked,
                   self.btn_building_expression.clicked,
                   self.btn_building_unit_expression.clicked]

        for signal in signals:
            try:
                signal.disconnect()
            except:
                pass

    def disconnect_signals_controls_select_features_on_map(self):
        signals = [self.btn_plot_map.clicked,
                   self.btn_building_map.clicked,
                   self.btn_building_unit_map.clicked]

        for signal in signals:
            try:
                signal.disconnect()
            except:
                pass

    def edit_feature(self):
        if self._current_layer.selectedFeatureCount() == 1:
            # Open Form
            self.iface.layerTreeView().setCurrentLayer(self._layers[self.EDITING_LAYER_NAME][LAYER])
            self._layers[self.EDITING_LAYER_NAME][LAYER].committedFeaturesAdded.connect(self.finish_feature_creation)

            self.qgis_utils.active_snapping_all_layers()
            self.open_form(self._layers[self.EDITING_LAYER_NAME][LAYER])

            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate(self.WIZARD_NAME,
                                           "Now you can click on the map to locate the new address..."),
                Qgis.Info)
        else:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate(self.WIZARD_NAME,
                                           "First select a {}.").format(self._db.get_ladm_layer_name(self._current_layer)),
                Qgis.Warning)

    def exec_form_advance(self, layer):
        for f in layer.editBuffer().addedFeatures():
            feature = layer.editBuffer().addedFeatures()[f]
            break

        spatial_unit_field_idx = None
        if feature:

            # Get t_id of spatial unit to associate
            feature_id = self._current_layer.selectedFeatures()[0][ID_FIELD]
            fid = feature.id()

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
                                                 "'{}' tool has been closed because when try to create {} it was not possible to associate a space unit.").format(self.WIZARD_TOOL_NAME, self.EDITING_LAYER_NAME)
            self.close_wizard(message)

    #############################################################################
    # Override methods
    #############################################################################

    def adjust_page_2_controls(self):
        self.button(self.FinishButton).setDisabled(True)
        self.disconnect_signals()

        # Load layers
        result = self.prepare_feature_creation_layers()
        if result is None:
            self.close_wizard(show_message=False)

        # Check if a previous features are selected
        self.check_selected_features()

        # Register select features by expression
        if hasattr(self, 'SELECTION_BY_EXPRESSION'):
            self.register_select_features_by_expression()

        # Register select features on map
        if hasattr(self, 'SELECTION_ON_MAP'):
            self.register_select_feature_on_map()

        self.rad_to_plot.toggled.connect(self.toggle_spatial_unit)
        self.rad_to_building.toggled.connect(self.toggle_spatial_unit)
        self.rad_to_building_unit.toggled.connect(self.toggle_spatial_unit)
        self.toggle_spatial_unit()

    def select_features_by_expression(self, layer):
        self._current_layer = layer
        self.iface.setActiveLayer(layer)
        dlg_expression_selection = QgsExpressionSelectionDialog(layer)
        layer.selectionChanged.connect(self.check_selected_features)
        dlg_expression_selection.exec()
        layer.selectionChanged.disconnect(self.check_selected_features)

    def select_features_on_map(self, layer):
        self._current_layer = layer
        self.iface.setActiveLayer(layer)
        self.setVisible(False)  # Make wizard disappear

        # Enable Select Map Tool
        self.select_maptool = SelectMapTool(self.canvas, layer, multi=False)

        self.canvas.setMapTool(self.select_maptool)
        # Connect signal that check if map tool change
        # This is necessary after select the maptool
        self.canvas.mapToolSet.connect(self.map_tool_changed)

        # Connect signal that check a feature was selected
        self.select_maptool.features_selected_signal.connect(self.features_selected)

    #############################################################################
    # Custom methods
    #############################################################################

    def toggle_spatial_unit(self):

        self.btn_plot_map.setEnabled(False)
        self.btn_building_map.setEnabled(False)
        self.btn_building_unit_map.setEnabled(False)

        self.btn_plot_expression.setEnabled(False)
        self.btn_building_expression.setEnabled(False)
        self.btn_building_unit_expression.setEnabled(False)

        if self.rad_to_plot.isChecked():
            self.txt_help_page_2.setHtml(self.wizard_config[WizardConfig.WIZARD_HELP_PAGES_SETTING][WizardConfig.WIZARD_HELP1])
            self._current_layer = self._layers[PLOT_TABLE][LAYER]

            self.btn_plot_map.setEnabled(True)
            self.btn_plot_expression.setEnabled(True)

        elif self.rad_to_building.isChecked():
            self.txt_help_page_2.setHtml(self.wizard_config[WizardConfig.WIZARD_HELP_PAGES_SETTING][WizardConfig.WIZARD_HELP2])
            self._current_layer = self._layers[BUILDING_TABLE][LAYER]

            self.btn_building_map.setEnabled(True)
            self.btn_building_expression.setEnabled(True)

        elif self.rad_to_building_unit.isChecked():
            self.txt_help_page_2.setHtml(self.wizard_config[WizardConfig.WIZARD_HELP_PAGES_SETTING][WizardConfig.WIZARD_HELP3])
            self._current_layer = self._layers[BUILDING_UNIT_TABLE][LAYER]

            self.btn_building_unit_map.setEnabled(True)
            self.btn_building_unit_expression.setEnabled(True)

        self.iface.setActiveLayer(self._current_layer)
        self.check_selected_features()