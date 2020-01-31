# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-02-06
        git sha              : :%H$
        copyright            : (C) 2019 by Jhon Galindo (Incige SAS)
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
import hashlib
import shutil
from functools import partial

import qgis.utils
from qgis.PyQt.QtCore import QObject, QCoreApplication

from asistente_ladm_col.config.general_config import DEPENDENCIES_BASE_PATH
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.qt_utils import (get_plugin_metadata,
                                               remove_readonly,
                                               normalize_local_url)


class Utils(QObject):
    """
    Utility methods are here to be able to use internationalization on some messages
    """
    def __init__(self):
        QObject.__init__(self)
 
    def set_time_format(self, time):
        time_format = '.1f'
        unit_millisecond = "ms"
        unit_second = "seg"
        unit_minutes = "min"
        unit_hours = "h"
        unit_days = "D"
        
        if time < 1:
            return "{}{}".format(format(time*1000, '.0f'), unit_millisecond)
        elif time < 60:
            return "{}{}".format(format(time, time_format), unit_second)
        elif time >= 60 and time < 3600:
            minu = int(time/float(60))
            seg = 60*(time/float(60) - minu)
            return "{}{} {}{}".format(minu, unit_minutes, format(seg, time_format), unit_second)
        elif time >= 3600 and time < 86400:
            h = int(time/float(3600))
            minu = int(60*(time/float(3600) - h))
            seg = 60*((60*(time/float(3600) - h)) - minu)
            return "{}{} {}{} {}{}".format(h, unit_hours, minu, unit_minutes, format(seg, time_format), unit_second)
        elif time >= 86400:
            D = int(time/float(86400))
            h = int(24*(time/float(86400) - D))
            minu = int(60*((24*(time/float(86400) - D) - h)))
            seg = 60*((60*((24*(time/float(86400) - D) - h))) - minu)
            return "{}{} {}{} {}{} {}{}".format(D, unit_days, h, unit_hours, minu, unit_minutes, format(seg, time_format), unit_second)

    @staticmethod
    def remove_dependency_directory(dir_name_dependency):
        """
        We need to get rid of dependencies when they don't match the version
        that should be installed for this version of the plugin.
        """
        base_path = os.path.join(DEPENDENCIES_BASE_PATH, dir_name_dependency)

        # Since folders might contain read only files, we need to delete them
        # using a callback (see https://docs.python.org/3/library/shutil.html#rmtree-example)
        shutil.rmtree(base_path, onerror=remove_readonly)
        Logger().clear_message_bar()

        if os.path.exists(base_path):
            Logger().warning_msg(__name__, QCoreApplication.translate("Utils",
                                                                      "It wasn't possible to remove the dependency folder. You need to remove this folder yourself to generate reports: <a href='file:///{path}'>{path}</a>").format(path=normalize_local_url(base_path)))

def is_plugin_version_valid(plugin_name, min_required_version, exact_required_version):
    plugin_found = plugin_name in qgis.utils.plugins
    if not plugin_found:
        return False
    current_version = get_plugin_metadata(plugin_name, 'version')
    return is_version_valid(current_version, min_required_version, exact_required_version, plugin_name)

def is_version_valid(current_version, min_required_version, exact_required_version=False, module_tested=''):
    """
    Gerneric one, it helps us to validate whether a current version is greater or equal (if exact_required_version)
    to a min_required_version

    :param current_version: String, in the form 2.9.5
    :param min_required_version: String, in the form 2.9.5
    :param exact_required_version: Boolean, if true, only the exact version is valid
    :param module_tested: String, only for displaying a log with context
    :return: Whether the current version is valid or not
    """
    if current_version is None:
        return False

    current_version_splitted = current_version.split(".")
    if len(current_version_splitted) < 4: # We could need 4 places for our custom plugin versions
        current_version_splitted = current_version_splitted + ['0','0','0','0']
        current_version_splitted = current_version_splitted[:4]

    min_required_version_splitted = min_required_version.split(".")
    if len(min_required_version_splitted) < 4:
        min_required_version_splitted = min_required_version_splitted + ['0','0','0','0']
        min_required_version_splitted = min_required_version_splitted[:4]

    Logger().info(__name__, "[{}] {}equired version: {}, current_version: {}".format(
            module_tested,
            'R' if exact_required_version else 'Min r',
            min_required_version_splitted,
            current_version_splitted))

    if exact_required_version:
        return min_required_version_splitted == current_version_splitted

    else: # Min version and subsequent versions should work
        for i in range(len(current_version_splitted)):
            if int(current_version_splitted[i]) < int(min_required_version_splitted[i]):
                return False
            elif int(current_version_splitted[i]) > int(min_required_version_splitted[i]):
                return True

    return True


def normalize_iliname(name):
    """
    Removes version from an iliname

    :param name: iliname
    :return: iliname with no version information
    """
    parts = name.split(".")
    parts[0] = parts[0].split("_V")[0]
    return ".".join(parts)


def md5sum(filename):
    with open(filename, mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    return d.hexdigest()
