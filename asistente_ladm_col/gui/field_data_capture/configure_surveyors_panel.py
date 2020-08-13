# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-07-23
        git sha              : :%H$
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
from qgis.PyQt.QtWidgets import QTableWidgetItem
from qgis.PyQt.QtCore import (QCoreApplication,
                              Qt,
                              pyqtSignal)
from qgis.gui import QgsPanelWidget

from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('field_data_capture/configure_surveyors_panel_widget.ui')


class ConfigureSurveyorsPanelWidget(QgsPanelWidget, WIDGET_UI):
    clear_message_bar_requested = pyqtSignal()

    def __init__(self, parent, controller):
        QgsPanelWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.logger = Logger()
        self.controller = controller

        self.setDockMode(True)
        self.setPanelTitle(QCoreApplication.translate("ConfigureSurveyorsPanelWidget", "Configure surveyors"))
        self.panelAccepted.connect(self.panel_accepted)
        self.tbl_surveyors.itemSelectionChanged.connect(self.selection_changed)
        self.btn_save.clicked.connect(self.save_surveyor)
        self.btn_delete.clicked.connect(self.delete_surveyor)

        self.btn_delete.setEnabled(False)
        self.fill_data()
        self.tbl_surveyors.resizeColumnsToContents()

    def panel_accepted(self):
        self.clear_message_bar_requested.emit()

    def fill_data(self):
        self.tbl_surveyors.clearContents()
        surveyors_data = self.controller.get_surveyors_data()

        self.tbl_surveyors.setRowCount(len(surveyors_data))
        self.tbl_surveyors.setSortingEnabled(False)

        for row, data in enumerate(surveyors_data.items()):
            surveyor_name, surveyor_docid = data[1]
            self.fill_row(data[0], surveyor_name, surveyor_docid, row)

        self.tbl_surveyors.setSortingEnabled(True)
        self.tbl_surveyors.resizeColumnsToContents()

    def fill_row(self, surveyor_t_id, surveyor_name, surveyor_docid, row):
        item = QTableWidgetItem(surveyor_name)
        item.setData(Qt.UserRole, surveyor_t_id)
        self.tbl_surveyors.setItem(row, 0, item)

        item2 = QTableWidgetItem(surveyor_docid)
        item2.setData(Qt.UserRole, surveyor_t_id)
        self.tbl_surveyors.setItem(row, 1, item2)

    def selection_changed(self):
        self.btn_delete.setEnabled(bool(self.tbl_surveyors.selectedItems()))

    def save_surveyor(self):
        if self.txt_first_name.text().strip() and self.txt_first_last_name.text().strip() and self.txt_document_id.text().strip():
            try:
                int(self.txt_document_id.text().strip())
            except ValueError as e:
                self.logger.warning_msg(__name__, QCoreApplication.translate("ConfigureSurveyorsPanelWidget",
                                                                             "Invalid value for document id. Only digits are accepted."))
                return

            names = self.controller.db().names
            surveyor_data = {names.FDC_SURVEYOR_T_DOCUMENT_TYPE_F: "Cedula_ciudadania",
                             names.FDC_SURVEYOR_T_DOCUMENT_ID_F: self.txt_document_id.text().strip(),
                             names.FDC_SURVEYOR_T_FIRST_NAME_F: self.txt_first_name.text().strip(),
                             names.FDC_SURVEYOR_T_SECOND_NAME_F: self.txt_second_name.text().strip(),
                             names.FDC_SURVEYOR_T_FIRST_LAST_NAME_F: self.txt_first_last_name.text().strip(),
                             names.FDC_SURVEYOR_T_SECOND_LAST_NAME_F: self.txt_second_last_name.text().strip()}
            res = self.controller.save_surveyor(surveyor_data)
            if res:
                self.logger.info_msg(__name__, QCoreApplication.translate("ConfigureSurveyorsPanelWidget", "Surveyor saved!"))
                self.fill_data()
            else:
                self.logger.warning_msg(__name__, QCoreApplication.translate("ConfigureSurveyorsPanelWidget",
                                                                             "There was an error saving the surveyor."))
        else:
            self.logger.warning_msg(__name__, QCoreApplication.translate("ConfigureSurveyorsPanelWidget", "First name, last name and document id are mandatory."))

    def delete_surveyor(self):
        selected_surveyor_t_id = [item.data(Qt.UserRole) for item in self.tbl_surveyors.selectedItems()]
        if selected_surveyor_t_id:
            res = self.controller.delete_surveyor(selected_surveyor_t_id[0])
            if res:
                self.logger.info_msg(__name__, QCoreApplication.translate("ConfigureSurveyorsPanelWidget", "Surveyor deleted!"))
                self.fill_data()
            else:
                self.logger.warning_msg(__name__, QCoreApplication.translate("ConfigureSurveyorsPanelWidget",
                                                                             "There was an error deleting the surveyor."))

