# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                                 Piloto UAECD
                             --------------------
        begin                : 2017-12-18
        git sha              : :%H$
        copyright            : (C) 2017, 2018 by Germán Carrillo (BSF Swissphoto)
                               (C) 2017, 2018 by Jonathan Albarracín (UAECD)
        email                : gcarrillo@linuxmail.org
                               jonyfido@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
import os
import qgis
import processing

INPUT_DB_PATH = '/docs/tr/ai/insumos/uaecd/Capas_Sector_Piloto/GDB_Piloto.gpkg'
REFACTORED_DB_PATH = '/docs/tr/ai/productos/uaecd/resultados_intermedios/refactored_02_14.gpkg'
INPUT_PREDIO_INTERESADO_PATH = '/docs/tr/ai/insumos/uaecd/interesado_predio_full.ods'
LAYER_PREDIO_INTERESADO = os.path.splitext(os.path.basename(INPUT_PREDIO_INTERESADO_PATH))[0]

# PostgreSQL connection to schema with a LADM_COL model
OUTPUT_DB_NAME = 'test'
OUTPUT_DB_SCHEMA = 'uaecd_ladm_col_03'
OUTPUT_DB_USER = 'postgres'
OUTPUT_DB_PASSWORD = 'postgres'

# Asistente-LADM_COL plugin is a prerrequisite
asistente_ladm_col = qgis.utils.plugins["asistente_ladm_col"]

def refactor_and_copy_paste(params_refactor, input_uri, output_layer):
    processing.run("qgis:refactorfields", params_refactor)
    input_layer = QgsVectorLayer(input_uri, "r_input_layer", "ogr")
    if not input_layer.isValid():
        print("Layer '{}' is not valid!".format(input_uri))
    input_layer.selectAll()
    iface.copySelectionToClipboard(input_layer)
    if not output_layer.isValid():
        print("Layer {} is not valid!".format(output_layer.name()))
    output_layer.startEditing()
    iface.pasteFromClipboard(output_layer)
    output_layer.commitChanges()

def llenar_punto_lindero():
    params_refactor_punto_lindero = { 'FIELDS_MAPPING' : [{'length': -1, 'precision': 0, 'expression': '"t_id"', 'name': 't_id', 'type': 4}, {'length': 255, 'precision': -1, 'expression': "'Acuerdo'", 'name': 'acuerdo', 'type': 10}, {'length': 255, 'precision': -1, 'expression': "'Bien_Definido'", 'name': 'definicion_punto', 'type': 10}, {'length': 255, 'precision': -1, 'expression': '"descripcion_punto"', 'name': 'descripcion_punto', 'type': 10}, {'length': -1, 'precision': 0, 'expression': '"exactitud_vertical"', 'name': 'exactitud_vertical', 'type': 2}, {'length': -1, 'precision': 0, 'expression': '12', 'name': 'exactitud_horizontal', 'type': 2}, {'length': -1, 'precision': -1, 'expression': '"confiabilidad"', 'name': 'confiabilidad', 'type': 1}, {'length': 10, 'precision': -1, 'expression': '"nombre_punto"', 'name': 'nombre_punto', 'type': 10}, {'length': 255, 'precision': -1, 'expression': '"posicion_interpolacion"', 'name': 'posicion_interpolacion', 'type': 10}, {'length': 255, 'precision': -1, 'expression': "'Otros'", 'name': 'monumentacion', 'type': 10}, {'length': 255, 'precision': -1, 'expression': "'Catastro'", 'name': 'puntotipo', 'type': 10}, {'length': 255, 'precision': -1, 'expression': "'UAECD_Punto_Lindero'", 'name': 'p_espacio_de_nombres', 'type': 10}, {'length': 255, 'precision': -1, 'expression': '"fid"', 'name': 'p_local_id', 'type': 10}, {'length': -1, 'precision': 0, 'expression': '"ue_la_unidadespacial"', 'name': 'ue_la_unidadespacial', 'type': 4}, {'length': -1, 'precision': 0, 'expression': '"ue_terreno"', 'name': 'ue_terreno', 'type': 4}, {'length': -1, 'precision': 0, 'expression': '"ue_la_espaciojuridicoredservicios"', 'name': 'ue_la_espaciojuridicoredservicios', 'type': 4}, {'length': -1, 'precision': 0, 'expression': '"ue_la_espaciojuridicounidadedificacion"', 'name': 'ue_la_espaciojuridicounidadedificacion', 'type': 4}, {'length': -1, 'precision': 0, 'expression': '"ue_servidumbrepaso"', 'name': 'ue_servidumbrepaso', 'type': 4}, {'length': -1, 'precision': 0, 'expression': '"ue_unidadconstruccion"', 'name': 'ue_unidadconstruccion', 'type': 4}, {'length': -1, 'precision': 0, 'expression': '"ue_construccion"', 'name': 'ue_construccion', 'type': 4}, {'length': -1, 'precision': -1, 'expression': 'now()', 'name': 'comienzo_vida_util_version', 'type': 16}, {'length': -1, 'precision': -1, 'expression': '"fin_vida_util_version"', 'name': 'fin_vida_util_version', 'type': 16}], 'OUTPUT' : 'ogr:dbname="{refactored_db_path}" table="R_punto_lindero" (geom) sql='.format(refactored_db_path=REFACTORED_DB_PATH), 'INPUT' : '{input_db_path}|layername=Vertices_Lot'.format(input_db_path=INPUT_DB_PATH) }
    input_uri = '{refactored_db_path}|layername=R_punto_lindero'.format(refactored_db_path=REFACTORED_DB_PATH)
    db = asistente_ladm_col.get_db_connection()
    output_uri = db.get_uri_for_layer('puntolindero')[1]
    output_punto_lindero = QgsVectorLayer(output_uri, "punto_lindero", "postgres")
    refactor_and_copy_paste(params_refactor_punto_lindero, input_uri, output_punto_lindero)

