"""
/***************************************************************************
Name                 : PyQT Models
Description          : Contains entity models for using in PyQt widgets
                       for those controls implementing the Model/View
                       framework
Date                 : 4/June/2013
copyright            : (C) 2013 by John Gitau
email                : gkahiu@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtCore import QAbstractItemModel, Qt, QModelIndex
from PyQt5.QtGui import QIcon, QBrush, QFont
from PyQt5.QtWidgets import QTreeWidgetItem


class QueryTreeViewModel(QAbstractItemModel):
    """
    Model for rendering social tenure relationship nodes in a tree view.
    @link: https://github.com/qgis/QGIS/blob/b315fbce8d23cc348a486bdcb0305667bbe9d8fc/python/plugins/db_manager/db_model.py#L292
    """
    def __init__(self, parent=None):
        QAbstractItemModel.__init__(self, parent)
        self.rootItem = QTreeWidgetItem(parent)

        self.agregar()

    def agregar(self):
        #item2 = QTreeWidgetItem(self.rootItem)
        #item2 = QTreeWidgetItem(['hola'])
        item2 = QTreeWidgetItem()
        icon_name = 'domains'
        icon = QIcon(":/Asistente-LADM_COL/resources/images/{}.png".format(icon_name))
        item2.setText(0, 'Jejeje')
        item2.setData(0, Qt.DecorationRole, icon)
        #item2.setData(1, Qt.UserRole, 1)
        item2.setData(0, Qt.DisplayRole, "Porque")
        item2.setData(1, Qt.DisplayRole, "Porque")
        item2.setData(3, Qt.DisplayRole, "Porque")
        item2.setData(0, Qt.ForegroundRole, QBrush(Qt.lightGray))
        font = QFont()
        font.setBold(True)
        item2.setData(0, Qt.FontRole, font)

        #self.rootItem.addChild(item2)

    def columnCount(self, parent):
        return 1

    def rowCount(self, parent):
        parentItem = parent.internalPointer() if parent.isValid() else self.rootItem
        return parentItem.childCount()

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        parentItem = parent.internalPointer() if parent.isValid() else self.rootItem
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def data(self, index, role):
        return None
