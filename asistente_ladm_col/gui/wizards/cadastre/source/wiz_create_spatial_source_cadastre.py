from functools import partial

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsVectorLayerUtils,
                       Qgis)

from .....config.general_config import (LAYER,
                                        PLUGIN_NAME)
from .....config.table_mapping_config import (PLOT_TABLE,
                                              BOUNDARY_TABLE,
                                              BOUNDARY_POINT_TABLE,
                                              SURVEY_POINT_TABLE,
                                              CONTROL_POINT_TABLE,
                                              UESOURCE_TABLE,
                                              UESOURCE_TABLE_PLOT_FIELD,
                                              UESOURCE_TABLE_SOURCE_FIELD,
                                              CCLSOURCE_TABLE,
                                              CCLSOURCE_TABLE_BOUNDARY_FIELD,
                                              CCLSOURCE_TABLE_SOURCE_FIELD,
                                              POINTSOURCE_TABLE_BOUNDARYPOINT_FIELD,
                                              POINTSOURCE_TABLE_SURVEYPOINT_FIELD,
                                              POINTSOURCE_TABLE,
                                              POINTSOURCE_TABLE_CONTROLPOINT_FIELD,
                                              POINTSOURCE_TABLE_SOURCE_FIELD,
                                              ID_FIELD)
