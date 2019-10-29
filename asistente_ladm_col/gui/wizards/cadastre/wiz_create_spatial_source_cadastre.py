from functools import partial

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsVectorLayerUtils,
                       Qgis)

from asistente_ladm_col.config.general_config import (LAYER,
                                                      PLUGIN_NAME)
from asistente_ladm_col.gui.wizards.multi_page_wizard_factory import MultiPageWizardFactory
from asistente_ladm_col.gui.wizards.select_features_by_expression_dialog_wrapper import SelectFeatureByExpressionDialogWrapper
from asistente_ladm_col.gui.wizards.select_features_on_map_wrapper import SelectFeaturesOnMapWrapper


class CreateSpatialSourceCadastreWizard(MultiPageWizardFactory,
                                        SelectFeatureByExpressionDialogWrapper,
                                        SelectFeaturesOnMapWrapper):
    def __init__(self, iface, db, qgis_utils, wizard_settings):
        MultiPageWizardFactory.__init__(self, iface, db, qgis_utils, wizard_settings)
        SelectFeatureByExpressionDialogWrapper.__init__(self)
        SelectFeaturesOnMapWrapper.__init__(self)

    def post_save(self, features):
        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because an error occurred while trying to save the data.").format(self.WIZARD_TOOL_NAME)
        if len(features) != 1:
            message = QCoreApplication.translate(self.WIZARD_NAME, "'{}' tool has been closed. We should have got only one {} by we have {}").format(self.WIZARD_TOOL_NAME, self.WIZARD_FEATURE_NAME, len(features))
            self.log.logMessage("We should have got only one {}, but we have {}".format(self.WIZARD_FEATURE_NAME, len(features)), PLUGIN_NAME, Qgis.Warning)
        else:
            feature = features[0]
            feature_ids_dict = dict()

            if self._layers[self.names.OP_PLOT_T][LAYER] is not None:
                if self._layers[self.names.OP_PLOT_T][LAYER].selectedFeatureCount() > 0:
                    feature_ids_dict[self.names.OP_PLOT_T] = [f[self.names.T_ID_F] for f in self._layers[self.names.OP_PLOT_T][LAYER].selectedFeatures()]

            if self._layers[self.names.OP_BOUNDARY_T][LAYER] is not None:
                if self._layers[self.names.OP_BOUNDARY_T][LAYER].selectedFeatureCount() > 0:
                    feature_ids_dict[self.names.OP_BOUNDARY_T] = [f[self.names.T_ID_F] for f in self._layers[self.names.OP_BOUNDARY_T][LAYER].selectedFeatures()]

            if self._layers[self.names.OP_BOUNDARY_POINT_T][LAYER] is not None:
                if self._layers[self.names.OP_BOUNDARY_POINT_T][LAYER].selectedFeatureCount() > 0:
                    feature_ids_dict[self.names.OP_BOUNDARY_POINT_T] = [f[self.names.T_ID_F] for f in self._layers[self.names.OP_BOUNDARY_POINT_T][LAYER].selectedFeatures()]

            if self._layers[self.names.OP_SURVEY_POINT_T][LAYER] is not None:
                if self._layers[self.names.OP_SURVEY_POINT_T][LAYER].selectedFeatureCount() > 0:
                    feature_ids_dict[self.names.OP_SURVEY_POINT_T] = [f[self.names.T_ID_F] for f in self._layers[self.names.OP_SURVEY_POINT_T][LAYER].selectedFeatures()]

            if self._layers[self.names.OP_CONTROL_POINT_T][LAYER] is not None:
                if self._layers[self.names.OP_CONTROL_POINT_T][LAYER].selectedFeatureCount() > 0:
                    feature_ids_dict[self.names.OP_CONTROL_POINT_T] = [f[self.names.T_ID_F] for f in self._layers[self.names.OP_CONTROL_POINT_T][LAYER].selectedFeatures()]

            if not feature.isValid():
                self.log.logMessage("Feature not found in layer Spatial Source...", PLUGIN_NAME, Qgis.Warning)
            else:
                spatial_source_id = feature[self.names.T_ID_F]
                all_new_features = list()

                # Fill association table, depending on the case
                new_features = list()
                if self.names.OP_PLOT_T in feature_ids_dict:
                    # Fill uesource table
                    for plot_id in feature_ids_dict[self.names.OP_PLOT_T]:
                        new_feature = QgsVectorLayerUtils().createFeature(self._layers[self.names.COL_UE_SOURCE_T][LAYER])
                        new_feature.setAttribute(self.names.COL_UE_SOURCE_T_OP_PLOT_F, plot_id)
                        new_feature.setAttribute(self.names.COL_UE_SOURCE_T_SOURCE_F, spatial_source_id)
                        self.log.logMessage("Saving Plot-SpatialSource: {}-{}".format(plot_id, spatial_source_id), PLUGIN_NAME, Qgis.Info)
                        new_features.append(new_feature)

                    self._layers[self.names.COL_UE_SOURCE_T][LAYER].dataProvider().addFeatures(new_features)
                    all_new_features.extend(new_feature)

                new_features = list()
                if self.names.OP_BOUNDARY_T in feature_ids_dict:
                    # Fill cclsource table
                    for boundary_id in feature_ids_dict[self.names.OP_BOUNDARY_T]:
                        new_feature = QgsVectorLayerUtils().createFeature(self._layers[self.names.COL_CCL_SOURCE_T][LAYER])

                        # Todo: Update COL_CCL_SOURCE_T_BOUNDARY_F_OP by COL_CCL_SOURCE_T_BOUNDARY_F.
                        # Todo: When an abstract class only implements a concrete class, the name of the attribute is different if two or more classes are implemented.
                        new_feature.setAttribute(self.names.COL_CCL_SOURCE_T_BOUNDARY_F_OP, boundary_id)
                        new_feature.setAttribute(self.names.COL_CCL_SOURCE_T_SOURCE_F, spatial_source_id)
                        self.log.logMessage("Saving Boundary-SpatialSource: {}-{}".format(boundary_id, spatial_source_id), PLUGIN_NAME, Qgis.Info)
                        new_features.append(new_feature)

                    self._layers[self.names.COL_CCL_SOURCE_T][LAYER].dataProvider().addFeatures(new_features)
                    all_new_features.extend(new_feature)

                new_features = list()
                if self.names.OP_BOUNDARY_POINT_T in feature_ids_dict:
                    for boundary_point_id in feature_ids_dict[self.names.OP_BOUNDARY_POINT_T]:
                        new_feature = QgsVectorLayerUtils().createFeature(self._layers[self.names.COL_POINT_SOURCE_T][LAYER])
                        new_feature.setAttribute(self.names.COL_POINT_SOURCE_T_OP_BOUNDARY_POINT_F, boundary_point_id)
                        new_feature.setAttribute(self.names.COL_POINT_SOURCE_T_SOURCE_F, spatial_source_id)
                        self.log.logMessage("Saving BoundaryPoint-SpatialSource: {}-{}".format(boundary_point_id, spatial_source_id), PLUGIN_NAME, Qgis.Info)
                        new_features.append(new_feature)

                    self._layers[self.names.COL_POINT_SOURCE_T][LAYER].dataProvider().addFeatures(new_features)
                    all_new_features.extend(new_feature)

                new_features = list()
                if self.names.OP_SURVEY_POINT_T in feature_ids_dict:
                    for survey_point_id in feature_ids_dict[self.names.OP_SURVEY_POINT_T]:
                        new_feature = QgsVectorLayerUtils().createFeature(self._layers[self.names.COL_POINT_SOURCE_T][LAYER])
                        new_feature.setAttribute(self.names.COL_POINT_SOURCE_T_OP_SURVEY_POINT_F, survey_point_id)
                        new_feature.setAttribute(self.names.COL_POINT_SOURCE_T_SOURCE_F, spatial_source_id)
                        self.log.logMessage("Saving SurveyPoint-SpatialSource: {}-{}".format(survey_point_id, spatial_source_id), PLUGIN_NAME, Qgis.Info)
                        new_features.append(new_feature)

                    self._layers[self.names.COL_POINT_SOURCE_T][LAYER].dataProvider().addFeatures(new_features)
                    all_new_features.extend(new_feature)

                new_features = list()
                if self.names.OP_CONTROL_POINT_T in feature_ids_dict:
                    for control_point_id in feature_ids_dict[self.names.OP_CONTROL_POINT_T]:
                        new_feature = QgsVectorLayerUtils().createFeature(self._layers[self.names.COL_POINT_SOURCE_T][LAYER])
                        new_feature.setAttribute(self.names.COL_POINT_SOURCE_T_OP_CONTROL_POINT_F, control_point_id)
                        new_feature.setAttribute(self.names.COL_POINT_SOURCE_T_SOURCE_F, spatial_source_id)
                        self.log.logMessage("Saving ControlPoint-SpatialSource: {}-{}".format(control_point_id, spatial_source_id), PLUGIN_NAME, Qgis.Info)
                        new_features.append(new_feature)

                    self._layers[self.names.COL_POINT_SOURCE_T][LAYER].dataProvider().addFeatures(new_features)
                    all_new_features.extend(new_feature)

                if all_new_features:
                    message = QCoreApplication.translate(self.WIZARD_NAME,
                                                   "The new spatial source (t_id={}) was successfully created and associated with the following features: {}").format(spatial_source_id, feature_ids_dict)
                else:
                    message = QCoreApplication.translate(self.WIZARD_NAME,
                                                   "The new spatial source (t_id={}) was successfully created and it wasn't associated with a spatial unit").format(spatial_source_id)

        return message

    def exec_form_advanced(self, layer):
        pass

    def check_selected_features(self):
        # Check selected features in plot layer
        self.lb_plot.setText(QCoreApplication.translate(self.WIZARD_NAME, "<b>Plot(s)</b>: {count} Feature(s) Selected").format(count=self._layers[self.names.OP_PLOT_T][LAYER].selectedFeatureCount()))
        # Check selected features in boundary layer
        self.lb_boundary.setText(QCoreApplication.translate(self.WIZARD_NAME, "<b>Boundary(ies)</b>: {count} Feature(s) Selected").format(count=self._layers[self.names.OP_BOUNDARY_T][LAYER].selectedFeatureCount()))
        # Check selected features in boundary point layer
        self.lb_boundary_point.setText(QCoreApplication.translate(self.WIZARD_NAME, "<b>Boundary</b>: {count} Feature(s) Selected").format(count=self._layers[self.names.OP_BOUNDARY_POINT_T][LAYER].selectedFeatureCount()))
        # Check selected features in survey point layer
        self.lb_survey_point.setText(QCoreApplication.translate(self.WIZARD_NAME, "<b>Survey</b>: {count} Feature(s) Selected").format(count=self._layers[self.names.OP_SURVEY_POINT_T][LAYER].selectedFeatureCount()))
        # Check selected features in control point layer
        self.lb_control_point.setText(QCoreApplication.translate(self.WIZARD_NAME, "<b>Control</b>: {count} Feature(s) Selected").format(count=self._layers[self.names.OP_CONTROL_POINT_T][LAYER].selectedFeatureCount()))

        # Verifies that an feature has been selected
        if self._layers[self.names.OP_PLOT_T][LAYER].selectedFeatureCount() + self._layers[self.names.OP_BOUNDARY_T][LAYER].selectedFeatureCount() + self._layers[self.names.OP_BOUNDARY_POINT_T][LAYER].selectedFeatureCount() + self._layers[self.names.OP_SURVEY_POINT_T][LAYER].selectedFeatureCount() + self._layers[self.names.OP_CONTROL_POINT_T][LAYER].selectedFeatureCount() >= 1:
            self.button(self.FinishButton).setDisabled(False)
        else:
            self.button(self.FinishButton).setDisabled(True)

    def disconnect_signals_select_features_by_expression(self):
        signals = [self.btn_plot_expression.clicked,
                   self.btn_boundary_expression.clicked,
                   self.btn_boundary_point_expression.clicked,
                   self.btn_survey_point_expression.clicked,
                   self.btn_control_point_expression.clicked]

        for signal in signals:
            try:
                signal.disconnect()
            except:
                pass

    def register_select_features_by_expression(self):
        self.btn_plot_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[self.names.OP_PLOT_T][LAYER]))
        self.btn_boundary_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[self.names.OP_BOUNDARY_T][LAYER]))
        self.btn_boundary_point_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[self.names.OP_BOUNDARY_POINT_T][LAYER]))
        self.btn_survey_point_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[self.names.OP_SURVEY_POINT_T][LAYER]))
        self.btn_control_point_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[self.names.OP_CONTROL_POINT_T][LAYER]))

    def disconnect_signals_controls_select_features_on_map(self):
        signals = [self.btn_plot_map.clicked,
                   self.btn_boundary_map.clicked,
                   self.btn_boundary_point_map.clicked,
                   self.btn_survey_point_map.clicked,
                   self.btn_control_point_map.clicked]

        for signal in signals:
            try:
                signal.disconnect()
            except:
                pass

    def register_select_feature_on_map(self):
        self.btn_plot_map.clicked.connect(partial(self.select_features_on_map, self._layers[self.names.OP_PLOT_T][LAYER]))
        self.btn_boundary_map.clicked.connect(partial(self.select_features_on_map, self._layers[self.names.OP_BOUNDARY_T][LAYER]))
        self.btn_boundary_point_map.clicked.connect(partial(self.select_features_on_map, self._layers[self.names.OP_BOUNDARY_POINT_T][LAYER]))
        self.btn_survey_point_map.clicked.connect(partial(self.select_features_on_map, self._layers[self.names.OP_SURVEY_POINT_T][LAYER]))
        self.btn_control_point_map.clicked.connect(partial(self.select_features_on_map, self._layers[self.names.OP_CONTROL_POINT_T][LAYER]))
