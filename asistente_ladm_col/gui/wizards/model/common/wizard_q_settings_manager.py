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
from enum import Enum
import importlib

from qgis.PyQt.QtCore import QSettings


class WizardQSettingsManager:
    __ENUM_VALUE_INDEX = 0
    __ENUM_MODULE_INDEX = 1
    __ENUM_TYPE_INDEX = 2

    __ENUM_SEPARATOR = ":::"
    __ENUM_PART_COUNT = 3  # enum value, enum module, enum type name

    __PLUGIN_ROOT_PATH = "Asistente-LADM-COL"

    def __init__(self, __q_settings_path_key: str):
        self.__q_settings_path_key = WizardQSettingsManager.__PLUGIN_ROOT_PATH + "/" + __q_settings_path_key

    def get_settings(self) -> dict:
        result = dict()
        settings = QSettings()
        settings.beginGroup(self.__q_settings_path_key)

        keys = settings.childKeys()

        for key in keys:
            q_settings_value = settings.value(key)

            if WizardQSettingsManager.__is_q_settings_value_a_enum(q_settings_value):
                result[key] = self.__get_enum_value(q_settings_value)
            else:
                result[key] = q_settings_value

        return result

    def save_settings(self, values: dict):
        settings = QSettings()
        settings.beginGroup(self.__q_settings_path_key)

        for index in values:
            # is value type a Enum?
            if isinstance(values[index], Enum):
                setting_value = WizardQSettingsManager.__get_enum_value_string(values[index])
            else:
                setting_value = values[index]

            settings.setValue(index, setting_value)

    @staticmethod
    def __is_q_settings_value_a_enum(q_settings_value):
        # is value a string and does it contain the enum separator?
        separator_count = WizardQSettingsManager.__ENUM_PART_COUNT - 1
        return isinstance(q_settings_value, str) and \
            q_settings_value.count(WizardQSettingsManager.__ENUM_SEPARATOR) == separator_count

    @staticmethod
    def __get_enum_value(q_settings_value):
        result = None

        try:
            value_parts = q_settings_value.split(WizardQSettingsManager.__ENUM_SEPARATOR)
            module = importlib.import_module(value_parts[WizardQSettingsManager.__ENUM_MODULE_INDEX])
            class_ = getattr(module, value_parts[WizardQSettingsManager.__ENUM_TYPE_INDEX])
            # enumeration value from string is got from '[]' operator
            result = class_[value_parts[WizardQSettingsManager.__ENUM_VALUE_INDEX]]
        except ModuleNotFoundError as e:
            # TODO is better to launch a specific exception?
            pass

        return result

    @staticmethod
    def __get_enum_value_string(enum_value: Enum):
        value_parts = []
        enum_type = type(enum_value)
        
        # __ENUM_VALUE_INDEX
        value_parts.append(enum_value.name)
        # __ENUM_TYPE_INDEX
        value_parts.append(enum_type.__name__)
        # __ENUM_MODULE_INDEX
        value_parts.append(enum_type.__module__)

        return WizardQSettingsManager.__ENUM_SEPARATOR.join(value_parts)
