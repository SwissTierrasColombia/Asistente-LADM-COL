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
import gc
from math import sqrt

from qgis.PyQt.QtCore import (QCoreApplication,
                              Qt,
                              QObject)
from qgis.PyQt.QtWidgets import (QMessageBox,
                                 QProgressBar)
from qgis.core import (Qgis,
                       QgsProject,
                       QgsWkbTypes,
                       QgsExpression,
                       QgsVectorLayer,
                       QgsGeometry,
                       QgsFeatureRequest,
                       QgsMultiLineString,
                       QgsSpatialIndex,
                       QgsProcessingException,
                       edit,
                       QgsVectorLayerUtils)

from asistente_ladm_col.config.enums import EnumLayerRegistryType
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.processing.custom_processing_feedback import CustomFeedbackWithErrors
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData
from asistente_ladm_col.utils.qt_utils import ProcessWithStatus
from asistente_ladm_col.utils.crs_utils import get_crs_authid

import processing


class ToolBar(QObject):

    def __init__(self, iface):
        QObject.__init__(self)
        self.iface = iface
        self.logger = Logger()
        self.app = AppInterface()

    def show_message_progress_bar(self, msg):
        self.progress_message_bar.setText(msg)
        self.logger.info(__name__, msg)

    def create_progress_bar(self, msg):
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.progress_bar.setFixedWidth(80)
        self.progress_bar.setMaximum(100)
        self.progress_bar_value = 0

        self.app.gui.clear_message_bar()  # Remove previous messages before showing a new one
        self.progress_message_bar = self.iface.messageBar().createMessage("Asistente LADM-COL", msg)
        self.progress_message_bar.layout().addWidget(self.progress_bar)
        self.iface.messageBar().pushWidget(self.progress_message_bar, Qgis.Info)

    def build_boundaries_and_topology_tables(self, db, skip_selection=False):
        """
        It analyzes the boundaries selected by the user and build them correctly.
        If the topology tables (point_bfs, more_bfs and less_bfs) are modified, they are recalculated for the modified boundaries.

        :param db: db connection instance
        :param skip_selection: Boolean True if we omit the boundaries selected by the user, False if we validate the user's selection.
        :return:
        """
        QgsProject.instance().setAutoTransaction(False)
        use_selection = True

        layers = {
            db.names.LC_PLOT_T: None,
            db.names.LC_BOUNDARY_T: None,
            db.names.POINT_BFS_T: None,
            db.names.MORE_BFS_T: None,
            db.names.LESS_BFS_T: None
        }
        self.app.core.get_layers(db, layers, load=True)

        if layers[db.names.LC_BOUNDARY_T].featureCount() == 0:
            self.logger.info_msg(__name__, QCoreApplication.translate("ToolBar", "There are no boundaries to build."))
            return

        if skip_selection:
            # When skip selection we use all boundaries, for that reason the
            # use_selection should be false (it's necessary for the tests)
            use_selection = False
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

        self.create_progress_bar(QCoreApplication.translate("ToolBar", "Building boundaries..."))

        with ProcessWithStatus(QCoreApplication.translate("ToolBar", "Building boundaries...")):
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
            self.set_value_progress_bar(10)

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

                plots_topology_tables = list()
                plot_topology_relation = {
                    db.names.MORE_BFS_T: db.names.MORE_BFS_T_LC_PLOT_F,
                    db.names.LESS_BFS_T: db.names.LESS_BFS_T_LC_PLOT_F
                }

                for topology_table_name, topology_boundary_field in boundary_topology_relation.items():
                    select_ids_topology_table = LADMData.get_fids_from_key_values(layers[topology_table_name],
                                                                                  topology_boundary_field,
                                                                                  boundary_t_ids)

                    # Get plots register in the topology tables (moreBFS and lessBFS)
                    if topology_table_name in (db.names.MORE_BFS_T, db.names.LESS_BFS_T):
                        plots_topology_tables.extend(
                            LADMData.get_t_ids_from_fids(layers[topology_table_name],
                                                         plot_topology_relation[topology_table_name],
                                                         select_ids_topology_table)
                        )

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
                plots_topology_tables = list(set(plots_topology_tables))  # remove duplicate plots

                self.set_value_progress_bar(20)
                selected_boundaries_layer = processing.run("native:saveselectedfeatures", {'INPUT': layers[db.names.LC_BOUNDARY_T], 'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']
                build_boundaries_layer = self.build_boundaries(selected_boundaries_layer)

                build_boundaries_count = build_boundaries_layer.featureCount()
                expected_boundaries_count = boundaries_count - selected_boundaries_count + build_boundaries_count

                # Build boundaries should have generated at least one boundary.
                if build_boundaries_count > 0:
                    with edit(layers[db.names.LC_BOUNDARY_T]):
                        # Delete selected features as they will be imported again from a newly created layer after processed
                        layers[db.names.LC_BOUNDARY_T].deleteSelectedFeatures()

                    # Bring back the features we deleted before, but this time, with the boundaries fixed
                    self.app.core.run_etl_model_in_backgroud_mode_disable_automatic_values_in_batch_mode(db, build_boundaries_layer, db.names.LC_BOUNDARY_T)

                    # check if features were inserted successfully
                    if layers[db.names.LC_BOUNDARY_T].featureCount() == expected_boundaries_count:
                        self._fill_topology_tables(db, layers, build_boundaries_layer, use_selection, related_topology_features, plots_topology_tables)
                        if related_topology_features[db.names.MORE_BFS_T] + related_topology_features[db.names.LESS_BFS_T] + related_topology_features[db.names.POINT_BFS_T]:
                            self.show_message_progress_bar(QCoreApplication.translate("ToolBar",
                                                                                      "{} feature(s) was(were) analyzed generating {} boundary(ies) and the topology tables were updated!").format(selected_boundaries_count, build_boundaries_layer.featureCount()))
                        else:
                            self.show_message_progress_bar(QCoreApplication.translate("ToolBar",
                                                                                      "{} feature(s) was(were) analyzed generating {} boundary(ies)!").format(selected_boundaries_count, build_boundaries_layer.featureCount()))
                    else:
                        if layers[db.names.LC_BOUNDARY_T].featureCount() != boundaries_count - selected_boundaries_count:
                            # Clean layer because wrong data could have been inserted previously
                            expr = "{} NOT IN ('{}')".format(db.names.T_ILI_TID_F, "','".join([t_ili_tid for t_ili_tid in boundary_t_ili_tids]))
                            layers[db.names.LC_BOUNDARY_T].selectByExpression(expr)

                            with edit(layers[db.names.LC_BOUNDARY_T]):
                                layers[db.names.LC_BOUNDARY_T].deleteSelectedFeatures()

                        # the previously deleted boundaries are restored because an error occurred when trying to insert the building boundaries
                        self.app.core.run_etl_model_in_backgroud_mode_disable_automatic_values_in_batch_mode(db, copy_boundary_layer, db.names.LC_BOUNDARY_T)
                        self._fill_topology_tables(db, layers, copy_boundary_layer, use_selection, related_topology_features, plots_topology_tables)
                        self.logger.warning_msg(__name__, QCoreApplication.translate("ToolBar",
                                                                                     "An error occurred when trying to build the boundary(ies). No changes are made!"))
                else:
                    self._fill_topology_tables(db,  layers, copy_boundary_layer, use_selection, related_topology_features, plots_topology_tables)
                    self.logger.warning_msg(__name__, QCoreApplication.translate("ToolBar",
                                                                                 "An error occurred when trying to build the boundary(ies). No changes are made!"))
            else:
                self.show_message_progress_bar(QCoreApplication.translate("ToolBar", "There are no boundaries to build."))
            self.iface.mapCanvas().refresh()
            self.set_value_progress_bar(100)

    def _fill_topology_tables(self, db,  layers, boundary_layer_used, use_selection, related_topology_features, plots_topology_tables):
        """
        Fills the topology tables (PointBFS, MoreBFS and LessBFS) for the affected records,
        if the topology tables are not modified, they are not recalculated.

        :param db: db connection instance
        :param layers:
        :param boundary_layer_used: If an error occurred when build the boundaries we use the original boundaries to
            fill the topology table, if everything went well, we use the build boundaries to fill the topology table.
        :param use_selection: If true, we use the boundaries selected by the user, otherwise all the boundaries registered in the database.
        :param related_topology_features:
        :param plots_topology_tables:
        :return:
        """
        self.iface.mapCanvas().refresh()
        self.set_value_progress_bar(80)

        # topology tables are recalculated
        if related_topology_features[db.names.POINT_BFS_T]:
            if use_selection:
                idx = boundary_layer_used.fields().indexOf(db.names.T_ILI_TID_F)
                exp = "{} in ('{}')".format(db.names.T_ILI_TID_F, "', '".join(boundary_layer_used.uniqueValues(idx)))
                layers[db.names.LC_BOUNDARY_T].selectByExpression(exp)
                self.fill_topology_table_pointbfs(db, True, False)
            else:
                self.fill_topology_table_pointbfs(db, False, False)

        if related_topology_features[db.names.MORE_BFS_T] + related_topology_features[db.names.LESS_BFS_T]:
            if use_selection:
                exp = "{} in ({})".format(db.names.T_ID_F, ", ".join([str(t_id) for t_id in plots_topology_tables]))
                layers[db.names.LC_PLOT_T].selectByExpression(exp)
                self.fill_topology_tables_morebfs_less(db, True, False)
            else:
                self.fill_topology_tables_morebfs_less(db, False, False)

    def set_value_progress_bar(self, progress):
        self.progress_bar_value = int(progress)
        try:
            self.progress_bar.setValue(self.progress_bar_value)
        except RuntimeError:
            pass  # progressBar was deleted

    def build_boundaries_progress_changed(self, progress):
        self.progress_bar_value = int(20 + (progress * 50/100))
        try:
            self.progress_bar.setValue(self.progress_bar_value)
        except RuntimeError:
            pass  # progressBar was deleted

    def build_boundaries(self, boundary_layer):
        """
        creates a boundary layer with well-defined boundaries
        :return: QgsVectorLayer
        """
        feedback = CustomFeedbackWithErrors()
        feedback.progressChanged.connect(self.build_boundaries_progress_changed)

        try:
            params = {'boundaries': boundary_layer, 'native:refactorfields_2:built_boundaries': 'TEMPORARY_OUTPUT'}
            build_boundary_layer = processing.run("model:Build_Boundaries", params, feedback=feedback)['native:refactorfields_2:built_boundaries']
        except QgsProcessingException as e:
            self.logger.warning(__name__, QCoreApplication.translate("ToolBar",
                                                                     "Error running the model to build boundaries. Details: {}".format(feedback.msg)))
            build_boundary_layer = QgsVectorLayer("LineString?crs={}".format(get_crs_authid(boundary_layer.sourceCrs())), "build_boundaries", "memory")

        # For CTM12 the output layer remains without projection. The projection of the input layer is assigned
        if not build_boundary_layer.crs().authid():
            build_boundary_layer.setCrs(boundary_layer.crs())
        return build_boundary_layer

    def fill_topology_table_pointbfs(self, db, use_selection=True, single_call=True):
        """
        Fill the topology table PointBFS.

        Note: This method can be called directly or by the build_boundaries_and_topology_tables method,
        so the state of the progress bar will change depending on the type of call.
        We use the single_call parameter to know how to define how to show the progress bar status.

        :param db: DB Connector object
        :param use_selection: If true, the topology table is filled for the selected boundaries,
                              If false, the topology table is filled for all the boundaries registered in the database.
        :param single_call: If True, This method can be called directly (the progress bar should be created)
                            If False, This method was call by another method (we use existing progress bar)
        :return:
        """
        layers = {
            db.names.LC_BOUNDARY_T: None,
            db.names.POINT_BFS_T: None,
            db.names.LC_BOUNDARY_POINT_T: None
        }

        self.app.core.get_layers(db, layers, load=True)
        if not layers:
            return

        if layers[db.names.LC_BOUNDARY_T].featureCount() == 0 and layers[db.names.LC_BOUNDARY_POINT_T].featureCount() == 0:
            self.logger.info_msg(__name__, QCoreApplication.translate("ToolBar", "There are no boundary points and boundaries to check."))
            return
        elif layers[db.names.LC_BOUNDARY_T].featureCount() == 0:
            self.logger.info_msg(__name__, QCoreApplication.translate("ToolBar", "There are no boundaries to check."))
            return
        elif layers[db.names.LC_BOUNDARY_POINT_T].featureCount() == 0:
            self.logger.info_msg(__name__, QCoreApplication.translate("ToolBar", "There are no boundary points to check."))
            return

        # When fill_topology_table_pointbfs is called by another method it should not ask questions to the user
        if use_selection and single_call:
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

        if single_call:
            self.create_progress_bar(QCoreApplication.translate("ToolBar", 'Fill in topology table PointBFS...'))

        with ProcessWithStatus(QCoreApplication.translate("ToolBar", "Fill in topology table PointBFS...")):
            bfs_features = layers[db.names.POINT_BFS_T].getFeatures()

            # Get unique pairs id_boundary-id_boundary_point
            existing_pairs = [(bfs_feature[db.names.POINT_BFS_T_LC_BOUNDARY_F], bfs_feature[db.names.POINT_BFS_T_LC_BOUNDARY_POINT_F]) for
                              bfs_feature in bfs_features]
            existing_pairs = set(existing_pairs)

            tolerance = self.app.settings.tolerance
            id_pairs = self.get_pair_boundary_boundary_point(layers[db.names.LC_BOUNDARY_T],
                                                             layers[db.names.LC_BOUNDARY_POINT_T],
                                                             db.names.T_ID_F,
                                                             use_selection=use_selection,
                                                             single_call=single_call,
                                                             tolerance=tolerance)

            self.set_value_progress_bar(90) if single_call else self.set_value_progress_bar(85)

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

                self.show_message_progress_bar(QCoreApplication.translate("ToolBar",
                    "{} out of {} records were saved into {}! {} out of {} records already existed in the database.").format(
                        len(features),
                        len(id_pairs),
                        db.names.POINT_BFS_T,
                        len(id_pairs) - len(features),
                        len(id_pairs)
                    ))

            else:
                self.show_message_progress_bar(QCoreApplication.translate("ToolBar",
                                                                          "No pairs id_boundary-id_boundary_point found."))

            if not single_call:
                # The layer selection previously made to call this method is removed.
                layers[db.names.LC_BOUNDARY_T].removeSelection()

            self.set_value_progress_bar(100) if single_call else self.set_value_progress_bar(90)

    def get_pair_boundary_boundary_point(self, boundary_layer, boundary_point_layer, id_field, use_selection=True, single_call=True, tolerance=0):
        id_field_idx = boundary_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
        if use_selection:
            lines = [feature for feature in boundary_layer.getSelectedFeatures(request)]
        else:
            lines = [feature for feature in boundary_layer.getFeatures(request)]

        intersect_pairs = list()

        if boundary_point_layer.featureCount() == 0:
            return intersect_pairs

        id_field_idx = boundary_point_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
        dict_features = {feature.id(): feature for feature in boundary_point_layer.getFeatures(request)}
        index = QgsSpatialIndex(boundary_point_layer)
        candidate_features = None

        tolerance_in_m = tolerance/1000

        line_count = 0
        lines_count = len(lines)

        for line in lines:
            line_count += 1

            if single_call:
                self.set_value_progress_bar(line_count * 80 / lines_count)  # Update progress bar status
            else:
                self.set_value_progress_bar(80 + line_count * 5 / lines_count)

            bbox = line.geometry().boundingBox()
            candidates_ids = index.intersects(bbox.buffered(tolerance_in_m))
            candidate_features = [dict_features[candidate_id] for candidate_id in candidates_ids]
            for candidate_feature in candidate_features:
                candidate_point = candidate_feature.geometry().asPoint()
                for line_vertex in line.geometry().asPolyline():
                    intersects = False
                    if tolerance_in_m:
                        intersects = sqrt((line_vertex.x() - candidate_point.x()) ** 2 +
                                          (line_vertex.y() - candidate_point.y()) ** 2) <= tolerance_in_m
                    else:
                        intersects = (line_vertex.x() == candidate_point.x() and line_vertex.y() == candidate_point.y())

                    if intersects:
                        pair = (line[id_field], candidate_feature[id_field])
                        if pair not in intersect_pairs:
                            intersect_pairs.append(pair)
        # free up memory
        del candidate_features
        del dict_features
        gc.collect()
        return intersect_pairs

    def fill_topology_tables_morebfs_less(self, db, use_selection=True, single_call=True):
        """
        Fill the topology tables MoreBFS and LessBFS.

        Note: This method can be called directly or by the build_boundaries_and_topology_tables method,
        so the state of the progress bar will change depending on the type of call.
        We use the single_call parameter to know how to define how to show the progress bar status.

        :param db: DB Connector object
        :param use_selection: If true, the topologies tables are filled for the selected plots,
                              If false, the topologies tables are filled for all the plots registered in the database.
        :param single_call: If True, This method can be called directly (the progress bar should be created)
                            If False, This method was call by another method (we use existing progress bar)
        :return:
        """
        layers = {
            db.names.LC_PLOT_T: None,
            db.names.MORE_BFS_T: None,
            db.names.LESS_BFS_T: None,
            db.names.LC_BOUNDARY_T: None
        }

        self.app.core.get_layers(db, layers, load=True)
        if not layers:
            return

        if layers[db.names.LC_BOUNDARY_T].featureCount() == 0 and layers[db.names.LC_PLOT_T].featureCount() == 0:
            self.logger.info_msg(__name__, QCoreApplication.translate("ToolBar", "There are no plots and boundaries to check."))
            return
        elif layers[db.names.LC_BOUNDARY_T].featureCount() == 0:
            self.logger.info_msg(__name__, QCoreApplication.translate("ToolBar", "There are no boundaries to check."))
            return
        elif layers[db.names.LC_PLOT_T].featureCount() == 0:
            self.logger.info_msg(__name__, QCoreApplication.translate("ToolBar", "There are no plots to check."))
            return

        # When fill_topology_tables_morebfs_less is called by another method it should not ask questions to the user
        if use_selection and single_call:
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

        if single_call:
            self.create_progress_bar(QCoreApplication.translate("ToolBar", 'Fill in topology tables MoreBFS and LessBFS...'))

        with ProcessWithStatus(QCoreApplication.translate("ToolBar", "Fill in topology tables MoreBFS and LessBFS...")):
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

            self.set_value_progress_bar(10) if single_call else self.set_value_progress_bar(91)
            id_more_pairs, id_less_pairs = self.get_pair_boundary_plot(layers[db.names.LC_BOUNDARY_T],
                                                                       layers[db.names.LC_PLOT_T],
                                                                       db.names.T_ID_F,
                                                                       use_selection=use_selection,
                                                                       single_call=False)

            self.set_value_progress_bar(90) if single_call else self.set_value_progress_bar(97)
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
                self.show_message_progress_bar(QCoreApplication.translate("ToolBar",
                    "{} out of {} records were saved into '{}'! {} out of {} records already existed in the database.").format(
                        len(features),
                        len(id_less_pairs),
                        db.names.LESS_BFS_T,
                        len(id_less_pairs) - len(features),
                        len(id_less_pairs)
                    ))
            else:
                self.show_message_progress_bar(QCoreApplication.translate("ToolBar",
                    "No pairs id_boundary-id_plot found for '{}' table.").format(db.names.LESS_BFS_T))

            self.set_value_progress_bar(95) if single_call else self.set_value_progress_bar(98)
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
                self.show_message_progress_bar(QCoreApplication.translate("ToolBar",
                    "{} out of {} records were saved into '{}'! {} out of {} records already existed in the database.").format(
                        len(features),
                        len(id_more_pairs),
                        db.names.MORE_BFS_T,
                        len(id_more_pairs) - len(features),
                        len(id_more_pairs)
                    ))
            else:
                self.show_message_progress_bar(QCoreApplication.translate("ToolBar",
                    "No pairs id_boundary-id_plot found for '{}' table.").format(db.names.MORE_BFS_T))

        if not single_call:
            # The layer selection previously made to call this method is removed.
            layers[db.names.LC_PLOT_T].removeSelection()
        self.set_value_progress_bar(100) if single_call else self.set_value_progress_bar(99)

    def get_pair_boundary_plot(self, boundary_layer, plot_layer, id_field, use_selection=True, single_call=True):
        id_field_idx = plot_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
        if use_selection:
            polygons = [feature for feature in plot_layer.getSelectedFeatures(request)]
        else:
            polygons = [feature for feature in plot_layer.getFeatures(request)]

        intersect_more_pairs = list()
        intersect_less_pairs = list()

        if boundary_layer.featureCount() == 0:
            return intersect_more_pairs, intersect_less_pairs

        id_field_idx = boundary_layer.fields().indexFromName(id_field)
        request = QgsFeatureRequest().setSubsetOfAttributes([id_field_idx])
        dict_features = {feature.id(): feature for feature in boundary_layer.getFeatures(request)}
        index = QgsSpatialIndex(boundary_layer)
        candidate_features = None

        polygon_count = 0
        polygons_count = len(polygons)

        for polygon in polygons:
            polygon_count += 1

            if single_call:
                self.set_value_progress_bar(10 + polygon_count * 80 / polygons_count)  # Update progress bar status
            else:
                self.set_value_progress_bar(91 + polygon_count * 5 / polygons_count)

            bbox = polygon.geometry().boundingBox()
            bbox.scale(1.001)
            candidates_ids = index.intersects(bbox)

            candidate_features = [dict_features[candidate_id] for candidate_id in candidates_ids]

            for candidate_feature in candidate_features:
                polygon_geom = polygon.geometry()
                is_multipart = polygon_geom.isMultipart()
                candidate_geometry = candidate_feature.geometry()

                if polygon_geom.intersects(candidate_geometry):
                    # Does the current multipolygon have inner rings?
                    has_inner_rings = False
                    multi_polygon = None
                    single_polygon = None

                    if is_multipart:
                        multi_polygon = polygon_geom.constGet()
                        for part in range(multi_polygon.numGeometries()):
                            if multi_polygon.ringCount(part) > 1:
                                has_inner_rings = True
                                break
                    else:
                        single_polygon = polygon_geom.constGet()
                        if single_polygon.numInteriorRings() > 0:
                            has_inner_rings = True

                    # Now we'll test intersections against borders
                    if has_inner_rings:
                        # In this case we need to identify whether the
                        # intersection is with outer rings (goes to MOREBFS
                        # table) or with inner rings (goes to LESS table)
                        multi_outer_rings = QgsMultiLineString()
                        multi_inner_rings = QgsMultiLineString()

                        if is_multipart and multi_polygon:
                            for i in range(multi_polygon.numGeometries()):
                                temp_polygon = multi_polygon.geometryN(i)
                                multi_outer_rings.addGeometry(temp_polygon.exteriorRing().clone())
                                for j in range(temp_polygon.numInteriorRings()):
                                    multi_inner_rings.addGeometry(temp_polygon.interiorRing(j).clone())

                        elif not is_multipart and single_polygon:
                            multi_outer_rings.addGeometry(single_polygon.exteriorRing().clone())
                            for j in range(single_polygon.numInteriorRings()):
                                multi_inner_rings.addGeometry(single_polygon.interiorRing(j).clone())

                        outer_intersection = QgsGeometry(multi_outer_rings).intersection(candidate_geometry)
                        if not outer_intersection.isEmpty():
                            intersection_type = outer_intersection.type()
                            if intersection_type == QgsWkbTypes.LineGeometry:
                                intersect_more_pairs.append((polygon[id_field], candidate_feature[id_field]))
                            else:
                                self.logger.warning(__name__,
                                    "(MoreBFS) Intersection between plot (t_id={}) and boundary (t_id={}) is a geometry of type: {}".format(
                                        polygon[id_field],
                                        candidate_feature[id_field],
                                        intersection_type))

                        inner_intersection = QgsGeometry(multi_inner_rings).intersection(candidate_geometry)
                        if not inner_intersection.isEmpty():
                            intersection_type = inner_intersection.type()
                            if intersection_type == QgsWkbTypes.LineGeometry:
                                intersect_less_pairs.append((polygon[id_field], candidate_feature[id_field]))
                            else:
                                self.logger.warning(__name__,
                                    "(Less) Intersection between plot (t_id={}) and boundary (t_id={}) is a geometry of type: {}".format(
                                        polygon[id_field],
                                        candidate_feature[id_field],
                                        intersection_type))

                    else:
                        boundary = None
                        if is_multipart and multi_polygon:
                            boundary = multi_polygon.boundary()
                        elif not is_multipart and single_polygon:
                            boundary = single_polygon.boundary()

                        simple_intersection = QgsGeometry(boundary).intersection(candidate_geometry)
                        if not simple_intersection.isEmpty():
                            intersection_type = simple_intersection.type()
                            if boundary and intersection_type == QgsWkbTypes.LineGeometry:
                                intersect_more_pairs.append((polygon[id_field], candidate_feature[id_field]))
                            else:
                                self.logger.warning(__name__,
                                    "(MoreBFS) Intersection between plot (t_id={}) and boundary (t_id={}) is a geometry of type: {}".format(
                                        polygon[id_field],
                                        candidate_feature[id_field],
                                        intersection_type))
        # free up memory
        del candidate_features
        del dict_features
        gc.collect()
        return intersect_more_pairs, intersect_less_pairs