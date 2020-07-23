# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-07-23
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
from qgis.PyQt.QtCore import QCoreApplication
from qgis.gui import QgsPanelWidget

from asistente_ladm_col.utils import get_ui_class

WIDGET_UI = get_ui_class('field_data_capture/configure_surveyors_panel_widget.ui')


class ConfigureSurveyorsPanelWidget(QgsPanelWidget, WIDGET_UI):
    def __init__(self, parent):
        QgsPanelWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent

        self.setDockMode(True)
        self.setPanelTitle(QCoreApplication.translate("ConfigureSurveyorsPanelWidget", "Configure surveyors"))

        self.panelAccepted.connect(self.deselect_plots)

        self.fill_table()
        self.tbl_surveyors.resizeColumnsToContents()

    def deselect_plots(self):
        pass

    def fill_table(self):
        pass