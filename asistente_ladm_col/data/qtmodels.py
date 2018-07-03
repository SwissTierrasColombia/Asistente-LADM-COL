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
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, Qt
from db_manager.db_model import TreeItem


class TreeViewModel(QAbstractItemModel):
    """
    Model for rendering social tenure relationship nodes in a tree view.
    """
    def __init__(self, root, parent=None, view=None):
        QAbstractItemModel.__init__(self,parent)
        TreeItem
        self._rootNode = root
        self._view = view

    def rowCount(self, parent=QModelIndex()):
        if not parent.isValid():
            parentNode = self._rootNode

        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()

    def columnCount(self, parent=QModelIndex()):
        return self._rootNode.columnCount()

    def _getNode(self,index):
        """
        Convenience method for extracting STRNodes from the model index.
        """
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node

        return self._rootNode

    def data(self, index, role):
        """
        Data to be displayed in the tree view.
        """
        if not index.isValid():
            return None

        node = self._getNode(index)

        if role == Qt.DisplayRole or role == Qt.EditRole:
            if index.column() >= node.columnCount():
                return None

            return node.data(index.column())

        elif role == Qt.DecorationRole:
            if index.column() == 0:
                if not node.icon() is None and node.depth() > 1:
                    return node.icon()

        elif role == Qt.FontRole:
            if index.column() == 0:
                if node.styleIfChild():
                    if self._view is not None:
                        currFont = self._view.font()
                        currFont.setBold(True)
                        return currFont

        elif role == Qt.ToolTipRole:
            if index.column() >= node.columnCount():
                return None

            return node.data(index.column())

        else:
            return None

    def headerData(self, section, orientation, role):
        """
        Set the column headers to be displayed by the tree view.
        """
        if self._rootNode.columnCount() == 0:
            return

        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._rootNode.data(section)

        elif orientation == Qt.Vertical and role == Qt.DisplayRole:
            return section + 1

        return None

    def flags(self,index):
        return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable

    def parent(self,index):
        """
        Returns a QModelIndex reference of the parent node.
        """
        if not index.isValid():
            return QModelIndex()

        node = self._getNode(index)

        parentNode = node.parent()

        if parentNode == self._rootNode or parentNode == None:
            return QModelIndex()

        return self.createIndex(parentNode.row(), 0, parentNode)

    def index(self, row, column, parent=QModelIndex()):
        if parent.isValid() and parent.column() != 0:
            return QModelIndex()

        parentNode = self._getNode(parent)

        childItem = parentNode.child(row)

        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def removeAllChildren(self, position, count, parent=QModelIndex()):
        """
        Removes all children under the node with the specified parent index.
        """
        parentNode = self._getNode(parent)
        success = True

        self.beginRemoveRows(parent, position, position + count - 1)

        success = parentNode.clear()

        self.endRemoveRows()

        return success

    def removeRows(self,position,count,parent=QModelIndex()):
        """
        Removes count rows starting with the given position under parent from the model.
        """
        parentNode = self._getNode(parent)
        success = True

        self.beginRemoveRows(parent, position, position + count - 1)

        for row in range(count):
            success = parentNode.removeChild(position)

        self.endRemoveRows()

        return success

    def insertRows(self,position,count,parent=QModelIndex()):
        """
        Insert children starting at the given position for the given parent item.
        """
        parentNode = self._getNode(parent)
        success = True

        self.beginInsertRows(parent,position,position + count -1)
        '''
        We do not insert any children in this case since the internal methods of the
        BaseSTRNode have already inserted the children nodes that contain the
        information.
        '''
        self.endInsertRows()

        return success

    def removeColumns(self,position,columnCount,parent = QModelIndex()):
        success = True

        self.beginRemoveColumns(parent, position, position + columnCount-1)
        success = self._rootNode.removeColumns(position, columnCount)
        self.endRemoveColumns()

        if self._rootNode.columnCount() == 0:
            self.removeRows(0, self.rowCount())

        return success

    def clear(self):
        """
        Removes all items (rows and columns) in the model.
        """
        rootChildrenNum = self._rootNode.childCount()
        self.beginResetModel()

        #Delete each child individually then clear the root node or else there will be indexing issues
        for i in range(rootChildrenNum):
            childNode = self._rootNode.child(i)
            childNode._parent = None
            del childNode

        self._rootNode.clear()
        #TODO: Clear columns
        self.endResetModel()

    def setData(self, index, value, role):
        """
        Sets the role data for the item at index to value.
        """
        if role == Qt.EditRole or role == Qt.DisplayRole:
            nodeItem = self._getNode(index)
            result = nodeItem.setData(index.column(), value)

            if result:
                self.dataChanged.emit(index,index)

            return result

        return False