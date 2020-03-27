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
from qgis.PyQt.QtWidgets import (QTableWidgetItem,
                                 QApplication)
from qgis.core import (QgsWkbTypes,
                       QgsFeatureRequest,
                       QgsExpression,
                       QgsRectangle,
                       QgsGeometry,
                       QgsProject,
                       NULL)

from qgis.gui import (QgsPanelWidget,
                      QgsMapToolIdentifyFeature)

from asistente_ladm_col.config.layer_config import LayerConfig
from asistente_ladm_col.config.symbology import Symbology
from asistente_ladm_col.config.general_config import (SUPPLIES_DB_SOURCE,
                                                      COLLECTED_DB_SOURCE)
from asistente_ladm_col.config.gui.change_detection_config import (PLOT_GEOMETRY_KEY,
                                                                   DICT_KEY_PARTIES,
                                                                   PARCEL_NUMBER_SEARCH_KEY,
                                                                   PREVIOUS_PARCEL_NUMBER_SEARCH_KEY,
                                                                   FMI_PARCEL_SEARCH_KEY,
                                                                   get_collected_search_options,
                                                                   get_supplies_search_options,
                                                                   DICT_ALIAS_KEYS_CHANGE_DETECTION)
from asistente_ladm_col.gui.change_detection.dlg_select_duplicate_parcel_change_detection import SelectDuplicateParcelDialog
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.decorators import _with_override_cursor
from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('change_detection/changes_per_parcel_panel_widget.ui')


