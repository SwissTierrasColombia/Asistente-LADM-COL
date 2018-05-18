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
import qgis
from qgis.core import QgsProject, Qgis, QgsApplication
from qgis.PyQt.QtCore import QObject

from ..config.general_config import (
    PLUGIN_NAME,
    KIND_SETTINGS,
    TABLE_NAME,
    REFERENCING_FIELD
)
from ..config.table_mapping_config import TABLE_PROP_DOMAIN
from .domains_parser import DomainRelationGenerator

class ProjectGeneratorUtils(QObject):

    def __init__(self):
        QObject.__init__(self)
        self.log = QgsApplication.messageLog()

    def load_layers(self, layer_list, db):
        if 'projectgenerator' in qgis.utils.plugins:
            projectgenerator = qgis.utils.plugins["projectgenerator"]
            generator = projectgenerator.get_generator()("ili2pg" if db.mode=="pg" else "ili2gpkg",
                db.uri, "smart2", db.schema, pg_estimated_metadata=False)
            layers = generator.layers(layer_list)
            relations = generator.relations(layers, layer_list)
            legend = generator.legend(layers)
            projectgenerator.create_project(layers, relations, legend, auto_transaction=False)
        else:
            self.log.logMessage(
                "El plugin Project Generator es un prerrequisito, instálalo antes de usar Asistente LADM_COL.",
                PLUGIN_NAME,
                Qgis.Critical
            )

    def get_layers_and_relations_info(self, db):
        if 'projectgenerator' in qgis.utils.plugins:
            projectgenerator = qgis.utils.plugins["projectgenerator"]
            generator = projectgenerator.get_generator()("ili2pg" if db.mode=="pg" else "ili2gpkg",
                db.uri, "smart2", db.schema)

            layers = generator.get_tables_info_without_ignored_tables()
            relations = generator.get_relations_info()
            relations = self.filter_relations(relations)

            domain_generator = DomainRelationGenerator(generator._db_connector, "smart2")
            layer_names = [record[TABLE_NAME] for record in layers]
            domain_names = [record[TABLE_NAME] for record in layers if record[KIND_SETTINGS] == TABLE_PROP_DOMAIN]
            domains = domain_generator.get_domain_relations_info(layer_names, domain_names)

            return (layers, relations + domains)
        else:
            self.log.logMessage(
                "El plugin Project Generator es un prerrequisito, instálalo antes de usar Asistente LADM_COL.",
                PLUGIN_NAME,
                Qgis.Critical
            )
            return (None, None)

    def filter_relations(self, relations):
        filtered_relations = list()
        for relation in relations:
            if not relation[REFERENCING_FIELD].startswith('uej2_') and \
               not relation[REFERENCING_FIELD].startswith('ue_'):
                filtered_relations.append(relation)
        return filtered_relations

    def get_tables_info_without_ignored_tables(self, db):
        if 'projectgenerator' in qgis.utils.plugins:
            projectgenerator = qgis.utils.plugins["projectgenerator"]
            generator = projectgenerator.get_generator()("ili2pg" if db.mode=="pg" else "ili2gpkg",
                db.uri, "smart2", db.schema, pg_estimated_metadata=False)
            return generator.get_tables_info_without_ignored_tables()
        else:
            self.log.logMessage(
                "El plugin Project Generator es un prerrequisito, instálalo antes de usar Asistente LADM_COL.",
                PLUGIN_NAME,
                Qgis.Critical
            )

    def get_first_index_for_layer_type(self, layer_type, group=QgsProject.instance().layerTreeRoot()):
        if 'projectgenerator' in qgis.utils.plugins:
            import projectgenerator
            return projectgenerator.utils.qgis_utils.get_first_index_for_layer_type(layer_type, group)
        return None
