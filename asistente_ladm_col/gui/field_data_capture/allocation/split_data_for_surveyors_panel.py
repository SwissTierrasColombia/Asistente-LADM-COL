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

from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication)
from qgis.core import QgsMapLayerProxyModel

from asistente_ladm_col.config.enums import EnumLogHandler
from asistente_ladm_col.gui.field_data_capture.base_split_data_for_receivers_panel import BaseSplitDataForReceiversPanelWidget
from asistente_ladm_col.utils.qt_utils import OverrideCursor


class SplitDataForSurveyorsPanelWidget(BaseSplitDataForReceiversPanelWidget):
    def __init__(self, parent, controller):
        BaseSplitDataForReceiversPanelWidget.__init__(self, parent, controller)

        self.setPanelTitle(QCoreApplication.translate("SplitDataForSurveyorsPanelWidget", "Convert to offline"))
        self.lbl_receiver.setText(QCoreApplication.translate("SplitDataForSurveyorsPanelWidget", "<b>Surveyor</b>"))
        self.btn_split_data.setToolTip(QCoreApplication.translate("SplitDataForSurveyorsPanelWidget", "Generate offline projects"))
        self.mQgsFileWidget.setDialogTitle(QCoreApplication.translate("SplitDataForSurveyorsPanelWidget",
                                                                      "Select the folder to store offline projects"))

        self.qfw_file_template.lineEdit().setPlaceholderText(QCoreApplication.translate(
            "SplitDataForSurveyorsPanelWidget", "Choose the .qgs project template..."))
        self.qfw_file_template.setDefaultRoot(self.app.settings.fdc_project_template_path)
        self.qfw_file_template.setDialogTitle(QCoreApplication.translate("SplitDataForSurveyorsPanelWidget",
                                                                         "Select the QGS project to be used as template"))
        self.qfw_file_template.setFilter('QGIS projects (*.qgs)')

        self.cbo_raster_layer.setFilters(QgsMapLayerProxyModel.RasterLayer)

        self.grb_template_project.setVisible(True)
        self.grb_raster_layer.setVisible(True)

    def export_field_data(self):
        self.logger.clear_message_bar()
        self._controller.raster_layer = self.cbo_raster_layer.currentLayer()

        template_path = self.qfw_file_template.filePath()
        if template_path and os.path.isfile(template_path):
            self._controller.template_project_path = template_path
            self.app.settings.fdc_project_template_path = template_path
        else:
            self._controller.template_project_path = ''
            self.logger.warning_msg(__name__, QCoreApplication.translate("SplitDataForSurveyorsPanelWidget",
                                                                         "First, choose a valid QGS project template for the field data capture."))
            return

        export_dir = self.mQgsFileWidget.filePath()
        if export_dir and os.path.isdir(export_dir):
            self.app.settings.export_dir_field_data = export_dir
            self.prb_export_field_data.setRange(0, 100)
            self.prb_export_field_data.setValue(0)

            with OverrideCursor(Qt.WaitCursor):
                res, msg = self._controller.export_field_data(export_dir)

            self.logger.success_warning(__name__, res, msg, EnumLogHandler.MESSAGE_BAR)
        else:
            self.logger.warning_msg(__name__, QCoreApplication.translate("SplitDataForSurveyorsPanelWidget", "The output folder is invalid. Choose a valid folder."))
