# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-09-10
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BFS Swissphoto)
                               (C) 2019 by Leo Cardona (BFS Swissphoto)
        email                : gcarrillo@linuxmail.org
                               leo.cardona.p@gmail.com
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
                              pyqtSignal)
from qgis.PyQt.QtWidgets import QWizard
from qgis.core import (QgsVectorLayerUtils,
                       QgsGeometry,
                       Qgis)

from asistente_ladm_col.config.general_config import (CSS_COLOR_OKAY_LABEL,
                                                      CSS_COLOR_ERROR_LABEL,
                                                      WIZARD_HELP_PAGES,
                                                      WIZARD_HELP1)
from asistente_ladm_col.gui.wizards.multi_page_wizard_factory import MultiPageWizardFactory
from asistente_ladm_col.gui.wizards.select_features_by_expression_dialog_wrapper import SelectFeatureByExpressionDialogWrapper
from asistente_ladm_col.gui.wizards.select_features_on_map_wrapper import SelectFeaturesOnMapWrapper
from asistente_ladm_col.utils.qt_utils import (enable_next_wizard,
                                               disable_next_wizard)


class CreatePlotOperationWizard(MultiPageWizardFactory,
                               SelectFeatureByExpressionDialogWrapper,
                               SelectFeaturesOnMapWrapper):
    update_wizard_is_open_flag = pyqtSignal(bool)
    set_finalize_geometry_creation_enabled_emitted = pyqtSignal(bool)

    def __init__(self, iface, db, qgis_utils, wizard_settings):
        self.iface = iface
        MultiPageWizardFactory.__init__(self, iface, db, qgis_utils, wizard_settings)
        SelectFeatureByExpressionDialogWrapper.__init__(self)
        SelectFeaturesOnMapWrapper.__init__(self)

    def post_save(self, features):
        pass

    def exec_form_advanced(self, layer):
        pass

    def check_selected_features(self):
        self.lb_info.setText(QCoreApplication.translate("WizardTranslations", "<b>Boundary(ies)</b>: {count} Feature(s) Selected").format(count=self._layers[self.names.OP_BOUNDARY_T].selectedFeatureCount()))
        self.lb_info.setStyleSheet(CSS_COLOR_OKAY_LABEL)  # Default color

        _color = CSS_COLOR_OKAY_LABEL
        has_selected_boundaries = self._layers[self.names.OP_BOUNDARY_T].selectedFeatureCount() > 0
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
        self.btn_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[self.names.OP_BOUNDARY_T]))
        self.btn_select_all.clicked.connect(partial(self.select_all_features, self._layers[self.names.OP_BOUNDARY_T]))

    def disconnect_signals_controls_select_features_on_map(self):
        signals = [self.btn_map.clicked]

        for signal in signals:
            try:
                signal.disconnect()
            except:
                pass

    def register_select_feature_on_map(self):
        self.btn_map.clicked.connect(partial(self.select_features_on_map, self._layers[self.names.OP_BOUNDARY_T]))

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
            finish_button_text = QCoreApplication.translate("WizardTranslations", "Import")
            self.txt_help_page_1.setHtml(self.help_strings.get_refactor_help_string(self._db, self._layers[self.EDITING_LAYER_NAME]))
            self.wizardPage1.setButtonText(QWizard.FinishButton, finish_button_text)
        elif self.rad_create_manually.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            enable_next_wizard(self)
            self.wizardPage1.setFinalPage(False)
            finish_button_text = QCoreApplication.translate("WizardTranslations", "Create")
            self.txt_help_page_1.setHtml(self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP1])

        self.wizardPage1.setButtonText(QWizard.FinishButton, finish_button_text)

    def edit_feature(self):
        if self._layers[self.names.OP_BOUNDARY_T].selectedFeatureCount() > 0:
            # Open Form
            self.iface.layerTreeView().setCurrentLayer(self._layers[self.EDITING_LAYER_NAME])
            self.qgis_utils.active_snapping_all_layers()
            self.create_plots_from_boundaries()
        else:
            self.logger.warning_msg(__name__, QCoreApplication.translate("WizardTranslations", "First select boundaries!"))

    #############################################################################
    # Custom methods
    #############################################################################

    def select_all_features(self, layer):
        layer.selectAll()
        self.check_selected_features()

    def create_plots_from_boundaries(self):
        selected_boundaries = self._layers[self.names.OP_BOUNDARY_T].selectedFeatures()

        boundary_geometries = [f.geometry() for f in selected_boundaries]
        collection = QgsGeometry().polygonize(boundary_geometries)
        features = list()
        for polygon in collection.asGeometryCollection():
            feature = QgsVectorLayerUtils().createFeature(self._layers[self.EDITING_LAYER_NAME], polygon)
            features.append(feature)

        if features:
            if not self._layers[self.EDITING_LAYER_NAME].isEditable():
                self._layers[self.EDITING_LAYER_NAME].startEditing()

            self._layers[self.EDITING_LAYER_NAME].addFeatures(features)
            self.iface.mapCanvas().refresh()

            message = QCoreApplication.translate("QGISUtils", "{} new plot(s) has(have) been created! To finish the creation of the plots, open its attribute table and fill in the mandatory fields.").format(len(features))
            button_text = QCoreApplication.translate("QGISUtils", "Open table of attributes")
            level = Qgis.Info
            layer = self._layers[self.EDITING_LAYER_NAME]
            filter = '"{}" is Null'.format(self.names.OP_PLOT_T_PLOT_AREA_F)
            self.logger.message_with_button_open_table_attributes_emitted.emit(message, button_text, level, layer, filter)
            self.close_wizard(show_message=False)
        else:
            message = QCoreApplication.translate("QGISUtils", "No plot could be created. Make sure selected boundaries are closed!")
            self.close_wizard(message)
