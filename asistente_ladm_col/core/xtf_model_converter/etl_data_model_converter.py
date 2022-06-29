# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2022-06-28
        git sha              : :%H$
        copyright            : (C) 2022 by Sergio Ramírez (Swisstierras Colombia)
        email                : sramirez@colsolutions.com

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
from qgis.core import (QgsProcessingException,
                       QgsProject,
                       QgsVectorLayer,
                       Qgis)
import processing

from asistente_ladm_col.config.general_config import BLO_LIS_FILE_PATH
from asistente_ladm_col.core.supplies.etl_supplies import ETLSupplies
from asistente_ladm_col.utils.qt_utils import normalize_local_url

class ETLDataModelConverter(ETLSupplies):
    pass