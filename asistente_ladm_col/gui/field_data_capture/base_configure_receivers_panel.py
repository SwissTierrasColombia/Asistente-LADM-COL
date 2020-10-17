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
import uuid

from qgis.PyQt.QtWidgets import QTableWidgetItem
from qgis.PyQt.QtCore import (QCoreApplication,
                              Qt,
                              pyqtSignal)
from qgis.gui import QgsPanelWidget

from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('field_data_capture/base_configure_receivers_panel_widget.ui')


class BaseConfigureReceiversPanelWidget(QgsPanelWidget, WIDGET_UI):
    clear_message_bar_requested = pyqtSignal()

    DOCUMENT_COLUMN = 0
    NAME_COLUMN = 1

    def __init__(self, parent, controller):
        QgsPanelWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.logger = Logger()
        self._controller = controller

        self.setDockMode(True)
        self.setPanelTitle(QCoreApplication.translate("BaseConfigureReceiversPanelWidget", "Configure receivers"))
        self.panelAccepted.connect(self.panel_accepted)
        self.tbl_receivers.itemSelectionChanged.connect(self.selection_changed)
        self.btn_save.clicked.connect(self.save_receiver)
        self.btn_delete.clicked.connect(self.delete_receiver)

        self.btn_delete.setEnabled(False)
        self.fill_data()
        self.tbl_receivers.resizeColumnsToContents()

        self.fill_document_types()

    def panel_accepted(self):
        self.clear_message_bar_requested.emit()

    def fill_data(self):
        self.tbl_receivers.clearContents()
        receivers_data = self._controller.get_receivers_data()

        self.tbl_receivers.setRowCount(len(receivers_data))
        self.tbl_receivers.setSortingEnabled(False)

        for row, data in enumerate(receivers_data.items()):
            receiver_name, receiver_docid = data[1]
            self.fill_row(data[0], receiver_name, receiver_docid, row)

        self.tbl_receivers.setSortingEnabled(True)
        self.tbl_receivers.resizeColumnsToContents()

    def fill_row(self, receiver_t_id, receiver_name, receiver_docid, row):
        item = QTableWidgetItem(receiver_name)
        item.setData(Qt.UserRole, receiver_t_id)
        self.tbl_receivers.setItem(row, self.NAME_COLUMN, item)

        item2 = QTableWidgetItem(receiver_docid)
        item2.setData(Qt.UserRole, receiver_t_id)
        self.tbl_receivers.setItem(row, self.DOCUMENT_COLUMN, item2)

    def fill_document_types(self):
        self.cbo_document_type.clear()
        for t_id, text in self._controller.get_document_types().items():
            self.cbo_document_type.addItem(text, t_id)

    def selection_changed(self):
        self.btn_delete.setEnabled(bool(self.tbl_receivers.selectedItems()))

    def save_receiver(self):
        if self.txt_name.text().strip() and self.txt_document_id.text().strip():
            try:
                int(self.txt_document_id.text().strip())
            except ValueError as e:
                self.logger.warning_msg(__name__, QCoreApplication.translate("BaseConfigureReceiversPanelWidget",
                                                                             "Invalid value for document id. Only digits are accepted."))
                return

            basket_t_id, msg = self._controller.get_basket_id_for_new_receiver()
            if basket_t_id is None:
                self.logger.warning_msg(__name__, msg)
                return

            coordinator_basket_t_id, msg = self._controller.get_coordinator_basket_id_for_new_receiver()
            if coordinator_basket_t_id == False:  # We don't want to catch None value here, hence the explicit condition
                self.logger.warning_msg(__name__, msg)
                return

            names = self._controller.db().names
            receiver_data = {names.FDC_USER_T_DOCUMENT_TYPE_F: self.cbo_document_type.currentData(),
                             names.FDC_USER_T_DOCUMENT_ID_F: self.txt_document_id.text().strip(),
                             names.FDC_USER_T_NAME_F: self.txt_name.text().strip(),
                             names.FDC_USER_T_ROLE_F: self._controller.receiver_type,
                             names.FDC_USER_T_COORDINATOR_F: coordinator_basket_t_id,
                             names.T_ILI_TID_F: str(uuid.uuid4()),
                             names.T_BASKET_F: basket_t_id}
            res = self._controller.save_receiver(receiver_data)
            if res:
                self.logger.success_msg(__name__, QCoreApplication.translate("BaseConfigureReceiversPanelWidget", "Receiver saved!"))
                self.fill_data()
                self.initialize_input_controls()
            else:
                self.logger.warning_msg(__name__, QCoreApplication.translate("BaseConfigureReceiversPanelWidget",
                                                                             "There was an error saving the receiver."))
        else:
            self.logger.warning_msg(__name__, QCoreApplication.translate("BaseConfigureReceiversPanelWidget", "Name and document id are mandatory."))

    def delete_receiver(self):
        selected_receiver_id = [item.data(Qt.UserRole) for item in self.tbl_receivers.selectedItems()]
        if selected_receiver_id:
            res, msg = self._controller.delete_receiver(selected_receiver_id[0])
            if res:
                self.logger.success_msg(__name__, QCoreApplication.translate("BaseConfigureReceiversPanelWidget", "Receiver deleted!"))
                self.fill_data()
            else:
                if not msg:
                    msg = QCoreApplication.translate("BaseConfigureReceiversPanelWidget", "There was an error deleting the receiver.")
                self.logger.warning_msg(__name__, msg)

    def initialize_input_controls(self):
        self.txt_name.setText('')
        self.txt_name.setFocus()
        self.txt_document_id.setText('')