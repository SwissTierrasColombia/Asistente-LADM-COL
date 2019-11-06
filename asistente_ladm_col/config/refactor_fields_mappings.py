from qgis.PyQt.QtCore import QSettings
from .table_mapping_config import *

class RefactorFieldsMappings:
    def __init__(self):
        self.names = Names()

    def get_refactor_fields_mapping(self, layer_name, qgis_utils):
        mapping = []

        # --------------------------------
        # OPERATION MODEL
        # --------------------------------
        if layer_name == self.names.OP_BOUNDARY_POINT_T:
            mapping = [
                {'expression': '"{}"'.format(self.names.OP_BOUNDARY_POINT_T_ID_F), 'length': 255, 'name': '{}'.format(self.names.OP_BOUNDARY_POINT_T_ID_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.OP_BOUNDARY_POINT_T_POINT_TYPE_F), 'length': -1, 'name': '{}'.format(self.names.OP_BOUNDARY_POINT_T_POINT_TYPE_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.OP_BOUNDARY_POINT_T_AGREEMENT_F), 'length': -1, 'name': '{}'.format(self.names.OP_BOUNDARY_POINT_T_AGREEMENT_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.OP_BOUNDARY_POINT_T_PHOTO_IDENTIFICATION_F), 'length': -1, 'name': '{}'.format(self.names.OP_BOUNDARY_POINT_T_PHOTO_IDENTIFICATION_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.OP_BOUNDARY_POINT_T_POINT_LOCATION_F), 'length': -1, 'name': '{}'.format(self.names.OP_BOUNDARY_POINT_T_POINT_LOCATION_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.OP_BOUNDARY_POINT_T_HORIZONTAL_ACCURACY_F), 'length': -1, 'name': '{}'.format(self.names.OP_BOUNDARY_POINT_T_HORIZONTAL_ACCURACY_F), 'precision': 0, 'type': 2},
                {'expression': '"{}"'.format(self.names.OP_BOUNDARY_POINT_T_VERTICAL_ACCURACY_F), 'length': -1, 'name': '{}'.format(self.names.OP_BOUNDARY_POINT_T_VERTICAL_ACCURACY_F), 'precision': 0, 'type': 2},
                {'expression': '"{}"'.format(self.names.COL_POINT_T_INTERPOLATION_POSITION_F), 'length': -1, 'name': '{}'.format(self.names.COL_POINT_T_INTERPOLATION_POSITION_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_POINT_T_MONUMENTATION_F), 'length': -1, 'name': '{}'.format(self.names.COL_POINT_T_MONUMENTATION_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_POINT_T_PRODUCTION_METHOD_F), 'length': -1, 'name': '{}'.format(self.names.COL_POINT_T_PRODUCTION_METHOD_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_POINT_T_NAMESPACE_F), 'length': 255, 'name': '{}'.format(self.names.COL_POINT_T_NAMESPACE_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_POINT_T_LOCAL_ID_F), 'length': 255, 'name': '{}'.format(self.names.COL_POINT_T_LOCAL_ID_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16}
            ]
        elif layer_name == self.names.OP_SURVEY_POINT_T:
            mapping = [
                {'expression': '"{}"'.format(self.names.OP_SURVEY_POINT_T_ID_F), 'length': 255, 'name': '{}'.format(self.names.OP_SURVEY_POINT_T_ID_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.OP_SURVEY_POINT_T_POINT_TYPE_F), 'length': -1, 'name': '{}'.format(self.names.OP_SURVEY_POINT_T_POINT_TYPE_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.OP_SURVEY_POINT_T_SURVEY_POINT_TYPE_F), 'length': -1, 'name': '{}'.format(self.names.OP_SURVEY_POINT_T_SURVEY_POINT_TYPE_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.OP_SURVEY_POINT_T_PHOTO_IDENTIFICATION_F), 'length': -1, 'name': '{}'.format(self.names.OP_SURVEY_POINT_T_PHOTO_IDENTIFICATION_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.OP_SURVEY_POINT_T_HORIZONTAL_ACCURACY_F), 'length': -1, 'name': '{}'.format(self.names.OP_SURVEY_POINT_T_HORIZONTAL_ACCURACY_F), 'precision': 0, 'type': 2},
                {'expression': '"{}"'.format(self.names.OP_SURVEY_POINT_T_VERTICAL_ACCURACY_F), 'length': -1, 'name': '{}'.format(self.names.OP_SURVEY_POINT_T_VERTICAL_ACCURACY_F), 'precision': 0, 'type': 2},
                {'expression': '"{}"'.format(self.names.COL_POINT_T_INTERPOLATION_POSITION_F), 'length': -1, 'name': '{}'.format(self.names.COL_POINT_T_INTERPOLATION_POSITION_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_POINT_T_MONUMENTATION_F), 'length': -1, 'name': '{}'.format(self.names.COL_POINT_T_MONUMENTATION_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_POINT_T_PRODUCTION_METHOD_F), 'length': -1, 'name': '{}'.format(self.names.COL_POINT_T_PRODUCTION_METHOD_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_POINT_T_NAMESPACE_F), 'length': 255, 'name': '{}'.format(self.names.COL_POINT_T_NAMESPACE_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_POINT_T_LOCAL_ID_F), 'length': 255, 'name': '{}'.format(self.names.COL_POINT_T_LOCAL_ID_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16}
            ]
        elif layer_name == self.names.OP_CONTROL_POINT_T:
            mapping = [
                {'expression': '"{}"'.format(self.names.OP_CONTROL_POINT_T_ID_F), 'length': 255, 'name': '{}'.format(self.names.OP_CONTROL_POINT_T_ID_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.OP_CONTROL_POINT_T_POINT_TYPE_F), 'length': -1, 'name': '{}'.format(self.names.OP_CONTROL_POINT_T_POINT_TYPE_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.OP_CONTROL_POINT_T_CONTROL_POINT_TYPE_F), 'length': -1, 'name': '{}'.format(self.names.OP_CONTROL_POINT_T_CONTROL_POINT_TYPE_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.OP_CONTROL_POINT_T_HORIZONTAL_ACCURACY_F), 'length': -1, 'name': '{}'.format(self.names.OP_CONTROL_POINT_T_HORIZONTAL_ACCURACY_F), 'precision': 0, 'type': 2},
                {'expression': '"{}"'.format(self.names.OP_CONTROL_POINT_T_VERTICAL_ACCURACY_F), 'length': -1, 'name': '{}'.format(self.names.OP_CONTROL_POINT_T_VERTICAL_ACCURACY_F), 'precision': 0, 'type': 2},
                {'expression': '"{}"'.format(self.names.COL_POINT_T_INTERPOLATION_POSITION_F), 'length': -1, 'name': '{}'.format(self.names.COL_POINT_T_INTERPOLATION_POSITION_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_POINT_T_MONUMENTATION_F), 'length': -1, 'name': '{}'.format(self.names.COL_POINT_T_MONUMENTATION_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_POINT_T_PRODUCTION_METHOD_F), 'length': -1, 'name': '{}'.format(self.names.COL_POINT_T_PRODUCTION_METHOD_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_POINT_T_NAMESPACE_F), 'length': 255, 'name': '{}'.format(self.names.COL_POINT_T_NAMESPACE_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_POINT_T_LOCAL_ID_F), 'length': 255, 'name': '{}'.format(self.names.COL_POINT_T_LOCAL_ID_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16}
            ]
        elif layer_name == self.names.OP_BOUNDARY_T:
            mapping = [
                {'expression': '"{}"'.format(self.names.OP_BOUNDARY_T_LENGTH_F), 'length': 6, 'name': '{}'.format(self.names.OP_BOUNDARY_T_LENGTH_F), 'precision': 1, 'type': 6},
                {'expression': '"{}"'.format(self.names.COL_BFS_T_TEXTUAL_LOCATION_F), 'length': 255, 'name': '{}'.format(self.names.COL_BFS_T_TEXTUAL_LOCATION_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_POINT_T_NAMESPACE_F), 'length': 255, 'name': '{}'.format(self.names.COL_POINT_T_NAMESPACE_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_POINT_T_LOCAL_ID_F), 'length': 255, 'name': '{}'.format(self.names.COL_POINT_T_LOCAL_ID_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16}
            ]
        elif layer_name == self.names.OP_PLOT_T:
            mapping = [
                {'expression': '{}'.format(self.names.OP_PLOT_T_PLOT_AREA_F), 'length': 15, 'name': '{}'.format(self.names.OP_PLOT_T_PLOT_AREA_F), 'precision': 1, 'type': 6},
                {'expression': '"{}"'.format(self.names.OP_PLOT_T_PLOT_VALUATION_F), 'length': 16, 'name': '{}'.format(self.names.OP_PLOT_T_PLOT_VALUATION_F), 'precision': 1, 'type': 6},
                {'expression': '"{}"'.format(self.names.COL_SPATIAL_UNIT_T_DIMENSION_F), 'length': -1, 'name': '{}'.format(self.names.COL_SPATIAL_UNIT_T_DIMENSION_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_SPATIAL_UNIT_T_LABEL_F), 'length': 255, 'name': '{}'.format(self.names.COL_SPATIAL_UNIT_T_LABEL_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_SPATIAL_UNIT_T_SURFACE_RELATION_F), 'length': -1, 'name': '{}'.format(self.names.COL_SPATIAL_UNIT_T_SURFACE_RELATION_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_SPATIAL_UNIT_T_NAMESPACE_F), 'length': 255, 'name': '{}'.format(self.names.COL_SPATIAL_UNIT_T_NAMESPACE_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_SPATIAL_UNIT_T_LOCAL_ID_F), 'length': 255, 'name': '{}'.format(self.names.COL_SPATIAL_UNIT_T_LOCAL_ID_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16}
            ]
        elif layer_name == self.names.OP_PARCEL_T:
            mapping = [
                {'expression': '"{}"'.format(self.names.OP_PARCEL_T_DEPARTMENT_F), 'length': 2, 'name': '{}'.format(self.names.OP_PARCEL_T_DEPARTMENT_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.OP_PARCEL_T_MUNICIPALITY_F), 'length': 3, 'name': '{}'.format(self.names.OP_PARCEL_T_MUNICIPALITY_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.OP_PARCEL_T_NUPRE_F), 'length': 11, 'name': '{}'.format(self.names.OP_PARCEL_T_NUPRE_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.OP_PARCEL_T_ORIP_CODE_F), 'length': 3, 'name': '{}'.format(self.names.OP_PARCEL_T_ORIP_CODE_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.OP_PARCEL_T_FMI_F), 'length': 80, 'name': '{}'.format(self.names.OP_PARCEL_T_FMI_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.OP_PARCEL_T_PARCEL_NUMBER_F), 'length': 30, 'name': '{}'.format(self.names.OP_PARCEL_T_PARCEL_NUMBER_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F), 'length': 20, 'name': '{}'.format(self.names.OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.OP_PARCEL_T_VALUATION_F), 'length': 16, 'name': '{}'.format(self.names.OP_PARCEL_T_VALUATION_F), 'precision': 1, 'type': 6},
                {'expression': '"{}"'.format(self.names.OP_PARCEL_T_PARCEL_TYPE_F), 'length': -1, 'name': '{}'.format(self.names.OP_PARCEL_T_PARCEL_TYPE_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.OP_PARCEL_T_TYPE_F), 'length': -1, 'name': '{}'.format(self.names.OP_PARCEL_T_TYPE_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.OP_PARCEL_T_ADDRESS_F), 'length': 255, 'name': '{}'.format(self.names.OP_PARCEL_T_ADDRESS_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_BAUNIT_T_NAME_F), 'length': 255, 'name': '{}'.format(self.names.COL_BAUNIT_T_NAME_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_BAUNIT_T_NAMESPACE_F), 'length': 255, 'name': '{}'.format(self.names.COL_BAUNIT_T_NAMESPACE_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_BAUNIT_T_LOCAL_ID_F), 'length': 255, 'name': '{}'.format(self.names.COL_BAUNIT_T_LOCAL_ID_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16}
            ]
        elif layer_name == self.names.OP_PARTY_T:
            mapping = [
                {'expression': '"{}"'.format(self.names.OP_PARTY_T_TYPE_F), 'length': -1, 'name': '{}'.format(self.names.OP_PARTY_T_TYPE_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.OP_PARTY_T_DOCUMENT_TYPE_F), 'length': -1, 'name': '{}'.format(self.names.OP_PARTY_T_DOCUMENT_TYPE_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.OP_PARTY_T_DOCUMENT_ID_F), 'length': 50, 'name': '{}'.format(self.names.OP_PARTY_T_DOCUMENT_ID_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.OP_PARTY_T_FIRST_NAME_1_F), 'length': 100, 'name': '{}'.format(self.names.OP_PARTY_T_FIRST_NAME_1_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.OP_PARTY_T_FIRST_NAME_2_F), 'length': 100, 'name': '{}'.format(self.names.OP_PARTY_T_FIRST_NAME_2_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.OP_PARTY_T_SURNAME_1_F), 'length': 100, 'name': '{}'.format(self.names.OP_PARTY_T_SURNAME_1_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.OP_PARTY_T_SURNAME_2_F), 'length': 100, 'name': '{}'.format(self.names.OP_PARTY_T_SURNAME_2_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.OP_PARTY_T_GENRE_F), 'length': -1, 'name': '{}'.format(self.names.OP_PARTY_T_GENRE_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.OP_PARTY_T_ETHNIC_GROUP_F), 'length': -1, 'name': '{}'.format(self.names.OP_PARTY_T_ETHNIC_GROUP_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.OP_PARTY_T_BUSINESS_NAME_F), 'length': 255, 'name': '{}'.format(self.names.OP_PARTY_T_BUSINESS_NAME_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_PARTY_T_NAME_F), 'length': 255, 'name': '{}'.format(self.names.COL_PARTY_T_NAME_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_PARTY_T_NAMESPACE_F), 'length': 255, 'name': '{}'.format(self.names.COL_PARTY_T_NAMESPACE_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_PARTY_T_LOCAL_ID_F), 'length': 255, 'name': '{}'.format(self.names.COL_PARTY_T_LOCAL_ID_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16}
            ]
        elif layer_name == self.names.OP_ADMINISTRATIVE_SOURCE_T:
            mapping = [
                {'expression': '"{}"'.format(self.names.OP_ADMINISTRATIVE_SOURCE_T_TYPE_F), 'length': -1, 'name': '{}'.format(self.names.OP_ADMINISTRATIVE_SOURCE_T_TYPE_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.OP_ADMINISTRATIVE_SOURCE_T_EMITTING_ENTITY_F), 'length': 255, 'name': '{}'.format(self.names.OP_ADMINISTRATIVE_SOURCE_T_EMITTING_ENTITY_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_ADMINISTRATIVE_SOURCE_T_OBSERVATION_F), 'length': 255, 'name': '{}'.format(self.names.COL_ADMINISTRATIVE_SOURCE_T_OBSERVATION_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_ADMINISTRATIVE_SOURCE_T_SOURCE_NUMBER_F), 'length': 150, 'name': '{}'.format(self.names.COL_ADMINISTRATIVE_SOURCE_T_SOURCE_NUMBER_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_SOURCE_T_AVAILABILITY_STATUS_F), 'length': -1, 'name': '{}'.format(self.names.COL_SOURCE_T_AVAILABILITY_STATUS_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_SOURCE_T_MAIN_TYPE_F), 'length': -1, 'name': '{}'.format(self.names.COL_SOURCE_T_MAIN_TYPE_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_SOURCE_T_NAMESPACE_F), 'length': 255, 'name': '{}'.format(self.names.COL_SOURCE_T_NAMESPACE_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_SOURCE_T_LOCAL_ID_F), 'length': 255, 'name': '{}'.format(self.names.COL_SOURCE_T_LOCAL_ID_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_SOURCE_T_OFFICIAL_F), 'length': -1, 'name': '{}'.format(self.names.COL_SOURCE_T_OFFICIAL_F), 'precision': -1, 'type': 1},
                {'expression': '"{}"'.format(self.names.COL_SOURCE_T_DATE_DOCUMENT_F), 'length': -1, 'name': '{}'.format(self.names.COL_SOURCE_T_DATE_DOCUMENT_F), 'precision': -1, 'type': 14}
            ]
        elif layer_name == self.names.COL_SPATIAL_SOURCE_T:
            mapping = [
                {'expression': '"{}"'.format(self.names.COL_SPATIAL_SOURCE_T_TYPE_F), 'length': -1, 'name': '{}'.format(self.names.COL_SPATIAL_SOURCE_T_TYPE_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_SOURCE_T_AVAILABILITY_STATUS_F), 'length': -1, 'name': '{}'.format(self.names.COL_SOURCE_T_AVAILABILITY_STATUS_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_SOURCE_T_MAIN_TYPE_F), 'length': -1, 'name': '{}'.format(self.names.COL_SOURCE_T_MAIN_TYPE_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_SOURCE_T_NAMESPACE_F), 'length': 255, 'name': '{}'.format(self.names.COL_SOURCE_T_NAMESPACE_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_SOURCE_T_LOCAL_ID_F), 'length': 255, 'name': '{}'.format(self.names.COL_SOURCE_T_LOCAL_ID_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_SOURCE_T_OFFICIAL_F), 'length': -1, 'name': '{}'.format(self.names.COL_SOURCE_T_OFFICIAL_F), 'precision': -1, 'type': 1},
                {'expression': '"{}"'.format(self.names.COL_SOURCE_T_DATE_DOCUMENT_F), 'length': -1, 'name': '{}'.format(self.names.COL_SOURCE_T_DATE_DOCUMENT_F), 'precision': -1, 'type': 14}
            ]
        elif layer_name == self.names.OP_BUILDING_T:
            mapping = [
                {'expression': '"{}"'.format(self.names.OP_BUILDING_T_BUILDING_AREA_F), 'length': 15, 'name': '{}'.format(self.names.OP_BUILDING_T_BUILDING_AREA_F), 'precision': 1, 'type': 6},
                {'expression': '"{}"'.format(self.names.OP_BUILDING_T_NUMBER_OF_FLOORS_F), 'length': -1, 'name': '{}'.format(self.names.OP_BUILDING_T_NUMBER_OF_FLOORS_F), 'precision': 0, 'type': 2},
                {'expression': '"{}"'.format(self.names.OP_BUILDING_T_BUILDING_VALUATION_F), 'length': 16, 'name': '{}'.format(self.names.OP_BUILDING_T_BUILDING_VALUATION_F), 'precision': 1, 'type': 6},
                {'expression': '"{}"'.format(self.names.COL_SPATIAL_UNIT_T_DIMENSION_F), 'length': -1, 'name': '{}'.format(self.names.COL_SPATIAL_UNIT_T_DIMENSION_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_SPATIAL_UNIT_T_LABEL_F), 'length': 255, 'name': '{}'.format(self.names.COL_SPATIAL_UNIT_T_LABEL_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_SPATIAL_UNIT_T_SURFACE_RELATION_F), 'length': -1, 'name': '{}'.format(self.names.COL_SPATIAL_UNIT_T_SURFACE_RELATION_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_SPATIAL_UNIT_T_NAMESPACE_F), 'length': 255, 'name': '{}'.format(self.names.COL_SPATIAL_UNIT_T_NAMESPACE_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_SPATIAL_UNIT_T_LOCAL_ID_F), 'length': 255, 'name': '{}'.format(self.names.COL_SPATIAL_UNIT_T_LOCAL_ID_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16}
            ]
        elif layer_name == self.names.OP_BUILDING_UNIT_T:
            mapping = [
                {'expression': '"{}"'.format(self.names.OP_BUILDING_UNIT_T_IDENTIFICATION_F), 'length': 3, 'name': '{}'.format(self.names.OP_BUILDING_UNIT_T_IDENTIFICATION_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.OP_BUILDING_UNIT_T_BUILT_AREA_F), 'length': 15, 'name': '{}'.format(self.names.OP_BUILDING_UNIT_T_BUILT_AREA_F), 'precision': 1, 'type': 6},
                {'expression': '"{}"'.format(self.names.OP_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F), 'length': 15, 'name': '{}'.format(self.names.OP_BUILDING_UNIT_T_BUILT_PRIVATE_AREA_F), 'precision': 1, 'type': 6},
                {'expression': '"{}"'.format(self.names.OP_BUILDING_UNIT_T_USE_F), 'length': -1, 'name': '{}'.format(self.names.OP_BUILDING_UNIT_T_USE_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.OP_BUILDING_UNIT_T_NUMBER_OF_FLOORS_F), 'length': -1, 'name': '{}'.format(self.names.OP_BUILDING_UNIT_T_NUMBER_OF_FLOORS_F), 'precision': 0, 'type': 2},
                {'expression': '"{}"'.format(self.names.OP_BUILDING_UNIT_T_BUILDING_UNIT_VALUATION_F), 'length': 16, 'name': '{}'.format(self.names.OP_BUILDING_UNIT_T_BUILDING_UNIT_VALUATION_F), 'precision': 1, 'type': 6},
                {'expression': '"{}"'.format(self.names.OP_BUILDING_UNIT_T_FLOOR_F), 'length': -1, 'name': '{}'.format(self.names.OP_BUILDING_UNIT_T_FLOOR_F), 'precision': 0, 'type': 2},
                {'expression': '"{}"'.format(self.names.OP_BUILDING_UNIT_T_BUILDING_F), 'length': -1, 'name': '{}'.format(self.names.OP_BUILDING_UNIT_T_BUILDING_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_SPATIAL_UNIT_T_DIMENSION_F), 'length': -1, 'name': '{}'.format(self.names.COL_SPATIAL_UNIT_T_DIMENSION_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_SPATIAL_UNIT_T_LABEL_F), 'length': 255, 'name': '{}'.format(self.names.COL_SPATIAL_UNIT_T_LABEL_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_SPATIAL_UNIT_T_SURFACE_RELATION_F), 'length': -1, 'name': '{}'.format(self.names.COL_SPATIAL_UNIT_T_SURFACE_RELATION_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_SPATIAL_UNIT_T_NAMESPACE_F), 'length': 255, 'name': '{}'.format(self.names.COL_SPATIAL_UNIT_T_NAMESPACE_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_SPATIAL_UNIT_T_LOCAL_ID_F), 'length': 255, 'name': '{}'.format(self.names.COL_SPATIAL_UNIT_T_LOCAL_ID_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16}
            ]
        elif layer_name == self.names.OP_RIGHT_T:
            mapping = [
                {'expression': '"{}"'.format(self.names.OP_RIGHT_T_TYPE_F), 'length': -1, 'name': '{}'.format(self.names.OP_RIGHT_T_TYPE_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_RRR_T_DESCRIPTION_F), 'length': 255, 'name': '{}'.format(self.names.COL_RRR_T_DESCRIPTION_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_RRR_T_SHARE_CHECK_F), 'length': -1, 'name': '{}'.format(self.names.COL_RRR_T_SHARE_CHECK_F), 'precision': -1, 'type': 1},
                {'expression': '"{}"'.format(self.names.COL_RRR_T_EFFECTIVE_USAGE_F), 'length': 255, 'name': '{}'.format(self.names.COL_RRR_T_EFFECTIVE_USAGE_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_RRR_T_NAMESPACE_F), 'length': 255, 'name': '{}'.format(self.names.COL_RRR_T_NAMESPACE_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_RRR_T_LOCAL_ID_F), 'length': 255, 'name': '{}'.format(self.names.COL_RRR_T_LOCAL_ID_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_RRR_PARTY_T_OP_PARTY_F), 'length': -1, 'name': '{}'.format(self.names.COL_RRR_PARTY_T_OP_PARTY_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F), 'length': -1, 'name': '{}'.format(self.names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_BAUNIT_RRR_T_UNIT_F), 'length': -1, 'name': '{}'.format(self.names.COL_BAUNIT_RRR_T_UNIT_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16}
            ]
        elif layer_name == self.names.OP_RESTRICTION_T:
            mapping = [
                {'expression': '"{}"'.format(self.names.OP_RESTRICTION_T_TYPE_F), 'length': -1, 'name': '{}'.format(self.names.OP_RESTRICTION_T_TYPE_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_RRR_T_DESCRIPTION_F), 'length': 255, 'name': '{}'.format(self.names.COL_RRR_T_DESCRIPTION_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_RRR_T_SHARE_CHECK_F), 'length': -1, 'name': '{}'.format(self.names.COL_RRR_T_SHARE_CHECK_F), 'precision': -1, 'type': 1},
                {'expression': '"{}"'.format(self.names.COL_RRR_T_EFFECTIVE_USAGE_F), 'length': 255, 'name': '{}'.format(self.names.COL_RRR_T_EFFECTIVE_USAGE_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_RRR_T_NAMESPACE_F), 'length': 255, 'name': '{}'.format(self.names.COL_RRR_T_NAMESPACE_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_RRR_T_LOCAL_ID_F), 'length': 255, 'name': '{}'.format(self.names.COL_RRR_T_LOCAL_ID_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_RRR_PARTY_T_OP_PARTY_F), 'length': -1, 'name': '{}'.format(self.names.COL_RRR_PARTY_T_OP_PARTY_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F), 'length': -1, 'name': '{}'.format(self.names.COL_RRR_PARTY_T_OP_GROUP_PARTY_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_BAUNIT_RRR_T_UNIT_F), 'length': -1, 'name': '{}'.format(self.names.COL_BAUNIT_RRR_T_UNIT_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16}
            ]
        elif layer_name == self.names.OP_RIGHT_OF_WAY_T:
            mapping = [
                {'expression': '"{}"'.format(self.names.OP_RIGHT_OF_WAY_T_RIGHT_OF_WAY_AREA_F), 'length': 15, 'name': '{}'.format(self.names.OP_RIGHT_OF_WAY_T_RIGHT_OF_WAY_AREA_F), 'precision': 1, 'type': 6},
                {'expression': '"{}"'.format(self.names.COL_SPATIAL_UNIT_T_DIMENSION_F), 'length': -1, 'name': '{}'.format(self.names.COL_SPATIAL_UNIT_T_DIMENSION_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_SPATIAL_UNIT_T_LABEL_F), 'length': 255, 'name': '{}'.format(self.names.COL_SPATIAL_UNIT_T_LABEL_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_SPATIAL_UNIT_T_SURFACE_RELATION_F), 'length': -1, 'name': '{}'.format(self.names.COL_SPATIAL_UNIT_T_SURFACE_RELATION_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_SPATIAL_UNIT_T_NAMESPACE_F), 'length': 255, 'name': '{}'.format(self.names.COL_SPATIAL_UNIT_T_NAMESPACE_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_SPATIAL_UNIT_T_LOCAL_ID_F), 'length': 255, 'name': '{}'.format(self.names.COL_SPATIAL_UNIT_T_LOCAL_ID_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16}
            ]
        elif layer_name == self.names.EXT_ADDRESS_S:
            mapping = [
                {'expression': '"{}"'.format(self.names.EXT_ADDRESS_S_ADDRESS_TYPE_F), 'length': -1, 'name': '{}'.format(self.names.EXT_ADDRESS_S_ADDRESS_TYPE_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.EXT_ADDRESS_S_IS_MAIN_ADDRESS_F), 'length': -1, 'name': '{}'.format(self.names.EXT_ADDRESS_S_IS_MAIN_ADDRESS_F), 'precision': -1, 'type': 1},
                {'expression': '"{}"'.format(self.names.EXT_ADDRESS_S_POSTAL_CODE_F), 'length': 255, 'name': '{}'.format(self.names.EXT_ADDRESS_S_POSTAL_CODE_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.EXT_ADDRESS_S_MAIN_ROAD_CLASS_F), 'length': -1, 'name': '{}'.format(self.names.EXT_ADDRESS_S_MAIN_ROAD_CLASS_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.EXT_ADDRESS_S_VALUE_MAIN_ROAD_F), 'length': 100, 'name': '{}'.format(self.names.EXT_ADDRESS_S_VALUE_MAIN_ROAD_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.EXT_ADDRESS_S_LETTER_MAIN_ROAD_F), 'length': 20, 'name': '{}'.format(self.names.EXT_ADDRESS_S_LETTER_MAIN_ROAD_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.EXT_ADDRESS_S_CITY_SECTOR_F), 'length': -1, 'name': '{}'.format(self.names.EXT_ADDRESS_S_CITY_SECTOR_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.EXT_ADDRESS_S_VALUE_GENERATOR_ROAD_F), 'length': 100, 'name': '{}'.format(self.names.EXT_ADDRESS_S_VALUE_GENERATOR_ROAD_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.EXT_ADDRESS_S_LETTER_GENERATOR_ROAD_F), 'length': 20, 'name': '{}'.format(self.names.EXT_ADDRESS_S_LETTER_GENERATOR_ROAD_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.EXT_ADDRESS_S_PARCEL_NUMBER_F), 'length': 20, 'name': '{}'.format(self.names.EXT_ADDRESS_S_PARCEL_NUMBER_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.EXT_ADDRESS_S_PARCEL_SECTOR_F), 'length': -1, 'name': '{}'.format(self.names.EXT_ADDRESS_S_PARCEL_SECTOR_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.EXT_ADDRESS_S_COMPLEMENT_F), 'length': 255, 'name': '{}'.format(self.names.EXT_ADDRESS_S_COMPLEMENT_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.EXT_ADDRESS_S_PARCEL_NAME_F), 'length': 255, 'name': '{}'.format(self.names.EXT_ADDRESS_S_PARCEL_NAME_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.EXT_ADDRESS_S_OP_BUILDING_F), 'length': -1, 'name': '{}'.format(self.names.EXT_ADDRESS_S_OP_BUILDING_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.EXT_ADDRESS_S_OP_PLOT_F), 'length': -1, 'name': '{}'.format(self.names.EXT_ADDRESS_S_OP_PLOT_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.EXT_ADDRESS_S_OP_RIGHT_OF_WAY_F), 'length': -1, 'name': '{}'.format(self.names.EXT_ADDRESS_S_OP_RIGHT_OF_WAY_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.EXT_ADDRESS_S_OP_BUILDING_UNIT_F), 'length': -1, 'name': '{}'.format(self.names.EXT_ADDRESS_S_OP_BUILDING_UNIT_F), 'precision': 0, 'type': 4}
            ]
        # --------------------------------
        # UNIQUE CADASTRAL FORM MODEL
        # --------------------------------
        elif layer_name == UNIQUE_CADASTRAL_FORM_TABLE:
            mapping = [
                {'expression': '"corregimiento"', 'length': 100, 'name': 'corregimiento', 'precision': -1, 'type': 10},
                {'expression': '"localidad_comuna"', 'length': 100, 'name': 'localidad_comuna', 'precision': -1, 'type': 10},
                {'expression': '"barrio_vereda"', 'length': 100, 'name': 'barrio_vereda', 'precision': -1, 'type': 10},
                {'expression': '"formalidad"', 'length': -1, 'name': 'formalidad', 'precision': 0, 'type': 4},
                {'expression': '"destinacion_economica"', 'length': -1, 'name': 'destinacion_economica', 'precision': 0, 'type': 4},
                {'expression': '"clase_suelo"', 'length': -1, 'name': 'clase_suelo', 'precision': 0, 'type': 4},
                {'expression': '"categoria_suelo"', 'length': -1, 'name': 'categoria_suelo', 'precision': 0, 'type': 4},
                {'expression': '"tiene_fmi"', 'length': -1, 'name': 'tiene_fmi', 'precision': -1, 'type': 1},
                {'expression': '"fecha_inicio_tenencia"', 'length': -1, 'name': 'fecha_inicio_tenencia', 'precision': -1, 'type': 14},
                {'expression': '"numero_predial_predio_matriz"', 'length': 30, 'name': 'numero_predial_predio_matriz', 'precision': -1, 'type': 10},
                {'expression': '"observaciones"', 'length': 500, 'name': 'observaciones', 'precision': -1, 'type': 10},
                {'expression': '"fecha_visita_predial"', 'length': -1, 'name': 'fecha_visita_predial', 'precision': -1, 'type': 14},
                {'expression': '"nombre_reconocedor"', 'length': 255, 'name': 'nombre_reconocedor', 'precision': -1, 'type': 10},
                {'expression': '"op_predio"', 'length': -1, 'name': 'op_predio', 'precision': 0, 'type': 4}
            ]
        elif layer_name == UNIQUE_CADASTRAL_FORM_CONTACT_VISIT_TABLE:
            mapping = [
                {'expression': '"nombre_quien_atendio"', 'length': 255, 'name': 'nombre_quien_atendio', 'precision': -1, 'type': 10},
                {'expression': '"relacion_con_predio"', 'length': 100, 'name': 'relacion_con_predio', 'precision': -1, 'type': 10},
                {'expression': '"domicilio_notificaciones"', 'length': 255, 'name': 'domicilio_notificaciones', 'precision': -1, 'type': 10},
                {'expression': '"celular"', 'length': 20, 'name': 'celular', 'precision': -1, 'type': 10},
                {'expression': '"correo_electronico"', 'length': 100, 'name': 'correo_electronico', 'precision': -1, 'type': 10},
                {'expression': '"autoriza_notificaciones"', 'length': -1, 'name': 'autoriza_notificaciones', 'precision': -1, 'type': 1},
                {'expression': '"fcm_formulario"', 'length': -1, 'name': 'fcm_formulario', 'precision': 0, 'type': 4}
            ]
        # --------------------------------
        # VALUATION MODEL
        # --------------------------------
        elif layer_name == VALUATION_BUILDING_UNIT_TABLE:
            mapping = [
                {'expression': '"tipo_unidad_construccion"', 'length': -1, 'name': 'tipo_unidad_construccion', 'precision': 0, 'type': 4},
                {'expression': '"puntuacion"', 'length': -1, 'name': 'puntuacion', 'precision': 0, 'type': 2},
                {'expression': '"valor_m2_construccion"', 'length': 16, 'name': 'valor_m2_construccion', 'precision': 1, 'type': 6},
                {'expression': '"anio_construccion"', 'length': -1, 'name': 'anio_construccion', 'precision': 0, 'type': 2},
                {'expression': '"observaciones"', 'length': 255, 'name': 'observaciones', 'precision': -1, 'type': 10},
                {'expression': '"op_unidad_construccion"', 'length': -1, 'name': 'op_unidad_construccion', 'precision': 0, 'type': 4}
            ]
        elif layer_name == VALUATION_COMPONENT_BUILDING:
            mapping = [
                {'expression': '"tipo_componente"', 'length': -1, 'name': 'tipo_componente', 'precision': 0, 'type': 4},
                {'expression': '"cantidad"', 'length': -1, 'name': 'cantidad', 'precision': 0, 'type': 2},
                {'expression': '"av_unidad_construccion"', 'length': -1, 'name': 'av_unidad_construccion', 'precision': 0, 'type': 4}
            ]
        elif layer_name == VALUATION_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_TABLE:
            mapping = [
                {'expression': '"tipo_anexo"', 'length': -1, 'name': 'tipo_anexo', 'precision': 0, 'type': 4},
                {'expression': '"descripcion_anexo"', 'length': 256, 'name': 'descripcion_anexo', 'precision': -1, 'type': 10},
                {'expression': '"puntaje_anexo"', 'length': 2, 'name': 'puntaje_anexo', 'precision': -1, 'type': 10},
                {'expression': '"av_unidad_construccion"', 'length': -1, 'name': 'av_unidad_construccion', 'precision': 0, 'type': 4}
            ]
        elif layer_name == VALUATION_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_TABLE:
            mapping = [
                {'expression': '"tipo_calificar"', 'length': -1, 'name': 'tipo_calificar', 'precision': 0, 'type': 4},
                {'expression': '"total_calificacion"', 'length': -1, 'name': 'total_calificacion', 'precision': 0, 'type': 2},
                {'expression': '"av_unidad_construccion"', 'length': -1, 'name': 'av_unidad_construccion', 'precision': 0, 'type': 4}
            ]
        elif layer_name == VALUATION_GROUP_QUALIFICATION:
            mapping = [
                {'expression': '"clase_calificacion"', 'length': -1, 'name': 'clase_calificacion', 'precision': 0, 'type': 4},
                {'expression': '"conservacion"', 'length': -1, 'name': 'conservacion', 'precision': 0, 'type': 4},
                {'expression': '"subtotal"', 'length': -1, 'name': 'subtotal', 'precision': 0, 'type': 2},
                {'expression': '"av_calificacion_convencional"', 'length': -1, 'name': 'av_calificacion_convencional', 'precision': 0, 'type': 4}
            ]
        elif layer_name == VALUATION_BUILDING_OBJECT:
            mapping = [
                {'expression': '"puntos"', 'length': -1, 'name': 'puntos', 'precision': 0, 'type': 2},
                {'expression': '"caracteristica"', 'length': 255, 'name': 'caracteristica', 'precision': -1, 'type': 10},
                {'expression': '"av_grupo_calificacion"', 'length': -1, 'name': 'av_grupo_calificacion', 'precision': 0, 'type': 4}
            ]
        elif layer_name == VALUATION_GEOECONOMIC_ZONE_TABLE:
            mapping = [
                {'expression': '"identificador"', 'length': 20, 'name': 'identificador', 'precision': -1, 'type': 10},
                {'expression': '"valor"', 'length': -1, 'name': 'valor', 'precision': 0, 'type': 2}
            ]
        elif layer_name == VALUATION_PHYSICAL_ZONE_TABLE:
            mapping = [
                {'expression': '"identificador"', 'length': 20, 'name': 'identificador', 'precision': -1, 'type': 10}
            ]

        # If the user wants to enable automatic fields...
        if QSettings().value('Asistente-LADM_COL/automatic_values/automatic_values_in_batch_mode', True, bool):
            self.set_automatic_values(mapping, layer_name, qgis_utils)

        return mapping

    def get_refactor_fields_mapping_resolve_domains(self, layer_name, qgis_utils):
        names = Names()
        mapping = []

        # --------------------------------
        # OPERATION MODEL
        # --------------------------------
        if layer_name == self.names.OP_BOUNDARY_POINT_T:
            mapping = [
                {'expression': '"{}"'.format(self.names.OP_BOUNDARY_POINT_T_ID_F), 'length': 255, 'name': '{}'.format(self.names.OP_BOUNDARY_POINT_T_ID_F), 'precision': -1, 'type': 10},
                 {'expression': "get_domain_code_from_value('{}', {}, True, False)".format(self.names.OP_POINT_TYPE_D, self.names.OP_BOUNDARY_POINT_T_POINT_TYPE_F), 'length': -1, 'name': '{}'.format(self.names.OP_BOUNDARY_POINT_T_POINT_TYPE_F), 'precision': 0, 'type': 4},
                 {'expression': "get_domain_code_from_value('{}', {}, True, False)".format(self.names.OP_AGREEMENT_TYPE_D, self.names.OP_BOUNDARY_POINT_T_AGREEMENT_F), 'length': -1, 'name': '{}'.format(self.names.OP_BOUNDARY_POINT_T_AGREEMENT_F), 'precision': 0, 'type': 4},
                 {'expression': "get_domain_code_from_value('{}', {}, True, False)".format(self.names.OP_PHOTO_IDENTIFICATION_TYPE_D, self.names.OP_BOUNDARY_POINT_T_PHOTO_IDENTIFICATION_F), 'length': -1, 'name': '{}'.format(self.names.OP_BOUNDARY_POINT_T_PHOTO_IDENTIFICATION_F), 'precision': 0, 'type': 4},
                 {'expression': "get_domain_code_from_value('{}', {}, True, False)".format(self.names.OP_LOCATION_POINT_TYPE_D, self.names.OP_BOUNDARY_POINT_T_POINT_LOCATION_F), 'length': -1, 'name': '{}'.format(self.names.OP_BOUNDARY_POINT_T_POINT_LOCATION_F), 'precision': 0, 'type': 4},
                 {'expression': '"{}"'.format(self.names.OP_BOUNDARY_POINT_T_HORIZONTAL_ACCURACY_F), 'length': -1, 'name': '{}'.format(self.names.OP_BOUNDARY_POINT_T_HORIZONTAL_ACCURACY_F), 'precision': 0, 'type': 2},
                 {'expression': '"{}"'.format(self.names.OP_BOUNDARY_POINT_T_VERTICAL_ACCURACY_F), 'length': -1, 'name': '{}'.format(self.names.OP_BOUNDARY_POINT_T_VERTICAL_ACCURACY_F), 'precision': 0, 'type': 2},
                 {'expression': "get_domain_code_from_value('{}', {}, True, False)".format(self.names.COL_INTERPOLATION_TYPE_D, self.names.COL_POINT_T_INTERPOLATION_POSITION_F), 'length': -1, 'name': '{}'.format(self.names.COL_POINT_T_INTERPOLATION_POSITION_F), 'precision': 0, 'type': 4},
                 {'expression': "get_domain_code_from_value('{}', {}, True, False)".format(self.names.COL_MONUMENTATION_TYPE_D, self.names.COL_POINT_T_MONUMENTATION_F), 'length': -1, 'name': '{}'.format(self.names.COL_POINT_T_MONUMENTATION_F), 'precision': 0, 'type': 4},
                 {'expression': "get_domain_code_from_value('{}', {}, True, False)".format(self.names.COL_PRODUCTION_METHOD_TYPE_D, self.names.COL_POINT_T_PRODUCTION_METHOD_F), 'length': -1, 'name': '{}'.format(self.names.COL_POINT_T_PRODUCTION_METHOD_F), 'precision': 0, 'type': 4},
                 {'expression': '"{}"'.format(self.names.COL_POINT_T_NAMESPACE_F), 'length': 255, 'name': '{}'.format(self.names.COL_POINT_T_NAMESPACE_F), 'precision': -1, 'type': 10},
                 {'expression': '"{}"'.format(self.names.COL_POINT_T_LOCAL_ID_F), 'length': 255, 'name': '{}'.format(self.names.COL_POINT_T_LOCAL_ID_F), 'precision': -1, 'type': 10},
                 {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16},
                 {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16}
            ]
        elif layer_name == self.names.OP_SURVEY_POINT_T:
            mapping = [
                {'expression': '"{}"'.format(self.names.OP_SURVEY_POINT_T_ID_F), 'length': 255, 'name': '{}'.format(self.names.OP_SURVEY_POINT_T_ID_F), 'precision': -1, 'type': 10},
                {'expression': "get_domain_code_from_value('{}', {}, True, False)".format(self.names.OP_POINT_TYPE_D, self.names.OP_SURVEY_POINT_T_POINT_TYPE_F), 'length': -1, 'name': '{}'.format(self.names.OP_SURVEY_POINT_T_POINT_TYPE_F), 'precision': 0, 'type': 4},
                {'expression': "get_domain_code_from_value('{}', {}, True, False)".format(self.names.OP_SURVEY_POINT_TYPE_D, self.names.OP_SURVEY_POINT_T_SURVEY_POINT_TYPE_F), 'length': -1, 'name': '{}'.format(self.names.OP_SURVEY_POINT_T_SURVEY_POINT_TYPE_F), 'precision': 0, 'type': 4},
                {'expression': "get_domain_code_from_value('{}', {}, True, False)".format(self.names.OP_PHOTO_IDENTIFICATION_TYPE_D, self.names.OP_SURVEY_POINT_T_PHOTO_IDENTIFICATION_F),'length': -1, 'name': '{}'.format(self.names.OP_SURVEY_POINT_T_PHOTO_IDENTIFICATION_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.OP_SURVEY_POINT_T_HORIZONTAL_ACCURACY_F), 'length': -1, 'name': '{}'.format(self.names.OP_SURVEY_POINT_T_HORIZONTAL_ACCURACY_F), 'precision': 0, 'type': 2},
                {'expression': '"{}"'.format(self.names.OP_SURVEY_POINT_T_VERTICAL_ACCURACY_F), 'length': -1, 'name': '{}'.format(self.names.OP_SURVEY_POINT_T_VERTICAL_ACCURACY_F), 'precision': 0, 'type': 2},
                {'expression': "get_domain_code_from_value('{}', {}, True, False)".format(self.names.COL_INTERPOLATION_TYPE_D, self.names.COL_POINT_T_INTERPOLATION_POSITION_F), 'length': -1, 'name': '{}'.format(self.names.COL_POINT_T_INTERPOLATION_POSITION_F), 'precision': 0, 'type': 4},
                {'expression': "get_domain_code_from_value('{}', {}, True, False)".format(self.names.COL_MONUMENTATION_TYPE_D, self.names.COL_POINT_T_MONUMENTATION_F), 'length': -1, 'name': '{}'.format(self.names.COL_POINT_T_MONUMENTATION_F), 'precision': 0, 'type': 4},
                {'expression': "get_domain_code_from_value('{}', {}, True, False)".format(self.names.COL_PRODUCTION_METHOD_TYPE_D, self.names.COL_POINT_T_PRODUCTION_METHOD_F), 'length': -1, 'name': '{}'.format(self.names.COL_POINT_T_PRODUCTION_METHOD_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_POINT_T_NAMESPACE_F), 'length': 255, 'name': '{}'.format(self.names.COL_POINT_T_NAMESPACE_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_POINT_T_LOCAL_ID_F), 'length': 255, 'name': '{}'.format(self.names.COL_POINT_T_LOCAL_ID_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'precision': -1,'type': 16}
            ]
        elif layer_name == self.names.OP_CONTROL_POINT_T:
            mapping = [
                {'expression': '"{}"'.format(self.names.OP_CONTROL_POINT_T_ID_F), 'length': 255, 'name': '{}'.format(self.names.OP_CONTROL_POINT_T_ID_F), 'precision': -1, 'type': 10},
                {'expression': "get_domain_code_from_value('{}', {}, True, False)".format(self.names.OP_POINT_TYPE_D, self.names.OP_CONTROL_POINT_T_POINT_TYPE_F), 'length': -1, 'name': '{}'.format(self.names.OP_CONTROL_POINT_T_POINT_TYPE_F), 'precision': 0, 'type': 4},
                {'expression': "get_domain_code_from_value('{}', {}, True, False)".format(self.names.OP_CONTROL_POINT_TYPE_D, self.names.OP_CONTROL_POINT_T_CONTROL_POINT_TYPE_F), 'length': -1, 'name': '{}'.format(self.names.OP_CONTROL_POINT_T_CONTROL_POINT_TYPE_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.OP_CONTROL_POINT_T_HORIZONTAL_ACCURACY_F), 'length': -1, 'name': '{}'.format(self.names.OP_CONTROL_POINT_T_HORIZONTAL_ACCURACY_F), 'precision': 0, 'type': 2},
                {'expression': '"{}"'.format(self.names.OP_CONTROL_POINT_T_VERTICAL_ACCURACY_F), 'length': -1, 'name': '{}'.format(self.names.OP_CONTROL_POINT_T_VERTICAL_ACCURACY_F), 'precision': 0, 'type': 2},
                {'expression': "get_domain_code_from_value('{}', {}, True, False)".format(self.names.COL_INTERPOLATION_TYPE_D, self.names.COL_POINT_T_INTERPOLATION_POSITION_F), 'length': -1, 'name': '{}'.format(self.names.COL_POINT_T_INTERPOLATION_POSITION_F), 'precision': 0, 'type': 4},
                {'expression': "get_domain_code_from_value('{}', {}, True, False)".format(self.names.COL_MONUMENTATION_TYPE_D, self.names.COL_POINT_T_MONUMENTATION_F), 'length': -1, 'name': '{}'.format(self.names.COL_POINT_T_MONUMENTATION_F), 'precision': 0, 'type': 4},
                {'expression': "get_domain_code_from_value('{}', {}, True, False)".format(self.names.COL_PRODUCTION_METHOD_TYPE_D, self.names.COL_POINT_T_PRODUCTION_METHOD_F), 'length': -1, 'name': '{}'.format(self.names.COL_POINT_T_PRODUCTION_METHOD_F), 'precision': 0, 'type': 4},
                {'expression': '"{}"'.format(self.names.COL_POINT_T_NAMESPACE_F), 'length': 255, 'name': '{}'.format(self.names.COL_POINT_T_NAMESPACE_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.COL_POINT_T_LOCAL_ID_F), 'length': 255, 'name': '{}'.format(self.names.COL_POINT_T_LOCAL_ID_F), 'precision': -1, 'type': 10},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16},
                {'expression': '"{}"'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(self.names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16}
            ]

        # If the user wants to enable automatic fields...
        if QSettings().value('Asistente-LADM_COL/automatic_values/automatic_values_in_batch_mode', True, bool):
            self.set_automatic_values(mapping, layer_name, qgis_utils)

        return mapping

    def set_automatic_values(self, mapping, layer_name, qgis_utils):
        # Now see if we can adjust the mapping depending on user settings
        ns_enabled, ns_field, ns_value = qgis_utils.get_namespace_field_and_value(layer_name)
        lid_enabled, lid_field, lid_value = qgis_utils.get_local_id_field_and_value(layer_name)

        for field in mapping:
            if ns_enabled and ns_field:
                if field['name'] == ns_field:
                    field['expression'] = '{}'.format(ns_value)

            if lid_enabled and lid_field:
                if field['name'] == lid_field:
                    field['expression'] = '{}'.format(lid_value)

            if field['name'] == self.names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F:
                field['expression'] = 'now()'