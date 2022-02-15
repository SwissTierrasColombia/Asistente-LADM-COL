"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2022-01-13
        copyright       : (C) 2022 by Germán Carrillo (SwissTierras Colombia)
        email           : gcarrillo@linuxmail.org
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
import json

from qgis.PyQt.QtCore import (QCoreApplication,
                              pyqtSignal,
                              QSettings,
                              QObject)
from qgis.core import (QgsVectorLayer,
                       QgsRectangle)

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.enums import EnumQualityRulePanelMode
from asistente_ladm_col.config.general_config import DEFAULT_USE_ROADS_VALUE
from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.config.quality_rule_config import QR_IGACR3006
from asistente_ladm_col.config.translation_strings import TranslatableConfigStrings
from asistente_ladm_col.core.quality_rules.quality_rule_engine import (QualityRuleEngine,
                                                                       QualityRuleResultLog)
from asistente_ladm_col.core.quality_rules.quality_rule_registry import QualityRuleRegistry
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData
from asistente_ladm_col.utils.quality_error_db_utils import QualityErrorDBUtils
from asistente_ladm_col.utils.qt_utils import normalize_local_url


class QualityRuleController(QObject):

    open_report_called = pyqtSignal(QualityRuleResultLog)  # log result
    quality_rule_layer_removed = pyqtSignal()
    refresh_error_layer_symbology = pyqtSignal(QgsVectorLayer)
    total_progress_changed = pyqtSignal(int)  # Progress value

    def __init__(self, db):
        QObject.__init__(self)
        self.app = AppInterface()
        self.logger = Logger()
        self.__db = db

        self.__tr_dict = TranslatableConfigStrings().get_translatable_config_strings()

        # Hierarquical dict of qrs and qr groups
        self.__qrs_tree_data = dict()  # {type: {qr_key1: qr_obj1, ...}, ...}

        # Hierarquical dict of qrs and qr groups with general results
        self.__general_results_tree_data = dict()  # {type: {qr_obj1: qr_results1, ...}, ...}

        # Hierarchical dict of qrs and their corresponding error instances
        # feature1: {uuids, rel_uuids, error_type, nombre_ili_obj, details, values, fixed, exception, geom_fks}
        self.__error_results_data = dict()  # {qr_key1: {t_id1: feature1}}

        self.__qr_results_dir_path = ''  # Dir path where results will be stored
        self.__selected_qrs = list()  # QRs to be validated (at least 1)
        self.__selected_qr = None  # QR selected by the user to show its corresponding errors (exactly 1)

        self.__qr_engine = None  # Once set, we can reuse it
        self.__qrs_results = None  # QualityRulesExecutionResult object

        # To cache layers from QR DB
        self.__error_layer = None
        self.__point_layer = None
        self.__line_layer = None
        self.__polygon_layer = None

        # Cache by t_id (built on demand): {t_id1: 'Error', t_id2: 'Corregido', t_id3: 'Exception'}
        self.__error_state_dict = dict()

    def get_tr_string(self, key):
        return self.__tr_dict.get(key, key)

    def validate_qrs(self):
        if self.__qr_engine is None:
            self.__qr_engine = QualityRuleEngine(self.__db,
                                                 self.__selected_qrs,
                                                 self.app.settings.tolerance,
                                                 self.__qr_results_dir_path)
            self.__qr_engine.progress_changed.connect(self.total_progress_changed)
        else:
            self.__qr_engine.initialize(self.__db,
                                        self.__selected_qrs,
                                        self.app.settings.tolerance,
                                        self.__qr_results_dir_path)
        #self.__qr_engine.qr_logger.show_message_emitted.connect(self.show_log_quality_message)
        #self.__qr_engine.qr_logger.show_button_emitted.connect(self.show_log_quality_button)
        #self.__qr_engine.qr_logger.set_initial_progress_emitted.connect(self.set_log_quality_initial_progress)
        #self.__qr_engine.qr_logger.set_final_progress_emitted.connect(self.set_log_quality_final_progress)

        use_roads = bool(QSettings().value('Asistente-LADM-COL/quality/use_roads', DEFAULT_USE_ROADS_VALUE, bool))
        options = {QR_IGACR3006: {'use_roads': use_roads}}

        res, msg, qrs_res = self.__qr_engine.validate_quality_rules(options)
        if not res:
            return res, msg, None

        self.__qrs_results = qrs_res

        self.__connect_layer_willbedeleted_signals()  # Note: Call it after validate_quality_rules!

        res_u, msg_u, output_qr_dir = QualityErrorDBUtils.get_quality_validation_output_path(self.__qr_results_dir_path,
                                                                                             self.__qr_engine.get_timestamp())

        if len(self.__selected_qrs) == 1:
            pre_text = QCoreApplication.translate("QualityRules", "The quality rule was checked!")
        else:
            pre_text = QCoreApplication.translate("QualityRules", "All the {} quality rules were checked!").format(len(self.__selected_qrs))

        post_text = QCoreApplication.translate("QualityRules",
                                               "Both a PDF report and a GeoPackage database with errors can be found in <a href='file:///{}'>{}</a>.").format(
            normalize_local_url(output_qr_dir),
            output_qr_dir)

        self.logger.success_msg(__name__, "{} {}".format(pre_text, post_text))

        self.__emit_refresh_error_layer_symbology()

        return res, msg, self.__qrs_results

    def __connect_layer_willbedeleted_signals(self):
        """
        Iterate QR DB layers from the layer tree and connect their layerwillberemoved signals.
        If a QR DB layer is removed, we'll react in the GUI.
        """
        group = QualityErrorDBUtils.get_quality_error_group(self.__qr_engine.get_timestamp())

        if group:
            for tree_layer in group.findLayers():
                try:
                    tree_layer.layer().willBeDeleted.disconnect(self.quality_rule_layer_removed)
                except:
                    pass
                tree_layer.layer().willBeDeleted.connect(self.quality_rule_layer_removed)

    def disconnect_layer_willberemoved_signals(self):
        group = QualityErrorDBUtils.get_quality_error_group(self.__qr_engine.get_timestamp(), False)

        if group:
            for tree_layer in group.findLayers():
                try:
                    tree_layer.layer().willBeDeleted.disconnect(self.quality_rule_layer_removed)
                except:
                    pass

    def get_qr_result(self, qr_key):
        """
        Return the QRExecutionResult object for the given qr_key.

        It first attempts to find it in the __qrs_results dict, but, chances are,
        the whole set of QRs hasn't been validated when this method is called,
        so, as a last resort, we go for the tree_data, which is updated each time
        a QR gets its result.
        """
        if self.__qrs_results is not None:
            return self.__qrs_results.result(qr_key)

        for type, qr_dict in self.__general_results_tree_data.items():
            for k, v in qr_dict.items():
                if k.id() == qr_key:
                    return self.__general_results_tree_data[type][k]

        return None

    def __reset_qrs_results(self):
        # To be used when we are returning to select QRs (i.e., to the initial panel)
        self.__qrs_results = None

    def __get_qrs_per_role_and_models(self):
        return QualityRuleRegistry().get_qrs_per_role_and_models(self.__db)

    def load_tree_data(self, mode):
        """
        Builds a hierarchical dict by qr type: {qr_type1: {qr_key1: qr_obj1, ...}, ...}

        Tree data for panel 1.

        :params mode: Value from EnumQualityRulePanelMode (either VALIDATE or READ).
                      For VALIDATE we load QRs from registry (filtered by role and current db models).
                      For READ we load QRs from the DB itself.
        """
        if mode == EnumQualityRulePanelMode.VALIDATE:
            qrs = self.__get_qrs_per_role_and_models()  # Dict of qr key and qr objects.
        else:
            qrs =  dict()  # TODO: Read QRs from the QR DB

        for qr_key, qr_obj in qrs.items():
            type = qr_obj.type()
            if type not in self.__qrs_tree_data:
                self.__qrs_tree_data[type] = {qr_key: qr_obj}
            else:
                self.__qrs_tree_data[type][qr_key] = qr_obj

    def get_qrs_tree_data(self):
        return self.__qrs_tree_data

    def set_qr_dir_path(self, path):
        self.__qr_results_dir_path = path

    def set_selected_qrs(self, selected_qrs):
        # We sort them because the engine needs the QRs sorted for the PDF report
        for type, qr_dict in self.__qrs_tree_data.items():
            for qr_key, qr_obj in qr_dict.items():
                if qr_key in selected_qrs:
                    self.__selected_qrs.append(qr_key)

    def get_selected_qrs(self):
        return self.__selected_qrs

    def __reset_selected_qrs(self):
        # To be used when we are returning to select QRs (i.e., to the initial panel)
        self.__selected_qrs = list()

    def reset_vars_for_general_results_panel(self):
        # Initialize variables when we leave the general results panel
        self.__reset_general_results_tree_data()
        self.__reset_selected_qrs()
        self.__reset_qrs_results()
        self.__reset_layers()

        # Call it before removing QR DB group to avoid triggering parent.layer_removed() slot again.
        self.disconnect_layer_willberemoved_signals()

        # When we leave the GRP, we remove the QR DB group from layer tree,
        # because we won't be working anymore with that QR DB
        QualityErrorDBUtils.remove_quality_error_group(self.__qr_engine.get_timestamp())

    def reset_vars_for_error_results_panel(self):
        # Initialize variables when we leave the error results panel
        self.__reset_error_results_data()
        self.__reset_selected_qr()
        self.__reset_error_state_dict()
        self.__reset_layers()

    def load_general_results_tree_data(self):
        """
        Builds a hierarchical dict by qr type: {type: {qr_obj1: qr_results1, ...}, ...}

        Tree data for panel 2.
        """
        for type, qr_dict in self.__qrs_tree_data.items():
            for qr_key, qr_obj in qr_dict.items():
                if qr_key in self.__selected_qrs:
                    if type not in self.__general_results_tree_data:
                        self.__general_results_tree_data[type] = {qr_obj: None}
                    else:
                        self.__general_results_tree_data[type][qr_obj] = None

    def get_general_results_tree_data(self):
        return self.__general_results_tree_data

    def __reset_general_results_tree_data(self):
        # To be used when we are returning to select QRs (i.e., to the initial panel)
        self.__general_results_tree_data = dict()

    def set_qr_validation_result(self, qr, qr_result):
        """
        When a QR has its validation result after validation,
        we can store it in our custom dict by using this method.
        """
        for type, qr_dict in self.__general_results_tree_data.items():
            for k, v in qr_dict.items():
                if k == qr:
                    self.__general_results_tree_data[type][k] = qr_result

    def open_report(self):
        if self.__qr_engine:
            log_result = self.__qr_engine.qr_logger.get_log_result()
            self.open_report_called.emit(log_result)

    def set_selected_qr(self, qr_key):
        self.__selected_qr = QualityRuleRegistry().get_quality_rule(qr_key)
        return self.__selected_qr is not None  # We should not be able to continue if we don't find the QR

    def get_selected_qr(self):
        return self.__selected_qr

    def load_error_results_data(self):
        """
        Go to table and bring data to the dict.
        We should keep this dict updated with changes from the user.
        From time to time we reflect this dict changes in the original data source.
        """
        db = self.__qr_engine.get_db_quality()
        names = db.names

        layers = {names.ERR_QUALITY_ERROR_T: None,  names.ERR_RULE_TYPE_T: None}
        self.app.core.get_layers(db, layers, load=False)
        if not layers:
            self.logger.critical(__name__, "Quality error layers ('{}') not found!".format(",".join(list(layers.keys()))))
            return

        # First go for the selected quality error's t_id
        features = LADMData.get_features_from_t_ids(layers[names.ERR_RULE_TYPE_T],
                                                    names.ERR_RULE_TYPE_T_CODE_F,
                                                    [self.__selected_qr.id()])
        t_id = features[0][names.T_ID_F] if features else None
        if not t_id:
            self.logger.critical(__name__, "Quality error rule ('{}') not found!".format(self.__selected_qr.id()))
            return

        # Now go for all features that match the selected quality rule
        features = LADMData.get_features_from_t_ids(layers[names.ERR_QUALITY_ERROR_T],
                                                    names.ERR_QUALITY_ERROR_T_RULE_TYPE_F,
                                                    [t_id])

        self.__error_results_data[self.__selected_qr.id()] = {feature[names.T_ID_F]: feature for feature in features}

    def get_error_results_data(self):
        # Get the subdict {t_id1: feature1, ...} corresponding to selected qr
        return self.__error_results_data.get(self.__selected_qr.id() if self.__selected_qr else '', dict())

    def __reset_error_results_data(self):
        # To be used when we are returning to select QR results (i.e., to the general results panel)
        self.__error_results_data = dict()

    def error_t_id(self, feature):
        return feature[self.__qr_engine.get_db_quality().names.T_ID_F]

    def is_fixed_error(self, feature):
        db = self.__qr_engine.get_db_quality()
        state_t_id = feature[db.names.ERR_QUALITY_ERROR_T_ERROR_STATE_F]
        return self.__get_error_state_value(state_t_id) == LADMNames.ERR_ERROR_STATE_D_FIXED_V

    def is_error(self, feature):
        db = self.__qr_engine.get_db_quality()
        state_t_id = feature[db.names.ERR_QUALITY_ERROR_T_ERROR_STATE_F]
        return self.__get_error_state_value(state_t_id) == LADMNames.ERR_ERROR_STATE_D_ERROR_V

    def is_exception(self, feature):
        db = self.__qr_engine.get_db_quality()
        state_t_id = feature[db.names.ERR_QUALITY_ERROR_T_ERROR_STATE_F]
        return self.__get_error_state_value(state_t_id) == LADMNames.ERR_ERROR_STATE_D_EXCEPTION_V

    def uuid_objs(self, feature):
        return "\n".join(feature[self.__qr_engine.get_db_quality().names.ERR_QUALITY_ERROR_T_OBJECT_IDS_F])

    def ili_obj_name(self, feature):
        ili_name = feature[self.__qr_engine.get_db_quality().names.ERR_QUALITY_ERROR_T_ILI_NAME_F]
        return ili_name.split(".")[-1] if ili_name else ''

    def error_type_code_and_display(self, feature):
        db = self.__qr_engine.get_db_quality()
        names = db.names
        layer = self.app.core.get_layer(db, names.ERR_ERROR_TYPE_T, load=False)
        features = LADMData.get_features_from_t_ids(layer,
                                                    names.T_ID_F,
                                                    [feature[db.names.ERR_QUALITY_ERROR_T_ERROR_TYPE_F]])  # tid

        return features[0][names.ERR_ERROR_TYPE_T_CODE_F] if features else QCoreApplication.translate(
            "QualityRules", "No error type found!"), features[0][
                   names.ERR_ERROR_TYPE_T_DESCRIPTION_F] if features else QCoreApplication.translate(
            "QualityRules", "No error description found!")

    def error_details_and_values(self, feature):
        res = ""
        db = self.__qr_engine.get_db_quality()
        details = feature[db.names.ERR_QUALITY_ERROR_T_DETAILS_F]
        values = feature[db.names.ERR_QUALITY_ERROR_T_VALUES_F]

        if details:
            res = details
        if values:
            try:
                res_values = json.loads(values)
                if type(res_values) is dict:
                    items = ""
                    for k, v in res_values.items():
                        items = res + "{}: {}\n".format(k, v)

                    res_values = items.strip()
                else:
                    res_values = str(res_values)
            except json.decoder.JSONDecodeError as e:
                res_values = values

            res = res_values if not res else "{}\n\n{}".format(res, res_values)

        return res

    def error_state(self, feature):
        db = self.__qr_engine.get_db_quality()
        state_t_id = feature[db.names.ERR_QUALITY_ERROR_T_ERROR_STATE_F]
        return self.__get_error_state_value(state_t_id)

    def __get_error_state_value(self, state_t_id):
        if state_t_id not in self.__error_state_dict:
            db = self.__qr_engine.get_db_quality()
            self.__error_state_dict[state_t_id] = LADMData().get_domain_value_from_code(db,
                                                                                        db.names.ERR_ERROR_STATE_D,
                                                                                        state_t_id)

        return self.__error_state_dict.get(state_t_id, "")

    def __get_error_state_t_id(self, state_value):
        # Use __error_state_dict to read cached values, but this time we have the value,
        # not the key, so check in dict values and if not found, go for its t_id
        if state_value not in self.__error_state_dict.values():
            db = self.__qr_engine.get_db_quality()
            t_id = LADMData().get_domain_code_from_value(db, db.names.ERR_ERROR_STATE_D, state_value)
            self.__error_state_dict[t_id] = state_value

        # Get key by value in a dict:
        return next((k for k in self.__error_state_dict if self.__error_state_dict[k] == state_value), None)

    def __get_error_layer(self):
        if not self.__error_layer:
            db = self.__qr_engine.get_db_quality()
            self.__error_layer = self.app.core.get_layer(db, db.names.ERR_QUALITY_ERROR_T)

        return self.__error_layer

    def __get_point_error_layer(self):
        if not self.__point_layer:
            db = self.__qr_engine.get_db_quality()
            self.__point_layer = self.app.core.get_layer(db, db.names.ERR_POINT_T)

        return self.__point_layer

    def __get_line_error_layer(self):
        if not self.__line_layer:
            db = self.__qr_engine.get_db_quality()
            self.__line_layer = self.app.core.get_layer(db, db.names.ERR_LINE_T)

        return self.__line_layer

    def __get_polygon_error_layer(self):
        if not self.__polygon_layer:
            db = self.__qr_engine.get_db_quality()
            self.__polygon_layer = self.app.core.get_layer(db, db.names.ERR_POLYGON_T)

        return self.__polygon_layer

    def __reset_layers(self):
        # To be used when we are returning to select QR results (i.e., to the general results panel)
        self.__error_layer = None
        self.__point_layer = None
        self.__line_layer = None
        self.__polygon_layer = None

    def __reset_selected_qr(self):
        # To be used when we are returning to select QR results (i.e., to the general results panel)
        self.__selected_qr = None

    def __reset_error_state_dict(self):
        # To be used when we are returning to select QR results (i.e., to the general results panel)
        self.__error_state_dict = dict()

    def __error_related_geometries(self, error_t_ids):
        # Prefered geometry types are polygons, lines, points, in that order
        db = self.__qr_engine.get_db_quality()
        error_data = self.get_error_results_data()
        dict_layer_fids = dict()

        for error_t_id in error_t_ids:
            feature = error_data.get(error_t_id, None)

            if feature:
                polygon = feature[db.names.ERR_QUALITY_ERROR_T_POLYGON_F]
                line = feature[db.names.ERR_QUALITY_ERROR_T_LINE_F]
                point = feature[db.names.ERR_QUALITY_ERROR_T_POINT_F]

                if polygon:
                    if 'polygon' in dict_layer_fids:
                        dict_layer_fids['polygon']['fids'].append(polygon)
                    else:
                        dict_layer_fids['polygon'] = {'layer': self.__get_polygon_error_layer(), 'fids': [polygon]}
                elif line:
                    if 'line' in dict_layer_fids:
                        dict_layer_fids['line']['fids'].append(line)
                    else:
                        dict_layer_fids['line'] = {'layer': self.__get_line_error_layer(), 'fids': [line]}
                elif point:
                    if 'point' in dict_layer_fids:
                        dict_layer_fids['point']['fids'].append(point)
                    else:
                        dict_layer_fids['point'] = {'layer': self.__get_point_error_layer(), 'fids': [point]}

        return dict_layer_fids

    def highlight_geometries(self, t_ids):
        res_geometries = self.__error_related_geometries(t_ids)

        if res_geometries:
            # First zoom to geometries
            if len(res_geometries) == 1:  # Only one geometry type related
                for geom_type, dict_layer_fids in res_geometries.items():  # We know this will be called just once
                    self.app.gui.zoom_to_feature_ids(dict_layer_fids['layer'], dict_layer_fids['fids'])
            else:  # Multiple geometry types were found, so combine the extents and then zoom to it
                combined_extent = QgsRectangle()
                for geom_type, dict_layer_fids in res_geometries.items():
                    combined_extent.combineExtentWith(
                        self.app.core.get_extent_from_feature_ids(dict_layer_fids['layer'], dict_layer_fids['fids']))

                self.app.gui.zoom_to_extent(combined_extent)

            # Now highlight geometries
            for geom_type, dict_layer_fids in res_geometries.items():
                self.app.gui.flash_features(dict_layer_fids['layer'], dict_layer_fids['fids'], flashes=5)

    def get_uuids_display_name(self):
        names = self.__qr_engine.get_db_quality().names
        res = self.__selected_qr.field_mapping(names).get(names.ERR_QUALITY_ERROR_T_OBJECT_IDS_F, '')

        return res if res else QCoreApplication.translate("QualityRules", "UUIDs")

    def set_fixed_error(self, error_t_id, fixed):
        # Save to the intermediate dict of data and to the underlying data source whether an error is fixed or not
        db = self.__qr_engine.get_db_quality()
        idx_state = self.__get_error_layer().fields().indexOf(db.names.ERR_QUALITY_ERROR_T_ERROR_STATE_F)

        value = LADMNames.ERR_ERROR_STATE_D_FIXED_V if fixed else LADMNames.ERR_ERROR_STATE_D_ERROR_V
        fixed_or_error_t_id = self.__get_error_state_t_id(value)

        if fixed_or_error_t_id is None:
            self.logger.critical(__name__, "The error state t_id couldn't be found for value '{}'!".format(value))
            return

        # Save to dict
        self.get_error_results_data()[error_t_id].setAttribute(idx_state, fixed_or_error_t_id)

        fids = LADMData.get_fids_from_key_values(self.__get_error_layer(), db.names.T_ID_F, [error_t_id])

        # Save to underlying data source
        if fids:
            res = self.__get_error_layer().dataProvider().changeAttributeValues({fids[0]: {idx_state: fixed_or_error_t_id}})

            if not res:
                self.logger.critical(__name__, "Error modifying the error state value!")
        else:
            self.logger.critical(__name__, "Error with t_id '' not found!".format(error_t_id))

    def __emit_refresh_error_layer_symbology(self):
        if self.__get_point_error_layer().featureCount():
            self.refresh_error_layer_symbology.emit(self.__get_point_error_layer())

        if self.__get_line_error_layer().featureCount():
            self.refresh_error_layer_symbology.emit(self.__get_line_error_layer())

        if self.__get_polygon_error_layer().featureCount():
            self.refresh_error_layer_symbology.emit(self.__get_polygon_error_layer())
