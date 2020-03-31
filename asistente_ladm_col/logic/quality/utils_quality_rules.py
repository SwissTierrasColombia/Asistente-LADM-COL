import processing

from qgis.PyQt.QtCore import (QVariant)
from qgis.core import (QgsField,
                       QgsProject,
                       QgsVectorLayer,
                       QgsVectorLayerUtils,
                       QgsFeatureRequest)

from asistente_ladm_col.utils.qgis_model_baker_utils import QgisModelBakerUtils


class UtilsQualityRules:

    @staticmethod
    def get_boundary_points_features_not_covered_by_plot_nodes_and_viceversa(db, boundary_point_layer, plot_layer, error_layer, topology_rule, id_field):
        tmp_plot_nodes_layer = processing.run("native:extractvertices", {'INPUT': plot_layer, 'OUTPUT': 'memory:'})['OUTPUT']

        # layer is created with unique vertices
        # It is necessary because 'remove duplicate vertices' processing algorithm does not filter the data as wee need them
        plot_nodes_layer = QgsVectorLayer("Point?crs={}".format(plot_layer.sourceCrs().authid()), 'unique boundary nodes', "memory")
        data_provider = plot_nodes_layer.dataProvider()
        data_provider.addAttributes([QgsField(id_field, QVariant.Int)])
        plot_nodes_layer.updateFields()

        id_field_idx = tmp_plot_nodes_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])

        filter_fs = list()
        fs = list()
        for f in tmp_plot_nodes_layer.getFeatures(request):
            item = [f[id_field], f.geometry().asWkt()]
            if item not in filter_fs:
                filter_fs.append(item)
                fs.append(f)
        plot_nodes_layer.dataProvider().addFeatures(fs)

        input_layer = None
        join_layer = None

        if topology_rule == 'boundary_points_covered_by_plot_nodes':
            input_layer = boundary_point_layer
            join_layer = plot_nodes_layer
        elif topology_rule == 'plot_nodes_covered_by_boundary_points':
            input_layer = plot_nodes_layer
            join_layer = boundary_point_layer

        # get non matching features between boundary point and plot node
        spatial_join_layer = processing.run("qgis:joinattributesbylocation",
                                                   {'INPUT': input_layer,
                                                    'JOIN': join_layer,
                                                    'PREDICATE': [0], # Intersects
                                                    'JOIN_FIELDS': [db.names.T_ID_F],
                                                    'METHOD': 0,
                                                    'DISCARD_NONMATCHING': False,
                                                    'PREFIX': '',
                                                    'NON_MATCHING': 'memory:'})['NON_MATCHING']
        features = list()

        for feature in spatial_join_layer.getFeatures():
            feature_id = feature[db.names.T_ID_F]
            feature_geom = feature.geometry()
            new_feature = QgsVectorLayerUtils().createFeature(error_layer, feature_geom, {0: feature_id})
            features.append(new_feature)

        return features

    @staticmethod
    def add_error_layer(db, qgis_utils, error_layer):
        group = qgis_utils.get_error_layers_group()

        # Check if layer is loaded and remove it
        layers = group.findLayers()
        for layer in layers:
            if layer.name() == error_layer.name():
                group.removeLayer(layer.layer())
                break

        added_layer = QgsProject.instance().addMapLayer(error_layer, False)
        index = QgisModelBakerUtils().get_suggested_index_for_layer(added_layer, group)
        added_layer = group.insertLayer(index, added_layer).layer()
        if added_layer.isSpatial():
            # db connection is none because we are using a memory layer
            qgis_utils.symbology.set_layer_style_from_qml(db, added_layer, is_error_layer=True)
        return added_layer
