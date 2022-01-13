"""
/***************************************************************************
                              Asistente LADM-COL
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
from qgis.PyQt.QtCore import (QCoreApplication,
                              QEventLoop)
from qgis.core import Qgis

from asistente_ladm_col.lib.dependency.plugin_dependency import PluginDependency
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.config.general_config import (PLUGIN_NAME,
                                                      QGIS_REQUIRED_VERSION,
                                                      QGIS_REQUIRED_VERSION_INT,
                                                      QGIS_MODEL_BAKER_PLUGIN_NAME,
                                                      QGIS_MODEL_BAKER_EXACT_REQUIRED_VERSION,
                                                      QGIS_MODEL_BAKER_MIN_REQUIRED_VERSION,
                                                      QGIS_MODEL_BAKER_REQUIRED_VERSION_URL)
from asistente_ladm_col.utils.utils import is_plugin_version_valid


def classFactory(iface):
    if Qgis.QGIS_VERSION_INT >= QGIS_REQUIRED_VERSION_INT:
        # Do we need to install Model Baker on our own?
        valid_dependency = is_plugin_version_valid(QGIS_MODEL_BAKER_PLUGIN_NAME,
                                                   QGIS_MODEL_BAKER_MIN_REQUIRED_VERSION,
                                                   QGIS_MODEL_BAKER_EXACT_REQUIRED_VERSION)

        if not valid_dependency:
            # Only create the dependency object if we know that we need to install the dependency
            qmb_plugin = PluginDependency(QGIS_MODEL_BAKER_PLUGIN_NAME,
                                          QGIS_MODEL_BAKER_MIN_REQUIRED_VERSION,
                                          QGIS_MODEL_BAKER_EXACT_REQUIRED_VERSION,
                                          QGIS_MODEL_BAKER_REQUIRED_VERSION_URL)
            loop = QEventLoop()  # Do the installation synchronously
            qmb_plugin.download_dependency_completed.connect(loop.exit)
            qmb_plugin.install()
            Logger().info(__name__, "Installing dependency ({} {})...".format(QGIS_MODEL_BAKER_PLUGIN_NAME,
                                                                              QGIS_MODEL_BAKER_MIN_REQUIRED_VERSION))
            loop.exec()

        try:
            Logger().info(__name__, "STARTING LADM-COL ASSISTANT...")
            from .asistente_ladm_col_plugin import AsistenteLADMCOLPlugin
        except ImportError as e:
            iface.messageBar().clearWidgets()
            widget = iface.messageBar().createMessage("Asistente LADM-COL", QCoreApplication.translate("__init__",
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

        try:
            from asistente_ladm_col.tests.gui_tests import gui_tests_model_baker
            from qgistester.tests import addTestModule
            addTestModule(gui_tests_model_baker, PLUGIN_NAME)
        except:
            Logger().debug(__name__, "QGIS Tester plugin was not found. Therefore, no GUI tests could be registered!")

        return AsistenteLADMCOLPlugin(iface)
    else:
        iface.messageBar().pushMessage("Asistente LADM-COL",
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
