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
        self.__point_quality_rules = dict()
        self.__line_quality_rules = dict()
        self.__polygon_quality_rules = dict()
        self.__logic_quality_rules = dict()
        self.__all_quality_rules = dict()

        self._initialize_quality_rule_manager()

    def _initialize_quality_rule_manager(self):
        self.logger.info(__name__, "Initialize quality rule manager...")
        for group_k, group_v in self.__quality_rules_data.items():
            self._quality_rule_groups[group_k] = group_v[QUALITY_GROUP_NAME]

            for rule_k, rule_v in group_v[QUALITY_RULES].items():
                if group_k == EnumQualityRule.Point:
                    self.__point_quality_rules[rule_k] = QualityRule(rule_v)
                elif group_k == EnumQualityRule.Line:
                    self.__line_quality_rules[rule_k] = QualityRule(rule_v)
                elif group_k == EnumQualityRule.Polygon:
                    self.__polygon_quality_rules[rule_k] = QualityRule(rule_v)
                elif group_k == EnumQualityRule.Logic:
                    self.__logic_quality_rules[rule_k] = QualityRule(rule_v)

        for quality_rules in [self.__point_quality_rules, self.__line_quality_rules, self.__polygon_quality_rules, self.__logic_quality_rules]:
            self.__all_quality_rules.update(quality_rules)
            self.logger.info(__name__, "All quality rules were register...")

    def get_quality_rule(self, rule_code):
        return self.__all_quality_rules.get(rule_code)

    @property
    def quality_rule_groups(self):
        return self._quality_rule_groups

    def get_rules(self, group_code):
        if group_code == EnumQualityRule.Point:
            return self.__get_rules(self.__point_quality_rules)
        elif group_code == EnumQualityRule.Line:
            return self.__get_rules(self.__line_quality_rules)
        elif group_code == EnumQualityRule.Polygon:
            return self.__get_rules(self.__polygon_quality_rules)
        elif group_code == EnumQualityRule.Logic:
            return self.__get_rules(self.__logic_quality_rules)

    @staticmethod
    def __get_rules(quality_rules):
        rules = dict()
        for rule in quality_rules:
            rules[quality_rules[rule].rule_id] = quality_rules[rule].rule_name
        return rules

    def get_error_message(self, error_code):
        return self.__translated_strings.get(error_code)
