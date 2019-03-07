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
from qgis.PyQt.QtCore import (QObject,pyqtSignal)
from qgis.core import (Qgis)


class DbConfigPanel(QObject):

    notify_message_requested = pyqtSignal(str, Qgis.MessageLevel)

    def __init__(self):
        super(DbConfigPanel, self).__init__()
        self._mode = None
        self.params_changed = False

    def read_connection_parameters(self):
        """
        Convenient function to read connection parameters and apply default
        values if needed.
        """
        raise Exception('unimplemented method')

    def write_connection_parameters(self, dict_conn):
        raise Exception('unimplemented method')

    def get_keys_connection_parameters(self):
        raise Exception('unimplemented method')

    def _set_params_changed(self):
        self.params_changed = True

    def set_action(self, action):
        pass