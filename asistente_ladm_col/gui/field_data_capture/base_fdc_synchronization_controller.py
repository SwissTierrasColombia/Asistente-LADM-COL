# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin                : 2020-10-22
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
from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject,
                              pyqtSignal)

from asistente_ladm_col.app_interface import AppInterface


class BaseFDCSynchronizationController(QObject):
    field_data_capture_layer_removed = pyqtSignal()

    def __init__(self, iface, db, ladm_data):
        QObject.__init__(self)
        self.iface = iface
        self._db = db
        self._ladm_data = ladm_data

        self.app = AppInterface()

    def db(self):
        return self._db

    def plot_layer(self):
        return self._layers[self._db.names.FDC_PLOT_T]

    def parcel_layer(self):
        return self._layers[self._db.names.FDC_PARCEL_T]

    def user_layer(self):
        return self._layers[self._db.names.FDC_USER_T]
