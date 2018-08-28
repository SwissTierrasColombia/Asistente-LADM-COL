# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-08-10
        git sha              : :%H$
        copyright            : (C) 2018 by Sergio Ramírez (Incige SAS)
        email                : seralra96@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
import copy
from functools import partial

from qgis.core import (QgsEditFormConfig, QgsVectorLayerUtils, Qgis, edit,
                       QgsWkbTypes, QgsMapLayerProxyModel, QgsApplication)
from qgis.gui import QgsMessageBar
from qgis.PyQt.QtCore import Qt, QPoint, QCoreApplication, QSettings
from qgis.PyQt.QtWidgets import (QDialog, QTableWidgetItem, QListWidgetItem,
                                 QSizePolicy, QGridLayout)

from ..utils import get_ui_class
from ..config.general_config import PLUGIN_NAME
from ..config.table_mapping_config import (
    COL_PARTY_TABLE,
    DOMAIN_KEY_FIELD,
    FRACTION_DENOMINATOR_FIELD,
    FRACTION_MEMBER_FIELD,
    FRACTION_NUMERATOR_FIELD,
    FRACTION_TABLE,
    ID_FIELD,
    LA_GROUP_PARTY_NAME_FIELD,
    LA_GROUP_PARTY_GPTYPE_FIELD,
    LA_GROUP_PARTY_TABLE,
    LA_GROUP_PARTY_TYPE_FIELD,
    LA_GROUP_PARTY_TYPE_TABLE,
    LA_GROUP_PARTY_TYPE_VALUE,
    MEMBERS_GROUP_PARTY_FIELD,
    MEMBERS_PARTY_FIELD,
    MEMBERS_TABLE
)
from ..config.help_strings import HelpStrings

DIALOG_UI = get_ui_class('dlg_group_party.ui')

