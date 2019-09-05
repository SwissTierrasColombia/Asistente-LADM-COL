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
                              QObject,
                              pyqtSignal)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QMessageBox)
from qgis.core import (Qgis,
                       QgsProject,
                       QgsVectorLayerUtils,
                       QgsWkbTypes)

from ..config.general_config import LAYER
from ..config.table_mapping_config import (POINT_BFS_TABLE_BOUNDARY_FIELD,
                                           BFS_TABLE_BOUNDARY_POINT_FIELD,
                                           BOUNDARY_POINT_TABLE,
                                           BOUNDARY_TABLE,
                                           LESS_TABLE,
                                           LESS_TABLE_BOUNDARY_FIELD,
                                           LESS_TABLE_PLOT_FIELD,
                                           MOREBFS_TABLE_PLOT_FIELD,
                                           MOREBFS_TABLE_BOUNDARY_FIELD,
                                           MORE_BOUNDARY_FACE_STRING_TABLE,
                                           PLOT_TABLE,
                                           POINT_BOUNDARY_FACE_STRING_TABLE)
from ..gui.dialogs.dlg_topological_edition import LayersForTopologicalEditionDialog
from ..utils.geometry import GeometryUtils


class ToolBar(QObject):
    wiz_geometry_created_requested = pyqtSignal()

    def __init__(self, iface, qgis_utils, db):
        QObject.__init__(self)
        self.iface = iface
        self.qgis_utils = qgis_utils
        self.db = db
        self.geometry = GeometryUtils()

    def build_boundary(self, db):
        self.turn_transaction_off()
        layer = self.qgis_utils.get_layer_from_layer_tree(db, BOUNDARY_TABLE)
        use_selection = True

        if layer is None:
            self.qgis_utils.message_with_button_load_layer_emitted.emit(
                QCoreApplication.translate("ToolBar", "First load the layer {} into QGIS!").format(BOUNDARY_TABLE),
                QCoreApplication.translate("ToolBar", "Load layer {} now").format(BOUNDARY_TABLE), [BOUNDARY_TABLE, None], Qgis.Warning)
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
            BOUNDARY_TABLE: {'name': BOUNDARY_TABLE, 'geometry': None, LAYER: None},
            POINT_BOUNDARY_FACE_STRING_TABLE: {'name': POINT_BOUNDARY_FACE_STRING_TABLE, 'geometry': None, LAYER: None},
            BOUNDARY_POINT_TABLE: {'name': BOUNDARY_POINT_TABLE, 'geometry': None, LAYER: None}
        }

        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        if use_selection:
            if layers[BOUNDARY_TABLE][LAYER].selectedFeatureCount() == 0:
                if self.qgis_utils.get_layer_from_layer_tree(db, BOUNDARY_TABLE) is None:
                    self.qgis_utils.message_with_button_load_layer_emitted.emit(
                        QCoreApplication.translate("ToolBar",
                                                   "First load the layer {} into QGIS and select at least one boundary!").format(
                            BOUNDARY_TABLE),
                        QCoreApplication.translate("ToolBar", "Load layer {} now").format(BOUNDARY_TABLE),
                        [BOUNDARY_TABLE, None],
                        Qgis.Warning)
                else:
                    reply = QMessageBox.question(None,
                                                 QCoreApplication.translate("ToolBar", "Continue?"),
                                                 QCoreApplication.translate("ToolBar",
                                                                            "There are no selected boundaries, do you like to fill the '{}' table for all the {} boundaries in the data base?")
                                                 .format(POINT_BOUNDARY_FACE_STRING_TABLE,
                                                         layers[BOUNDARY_TABLE][LAYER].featureCount()),
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
                                             .format(selected=layers[BOUNDARY_TABLE][LAYER].selectedFeatureCount(),
                                                     table=POINT_BOUNDARY_FACE_STRING_TABLE),
                                             QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.No:
                    use_selection = False

        bfs_features = layers[POINT_BOUNDARY_FACE_STRING_TABLE][LAYER].getFeatures()

        # Get unique pairs id_boundary-id_boundary_point
        existing_pairs = [(bfs_feature[POINT_BFS_TABLE_BOUNDARY_FIELD], bfs_feature[BFS_TABLE_BOUNDARY_POINT_FIELD]) for
                          bfs_feature in bfs_features]
        existing_pairs = set(existing_pairs)

        id_pairs = self.geometry.get_pair_boundary_boundary_point(layers[BOUNDARY_TABLE][LAYER],
                                                                  layers[BOUNDARY_POINT_TABLE][LAYER],
                                                                  use_selection=use_selection)

        if id_pairs:
            layers[POINT_BOUNDARY_FACE_STRING_TABLE][LAYER].startEditing()
            features = list()
            for id_pair in id_pairs:
                if not id_pair in existing_pairs:  # Avoid duplicated pairs in the DB
                    # Create feature
                    feature = QgsVectorLayerUtils().createFeature(layers[POINT_BOUNDARY_FACE_STRING_TABLE][LAYER])
                    feature.setAttribute(POINT_BFS_TABLE_BOUNDARY_FIELD, id_pair[0])
                    feature.setAttribute(BFS_TABLE_BOUNDARY_POINT_FIELD, id_pair[1])
                    features.append(feature)
            layers[POINT_BOUNDARY_FACE_STRING_TABLE][LAYER].addFeatures(features)
            layers[POINT_BOUNDARY_FACE_STRING_TABLE][LAYER].commitChanges()
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("ToolBar",
                                           "{} out of {} records were saved into {}! {} out of {} records already existed in the database.").format(
                    len(features),
                    len(id_pairs),
                    POINT_BOUNDARY_FACE_STRING_TABLE,
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
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry, LAYER: None},
            MORE_BOUNDARY_FACE_STRING_TABLE: {'name': MORE_BOUNDARY_FACE_STRING_TABLE, 'geometry': None, LAYER: None},
            LESS_TABLE: {'name': LESS_TABLE, 'geometry': None, LAYER: None},
            BOUNDARY_TABLE: {'name': BOUNDARY_TABLE, 'geometry': None, LAYER: None}
        }

        self.qgis_utils.get_layers(db, layers, load=True)
        if not layers:
            return None

        if use_selection:
            if layers[PLOT_TABLE][LAYER].selectedFeatureCount() == 0:
                if self.qgis_utils.get_layer_from_layer_tree(db, PLOT_TABLE,
                                                             geometry_type=QgsWkbTypes.PolygonGeometry) is None:
                    self.qgis_utils.message_with_button_load_layer_emitted.emit(
                        QCoreApplication.translate("ToolBar",
                                                   "First load the layer {} into QGIS and select at least one plot!").format(
                            PLOT_TABLE),
                        QCoreApplication.translate("ToolBar", "Load layer {} now").format(PLOT_TABLE),
                        [PLOT_TABLE, None],
                        Qgis.Warning)
                else:
                    reply = QMessageBox.question(None,
                                                 QCoreApplication.translate("ToolBar", "Continue?"),
                                                 QCoreApplication.translate("ToolBar",
                                                                            "There are no selected plots, do you like to fill the '{more}' and '{less}' tables for all the {all} plots in the data base?")
                                                 .format(more=MORE_BOUNDARY_FACE_STRING_TABLE,
                                                         less=LESS_TABLE,
                                                         all=layers[PLOT_TABLE][LAYER].featureCount()),
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
                                             .format(selected=layers[PLOT_TABLE][LAYER].selectedFeatureCount(),
                                                     more=MORE_BOUNDARY_FACE_STRING_TABLE,
                                                     less=LESS_TABLE),
                                             QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.No:
                    use_selection = False

        more_bfs_features = layers[MORE_BOUNDARY_FACE_STRING_TABLE][LAYER].getFeatures()
        less_features = layers[LESS_TABLE][LAYER].getFeatures()

        # Get unique pairs id_boundary-id_plot in both tables
        existing_more_pairs = [
            (more_bfs_feature[MOREBFS_TABLE_PLOT_FIELD], more_bfs_feature[MOREBFS_TABLE_BOUNDARY_FIELD]) for
            more_bfs_feature in more_bfs_features]
        existing_more_pairs = set(existing_more_pairs)
        existing_less_pairs = [(less_feature[LESS_TABLE_PLOT_FIELD], less_feature[LESS_TABLE_BOUNDARY_FIELD]) for
                               less_feature in less_features]
        existing_less_pairs = set(existing_less_pairs)

        id_more_pairs, id_less_pairs = self.geometry.get_pair_boundary_plot(layers[BOUNDARY_TABLE][LAYER],
                                                                            layers[PLOT_TABLE][LAYER],
                                                                            use_selection=use_selection)
        if id_less_pairs:
            layers[LESS_TABLE][LAYER].startEditing()
            features = list()
            for id_pair in id_less_pairs:
                if not id_pair in existing_less_pairs:  # Avoid duplicated pairs in the DB
                    # Create feature
                    feature = QgsVectorLayerUtils().createFeature(layers[LESS_TABLE][LAYER])
                    feature.setAttribute(LESS_TABLE_PLOT_FIELD, id_pair[0])
                    feature.setAttribute(LESS_TABLE_BOUNDARY_FIELD, id_pair[1])
                    features.append(feature)
            layers[LESS_TABLE][LAYER].addFeatures(features)
            layers[LESS_TABLE][LAYER].commitChanges()
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("ToolBar",
                                           "{} out of {} records were saved into '{}'! {} out of {} records already existed in the database.").format(
                    len(features),
                    len(id_less_pairs),
                    LESS_TABLE,
                    len(id_less_pairs) - len(features),
                    len(id_less_pairs)
                ),
                Qgis.Info)
        else:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("ToolBar", "No pairs id_boundary-id_plot found for '{}' table.").format(
                    LESS_TABLE),
                Qgis.Info)

        if id_more_pairs:
            layers[MORE_BOUNDARY_FACE_STRING_TABLE][LAYER].startEditing()
            features = list()
            for id_pair in id_more_pairs:
                if not id_pair in existing_more_pairs:  # Avoid duplicated pairs in the DB
                    # Create feature
                    feature = QgsVectorLayerUtils().createFeature(layers[MORE_BOUNDARY_FACE_STRING_TABLE][LAYER])
                    feature.setAttribute(MOREBFS_TABLE_PLOT_FIELD, id_pair[0])
                    feature.setAttribute(MOREBFS_TABLE_BOUNDARY_FIELD, id_pair[1])
                    features.append(feature)
            layers[MORE_BOUNDARY_FACE_STRING_TABLE][LAYER].addFeatures(features)
            layers[MORE_BOUNDARY_FACE_STRING_TABLE][LAYER].commitChanges()
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("ToolBar",
                                           "{} out of {} records were saved into '{}'! {} out of {} records already existed in the database.").format(
                    len(features),
                    len(id_more_pairs),
                    MORE_BOUNDARY_FACE_STRING_TABLE,
                    len(id_more_pairs) - len(features),
                    len(id_more_pairs)
                ),
                Qgis.Info)
        else:
            self.qgis_utils.message_emitted.emit(
                QCoreApplication.translate("ToolBar", "No pairs id_boundary-id_plot found for '{}' table.").format(
                    MORE_BOUNDARY_FACE_STRING_TABLE),
                Qgis.Info)

    @staticmethod
    def turn_transaction_off():
        QgsProject.instance().setAutoTransaction(False)
