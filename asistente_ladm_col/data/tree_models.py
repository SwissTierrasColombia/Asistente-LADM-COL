# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2017 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################
from qgis.PyQt.QtCore import (
    QAbstractItemModel,
    QModelIndex,
    Qt,
    QVariant)
from qgis.PyQt.QtGui import QColor, QIcon, QBrush, QFont

from ..config.table_mapping_config import DICT_PACKAGE_ICON, DICT_TABLE_PACKAGE, DICT_PLURAL


class TreeItem(object):
    def __init__(self, data, parent=None):
        """
        :param data: list of dicts. Each element in the list represents the data of a column. Such data should have
                     at least a Qt.DisplayRole.
        :param parent:
        """
        self.parentItem = parent
        self.itemData = [{Qt.DisplayRole: ""}]
        self.childItems = []

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def childNumber(self):
        if self.parentItem != None:
            return self.parentItem.childItems.index(self)
        return 0

    def columnCount(self):
        return len(self.itemData)

    def data(self, column, role=Qt.DisplayRole):
        if role not in self.itemData[column]:
            return None

        return self.itemData[column][role]

    def insertChildren(self, position, count, columns):
        if position < 0 or position > len(self.childItems):
            return False

        for row in range(count):
            data = [{Qt.DisplayRole: None} for v in range(columns)]
            item = TreeItem(data, self)
            self.childItems.insert(position, item)

        return True

    def insertColumns(self, position, columns):
        if position < 0 or position > len(self.itemData):
            return False

        for column in range(columns):
            self.itemData.insert(position, {Qt.DisplayRole: None})

        for child in self.childItems:
            child.insertColumns(position, columns)

        return True

    def parent(self):
        return self.parentItem

    def removeChildren(self, position, count):
        if position < 0 or position + count > len(self.childItems):
            return False

        for row in range(count):
            self.childItems.pop(position)

        return True

    def removeColumns(self, position, columns):
        if position < 0 or position + columns > len(self.itemData):
            return False

        for column in range(columns):
            self.itemData.pop(position)

        for child in self.childItems:
            child.removeColumns(position, columns)

        return True

    def setData(self, column, value, role=Qt.DisplayRole):
        if column < 0 or column >= len(self.itemData):
            return False

        self.itemData[column][role] = value

        return True


