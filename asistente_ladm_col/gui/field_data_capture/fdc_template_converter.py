# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin                : 2021-02-26
        git sha              : :%H$
        copyright            : (C) 2021 by Germán Carrillo (SwissTierras Colombia)
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
import os.path
import datetime
import tempfile
import xml.etree.ElementTree as ET

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import QgsProject

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.query_names import QueryNames
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils.qt_utils import normalize_local_url


class TemplateConverterFieldDataCapture:
    ID_TAG = 'id'
    NAME_TAG = 'name'
    PROVIDER_TAG = 'providerKey'
    SOURCE_TAG = 'source'
    QGS_EXTENSION = '.qgs'

    def __init__(self, db):
        self.logger = Logger()
        self.app = AppInterface()

        self._file_path = ""
        self.dict_layers = dict()  # Layer info to use when replacing data in the template

        self._db = db

    def convert_template_project(self, file_path):
        self._file_path = file_path

        res, msg = self.validate_file()
        if not res:
            self.logger.warning_msg(__name__, res)
            return

        tree = ET.parse(self._file_path)
        root = tree.getroot()

        cached_layers = self.app.core.get_cached_layers()
        if not cached_layers:
            self.app.core.cache_layers_and_relations(self._db, True, None)
            cached_layers = self.app.core.get_cached_layers()

        cached_layers_info = {d[QueryNames.TABLE_NAME_MODEL_BAKER]: d for d in cached_layers}

        # Adjust layer-tree-layers
        self.read_tree_groups(root, cached_layers_info)

        # Adjust project relations
        self.change_relation_field_case(root)

        # Adjust map layers and their configs
        self.adjuts_map_layers(root)

        # Save the modified project copy
        basename = os.path.splitext(os.path.basename(file_path))[0]
        new_filename = "{}_{}{}".format(basename, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"), self.QGS_EXTENSION)
        write_file_path = os.path.join(tempfile.gettempdir(), new_filename)
        tree.write(write_file_path)

        # Finally load the template into QGIS
        res_read = QgsProject.instance().read(write_file_path)
        if res_read:
            self.logger.success_msg(__name__, QCoreApplication.translate("TemplateConverterFieldDataCapture", "The template (.qgs) project has been adapted and opened successfully! It's saved in <a href='file:///{}'>{}</a>").format(normalize_local_url(tempfile.gettempdir()), new_filename))
        else:
            self.logger.warning_msg(__name__, QCoreApplication.translate("TemplateConverterFieldDataCapture", "There was an error opening the generated .qgs file. It's saved in <a href='file:///{}'>{}</a>").format(normalize_local_url(tempfile.gettempdir()), new_filename))

    def read_tree_layers(self, group, cached_layers_info):
        for tree_layer in group.findall('layer-tree-layer'):
            attrs = tree_layer.attrib

            if attrs.get(self.PROVIDER_TAG) != "ogr":  # Filter out other layers (e.g., rasters)
                continue

            current_source = attrs.get(self.SOURCE_TAG)
            current_layer_name = self.extract_layer_name(current_source)
            cached_layer_info = cached_layers_info.get(current_layer_name)
            if not cached_layer_info:
                self.logger.warning(__name__, "No cached layer info for layer '{}'!".format(current_layer_name))
                continue

            new_provider = self._db.provider
            new_source = self._db.get_qgis_layer_source(current_layer_name, cached_layer_info)
            self.dict_layers.update({attrs.get(self.ID_TAG): {
                self.PROVIDER_TAG: new_provider,
                self.SOURCE_TAG: new_source
            }})
            tree_layer.set(self.PROVIDER_TAG, new_provider)
            tree_layer.set(self.SOURCE_TAG, new_source)

    def read_tree_groups(self, root_element, cached_layers_info):
        # iterate over all the nodes with tag name - holiday
        for tree_group in root_element.findall('layer-tree-group'):
            self.read_tree_groups(tree_group, cached_layers_info)
            self.read_tree_layers(tree_group, cached_layers_info)

    def change_relation_field_case(self, root):
        relations = root.find('relations')
        for relation in relations.findall('relation'):
            field_ref = relation.find('fieldRef')
            field_ref.set('referencedField', field_ref.attrib.get('referencedField').lower())

    def adjuts_map_layers(self, root):
        project_layers = root.find('projectlayers')
        for map_layer in project_layers.findall('maplayer'):
            layer_id = map_layer.find('id')
            if layer_id.text in self.dict_layers:
                layer_datasource = map_layer.find('datasource')
                layer_datasource.text = self.dict_layers[layer_id.text][self.SOURCE_TAG]
                layer_provider = map_layer.find('provider')
                layer_provider.text = self.dict_layers[layer_id.text][self.PROVIDER_TAG]

                # Adjust relations (dataSource, provider, referenced field)
                referenced_layers = map_layer.find('referencedLayers')
                for rel in referenced_layers.findall('relation'):
                    referenced_layer = rel.attrib.get('referencedLayer')
                    rel.set('dataSource', self.dict_layers[referenced_layer][self.SOURCE_TAG])
                    rel.set(self.PROVIDER_TAG, self.dict_layers[referenced_layer][self.PROVIDER_TAG])
                    field_ref = rel.find('fieldRef')
                    field_ref.set('referencedField', field_ref.attrib.get('referencedField').lower())

                field_config = map_layer.find('fieldConfiguration')
                for ew_field in field_config.findall('field'):
                    ew = ew_field.find('editWidget')
                    if ew:
                        if ew.attrib.get('type') == 'ValueRelation':
                            ew_config = ew.find('config')
                            root_options = ew_config.find('Option')

                            # First go for the layer id
                            ew_layer_id = ''
                            all_options = root_options.findall('Option')
                            for option in all_options:
                                if option.attrib.get('name') == 'Layer':
                                    ew_layer_id = option.attrib.get('value')
                                    break

                            for option in all_options:
                                option_name = option.attrib.get('name')
                                if option_name == 'Key':
                                    option.set('value', option.attrib.get('value').lower())
                                elif option_name == 'Value':
                                    option.set('value', option.attrib.get('value').lower())
                                elif option_name == 'LayerProviderName':
                                    option.set('value', self.dict_layers[ew_layer_id][self.PROVIDER_TAG])
                                elif option_name == 'LayerSource':
                                    option.set('value', self.dict_layers[ew_layer_id][self.SOURCE_TAG])

                # Make all fields editable, we need it because default values
                # might not work for other DB engines than GPKG, so we need to edit them by hand
                editable = map_layer.find('editable')
                for field_editable in editable.findall('field'):
                    field_editable.set('editable', "1")
            else:
                self.logger.warning(__name__, "Converting template: {} layer cannot be handled...".format(layer_id.text))

    def validate_file(self):
        res = True
        msg = ""
        if os.path.splitext(self._file_path)[1].lower() != self.QGS_EXTENSION or not os.path.isfile(self._file_path):
            res = False
            res = QCoreApplication.translate("TemplateConverterFieldDataCapture", "The file is not a valid QGS project template!")

        return res, msg

    def extract_layer_name(self, gpkg_source):
        array = gpkg_source.split("layername=")
        return array[1] if len(array) == 2 else gpkg_source