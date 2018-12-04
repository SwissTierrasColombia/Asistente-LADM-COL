from qgis.PyQt.QtCore import QSettings
from .table_mapping_config import *

def get_refactor_fields_mapping(layer_name, qgis_utils):
    mapping = []
    if layer_name == BOUNDARY_POINT_TABLE:
         mapping = [
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
            {'name': 'longitud', 'type': 6, 'length': 6, 'precision': 1, 'expression': '"longitud"'},
            {'name': 'localizacion_textual', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"localizacion_textual"'},
            {'name': 'ccl_espacio_de_nombres', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"ccl_espacio_de_nombres"'},
            {'name': 'ccl_local_id', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"ccl_local_id"'},
            {'name': 'comienzo_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': '"comienzo_vida_util_version"'},
            {'name': 'fin_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': '"fin_vida_util_version"'}
        ]
    elif layer_name == PLOT_TABLE:
        mapping = [
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
    elif layer_name == PROPERTY_RECORD_CARD_TABLE: # predio_ficha
        mapping = [
            {'expression': '"sector"', 'length': 2, 'precision': -1, 'type': 10, 'name': 'sector'},
            {'expression': '"localidad_comuna"', 'length': 2, 'precision': -1, 'type': 10, 'name': 'localidad_comuna'},
            {'expression': '"barrio"', 'length': 2, 'precision': -1, 'type': 10, 'name': 'barrio'},
            {'expression': '"manzana_vereda"', 'length': 4, 'precision': -1, 'type': 10, 'name': 'manzana_vereda'},
            {'expression': '"terreno"', 'length': 4, 'precision': -1, 'type': 10, 'name': 'terreno'},
            {'expression': '"condicion_propiedad"', 'length': 1, 'precision': -1, 'type': 10, 'name': 'condicion_propiedad'},
            {'expression': '"edificio"', 'length': 2, 'precision': -1, 'type': 10, 'name': 'edificio'},
            {'expression': '"piso"', 'length': 2, 'precision': -1, 'type': 10, 'name': 'piso'},
            {'expression': '"unidad"', 'length': 4, 'precision': -1, 'type': 10, 'name': 'unidad'},
            {'expression': '"estado_nupre"', 'length': 255, 'precision': -1, 'type': 10, 'name': 'estado_nupre'},
            {'expression': '"destinacion_economica"', 'length': 255, 'precision': -1, 'type': 10, 'name': 'destinacion_economica'},
            {'expression': '"predio_tipo"', 'length': 255, 'precision': -1, 'type': 10, 'name': 'predio_tipo'},
            {'expression': '"tipo_predio_publico"', 'length': 255, 'precision': -1, 'type': 10, 'name': 'tipo_predio_publico'},
            {'expression': '"formalidad"', 'length': 255, 'precision': -1, 'type': 10, 'name': 'formalidad'},
            {'expression': '"estrato"', 'length': 255, 'precision': -1, 'type': 10, 'name': 'estrato'},
            {'expression': '"clase_suelo_pot"', 'length': 255, 'precision': -1, 'type': 10, 'name': 'clase_suelo_pot'},
            {'expression': '"categoria_suelo_pot"', 'length': 255, 'precision': -1, 'type': 10, 'name': 'categoria_suelo_pot'},
            {'expression': '"derecho_fmi"', 'length': 255, 'precision': -1, 'type': 10, 'name': 'derecho_fmi'},
            {'expression': '"inscrito_rupta"', 'length': -1, 'precision': -1, 'type': 1, 'name': 'inscrito_rupta'},
            {'expression': '"fecha_medida_rupta"', 'length': -1, 'precision': -1, 'type': 14, 'name': 'fecha_medida_rupta'},
            {'expression': '"anotacion_fmi_rupta"', 'length': -1, 'precision': -1, 'type': 1, 'name': 'anotacion_fmi_rupta'},
            {'expression': '"inscrito_proteccion_colectiva"', 'length': -1, 'precision': -1, 'type': 1, 'name': 'inscrito_proteccion_colectiva'},
            {'expression': '"fecha_proteccion_colectiva"', 'length': -1, 'precision': -1, 'type': 14, 'name': 'fecha_proteccion_colectiva'},
            {'expression': '"anotacion_fmi_proteccion_colectiva"', 'length': -1, 'precision': -1, 'type': 1, 'name': 'anotacion_fmi_proteccion_colectiva'},
            {'expression': '"inscrito_proteccion_ley1448"', 'length': -1, 'precision': -1, 'type': 1, 'name': 'inscrito_proteccion_ley1448'},
            {'expression': '"fecha_proteccion_ley1448"', 'length': -1, 'precision': -1, 'type': 14, 'name': 'fecha_proteccion_ley1448'},
            {'expression': '"anotacion_fmi_ley1448"', 'length': -1, 'precision': -1, 'type': 1, 'name': 'anotacion_fmi_ley1448'},
            {'expression': '"inscripcion_urt"', 'length': -1, 'precision': -1, 'type': 1, 'name': 'inscripcion_urt'},
            {'expression': '"fecha_inscripcion_urt"', 'length': -1, 'precision': -1, 'type': 14, 'name': 'fecha_inscripcion_urt'},
            {'expression': '"anotacion_fmi_urt"', 'length': -1, 'precision': -1, 'type': 1, 'name': 'anotacion_fmi_urt'},
            {'expression': '"vigencia_fiscal"', 'length': -1, 'precision': -1, 'type': 14, 'name': 'vigencia_fiscal'},
            {'expression': '"observaciones"', 'length': 255, 'precision': -1, 'type': 10, 'name': 'observaciones'},
            {'expression': '"fecha_visita_predial"', 'length': -1, 'precision': -1, 'type': 14, 'name': 'fecha_visita_predial'},
            {'expression': '"nombre_quien_atendio"', 'length': 40, 'precision': -1, 'type': 10, 'name': 'nombre_quien_atendio'},
            {'expression': '"numero_documento_quien_atendio"', 'length': 10, 'precision': -1, 'type': 10, 'name': 'numero_documento_quien_atendio'},
            {'expression': '"categoria_quien_atendio"', 'length': 255, 'precision': -1, 'type': 10, 'name': 'categoria_quien_atendio'},
            {'expression': '"tipo_documento_quien_atendio"', 'length': 255, 'precision': -1, 'type': 10, 'name': 'tipo_documento_quien_atendio'},
            {'expression': '"nombre_encuestador"', 'length': 40, 'precision': -1, 'type': 10, 'name': 'nombre_encuestador'},
            {'expression': '"numero_documento_encuestador"', 'length': 10, 'precision': -1, 'type': 10, 'name': 'numero_documento_encuestador'},
            {'expression': '"tipo_documento_encuestador"', 'length': 255, 'precision': -1, 'type': 10, 'name': 'tipo_documento_encuestador'}
        ]
    elif layer_name == MARKET_RESEARCH_TABLE:
        mapping = [
            {'expression': '"disponible_mercado"', 'length': -1, 'precision': -1, 'type': 1, 'name': 'disponible_mercado'},
            {'expression': '"tipo_oferta"', 'length': 255, 'precision': -1, 'type': 10, 'name': 'tipo_oferta'},
            {'expression': '"valor"', 'length': 16, 'precision': 1, 'type': 6, 'name': 'valor'},
            {'expression': '"nombre_oferente"', 'length': 40, 'precision': -1, 'type': 10, 'name': 'nombre_oferente'},
            {'expression': '"telefono_contacto_oferente"', 'length': 10, 'precision': -1, 'type': 10, 'name': 'telefono_contacto_oferente'},
            {'expression': '"observaciones"', 'length': 100, 'precision': -1, 'type': 10, 'name': 'observaciones'},
            {'expression': '"fichapredio"', 'length': -1, 'precision': 0, 'type': 4, 'name': 'fichapredio'}
        ]
    elif layer_name == NUCLEAR_FAMILY_TABLE:
        mapping = [
            {'expression': '"documento_identidad"', 'length': 10, 'precision': -1, 'type': 10, 'name': 'documento_identidad'},
            {'expression': '"tipo_documento"', 'length': 255, 'precision': -1, 'type': 10, 'name': 'tipo_documento'},
            {'expression': '"organo_emisor"', 'length': 20, 'precision': -1, 'type': 10, 'name': 'organo_emisor'},
            {'expression': '"fecha_emision"', 'length': -1, 'precision': -1, 'type': 14, 'name': 'fecha_emision'},
            {'expression': '"primer_nombre"', 'length': 20, 'precision': -1, 'type': 10, 'name': 'primer_nombre'},
            {'expression': '"segundo_nombre"', 'length': 20, 'precision': -1, 'type': 10, 'name': 'segundo_nombre'},
            {'expression': '"primer_apellido"', 'length': 20, 'precision': -1, 'type': 10, 'name': 'primer_apellido'},
            {'expression': '"segundo_apellido"', 'length': 20, 'precision': -1, 'type': 10, 'name': 'segundo_apellido'},
            {'expression': '"fecha_nacimiento"', 'length': -1, 'precision': -1, 'type': 14, 'name': 'fecha_nacimiento'},
            {'expression': '"lugar_nacimiento"', 'length': 100, 'precision': -1, 'type': 10, 'name': 'lugar_nacimiento'},
            {'expression': '"nacionalidad"', 'length': 20, 'precision': -1, 'type': 10, 'name': 'nacionalidad'},
            {'expression': '"discapacidad"', 'length': -1, 'precision': -1, 'type': 1, 'name': 'discapacidad'},
            {'expression': '"genero"', 'length': 255, 'precision': -1, 'type': 10, 'name': 'genero'},
            {'expression': '"habita_predio"', 'length': -1, 'precision': -1, 'type': 1, 'name': 'habita_predio'},
            {'expression': '"parentesco"', 'length': 20, 'precision': -1, 'type': 10, 'name': 'parentesco'},
            {'expression': '"etnia"', 'length': 20, 'precision': -1, 'type': 10, 'name': 'etnia'},
            {'expression': '"direccion"', 'length': 100, 'precision': -1, 'type': 10, 'name': 'direccion'},
            {'expression': '"celular"', 'length': 10, 'precision': -1, 'type': 10, 'name': 'celular'},
            {'expression': '"fichapredio"', 'length': -1, 'precision': 0, 'type': 4, 'name': 'fichapredio'}
        ]
    elif layer_name == NATURAL_PARTY_TABLE:
        mapping = [
            {'expression': '"nacionalidad"', 'length': 20, 'precision': -1, 'type': 10, 'name': 'nacionalidad'},
            {'expression': '"fecha_nacimiento"', 'length': -1, 'precision': -1, 'type': 14, 'name': 'fecha_nacimiento'},
            {'expression': '"lugar_nacimiento"', 'length': 100, 'precision': -1, 'type': 10, 'name': 'lugar_nacimiento'},
            {'expression': '"cabeza_hogar"', 'length': -1, 'precision': -1, 'type': 1, 'name': 'cabeza_hogar'},
            {'expression': '"discapacidad"', 'length': -1, 'precision': -1, 'type': 1, 'name': 'discapacidad'},
            {'expression': '"etnia"', 'length': 20, 'precision': -1, 'type': 10, 'name': 'etnia'},
            {'expression': '"interesadonaturalcatastro"', 'length': -1, 'precision': 0, 'type': 4, 'name': 'interesadonaturalcatastro'}
        ]
    elif layer_name == LEGAL_PARTY_TABLE:
        mapping = [
            {'expression': '"fecha_constitucion"', 'length': -1, 'precision': -1, 'type': 14, 'name': 'fecha_constitucion'},
            {'expression': '"lugar_inscripcion"', 'length': 500, 'precision': -1, 'type': 10, 'name': 'lugar_inscripcion'},
            {'expression': '"nacionalidad"', 'length': 20, 'precision': -1, 'type': 10, 'name': 'nacionalidad'},
            {'expression': '"interesadojuridicocatastro"', 'length': -1, 'precision': 0, 'type': 4, 'name': 'interesadojuridicocatastro'}
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
