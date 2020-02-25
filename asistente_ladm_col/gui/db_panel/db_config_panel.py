# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-02-21
        git sha              : :%H$
        copyright            : (C) 2019 by Yesid Polanía (BSF Swissphoto)
        email                : yesidpol.3@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import QWidget
from qgis.core import Qgis


class DbConfigPanel(QWidget):

    notify_message_requested = pyqtSignal(str, Qgis.MessageLevel)

    def __init__(self, parent: QWidget):
        QWidget.__init__(self, parent)
        self.state = None

    def read_connection_parameters(self):
        """
        Convenient function to read connection parameters and apply default
        values if needed.
        """
        raise NotImplementedError

    def write_connection_parameters(self, dict_conn):
        raise NotImplementedError

    def get_keys_connection_parameters(self):
        raise NotImplementedError

    def set_action(self, action):
        pass

    def save_state(self):
        self.state = self.read_connection_parameters()

    def state_changed(self):
        raise NotImplementedError
