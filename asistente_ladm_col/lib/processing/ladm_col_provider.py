# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-04-02
        git sha              : :%H$
        copyright            : (C) 2018 by Germán Carrillo (BSF Swissphoto)
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
from PyQt5.QtGui import QIcon
from qgis.core import QgsProcessingProvider
from processing.core.ProcessingConfig import (Setting,
                                              ProcessingConfig)
from asistente_ladm_col.lib.processing.algs.InsertFeaturesToLayer import InsertFeaturesToLayer
from asistente_ladm_col.lib.processing.algs.PolygonsToLines import PolygonsToLines
from asistente_ladm_col.lib.processing.algs.FieldCalculator import FieldsCalculator

class LADMCOLAlgorithmProvider(QgsProcessingProvider):

    def __init__(self):
        super().__init__()

    def load(self):
        """In this method we add settings needed to configure our
        provider.
        """
        ProcessingConfig.settingIcons[self.name()] = self.icon()
        # Activate provider by default
        ProcessingConfig.addSetting(Setting(self.name(), 'ACTIVATE_LADM_COL',
                                            'Activate', True))
        ProcessingConfig.readSettings()
        self.refreshAlgorithms()
        return True

    def unload(self):
        """Setting should be removed here, so they do not appear anymore
        when the plugin is unloaded.
        """
        ProcessingConfig.removeSetting('ACTIVATE_LADM_COL')

    def isActive(self):
        """Return True if the provider is activated and ready to run algorithms"""
        return ProcessingConfig.getSetting('ACTIVATE_LADM_COL')

    def setActive(self, active):
        ProcessingConfig.setSettingValue('ACTIVATE_LADM_COL', active)

    def id(self):
        """This is the name that will appear on the toolbox group.

        It is also used to create the command line name of all the
        algorithms from this provider.
        """
        return 'ladm_col'

    def name(self):
        """This is the localised full name.
        """
        return 'LADM_COL'

    def icon(self):
        return QIcon(":/Asistente-LADM_COL/resources/images/icon.png")

    def loadAlgorithms(self):
        """Here we fill the list of algorithms in self.algs.

        This method is called whenever the list of algorithms should
        be updated. If the list of algorithms can change (for instance,
        if it contains algorithms from user-defined scripts and a new
        script might have been added), you should create the list again
        here.

        In this case, since the list is always the same, we assign from
        the pre-made list. This assignment has to be done in this method
        even if the list does not change, since the self.algs list is
        cleared before calling this method.
        """
        for alg in [InsertFeaturesToLayer(), PolygonsToLines(), FieldsCalculator()]:
            self.addAlgorithm(alg)
