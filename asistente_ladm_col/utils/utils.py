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
import tempfile
import zipfile
from functools import partial
import socket
import webbrowser

import qgis.utils
from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication)
from qgis.core import (QgsFeatureRequest,
                       QgsCoordinateReferenceSystem)

import processing

from asistente_ladm_col.config.general_config import (DEPENDENCIES_BASE_PATH,
                                                      MODULE_HELP_MAPPING,
                                                      TEST_SERVER,
                                                      HELP_URL,
                                                      HELP_DIR_NAME)
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.qt_utils import (get_plugin_metadata,
                                               remove_readonly,
                                               normalize_local_url,
                                               ProcessWithStatus)
from asistente_ladm_col.config.translator import (QGIS_LANG,
                                                  PLUGIN_DIR)


class Utils(QObject):
    """
    Utility methods are here to be able to use internationalization on some messages
    """
    def __init__(self):
        QObject.__init__(self)

    @staticmethod
    def set_time_format(time):
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
        elif 60 <= time < 3600:
            minu = int(time/float(60))
            seg = 60*(time/float(60) - minu)
            return "{}{} {}{}".format(minu, unit_minutes, format(seg, time_format), unit_second)
        elif 3600 <= time < 86400:
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

    @staticmethod
    def compress_file(file_path):
        zip_file_path = "{}.zip".format(tempfile.mktemp())
        with ProcessWithStatus(QCoreApplication.translate("Utils", "Compressing file...")):
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.write(file_path, os.path.basename(file_path))

        return zip_file_path


def is_plugin_version_valid(plugin_name, min_required_version, exact_required_version):
    plugin_found = plugin_name in qgis.utils.plugins

    if not plugin_found:
        if plugin_name in qgis.utils.available_plugins:
            # It just needs to be activated
            if not qgis.utils.startPlugin(plugin_name):
                return False  # We couldn't started, no details, so return False to be safe
        else:
            return False

    current_version = get_plugin_metadata(plugin_name, 'version')
    current_version = current_version[1:] if current_version.startswith("v") else current_version
    return is_version_valid(current_version, min_required_version, exact_required_version, plugin_name)


def is_version_valid(current_version, min_required_version, exact_required_version=False, module_tested=''):
    """
    Generic one, it helps us to validate whether a current version is greater or equal (if exact_required_version)
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


def is_connected(hostname):
    try:
        host = socket.gethostbyname(hostname)
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    finally:
        try:
            # s might not exist if socket.create_connection breaks
            s.close()
        except:
            pass

    return False


def show_plugin_help(module='', offline=False):
    url = ''
    section = MODULE_HELP_MAPPING[module]

    # If we don't have Internet access check if the documentation is in the
    # expected local dir and show it. Otherwise, show a warning message.
    # web_url = "{}/{}/{}".format(HELP_URL, QGIS_LANG, PLUGIN_VERSION)  # TODO: To be used when the documentation has been versioned
    web_url = HELP_URL

    _is_connected = is_connected(TEST_SERVER)
    if offline or not _is_connected:

        help_path = os.path.join(
            PLUGIN_DIR,
            HELP_DIR_NAME,
            QGIS_LANG
        )
        if os.path.exists(help_path):
            url = os.path.join("file://", help_path)
        else:
            if _is_connected:
                Logger().warning_msg(__name__, QCoreApplication.translate("Utils",
                    "The local help could not be found in '{}' and cannot be open.").format(help_path), 20)
            else:
                Logger().warning_msg(__name__, QCoreApplication.translate("Utils",
                    "Is your computer connected to Internet? If so, go to <a href=\"{}\">online help</a>.").format(web_url), 20)
            return
    else:
        url = web_url

    webbrowser.open("{}/{}".format(url, section))


def get_uuid_dict(layer, names, id_field=None):
    """
    Return dict with id_field as key and uuid field as value
    When id_field is None the key value is the id (QGIS) of the feature
    """
    field_names = [field.name() for field in layer.fields()]
    dict_uuid = dict()

    if names.T_ILI_TID_F in field_names and (id_field in field_names or id_field is None):
        request = QgsFeatureRequest().setFlags(QgsFeatureRequest.NoGeometry)
        attrs = [names.T_ILI_TID_F]
        if id_field:
            attrs.append(id_field)
        request.setSubsetOfAttributes(attrs, layer.fields())  # Note: this adds a new flag
        for feature in layer.getFeatures(request):
            if id_field:
                dict_uuid[feature[id_field]] = str(feature[names.T_ILI_TID_F])
            else:
                dict_uuid[feature.id()] = str(feature[names.T_ILI_TID_F])
    return dict_uuid


def remove_keys_from_dict(keys, dictionary):
    for key in keys:
        if key in dictionary:
            del dictionary[key]


def get_key_for_quality_rule_adjusted_layer(input, reference, fix=False):
    return "{}..{}{}".format(input, reference, '..fix' if fix else '')


def get_extent_for_processing(layer, scale=1.5):
    # Get extent in this form: 'Xmin,Xmax,Ymin,Ymax [EPSG:9377]'
    # Example: '4843772.266000000,4844770.188000000,2143021.638000000,2144006.634000000 [EPSG:9377]'
    # See https://github.com/qgis/QGIS/blob/ccc34c76e714e5f6f87d2a329ca048896eb4c87f/src/gui/qgsextentwidget.cpp#L211

    layer.updateExtents(True)  # Required by GeoPackage, probably until EPSG:9377 is officially included in QGIS
    extent = layer.extent()

    extent_layer = processing.run("native:polygonfromlayerextent", {
        'INPUT': layer,
        'ROUND_TO': 0,
        'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']
    extent = extent_layer.extent()
    extent.scale(scale)

    return "{},{},{},{} [{}]".format(extent.xMinimum(),
                                     extent.xMaximum(),
                                     extent.yMinimum(),
                                     extent.yMaximum(),
                                     layer.crs().userFriendlyIdentifier(
                                         QgsCoordinateReferenceSystem.ShortString))
