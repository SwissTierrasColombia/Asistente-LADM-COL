# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              -------------------
        begin                : 2017-01-27
        git sha              : :%H$
        copyright            : (C) 2017 by OPENGIS.ch
                               (C) 2022 Adapted by Germán Carrillo (STC)
        email                : info@opengis.ch
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import locale
import os

from qgis.core import QgsProject
from qgis.utils import available_plugins
from qgis.PyQt.QtWidgets import QAction, QMenu, QMessageBox
from qgis.PyQt.QtCore import QObject, QTranslator, QSettings, QLocale, QCoreApplication, Qt
from qgis.PyQt.QtGui import QIcon

from asistente_ladm_col.lib.model_baker_lib.dataobjects.project import Project
from asistente_ladm_col.lib.model_baker_lib.generator.generator import Generator


class QgisModelBakerPluginLib(QObject):

    def __init__(self):
        QObject.__init__(self)

    def get_generator(self):
        return Generator

    def create_project(self, layers, relations, bags_of_enum, legend, auto_transaction=True, evaluate_default_values=True, group=None):
        """
        Expose the main functionality from Model Baker to other plugins,
        namely, create a QGIS project from objects obtained from the Generator
        class.

        :param layers: layers object from generator.layers
        :param relations: relations object obtained from generator.relations
        :param bags_of_enum: bags_of_enum object from generator.relations
        :param legend: legend object obtained from generator.legend
        :param auto_transaction: whether transactions should be enabled or not
                                 when editing layers from supported DB like PG
        :param evaluate_default_values: should default values be evaluated on
                                        provider side when requested and not
                                        when committed. (from QGIS docs)
        :param group: QgsLayerTreeGroup that should be taken as parent for all loaded layers and subgroups
        """
        project = Project(auto_transaction, evaluate_default_values)
        project.layers = layers
        project.relations = relations
        project.bags_of_enum = bags_of_enum
        project.legend = legend
        project.post_generate()
        qgis_project = QgsProject.instance()
        project.create(None, qgis_project, group)
