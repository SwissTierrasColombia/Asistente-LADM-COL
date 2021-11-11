"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin          : 2021-11-10
        git sha        : :%H$
        copyright      : (C) 2021 by Germán Carrillo (SwissTierras Colombia)
        email          : gcarrillo@linuxmail.org
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
import os.path
import tempfile
import uuid

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import QgsVectorLayerUtils

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.enums import EnumQualityRuleType
from asistente_ladm_col.config.layer_config import LADMNames
from asistente_ladm_col.lib.db.gpkg_connector import GPKGConnector
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.model_registry import LADMColModelRegistry
from asistente_ladm_col.lib.qgis_model_baker.ili2db import Ili2DB
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData

app = AppInterface()
logger = Logger()


def get_quality_error_connector(output_path, timestamp):
    output_path = _get_valid_output_path(output_path, timestamp)
    if output_path is None:
        return False, "", None

    db_file = os.path.join(output_path, "Reglas_de_Calidad_{}.gpkg".format(timestamp))
    db = GPKGConnector(db_file)
    ili2db = Ili2DB()
    error_model = LADMColModelRegistry().model(LADMNames.QUALITY_ERROR_MODEL_KEY)
    res, msg = ili2db.import_schema(db, [error_model.full_name()])

    if res:
        for catalogue_key, catalogue_xtf_path in error_model.get_catalogues().items():
            logger.info(__name__, "Importing catalogue '{}' to quality error database...".format(catalogue_key))
            res_xtf, msg_xtf = ili2db.import_data(db, catalogue_xtf_path)
            if not res_xtf:
                logger.warning(__name__,
                               "There was a problem importing catalogue '{}'! Skipping...".format(catalogue_key))

    return res, msg, None if not res else db


def _get_valid_output_path(output_path, timestamp):
    if not os.path.exists(output_path):
        output_path = tempfile.gettempdir()
        logger.warning(__name__, QCoreApplication.translate("QualityRuleEngine",
                                                            "Output dir doesn't exist! Using now '{}'").format(
            OUTPUT_DIR))

    output_path = os.path.join(output_path, "Reglas_de_Calidad_{}".format(timestamp))
    try:
        os.makedirs(output_path)
    except PermissionError as e:
        logger.critical_msg(__name__, QCoreApplication.translate("QualityRuleEngine",
                                                                 "Output dir '{}' is read-only!").format(
            output_path))
        output_path = None

    return output_path


