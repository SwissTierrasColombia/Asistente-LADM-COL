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
import qgis
from qgis.PyQt.QtCore import (Qt,
                              pyqtSignal,
                              QCoreApplication,
                              QObject)
from qgis.core import (QgsVectorLayer,
                       Qgis,
                       NULL,
                       QgsGeometry)
from qgis.gui import QgsDockWidget

from asistente_ladm_col.gui.change_detection.changes_all_parcels_panel import ChangesAllParcelsPanelWidget
from asistente_ladm_col.gui.change_detection.changes_per_parcel_panel import ChangesPerParcelPanelWidget
from asistente_ladm_col.gui.change_detection.parcels_changes_summary_panel import ParcelsChangesSummaryPanelWidget
from asistente_ladm_col.gui.change_detection.changes_parties_panel import ChangesPartyPanelWidget
from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.qt_utils import OverrideCursor

from asistente_ladm_col.config.symbology import Symbology
from asistente_ladm_col.config.general_config import MAP_SWIPE_TOOL_PLUGIN_NAME
from asistente_ladm_col.config.layer_config import LayerConfig
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.config.gui.change_detection_config import (CHANGE_DETECTION_NEW_PARCEL,
                                                                   CHANGE_DETECTION_PARCEL_CHANGED,
                                                                   CHANGE_DETECTION_PARCEL_ONLY_GEOMETRY_CHANGED,
                                                                   CHANGE_DETECTION_PARCEL_REMAINS,
                                                                   CHANGE_DETECTION_SEVERAL_PARCELS,
                                                                   CHANGE_DETECTION_NULL_PARCEL,
                                                                   CHANGE_DETECTION_MISSING_PARCEL,
                                                                   DICT_KEY_PARCEL_T_PARCEL_NUMBER_F,
                                                                   PARCEL_STATUS,
                                                                   PARCEL_STATUS_DISPLAY,
                                                                   PLOT_GEOMETRY_KEY)

DOCKWIDGET_UI = get_ui_class('change_detection/dockwidget_change_detection.ui')