class ChangesPerParcelPanelWidget(QgsPanelWidget, WIDGET_UI):
    def __init__(self, parent, utils, parcel_number=None, collected_parcel_t_id=None):
        QgsPanelWidget.__init__(self, None)
        self.setupUi(self)
        self.parent = parent
        self.utils = utils
        self.logger = Logger()
        self.symbology = Symbology()

        self.setDockMode(True)
        self.setPanelTitle(QCoreApplication.translate("ChangesPerParcelPanelWidget", "Change detection per parcel"))

        self._current_supplies_substring = ""
        self._current_substring = ""

        self.utils.add_layers()
        self.fill_combos()

        # Remove selection in plot layers
        self.utils._layers[self.utils._db.names.OP_PLOT_T].removeSelection()
        self.utils._supplies_layers[self.utils._supplies_db.names.GC_PLOT_T].removeSelection()

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
            if collected_parcel_t_id is not None:  # Search data for a duplicated parcel_number, so, take the t_id into account!
                self.search_data(parcel_number=parcel_number, collected_parcel_t_id=collected_parcel_t_id)
            else:
                self.search_data(parcel_number=parcel_number)

    def btn_plot_toggled(self):
        self.clear_result_table()

        if self.btn_identify_plot.isChecked():
            self.prepare_identify_plot()
        else:
            # The button was toggled and deactivated, go back to the previous tool
            self.utils.canvas.setMapTool(self.active_map_tool_before_custom)

    def clear_result_table(self):
        self.tbl_changes_per_parcel.clearContents()
        self.tbl_changes_per_parcel.setRowCount(0)

    def prepare_identify_plot(self):
        """
            Custom Identify tool was activated, prepare everything for identifying plots
        """
        self.active_map_tool_before_custom = self.utils.canvas.mapTool()

        self.btn_identify_plot.setChecked(True)

        self.utils.canvas.mapToolSet.connect(self.initialize_maptool)

        if self.utils._supplies_layers[self.utils._supplies_db.names.GC_PLOT_T] is None:
            self.utils.add_layers()

        self.maptool_identify.setLayer(self.utils._supplies_layers[self.utils._supplies_db.names.GC_PLOT_T])
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
        """
        :param plot_feature: from supplies db
        """
        plot_t_id = plot_feature[self.utils._supplies_db.names.T_ID_F]

        self.utils.canvas.flashFeatureIds(self.utils._supplies_layers[self.utils._supplies_db.names.GC_PLOT_T],
                                    [plot_feature.id()],
                                    QColor(255, 0, 0, 255),
                                    QColor(255, 0, 0, 0),
                                    flashes=1,
                                    duration=500)

        if not self.isVisible():
            self.show()

        self.spatial_query(plot_t_id)
        self.utils._supplies_layers[self.utils._supplies_db.names.GC_PLOT_T].selectByIds([plot_feature.id()])

    def spatial_query(self, plot_id):
        if plot_id:
            parcel_number = self.utils.ladm_data.get_parcels_related_to_plots_supplies(self.utils._supplies_db, [plot_id], self.utils._supplies_db.names.GC_PARCEL_T_PARCEL_NUMBER_F)
            if parcel_number:  # Delegate handling of duplicates to search_data() method
                self.search_data(parcel_number=parcel_number[0])

    def call_party_panel(self, item):
        row = item.row()
        if self.tbl_changes_per_parcel.item(row, 0).text() == DICT_ALIAS_KEYS_CHANGE_DETECTION[DICT_KEY_PARTIES]:
            data = {SUPPLIES_DB_SOURCE: self.tbl_changes_per_parcel.item(row, 1).data(Qt.UserRole),
                    COLLECTED_DB_SOURCE: self.tbl_changes_per_parcel.item(row, 2).data(Qt.UserRole)}
            self.parent.show_party_panel(data)

    def search_field_updated(self, index=None):
        self.initialize_field_values_line_edit()

    def initialize_field_values_line_edit(self):
        # We search for alphanumeric data in supplies data source
        self.txt_alphanumeric_query.setLayer(self.utils._supplies_layers[self.utils._supplies_db.names.GC_PARCEL_T])
        search_option = self.cbo_parcel_fields.currentData()
        search_field_supplies = get_supplies_search_options(self.utils._supplies_db.names)[search_option]
        idx = self.utils._supplies_layers[self.utils._supplies_db.names.GC_PARCEL_T].fields().indexOf(search_field_supplies)
        self.txt_alphanumeric_query.setAttributeIndex(idx)

    def fill_combos(self):
        self.cbo_parcel_fields.clear()
        self.cbo_parcel_fields.addItem(QCoreApplication.translate("DockWidgetChanges", "Parcel Number"), PARCEL_NUMBER_SEARCH_KEY)
        self.cbo_parcel_fields.addItem(QCoreApplication.translate("DockWidgetChanges", "Previous Parcel Number"), PREVIOUS_PARCEL_NUMBER_SEARCH_KEY)
        self.cbo_parcel_fields.addItem(QCoreApplication.translate("DockWidgetChanges", "Folio de Matrícula Inmobiliaria"), FMI_PARCEL_SEARCH_KEY)

    @_with_override_cursor
    def search_data(self, **kwargs):
        """
        Get plot geometries associated with parcels, both collected and supplies, zoom to them, fill comparison table
        and activate map swipe tool.

        To fill the comparison table we build two search dicts, one for supplies (already given because the alphanumeric
        search is on supplies db source), and another one for collected. For the latter, we have 3 cases. We specify
        them below (inline).

        :param kwargs: key-value (field name-field value) to search in parcel tables, both collected and supplies
                       Normally, keys are parcel_number, old_parcel_number or FMI, but if duplicates are found, an
                       additional t_id disambiguates only for the collected source. In the supplies source we assume
                       we will not find duplicates, if there are, we will choose the first record found an will not deal
                       with letting the user choose one of the duplicates by hand (as we do for the collected source).
        """
        self.chk_show_all_plots.setEnabled(False)
        self.chk_show_all_plots.setChecked(True)
        self.initialize_tools_and_layers()  # Reset any filter on layers

        plots_supplies = list()
        plots_collected = list()
        self.clear_result_table()

        search_option = self.cbo_parcel_fields.currentData()
        search_field_supplies = get_supplies_search_options(self.utils._supplies_db.names)[search_option]
        search_field_collected = get_collected_search_options(self.utils._db.names)[search_option]
        search_value = list(kwargs.values())[0]


        # Build search criterion for both supplies and collected
        search_criterion_supplies = {search_field_supplies: search_value}

        # Get supplies parcel's t_id and get related plot(s)
        expression_supplies = QgsExpression("{}='{}'".format(search_field_supplies, search_value))
        request = QgsFeatureRequest(expression_supplies)
        field_idx = self.utils._supplies_layers[self.utils._supplies_db.names.GC_PARCEL_T].fields().indexFromName(self.utils._supplies_db.names.T_ID_F)
        request.setFlags(QgsFeatureRequest.NoGeometry)
        request.setSubsetOfAttributes([field_idx])  # Note: this adds a new flag
        supplies_parcels = [feature for feature in self.utils._supplies_layers[self.utils._supplies_db.names.GC_PARCEL_T].getFeatures(request)]

        if len(supplies_parcels) > 1:
            # We do not expect duplicates in the supplies source!
            pass  # We'll choose the first one anyways
        elif len(supplies_parcels) == 0:
            self.logger.info(__name__, "No supplies parcel found! Search: {}={}".format(search_field_supplies, search_value))

        supplies_plot_t_ids = []
        if supplies_parcels:
            supplies_plot_t_ids = self.utils.ladm_data.get_plots_related_to_parcels_supplies(self.utils._supplies_db,
                                              [supplies_parcels[0][self.utils._supplies_db.names.T_ID_F]],
                                              self.utils._supplies_db.names.T_ID_F,
                                              self.utils._supplies_layers[self.utils._supplies_db.names.GC_PLOT_T])

            if supplies_plot_t_ids:
                self._current_supplies_substring = "\"{}\" IN ('{}')".format(self.utils._supplies_db.names.T_ID_F, "','".join([str(t_id) for t_id in supplies_plot_t_ids]))
                plots_supplies = self.utils.ladm_data.get_features_from_t_ids(
                    self.utils._supplies_layers[self.utils._supplies_db.names.GC_PLOT_T],
                    self.utils._supplies_db.names.T_ID_F, supplies_plot_t_ids, True)


        # Now get COLLECTED parcel's t_id to build the search dict for collected
        collected_parcel_t_id = None
        if 'collected_parcel_t_id' in kwargs:
            # This is the case when this panel is called and we already know the parcel number is duplicated
            collected_parcel_t_id = kwargs['collected_parcel_t_id']
            search_criterion_collected = {self.utils._db.names.T_ID_F: collected_parcel_t_id}  # As there are duplicates, we need to use t_ids
        else:
            # This is the case when:
            #   + Either this panel was called and we know the parcel number is not duplicated, or
            #   + This panel was shown without knowing about duplicates (e.g., individual parcel search) and we still
            #     need to discover whether we have duplicates for this search criterion
            search_criterion_collected = {search_field_collected: search_value}

            expression_collected = QgsExpression("{}='{}'".format(search_field_collected, search_value))
            request = QgsFeatureRequest(expression_collected)
            request.setFlags(QgsFeatureRequest.NoGeometry)
            request.setSubsetOfAttributes([self.utils._db.names.T_ID_F],
                                          self.utils._layers[self.utils._db.names.OP_PARCEL_T].fields())  # Note this adds a new flag
            collected_parcels = self.utils._layers[self.utils._db.names.OP_PARCEL_T].getFeatures(request)
            collected_parcels_t_ids = [feature[self.utils._db.names.T_ID_F] for feature in collected_parcels]

            if collected_parcels_t_ids:
                collected_parcel_t_id = collected_parcels_t_ids[0]
                if len(collected_parcels_t_ids) > 1:  # Duplicates in collected source after a search
                    QApplication.restoreOverrideCursor()  # Make sure cursor is not waiting (it is if on an identify)
                    QCoreApplication.processEvents()
                    dlg_select_parcel = SelectDuplicateParcelDialog(self.utils, collected_parcels_t_ids, self.parent)
                    dlg_select_parcel.exec_()

                    if dlg_select_parcel.parcel_t_id:  # User selected one of the duplicated parcels
                        collected_parcel_t_id = dlg_select_parcel.parcel_t_id
                        search_criterion_collected = {self.utils._db.names.T_ID_F: collected_parcel_t_id}
                    else:
                        return  # User just cancelled the dialog, there is nothing more to do


        self.fill_table(search_criterion_supplies, search_criterion_collected)

        # Now get related plot(s) for both collected and supplies,
        if collected_parcel_t_id is not None:
            plot_t_ids = self.utils.ladm_data.get_plots_related_to_parcels(self.utils._db,
                                                                           [collected_parcel_t_id],
                                                                           self.utils._db.names.T_ID_F,
                                                                           plot_layer=self.utils._layers[self.utils._db.names.OP_PLOT_T],
                                                                           uebaunit_table=self.utils._layers[self.utils._db.names.COL_UE_BAUNIT_T])

            if plot_t_ids:
                self._current_substring = "{} IN ('{}')".format(self.utils._db.names.T_ID_F, "','".join([str(t_id) for t_id in plot_t_ids]))
                plots_collected = self.utils.ladm_data.get_features_from_t_ids(self.utils._layers[self.utils._db.names.OP_PLOT_T],
                                                                               self.utils._db.names.T_ID_F,
                                                                               plot_t_ids,
                                                                               True)

        # Zoom to combined extent
        plot_features = plots_supplies + plots_collected  # Feature list
        plots_extent = QgsRectangle()
        for plot in plot_features:
            plots_extent.combineExtentWith(plot.geometry().boundingBox())

        if not plots_extent.isEmpty():
            self.utils.iface.mapCanvas().zoomToFeatureExtent(plots_extent)

            if plots_supplies and plots_collected:  # Otherwise the map swipe tool doesn't add any value :)
                # Activate Swipe Tool
                self.utils.qgis_utils.activate_layer_requested.emit(self.utils._supplies_layers[self.utils._supplies_db.names.GC_PLOT_T])
                self.parent.activate_map_swipe_tool()

                # Send a custom mouse move on the map to make the map swipe tool's limit appear on the canvas
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

    def fill_table(self, search_criterion_supplies, search_criterion_collected):
        """
        Shouldn't handle 'inverse' mode as we won't switch table columns at runtime.

        :param search_criterion_supplies: key-value pair to build an expression to search data in the supplies source
        :param search_criterion_collected: key-value pair to build an expression to search data in the collected source
        :return:
        """
        plural = LayerConfig.get_dict_plural(self.utils._db.names)
        dict_collected_parcels = self.utils.ladm_data.get_parcel_data_to_compare_changes(self.utils._db, search_criterion_collected)

        # Custom layer modifiers
        layer_modifiers = {
            LayerConfig.PREFIX_LAYER_MODIFIERS: LayerConfig.SUPPLIES_DB_PREFIX,
            LayerConfig.SUFFIX_LAYER_MODIFIERS: LayerConfig.SUPPLIES_DB_SUFFIX,
            LayerConfig.STYLE_GROUP_LAYER_MODIFIERS: self.symbology.get_supplies_style_group(self.utils._supplies_db.names)
        }
        dict_supplies_parcels = self.utils.ladm_data.get_parcel_data_to_compare_changes_supplies(self.utils._supplies_db, search_criterion_supplies, layer_modifiers=layer_modifiers)

        # Before filling the table we make sure we get one and only one parcel attrs dict
        collected_attrs = dict()
        if dict_collected_parcels:
            collected_parcel_number = list(dict_collected_parcels.keys())[0]
            collected_attrs = dict_collected_parcels[collected_parcel_number][0]
            del collected_attrs[self.utils._db.names.T_ID_F]  # Remove this line if self.utils._db.names.T_ID_F is somehow needed

        supplies_attrs = dict()
        if dict_supplies_parcels:
            supplies_parcel_number = list(dict_supplies_parcels.keys())[0]
            supplies_attrs = dict_supplies_parcels[supplies_parcel_number][0]
            del supplies_attrs[self.utils._supplies_db.names.T_ID_F]  # Remove this line if self.utils._supplies_db.names,T_ID_F is somehow needed

        number_of_rows = len(collected_attrs) or len(supplies_attrs)
        self.tbl_changes_per_parcel.setRowCount(number_of_rows)  # t_id shouldn't be counted
        self.tbl_changes_per_parcel.setSortingEnabled(False)

        field_names = list(collected_attrs.keys()) if collected_attrs else list(supplies_attrs.keys())
        if PLOT_GEOMETRY_KEY in field_names:
            field_names.remove(PLOT_GEOMETRY_KEY)  # We'll handle plot geometry separately

        for row, field_name in enumerate(field_names):
            supplies_value = supplies_attrs[field_name] if field_name in supplies_attrs else NULL
            collected_value = collected_attrs[field_name] if field_name in collected_attrs else NULL
            field_alias = DICT_ALIAS_KEYS_CHANGE_DETECTION[field_name] if field_name in DICT_ALIAS_KEYS_CHANGE_DETECTION else field_name
            self.fill_row(field_alias, supplies_value, collected_value, row, plural)

        if number_of_rows:  # At least one row in the table?
            self.fill_geometry_row(PLOT_GEOMETRY_KEY,
                               supplies_attrs[PLOT_GEOMETRY_KEY] if PLOT_GEOMETRY_KEY in supplies_attrs else QgsGeometry(),
                               collected_attrs[PLOT_GEOMETRY_KEY] if PLOT_GEOMETRY_KEY in collected_attrs else QgsGeometry(),
                               number_of_rows - 1)

        self.tbl_changes_per_parcel.setSortingEnabled(True)

    def fill_row(self, field_name, supplies_value, collected_value, row, plural):
        item = QTableWidgetItem(field_name)
        # item.setData(Qt.UserRole, parcel_attrs[self.names.T_ID_F])
        self.tbl_changes_per_parcel.setItem(row, 0, item)

        if field_name == DICT_ALIAS_KEYS_CHANGE_DETECTION[DICT_KEY_PARTIES]:
            item = self.fill_party_item(supplies_value)
            self.tbl_changes_per_parcel.setItem(row, 1, item)

            item = self.fill_party_item(collected_value)
            self.tbl_changes_per_parcel.setItem(row, 2, item)

            self.tbl_changes_per_parcel.setItem(row, 3, QTableWidgetItem())
            self.tbl_changes_per_parcel.item(row, 3).setBackground(Qt.green if supplies_value == collected_value else Qt.red)
        else:
            item = QTableWidgetItem(str(supplies_value) if supplies_value != NULL else '')
            #item.setData(Qt.UserRole, parcel_attrs[self.names.T_ID_F])
            self.tbl_changes_per_parcel.setItem(row, 1, item)

            item = QTableWidgetItem(str(collected_value) if collected_value != NULL else '')
            # item.setData(Qt.UserRole, parcel_attrs[self.names.T_ID_F])
            self.tbl_changes_per_parcel.setItem(row, 2, item)

            self.tbl_changes_per_parcel.setItem(row, 3, QTableWidgetItem())
            self.tbl_changes_per_parcel.item(row, 3).setBackground(Qt.green if supplies_value == collected_value else Qt.red)

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

    def fill_geometry_row(self, field_name, supplies_geom, collected_geom, row):
        self.tbl_changes_per_parcel.setItem(row, 0, QTableWidgetItem(QCoreApplication.translate("DockWidgetChanges", "Geometry")))
        self.tbl_changes_per_parcel.setItem(row, 1, QTableWidgetItem(self.get_geometry_type_name(supplies_geom)))
        self.tbl_changes_per_parcel.setItem(row, 2, QTableWidgetItem(self.get_geometry_type_name(collected_geom)))

        self.tbl_changes_per_parcel.setItem(row, 3, QTableWidgetItem())
        self.tbl_changes_per_parcel.item(row, 3).setBackground(
            Qt.green if self.utils.compare_features_geometries(collected_geom, supplies_geom) else Qt.red)

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
        Alphanumeric query (On supplies db)
        """
        option = self.cbo_parcel_fields.currentData()
        query = self.txt_alphanumeric_query.value()
        if query:
            if option == FMI_PARCEL_SEARCH_KEY:
                self.search_data(parcel_fmi=query)
            elif option == PARCEL_NUMBER_SEARCH_KEY:
                self.search_data(parcel_number=query)
            else: # previous_parcel_number
                self.search_data(previous_parcel_number=query)

        else:
            self.utils.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("DockWidgetChanges", "First enter a query"))

    def show_all_plots(self, state):
        try:
            self.utils._supplies_layers[self.utils._supplies_db.names.GC_PLOT_T].setSubsetString(self._current_supplies_substring if not state else "")
        except RuntimeError:  # If the layer was previously removed
            pass

        try:
            self.utils._layers[self.utils._db.names.OP_PLOT_T].setSubsetString(self._current_substring if not state else "")
        except RuntimeError:  # If the layer was previously removed
            pass

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
        self.show_all_plots(True)  # Remove filter in plots layers if it was activate and panel is closed
        # custom identify was deactivated
        try:
            self.utils.canvas.mapToolSet.disconnect(self.initialize_maptool)
        except TypeError as e:
            pass

        self.utils.canvas.setMapTool(self.init_map_tool)
