# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin                : 2020-10-22
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

from asistente_ladm_col.gui.field_data_capture.base_synchronize_data_initial_panel import BaseSynchronizeDataInitialPanelWidget


class SynchronizeDataAdminInitialPanelWidget(BaseSynchronizeDataInitialPanelWidget):
    def __init__(self, parent, controller, db):
        BaseSynchronizeDataInitialPanelWidget.__init__(self, parent, controller, db)

        self.grb_original_db.setTitle(QCoreApplication.translate("SynchronizeDataAdminInitialPanelWidget",
                                                                 "Original database (Administrator)"))

        self.grb_input_file.setTitle(QCoreApplication.translate("SynchronizeDataAdminInitialPanelWidget",
                                                                "XTF file from coordinator"))

        self.qfw_input_file.lineEdit().setPlaceholderText(QCoreApplication.translate(
            "SynchronizeDataAdminInitialPanelWidget", "Choose the input XTF file..."))
        self.qfw_input_file.setDefaultRoot(self.app.settings.fdc_project_template_path)
        self.qfw_input_file.setDialogTitle(QCoreApplication.translate("SynchronizeDataAdminInitialPanelWidget",
                                                                      "Select the XTF file from coordinator"))
        self.qfw_input_file.setFilter('INTERLIS 2 transfer format (*.xtf)')