class TreeModel(QAbstractItemModel):
    def __init__(self, headers=None, data=None, parent=None):
        super(TreeModel, self).__init__(parent)

        rootData = ("",) # [header for header in headers]
        self.rootItem = TreeItem(rootData)
        self.setupModelData(data, self.rootItem)

    def columnCount(self, parent=QModelIndex()):
        return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role in (Qt.DisplayRole, Qt.UserRole, Qt.ToolTipRole, Qt.DecorationRole, Qt.ForegroundRole, Qt.FontRole):
            return self.getItem(index).data(index.column(), role)
        else:
            return QVariant()


    def flags(self, index):
        if not index.isValid():
            return 0

        return super(TreeModel, self).flags(index)

    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self.rootItem

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row, column, parent=QModelIndex()):
        if parent.isValid() and parent.column() != 0:
            return QModelIndex()

        parentItem = self.getItem(parent)
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def insertColumns(self, position, columns, parent=QModelIndex()):
        self.beginInsertColumns(parent, position, position + columns - 1)
        success = self.rootItem.insertColumns(position, columns)
        self.endInsertColumns()

        return success

    def insertRows(self, position, rows, parent=QModelIndex()):
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        success = parentItem.insertChildren(position, rows,
                self.rootItem.columnCount())
        self.endInsertRows()

        return success

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = self.getItem(index)
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.childNumber(), 0, parentItem)

    def removeColumns(self, position, columns, parent=QModelIndex()):
        self.beginRemoveColumns(parent, position, position + columns - 1)
        success = self.rootItem.removeColumns(position, columns)
        self.endRemoveColumns()

        if self.rootItem.columnCount() == 0:
            self.removeRows(0, self.rowCount())

        return success

    def removeRows(self, position, rows, parent=QModelIndex()):
        parentItem = self.getItem(parent)

        self.beginRemoveRows(parent, position, position + rows - 1)
        success = parentItem.removeChildren(position, rows)
        self.endRemoveRows()

        return success

    def rowCount(self, parent=QModelIndex()):
        parentItem = self.getItem(parent)

        return parentItem.childCount()

    def setData(self, index, value, role=Qt.DisplayRole):
        if role not in (Qt.DisplayRole, Qt.UserRole, Qt.ToolTipRole, Qt.DecorationRole, Qt.ForegroundRole, Qt.FontRole):
            return False

        item = self.getItem(index)
        result = item.setData(index.column(), value, role)

        if result:
            self.dataChanged.emit(index, index)

        return result

    def setHeaderData(self, section, orientation, value, role=Qt.DisplayRole):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return False

        result = self.rootItem.setData(section, value)
        if result:
            self.headerDataChanged.emit(orientation, section, section)

        return result

    def setupModelData(self, data, parent=None):
        if data is None:
            return

        if parent is None:
            parent = self.rootItem

        if data is None:
            return

        #print(data)
        for record in data:
            self.fill_model(record, parent)

    def fill_model(self, record, parent):
        """
        Fill data in the treeview depending on the structure. It expects JSON data. The JSON data may contain LADM_COL
        object collections in the form:
            "ladm_col_table_name" : [{"id": 5, "records":{k,v pairs}}, {"id": 5, "records":{k,v pairs}}, ...]
        """
        for key, values in record.items():  # either tuple or dict
            if type(values) is list:
                if not len(values):
                    parent.insertChildren(parent.childCount(), 1, self.rootItem.columnCount())
                    kv_item = parent.child(parent.childCount() - 1)
                    kv_item.setData(0, "{} (0)".format(DICT_PLURAL[key] if key in DICT_PLURAL else key))
                    kv_item.setData(0, QBrush(Qt.lightGray), Qt.ForegroundRole)
                    kv_item.setData(0, {"type": key}, Qt.UserRole)
                    kv_item.setData(0, QIcon(
                        DICT_PACKAGE_ICON[DICT_TABLE_PACKAGE[key]]) if key in DICT_TABLE_PACKAGE else None,
                                                    Qt.DecorationRole)
                    continue

                for value in values:
                    if type(value) is dict:
                        if len(value) == 2 and 'id' in value and 'attributes' in value:
                            # We have a list of LADM_COL model objects, we deal differently with them...
                            self.fill_collection(key, values, parent)
                            break
            elif type(values) is dict:
                # Dict of key-value pairs, reuse the function
                self.fill_model(values, parent)
            else:
                # Simple key-value pair
                parent.insertChildren(parent.childCount(), 1, self.rootItem.columnCount())
                kv_item = parent.child(parent.childCount() - 1)
                kv_item.setData(0, "{}: {}".format(key, values))
                kv_item.setData(0, {"value": values}, Qt.UserRole)
                if values is None:
                    kv_item.setData(0, QBrush(Qt.lightGray), Qt.ForegroundRole)

    def fill_collection(self, key, collection, parent):
        """
        Fill a collection of LADM_COL objects
        """
        parent.insertChildren(parent.childCount(), 1, self.rootItem.columnCount())
        collection_parent = parent.child(parent.childCount() - 1)
        collection_parent.setData(0, "{} ({})".format(DICT_PLURAL[key] if key in DICT_PLURAL else key, len(collection)))
        collection_parent.setData(0, {"type": key}, Qt.UserRole)
        res = collection_parent.setData(0, QIcon(
            DICT_PACKAGE_ICON[DICT_TABLE_PACKAGE[key]]) if key in DICT_TABLE_PACKAGE else None, Qt.DecorationRole)

        for object in collection:
            # Fill LADM_COL object
            collection_parent.insertChildren(collection_parent.childCount(), 1, self.rootItem.columnCount())
            object_parent = collection_parent.child(collection_parent.childCount() - 1)
            object_parent.setData(0, "t_id: {}".format(object['id']))
            object_parent.setData(0, {"type": key, "id": object['id'], "value": object['id']}, Qt.UserRole)
            object_parent.setData(0, key, Qt.ToolTipRole)
            font = QFont()
            font.setBold(True)
            object_parent.setData(0, font, Qt.FontRole)
            self.fill_model(object['attributes'], object_parent)
