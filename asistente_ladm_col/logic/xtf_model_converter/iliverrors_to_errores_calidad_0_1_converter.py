"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin           : 2021-11-24
        git sha         : :%H$
        copyright       : (C) 2021 by Germán Carrillo (SwissTierras Colombia)
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
import uuid

from qgis.PyQt.QtCore import (pyqtSignal,
                              QObject,
                              QCoreApplication)
from qgis.core import (QgsVectorLayer,
                       QgsProject,
                       QgsVectorLayerUtils,
                       QgsGeometry,
                       QgsPoint)
import processing

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.config.quality_rule_config import (QR_ILIVALIDATORR0001,
                                                           QRE_ILIVALIDATORR0001E01)
from asistente_ladm_col.core.xtf_model_converter.ladm_col_model_converter import LADMColModelConverter
from asistente_ladm_col.logic.ladm_col.ladm_data import LADMData
from asistente_ladm_col.utils.interlis_utils import get_layer_from_xtflog


class IliVErrorsToErroresCalidad01Converter(LADMColModelConverter):
    """
    Convert data from IliVErrors to Errores_Calidad_V0_1
    """
    def __init__(self):
        LADMColModelConverter.__init__(self)

        self._key = "iliverrors-errores_calidad_0_1"
        self._display_name = "IliVErrors a Errores Calidad 0.1"
        self._from_models = ["IliVErrors"]
        self._to_models = ["Errores_Calidad_V0_1"]

        self.app = AppInterface()

    def convert(self, source_xtf, target_xtf, params):
        # TODO: overload convert() with target_db
        db_qr = target_xtf

        # Load XTF as QGIS Layer
        xtf_layer = get_layer_from_xtflog(source_xtf)

        if xtf_layer is None or not xtf_layer.isValid():
            return False, QCoreApplication.translate("IliVErrorsToErroresCalidad01Converter",
                                                     "The XTFLog file '{}' is not a valid QGIS layer!").format(source_xtf)
        if not xtf_layer.featureCount():
            return True, QCoreApplication.translate("IliVErrorsToErroresCalidad01Converter",
                                                     "The XTFLog file '{}' has no errors!").format(source_xtf)

        xtf_layer = QgsProject.instance().addMapLayer(xtf_layer, False)

        # Get required DB Layers
        names = db_qr.names
        layers = {names.ERR_QUALITY_ERROR_T: None,
                  names.ERR_RULE_TYPE_T: None,
                  names.ERR_ERROR_TYPE_T: None,
                  names.ERR_POINT_T: None,
                  names.ERR_ERROR_STATE_D: None}
        self.app.core.get_layers(db_qr, layers, load=True)

        if not layers:
            return False, QCoreApplication.translate("IliVErrorsToErroresCalidad01Converter",
                                                     "Are you sure the target DB has the Errores Calidad structure? At least one layer from the quality error DB was not found!")

        point_layer = layers[names.ERR_POINT_T]
        quality_error_layer = layers[names.ERR_QUALITY_ERROR_T]
        self.progress_changed.emit(10)

        # Validate that we have the required rule and error domain values
        qr_rule = LADMData().get_fids_from_key_values(layers[names.ERR_RULE_TYPE_T], names.ERR_RULE_TYPE_T_CODE_F,
                                                      [QR_ILIVALIDATORR0001])
        qr_error = LADMData().get_fids_from_key_values(layers[names.ERR_ERROR_TYPE_T], names.ERR_ERROR_TYPE_T_CODE_F,
                                                       [QRE_ILIVALIDATORR0001E01])
        if not qr_rule:
            return False, QCoreApplication.translate("IliVErrorsToErroresCalidad01Converter",
                                                     "The quality rule '{}' was not found in the quality error DB!").format(
                QR_ILIVALIDATORR0001)
        if not qr_error:
            return False, QCoreApplication.translate("IliVErrorsToErroresCalidad01Converter",
                                                     "The quality error '{}' was not found in the quality error DB!").format(
                QRE_ILIVALIDATORR0001E01)

        qr_rule = qr_rule[0]
        qr_error = qr_error[0]

        ## 1. Deal with Points

        # 1.1 Calculate UUID for points
        alg_params = {'INPUT': xtf_layer,
                      'FIELD_NAME': 'uuid_point',
                      'FIELD_TYPE': 2,  # String
                      'FIELD_LENGTH': 36,
                      'FIELD_PRECISION': 3,
                      'NEW_FIELD': True,
                      'FORMULA': 'substr(uuid(),2,36)'}
        processing.run("ladm_col:fieldcalculatorforinputlayer", alg_params)
        self.progress_changed.emit(20)

        # 1.2 Copy only the points to target layer (passing the calculated uuid to t_ili_tid)
        features = list()
        idx_t_ili_tid_points = point_layer.fields().indexOf(names.T_ILI_TID_F)
        for xtf_feature in xtf_layer.getFeatures():
            if xtf_feature['CoordX'] and xtf_feature['CoordY']:
                new_feature = QgsVectorLayerUtils().createFeature(point_layer,
                                                                  QgsGeometry(QgsPoint(xtf_feature['CoordX'],
                                                                                       xtf_feature['CoordY'],
                                                                                       0)),
                                                                  {idx_t_ili_tid_points: xtf_feature['uuid_point']})
                features.append(new_feature)

        point_layer.dataProvider().addFeatures(features)

        self.progress_changed.emit(40)

        ## 2. Deal with Quality Errors

        # 2.1 Join to take t_id from Point layer to the source XTFLog layer based on the calculated uuid
        alg_params = {'INPUT': xtf_layer,
                      'FIELD': 'uuid_point',
                      'INPUT_2': point_layer,
                      'FIELD_2': 'T_Ili_Tid',
                      'DISCARD_NONMATCHING': False,
                      'FIELDS_TO_COPY': [],
                      'METHOD': 1,  # 1:1 relationship
                      'OUTPUT': 'TEMPORARY_OUTPUT',
                      'PREFIX': 'point_'}
        joined_layer = processing.run("native:joinattributestable", alg_params)['OUTPUT']

        self.progress_changed.emit(50)

        # 2.2 Copy features to Quality Errors target layer
        features = list()
        quality_error_layer_fields = quality_error_layer.fields()
        idx_ili_t_ili_tid = joined_layer.fields().indexOf('Tid')
        idx_ili_obj_tag = joined_layer.fields().indexOf('ObjTag')
        idx_ili_message = joined_layer.fields().indexOf('Message')
        idx_t_ili_tid_errors = quality_error_layer_fields.indexOf(names.T_ILI_TID_F)
        idx_rule_type = quality_error_layer_fields.indexOf(names.ERR_QUALITY_ERROR_T_RULE_TYPE_F)
        idx_error_type = quality_error_layer_fields.indexOf(names.ERR_QUALITY_ERROR_T_ERROR_TYPE_F)
        idx_object_ids = quality_error_layer_fields.indexOf(names.ERR_QUALITY_ERROR_T_OBJECT_IDS_F)
        idx_object_ili_name = quality_error_layer_fields.indexOf(names.ERR_QUALITY_ERROR_T_ILI_NAME_F)
        idx_details = quality_error_layer_fields.indexOf(names.ERR_QUALITY_ERROR_T_DETAILS_F)
        idx_error_state = quality_error_layer_fields.indexOf(names.ERR_QUALITY_ERROR_T_ERROR_STATE_F)
        idx_related_point = quality_error_layer_fields.indexOf(names.ERR_QUALITY_ERROR_T_POINT_F)

        count = 0
        num_features = xtf_layer.featureCount()
        dict_percentages = {0 if k == 0 else int(num_features * k / 100): v for k,v in {0:60, 25:70, 50:80, 75:90}.items()}  # {val: percentage}
        list_percentages = list(dict_percentages.keys())

        for xtf_feature in joined_layer.getFeatures():
            # Progress handling
            count += 1
            if list_percentages and count > list_percentages[0]:
                self.progress_changed.emit(dict_percentages[list_percentages[0]])
                list_percentages.pop(0)

            if xtf_feature[idx_ili_t_ili_tid]:
                attrs = {idx_t_ili_tid_errors: str(uuid.uuid4()),
                         idx_rule_type: qr_rule,
                         idx_error_type: qr_error,
                         idx_object_ids: [xtf_feature[idx_ili_t_ili_tid]],  # It's a JSON array
                         idx_object_ili_name: xtf_feature[idx_ili_obj_tag] if idx_ili_obj_tag != -1 else None,
                         idx_details: xtf_feature[idx_ili_message] if idx_ili_message != -1 else None,
                         idx_error_state: LADMData().get_domain_code_from_value(db_qr, layers[names.ERR_ERROR_STATE_D],
                                                                                LADMNames.ERR_ERROR_STATE_D_ERROR_V),
                         idx_related_point: xtf_feature['point_T_id']}
                new_feature = QgsVectorLayerUtils().createFeature(quality_error_layer, attributes=attrs)
                features.append(new_feature)

        quality_error_layer.dataProvider().addFeatures(features)

        QgsProject.instance().removeMapLayer(xtf_layer)
        self.progress_changed.emit(100)

        return True, QCoreApplication.translate("IliVErrorsToErroresCalidad01Converter",
                                                "The data was successfully converted to '{}' model!").format(
            self._to_models[0])
