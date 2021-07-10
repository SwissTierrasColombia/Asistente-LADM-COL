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
                              Qt,
                              QObject)
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import (Qgis,
                       QgsProject,
                       QgsExpression,
                       edit,
                       QgsVectorLayerUtils)

from asistente_ladm_col.config.enums import EnumLayerRegistryType
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.geometry import GeometryUtils
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData
from asistente_ladm_col.utils.qt_utils import ProcessWithStatus

import processing


class ToolBar(QObject):

    def __init__(self, iface):
        QObject.__init__(self)
        self.iface = iface
        self.logger = Logger()
        self.app = AppInterface()
        self.geometry = GeometryUtils()

    def build_boundaries(self, db, skip_selection=False):
        """
        Builds the boundaries correctly and update boundary layer

        :param db: db connection instance
        :param skip_selection: Boolean True if we omit the boundaries selected by the user, False if we validate the user's selection.
        :return:
        """
        QgsProject.instance().setAutoTransaction(False)
        use_selection = True

        with ProcessWithStatus(QCoreApplication.translate("ToolBar", "Building boundaries...")):
            layers = {
                db.names.LC_BOUNDARY_T: None,
                db.names.POINT_BFS_T: None,
                db.names.MORE_BFS_T: None,
                db.names.LESS_BFS_T: None
            }
            self.app.core.get_layers(db, layers, load=True)

            if skip_selection:
                layers[db.names.LC_BOUNDARY_T].selectAll()

            if layers[db.names.LC_BOUNDARY_T].selectedFeatureCount() == 0:
                reply = QMessageBox.question(None,
                                             QCoreApplication.translate("ToolBar", "Continue?"),
                                             QCoreApplication.translate("ToolBar",
                                                                        "There are no selected boundaries. Do you want to use all the {} boundaries in the database?").format(
                                                 layers[db.names.LC_BOUNDARY_T].featureCount()),
                                             QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
                if reply == QMessageBox.Yes:
                    use_selection = False
                elif reply == QMessageBox.Cancel:
                    return

            boundary_t_ids = list()
            if use_selection:
                copy_boundary_layer = processing.run("native:saveselectedfeatures",{'INPUT': layers[db.names.LC_BOUNDARY_T], 'OUTPUT': 'memory:'})['OUTPUT']
                boundary_t_ids = QgsVectorLayerUtils.getValues(layers[db.names.LC_BOUNDARY_T], db.names.T_ID_F, selectedOnly=True)[0]
            else:
                copy_boundary_layer = self.app.core.get_layer_copy(layers[db.names.LC_BOUNDARY_T])
                boundary_t_ids = QgsVectorLayerUtils.getValues(layers[db.names.LC_BOUNDARY_T], db.names.T_ID_F)[0]
                layers[db.names.LC_BOUNDARY_T].selectAll()

            boundaries_count = layers[db.names.LC_BOUNDARY_T].featureCount()
            selected_boundaries_count = layers[db.names.LC_BOUNDARY_T].selectedFeatureCount()
            boundary_t_ili_tids = QgsVectorLayerUtils.getValues(layers[db.names.LC_BOUNDARY_T], db.names.T_ILI_TID_F)[0]

            if boundary_t_ids:
                boundary_topology_relation = {
                    db.names.POINT_BFS_T: db.names.POINT_BFS_T_LC_BOUNDARY_F,
                    db.names.MORE_BFS_T: db.names.MORE_BFS_T_LC_BOUNDARY_F,
                    db.names.LESS_BFS_T: db.names.LESS_BFS_T_LC_BOUNDARY_F
                }

                related_topology_features = {
                    db.names.POINT_BFS_T: 0,
                    db.names.MORE_BFS_T: 0,
                    db.names.LESS_BFS_T: 0
                }

                for topology_table_name, topology_boundary_field in boundary_topology_relation.items():
                    select_ids_topology_table = LADMData.get_fids_from_key_values(layers[topology_table_name],
                                                                                  topology_boundary_field,
                                                                                  boundary_t_ids)

                    # Number of related records in each of the topology tables
                    related_topology_features[topology_table_name] = len(select_ids_topology_table)

                    if select_ids_topology_table:
                        with edit(layers[topology_table_name]):
                            # Delete related features in topology tables, because we'll also remove boundaries.
                            # After the whole process is done, we'll recalculate those relationships again.
                            layers[topology_table_name].deleteFeatures(select_ids_topology_table)
                            self.logger.info(__name__, QCoreApplication.translate("ToolBar",
                                                                                  "{} features deleted from table {}!".format(
                                                                                      len(select_ids_topology_table),
                                                                                      topology_table_name)))

                selected_boundaries_layer = processing.run("native:saveselectedfeatures", {'INPUT': layers[db.names.LC_BOUNDARY_T], 'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']
                build_boundaries_layer = self.geometry.build_boundaries(selected_boundaries_layer)

                build_boundaries_count = build_boundaries_layer.featureCount()
                expected_boundaries_count = boundaries_count - selected_boundaries_count + build_boundaries_count

                # Build boundaries should have generated at least one boundary.
                if build_boundaries_count > 0:
                    with edit(layers[db.names.LC_BOUNDARY_T]):
                        # Delete selected features as they will be imported again from a newly created layer after processed
                        layers[db.names.LC_BOUNDARY_T].deleteSelectedFeatures()

                    # Bring back the features we deleted before, but this time, with the boundaries fixed
                    self.app.core.run_etl_model_in_backgroud_mode(db, build_boundaries_layer, db.names.LC_BOUNDARY_T)

                    # check if features were inserted successfully
                    if layers[db.names.LC_BOUNDARY_T].featureCount() == expected_boundaries_count:
                        self.logger.info_msg(__name__, QCoreApplication.translate("ToolBar",
                                                                                  "{} feature(s) was(were) analyzed generating {} boundary(ies)!").format(selected_boundaries_count, build_boundaries_layer.featureCount()))

                    else:
                        if layers[db.names.LC_BOUNDARY_T].featureCount() != boundaries_count - selected_boundaries_count:
                            # Clean layer because wrong data could have been inserted previously
                            expr = "{} NOT IN ('{}')".format(db.names.T_ILI_TID_F, "','".join([t_ili_tid for t_ili_tid in boundary_t_ili_tids]))
                            layers[db.names.LC_BOUNDARY_T].selectByExpression(expr)

                            with edit(layers[db.names.LC_BOUNDARY_T]):
                                layers[db.names.LC_BOUNDARY_T].deleteSelectedFeatures()

                        # the previously deleted boundaries are restored because an error occurred when trying to insert the building boundaries
                        self.app.core.run_etl_model_in_backgroud_mode(db, copy_boundary_layer, db.names.LC_BOUNDARY_T)

                        self.logger.warning_msg(__name__, QCoreApplication.translate("ToolBar",
                                                                                     "An error occurred when trying to build the boundary(ies). No changes are made!"))
                else:
                    self.logger.warning_msg(__name__, QCoreApplication.translate("ToolBar",
                                                                                 "An error occurred when trying to build the boundary(ies). No changes are made!"))

                self.iface.mapCanvas().refresh()

                # topology tables are recalculated with the new boundaries
                if related_topology_features[db.names.POINT_BFS_T]:
                    # it is not possible to use the features selected by the user because they have been removed
                    self.fill_topology_table_pointbfs(db, False)

                if related_topology_features[db.names.MORE_BFS_T] + related_topology_features[db.names.LESS_BFS_T]:
                    # it is not possible to use the features selected by the user because they have been removed
                    self.fill_topology_tables_morebfs_less(db, False)

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
            # Use the same configuration we use in quality rule 3004 (Plots should be covered by boundaries).
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