def save_errors(db_qr, rule_code, error_code, error_data, target_layer, ili_name=''):
    """
    Save error data in the quality error model by error_code, which means that you should call this function once
    per error type. Accepts both, spatial and non-spatial errors.

    :param db_qr: DB Connector
    :param rule_code: Rule code as specified in the external catalogues.
    :param error_code: Error code as specified in the external catalogues.
    :param error_data: Dict of lists:
                           {'geometries': [geometries], 'data': [obj_uuids, rel_obj_uuids, values, details]}
                           Note: this dict will always have 2 elements.
                           Note 2: For geometry errors, this dict will always have the same number of elements in
                                   each of the two lists (and the element order matters!).
                           Note 3: For geometryless errors, the 'geometries' value won't be even read.
    :param target_layer: Value of EnumQualityRuleType.
    :param ili_name: Interlis name of the class where the object uuids can be found.
    :return: Tuple (res: boolean, msg: string)
    """
    if not hasattr(db_qr.names, "T_ID_F"):
        db_qr.test_connection()
    names = db_qr.names
    layers = {names.ERR_QUALITY_ERROR_T: None,
              names.ERR_RULE_TYPE_T: None,
              names.ERR_ERROR_TYPE_T: None}

    if target_layer == EnumQualityRuleType.POINT:
        layers[names.ERR_POINT_T] = None
    elif target_layer == EnumQualityRuleType.LINE:
        layers[names.ERR_LINE_T] = None
    elif target_layer == EnumQualityRuleType.POLYGON:
        layers[names.ERR_POLYGON_T] = None

    app.core.get_layers(db_qr, layers, load=True)

    if not layers:
        return False, "At least one layer was not found in the quality error db!"

    # We do now a soon check of rule code and error code to stop if cannot be found
    fids = LADMData.get_fids_from_key_values(layers[names.ERR_RULE_TYPE_T], names.ERR_RULE_TYPE_T_CODE_F, [rule_code])
    if not fids:
        return False, "There was a problem saving quality error data. The rule '{}' cannot be found in the database. Is that rule in any registered catalogue?".format(rule_code)
    rule_code_id = fids[0]

    fids = LADMData.get_fids_from_key_values(layers[names.ERR_ERROR_TYPE_T], names.ERR_ERROR_TYPE_T_CODE_F, [error_code])
    if not fids:
        return False, "There was a problem saving quality error data. The error '{}' cannot be found in the database. Is that error in any registered catalogue?".format(
            error_code)
    error_code_id = fids[0]

    qr_error_layer = layers[names.ERR_QUALITY_ERROR_T]

    # First we deal with geometries
    geom_layer = None
    idx_geometry_fk = None
    geom_t_ids = list()  # To store fks (geom t_id)
    if target_layer == EnumQualityRuleType.POINT:
        geom_layer = layers[names.ERR_POINT_T]
        idx_geometry_fk = qr_error_layer.fields().indexOf(names.ERR_QUALITY_ERROR_T_POINT_F)
    elif target_layer == EnumQualityRuleType.LINE:
        geom_layer = layers[names.ERR_LINE_T]
        idx_geometry_fk = qr_error_layer.fields().indexOf(names.ERR_QUALITY_ERROR_T_LINE_F)
    elif target_layer == EnumQualityRuleType.POLYGON:
        geom_layer = layers[names.ERR_POLYGON_T]
        idx_geometry_fk = qr_error_layer.fields().indexOf(names.ERR_QUALITY_ERROR_T_POLYGON_F)

    if geom_layer:
        idx_t_ili_tid_geom = geom_layer.fields().indexOf(names.T_ILI_TID_F)
        geometries = error_data['geometries']

        features = list()
        for geometry in geometries:
            new_feature = QgsVectorLayerUtils().createFeature(geom_layer,
                                                              geometry,
                                                              {idx_t_ili_tid_geom: str(uuid.uuid4())})
            features.append(new_feature)

        res_geom, out_features = geom_layer.dataProvider().addFeatures(features)
        if res_geom:
            geom_t_ids = [out_feature[names.T_ID_F] for out_feature in out_features]
        else:
            return False, "There was a problem saving error geometries for error code '{}'!".format(error_code)

    # Now we deal with the alphanumeric data
    idx_t_ili_tid = qr_error_layer.fields().indexOf(names.T_ILI_TID_F)
    idx_rule_type = qr_error_layer.fields().indexOf(names.ERR_QUALITY_ERROR_T_RULE_TYPE_F)
    idx_error_type = qr_error_layer.fields().indexOf(names.ERR_QUALITY_ERROR_T_ERROR_TYPE_F)
    idx_object_ids = qr_error_layer.fields().indexOf(names.ERR_QUALITY_ERROR_T_OBJECT_IDS_F)
    idx_rel_object_ids = qr_error_layer.fields().indexOf(names.ERR_QUALITY_ERROR_T_RELATED_OBJECT_IDS_F)
    idx_values = qr_error_layer.fields().indexOf(names.ERR_QUALITY_ERROR_T_VALUES_F)
    idx_ili_name = qr_error_layer.fields().indexOf(names.ERR_QUALITY_ERROR_T_ILI_NAME_F)
    idx_details = qr_error_layer.fields().indexOf(names.ERR_QUALITY_ERROR_T_DETAILS_F)

    features = list()
    for i, data in enumerate(error_data['data']):
        attr_map = {idx_t_ili_tid: str(uuid.uuid4()),
                    idx_rule_type: rule_code_id,
                    idx_error_type: error_code_id,
                    idx_object_ids: data[0],
                    idx_rel_object_ids: data[1],
                    idx_values: data[2],
                    idx_details: data[3],
                    idx_ili_name: ili_name}
        if geom_layer:
            attr_map[idx_geometry_fk] = geom_t_ids[i]  # We take advantage of the preserved order here

        features.append(QgsVectorLayerUtils().createFeature(qr_error_layer, attributes=attr_map))

    res_data, out_features = qr_error_layer.dataProvider().addFeatures(features)
    if not res_data:
        return False, "There was a problem saving error alphanumeric data for error code '{}'!".format(error_code)

    return True, "Success!"


def save_metadata(db_qr, metadata):
    return True, "Success!"
