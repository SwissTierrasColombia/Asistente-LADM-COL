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
from functools import partial

from qgis.PyQt.QtWidgets import QPushButton
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsApplication,
                       Qgis)

from asistente_ladm_col.lib.logger import Logger
from .config.general_config import (PLUGIN_NAME,
                                    QGIS_REQUIRED_VERSION,
                                    QGIS_REQUIRED_VERSION_INT)


def classFactory(iface):
    if Qgis.QGIS_VERSION_INT >= QGIS_REQUIRED_VERSION_INT:
        try:
            from .asistente_ladm_col_plugin import AsistenteLADMCOLPlugin
        except ImportError as e:
            iface.messageBar().clearWidgets()
            widget = iface.messageBar().createMessage("Asistente LADM_COL", QCoreApplication.translate("__init__",
                                                      "There was a problem loading the plugin {}. See the log for details.").format(
                                               PLUGIN_NAME))
            button = QPushButton(widget)
            button.setText(QCoreApplication.translate("__init__", "Open log panel..."))
            button.pressed.connect(partial(open_log, iface))
            widget.layout().addWidget(button)
            iface.messageBar().pushWidget(widget, Qgis.Warning, 0)

            Logger().critical(__name__, "ERROR while loading the plugin: " + repr(e))

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

        Logger().critical(__name__, "ERROR while loading the plugin: QGIS version {} not supported! Required: {}".format(Qgis.QGIS_VERSION_INT, QGIS_REQUIRED_VERSION_INT))

        from mock import Mock
        return Mock()

def open_log(iface):
    iface.messageBar().clearWidgets()
    iface.openMessageLog()