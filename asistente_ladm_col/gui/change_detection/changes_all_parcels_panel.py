# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-05-16
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

from qgis.gui import QgsPanelWidgetStack, QgsPanelWidget

from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('change_detection/changes_all_parcels_panel_widget.ui')

class ChangesAllParcelsPanelWidget(QgsPanelWidget, WIDGET_UI):
    def __init__(self, iface, parent=None):
        QgsPanelWidget.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.setDockMode(True)
