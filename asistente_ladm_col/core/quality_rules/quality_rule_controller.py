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
from asistente_ladm_col.core.quality_rules.quality_rule_engine import QualityRuleEngine


class QualityRuleController:
    def __init__(self):
        pass

    def validate_qrs(self, selected_rules, tolerance, options=dict()):
        self.qr_engine = QualityRuleEngine(self.get_db_connection(), quality_dialog.selected_rules, self.app.settings.tolerance)
        self.qr_engine.qr_logger.show_message_emitted.connect(self.show_log_quality_message)
        self.qr_engine.qr_logger.show_button_emitted.connect(self.show_log_quality_button)
        self.qr_engine.qr_logger.set_initial_progress_emitted.connect(self.set_log_quality_initial_progress)
        self.qr_engine.qr_logger.set_final_progress_emitted.connect(self.set_log_quality_final_progress)

        use_roads = bool(QSettings().value('Asistente-LADM-COL/quality/use_roads', DEFAULT_USE_ROADS_VALUE, bool))
        options = {QR_IGACR3006: {'use_roads': use_roads}}

        self.qr_engine.validate_quality_rules(options)

    def all_error_layers(self):
        return [layer for qr_res in self.__res_dict.values() for layer in qr_res.error_layers if layer.featureCount()]

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
    # def show_log_quality_dialog(self):
    #     log_result = self.quality_rule_engine.qr_logger.get_log_result()
    #     dlg = LogQualityDialog(self.conn_manager.get_db_connector_from_source(), log_result, self.main_window)
    #     dlg.exec_()
