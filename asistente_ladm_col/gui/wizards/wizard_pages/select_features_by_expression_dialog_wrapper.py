# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-09-10
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BFS Swissphoto)
                               (C) 2018 by Sergio Ramírez (Incige SAS)
                               (C) 2019 by Leo Cardona (BFS Swissphoto)
        email                : gcarrillo@linuxmail.org
                               sergio.ramirez@incige.com
                               leo.cardona.p@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
 """
from qgis.gui import QgsExpressionSelectionDialog


class SelectFeatureByExpressionDialogWrapper:
    """
    Wrapper class that extends selecting by expression.
    """

    def __init__(self, iface):
        self.__iface = iface
        self.__observer = None

    def register_observer(self, observer):
        self.__observer = observer

    def select_features_by_expression(self, layer):
        self.__iface.setActiveLayer(layer)
        dlg_expression_selection = QgsExpressionSelectionDialog(layer)
        layer.selectionChanged.connect(self.__observer.check_selected_features)
        dlg_expression_selection.exec()
        layer.selectionChanged.disconnect(self.__observer.check_selected_features)
