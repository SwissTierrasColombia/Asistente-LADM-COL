# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-01-15
        git sha              : :%H$
        copyright            : (C) 2020 by Leonardo Cardona (BSF Swissphoto)
        email                : leocardonapiedrahita@gmail.com
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
import platform
import re
import shutil
import subprocess
import requests
import sys
import tarfile
from pathlib import Path
from shutil import which

from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject,
                              QSettings)
from qgis.PyQt.QtWidgets import QMessageBox

from asistente_ladm_col.config.general_config import JAVA_REQUIRED_VERSION
from asistente_ladm_col.utils.utils import md5sum


class JavaUtils(QObject):

    JAVA_DIR_NAME = "jre1.8.0_241"
    JAVA_NAME = 'java.exe' if platform.system() == 'Windows' else 'java'

    JAVA_REPOSITORY_HTTP = "http://localhost/java/"
    USER_OUTPUT_DIR = os.path.join(str(Path.home()), 'Asistente-LADM_COL')

    DICT_JAVA_BY_OS = {
        'Linux_32bit': 'jre-8u241-linux-i586.tar.gz',
        'Linux_64bit': 'jre-8u241-linux-x64.tar.gz',
        'Darwin_64bit': 'jre-8u241-macosx-x64.tar.gz',
        'Windows_32bit': 'jre-8u241-windows-i586.tar.gz',
        'Windows_64bit': 'jre-8u241-windows-x64.tar.gz'
    }

    DICT_JAVA_MD5SUM = {
        'Linux_32bit': '349cf9d4ce26c3ea413be17f59d8b4fe',
        'Linux_64bit': '98f53c5894eeb2e8ffcff84092e0d2f2',
        'Darwin_64bit': '4903a131c25f9e40dcaf18a06464a6af',
        'Windows_32bit': '6df62a6b8e9a1bbbe2416ebaf314a50d',
        'Windows_64bit': '01d5f5543743b1ce1fb50ebb391d3fdf'
    }

    def __init__(self):
        QObject.__init__(self)

    @staticmethod
    def get_full_java_exe_path():
        java_name = 'java.exe' if sys.platform == 'win32' else 'java'
        pattern_java = "bin{}java".format(os.sep)
        full_java_exe_path = ""

        # Get JAVA_HOME environment variable
        if 'JAVA_HOME' in os.environ:
            java_home = os.environ['JAVA_HOME']

            full_java_exe_path = os.path.join(java_home, 'bin', java_name)
            (is_valid, java_message) = JavaUtils.java_path_is_valid(full_java_exe_path)

            if not is_valid:
                # Another try: does JAVA_HOME include bin dir?
                full_java_exe_path = os.path.join(java_home, java_name)
                (is_valid, java_message) = JavaUtils.java_path_is_valid(full_java_exe_path)
                if not is_valid:
                    full_java_exe_path = ""
        else:
            full_java_exe_path = which(java_name)
            # verifies that the java configured in the system is valid.
            (is_valid, java_message) = JavaUtils.java_path_is_valid(full_java_exe_path)
            if not is_valid:
                full_java_exe_path = ""

        print(full_java_exe_path)
        return full_java_exe_path

    @staticmethod
    def get_java_on_demand():
        # Create required directories
        Path(JavaUtils.USER_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

        # Remove previous java download
        custom_java_dir_path = os.path.join(JavaUtils.USER_OUTPUT_DIR, JavaUtils.JAVA_DIR_NAME)
        if os.path.exists(custom_java_dir_path):
            shutil.rmtree(custom_java_dir_path, ignore_errors=True)

        key_java_os_version = platform.system() + '_' + platform.architecture()[0]
        file_java_name = JavaUtils.DICT_JAVA_BY_OS[key_java_os_version]
        url_java = '{}{}'.format(JavaUtils.JAVA_REPOSITORY_HTTP, file_java_name)

        binary_java_file = requests.get(url_java)
        output_path_java = os.path.join(JavaUtils.USER_OUTPUT_DIR, file_java_name)
        open(output_path_java, 'wb').write(binary_java_file.content)
        os.chmod(output_path_java, 0o777)

        # Check MD5
        if md5sum(output_path_java) == JavaUtils.DICT_JAVA_MD5SUM[key_java_os_version]:
            if output_path_java.endswith("tar.gz"):
                tar = tarfile.open(output_path_java)
                tar.extractall(JavaUtils.USER_OUTPUT_DIR)
                tar.close()
        else:
            print('An error occurred while trying to download java')

        # Remove tar.gz java file.
        if os.path.exists(output_path_java):
            os.remove(output_path_java)

    @staticmethod
    def java_path_is_valid(java_path):
        """
        Check if java path exists
        :param java_path: (str) java path to validate
        :return: (bool, str)  True if java Path is valid, False in another case
        """
        try:
            if os.name == 'nt':
                java_path = JavaUtils.validate_java_path(java_path)

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
        First try with the system JAVA_HOME, if not present, try with the Java configured in Model Baker.
        if not the user is asked if he wants to be downloaded java on demand. Otherwise return false.
        :return: Whether a proper Java could be set or not in the current session's JAVA_HOME
        """
        java_name = 'java.exe' if sys.platform == 'win32' else 'java'
        pattern_java = "bin{}java".format(os.sep)

        # Get JAVA_HOME environment variable
        if 'JAVA_HOME' in os.environ:
            java_home = os.environ['JAVA_HOME']

            java_exe = os.path.join(java_home, 'bin', java_name)
            (is_valid, java_message) = JavaUtils.java_path_is_valid(java_exe)

            if not is_valid:
                # Another try: does JAVA_HOME include bin dir?
                java_exe = os.path.join(java_home, java_name)
                (is_valid, java_message) = JavaUtils.java_path_is_valid(java_exe)

                if is_valid:
                    os.environ['JAVA_HOME'] = java_exe.split(pattern_java)[0]
                    return True
            else:
                os.environ['JAVA_HOME'] = java_exe.split(pattern_java)[0]
                # JAVA_HOME is valid, we'll use it as it is!
                return True
        else:
            java_exe = which(java_name)
            if java_exe:
                # verifies that the java configured in the system is valid.
                (is_valid, java_message) = JavaUtils.java_path_is_valid(java_exe)
                if is_valid:
                    os.environ['JAVA_HOME'] = java_exe.split(pattern_java)[0]
                    return True

        # If JAVA_HOME environment variable doesn't exist
        # We use the value defined in QgisModelBaker
        java_exe = JavaUtils.get_java_path_from_qgis_model_baker()

        if java_exe:
            (is_valid, java_message) = JavaUtils.java_path_is_valid(java_exe)
            if is_valid:
                os.environ['JAVA_HOME'] = java_exe.split(pattern_java)[0]
                return True

        # If JAVA_HOME environment variable doesn't exist
        # If JAVA_HOME is no defined in QgisModelBaker
        # We will download JAVA by demand

        # Check if java was not installed previously, if it was download it is download again
        full_path_java = os.path.join(JavaUtils.USER_OUTPUT_DIR, JavaUtils.JAVA_DIR_NAME, 'bin', JavaUtils.JAVA_NAME)
        (is_valid, java_message) = JavaUtils.java_path_is_valid(full_path_java)

        if is_valid:
            # java was download previueslly, it is no necessary download again because it is valid.
            os.environ['JAVA_HOME'] = full_path_java.split(pattern_java)[0]
            return True
        else:

            reply = QMessageBox.question(None,
                                         QCoreApplication.translate("AsistenteLADMCOLPlugin", "Continue?"),
                                         QCoreApplication.translate("AsistenteLADMCOLPlugin",
                                                                    "Java {} is a prerequisite, but was not found. Do you want it to be installed?").format(JAVA_REQUIRED_VERSION),
                                         QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                JavaUtils.get_java_on_demand()
                (is_valid, java_message) = JavaUtils.java_path_is_valid(full_path_java)

                if is_valid:
                    os.environ['JAVA_HOME'] = full_path_java.split(pattern_java)[0]
                    return True

        return False

    @staticmethod
    def get_java_path_from_qgis_model_baker():
        java_path = QSettings().value('QgisModelBaker/ili2db/JavaPath', '', str)
        return java_path