class CreateGroupPartyCadastre(QDialog, DIALOG_UI):
    def __init__(self, iface, db, qgis_utils, parent=None):
        QDialog.__init__(self)
        self.setupUi(self)
        self.iface = iface
        self.log = QgsApplication.messageLog()
        self._la_group_party_table = None
        self._members_table = None
        self._fraction_table = None
        self._col_party_layer = None
        self._db = db
        self.qgis_utils = qgis_utils
        self.help_strings = HelpStrings()

        self.data = {} # {t_id: [display_text, denominator, numerator]}
        self.current_selected_parties = [] #  [t_ids]
        self.parties_to_group = {} # {t_id: [denominator, numerator]}

        # Fill combo of types
        la_group_party_type_table = self.qgis_utils.get_layer(self._db, LA_GROUP_PARTY_TYPE_TABLE, None, True)
        if la_group_party_type_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateGroupPartyCadastreWizard",
                                           "Group Party Type Table couldn't be found... {}").format(self._db.get_description()),
                Qgis.Warning)
            return

        domain_key_index = la_group_party_type_table.fields().indexOf(DOMAIN_KEY_FIELD[self._db.mode])
        domain_keys = list(la_group_party_type_table.uniqueValues(domain_key_index))
        domain_keys.sort()
        self.cbo_group_type.addItems(domain_keys)

        self.txt_search_party.setText("")
        self.btn_select.setEnabled(False)
        self.btn_deselect.setEnabled(False)

        self.tbl_selected_parties.setColumnCount(3)
        self.tbl_selected_parties.setColumnWidth(0, 120)
        self.tbl_selected_parties.setColumnWidth(1, 70)
        self.tbl_selected_parties.setColumnWidth(2, 70)
        self.tbl_selected_parties.sortItems(0, Qt.AscendingOrder)

        self.txt_search_party.textEdited.connect(self.search)
        self.lst_all_parties.itemSelectionChanged.connect(self.selection_changed_all)
        self.tbl_selected_parties.itemSelectionChanged.connect(self.selection_changed_selected)
        self.tbl_selected_parties.cellChanged.connect(self.valueEdited)
        self.btn_select_all.clicked.connect(self.select_all)
        self.btn_deselect_all.clicked.connect(self.deselect_all)
        self.btn_select.clicked.connect(self.select)
        self.btn_deselect.clicked.connect(self.deselect)

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.setLayout(QGridLayout())
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

    def set_parties_data(self, parties_data):
        """
        Initialize parties data.

        :param parties_data: Dictionary {t_id: [display_text, denominator, numerator]}
        :type parties_data: dict
        """
        self.data = parties_data
        self.update_lists()

    def search(self, text):
        self.update_lists(True)

    def selection_changed_all(self):
        self.btn_select.setEnabled(len(self.lst_all_parties.selectedItems()))

    def selection_changed_selected(self):
        self.btn_deselect.setEnabled(len(self.tbl_selected_parties.selectedItems()))

    def select_all(self):
        """
        SLOT. Select all parties listed from left list widget.
        """
        items_ids = []
        for index in range(self.lst_all_parties.count()):
             items_ids.append(self.lst_all_parties.item(index).data(Qt.UserRole))
        self.add_parties_to_selected(items_ids)

    def deselect_all(self):
        """
        SLOT. Remove all parties from left list widget.
        """
        items_ids = []
        for index in range(self.tbl_selected_parties.rowCount()):
             items_ids.append(self.tbl_selected_parties.item(index, 0).data(Qt.UserRole))
        self.remove_parties_from_selected(items_ids)

    def select(self):
        """
        SLOT. Select all parties highlighted in left list widget.
        """
        self.add_parties_to_selected([item.data(Qt.UserRole) for item in self.lst_all_parties.selectedItems()])

    def deselect(self):
        """
        SLOT. Remove all parties highlighted in right list widget.
        """
        self.remove_parties_from_selected([item.data(Qt.UserRole) for item in self.tbl_selected_parties.selectedItems() if item.column() == 0])

    def add_parties_to_selected(self, parties_ids):
        self.current_selected_parties.extend(parties_ids)
        self.update_lists()

    def remove_parties_from_selected(self, parties_ids):
        for party_id in parties_ids:
            self.current_selected_parties.remove(party_id)
            if party_id in self.parties_to_group:
                del self.parties_to_group[party_id]
        self.update_lists()

    def update_lists(self, only_update_all_list=False):
        """
        Update left list widget and optionally the right one.

        :param only_update_all_list: Only updat left list widget.
        :type only_update_all_list: bool
        """
        # All parties
        self.lst_all_parties.clear()
        if self.txt_search_party.text():
            tmp_parties = {i:d for i,d in self.data.items() if self.txt_search_party.text().lower() in d[0].lower()}
        else:
            tmp_parties = copy.deepcopy(self.data) # Copy all!

        for party_id in self.current_selected_parties:
            if party_id in tmp_parties:
                del tmp_parties[party_id]

        for i,d in tmp_parties.items():
            item = QListWidgetItem(d[0])
            item.setData(Qt.UserRole, i)
            self.lst_all_parties.addItem(item)

        if not only_update_all_list:
            # Selected parties
            self.tbl_selected_parties.clearContents()
            self.tbl_selected_parties.setRowCount(len(self.current_selected_parties))
            self.tbl_selected_parties.setColumnCount(3)
            self.tbl_selected_parties.setSortingEnabled(False)

            for row, party_id in enumerate(self.current_selected_parties):
                item = QTableWidgetItem(self.data[party_id][0])
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                item.setData(Qt.UserRole, party_id)
                self.tbl_selected_parties.setItem(row, 0, item)
                value_denominator = self.parties_to_group[party_id][0] if party_id in self.parties_to_group else self.data[party_id][1]
                self.tbl_selected_parties.setItem(row, 1, QTableWidgetItem(str(value_denominator)))
                value_numerator = self.parties_to_group[party_id][1] if party_id in self.parties_to_group else self.data[party_id][2]
                self.tbl_selected_parties.setItem(row, 2, QTableWidgetItem(str(value_numerator)))

            self.tbl_selected_parties.setSortingEnabled(True)


    def valueEdited(self, row, column):
        """
        SLOT. Update either the denominator or the numerator for given row.

        :param row: Edited row
        :type row: int
        :param column: Edited column
        :type column: int
        """
        if column != 0:
            party_id = self.tbl_selected_parties.item(row, 0).data(Qt.UserRole)
            value_denominator = self.tbl_selected_parties.item(row, 1).text()

            # While creating a row and the second column is created, the third
            # one doesn't exist, so use the value already stored for that case
            value_numerator = self.parties_to_group[party_id][1] if party_id in self.parties_to_group else 0
            if self.tbl_selected_parties.item(row, 2) is not None:
                value_numerator = self.tbl_selected_parties.item(row, 2).text()

            self.parties_to_group[party_id] = [value_denominator, value_numerator]

    def accept(self):
        """ Overwrite the dialog's `accept
        <https://doc.qt.io/qt-5/qdialog.html#accept>`_ SLOT to store
        selected parties and numerator-denominator before closing the dialog.
        """
        self.parties_to_group = {}
        for index in range(self.tbl_selected_parties.rowCount()):
             k = self.tbl_selected_parties.item(index, 0).data(Qt.UserRole)
             v_n = int(self.tbl_selected_parties.item(index, 1).text())
             v_d = int(self.tbl_selected_parties.item(index, 2).text())
             self.parties_to_group[ k ] = [v_n, v_d]

        name = self.txt_group_name.text()
        group_party_type = self.cbo_group_type.currentText()
        dict_params = {LA_GROUP_PARTY_NAME_FIELD: name,
                       LA_GROUP_PARTY_GPTYPE_FIELD: group_party_type,
                       'porcentajes': self.parties_to_group}

        validation = self.validate_group_party()

        self.show_message(validation[1], Qgis.Info if validation[0] else Qgis.Warning)

        if not validation[0]:
            return

        self.save_group_party(self._db, [dict_params])

        self.close()

    def validate_group_party(self):
        res = False
        msg = "Aún no estoy listo para continuar"

        return (res, msg)

    def show_message(self, message, level):
        self.bar.pushMessage(message, level, 10)

    def save_group_party(self, db, params):
        """
        Save group party data into associated tables: LA_GROUP_PARTY_TABLE,
        MEMBERS_TABLE and FRACTION_TABLE.

        params: List of dicts, where each dict is an independent group party:
            {
                LA_GROUP_PARTY_NAME_FIELD: '',
                LA_GROUP_PARTY_GPTYPE_FIELD: '',
                'porcentajes': {
                    't_id_miembro': [20, 100], # numerador/denominador
                    't_id_miembro2': [40, 100]
                }
            }
        """
        # Get the required target layers
        res_layers = self.qgis_utils.get_layers(db, {
            LA_GROUP_PARTY_TABLE: {'name': LA_GROUP_PARTY_TABLE, 'geometry': None},
            MEMBERS_TABLE: {'name': MEMBERS_TABLE, 'geometry': None},
            FRACTION_TABLE: {'name': FRACTION_TABLE, 'geometry': None}}, load=True)

        self._la_group_party_table = res_layers[LA_GROUP_PARTY_TABLE]
        if self._la_group_party_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateGroupPartyCadastre",
                                           "Group party table couldn't be found... {}").format(db.get_description()),
                Qgis.Warning)
            return

        self._members_table = res_layers[MEMBERS_TABLE]
        if self._members_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateGroupPartyCadastre",
                                           "Members table couldn't be found... {}").format(db.get_description()),
                Qgis.Warning)
            return

        self._fraction_table = res_layers[FRACTION_TABLE]
        if self._fraction_table is None:
            self.iface.messageBar().pushMessage("Asistente LADM_COL",
                QCoreApplication.translate("CreateGroupPartyCadastre",
                                           "Fraction table couldn't be found... {}").format(db.get_description()),
                Qgis.Warning)
            return

        # Disconnect from previous runs
        try:
            self._la_group_party_table.committedFeaturesAdded.disconnect()
        except TypeError as e:
            pass
        try:
            self._members_table.committedFeaturesAdded.disconnect()
        except TypeError as e:
            pass

        for group in params:
            # Create connections to react when a group party is stored to the DB
            self._la_group_party_table.committedFeaturesAdded.connect(partial(self.finish_group_party_saving, group['porcentajes']))

            # First save the group party
            new_feature = QgsVectorLayerUtils().createFeature(self._la_group_party_table)
            new_feature.setAttribute(LA_GROUP_PARTY_GPTYPE_FIELD, group[LA_GROUP_PARTY_GPTYPE_FIELD])
            new_feature.setAttribute(LA_GROUP_PARTY_NAME_FIELD, group[LA_GROUP_PARTY_NAME_FIELD])
            new_feature.setAttribute(LA_GROUP_PARTY_TYPE_FIELD, LA_GROUP_PARTY_TYPE_VALUE)
            new_feature.setAttribute("p_espacio_de_nombres", 'ABC')
            new_feature.setAttribute("p_local_id", 1)
            new_feature.setAttribute("comienzo_vida_util_version", 'now()')
            self.log.logMessage("Saving Group Party: {}".format(group), PLUGIN_NAME, Qgis.Info)
            with edit(self._la_group_party_table):
                self._la_group_party_table.addFeature(new_feature)

    def finish_group_party_saving(self, members, layer_id, features):
        try:
            self._la_group_party_table.committedFeaturesAdded.disconnect()
        except TypeError as e:
            pass

        if len(features) != 1:
            self.log.logMessage("We should have got only one group party... We cannot do anything with {} group parties".format(len(features)), PLUGIN_NAME, Qgis.Warning)
        else:
            fid = features[0].id()
            if not self._la_group_party_table.getFeature(fid).isValid():
                self.log.logMessage("Feature not found in table Group Party...", PLUGIN_NAME, Qgis.Warning)
            else:
                group_party_id = self._la_group_party_table.getFeature(fid)[ID_FIELD]

                # Now save members
                for party_id, fraction in members.items():
                    # Create connections to react when a group party is stored to the DB
                    self._members_table.committedFeaturesAdded.connect(partial(self.finish_member_saving, fraction))

                    new_feature = QgsVectorLayerUtils().createFeature(self._members_table)
                    new_feature.setAttribute(MEMBERS_GROUP_PARTY_FIELD, group_party_id)
                    new_feature.setAttribute(MEMBERS_PARTY_FIELD, party_id)
                    self.log.logMessage("Saving group party's member ({}: {}).".format(group_party_id, party_id), PLUGIN_NAME, Qgis.Info)
                    with edit(self._members_table):
                        self._members_table.addFeature(new_feature)

    def finish_member_saving(self, fraction, layer_id, features):
        try:
            self._members_table.committedFeaturesAdded.disconnect()
        except TypeError as e:
            pass

        if len(features) != 1:
            self.log.logMessage("We should have got only one member... We cannot do anything with {} members".format(len(features)), PLUGIN_NAME, Qgis.Warning)
        else:
            fid = features[0].id()
            if not self._members_table.getFeature(fid).isValid():
                self.log.logMessage("Feature not found in table Members...", PLUGIN_NAME, Qgis.Warning)
            else:
                member_id = self._members_table.getFeature(fid)[ID_FIELD]

                # And finally save fractions
                new_feature = QgsVectorLayerUtils().createFeature(self._fraction_table)
                new_feature.setAttribute(FRACTION_MEMBER_FIELD, member_id)
                new_feature.setAttribute(FRACTION_NUMERATOR_FIELD, fraction[0])
                new_feature.setAttribute(FRACTION_DENOMINATOR_FIELD, fraction[1])
                with edit(self._fraction_table):
                    self.log.logMessage("Saving member's fraction ({}: {}).".format(member_id, fraction), PLUGIN_NAME, Qgis.Info)
                    self._fraction_table.addFeature(new_feature)

    def show_help(self):
        self.qgis_utils.show_help("group_party")
