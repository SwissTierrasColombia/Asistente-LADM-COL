# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-04-17
        git sha              : :%H$
        copyright            : (C) 2017 by Jhon Galindo
        email                : jhonsigpjc@gmail.com
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

from ..utils.qfield_utils import (import_capture_model,
                                  organize_legend,
                                  change_multimedia_suppord,
                                  load_default_value,
                                  load_simbology)

from qgis.PyQt.QtCore import (Qt,
                              QSettings,
                              QCoreApplication,
                              QFile)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QFileDialog,
                                 QSizePolicy,
                                 QGridLayout)
from qgis.core import (Qgis,
                       QgsMapLayerProxyModel,
                       QgsProject,
                       QgsApplication,
                       QgsCoordinateReferenceSystem,
                       QgsWkbTypes)
from qgis.gui import QgsMessageBar

from ..config.help_strings import HelpStrings

from ..utils import get_ui_class

WIZARD_UI = get_ui_class('wiz_project_configuration_field_data_capture.ui')

class ProjectConfigurationFieldDataCaptureDialog(QDialog, WIZARD_UI):
    def __init__(self, iface, db, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._db = db
        self.help_strings = HelpStrings()
        self.buttonBox.accepted.connect(self.accepted)

    def show_help(self):
        self.qgis_utils.show_help("create_points")

    def accepted(self):
        settings = QSettings()
        filename, filter = QFileDialog.getSaveFileName(self,
                                   QCoreApplication.translate("ProjectConfigurationFieldDataCaptureDialog",
                                                              "Save File"),
                                   os.path.join(settings.value(
                        'Asistente-LADM_COL/wizards/project_configuration_field_data_captura_path', '.')),
                                   QCoreApplication.translate("ProjectConfigurationFieldDataCaptureDialog",
                                                              "GeoPackage Database (*.gpkg)"))

        if self.rad_geo.isChecked():
            import_capture_model('ili2gpkg', 'Captura_Geografica_V0_3', filename)
            organize_legend('Captura_Geografica_V0_3')
            change_multimedia_suppord()
            load_default_value()
            load_simbology()
        elif self.rad_alfa.isChecked():
            import_capture_model('ili2gpkg', 'Captura_Alfanumerica_V0_3', filename)
            organize_legend('Captura_Alfanumerica_V0_3')
            change_multimedia_suppord()
            load_default_value()
            load_simbology()