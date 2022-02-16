"""
/***************************************************************************
                              Asistente LADM-COL
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
from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication)
from qgis.core import QgsProject

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.layer_config import LayerConfig
from asistente_ladm_col.config.query_names import QueryNames
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.model_baker_lib.qgismodelbaker_lib import QgisModelBakerPluginLib
from asistente_ladm_col.lib.model_baker_lib.utils.qgis_utils import get_suggested_index_for_layer
from asistente_ladm_col.utils.quality_error_db_utils import QualityErrorDBUtils
from asistente_ladm_col.utils.utils import is_plugin_version_valid


class QgisModelBakerUtils(QObject):

    def __init__(self):
        QObject.__init__(self)
        self.logger = Logger()
        from asistente_ladm_col.config.config_db_supported import ConfigDBsSupported
        self._dbs_supported = ConfigDBsSupported()

        self.__mb_lib = QgisModelBakerPluginLib()

    def get_generator(self, db):
        tool = self._dbs_supported.get_db_factory(db.engine).get_model_baker_db_ili_mode()

        return self.__mb_lib.get_generator()(tool, db.uri, "smart2", db.schema, pg_estimated_metadata=False)

    def load_layers(self, db, layer_list, group=None):
        """
        Load a selected list of layers from qgis model baker.
        This call should configure relations and bag of enums
        between layers being loaded, but not when a layer already
        loaded has a relation or is part of a bag of enum. For
        that case, we use a cached set of relations and bags of
        enums that we get only once per session and configure in
        the Asistente LADM-COL.
        """
        generator = self.get_generator(db)
        layers = generator.layers(layer_list)
        layers = self._filter_layers(layers)
        relations, bags_of_enum = generator.relations(layers, layer_list)
        legend = generator.legend(layers, ignore_node_names=QualityErrorDBUtils.get_quality_error_group_names())
        self.__mb_lib.create_project(layers, relations, bags_of_enum, legend, auto_transaction=False, group=group)

    def get_required_layers_without_load(self, layer_list, db):
        """
        Gets a list of layers from a list of layer names using QGIS Model Baker.
        Layers are register in QgsProject, but not loaded to the canvas!
        :param layer_list: list of layers names (e.g., ['lc_terreno', 'lc_lindero'])
        :param db: db connection
        :return: list of QgsVectorLayers registered in the project
        """
        layers = list()

        tool = self._dbs_supported.get_db_factory(db.engine).get_model_baker_db_ili_mode()
        generator = self.get_generator(db)
        model_baker_layers = generator.layers(layer_list)
        model_baker_layers = self._filter_layers(model_baker_layers)

        for model_baker_layer in model_baker_layers:
            layer = model_baker_layer.create()  # Convert Model Baker layer to QGIS layer
            QgsProject.instance().addMapLayer(layer, False)  # Do not load it to canvas
            layers.append(layer)

        return layers

    @staticmethod
    def _filter_layers(layers):
        """
        Modifies the input list of MB layers, removing elements that meet a condition.

        :param layers: List of Model Baker Layer objects of list of layer info dicts.
        :return: Filtered list of layers.
        """
        if layers:
            if isinstance(layers[0], dict):
                layers = [layer for layer in layers if not "_nu_" in layer["tablename"].lower()]
            elif isinstance(layers[0], list):
                layers = [layer for layer in layers if not "_nu_" in layer.name.lower()]

        return layers

    def get_layers_and_relations_info(self, db):
        """
        Called once per session, this is used to get information
        of all relations and bags of enums in the DB and cache it
        in the Asistente LADM-COL.
        """
        generator = self.get_generator(db)

        layers = generator.get_tables_info_without_ignored_tables()
        layers = self._filter_layers(layers)
        relations = [relation for relation in generator.get_relations_info()]
        QgisModelBakerUtils._filter_relations(relations)
        return (layers, relations, {})

    @staticmethod
    def _filter_relations(relations):
        """
        Modifies the input list of relations, removing elements that meet a condition.

        :param relations: List of a dict of relations.
        :return: Nothing, changes the input list of relations.
        """
        to_delete = list()
        for relation in relations:
            if relation[QueryNames.REFERENCING_FIELD].startswith('uej2_') or \
                    relation[QueryNames.REFERENCING_FIELD].startswith('ue_') or \
                    '_nu_' in relation[QueryNames.REFERENCING_LAYER].lower() or \
                    '_nu_' in relation[QueryNames.REFERENCED_LAYER].lower():
                to_delete.append(relation)

        for idx in to_delete:
            relations.remove(idx)

    def get_tables_info_without_ignored_tables(self, db):
        generator = self.get_generator(db)
        return generator.get_tables_info_without_ignored_tables()

    @staticmethod
    def get_suggested_index_for_layer(layer, group):
        return get_suggested_index_for_layer(layer, group)
