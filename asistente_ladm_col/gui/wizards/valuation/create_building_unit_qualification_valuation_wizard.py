# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-11-23
        git sha              : :%H$
        copyright            : (C) 2018 by Jhon Galindo
        email                : jhonsigpjc@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import (QCoreApplication,
                              QSettings)
from qgis.PyQt.QtWidgets import QWizard
from qgis.core import (QgsApplication,
                       Qgis,
                       QgsMapLayerProxyModel)

from ....config.general_config import (PLUGIN_NAME,
                                       LAYER)
from ....config.help_strings import HelpStrings
from ....config.table_mapping_config import (ID_FIELD,
                                             VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE,
                                             VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE)
from ....utils import get_ui_class
from ....utils.qt_utils import enable_next_wizard

WIZARD_UI = get_ui_class('wizards/valuation/wiz_create_building_unit_qualification_valuation.ui')


class CreateBuildingUnitQualificationValuationWizard(QWizard, WIZARD_UI):
    WIZARD_NAME = "CreateBuildingUnitQualificationValuationWizard"
    WIZARD_TOOL_NAME = QCoreApplication.translate(WIZARD_NAME, "Create building unit qualification")

    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()

        self._layers = {
            VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE: {'name': VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE, 'geometry': None, LAYER: None},
            VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE: {'name': VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE, 'geometry': None, LAYER: None}
        }

        # Auxiliary data to set nonlinear next pages
        self.pages = [self.wizardPage1, self.wizardPage2]
        self.dict_pages_ids = {self.pages[idx]: pid for idx, pid in enumerate(self.pageIds())}
        self.restore_settings()
        self.rad_create_manually.toggled.connect(self.adjust_page_2_controls)
        self.rad_conventional.toggled.connect(self.building_unit_qualification_option_changed)

        self.building_unit_qualification_option_changed()  # Initialize it
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.currentIdChanged.connect(self.current_page_changed)
        self.rejected.connect(self.close_wizard)
        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.NoGeometry)

        self.txt_help_page_2.setHtml(self.help_strings.WIZ_ADD_POINTS_CADASTRE_PAGE_2_OPTION_CSV)
        self.wizardPage2.setButtonText(QWizard.FinishButton, QCoreApplication.translate(self.WIZARD_NAME, "Import"))
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)

    def nextId(self):
        """
        Set navigation order. Should return an integer. -1 is Finish.
        """
        if self.currentId() == self.dict_pages_ids[self.wizardPage1]:
            return self.dict_pages_ids[self.wizardPage2]
        elif self.currentId() == self.dict_pages_ids[self.wizardPage2]:
            return -1

    def current_page_changed(self, id):
        """
        Reset the Next button. Needed because Next might have been disabled by a
        condition in a another SLOT.
        """
        enable_next_wizard(self)

        if id == self.dict_pages_ids[self.wizardPage2]:
            self.adjust_page_2_controls()
            self.set_buttons_visible(True)
            self.set_buttons_enabled(True)

    def set_buttons_visible(self, visible):
        self.button(self.BackButton).setVisible(visible)
        self.button(self.FinishButton).setVisible(visible)
        self.button(self.CancelButton).setVisible(visible)

    def set_buttons_enabled(self, enabled):
        self.wizardPage2.setEnabled(enabled)
        self.button(self.BackButton).setEnabled(enabled)
        self.button(self.FinishButton).setEnabled(enabled)
        self.button(self.CancelButton).setEnabled(enabled)

    def adjust_page_2_controls(self):
        self.cbo_mapping.clear()
        self.cbo_mapping.addItem("")
        self.cbo_mapping.addItems(self.qgis_utils.get_field_mappings_file_names(self.current_building_unit_qualification_valuation_name()))

        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            self.lbl_field_mapping.setEnabled(True)
            self.cbo_mapping.setEnabled(True)
            finish_button_text = QCoreApplication.translate("create_building_unit_qualification_valuation_wizard", "Import")
            self.txt_help_page_2.setHtml(self.help_strings.get_refactor_help_string(self.current_building_unit_qualification_valuation_name(), False))
        elif self.rad_create_manually.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            finish_button_text = QCoreApplication.translate("create_building_unit_qualification_valuation_wizard", "Create")

            output_layer_name = self.current_building_unit_qualification_valuation_name()
            if output_layer_name == "calificacion_convencional":
                self.txt_help_page_2.setHtml(self.help_strings.WIZ_USING_FORM_BUILDING_UNIT_QUALIFICATION_PAGE_2_OPTION)
            else:
                self.txt_help_page_2.setHtml(self.help_strings.WIZ_USING_FORM_BUILDING_UNIT_NO_QUALIFICATION_PAGE_2_OPTION)

        self.wizardPage1.setButtonText(QWizard.FinishButton, finish_button_text)

    def building_unit_qualification_option_changed(self):
        if self.rad_conventional.isChecked():
            self.gbx_page_2.setTitle(QCoreApplication.translate(self.WIZARD_NAME,
                                                                "Load data to conventional building unit qualification..."))
            self.txt_help_page_1.setHtml(
                self.help_strings.WIZ_CREATE_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_VALUATION_PAGE_1_OPTION_FORM)
        elif self.rad_unconventional.isChecked():
            self.gbx_page_2.setTitle(QCoreApplication.translate(self.WIZARD_NAME,
                                                                "Load data to unconventional building unit qualification..."))
            self.txt_help_page_1.setHtml(
                self.help_strings.WIZ_CREATE_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_VALUATION_PAGE_1_OPTION_FORM)

    def finished_dialog(self):
        self.save_settings()
        output_layer_name = self.current_building_unit_qualification_valuation_name()

        if self.rad_refactor.isChecked():
            if self.mMapLayerComboBox.currentLayer() is not None:
                field_mapping = self.cbo_mapping.currentText()
                res_etl_model = self.qgis_utils.show_etl_model(self._db,
                                                               self.mMapLayerComboBox.currentLayer(),
                                                               output_layer_name,
                                                               field_mapping=field_mapping)

                if res_etl_model:
                    if field_mapping:
                        self.qgis_utils.delete_old_field_mapping(field_mapping)

                    self.qgis_utils.save_field_mapping(output_layer_name)


            else:
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("create_building_unit_qualification_valuation_wizard",
                                               "Select a source layer to set the field mapping to '{}'.").format(self.current_building_unit_qualification_valuation_name()),
                    Qgis.Warning)

        elif self.rad_create_manually.isChecked():
            self.prepare_feature_creation()

    def current_building_unit_qualification_valuation_name(self):
        if self.rad_conventional.isChecked():
            return VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE
        else:
            return VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE

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

        # All layers were successfully loaded
        return True

    def required_layers_are_available(self):
        # Load layers
        res_layers = self.qgis_utils.get_layers(self._db, self._layers, load=True)
        if res_layers is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate(self.WIZARD_NAME,
                                                                           "'{}' tool has been closed because there was a problem loading the requeries layers.").format(
                                                    self.WIZARD_TOOL_NAME),
                                                Qgis.Warning)
            return False

        # Check if layers any layer is in editing mode
        layers_name = list()
        for layer in self._layers:
            if self._layers[layer]['layer'].isEditable():
                layers_name.append(self._layers[layer]['layer'].name())

        if layers_name:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                QCoreApplication.translate(self.WIZARD_NAME,
                                                                           "Wizard cannot be opened until the following layers are not in edit mode '{}'.").format(
                                                    '; '.join([layer_name for layer_name in layers_name])),
                                                Qgis.Warning)
            return False

        return True

    def close_wizard(self, message=None, show_message=True):
        if message is None:
            message = QCoreApplication.translate(self.WIZARD_NAME, "'{}' tool has been closed.").format(self.WIZARD_TOOL_NAME)
        if show_message:
            self.iface.messageBar().pushMessage("Asistente LADM_COL", message, Qgis.Info)
        self.disconnect_signals()
        self.close()

    def disconnect_signals(self):
        # QGIS APP
        try:
            self._layers[self.current_building_unit_qualification_valuation_name()][LAYER].committedFeaturesAdded.disconnect(self.finish_feature_creation)
        except:
            pass

    def edit_feature(self):
        self.iface.layerTreeView().setCurrentLayer(self._layers[self.current_building_unit_qualification_valuation_name()][LAYER])
        self._layers[self.current_building_unit_qualification_valuation_name()][LAYER].committedFeaturesAdded.connect(self.finish_feature_creation)
        self.open_form(self._layers[self.current_building_unit_qualification_valuation_name()][LAYER])

    def finish_feature_creation(self, layerId, features):
        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because an error occurred while trying to save the data.").format(self.WIZARD_TOOL_NAME)
        fid = features[0].id()

        if not self._layers[self.current_building_unit_qualification_valuation_name()][LAYER].getFeature(fid).isValid():
            message = QCoreApplication.translate(self.WIZARD_NAME,
                                                 "'{}' tool has been closed. Feature not found in layer {}... It's not posible create a boundary. ").format(self.WIZARD_TOOL_NAME, self.current_building_unit_qualification_valuation_name())
            self.log.logMessage("Feature not found in layer {} ...".format(self.current_building_unit_qualification_valuation_name()), PLUGIN_NAME, Qgis.Warning)
        else:
            feature_tid = self._layers[self.current_building_unit_qualification_valuation_name()][LAYER].getFeature(fid)[ID_FIELD]
            message = QCoreApplication.translate(self.WIZARD_NAME,
                                                 "The new building unit qualification (t_id={}) was successfully created ").format(feature_tid)

        self._layers[self.current_building_unit_qualification_valuation_name()][LAYER].committedFeaturesAdded.disconnect(self.finish_feature_creation)
        self.log.logMessage("Building unit qualification's committedFeaturesAdded SIGNAL disconnected", PLUGIN_NAME, Qgis.Info)
        self.close_wizard(message)

    def open_form(self, layer):
        if not layer.isEditable():
            layer.startEditing()

        self.exec_form(layer)

    def exec_form(self, layer):
        feature = self.qgis_utils.get_new_feature(layer)
        dialog = self.iface.getFeatureForm(layer, feature)
        dialog.rejected.connect(self.form_rejected)
        dialog.setModal(True)

        if dialog.exec_():
            saved = layer.commitChanges()

            if not saved:
                layer.rollBack()
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                                                    QCoreApplication.translate(self.WIZARD_NAME,
                                                                               "Error while saving changes. Party could not be created."),
                                                    Qgis.Warning)

                for e in layer.commitErrors():
                    self.log.logMessage("Commit error: {}".format(e), PLUGIN_NAME, Qgis.Warning)

            self.iface.mapCanvas().refresh()
        else:
            layer.rollBack()

    def form_rejected(self):
        message = QCoreApplication.translate(self.WIZARD_NAME,
                                             "'{}' tool has been closed because you just closed the form.").format(self.WIZARD_TOOL_NAME)
        self.close_wizard(message)

    def save_settings(self):
        settings = QSettings()
        settings.setValue('Asistente-LADM_COL/wizards/building_unit_qualification_load_data_type',
                          'create_manually' if self.rad_create_manually.isChecked() else 'refactor')
        settings.setValue('Asistente-LADM_COL/wizards/building_unit_qualification_load_convention_type',
                          'conventional' if self.rad_conventional.isChecked() else 'unconventional')

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value('Asistente-LADM_COL/wizards/'
                                        'building_unit_qualification_load_data_type') or 'create_manually'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_create_manually.setChecked(True)

        load_convention_type = settings.value('Asistente-LADM_COL/wizards/'
                                              'building_unit_qualification_load_convention_type') or 'conventional'
        if load_convention_type == 'conventional':
            self.rad_conventional.setChecked(True)
        else:
            self.rad_unconventional.setChecked(True)

    def show_help(self):
        if self.current_building_unit_qualification_valuation_name() == VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE:
            self.qgis_utils.show_help("create_building_unit_qualification_valuation_conventional")
        else:
            self.qgis_utils.show_help("create_building_unit_qualification_valuation_unconventional")
