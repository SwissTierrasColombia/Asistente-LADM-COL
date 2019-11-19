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
                       QgsWkbTypes,
                       Qgis,
                       NULL,
                       QgsGeometry)
from qgis.gui import QgsDockWidget

from ...gui.change_detection.changes_all_parcels_panel import ChangesAllParcelsPanelWidget
from ...gui.change_detection.changes_per_parcel_panel import ChangesPerParcelPanelWidget
from ...gui.change_detection.parcels_changes_summary_panel import ParcelsChangesSummaryPanelWidget
from ...gui.change_detection.changes_parties_panel import ChangesPartyPanelWidget
from ...utils import get_ui_class
from ...utils.qt_utils import OverrideCursor

from ...config.symbology import Symbology
from ...config.general_config import (OFFICIAL_DB_PREFIX,
                                      OFFICIAL_DB_SUFFIX,
                                      PREFIX_LAYER_MODIFIERS,
                                      SUFFIX_LAYER_MODIFIERS,
                                      STYLE_GROUP_LAYER_MODIFIERS,
                                      MAP_SWIPE_TOOL_PLUGIN_NAME,
                                      CHANGE_DETECTION_NEW_PARCEL,
                                      CHANGE_DETECTION_PARCEL_CHANGED,
                                      CHANGE_DETECTION_PARCEL_ONLY_GEOMETRY_CHANGED,
                                      CHANGE_DETECTION_PARCEL_REMAINS,
                                      CHANGE_DETECTION_SEVERAL_PARCELS,
                                      CHANGE_DETECTION_NULL_PARCEL,
                                      LAYER,
                                      PARCEL_STATUS,
                                      PARCEL_STATUS_DISPLAY,
                                      PLOT_GEOMETRY_KEY)

from asistente_ladm_col.config.table_mapping_config import Names

DOCKWIDGET_UI = get_ui_class('change_detection/dockwidget_change_detection.ui')


class DockWidgetChangeDetection(QgsDockWidget, DOCKWIDGET_UI):

    zoom_to_features_requested = pyqtSignal(QgsVectorLayer, list, list, int)  # layer, ids, t_ids, duration

    def __init__(self, iface, db, official_db, qgis_utils, ladm_data, all_parcels_mode=True):
        super(DockWidgetChangeDetection, self).__init__(None)
        self.setupUi(self)
        self.names = Names()
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.utils = ChangeDetectionUtils(iface, db, official_db, qgis_utils, ladm_data)
        self.utils.change_detection_layer_removed.connect(self.layer_removed)

        self.map_swipe_tool = qgis.utils.plugins[MAP_SWIPE_TOOL_PLUGIN_NAME]

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

    def show_all_parcels_panel(self, filter_parcels=dict()):
        with OverrideCursor(Qt.WaitCursor):
            if self.lst_all_parcels_panels:
                for panel in self.lst_all_parcels_panels:
                    try:
                        self.widget.closePanel(panel)
                    except RuntimeError as e:  # Panel in C++ could be already closed...
                        pass

                self.lst_all_parcels_panels = list()
                self.all_parcels_panel = None

            self.all_parcels_panel = ChangesAllParcelsPanelWidget(self, self.utils, filter_parcels=filter_parcels)
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

    def update_db_connection(self, db, ladm_col_db):
        self.close_dock_widget()  # The user needs to use the menus again, which will start everything from scratch

    def close_dock_widget(self):
        try:
            self.utils.change_detection_layer_removed.disconnect()  # disconnect layer signals
        except:
            pass

        self.close()  # The user needs to use the menus again, which will start everything from scratch

    def initialize_layers(self):
        self.utils.initialize_layers()

    def request_zoom_to_features(self, layer, ids=list(), t_ids=list(), duration=500):
        self.zoom_to_features_requested.emit(layer, ids, t_ids, duration)

    def activate_map_swipe_tool(self):
        if not self.map_swipe_tool.action.isChecked():
            self.map_swipe_tool.run(True)
            self.utils.iface.messageBar().clearWidgets()

    def deactivate_map_swipe_tool(self):
        if self.map_swipe_tool.action.isChecked():
            self.map_swipe_tool.run(False)

        self.utils.qgis_utils.set_layer_visibility(self.utils._official_layers[self.names.OP_PLOT_T][LAYER], True)
        self.utils.qgis_utils.set_layer_visibility(self.utils._layers[self.names.OP_PLOT_T][LAYER], True)


