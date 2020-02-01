# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-02-06
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
import os

import qgis
from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication,
                              QSettings)
from qgis.core import (QgsProject,
                       Qgis,
                       QgsApplication)

from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.config.translation_strings import (TranslatableConfigStrings,
                                                           ERROR_LAYER_GROUP)
from asistente_ladm_col.config.mapping_config import QueryNames


class QgisModelBakerUtils(QObject):

    def __init__(self):
        QObject.__init__(self)
        self.logger = Logger()
        from asistente_ladm_col.config.config_db_supported import ConfigDbSupported
        self._conf_db = ConfigDbSupported()
        self.translatable_config_strings = TranslatableConfigStrings()

    def get_generator(self, db):
        if 'QgisModelBaker' in qgis.utils.plugins:
            tool = self._conf_db.get_db_items()[db.mode].get_mbaker_db_ili_mode()

            QgisModelBaker = qgis.utils.plugins["QgisModelBaker"]
            generator = QgisModelBaker.get_generator()(tool,
                db.uri, "smart2", db.schema, pg_estimated_metadata=False)
            return generator
        else:
            self.logger.critical(__name__, QCoreApplication.translate("AsistenteLADMCOLPlugin",
                "The QGIS Model Baker plugin is a prerequisite, install it before using LADM_COL Assistant."))
            return None

    def get_model_baker_db_connection(self, db):
        generator = self.get_generator(db)
        if generator is not None:
            return generator._db_connector

        return None

    def load_layers(self, layer_list, db):
        """
        Load a selected list of layers from qgis model baker.
        This call should configure relations and bag of enums
        between layers being loaded, but not when a layer already
        loaded has a relation or is part of a bag of enum. For
        that case, we use a cached set of relations and bags of
        that case, we use a cached set of relations and bags of
        enums that we get only once per session and configure in
        the Asistente LADM_COL.
        """
        translated_strings = self.translatable_config_strings.get_translatable_config_strings()

        if 'QgisModelBaker' in qgis.utils.plugins:
            QgisModelBaker = qgis.utils.plugins["QgisModelBaker"]

            tool = self._conf_db.get_db_items()[db.mode].get_mbaker_db_ili_mode()

            generator = QgisModelBaker.get_generator()(tool,
                db.uri, "smart2", db.schema, pg_estimated_metadata=False)
            layers = generator.layers(layer_list)
            relations, bags_of_enum = generator.relations(layers, layer_list)
            legend = generator.legend(layers, ignore_node_names=[translated_strings[ERROR_LAYER_GROUP]])
            QgisModelBaker.create_project(layers, relations, bags_of_enum, legend, auto_transaction=False)
        else:
            self.logger.critical(__name__, QCoreApplication.translate("AsistenteLADMCOLPlugin",
                "The QGIS Model Baker plugin is a prerequisite, install it before using LADM_COL Assistant."))

    def get_layers_and_relations_info(self, db):
        """
        Called once per session, this is used to get information
        of all relations and bags of enums in the DB and cache it
        in the Asistente LADM_COL.
        """
        if 'QgisModelBaker' in qgis.utils.plugins:
            generator = self.get_generator(db)

            layers = generator.get_tables_info_without_ignored_tables()
            relations = [relation for relation in generator.get_relations_info()]
            self.logger.debug(__name__, "Relationships before filter: {}".format(len(relations)))
            self.filter_relations(relations)
            self.logger.debug(__name__, "Relationships after filter: {}".format(len(relations)))
            return (layers, relations, {})
        else:
            self.logger.critical(__name__, QCoreApplication.translate("AsistenteLADMCOLPlugin",
                "The QGIS Model Baker plugin is a prerequisite, install it before using LADM_COL Assistant."))
            return (None, None)

    def filter_relations(self, relations):
        """
        Modifies the input list of relations, removing elements that meet a condition.

        :param relations: List of a dict of relations.
        :return: Nothing, changes the input list of relations.
        """
        to_delete = list()
        for relation in relations:
            if relation[QueryNames.REFERENCING_FIELD].startswith('uej2_') or relation[QueryNames.REFERENCING_FIELD].startswith('ue_'):
                to_delete.append(relation)

        for idx in to_delete:
            relations.remove(idx)

    def get_tables_info_without_ignored_tables(self, db):
        if 'QgisModelBaker' in qgis.utils.plugins:
            generator = self.get_generator(db)
            return generator.get_tables_info_without_ignored_tables()
        else:
            self.logger.critical(__name__, QCoreApplication.translate("AsistenteLADMCOLPlugin",
                "The QGIS Model Baker plugin is a prerequisite, install it before using LADM_COL Assistant."))

    def get_first_index_for_layer_type(self, layer_type, group=QgsProject.instance().layerTreeRoot()):
        if 'QgisModelBaker' in qgis.utils.plugins:
            import QgisModelBaker
            return QgisModelBaker.utils.qgis_utils.get_first_index_for_layer_type(layer_type, group)
        return None

    def get_suggested_index_for_layer(self, layer, group):
        if 'QgisModelBaker' in qgis.utils.plugins:
            import QgisModelBaker
            return QgisModelBaker.utils.qgis_utils.get_suggested_index_for_layer(layer, group)
        return None

def get_java_path_dir_from_qgis_model_baker():
    java_path = QSettings().value('QgisModelBaker/ili2db/JavaPath')
    java_path_dir = os.path.dirname(os.path.dirname(java_path or ''))
    return java_path_dir

def get_java_path_from_qgis_model_baker():
    java_path = QSettings().value('QgisModelBaker/ili2db/JavaPath', '', str)
    return java_path

