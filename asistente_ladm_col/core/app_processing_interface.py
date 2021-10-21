"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin          : 2021-10-20
        git sha        : :%H$
        copyright      : (C) 2021 by Germán Carrillo (SwissTierras Colombia)
        email          : gcarrillo@linuxmail.org
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
import glob
import shutil

from qgis.PyQt.QtCore import QObject
from qgis.core import (Qgis,
                       QgsApplication,
                       QgsProcessingModelAlgorithm)

from processing.modeler.ModelerUtils import ModelerUtils
from processing.script import ScriptUtils

from asistente_ladm_col.config.enums import EnumLogMode
from asistente_ladm_col.config.general_config import (DEFAULT_LOG_MODE,
                                                      PROCESSING_MODELS_DIR,
                                                      PROCESSING_SCRIPTS_DIR)
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.processing.ladm_col_provider import LADMCOLAlgorithmProvider


class AppProcessingInterface(QObject):

    def __init__(self):
        QObject.__init__(self)

        self.logger = Logger()

        self.ladm_col_provider = LADMCOLAlgorithmProvider()
        self.__processing_resources_installed = list()
        self.__processing_model_dirs_to_register = [PROCESSING_MODELS_DIR]
        self.__processing_script_dirs_to_register = [PROCESSING_SCRIPTS_DIR]

    def initialize_processing_resources(self):
        """
        Add custom provider, models and scripts to QGIS
        """
        QgsApplication.processingRegistry().addProvider(self.ladm_col_provider)

        connect_provider_added = False
        if QgsApplication.processingRegistry().providerById('model'):
            self.__add_processing_resources_by_provider('model')
        else:
            connect_provider_added = True

        if QgsApplication.processingRegistry().providerById('script'):
            self.__add_processing_resources_by_provider('script')
        else:
            connect_provider_added = True

        if connect_provider_added:  # We need to wait until processing is initialized
            QgsApplication.processingRegistry().providerAdded.connect(self.__add_processing_resources_by_provider)

    def __add_processing_resources_by_provider(self, provider_id):
        if provider_id not in ['model', 'script']:
            return

        if sorted(self.__processing_resources_installed) == ["models", "script"]:  # We are done, disconnect.
            try:
                QgsApplication.processingRegistry().providerAdded.disconnect(self.__add_processing_resources_by_provider)
            except:
                pass  # Disconnect throws an error if the SLOT is already disconnected

        if provider_id == 'model':
            for models_dir in self.__processing_model_dirs_to_register:
                self.__register_processing_models(models_dir)

            self.__processing_resources_installed.append('model')
        elif provider_id == 'script':
            for scripts_dir in self.__processing_script_dirs_to_register:
                self.__register_processing_scripts(scripts_dir)

            self.__processing_resources_installed.append('script')

    def __register_processing_models(self, models_dir):
        # First get model file names from the model root folder
        filenames = list()
        for filename in glob.glob(os.path.join(models_dir, '*.model3')):  # Non-recursive
            filenames.append(filename)

        # Now, go for subfolders.
        # We store models that depend on QGIS versions in folders like "314" (for QGIS 3.14.x)
        # This was initially needed for the FieldMapper input, which was migrated to C++ in QGIS 3.14
        qgis_major_version = str(Qgis.QGIS_VERSION_INT)[:3]
        qgis_major_version_path = os.path.join(models_dir, qgis_major_version)

        if not os.path.isdir(qgis_major_version_path):
            # No folder for this version (e.g., unit tests on QGIS-dev), so let's find the most recent version
            subfolders = [sf.name for sf in os.scandir(models_dir) if sf.is_dir()]
            if subfolders:
                qgis_major_version_path = os.path.join(models_dir, max(subfolders))

        for filename in glob.glob(os.path.join(qgis_major_version_path, '*.model3')):
            filenames.append(filename)

        # Finally, do load the models!
        count = 0
        registered_models = list()
        for filename in filenames:
            alg = QgsProcessingModelAlgorithm()
            if not alg.fromFile(filename):
                self.logger.critical(__name__, "Couldn't load model from '{}'!".format(filename))
                return

            registered_models.append(os.path.basename(filename))
            destFilename = os.path.join(ModelerUtils.modelsFolders()[0], os.path.basename(filename))
            shutil.copyfile(filename, destFilename)
            count += 1

        if count:
            QgsApplication.processingRegistry().providerById('model').refreshAlgorithms()
            if DEFAULT_LOG_MODE == EnumLogMode.DEV:
                self.logger.debug(__name__, "{} LADM-COL Processing models were installed! {}".format(count, registered_models))
            else:
                self.logger.debug(__name__, "{} LADM-COL Processing models were installed!".format(count))


    def __register_processing_scripts(self, scripts_dir):
        count = 0
        registered_scripts = list()
        qgis_scripts_dir = ScriptUtils.defaultScriptsFolder()
        for filename in glob.glob(os.path.join(scripts_dir, '*.py')):
            try:
                shutil.copy(filename, qgis_scripts_dir)
                count += 1
                registered_scripts.append(os.path.basename(filename))
            except OSError as e:
                self.logger.critical(__name__, "Couldn't install LADM-COL script '{}'!".format(filename))

        if count:
            QgsApplication.processingRegistry().providerById("script").refreshAlgorithms()
            if DEFAULT_LOG_MODE == EnumLogMode.DEV:
                self.logger.debug(__name__, "{} LADM-COL Processing scripts were installed!".format(count, registered_scripts))
            else:
                self.logger.debug(__name__, "{} LADM-COL Processing scripts were installed!".format(count))

    def register_add_on_processing_models(self, models_dir):
        """
        For add-ons to delegate the registration of their own Processing models.

        :param models_dir: Path to the directory containing Processing models
        """
        if 'model' in self.__processing_resources_installed:
            # The plugin already registered its models, so register right away.
            self.__register_processing_models(models_dir)
        else:
            # The plugin has not yet registered its models (waiting for Processing
            # to setup the 'model' provider). Pass the add-on's model dir to a list
            # of paths to be registered by the plugin, when Processing is ready.
            self.__processing_model_dirs_to_register.append(models_dir)

    def register_add_on_processing_scripts(self, scripts_dir):
        """
        For add-ons to delegate the registration of their own Processing scripts.

        :param models_dir: Path to the directory containing Processing scripts
        """
        if 'script' in self.__processing_resources_installed:
            # The plugin already registered its scripts, so register right away.
            self.__register_processing_scripts(scripts_dir)
        else:
            # The plugin has not yet registered its scripts (waiting for Processing
            # to setup the 'script' provider). Pass the add-on's script dir to a list
            # of paths to be registered by the plugin, when Processing is ready.
            self.__processing_script_dirs_to_register.append(scripts_dir)

    def unload_resources(self):
        # TODO: Also unregister models and scripts
        QgsApplication.processingRegistry().removeProvider(self.ladm_col_provider)
