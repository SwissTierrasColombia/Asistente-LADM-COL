# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2020-03-06
        git sha              : :%H$
        copyright            : (C) 2020 by Leo Cardona (BSF Swissphoto)
                               (C) 2020 by Germán Carrillo (BSF Swissphoto)
        email                : leo.cardona.p@gmail.com
                               gcarrillo@linuxmail.org
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
 """
import processing
from qgis.PyQt.QtCore import (QCoreApplication,
                              QSettings)
from qgis.core import (Qgis,
                       QgsVectorLayer,
                       QgsProcessingFeatureSourceDefinition,
                       QgsVectorLayerUtils,
                       QgsWkbTypes,
                       QgsFeatureRequest)

from asistente_ladm_col.config.quality_rules_config import (QUALITY_RULE_ERROR_CODE_E3001,
                                                            QUALITY_RULE_ERROR_CODE_E3002,
                                                            QUALITY_RULE_ERROR_CODE_E3003,
                                                            QUALITY_RULE_ERROR_CODE_E300401,
                                                            QUALITY_RULE_ERROR_CODE_E300402,
                                                            QUALITY_RULE_ERROR_CODE_E300403,
                                                            QUALITY_RULE_ERROR_CODE_E300404,
                                                            QUALITY_RULE_ERROR_CODE_E300405,
                                                            QUALITY_RULE_ERROR_CODE_E3005,
                                                            QUALITY_RULE_ERROR_CODE_E3006,
                                                            QUALITY_RULE_ERROR_CODE_E3007,
                                                            QUALITY_RULE_ERROR_CODE_E3008,
                                                            QUALITY_RULE_ERROR_CODE_E300901,
                                                            QUALITY_RULE_ERROR_CODE_E300902,
                                                            QUALITY_RULE_ERROR_CODE_E300903,
                                                            QUALITY_RULE_ERROR_CODE_E301001,
                                                            QUALITY_RULE_ERROR_CODE_E301002,
                                                            QUALITY_RULE_ERROR_CODE_E301003,
                                                            QUALITY_RULE_ERROR_CODE_E301004,
                                                            QUALITY_RULE_ERROR_CODE_E301005,
                                                            QUALITY_RULE_ERROR_CODE_E301006)
from asistente_ladm_col.config.general_config import DEFAULT_USE_ROADS_VALUE
from asistente_ladm_col.config.enums import EnumQualityRule
from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.quality_rule.quality_rule_manager import QualityRuleManager
from asistente_ladm_col.utils.utils import get_uuid_dict, remove_keys_from_dict
from asistente_ladm_col.lib.geometry import GeometryUtils


class PolygonQualityRules:
    def __init__(self, qgis_utils):
        self.quality_rules_manager = QualityRuleManager()
        self.qgis_utils = qgis_utils
        self.logger = Logger()

    def check_overlapping_plots(self, db):
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Polygon.OVERLAPS_IN_PLOTS)
        return self.__check_overlapping_polygons(db, rule, db.names.OP_PLOT_T, QUALITY_RULE_ERROR_CODE_E3001)

    def check_overlapping_buildings(self, db):
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Polygon.OVERLAPS_IN_BUILDINGS)
        return self.__check_overlapping_polygons(db, rule, db.names.OP_BUILDING_T, QUALITY_RULE_ERROR_CODE_E3002)

    def check_overlapping_right_of_way(self, db):
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Polygon.OVERLAPS_IN_RIGHTS_OF_WAY)
        return self.__check_overlapping_polygons(db, rule, db.names.OP_RIGHT_OF_WAY_T, QUALITY_RULE_ERROR_CODE_E3003)

    def __check_overlapping_polygons(self, db, rule, polygon_layer_name, error_code):
        polygon_layer = self.qgis_utils.get_layer(db, polygon_layer_name, load=True)
        if not polygon_layer:
            return

        if polygon_layer:
            error_layer = QgsVectorLayer("Polygon?crs={}".format(polygon_layer.sourceCrs().authid()), rule.error_table_name, "memory")
            data_provider = error_layer.dataProvider()
            data_provider.addAttributes(rule.error_table_fields)
            error_layer.updateFields()

            if QgsWkbTypes.isMultiType(polygon_layer.wkbType()) and polygon_layer.geometryType() == QgsWkbTypes.PolygonGeometry:
                polygon_layer = processing.run("native:multiparttosingleparts",
                                               {'INPUT': polygon_layer, 'OUTPUT': 'memory:'})['OUTPUT']

            overlapping = self.qgis_utils.geometry.get_overlapping_polygons(polygon_layer)

            flat_overlapping = [id for items in overlapping for id in items]  # Build a flat list of ids
            flat_overlapping = list(set(flat_overlapping))  # unique values

            if type(polygon_layer) == QgsVectorLayer: # A string might come from processing for empty layers
                dict_uuids = {f.id(): f[db.names.T_ILI_TID_F] for f in polygon_layer.getFeatures() if f.id() in flat_overlapping}

            features = []

            for overlapping_item in overlapping:
                polygon_id_field = overlapping_item[0]
                overlapping_id_field = overlapping_item[1]
                polygon_intersection = self.qgis_utils.geometry.get_intersection_polygons(polygon_layer, polygon_id_field, overlapping_id_field)

                if polygon_intersection is not None:
                    new_feature = QgsVectorLayerUtils().createFeature(
                        error_layer,
                        polygon_intersection,
                        {0: dict_uuids.get(polygon_id_field),
                         1: dict_uuids.get(overlapping_id_field),
                         2: self.quality_rules_manager.get_error_message(error_code),
                         3: error_code})
                    features.append(new_feature)

            error_layer.dataProvider().addFeatures(features)

            if error_layer.featureCount() > 0:
                added_layer = self.qgis_utils.add_error_layer(db, error_layer)

                return (QCoreApplication.translate("PolygonQualityRules",
                                 "A memory layer with {} overlapping polygons in layer '{}' has been added to the map!").format(
                                 added_layer.featureCount(), polygon_layer_name), Qgis.Critical)
            else:
                return (QCoreApplication.translate("PolygonQualityRules",
                                 "There are no overlapping polygons in layer '{}'!").format(polygon_layer_name), Qgis.Success)

    def check_plots_covered_by_boundaries(self, db):
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Polygon.PLOTS_COVERED_BY_BOUNDARIES)
        # read data
        layers = {
            db.names.OP_PLOT_T: None,
            db.names.OP_BOUNDARY_T: None,
            db.names.LESS_BFS_T: None,
            db.names.MORE_BFS_T: None
        }

        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        if layers[db.names.OP_PLOT_T].featureCount() == 0:
            return (QCoreApplication.translate("PolygonQualityRules",
                             "There are no plots to check 'plots should be covered by boundaries'."), Qgis.Warning)
        else:
            error_layer = QgsVectorLayer("MultiLineString?crs={}".format(layers[db.names.OP_PLOT_T].sourceCrs().authid()),
                                         rule.error_table_name, "memory")

            data_provider = error_layer.dataProvider()
            data_provider.addAttributes(rule.error_table_fields)
            error_layer.updateFields()

            features = self.get_plot_features_not_covered_by_boundaries(db,
                                                                        layers[db.names.OP_PLOT_T],
                                                                        layers[db.names.OP_BOUNDARY_T],
                                                                        layers[db.names.MORE_BFS_T],
                                                                        layers[db.names.LESS_BFS_T],
                                                                        error_layer,
                                                                        db.names.T_ID_F)
            if features:
                error_layer.dataProvider().addFeatures(features)
                added_layer = self.qgis_utils.add_error_layer(db, error_layer)

                return (QCoreApplication.translate("PolygonQualityRules",
                                 "A memory layer with {} plots not covered by boundaries has been added to the map!").format(added_layer.featureCount()), Qgis.Critical)

            else:
                return (QCoreApplication.translate("PolygonQualityRules",
                                 "All plots are covered by boundaries!"), Qgis.Success)

    def check_right_of_way_overlaps_buildings(self, db):
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Polygon.RIGHT_OF_WAY_OVERLAPS_BUILDINGS)
        layers = {
            db.names.OP_RIGHT_OF_WAY_T: None,
            db.names.OP_BUILDING_T: None
        }

        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        if layers[db.names.OP_RIGHT_OF_WAY_T].featureCount() == 0:
            return (QCoreApplication.translate("PolygonQualityRules",
                             "There are no Right of Way features to check 'Right of Way should not overlap buildings'."), Qgis.Warning)

        elif layers[db.names.OP_BUILDING_T].featureCount() == 0:
            return (QCoreApplication.translate("PolygonQualityRules",
                             "There are no buildings to check 'Right of Way should not overlap buildings'."), Qgis.Warning)

        else:

            dict_uuid_building = get_uuid_dict(layers[db.names.OP_BUILDING_T], db.names, db.names.T_ID_F)
            dict_uuid_right_of_way = get_uuid_dict(layers[db.names.OP_RIGHT_OF_WAY_T], db.names, db.names.T_ID_F)
            error_layer = QgsVectorLayer("MultiPolygon?crs={}".format(layers[db.names.OP_BUILDING_T].sourceCrs().authid()),
                                         rule.error_table_name, "memory")
            data_provider = error_layer.dataProvider()
            data_provider.addAttributes(rule.error_table_fields)
            error_layer.updateFields()

            ids, overlapping_polygons = self.qgis_utils.geometry.get_inner_intersections_between_polygons(layers[db.names.OP_RIGHT_OF_WAY_T], layers[db.names.OP_BUILDING_T])

            if overlapping_polygons is not None:
                new_features = list()
                for key, polygon in zip(ids, overlapping_polygons.asGeometryCollection()):
                    new_feature = QgsVectorLayerUtils().createFeature(error_layer,
                                      polygon,
                                      {0: dict_uuid_right_of_way.get(key[0]),  # right_of_way_id
                                       1: dict_uuid_building.get(key[1]),  # building_id
                                       2: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E3005),
                                       3: QUALITY_RULE_ERROR_CODE_E3005})
                    new_features.append(new_feature)

                data_provider.addFeatures(new_features)

            if error_layer.featureCount() > 0:
                added_layer = self.qgis_utils.add_error_layer(db, error_layer)

                return (QCoreApplication.translate("PolygonQualityRules",
                                 "A memory layer with {} Right of Way-Building overlaps has been added to the map!").format(
                                 added_layer.featureCount()), Qgis.Critical)
            else:
                return (QCoreApplication.translate("PolygonQualityRules",
                                 "There are no Right of Way-Building overlaps."), Qgis.Success)

    def check_gaps_in_plots(self, db):
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Polygon.GAPS_IN_PLOTS)
        use_roads = bool(QSettings().value('Asistente-LADM_COL/quality/use_roads', DEFAULT_USE_ROADS_VALUE, bool))
        plot_layer = self.qgis_utils.get_layer(db, db.names.OP_PLOT_T, True)
        if not plot_layer:
            return

        if plot_layer.featureCount() == 0:
            return (QCoreApplication.translate("PolygonQualityRules",
                             "There are no Plot features to check 'Plot should not have gaps'."), Qgis.Warning)

        else:
            error_layer = QgsVectorLayer("MultiPolygon?crs={}".format(plot_layer.sourceCrs().authid()),
                                         rule.error_table_name, "memory")
            data_provider = error_layer.dataProvider()
            data_provider.addAttributes(rule.error_table_fields)
            error_layer.updateFields()

            gaps = self.qgis_utils.geometry.get_gaps_in_polygon_layer(plot_layer, use_roads)
            fids_list = GeometryUtils.get_intersection_features(plot_layer, gaps)  # List of lists of qgis ids

            uuids_list = list()
            for fids in fids_list:
                uuids_list.append([f[db.names.T_ILI_TID_F] for f in plot_layer.getFeatures(fids)])

            if gaps is not None:
                new_features = list()
                for geom, id_serial in zip(gaps, range(0, len(gaps))):
                    feature = QgsVectorLayerUtils().createFeature(error_layer,
                                  geom,
                                  {0: id_serial,
                                   1: ', '.join(uuids_list[id_serial]),  # list of geometries and ids are corresponding in order
                                   2: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E3006),
                                   3: QUALITY_RULE_ERROR_CODE_E3006})
                    new_features.append(feature)
                data_provider.addFeatures(new_features)

            if error_layer.featureCount() > 0:
                added_layer = self.qgis_utils.add_error_layer(db, error_layer)

                return (QCoreApplication.translate("PolygonQualityRules",
                                 "A memory layer with {} gaps in layer Plots has been added to the map!").format(added_layer.featureCount()), Qgis.Critical)

            else:
                return (QCoreApplication.translate("PolygonQualityRules",
                                 "There are no gaps in layer Plot."), Qgis.Success)

    def check_multiparts_in_right_of_way(self, db):
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Polygon.MULTIPART_IN_RIGHT_OF_WAY)
        right_of_way_layer = self.qgis_utils.get_layer(db, db.names.OP_RIGHT_OF_WAY_T, True)
        if not right_of_way_layer:
            return

        if right_of_way_layer.featureCount() == 0:
            return (QCoreApplication.translate("PolygonQualityRules",
                             "There are no Right Of Way features to check 'Right Of Way should not have Multipart geometries'."), Qgis.Warning)

        else:
            error_layer = QgsVectorLayer("Polygon?crs={}".format(right_of_way_layer.sourceCrs().authid()),
                                         rule.error_table_name, "memory")
            data_provider = error_layer.dataProvider()
            data_provider.addAttributes(rule.error_table_fields)
            error_layer.updateFields()

            multi_parts, ids = self.qgis_utils.geometry.get_multipart_geoms(right_of_way_layer)

            if multi_parts is not None:
                new_features = list()
                for geom, id in zip(multi_parts, ids):
                    feature = QgsVectorLayerUtils().createFeature(error_layer,
                                  geom,
                                  {0: right_of_way_layer.getFeature(id)[db.names.T_ILI_TID_F],
                                   1: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E3007),
                                   2: QUALITY_RULE_ERROR_CODE_E3007})
                    new_features.append(feature)
                data_provider.addFeatures(new_features)

            if error_layer.featureCount() > 0:
                added_layer = self.qgis_utils.add_error_layer(db, error_layer)

                return (QCoreApplication.translate("PolygonQualityRules",
                                 "A memory layer with {} multipart geometries in layer Right Of Way has been added to the map!").format(
                                 added_layer.featureCount()), Qgis.Critical)

            else:
                return (QCoreApplication.translate("PolygonQualityRules",
                                 "There are no multipart geometries in layer Right Of Way."), Qgis.Success)

    def check_plot_nodes_covered_by_boundary_points(self, db):
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Polygon.PLOT_NODES_COVERED_BY_BOUNDARY_POINTS)
        layers = {
            db.names.OP_PLOT_T: None,
            db.names.OP_BOUNDARY_POINT_T: None
        }
        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        if layers[db.names.OP_PLOT_T].featureCount() == 0:
            return (QCoreApplication.translate("PolygonQualityRules",
                             "There are no plots to check 'Plots should be covered by boundary points'."), Qgis.Warning)
        else:
            error_layer = QgsVectorLayer("Point?crs={}".format(layers[db.names.OP_PLOT_T].sourceCrs().authid()),
                                         rule.error_table_name,
                                         "memory")

            data_provider = error_layer.dataProvider()
            data_provider.addAttributes(rule.error_table_fields)
            error_layer.updateFields()

            point_list = self.get_plot_nodes_features_not_covered_by_boundary_points(layers[db.names.OP_BOUNDARY_POINT_T],
                                                                                                  layers[db.names.OP_PLOT_T],
                                                                                                  db.names.T_ILI_TID_F)

            features = list()
            for point in point_list:
                new_feature = QgsVectorLayerUtils().createFeature(error_layer,
                                  point[1],  # Geometry
                                  {0: point[0],  # feature uuid
                                   1: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E3008),
                                   2: QUALITY_RULE_ERROR_CODE_E3008})
                features.append(new_feature)

            error_layer.dataProvider().addFeatures(features)

            if error_layer.featureCount() > 0:
                added_layer = self.qgis_utils.add_error_layer(db, error_layer)
                return (QCoreApplication.translate(
                                 "PolygonQualityRules",
                                 "A memory layer with {} plot nodes not covered by boundary points has been added to the map!")
                                 .format(added_layer.featureCount()), Qgis.Critical)

            else:
                return (QCoreApplication.translate("PolygonQualityRules",
                                 "All plot nodes are covered by boundary points!"), Qgis.Success)

    def check_building_within_plots(self, db):
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Polygon.BUILDINGS_SHOULD_BE_WITHIN_PLOTS)
        names = db.names
        layers = {
            names.OP_BUILDING_T: None,
            names.OP_PLOT_T: None,
            names.OP_PARCEL_T: None,
            names.COL_UE_BAUNIT_T: None,
            names.OP_CONDITION_PARCEL_TYPE_D: None
        }
        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        if layers[names.OP_BUILDING_T].featureCount() == 0:
            return (QCoreApplication.translate("PolygonQualityRules",
                             "There are no buildings to check 'Building should be within Plots'."), Qgis.Warning)

        else:
            error_layer = QgsVectorLayer("MultiPolygon?crs={}".format(layers[names.OP_BUILDING_T].sourceCrs().authid()),
                                         rule.error_table_name, "memory")
            data_provider = error_layer.dataProvider()
            data_provider.addAttributes(rule.error_table_fields)
            error_layer.updateFields()

            building_disjoint, building_overlaps, building_within = GeometryUtils.get_relationships_among_polygons(layers[names.OP_BUILDING_T], layers[names.OP_PLOT_T])

            tid_buildings = self.check_building_not_associated_with_correct_plot(building_within,
                                                                                 layers[names.OP_BUILDING_T],
                                                                                 layers[names.OP_PLOT_T],
                                                                                 layers[names.OP_PARCEL_T],
                                                                                 layers[names.COL_UE_BAUNIT_T],
                                                                                 layers[names.OP_CONDITION_PARCEL_TYPE_D],
                                                                                 names)

            new_features = list()
            # Buildings that are not covered by a plot
            for building_with_no_plot in layers[names.OP_BUILDING_T].getFeatures(building_disjoint):
                new_feature = QgsVectorLayerUtils().createFeature(
                                error_layer,
                                building_with_no_plot.geometry(),
                                {0: building_with_no_plot[names.T_ILI_TID_F],
                                 1: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E300901),
                                 2: QUALITY_RULE_ERROR_CODE_E300901})
                new_features.append(new_feature)

            # Buildings that are not within a plot
            for building_not_within_plot in layers[names.OP_BUILDING_T].getFeatures(building_overlaps):
                new_feature = QgsVectorLayerUtils().createFeature(
                                error_layer,
                                building_not_within_plot.geometry(),
                                {0: building_not_within_plot[names.T_ILI_TID_F],
                                 1: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E300902),
                                 2: QUALITY_RULE_ERROR_CODE_E300902})
                new_features.append(new_feature)
            data_provider.addFeatures(new_features)

            exp = "{} in ({})".format(names.T_ID_F, ", ".join([str(tid) for tid in tid_buildings]))
            # Building is within a plot, but this is not the corresponding plot
            for building in layers[names.OP_BUILDING_T].getFeatures(exp):
                new_feature = QgsVectorLayerUtils().createFeature(
                                error_layer,
                                building.geometry(),
                                {0: building[names.T_ILI_TID_F],
                                 1: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E300903),
                                 2: QUALITY_RULE_ERROR_CODE_E300903})
                new_features.append(new_feature)
            data_provider.addFeatures(new_features)

            if error_layer.featureCount() > 0:
                added_layer = self.qgis_utils.add_error_layer(db, error_layer)

                return (QCoreApplication.translate("PolygonQualityRules",
                                 "A memory layer with {} buildings not within a plot has been added to the map!").format(added_layer.featureCount()), Qgis.Critical)

            else:
                return (QCoreApplication.translate("PolygonQualityRules",
                                 "All buildings are within a plot."), Qgis.Success)


    @staticmethod
    def check_building_not_associated_with_correct_plot(building_within, building_layer, plot_layer, parcel_layer, ue_baunit_layer, condition_parcel_layer, names):

        buildings_bad_relation = list()
        buildings_to_check = {f[names.T_ID_F]: f for f in building_layer.getFeatures(building_within)}

        # Get spatial relation (within) between building and plots
        building_layer.selectByIds(building_within)
        building_within_plots_layer = processing.run("qgis:joinattributesbylocation",
                                                     {'INPUT': QgsProcessingFeatureSourceDefinition(building_layer.id(), True),
                                                      'JOIN': plot_layer,
                                                      'PREDICATE': [5],  # within
                                                      'JOIN_FIELDS': ['t_id'],
                                                      'METHOD': 0,  # 1 to many
                                                      'DISCARD_NONMATCHING': True,
                                                      'PREFIX': '',
                                                      'OUTPUT': 'memory:'})['OUTPUT']
        building_layer.removeSelection()  # Remove previous selection

        # Get building units within plots
        building_within_plots = dict()
        for feature in building_within_plots_layer.getFeatures():
            if not building_within_plots.get(feature[names.T_ID_F]):
                building_within_plots[feature[names.T_ID_F]] = feature[names.T_ID_F + '_2']
            else:
                # error: building should only be within one plot
                buildings_bad_relation.append(feature[names.T_ID_F])
                del building_within_plots[feature[names.T_ID_F]]

        # Remove buildings that are within more than one plot
        remove_keys_from_dict(buildings_bad_relation, buildings_to_check)

        # Relation building - parcel
        building_parcels = dict()
        expr = "{building_f} in ({filter}) and {plot_f} is null and {building_unit_f} is null and {right_of_way_f} is null".format(
            filter=', '.join([str(t_id) for t_id in buildings_to_check.keys()]),
            plot_f=names.COL_UE_BAUNIT_T_OP_PLOT_F,
            building_f=names.COL_UE_BAUNIT_T_OP_BUILDING_F,
            building_unit_f=names.COL_UE_BAUNIT_T_OP_BUILDING_UNIT_F,
            right_of_way_f=names.COL_UE_BAUNIT_T_OP_RIGHT_OF_WAY_F
        )

        for feature in ue_baunit_layer.getFeatures(expr):
            if not building_parcels.get(feature[names.COL_UE_BAUNIT_T_OP_BUILDING_F]):
                building_parcels[feature[names.COL_UE_BAUNIT_T_OP_BUILDING_F]] = feature[names.COL_UE_BAUNIT_T_PARCEL_F]
            else:
                # error: building should only have one parcel associated
                buildings_bad_relation.append(feature[names.COL_UE_BAUNIT_T_OP_BUILDING_F])
                del building_parcels[feature[names.COL_UE_BAUNIT_T_OP_BUILDING_F]]

        # Remove buildings that have more than one association with parcel
        remove_keys_from_dict(buildings_bad_relation, buildings_to_check)

        # Get parcel condition
        expr = "{} in ({})".format(names.T_ID_F, ', '.join([str(t_id) for t_id in building_parcels.values()]))
        domain_condition_parcel = {f[names.T_ID_F]: f[names.ILICODE_F] for f in condition_parcel_layer.getFeatures()}
        parcel_condition = {f[names.T_ID_F]: domain_condition_parcel.get(f[names.OP_PARCEL_T_PARCEL_TYPE_F]) for f in parcel_layer.getFeatures(expr)}

        # Relation parcel - plot
        parcel_plot = dict()
        expr = "{parcel_f} in ({filter}) and {building_f} is null and {building_unit_f} is null and {right_of_way_f} is null".format(
            filter=', '.join([str(t_id) for t_id in building_parcels.values()]),
            parcel_f=names.COL_UE_BAUNIT_T_PARCEL_F,
            building_f=names.COL_UE_BAUNIT_T_OP_BUILDING_F,
            building_unit_f=names.COL_UE_BAUNIT_T_OP_BUILDING_UNIT_F,
            right_of_way_f=names.COL_UE_BAUNIT_T_OP_RIGHT_OF_WAY_F
        )

        for feature in ue_baunit_layer.getFeatures(expr):
            if not parcel_plot.get(feature[names.COL_UE_BAUNIT_T_PARCEL_F]):
                parcel_plot[feature[names.COL_UE_BAUNIT_T_PARCEL_F]] = feature[names.COL_UE_BAUNIT_T_OP_PLOT_F]
            else:
                # error: parcel should only have one plot associate
                del parcel_plot[feature[names.COL_UE_BAUNIT_T_PARCEL_F]]

        for t_id_building in buildings_to_check:
            parcel_tid = building_parcels.get(t_id_building)
            if parcel_tid:
                # If the building is associated to parcel with condition mejora, it does not have corresponding plot.
                if parcel_condition.get(parcel_tid) not in (LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA,
                                                            LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA):
                    # the associated plot in the uebaunit table must coincide with the spatially associated plot
                    if parcel_plot.get(parcel_tid):
                        if parcel_plot.get(parcel_tid) != building_within_plots.get(t_id_building):
                            # error: alphanumeric relation between building and plot should be equal to spatial relation
                            buildings_bad_relation.append(t_id_building)
                    else:
                        # error: relation between building and plot not register in uebaunit
                        buildings_bad_relation.append(t_id_building)
            else:
                # error: building not register in uebaunit
                buildings_bad_relation.append(t_id_building)

        return list(set(buildings_bad_relation))  # Uniques t_id

    def check_building_unit_within_plots(self, db):
        rule = self.quality_rules_manager.get_quality_rule(EnumQualityRule.Polygon.BUILDING_UNITS_SHOULD_BE_WITHIN_PLOTS)
        names = db.names
        layers = {
            names.OP_BUILDING_T: None,
            names.OP_BUILDING_UNIT_T: None,
            names.OP_PLOT_T: None,
            names.OP_PARCEL_T: None,
            names.COL_UE_BAUNIT_T: None,
            names.OP_CONDITION_PARCEL_TYPE_D: None
        }

        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        if layers[names.OP_BUILDING_UNIT_T].featureCount() == 0:
            return (QCoreApplication.translate("PolygonQualityRules",
                             "There are no buildings to check 'Building should be within Plots'."), Qgis.Warning)

        else:
            error_layer = QgsVectorLayer("MultiPolygon?crs={}".format(layers[names.OP_BUILDING_UNIT_T].sourceCrs().authid()),
                                         rule.error_table_name, "memory")
            data_provider = error_layer.dataProvider()
            data_provider.addAttributes(rule.error_table_fields)
            error_layer.updateFields()

            building_units_disjoint_plots, building_units_overlaps_plots, building_units_within_plots = GeometryUtils.get_relationships_among_polygons(layers[names.OP_BUILDING_UNIT_T], layers[names.OP_PLOT_T])

            tids_building_units_bad_relation_plots = self.check_building_unit_not_associated_with_correct_plot(
                building_units_within_plots,
                layers[names.OP_BUILDING_UNIT_T],
                layers[names.OP_PLOT_T],
                layers[names.OP_PARCEL_T],
                layers[names.COL_UE_BAUNIT_T],
                layers[names.OP_CONDITION_PARCEL_TYPE_D],
                names)

            exp = "{} in ({})".format(names.T_ID_F, ", ".join([str(tid) for tid in tids_building_units_bad_relation_plots]))
            building_units_bad_relation_plots = [f for f in layers[names.OP_BUILDING_UNIT_T].getFeatures(exp)]
            ids_building_units_bad_relation_plots = [f.id() for f in building_units_bad_relation_plots]

            # Check relations between building units and building
            building_units_disjoint_buildings, building_units_overlaps_buildings, building_units_within_building = GeometryUtils.get_relationships_among_polygons(layers[names.OP_BUILDING_UNIT_T], layers[names.OP_BUILDING_T])
            missing_building_units_disjoint_buildings = list(set(building_units_disjoint_buildings) - set(ids_building_units_bad_relation_plots))
            missing_building_units_overlaps_buildings = list(set(building_units_overlaps_buildings) - set(ids_building_units_bad_relation_plots))
            missing_building_units_within_building = list(set(building_units_within_building) - set(ids_building_units_bad_relation_plots))

            t_ids_building_units_bad_relation_buildings = list()
            if missing_building_units_within_building:
                t_ids_building_units_bad_relation_buildings = self.check_building_unit_not_associated_with_correct_building(
                    missing_building_units_within_building,
                    layers[names.OP_BUILDING_UNIT_T],
                    layers[names.OP_BUILDING_T],
                    layers[names.OP_PARCEL_T],
                    layers[names.COL_UE_BAUNIT_T],
                    layers[names.OP_CONDITION_PARCEL_TYPE_D],
                    names)
            exp = "{} in ({})".format(names.T_ID_F, ", ".join([str(tid) for tid in t_ids_building_units_bad_relation_buildings]))
            building_units_bad_relation_buildings = [f for f in layers[names.OP_BUILDING_UNIT_T].getFeatures(exp)]

            new_features = list()
            # Building unit disjoint from plots
            for building_unit_disjoint_plot in layers[names.OP_BUILDING_UNIT_T].getFeatures(building_units_disjoint_plots):
                new_feature = QgsVectorLayerUtils().createFeature(
                                error_layer,
                                building_unit_disjoint_plot.geometry(),
                                {0: building_unit_disjoint_plot[names.T_ILI_TID_F],
                                 1: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E301001),
                                 2: QUALITY_RULE_ERROR_CODE_E301001})
                new_features.append(new_feature)

            # Building unit not within a plot
            for building_unit_overlap_plot in layers[names.OP_BUILDING_UNIT_T].getFeatures(building_units_overlaps_plots):
                new_feature = QgsVectorLayerUtils().createFeature(
                                error_layer,
                                building_unit_overlap_plot.geometry(),
                                {0: building_unit_overlap_plot[names.T_ILI_TID_F],
                                 1: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E301002),
                                 2: QUALITY_RULE_ERROR_CODE_E301002})
                new_features.append(new_feature)

            # Building unit is within a plot, but this is not the corresponding plot
            for building_unit_bad_relation_plot in building_units_bad_relation_plots:
                new_feature = QgsVectorLayerUtils().createFeature(
                                error_layer,
                                building_unit_bad_relation_plot.geometry(),
                                {0: building_unit_bad_relation_plot[names.T_ILI_TID_F],
                                 1: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E301003),
                                 2: QUALITY_RULE_ERROR_CODE_E301003})
                new_features.append(new_feature)

            # Building unit disjoint from building
            for building_unit_disjoint_building in layers[names.OP_BUILDING_UNIT_T].getFeatures(missing_building_units_disjoint_buildings):
                new_feature = QgsVectorLayerUtils().createFeature(
                                error_layer,
                                building_unit_disjoint_building.geometry(),
                                {0: building_unit_disjoint_building[names.T_ILI_TID_F],
                                 1: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E301004),
                                 2: QUALITY_RULE_ERROR_CODE_E301004})
                new_features.append(new_feature)

            # Building unit not within a building
            for building_unit_overlap_building in layers[names.OP_BUILDING_UNIT_T].getFeatures(missing_building_units_overlaps_buildings):
                new_feature = QgsVectorLayerUtils().createFeature(
                                error_layer,
                                building_unit_overlap_building.geometry(),
                                {0: building_unit_overlap_building[names.T_ILI_TID_F],
                                 1: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E301005),
                                 2: QUALITY_RULE_ERROR_CODE_E301005})
                new_features.append(new_feature)

            # Building unit is within a building, but this is not the corresponding building
            for building_units_bad_relation_building in building_units_bad_relation_buildings:
                new_feature = QgsVectorLayerUtils().createFeature(
                                error_layer,
                                building_units_bad_relation_building.geometry(),
                                {0: building_units_bad_relation_building[names.T_ILI_TID_F],
                                 1: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E301006),
                                 2: QUALITY_RULE_ERROR_CODE_E301006})
                new_features.append(new_feature)

            data_provider.addFeatures(new_features)

            if error_layer.featureCount() > 0:
                added_layer = self.qgis_utils.add_error_layer(db, error_layer)

                return (QCoreApplication.translate("PolygonQualityRules",
                                 "A memory layer with {} building units not within a plot has been added to the map!").format(added_layer.featureCount()), Qgis.Critical)
            else:
                return (QCoreApplication.translate("PolygonQualityRules",
                                 "All building units are within a plot."), Qgis.Success)

    @staticmethod
    def check_building_unit_not_associated_with_correct_plot(building_units_within_plots, building_unit_layer, plot_layer, parcel_layer, ue_baunit_layer, condition_parcel_layer, names):
        building_units_bad_relation = list()
        building_units_to_check = {f[names.T_ID_F]: f for f in building_unit_layer.getFeatures(building_units_within_plots)}

        # Get spatial relation (within) between building units and plots
        building_unit_layer.selectByIds(building_units_within_plots)
        building_unit_within_plot_layer = processing.run("qgis:joinattributesbylocation",
             {'INPUT': QgsProcessingFeatureSourceDefinition(building_unit_layer.id(), True),
              'JOIN': plot_layer,
              'PREDICATE': [5],  # within
              'JOIN_FIELDS': ['t_id'],
              'METHOD': 0,  # 1 to many
              'DISCARD_NONMATCHING': True,
              'PREFIX': '',
              'OUTPUT': 'memory:'})['OUTPUT']
        building_unit_layer.removeSelection()  # Remove previous selection

        # Get building units within plots
        building_unit_within_plots = dict()
        for feature in building_unit_within_plot_layer.getFeatures():
            if not building_unit_within_plots.get(feature[names.T_ID_F]):
                building_unit_within_plots[feature[names.T_ID_F]] = feature[names.T_ID_F + '_2']
            else:
                # error: building unit should only be within one plot
                building_units_bad_relation.append(feature[names.T_ID_F])
                del building_unit_within_plots[feature[names.T_ID_F]]

        # Remove buildings units that are within more than one plot
        remove_keys_from_dict(building_units_bad_relation, building_units_to_check)

        # Relation building unit - parcel
        building_unit_parcels = dict()
        expr = "{building_unit_f} in ({filter}) and {plot_f} is null and {building_f} is null and {right_of_way_f} is null".format(
            filter=', '.join([str(t_id) for t_id in building_units_to_check.keys()]),
            plot_f=names.COL_UE_BAUNIT_T_OP_PLOT_F,
            building_f=names.COL_UE_BAUNIT_T_OP_BUILDING_F,
            building_unit_f=names.COL_UE_BAUNIT_T_OP_BUILDING_UNIT_F,
            right_of_way_f=names.COL_UE_BAUNIT_T_OP_RIGHT_OF_WAY_F
        )

        for feature in ue_baunit_layer.getFeatures(expr):
            if not building_unit_parcels.get(feature[names.COL_UE_BAUNIT_T_OP_BUILDING_UNIT_F]):
                building_unit_parcels[feature[names.COL_UE_BAUNIT_T_OP_BUILDING_UNIT_F]] = feature[names.COL_UE_BAUNIT_T_PARCEL_F]
            else:
                # error: building unit should only have one parcel associated
                building_units_bad_relation.append(feature[names.COL_UE_BAUNIT_T_OP_BUILDING_UNIT_F])
                del building_unit_parcels[feature[names.COL_UE_BAUNIT_T_OP_BUILDING_UNIT_F]]

        # Remove buildings units that have more than one association with parcel
        remove_keys_from_dict(building_units_bad_relation, building_units_to_check)

        # Get parcel condition
        expr = "{} in ({})".format(names.T_ID_F, ', '.join([str(t_id) for t_id in building_unit_parcels.values()]))
        domain_condition_parcel = {f[names.T_ID_F]: f[names.ILICODE_F] for f in condition_parcel_layer.getFeatures()}
        parcel_condition = {f[names.T_ID_F]: domain_condition_parcel.get(f[names.OP_PARCEL_T_PARCEL_TYPE_F]) for f in parcel_layer.getFeatures(expr)}

        # Relation parcel - plot
        parcel_plot = dict()
        expr = "{parcel_f} in ({filter}) and {building_f} is null and {building_unit_f} is null and {right_of_way_f} is null".format(
            filter=', '.join([str(t_id) for t_id in building_unit_parcels.values()]),
            parcel_f=names.COL_UE_BAUNIT_T_PARCEL_F,
            building_f=names.COL_UE_BAUNIT_T_OP_BUILDING_F,
            building_unit_f=names.COL_UE_BAUNIT_T_OP_BUILDING_UNIT_F,
            right_of_way_f=names.COL_UE_BAUNIT_T_OP_RIGHT_OF_WAY_F
        )

        for feature in ue_baunit_layer.getFeatures(expr):
            if not parcel_plot.get(feature[names.COL_UE_BAUNIT_T_PARCEL_F]):
                parcel_plot[feature[names.COL_UE_BAUNIT_T_PARCEL_F]] = feature[names.COL_UE_BAUNIT_T_OP_PLOT_F]
            else:
                # error: parcel should only have one plot associate
                del parcel_plot[feature[names.COL_UE_BAUNIT_T_PARCEL_F]]

        for t_id_building_unit in building_units_to_check:
            parcel_tid = building_unit_parcels.get(t_id_building_unit)
            if parcel_tid:
                # If the building unit is associated to parcel with condition horizontal property parcel unit, it does not have corresponding plot.
                if parcel_condition.get(parcel_tid) not in (LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT):
                    # the associated plot in the uebaunit table must coincide with the spatially associated plot
                    if parcel_plot.get(parcel_tid):
                        if parcel_plot.get(parcel_tid) != building_unit_within_plots.get(t_id_building_unit):
                            # error: alphanumeric relation between building unit and plot should be equal to spatial relation
                            building_units_bad_relation.append(t_id_building_unit)
                    else:
                        # error: relation between building unit and plot not register in uebaunit
                        building_units_bad_relation.append(t_id_building_unit)
            else:
                # error: building unit not register in uebaunit
                building_units_bad_relation.append(t_id_building_unit)

        return list(set(building_units_bad_relation))  # Uniques t_id

    @staticmethod
    def check_building_unit_not_associated_with_correct_building(building_units_within_building, building_unit_layer, building_layer, parcel_layer, ue_baunit_layer, condition_parcel_layer, names):
        building_units_bad_relation = list()
        building_units_to_check = {f[names.T_ID_F]: f for f in building_unit_layer.getFeatures(building_units_within_building)}

        # Get spatial relation (within) between building units and buildings
        building_unit_layer.selectByIds(building_units_within_building)
        building_unit_within_building_layer = processing.run("qgis:joinattributesbylocation",
             {'INPUT': QgsProcessingFeatureSourceDefinition(building_unit_layer.id(), True),
              'JOIN': building_layer,
              'PREDICATE': [5],  # within
              'JOIN_FIELDS': ['t_id'],
              'METHOD': 0,  # 1 to many
              'DISCARD_NONMATCHING': True,
              'PREFIX': '',
              'OUTPUT': 'memory:'})['OUTPUT']
        building_unit_layer.removeSelection()  # Remove previous selection

        # Get building units within buildings
        building_unit_within_building = dict()
        for feature in building_unit_within_building_layer.getFeatures():
            if not building_unit_within_building.get(feature[names.T_ID_F]):
                if feature[names.OP_BUILDING_UNIT_T_BUILDING_F] != feature[names.T_ID_F + '_2']:
                    # error: alphanumeric relation between building and building unit should be equal to spatial relation
                    building_units_bad_relation.append(feature[names.T_ID_F])
                else:
                    building_unit_within_building[feature[names.T_ID_F]] = feature[names.T_ID_F + '_2']
            else:
                # error: building unit should only be within one building
                building_units_bad_relation.append(feature[names.T_ID_F])
                del building_unit_within_building[feature[names.T_ID_F]]

        # Remove buildings units that are within more than one building or
        # alphanumeric relation between building and building unit should be equal to spatial relation
        remove_keys_from_dict(building_units_bad_relation, building_units_to_check)

        # Relation building unit - parcel
        building_unit_parcels = dict()
        expr = "{building_unit_f} in ({filter}) and {plot_f} is null and {building_f} is null and {right_of_way_f} is null".format(
            filter=', '.join([str(t_id) for t_id in building_units_to_check.keys()]),
            plot_f=names.COL_UE_BAUNIT_T_OP_PLOT_F,
            building_f=names.COL_UE_BAUNIT_T_OP_BUILDING_F,
            building_unit_f=names.COL_UE_BAUNIT_T_OP_BUILDING_UNIT_F,
            right_of_way_f=names.COL_UE_BAUNIT_T_OP_RIGHT_OF_WAY_F
        )

        for feature in ue_baunit_layer.getFeatures(expr):
            if not building_unit_parcels.get(feature[names.COL_UE_BAUNIT_T_OP_BUILDING_UNIT_F]):
                building_unit_parcels[feature[names.COL_UE_BAUNIT_T_OP_BUILDING_UNIT_F]] = feature[names.COL_UE_BAUNIT_T_PARCEL_F]
            else:
                # error: building unit should only have one parcel associated
                building_units_bad_relation.append(feature[names.COL_UE_BAUNIT_T_OP_BUILDING_UNIT_F])
                del building_unit_parcels[feature[names.COL_UE_BAUNIT_T_OP_BUILDING_UNIT_F]]

        # Remove buildings units that are within more than one plot
        remove_keys_from_dict(building_units_bad_relation, building_units_to_check)

        # Get parcel condition
        expr = "{} in ({})".format(names.T_ID_F, ', '.join([str(t_id) for t_id in building_unit_parcels.values()]))
        domain_condition_parcel = {f[names.T_ID_F]: f[names.ILICODE_F] for f in condition_parcel_layer.getFeatures()}
        parcel_condition = {f[names.T_ID_F]: domain_condition_parcel.get(f[names.OP_PARCEL_T_PARCEL_TYPE_F]) for f in parcel_layer.getFeatures(expr)}

        # Relation parcel - building
        parcel_building = dict()
        expr = "{parcel_f} in ({filter}) and {plot_f} is null and {building_unit_f} is null and {right_of_way_f} is null".format(
            filter=', '.join([str(t_id) for t_id in building_unit_parcels.values()]),
            parcel_f=names.COL_UE_BAUNIT_T_PARCEL_F,
            plot_f=names.COL_UE_BAUNIT_T_OP_PLOT_F,
            building_unit_f=names.COL_UE_BAUNIT_T_OP_BUILDING_UNIT_F,
            right_of_way_f=names.COL_UE_BAUNIT_T_OP_RIGHT_OF_WAY_F
        )

        for feature in ue_baunit_layer.getFeatures(expr):
            if not parcel_building.get(feature[names.COL_UE_BAUNIT_T_PARCEL_F]):
                parcel_building[feature[names.COL_UE_BAUNIT_T_PARCEL_F]] = [feature[names.COL_UE_BAUNIT_T_OP_BUILDING_F]]
            else:
                parcel_building.get(feature[names.COL_UE_BAUNIT_T_PARCEL_F]).append(feature[names.COL_UE_BAUNIT_T_OP_BUILDING_F])

        for t_id_building_unit in building_units_to_check:
            parcel_tid = building_unit_parcels.get(t_id_building_unit)
            if parcel_tid:
                # If the building unit is associated to parcel with condition horizontal property parcel unit, it does not have corresponding building.
                if parcel_condition.get(parcel_tid) not in (LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT):
                    # the associated building in the uebaunit table must coincide with the spatially associated plot
                    if parcel_building.get(parcel_tid):
                        if building_unit_within_building.get(t_id_building_unit) not in parcel_building.get(parcel_tid):
                            # error: alphanumeric relation between building unit and building should be equal to spatial relation
                            building_units_bad_relation.append(t_id_building_unit)
                    else:
                        # error: relation between building unit and plot not register in uebaunit
                        building_units_bad_relation.append(t_id_building_unit)
            else:
                # error: building unit not register in uebaunit
                building_units_bad_relation.append(t_id_building_unit)

        return list(set(building_units_bad_relation))  # Uniques t_id

    # UTILS METHODS
    def get_plot_features_not_covered_by_boundaries(self, db, plot_layer, boundary_layer, more_bfs_layer, less_layer, error_layer, id_field):
        """
        Returns all plot features that have errors when checking if they are covered by boundaries.
        That is both geometric and alphanumeric (topology table) errors.
        """
        dict_uuid_plots = get_uuid_dict(plot_layer, db.names, id_field)
        dict_uuid_boundary = get_uuid_dict(boundary_layer, db.names, id_field)
        plot_as_lines_layer = processing.run("ladm_col:polygonstolines", {'INPUT': plot_layer, 'OUTPUT': 'memory:'})['OUTPUT']

        # create dict with layer data
        id_field_idx = plot_as_lines_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
        dict_plot_as_lines = {feature[id_field]: feature for feature in plot_as_lines_layer.getFeatures(request)}

        id_field_idx = boundary_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
        dict_boundary = {feature[id_field]: feature for feature in boundary_layer.getFeatures(request)}

        exp_more = '"{}" is not null and "{}" is not null'.format(db.names.MORE_BFS_T_OP_BOUNDARY_F, db.names.MORE_BFS_T_OP_PLOT_F)
        list_more_bfs = [{'plot_id': feature[db.names.MORE_BFS_T_OP_PLOT_F], 'boundary_id': feature[db.names.MORE_BFS_T_OP_BOUNDARY_F]}
                         for feature in more_bfs_layer.getFeatures(exp_more)]

        exp_less = '"{}" is not null and "{}" is not null'.format(db.names.LESS_BFS_T_OP_BOUNDARY_F, db.names.LESS_BFS_T_OP_PLOT_F)
        list_less = [{'plot_id': feature[db.names.LESS_BFS_T_OP_PLOT_F], 'boundary_id': feature[db.names.LESS_BFS_T_OP_BOUNDARY_F]}
                     for feature in less_layer.getFeatures(exp_less)]

        tmp_inner_rings_layer = self.qgis_utils.geometry.get_inner_rings_layer(db.names, plot_layer, db.names.T_ID_F)
        inner_rings_layer = processing.run("native:addautoincrementalfield",
                                           {'INPUT': tmp_inner_rings_layer,
                                            'FIELD_NAME': 'AUTO',
                                            'START': 0,
                                            'GROUP_FIELDS': [],
                                            'SORT_EXPRESSION': '',
                                            'SORT_ASCENDING': True,
                                            'SORT_NULLS_FIRST': False,
                                            'OUTPUT': 'memory:'})['OUTPUT']


        id_field_idx = inner_rings_layer.fields().indexFromName(id_field)
        auto_idx = inner_rings_layer.fields().indexFromName('AUTO')
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx, auto_idx])
        dict_inner_rings = {'{}-{}'.format(feature[id_field], feature['AUTO']): feature for feature in inner_rings_layer.getFeatures(request)}

        # spatial joins between inner rings and boundary
        spatial_join_inner_rings_boundary_layer = processing.run("qgis:joinattributesbylocation",
                                                                 {'INPUT': inner_rings_layer,
                                                                  'JOIN': boundary_layer,
                                                                  'PREDICATE': [0],  # Intersects
                                                                  'JOIN_FIELDS': [id_field],
                                                                  'METHOD': 0,
                                                                  'DISCARD_NONMATCHING': True,
                                                                  'PREFIX': '',
                                                                  'OUTPUT': 'memory:'})['OUTPUT']
        # The id field has the same name for both layers
        # This list is only used to check plot's inner rings without boundaries
        dict_spatial_join_inner_rings_boundary = [{'plot_ring_id': '{}-{}'.format(feature[id_field], feature['AUTO']), 'boundary_id': feature[id_field + '_2']}
                                                  for feature in spatial_join_inner_rings_boundary_layer.getFeatures()]

        # list create for filter inner rings from spatial join with between plot and boundary
        list_spatial_join_plot_ring_boundary = [{'plot_id': feature[id_field],
                                                   'boundary_id': feature[id_field + '_2']}
                                                  for feature in spatial_join_inner_rings_boundary_layer.getFeatures()]

        # Spatial join between plot as lines and boundary
        spatial_join_plot_boundary_layer = processing.run("qgis:joinattributesbylocation",
                                                          {'INPUT': plot_as_lines_layer,
                                                           'JOIN': boundary_layer,
                                                           'PREDICATE': [0],
                                                           'JOIN_FIELDS': [id_field],
                                                           'METHOD': 0,
                                                           'DISCARD_NONMATCHING': True,
                                                           'PREFIX': '',
                                                           'OUTPUT': 'memory:'})['OUTPUT']
        # The id field has the same name for both layers
        dict_spatial_join_plot_boundary = [{'plot_id': feature[id_field], 'boundary_id': feature[id_field + '_2']}
                                           for feature in spatial_join_plot_boundary_layer.getFeatures()]

        #####################################################
        # Validation of geometric errors
        #####################################################

        # Identify plots with geometry problems and remove coincidence in spatial join between plot as line and boundary
        # and inner_rings and boundary. No need to check further topological rules for plots

        errors_plot_boundary_diffs = self.qgis_utils.geometry.difference_plot_boundary(db.names, plot_as_lines_layer, boundary_layer, db.names.T_ID_F)
        for error_diff in errors_plot_boundary_diffs:
            plot_id = error_diff['id']
            # All plots with geometric errors are eliminated. It is not necessary check more
            # in spatial join between plot as line and boundary
            for item_sj in dict_spatial_join_plot_boundary.copy():
                if item_sj['plot_id'] == plot_id:
                    dict_spatial_join_plot_boundary.remove(item_sj)

            # All plots with geometric errors are eliminated. It is not necessary check more
            # in spatial join between inner_rings and boundary
            for item_sj in dict_spatial_join_inner_rings_boundary.copy():
                if int(item_sj['plot_ring_id'].split('-')[0]) == plot_id:
                    dict_spatial_join_inner_rings_boundary.remove(item_sj)

        ######################################################
        # Validation of errors in alphanumeric topology tables
        ######################################################

        # start validation for more_bfs table
        # remove spatial join intersection with geometries that no contain lines. Because it is not necessary to check
        for item_sj in dict_spatial_join_plot_boundary.copy():
            boundary_id = item_sj['boundary_id']
            plot_id = item_sj['plot_id']

            if item_sj in list_spatial_join_plot_ring_boundary:
                # it is removed because it is registered in the spatial join between rings and boundaries
                # and it shouldn't be registered in the topology table of more_bfs
                dict_spatial_join_plot_boundary.remove(item_sj)
            else:
                plot_geom = dict_plot_as_lines[plot_id].geometry()
                boundary_geom = dict_boundary[boundary_id].geometry()
                intersection = plot_geom.intersection(boundary_geom)

                if intersection.type() != QgsWkbTypes.LineGeometry:
                    if intersection.type() == QgsWkbTypes.UnknownGeometry:
                        has_line = False
                        for part in intersection.asGeometryCollection():
                            if part.isMultipart():
                                for i in range(part.numGeometries()):
                                    if QgsWkbTypes.geometryType(
                                            part.geometryN(i).wkbType()) == QgsWkbTypes.LineGeometry:
                                        has_line = True
                                        break
                            else:
                                if part.type() == QgsWkbTypes.LineGeometry:
                                    has_line = True
                                    break
                        if not has_line:
                            # Remove point intersections plot-boundary
                            dict_spatial_join_plot_boundary.remove(item_sj)
                    else:
                        dict_spatial_join_plot_boundary.remove(item_sj)

        # Check relation between plot and boundary not registered in more_bfs
        errors_not_in_more_bfs = list()
        errors_duplicate_in_more_bfs = list()
        for item_sj_pb in dict_spatial_join_plot_boundary:
            count_more_bfs = list_more_bfs.count(item_sj_pb)
            if count_more_bfs > 1:
                errors_duplicate_in_more_bfs.append((item_sj_pb['plot_id'], item_sj_pb['boundary_id']))
            elif count_more_bfs == 0:
                errors_not_in_more_bfs.append((item_sj_pb['plot_id'], item_sj_pb['boundary_id']))

        # finalize validation for more_bfs table

        # start validation for less table

        errors_not_in_less = list()
        errors_duplicate_in_less = list()
        # start validation for more_bfs table
        # remove spatial join intersection with geometries that no contain lines.
        # Because it is not necessary to check topology register
        for inner_ring in dict_spatial_join_inner_rings_boundary:
            boundary_id = inner_ring['boundary_id']
            plot_ring_id = inner_ring['plot_ring_id']

            boundary_geom = dict_boundary[boundary_id].geometry()
            inner_ring_geom = dict_inner_rings[plot_ring_id].geometry()

            # check intersections difference to line, we check that collections dont have lines parts
            intersection = inner_ring_geom.intersection(boundary_geom)
            has_line = False
            if intersection.type() != QgsWkbTypes.LineGeometry:
                if intersection.type() == QgsWkbTypes.UnknownGeometry:
                    for part in intersection.asGeometryCollection():
                        if part.isMultipart():
                            for i in range(part.numGeometries()):
                                if QgsWkbTypes.geometryType(part.geometryN(i).wkbType()) == QgsWkbTypes.LineGeometry:
                                    has_line = True
                                    break
                        else:
                            if part.type() == QgsWkbTypes.LineGeometry:
                                has_line = True
                                break
            else:
                has_line = True

            if has_line:
                tmp_dict_plot_boundary = {'plot_id': int(plot_ring_id.split('-')[0]), 'boundary_id': boundary_id}
                count_less = list_less.count(tmp_dict_plot_boundary)

                if count_less >1:
                    errors_duplicate_in_less.append((plot_ring_id, boundary_id))  # duplicate in less table
                elif count_less == 0:
                    errors_not_in_less.append((plot_ring_id, boundary_id))  # not registered less table
        # finalize validation for less table

        features = list()

        # plot not covered by boundary
        for plot_boundary_diff in errors_plot_boundary_diffs:
            plot_id = plot_boundary_diff['id']
            plot_geom = plot_boundary_diff['geometry']
            new_feature = QgsVectorLayerUtils().createFeature(error_layer,
                                                              plot_geom,
                                                              {0: dict_uuid_plots.get(plot_id),
                                                               1: None,
                                                               2: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E300401),
                                                               3: QUALITY_RULE_ERROR_CODE_E300401})
            features.append(new_feature)

        # not registered more bfs
        if errors_not_in_more_bfs:
            for error_more_bfs in set(errors_not_in_more_bfs):
                plot_id = error_more_bfs[0]  # plot_id
                boundary_id = error_more_bfs[1]  # boundary_id
                geom_plot = dict_plot_as_lines[plot_id].geometry()
                new_feature = QgsVectorLayerUtils().createFeature(error_layer, geom_plot,
                                                                  {0: dict_uuid_plots.get(plot_id),
                                                                   1: dict_uuid_boundary.get(boundary_id),
                                                                   2: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E300404),
                                                                   3: QUALITY_RULE_ERROR_CODE_E300404})
                features.append(new_feature)

        # Duplicate in more bfs
        if errors_duplicate_in_more_bfs:
            for error_more_bfs in set(errors_duplicate_in_more_bfs):
                plot_id = error_more_bfs[0]  # plot_id
                boundary_id = error_more_bfs[1]  # boundary_id
                geom_plot = dict_plot_as_lines[plot_id].geometry()
                new_feature = QgsVectorLayerUtils().createFeature(error_layer,
                                                                  geom_plot,
                                                                  {0: dict_uuid_plots.get(plot_id),
                                                                   1: dict_uuid_boundary.get(boundary_id),
                                                                   2: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E300402),
                                                                   3: QUALITY_RULE_ERROR_CODE_E300402})
                features.append(new_feature)

        # not registered less
        if errors_not_in_less:
            for error_less in set(errors_not_in_less):
                plot_ring_id = error_less[0]  # plot_ring_id
                plot_id = int(plot_ring_id.split('-')[0]) # plot_id
                boundary_id = error_less[1]  # boundary_id
                geom_ring = dict_inner_rings[plot_ring_id].geometry()
                new_feature = QgsVectorLayerUtils().createFeature(error_layer,
                                                                  geom_ring,
                                                                  {0: dict_uuid_plots.get(plot_id),
                                                                   1: dict_uuid_boundary.get(boundary_id),
                                                                   2: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E300405),
                                                                   3: QUALITY_RULE_ERROR_CODE_E300405})
                features.append(new_feature)

        # Duplicate in less
        if errors_duplicate_in_less:
            for error_less in set(errors_duplicate_in_less):
                plot_ring_id = error_less[0]  # plot_ring_id
                plot_id = int(plot_ring_id.split('-')[0]) # plot_id
                boundary_id = error_less[1]  # boundary_id
                geom_ring = dict_inner_rings[plot_ring_id].geometry()
                new_feature = QgsVectorLayerUtils().createFeature(error_layer,
                                                                  geom_ring,
                                                                  {0: dict_uuid_plots.get(plot_id),
                                                                   1: dict_uuid_boundary.get(boundary_id),
                                                                   2: self.quality_rules_manager.get_error_message(QUALITY_RULE_ERROR_CODE_E300403),
                                                                   3: QUALITY_RULE_ERROR_CODE_E300403})
                features.append(new_feature)

        return features

    @staticmethod
    def get_plot_nodes_features_not_covered_by_boundary_points(boundary_point_layer, plot_layer, id_field):
        plot_nodes_layer = GeometryUtils.get_polygon_nodes_layer(plot_layer, id_field)
        return GeometryUtils.get_non_intersecting_geometries(plot_nodes_layer, boundary_point_layer, id_field)
