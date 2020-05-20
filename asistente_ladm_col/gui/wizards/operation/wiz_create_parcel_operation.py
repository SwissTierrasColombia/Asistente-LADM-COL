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
        email                : gcarrillo@linuxmail.org
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
from qgis.core import QgsVectorLayerUtils

from asistente_ladm_col.config.layer_config import LayerConfig
from asistente_ladm_col.config.general_config import (CSS_COLOR_OKAY_LABEL,
                                                      CSS_COLOR_ERROR_LABEL,
                                                      CSS_COLOR_INACTIVE_LABEL,
                                                      WIZARD_HELP_PAGES,
                                                      WIZARD_QSETTINGS,
                                                      WIZARD_QSETTINGS_LOAD_DATA_TYPE,
                                                      WIZARD_QSETTINGS_TYPE_PARCEL_SELECTED,
                                                      WIZARD_HELP2)
from asistente_ladm_col.gui.wizards.multi_page_wizard_factory import MultiPageWizardFactory
from asistente_ladm_col.gui.wizards.select_features_by_expression_dialog_wrapper import SelectFeatureByExpressionDialogWrapper
from asistente_ladm_col.gui.wizards.select_features_on_map_wrapper import SelectFeaturesOnMapWrapper


class CreateParcelOperationWizard(MultiPageWizardFactory,
                                 SelectFeatureByExpressionDialogWrapper,
                                 SelectFeaturesOnMapWrapper):

    def __init__(self, iface, db, wizard_settings):
        MultiPageWizardFactory.__init__(self, iface, db, wizard_settings)
        SelectFeatureByExpressionDialogWrapper.__init__(self)
        SelectFeaturesOnMapWrapper.__init__(self)
        self._spatial_unit_layers = dict()

    def post_save(self, features):
        constraint_types_of_parcels = LayerConfig.get_constraint_types_of_parcels(self.names)
        message = QCoreApplication.translate("WizardTranslations",
                                             "'{}' tool has been closed because an error occurred while trying to save the data.").format(self.WIZARD_TOOL_NAME)
        if len(features) != 1:
            message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed. We should have got only one {} by we have {}").format(self.WIZARD_TOOL_NAME, self.WIZARD_FEATURE_NAME, len(features))
            self.logger.warning(__name__, "We should have got only one {}, but we have {}".format(self.WIZARD_FEATURE_NAME, len(features)))
        else:
            fid = features[0].id()

            if not self._layers[self.EDITING_LAYER_NAME].getFeature(fid).isValid():
                self.logger.warning(__name__, "Feature not found in layer {}...".format(self.EDITING_LAYER_NAME))
            else:
                parcel_id = self._layers[self.EDITING_LAYER_NAME].getFeature(fid)[self.names.T_ID_F]

                plot_ids = list()
                building_ids = list()
                building_unit_ids = list()

                # Apply restriction to the selection
                if self.names.LC_PLOT_T in constraint_types_of_parcels[self.dict_parcel_type[self.cb_parcel_type.currentText()]]:
                    if constraint_types_of_parcels[self.dict_parcel_type[self.cb_parcel_type.currentText()]][self.names.LC_PLOT_T] is not None:
                        plot_ids = [f[self.names.T_ID_F] for f in self._layers[self.names.LC_PLOT_T].selectedFeatures()]
                else:
                    plot_ids = [f[self.names.T_ID_F] for f in self._layers[self.names.LC_PLOT_T].selectedFeatures()]

                if self.names.LC_BUILDING_T in constraint_types_of_parcels[self.dict_parcel_type[self.cb_parcel_type.currentText()]]:
                    if constraint_types_of_parcels[self.dict_parcel_type[self.cb_parcel_type.currentText()]][self.names.LC_BUILDING_T] is not None:
                        building_ids = [f[self.names.T_ID_F] for f in self._layers[self.names.LC_BUILDING_T].selectedFeatures()]
                else:
                    building_ids = [f[self.names.T_ID_F] for f in self._layers[self.names.LC_BUILDING_T].selectedFeatures()]

                if self.names.LC_BUILDING_UNIT_T in constraint_types_of_parcels[self.dict_parcel_type[self.cb_parcel_type.currentText()]]:
                    if constraint_types_of_parcels[self.dict_parcel_type[self.cb_parcel_type.currentText()]][self.names.LC_BUILDING_UNIT_T] is not None:
                        building_unit_ids = [f[self.names.T_ID_F] for f in
                                             self._layers[self.names.LC_BUILDING_UNIT_T].selectedFeatures()]
                else:
                    building_unit_ids = [f[self.names.T_ID_F] for f in
                                         self._layers[self.names.LC_BUILDING_UNIT_T].selectedFeatures()]

                # Fill uebaunit table
                new_features = []
                for plot_id in plot_ids:
                    new_feature = QgsVectorLayerUtils().createFeature(self._layers[self.names.COL_UE_BAUNIT_T])
                    new_feature.setAttribute(self.names.COL_UE_BAUNIT_T_LC_PLOT_F, plot_id)
                    new_feature.setAttribute(self.names.COL_UE_BAUNIT_T_PARCEL_F, parcel_id)
                    self.logger.info(__name__, "Saving Plot-Parcel: {}-{}".format(plot_id, parcel_id))
                    new_features.append(new_feature)

                for building_id in building_ids:
                    new_feature = QgsVectorLayerUtils().createFeature(self._layers[self.names.COL_UE_BAUNIT_T])
                    new_feature.setAttribute(self.names.COL_UE_BAUNIT_T_LC_BUILDING_F, building_id)
                    new_feature.setAttribute(self.names.COL_UE_BAUNIT_T_PARCEL_F, parcel_id)
                    self.logger.info(__name__, "Saving Building-Parcel: {}-{}".format(building_id, parcel_id))
                    new_features.append(new_feature)

                for building_unit_id in building_unit_ids:
                    new_feature = QgsVectorLayerUtils().createFeature(self._layers[self.names.COL_UE_BAUNIT_T])
                    new_feature.setAttribute(self.names.COL_UE_BAUNIT_T_LC_BUILDING_UNIT_F, building_unit_id)
                    new_feature.setAttribute(self.names.COL_UE_BAUNIT_T_PARCEL_F, parcel_id)
                    self.logger.info(__name__, "Saving Building Unit-Parcel: {}-{}".format(building_unit_id, parcel_id))
                    new_features.append(new_feature)

                self._layers[self.names.COL_UE_BAUNIT_T].dataProvider().addFeatures(new_features)

                if plot_ids and building_ids and building_unit_ids:
                    message = QCoreApplication.translate("WizardTranslations",
                                                   "The new parcel (t_id={}) was successfully created and associated with its corresponding Plot (t_id={}) and Building(s) (t_id={}) and Building Unit(s) (t_id={})!").format(parcel_id, ", ".join([str(b) for b in plot_ids]), ", ".join([str(b) for b in building_ids]), ", ".join([str(b) for b in building_unit_ids]))
                elif plot_ids and building_ids and not building_unit_ids:
                    message = QCoreApplication.translate("WizardTranslations",
                                                   "The new parcel (t_id={}) was successfully created and associated with its corresponding Plot (t_id={}) and Building(s) (t_id={})!").format(parcel_id, ", ".join([str(b) for b in plot_ids]), ", ".join([str(b) for b in building_ids]))
                elif plot_ids and not building_ids and building_unit_ids:
                    message = QCoreApplication.translate("WizardTranslations",
                                                   "The new parcel (t_id={}) was successfully created and associated with its corresponding Plot (t_id={}) and Building Unit(s) (t_id={})!").format(parcel_id, ", ".join([str(b) for b in plot_ids]), ", ".join([str(b) for b in building_unit_ids]))
                elif plot_ids and not building_ids and not building_unit_ids:
                    message = QCoreApplication.translate("WizardTranslations",
                                                   "The new parcel (t_id={}) was successfully created and associated with its corresponding Plot (t_id={})!").format(parcel_id, ", ".join([str(b) for b in plot_ids]))
                elif not plot_ids and building_ids and not building_unit_ids:
                    message = QCoreApplication.translate("WizardTranslations",
                                                   "The new parcel (t_id={}) was successfully created and associated with its corresponding Building(s) (t_id={})!").format(parcel_id, ", ".join([str(b) for b in building_ids]))
                elif not plot_ids and building_ids and building_unit_ids:
                    message = QCoreApplication.translate("WizardTranslations",
                                                         "The new parcel (t_id={}) was successfully created and associated with its corresponding Building(s) (t_id={}) and Building Unit(s) (t_id={})!").format(parcel_id, ", ".join([str(b) for b in building_ids]), ", ".join([str(b) for b in building_unit_ids]))
                elif not plot_ids and not building_ids and building_unit_ids:
                    message = QCoreApplication.translate("WizardTranslations",
                                                         "The new parcel (t_id={}) was successfully created and associated with its corresponding Building Unit(s) (t_id={})!").format(parcel_id, ", ".join([str(b) for b in building_unit_ids]))
                elif not plot_ids and not building_ids and not building_unit_ids:
                    message = QCoreApplication.translate("WizardTranslations",
                                                         "The new parcel (t_id={}) was successfully created but this one wasn't associated with a spatial unit").format(parcel_id)

        return message

    def exec_form_advanced(self, layer):
        pass

    def check_selected_features(self):
        constraint_types_of_parcels = LayerConfig.get_constraint_types_of_parcels(self.names)
        self.lb_plot.setText(QCoreApplication.translate("WizardTranslations", "<b>Plot(s)</b>: {count} Feature(s) Selected").format(count=self._layers[self.names.LC_PLOT_T].selectedFeatureCount()))
        self.lb_plot.setStyleSheet(CSS_COLOR_OKAY_LABEL)  # Default color
        self.lb_building.setText(QCoreApplication.translate("WizardTranslations","<b>Building(s)</b>: {count} Feature(s) Selected").format(count=self._layers[self.names.LC_BUILDING_T].selectedFeatureCount()))
        self.lb_building.setStyleSheet(CSS_COLOR_OKAY_LABEL)  # Default color
        self.lb_building_unit.setText(QCoreApplication.translate("WizardTranslations","<b>Building unit(s)</b>: {count} Feature(s) Selected").format(count=self._layers[self.names.LC_BUILDING_UNIT_T].selectedFeatureCount()))
        self.lb_building_unit.setStyleSheet(CSS_COLOR_OKAY_LABEL)  # Default color

        parcel_type = self.dict_parcel_type[self.cb_parcel_type.currentText()]
        for spatial_unit in constraint_types_of_parcels[parcel_type]:
            _layer = self._spatial_unit_layers[spatial_unit]

            _color = CSS_COLOR_OKAY_LABEL

            if constraint_types_of_parcels[parcel_type][spatial_unit] == 1 and not _layer.selectedFeatureCount() == 1:
                _color = CSS_COLOR_ERROR_LABEL
            elif constraint_types_of_parcels[parcel_type][spatial_unit] == '+' and _layer.selectedFeatureCount() < 1:
                _color = CSS_COLOR_ERROR_LABEL
            elif constraint_types_of_parcels[parcel_type][spatial_unit] is None:
                _color = CSS_COLOR_INACTIVE_LABEL

            if spatial_unit == self.names.LC_PLOT_T:
                self.lb_plot.setStyleSheet(_color)
            elif spatial_unit == self.names.LC_BUILDING_T:
                self.lb_building.setStyleSheet(_color)
            elif spatial_unit == self.names.LC_BUILDING_UNIT_T:
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
        self.btn_plot_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[self.names.LC_PLOT_T]))
        self.btn_building_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[self.names.LC_BUILDING_T]))
        self.btn_building_unit_expression.clicked.connect(partial(self.select_features_by_expression, self._layers[self.names.LC_BUILDING_UNIT_T]))

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
        self.btn_plot_map.clicked.connect(partial(self.select_features_on_map, self._layers[self.names.LC_PLOT_T]))
        self.btn_building_map.clicked.connect(partial(self.select_features_on_map, self._layers[self.names.LC_BUILDING_T]))
        self.btn_building_unit_map.clicked.connect(partial(self.select_features_on_map, self._layers[self.names.LC_BUILDING_UNIT_T]))

    #############################################################################
    # Override methods
    #############################################################################
    def adjust_page_2_controls(self):
        constraint_types_of_parcels = LayerConfig.get_constraint_types_of_parcels(self.names)
        self.button(self.FinishButton).setDisabled(True)
        self.disconnect_signals()

        # Load layers
        result = self.prepare_feature_creation_layers()
        if result is None:
            self.close_wizard(show_message=False)

        self.dict_parcel_type = dict()
        for feature in self._layers[self.names.LC_CONDITION_PARCEL_TYPE_D].getFeatures():
            self.dict_parcel_type[feature[self.names.DISPLAY_NAME_F]] = feature[self.names.ILICODE_F]

        if self.cb_parcel_type.count() == 0:
            for feature in self._layers[self.names.LC_CONDITION_PARCEL_TYPE_D].getFeatures():
                if feature[self.names.ILICODE_F] in constraint_types_of_parcels:
                    self.cb_parcel_type.addItem(feature[self.names.DISPLAY_NAME_F], feature[self.names.T_ID_F])

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
            self.names.LC_PLOT_T: self._layers[self.names.LC_PLOT_T],
            self.names.LC_BUILDING_T: self._layers[self.names.LC_BUILDING_T],
            self.names.LC_BUILDING_UNIT_T: self._layers[self.names.LC_BUILDING_UNIT_T]
        }

        # All layers were successfully loaded
        return True

    def exec_form(self, layer):
        feature = self.get_feature_exec_form(layer)
        feature[self.names.LC_PARCEL_T_PARCEL_TYPE_F] = self.cb_parcel_type.currentText()

        dialog = self.iface.getFeatureForm(layer, feature)
        dialog.rejected.connect(self.form_rejected)
        dialog.setModal(True)

        if dialog.exec_():
            fid = feature.id()

            # assigns the type of parcel before to creating it
            parcel_condition_field_idx = layer.getFeature(fid).fieldNameIndex(self.names.LC_PARCEL_T_PARCEL_TYPE_F)
            layer.changeAttributeValue(fid, parcel_condition_field_idx, self.cb_parcel_type.itemData(self.cb_parcel_type.currentIndex()))

            saved = layer.commitChanges()

            if not saved:
                layer.rollBack()
                self.logger.warning_msg(__name__, QCoreApplication.translate("WizardTranslations",
                    "Error while saving changes. {} could not be created.").format(self.WIZARD_FEATURE_NAME))
                for e in layer.commitErrors():
                    self.logger.warning(__name__, "Commit error: {}".format(e))
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
        constraint_types_of_parcels = LayerConfig.get_constraint_types_of_parcels(self.names)
        # Activate all push buttons
        self.btn_plot_map.setEnabled(True)
        self.btn_plot_expression.setEnabled(True)
        self.btn_building_map.setEnabled(True)
        self.btn_building_expression.setEnabled(True)
        self.btn_building_unit_map.setEnabled(True)
        self.btn_building_unit_expression.setEnabled(True)

        parcel_type = self.dict_parcel_type[parcel_type]

        # Disable labels/controls depending on parcel_type
        for spatial_unit in constraint_types_of_parcels[parcel_type]:
            if constraint_types_of_parcels[parcel_type][spatial_unit] is None:
                if spatial_unit == self.names.LC_PLOT_T:
                    self.btn_plot_map.setEnabled(False)
                    self.btn_plot_expression.setEnabled(False)
                elif spatial_unit == self.names.LC_BUILDING_T:
                    self.btn_building_map.setEnabled(False)
                    self.btn_building_expression.setEnabled(False)
                elif spatial_unit == self.names.LC_BUILDING_UNIT_T:
                    self.btn_building_unit_map.setEnabled(False)
                    self.btn_building_unit_expression.setEnabled(False)

        self.update_help_message(parcel_type)
        self.check_selected_features()

    def update_help_message(self, parcel_type):
        msg_parcel_type = self.help_strings.get_message_parcel_type(parcel_type)
        msg_parcel_type = msg_parcel_type.replace(parcel_type, self.cb_parcel_type.currentText())

        msg_help = self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP2].format(msg_parcel_type=msg_parcel_type)
        self.txt_help_page_2.setHtml(msg_help)

    def is_constraint_satisfied(self, parcel_type):
        constraint_types_of_parcels = LayerConfig.get_constraint_types_of_parcels(self.names)
        result = True
        for spatial_unit in constraint_types_of_parcels[parcel_type]:
            _layer = self._spatial_unit_layers[spatial_unit]

            if constraint_types_of_parcels[parcel_type][spatial_unit] == 1 and not _layer.selectedFeatureCount() == 1:
                result = False
            elif constraint_types_of_parcels[parcel_type][spatial_unit] == '+' and _layer.selectedFeatureCount() < 1:
                result = False

        return result
