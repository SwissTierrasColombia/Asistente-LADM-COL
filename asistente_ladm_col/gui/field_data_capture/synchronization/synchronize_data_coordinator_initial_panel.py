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


class SynchronizeDataCoordinatorInitialPanelWidget(BaseSynchronizeDataInitialPanelWidget):
    def __init__(self, parent, controller, db):
        BaseSynchronizeDataInitialPanelWidget.__init__(self, parent, controller, db)

        self.grb_original_db.setTitle(QCoreApplication.translate("SynchronizeDataCoordinatorInitialPanelWidget",
                                                                 "Original database (Coordinator)"))

        self.grb_input_file.setTitle(QCoreApplication.translate("SynchronizeDataCoordinatorInitialPanelWidget",
                                                                "GeoPackage file from surveyor"))

        self.qfw_input_file.lineEdit().setPlaceholderText(QCoreApplication.translate(
            "SynchronizeDataCoordinatorInitialPanelWidget", "Choose the input GeoPackage file..."))
        self.qfw_input_file.setDefaultRoot(self.app.settings.fdc_project_template_path)
        self.qfw_input_file.setDialogTitle(QCoreApplication.translate("SynchronizeDataCoordinatorInitialPanelWidget",
                                                                      "Select the GeoPackage file from surveyor"))
        self.qfw_input_file.setFilter('GeoPackage Database (*.gpkg)')
