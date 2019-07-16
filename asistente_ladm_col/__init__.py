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
from qgis.core import (QgsApplication,
                       Qgis)

from .config.general_config import (PLUGIN_NAME,
                                    QGIS_REQUIRED_VERSION,
                                    QGIS_REQUIRED_VERSION_INT)


def classFactory(iface):
    if Qgis.QGIS_VERSION_INT >= QGIS_REQUIRED_VERSION_INT:

        is_installed_qmb = False
        try:
            from QgisModelBaker.libili2db import iliimporter
            is_installed_qmb = True
        except ImportError as e:
            iface.messageBar().pushMessage("Asistente LADM_COL",
                                           QCoreApplication.translate("__init__",
                                                                      "There was a problem loading the plugin 'QGIS Model Baker'. See the log for details."),
                                           1, 0)

            QgsApplication.messageLog().logMessage("ERROR while loading the plugin: " + repr(e), PLUGIN_NAME,
                                                   Qgis.Critical)


        try:
            from .asistente_ladm_col_plugin import AsistenteLADMCOLPlugin
        except ImportError as e:
            if is_installed_qmb:
                iface.messageBar().pushMessage("Asistente LADM_COL",
                                               QCoreApplication.translate("__init__",
                                                                          "There was a problem loading the plugin {}. See the log for details.").format(
                                                   PLUGIN_NAME),
                                               1, 0)

                QgsApplication.messageLog().logMessage("ERROR while loading the plugin: " + repr(e), PLUGIN_NAME,
                                                       Qgis.Critical)

            from mock import Mock
            return Mock()

        return AsistenteLADMCOLPlugin(iface)
    else:
        iface.messageBar().pushMessage("Asistente LADM_COL",
                                       QCoreApplication.translate("__init__",
                                                                  "{} plugin requires QGIS {} version or higher. Please install the required version.").format(
                                           PLUGIN_NAME,
                                           QGIS_REQUIRED_VERSION),
                                       1, 0)

        QgsApplication.messageLog().logMessage("ERROR while loading the plugin: ", PLUGIN_NAME, Qgis.Critical)

        from mock import Mock
        return Mock()
