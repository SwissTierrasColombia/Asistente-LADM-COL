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
                              QSettings)
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import (Qgis,
                       QgsProject,
                       QgsVectorLayerUtils)

from asistente_ladm_col.config.enums import EnumLayerRegistryType
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.geometry import GeometryUtils


class ToolBar(QObject):

    def __init__(self, iface):
        QObject.__init__(self)
        self.iface = iface
        self.logger = Logger()
        self.app = AppInterface()
        self.geometry = GeometryUtils()

    def build_boundary(self, db):
        QgsProject.instance().setAutoTransaction(False)
        layer = self.app.core.get_ladm_layer_from_qgis(db, db.names.LC_BOUNDARY_T, EnumLayerRegistryType.IN_LAYER_TREE)
        use_selection = True

        if layer is None:
            self.logger.message_with_button_load_layer_emitted.emit(
                QCoreApplication.translate("ToolBar", "First load the layer {} into QGIS!").format(db.names.LC_BOUNDARY_T),
                QCoreApplication.translate("ToolBar", "Load layer {} now").format(db.names.LC_BOUNDARY_T), db.names.LC_BOUNDARY_T, Qgis.Warning)
            return
        else:
            if layer.selectedFeatureCount() == 0:

                reply = QMessageBox.question(None,
                                             QCoreApplication.translate("ToolBar", "Continue?"),
                                             QCoreApplication.translate("ToolBar",
                                                                        "There are no selected boundaries. Do you want to use all the {} boundaries in the database?").format(
                                                 layer.featureCount()),
                                             QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
                if reply == QMessageBox.Yes:
                    use_selection = False
                elif reply == QMessageBox.Cancel:
                    self.logger.warning_msg(__name__, QCoreApplication.translate("ToolBar", "First select at least one boundary!"))
                    return

        if use_selection:
            new_boundary_geoms, boundaries_to_del_ids = self.geometry.fix_selected_boundaries(db.names, layer, db.names.T_ID_F)
            num_boundaries = layer.selectedFeatureCount()
        else:
            new_boundary_geoms, boundaries_to_del_ids = self.geometry.fix_boundaries(layer, db.names.T_ID_F)
            num_boundaries = layer.featureCount()

        if len(new_boundary_geoms) > 0:
            layer.startEditing()  # Safe, even if layer is already on editing state

            # the boundaries that are to be replaced are removed
            layer.deleteFeatures(boundaries_to_del_ids)

            # Create features based on segment geometries
            new_fix_boundary_features = list()
            for boundary_geom in new_boundary_geoms:
                feature = QgsVectorLayerUtils().createFeature(layer, boundary_geom)

                # TODO: Remove when local id and namespace are defined
                feature.setAttribute(db.names.OID_T_LOCAL_ID_F, 1)
                feature.setAttribute(db.names.OID_T_NAMESPACE_F, db.names.LC_BOUNDARY_T)

                new_fix_boundary_features.append(feature)

            layer.addFeatures(new_fix_boundary_features)
            self.logger.info_msg(__name__, QCoreApplication.translate("ToolBar",
                                           "{} feature(s) was(were) analyzed generating {} boundary(ies)!").format(
                    num_boundaries, len(new_fix_boundary_features)))
            self.iface.mapCanvas().refresh()
        else:
            self.logger.info_msg(__name__, QCoreApplication.translate("ToolBar", "There are no boundaries to build."))

    def fill_topology_table_pointbfs(self, db, use_selection=True):
        layers = {
            db.names.LC_BOUNDARY_T: None,
            db.names.POINT_BFS_T: None,
            db.names.LC_BOUNDARY_POINT_T: None
        }

        self.app.core.get_layers(db, layers, load=True)
        if not layers:
            return None

        if use_selection:
            if layers[db.names.LC_BOUNDARY_T].selectedFeatureCount() == 0:
                if self.app.core.get_ladm_layer_from_qgis(db, db.names.LC_BOUNDARY_T, EnumLayerRegistryType.IN_LAYER_TREE) is None:
                    self.logger.message_with_button_load_layer_emitted.emit(
                        QCoreApplication.translate("ToolBar",
                                                   "First load the layer {} into QGIS and select at least one boundary!").format(
                            db.names.LC_BOUNDARY_T),
                        QCoreApplication.translate("ToolBar", "Load layer {} now").format(db.names.LC_BOUNDARY_T),
                        db.names.LC_BOUNDARY_T,
                        Qgis.Warning)
                else:
                    reply = QMessageBox.question(None,
                                                 QCoreApplication.translate("ToolBar", "Continue?"),
                                                 QCoreApplication.translate("ToolBar",
                                                                            "There are no selected boundaries. Do you want to fill the '{}' table for all the {} boundaries in the database?").format(
                                                     db.names.POINT_BFS_T,
                                                     layers[db.names.LC_BOUNDARY_T].featureCount()),
                                                 QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
                    if reply == QMessageBox.Yes:
                        use_selection = False
                    elif reply == QMessageBox.Cancel:
                        self.logger.warning_msg(__name__, QCoreApplication.translate("ToolBar", "First select at least one boundary!"))
                        return
            else:
                reply = QMessageBox.question(None,
                                             QCoreApplication.translate("ToolBar", "Continue?"),
                                             QCoreApplication.translate("ToolBar",
                                                                        "There are {selected} boundaries selected. Do you want to fill the '{table}' table just for the selected boundaries?\n\nIf you say 'No', the '{table}' table will be filled for all boundaries in the database.").format(
                                                 selected=layers[db.names.LC_BOUNDARY_T].selectedFeatureCount(), table=db.names.POINT_BFS_T),
                                             QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
                if reply == QMessageBox.Yes:
                    use_selection = True
                elif reply == QMessageBox.No:
                    use_selection = False
                elif reply == QMessageBox.Cancel:
                    return

        bfs_features = layers[db.names.POINT_BFS_T].getFeatures()

        # Get unique pairs id_boundary-id_boundary_point
        existing_pairs = [(bfs_feature[db.names.POINT_BFS_T_LC_BOUNDARY_F], bfs_feature[db.names.POINT_BFS_T_LC_BOUNDARY_POINT_F]) for
                          bfs_feature in bfs_features]
        existing_pairs = set(existing_pairs)

        tolerance = self.app.settings.tolerance
        id_pairs = self.geometry.get_pair_boundary_boundary_point(layers[db.names.LC_BOUNDARY_T],
                                                                  layers[db.names.LC_BOUNDARY_POINT_T],
                                                                  db.names.T_ID_F,
                                                                  use_selection=use_selection,
                                                                  tolerance=tolerance)

        if id_pairs:
            layers[db.names.POINT_BFS_T].startEditing()
            features = list()
            for id_pair in id_pairs:
                if not id_pair in existing_pairs:  # Avoid duplicated pairs in the DB
                    # Create feature
                    feature = QgsVectorLayerUtils().createFeature(layers[db.names.POINT_BFS_T])
                    feature.setAttribute(db.names.POINT_BFS_T_LC_BOUNDARY_F, id_pair[0])
                    feature.setAttribute(db.names.POINT_BFS_T_LC_BOUNDARY_POINT_F, id_pair[1])
                    features.append(feature)
            layers[db.names.POINT_BFS_T].addFeatures(features)
            layers[db.names.POINT_BFS_T].commitChanges()
            self.logger.info_msg(__name__, QCoreApplication.translate("ToolBar",
                "{} out of {} records were saved into {}! {} out of {} records already existed in the database.").format(
                    len(features),
                    len(id_pairs),
                    db.names.POINT_BFS_T,
                    len(id_pairs) - len(features),
                    len(id_pairs)
                ))
        else:
            self.logger.info_msg(__name__, QCoreApplication.translate("ToolBar",
                                                                      "No pairs id_boundary-id_boundary_point found."))

    def fill_topology_tables_morebfs_less(self, db, use_selection=True):
        layers = {
            db.names.LC_PLOT_T: None,
            db.names.MORE_BFS_T: None,
            db.names.LESS_BFS_T: None,
            db.names.LC_BOUNDARY_T: None
        }

        self.app.core.get_layers(db, layers, load=True)
        if not layers:
            return None

        if use_selection:
            if layers[db.names.LC_PLOT_T].selectedFeatureCount() == 0:
                if self.app.core.get_ladm_layer_from_qgis(db, db.names.LC_PLOT_T, EnumLayerRegistryType.IN_LAYER_TREE) is None:
                    self.logger.message_with_button_load_layer_emitted.emit(
                        QCoreApplication.translate("ToolBar",
                                                   "First load the layer {} into QGIS and select at least one plot!").format(
                            db.names.LC_PLOT_T),
                        QCoreApplication.translate("ToolBar", "Load layer {} now").format(db.names.LC_PLOT_T),
                        db.names.LC_PLOT_T,
                        Qgis.Warning)
                else:
                    reply = QMessageBox.question(None,
                                                 QCoreApplication.translate("ToolBar", "Continue?"),
                                                 QCoreApplication.translate("ToolBar",
                                                                            "There are no selected plots. Do you want to fill the '{more}' and '{less}' tables for all the {all} plots in the database?").format(
                                                     more=db.names.MORE_BFS_T, less=db.names.LESS_BFS_T,
                                                     all=layers[db.names.LC_PLOT_T].featureCount()),
                                                 QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
                    if reply == QMessageBox.Yes:
                        use_selection = False
                    elif reply == QMessageBox.Cancel:
                        self.logger.warning_msg(__name__, QCoreApplication.translate("ToolBar",
                                                                                     "First select at least one plot!"))
                        return
            else:
                reply = QMessageBox.question(None,
                                             QCoreApplication.translate("ToolBar", "Continue?"),
                                             QCoreApplication.translate("ToolBar",
                                                                        "There are {selected} plots selected. Do you want to fill the '{more}' and '{less}' tables just for the selected plots?\n\nIf you say 'No', the '{more}' and '{less}' tables will be filled for all plots in the database.").format(
                                                 selected=layers[db.names.LC_PLOT_T].selectedFeatureCount(),
                                                 more=db.names.MORE_BFS_T, less=db.names.LESS_BFS_T),
                                             QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
                if reply == QMessageBox.Yes:
                    use_selection = True
                elif reply == QMessageBox.No:
                    use_selection = False
                elif reply == QMessageBox.Cancel:
                    return

        tolerance = self.app.settings.tolerance
        if tolerance:
            # We need to adjust input layers to take tolerance into account
            # Use the same configuration we use in quality rule 3004 (Plots should be covereed by boundaries).
            layers[db.names.LC_PLOT_T] = self.app.core.adjust_layer(layers[db.names.LC_PLOT_T],
                                                                    layers[db.names.LC_PLOT_T],
                                                                    tolerance,
                                                                    True,
                                                                    use_selection)
            layers[db.names.LC_BOUNDARY_T] = self.app.core.adjust_layer(layers[db.names.LC_BOUNDARY_T],
                                                                        layers[db.names.LC_PLOT_T],
                                                                        tolerance,
                                                                        True)
            if use_selection:
                layers[db.names.LC_PLOT_T].selectAll()  # Because this layer is already filtered by selected features

        # Get unique pairs id_boundary-id_plot in both tables
        existing_more_pairs = set(
            [(more_bfs_feature[db.names.MORE_BFS_T_LC_PLOT_F], more_bfs_feature[db.names.MORE_BFS_T_LC_BOUNDARY_F]) for
            more_bfs_feature in layers[db.names.MORE_BFS_T].getFeatures()])
        existing_less_pairs = set(
            [(less_feature[db.names.LESS_BFS_T_LC_PLOT_F], less_feature[db.names.LESS_BFS_T_LC_BOUNDARY_F]) for
             less_feature in layers[db.names.LESS_BFS_T].getFeatures()])

        id_more_pairs, id_less_pairs = self.geometry.get_pair_boundary_plot(layers[db.names.LC_BOUNDARY_T],
                                                                            layers[db.names.LC_PLOT_T],
                                                                            db.names.T_ID_F,
                                                                            use_selection=use_selection)
        if id_less_pairs:
            layers[db.names.LESS_BFS_T].startEditing()
            features = list()
            for id_pair in id_less_pairs:
                if not id_pair in existing_less_pairs:  # Avoid duplicated pairs in the DB
                    # Create feature
                    feature = QgsVectorLayerUtils().createFeature(layers[db.names.LESS_BFS_T])
                    feature.setAttribute(db.names.LESS_BFS_T_LC_PLOT_F, id_pair[0])
                    feature.setAttribute(db.names.LESS_BFS_T_LC_BOUNDARY_F, id_pair[1])
                    features.append(feature)
            layers[db.names.LESS_BFS_T].addFeatures(features)
            layers[db.names.LESS_BFS_T].commitChanges()
            self.logger.info_msg(__name__, QCoreApplication.translate("ToolBar",
                "{} out of {} records were saved into '{}'! {} out of {} records already existed in the database.").format(
                    len(features),
                    len(id_less_pairs),
                    db.names.LESS_BFS_T,
                    len(id_less_pairs) - len(features),
                    len(id_less_pairs)
                ))
        else:
            self.logger.info_msg(__name__, QCoreApplication.translate("ToolBar",
                "No pairs id_boundary-id_plot found for '{}' table.").format(db.names.LESS_BFS_T))

        if id_more_pairs:
            layers[db.names.MORE_BFS_T].startEditing()
            features = list()
            for id_pair in id_more_pairs:
                if not id_pair in existing_more_pairs:  # Avoid duplicated pairs in the DB
                    # Create feature
                    feature = QgsVectorLayerUtils().createFeature(layers[db.names.MORE_BFS_T])
                    feature.setAttribute(db.names.MORE_BFS_T_LC_PLOT_F, id_pair[0])
                    feature.setAttribute(db.names.MORE_BFS_T_LC_BOUNDARY_F, id_pair[1])
                    features.append(feature)
            layers[db.names.MORE_BFS_T].addFeatures(features)
            layers[db.names.MORE_BFS_T].commitChanges()
            self.logger.info_msg(__name__, QCoreApplication.translate("ToolBar",
                "{} out of {} records were saved into '{}'! {} out of {} records already existed in the database.").format(
                    len(features),
                    len(id_more_pairs),
                    db.names.MORE_BFS_T,
                    len(id_more_pairs) - len(features),
                    len(id_more_pairs)
                ))
        else:
            self.logger.info_msg(__name__, QCoreApplication.translate("ToolBar",
                "No pairs id_boundary-id_plot found for '{}' table.").format(db.names.MORE_BFS_T))
