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
                               (C) 2021 by Yesid Polania (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
                               sergio.ramirez@incige.com
                               naturalmentejorge@gmail.com
                               jhonsigpjc@gmail.com
                               yeesidpol.3@gmail.com
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
from qgis.PyQt.QtWidgets import QWizardPage
from qgis.PyQt.QtCore import (pyqtSignal,
                              QObject)

from asistente_ladm_col.config.general_config import (WIZARD_SEL_SOURCE_TITLE,
                                                      WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY)
from asistente_ladm_col.gui.wizards.view.common.view_enum import EnumLayerCreationMode
from asistente_ladm_col.utils.ui import load_ui


class SelectSource(QObject):
    option_changed = pyqtSignal(EnumLayerCreationMode)
    layer_changed = pyqtSignal(QgsMapLayer)

    def __init__(self, items=None, layer_filters=None, wizard_texts=None):
        QObject.__init__(self)

        self.__qwizard_page = self._init_qwizard_page()

        if items is not None:
            self.set_mapping_items(items)

        if layer_filters is not None:
            self.set_layer_filter(layer_filters)

        if wizard_texts is not None:
            self.__qwizard_page.gbx_page.setTitle(wizard_texts[WIZARD_SEL_SOURCE_TITLE])
            self.__qwizard_page.rad_create_manually.setText(wizard_texts[WIZARD_SEL_SOURCE_ENTERING_DATA_MANUALLY])

    def _init_qwizard_page(self) -> QWizardPage:
        qwizard_page = QWizardPage()
        ui_path = 'wizards/wizard_pages/select_source.ui'
        load_ui(ui_path, qwizard_page)
        return qwizard_page

    def set_description(self, description):
        self.__qwizard_page.gbx_page_1.setTitle(description)

    # TODO immutable
    def set_mapping_items(self, items):
        self.__qwizard_page.cbo_mapping.clear()
        self.__qwizard_page.cbo_mapping.addItem("")
        self.__qwizard_page.cbo_mapping.addItems(items)

    # TODO immutable?
    def set_layer_filter(self, filters):
        self.__qwizard_page.mMapLayerComboBox.setFilters(filters)

    # PROPS
    @property
    def selected_layer(self):
        return self.__qwizard_page.mMapLayerComboBox.currentLayer()

    @property
    def field_mapping(self):
        return self.__qwizard_page.cbo_mapping.currentText()

    @property
    def layer_creation_mode(self):
        result = None

        if self.__qwizard_page.rad_create_manually.isChecked():
            result = EnumLayerCreationMode.MANUALLY
        elif self.__qwizard_page.rad_refactor.isChecked():
            result = EnumLayerCreationMode.REFACTOR

        return result

    @layer_creation_mode.setter
    def layer_creation_mode(self, value: EnumLayerCreationMode):
        if value == EnumLayerCreationMode.REFACTOR:
            self.__qwizard_page.rad_refactor.setChecked(True)
        elif value == EnumLayerCreationMode.MANUALLY:
            self.__qwizard_page.rad_create_manually.setChecked(True)

    def set_help_text(self, text):
        self.__qwizard_page.txt_help_page_1.setHtml(text)

    def connect_signals(self):
        self.__qwizard_page.rad_create_manually.toggled.connect(self._controls_changed)
        self.__qwizard_page.rad_refactor.toggled.connect(self._controls_changed)
        self.__qwizard_page.mMapLayerComboBox.layerChanged.connect(self.layer_changed)

    def disconnect_signals(self):
        self.__qwizard_page.rad_create_manually.toggled.disconnect(self._controls_changed)
        self.__qwizard_page.rad_refactor.toggled.disconnect(self._controls_changed)
        self.__qwizard_page.mMapLayerComboBox.layerChanged.disconnect(self.layer_changed)

    def _controls_changed(self, checked):
        if not checked:
            return

        self.__enable_rad_refactor_controls(self.__qwizard_page.rad_refactor.isChecked())
        self.option_changed.emit(self.layer_creation_mode)

    def __enable_rad_refactor_controls(self, is_enabled):
        self.__qwizard_page.lbl_refactor_source.setEnabled(is_enabled)
        self.__qwizard_page.mMapLayerComboBox.setEnabled(is_enabled)
        self.__qwizard_page.lbl_field_mapping.setEnabled(is_enabled)
        self.__qwizard_page.cbo_mapping.setEnabled(is_enabled)

    def get_wizard_page(self):
        return self.__qwizard_page


class SelectSourceExt(SelectSource):

    def __init__(self, items=None, layer_filters=None, wizard_texts=None):
        super().__init__(items, layer_filters, wizard_texts)
        self.__qwizard_page = self.get_wizard_page()

    def _init_qwizard_page(self) -> QWizardPage:
        qwizard_page = QWizardPage()
        ui_path = 'wizards/wizard_pages/survey/wiz_create_right_of_way_survey.ui'
        load_ui(ui_path, qwizard_page)
        return qwizard_page

    @property
    def layer_creation_mode(self):
        result = super().layer_creation_mode

        if result is None and self.__qwizard_page.rad_digitizing_line.isChecked():
            result = EnumLayerCreationMode.DIGITIZING_LINE

        return result

    @layer_creation_mode.setter
    def layer_creation_mode(self, value: EnumLayerCreationMode):
        if value == EnumLayerCreationMode.DIGITIZING_LINE:
            self.__qwizard_page.rad_digitizing_line.setChecked(True)
        else:
            SelectSource.layer_creation_mode.fset(self, value)

    def connect_signals(self):
        super().connect_signals()
        self.__qwizard_page.rad_digitizing_line.toggled.connect(self._controls_changed)

    def disconnect_signals(self):
        super().disconnect_signals()
        self.__qwizard_page.rad_digitizing_line.toggled.disconnect(self._controls_changed)

    def _controls_changed(self, checked):
        super()._controls_changed(checked)
        self.__enable_digitalizing_line(self.__qwizard_page.rad_digitizing_line.isChecked())

    def __enable_digitalizing_line(self, is_enabled):
        self.__qwizard_page.lbl_width.setEnabled(is_enabled)
        self.__qwizard_page.width_line_edit.setEnabled(is_enabled)

    def get_with_line_edit(self):
        return self.__qwizard_page.width_line_edit.value()