def llenar_lindero():
    # Lindero
    params_refactor_lindero = { 'INPUT' : '{input_db_path}|layername=PLot'.format(input_db_path=INPUT_DB_PATH), 'FIELDS_MAPPING' : [{'name': 't_id', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"t_id"'}, {'name': 'longitud', 'type': 6, 'length': 6, 'precision': 1, 'expression': '"PELDISTANC"'}, {'name': 'localizacion_textual', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"localizacion_textual"'}, {'name': 'ccl_espacio_de_nombres', 'type': 10, 'length': 255, 'precision': -1, 'expression': "'UAECD_Lindero'"}, {'name': 'ccl_local_id', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"fid"'}, {'name': 'comienzo_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': 'now()'}, {'name': 'fin_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': '"fin_vida_util_version"'}], 'OUTPUT' : 'ogr:dbname="{refactored_db_path}" table="R_lindero" (geom) sql='.format(refactored_db_path=REFACTORED_DB_PATH) }
    input_uri = '{refactored_db_path}|layername=R_lindero'.format(refactored_db_path=REFACTORED_DB_PATH)
    db = asistente_ladm_col.get_db_connection()
    output_uri = db.get_uri_for_layer('lindero')[1]
    output_lindero = QgsVectorLayer(output_uri, "lindero", "postgres")
    refactor_and_copy_paste(params_refactor_lindero, input_uri, output_lindero)

def llenar_terreno():
    # Terreno
    params_refactor_terreno = { 'INPUT' : '{input_db_path}|layername=Lote_fixed'.format(input_db_path=INPUT_DB_PATH), 'FIELDS_MAPPING' : [{'name': 't_id', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"t_id"'}, {'name': 'area_registral', 'type': 6, 'length': 15, 'precision': 1, 'expression': '"AREA_TERRENO"'}, {'name': 'area_calculada', 'type': 6, 'length': 15, 'precision': 1, 'expression': '"SHAPE_Area"'}, {'name': 'avaluo_terreno', 'type': 6, 'length': 13, 'precision': 1, 'expression': '"AV_TERRENO"'}, {'name': 'dimension', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"dimension"'}, {'name': 'etiqueta', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"etiqueta"'}, {'name': 'relacion_superficie', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"relacion_superficie"'}, {'name': 'su_espacio_de_nombres', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"u_nombres"'}, {'name': 'su_local_id', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"Cod_LOTE"'}, {'name': 'nivel', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"nivel"'}, {'name': 'uej2_la_unidadespacial', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"uej2_la_unidadespacial"'}, {'name': 'uej2_servidumbrepaso', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"uej2_servidumbrepaso"'}, {'name': 'uej2_terreno', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"uej2_terreno"'}, {'name': 'uej2_la_espaciojuridicoredservicios', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"uej2_la_espaciojuridicoredservicios"'}, {'name': 'uej2_la_espaciojuridicounidadedificacion', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"uej2_la_espaciojuridicounidadedificacion"'}, {'name': 'uej2_construccion', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"uej2_construccion"'}, {'name': 'uej2_unidadconstruccion', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"uej2_unidadconstruccion"'}, {'name': 'comienzo_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': 'now()'}, {'name': 'fin_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': '"fin_vida_util_version"'}, {'name': 'punto_referencia', 'type': 10, 'length': -1, 'precision': -1, 'expression': '"punto_referencia"'}], 'OUTPUT' : 'ogr:dbname="{refactored_db_path}" table="R_terreno" (geom) sql='.format(refactored_db_path=REFACTORED_DB_PATH) }
    input_uri = '{refactored_db_path}|layername=R_terreno'.format(refactored_db_path=REFACTORED_DB_PATH)
    db = asistente_ladm_col.get_db_connection()
    output_uri = db.get_uri_for_layer('terreno')[1]
    output_terreno = QgsVectorLayer(output_uri, "terreno", "postgres")
    refactor_and_copy_paste(params_refactor_terreno, input_uri, output_terreno)

def llenar_tablas_de_topologia():
    # PuntoCCL, MasCCL, Menos
    db = asistente_ladm_col.get_db_connection()
    asistente_ladm_col.qgis_utils.fill_topology_table_pointbfs(db, use_selection=False)
    asistente_ladm_col.qgis_utils.fill_topology_tables_morebfs_less(db, use_selection=False)

def llenar_predio():
    # Predio
    params_refactor_predio = { 'INPUT' : '{input_db_path}|layername=Pred_Identificador'.format(input_db_path=INPUT_DB_PATH), 'FIELDS_MAPPING' : [{'name': 't_id', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"t_id"'}, {'name': 'departamento', 'type': 10, 'length': 2, 'precision': -1, 'expression': "'11'"}, {'name': 'municipio', 'type': 10, 'length': 3, 'precision': -1, 'expression': "'001'"}, {'name': 'zona', 'type': 10, 'length': 2, 'precision': -1, 'expression': "'01'"}, {'name': 'nupre', 'type': 10, 'length': 20, 'precision': -1, 'expression': '"CHIP"'}, {'name': 'fmi', 'type': 10, 'length': 20, 'precision': -1, 'expression': '"MATRICULA"'}, {'name': 'numero_predial', 'type': 10, 'length': 30, 'precision': -1, 'expression': '"NUMERO_PREDIAL_NAL"'}, {'name': 'numero_predial_anterior', 'type': 10, 'length': 20, 'precision': -1, 'expression': '"numero_predial_anterior"'}, {'name': 'avaluo_predio', 'type': 6, 'length': 13, 'precision': 1, 'expression': '"VALOR_AVALUO"'}, {'name': 'nombre', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"DIRECCION_REAL"'}, {'name': 'tipo', 'type': 10, 'length': 255, 'precision': -1, 'expression': "'Unidad_Propiedad_Basica'"}, {'name': 'u_espacio_de_nombres', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"u_nombres"'}, {'name': 'u_local_id', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"CHIP"'}, {'name': 'comienzo_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': 'now()'}, {'name': 'fin_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': '"fin_vida_util_version"'}], 'OUTPUT' : 'ogr:dbname="{refactored_db_path}" table="R_predio" sql='.format(refactored_db_path=REFACTORED_DB_PATH) }
    input_uri = '{refactored_db_path}|layername=R_predio'.format(refactored_db_path=REFACTORED_DB_PATH)
    db = asistente_ladm_col.get_db_connection()
    output_uri = db.get_uri_for_layer('predio')[1]
    output_predio = QgsVectorLayer(output_uri, "predio", "postgres")
    refactor_and_copy_paste(params_refactor_predio, input_uri, output_predio)

def llenar_uebaunit():
    # Relación Terreno-Predio (Necesita una tabla fuente de paso, en la UAECD tienen CHIP vs. COD LOTE)
    db = asistente_ladm_col.get_db_connection()

    # Predio: dict = {CHIP : t_id}
    output_uri_predio = db.get_uri_for_layer('predio')[1]
    layer_predio = QgsVectorLayer(output_uri_predio, "predio", "postgres")
    it_predio = layer_predio.getFeatures()
    dict_predio = {feat_predio['nupre']: feat_predio['t_id'] for feat_predio in it_predio}

    # Terreno: dict = {COD_LOTE : t_id}
    output_uri_terreno = db.get_uri_for_layer('terreno')[1]
    layer_terreno = QgsVectorLayer(output_uri_terreno, "terreno", "postgres")
    it_terreno = layer_terreno.getFeatures()
    dict_terreno = {feat_terreno['su_local_id']: feat_terreno['t_id'] for feat_terreno in it_terreno}

    # Get uebaunit
    output_uri_uebaunit = db.get_uri_for_layer('uebaunit')[1]
    table_uebaunit = QgsVectorLayer(output_uri_uebaunit, "uebeaunit", "postgres")
    rows = list()

    # Iterar tabla fuente de paso buscando CHIP y COD_LOTE en dicts Predio y Terreno
    uri_association_table = '{}|layername={}'.format(INPUT_DB_PATH,'Pred_Identificador')
    terreno_predio = QgsVectorLayer(uri_association_table, 'terreno_predio', 'ogr')
    for f in terreno_predio.getFeatures():
        cod_lote = f['Cod_LOTE']
        chip = f['CHIP']
        new_row = QgsVectorLayerUtils().createFeature(table_uebaunit)
        if cod_lote in dict_terreno and chip in dict_predio:
            new_row.setAttribute("ue_terreno", dict_terreno[cod_lote])
            new_row.setAttribute("baunit_predio", dict_predio[chip])
            rows.append(new_row)
        else:
            print("### NOT FOUND COD_LOTE-CHIP ###", cod_lote, chip)

    # Llenar uebaunit
    print(len(rows), "added to uebaunit!!!")
    table_uebaunit.dataProvider().addFeatures(rows)

def llenar_construccion(layer_name):
    # Construccion
    params_refactor_construccion = { 'INPUT' : '{input_db_path}|layername={input_layer_name}'.format(input_db_path=INPUT_DB_PATH, input_layer_name=layer_name), 'FIELDS_MAPPING' : [{'name': 't_id', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"t_id"'}, {'name': 'avaluo_construccion', 'type': 6, 'length': 13, 'precision': 1, 'expression': '"AVTotal_CONSTRUC"'}, {'name': 'tipo', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"tipo"'}, {'name': 'dimension', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"dimension"'}, {'name': 'etiqueta', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"etiqueta"'}, {'name': 'relacion_superficie', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"relacion_superficie"'}, {'name': 'su_espacio_de_nombres', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"u_nombres"'}, {'name': 'su_local_id', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"Cod_LOTE"'}, {'name': 'nivel', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"nivel"'}, {'name': 'uej2_la_unidadespacial', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"uej2_la_unidadespacial"'}, {'name': 'uej2_servidumbrepaso', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"uej2_servidumbrepaso"'}, {'name': 'uej2_terreno', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"uej2_terreno"'}, {'name': 'uej2_la_espaciojuridicoredservicios', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"uej2_la_espaciojuridicoredservicios"'}, {'name': 'uej2_la_espaciojuridicounidadedificacion', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"uej2_la_espaciojuridicounidadedificacion"'}, {'name': 'uej2_construccion', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"uej2_construccion"'}, {'name': 'uej2_unidadconstruccion', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"uej2_unidadconstruccion"'}, {'name': 'comienzo_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': 'now()'}, {'name': 'fin_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': '"fin_vida_util_version"'}, {'name': 'punto_referencia', 'type': 10, 'length': -1, 'precision': -1, 'expression': '"punto_referencia"'}], 'OUTPUT' : 'ogr:dbname="{refactored_db_path}" table="R_construccion" (geom) sql='.format(refactored_db_path=REFACTORED_DB_PATH) }
    input_uri = '{refactored_db_path}|layername=R_construccion'.format(refactored_db_path=REFACTORED_DB_PATH)
    db = asistente_ladm_col.get_db_connection()
    output_uri = db.get_uri_for_layer('construccion')[1]
    output_construccion = QgsVectorLayer(output_uri, "construccion", "postgres")
    refactor_and_copy_paste(params_refactor_construccion, input_uri, output_construccion)

def llenar_unidad_construccion():
    params_refactor_unidad_construccion = { 'INPUT' : '{input_db_path}|layername=Und_Cons'.format(input_db_path=INPUT_DB_PATH), 'FIELDS_MAPPING' : [{'name': 't_id', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"t_id"'}, {'name': 'avaluo_unidad_construccion', 'type': 2, 'length': -1, 'precision': 0, 'expression': '"AV_Und_CONS"'}, {'name': 'numero_pisos', 'type': 2, 'length': -1, 'precision': 0, 'expression': '"MAX_NUM_PISOS"'}, {'name': 'tipo_construccion', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"tipo_construccion"'}, {'name': 'area_construida', 'type': 6, 'length': 15, 'precision': 1, 'expression': '"Area_UND_CONS"'}, {'name': 'area_privada_construida', 'type': 6, 'length': 15, 'precision': 1, 'expression': '"area_privada_construida"'}, {'name': 'construccion', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"Cod_CONS"'}, {'name': 'tipo', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"tipo"'}, {'name': 'dimension', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"dimension"'}, {'name': 'etiqueta', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"etiqueta"'}, {'name': 'relacion_superficie', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"relacion_superficie"'}, {'name': 'su_espacio_de_nombres', 'type': 10, 'length': 255, 'precision': -1, 'expression': "'UAECD_UnidadConstruccion'"}, {'name': 'su_local_id', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"Cod_CONS"'}, {'name': 'nivel', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"nivel"'}, {'name': 'uej2_la_unidadespacial', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"uej2_la_unidadespacial"'}, {'name': 'uej2_servidumbrepaso', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"uej2_servidumbrepaso"'}, {'name': 'uej2_terreno', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"uej2_terreno"'}, {'name': 'uej2_la_espaciojuridicoredservicios', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"uej2_la_espaciojuridicoredservicios"'}, {'name': 'uej2_la_espaciojuridicounidadedificacion', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"uej2_la_espaciojuridicounidadedificacion"'}, {'name': 'uej2_construccion', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"uej2_construccion"'}, {'name': 'uej2_unidadconstruccion', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"uej2_unidadconstruccion"'}, {'name': 'comienzo_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': 'now()'}, {'name': 'fin_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': '"fin_vida_util_version"'}, {'name': 'punto_referencia', 'type': 10, 'length': -1, 'precision': -1, 'expression': '"punto_referencia"'}], 'OUTPUT' : 'ogr:dbname="{refactored_db_path}" table="R_unidadconstruccion" (geom) sql='.format(refactored_db_path=REFACTORED_DB_PATH) }

    processing.run("qgis:refactorfields", params_refactor_unidad_construccion)
    input_uri = '{refactored_db_path}|layername=R_unidadconstruccion'.format(refactored_db_path=REFACTORED_DB_PATH)
    input_layer = QgsVectorLayer(input_uri, "r_input_layer", "ogr")

    db = asistente_ladm_col.get_db_connection()
    output_uri = db.get_uri_for_layer('construccion')[1]
    layer_construccion = QgsVectorLayer(output_uri, "construccion", "postgres")

    output_uri = db.get_uri_for_layer('unidadconstruccion')[1]
    output_unidad_construccion = QgsVectorLayer(output_uri, "unidad_construccion", "postgres")

    # Llenar relacion unidad_construccion - construccion en capa refactored
    features_unidad_construccion = [f for f in input_layer.getFeatures()]
    attrMap = {}
    idx_construccion = input_layer.fields().indexFromName('construccion')
    for f in features_unidad_construccion:
        it_construccion = layer_construccion.getFeatures('"su_local_id"=\'{}\''.format(f['su_local_id']))
        f_construccion = QgsFeature()
        it_construccion.nextFeature(f_construccion)
        if f_construccion.isValid():
            attrs = {idx_construccion : f_construccion['t_id']}
            attrMap[f.id()] = attrs
        else:
            print("Construccion not found:",f['su_local_id'])

    input_layer.dataProvider().changeAttributeValues(attrMap)
    input_layer.reload()

    # Finalmente, copiar refactored en capa unidad construccion
    input_layer.selectAll()
    iface.copySelectionToClipboard(input_layer)
    output_unidad_construccion.startEditing()
    iface.pasteFromClipboard(output_unidad_construccion)
    output_unidad_construccion.commitChanges()

def llenar_interesado_natural():
    # Interesado Natural
    params_refactor_interesado_natural = { 'INPUT' : '{input_db_path}|layername=Interesados'.format(input_db_path=INPUT_DB_PATH), 'FIELDS_MAPPING' : [{'name': 't_id', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"t_id"'}, {'name': 'documento_identidad', 'type': 10, 'length': 10, 'precision': -1, 'expression': '"documento_identidad"'}, {'name': 'tipo_documento', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"tipo_documento"'}, {'name': 'organo_emisor', 'type': 10, 'length': 20, 'precision': -1, 'expression': '"organo_emisor"'}, {'name': 'fecha_emision', 'type': 14, 'length': -1, 'precision': -1, 'expression': '"fecha_emision"'}, {'name': 'primer_apellido', 'type': 10, 'length': 50, 'precision': -1, 'expression': '"primer_apellido"'}, {'name': 'primer_nombre', 'type': 10, 'length': 50, 'precision': -1, 'expression': '"primer_nombre"'}, {'name': 'segundo_apellido', 'type': 10, 'length': 50, 'precision': -1, 'expression': '"segundo_apellido"'}, {'name': 'segundo_nombre', 'type': 10, 'length': 50, 'precision': -1, 'expression': '"segundo_nombre"'}, {'name': 'genero', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"genero"'}, {'name': 'nombre', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"nombre"'}, {'name': 'tipo', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"TIPO_interesado"'}, {'name': 'p_espacio_de_nombres', 'type': 10, 'length': 255, 'precision': -1, 'expression': "'UAECD_IntNatural'"}, {'name': 'p_local_id', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"OBJECTID"'}, {'name': 'agrupacion', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"agrupacion"'}, {'name': 'comienzo_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': 'now()'}, {'name': 'fin_vida_util_version', 'type': 16, 'length': -1, 'precision': -1, 'expression': '"fin_vida_util_version"'}], 'OUTPUT' : 'ogr:dbname="{refactored_db_path}" table="R_interesado_natural" (geom) sql='.format(refactored_db_path=REFACTORED_DB_PATH) }

    input_uri_interesado_natural = '{refactored_db_path}|layername=R_interesado_natural'.format(refactored_db_path=REFACTORED_DB_PATH)
    db = asistente_ladm_col.get_db_connection()
    output_uri = db.get_uri_for_layer('interesado_natural')[1]
    output_interesado_natural = QgsVectorLayer(output_uri, "interesado_natural", "postgres")
    refactor_and_copy_paste(params_refactor_interesado_natural, input_uri_interesado_natural, output_interesado_natural)

def llenar_interesado_juridico():
    # Interesado Juridico
    params_refactor_interesado_juridico = { 'OUTPUT' : 'ogr:dbname="{refactored_db_path}" table="R_interesado_juridico" (geom) sql='.format(refactored_db_path=REFACTORED_DB_PATH), 'INPUT' : '{input_db_path}|layername=Interesado_Juridico'.format(input_db_path=INPUT_DB_PATH), 'FIELDS_MAPPING' : [{'type': 4, 'precision': 0, 'name': 't_id', 'expression': '"t_id"', 'length': -1}, {'type': 10, 'precision': -1, 'name': 'numero_nit', 'expression': '"numero_nit"', 'length': 20}, {'type': 10, 'precision': -1, 'name': 'razon_social', 'expression': '"razon_social"', 'length': 100}, {'type': 10, 'precision': -1, 'name': 'nombre', 'expression': '"nombre"', 'length': 255}, {'type': 10, 'precision': -1, 'name': 'tipo', 'expression': '"TIPO"', 'length': 255}, {'type': 10, 'precision': -1, 'name': 'p_espacio_de_nombres', 'expression': "'UAECD_Interesado_Juridico'", 'length': 255}, {'type': 10, 'precision': -1, 'name': 'p_local_id', 'expression': '"OBJECTID"', 'length': 255}, {'type': 16, 'precision': -1, 'name': 'comienzo_vida_util_version', 'expression': 'now()', 'length': -1}, {'type': 16, 'precision': -1, 'name': 'fin_vida_util_version', 'expression': '"fin_vida_util_version"', 'length': -1}] }

    input_uri_interesado_juridico = '{refactored_db_path}|layername=R_interesado_juridico'.format(refactored_db_path=REFACTORED_DB_PATH)
    db = asistente_ladm_col.get_db_connection()
    output_uri = db.get_uri_for_layer('interesado_juridico')[1]
    output_interesado_juridico = QgsVectorLayer(output_uri, "interesado_juridico", "postgres")
    refactor_and_copy_paste(params_refactor_interesado_juridico, input_uri_interesado_juridico, output_interesado_juridico)

def llenar_col_derecho(tipo='interesado_natural'):
    # Relación Interesado-Derecho (Necesita una tabla fuente de paso)
    db = asistente_ladm_col.get_db_connection()

    # Predio: dict = {CHIP: t_id}
    output_uri_predio = db.get_uri_for_layer('predio')[1]
    layer_predio = QgsVectorLayer(output_uri_predio, "predio", "postgres")
    it_predio = layer_predio.getFeatures()
    dict_predio = {feat_predio['nupre']: feat_predio['t_id'] for feat_predio in it_predio}

    # Interesado: dict = {numero_documento : t_id}
    if tipo == 'interesado_juridico':
        association_table_name = 'Maestra_Juridicos'
        ladm_attribute = "interesado_interesado_juridico"
        output_uri_interesado_juridico = db.get_uri_for_layer('interesado_juridico')[1]
        table_interesado = QgsVectorLayer(output_uri_interesado_juridico, "Interesado Juridico", "postgres")
        it_interesado = table_interesado.getFeatures()
        dict_interesado = {feat_interesado['numero_nit']: feat_interesado['t_id'] for feat_interesado in it_interesado}
    else:
        association_table_name = 'Maestra_Naturales'
        ladm_attribute = "interesado_interesado_natural"
        output_uri_interesado_natural = db.get_uri_for_layer('interesado_natural')[1]
        table_interesado = QgsVectorLayer(output_uri_interesado_natural, "Interesado Natural", "postgres")
        it_interesado = table_interesado.getFeatures()
        dict_interesado = {feat_interesado['documento_identidad']: feat_interesado['t_id'] for feat_interesado in it_interesado}

    # Get col_derecho
    output_uri_col_derecho = db.get_uri_for_layer('col_derecho')[1]
    table_col_derecho = QgsVectorLayer(output_uri_col_derecho, "col_derecho", "postgres")
    asistente_ladm_col.qgis_utils.configureAutomaticField(table_col_derecho, "comienzo_vida_util_version", "now()")
    asistente_ladm_col.qgis_utils.configureAutomaticField(table_col_derecho, "r_espacio_de_nombres", "'UAECD_Col_Derecho'")
    rows = list()

    # Iterar tabla fuente de paso buscando CHIP y COD_LOTE en dicts Predio y Terreno
    uri_association_table = '{}|layername={}'.format(INPUT_DB_PATH, association_table_name)
    predio_interesado = QgsVectorLayer(uri_association_table, 'predio_interesado', 'ogr')
    for f in predio_interesado.getFeatures():
        numero_documento = str(int(f['documento_identidad']))
        chip = f['chip']
        col_derecho_tipo = f['Col_DerechoTipo']
        r_local_id = f['OBJECTID'] # Had to do this because an automatic field with @row_number didn't work
        new_row = QgsVectorLayerUtils().createFeature(table_col_derecho)
        if numero_documento in dict_interesado and chip in dict_predio:
            new_row.setAttribute(ladm_attribute, dict_interesado[numero_documento])
            new_row.setAttribute("unidad_predio", dict_predio[chip])
            new_row.setAttribute("tipo", col_derecho_tipo)
            new_row.setAttribute("r_local_id", r_local_id)
            rows.append(new_row)
        else:
            print("### NOT FOUND NUM_DOCUMENTO-CHIP ###", numero_documento, chip)

    # Llenar col_derecho
    res = table_col_derecho.dataProvider().addFeatures(rows)
    if res[0]:
        print(len(rows), "rows added to col_derecho!!!")
    else:
        print("There was an error adding {} rows to col_derecho...".format(len(rows)))


def llenar_fuente_administrativa():
    params_refactor_fuente_administrativa = { 'INPUT' : '{}'.format(INPUT_PREDIO_INTERESADO_PATH), 'FIELDS_MAPPING' : [{'name': 't_id', 'type': 4, 'length': -1, 'precision': 0, 'expression': '"t_id"'}, {'name': 'texto', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"texto"'}, {'name': 'tipo', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"Col_FuenteAdministrativa"'}, {'name': 'codigo_registral_transaccion', 'type': 10, 'length': 3, 'precision': -1, 'expression': '"codigo_registral_transaccion"'}, {'name': 'fecha_aceptacion', 'type': 16, 'length': -1, 'precision': -1, 'expression': '"fecha_aceptacion"'}, {'name': 'estado_disponibilidad', 'type': 10, 'length': 255, 'precision': -1, 'expression': "'Disponible'"}, {'name': 'sello_inicio_validez', 'type': 16, 'length': -1, 'precision': -1, 'expression': '"sello_inicio_validez"'}, {'name': 'tipo_principal', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"tipo_principal"'}, {'name': 'fecha_grabacion', 'type': 16, 'length': -1, 'precision': -1, 'expression': '"fecha_grabacion"'}, {'name': 'fecha_entrega', 'type': 16, 'length': -1, 'precision': -1, 'expression': '"fecha_entrega"'}, {'name': 's_espacio_de_nombres', 'type': 10, 'length': 255, 'precision': -1, 'expression': "'UAECD_col_fuente_admin'"}, {'name': 's_local_id', 'type': 10, 'length': 255, 'precision': -1, 'expression': '"local_id"'}, {'name': 'oficialidad', 'type': 1, 'length': -1, 'precision': -1, 'expression': '"oficialidad"'}], 'OUTPUT' : 'ogr:dbname="{refactored_db_path}" table="R_col_fte_adminis" (geom) sql='.format(refactored_db_path=REFACTORED_DB_PATH) }
    input_uri_col_fte_adminis = '{refactored_db_path}|layername=R_col_fte_adminis'.format(refactored_db_path=REFACTORED_DB_PATH)
    db = asistente_ladm_col.get_db_connection()
    output_uri = db.get_uri_for_layer('col_fuenteadministrativa')[1]
    output_col_fte_adminis = QgsVectorLayer(output_uri, "col_fuenteadministrativa", "postgres")
    refactor_and_copy_paste(params_refactor_fuente_administrativa, input_uri_col_fte_adminis, output_col_fte_adminis)

def llenar_rrr_fuente():
    db = asistente_ladm_col.get_db_connection()
    output_uri_col_derecho = db.get_uri_for_layer('col_derecho')[1]
    output_uri_col_fuente_administrativa = db.get_uri_for_layer('col_fuenteadministrativa')[1]
    output_uri_rrr_fuente = db.get_uri_for_layer('rrrfuente')[1]
    output_col_derecho = QgsVectorLayer(output_uri_col_derecho, "col derecho", "postgres")
    output_col_fuente_administrativa = QgsVectorLayer(output_uri_col_fuente_administrativa, "fuente administrativa", "postgres")
    output_rrr_fuente = QgsVectorLayer(output_uri_rrr_fuente, "rrr fuente", "postgres")

    features_col_derecho = [f for f in output_col_derecho.getFeatures()]
    features = []
    for f in features_col_derecho:
        # Match col_derecho and col_fuenteadministrativa by local_id
        it_col_fuente_administrativa = output_col_fuente_administrativa.getFeatures('"s_local_id"=\'{}\''.format(f['r_local_id']))
        f_col_fuente_administrativa = QgsFeature()
        it_col_fuente_administrativa.nextFeature(f_col_fuente_administrativa)
        if f_col_fuente_administrativa.isValid():
            feature = QgsVectorLayerUtils().createFeature(output_rrr_fuente)
            feature.setAttribute('rrr_col_derecho', f['t_id'])
            feature.setAttribute('rfuente', f_col_fuente_administrativa['t_id'])
            features.append(feature)
        else:
            print("Col_derecho local id not found in fuente administrativa:",f['r_local_id'])

    output_rrr_fuente.startEditing()
    output_rrr_fuente.addFeatures(features)
    output_rrr_fuente.commitChanges()


llenar_punto_lindero()
llenar_lindero()
llenar_terreno() # First fix the source layer (with 'Fix Geometries' algorithm)
llenar_tablas_de_topologia()
llenar_predio()
llenar_uebaunit()
llenar_construccion('Construccion_NPH_Fixed') # First fix source layer geometries
llenar_construccion('Construccion_PH')
llenar_construccion('Construccion_MJ')
llenar_unidad_construccion()
llenar_interesado_natural()
llenar_interesado_juridico()
llenar_col_derecho('interesado_natural')
llenar_col_derecho('interesado_juridico')
llenar_fuente_administrativa()
llenar_rrr_fuente()