from .....gui.wizards.multi_page_wizard_factory import MultiPageWizardFactory
from .....gui.wizards.select_features_by_expression_dialog_wrapper import SelectFeatureByExpressionDialogWrapper
from .....gui.wizards.select_features_on_map_wrapper import SelectFeaturesOnMapWrapper


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

            if self._layers[PLOT_TABLE][LAYER] is not None:
                if self._layers[PLOT_TABLE][LAYER].selectedFeatureCount() > 0:
                    feature_ids_dict[PLOT_TABLE] = [f[ID_FIELD] for f in self._layers[PLOT_TABLE][LAYER].selectedFeatures()]

            if self._layers[BOUNDARY_TABLE][LAYER] is not None:
                if self._layers[BOUNDARY_TABLE][LAYER].selectedFeatureCount() > 0:
                    feature_ids_dict[BOUNDARY_TABLE] = [f[ID_FIELD] for f in self._layers[BOUNDARY_TABLE][LAYER].selectedFeatures()]

            if self._layers[BOUNDARY_POINT_TABLE][LAYER] is not None:
                if self._layers[BOUNDARY_POINT_TABLE][LAYER].selectedFeatureCount() > 0:
                    feature_ids_dict[BOUNDARY_POINT_TABLE] = [f[ID_FIELD] for f in self._layers[BOUNDARY_POINT_TABLE][LAYER].selectedFeatures()]

            if self._layers[SURVEY_POINT_TABLE][LAYER] is not None:
                if self._layers[SURVEY_POINT_TABLE][LAYER].selectedFeatureCount() > 0:
                    feature_ids_dict[SURVEY_POINT_TABLE] = [f[ID_FIELD] for f in self._layers[SURVEY_POINT_TABLE][LAYER].selectedFeatures()]

            if self._layers[CONTROL_POINT_TABLE][LAYER] is not None:
                if self._layers[CONTROL_POINT_TABLE][LAYER].selectedFeatureCount() > 0:
                    feature_ids_dict[CONTROL_POINT_TABLE] = [f[ID_FIELD] for f in self._layers[CONTROL_POINT_TABLE][LAYER].selectedFeatures()]

            if not feature.isValid():
                self.log.logMessage("Feature not found in layer Spatial Source...", PLUGIN_NAME, Qgis.Warning)
            else:
                spatial_source_id = feature[ID_FIELD]
                all_new_features = list()

                # Fill association table, depending on the case
                new_features = list()
                if PLOT_TABLE in feature_ids_dict:
                    # Fill uesource table
                    for plot_id in feature_ids_dict[PLOT_TABLE]:
                        new_feature = QgsVectorLayerUtils().createFeature(self._layers[UESOURCE_TABLE][LAYER])
                        new_feature.setAttribute(UESOURCE_TABLE_PLOT_FIELD, plot_id)
                        new_feature.setAttribute(UESOURCE_TABLE_SOURCE_FIELD, spatial_source_id)
                        self.log.logMessage("Saving Plot-SpatialSource: {}-{}".format(plot_id, spatial_source_id), PLUGIN_NAME, Qgis.Info)
                        new_features.append(new_feature)

                    self._layers[UESOURCE_TABLE][LAYER].dataProvider().addFeatures(new_features)
                    all_new_features.extend(new_feature)

                new_features = list()
                if BOUNDARY_TABLE in feature_ids_dict:
                    # Fill cclsource table
                    for boundary_id in feature_ids_dict[BOUNDARY_TABLE]:
                        new_feature = QgsVectorLayerUtils().createFeature(self._layers[CCLSOURCE_TABLE][LAYER])
                        new_feature.setAttribute(CCLSOURCE_TABLE_BOUNDARY_FIELD, boundary_id)
                        new_feature.setAttribute(CCLSOURCE_TABLE_SOURCE_FIELD, spatial_source_id)
                        self.log.logMessage("Saving Boundary-SpatialSource: {}-{}".format(boundary_id, spatial_source_id), PLUGIN_NAME, Qgis.Info)
                        new_features.append(new_feature)

                    self._layers[CCLSOURCE_TABLE][LAYER].dataProvider().addFeatures(new_features)
                    all_new_features.extend(new_feature)

                new_features = list()
                if BOUNDARY_POINT_TABLE in feature_ids_dict:
                    for boundary_point_id in feature_ids_dict[BOUNDARY_POINT_TABLE]:
                        new_feature = QgsVectorLayerUtils().createFeature(self._layers[POINTSOURCE_TABLE][LAYER])
                        new_feature.setAttribute(POINTSOURCE_TABLE_BOUNDARYPOINT_FIELD, boundary_point_id)
                        new_feature.setAttribute(POINTSOURCE_TABLE_SOURCE_FIELD, spatial_source_id)
                        self.log.logMessage("Saving BoundaryPoint-SpatialSource: {}-{}".format(boundary_point_id, spatial_source_id), PLUGIN_NAME, Qgis.Info)
                        new_features.append(new_feature)

                    self._layers[POINTSOURCE_TABLE][LAYER].dataProvider().addFeatures(new_features)
                    all_new_features.extend(new_feature)

                new_features = list()
                if SURVEY_POINT_TABLE in feature_ids_dict:
                    for survey_point_id in feature_ids_dict[SURVEY_POINT_TABLE]:
                        new_feature = QgsVectorLayerUtils().createFeature(self._layers[POINTSOURCE_TABLE][LAYER])
                        new_feature.setAttribute(POINTSOURCE_TABLE_SURVEYPOINT_FIELD, survey_point_id)
                        new_feature.setAttribute(POINTSOURCE_TABLE_SOURCE_FIELD, spatial_source_id)
                        self.log.logMessage("Saving SurveyPoint-SpatialSource: {}-{}".format(survey_point_id, spatial_source_id), PLUGIN_NAME, Qgis.Info)
                        new_features.append(new_feature)

                    self._layers[POINTSOURCE_TABLE][LAYER].dataProvider().addFeatures(new_features)
                    all_new_features.extend(new_feature)

                new_features = list()
                if CONTROL_POINT_TABLE in feature_ids_dict:
                    for control_point_id in feature_ids_dict[CONTROL_POINT_TABLE]:
                        new_feature = QgsVectorLayerUtils().createFeature(self._layers[POINTSOURCE_TABLE][LAYER])
                        new_feature.setAttribute(POINTSOURCE_TABLE_CONTROLPOINT_FIELD, control_point_id)
                        new_feature.setAttribute(POINTSOURCE_TABLE_SOURCE_FIELD, spatial_source_id)
                        self.log.logMessage("Saving ControlPoint-SpatialSource: {}-{}".format(control_point_id, spatial_source_id), PLUGIN_NAME, Qgis.Info)
                        new_features.append(new_feature)

                    self._layers[POINTSOURCE_TABLE][LAYER].dataProvider().addFeatures(new_features)
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
        self.lb_plot.setText(QCoreApplication.translate(self.WIZARD_NAME, "<b>Plot(s)</b>: {count} Feature(s) Selected").format(count=self._layers[PLOT_TABLE][LAYER].selectedFeatureCount()))
        # Check selected features in boundary layer
        self.lb_boundary.setText(QCoreApplication.translate(self.WIZARD_NAME, "<b>Boundary(ies)</b>: {count} Feature(s) Selected").format(count=self._layers[BOUNDARY_TABLE][LAYER].selectedFeatureCount()))
        # Check selected features in boundary point layer
        self.lb_boundary_point.setText(QCoreApplication.translate(self.WIZARD_NAME, "<b>Boundary</b>: {count} Feature(s) Selected").format(count=self._layers[BOUNDARY_POINT_TABLE][LAYER].selectedFeatureCount()))
        # Check selected features in survey point layer
        self.lb_survey_point.setText(QCoreApplication.translate(self.WIZARD_NAME, "<b>Survey</b>: {count} Feature(s) Selected").format(count=self._layers[SURVEY_POINT_TABLE][LAYER].selectedFeatureCount()))
        # Check selected features in control point layer
        self.lb_control_point.setText(QCoreApplication.translate(self.WIZARD_NAME, "<b>Control</b>: {count} Feature(s) Selected").format(count=self._layers[CONTROL_POINT_TABLE][LAYER].selectedFeatureCount()))

        # Verifies that an feature has been selected
        if self._layers[PLOT_TABLE][LAYER].selectedFeatureCount() + self._layers[BOUNDARY_TABLE][LAYER].selectedFeatureCount() + self._layers[BOUNDARY_POINT_TABLE][LAYER].selectedFeatureCount() + self._layers[SURVEY_POINT_TABLE][LAYER].selectedFeatureCount() + self._layers[CONTROL_POINT_TABLE][LAYER].selectedFeatureCount() >= 1:
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
        self.btn_plot_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[PLOT_TABLE][LAYER]))
        self.btn_boundary_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[BOUNDARY_TABLE][LAYER]))
        self.btn_boundary_point_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[BOUNDARY_POINT_TABLE][LAYER]))
        self.btn_survey_point_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[SURVEY_POINT_TABLE][LAYER]))
        self.btn_control_point_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[CONTROL_POINT_TABLE][LAYER]))

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
        self.btn_plot_map.clicked.connect(partial(self.select_features_on_map, self._layers[PLOT_TABLE][LAYER]))
        self.btn_boundary_map.clicked.connect(partial(self.select_features_on_map, self._layers[BOUNDARY_TABLE][LAYER]))
        self.btn_boundary_point_map.clicked.connect(partial(self.select_features_on_map, self._layers[BOUNDARY_POINT_TABLE][LAYER]))
        self.btn_survey_point_map.clicked.connect(partial(self.select_features_on_map, self._layers[SURVEY_POINT_TABLE][LAYER]))
        self.btn_control_point_map.clicked.connect(partial(self.select_features_on_map, self._layers[CONTROL_POINT_TABLE][LAYER]))
