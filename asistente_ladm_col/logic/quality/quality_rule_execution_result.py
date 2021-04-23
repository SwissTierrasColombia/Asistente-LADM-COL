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


class QualityRuleExecutionResult:
    def __init__(self, msg, level, error_layers):
        """
        Stores the result of a single quality rule.

        :param msg: Message describing the obtained result.
        :param level: Indicates whether the rule was successful (Qgis.Success), couldn't be validated (Qgis.Warning),
                      or was not successful (Qgis.Critical).
        :param error_layers: List of QgsVectorLayers. They may be spatial or not and they might be empty if no error is
                             found.
        """
        self.msg = msg
        self.level = level
        self.error_layers = error_layers

        # We add a handy member variable to get the error layer directly. Up to now, only 1 QR returns more than 1
        # layer. Note that error_layers might be empty, if there were errors or the prerequisites for running the
        # quality rule were not met (e.g., an imput layer has no feature to validate the QR).
        self.error_layer = error_layers[0] if error_layers else None
