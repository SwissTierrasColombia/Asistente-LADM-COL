# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-08-25
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

from asistente_ladm_col.gui.field_data_capture.base_configure_receivers_panel import BaseConfigureReceiversPanelWidget


class ConfigureCoordinatorsPanelWidget(BaseConfigureReceiversPanelWidget):
    def __init__(self, parent, controller):
        BaseConfigureReceiversPanelWidget.__init__(self, parent, controller)

        self.setPanelTitle(QCoreApplication.translate("ConfigureSurveyorsPanelWidget", "Configure coordinators"))


