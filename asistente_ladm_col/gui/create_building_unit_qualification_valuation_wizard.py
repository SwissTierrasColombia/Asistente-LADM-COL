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
from qgis.core import (QgsEditFormConfig,
                       Qgis,
                       QgsMapLayerProxyModel)

from ..config.help_strings import HelpStrings
from ..config.table_mapping_config import (VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE,
                                           VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE)
from ..utils import get_ui_class
from ..utils.qt_utils import (make_file_selector,
                              enable_next_wizard,
                              disable_next_wizard)

WIZARD_UI = get_ui_class('wiz_create_building_unit_qualification_valuation.ui')


class CreateBuildingUnitQualificationValuationWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self._building_unit_qualification_valuation = None
        self._selection_building_unit_qualification_valuation = None
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()
        self.valuation_building_unit = None

        self.target_layer = None

        # Auxiliary data to set nonlinear next pages
        self.pages = [self.wizardPage1, self.wizardPage2]
        self.dict_pages_ids = {self.pages[idx]: pid for idx, pid in enumerate(self.pageIds())}

        self.restore_settings()

        self.rad_create_manually.toggled.connect(self.adjust_page_2_controls)
        self.rad_conventional.toggled.connect(self.building_unit_qualification_option_changed)
        self.building_unit_qualification_option_changed()  # Initialize it
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.currentIdChanged.connect(self.current_page_changed)

        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.NoGeometry)

        self.txt_help_page_2.setHtml(self.help_strings.WIZ_ADD_POINTS_CADASTRE_PAGE_2_OPTION_CSV)

        self.wizardPage2.setButtonText(QWizard.FinishButton,
                                       QCoreApplication.translate("CreateBuildingUnitQualificationValuationWizard",
                                                                  "Import"))

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
        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            finish_button_text = QCoreApplication.translate("create_building_unit_qualification_valuation_wizard", "Import")
            self.txt_help_page_2.setHtml(self.help_strings.get_refactor_help_string(self.current_building_unit_qualification_valuation_name(), False))

        elif self.rad_create_manually.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            finish_button_text = QCoreApplication.translate("create_building_unit_qualification_valuation_wizard", "Create")

            output_layer_name = self.current_building_unit_qualification_valuation_name()
            if output_layer_name == "calificacion_convencional":
                self.txt_help_page_2.setHtml(self.help_strings.WIZ_USING_FORM_BUILDING_UNIT_QUALIFICATION_PAGE_2_OPTION)
            else:
                self.txt_help_page_2.setHtml(self.help_strings.WIZ_USING_FORM_BUILDING_UNIT_NO_QUALIFICATION_PAGE_2_OPTION)

        self.wizardPage1.setButtonText(QWizard.FinishButton,
                                       QCoreApplication.translate("create_building_unit_qualification_valuation_wizard",
                                       finish_button_text))

    def building_unit_qualification_option_changed(self):
        if self.rad_conventional.isChecked():
            self.gbx_page_2.setTitle(QCoreApplication.translate("CreateBuildingUnitQualificationValuationWizard",
                                                                "Load data to building unit conventional..."))
            self.txt_help_page_1.setHtml(
                self.help_strings.WIZ_CREATE_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_VALUATION_PAGE_1_OPTION_FORM)
        elif self.rad_unconventional.isChecked():  # self.rad_survey_point is checked1
            self.gbx_page_2.setTitle(QCoreApplication.translate("CreateBuildingUnitQualificationValuationWizard",
                                                                "Load data to building unit unconventional..."))
            self.txt_help_page_1.setHtml(
                self.help_strings.WIZ_CREATE_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_VALUATION_PAGE_1_OPTION_FORM)

    def finished_dialog(self):
        self.save_settings()
        output_layer_name = self.current_building_unit_qualification_valuation_name()

        if self.rad_refactor.isChecked():
            if self.mMapLayerComboBox.currentLayer() is not None:
                self.qgis_utils.show_etl_model(self._db,
                                               self.mMapLayerComboBox.currentLayer(),
                                               output_layer_name)
            else:
                self.iface.messageBar().pushMessage("Asistente LADM_COL",
                    QCoreApplication.translate("create_building_unit_qualification_valuation_wizard",
                                               "Select a source layer to set the field mapping to '{}'.").format(self.valuation_building_unit),
                    Qgis.Warning)

        elif self.rad_create_manually.isChecked():
            self.prepare_building_unit_qualification_valuation_creation()

    def current_building_unit_qualification_valuation_name(self):
        if self.rad_conventional.isChecked():
            return VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE
        else:
            return VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE

    def prepare_building_unit_qualification_valuation_creation(self):
        # Load layers
        self._building_unit_qualification_valuation = self.qgis_utils.get_layer(self._db, self.current_building_unit_qualification_valuation_name(), load=True)
        if self._building_unit_qualification_valuation is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("create_building_unit_qualification_valuation_wizard",
                                           "building unit qualification table couldn't be found... {}").format(self._db.get_description()),
                Qgis.Warning)
            return

        # Don't suppress (i.e., show) feature form
        form_config = self._building_unit_qualification_valuation.editFormConfig()
        form_config.setSuppress(QgsEditFormConfig.SuppressOff)
        self._building_unit_qualification_valuation.setEditFormConfig(form_config)

        self.edit_building_unit_qualification_valuation()

    def edit_building_unit_qualification_valuation(self):
        # Open Form
        self.iface.layerTreeView().setCurrentLayer(self._building_unit_qualification_valuation)
        self._building_unit_qualification_valuation.startEditing()
        self.iface.actionAddFeature().trigger()

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
        self.qgis_utils.show_help("create_building_unit_qualification_valuation")
