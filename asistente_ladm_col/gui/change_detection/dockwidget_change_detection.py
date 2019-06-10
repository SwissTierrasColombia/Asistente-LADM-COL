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
                              pyqtSignal, QCoreApplication)
from qgis.core import (QgsVectorLayer,
                       QgsWkbTypes,
                       Qgis)
from qgis.gui import QgsDockWidget, QgsMapToolIdentifyFeature

from asistente_ladm_col.gui.change_detection.changes_all_parcels_panel import ChangesAllParcelsPanelWidget
from asistente_ladm_col.gui.change_detection.changes_per_parcel_panel import ChangesPerParcelPanelWidget
from asistente_ladm_col.gui.change_detection.parcels_changes_summary_panel import ParcelsChangesSummaryPanelWidget
from asistente_ladm_col.utils import get_ui_class

from ...config.symbology import OFFICIAL_STYLE_GROUP
from ...config.general_config import (OFFICIAL_DB_PREFIX,
                                      OFFICIAL_DB_SUFFIX,
                                      PREFIX_LAYER_MODIFIERS,
                                      SUFFIX_LAYER_MODIFIERS,
                                      STYLE_GROUP_LAYER_MODIFIERS,
                                      MAP_SWIPE_TOOL_PLUGIN_NAME,
                                      CHANGE_DETECTION_NEW_PARCEL,
                                      CHANGE_DETECTION_MISSING_PARCEL,
                                      CHANGE_DETECTION_PARCEL_CHANGED,
                                      CHANGE_DETECTION_PARCEL_REMAINS,
                                      CHANGE_DETECTION_SEVERAL_PARCELS,
                                      CHANGE_DETECTION_NULL_PARCEL,
                                      PARCEL_STATUS,
                                      PARCEL_STATUS_DISPLAY)

from ...config.table_mapping_config import (PLOT_TABLE,
                                            PARCEL_TABLE,
                                            UEBAUNIT_TABLE,
                                            PARCEL_NUMBER_FIELD,
                                            ID_FIELD)

DOCKWIDGET_UI = get_ui_class('change_detection/dockwidget_change_detection.ui')


class DockWidgetChangeDetection(QgsDockWidget, DOCKWIDGET_UI):

    zoom_to_features_requested = pyqtSignal(QgsVectorLayer, list, list)

    def __init__(self, iface, db, official_db, qgis_utils, ladm_data):
        super(DockWidgetChangeDetection, self).__init__(None)
        self.setupUi(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.utils = ChangeDetectionUtils(iface, db, official_db, qgis_utils, ladm_data)

        self.map_swipe_tool = qgis.utils.plugins[MAP_SWIPE_TOOL_PLUGIN_NAME]

        self._layers = dict()
        self._official_layers = dict()
        self.initialize_layers()

        # Configure panels
        self.main_panel = ParcelsChangesSummaryPanelWidget(self, self.utils)
        self.widget.setMainPanel(self.main_panel)

        self.all_parcels_panel = None
        self.lst_all_parcels_panels = list()

        self.parcel_panel = None
        self.lst_parcel_panels = list()

    def add_layers(self):
        self.utils.qgis_utils.map_freeze_requested.emit(True)

        res_layers = self.utils.qgis_utils.get_layers(self.utils._db, self._layers, load=True, emit_map_freeze=False)
        if res_layers is None:
            return

        # Now load official layers
        # Set layer modifiers
        layer_modifiers = {
            PREFIX_LAYER_MODIFIERS: OFFICIAL_DB_PREFIX,
            SUFFIX_LAYER_MODIFIERS: OFFICIAL_DB_SUFFIX,
            STYLE_GROUP_LAYER_MODIFIERS: OFFICIAL_STYLE_GROUP
        }
        res_layers = self.utils.qgis_utils.get_layers(self.utils._official_db,
                                                      self._official_layers,
                                                      load=True,
                                                      emit_map_freeze=False,
                                                      layer_modifiers=layer_modifiers)
        if res_layers is None:
            return

        self.utils.qgis_utils.map_freeze_requested.emit(False)

        for layer_name in self._layers:
            if self._layers[layer_name]['layer']: # Layer was found, listen to its removal so that we can react properly
                try:
                    self._layers[layer_name]['layer'].willBeDeleted.disconnect(self.layer_removed)
                except:
                    pass
                self._layers[layer_name]['layer'].willBeDeleted.connect(self.layer_removed)

        for layer_name in self._official_layers:
            if self._official_layers[layer_name]['layer']: # Layer was found, listen to its removal so that we can react properly
                try:
                    self._official_layers[layer_name]['layer'].willBeDeleted.disconnect(self.layer_removed)
                except:
                    pass
                self._official_layers[layer_name]['layer'].willBeDeleted.connect(self.layer_removed)

    def layer_removed(self):
        self.utils.iface.messageBar().pushMessage("Asistente LADM_COL",
                                            QCoreApplication.translate("CreateParcelCadastreWizard",
                                                                       "'Change detection' has been closed because you just removed a required layer."),
                                            Qgis.Info)
        self.close()

    def show_main_panel(self):
        self.add_layers()
        self.main_panel.fill_data()

    def show_all_parcels_panel(self, filter_parcels=dict()):
        if self.lst_all_parcels_panels:
            for panel in self.lst_all_parcels_panels:
                try:
                    self.widget.closePanel(panel)
                except RuntimeError as e:  # Panel in C++ could be already closed...
                    pass

            self.lst_all_parcels_panels = list()

        self.all_parcels_panel = ChangesAllParcelsPanelWidget(self, self.utils, filter_parcels=filter_parcels)
        self.all_parcels_panel.changes_per_parcel_panel_requested.connect(self.show_parcel_panel)
        self.widget.showPanel(self.all_parcels_panel)
        self.lst_all_parcels_panels.append(self.all_parcels_panel)

    def show_parcel_panel(self, parcel_number=None):
        if self.lst_parcel_panels:
            for panel in self.lst_parcel_panels:
                try:
                    self.widget.closePanel(panel)
                except RuntimeError as e:  # Panel in C++ could be already closed...
                    pass

            self.lst_parcel_panels = list()

        self.parcel_panel = ChangesPerParcelPanelWidget(self, self.utils, parcel_number)
        self.widget.showPanel(self.parcel_panel)
        self.lst_parcel_panels.append(self.parcel_panel)

    def update_db_connection(self, db, ladm_col_db):
        self.utils._db = db
        self.initialize_layers()

        if not ladm_col_db:
            self.setVisible(False)

        # TODO update_official_db_connection

    def initialize_layers(self):
        self._layers = {
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, 'layer': None},
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None, 'layer': None},
            UEBAUNIT_TABLE: {'name': UEBAUNIT_TABLE, 'geometry': None, 'layer': None}
        }

        self._official_layers = {
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, 'layer': None},
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None, 'layer': None},
            UEBAUNIT_TABLE: {'name': UEBAUNIT_TABLE, 'geometry': None, 'layer': None}
        }

    def request_zoom_to_features(self, layer, ids=list(), t_ids=list()):
        self.zoom_to_features_requested.emit(layer, ids, t_ids)

    def activate_mapswipe_tool(self):
        self.map_swipe_tool.run(True)
        self.utils.iface.messageBar().clearWidgets()

    def deactivate_mapswipe_tool(self):
        self.map_swipe_tool.run(False)
        self.utils.qgis_utils.set_layer_visibility(self._official_layers[PLOT_TABLE]['layer'], True)
        self.utils.qgis_utils.set_layer_visibility(self._layers[PLOT_TABLE]['layer'], True)


