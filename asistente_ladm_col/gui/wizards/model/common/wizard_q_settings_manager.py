# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2021-05-21
        git sha              : :%H$
        copyright            : (C) 2021 by Yesid Polanía (BFS Swissphoto)
        email                : yesidpol.3@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
 """
from qgis.PyQt.QtCore import QSettings

from asistente_ladm_col.gui.wizards.view.common.view_enum import EnumLayerCreationMode


class WizardQSettingsManager:

    def __init__(self, q_settings_key: str):
        self.__q_settings_key = q_settings_key

    def get_settings(self) -> EnumLayerCreationMode:
        settings = QSettings()
        result = None
        load_data_type = settings.value(self.__q_settings_key) or 'create_manually'

        if load_data_type == 'refactor':
            result = EnumLayerCreationMode.REFACTOR
        elif load_data_type == 'create_manually':
            result = EnumLayerCreationMode.MANUALLY
        elif load_data_type == 'digitizing_line':
            result = EnumLayerCreationMode.DIGITIZING_LINE

        return result

    def save_settings(self, value: EnumLayerCreationMode):
        settings = QSettings()
        setting_value = None

        if value == EnumLayerCreationMode.REFACTOR:
            setting_value = 'refactor'
        elif value == EnumLayerCreationMode.MANUALLY:
            setting_value = 'create_manually'
        elif value == EnumLayerCreationMode.DIGITIZING_LINE:
            setting_value = 'digitizing_line'

        settings.setValue(self.__q_settings_key, setting_value)
