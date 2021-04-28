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
import time

from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject,
                              pyqtSignal,
                              QSettings)

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.quality_rule.quality_rule_manager import QualityRuleManager
from asistente_ladm_col.logic.quality.quality_rule_layer_manager import QualityRuleLayerManager
from asistente_ladm_col.logic.quality.quality_rule_execution_result import (QualityRulesExecutionResult,
                                                                            QualityRuleExecutionResult)
from asistente_ladm_col.logic.quality.quality_rules import QualityRules
from asistente_ladm_col.utils.decorators import _log_quality_rule_validations
from asistente_ladm_col.utils.utils import Utils


class QualityRuleEngine(QObject):
    """
    Engine that executes Quality Rules

    :param db: DBConnector object
    :param rules: Either a dict {rule_key:rule_name} or a list [rule_key1, rule_key2]
    :param tolerance: Tolerance to be used when running the QRs, in millimeters
    :param with_gui:
    """
    def __init__(self, db, rules, tolerance, with_gui=True):
        QObject.__init__(self)
        self.logger = Logger()
        self.app = AppInterface()

        self.__qr_manager = QualityRuleManager()

        self.__db = db
        self.__rules = self.__get_dict_rules(rules)
        self.__result_layers = list()
        self.__with_gui = with_gui

        self.app.settings.tolerance = tolerance  # Tolerance must be given, we don't want anything implicit about it
        self.__tolerance = self.app.settings.tolerance  # Tolerance input might be altered (e.g., if it comes negative)
        self.__layer_manager = QualityRuleLayerManager(db, self.__rules.keys(), self.__tolerance)
        self.__quality_rules = QualityRules()
        self.quality_rule_logger = QualityRuleLogger(self.__db, self.__tolerance)

    def initialize(self, db, rules, tolerance, with_gui=True):
        """
        Objects of this class are reusable calling initialize()
        """
        self.__result_layers = list()
        self.__db = db
        self.__rules = self.__get_dict_rules(rules)
        self.__with_gui = with_gui
        self.app.settings.tolerance = tolerance
        self.__tolerance = self.app.settings.tolerance  # Tolerance input might be altered (e.g., if it comes negative)
        self.__layer_manager.initialize(self.__rules.keys(), self.__tolerance)
        self.quality_rule_logger.initialize(self.__db, self.__tolerance)

    def __get_dict_rules(self, rules):
        if isinstance(rules, dict):
            return rules  # We have everything ready

        # If rules is a list, we need to retrieve the quality rule names from the QRManager
        return {rule_key: self.__qr_manager.get_quality_rule_name(rule_key) for rule_key in rules}

    def validate_quality_rules(self):
        res = dict()  # {rule_key: QualityRuleExecutionResult}
        if self.__rules:
            self.quality_rule_logger.set_count_topology_rules(len(self.__rules))
            self.logger.info(__name__,
                             QCoreApplication.translate("QualityRuleEngine",
                                "Validating {} quality rules (tolerance: {}).").format(len(self.__rules), self.__tolerance))

            for rule_key, rule_name in self.__rules.items():
                if rule_name is not None:
                    layers = self.__layer_manager.get_layers(rule_key)
                    if layers:
                        res[rule_key] = self.__validate_quality_rule(rule_key, layers, rule_name=rule_name)
                        if self.__with_gui:
                            self.add_error_layers(res[rule_key].error_layers)
                    else:
                        msg = QCoreApplication.translate("QualityRuleEngine",
                                "Couldn't execute '{}' quality rule! Required layers are not available. Skipping...").format(rule_name)
                        res[rule_key] = QualityRuleExecutionResult(msg, None, dict())  # TODO: should be Qgis.None when https://github.com/qgis/QGIS/issues/42996 is solved
                        self.logger.warning(__name__, msg)
                else:
                    msg = QCoreApplication.translate("QualityRuleEngine",
                                                     "Quality rule with key '{}' does not exist! Skipping...").format(
                        rule_key)
                    res[rule_key] = QualityRuleExecutionResult(msg, None, dict())
                    self.logger.warning(__name__, msg)

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
            if error_layer.featureCount():  # Only load error layers that have at least one feature
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

    def __init__(self, db, tolerance):
        QObject.__init__(self)
        self.log_text = ""
        self.log_total_time = 0
        self.tolerance = tolerance
        self.__db = db

    def initialize(self, db, tolerance):
        """
        Objects of this class are reusable calling initialize()
        """
        self.log_text = ""
        self.log_total_time = 0
        self.tolerance = tolerance
        self.__db = db

    def set_count_topology_rules(self, count):
        self.show_message_emitted.emit(QCoreApplication.translate("QualityDialog", ""), count)

    def generate_log_button(self):
        self.show_button_emitted.emit()

    def get_log_result(self):
        return QualityRuleResultLog(self.__db, self.log_text, self.tolerance, self.log_total_time)


class QualityRuleResultLog(QObject):
    def __init__(self, db, log_text, tolerance, log_total_time):
        QObject.__init__(self)
        self.__db = db
        self.text = log_text
        self.tolerance = tolerance
        self.log_total_time = log_total_time

    @property
    def title(self):
        return QCoreApplication.translate(
            "QualityRuleResultLog",
            "<h2 align='center'>Quality Check Results</h2><div style='text-align:center;'>{}<br>Database: {}<br>Total execution time: {}<br>Tolerance {}mm.</div>").format(
            time.strftime("%d/%m/%y %H:%M:%S"),
            self.__db.get_description_conn_string(),
            Utils.set_time_format(self.log_total_time),
            self.tolerance)
