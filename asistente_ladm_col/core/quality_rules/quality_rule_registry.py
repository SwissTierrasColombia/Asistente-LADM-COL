"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2021-11-08
        git sha         : :%H$
        copyright       : (C) 2021 by Germán Carrillo (SwissTierras Colombia)
        email           : gcarrillo@linuxmail.org
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.core.quality_rules.abstract_quality_rule import AbstractQualityRule
from asistente_ladm_col.logic.quality_rules.qr_overlapping_boundary_points import QROverlappingBoundaryPoints
from asistente_ladm_col.logic.quality_rules.qr_validate_data_against_model import QRValidateDataAgainstModel
from asistente_ladm_col.utils.singleton import Singleton


class QualityRuleRegistry(metaclass=Singleton):
    """
    Registry of supported quality rules.
    """
    def __init__(self):
        self.logger = Logger()
        self.app = AppInterface()
        self.__quality_rules = dict()  # {quality_rule_key1: QualityRule1, ...}

        # Register default quality rules
        self.register_quality_rule(QRValidateDataAgainstModel())
        self.register_quality_rule(QROverlappingBoundaryPoints())

    def register_quality_rule(self, quality_rule):
        """
        Registers a quality rule.

        :param quality_rule: QualityRule instance.
        :return: True if the quality rule was registered, False otherwise.
        """
        if not isinstance(quality_rule, AbstractQualityRule):
            self.logger.warning(__name__,
                                "The quality rule '{}' is not an 'AbstractQualityRule' instance!".format(quality_rule.id()))
            return False

        if not quality_rule.is_valid():
            self.logger.warning(__name__, "The quality rule '{}' is not valid! Check the quality rule definition!".format(
                quality_rule.id()))
            return False

        if quality_rule.id() in self.__quality_rules:
            self.logger.warning(__name__, "The quality rule '{}' is already registered.".format(quality_rule.id()))
            return False

        self.__quality_rules[quality_rule.id()] = quality_rule
        self.logger.info(__name__, "Quality rule '{}' has been registered!".format(quality_rule.id()))

        return True

    def unregister_quality_rule(self, quality_rule_id):
        """
        Unregisters a quality rule by id.

        :param quality_rule_id: Id of the quality rule to unregister.
        :return: True if the quality rule was unregistered, False otherwise.
        """
        if quality_rule_id not in self.__quality_rules:
            self.logger.error(__name__, "Quality rule '{}' was not found in registered quality rules, therefore, it cannot be unregistered!".format(quality_rule_id))
            return False

        self.__quality_rules[quality_rule_id] = None
        del self.__quality_rules[quality_rule_id]
        self.logger.info(__name__, "Quality rule '{}' has been unregistered!".format(quality_rule_id))

        return True

    def get_quality_rule(self, quality_rule_id):
        qr = self.__quality_rules.get(quality_rule_id, None)
        if not qr:
            self.logger.warning(__name__, "Quality rule '{}' is not registered, therefore it cannot be obtained!".format(quality_rule_id))

        return qr
