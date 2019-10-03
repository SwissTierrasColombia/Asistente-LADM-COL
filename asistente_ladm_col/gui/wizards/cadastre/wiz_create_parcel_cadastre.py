# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-09-10
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BSF Swissphoto)
                               (C) 2018 by Sergio Ramírez (Incige SAS)
                               (C) 2018 by Jorge Useche (Incige SAS)
                               (C) 2018 by Jhon Galindo (Incige SAS)
                               (C) 2019 by Leo Cardona (BSF Swissphoto)
        email                : gcarrillo@linuxmail.com
                               sergio.ramirez@incige.com
                               naturalmentejorge@gmail.com
                               jhonsigpjc@gmail.com
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

from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtCore import QSettings
from qgis.core import (QgsVectorLayerUtils,
                       Qgis)

from asistente_ladm_col.config.general_config import (LAYER,
                                                      WIZARD_HELP_PAGES,
                                                      WIZARD_QSETTINGS,
                                                      WIZARD_QSETTINGS_LOAD_DATA_TYPE,
                                                      WIZARD_QSETTINGS_TYPE_PARCEL_SELECTED,
                                                      WIZARD_HELP2,
                                                      CSS_COLOR_OKAY_LABEL,
                                                      CSS_COLOR_ERROR_LABEL,
                                                      CSS_COLOR_INACTIVE_LABEL,
                                                      PLUGIN_NAME)
from asistente_ladm_col.config.table_mapping_config import (PLOT_TABLE,
                                                            BUILDING_TABLE,
                                                            BUILDING_UNIT_TABLE,
                                                            PARCEL_TYPE_FIELD,
                                                            CONSTRAINT_TYPES_OF_PARCEL,
                                                            UEBAUNIT_TABLE,
                                                            UEBAUNIT_TABLE_PLOT_FIELD,
                                                            UEBAUNIT_TABLE_PARCEL_FIELD,
                                                            UEBAUNIT_TABLE_BUILDING_FIELD,
                                                            UEBAUNIT_TABLE_BUILDING_UNIT_FIELD,
                                                            ID_FIELD)
from asistente_ladm_col.gui.wizards.multi_page_wizard_factory import MultiPageWizardFactory
from asistente_ladm_col.gui.wizards.select_features_by_expression_dialog_wrapper import SelectFeatureByExpressionDialogWrapper
from asistente_ladm_col.gui.wizards.select_features_on_map_wrapper import SelectFeaturesOnMapWrapper


