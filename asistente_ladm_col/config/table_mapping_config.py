from qgis.core import QgsWkbTypes
from qgis.PyQt.QtGui import QColor

ADMINISTRATIVE_SOURCE_TABLE = "col_fuenteadministrativa"
ADMINISTRATIVE_SOURCE_TYPE_TABLE = "col_fuenteadministrativatipo"
AVAILABILITY_STATE_TABLE = "col_estadodisponibilidadtipo"
BFS_TABLE_BOUNDARY_FIELD = "ccl_lindero"
BFS_TABLE_BOUNDARY_POINT_FIELD = "punto_puntolindero"
BOUNDARY_POINT_TABLE = "puntolindero"
BOUNDARY_TABLE = "lindero"
CONSTRUCTION_TABLE = "construccion"
CONTROL_POINT_TABLE = "puntocontrol"
DEFAULT_EPSG = "3116"
DEFAULT_TOO_LONG_BOUNDARY_SEGMENTS_TOLERANCE = 200 # meters
ERROR_LAYER_GROUP = "Validation errors"
GENDER_TYPE_TABLE = "col_generotipo"
ID_FIELD = "t_id"
PARCEL_TABLE = "predio"
PLOT_TABLE = "terreno"
LA_BAUNIT_TYPE_TABLE = "la_baunittipo"
LENGTH_FIELD_BOUNDARY_TABLE = "longitud"
LEGAL_PARTY_TABLE = "interesado_juridico"
LEGAL_PARTY_TYPE_TABLE = "col_interesadojuridicotipo"
LESS_TABLE = "menos"
LESS_TABLE_BOUNDARY_FIELD = "ccl_lindero"
LESS_TABLE_PLOT_FIELD = "eu_terreno"
LOCAL_ID_FIELD = "_local_id"
MORE_BOUNDARY_FACE_STRING_TABLE = "masccl"
MOREBFS_TABLE_BOUNDARY_FIELD = "cclp_lindero"
MOREBFS_TABLE_PLOT_FIELD = "uep_terreno"
NAMESPACE_FIELD = "_espacio_de_nombres"
NATURAL_PARTY_TABLE = "interesado_natural"
PARTY_DOCUMENT_TYPE_TABLE = "col_interesadodocumentotipo"
PARTY_TYPE_TABLE = "la_interesadotipo"
POINT_BOUNDARY_FACE_STRING_TABLE = "puntoccl"
PROJECT_GENERATOR_MIN_REQUIRED_VERSION = "3.0.0"
SPATIAL_SOURCE_TABLE = "col_fuenteespacial"
SPATIAL_SOURCE_TYPE_TABLE = "col_fuenteespacialtipo"
SURVEY_POINT_TABLE = "puntolevantamiento"
UEBAUNIT_TABLE = "uebaunit"
UEBAUNIT_TABLE_PARCEL_FIELD = "baunit_predio"
UEBAUNIT_TABLE_PLOT_FIELD = "ue_terreno"
VIDA_UTIL_FIELD_BOUNDARY_TABLE = "comienzo_vida_util_version"

LAYERS_STYLE = {
    BOUNDARY_TABLE: {QgsWkbTypes.LineGeometry: {'symbology': {'name': 'Simple line', 'color': '#45508a', 'width': '0.16'}, 'label' : None}},
    BOUNDARY_POINT_TABLE: {QgsWkbTypes.PointGeometry:{'symbology': {'name': 'diamond', 'color': '#487bb6', 'size': '2'}, 'label' : {'field_name': 'nombre_punto', 'text_size' : 8 , 'color' : QColor(40,51,105)}}},
    SURVEY_POINT_TABLE: {QgsWkbTypes.PointGeometry: {'symbology': {'name': 'diamond', 'color': '#b2df8a', 'size': '2'}, 'label':{'field_name': 'nombre_punto', 'text_size' : 8 , 'color' : QColor(140,46,0)}}},
    PLOT_TABLE: {QgsWkbTypes.PointGeometry:{'symbology': {'name': 'star', 'color': '#b80808', 'size': '4.8'}, 'label': {'field_name': 'nombre_punto', 'text_size' : 9 , 'color' : QColor(0,0,0)}},
        QgsWkbTypes.PolygonGeometry:{'symbology': {'name': 'Simple fill', 'color': '166,206,227,128', 'outline_color': '131,167,184,128'}, 'label': None}},
    CONSTRUCTION_TABLE: {QgsWkbTypes.PointGeometry:{'symbology': {'name': 'square', 'color': '#000000', 'size': '3'}, 'label': None},
        QgsWkbTypes.PolygonGeometry: {'symbology': {'name': 'Simple fill', 'color': '251,154,153,128', 'outline_color': '148,90,90,128'}, 'label': None}}}
