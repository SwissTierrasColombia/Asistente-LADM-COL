# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin                : 2020-08-26
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
import os

from qgis.PyQt.QtCore import QCoreApplication
from asistente_ladm_col.gui.field_data_capture.base_split_data_for_receivers_panel import BaseSplitDataForReceiversPanelWidget


class SplitDataForCoordinatorsPanelWidget(BaseSplitDataForReceiversPanelWidget):
    def __init__(self, parent, controller):
        BaseSplitDataForReceiversPanelWidget.__init__(self, parent, controller)

        self.setPanelTitle(QCoreApplication.translate("SplitDataForCoordinatorsPanelWidget", "Generate data for coordinators"))
        self.lbl_receiver.setText(QCoreApplication.translate("SplitDataForCoordinatorsPanelWidget", "<b>Coordinator</b>"))
        self.btn_split_data.setToolTip(QCoreApplication.translate("SplitDataForCoordinatorsPanelWidget", "Generate XTF data for coordinators"))
        self.mQgsFileWidget.setDialogTitle(QCoreApplication.translate("SplitDataForCoordinatorsPanelWidget",
                                                                      "Select the folder to store XTF data for coordinators"))