class ChangeDetectionUtils(QObject):

    change_detection_layer_removed = pyqtSignal()

    def __init__(self, iface, db, official_db, qgis_utils, ladm_data):
        QObject.__init__(self)
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self._db = db
        self._official_db = official_db
        self.qgis_utils = qgis_utils
        self.ladm_data = ladm_data
        self.names = Names()
        self.symbology = Symbology()

        self._layers = dict()
        self._official_layers = dict()
        self.initialize_layers()

        self._compared_parcels_data = dict()
        self._compared_parcels_data_inverse = dict()

    def initialize_layers(self):
        self._layers = {
            self.names.OP_PLOT_T: {'name': self.names.OP_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.OP_PARCEL_T: {'name': self.names.OP_PARCEL_T, 'geometry': None, LAYER: None},
            self.names.COL_UE_BAUNIT_T: {'name': self.names.COL_UE_BAUNIT_T, 'geometry': None, LAYER: None}
        }

        self._official_layers = {
            self.names.OP_PLOT_T: {'name': self.names.OP_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.OP_PARCEL_T: {'name': self.names.OP_PARCEL_T, 'geometry': None, LAYER: None},
            self.names.COL_UE_BAUNIT_T: {'name': self.names.COL_UE_BAUNIT_T, 'geometry': None, LAYER: None}
        }

    def initialize_data(self):
        self._compared_parcels_data = dict()
        self._compared_parcels_data_inverse = dict()

    def add_layers(self):
        # We can pick any required layer, if it is None, no prior load has been done, otherwise skip...
        if self._layers[self.names.OP_PLOT_T][LAYER] is None:
            self.qgis_utils.map_freeze_requested.emit(True)

            self.qgis_utils.get_layers(self._db, self._layers, load=True, emit_map_freeze=False)
            if not self._layers:
                return None

            # Now load official layers
            # Set layer modifiers
            layer_modifiers = {
                PREFIX_LAYER_MODIFIERS: OFFICIAL_DB_PREFIX,
                SUFFIX_LAYER_MODIFIERS: OFFICIAL_DB_SUFFIX,
                STYLE_GROUP_LAYER_MODIFIERS: self.symbology.get_official_style_group()
            }
            self.qgis_utils.get_layers(self._official_db,
                                       self._official_layers,
                                       load=True,
                                       emit_map_freeze=False,
                                       layer_modifiers=layer_modifiers)
            if not self._official_layers:
                return None
            else:
                # In some occasions the official and collected plots might not overlap and have different extents
                self.iface.setActiveLayer(self._official_layers[self.names.OP_PLOT_T][LAYER])
                self.iface.zoomToActiveLayer()

            self.qgis_utils.map_freeze_requested.emit(False)

            for layer_name in self._layers:
                if self._layers[layer_name][LAYER]: # Layer was found, listen to its removal so that we can react properly
                    try:
                        self._layers[layer_name][LAYER].willBeDeleted.disconnect(self.change_detection_layer_removed)
                    except:
                        pass
                    self._layers[layer_name][LAYER].willBeDeleted.connect(self.change_detection_layer_removed)

            for layer_name in self._official_layers:
                if self._official_layers[layer_name][LAYER]: # Layer was found, listen to its removal so that we can react properly
                    try:
                        self._official_layers[layer_name][LAYER].willBeDeleted.disconnect(self.change_detection_layer_removed)
                    except:
                        pass
                    self._official_layers[layer_name][LAYER].willBeDeleted.connect(self.change_detection_layer_removed)

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
        inverse: By default False, which takes the collected db as base_db and the official_db as compare_db
                 Inverse True is useful to find missing parcels (from the official authority's perspective)

        :return: dict() --> {PARCEL_NUMBER: X,
                             PARCEL_ATTRIBUTES: {PARCEL_ID: [self.names.T_ID_F], PARCEL_STATUS: '', PARCEL_STATUS_DISPLAY: ''}]
        """
        base_db = self._official_db if inverse else self._db
        compare_db = self._db if inverse else self._official_db

        layer_modifiers = {
            PREFIX_LAYER_MODIFIERS: OFFICIAL_DB_PREFIX,
            SUFFIX_LAYER_MODIFIERS: OFFICIAL_DB_SUFFIX,
            STYLE_GROUP_LAYER_MODIFIERS: self.symbology.get_official_style_group()
        }
        dict_collected_parcels = self.ladm_data.get_parcel_data_to_compare_changes(base_db, None)
        dict_official_parcels = self.ladm_data.get_parcel_data_to_compare_changes(compare_db, None, layer_modifiers=layer_modifiers)

        dict_compared_parcel_data = dict()
        for collected_parcel_number, collected_features in dict_collected_parcels.items():
            dict_attrs_comparison = dict()

            if not collected_parcel_number: # NULL parcel numbers
                dict_attrs_comparison[self.names.OP_PARCEL_T_PARCEL_NUMBER_F] = NULL
                dict_attrs_comparison[self.names.T_ID_F] = [feature[self.names.T_ID_F] for feature in collected_features]
                dict_attrs_comparison[PARCEL_STATUS] = CHANGE_DETECTION_NULL_PARCEL
                dict_attrs_comparison[PARCEL_STATUS_DISPLAY] = "({})".format(len(collected_features))
            else:
                # A parcel number has at least one dict of attributes (i.e., one feature)
                dict_attrs_comparison[self.names.OP_PARCEL_T_PARCEL_NUMBER_F] = collected_parcel_number
                dict_attrs_comparison[self.names.T_ID_F] = [feature[self.names.T_ID_F] for feature in collected_features]

                if len(collected_features) > 1:
                    dict_attrs_comparison[PARCEL_STATUS] = CHANGE_DETECTION_SEVERAL_PARCELS
                    dict_attrs_comparison[PARCEL_STATUS_DISPLAY] = "({})".format(len(collected_features))
                else:  # Only one feature, at this point is safe to call the first element ([0]) of the array
                    if not collected_parcel_number in dict_official_parcels:
                        dict_attrs_comparison[PARCEL_STATUS] = CHANGE_DETECTION_NEW_PARCEL
                        dict_attrs_comparison[PARCEL_STATUS_DISPLAY] = CHANGE_DETECTION_NEW_PARCEL
                    else:
                        official_features = dict_official_parcels[collected_parcel_number]

                        del collected_features[0][self.names.T_ID_F]  # We won't compare ID_FIELDS
                        del official_features[0][self.names.T_ID_F]  # We won't compare ID_FIELDS

                        # Compare all attributes except geometry: a change in feature attrs is enough to mark it as
                        #   changed in the summary panel
                        if not self.compare_features_attrs(collected_features[0], official_features[0]):
                            dict_attrs_comparison[PARCEL_STATUS] = CHANGE_DETECTION_PARCEL_CHANGED
                            dict_attrs_comparison[PARCEL_STATUS_DISPLAY] = CHANGE_DETECTION_PARCEL_CHANGED
                        else:  # Attrs are equal, what about geometries?
                            collected_geometry = QgsGeometry()
                            official_geometry = QgsGeometry()
                            if PLOT_GEOMETRY_KEY in collected_features[0]:
                                collected_geometry = collected_features[0][PLOT_GEOMETRY_KEY]
                            if PLOT_GEOMETRY_KEY in official_features[0]:
                                official_geometry = official_features[0][PLOT_GEOMETRY_KEY]

                            if not self.compare_features_geometries(collected_geometry, official_geometry):
                                dict_attrs_comparison[PARCEL_STATUS] = CHANGE_DETECTION_PARCEL_ONLY_GEOMETRY_CHANGED
                                dict_attrs_comparison[PARCEL_STATUS_DISPLAY] = CHANGE_DETECTION_PARCEL_ONLY_GEOMETRY_CHANGED
                            else:  # Attrs and geometry are the same!
                                dict_attrs_comparison[PARCEL_STATUS] = CHANGE_DETECTION_PARCEL_REMAINS
                                dict_attrs_comparison[PARCEL_STATUS_DISPLAY] = CHANGE_DETECTION_PARCEL_REMAINS

            dict_compared_parcel_data[collected_parcel_number or NULL] = dict_attrs_comparison

        return dict_compared_parcel_data

    def compare_features_attrs(self, collected, official):
        """
        Compare all alphanumeric attibutes for two custom feature dicts

        :param collected: Dict with parcel info defined in get_parcel_fields_to_compare, get_party_fields_to_compare,
                          get_plot_field_to_compare, PROPERTY_RECORD_CARD_FIELDS_TO_COMPARE
        :param official: Dict with parcel info defined in get_parcel_fields_to_compare, get_party_fields_to_compare,
                          get_plot_field_to_compare, PROPERTY_RECORD_CARD_FIELDS_TO_COMPARE
        :return: True means equal, False unequal
        """
        if len(collected) != len(official):
            return False

        for k,v in collected.items():
            if k != PLOT_GEOMETRY_KEY:
                if v != official[k]:
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
