# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-08-09
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
from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QMessageBox)
from qgis.core import (Qgis,
                       QgsProject,
                       QgsVectorLayerUtils,
                       QgsWkbTypes)

from ..config.general_config import LAYER
from ..config.table_mapping_config import Names
from ..gui.dialogs.dlg_topological_edition import LayersForTopologicalEditionDialog
from ..utils.geometry import GeometryUtils


class ToolBar(QObject):

    def __init__(self, iface, qgis_utils, db):
        QObject.__init__(self)
        self.iface = iface
        self.qgis_utils = qgis_utils
        self.db = db
        self.geometry = GeometryUtils()
        self.names = Names()

    def build_boundary(self, db):
        QgsProject.instance().setAutoTransaction(False)
        layer = self.qgis_utils.get_layer_from_layer_tree(db, self.names.OP_BOUNDARY_T)
        use_selection = True

        if layer is None:
            self.qgis_utils.message_with_button_load_layer_emitted.emit(
                QCoreApplication.translate("ToolBar", "First load the layer {} into QGIS!").format(self.names.OP_BOUNDARY_T),
                QCoreApplication.translate("ToolBar", "Load layer {} now").format(self.names.OP_BOUNDARY_T), [self.names.OP_BOUNDARY_T, None], Qgis.Warning)
            return
        else:
            if layer.selectedFeatureCount() == 0:
                reply = QMessageBox.question(None,
                                             QCoreApplication.translate("ToolBar", "Continue?"),
                                             QCoreApplication.translate("ToolBar",
                                                                        "There are no selected boundaries, do you like to use all the {} boundaries in the data base?").format(
                                                 layer.featureCount()),
                                             QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    use_selection = False
                else:
                    self.qgis_utils.message_emitted.emit(
                        QCoreApplication.translate("ToolBar", "First select at least one boundary!"),
                        Qgis.Warning)
                    return

        if use_selection:
            new_boundary_geoms, boundaries_to_del_ids = self.geometry.fix_selected_boundaries(layer)
            num_boundaries = layer.selectedFeatureCount()
        else:
            new_boundary_geoms, boundaries_to_del_ids = self.geometry.fix_boundaries(layer)
            num_boundaries = layer.featureCount()

        if len(new_boundary_geoms) > 0:
            layer.startEditing()  # Safe, even if layer is already on editing state

            # the boundaries that are to be replaced are removed
            layer.deleteFeatures(boundaries_to_del_ids)

            # Create features based on segment geometries
            new_fix_boundary_features = list()
            for boundary_geom in new_boundary_geoms:
                feature = QgsVectorLayerUtils().createFeature(layer, boundary_geom)

                # TODO: Remove when local id and working space are defined
                feature.setAttribute(self.names.COL_BFS_T_LOCAL_ID_F, 1)
                feature.setAttribute(self.names.COL_BFS_T_NAMESPACE_F, self.names.OP_BOUNDARY_T)

                new_fix_boundary_features.append(feature)

            layer.addFeatures(new_fix_boundary_features)
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("ToolBar",
                                           "{} feature(s) was(were) analyzed generating {} boundary(ies)!").format(
                    num_boundaries, len(new_fix_boundary_features)),
                Qgis.Info)
            self.iface.mapCanvas().refresh()
        else:
            self.qgis_utils.message_emitted.emit(QCoreApplication.translate("ToolBar", "There are no boundaries to build."), Qgis.Info)

    def enable_topological_editing(self, db):
        # Enable Topological Editing
        QgsProject.instance().setTopologicalEditing(True)

        dlg = LayersForTopologicalEditionDialog()
        if dlg.exec_() == QDialog.Accepted:
            # Load layers selected in the dialog

            layers = dlg.selected_layers_info
            self.qgis_utils.get_layers(db, layers, load=True)
            if not layers:
                return None

            list_layers = list()
            # Open edit session in all layers
            for layer_name, layer_info in layers.items():
                layer = layers[layer_name][LAYER]
                layer.startEditing()
                list_layers.append(layer)

            # Activate "Vertex Tool (All Layers)"
            self.qgis_utils.activate_layer_requested.emit(list_layers[0])
            self.qgis_utils.action_vertex_tool_requested.emit()

            self.qgis_utils.message_with_duration_emitted.emit(
                QCoreApplication.translate("ToolBar",
                                           "You can start moving nodes in layers {} and {}, simultaneously!").format(
                    ", ".join(layer.name() for layer in layers[:-1]), layers[-1].name()),
                Qgis.Info, 30)

    def fill_topology_table_pointbfs(self, db, use_selection=True):
        layers = {
            self.names.OP_BOUNDARY_T: {'name': self.names.OP_BOUNDARY_T, 'geometry': None, LAYER: None},
            self.names.POINT_BFS_T: {'name': self.names.POINT_BFS_T, 'geometry': None, LAYER: None},
            self.names.OP_BOUNDARY_POINT_T: {'name': self.names.OP_BOUNDARY_POINT_T, 'geometry': None, LAYER: None}
        }

        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        if use_selection:
            if layers[self.names.OP_BOUNDARY_T][LAYER].selectedFeatureCount() == 0:
                if self.qgis_utils.get_layer_from_layer_tree(db, self.names.OP_BOUNDARY_T) is None:
                    self.qgis_utils.message_with_button_load_layer_emitted.emit(
                        QCoreApplication.translate("ToolBar",
                                                   "First load the layer {} into QGIS and select at least one boundary!").format(
                            self.names.OP_BOUNDARY_T),
                        QCoreApplication.translate("ToolBar", "Load layer {} now").format(self.names.OP_BOUNDARY_T),
                        [self.names.OP_BOUNDARY_T, None],
                        Qgis.Warning)
                else:
                    reply = QMessageBox.question(None,
                                                 QCoreApplication.translate("ToolBar", "Continue?"),
                                                 QCoreApplication.translate("ToolBar",
                                                                            "There are no selected boundaries, do you like to fill the '{}' table for all the {} boundaries in the data base?")
                                                 .format(self.names.POINT_BFS_T,
                                                         layers[self.names.OP_BOUNDARY_T][LAYER].featureCount()),
                                                 QMessageBox.Yes, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        use_selection = False
                    else:
                        self.qgis_utils.message_emitted.emit(
                            QCoreApplication.translate("ToolBar", "First select at least one boundary!"),
                            Qgis.Warning)
                        return
            else:
                reply = QMessageBox.question(None,
                                             QCoreApplication.translate("ToolBar", "Continue?"),
                                             QCoreApplication.translate("ToolBar",
                                                                        "There are {selected} boundaries selected, do you like to fill the '{table}' table just for the selected boundaries?\n\nIf you say 'No', the '{table}' table will be filled for all boundaries in the database.")
                                             .format(selected=layers[self.names.OP_BOUNDARY_T][LAYER].selectedFeatureCount(),
                                                     table=self.names.POINT_BFS_T),
                                             QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.No:
                    use_selection = False

        bfs_features = layers[self.names.POINT_BFS_T][LAYER].getFeatures()

        # Get unique pairs id_boundary-id_boundary_point
        existing_pairs = [(bfs_feature[self.names.POINT_BFS_T_BOUNDARY_F], bfs_feature[self.names.POINT_BFS_T_OP_BOUNDARY_POINT_F]) for
                          bfs_feature in bfs_features]
        existing_pairs = set(existing_pairs)

        id_pairs = self.geometry.get_pair_boundary_boundary_point(layers[self.names.OP_BOUNDARY_T][LAYER],
                                                                  layers[self.names.OP_BOUNDARY_POINT_T][LAYER],
                                                                  use_selection=use_selection)

        if id_pairs:
            layers[self.names.POINT_BFS_T][LAYER].startEditing()
            features = list()
            for id_pair in id_pairs:
                if not id_pair in existing_pairs:  # Avoid duplicated pairs in the DB
                    # Create feature
                    feature = QgsVectorLayerUtils().createFeature(layers[self.names.POINT_BFS_T][LAYER])
                    feature.setAttribute(self.names.POINT_BFS_T_BOUNDARY_F, id_pair[0])
                    feature.setAttribute(self.names.POINT_BFS_T_OP_BOUNDARY_POINT_F, id_pair[1])
                    features.append(feature)
            layers[self.names.POINT_BFS_T][LAYER].addFeatures(features)
            layers[self.names.POINT_BFS_T][LAYER].commitChanges()
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("ToolBar",
                                           "{} out of {} records were saved into {}! {} out of {} records already existed in the database.").format(
                    len(features),
                    len(id_pairs),
                    self.names.POINT_BFS_T,
                    len(id_pairs) - len(features),
                    len(id_pairs)
                ),
                Qgis.Info)
        else:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("ToolBar", "No pairs id_boundary-id_boundary_point found."),
                Qgis.Info)

    def fill_topology_tables_morebfs_less(self, db, use_selection=True):
        layers = {
            self.names.OP_PLOT_T: {'name': self.names.OP_PLOT_T, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            self.names.MORE_BFS_T: {'name': self.names.MORE_BFS_T, 'geometry': None, LAYER: None},
            self.names.LESS_BFS_T: {'name': self.names.LESS_BFS_T, 'geometry': None, LAYER: None},
            self.names.OP_BOUNDARY_T: {'name': self.names.OP_BOUNDARY_T, 'geometry': None, LAYER: None}
        }

        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        if use_selection:
            if layers[self.names.OP_PLOT_T][LAYER].selectedFeatureCount() == 0:
                if self.qgis_utils.get_layer_from_layer_tree(db, self.names.OP_PLOT_T,
                                                             geometry_type=QgsWkbTypes.PolygonGeometry) is None:
                    self.qgis_utils.message_with_button_load_layer_emitted.emit(
                        QCoreApplication.translate("ToolBar",
                                                   "First load the layer {} into QGIS and select at least one plot!").format(
                            self.names.OP_PLOT_T),
                        QCoreApplication.translate("ToolBar", "Load layer {} now").format(self.names.OP_PLOT_T),
                        [self.names.OP_PLOT_T, None],
                        Qgis.Warning)
                else:
                    reply = QMessageBox.question(None,
                                                 QCoreApplication.translate("ToolBar", "Continue?"),
                                                 QCoreApplication.translate("ToolBar",
                                                                            "There are no selected plots, do you like to fill the '{more}' and '{less}' tables for all the {all} plots in the data base?")
                                                 .format(more=self.names.MORE_BFS_T,
                                                         less=self.names.LESS_BFS_T,
                                                         all=layers[self.names.OP_PLOT_T][LAYER].featureCount()),
                                                 QMessageBox.Yes, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        use_selection = False
                    else:
                        self.qgis_utils.message_emitted.emit(
                            QCoreApplication.translate("ToolBar", "First select at least one plot!"),
                            Qgis.Warning)
                        return
            else:
                reply = QMessageBox.question(None,
                                             QCoreApplication.translate("ToolBar", "Continue?"),
                                             QCoreApplication.translate("ToolBar",
                                                                        "There are {selected} plots selected, do you like to fill the '{more}' and '{less}' tables just for the selected plots?\n\nIf you say 'No', the '{more}' and '{less}' tables will be filled for all plots in the database.")
                                             .format(selected=layers[self.names.OP_PLOT_T][LAYER].selectedFeatureCount(),
                                                     more=self.names.MORE_BFS_T,
                                                     less=self.names.LESS_BFS_T),
                                             QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.No:
                    use_selection = False

        more_bfs_features = layers[self.names.MORE_BFS_T][LAYER].getFeatures()
        less_features = layers[self.names.LESS_BFS_T][LAYER].getFeatures()

        # Get unique pairs id_boundary-id_plot in both tables
        existing_more_pairs = [
            (more_bfs_feature[self.names.MORE_BFS_T_OP_PLOT_F], more_bfs_feature[self.names.MORE_BFS_T_BOUNDARY_F]) for
            more_bfs_feature in more_bfs_features]
        existing_more_pairs = set(existing_more_pairs)
        # Todo: Update LESS_BFS_T_OP_BOUNDARY_F_OP by LESS_BFS_T_OP_BOUNDARY_F.
        # Todo: When an abstract class only implements a concrete class, the name of the attribute is different if two or more classes are implemented.
        existing_less_pairs = [(less_feature[self.names.LESS_BFS_T_OP_PLOT_F], less_feature[self.names.LESS_BFS_T_OP_BOUNDARY_F_OP]) for
                               less_feature in less_features]
        existing_less_pairs = set(existing_less_pairs)

        id_more_pairs, id_less_pairs = self.geometry.get_pair_boundary_plot(layers[self.names.OP_BOUNDARY_T][LAYER],
                                                                            layers[self.names.OP_PLOT_T][LAYER],
                                                                            use_selection=use_selection)
        if id_less_pairs:
            layers[self.names.LESS_BFS_T][LAYER].startEditing()
            features = list()
            for id_pair in id_less_pairs:
                if not id_pair in existing_less_pairs:  # Avoid duplicated pairs in the DB
                    # Create feature
                    feature = QgsVectorLayerUtils().createFeature(layers[self.names.LESS_BFS_T][LAYER])
                    feature.setAttribute(self.names.LESS_BFS_T_OP_PLOT_F, id_pair[0])
                    # Todo: Update LESS_BFS_T_OP_BOUNDARY_F_OP by LESS_BFS_T_OP_BOUNDARY_F.
                    # Todo: When an abstract class only implements a concrete class, the name of the attribute is different if two or more classes are implemented.
                    feature.setAttribute(self.names.LESS_BFS_T_OP_BOUNDARY_F_OP, id_pair[1])
                    features.append(feature)
            layers[self.names.LESS_BFS_T][LAYER].addFeatures(features)
            layers[self.names.LESS_BFS_T][LAYER].commitChanges()
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("ToolBar",
                                           "{} out of {} records were saved into '{}'! {} out of {} records already existed in the database.").format(
                    len(features),
                    len(id_less_pairs),
                    self.names.LESS_BFS_T,
                    len(id_less_pairs) - len(features),
                    len(id_less_pairs)
                ),
                Qgis.Info)
        else:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("ToolBar", "No pairs id_boundary-id_plot found for '{}' table.").format(
                    self.names.LESS_BFS_T),
                Qgis.Info)

        if id_more_pairs:
            layers[self.names.MORE_BFS_T][LAYER].startEditing()
            features = list()
            for id_pair in id_more_pairs:
                if not id_pair in existing_more_pairs:  # Avoid duplicated pairs in the DB
                    # Create feature
                    feature = QgsVectorLayerUtils().createFeature(layers[self.names.MORE_BFS_T][LAYER])
                    feature.setAttribute(self.names.MORE_BFS_T_OP_PLOT_F, id_pair[0])
                    feature.setAttribute(self.names.MORE_BFS_T_BOUNDARY_F, id_pair[1])
                    features.append(feature)
            layers[self.names.MORE_BFS_T][LAYER].addFeatures(features)
            layers[self.names.MORE_BFS_T][LAYER].commitChanges()
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("ToolBar",
                                           "{} out of {} records were saved into '{}'! {} out of {} records already existed in the database.").format(
                    len(features),
                    len(id_more_pairs),
                    self.names.MORE_BFS_T,
                    len(id_more_pairs) - len(features),
                    len(id_more_pairs)
                ),
                Qgis.Info)
        else:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("ToolBar", "No pairs id_boundary-id_plot found for '{}' table.").format(
                    self.names.MORE_BFS_T),
                Qgis.Info)
