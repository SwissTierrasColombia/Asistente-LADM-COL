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

from asistente_ladm_col.gui.gui_builder.role_registry import RoleRegistry
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

        self.role_registry = RoleRegistry()

        self._initialize_quality_rule_manager()

    def _initialize_quality_rule_manager(self):
        for group_k, group_v in self.__quality_rules_data.items():
            self._quality_rule_groups[group_k] = group_v[QUALITY_GROUP_NAME]

            for rule_k, rule_v in group_v[QUALITY_RULES].items():
                self.__quality_rules[rule_k] = QualityRule(rule_v)
        self.logger.info(__name__, "{} quality rules registered!".format(len(self.__quality_rules)))

    def get_quality_rule(self, rule_key):
        """
        Returns the QualityRule object corresponding to a rule code.

        :param rule_key: rule key
        :return: QualityRule
        """
        return self.__quality_rules.get(rule_key)

    def get_quality_rule_name(self, rule_key):
        """
        Returns the QualityRule name corresponding to a rule code.

        :param rule_key: rule key
        :return: Name of the quality rule (string). None if the QR is not found.
        """
        rule = self.__quality_rules.get(rule_key)
        return rule.rule_name if rule is not None else None

    def get_quality_rule_group_name(self, group_key):
        """
        Returns a quality rule group name.

        :param group_key: Group key
        :return: Group name if the group key is found. Otherwise, None.
        """
        return self._quality_rule_groups.get(group_key)

    def get_quality_rules_by_group(self, enum_group=None):
        """
        Returns all rules in a given group. If no enum_group is given,
        it returns the whole set of rules classified by group.

        :param enum_group:  EnumQualityRule.Point|Line|Polygon|Logic
        :return: dict of rules
        """
        quality_rules_group = dict()
        role_key = self.role_registry.get_active_role()
        role_quality_rules = self.role_registry.get_role_quality_rules(role_key)

        if enum_group:
            quality_rules_group = {k_rule: v_rule for k_rule, v_rule in self.__quality_rules.items() if k_rule in enum_group and k_rule in role_quality_rules}
        else:
            quality_rules_group[EnumQualityRule.Point] = dict()
            quality_rules_group[EnumQualityRule.Line] = dict()
            quality_rules_group[EnumQualityRule.Polygon] = dict()
            quality_rules_group[EnumQualityRule.Logic] = dict()

            for k_quality_rule, v_quality_rule in self.__quality_rules.items():
                if k_quality_rule in role_quality_rules:
                    if k_quality_rule in EnumQualityRule.Point:
                        quality_rules_group[EnumQualityRule.Point][k_quality_rule] = v_quality_rule
                    elif k_quality_rule in EnumQualityRule.Line:
                        quality_rules_group[EnumQualityRule.Line][k_quality_rule] = v_quality_rule
                    elif k_quality_rule in EnumQualityRule.Polygon:
                        quality_rules_group[EnumQualityRule.Polygon][k_quality_rule] = v_quality_rule
                    elif k_quality_rule in EnumQualityRule.Logic:
                        quality_rules_group[EnumQualityRule.Logic][k_quality_rule] = v_quality_rule

            self.logger.debug(__name__, "Quality Rules for role '{}': {}".format(role_key, ", ".join([str(rqr.value) for rqr in role_quality_rules])))

        return quality_rules_group

    def get_error_message(self, error_code):
        return self.__translated_strings.get(error_code)
