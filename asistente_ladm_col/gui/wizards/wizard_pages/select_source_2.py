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

from qgis.core import QgsMapLayer
from qgis.PyQt.QtWidgets import (QWizard, QWizardPage)
from qgis.PyQt.QtCore import pyqtSignal

from asistente_ladm_col.config.general_config import WIZARD_SEL_SOURCE_TITLE, WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY
from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('wizards/wizard_pages/survey/wiz_create_right_of_way_survey.ui')


class SelectSource2(QWizardPage, WIDGET_UI):
    option_changed = pyqtSignal()
    layer_changed = pyqtSignal(QgsMapLayer)

    def __init__(self, items, layer_filters, wizard_texts):
        QWizardPage.__init__(self)
        self.setupUi(self)

        # TODO should this code be in its own method?
        self.rad_create_manually.toggled.connect(self.controls_changed)
        self.mMapLayerComboBox.layerChanged.connect(self.layer_changed)

        if items is not None:
            self.set_mapping_items(items)

        if layer_filters is not None:
            self.set_layer_filter(layer_filters)

        if wizard_texts is not None:
            self.gbx_page.setTitle(wizard_texts[WIZARD_SEL_SOURCE_TITLE])
            self.rad_create_manually.setText(wizard_texts[WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY])

    def set_description(self, description):
        self.gbx_page_1.setTitle(description)

    def controls_changed(self):
        if self.rad_refactor.isChecked():
            self.__enable_digitalizing_line(False)
            self.__enable_rad_refactor_controls(True)
        elif self.rad_create_manually.isChecked():
            self.__enable_digitalizing_line(False)
            self.__enable_rad_refactor_controls(False)
        elif self.rad_digitizing_line.isChecked():
            self.__enable_digitalizing_line(True)
            self.__enable_rad_refactor_controls(False)

        self.option_changed.emit()

    def __enable_rad_refactor_controls(self, is_enabled):
        self.lbl_refactor_source.setEnabled(is_enabled)
        self.mMapLayerComboBox.setEnabled(is_enabled)
        self.lbl_field_mapping.setEnabled(is_enabled)
        self.cbo_mapping.setEnabled(is_enabled)

    def __enable_digitalizing_line(self, is_enabled):
        self.lbl_width.setEnabled(is_enabled)
        self.width_line_edit.setEnabled(is_enabled)

    # TODO immutable
    def set_mapping_items(self, items):
        self.cbo_mapping.clear()
        self.cbo_mapping.addItem("")
        self.cbo_mapping.addItems(items)

    # TODO immutable?
    def set_layer_filter(self, filters):
        self.mMapLayerComboBox.setFilters(filters)

    # PROPS
    @property
    def selected_layer(self):
        return self.mMapLayerComboBox.currentLayer()

    @property
    def field_mapping(self):
        return self.cbo_mapping.currentText()

    @property
    def enabled_refactor(self):
        return self.rad_refactor.isChecked()

    @enabled_refactor.setter
    def enabled_refactor(self, value):
        self.rad_refactor.setChecked(value)

    @property
    def enabled_create_manually(self):
        return self.rad_create_manually.isChecked()

    @enabled_create_manually.setter
    def enabled_create_manually(self, value):
        self.rad_create_manually.setChecked(value)

    def set_help_text(self, text):
        self.txt_help_page_1.setHtml(text)

    @property
    def enabled_digitalizing_line(self):
        return self.rad_digitizing_line.isChecked()

    @enabled_digitalizing_line.setter
    def enabled_digitalizing_line(self, value):
        self.rad_digitizing_line.setChecked(value)
