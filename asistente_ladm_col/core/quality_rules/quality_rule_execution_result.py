# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin                : 2021-04-23
        copyright            : (C) 2021 by Germán Carrillo (SwissTierras Colombia)
        email                : gcarrillo@linuxmail.org
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""


class QualityRulesExecutionResult:
    def __init__(self, res_dict):
        """
        Stores the result of executing several quality rules.

        :param res_dict: Dict in the form {rule_key: QualityRuleExecutionResult}
        """
        self.__res_dict = res_dict

    def result(self, rule_key):
        return self.__res_dict.get(rule_key)

    def all_error_layers(self):
        return [layer for qr_res in self.__res_dict.values() for layer in qr_res.error_layers if layer.featureCount()]


class QualityRuleExecutionResult:
    def __init__(self, level, msg):
        """
        Stores the result of a single quality rule.

        :param level: Indicates whether the rule was successful (Qgis.Success), couldn't be validated (Qgis.Warning),
                      or was not successful (Qgis.Critical).
        :param msg: Message describing the obtained result.
        :param error_layers: List of QgsVectorLayers. They may be spatial or not and they might be empty if no error is
                             found.
        """
        self.level = level
        self.msg = msg
