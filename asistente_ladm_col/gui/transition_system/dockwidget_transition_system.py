# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-11-29
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

from asistente_ladm_col.gui.transition_system.transition_system_initial_panel import TransitionSystemInitialPanelWidget
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

DOCKWIDGET_UI = get_ui_class('transition_system/dockwidget_transition_system.ui')


class DockWidgetTransitionSystem(QgsDockWidget, DOCKWIDGET_UI):

    def __init__(self, user, parent):
        super(DockWidgetTransitionSystem, self).__init__(parent)
        self.setupUi(self)
        self._user = user
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        # Configure panels
        self.all_parcels_panel = None
        self.lst_all_parcels_panels = list()

        self.main_panel = TransitionSystemInitialPanelWidget(user, self)
        self.widget.setMainPanel(self.main_panel)
        # self.main_panel.fill_data()

    def closeEvent(self, event):
        # closes open signals on panels
        # if self.parcel_panel:
        #     self.parcel_panel.close_panel()

        self.close_dock_widget()

    def update_db_connection(self, db, ladm_col_db):
        #self.close_dock_widget()  # The user needs to use the menus again, which will start everything from scratch
        pass

    def after_logout(self):
        self.close_dock_widget()

    def close_dock_widget(self):
        # try:
        #     self.utils.change_detection_layer_removed.disconnect()  # disconnect layer signals
        # except:
        #     pass

        self.close()  # The user needs to use the menus again, which will start everything from scratch
