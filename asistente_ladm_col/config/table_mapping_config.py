from qgis.core import (QgsWkbTypes)

BFS_TABLE_BOUNDARY_FIELD = "ccl_lindero"
BFS_TABLE_BOUNDARY_POINT_FIELD = "punto_puntolindero"
BOUNDARY_POINT_TABLE = "puntolindero"
BOUNDARY_TABLE = "lindero"
CONTROL_POINT_TABLE = "puntocontrol"
ID_FIELD = "t_id"
PARCEL_TABLE = "predio"
PLOT_TABLE = "terreno"
LENGTH_FIELD_BOUNDARY_TABLE = "longitud"
LESS_TABLE = "menos"
LESS_TABLE_BOUNDARY_FIELD = "ccl_lindero"
LESS_TABLE_PLOT_FIELD = "eu_terreno"
MORE_BOUNDARY_FACE_STRING_TABLE = "masccl"
MOREBFS_TABLE_BOUNDARY_FIELD = "cclp_lindero"
MOREBFS_TABLE_PLOT_FIELD = "uep_terreno"
POINT_BOUNDARY_FACE_STRING_TABLE = "puntoccl"
SURVEY_POINT_TABLE = "puntolevantamiento"
UEBAUNIT_TABLE = "uebaunit"
UEBAUNIT_TABLE_PARCEL_FIELD = "baunit_predio"
UEBAUNIT_TABLE_PLOT_FIELD = "ue_terreno"
VIDA_UTIL_FIELD_BOUNDARY_TABLE = "comienzo_vida_util_version"
CONSTRUCTION_TABLE = "construccion"

LAYERS_STYLE = {BOUNDARY_TABLE: {QgsWkbTypes.LineGeometry: {'symbology': {'name': 'Simple line', 'color': '#45508a', 'width': '0.16'}, 'label' : None}},
    BOUNDARY_POINT_TABLE: {QgsWkbTypes.PointGeometry:{'symbology': {'name': 'diamond', 'color': '#487bb6', 'size': '2'}, 'label' : {'field_name': 'nombre_punto', 'text_size' : 8 , 'color' : QColor(40,51,105)}}},
    SURVEY_POINT_TABLE: {QgsWkbTypes.PointGeometry: {'symbology': {'name': 'diamond', 'color': '#b2df8a', 'size': '2'}, 'label':{'field_name': 'nombre_punto', 'text_size' : 8 , 'color' : QColor(140,46,0)}}},
    PLOT_TABLE: {QgsWkbTypes.PointGeometry:{'symbology': {'name': 'star', 'color': '#b80808', 'size': '4.8'}, 'label': {'field_name': 'nombre_punto', 'text_size' : 9 , 'color' : QColor(0,0,0)}},
    QgsWkbTypes.PolygonGeometry:{'symbology': {'name': 'Simple fill', 'color': '166,206,227,128', 'outline_color': '131,167,184,128'}, 'label': None}},
    CONSTRUCTION_TABLE: {QgsWkbTypes.PointGeometry:{'symbology': {'name': 'square', 'color': '#000000', 'size': '3'}, 'label': None},
    QgsWkbTypes.PolygonGeometry: {'symbology': {'name': 'Simple fill', 'color': '251,154,153,128', 'outline_color': '148,90,90,128'}, 'label': None}}}