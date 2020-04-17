# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-04-02
        git sha              : :%H$
        copyright            : (C) 2020 by Leo Cardona (BSF Swissphoto)
        email                : leo.cardona.p@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
 """
from qgis.PyQt.QtCore import QObject

from asistente_ladm_col.lib.quality_rule.quality_rule import QualityRule
from asistente_ladm_col.config.enums import EnumQualityRule
from asistente_ladm_col.config.quality_rules_config import (QUALITY_GROUP_NAME,
                                                            QUALITY_RULES,
                                                            QualityRuleConfig)
from asistente_ladm_col.config.translation_strings import TranslatableConfigStrings
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.singleton import SingletonQObject


class QualityRuleManager(QObject, metaclass=SingletonQObject):
    def __init__(self):
        self.logger = Logger()
        self.__quality_rules_data = QualityRuleConfig.get_quality_rules_config()
        self.__translated_strings = TranslatableConfigStrings().get_translatable_config_strings()
        self._quality_rule_groups = dict()
        self.__quality_rules = dict()

        self._initialize_quality_rule_manager()

    def _initialize_quality_rule_manager(self):
        self.logger.info(__name__, "Initialize quality rule manager...")
        for group_k, group_v in self.__quality_rules_data.items():
            self._quality_rule_groups[group_k] = group_v[QUALITY_GROUP_NAME]

            for rule_k, rule_v in group_v[QUALITY_RULES].items():
                self.__quality_rules[rule_k] = QualityRule(rule_v)
        self.logger.info(__name__, "All quality rules were register...")

    def get_quality_rule(self, rule_code):
        return self.__quality_rules.get(rule_code)

    @property
    def quality_rule_groups(self):
        return self._quality_rule_groups

    def get_quality_rules_by_group(self, enum_group=None):
        return self.__get_quality_rules_by_group(enum_group)

    def __get_quality_rules_by_group(self, enum_group):
        quality_rules_group = dict()
        if enum_group:
            quality_rules_group = {k_rule: v_rule for k_rule, v_rule in self.__quality_rules.items() if k_rule in enum_group}
        else:
            quality_rules_group[EnumQualityRule.Point] = dict()
            quality_rules_group[EnumQualityRule.Line] = dict()
            quality_rules_group[EnumQualityRule.Polygon] = dict()
            quality_rules_group[EnumQualityRule.Logic] = dict()

            for k_quality_rule, v_quality_rule in self.__quality_rules.items():
                if k_quality_rule in EnumQualityRule.Point:
                    quality_rules_group[EnumQualityRule.Point][k_quality_rule] = v_quality_rule
                elif k_quality_rule in EnumQualityRule.Line:
                    quality_rules_group[EnumQualityRule.Line][k_quality_rule] = v_quality_rule
                elif k_quality_rule in EnumQualityRule.Polygon:
                    quality_rules_group[EnumQualityRule.Polygon][k_quality_rule] = v_quality_rule
                elif k_quality_rule in EnumQualityRule.Logic:
                    quality_rules_group[EnumQualityRule.Logic][k_quality_rule] = v_quality_rule

        return quality_rules_group

    def get_error_message(self, error_code):
        return self.__translated_strings.get(error_code)
