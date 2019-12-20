# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-09-10
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BFS Swissphoto)
                               (C) 2018 by Sergio Ramírez (Incige SAS)
                               (C) 2018 by Jorge Useche (Incige SAS)
                               (C) 2018 by Jhon Galindo (Incige SAS)
                               (C) 2019 by Leo Cardona (BFS Swissphoto)
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
from qgis.PyQt.QtCore import (QSettings,
                              QCoreApplication)
from qgis.PyQt.QtWidgets import QWizard
from qgis.core import QgsMapLayerProxyModel

from asistente_ladm_col.config.general_config import (LAYER,
                                                      WIZARD_HELP,
                                                      WIZARD_HELP_PAGES,
                                                      WIZARD_QSETTINGS,
                                                      WIZARD_QSETTINGS_LOAD_DATA_TYPE,
                                                      WIZARD_QSETTINGS_LOAD_CONVENTION_TYPE,
                                                      WIZARD_HELP1,
                                                      WIZARD_HELP2,
                                                      WIZARD_HELP3,
                                                      WIZARD_HELP4,
                                                      WIZARD_HELP5,
                                                      WIZARD_MAP_LAYER_PROXY_MODEL)
from ....config.table_mapping_config import (VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE,
                                             VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE)
from ....gui.wizards.single_page_wizard_factory import SinglePageWizardFactory
from ....utils.qt_utils import enable_next_wizard


class CreateBuildingUnitQualificationValuationWizard(SinglePageWizardFactory):
    def __init__(self, iface, db, qgis_utils, wizard_settings):
        SinglePageWizardFactory.__init__(self, iface, db, qgis_utils, wizard_settings)

    #############################################################################
    # Override methods
    #############################################################################
    def init_gui(self):
        # Auxiliary data to set nonlinear next pages
        self.pages = [self.wizardPage1, self.wizardPage2]
        self.dict_pages_ids = {self.pages[idx]: pid for idx, pid in enumerate(self.pageIds())}
        self.restore_settings()
        self.rad_create_manually.toggled.connect(self.adjust_page_1_controls)
        self.rad_conventional.toggled.connect(self.building_unit_qualification_option_changed)

        self.building_unit_qualification_option_changed()  # Initialize it
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)
        self.currentIdChanged.connect(self.current_page_changed)
        self.rejected.connect(self.close_wizard)
        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.Filter(self.wizard_config[WIZARD_MAP_LAYER_PROXY_MODEL]))

        self.txt_help_page_2.setHtml(self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP1])
        self.wizardPage2.setButtonText(QWizard.FinishButton, QCoreApplication.translate("WizardTranslations", "Import"))

    def adjust_page_1_controls(self):
        self.cbo_mapping.clear()
        self.cbo_mapping.addItem("")
        self.cbo_mapping.addItems(self.qgis_utils.get_field_mappings_file_names(self.EDITING_LAYER_NAME))

        if self.rad_refactor.isChecked():
            self.lbl_refactor_source.setEnabled(True)
            self.mMapLayerComboBox.setEnabled(True)
            self.lbl_field_mapping.setEnabled(True)
            self.cbo_mapping.setEnabled(True)
            finish_button_text = QCoreApplication.translate("WizardTranslations", "Import")
            self.txt_help_page_2.setHtml(self.help_strings.get_refactor_help_string(self._db, self._layers[self.EDITING_LAYER_NAME][LAYER]))
        elif self.rad_create_manually.isChecked():
            self.lbl_refactor_source.setEnabled(False)
            self.mMapLayerComboBox.setEnabled(False)
            self.lbl_field_mapping.setEnabled(False)
            self.cbo_mapping.setEnabled(False)
            finish_button_text = QCoreApplication.translate("WizardTranslations", "Create")

            if self.EDITING_LAYER_NAME == VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE:
                self.txt_help_page_2.setHtml(self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP2])
            else:
                self.txt_help_page_2.setHtml(self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP3])

        self.wizardPage1.setButtonText(QWizard.FinishButton, finish_button_text)

    def save_settings(self):
        settings = QSettings()
        settings.setValue(self.wizard_config[WIZARD_QSETTINGS][WIZARD_QSETTINGS_LOAD_DATA_TYPE], 'create_manually' if self.rad_create_manually.isChecked() else 'refactor')
        settings.setValue(self.wizard_config[WIZARD_QSETTINGS][WIZARD_QSETTINGS_LOAD_CONVENTION_TYPE], 'conventional' if self.rad_conventional.isChecked() else 'unconventional')

    def restore_settings(self):
        settings = QSettings()

        load_data_type = settings.value(self.wizard_config[WIZARD_QSETTINGS][WIZARD_QSETTINGS_LOAD_DATA_TYPE]) or 'create_manually'
        if load_data_type == 'refactor':
            self.rad_refactor.setChecked(True)
        else:
            self.rad_create_manually.setChecked(True)

        load_convention_type = settings.value(self.wizard_config[WIZARD_QSETTINGS][WIZARD_QSETTINGS_LOAD_CONVENTION_TYPE]) or 'conventional'
        if load_convention_type == 'conventional':
            self.rad_conventional.setChecked(True)
        else:
            self.rad_unconventional.setChecked(True)

    def show_help(self):
        if self.EDITING_LAYER_NAME == VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE:
            self.qgis_utils.show_help(self.wizard_config[WIZARD_HELP])
        else:
            self.qgis_utils.show_help("create_building_unit_qualification_valuation_unconventional")

    #############################################################################
    # Custom methods
    #############################################################################
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
            self.adjust_page_1_controls()
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

    def building_unit_qualification_option_changed(self):
        if self.rad_conventional.isChecked():
            self.EDITING_LAYER_NAME = VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE
            self.gbx_page_2.setTitle(QCoreApplication.translate("WizardTranslations",
                                                                "Load data to conventional building unit qualification..."))
            self.txt_help_page_1.setHtml(self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP4])

        elif self.rad_unconventional.isChecked():
            self.EDITING_LAYER_NAME = VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE
            self.gbx_page_2.setTitle(QCoreApplication.translate("WizardTranslations",
                                                                "Load data to unconventional building unit qualification..."))
            self.txt_help_page_1.setHtml(self.wizard_config[WIZARD_HELP_PAGES][WIZARD_HELP5])
