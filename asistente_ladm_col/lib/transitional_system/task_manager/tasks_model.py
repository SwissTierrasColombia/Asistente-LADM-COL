# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-12-02
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
from qgis.PyQt.QtCore import (Qt,
                              QAbstractListModel,
                              QAbstractItemModel,
                              QModelIndex,
                              QVariant)


class TasksModel(QAbstractListModel):
    def __init__(self, data, parent=None, *args):
        QAbstractListModel.__init__(self, parent, *args)
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        if row < 0 or row >= len(self._data):
            return None

        return self._data[index.row()]

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
