from functools import partial

from qgis.PyQt.QtCore import (QCoreApplication,
                              pyqtSignal)
from qgis.PyQt.QtWidgets import QWizard
from qgis.core import (QgsVectorLayerUtils,
                       QgsGeometry,
                       Qgis)

from .....config.general_config import (LAYER,
                                        CSS_COLOR_OKAY_LABEL,
                                        CSS_COLOR_ERROR_LABEL)
from .....config.table_mapping_config import (BOUNDARY_TABLE,
                                              PLOT_REGISTRY_AREA_FIELD,
                                              PLOT_CALCULATED_AREA_FIELD)
from .....config.wizards_config import WizardConfig
from .....gui.wizards.multi_page_wizard_factory import MultiPageWizardFactory
from .....gui.wizards.select_features_by_expression_wizard import SelectFeatureByExpressionWizard
from .....gui.wizards.select_features_on_map_wizard import SelectFeaturesOnMapWizard
from .....utils.qt_utils import (enable_next_wizard,
                                 disable_next_wizard)


class CreatePlotCadastreWizard(MultiPageWizardFactory,
                               SelectFeatureByExpressionWizard,
                               SelectFeaturesOnMapWizard):
    set_wizard_is_open_emitted = pyqtSignal(bool)
    set_finalize_geometry_creation_enabled_emitted = pyqtSignal(bool)

    def __init__(self, iface, db, qgis_utils, wizard_settings):
        self.iface = iface
        MultiPageWizardFactory.__init__(self, iface, db, qgis_utils, wizard_settings)
        SelectFeatureByExpressionWizard.__init__(self)
        SelectFeaturesOnMapWizard.__init__(self)

    def advance_save(self, features):
        pass

    def exec_form_advance(self, layer):
        pass

    def check_selected_features(self):
        self.lb_info.setText(QCoreApplication.translate(self.WIZARD_NAME, "<b>Boundary(ies)</b>: {count} Feature(s) Selected").format(count=self._layers[BOUNDARY_TABLE][LAYER].selectedFeatureCount()))
        self.lb_info.setStyleSheet(CSS_COLOR_OKAY_LABEL)  # Default color

        _color = CSS_COLOR_OKAY_LABEL
        has_selected_boundaries = self._layers[BOUNDARY_TABLE][LAYER].selectedFeatureCount() > 0
        if not has_selected_boundaries:
            _color = CSS_COLOR_ERROR_LABEL
        self.lb_info.setStyleSheet(_color)

        self.button(self.FinishButton).setEnabled(has_selected_boundaries)

    def disconnect_signals_select_features_by_expression(self):
        signals = [self.btn_expression.clicked,
                   self.btn_select_all.clicked]

        for signal in signals:
            try:
                signal.disconnect()
            except:
                pass

    def register_select_features_by_expression(self):
        self.btn_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[BOUNDARY_TABLE][LAYER]))
        self.btn_select_all.clicked.connect(partial(self.select_all_features, self._layers[BOUNDARY_TABLE][LAYER]))

    def disconnect_signals_controls_select_features_on_map(self):
        signals = [self.btn_map.clicked]

        for signal in signals:
            try:
                signal.disconnect()
            except:
                pass

    def register_select_feature_on_map(self):
        self.btn_map.clicked.connect(partial(self.select_features_on_map, self._layers[BOUNDARY_TABLE][LAYER]))

    #############################################################################
    # Override methods
    #############################################################################

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
            finish_button_text = QCoreApplication.translate(self.WIZARD_NAME, "Import")
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(self.EDITING_LAYER_NAME, True))
            self.wizardPage1.setButtonText(QWizard.FinishButton, finish_button_text)
        elif self.rad_create_manually.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            enable_next_wizard(self)
            self.wizardPage1.setFinalPage(False)
            finish_button_text = QCoreApplication.translate(self.WIZARD_NAME, "Create")
            self.txt_help_page_1.setHtml(self.wizard_config[WizardConfig.WIZARD_HELP_PAGES_SETTING][WizardConfig.WIZARD_HELP_PAGE1])

        self.wizardPage1.setButtonText(QWizard.FinishButton, finish_button_text)

    def edit_feature(self):
        if self._layers[BOUNDARY_TABLE][LAYER].selectedFeatureCount() > 0:
            # Open Form
            self.iface.layerTreeView().setCurrentLayer(self._layers[self.EDITING_LAYER_NAME][LAYER])
            self.qgis_utils.active_snapping_all_layers()
            self.create_plots_from_boundaries()
        else:
            self.qgis_utils.message_emitted.emit(QCoreApplication.translate(self.WIZARD_NAME, "First select boundaries!"), Qgis.Warning)

    #############################################################################
    # Custom methods
    #############################################################################

    def select_all_features(self, layer):
        layer.selectAll()
        self.check_selected_features()

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
