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
from fractions import Fraction
from functools import partial

from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication)
from qgis.PyQt.QtWidgets import (QDialog,
                                 QTableWidgetItem,
                                 QListWidgetItem,
                                 QSizePolicy)
from qgis.core import (QgsVectorLayerUtils,
                       QgsExpression,
                       QgsExpressionContext,
                       Qgis,
                       edit)
from qgis.gui import QgsMessageBar

from asistente_ladm_col.config.layer_config import LayerConfig
from asistente_ladm_col.config.general_config import LAYER
from asistente_ladm_col.config.help_strings import HelpStrings
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.utils import get_ui_class
from asistente_ladm_col.utils.utils import show_plugin_help
from qgis.core import NULL

DIALOG_UI = get_ui_class('wizards/operation/dlg_group_party.ui')


class CreateGroupPartyOperation(QDialog, DIALOG_UI):
    WIZARD_NAME = "CreateGroupPartyOperationWizard"
    WIZARD_TOOL_NAME = QCoreApplication.translate(WIZARD_NAME, "Create group party")

    def __init__(self, iface, db, qgis_utils, parent=None):
        QDialog.__init__(self)
        self.setupUi(self)
        self.iface = iface
        self._db = db
        self.qgis_utils = qgis_utils
        self.logger = Logger()
        self.names = self._db.names
        self.help_strings = HelpStrings()

        self.data = {} # {t_id: [display_text, denominator, numerator]}
        self.current_selected_parties = [] #  [t_ids]
        self.parties_to_group = {} # {t_id: [denominator, numerator]}

        self._layers = {
            self.names.OP_GROUP_PARTY_T: {'name': self.names.OP_GROUP_PARTY_T, 'geometry': None, LAYER: None},
            self.names.OP_PARTY_T: {'name': self.names.OP_PARTY_T, 'geometry': None, LAYER: None},
            self.names.MEMBERS_T: {'name': self.names.MEMBERS_T, 'geometry': None, LAYER: None},
            self.names.FRACTION_S: {'name': self.names.FRACTION_S, 'geometry': None, LAYER: None},
            self.names.COL_GROUP_PARTY_TYPE_D: {'name': self.names.COL_GROUP_PARTY_TYPE_D, 'geometry': None, LAYER: None}
        }

        # Fill combo of types
        col_group_party_type_table = self.qgis_utils.get_layer(self._db, self.names.COL_GROUP_PARTY_TYPE_D, None, True)
        if not col_group_party_type_table:
            return

        for feature in col_group_party_type_table.getFeatures():
            self.cbo_group_type.addItem(feature[self.names.DISPLAY_NAME_F], feature[self.names.T_ID_F])

        self.txt_search_party.setText("")
        self.btn_select.setEnabled(False)
        self.btn_deselect.setEnabled(False)

        self.tbl_selected_parties.setColumnCount(3)
        self.tbl_selected_parties.setColumnWidth(0, 140)
        self.tbl_selected_parties.setColumnWidth(1, 90)
        self.tbl_selected_parties.setColumnWidth(2, 90)
        self.tbl_selected_parties.sortItems(0, Qt.AscendingOrder)

        self.txt_search_party.textEdited.connect(self.search)
        self.lst_all_parties.itemSelectionChanged.connect(self.selection_changed_all)
        self.tbl_selected_parties.itemSelectionChanged.connect(self.selection_changed_selected)
        self.tbl_selected_parties.cellChanged.connect(self.valueEdited)
        self.btn_select_all.clicked.connect(self.select_all)
        self.btn_deselect_all.clicked.connect(self.deselect_all)
        self.btn_select.clicked.connect(self.select)
        self.btn_deselect.clicked.connect(self.deselect)
        self.buttonBox.helpRequested.connect(self.show_help)

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)
        self.rejected.connect(self.close_wizard)

    def closeEvent(self, e):
        # It's necessary to prevent message bar alert
        pass

    def required_layers_are_available(self):
        layers_are_available = self.qgis_utils.required_layers_are_available(self._db, self._layers, self.WIZARD_TOOL_NAME)
        return layers_are_available

    def load_parties_data(self):
        expression = QgsExpression(LayerConfig.get_dict_display_expressions(self.names)[self.names.OP_PARTY_T])
        context = QgsExpressionContext()
        data = dict()
        for feature in self._layers[self.names.OP_PARTY_T][LAYER].getFeatures():
            context.setFeature(feature)
            expression.prepare(context)
            value = expression.evaluate(context)
            data[feature[self.names.T_ID_F]] = [value if value != NULL else None, 0, 0]
        self.set_parties_data(data)

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

        :param only_update_all_list: Only update left list widget.
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
             try:
                 v_n = int(self.tbl_selected_parties.item(index, 1).text())
             except ValueError as e:
                 self.show_message(QCoreApplication.translate("WizardTranslations",
                    "There are some invalid values in the numerator column. Fix them before continuing..."), Qgis.Warning)
                 return
             try:
                 v_d = int(self.tbl_selected_parties.item(index, 2).text())
             except ValueError as e:
                 self.show_message(QCoreApplication.translate("WizardTranslations",
                    "There are some invalid values in the denominator column. Fix them before continuing..."), Qgis.Warning)
                 return

             self.parties_to_group[k] = [v_n, v_d]

        name = self.txt_group_name.text()
        group_party_type = self.cbo_group_type.itemData(self.cbo_group_type.currentIndex())
        dict_params = {
            self.names.COL_PARTY_T_NAME_F: name,
            self.names.COL_GROUP_PARTY_T_TYPE_F: group_party_type,
            'porcentajes': self.parties_to_group
        }

        res, msg = self.validate_group_party(dict_params)

        if not res:
            self.show_message(msg, Qgis.Warning)
            return

        self.save_group_party(self._db, [dict_params])

    def validate_group_party(self, params):
        name = params[self.names.COL_PARTY_T_NAME_F]
        group_party_type = params[self.names.COL_GROUP_PARTY_T_TYPE_F]
        porcentajes = params['porcentajes']

        if not porcentajes:
            return (False, QCoreApplication.translate("CreateGroupParty",
                    "You need to select some parties to create a group."))
        elif len(porcentajes) == 1:
            return (False, QCoreApplication.translate("CreateGroupParty",
                    "There is just one party, you need to add at least two parties to a group."))

        there_percents = False
        fraction = Fraction()
        for t, nd in porcentajes.items():
            if porcentajes[t] != [0,0]:
                there_percents = True
                break

        if there_percents:
            for t, nd in porcentajes.items():
                if porcentajes[t][1] == 0:
                    return (False, QCoreApplication.translate("CreateGroupParty",
                            "There are denominators equal to zero. You need to change those values."))
                elif porcentajes[t][1] < porcentajes[t][0]:
                    return (False, QCoreApplication.translate("CreateGroupParty",
                            "The denominator cannot be less than the numerator."))
                else:
                    fraction = Fraction(porcentajes[t][0], porcentajes[t][1]) + fraction
            if fraction != 1.0:
                return (False, QCoreApplication.translate("CreateGroupParty",
                        "The sum of the fractions must be equal to one."))

        return (True, QCoreApplication.translate("CreateGroupParty",
                "Validation passed!"))

    def show_message(self, message, level):
        self.bar.clearWidgets()  # Remove previous messages before showing a new one
        self.bar.pushMessage(message, level, 10)

    def save_group_party(self, db, params):
        """
        Save group party data into associated tables: self.names.OP_GROUP_PARTY_T,
        self.names.MEMBERS_T and self.names.FRACTION_S.

        params: List of dicts, where each dict is an independent group party:
            {
                self.names.COL_PARTY_T_NAME_F: '',
                self.names.COL_GROUP_PARTY_T_TYPE_F: '',
                'porcentajes': {
                    't_id_miembro': [20, 100], # numerador/denominador
                    't_id_miembro2': [40, 100]
                }
            }
        """
        # Disconnect from previous runs
        self.disconnect_signals()

        for group in params:
            # Create connections to react when a group party is stored to the DB
            self._layers[self.names.OP_GROUP_PARTY_T][LAYER].committedFeaturesAdded.connect(partial(self.finish_group_party_saving, group['porcentajes']))

            # First save the group party
            new_feature = QgsVectorLayerUtils().createFeature(self._layers[self.names.OP_GROUP_PARTY_T][LAYER])
            new_feature.setAttribute(self.names.COL_GROUP_PARTY_T_TYPE_F, group[self.names.COL_GROUP_PARTY_T_TYPE_F])
            new_feature.setAttribute(self.names.COL_PARTY_T_NAME_F, group[self.names.COL_PARTY_T_NAME_F])

            # TODO: Remove when local id and working space are defined
            new_feature.setAttribute(self.names.OID_T_LOCAL_ID_F, 1)
            new_feature.setAttribute(self.names.OID_T_NAMESPACE_F, self.names.OP_GROUP_PARTY_T)

            # TODO: Gui should allow users to ented namespace, local_id and date values
            #new_feature.setAttribute("p_espacio_de_nombres", self.names.OP_GROUP_PARTY_T)
            #new_feature.setAttribute("p_local_id", '0')
            #new_feature.setAttribute("comienzo_vida_util_version", 'now()')

            self.logger.info(__name__, "Saving Group Party: {}".format(group))
            with edit(self._layers[self.names.OP_GROUP_PARTY_T][LAYER]):
                self._layers[self.names.OP_GROUP_PARTY_T][LAYER].addFeature(new_feature)

    def finish_group_party_saving(self, members, layer_id, features):
        try:
            self._layers[self.names.OP_GROUP_PARTY_T][LAYER].committedFeaturesAdded.disconnect()
        except TypeError as e:
            pass

        message = QCoreApplication.translate("WizardTranslations",
                                             "'{}' tool has been closed because an error occurred while trying to save the data.").format(self.WIZARD_TOOL_NAME)
        if len(features) != 1:
            message = QCoreApplication.translate("WizardTranslations",
                                                 "'{}' tool has been closed. We should have got only one group party... We cannot do anything with {} group parties").format(self.WIZARD_TOOL_NAME, len(features))
            self.logger.warning(__name__, "We should have got only one group party... We cannot do anything with {} group parties".format(len(features)))
        else:
            fid = features[0].id()
            if not self._layers[self.names.OP_GROUP_PARTY_T][LAYER].getFeature(fid).isValid():
                self.logger.warning(__name__, "Feature not found in table Group Party...")
            else:
                group_party_id = self._layers[self.names.OP_GROUP_PARTY_T][LAYER].getFeature(fid)[self.names.T_ID_F]

                # Now save members
                party_ids = list()
                for party_id, fraction in members.items():
                    # Create connections to react when a group party is stored to the DB
                    self._layers[self.names.MEMBERS_T][LAYER].committedFeaturesAdded.connect(partial(self.finish_member_saving, fraction))

                    new_feature = QgsVectorLayerUtils().createFeature(self._layers[self.names.MEMBERS_T][LAYER])
                    new_feature.setAttribute(self.names.MEMBERS_T_GROUP_PARTY_F, group_party_id)
                    new_feature.setAttribute(self.names.MEMBERS_T_PARTY_F, party_id)
                    self.logger.info(__name__, "Saving group party's member ({}: {}).".format(group_party_id, party_id))
                    with edit(self._layers[self.names.MEMBERS_T][LAYER]):
                        self._layers[self.names.MEMBERS_T][LAYER].addFeature(new_feature)
                        party_ids.append(party_id)

                if len(party_ids):
                    message = QCoreApplication.translate("WizardTranslations",
                                                         "The new group party (t_id={}) was successfully created and associated with its corresponding party(ies) (t_id={})!").format(group_party_id, ", ".join([str(b) for b in party_ids]))
                else:
                    message = QCoreApplication.translate("WizardTranslations",
                                                     "The new group party (t_id={}) was successfully created but this one wasn't associated with a party(ies)").format(group_party_id)
        self.close_wizard(message)

    def finish_member_saving(self, fraction, layer_id, features):
        try:
            self._layers[self.names.MEMBERS_T][LAYER].committedFeaturesAdded.disconnect()
        except TypeError as e:
            pass

        if len(features) != 1:
            self.logger.warning(__name__, "We should have got only one member... We cannot do anything with {} members".format(len(features)))
        else:
            fid = features[0].id()
            if not self._layers[self.names.MEMBERS_T][LAYER].getFeature(fid).isValid():
                self.logger.warning(__name__, "Feature not found in table Members...")
            else:
                member_id = self._layers[self.names.MEMBERS_T][LAYER].getFeature(fid)[self.names.T_ID_F]

                if fraction == [0, 0]:
                    return

                # And finally save fractions
                new_feature = QgsVectorLayerUtils().createFeature(self._layers[self.names.FRACTION_S][LAYER])
                new_feature.setAttribute(self.names.FRACTION_S_MEMBER_F, member_id)
                new_feature.setAttribute(self.names.FRACTION_S_NUMERATOR_F, fraction[0])
                new_feature.setAttribute(self.names.FRACTION_S_DENOMINATOR_F, fraction[1])
                with edit(self._layers[self.names.FRACTION_S][LAYER]):
                    self.logger.info(__name__, "Saving member's fraction ({}: {}).".format(member_id, fraction))
                    self._layers[self.names.FRACTION_S][LAYER].addFeature(new_feature)

    def close_wizard(self, message=None, show_message=True):
        if message is None:
            message = QCoreApplication.translate("WizardTranslations", "'{}' tool has been closed.").format(self.WIZARD_TOOL_NAME)
        if show_message:
            self.logger.info_msg(__name__, message)
        self.disconnect_signals()
        self.close()

    def disconnect_signals(self):
        try:
            self._layers[self.names.OP_GROUP_PARTY_T][LAYER].committedFeaturesAdded.disconnect()
        except TypeError as e:
            pass
        try:
            self._layers[self.names.MEMBERS_T][LAYER].committedFeaturesAdded.disconnect()
        except TypeError as e:
            pass

    def show_help(self):
        show_plugin_help("group_party")
