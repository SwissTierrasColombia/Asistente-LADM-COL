# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-06-07
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

from qgis.gui import QgsPanelWidget
from qgis.PyQt.QtCore import (pyqtSignal,
                              QCoreApplication)

from asistente_ladm_col.config.general_config import (LAYER,
                                                      SOURCE_DB,
                                                      COLLECTED_DB_SOURCE,
                                                      SUPPLIES_DB_SOURCE)
from asistente_ladm_col.config.gui.change_detection_config import (CHANGE_DETECTION_NEW_PARCEL,
                                                                   CHANGE_DETECTION_MISSING_PARCEL,
                                                                   CHANGE_DETECTION_PARCEL_CHANGED,
                                                                   CHANGE_DETECTION_PARCEL_ONLY_GEOMETRY_CHANGED,
                                                                   CHANGE_DETECTION_PARCEL_REMAINS,
                                                                   CHANGE_DETECTION_SEVERAL_PARCELS,
                                                                   CHANGE_DETECTION_NULL_PARCEL,
                                                                   DICT_KEY_PARCEL_T_PARCEL_NUMBER_F,
                                                                   PARCEL_STATUS)
from asistente_ladm_col.config.mapping_config import QueryNames
from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('change_detection/parcels_changes_summary_panel_widget.ui')