class ChangeDetectionUtils():
    def __init__(self, iface, db, official_db, qgis_utils, ladm_data):
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self._db = db
        self._official_db = official_db
        self.qgis_utils = qgis_utils
        self.ladm_data = ladm_data

    def get_compared_parcels_data(self, base_db, compare_db):
        """
        base_db: normally the collected db
        compare_db: normally the official_db

        :return: dict() --> {PARCEL_NUMBER: X,
                             PARCEL_ATTRIBUTES: {PARCEL_ID: [ID_FIELD], PARCEL_STATUS: '', PARCEL_STATUS_DISPLAY: ''}]
        """
        dict_collected_parcels = self.ladm_data.get_parcel_data_to_compare_changes(base_db, None)

        dict_official_parcels = self.ladm_data.get_parcel_data_to_compare_changes(compare_db, None)

        dict_compared_parcel_data = dict()
        for collected_parcel_number, collected_attrs in dict_collected_parcels.items():
            dict_attrs_comparison = dict()

            if not collected_parcel_number: # NULL parcel numbers
                dict_attrs_comparison[PARCEL_NUMBER_FIELD] = 'NULL'
                dict_attrs_comparison[ID_FIELD] = [attr[ID_FIELD] for attr in collected_attrs]
                dict_attrs_comparison[PARCEL_STATUS] = CHANGE_DETECTION_NULL_PARCEL
                dict_attrs_comparison[PARCEL_STATUS_DISPLAY] = "({})".format(len(collected_attrs))
            else:
                # A parcel number has at least one dict of attributes (i.e., one feature)
                dict_attrs_comparison[PARCEL_NUMBER_FIELD] = collected_parcel_number
                dict_attrs_comparison[ID_FIELD] = [attr[ID_FIELD] for attr in collected_attrs]

                if len(collected_attrs) > 1:
                    dict_attrs_comparison[PARCEL_STATUS] = CHANGE_DETECTION_SEVERAL_PARCELS
                    dict_attrs_comparison[PARCEL_STATUS_DISPLAY] = "({})".format(len(collected_attrs))
                else:
                    if not collected_parcel_number in dict_official_parcels:
                        dict_attrs_comparison[PARCEL_STATUS] = CHANGE_DETECTION_NEW_PARCEL
                        dict_attrs_comparison[PARCEL_STATUS_DISPLAY] = CHANGE_DETECTION_NEW_PARCEL
                    else:
                        official_attrs = dict_official_parcels[collected_parcel_number]

                        del collected_attrs[0][ID_FIELD]
                        del official_attrs[0][ID_FIELD]
                        dict_attrs_comparison[PARCEL_STATUS] = CHANGE_DETECTION_PARCEL_REMAINS if collected_attrs[0] == official_attrs[0] else CHANGE_DETECTION_PARCEL_CHANGED
                        dict_attrs_comparison[PARCEL_STATUS_DISPLAY] = CHANGE_DETECTION_PARCEL_REMAINS if collected_attrs[0] == official_attrs[0] else CHANGE_DETECTION_PARCEL_CHANGED

            dict_compared_parcel_data[collected_parcel_number or 'NULL'] = dict_attrs_comparison

        return dict_compared_parcel_data
