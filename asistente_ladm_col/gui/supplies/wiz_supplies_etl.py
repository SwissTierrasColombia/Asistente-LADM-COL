# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-03-18
        git sha              : :%H$
        copyright            : (C) 2020 by Germán Carrillo (BSF Swissphoto)
                               (C) 2020 by Jhon Galindo (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
                               jhonsigpjc@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
import os
import stat

from qgis.PyQt.QtCore import (Qt,
                              QSettings,
                              QCoreApplication,
                              QFile)
from qgis.PyQt.QtWidgets import (QWizard,
                                 QFileDialog,
                                 QSizePolicy,
                                 QGridLayout)
from qgis.core import (Qgis,
                       QgsMapLayerProxyModel,
                       QgsCoordinateReferenceSystem,
                       QgsWkbTypes)
from qgis.gui import QgsMessageBar

from asistente_ladm_col.config.general_config import (LAYER,
                                                      DEFAULT_EPSG)
from asistente_ladm_col.config.help_strings import HelpStrings
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.qt_utils import (make_file_selector,
                                               OverrideCursor,
                                               enable_next_wizard,
                                               disable_next_wizard,
                                               normalize_local_url)

WIZARD_UI = get_ui_class('supplies/wiz_supplies_etl.ui')


class SuppliesETLWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils):
        QWizard.__init__(self)
        self.setupUi(self)
        self.iface = iface
        self._db = db
        self.qgis_utils = qgis_utils
        self.logger = Logger()
        self.names = self._db.names
        self.help_strings = HelpStrings()

        self._layers = dict()

        self.wizardPage2.setButtonText(QWizard.CustomButton1,
                                       QCoreApplication.translate("SuppliesETLWizard",
                                                                  "Run"))
        # Auxiliary data to set nonlinear next pages
        self.pages = [self.wizardPage1, self.wizardPage2, self.wizardPage3, self.wizardPage4]
        self.dict_pages_ids = {self.pages[idx] : pid for idx, pid in enumerate(self.pageIds())}

        self.restore_settings()

        # Set connections
        self.rad_snc_data.toggled.connect(self.etl_option_changed)
        self.etl_option_changed() # Initialize it
        self.button(QWizard.CustomButton1).clicked.connect(self.run_button_clicked)
        self.button(QWizard.FinishButton).clicked.connect(self.finished_dialog)
        self.button(QWizard.HelpButton).clicked.connect(self.show_help)
        self.currentIdChanged.connect(self.current_page_changed)

        # Initialize
        self.current_page_changed(1)

        # Set help pages
        #self.txt_help_page_2.setHtml(self.help_strings.WIZ_ADD_POINTS_OPERATION_PAGE_2_OPTION_CSV)
        #self.txt_help_page_3.setHtml(self.help_strings.WIZ_ADD_POINTS_OPERATION_PAGE_3_OPTION_CSV)

        # Set MessageBar for QWizard
        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.setLayout(QGridLayout())
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

    def nextId(self):
        """
        Set navigation order. Should return an integer. -1 is Finish.
        """
        if self.currentId() == self.dict_pages_ids[self.wizardPage1]:
            if self.rad_snc_data.isChecked():
                return self.dict_pages_ids[self.wizardPage3]
            elif self.rad_cobol_data.isChecked():
                return self.dict_pages_ids[self.wizardPage2]
        elif self.currentId() == self.dict_pages_ids[self.wizardPage2]:
            return self.dict_pages_ids[self.wizardPage4]
        elif self.currentId() == self.dict_pages_ids[self.wizardPage3]:
            return self.dict_pages_ids[self.wizardPage4]
        else:
            return -1

    def current_page_changed(self, id):
        """
        Reset the Next button. Needed because Next might have been disabled by a
        condition in a another SLOT.
        """
        #enable_next_wizard(self)
        button_list = [QWizard.HelpButton,
                       QWizard.Stretch,
                       QWizard.BackButton,
                       QWizard.CustomButton1,
                       QWizard.NextButton,
                       QWizard.FinishButton,
                       QWizard.CancelButton]

        if id == self.dict_pages_ids[self.wizardPage1]:
            button_list.remove(QWizard.BackButton)
            button_list.remove(QWizard.CustomButton1)
        elif id == self.dict_pages_ids[self.wizardPage2]:
            button_list.remove(QWizard.NextButton)
            #button_list.remove(QWizard.FinishButton)
            self.button(self.FinishButton).setVisible(False)
        elif id == self.dict_pages_ids[self.wizardPage3]:
            button_list.remove(QWizard.NextButton)
            button_list.remove(QWizard.FinishButton)
        elif id == self.dict_pages_ids[self.wizardPage4]:
            button_list.remove(QWizard.NextButton)
            self.wizardPage4.setFinalPage(True)

        self.setButtonLayout(button_list)

    def set_buttons_visible(self, visible):
        self.button(self.BackButton).setVisible(visible)
        self.button(self.CustomButton1).setVisible(visible)
        self.button(self.FinishButton).setVisible(visible)
        self.button(self.CancelButton).setVisible(visible)

    def set_buttons_enabled(self, enabled):
        self.wizardPage3.setEnabled(enabled)
        self.button(self.CustomButton1).setEnabled(enabled)
        self.button(self.BackButton).setEnabled(enabled)
        self.button(self.FinishButton).setEnabled(enabled)
        self.button(self.CancelButton).setEnabled(enabled)

    def adjust_page_2_controls(self):
        """ If shown, page 2 becomes a final page"""
        disable_next_wizard(self)
        self.wizardPage2.setFinalPage(True)
        #self.txt_help_page_2.setHtml(self.help_strings.get_refactor_help_string(self._db, self._layers[self.current_point_name()][LAYER]))

    def etl_option_changed(self):
        """
        Adjust help, names and titles according to the selected option
        """
        if self.rad_snc_data.isChecked():
            #self.txt_help_page_1.setHtml(self.help_strings.WIZ_ADD_POINTS_OPERATION_PAGE_1_OPTION_BP)
            pass
        elif self.rad_cobol_data.isChecked(): # self.rad_cobol_data is checked
            #self.txt_help_page_1.setHtml(self.help_strings.WIZ_ADD_POINTS_OPERATION_PAGE_1_OPTION_SP)
            pass

    def run_button_clicked(self):
        print("Yes!")
        self.button(self.FinishButton).setVisible(True)

    def finished_dialog(self):
        self.save_settings()

    def reject(self):
        # Overwrite reject to disallow cancelling while running
        self.done(1)

    def show_message(self, message, level):
        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.bar.pushMessage(message, level, 10)

    def save_settings(self):
        settings = QSettings()
        etl_source = "snc"
        if self.rad_snc_data.isChecked():
            etl_source = "snc"
        elif self.rad_cobol_data.isChecked():
            etl_source = "cobol"

        settings.setValue('Asistente-LADM_COL/supplies/etl_source', etl_source)

    def restore_settings(self):
        settings = QSettings()
        etl_source = settings.value('Asistente-LADM_COL/supplies/etl_source') or 'snc'
        if etl_source == 'snc':
            self.rad_snc_data.setChecked(True)
        elif etl_source == 'cobol':
            self.rad_cobol_data.setChecked(True)

    def show_help(self):
        self.qgis_utils.show_help()
