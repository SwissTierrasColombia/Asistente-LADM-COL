# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin                : 2020-06-01
        copyright            : (C) 2020 by Germán Carrillo (SwissTierras Colombia)
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
from asistente_ladm_col.logic.quality.quality_rules import QualityRules

from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject,
                              pyqtSignal)

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.logic.quality.quality_rule_layer_manager import QualityRuleLayerManager
from asistente_ladm_col.utils.decorators import _log_quality_rule_validations


class QualityRuleEngine(QObject):
    """
    Engine that executes Quality Rules
    """
    def __init__(self, db, rule_keys):
        QObject.__init__(self)
        self.logger = Logger()
        self.app = AppInterface()

        self.__layer_manager = QualityRuleLayerManager(db, rule_keys)
        self.__quality_rules = QualityRules()
        self.quality_rule_logger = QualityRuleLogger()

        self.__db = db
        self.__rule_keys = rule_keys
        self.__result_layers = list()

    def initialize(self, db, rule_keys):
        """
        Objects of this class are reusable calling initialize()
        """
        self.__result_layers = list()
        self.__db = db
        self.__rule_keys = rule_keys
        self.__layer_manager.initialize(rule_keys)
        self.quality_rule_logger.initialize()

    def validate_quality_rules(self):
        if len(self.__rule_keys):
            self.quality_rule_logger.set_count_topology_rules(len(self.__rule_keys))

            for rule_key in self.__rule_keys:
                layers = self.__layer_manager.get_layers(rule_key)
                self.__validate_quality_rule(rule_key, layers, rule_name="rule_name")

            self.quality_rule_logger.generate_log_button()
            self.__layer_manager.clean_temporary_layers()
        else:
            self.logger.critical(__name__, QCoreApplication.translate("QualityRuleEngine", "No rules to validate!"))

    @_log_quality_rule_validations
    def __validate_quality_rule(self, rule_key, layers, rule_name):
        """
        Intermediate function to log quality rule execution.

        :param rule_key: rule key
        :param rule_name: Rule name (needed for the logging decorator)
        :return: tuple (msg, level), where level indicates whether the rule was successful,
                 couldn't be validated (warning), or was not successful (critical)
        """
        return self.__quality_rules.validate_quality_rule(self.__db, rule_key, layers)


class QualityRuleLogger(QObject):
    """
    Works with the @_log_quality_rule_validations decorator to log both text
    and time for each quality rule executed.
    """
    show_message_emitted = pyqtSignal(str, int)
    show_button_emitted = pyqtSignal()
    set_initial_progress_emitted = pyqtSignal(str)
    set_final_progress_emitted = pyqtSignal(str)

    def __init__(self):
        QObject.__init__(self)
        self.log_text = ""
        self.log_total_time = 0

    def initialize(self):
        """
        Objects of this class are reusable calling initialize()
        """
        self.log_text = ""
        self.log_total_time = 0

    def set_count_topology_rules(self, count):
        self.show_message_emitted.emit(QCoreApplication.translate("QualityDialog", ""), count)

    def generate_log_button(self):
        self.show_button_emitted.emit()

    def get_log_text(self):
        return self.log_text, self.log_total_time