class DockWidgetChangeDetection(QgsDockWidget, DOCKWIDGET_UI):

    zoom_to_features_requested = pyqtSignal(QgsVectorLayer, list, dict, int)  # layer, ids, t_ids, duration

    def __init__(self, iface, db, supplies_db, qgis_utils, ladm_data, all_parcels_mode=True):
        super(DockWidgetChangeDetection, self).__init__(None)
        self.setupUi(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.utils = ChangeDetectionUtils(iface, db, supplies_db, qgis_utils, ladm_data)
        self.utils.change_detection_layer_removed.connect(self.layer_removed)

        self.map_swipe_tool = qgis.utils.plugins[MAP_SWIPE_TOOL_PLUGIN_NAME]
        Logger().clear_message_bar()  # Clear QGIS message bar

        # Configure panels
        self.all_parcels_panel = None
        self.lst_all_parcels_panels = list()

        self.parcel_panel = None
        self.lst_parcel_panels = list()

        self.party_panel = None
        self.lst_party_panels = list()

        if all_parcels_mode:
            self.main_panel = ParcelsChangesSummaryPanelWidget(self, self.utils)
            self.widget.setMainPanel(self.main_panel)
            self.add_layers()
            self.main_panel.fill_data()

        else:  # Per parcel mode
            self.parcel_panel = ChangesPerParcelPanelWidget(self, self.utils)
            self.widget.setMainPanel(self.parcel_panel)
            self.lst_parcel_panels.append(self.parcel_panel)

    def closeEvent(self, event):
        # closes open signals on panels
        if self.parcel_panel:
            self.parcel_panel.close_panel()

        self.close_dock_widget()

    def add_layers(self):
        self.utils.add_layers()

    def layer_removed(self):
        self.utils.iface.messageBar().pushMessage("Asistente LADM_COL",
                                            QCoreApplication.translate("DockWidgetChangeDetection",
                                                                       "'Change detection' has been closed because you just removed a required layer."),
                                            Qgis.Info)
        self.close_dock_widget()

    def show_all_parcels_panel(self, dict_parcels, types_change_detection):
        with OverrideCursor(Qt.WaitCursor):
            if self.lst_all_parcels_panels:
                for panel in self.lst_all_parcels_panels:
                    try:
                        self.widget.closePanel(panel)
                    except RuntimeError as e:  # Panel in C++ could be already closed...
                        pass

                self.lst_all_parcels_panels = list()
                self.all_parcels_panel = None

            self.all_parcels_panel = ChangesAllParcelsPanelWidget(self, self.utils, dict_parcels, types_change_detection)
            self.all_parcels_panel.changes_per_parcel_panel_requested.connect(self.show_parcel_panel)
            self.widget.showPanel(self.all_parcels_panel)
            self.lst_all_parcels_panels.append(self.all_parcels_panel)

    def show_parcel_panel(self, parcel_number=None, parcel_t_id=None):
        """
        Only for all_parcels_mode

        :param parcel_number:
        :param parcel_t_id:
        :return:
        """
        if self.lst_parcel_panels:
            for panel in self.lst_parcel_panels:
                try:
                    self.widget.closePanel(panel)
                except RuntimeError as e:  # Panel in C++ could be already closed...
                    pass

            self.lst_parcel_panels = list()
            self.parcel_panel = None

        if parcel_t_id is not None and parcel_t_id != '':
            self.parcel_panel = ChangesPerParcelPanelWidget(self, self.utils, parcel_number, parcel_t_id)
        else:
            self.parcel_panel = ChangesPerParcelPanelWidget(self, self.utils, parcel_number)

        self.widget.showPanel(self.parcel_panel)
        self.lst_parcel_panels.append(self.parcel_panel)

    def show_party_panel(self, data):
        if self.lst_party_panels:
            for panel in self.lst_party_panels:
                try:
                    self.widget.closePanel(panel)
                except RuntimeError as e:  # Panel in C++ could be already closed...
                    pass

            self.lst_party_panels = list()
            self.party_panel = None

        self.party_panel = ChangesPartyPanelWidget(self, self.utils, data)
        self.widget.showPanel(self.party_panel)
        self.lst_party_panels.append(self.party_panel)

    def update_db_connection(self, db, ladm_col_db, db_source):
        self.close_dock_widget()  # The user needs to use the menus again, which will start everything from scratch

    def close_dock_widget(self):
        try:
            self.utils.change_detection_layer_removed.disconnect()  # disconnect layer signals
        except:
            pass

        self.close()  # The user needs to use the menus again, which will start everything from scratch

    def initialize_layers(self):
        self.utils.initialize_layers()

    def request_zoom_to_features(self, layer, ids=list(), t_ids=dict(), duration=500):
        self.zoom_to_features_requested.emit(layer, ids, t_ids, duration)

    def activate_map_swipe_tool(self):
        if not self.map_swipe_tool.action.isChecked():
            self.map_swipe_tool.run(True)
            self.utils.iface.messageBar().clearWidgets()

    def deactivate_map_swipe_tool(self):
        if self.map_swipe_tool.action.isChecked():
            self.map_swipe_tool.run(False)

        self.utils.qgis_utils.set_layer_visibility(self.utils._supplies_layers[self.utils._supplies_db.names.GC_PLOT_T], True)
        self.utils.qgis_utils.set_layer_visibility(self.utils._layers[self.utils._db.names.OP_PLOT_T], True)


class ChangeDetectionUtils(QObject):

    change_detection_layer_removed = pyqtSignal()

    def __init__(self, iface, db, supplies_db, qgis_utils, ladm_data):
        QObject.__init__(self)
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self._db = db
        self._supplies_db = supplies_db
        self.qgis_utils = qgis_utils
        self.ladm_data = ladm_data
        self.symbology = Symbology()

        self._layers = dict()
        self._supplies_layers = dict()
        self.initialize_layers()

        self._compared_parcels_data = dict()
        self._compared_parcels_data_inverse = dict()

    def initialize_layers(self):
        self._layers = {
            self._db.names.OP_PLOT_T: None,
            self._db.names.OP_PARCEL_T: None,
            self._db.names.COL_UE_BAUNIT_T: None
        }

        self._supplies_layers = {
            self._supplies_db.names.GC_PLOT_T: None,
            self._supplies_db.names.GC_PARCEL_T: None
        }

    def initialize_data(self):
        self._compared_parcels_data = dict()
        self._compared_parcels_data_inverse = dict()

    def add_layers(self):
        # We can pick any required layer, if it is None, no prior load has been done, otherwise skip...
        if self._layers[self._db.names.OP_PLOT_T] is None:
            self.qgis_utils.map_freeze_requested.emit(True)

            self.qgis_utils.get_layers(self._db, self._layers, load=True, emit_map_freeze=False)
            if not self._layers:
                return None

            # Now load supplies layers
            # Set layer modifiers
            layer_modifiers = {
                LayerConfig.PREFIX_LAYER_MODIFIERS: LayerConfig.SUPPLIES_DB_PREFIX,
                LayerConfig.SUFFIX_LAYER_MODIFIERS: LayerConfig.SUPPLIES_DB_SUFFIX,
                LayerConfig.STYLE_GROUP_LAYER_MODIFIERS: self.symbology.get_supplies_style_group(self._supplies_db.names)
            }
            self.qgis_utils.get_layers(self._supplies_db,
                                       self._supplies_layers,
                                       load=True,
                                       emit_map_freeze=False,
                                       layer_modifiers=layer_modifiers)
            if not self._supplies_layers:
                return None
            else:
                # In some occasions the supplies and collected plots might not overlap and have different extents
                self.iface.setActiveLayer(self._supplies_layers[self._supplies_db.names.GC_PLOT_T])
                self.iface.zoomToActiveLayer()

            self.qgis_utils.map_freeze_requested.emit(False)

            for layer_name in self._layers:
                if self._layers[layer_name]: # Layer was found, listen to its removal so that we can react properly
                    try:
                        self._layers[layer_name].willBeDeleted.disconnect(self.change_detection_layer_removed)
                    except:
                        pass
                    self._layers[layer_name].willBeDeleted.connect(self.change_detection_layer_removed)

            for layer_name in self._supplies_layers:
                if self._supplies_layers[layer_name]: # Layer was found, listen to its removal so that we can react properly
                    try:
                        self._supplies_layers[layer_name].willBeDeleted.disconnect(self.change_detection_layer_removed)
                    except:
                        pass
                    self._supplies_layers[layer_name].willBeDeleted.connect(self.change_detection_layer_removed)

    def get_compared_parcels_data(self, inverse=False):
        # If it's the first call, get from the DB, else get from a cache
        if inverse:
            if not self._compared_parcels_data_inverse:
                self._compared_parcels_data_inverse = self._get_compared_parcels_data(inverse)

            return self._compared_parcels_data_inverse
        else:
            if not self._compared_parcels_data:
                self._compared_parcels_data = self._get_compared_parcels_data()

            return self._compared_parcels_data

    def _get_compared_parcels_data(self, inverse=False):
        """
        inverse: By default False, which takes the collected db as base_db and the supplies_db as compare_db
                 Inverse True is useful to find missing parcels (from the supplies authority's perspective)

        :return: dict() --> {PARCEL_NUMBER: X,
                             PARCEL_ATTRIBUTES: {PARCEL_ID: [self._db.names.T_ID_F], PARCEL_STATUS: '', PARCEL_STATUS_DISPLAY: ''}]
        """
        base_db = self._supplies_db if inverse else self._db
        compare_db = self._db if inverse else self._supplies_db

        layer_modifiers = {
            LayerConfig.PREFIX_LAYER_MODIFIERS: LayerConfig.SUPPLIES_DB_PREFIX,
            LayerConfig.SUFFIX_LAYER_MODIFIERS: LayerConfig.SUPPLIES_DB_SUFFIX,
            LayerConfig.STYLE_GROUP_LAYER_MODIFIERS: self.symbology.get_supplies_style_group(self._supplies_db.names)
        }

        if inverse:
            dict_collected_parcels = self.ladm_data.get_parcel_data_to_compare_changes_supplies(self._supplies_db, None)
            dict_supplies_parcels = self.ladm_data.get_parcel_data_to_compare_changes(self._db, None, layer_modifiers=layer_modifiers)
        else:
            dict_collected_parcels = self.ladm_data.get_parcel_data_to_compare_changes(self._db, None)
            dict_supplies_parcels = self.ladm_data.get_parcel_data_to_compare_changes_supplies(self._supplies_db, None, layer_modifiers=layer_modifiers)

        dict_compared_parcel_data = dict()
        for collected_parcel_number, collected_features in dict_collected_parcels.items():
            dict_attrs_comparison = dict()

            if not collected_parcel_number: # NULL parcel numbers
                dict_attrs_comparison[DICT_KEY_PARCEL_T_PARCEL_NUMBER_F] = NULL
                dict_attrs_comparison[base_db.names.T_ID_F] = [feature[base_db.names.T_ID_F] for feature in collected_features]
                dict_attrs_comparison[PARCEL_STATUS] = CHANGE_DETECTION_NULL_PARCEL
                dict_attrs_comparison[PARCEL_STATUS_DISPLAY] = "({})".format(len(collected_features))
            else:
                # A parcel number has at least one dict of attributes (i.e., one feature)
                dict_attrs_comparison[DICT_KEY_PARCEL_T_PARCEL_NUMBER_F] = collected_parcel_number
                dict_attrs_comparison[base_db.names.T_ID_F] = [feature[base_db.names.T_ID_F] for feature in collected_features]

                if len(collected_features) > 1:
                    dict_attrs_comparison[PARCEL_STATUS] = CHANGE_DETECTION_SEVERAL_PARCELS
                    dict_attrs_comparison[PARCEL_STATUS_DISPLAY] = "({})".format(len(collected_features))
                else:  # Only one feature, at this point is safe to call the first element ([0]) of the array
                    if not collected_parcel_number in dict_supplies_parcels:
                        dict_attrs_comparison[PARCEL_STATUS] = CHANGE_DETECTION_NEW_PARCEL
                        dict_attrs_comparison[PARCEL_STATUS_DISPLAY] = CHANGE_DETECTION_NEW_PARCEL
                    else:
                        supplies_features = dict_supplies_parcels[collected_parcel_number]

                        del collected_features[0][base_db.names.T_ID_F]  # We won't compare ID_FIELDS
                        del supplies_features[0][compare_db.names.T_ID_F]  # We won't compare ID_FIELDS

                        # Compare all attributes except geometry: a change in feature attrs is enough to mark it as
                        #   changed in the summary panel
                        if not self.compare_features_attrs(collected_features[0], supplies_features[0]):
                            dict_attrs_comparison[PARCEL_STATUS] = CHANGE_DETECTION_PARCEL_CHANGED
                            dict_attrs_comparison[PARCEL_STATUS_DISPLAY] = CHANGE_DETECTION_PARCEL_CHANGED
                        else:  # Attrs are equal, what about geometries?
                            collected_geometry = QgsGeometry()
                            supplies_geometry = QgsGeometry()
                            if PLOT_GEOMETRY_KEY in collected_features[0]:
                                collected_geometry = collected_features[0][PLOT_GEOMETRY_KEY]
                            if PLOT_GEOMETRY_KEY in supplies_features[0]:
                                supplies_geometry = supplies_features[0][PLOT_GEOMETRY_KEY]

                            if not self.compare_features_geometries(collected_geometry, supplies_geometry):
                                dict_attrs_comparison[PARCEL_STATUS] = CHANGE_DETECTION_PARCEL_ONLY_GEOMETRY_CHANGED
                                dict_attrs_comparison[PARCEL_STATUS_DISPLAY] = CHANGE_DETECTION_PARCEL_ONLY_GEOMETRY_CHANGED
                            else:  # Attrs and geometry are the same!
                                dict_attrs_comparison[PARCEL_STATUS] = CHANGE_DETECTION_PARCEL_REMAINS
                                dict_attrs_comparison[PARCEL_STATUS_DISPLAY] = CHANGE_DETECTION_PARCEL_REMAINS

            dict_compared_parcel_data[collected_parcel_number or NULL] = dict_attrs_comparison

        return dict_compared_parcel_data

    def compare_features_attrs(self, collected, supplies):
        """
        Compare all alphanumeric attibutes for two custom feature dicts

        :param collected: Dict with parcel info defined in parcel_fields_to_compare, party_fields_to_compare,
                          plot_field_to_compare, PROPERTY_RECORD_CARD_FIELDS_TO_COMPARE
        :param supplies: Dict with parcel info defined in parcel_fields_to_compare, party_fields_to_compare,
                          plot_field_to_compare, PROPERTY_RECORD_CARD_FIELDS_TO_COMPARE
        :return: True means equal, False unequal
        """
        if len(collected) != len(supplies):
            return False

        for k,v in collected.items():
            if k != PLOT_GEOMETRY_KEY:
                if v != supplies[k]:
                    return False

        return True

    def compare_features_geometries(self, geometry_a, geometry_b):
        """
        Function to compare two plot geometries:
            First compare bboxes, if equal compare centroids, if equal use QGIS equals() function.

        :param geometry_a: QgsGeometry
        :param geometry_b: QgsGeometry
        :return: True means equal, False unequal
        """
        if geometry_a is None:  # None for parcels that don't have any associated plot
            return geometry_b is None or geometry_b.isNull()

        if geometry_b is None:  # None for parcels that don't have any associated plot
            return geometry_a is None or geometry_a.isNull()

        if not geometry_a.isGeosValid() and not geometry_b.isGeosValid():
            return True

        if geometry_a.boundingBox() != geometry_b.boundingBox():
            return False

        if not geometry_a.centroid().equals(geometry_b.centroid()):
            return False

        if not geometry_a.equals(geometry_b):
            return False

        return True
