# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-07-17
        git sha              : :%H$
        copyright            : (C) 2019 by Germán Carrillo (BSF Swissphoto)
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
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import (QTableWidgetItem,
                                 QTextEdit)
from qgis.core import NULL
from qgis.gui import QgsPanelWidget

from asistente_ladm_col.config.change_detection_config import (DICT_KEY_PARTY_T_NAME_F,
                                                               DICT_KEY_PARTY_T_DOCUMENT_ID_F,
                                                               DICT_KEY_PARTY_T_DOCUMENT_TYPE_F,
                                                               DICT_KEY_PARTY_T_RIGHT)
from asistente_ladm_col.config.general_config import (COLLECTED_DB_SOURCE,
                                                      SUPPLIES_DB_SOURCE)
from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('change_detection/changes_parties_panel_widget.ui')


class ChangesPartyPanelWidget(QgsPanelWidget, WIDGET_UI):
    def __init__(self, parent, utils, data):
        QgsPanelWidget.__init__(self, None)
        self.setupUi(self)
        self.parent = parent
        self.utils = utils

        # dict with 2 k:v pairs, one for collected data and one for supplies data
        # Values are dicts themselves, with the party info we compare (see party_fields_to_compare + right type)
        self.data = data

        self.setDockMode(True)

        # Set connections
        # self.panelAccepted.connect(self.initialize_tools_and_layers)

        if data is not None:  # Do a search!
            self.fill_table()

    def fill_table(self):
        self.tbl_changes_parties.clearContents()

        # Get max num of columns for tbl_changes_parties (equals to the number of different documents in both db sources)
        list_documents = list()
        for db_source in self.data:
            if self.data[db_source] != NULL:
                for party in self.data[db_source]:
                    list_documents.append(party[DICT_KEY_PARTY_T_DOCUMENT_ID_F])

        number_of_supplies_rows = len(self.data[SUPPLIES_DB_SOURCE]) if self.data[SUPPLIES_DB_SOURCE] != NULL else 0
        max_num_rows = len(set(list_documents))
        self.tbl_changes_parties.setRowCount(max_num_rows)
        self.tbl_changes_parties.setSortingEnabled(False)

        sorted_supplies_parties = list()
        sorted_collected_parties = list()
        if self.data[SUPPLIES_DB_SOURCE] != NULL:
            sorted_supplies_parties = sorted(self.data[SUPPLIES_DB_SOURCE], key=lambda item: item[DICT_KEY_PARTY_T_DOCUMENT_ID_F])
        if self.data[COLLECTED_DB_SOURCE] != NULL:
            sorted_collected_parties = sorted(self.data[COLLECTED_DB_SOURCE], key=lambda item: item[DICT_KEY_PARTY_T_DOCUMENT_ID_F])

        # Iterate supplies parties looking for its corresponding collected party. If none found, pair it with empty dict
        for row, supplies_party in enumerate(sorted_supplies_parties):
            collected_party_pair = {}
            for collected_party in sorted_collected_parties:
                if supplies_party[DICT_KEY_PARTY_T_DOCUMENT_ID_F] == collected_party[DICT_KEY_PARTY_T_DOCUMENT_ID_F]:
                    collected_party_pair = collected_party
                    sorted_collected_parties.remove(collected_party_pair)  # Don't search again this party
                    break

            self.fill_item(supplies_party, collected_party_pair, row)

        for row, collected_party in enumerate(sorted_collected_parties):
            self.fill_item({}, collected_party, row + number_of_supplies_rows)

        self.tbl_changes_parties.setSortingEnabled(True)

    def fill_item(self, supplies_party, collected_party, row):
        self.tbl_changes_parties.setCellWidget(row, 0, self.get_widget_with_party_info_formatted(supplies_party))
        self.tbl_changes_parties.setCellWidget(row, 1, self.get_widget_with_party_info_formatted(collected_party))

        type_item = QTableWidgetItem()
        type_item.setBackground(Qt.green if supplies_party == collected_party else Qt.red)
        self.tbl_changes_parties.setItem(row, 2, type_item)

    def get_widget_with_party_info_formatted(self, party_info):
        widget = QTextEdit()

        if party_info:
            html = list()
            html.append("<b>{}</b>".format(party_info[DICT_KEY_PARTY_T_NAME_F]))
            html.append("<i>{}</i>: <b>{}</b>".format(party_info[DICT_KEY_PARTY_T_DOCUMENT_TYPE_F], party_info[DICT_KEY_PARTY_T_DOCUMENT_ID_F]))
            html.append("<i>Derecho</i>: <b>{}</b>".format(party_info[DICT_KEY_PARTY_T_RIGHT]))
            widget.setHtml("<br>".join(html))

        return widget