class ParcelsChangesSummaryPanelWidget(QgsPanelWidget, WIDGET_UI):
    all_parcels_panel_requested = pyqtSignal(str)

    def __init__(self, parent, utils):
        QgsPanelWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.utils = utils

        self.setDockMode(True)
        self.setPanelTitle(QCoreApplication.translate("ParcelsChangesSummaryPanelWidget", "Summary of changes detected"))

    def fill_data(self):
        compared_parcels_data = self.utils.get_compared_parcels_data()
        inverse_compared_parcels_data = self.utils.get_compared_parcels_data(inverse=True)

        # Summarize and show in its proper control
        summary = {CHANGE_DETECTION_NEW_PARCEL: {DICT_KEY_PARCEL_T_PARCEL_NUMBER_F: list(), self.utils._db.names.T_ID_F: list(), QueryNames.COUNT_KEY: 0, SOURCE_DB: COLLECTED_DB_SOURCE},
                   CHANGE_DETECTION_MISSING_PARCEL: {DICT_KEY_PARCEL_T_PARCEL_NUMBER_F: list(), self.utils._supplies_db.names.T_ID_F: list(), QueryNames.COUNT_KEY: 0, SOURCE_DB: SUPPLIES_DB_SOURCE},
                   CHANGE_DETECTION_PARCEL_CHANGED: {DICT_KEY_PARCEL_T_PARCEL_NUMBER_F: list(), self.utils._db.names.T_ID_F: list(), QueryNames.COUNT_KEY: 0, SOURCE_DB: COLLECTED_DB_SOURCE},
                   CHANGE_DETECTION_PARCEL_ONLY_GEOMETRY_CHANGED: {DICT_KEY_PARCEL_T_PARCEL_NUMBER_F: list(), self.utils._db.names.T_ID_F: list(), QueryNames.COUNT_KEY: 0, SOURCE_DB: COLLECTED_DB_SOURCE},
                   CHANGE_DETECTION_PARCEL_REMAINS: {DICT_KEY_PARCEL_T_PARCEL_NUMBER_F: list(), self.utils._db.names.T_ID_F: list(), QueryNames.COUNT_KEY: 0, SOURCE_DB: COLLECTED_DB_SOURCE},
                   CHANGE_DETECTION_SEVERAL_PARCELS: {DICT_KEY_PARCEL_T_PARCEL_NUMBER_F: list(), self.utils._db.names.T_ID_F: list(), QueryNames.COUNT_KEY: 0, SOURCE_DB: COLLECTED_DB_SOURCE},
                   CHANGE_DETECTION_NULL_PARCEL: {DICT_KEY_PARCEL_T_PARCEL_NUMBER_F: list(), self.utils._db.names.T_ID_F: list(), QueryNames.COUNT_KEY: 0, SOURCE_DB: COLLECTED_DB_SOURCE}}

        total_count = 0
        for parcel_number, parcel_attrs in compared_parcels_data.items():
            count = len(parcel_attrs[self.utils._db.names.T_ID_F])
            total_count += count
            summary[parcel_attrs[PARCEL_STATUS]][QueryNames.COUNT_KEY] += count
            summary[parcel_attrs[PARCEL_STATUS]][DICT_KEY_PARCEL_T_PARCEL_NUMBER_F].append(parcel_number)
            summary[parcel_attrs[PARCEL_STATUS]][self.utils._db.names.T_ID_F].extend(parcel_attrs[self.utils._db.names.T_ID_F])

        # Fill missing parcel data
        for parcel_number, parcel_attrs in inverse_compared_parcels_data.items():
            if parcel_attrs[PARCEL_STATUS] == CHANGE_DETECTION_NEW_PARCEL:
                count = len(parcel_attrs[self.utils._supplies_db.names.T_ID_F])
                total_count += count
                summary[CHANGE_DETECTION_MISSING_PARCEL][QueryNames.COUNT_KEY] += count
                summary[CHANGE_DETECTION_MISSING_PARCEL][DICT_KEY_PARCEL_T_PARCEL_NUMBER_F].append(parcel_number)
                summary[CHANGE_DETECTION_MISSING_PARCEL][self.utils._supplies_db.names.T_ID_F].extend(parcel_attrs[self.utils._supplies_db.names.T_ID_F])
                summary[CHANGE_DETECTION_MISSING_PARCEL][SOURCE_DB] = SUPPLIES_DB_SOURCE

        self.lbl_new_parcels_count.setText(str(summary[CHANGE_DETECTION_NEW_PARCEL][QueryNames.COUNT_KEY]))
        self.lbl_missing_parcels_count.setText(str(summary[CHANGE_DETECTION_MISSING_PARCEL][QueryNames.COUNT_KEY]))
        self.lbl_parcels_with_alphanumeric_changes_count.setText(str(summary[CHANGE_DETECTION_PARCEL_CHANGED][QueryNames.COUNT_KEY]))
        self.lbl_parcels_with_only_geometry_changes_count.setText(str(summary[CHANGE_DETECTION_PARCEL_ONLY_GEOMETRY_CHANGED][QueryNames.COUNT_KEY]))
        self.lbl_parcels_with_no_changes_count.setText(str(summary[CHANGE_DETECTION_PARCEL_REMAINS][QueryNames.COUNT_KEY]))
        self.lbl_duplicated_parcels_count.setText(str(summary[CHANGE_DETECTION_SEVERAL_PARCELS][QueryNames.COUNT_KEY]))
        self.lbl_null_parcel_numbers_count.setText(str(summary[CHANGE_DETECTION_NULL_PARCEL][QueryNames.COUNT_KEY]))
        self.lbl_total_parcels_count.setText(str(total_count))

        # Enable/Disable buttons
        self.btn_new_parcels.setEnabled(summary[CHANGE_DETECTION_NEW_PARCEL][QueryNames.COUNT_KEY])
        self.btn_missing_parcels.setEnabled(summary[CHANGE_DETECTION_MISSING_PARCEL][QueryNames.COUNT_KEY])
        self.btn_parcels_with_alphanumeric_changes.setEnabled(summary[CHANGE_DETECTION_PARCEL_CHANGED][QueryNames.COUNT_KEY])
        self.btn_parcels_with_only_geometry_changes.setEnabled(summary[CHANGE_DETECTION_PARCEL_ONLY_GEOMETRY_CHANGED][QueryNames.COUNT_KEY])
        self.btn_parcels_with_no_changes.setEnabled(summary[CHANGE_DETECTION_PARCEL_REMAINS][QueryNames.COUNT_KEY])
        self.btn_duplicated_parcels.setEnabled(summary[CHANGE_DETECTION_SEVERAL_PARCELS][QueryNames.COUNT_KEY])
        self.btn_null_parcel_numbers.setEnabled(summary[CHANGE_DETECTION_NULL_PARCEL][QueryNames.COUNT_KEY])
        self.btn_total_parcels.setEnabled(total_count)

        # Set button connections
        for button in [self.btn_new_parcels, self.btn_missing_parcels, self.btn_parcels_with_alphanumeric_changes,
                       self.btn_parcels_with_only_geometry_changes, self.btn_parcels_with_no_changes,
                       self.btn_duplicated_parcels, self.btn_null_parcel_numbers, self.btn_total_parcels]:
            try:
                button.clicked.disconnect()
            except:
                pass

        self.btn_new_parcels.clicked.connect(
            partial(self.parent.show_all_parcels_panel, summary, [CHANGE_DETECTION_NEW_PARCEL]))
        self.btn_missing_parcels.clicked.connect(
            partial(self.parent.show_all_parcels_panel, summary, [CHANGE_DETECTION_MISSING_PARCEL]))
        self.btn_parcels_with_alphanumeric_changes.clicked.connect(
            partial(self.parent.show_all_parcels_panel, summary, [CHANGE_DETECTION_PARCEL_CHANGED]))
        self.btn_parcels_with_only_geometry_changes.clicked.connect(
            partial(self.parent.show_all_parcels_panel, summary, [CHANGE_DETECTION_PARCEL_ONLY_GEOMETRY_CHANGED]))
        self.btn_parcels_with_no_changes.clicked.connect(
            partial(self.parent.show_all_parcels_panel, summary, [CHANGE_DETECTION_PARCEL_REMAINS]))
        self.btn_duplicated_parcels.clicked.connect(
            partial(self.parent.show_all_parcels_panel, summary, [CHANGE_DETECTION_SEVERAL_PARCELS]))
        self.btn_null_parcel_numbers.clicked.connect(
            partial(self.parent.show_all_parcels_panel, summary, [CHANGE_DETECTION_NULL_PARCEL]))
        self.btn_total_parcels.clicked.connect(
            partial(self.parent.show_all_parcels_panel, summary, [CHANGE_DETECTION_NEW_PARCEL,
                                                                  CHANGE_DETECTION_MISSING_PARCEL,
                                                                  CHANGE_DETECTION_PARCEL_CHANGED,
                                                                  CHANGE_DETECTION_PARCEL_ONLY_GEOMETRY_CHANGED,
                                                                  CHANGE_DETECTION_PARCEL_REMAINS,
                                                                  CHANGE_DETECTION_SEVERAL_PARCELS,
                                                                  CHANGE_DETECTION_NULL_PARCEL]))

        # Zoom to plot layer, remove selections
        self.utils._layers[self.utils._db.names.OP_PLOT_T][LAYER].removeSelection()
        self.utils._supplies_layers[self.utils._supplies_db.names.GC_PLOT_T][LAYER].removeSelection()
        self.utils.qgis_utils.activate_layer_requested.emit(self.utils._layers[self.utils._db.names.OP_PLOT_T][LAYER])
        self.utils.iface.zoomToActiveLayer()
