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
from qgis.PyQt.QtGui import (QMouseEvent,
                             QIcon,
                             QColor,
                             QCursor)
from qgis.PyQt.QtCore import (QCoreApplication,
                              Qt,
                              QEvent,
                              QPoint)
from qgis.PyQt.QtWidgets import QTableWidgetItem
from qgis.core import (QgsWkbTypes,
                       QgsFeature,
                       QgsFeatureRequest,
                       QgsExpression,
                       QgsRectangle,
                       QgsGeometry,
                       NULL)

from qgis.gui import (QgsPanelWidget,
                      QgsMapToolIdentifyFeature)
from ...config.symbology import OFFICIAL_STYLE_GROUP
from ...config.general_config import (OFFICIAL_DB_PREFIX,
                                      OFFICIAL_DB_SUFFIX,
                                      PREFIX_LAYER_MODIFIERS,
                                      SUFFIX_LAYER_MODIFIERS,
                                      STYLE_GROUP_LAYER_MODIFIERS,
                                      OFFICIAL_DB_SOURCE,
                                      COLLECTED_DB_SOURCE,
                                      LAYER,
                                      PLOT_GEOMETRY_KEY)
from ...config.table_mapping_config import (PARCEL_NUMBER_FIELD,
                                            PARCEL_NUMBER_BEFORE_FIELD,
                                            FMI_FIELD,
                                            ID_FIELD,
                                            PARCEL_TABLE,
                                            PLOT_TABLE,
                                            UEBAUNIT_TABLE,
                                            COL_PARTY_TABLE,
                                            DICT_PLURAL)
from .dlg_select_duplicate_parcel_change_detection import SelectDuplicateParcelDialog
from ...utils.qt_utils import OverrideCursor
from ...utils import get_ui_class

WIDGET_UI = get_ui_class('change_detection/changes_per_parcel_panel_widget.ui')


