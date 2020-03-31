# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-03-30
        copyright            : (C) 2020 by Germán Carrillo (BSF Swissphoto)
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
from qgis.PyQt.QtCore import QObject
from asistente_ladm_col.utils.singleton import SingletonQObject


class AppInterface(QObject, metaclass=SingletonQObject):
    def __init__(self):
        QObject.__init__(self)
        self.core = None
        self.gui = None

    def set_core_interface(self, core):
        self.core = core
        self.set_connections()

    def set_gui_interface(self, gui):
        self.gui = gui
        self.set_connections()

    def set_connections(self):
        if self.core and self.gui:
            self.core.action_vertex_tool_requested.connect(self.gui.trigger_vertex_tool)
            self.core.activate_layer_requested.connect(self.gui.activate_layer)
            self.core.map_refresh_requested.connect(self.gui.refresh_map)
            self.core.map_freeze_requested.connect(self.gui.freeze_map)
            self.core.zoom_full_requested.connect(self.gui.zoom_full)
            self.core.zoom_to_selected_requested.connect(self.gui.zoom_to_selected)
            self.core.set_node_visibility_requested.connect(self.gui.set_node_visibility)
