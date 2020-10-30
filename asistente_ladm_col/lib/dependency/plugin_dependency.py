# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-06-30
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
import tempfile

from qgis.PyQt.QtCore import (QCoreApplication,
                              QFile,
                              QIODevice,
                              pyqtSignal)
import pyplugin_installer

from asistente_ladm_col.lib.dependency.dependency import Dependency
from asistente_ladm_col.utils.utils import is_plugin_version_valid


class PluginDependency(Dependency):
    download_dependency_completed = pyqtSignal()
    download_dependency_progress_changed = pyqtSignal(int)  # progress

    def __init__(self, plugin_name, plugin_min_required_version, plugin_exact_required_version, plugin_required_version_url=''):
        Dependency.__init__(self)
        self.dependency_name = QCoreApplication.translate("Dependency", "plugin")
        self.plugin_name = plugin_name
        self.plugin_min_required_version = plugin_min_required_version
        self.plugin_exact_required_version = plugin_exact_required_version
        self.plugin_required_version_url = plugin_required_version_url

        _, self._tmp_file = tempfile.mkstemp(".zip")

        self.download_dependency_completed.connect(self.__install_plugin_from_zip)

    def _save_dependency_file(self):
        self.logger.status(QCoreApplication.translate("Dependency", "The plugin ZIP file was downloaded!"))

    def install(self):
        self.download_dependency(self.plugin_required_version_url)

    def __install_plugin_from_zip(self):
        if os.path.isfile(self._get_tmp_file()):
            pyplugin_installer.instance().installFromZipFile(self._get_tmp_file())
            self.logger.success_msg(__name__, QCoreApplication.translate("Dependency",
                "The plugin '{}' was successfully installed!").format(self.plugin_name))
        else:
            self.logger.warning_msg(__name__, QCoreApplication.translate("Dependency",
                "There was a problem installing the plugin. Plugin's ZIP file could not be found!"))

        self.logger.clear_status()

        try:
            os.remove(self._get_tmp_file())
        except:
            pass

    def check_if_dependency_is_valid(self):
        return is_plugin_version_valid(self.plugin_name,
                                       self.plugin_min_required_version,
                                       self.plugin_exact_required_version)