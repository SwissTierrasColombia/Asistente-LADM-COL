"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin                : 2021-04-26
        copyright            : (C) 2021 by Germán Carrillo (SwissTierras Col)
        email                : gcarrillo@linuxmail.org
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
# Instrucciones de uso del script:
# https://github.com/SwissTierrasColombia/Asistente-LADM-COL/blob/master/scripts/qr_standalone_README.md

# ------------------------------------------------------------------------------
# ------------------------------ SET PARAMETERS --------------------------------
# ------------------------------------------------------------------------------
QGIS_PREFIX_PATH = '/docs/dev/qgis/QGIS/build_qgis_master/output'
QGIS_PROCESSING_PLUGIN_DIR = '/docs/dev/qgis/QGIS/build_qgis_master/output/python/plugins'
QGIS_PLUGINS_DIR = '/home/germap/.local/share/QGIS/QGIS3/profiles/demo/python/plugins'
OUTPUT_DIR = '/tmp'
TOLERANCE = 1  # In millimeters

# GEOPACKAGE
db_conn = {'dbfile': '/docs/geodata/gpkgs/pruebas/test_quality_rules_tolerance.gpkg'}

# POSTGRESQL / POSTGIS
#db_conn = {'host': 'localhost',
#           'port': '5432',
#           'database': 'lev_cat_1_1',
#           'schema': 'survey_07',
#           'username': 'postgres',
#           'password': 'postgres'}

quality_rules = [
    ##------------------------------ POINTS ------------------------------------
    #'1001',  # Los Puntos de Lindero no deben superponerse
    #'1002',  # Los Puntos de Control no deben superponerse
    #'1003',  # Los Puntos de Lindero deben estar cubiertos por nodos de Lindero
    #'1004',  # Los Puntos de Lindero deben estar cubiertos por nodos de Terreno
    ##------------------------------- LINES ------------------------------------
    #'2001',  # Los Linderos no deben superponerse
    #'2002',  # Los Linderos deben terminar en cambio de colindancia
    #'2003',  # Los Linderos deben estar cubiertos por límites de Terrenos
    #'2004',  # Los nodos de Lindero deben estar cubiertos por Puntos de Lindero
    #'2005',  # Los Linderos no deben tener nodos sin conectar
    ##----------------------------- POLYGONS -----------------------------------
    #'3001',  # Los Terrenos no deben superponerse
    #'3002',  # Las Construcciones no deben superponerse
    #'3003',  # Las Servidumbres de Tránsito no deben superponerse
    #'3004',  # Los límites de Terreno deben estar cubiertos por Linderos
    #'3005',  # Las Servidumbres de Tránsito no se deben superponer con Construcciones
    #'3006',  # No deben haber huecos entre Terrenos
    #'3007',  # Las servidumbres de Tránsito no deben tener geometrías multiparte
    #'3008',  # Los nodos de Terrenos deben estar cubiertos por Puntos de Lindero
    #'3009',  # Las Construcciones deben estar dentro de su Terreno correspondiente
    #'3010',  # Las Unidades de Construcción deben estar dentro de sus Terrenos correspondientes
    #'3011',  # Las Unidades de Construcción deben estar dentro de sus Construcciones correspondientes
    ##------------------------- LOGIC CONSISTENCY ------------------------------
    #'4001',  # Los Predios deben tener Derecho asociado y pueden tener máximo un Derecho de tipo Dominio asociado
    #'4002',  # Las fracciones de las Agrupaciones de Interesados deben sumar uno (1)
    #'4003',  # Revisar que el campo departamento de la tabla Predio tiene dos caracteres numéricos
    #'4004',  # Revisar que el campo municipio de la tabla Predio tiene tres caracteres numéricos
    #'4005',  # Revisar que el número predial tiene 30 caracteres numéricos
    #'4006',  # Revisar que el número predial anterior tiene 20 caracteres numéricos
    #'4007',  # Revisar que los interesados naturales no incluyan datos de interesados jurídicos
    #'4008',  # Revisar que los interesados jurídicos no incluyan datos de interesados naturales
    #'4009',  # Revisar que el tipo de Predio corresponde a la posición 22 del número predial
    #'4010',  # Revisar que las Unidades Espaciales asociadas a Predios correspondan al tipo de Predio
    #'4011',  # Punto Lindero no debe tener registros duplicados
    #'4012',  # Punto de Levantamiento no debe tener registros duplicados
    #'4013',  # Punto Control no debe tener registros duplicados
    #'4014',  # Lindero no debe tener registros duplicados
    #'4015',  # Terreno no debe tener registros duplicados
    #'4016',  # Construcción no debe tener registros duplicados
    #'4017',  # Unidad de Construcción no debe tener registros duplicados
    #'4018',  # Predio no debe tener registros duplicados
    #'4019',  # Interesado no debe tener registros duplicados
    #'4020',  # Derecho no debe tener registros duplicados
    #'4021',  # Restricción no debe tener registros duplicados
    #'4022'  # Fuente Administrativa no debe tener registros duplicados
]
if not quality_rules:
    raise Exception("Debes elegir al menos 1 regla de calidad!")


# ------------------------------------------------------------------------------
# ----------------------- CHECK OUTPUT FOLDER PERMISSIONS ----------------------
# ------------------------------------------------------------------------------
import os.path
import datetime
import tempfile

TIMESTAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