class ChangesPerParcelPanelWidget(QgsPanelWidget, WIDGET_UI):
    def __init__(self, parent, utils, parcel_number=None, parcel_id=None):
        QgsPanelWidget.__init__(self, None)
        self.setupUi(self)
        self.parent = parent
        self.utils = utils

        self.setDockMode(True)

        self._current_official_substring = ""
        self._current_substring = ""

        self.utils.add_layers()
        self.fill_combos()

        # Remove selection in plot layers
        self.utils._layers[PLOT_TABLE][LAYER].removeSelection()
        self.utils._official_layers[PLOT_TABLE][LAYER].removeSelection()

        # Map tool before activate map swipe tool
        self.init_map_tool = self.utils.canvas.mapTool()

        self.active_map_tool_before_custom = None
        self.btn_identify_plot.setIcon(QIcon(":/Asistente-LADM_COL/resources/images/spatial_unit.png"))
        self.btn_identify_plot.clicked.connect(self.btn_plot_toggled)

        # Create maptool
        self.maptool_identify = QgsMapToolIdentifyFeature(self.utils.canvas)

        # Set connections
        self.btn_alphanumeric_query.clicked.connect(self.alphanumeric_query)
        self.chk_show_all_plots.toggled.connect(self.show_all_plots)
        self.cbo_parcel_fields.currentIndexChanged.connect(self.search_field_updated)
        self.panelAccepted.connect(self.initialize_tools_and_layers)
        self.tbl_changes_per_parcel.itemDoubleClicked.connect(self.call_party_panel)

        self.initialize_field_values_line_edit()
        self.initialize_tools_and_layers()

        if parcel_number is not None:  # Do a search!
            self.txt_alphanumeric_query.setValue(parcel_number)
            if parcel_id is not None:
                self.search_data(parcel_number=parcel_number, parcel_id=parcel_id)
            else:
                self.search_data(parcel_number=parcel_number)

    def btn_plot_toggled(self):
        self.tbl_changes_per_parcel.clearContents()
        self.tbl_changes_per_parcel.setRowCount(0)

        if self.btn_identify_plot.isChecked():
            self.prepare_identify_plot()
        else:
            # The button was toggled and deactivated, go back to the previous tool
            self.utils.canvas.setMapTool(self.active_map_tool_before_custom)

    def prepare_identify_plot(self):
        """
            Custom Identify tool was activated, prepare everything for identifying plots
        """
        self.active_map_tool_before_custom = self.utils.canvas.mapTool()

        self.btn_identify_plot.setChecked(True)

        self.utils.canvas.mapToolSet.connect(self.initialize_maptool)

        if self.utils._official_layers[PLOT_TABLE][LAYER] is None:
            self.utils.add_layers()

        self.maptool_identify.setLayer(self.utils._official_layers[PLOT_TABLE][LAYER])
        cursor = QCursor()
        cursor.setShape(Qt.PointingHandCursor)
        self.maptool_identify.setCursor(cursor)
        self.utils.canvas.setMapTool(self.maptool_identify)

        try:
            self.maptool_identify.featureIdentified.disconnect()
        except TypeError as e:
            pass
        self.maptool_identify.featureIdentified.connect(self.get_info_by_plot)

    def get_info_by_plot(self, plot_feature):
        plot_t_id = plot_feature[ID_FIELD]

        self.utils.canvas.flashFeatureIds(self.utils._official_layers[PLOT_TABLE][LAYER],
                                    [plot_feature.id()],
                                    QColor(255, 0, 0, 255),
                                    QColor(255, 0, 0, 0),
                                    flashes=1,
                                    duration=500)

        with OverrideCursor(Qt.WaitCursor):
            if not self.isVisible():
                self.show()

            self.spatial_query(plot_t_id)
            #self.search_data_by_component(plot_t_id=plot_t_id, zoom_and_select=False)
            self.utils._official_layers[PLOT_TABLE][LAYER].selectByIds([plot_feature.id()])

    def spatial_query(self, plot_id):
        if plot_id:
            parcel_number = self.utils.ladm_data.get_parcels_related_to_plots(self.utils._official_db, [plot_id], PARCEL_NUMBER_FIELD)
            if parcel_number:
                self.search_data(parcel_number=parcel_number[0])

    def call_party_panel(self, item):
        row = item.row()
        if self.tbl_changes_per_parcel.item(row, 0).text() == DICT_PLURAL[COL_PARTY_TABLE]:
            data = {OFFICIAL_DB_SOURCE: self.tbl_changes_per_parcel.item(row, 1).data(Qt.UserRole),
                    COLLECTED_DB_SOURCE: self.tbl_changes_per_parcel.item(row, 2).data(Qt.UserRole)}
            self.parent.show_party_panel(data)

    def search_field_updated(self, index=None):
        self.initialize_field_values_line_edit()

    def initialize_field_values_line_edit(self):
        self.txt_alphanumeric_query.setLayer(self.utils._official_layers[PARCEL_TABLE][LAYER])
        idx = self.utils._official_layers[PARCEL_TABLE][LAYER].fields().indexOf(self.cbo_parcel_fields.currentData())
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
        parcel_id = None

        search_field = self.cbo_parcel_fields.currentData()
        search_value = list(kwargs.values())[0]

        # Get OFFICIAL parcel's t_id and get related plot(s)
        request = QgsFeatureRequest(QgsExpression("{}='{}'".format(search_field, search_value)))
        field_idx = self.utils._official_layers[PARCEL_TABLE][LAYER].fields().indexFromName(ID_FIELD)
        request.setSubsetOfAttributes([field_idx])
        request.setFlags(QgsFeatureRequest.NoGeometry)
        official_parcels = [feature for feature in self.utils._official_layers[PARCEL_TABLE][LAYER].getFeatures(request)]

        if len(official_parcels) > 1:
            # We do not expect duplicates in the official source!
            pass
        elif len(official_parcels) == 0:
            print("No parcel found!", search_field, search_value)

        official_plot_t_ids = []
        if official_parcels:
            official_plot_t_ids = self.utils.ladm_data.get_plots_related_to_parcels(self.utils._official_db,
                                              [official_parcels[0][ID_FIELD]],
                                              field_name = ID_FIELD,
                                              plot_layer = self.utils._official_layers[PLOT_TABLE][LAYER],
                                              uebaunit_table = self.utils._official_layers[UEBAUNIT_TABLE][LAYER])

            if official_plot_t_ids:
                self._current_official_substring = "\"{}\" IN ('{}')".format(ID_FIELD, "','".join([str(t_id) for t_id in official_plot_t_ids]))
                self.parent.request_zoom_to_features(self.utils._official_layers[PLOT_TABLE][LAYER], list(), official_plot_t_ids)
                already_zoomed_in = True

        # Now get COLLECTED parcel's t_id and get related plot(s)
        if 'parcel_id' in kwargs and kwargs['parcel_id']:
            parcel_id = kwargs['parcel_id']
            expression = "{}={}".format(ID_FIELD, kwargs['parcel_id'])
            search_criterion_collected = {ID_FIELD: kwargs['parcel_id']}
        else:
            expression = "{}='{}'".format(search_field, search_value)
            search_criterion_collected = {search_field: search_value}

        search_criterion_official = {search_field: search_value}

        request = QgsFeatureRequest(QgsExpression(expression))
        field_idx = self.utils._layers[PARCEL_TABLE][LAYER].fields().indexFromName(ID_FIELD)
        request.setSubsetOfAttributes([field_idx])
        request.setFlags(QgsFeatureRequest.NoGeometry)
        parcels = self.utils._layers[PARCEL_TABLE][LAYER].getFeatures(request)
        parcels_id = [feature[ID_FIELD] for feature in parcels]

        if parcels_id and 'parcel_id' not in kwargs:
            parcel_id = parcels_id[0]
            if len(parcels_id) >= 2:
                dlg_select_parcel = SelectDuplicateParcelDialog(self.utils, parcels_id, self.parent)
                dlg_select_parcel.exec_()

                parcel_id = dlg_select_parcel.parcel_id
                search_criterion_collected = {ID_FIELD: dlg_select_parcel.parcel_id}

        self.fill_table(search_criterion_collected, search_criterion_official)
        if parcel_id:
            plot_t_ids = self.utils.ladm_data.get_plots_related_to_parcels(self.utils._db,
                                                                           [parcel_id],
                                                                           field_name=ID_FIELD,
                                                                           plot_layer=self.utils._layers[PLOT_TABLE][LAYER],
                                                                           uebaunit_table=self.utils._layers[UEBAUNIT_TABLE][LAYER])
            if plot_t_ids:
                self._current_substring = "{} IN ('{}')".format(ID_FIELD, "','".join([str(t_id) for t_id in plot_t_ids]))
                if not already_zoomed_in:
                    self.parent.request_zoom_to_features(self.utils._layers[PLOT_TABLE][LAYER], list(), plot_t_ids)

                # Selected features in collected db
                # exp_select_plots = "{} IN ({})".format(ID_FIELD, ",".join([str(plot_t_id) for plot_t_id in plot_t_ids]))
                # self.utils._layers[PLOT_TABLE][LAYER].selectByExpression(exp_select_plots)

                # Send a custom mouse move on the map to make the map swipe tool's limit appear on the canvas

                # Activate Swipe Tool
                self.utils.qgis_utils.activate_layer_requested.emit(self.utils._official_layers[PLOT_TABLE][LAYER])
                if official_plot_t_ids:  # Otherwise the map swipe tool doesn't add any value :)
                    self.parent.activate_map_swipe_tool()

                    plots = self.utils.ladm_data.get_features_from_t_ids(self.utils._layers[PLOT_TABLE][LAYER], plot_t_ids, True)
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

    def fill_table(self, search_criterion_collected, search_criterion_official):  # Shouldn't handle 'inverse' mode as we won't switch table columns at runtime
        dict_collected_parcels = self.utils.ladm_data.get_parcel_data_to_compare_changes(self.utils._db, search_criterion_collected)

        # Custom layer modifiers
        layer_modifiers = {
            PREFIX_LAYER_MODIFIERS: OFFICIAL_DB_PREFIX,
            SUFFIX_LAYER_MODIFIERS: OFFICIAL_DB_SUFFIX,
            STYLE_GROUP_LAYER_MODIFIERS: OFFICIAL_STYLE_GROUP
        }
        dict_official_parcels = self.utils.ladm_data.get_parcel_data_to_compare_changes(self.utils._official_db, search_criterion_official, layer_modifiers=layer_modifiers)

        # Before filling the table we make sure we get one and only one parcel attrs dict
        collected_attrs = dict()
        if dict_collected_parcels:
            collected_parcel_number = list(dict_collected_parcels.keys())[0]
            collected_attrs = dict_collected_parcels[collected_parcel_number][0]
            del collected_attrs[ID_FIELD]  # Remove this line if ID_FIELD is somehow needed

        official_attrs = dict()
        if dict_official_parcels:
            official_parcel_number = list(dict_official_parcels.keys())[0]
            official_attrs = dict_official_parcels[official_parcel_number][0]
            del official_attrs[ID_FIELD]  # Remove this line if ID_FIELD is somehow needed

        self.tbl_changes_per_parcel.clearContents()
        number_of_rows = len(collected_attrs) or len(official_attrs)
        self.tbl_changes_per_parcel.setRowCount(number_of_rows)  # t_id shouldn't be counted
        self.tbl_changes_per_parcel.setSortingEnabled(False)

        field_names = list(collected_attrs.keys()) if collected_attrs else list(official_attrs.keys())
        if PLOT_GEOMETRY_KEY in field_names:
            field_names.remove(PLOT_GEOMETRY_KEY)  # We'll handle plot geometry separately

        for row, field_name in enumerate(field_names):
            official_value = official_attrs[field_name] if field_name in official_attrs else NULL
            collected_value = collected_attrs[field_name] if field_name in collected_attrs else NULL

            self.fill_row(field_name, official_value, collected_value, row)

        if number_of_rows:  # At least one row in the table?
            self.fill_geometry_row(PLOT_GEOMETRY_KEY,
                               official_attrs[PLOT_GEOMETRY_KEY] if PLOT_GEOMETRY_KEY in official_attrs else QgsGeometry(),
                               collected_attrs[PLOT_GEOMETRY_KEY] if PLOT_GEOMETRY_KEY in collected_attrs else QgsGeometry(),
                               number_of_rows - 1)

        self.tbl_changes_per_parcel.setSortingEnabled(True)

    def fill_row(self, field_name, official_value, collected_value, row):
        item = QTableWidgetItem(field_name)
        # item.setData(Qt.UserRole, parcel_attrs[ID_FIELD])
        self.tbl_changes_per_parcel.setItem(row, 0, item)

        if field_name == DICT_PLURAL[COL_PARTY_TABLE]:  # Parties
            item = self.fill_party_item(official_value)
            self.tbl_changes_per_parcel.setItem(row, 1, item)

            item = self.fill_party_item(collected_value)
            self.tbl_changes_per_parcel.setItem(row, 2, item)

            self.tbl_changes_per_parcel.setItem(row, 3, QTableWidgetItem())
            self.tbl_changes_per_parcel.item(row, 3).setBackground(Qt.green if official_value == collected_value else Qt.red)
        else:
            item = QTableWidgetItem(str(official_value) if official_value != NULL else '')
            #item.setData(Qt.UserRole, parcel_attrs[ID_FIELD])
            self.tbl_changes_per_parcel.setItem(row, 1, item)

            item = QTableWidgetItem(str(collected_value) if collected_value != NULL else '')
            # item.setData(Qt.UserRole, parcel_attrs[ID_FIELD])
            self.tbl_changes_per_parcel.setItem(row, 2, item)

            self.tbl_changes_per_parcel.setItem(row, 3, QTableWidgetItem())
            self.tbl_changes_per_parcel.item(row, 3).setBackground(Qt.green if official_value == collected_value else Qt.red)

    def fill_party_item(self, value):
        # Party's info comes in a list or a list of lists if it's a group party
        display_value = ''

        if value != NULL:
            if type(value) is list and value:
                display_value = "{} {}".format(len(value),
                                               QCoreApplication.translate("DockWidgetChanges", "parties") if len(value)>1 else QCoreApplication.translate("DockWidgetChanges", "party"))
        #else:
        #    display_value = QCoreApplication.translate("DockWidgetChanges", "0 parties")

        item = QTableWidgetItem(display_value)
        item.setData(Qt.UserRole, value)
        return item

    def fill_geometry_row(self, field_name, official_geom, collected_geom, row):
        self.tbl_changes_per_parcel.setItem(row, 0, QTableWidgetItem(QCoreApplication.translate("DockWidgetChanges", "Geometry")))
        self.tbl_changes_per_parcel.setItem(row, 1, QTableWidgetItem(self.get_geometry_type_name(official_geom)))
        self.tbl_changes_per_parcel.setItem(row, 2, QTableWidgetItem(self.get_geometry_type_name(collected_geom)))

        self.tbl_changes_per_parcel.setItem(row, 3, QTableWidgetItem())
        self.tbl_changes_per_parcel.item(row, 3).setBackground(
            Qt.green if self.utils.compare_features_geometries(collected_geom, official_geom) else Qt.red)

    @staticmethod
    def get_geometry_type_name(geometry):
        if geometry is None:
            return QCoreApplication.translate("DockWidgetChanges", "No associated plot")
        elif geometry.type() == QgsWkbTypes.UnknownGeometry:
            return ''
        elif geometry.type() == QgsWkbTypes.PolygonGeometry:
            return QCoreApplication.translate("DockWidgetChanges", "Polygon")
        else:
            return "Type: {}".format(geometry.type())

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
        self.utils._official_layers[PLOT_TABLE][LAYER].setSubsetString(self._current_official_substring if not state else "")
        self.utils._layers[PLOT_TABLE][LAYER].setSubsetString(self._current_substring if not state else "")

    def initialize_tools_and_layers(self, panel=None):
        self.parent.deactivate_map_swipe_tool()
        self.show_all_plots(True)

    def initialize_maptool(self, new_tool, old_tool):
        if self.maptool_identify == old_tool:
            # custom identify was deactivated
            try:
                self.utils.canvas.mapToolSet.disconnect(self.initialize_maptool)
            except TypeError as e:
                pass

            self.btn_identify_plot.setChecked(False)
        else:
            # custom identify was activated
            pass

    def close_panel(self):
        # custom identify was deactivated
        try:
            self.utils.canvas.mapToolSet.disconnect(self.initialize_maptool)
        except TypeError as e:
            pass

        self.utils.canvas.setMapTool(self.init_map_tool)
