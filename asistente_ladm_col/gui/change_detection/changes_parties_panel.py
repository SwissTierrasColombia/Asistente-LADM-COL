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
from functools import partial

import qgis

from qgis.PyQt.QtGui import QMouseEvent
from qgis.PyQt.QtCore import QCoreApplication, Qt, QEvent, QPoint
from qgis.PyQt.QtWidgets import QTableWidgetItem, QTextEdit
from qgis.core import (QgsWkbTypes,
                       Qgis,
                       QgsMessageLog,
                       QgsFeature,
                       QgsFeatureRequest,
                       QgsExpression,
                       QgsRectangle,
                       NULL)

from qgis.gui import QgsPanelWidget
from asistente_ladm_col.config.general_config import (OFFICIAL_DB_PREFIX,
                                                      OFFICIAL_DB_SUFFIX,
                                                      PREFIX_LAYER_MODIFIERS,
                                                      SUFFIX_LAYER_MODIFIERS,
                                                      STYLE_GROUP_LAYER_MODIFIERS,
                                                      COLLECTED_DB_SOURCE,
                                                      OFFICIAL_DB_SOURCE)
from asistente_ladm_col.config.table_mapping_config import (PARCEL_NUMBER_FIELD,
                                                            PARCEL_NUMBER_BEFORE_FIELD,
                                                            COL_PARTY_DOCUMENT_ID_FIELD,
                                                            FMI_FIELD,
                                                            ID_FIELD,
                                                            PARCEL_TABLE,
                                                            PLOT_TABLE,
                                                            UEBAUNIT_TABLE,
                                                            COL_PARTY_TABLE,
                                                            DICT_PLURAL,
                                                            COL_PARTY_DOC_TYPE_FIELD,
                                                            DOCUMENT_ID_FIELD,
                                                            COL_PARTY_NAME_FIELD)
from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('change_detection/changes_parties_panel_widget.ui')

class ChangesPartyPanelWidget(QgsPanelWidget, WIDGET_UI):
    def __init__(self, parent, utils, data):
        QgsPanelWidget.__init__(self, None)
        self.setupUi(self)
        self.parent = parent
        self.utils = utils

        # dict with 2 k:v pairs, one for collected data and one for official data
        # Values are dicts themselves, with the party info we compare (see PARTY_FIELDS_TO_COMPARE + right type)
        self.data = data

        self.setDockMode(True)

        # Set connections
        # self.panelAccepted.connect(self.initialize_tools_and_layers)

        if data is not None:  # Do a search!
            self.fill_table()

    def fill_table(self):
        self.tbl_changes_parties.clearContents()
        self.tbl_changes_parties.setRowCount(max(len(self.data[COLLECTED_DB_SOURCE]), len(self.data[OFFICIAL_DB_SOURCE])))  # t_id shouldn't be counted
        self.tbl_changes_parties.setSortingEnabled(False)

        sorted_official_parties = sorted(self.data[OFFICIAL_DB_SOURCE], key=lambda item: item[COL_PARTY_DOCUMENT_ID_FIELD])
        sorted_collected_parties = sorted(self.data[COLLECTED_DB_SOURCE], key=lambda item: item[COL_PARTY_DOCUMENT_ID_FIELD])

        for row, official_party in enumerate(sorted_official_parties):
            collected_party_pair = {}
            for collected_party in sorted_collected_parties:
                if official_party[COL_PARTY_DOCUMENT_ID_FIELD] == official_party[COL_PARTY_DOCUMENT_ID_FIELD]:
                    collected_party_pair = official_party
                    sorted_collected_parties.remove(collected_party_pair)
                    break

            self.fill_item(official_party, collected_party_pair, row)

        for row, collected_party in enumerate(sorted_collected_parties):
            self.fill_item({}, collected_party, row + self.tbl_changes_parties.rowCount() - 1)

        self.tbl_changes_parties.setSortingEnabled(True)

    def fill_item(self, official_party, collected_party, row):
        self.tbl_changes_parties.setCellWidget(row, 0, self.get_widget_with_party_info_formatted(official_party))
        self.tbl_changes_parties.setCellWidget(row, 1, self.get_widget_with_party_info_formatted(collected_party))

        self.tbl_changes_parties.setItem(row, 2, QTableWidgetItem())
        self.tbl_changes_parties.item(row, 2).setBackground(Qt.green if official_party == collected_party else Qt.red)

    def get_widget_with_party_info_formatted(self, party_info):
        widget = QTextEdit()

        if party_info:
            html = list()
            html.append("<b>{}</b>".format(party_info[COL_PARTY_NAME_FIELD]))
            html.append("<i>{}</i>: <b>{}</b>".format(party_info[COL_PARTY_DOC_TYPE_FIELD], party_info[DOCUMENT_ID_FIELD]))
            html.append("<i>Derecho</i>: <b>{}</b>".format(party_info['derecho']))
            widget.setHtml("<br>".join(html))

        return widget