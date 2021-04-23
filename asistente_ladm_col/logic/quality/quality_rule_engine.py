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
from asistente_ladm_col.logic.quality.quality_rule_execution_result import QualityRulesExecutionResult
from asistente_ladm_col.logic.quality.quality_rules import QualityRules

from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject,
                              pyqtSignal,
                              QSettings)

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.logic.quality.quality_rule_layer_manager import QualityRuleLayerManager
from asistente_ladm_col.utils.decorators import _log_quality_rule_validations


class QualityRuleEngine(QObject):
    """
    Engine that executes Quality Rules
    """
    def __init__(self, db, rules, tolerance, with_gui=True):
        QObject.__init__(self)
        self.logger = Logger()
        self.app = AppInterface()

        self.__with_gui = with_gui

        self.app.settings.tolerance = tolerance  # Tolerance must be given, we don't want anything implicit about it
        self.__tolerance = self.app.settings.tolerance  # Tolerance input might be altered (e.g., if it comes negative)
        self.__layer_manager = QualityRuleLayerManager(db, rules.keys(), self.__tolerance)
        self.__quality_rules = QualityRules()
        self.quality_rule_logger = QualityRuleLogger(self.__tolerance)

        self.__db = db
        self.__rules = rules
        self.__result_layers = list()

    def initialize(self, db, rules, tolerance, with_gui=True):
        """
        Objects of this class are reusable calling initialize()
        """
        self.__result_layers = list()
        self.__db = db
        self.__rules = rules
        self.__with_gui = with_gui
        self.app.settings.tolerance = tolerance
        self.__tolerance = self.app.settings.tolerance  # Tolerance input might be altered (e.g., if it comes negative)
        self.__layer_manager.initialize(rules.keys(), self.__tolerance)
        self.quality_rule_logger.initialize(self.__tolerance)

    def validate_quality_rules(self):
        res = dict()  # {rule_key: QualityRuleExecutionResult}
        if self.__rules:
            self.quality_rule_logger.set_count_topology_rules(len(self.__rules))
            self.logger.info(__name__,
                             QCoreApplication.translate("QualityRuleEngine",
                                "Validating {} quality rules (tolerance: {}).").format(len(self.__rules), self.__tolerance))

            for rule_key, rule_name in self.__rules.items():
                layers = self.__layer_manager.get_layers(rule_key)
                if layers:
                    res[rule_key] = self.__validate_quality_rule(rule_key, layers, rule_name=rule_name)
                    if self.__with_gui:
                        self.add_error_layers(res[rule_key][2])
                else:
                    self.logger.warning(__name__, QCoreApplication.translate("QualityRuleEngine",
                            "Couldn't execute '{}' quality rule! Required layers are not available. Skipping...").format(rule_name))

            self.quality_rule_logger.generate_log_button()
            self.__layer_manager.clean_temporary_layers()
        else:
            self.logger.warning(__name__, QCoreApplication.translate("QualityRuleEngine", "No rules to validate!"))

        return QualityRulesExecutionResult(res)

    @_log_quality_rule_validations
    def __validate_quality_rule(self, rule_key, layers, rule_name):
        """
        Intermediate function to log quality rule execution.

        :param rule_key: rule key
        :param rule_name: Rule name (needed for the logging decorator)
        :return: An instance of QualityRuleExecutionResult
        """
        return self.__quality_rules.validate_quality_rule(self.__db, rule_key, layers)

    def add_error_layers(self, error_layers):
        for error_layer in error_layers:
            self.app.gui.add_error_layer(None, error_layer)


class QualityRuleLogger(QObject):
    """
    Works with the @_log_quality_rule_validations decorator to log both text
    and time for each quality rule executed.
    """
    show_message_emitted = pyqtSignal(str, int)
    show_button_emitted = pyqtSignal()
    set_initial_progress_emitted = pyqtSignal(str)
    set_final_progress_emitted = pyqtSignal(str)

    def __init__(self, tolerance):
        QObject.__init__(self)
        self.log_text = ""
        self.log_total_time = 0
        self.tolerance = tolerance

    def initialize(self, tolerance):
        """
        Objects of this class are reusable calling initialize()
        """
        self.log_text = ""
        self.log_total_time = 0
        self.tolerance = tolerance

    def set_count_topology_rules(self, count):
        self.show_message_emitted.emit(QCoreApplication.translate("QualityDialog", ""), count)

    def generate_log_button(self):
        self.show_button_emitted.emit()

    def get_log_text(self):
        return self.log_text, self.tolerance, self.log_total_time
