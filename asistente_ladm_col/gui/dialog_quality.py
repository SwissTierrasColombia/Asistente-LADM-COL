# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-06-11
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
import os
import collections

from qgis.PyQt.QtCore import Qt, QSettings, QCoreApplication
from qgis.PyQt.QtGui import QBrush, QFont, QIcon, QColor
from qgis.PyQt.QtWidgets import (
    QDialog,
    QTreeWidgetItem,
    QTreeWidgetItemIterator
)
from ..config.general_config import (
    DEFAULT_TOO_LONG_BOUNDARY_SEGMENTS_TOLERANCE
)
from ..config.table_mapping_config import (
    BOUNDARY_POINT_TABLE,
    CONTROL_POINT_TABLE,
    PLOT_TABLE
)
from ..utils import get_ui_class

from ..resources_rc import *

DIALOG_UI = get_ui_class('dlg_quality.ui')

class DialogQuality(QDialog, DIALOG_UI):
    def __init__(self, db, qgis_utils, quality, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self._db = db
        self.qgis_utils = qgis_utils
        self.quality = quality

        too_long_tolerance = int(QSettings().value('Asistente-LADM_COL/quality/too_long_tolerance', DEFAULT_TOO_LONG_BOUNDARY_SEGMENTS_TOLERANCE)) # meters

        self.trw_quality_rules.setItemsExpandable(False)

        # Set connections
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.rejected)
        self.buttonBox.helpRequested.connect(self.show_help)
        self.btn_select_all.clicked.connect(self.select_all)
        self.btn_clear_selection.clicked.connect(self.clear_selection)

        self.items_dict = collections.OrderedDict()
        self.items_dict[QCoreApplication.translate("DialogQuality", "Rules for Points")] = {
                'icon': 'points',
                'rules': [{
                    'id' : 'check_overlaps_in_boundary_points',
                    'text': QCoreApplication.translate("DialogQuality", "Boundary Points should not overlap")
                },{
                    'id' : 'check_overlaps_in_control_points',
                    'text': QCoreApplication.translate("DialogQuality", "Control Points should not overlap")
                },{
                    'id' : 'check_boundary_points_covered_boundaries',
                    'text': QCoreApplication.translate("DialogQuality", "Boundary points must be covered by boundaries")
                }]
            }
        self.items_dict[QCoreApplication.translate("DialogQuality", "Rules for Lines")] = {
                'icon' : 'lines',
                'rules': [{
                    'id': 'check_too_long_boundary_segments',
                    'text': QCoreApplication.translate("DialogQuality", "Boundary segments should not be longer than {}m.").format(too_long_tolerance)
                }, {
                    'id': 'check_overlaps_in_boundaries',
                    'text': QCoreApplication.translate("DialogQuality", "Boundaries should not overlap")
                }, {
                    'id': 'check_boundaries_covered_by_plots',
                    'text': QCoreApplication.translate("DialogQuality", "Boundaries must be covered by plots")
                }, {
                    'id': 'check_missing_boundary_points_in_boundaries',
                    'text': QCoreApplication.translate("DialogQuality", "Boundary nodes should be covered by Boundary Points")
                }, {
                    'id': 'check_dangles_in_boundaries',
                    'text': QCoreApplication.translate("DialogQuality", "Boundaries should not have dangles")
                }]
            }
        self.items_dict[QCoreApplication.translate("DialogQuality", "Rules for Polygons")] = {
                'icon': 'polygons',
                'rules': [{
                    'id': 'check_overlaps_in_plots',
                    'text': QCoreApplication.translate("DialogQuality", "Plots should not overlap")
                }, {
                    'id': 'check_plots_covered_by_boundaries',
                    'text': QCoreApplication.translate("DialogQuality", "Plots must be covered by boundaries")
                }, {
                    'id': 'check_missing_survey_points_in_buildings',
                    'text': QCoreApplication.translate("DialogQuality", "Buildings nodes should be covered by Survey Points")
                }, {
                    'id': 'check_right_of_way_overlaps_buildings',
                    'text': QCoreApplication.translate("DialogQuality", "Right of Way should not overlap Buildings")
                }, {
                    'id': 'check_gaps_in_plots',
                    'text': QCoreApplication.translate("DialogQuality", "Plots should not have gaps")
                }, {
                    'id': 'check_multipart_in_right_of_way',
                    'text': QCoreApplication.translate("DialogQuality", "Right of Way should not have multipart geometries")
                }]
            }

        self.load_items()

    def load_items(self):
        self.trw_quality_rules.setUpdatesEnabled(False) # Don't render until we're ready
        self.trw_quality_rules.clear()

        font = QFont()
        font.setBold(True)

        for group, items in self.items_dict.items():
            children = []
            group_item = QTreeWidgetItem([group])
            group_item.setData(0, Qt.BackgroundRole, QBrush(QColor(219, 219, 219, 255)))
            group_item.setData(0, Qt.FontRole, font)
            icon = QIcon(":/Asistente-LADM_COL/resources/images/{}.png".format(items['icon']))
            group_item.setData(0, Qt.DecorationRole, icon)

            for rule in items['rules']:
                rule_item = QTreeWidgetItem([rule['text']])
                rule_item.setData(0, Qt.UserRole, rule['id'])

                children.append(rule_item)

            group_item.addChildren(children)
            self.trw_quality_rules.addTopLevelItem(group_item)

        # Make group items non selectable and expanded
        for i in range(self.trw_quality_rules.topLevelItemCount()):
            self.trw_quality_rules.topLevelItem(i).setFlags(Qt.ItemIsEnabled) # Not selectable
            self.trw_quality_rules.topLevelItem(i).setExpanded(True)

        self.trw_quality_rules.setUpdatesEnabled(True) # Now render!

    def accepted(self):
        self.qgis_utils.remove_error_group_requested.emit()

        iterator = QTreeWidgetItemIterator(self.trw_quality_rules, QTreeWidgetItemIterator.Selectable)
        while iterator.value():
            item = iterator.value()

            if item.isSelected():
                id = item.data(0, Qt.UserRole)

                if id == 'check_overlaps_in_boundary_points':
                    self.quality.check_overlapping_points(self._db, BOUNDARY_POINT_TABLE)
                elif id == 'check_overlaps_in_control_points':
                    self.quality.check_overlapping_points(self._db, CONTROL_POINT_TABLE)
                elif id == 'check_boundary_points_covered_boundaries':
                    self.quality.check_boundary_points_covered_boundaries(self._db)
                elif id == 'check_too_long_boundary_segments':
                    self.quality.check_too_long_segments(self._db)
                elif id == 'check_overlaps_in_boundaries':
                    self.quality.check_overlaps_in_boundaries(self._db)
                elif id == 'check_boundaries_covered_by_plots':
                    self.quality.check_boundaries_covered_by_plots(self._db)
                elif id == 'check_missing_boundary_points_in_boundaries':
                    self.quality.check_missing_boundary_points_in_boundaries(self._db)
                elif id == 'check_dangles_in_boundaries':
                    self.quality.check_dangles_in_boundaries(self._db)
                elif id == 'check_overlaps_in_plots':
                    self.quality.check_overlapping_polygons(self._db, PLOT_TABLE)
                elif id == 'check_plots_covered_by_boundaries':
                    self.quality.check_plots_covered_by_boundaries(self._db)
                elif id == 'check_missing_survey_points_in_buildings':
                    self.quality.check_missing_survey_points_in_buildings(self._db)
                elif id == 'check_right_of_way_overlaps_buildings':
                    self.quality.check_right_of_way_overlaps_buildings(self._db)
                elif id == 'check_gaps_in_plots':
                    self.quality.check_gaps_in_plots(self._db)
                elif id == 'check_multipart_in_right_of_way':
                    self.quality.check_multiparts_in_right_of_way(self._db)

            iterator += 1

        if self.qgis_utils.error_group_exists():
            self.qgis_utils.set_error_group_visibility(True)

    def rejected(self):
        pass

    def select_all(self):
        self.trw_quality_rules.selectAll()

    def clear_selection(self):
        self.trw_quality_rules.clearSelection()

    def show_help(self):
        self.qgis_utils.show_help("quality_rules")
