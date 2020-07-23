# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin                : 2020-07-22
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
from qgis.gui import QgsPanelWidget
from qgis.PyQt.QtCore import QCoreApplication

from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('field_data_capture/allocate_parcels_initial_panel_widget.ui')


class AllocateParcelsFieldDataCapturePanelWidget(QgsPanelWidget, WIDGET_UI):
    def __init__(self, parent):
        QgsPanelWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent

        self.setDockMode(True)
        self.setPanelTitle(QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget", "Allocate parcels"))
        self.parent.setWindowTitle(QCoreApplication.translate("AllocateParcelsFieldDataCapturePanelWidget", "Allocate parcels"))

        self.tbl_parcels.resizeColumnsToContents()
        self.prb_to_offline.setVisible(False)

        self.btn_configure_surveyors.clicked.connect(self.parent.show_configure_surveyors_panel)
        self.btn_allocate.clicked.connect(self.parent.show_allocate_parcels_to_surveyor_panel)

    def fill_data(self):
        pass