# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-05-16
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
from qgis.PyQt.QtWidgets import QTableWidgetItem
from qgis.core import (QgsWkbTypes,
                       Qgis,
                       QgsMessageLog,
                       QgsFeature,
                       QgsFeatureRequest,
                       QgsExpression,
                       QgsRectangle)

from qgis.gui import QgsPanelWidget
from ...config.symbology import OFFICIAL_STYLE_GROUP
from asistente_ladm_col.config.general_config import (OFFICIAL_DB_PREFIX,
                                                      OFFICIAL_DB_SUFFIX,
                                                      PREFIX_LAYER_MODIFIERS,
                                                      SUFFIX_LAYER_MODIFIERS,
                                                      STYLE_GROUP_LAYER_MODIFIERS)
from asistente_ladm_col.config.table_mapping_config import (PARCEL_NUMBER_FIELD,
                                                            PARCEL_NUMBER_BEFORE_FIELD,
                                                            FMI_FIELD,
                                                            ID_FIELD, PARCEL_TABLE, PLOT_TABLE, UEBAUNIT_TABLE)
from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('change_detection/changes_per_parcel_panel_widget.ui')

class ChangesPerParcelPanelWidget(QgsPanelWidget, WIDGET_UI):
    def __init__(self, parent, utils, parcel_number=None):
        QgsPanelWidget.__init__(self, None)
        self.setupUi(self)
        self.parent = parent
        self.utils = utils

        self.setDockMode(True)

        self._current_official_substring = ""
        self._current_substring = ""

        self.utils.add_layers()
        self.fill_combos()

        self.tab_plot_options.setTabEnabled(0, False)

        # Set connections
        self.btn_alphanumeric_query.clicked.connect(self.alphanumeric_query)
        self.chk_show_all_plots.toggled.connect(self.show_all_plots)
        self.cbo_parcel_fields.currentIndexChanged.connect(self.search_field_updated)
        self.panelAccepted.connect(self.initialize_tools_and_layers)

        self.initialize_field_values_line_edit()
        self.initialize_tools_and_layers()

        if parcel_number is not None:  # Do a search!
            self.txt_alphanumeric_query.setValue(parcel_number)
            self.search_data(parcel_number=parcel_number)

    def search_field_updated(self, index=None):
        self.initialize_field_values_line_edit()

    def initialize_field_values_line_edit(self):
        self.txt_alphanumeric_query.setLayer(self.utils._official_layers[PARCEL_TABLE]['layer'])
        idx = self.utils._official_layers[PARCEL_TABLE]['layer'].fields().indexOf(self.cbo_parcel_fields.currentData())
        self.txt_alphanumeric_query.setAttributeIndex(idx)

    def fill_combos(self):
        self.cbo_parcel_fields.clear()

        self.cbo_parcel_fields.addItem(QCoreApplication.translate("DockWidgetChanges", "Parcel Number"), PARCEL_NUMBER_FIELD)
        self.cbo_parcel_fields.addItem(QCoreApplication.translate("DockWidgetChanges", "Previous Parcel Number"), PARCEL_NUMBER_BEFORE_FIELD)
        self.cbo_parcel_fields.addItem(QCoreApplication.translate("DockWidgetChanges", "Folio de Matrícula Inmobiliaria"), FMI_FIELD)

    def search_data(self, **kwargs):
        """
        Get plot geometries associated with parcels, both collected and official, zoom to them, activate map swipe tool
            and fill comparison table.

        :param kwargs: key-value (field name-field value) to search in parcel tables, both collected and official
        """
        self.chk_show_all_plots.setEnabled(False)
        self.chk_show_all_plots.setChecked(True)
        self.initialize_tools_and_layers()  # Reset any filter on layers
        already_zoomed_in = False

        search_field = self.cbo_parcel_fields.currentData()
        search_value = list(kwargs.values())[0]

        # Get OFFICIAL parcel's t_id and get related plot(s)
        request = QgsFeatureRequest(QgsExpression("{}='{}'".format(search_field, search_value)))
        field_idx = self.utils._official_layers[PARCEL_TABLE]['layer'].fields().indexFromName(ID_FIELD)
        request.setSubsetOfAttributes([field_idx])
        request.setFlags(QgsFeatureRequest.NoGeometry)
        official_parcels = [feature for feature in self.utils._official_layers[PARCEL_TABLE]['layer'].getFeatures(request)]

        if len(official_parcels) > 1:
            # TODO: Show dialog to select only one
            pass
        elif len(official_parcels) == 0:
            print("No parcel found!", search_field, search_value)

        self.fill_table({search_field: search_value})

        official_plot_t_ids = []
        if official_parcels:
            official_plot_t_ids = self.utils.ladm_data.get_plots_related_to_parcels(self.utils._official_db,
                                              [official_parcels[0][ID_FIELD]],
                                              field_name = ID_FIELD,
                                              plot_layer = self.utils._official_layers[PLOT_TABLE]['layer'],
                                              uebaunit_table = self.utils._official_layers[UEBAUNIT_TABLE]['layer'])

            if official_plot_t_ids:
                self._current_official_substring = "\"{}\" IN ('{}')".format(ID_FIELD, "','".join([str(t_id) for t_id in official_plot_t_ids]))
                self.parent.request_zoom_to_features(self.utils._official_layers[PLOT_TABLE]['layer'], list(), official_plot_t_ids)
                already_zoomed_in = True

        # Now get COLLECTED parcel's t_id and get related plot(s)
        request = QgsFeatureRequest(QgsExpression("{}='{}'".format(search_field, search_value)))
        field_idx = self.utils._layers[PARCEL_TABLE]['layer'].fields().indexFromName(ID_FIELD)
        request.setSubsetOfAttributes([field_idx])
        request.setFlags(QgsFeatureRequest.NoGeometry)
        parcels = self.utils._layers[PARCEL_TABLE]['layer'].getFeatures(request)
        parcel = QgsFeature()
        res = parcels.nextFeature(parcel)

        if res:
            plot_t_ids = self.utils.ladm_data.get_plots_related_to_parcels(self.utils._db,
                                                                     [parcel[ID_FIELD]],
                                                                     field_name=ID_FIELD,
                                                                     plot_layer=self.utils._layers[PLOT_TABLE]['layer'],
                                                                     uebaunit_table=self.utils._layers[UEBAUNIT_TABLE]['layer'])
            if plot_t_ids:
                self._current_substring = "{} IN ('{}')".format(ID_FIELD, "','".join([str(t_id) for t_id in plot_t_ids]))
                if not already_zoomed_in:
                    self.parent.request_zoom_to_features(self.utils._layers[PLOT_TABLE]['layer'], list(), plot_t_ids)

                # Send a custom mouse move on the map to make the map swipe tool's limit appear on the canvas

                # Activate Swipe Tool
                self.utils.qgis_utils.activate_layer_requested.emit(self.utils._official_layers[PLOT_TABLE]['layer'])
                if official_plot_t_ids:  # Otherwise the map swipe tool doesn't add any value :)
                    self.parent.activate_map_swipe_tool()

                    plots = self.utils.ladm_data.get_features_from_t_ids(self.utils._layers[PLOT_TABLE]['layer'], plot_t_ids, True)
                    plots_extent = QgsRectangle()
                    for plot in plots:
                        plots_extent.combineExtentWith(plot.geometry().boundingBox())

                    coord_x = plots_extent.xMaximum() - (plots_extent.xMaximum() - plots_extent.xMinimum()) / 9  # 90%
                    coord_y = plots_extent.yMaximum() - (plots_extent.yMaximum() - plots_extent.yMinimum()) / 2  # 50%

                    coord_transform = self.utils.iface.mapCanvas().getCoordinateTransform()
                    map_point = coord_transform.transform(coord_x, coord_y)
                    widget_point = map_point.toQPointF().toPoint()
                    global_point = self.utils.canvas.mapToGlobal(widget_point)

                    self.utils.canvas.mousePressEvent(QMouseEvent(QEvent.MouseButtonPress, global_point, Qt.LeftButton, Qt.LeftButton, Qt.NoModifier))
                    self.utils.canvas.mouseMoveEvent(QMouseEvent(QEvent.MouseMove, widget_point + QPoint(1,0), Qt.NoButton, Qt.LeftButton, Qt.NoModifier))
                    self.utils.canvas.mouseReleaseEvent(QMouseEvent(QEvent.MouseButtonRelease, widget_point + QPoint(1,0), Qt.LeftButton, Qt.LeftButton, Qt.NoModifier))

        # Once the query is done, activate the checkbox to alternate all plots/only selected plot
        self.chk_show_all_plots.setEnabled(True)

    def fill_table(self, search_criterion):  # Shouldn't handle 'inverse' mode
        dict_collected_parcels = self.utils.ladm_data.get_parcel_data_to_compare_changes(self.utils._db, search_criterion)

        # Custom layer modifiers
        layer_modifiers = {
            PREFIX_LAYER_MODIFIERS: OFFICIAL_DB_PREFIX,
            SUFFIX_LAYER_MODIFIERS: OFFICIAL_DB_SUFFIX,
            STYLE_GROUP_LAYER_MODIFIERS: OFFICIAL_STYLE_GROUP
        }

        dict_official_parcels = self.utils.ladm_data.get_parcel_data_to_compare_changes(self.utils._official_db, search_criterion, layer_modifiers=layer_modifiers)

        # Before filling the table we make sure we get one and only one parcel attrs dict
        collected_attrs = dict()
        if dict_collected_parcels:
            collected_parcel_number = list(dict_collected_parcels.keys())[0]
            collected_attrs = dict_collected_parcels[collected_parcel_number][0]
            del collected_attrs[ID_FIELD]  # Remove this line if ID_FIELD is somehow needed

        official_attrs = dict()
        if dict_official_parcels:
            official_parcel_number = list(dict_official_parcels.keys())[0]
            official_attrs = dict_official_parcels[official_parcel_number][0] if dict_official_parcels else []
            del official_attrs[ID_FIELD]  # Remove this line if ID_FIELD is somehow needed

        self.tbl_changes_per_parcel.clearContents()
        self.tbl_changes_per_parcel.setRowCount(len(collected_attrs) or len(official_attrs))  # t_id shouldn't be counted
        self.tbl_changes_per_parcel.setSortingEnabled(False)

        field_names = list(collected_attrs.keys()) if collected_attrs else list(official_attrs.keys())

        for row, field_name in enumerate(field_names):
            item = QTableWidgetItem(field_name)
            # item.setData(Qt.UserRole, parcel_attrs[ID_FIELD])
            self.tbl_changes_per_parcel.setItem(row, 0, item)

            official_value = official_attrs[field_name] if field_name in official_attrs else ''
            collected_value = collected_attrs[field_name] if field_name in collected_attrs else ''

            item = QTableWidgetItem(str(official_value))
            #item.setData(Qt.UserRole, parcel_attrs[ID_FIELD])
            self.tbl_changes_per_parcel.setItem(row, 1, item)

            item = QTableWidgetItem(str(collected_value))
            # item.setData(Qt.UserRole, parcel_attrs[ID_FIELD])
            self.tbl_changes_per_parcel.setItem(row, 2, item)

            self.tbl_changes_per_parcel.setItem(row, 3, QTableWidgetItem())
            self.tbl_changes_per_parcel.item(row, 3).setBackground(Qt.green if official_value == collected_value else Qt.red)

        self.tbl_changes_per_parcel.setSortingEnabled(True)

    def alphanumeric_query(self):
        """
        Alphanumeric query
        """
        option = self.cbo_parcel_fields.currentData()
        query = self.txt_alphanumeric_query.value()
        if query:
            if option == FMI_FIELD:
                self.search_data(parcel_fmi=query)
            elif option == PARCEL_NUMBER_FIELD:
                self.search_data(parcel_number=query)
            else: # previous_parcel_number
                self.search_data(previous_parcel_number=query)

        else:
            self.utils.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("DockWidgetChanges", "First enter a query"))

    def show_all_plots(self, state):
        self.utils._official_layers[PLOT_TABLE]['layer'].setSubsetString(self._current_official_substring if not state else "")
        self.utils._layers[PLOT_TABLE]['layer'].setSubsetString(self._current_substring if not state else "")

    def initialize_tools_and_layers(self, panel=None):
        self.parent.deactivate_map_swipe_tool()
        self.show_all_plots(True)