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
        return self.__res_dict.get(rule_key, None)

    def all_error_layers(self):
        return [layer for qr_res in self.__res_dict.values() for layer in qr_res.error_layers if layer.featureCount()]


class QualityRuleExecutionResult:
    def __init__(self, level, msg, record_count=0):
        """
        Stores the result of a single quality rule.

        :param level: EnumQualityRuleResult value. Indicates the result of the QR validation.
        :param msg: Message describing the obtained result.
        :param record_count: Number of invalid records generated. Note that this might differ from number of records in
                             the original layer that are invalid; for instance, 2 overlapping points generate only 1
                             record in the error DB.
        """
        self.level = level
        self.msg = msg
        self.record_count = record_count
