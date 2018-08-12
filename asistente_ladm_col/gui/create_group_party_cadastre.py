# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-08-10
        git sha              : :%H$
        copyright            : (C) 2018 by Sergio Ramírez (Incige SAS)
        email                : seralra96@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
import copy

from qgis.core import (QgsEditFormConfig, QgsVectorLayerUtils, Qgis,
                       QgsWkbTypes, QgsMapLayerProxyModel)
from qgis.gui import QgsMessageBar
from qgis.PyQt.QtCore import Qt, QPoint, QCoreApplication, QSettings
from qgis.PyQt.QtWidgets import QDialog, QTableWidgetItem, QListWidgetItem

from ..utils import get_ui_class
from ..config.table_mapping_config import NATURAL_PARTY_TABLE
from ..config.help_strings import HelpStrings

DIALOG_UI = get_ui_class('dlg_group_party.ui')

class CreateGroupPartyCadastre(QDialog, DIALOG_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QDialog.__init__(self)
        self.setupUi(self)
        self.iface = iface
        self._natural_party_layer = None
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()

        self.data = {} # {t_id: [display_text, denominator, numerator]}
        self.current_selected_parties = [] #  [t_ids]
        self.parties_to_group = {} # {t_id: [denominator, numerator]}

        self.txt_search_party.setText("")
        self.btn_select.setEnabled(False)
        self.btn_deselect.setEnabled(False)

        self.tbl_selected_parties.setColumnCount(3)
        self.tbl_selected_parties.setColumnWidth(0, 120)
        self.tbl_selected_parties.setColumnWidth(1, 70)
        self.tbl_selected_parties.setColumnWidth(2, 70)
        self.tbl_selected_parties.sortItems(0, Qt.AscendingOrder)

        self.txt_search_party.textEdited.connect(self.search)
        self.lst_all_parties.itemSelectionChanged.connect(self.selection_changed_all)
        self.tbl_selected_parties.itemSelectionChanged.connect(self.selection_changed_selected)
        self.tbl_selected_parties.cellChanged.connect(self.valueEdited)
        self.btn_select_all.clicked.connect(self.select_all)
        self.btn_deselect_all.clicked.connect(self.deselect_all)
        self.btn_select.clicked.connect(self.select)
        self.btn_deselect.clicked.connect(self.deselect)

    def set_parties_data(self, parties_data):
        """
        Initialize parties data.

        :param parties_data: Dictionary {t_id: [display_text, denominator, numerator]}
        :type parties_data: dict
        """
        self.data = parties_data
        self.update_lists()

    def search(self, text):
        self.update_lists(True)

    def selection_changed_all(self):
        self.btn_select.setEnabled(len(self.lst_all_parties.selectedItems()))

    def selection_changed_selected(self):
        self.btn_deselect.setEnabled(len(self.tbl_selected_parties.selectedItems()))

    def select_all(self):
        """
        SLOT. Select all parties listed from left list widget.
        """
        items_ids = []
        for index in range(self.lst_all_parties.count()):
             items_ids.append(self.lst_all_parties.item(index).data(Qt.UserRole))
        self.add_parties_to_selected(items_ids)

    def deselect_all(self):
        """
        SLOT. Remove all parties from left list widget.
        """
        items_ids = []
        for index in range(self.tbl_selected_parties.rowCount()):
             items_ids.append(self.tbl_selected_parties.item(index, 0).data(Qt.UserRole))
        self.remove_parties_from_selected(items_ids)

    def select(self):
        """
        SLOT. Select all parties highlighted in left list widget.
        """
        self.add_parties_to_selected([item.data(Qt.UserRole) for item in self.lst_all_parties.selectedItems()])

    def deselect(self):
        """
        SLOT. Remove all parties highlighted in right list widget.
        """
        self.remove_parties_from_selected([item.data(Qt.UserRole) for item in self.tbl_selected_parties.selectedItems() if item.column() == 0])

    def add_parties_to_selected(self, parties_ids):
        self.current_selected_parties.extend(parties_ids)
        self.update_lists()

    def remove_parties_from_selected(self, parties_ids):
        for party_id in parties_ids:
            self.current_selected_parties.remove(party_id)
            if party_id in self.parties_to_group:
                del self.parties_to_group[party_id]
        self.update_lists()

    def update_lists(self, only_update_all_list=False):
        """
        Update left list widget and optionally the right one.

        :param only_update_all_list: Only updat left list widget.
        :type only_update_all_list: bool
        """
        # All parties
        self.lst_all_parties.clear()
        if self.txt_search_party.text():
            tmp_parties = {i:d for i,d in self.data.items() if self.txt_search_party.text().lower() in d[0].lower()}
        else:
            tmp_parties = copy.deepcopy(self.data) # Copy all!

        for party_id in self.current_selected_parties:
            if party_id in tmp_parties:
                del tmp_parties[party_id]

        for i,d in tmp_parties.items():
            item = QListWidgetItem(d[0])
            item.setData(Qt.UserRole, i)
            self.lst_all_parties.addItem(item)

        if not only_update_all_list:
            # Selected parties
            self.tbl_selected_parties.clearContents()
            self.tbl_selected_parties.setRowCount(len(self.current_selected_parties))
            self.tbl_selected_parties.setColumnCount(3)
            self.tbl_selected_parties.setSortingEnabled(False)

            for row, party_id in enumerate(self.current_selected_parties):
                item = QTableWidgetItem(self.data[party_id][0])
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                item.setData(Qt.UserRole, party_id)
                self.tbl_selected_parties.setItem(row, 0, item)
                value_denominator = self.parties_to_group[party_id][0] if party_id in self.parties_to_group else self.data[party_id][1]
                self.tbl_selected_parties.setItem(row, 1, QTableWidgetItem(str(value_denominator)))
                value_numerator = self.parties_to_group[party_id][1] if party_id in self.parties_to_group else self.data[party_id][2]
                self.tbl_selected_parties.setItem(row, 2, QTableWidgetItem(str(value_numerator)))

            self.tbl_selected_parties.setSortingEnabled(True)


    def valueEdited(self, row, column):
        """
        SLOT. Update either the denominator or the numerator for given row.

        :param row: Edited row
        :type row: int
        :param column: Edited column
        :type column: int
        """
        if column != 0:
            party_id = self.tbl_selected_parties.item(row, 0).data(Qt.UserRole)
            value_denominator = self.tbl_selected_parties.item(row, 1).text()

            # While creating a row and the second column is created, the third
            # one doesn't exist, so use the value already stored for that case
            value_numerator = self.parties_to_group[party_id][1] if party_id in self.parties_to_group else 0
            if self.tbl_selected_parties.item(row, 2) is not None:
                value_numerator = self.tbl_selected_parties.item(row, 2).text()

            self.parties_to_group[party_id] = [value_denominator, value_numerator]

    def accept(self):
        """ Overwrit the dialog's `accept
        <https://doc.qt.io/qt-5/qdialog.html#accept>`_ SLOT to store
        selected parties and denominator-numerator before closing the dialog.
        """
        self.parties_to_group = {}
        for index in range(self.tbl_selected_parties.rowCount()):
             k = self.tbl_selected_parties.item(index, 0).data(Qt.UserRole)
             v_d = self.tbl_selected_parties.item(index, 1).text()
             v_n = self.tbl_selected_parties.item(index, 2).text()
             self.parties_to_group[ k ] = [v_d, v_n]
        self.done(1)


    def show_help(self):
        self.qgis_utils.show_help("natural_party")