if not os.path.exists(OUTPUT_DIR):
    OUTPUT_DIR = tempfile.gettempdir()
    print("[WARNING] Output dir doesn't exist! Using now '{}'".format(OUTPUT_DIR))

OUTPUT_DIR = os.path.join(OUTPUT_DIR, "Reglas_de_Calidad_{}".format(TIMESTAMP))
try:
    os.makedirs(OUTPUT_DIR)
except PermissionError as e:
    raise Exception(
        "[ERROR] No tienes permisos de escritura en la carpeta '{}' ".format(
            OUTPUT_DIR))


# ------------------------------------------------------------------------------
# -------------------------------- START QGIS ----------------------------------
# ------------------------------------------------------------------------------

import sys
from qgis.core import (QgsApplication, 
                       QgsProcessingFeedback,
                       Qgis)
from qgis.analysis import QgsNativeAlgorithms
from qgis.testing import (unittest,
                          start_app)
import qgis.utils

start_app()


QgsApplication.setPrefixPath(QGIS_PREFIX_PATH, True)
qgs = QgsApplication([], False)
qgs.initQgis()


# ------------------------------------------------------------------------------
# ----------------------------- START PROCESSING -------------------------------
# ------------------------------------------------------------------------------

sys.path.append(QGIS_PROCESSING_PLUGIN_DIR)
import processing
from processing.core.Processing import Processing
Processing.initialize()
if Qgis.QGIS_VERSION_INT < 31605:
    QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
print("[INFO] Processing initialized!")


# ------------------------------------------------------------------------------
# ---------------------------- START MODEL BAKER -------------------------------
# ------------------------------------------------------------------------------

from qgis.testing.mocked import get_iface
iface = get_iface()
sys.path.append(QGIS_PLUGINS_DIR)

def import_qgis_model_baker():
    global iface
    plugin_found = "QgisModelBaker" in qgis.utils.plugins
    if not plugin_found:
        import QgisModelBaker
        pg = QgisModelBaker.classFactory(iface)
        qgis.utils.plugins["QgisModelBaker"] = pg

import_qgis_model_baker()
print("[INFO] Model Baker initialized!")


# ------------------------------------------------------------------------------
# ------------------------- START ASISTENTE LADM-COL ---------------------------
# ------------------------------------------------------------------------------

from asistente_ladm_col.asistente_ladm_col_plugin import AsistenteLADMCOLPlugin
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.logic.quality.quality_rule_engine import QualityRuleEngine
from asistente_ladm_col.config.enums import EnumQualityRule
from asistente_ladm_col.utils.qt_utils import export_title_text_to_pdf

asistente_ladm_col_plugin = AsistenteLADMCOLPlugin(iface, False)
asistente_ladm_col_plugin.initGui()

print("[INFO] Asistente LADM-COL initialized!")


# ------------------------------------------------------------------------------
# ------------------------- PREPARE ENVIRONMENT FOR QR -------------------------
# ------------------------------------------------------------------------------

app = AppInterface()
provider = 'gpkg' if 'dbfile' in db_conn else 'pg'
db = asistente_ladm_col_plugin.conn_manager.get_opened_db_connector_for_tests(
        provider,
        db_conn)
res_tc, code, msg = db.test_connection()  # To initialize DBMappingRegistry obj.
if not res_tc:
    raise Exception("Base de datos inválida!\n\t{}".format(msg))

def get_qr_key(key):
    if key.startswith('1'):
        return EnumQualityRule.Point(int(key))
    elif key.startswith('2'):
        return EnumQualityRule.Line(int(key))
    elif key.startswith('3'):
        return EnumQualityRule.Polygon(int(key))
    elif key.startswith('4'):
        return EnumQualityRule.Logic(int(key))

quality_rules = [get_qr_key(k) for k in quality_rules]
qr_engine = QualityRuleEngine(db, quality_rules, TOLERANCE)


# ------------------------------------------------------------------------------
# ------------------------------ RUN QUALITY RULES -----------------------------
# ------------------------------------------------------------------------------

print("\n[INFO] Testing {} quality rules with {}mm of tolerance...".format(
    len(quality_rules),
    TOLERANCE))
res = qr_engine.validate_quality_rules()


# ------------------------------------------------------------------------------
# ------------------------------- PREPARE RESULTS ------------------------------
# ------------------------------------------------------------------------------

print(res.result(quality_rules[0]).msg, res.result(quality_rules[0]).level)
print("\n[INFO] Results can be found at '{}'!".format(OUTPUT_DIR))

# GeoPackage (only if at least 1 error is found)
error_layers = res.all_error_layers()
if error_layers:
    gpkg_filepath = os.path.join(OUTPUT_DIR, 
                                 "Reglas_de_Calidad_{}.gpkg".format(TIMESTAMP))
    processing.run("native:package", {
                   "LAYERS": error_layers,
                   "OUTPUT": gpkg_filepath,
                   "OVERWRITE": False,
                   "SAVE_STYLES": True},
                   feedback=QgsProcessingFeedback())

# PDF report
log_result = qr_engine.quality_rule_logger.get_log_result()
pdf_filepath = os.path.join(OUTPUT_DIR, 
                            "Reporte_Reglas_de_Calidad_{}.pdf".format(
                            TIMESTAMP))
export_title_text_to_pdf(pdf_filepath, log_result.title, log_result.text)

print("\n[INFO] Done!")
