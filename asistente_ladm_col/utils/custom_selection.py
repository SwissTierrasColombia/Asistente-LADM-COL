# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 15/01/19
        git sha              : :%H$
        copyright            : (C) 2019 by Sergio Ramírez (Incige SAS)
        email                : sergio.ramirez@incige.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.gui import QgsMapTool
from qgis.PyQt.QtCore import pyqtSignal

class CustomSelection(QgsMapTool):
    after_click = pyqtSignal()
    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        #self.wizard = wizard

    def canvasReleaseEvent(self, event):
        #Get the click
        if event.button() == 2:
           # Your "if" code goes here
           print("click derecho")
           #self.wizard.setVisible(True)
           self.after_click.emit()
