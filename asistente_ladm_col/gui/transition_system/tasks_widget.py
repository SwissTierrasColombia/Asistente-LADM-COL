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
from qgis.PyQt.QtCore import (pyqtSignal,
                              QCoreApplication)
from qgis.PyQt.QtWidgets import QWidget

from asistente_ladm_col.utils.ui import get_ui_class

WIDGET_UI = get_ui_class('transition_system/tasks_widget.ui')


class TasksWidget(QWidget, WIDGET_UI):
    def __init__(self, user):
        QWidget.__init__(self)
        self.setupUi(self)

        self.btn_start_task.clicked.connect(self.start_task)
        self.btn_close_task.clicked.connect(self.close_task)

    def start_task(self):
        print("TASK STARTED!")

    def close_task(self):
        print("TASK CLOSED!")
