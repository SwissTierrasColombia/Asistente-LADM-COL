# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-02-06
        git sha              : :%H$
        copyright            : (C) 2019 by Jhon Galindo
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
import sys
import re
import subprocess
from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication)
from ..config.general_config import JAVA_REQUIRED_VERSION
from ..utils.qgis_model_baker_utils import get_java_path_from_qgis_model_baker


class Utils(QObject):
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
    def java_path_is_valid(java_path):
        """
        Check if java path exists
        :param java_path: (str) java path to validate
        :return: (bool, str)  True if java Path is valid, False in another case
        """
        try:
            if os.name == 'nt':
                java_path = Utils.validate_java_path(java_path)

            procs_message = subprocess.check_output([java_path, '-version'], stderr=subprocess.STDOUT).decode('utf8').lower()
            types_java = ['jre', 'java', 'jdk']

            if procs_message:
                if any(type_java in procs_message for type_java in types_java):
                    pattern = '\"(\d+\.\d+).*\"'
                    java_version = re.search(pattern, procs_message).groups()[0]

                    if java_version:
                        if float(java_version) == JAVA_REQUIRED_VERSION:
                            return (True, QCoreApplication.translate("JavaPath", "Java path has been configured correctly."))
                        else:
                            return (False, QCoreApplication.translate("JavaPath", "Java version is not valid. Current version is {}, but must be {}.").format(java_version, JAVA_REQUIRED_VERSION))

                    return (False, QCoreApplication.translate("JavaPath", "Java exists but it is not possible to know and validate its version."))
                else:
                    return (False, QCoreApplication.translate("JavaPath", "Java path is not valid, please select a valid path..."))
            else:
                return (False, QCoreApplication.translate("JavaPath", "Java path is not valid, please select a valid path..."))
        except Exception as e:
            return (False, QCoreApplication.translate("JavaPath", "Java path is not valid, please select a valid path..."))

    @staticmethod
    def validate_java_path(java_path):
        escape_characters = [('\a', '\\a'), ('\b', '\\b'), ('\f', '\\f'), ('\n', '\\n'), ('\r', '\\r'), ('\t', '\\t'), ('\v', '\\v')]
        for escape_character in escape_characters:
            java_path = java_path.replace(escape_character[0], escape_character[1])
        return java_path

    @staticmethod
    def set_java_home():
        """
        Attempt to set a valid JAVA_HOME only for the current session, which is used by reports (MapFish).
        First try with the system JAVA_HOME, if not present, try with the Java configured in Model Baker. Otherwise return
        false.
        :return: Whether a proper Java could be set or not in the current session's JAVA_HOME
        """
        java_home = None
        java_name = None
        pattern_java = "bin{}java".format(os.sep)

        if sys.platform == 'win32':
            java_name = 'java.exe'
        else:
            java_name = 'java'

        # Get JAVA_HOME environment variable
        if 'JAVA_HOME' in os.environ:
            java_home = os.environ['JAVA_HOME']

            java_exe = os.path.join(java_home, 'bin', java_name)
            (is_valid, java_message) = Utils.java_path_is_valid(java_exe)

            if not is_valid:
                # Another try: does JAVA_HOME include bin dir?
                java_exe = os.path.join(java_home, java_name)
                (is_valid, java_message) = Utils.java_path_is_valid(java_exe)

                if is_valid:
                    os.environ['JAVA_HOME'] = java_exe.split(pattern_java)[0]
                    return True
            else:
                os.environ['JAVA_HOME'] = java_exe.split(pattern_java)[0]
                # JAVA_HOME is valid, we'll use it as it is!
                return True

        # If JAVA_HOME environment variable doesn't exist
        # We use the value defined in QgisModelBaker
        java_exe = get_java_path_from_qgis_model_baker()

        (is_valid, java_message) = Utils.java_path_is_valid(java_exe)
        if is_valid:
            os.environ['JAVA_HOME'] = java_exe.split(pattern_java)[0]
            return True

        return False
