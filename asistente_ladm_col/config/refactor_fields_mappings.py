from qgis.PyQt.QtCore import QSettings
from .table_mapping_config import *

def get_refactor_fields_mapping(layer_name, qgis_utils):
    mapping = []
    if layer_name == BOUNDARY_POINT_TABLE:
         mapping = [
            {'length': -1, 'precision': 0, 'expression': '"t_id"', 'name': 't_id', 'type': 4},
            {'length': 255, 'precision': -1, 'expression': '"acuerdo"', 'name': 'acuerdo', 'type': 10},
            {'length': 255, 'precision': -1, 'expression': '"definicion_punto"', 'name': 'definicion_punto', 'type': 10},
            {'length': 255, 'precision': -1, 'expression': '"descripcion_punto"', 'name': 'descripcion_punto', 'type': 10},
            {'length': -1, 'precision': 0, 'expression': '"exactitud_vertical"', 'name': 'exactitud_vertical', 'type': 2},
            {'length': -1, 'precision': 0, 'expression': '"exactitud_horizontal"', 'name': 'exactitud_horizontal', 'type': 2},
            {'length': -1, 'precision': -1, 'expression': '"confiabilidad"', 'name': 'confiabilidad', 'type': 1},
            {'length': 10, 'precision': -1, 'expression': '"nombre_punto"', 'name': 'nombre_punto', 'type': 10},
            {'length': 255, 'precision': -1, 'expression': '"posicion_interpolacion"', 'name': 'posicion_interpolacion', 'type': 10},
            {'length': 255, 'precision': -1, 'expression': '"monumentacion"', 'name': 'monumentacion', 'type': 10},
            {'length': 255, 'precision': -1, 'expression': '"puntotipo"', 'name': 'puntotipo', 'type': 10},
            {'length': 255, 'precision': -1, 'expression': '"p_espacio_de_nombres"', 'name': 'p_espacio_de_nombres', 'type': 10},
            {'length': 255, 'precision': -1, 'expression': '"p_local_id"', 'name': 'p_local_id', 'type': 10},
            {'length': -1, 'precision': -1, 'expression': '"comienzo_vida_util_version"', 'name': 'comienzo_vida_util_version', 'type': 16},
            {'length': -1, 'precision': -1, 'expression': '"fin_vida_util_version"', 'name': 'fin_vida_util_version', 'type': 16}
        ]
    elif layer_name == SURVEY_POINT_TABLE:
        mapping = [
            {'type': 4, 'length': -1, 'name': 't_id', 'precision': 0, 'expression': '"t_id"'},
            {'type': 10, 'length': 255, 'name': 'tipo_punto_levantamiento', 'precision': -1, 'expression': '"tipo_punto_levantamiento"'},
            {'type': 10, 'length': 255, 'name': 'definicion_punto', 'precision': -1, 'expression': '"definicion_punto"'},
            {'type': 2, 'length': -1, 'name': 'exactitud_vertical', 'precision': 0, 'expression': '"exactitud_vertical"'},
            {'type': 2, 'length': -1, 'name': 'exactitud_horizontal', 'precision': 0, 'expression': '"exactitud_horizontal"'},
            {'type': 10, 'length': 10, 'name': 'nombre_punto', 'precision': -1, 'expression': '"nombre_punto"'},
            {'type': 10, 'length': 255, 'name': 'posicion_interpolacion', 'precision': -1, 'expression': '"posicion_interpolacion"'},
            {'type': 10, 'length': 255, 'name': 'monumentacion', 'precision': -1, 'expression': '"monumentacion"'},
            {'type': 10, 'length': 255, 'name': 'puntotipo', 'precision': -1, 'expression': '"puntotipo"'},
            {'type': 10, 'length': 255, 'name': 'p_espacio_de_nombres', 'precision': -1, 'expression': '"p_espacio_de_nombres"'},
            {'type': 10, 'length': 255, 'name': 'p_local_id', 'precision': -1, 'expression': '"p_local_id"'},
            {'type': 16, 'length': -1, 'name': 'comienzo_vida_util_version', 'precision': -1, 'expression': '"comienzo_vida_util_version"'},
            {'type': 16, 'length': -1, 'name': 'fin_vida_util_version', 'precision': -1, 'expression': '"fin_vida_util_version"'}
        ]
    elif layer_name == CONTROL_POINT_TABLE:
        mapping = [
            {'name': 't_id', 'precision': 0, 'type': 4, 'length': -1, 'expression': '"t_id"'},
            {'name': 'nombre_punto', 'precision': -1, 'type': 10, 'length': 20, 'expression': '"nombre_punto"'},
            {'name': 'exactitud_vertical', 'precision': 0, 'type': 2, 'length': -1, 'expression': '"exactitud_vertical"'},
            {'name': 'exactitud_horizontal', 'precision': 0, 'type': 2, 'length': -1, 'expression': '"exactitud_horizontal"'},
            {'name': 'tipo_punto_control', 'precision': -1, 'type': 10, 'length': 255, 'expression': '"tipo_punto_control"'},
            {'name': 'confiabilidad', 'precision': -1, 'type': 1, 'length': -1, 'expression': '"confiabilidad"'},
            {'name': 'posicion_interpolacion', 'precision': -1, 'type': 10, 'length': 255, 'expression': '"posicion_interpolacion"'},
            {'name': 'monumentacion', 'precision': -1, 'type': 10, 'length': 255, 'expression': '"monumentacion"'},
            {'name': 'puntotipo', 'precision': -1, 'type': 10, 'length': 255, 'expression': '"puntotipo"'},
            {'name': 'p_espacio_de_nombres', 'precision': -1, 'type': 10, 'length': 255, 'expression': '"p_espacio_de_nombres"'},
            {'name': 'p_local_id', 'precision': -1, 'type': 10, 'length': 255, 'expression': '"p_local_id"'},
            {'name': 'comienzo_vida_util_version', 'precision': -1, 'type': 16, 'length': -1, 'expression': '"comienzo_vida_util_version"'},
            {'name': 'fin_vida_util_version', 'precision': -1, 'type': 16, 'length': -1, 'expression': '"fin_vida_util_version"'}
        ]
    elif layer_name == BOUNDARY_TABLE:
        mapping = [
            {'name': 't_id', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"t_id"'},
            {'name': 'longitud', 'type': 6, 'length': 6, 'precision': 1, 'expression': '"longitud"'},
            {'name': 'localizacion_textual', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"localizacion_textual"'},
            {'name': 'ccl_espacio_de_nombres', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"ccl_espacio_de_nombres"'},
            {'name': 'ccl_local_id', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"ccl_local_id"'},
            {'name': 'comienzo_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': '"comienzo_vida_util_version"'},
            {'name': 'fin_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': '"fin_vida_util_version"'}
        ]
    elif layer_name == PLOT_TABLE:
        mapping = [
            {'name': 't_id', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"t_id"'},
            {'name': 'area_registral', 'type': 6, 'length': 15, 'precision': 1, 'expression': '"area_registral"'},
            {'name': 'area_calculada', 'type': 6, 'length': 15, 'precision': 1, 'expression': '"area_calculada"'},
            {'name': 'avaluo_terreno', 'type': 6, 'length': 13, 'precision': 1, 'expression': '"avaluo_terreno"'},
            {'name': 'dimension', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"dimension"'},
            {'name': 'etiqueta', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"etiqueta"'},
            {'name': 'relacion_superficie', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"relacion_superficie"'},
            {'name': 'su_espacio_de_nombres', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"su_espacio_de_nombres"'},
            {'name': 'su_local_id', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"su_local_id"'},
            {'name': 'nivel', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"nivel"'},
            {'name': 'comienzo_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': '"comienzo_vida_util_version"'},
            {'name': 'fin_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': '"fin_vida_util_version"'}
        ]
    elif layer_name == PARCEL_TABLE:
        mapping = [
            {'name': 't_id', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"t_id"'},
            {'name': 'departamento', 'type': 10, 'length': 2, 'precision': -1, 'expression': '"departamento"'},
            {'name': 'municipio', 'type': 10, 'length': 3, 'precision': -1, 'expression': '"municipio"'},
            {'name': 'zona', 'type': 10, 'length': 2, 'precision': -1, 'expression': '"zona"'},
            {'name': 'nupre', 'type': 10, 'length': 20, 'precision': -1, 'expression': '"nupre"'},
            {'name': 'fmi', 'type': 10, 'length': 20, 'precision': -1, 'expression': '"fmi"'},
            {'name': 'numero_predial', 'type': 10, 'length': 30, 'precision': -1, 'expression': '"numero_predial"'},
            {'name': 'numero_predial_anterior', 'type': 10, 'length': 20, 'precision': -1, 'expression': '"numero_predial_anterior"'},
            {'name': 'avaluo_predio', 'type': 6, 'length': 13, 'precision': 1, 'expression': '"avaluo_predio"'},
            {'name': 'nombre', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"nombre"'},
            {'name': 'tipo', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"tipo"'},
            {'name': 'u_espacio_de_nombres', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"u_espacio_de_nombres"'},
            {'name': 'u_local_id', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"u_local_id"'},
            {'name': 'comienzo_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': '"comienzo_vida_util_version"'},
            {'name': 'fin_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': '"fin_vida_util_version"'}
        ]
    elif layer_name == COL_PARTY_TABLE:
        mapping = [
            {'name': 't_id', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"t_id"'},
            {'name': 'documento_identidad', 'type': 10, 'length': 10, 'precision': -1, 'expression': '"documento_identidad"'},
            {'name': 'tipo_documento', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"tipo_documento"'},
            {'name': 'organo_emisor', 'type': 10, 'length': 20, 'precision': -1, 'expression': '"organo_emisor"'},
            {'name': 'fecha_emision', 'type': 14, 'length': -1, 'precision': -1, 'expression': '"fecha_emision"'},
            {'name': 'primer_apellido', 'type': 10, 'length': 50, 'precision': -1, 'expression': '"primer_apellido"'},
            {'name': 'primer_nombre', 'type': 10, 'length': 50, 'precision': -1, 'expression': '"primer_nombre"'},
            {'name': 'segundo_apellido', 'type': 10, 'length': 50, 'precision': -1, 'expression': '"segundo_apellido"'},
            {'name': 'segundo_nombre', 'type': 10, 'length': 50, 'precision': -1, 'expression': '"segundo_nombre"'},
            {'name': 'genero', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"genero"'},
            {'name': 'nombre', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"nombre"'},
            {'name': 'tipo', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"tipo"'},
            {'name': 'razon_social', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"razon_social"'},
            {'name': 'p_espacio_de_nombres', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"p_espacio_de_nombres"'},
            {'name': 'p_local_id', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"p_local_id"'},
            {'name': 'agrupacion', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"agrupacion"'},
            {'name': 'comienzo_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': '"comienzo_vida_util_version"'},
            {'name': 'fin_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': '"fin_vida_util_version"'}
        ]
    elif layer_name == ADMINISTRATIVE_SOURCE_TABLE:
        mapping = [
            {'name': 't_id', 'precision': 0, 'expression': '"t_id"', 'type': 4, 'length': -1},
            {'name': 'texto', 'precision': -1, 'expression': '"texto"', 'type': 10, 'length': 255},
            {'name': 'tipo', 'precision': -1, 'expression': '"tipo"', 'type': 10, 'length': 255},
            {'name': 'codigo_registral_transaccion', 'precision': -1, 'expression': '"codigo_registral_transaccion"', 'type': 10, 'length': 3},
            {'name': 'nombre', 'precision': -1, 'expression': '"nombre"', 'type': 10, 'length': 50},
            {'name': 'fecha_aceptacion', 'precision': -1, 'expression': '"fecha_aceptacion"', 'type': 16, 'length': -1},
            {'name': 'estado_disponibilidad', 'precision': -1, 'expression': '"estado_disponibilidad"', 'type': 10, 'length': 255},
            {'name': 'sello_inicio_validez', 'precision': -1, 'expression': '"sello_inicio_validez"', 'type': 16, 'length': -1},
            {'name': 'tipo_principal', 'precision': -1, 'expression': '"tipo_principal"', 'type': 10, 'length': 255},
            {'name': 'fecha_grabacion', 'precision': -1, 'expression': '"fecha_grabacion"', 'type': 16, 'length': -1},
            {'name': 'fecha_entrega', 'precision': -1, 'expression': '"fecha_entrega"', 'type': 16, 'length': -1},
            {'name': 's_espacio_de_nombres', 'precision': -1, 'expression': '"s_espacio_de_nombres"', 'type': 10, 'length': 255},
            {'name': 's_local_id', 'precision': -1, 'expression': '"s_local_id"', 'type': 10, 'length': 255},
            {'name': 'oficialidad', 'precision': -1, 'expression': '"oficialidad"', 'type': 1, 'length': -1}
        ]
    elif layer_name == SPATIAL_SOURCE_TABLE:
        mapping = [
            {'type': 4, 'length': -1, 'name': 't_id', 'precision': 0, 'expression': '"t_id"'},
            {'type': 10, 'length': 255, 'name': 'tipo', 'precision': -1, 'expression': '"tipo"'},
            {'type': 16, 'length': -1, 'name': 'fecha_aceptacion', 'precision': -1, 'expression': '"fecha_aceptacion"'},
            {'type': 10, 'length': 255, 'name': 'estado_disponibilidad', 'precision': -1, 'expression': '"estado_disponibilidad"'},
            {'type': 16, 'length': -1, 'name': 'sello_inicio_validez', 'precision': -1, 'expression': '"sello_inicio_validez"'},
            {'type': 10, 'length': 255, 'name': 'tipo_principal', 'precision': -1, 'expression': '"tipo_principal"'},
            {'type': 16, 'length': -1, 'name': 'fecha_grabacion', 'precision': -1, 'expression': '"fecha_grabacion"'},
            {'type': 16, 'length': -1, 'name': 'fecha_entrega', 'precision': -1, 'expression': '"fecha_entrega"'},
            {'type': 10, 'length': 255, 'name': 's_espacio_de_nombres', 'precision': -1, 'expression': '"s_espacio_de_nombres"'},
            {'type': 10, 'length': 255, 'name': 's_local_id', 'precision': -1, 'expression': '"s_local_id"'},
            {'type': 1, 'length': -1, 'name': 'oficialidad', 'precision': -1, 'expression': '"oficialidad"'}
        ]
    elif layer_name == BUILDING_TABLE:
        mapping = [
            {'name': 't_id', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"t_id"'},
            {'name': 'avaluo_construccion', 'type': 6, 'length': 13, 'precision': 1, 'expression': '"avaluo_construccion"'},
            {'name': 'tipo', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"tipo"'},
            {'name': 'dimension', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"dimension"'},
            {'name': 'etiqueta', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"etiqueta"'},
            {'name': 'relacion_superficie', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"relacion_superficie"'},
            {'name': 'su_espacio_de_nombres', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"su_espacio_de_nombres"'},
            {'name': 'su_local_id', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"su_local_id"'},
            {'name': 'nivel', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"nivel"'},
            {'name': 'comienzo_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': '"comienzo_vida_util_version"'},
            {'name': 'fin_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': '"fin_vida_util_version"'}
        ]
    elif layer_name == BUILDING_UNIT_TABLE:
        mapping = [
            {'name': 't_id', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"t_id"'},
            {'name': 'avaluo_unidad_construccion', 'type': 6, 'length': 15, 'precision': 1, 'expression': '"avaluo_unidad_construccion"'},
            {'name': 'numero_pisos', 'type': 2, 'length': -1, 'precision': 0, 'expression': '"numero_pisos"'},
            {'name': 'tipo_construccion', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"tipo_construccion"'},
            {'name': 'area_construida', 'type': 6, 'length': 15, 'precision': 1, 'expression': '"area_construida"'},
            {'name': 'area_privada_construida', 'type': 6, 'length': 15, 'precision': 1, 'expression': '"area_privada_construida"'},
            {'name': 'construccion', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"construccion"'}, # This value will be updated in the next step...
            {'name': 'tipo', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"tipo"'},
            {'name': 'dimension', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"dimension"'},
            {'name': 'etiqueta', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"etiqueta"'},
            {'name': 'relacion_superficie', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"relacion_superficie"'},
            {'name': 'su_espacio_de_nombres', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"su_espacio_de_nombres"'},
            {'name': 'su_local_id', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"su_local_id"'},
            {'name': 'nivel', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"nivel"'},
            {'name': 'comienzo_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': 'comienzo_vida_util_version'},
            {'name': 'fin_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': '"fin_vida_util_version"'}
        ]
    elif layer_name == RIGHT_TABLE:
        mapping = [
            {'expression': '"t_id"', 'precision': 0, 'type': 4, 'length': -1, 'name': 't_id'},
            {'expression': '"tipo"', 'precision': -1, 'type': 10, 'length': 255, 'name': 'tipo'},
            {'expression': '"codigo_registral_derecho"', 'precision': -1, 'type': 10, 'length': 3, 'name': 'codigo_registral_derecho'},
            {'expression': '"descripcion"', 'precision': -1, 'type': 10, 'length': 255, 'name': 'descripcion'},
            {'expression': '"comprobacion_comparte"', 'precision': -1, 'type': 1, 'length': -1, 'name': 'comprobacion_comparte'},
            {'expression': '"uso_efectivo"', 'precision': -1, 'type': 10, 'length': 255, 'name': 'uso_efectivo'},
            {'expression': '"interesado_col_interesado"', 'precision': 0, 'type': 4, 'length': -1, 'name': 'interesado_col_interesado'},
            {'expression': '"interesado_la_agrupacion_interesados"', 'precision': 0, 'type': 4, 'length': -1, 'name': 'interesado_la_agrupacion_interesados'},
            {'expression': '"unidad_la_baunit"', 'precision': 0, 'type': 4, 'length': -1, 'name': 'unidad_la_baunit'},
            {'expression': '"unidad_predio"', 'precision': 0, 'type': 4, 'length': -1, 'name': 'unidad_predio'},
            {'expression': '"r_espacio_de_nombres"', 'precision': -1, 'type': 10, 'length': 255, 'name': 'r_espacio_de_nombres'},
            {'expression': '"r_local_id"', 'precision': -1, 'type': 10, 'length': 255, 'name': 'r_local_id'},
            {'expression': '"comienzo_vida_util_version"', 'precision': -1, 'type': 16, 'length': -1, 'name': 'comienzo_vida_util_version'},
            {'expression': '"fin_vida_util_version"', 'precision': -1, 'type': 16, 'length': -1, 'name': 'fin_vida_util_version'}
        ]
    elif layer_name == RESPONSIBILITY_TABLE:
        mapping = [
            {'expression': '"t_id"', 'precision': 0, 'type': 4, 'length': -1, 'name': 't_id'},
            {'expression': '"tipo"', 'precision': -1, 'type': 10, 'length': 255, 'name': 'tipo'},
            {'expression': '"codigo_registral_responsabilidad"', 'precision': -1, 'type': 10, 'length': 3, 'name': 'codigo_registral_responsabilidad'},
            {'expression': '"descripcion"', 'precision': -1, 'type': 10, 'length': 255, 'name': 'descripcion'},
            {'expression': '"comprobacion_comparte"', 'precision': -1, 'type': 1, 'length': -1, 'name': 'comprobacion_comparte'},
            {'expression': '"uso_efectivo"', 'precision': -1, 'type': 10, 'length': 255, 'name': 'uso_efectivo'},
            {'expression': '"r_espacio_de_nombres"', 'precision': -1, 'type': 10, 'length': 255, 'name': 'r_espacio_de_nombres'},
            {'expression': '"r_local_id"', 'precision': -1, 'type': 10, 'length': 255, 'name': 'r_local_id'},
            {'expression': '"interesado_interesado_natural"', 'precision': 0, 'type': 4, 'length': -1, 'name': 'interesado_interesado_natural'},
            {'expression': '"interesado_interesado_juridico"', 'precision': 0, 'type': 4, 'length': -1, 'name': 'interesado_interesado_juridico'},
            {'expression': '"interesado_la_agrupacion_interesados"', 'precision': 0, 'type': 4, 'length': -1, 'name': 'interesado_la_agrupacion_interesados'},
            {'expression': '"unidad_la_baunit"', 'precision': 0, 'type': 4, 'length': -1, 'name': 'unidad_la_baunit'},
            {'expression': '"unidad_predio"', 'precision': 0, 'type': 4, 'length': -1, 'name': 'unidad_predio'},
            {'expression': '"comienzo_vida_util_version"', 'precision': -1, 'type': 16, 'length': -1, 'name': 'comienzo_vida_util_version'},
            {'expression': '"fin_vida_util_version"', 'precision': -1, 'type': 16, 'length': -1, 'name': 'fin_vida_util_version'}
        ]
    elif layer_name == RESTRICTION_TABLE:
        mapping = [
            {'expression': '"t_id"', 'precision': 0, 'type': 4, 'length': -1, 'name': 't_id'},
            {'expression': '"interesado_requerido"', 'precision': -1, 'type': 1, 'length': -1, 'name': 'interesado_requerido'},
            {'expression': '"tipo"', 'precision': -1, 'type': 10, 'length': 255, 'name': 'tipo'},
            {'expression': '"codigo_registral_restriccion"', 'precision': -1, 'type': 10, 'length': 3, 'name': 'codigo_registral_restriccion'},
            {'expression': '"descripcion"', 'precision': -1, 'type': 10, 'length': 255, 'name': 'descripcion'},
            {'expression': '"comprobacion_comparte"', 'precision': -1, 'type': 1, 'length': -1, 'name': 'comprobacion_comparte'},
            {'expression': '"uso_efectivo"', 'precision': -1, 'type': 10, 'length': 255, 'name': 'uso_efectivo'},
            {'expression': '"r_espacio_de_nombres"', 'precision': -1, 'type': 10, 'length': 255, 'name': 'r_espacio_de_nombres'},
            {'expression': '"r_local_id"', 'precision': -1, 'type': 10, 'length': 255, 'name': 'r_local_id'},
            {'expression': '"interesado_interesado_natural"', 'precision': 0, 'type': 4, 'length': -1, 'name': 'interesado_interesado_natural'},
            {'expression': '"interesado_interesado_juridico"', 'precision': 0, 'type': 4, 'length': -1, 'name': 'interesado_interesado_juridico'},
            {'expression': '"interesado_la_agrupacion_interesados"', 'precision': 0, 'type': 4, 'length': -1, 'name': 'interesado_la_agrupacion_interesados'},
            {'expression': '"unidad_la_baunit"', 'precision': 0, 'type': 4, 'length': -1, 'name': 'unidad_la_baunit'},
            {'expression': '"unidad_predio"', 'precision': 0, 'type': 4, 'length': -1, 'name': 'unidad_predio'},
            {'expression': '"comienzo_vida_util_version"', 'precision': -1, 'type': 16, 'length': -1, 'name': 'comienzo_vida_util_version'},
            {'expression': '"fin_vida_util_version"', 'precision': -1, 'type': 16, 'length': -1, 'name': 'fin_vida_util_version'}
        ]

    # If the user doesn't want to disable automatic fields...
    if not QSettings().value('Asistente-LADM_COL/automatic_values/disable_automatic_fields', True, bool):
        # Now see if we can adjust the mapping depending on user settings
        ns_enabled, ns_field, ns_value = qgis_utils.get_namespace_field_and_value(layer_name)

        for field in mapping:
            if ns_enabled and ns_field:
                if field['name'] == ns_field:
                    field['expression'] = '{}'.format(ns_value)

            if field['name'] == VIDA_UTIL_FIELD:
                field['expression'] = 'now()'

    return mapping
