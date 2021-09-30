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
                               (C) 2021 by Yesid Polanía (BFS Swissphoto)
        email                : gcarrillo@linuxmail.org
                               sergio.ramirez@incige.com
                               leo.cardona.p@gmail.com
                               yesidpol.3@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
 """
from qgis.PyQt.QtCore import (QObject,
                             pyqtSignal)
from qgis.gui import QgsExpressionSelectionDialog


class SelectFeatureByExpressionDialogWrapper(QObject):
    """
    Wrapper class that extends selecting by expression.
    """
    feature_selection_by_expression_changed = pyqtSignal()

    def __init__(self, iface):
        QObject.__init__(self)
        self.__iface = iface

    def select_features_by_expression(self, layer):
        self.__iface.setActiveLayer(layer)
        dlg_expression_selection = QgsExpressionSelectionDialog(layer)
        layer.selectionChanged.connect(self.feature_selection_by_expression_changed)
        dlg_expression_selection.exec()
        layer.selectionChanged.disconnect(self.feature_selection_by_expression_changed)
