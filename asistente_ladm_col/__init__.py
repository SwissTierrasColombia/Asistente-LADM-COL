# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2017-10-31
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
from qgis.PyQt.QtCore import QCoreApplication

def classFactory(iface):
    try:
        from .asistente_ladm_col_plugin import AsistenteLADMCOLPlugin
    except ImportError as e:
        iface.messageBar().pushMessage("Asistente LADM_COL",
            QCoreApplication.translate("__init__",
               "The plugin Asistente LADM_COL requires a newer version of QGIS! \
               If you're on Windows, you can download a recent version from \
               <a target=\"_blank\" href=\"https://qgis.org/downloads/weekly/\">this link</a>. \
               Otherwise, use a <a href=\"https://qgis.org/en/site/forusers/download.html\" target=\"_blank\">nightly build</a>."),
            1, 0) # We don't use Qgis.Info because it was introduced after 2.99

        from mock import Mock
        return Mock()

    return AsistenteLADMCOLPlugin(iface)