class CreateParcelCadastreWizard(MultiPageWizardFactory,
                                 SelectFeatureByExpressionDialogWrapper,
                                 SelectFeaturesOnMapWrapper):

    def __init__(self, iface, db, qgis_utils, wizard_settings):
        MultiPageWizardFactory.__init__(self, iface, db, qgis_utils, wizard_settings)
        SelectFeatureByExpressionDialogWrapper.__init__(self)
        SelectFeaturesOnMapWrapper.__init__(self)
        self._spatial_unit_layers = dict()
        self.type_of_parcel_selected = None

    def post_save(self, features):
        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because an error occurred while trying to save the data.").format(self.WIZARD_TOOL_NAME)
        if len(features) != 1:
            message = QCoreApplication.translate(self.WIZARD_NAME, "'{}' tool has been closed. We should have got only one {} by we have {}").format(self.WIZARD_TOOL_NAME, self.WIZARD_FEATURE_NAME, len(features))
            self.log.logMessage("We should have got only one {}, but we have {}".format(self.WIZARD_FEATURE_NAME, len(features)), PLUGIN_NAME, Qgis.Warning)
        else:
            fid = features[0].id()

            if not self._layers[self.EDITING_LAYER_NAME][LAYER].getFeature(fid).isValid():
                self.log.logMessage("Feature not found in layer {}...".format(self.EDITING_LAYER_NAME), PLUGIN_NAME, Qgis.Warning)
            else:
                parcel_id = self._layers[self.EDITING_LAYER_NAME][LAYER].getFeature(fid)[ID_FIELD]

                plot_ids = list()
                building_ids = list()
                building_unit_ids = list()

                # Apply restriction to the selection
                if PLOT_TABLE in CONSTRAINT_TYPES_OF_PARCEL[self.cb_parcel_type.currentText()]:
                    if CONSTRAINT_TYPES_OF_PARCEL[self.cb_parcel_type.currentText()][PLOT_TABLE] is not None:
                        plot_ids = [f[ID_FIELD] for f in self._layers[PLOT_TABLE][LAYER].selectedFeatures()]
                else:
                    plot_ids = [f[ID_FIELD] for f in self._layers[PLOT_TABLE][LAYER].selectedFeatures()]

                if BUILDING_TABLE in CONSTRAINT_TYPES_OF_PARCEL[self.cb_parcel_type.currentText()]:
                    if CONSTRAINT_TYPES_OF_PARCEL[self.cb_parcel_type.currentText()][BUILDING_TABLE] is not None:
                        building_ids = [f[ID_FIELD] for f in self._layers[BUILDING_TABLE][LAYER].selectedFeatures()]
                else:
                    building_ids = [f[ID_FIELD] for f in self._layers[BUILDING_TABLE][LAYER].selectedFeatures()]

                if BUILDING_UNIT_TABLE in CONSTRAINT_TYPES_OF_PARCEL[self.cb_parcel_type.currentText()]:
                    if CONSTRAINT_TYPES_OF_PARCEL[self.cb_parcel_type.currentText()][BUILDING_UNIT_TABLE] is not None:
                        building_unit_ids = [f[ID_FIELD] for f in
                                             self._layers[BUILDING_UNIT_TABLE][LAYER].selectedFeatures()]
                else:
                    building_unit_ids = [f[ID_FIELD] for f in
                                         self._layers[BUILDING_UNIT_TABLE][LAYER].selectedFeatures()]

                # Fill uebaunit table
                new_features = []
                for plot_id in plot_ids:
                    new_feature = QgsVectorLayerUtils().createFeature(self._layers[UEBAUNIT_TABLE][LAYER])
                    new_feature.setAttribute(UEBAUNIT_TABLE_PLOT_FIELD, plot_id)
                    new_feature.setAttribute(UEBAUNIT_TABLE_PARCEL_FIELD, parcel_id)
                    self.log.logMessage("Saving Plot-Parcel: {}-{}".format(plot_id, parcel_id), PLUGIN_NAME, Qgis.Info)
                    new_features.append(new_feature)

                for building_id in building_ids:
                    new_feature = QgsVectorLayerUtils().createFeature(self._layers[UEBAUNIT_TABLE][LAYER])
                    new_feature.setAttribute(UEBAUNIT_TABLE_BUILDING_FIELD, building_id)
                    new_feature.setAttribute(UEBAUNIT_TABLE_PARCEL_FIELD, parcel_id)
                    self.log.logMessage("Saving Building-Parcel: {}-{}".format(building_id, parcel_id), PLUGIN_NAME, Qgis.Info)
                    new_features.append(new_feature)

                for building_unit_id in building_unit_ids:
                    new_feature = QgsVectorLayerUtils().createFeature(self._layers[UEBAUNIT_TABLE][LAYER])
                    new_feature.setAttribute(UEBAUNIT_TABLE_BUILDING_UNIT_FIELD, building_unit_id)
                    new_feature.setAttribute(UEBAUNIT_TABLE_PARCEL_FIELD, parcel_id)
                    self.log.logMessage("Saving Building Unit-Parcel: {}-{}".format(building_unit_id, parcel_id), PLUGIN_NAME, Qgis.Info)
                    new_features.append(new_feature)

                self._layers[UEBAUNIT_TABLE][LAYER].dataProvider().addFeatures(new_features)

                if plot_ids and building_ids and building_unit_ids:
                    message = QCoreApplication.translate(self.WIZARD_NAME,
                                                   "The new parcel (t_id={}) was successfully created and associated with its corresponding Plot (t_id={}) and Building(s) (t_id={}) and Building Unit(s) (t_id={})!").format(parcel_id, ", ".join([str(b) for b in plot_ids]), ", ".join([str(b) for b in building_ids]), ", ".join([str(b) for b in building_unit_ids]))
                elif plot_ids and building_ids and not building_unit_ids:
                    message = QCoreApplication.translate(self.WIZARD_NAME,
                                                   "The new parcel (t_id={}) was successfully created and associated with its corresponding Plot (t_id={}) and Building(s) (t_id={})!").format(parcel_id, ", ".join([str(b) for b in plot_ids]), ", ".join([str(b) for b in building_ids]))
                elif plot_ids and not building_ids and building_unit_ids:
                    message = QCoreApplication.translate(self.WIZARD_NAME,
                                                   "The new parcel (t_id={}) was successfully created and associated with its corresponding Plot (t_id={}) and Building Unit(s) (t_id={})!").format(parcel_id, ", ".join([str(b) for b in plot_ids]), ", ".join([str(b) for b in building_unit_ids]))
                elif plot_ids and not building_ids and not building_unit_ids:
                    message = QCoreApplication.translate(self.WIZARD_NAME,
                                                   "The new parcel (t_id={}) was successfully created and associated with its corresponding Plot (t_id={})!").format(parcel_id, ", ".join([str(b) for b in plot_ids]))
                elif not plot_ids and building_ids and not building_unit_ids:
                    message = QCoreApplication.translate(self.WIZARD_NAME,
                                                   "The new parcel (t_id={}) was successfully created and associated with its corresponding Building(s) (t_id={})!").format(parcel_id, ", ".join([str(b) for b in building_ids]))
                elif not plot_ids and building_ids and building_unit_ids:
                    message = QCoreApplication.translate(self.WIZARD_NAME,
                                                         "The new parcel (t_id={}) was successfully created and associated with its corresponding Building(s) (t_id={}) and Building Unit(s) (t_id={})!").format(parcel_id, ", ".join([str(b) for b in building_ids]), ", ".join([str(b) for b in building_unit_ids]))
                elif not plot_ids and not building_ids and building_unit_ids:
                    message = QCoreApplication.translate(self.WIZARD_NAME,
                                                         "The new parcel (t_id={}) was successfully created and associated with its corresponding Building Unit(s) (t_id={})!").format(parcel_id, ", ".join([str(b) for b in building_unit_ids]))
                elif not plot_ids and not building_ids and not building_unit_ids:
                    message = QCoreApplication.translate(self.WIZARD_NAME,
                                                         "The new parcel (t_id={}) was successfully created but this one wasn't associated with a spatial unit").format(parcel_id)

        return message

    def exec_form_advanced(self, layer):
        pass

    def check_selected_features(self):
        self.lb_plot.setText(QCoreApplication.translate(self.WIZARD_NAME, "<b>Plot(s)</b>: {count} Feature(s) Selected").format(count=self._layers[PLOT_TABLE][LAYER].selectedFeatureCount()))
        self.lb_plot.setStyleSheet(CSS_COLOR_OKAY_LABEL)  # Default color
        self.lb_building.setText(QCoreApplication.translate(self.WIZARD_NAME,"<b>Building(s)</b>: {count} Feature(s) Selected").format(count=self._layers[BUILDING_TABLE][LAYER].selectedFeatureCount()))
        self.lb_building.setStyleSheet(CSS_COLOR_OKAY_LABEL)  # Default color
        self.lb_building_unit.setText(QCoreApplication.translate(self.WIZARD_NAME,"<b>Building unit(s)</b>: {count} Feature(s) Selected").format(count=self._layers[BUILDING_UNIT_TABLE][LAYER].selectedFeatureCount()))
        self.lb_building_unit.setStyleSheet(CSS_COLOR_OKAY_LABEL)  # Default color

        parcel_type = self.cb_parcel_type.currentText()
        for spatial_unit in CONSTRAINT_TYPES_OF_PARCEL[parcel_type]:
            _layer = self._spatial_unit_layers[spatial_unit]

            _color = CSS_COLOR_OKAY_LABEL

            if CONSTRAINT_TYPES_OF_PARCEL[parcel_type][spatial_unit] == 1 and not _layer.selectedFeatureCount() == 1:
                    _color = CSS_COLOR_ERROR_LABEL
            elif CONSTRAINT_TYPES_OF_PARCEL[parcel_type][spatial_unit] == '+' and _layer.selectedFeatureCount() < 1:
                    _color = CSS_COLOR_ERROR_LABEL
            elif CONSTRAINT_TYPES_OF_PARCEL[parcel_type][spatial_unit] == None:
                _color = CSS_COLOR_INACTIVE_LABEL

            if spatial_unit == PLOT_TABLE:
                self.lb_plot.setStyleSheet(_color)
            elif spatial_unit == BUILDING_TABLE:
                self.lb_building.setStyleSheet(_color)
            elif spatial_unit == BUILDING_UNIT_TABLE:
                self.lb_building_unit.setStyleSheet(_color)

        self.button(self.FinishButton).setEnabled(self.is_constraint_satisfied(parcel_type))

    def disconnect_signals_select_features_by_expression(self):
        signals = [self.btn_plot_expression.clicked,
                   self.btn_building_expression.clicked,
                   self.btn_building_unit_expression.clicked,
                   self.cb_parcel_type.currentTextChanged]

        for signal in signals:
            try:
                signal.disconnect()
            except:
                pass

    def register_select_features_by_expression(self):
        self.btn_plot_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[PLOT_TABLE][LAYER]))
        self.btn_building_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[BUILDING_TABLE][LAYER]))
        self.btn_building_unit_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[BUILDING_UNIT_TABLE][LAYER]))

    def disconnect_signals_controls_select_features_on_map(self):
        signals = [self.btn_plot_map.clicked,
                   self.btn_building_map.clicked,
                   self.btn_building_unit_map.clicked]

        for signal in signals:
            try:
                signal.disconnect()
            except:
                pass

    def register_select_feature_on_map(self):
        self.btn_plot_map.clicked.connect(partial(self.select_features_on_map, self._layers[PLOT_TABLE][LAYER]))
        self.btn_building_map.clicked.connect(partial(self.select_features_on_map, self._layers[BUILDING_TABLE][LAYER]))
        self.btn_building_unit_map.clicked.connect(partial(self.select_features_on_map, self._layers[BUILDING_UNIT_TABLE][LAYER]))

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

        if self.cb_parcel_type.count() == 0:
            for parcel_type in CONSTRAINT_TYPES_OF_PARCEL:
                self.cb_parcel_type.addItem(parcel_type)

            # Select previous option saved
            if self.type_of_parcel_selected:
                index = self.cb_parcel_type.findText(self.type_of_parcel_selected)
                if index != -1:
                    self.cb_parcel_type.setCurrentIndex(index)

        self.cb_parcel_type.currentTextChanged.connect(self.validate_type_of_parcel)
        self.cb_parcel_type.currentTextChanged.emit(self.cb_parcel_type.currentText())

        # Check if a previous feature is selected
        self.check_selected_features()

        # Register select features by expression
        if isinstance(self, SelectFeatureByExpressionDialogWrapper):
            self.register_select_features_by_expression()

        # Register select features on map
        if isinstance(self, SelectFeaturesOnMapWrapper):
            self.register_select_feature_on_map()

    def prepare_feature_creation_layers(self):
        if isinstance(self, SelectFeaturesOnMapWrapper):
            # Add signal to check if a layer was removed
            self.connect_on_removing_layers()

        self._spatial_unit_layers = {
            PLOT_TABLE: self._layers[PLOT_TABLE][LAYER],
            BUILDING_TABLE: self._layers[BUILDING_TABLE][LAYER],
            BUILDING_UNIT_TABLE: self._layers[BUILDING_UNIT_TABLE][LAYER]
        }

        # All layers were successfully loaded
        return True

    def exec_form(self, layer):
        feature = self.get_feature_exec_form(layer)
        feature[PARCEL_TYPE_FIELD] = self.cb_parcel_type.currentText()

        dialog = self.iface.getFeatureForm(layer, feature)
        dialog.rejected.connect(self.form_rejected)
        dialog.setModal(True)

        if dialog.exec_():
            fid = feature.id()

            # assigns the type of parcel before to creating it
            parcel_type_field_idx = layer.getFeature(fid).fieldNameIndex(PARCEL_TYPE_FIELD)
            layer.changeAttributeValue(fid, parcel_type_field_idx, self.cb_parcel_type.currentText())

            saved = layer.commitChanges()

            if not saved:
                layer.rollBack()
                self.qgis_utils.message_emitted.emit(
                    QCoreApplication.translate(self.WIZARD_NAME,
                                               "Error while saving changes. {} could not be created.").format(self.WIZARD_FEATURE_NAME), Qgis.Warning)
                for e in layer.commitErrors():
                    self.log.logMessage("Commit error: {}".format(e), PLUGIN_NAME, Qgis.Warning)
        else:
            layer.rollBack()
        self.iface.mapCanvas().refresh()

    def save_settings(self):
        settings = QSettings()
        settings.setValue(self.wizard_config[WIZARD_QSETTINGS][WIZARD_QSETTINGS_LOAD_DATA_TYPE], 'create_manually' if self.rad_create_manually.isChecked() else 'refactor')
        settings.setValue(self.wizard_config[WIZARD_QSETTINGS][WIZARD_QSETTINGS_TYPE_PARCEL_SELECTED], self.cb_parcel_type.currentText())

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value(self.wizard_config[WIZARD_QSETTINGS][WIZARD_QSETTINGS_LOAD_DATA_TYPE]) or 'create_manually'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_create_manually.setChecked(True)

        self.type_of_parcel_selected = settings.value(self.wizard_config[WIZARD_QSETTINGS][WIZARD_QSETTINGS_TYPE_PARCEL_SELECTED])

    #############################################################################
    # Custom methods
    #############################################################################

    def validate_type_of_parcel(self, parcel_type):
        # Activate all push buttons
        self.btn_plot_map.setEnabled(True)
        self.btn_plot_expression.setEnabled(True)
        self.btn_building_map.setEnabled(True)
        self.btn_building_expression.setEnabled(True)
        self.btn_building_unit_map.setEnabled(True)
        self.btn_building_unit_expression.setEnabled(True)

        # Disable labels/controls depending on parcel_type
        for spatial_unit in CONSTRAINT_TYPES_OF_PARCEL[parcel_type]:
            if CONSTRAINT_TYPES_OF_PARCEL[parcel_type][spatial_unit] == None:
                if spatial_unit == PLOT_TABLE:
                    self.btn_plot_map.setEnabled(False)
                    self.btn_plot_expression.setEnabled(False)
                elif spatial_unit == BUILDING_TABLE:
                    self.btn_building_map.setEnabled(False)
                    self.btn_building_expression.setEnabled(False)
                elif spatial_unit == BUILDING_UNIT_TABLE:
                    self.btn_building_unit_map.setEnabled(False)
                    self.btn_building_unit_expression.setEnabled(False)

        self.update_help_message(parcel_type)
        self.check_selected_features()

    def update_help_message(self, parcel_type):
        msg_parcel_type = self.help_strings.MESSAGE_PARCEL_TYPES[parcel_type]
        msg_help = self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP2].format(msg_parcel_type=msg_parcel_type)
        self.txt_help_page_2.setHtml(msg_help)

    def is_constraint_satisfied(self, type):
        result = True
        for spatial_unit in CONSTRAINT_TYPES_OF_PARCEL[type]:
            _layer = self._spatial_unit_layers[spatial_unit]

            if CONSTRAINT_TYPES_OF_PARCEL[type][spatial_unit] == 1 and not _layer.selectedFeatureCount() == 1:
                result = False
            elif CONSTRAINT_TYPES_OF_PARCEL[type][spatial_unit] == '+' and _layer.selectedFeatureCount() < 1:
                result = False

        return result
