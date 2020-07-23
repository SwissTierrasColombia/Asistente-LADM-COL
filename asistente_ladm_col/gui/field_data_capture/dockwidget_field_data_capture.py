# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin                : 2020-07-22
        git sha              : :%H$
        copyright            : (C) 2020 by Germán Carrillo (SwissTierras Colombia)
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
from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication)
from qgis.core import Qgis
from qgis.gui import QgsDockWidget

from asistente_ladm_col.gui.field_data_capture.allocate_parcels_panel import AllocateParcelsFieldDataCapturePanelWidget
from asistente_ladm_col.utils import get_ui_class

from asistente_ladm_col.lib.logger import Logger

DOCKWIDGET_UI = get_ui_class('field_data_capture/dockwidget_field_data_capture.ui')


class DockWidgetFieldDataCapture(QgsDockWidget, DOCKWIDGET_UI):
    def __init__(self, iface, db, allocate_mode=True):
        super(DockWidgetFieldDataCapture, self).__init__(None)
        self.setupUi(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.iface = iface

        Logger().clear_message_bar()  # Clear QGIS message bar

        # Configure panels
        self.allocate_subpanels = None
        self.lst_all_allocate_subpanels = list()

        self.party_panel = None
        self.lst_party_panels = list()

        if allocate_mode:
            self.allocate_panel = AllocateParcelsFieldDataCapturePanelWidget(self)
            self.widget.setMainPanel(self.allocate_panel)
            self.add_layers()
            self.allocate_panel.fill_data()
        else:  # Synchronize mode
            # self.synchronize_panel = ChangesPerParcelPanelWidget(self, self.utils)
            # self.widget.setMainPanel(self.synchronize_panel)
            # self.lst_parcel_panels.append(self.synchronize_panel)
            pass

    def closeEvent(self, event):
        # Close here open signals in other panels (if needed)
        self.close_dock_widget()

    def add_layers(self):
        pass

    def layer_removed(self):
        self.iface.messageBar().pushMessage("Asistente LADM-COL",
                                            QCoreApplication.translate("DockWidgetFieldDataCapture",
                                                                       "'Field data capture' has been closed because you just removed a required layer."),
                                            Qgis.Info)
        self.close_dock_widget()

    def update_db_connection(self, db, ladm_col_db, db_source):
        self.close_dock_widget()  # The user needs to use the menus again, which will start everything from scratch

    def close_dock_widget(self):
        try:
            #self.utils.change_detection_layer_removed.disconnect()  # disconnect layer signals
            pass
        except:
            pass

        self.close()  # The user needs to use the menus again, which will start everything from scratch

    def initialize_layers(self):
        pass