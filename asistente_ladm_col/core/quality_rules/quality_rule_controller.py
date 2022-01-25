"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2022-01-13
        copyright       : (C) 2022 by Germán Carrillo (SwissTierras Colombia)
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
from qgis.PyQt.QtCore import (pyqtSignal,
                              QSettings,
                              QObject)

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.quality_rule_config import QR_IGACR3006
from asistente_ladm_col.config.general_config import DEFAULT_USE_ROADS_VALUE
from asistente_ladm_col.core.quality_rules.quality_rule_engine import (QualityRuleEngine,
                                                                       QualityRuleResultLog)
from asistente_ladm_col.core.quality_rules.quality_rule_registry import QualityRuleRegistry


class QualityRuleController(QObject):

    open_report_called = pyqtSignal(QualityRuleResultLog)  # log result
    total_progress_changed = pyqtSignal(int)  # Progress value

    def __init__(self, db):
        QObject.__init__(self)
        self.app = AppInterface()
        self._db = db

        # Hierarquical dict of qrs and qr groups
        self.__qrs_tree_data = dict()  # {type: {qr_key1: qr_obj1, ...}, ...}

        # Hierarquical dict of qrs and qr groups with general results
        self.__general_results_tree_data = dict()  # {type: {qr_obj1: qr_results1, ...}, ...}

        self.__selected_qrs = list()

        self.__qr_engine = None

    def validate_qrs(self):
        self.__qr_engine = QualityRuleEngine(self._db, self.__selected_qrs, self.app.settings.tolerance)
        self.__qr_engine.progress_changed.connect(self.total_progress_changed)
        #self.__qr_engine.qr_logger.show_message_emitted.connect(self.show_log_quality_message)
        #self.__qr_engine.qr_logger.show_button_emitted.connect(self.show_log_quality_button)
        #self.__qr_engine.qr_logger.set_initial_progress_emitted.connect(self.set_log_quality_initial_progress)
        #self.__qr_engine.qr_logger.set_final_progress_emitted.connect(self.set_log_quality_final_progress)

        use_roads = bool(QSettings().value('Asistente-LADM-COL/quality/use_roads', DEFAULT_USE_ROADS_VALUE, bool))
        options = {QR_IGACR3006: {'use_roads': use_roads}}

        res, msg, res_obj = self.__qr_engine.validate_quality_rules(options)

    def all_error_layers(self):
        return [layer for qr_res in self.__res_dict.values() for layer in qr_res.error_layers if layer.featureCount()]

    def __get_qrs_per_role_and_models(self):
        return QualityRuleRegistry().get_qrs_per_role_and_models(self._db)

    def load_tree_data(self):
        """
        Builds a hierarchical dict by qr type: {qr_type1: {qr_key1: qr_obj1, ...}, ...}

        Tree data for panel 1.
        """
        qrs = self.__get_qrs_per_role_and_models()  # Dict of qr key and qr objects.

        for qr_key, qr_obj in qrs.items():
            type = qr_obj.type()
            if type not in self.__qrs_tree_data:
                self.__qrs_tree_data[type] = {qr_key: qr_obj}
            else:
                self.__qrs_tree_data[type][qr_key] = qr_obj

    def get_qrs_tree_data(self):
        return self.__qrs_tree_data

    def set_selected_qrs(self, selected_qrs):
        # We sort them because the engine needs the QRs sorted for the PDF report
        for type, qr_dict in self.__qrs_tree_data.items():
            for qr_key, qr_obj in qr_dict.items():
                if qr_key in selected_qrs:
                    self.__selected_qrs.append(qr_key)

    def get_selected_qrs(self):
        return self.__selected_qrs

    def load_general_results_tree_data(self):
        """
        Builds a hierarchical dict by qr type: {type: {qr_obj1: qr_results1, ...}, ...}

        Tree data for panel 2.
        """
        for type, qr_dict in self.__qrs_tree_data.items():
            for qr_key, qr_obj in qr_dict.items():
                if qr_key in self.__selected_qrs:
                    if type not in self.__general_results_tree_data:
                        self.__general_results_tree_data[type] = {qr_obj: None}
                    else:
                        self.__general_results_tree_data[type][qr_obj] = None

    def get_general_results_tree_data(self):
        return self.__general_results_tree_data

    def set_qr_validation_result(self, qr, qr_result):
        """
        When a QR has its validation result after validation,
        we can store it in our custom dict by using this method.
        """
        for type, qr_dict in self.__general_results_tree_data.items():
            for k, v in qr_dict.items():
                if k == qr:
                    self.__general_results_tree_data[type][k] = qr_result

    def open_report(self):
        if self.__qr_engine:
            log_result = self.__qr_engine.qr_logger.get_log_result()
            self.open_report_called.emit(log_result)

    # def show_log_quality_message(self, msg, count):
    #     self.progress_message_bar = self.iface.messageBar().createMessage("Asistente LADM-COL", msg)
    #     self.log_quality_validation_progress = QProgressBar()
    #     self.log_quality_validation_progress.setFixedWidth(80)
    #     self.log_quality_total_rule_count = count
    #     self.log_quality_validation_progress.setMaximum(self.log_quality_total_rule_count * 10)
    #     self.progress_message_bar.layout().addWidget(self.log_quality_validation_progress)
    #     self.iface.messageBar().pushWidget(self.progress_message_bar, Qgis.Info)
    #     self.log_quality_validation_progress_count = 0
    #     self.log_quality_current_rule_count = 0
    #
    # def show_log_quality_button(self):
    #     self.button = QPushButton(self.progress_message_bar)
    #     self.button.pressed.connect(self.show_log_quality_dialog)
    #     self.button.setText(QCoreApplication.translate("LogQualityDialog", "Show Results"))
    #     self.progress_message_bar.layout().addWidget(self.button)
    #     QCoreApplication.processEvents()
    #
    # def set_log_quality_initial_progress(self, msg):
    #     self.log_quality_validation_progress_count += 2  # 20% of the current rule
    #     self.log_quality_validation_progress.setValue(self.log_quality_validation_progress_count)
    #     self.progress_message_bar.setText(
    #         QCoreApplication.translate("LogQualityDialog",
    #                                    "Checking {} out of {}: '{}'").format(
    #                                     self.log_quality_current_rule_count + 1,
    #                                     self.log_quality_total_rule_count,
    #                                     msg))
    #     QCoreApplication.processEvents()
    #
    # def set_log_quality_final_progress(self, msg):
    #     self.log_quality_validation_progress_count += 8  # 80% of the current rule
    #     self.log_quality_validation_progress.setValue(self.log_quality_validation_progress_count)
    #     self.log_quality_current_rule_count += 1
    #     if self.log_quality_current_rule_count ==  self.log_quality_total_rule_count:
    #         self.progress_message_bar.setText(QCoreApplication.translate("LogQualityDialog",
    #             "All the {} quality rules were checked! Click the button at the right-hand side to see a report.").format(self.log_quality_total_rule_count))
    #     else:
    #         self.progress_message_bar.setText(msg)
    #     QCoreApplication.processEvents()
    #
