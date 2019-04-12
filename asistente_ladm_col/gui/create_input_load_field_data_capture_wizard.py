# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2017-11-14
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BSF Swissphoto)
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
import stat

from qgis.PyQt.QtCore import (Qt,
                              QSettings,
                              QCoreApplication,
                              QFile)
from qgis.PyQt.QtWidgets import (QWizard,
                                 QFileDialog,
                                 QSizePolicy,
                                 QGridLayout)
from qgis.core import (Qgis,
                       QgsMapLayerProxyModel,
                       QgsApplication,
                       QgsCoordinateReferenceSystem,
                       QgsWkbTypes)
from qgis.gui import QgsMessageBar

from ..config.general_config import (PLUGIN_NAME,
                                     DEFAULT_EPSG,
                                     FIELD_MAPPING_PATH)
from ..config.help_strings import HelpStrings
from ..config.table_mapping_config import (BOUNDARY_POINT_TABLE,
                                           SURVEY_POINT_TABLE,
                                           CONTROL_POINT_TABLE)

from ..processing.algs.InsertFeaturesToLayer import InsertFeaturesToLayer
from ..utils import get_ui_class
from ..utils.qt_utils import (make_file_selector,
                              enable_next_wizard,
                              disable_next_wizard,
                              normalize_local_url)

WIZARD_UI = get_ui_class('wiz_input_load_field_data_capture.ui')


class InputLoadFieldDataCaptureWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()
        self.insert_features_to_layer = InsertFeaturesToLayer()

        self.target_layer = None

        # Auxiliary data to set nonlinear next pages
        self.pages = [self.wizardPage1, self.wizardPage2, self.wizardPage3]
        self.dict_pages_ids = {self.pages[idx] : pid for idx, pid in enumerate(self.pageIds())}

        # Set connections
        self.btn_browse_file.clicked.connect(
            make_file_selector(self.txt_file_path,
                               file_filter=QCoreApplication.translate("CreatePointsCadastreWizard",'CSV File (*.csv *.txt)')))
        
    def nextId(self):
        """
        Set navigation order. Should return an integer. -1 is Finish.
        """
        if self.currentId() == self.dict_pages_ids[self.wizardPage1]:
            return self.dict_pages_ids[self.wizardPage2]
        elif self.currentId() == self.dict_pages_ids[self.wizardPage2]:
            if self.rad_csv.isChecked():
                return self.dict_pages_ids[self.wizardPage3]
            elif self.rad_refactor.isChecked():
                return -1
        elif self.currentId() == self.dict_pages_ids[self.wizardPage3]:
            return -1
        else:
            return -1

    def show_help(self):
        self.qgis_utils.show_help("create_points")
