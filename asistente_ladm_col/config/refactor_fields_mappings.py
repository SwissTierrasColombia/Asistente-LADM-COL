from qgis.PyQt.QtCore import QSettings
from .table_mapping_config import *

def get_refactor_fields_mapping(layer_name, qgis_utils):
    names = Names()
    mapping = []

    # --------------------------------
    # OPERATION MODEL
    # --------------------------------
    if layer_name == names.OP_BOUNDARY_POINT_T:
        mapping = [
            {'expression': '"{}"'.format(names.OP_BOUNDARY_POINT_T_ID_F), 'length': 255, 'name': '{}'.format(names.OP_BOUNDARY_POINT_T_ID_F), 'precision': -1, 'type': 10},
            {'expression': '"{}"'.format(names.OP_BOUNDARY_POINT_T_POINT_TYPE_F), 'length': -1, 'name': '{}'.format(names.OP_BOUNDARY_POINT_T_POINT_TYPE_F), 'precision': 0, 'type': 4},
            {'expression': '"{}"'.format(names.OP_BOUNDARY_POINT_T_AGREEMENT_F), 'length': -1, 'name': '{}'.format(names.OP_BOUNDARY_POINT_T_AGREEMENT_F), 'precision': 0, 'type': 4},
            {'expression': '"{}"'.format(names.OP_BOUNDARY_POINT_T_PHOTO_IDENTIFICATION_F), 'length': -1, 'name': '{}'.format(names.OP_BOUNDARY_POINT_T_PHOTO_IDENTIFICATION_F), 'precision': 0, 'type': 4},
            {'expression': '"{}"'.format(names.OP_BOUNDARY_POINT_T_POINT_LOCATION_F), 'length': -1, 'name': '{}'.format(names.OP_BOUNDARY_POINT_T_POINT_LOCATION_F), 'precision': 0, 'type': 4},
            {'expression': '"{}"'.format(names.OP_BOUNDARY_POINT_T_HORIZONTAL_ACCURACY_F), 'length': -1, 'name': '{}'.format(names.OP_BOUNDARY_POINT_T_HORIZONTAL_ACCURACY_F), 'precision': 0, 'type': 2},
            {'expression': '"{}"'.format(names.OP_BOUNDARY_POINT_T_VERTICAL_ACCURACY_F), 'length': -1, 'name': '{}'.format(names.OP_BOUNDARY_POINT_T_VERTICAL_ACCURACY_F), 'precision': 0, 'type': 2},
            {'expression': '"{}"'.format(names.COL_POINT_T_INTERPOLATION_POSITION_F), 'length': -1, 'name': '{}'.format(names.COL_POINT_T_INTERPOLATION_POSITION_F), 'precision': 0, 'type': 4},
            {'expression': '"{}"'.format(names.COL_POINT_T_MONUMENTATION_F), 'length': -1, 'name': '{}'.format(names.COL_POINT_T_MONUMENTATION_F), 'precision': 0, 'type': 4},
            {'expression': '"{}"'.format(names.COL_POINT_T_PRODUCTION_METHOD_F), 'length': -1, 'name': '{}'.format(names.COL_POINT_T_PRODUCTION_METHOD_F), 'precision': 0, 'type': 4},
            {'expression': '"{}"'.format(names.COL_POINT_T_NAMESPACE_F), 'length': 255, 'name': '{}'.format(names.COL_POINT_T_NAMESPACE_F), 'precision': -1, 'type': 10},
            {'expression': '"{}"'.format(names.COL_POINT_T_LOCAL_ID_F), 'length': 255, 'name': '{}'.format(names.COL_POINT_T_LOCAL_ID_F), 'precision': -1, 'type': 10},
            {'expression': '"{}"'.format(names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(names.VERSIONED_OBJECT_T_BEGIN_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16},
            {'expression': '"{}"'.format(names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'length': -1, 'name': '{}'.format(names.VERSIONED_OBJECT_T_END_LIFESPAN_VERSION_F), 'precision': -1, 'type': 16}
        ]
    elif layer_name == names.OP_SURVEY_POINT_T:
        mapping = [
            {'expression': '"id_punto_levantamiento"', 'length': 255, 'name': 'id_punto_levantamiento', 'precision': -1, 'type': 10},
            {'expression': '"puntotipo"', 'length': -1, 'name': 'puntotipo', 'precision': 0, 'type': 4},
            {'expression': '"tipo_punto_levantamiento"', 'length': -1, 'name': 'tipo_punto_levantamiento', 'precision': 0, 'type': 4},
            {'expression': '"fotoidentificacion"', 'length': -1, 'name': 'fotoidentificacion', 'precision': 0, 'type': 4},
            {'expression': '"exactitud_horizontal"', 'length': -1, 'name': 'exactitud_horizontal', 'precision': 0, 'type': 2},
            {'expression': '"exactitud_vertical"', 'length': -1, 'name': 'exactitud_vertical', 'precision': 0, 'type': 2},
            {'expression': '"posicion_interpolacion"', 'length': -1, 'name': 'posicion_interpolacion', 'precision': 0, 'type': 4},
            {'expression': '"monumentacion"', 'length': -1, 'name': 'monumentacion', 'precision': 0, 'type': 4},
            {'expression': '"metodoproduccion"', 'length': -1, 'name': 'metodoproduccion', 'precision': 0, 'type': 4},
            {'expression': '"espacio_de_nombres"', 'length': 255, 'name': 'espacio_de_nombres', 'precision': -1, 'type': 10},
            {'expression': '"local_id"', 'length': 255, 'name': 'local_id', 'precision': -1, 'type': 10},
            {'expression': '"comienzo_vida_util_version"', 'length': -1, 'name': 'comienzo_vida_util_version', 'precision': -1, 'type': 16},
            {'expression': '"fin_vida_util_version"', 'length': -1, 'name': 'fin_vida_util_version', 'precision': -1, 'type': 16}
        ]
    elif layer_name == names.OP_CONTROL_POINT_T:
        mapping = [
            {'expression': '"id_punto_control"', 'length': 255, 'name': 'id_punto_control', 'precision': -1, 'type': 10},
            {'expression': '"puntotipo"', 'length': -1, 'name': 'puntotipo', 'precision': 0, 'type': 4},
            {'expression': '"tipo_punto_control"', 'length': -1, 'name': 'tipo_punto_control', 'precision': 0, 'type': 4},
            {'expression': '"exactitud_horizontal"', 'length': -1, 'name': 'exactitud_horizontal', 'precision': 0, 'type': 2},
            {'expression': '"exactitud_vertical"', 'length': -1, 'name': 'exactitud_vertical', 'precision': 0, 'type': 2},
            {'expression': '"posicion_interpolacion"', 'length': -1, 'name': 'posicion_interpolacion', 'precision': 0, 'type': 4},
            {'expression': '"monumentacion"', 'length': -1, 'name': 'monumentacion', 'precision': 0, 'type': 4},
            {'expression': '"metodoproduccion"', 'length': -1, 'name': 'metodoproduccion', 'precision': 0, 'type': 4},
            {'expression': '"espacio_de_nombres"', 'length': 255, 'name': 'espacio_de_nombres', 'precision': -1, 'type': 10},
            {'expression': '"local_id"', 'length': 255, 'name': 'local_id', 'precision': -1, 'type': 10},
            {'expression': '"comienzo_vida_util_version"', 'length': -1, 'name': 'comienzo_vida_util_version', 'precision': -1, 'type': 16},
            {'expression': '"fin_vida_util_version"', 'length': -1, 'name': 'fin_vida_util_version', 'precision': -1, 'type': 16}
        ]
    elif layer_name == names.OP_BOUNDARY_T:
        mapping = [
            {'expression': '"longitud"', 'length': 6, 'name': 'longitud', 'precision': 1, 'type': 6},
            {'expression': '"localizacion_textual"', 'length': 255, 'name': 'localizacion_textual', 'precision': -1, 'type': 10},
            {'expression': '"espacio_de_nombres"', 'length': 255, 'name': 'espacio_de_nombres', 'precision': -1, 'type': 10},
            {'expression': '"local_id"', 'length': 255, 'name': 'local_id', 'precision': -1, 'type': 10},
            {'expression': '"comienzo_vida_util_version"', 'length': -1, 'name': 'comienzo_vida_util_version', 'precision': -1, 'type': 16},
            {'expression': '"fin_vida_util_version"', 'length': -1, 'name': 'fin_vida_util_version', 'precision': -1, 'type': 16}
        ]
    elif layer_name == names.OP_PLOT_T:
        mapping = [
            {'expression': '"area_terreno"', 'length': 15, 'name': 'area_terreno', 'precision': 1, 'type': 6},
            {'expression': '"avaluo_terreno"', 'length': 16, 'name': 'avaluo_terreno', 'precision': 1, 'type': 6},
            {'expression': '"dimension"', 'length': -1, 'name': 'dimension', 'precision': 0, 'type': 4},
            {'expression': '"etiqueta"', 'length': 255, 'name': 'etiqueta', 'precision': -1, 'type': 10},
            {'expression': '"relacion_superficie"', 'length': -1, 'name': 'relacion_superficie', 'precision': 0, 'type': 4},
            {'expression': '"espacio_de_nombres"', 'length': 255, 'name': 'espacio_de_nombres', 'precision': -1, 'type': 10},
            {'expression': '"local_id"', 'length': 255, 'name': 'local_id', 'precision': -1, 'type': 10},
            {'expression': '"comienzo_vida_util_version"', 'length': -1, 'name': 'comienzo_vida_util_version', 'precision': -1, 'type': 16},
            {'expression': '"fin_vida_util_version"', 'length': -1, 'name': 'fin_vida_util_version', 'precision': -1, 'type': 16}
        ]
    elif layer_name == names.OP_PARCEL_T:
        mapping = [
            {'expression': '"departamento"', 'length': 2, 'name': 'departamento', 'precision': -1, 'type': 10},
            {'expression': '"municipio"', 'length': 3, 'name': 'municipio', 'precision': -1, 'type': 10},
            {'expression': '"nupre"', 'length': 11, 'name': 'nupre', 'precision': -1, 'type': 10},
            {'expression': '"codigo_orip"', 'length': 3, 'name': 'codigo_orip', 'precision': -1, 'type': 10},
            {'expression': '"matricula_inmobiliaria"', 'length': 80, 'name': 'matricula_inmobiliaria', 'precision': -1, 'type': 10},
            {'expression': '"numero_predial"', 'length': 30, 'name': 'numero_predial', 'precision': -1, 'type': 10},
            {'expression': '"numero_predial_anterior"', 'length': 20, 'name': 'numero_predial_anterior', 'precision': -1, 'type': 10},
            {'expression': '"avaluo_predio"', 'length': 16, 'name': 'avaluo_predio', 'precision': 1, 'type': 6},
            {'expression': '"condicion_predio"', 'length': -1, 'name': 'condicion_predio', 'precision': 0, 'type': 4},
            {'expression': '"tipo"', 'length': -1, 'name': 'tipo', 'precision': 0, 'type': 4},
            {'expression': '"direccion"', 'length': 255, 'name': 'direccion', 'precision': -1, 'type': 10},
            {'expression': '"nombre"', 'length': 255, 'name': 'nombre', 'precision': -1, 'type': 10},
            {'expression': '"espacio_de_nombres"', 'length': 255, 'name': 'espacio_de_nombres', 'precision': -1, 'type': 10},
            {'expression': '"local_id"', 'length': 255, 'name': 'local_id', 'precision': -1, 'type': 10},
            {'expression': '"comienzo_vida_util_version"', 'length': -1, 'name': 'comienzo_vida_util_version', 'precision': -1, 'type': 16},
            {'expression': '"fin_vida_util_version"', 'length': -1, 'name': 'fin_vida_util_version', 'precision': -1, 'type': 16}
        ]
    elif layer_name == names.OP_PARTY_T:
        mapping = [
            {'expression': '"tipo"', 'length': -1, 'name': 'tipo', 'precision': 0, 'type': 4},
            {'expression': '"tipo_documento"', 'length': -1, 'name': 'tipo_documento', 'precision': 0, 'type': 4},
            {'expression': '"documento_identidad"', 'length': 50, 'name': 'documento_identidad', 'precision': -1, 'type': 10},
            {'expression': '"primer_nombre"', 'length': 100, 'name': 'primer_nombre', 'precision': -1, 'type': 10},
            {'expression': '"segundo_nombre"', 'length': 100, 'name': 'segundo_nombre', 'precision': -1, 'type': 10},
            {'expression': '"primer_apellido"', 'length': 100, 'name': 'primer_apellido', 'precision': -1, 'type': 10},
            {'expression': '"segundo_apellido"', 'length': 100, 'name': 'segundo_apellido', 'precision': -1, 'type': 10},
            {'expression': '"sexo"', 'length': -1, 'name': 'sexo', 'precision': 0, 'type': 4},
            {'expression': '"grupo_etnico"', 'length': -1, 'name': 'grupo_etnico', 'precision': 0, 'type': 4},
            {'expression': '"razon_social"', 'length': 255, 'name': 'razon_social', 'precision': -1, 'type': 10},
            {'expression': '"nombre"', 'length': 255, 'name': 'nombre', 'precision': -1, 'type': 10},
            {'expression': '"espacio_de_nombres"', 'length': 255, 'name': 'espacio_de_nombres', 'precision': -1, 'type': 10},
            {'expression': '"local_id"', 'length': 255, 'name': 'local_id', 'precision': -1, 'type': 10},
            {'expression': '"comienzo_vida_util_version"', 'length': -1, 'name': 'comienzo_vida_util_version', 'precision': -1, 'type': 16},
            {'expression': '"fin_vida_util_version"', 'length': -1, 'name': 'fin_vida_util_version', 'precision': -1, 'type': 16}
        ]
    elif layer_name == names.OP_ADMINISTRATIVE_SOURCE_T:
        mapping = [
            {'expression': '"tipo"', 'length': -1, 'name': 'tipo', 'precision': 0, 'type': 4},
            {'expression': '"ente_emisor"', 'length': 255, 'name': 'ente_emisor', 'precision': -1, 'type': 10},
            {'expression': '"observacion"', 'length': 255, 'name': 'observacion', 'precision': -1, 'type': 10},
            {'expression': '"numero_fuente"', 'length': 150, 'name': 'numero_fuente', 'precision': -1, 'type': 10},
            {'expression': '"estado_disponibilidad"', 'length': -1, 'name': 'estado_disponibilidad', 'precision': 0, 'type': 4},
            {'expression': '"tipo_principal"', 'length': -1, 'name': 'tipo_principal', 'precision': 0, 'type': 4},
            {'expression': '"espacio_de_nombres"', 'length': 255, 'name': 'espacio_de_nombres', 'precision': -1, 'type': 10},
            {'expression': '"local_id"', 'length': 255, 'name': 'local_id', 'precision': -1, 'type': 10},
            {'expression': '"oficialidad"', 'length': -1, 'name': 'oficialidad', 'precision': -1, 'type': 1},
            {'expression': '"fecha_documento_fuente"', 'length': -1, 'name': 'fecha_documento_fuente', 'precision': -1, 'type': 14}
        ]
    elif layer_name == names.COL_SPATIAL_SOURCE_T:
        mapping = [
            {'expression': '"tipo"', 'length': -1, 'name': 'tipo', 'precision': 0, 'type': 4},
            {'expression': '"estado_disponibilidad"', 'length': -1, 'name': 'estado_disponibilidad', 'precision': 0, 'type': 4},
            {'expression': '"tipo_principal"', 'length': -1, 'name': 'tipo_principal', 'precision': 0, 'type': 4},
            {'expression': '"espacio_de_nombres"', 'length': 255, 'name': 'espacio_de_nombres', 'precision': -1, 'type': 10},
            {'expression': '"local_id"', 'length': 255, 'name': 'local_id', 'precision': -1, 'type': 10},
            {'expression': '"oficialidad"', 'length': -1, 'name': 'oficialidad', 'precision': -1, 'type': 1},
            {'expression': '"fecha_documento_fuente"', 'length': -1, 'name': 'fecha_documento_fuente', 'precision': -1, 'type': 14}
        ]
    elif layer_name == names.OP_BUILDING_T:
        mapping = [
            {'expression': '"area_construccion"', 'length': 15, 'name': 'area_construccion', 'precision': 1, 'type': 6},
            {'expression': '"numero_pisos"', 'length': -1, 'name': 'numero_pisos', 'precision': 0, 'type': 2},
            {'expression': '"avaluo_construccion"', 'length': 16, 'name': 'avaluo_construccion', 'precision': 1, 'type': 6},
            {'expression': '"dimension"', 'length': -1, 'name': 'dimension', 'precision': 0, 'type': 4},
            {'expression': '"etiqueta"', 'length': 255, 'name': 'etiqueta', 'precision': -1, 'type': 10},
            {'expression': '"relacion_superficie"', 'length': -1, 'name': 'relacion_superficie', 'precision': 0, 'type': 4},
            {'expression': '"espacio_de_nombres"', 'length': 255, 'name': 'espacio_de_nombres', 'precision': -1, 'type': 10},
            {'expression': '"local_id"', 'length': 255, 'name': 'local_id', 'precision': -1, 'type': 10},
            {'expression': '"comienzo_vida_util_version"', 'length': -1, 'name': 'comienzo_vida_util_version', 'precision': -1, 'type': 16},
            {'expression': '"fin_vida_util_version"', 'length': -1, 'name': 'fin_vida_util_version', 'precision': -1, 'type': 16}
        ]
    elif layer_name == names.OP_BUILDING_UNIT_T:
        mapping = [
            {'expression': '"identificador"', 'length': 3, 'name': 'identificador', 'precision': -1, 'type': 10},
            {'expression': '"area_construida"', 'length': 15, 'name': 'area_construida', 'precision': 1, 'type': 6},
            {'expression': '"area_privada_construida"', 'length': 15, 'name': 'area_privada_construida', 'precision': 1, 'type': 6},
            {'expression': '"uso"', 'length': -1, 'name': 'uso', 'precision': 0, 'type': 4},
            {'expression': '"numero_pisos"', 'length': -1, 'name': 'numero_pisos', 'precision': 0, 'type': 2},
            {'expression': '"avaluo_unidad_construccion"', 'length': 16, 'name': 'avaluo_unidad_construccion', 'precision': 1, 'type': 6},
            {'expression': '"piso_ubicacion"', 'length': -1, 'name': 'piso_ubicacion', 'precision': 0, 'type': 2},
            {'expression': '"op_construccion"', 'length': -1, 'name': 'op_construccion', 'precision': 0, 'type': 4},
            {'expression': '"dimension"', 'length': -1, 'name': 'dimension', 'precision': 0, 'type': 4},
            {'expression': '"etiqueta"', 'length': 255, 'name': 'etiqueta', 'precision': -1, 'type': 10},
            {'expression': '"relacion_superficie"', 'length': -1, 'name': 'relacion_superficie', 'precision': 0, 'type': 4},
            {'expression': '"espacio_de_nombres"', 'length': 255, 'name': 'espacio_de_nombres', 'precision': -1, 'type': 10},
            {'expression': '"local_id"', 'length': 255, 'name': 'local_id', 'precision': -1, 'type': 10},
            {'expression': '"comienzo_vida_util_version"', 'length': -1, 'name': 'comienzo_vida_util_version', 'precision': -1, 'type': 16},
            {'expression': '"fin_vida_util_version"', 'length': -1, 'name': 'fin_vida_util_version', 'precision': -1, 'type': 16}
        ]
    elif layer_name == names.OP_RIGHT_T:
        mapping = [
            {'expression': '"tipo"', 'length': -1, 'name': 'tipo', 'precision': 0, 'type': 4},
            {'expression': '"descripcion"', 'length': 255, 'name': 'descripcion', 'precision': -1, 'type': 10},
            {'expression': '"comprobacion_comparte"', 'length': -1, 'name': 'comprobacion_comparte', 'precision': -1, 'type': 1},
            {'expression': '"uso_efectivo"', 'length': 255, 'name': 'uso_efectivo', 'precision': -1, 'type': 10},
            {'expression': '"espacio_de_nombres"', 'length': 255, 'name': 'espacio_de_nombres', 'precision': -1, 'type': 10},
            {'expression': '"local_id"', 'length': 255, 'name': 'local_id', 'precision': -1, 'type': 10},
            {'expression': '"interesado_op_interesado"', 'length': -1, 'name': 'interesado_op_interesado', 'precision': 0, 'type': 4},
            {'expression': '"interesado_op_agrupacion_interesados"', 'length': -1, 'name': 'interesado_op_agrupacion_interesados', 'precision': 0, 'type': 4},
            {'expression': '"unidad"', 'length': -1, 'name': 'unidad', 'precision': 0, 'type': 4},
            {'expression': '"comienzo_vida_util_version"', 'length': -1, 'name': 'comienzo_vida_util_version', 'precision': -1, 'type': 16},
            {'expression': '"fin_vida_util_version"', 'length': -1, 'name': 'fin_vida_util_version', 'precision': -1, 'type': 16}
        ]
    elif layer_name == names.OP_RESTRICTION_T:
        mapping = [
            {'expression': '"tipo"', 'length': -1, 'name': 'tipo', 'precision': 0, 'type': 4},
            {'expression': '"descripcion"', 'length': 255, 'name': 'descripcion', 'precision': -1, 'type': 10},
            {'expression': '"comprobacion_comparte"', 'length': -1, 'name': 'comprobacion_comparte', 'precision': -1, 'type': 1},
            {'expression': '"uso_efectivo"', 'length': 255, 'name': 'uso_efectivo', 'precision': -1, 'type': 10},
            {'expression': '"espacio_de_nombres"', 'length': 255, 'name': 'espacio_de_nombres', 'precision': -1, 'type': 10},
            {'expression': '"local_id"', 'length': 255, 'name': 'local_id', 'precision': -1, 'type': 10},
            {'expression': '"interesado_op_interesado"', 'length': -1, 'name': 'interesado_op_interesado', 'precision': 0, 'type': 4},
            {'expression': '"interesado_op_agrupacion_interesados"', 'length': -1, 'name': 'interesado_op_agrupacion_interesados', 'precision': 0, 'type': 4},
            {'expression': '"unidad"', 'length': -1, 'name': 'unidad', 'precision': 0, 'type': 4},
            {'expression': '"comienzo_vida_util_version"', 'length': -1, 'name': 'comienzo_vida_util_version', 'precision': -1, 'type': 16},
            {'expression': '"fin_vida_util_version"', 'length': -1, 'name': 'fin_vida_util_version', 'precision': -1, 'type': 16}
        ]
    elif layer_name == names.OP_RIGHT_OF_WAY_T:
        mapping = [
            {'expression': '"area_servidumbre"', 'length': 15, 'name': 'area_servidumbre', 'precision': 1, 'type': 6},
            {'expression': '"dimension"', 'length': -1, 'name': 'dimension', 'precision': 0, 'type': 4},
            {'expression': '"etiqueta"', 'length': 255, 'name': 'etiqueta', 'precision': -1, 'type': 10},
            {'expression': '"relacion_superficie"', 'length': -1, 'name': 'relacion_superficie', 'precision': 0, 'type': 4},
            {'expression': '"espacio_de_nombres"', 'length': 255, 'name': 'espacio_de_nombres', 'precision': -1, 'type': 10},
            {'expression': '"local_id"', 'length': 255, 'name': 'local_id', 'precision': -1, 'type': 10},
            {'expression': '"comienzo_vida_util_version"', 'length': -1, 'name': 'comienzo_vida_util_version', 'precision': -1, 'type': 16},
            {'expression': '"fin_vida_util_version"', 'length': -1, 'name': 'fin_vida_util_version', 'precision': -1, 'type': 16}
        ]
    elif layer_name == EXTADDRESS_TABLE:
        mapping = [
            {'expression': '"tipo_direccion"', 'length': -1, 'name': 'tipo_direccion', 'precision': 0, 'type': 4},
            {'expression': '"es_direccion_principal"', 'length': -1, 'name': 'es_direccion_principal', 'precision': -1, 'type': 1},
            {'expression': '"codigo_postal"', 'length': 255, 'name': 'codigo_postal', 'precision': -1, 'type': 10},
            {'expression': '"clase_via_principal"', 'length': -1, 'name': 'clase_via_principal', 'precision': 0, 'type': 4},
            {'expression': '"valor_via_principal"', 'length': 100, 'name': 'valor_via_principal', 'precision': -1, 'type': 10},
            {'expression': '"letra_via_principal"', 'length': 20, 'name': 'letra_via_principal', 'precision': -1, 'type': 10},
            {'expression': '"sector_ciudad"', 'length': -1, 'name': 'sector_ciudad', 'precision': 0, 'type': 4},
            {'expression': '"valor_via_generadora"', 'length': 100, 'name': 'valor_via_generadora', 'precision': -1, 'type': 10},
            {'expression': '"letra_via_generadora"', 'length': 20, 'name': 'letra_via_generadora', 'precision': -1, 'type': 10},
            {'expression': '"numero_predio"', 'length': 20, 'name': 'numero_predio', 'precision': -1, 'type': 10},
            {'expression': '"sector_predio"', 'length': -1, 'name': 'sector_predio', 'precision': 0, 'type': 4},
            {'expression': '"complemento"', 'length': 255, 'name': 'complemento', 'precision': -1, 'type': 10},
            {'expression': '"nombre_predio"', 'length': 255, 'name': 'nombre_predio', 'precision': -1, 'type': 10},
            {'expression': '"op_construccion_ext_direccion_id"', 'length': -1, 'name': 'op_construccion_ext_direccion_id', 'precision': 0, 'type': 4},
            {'expression': '"op_terreno_ext_direccion_id"', 'length': -1, 'name': 'op_terreno_ext_direccion_id', 'precision': 0, 'type': 4},
            {'expression': '"op_servidumbrepaso_ext_direccion_id"', 'length': -1, 'name': 'op_servidumbrepaso_ext_direccion_id', 'precision': 0, 'type': 4},
            {'expression': '"op_unidadconstruccion_ext_direccion_id"', 'length': -1, 'name': 'op_unidadconstruccion_ext_direccion_id', 'precision': 0, 'type': 4}
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

            if field['name'] == VIDA_UTIL_FIELD:
                field['expression'] = 'now()'

    return mapping
