from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.logic.ladm_col.config.queries.pg.pg_queries_config_utils import (get_custom_filter_parcels,
                                                                                         get_custom_filter_plots)


def get_igac_legal_query(names, schema, plot_t_ids, parcel_fmi, parcel_number, previous_parcel_number):
    custom_filter_plots = get_custom_filter_plots(names, schema, plot_t_ids)
    custom_filter_parcels = get_custom_filter_parcels(names, schema, plot_t_ids)

    query = """
            WITH
             _unidad_area_terreno AS (
                 SELECT ' [' || setting || ']' FROM {schema}.t_ili2db_column_prop WHERE tablename = '{LC_PLOT_T}' AND columnname = '{LC_PLOT_T_PLOT_AREA_F}' LIMIT 1
             ),
             _terrenos_seleccionados AS (
                {custom_filter_plots}
                SELECT {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F} FROM {schema}.{LC_PARCEL_T} LEFT JOIN {schema}.{COL_UE_BAUNIT_T} ON {LC_PARCEL_T}.{T_ID_F} = {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_PARCEL_F}  WHERE {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F} IS NOT NULL AND CASE WHEN '{parcel_fmi}' = 'NULL' THEN  1 = 2 ELSE ({LC_PARCEL_T}.{LC_PARCEL_T_ORIP_CODE_F} || '-'|| {LC_PARCEL_T}.{LC_PARCEL_T_FMI_F}) = '{parcel_fmi}' END
                    UNION
                SELECT {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F} FROM {schema}.{LC_PARCEL_T} LEFT JOIN {schema}.{COL_UE_BAUNIT_T} ON {LC_PARCEL_T}.{T_ID_F} = {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_PARCEL_F}  WHERE {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F} IS NOT NULL AND CASE WHEN '{parcel_number}' = 'NULL' THEN  1 = 2 ELSE {LC_PARCEL_T}.{LC_PARCEL_T_PARCEL_NUMBER_F} = '{parcel_number}' END
                    UNION
                SELECT {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F} FROM {schema}.{LC_PARCEL_T} LEFT JOIN {schema}.{COL_UE_BAUNIT_T} ON {LC_PARCEL_T}.{T_ID_F} = {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_PARCEL_F}  WHERE {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F} IS NOT NULL AND CASE WHEN '{previous_parcel_number}' = 'NULL' THEN  1 = 2 ELSE {LC_PARCEL_T}.{LC_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F} = '{previous_parcel_number}' END
             ),
             _predios_seleccionados AS (
                {custom_filter_parcels}
                SELECT {T_ID_F} FROM {schema}.{LC_PARCEL_T} WHERE CASE WHEN '{parcel_fmi}' = 'NULL' THEN  1 = 2 ELSE ({LC_PARCEL_T}.{LC_PARCEL_T_ORIP_CODE_F} || '-'|| {LC_PARCEL_T}.{LC_PARCEL_T_FMI_F}) = '{parcel_fmi}' END
                    UNION
                SELECT {T_ID_F} FROM {schema}.{LC_PARCEL_T} WHERE CASE WHEN '{parcel_number}' = 'NULL' THEN  1 = 2 ELSE {LC_PARCEL_T}.{LC_PARCEL_T_PARCEL_NUMBER_F} = '{parcel_number}' END
                    UNION
                SELECT {T_ID_F} FROM {schema}.{LC_PARCEL_T} WHERE CASE WHEN '{previous_parcel_number}' = 'NULL' THEN  1 = 2 ELSE {LC_PARCEL_T}.{LC_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F} = '{previous_parcel_number}' END
             ),
             _derechos_seleccionados AS (
                 SELECT DISTINCT {LC_RIGHT_T}.{T_ID_F} FROM {schema}.{LC_RIGHT_T} WHERE {LC_RIGHT_T}.{COL_BAUNIT_RRR_T_UNIT_F} IN (SELECT * FROM _predios_seleccionados)
             ),
             _derecho_interesados AS (
                 SELECT DISTINCT {LC_RIGHT_T}.{COL_RRR_PARTY_T_LC_PARTY_F}, {LC_RIGHT_T}.{T_ID_F} FROM {schema}.{LC_RIGHT_T} WHERE {LC_RIGHT_T}.{T_ID_F} IN (SELECT * FROM _derechos_seleccionados) AND {LC_RIGHT_T}.{COL_RRR_PARTY_T_LC_PARTY_F} IS NOT NULL
             ),
             _derecho_agrupacion_interesados AS (
                 SELECT DISTINCT {LC_RIGHT_T}.{COL_RRR_PARTY_T_LC_GROUP_PARTY_F}, {MEMBERS_T}.{MEMBERS_T_PARTY_F}
                 FROM {schema}.{LC_RIGHT_T} LEFT JOIN {schema}.{MEMBERS_T} ON {LC_RIGHT_T}.{COL_RRR_PARTY_T_LC_GROUP_PARTY_F} = {MEMBERS_T}.{MEMBERS_T_GROUP_PARTY_F}
                 WHERE {LC_RIGHT_T}.{T_ID_F} IN (SELECT * FROM _derechos_seleccionados) AND {LC_RIGHT_T}.{COL_RRR_PARTY_T_LC_GROUP_PARTY_F} IS NOT NULL
             ),
              _restricciones_seleccionadas AS (
                 SELECT DISTINCT {LC_RESTRICTION_T}.{T_ID_F} FROM {schema}.{LC_RESTRICTION_T} WHERE {LC_RESTRICTION_T}.{COL_BAUNIT_RRR_T_UNIT_F} IN (SELECT * FROM _predios_seleccionados)
             ),
             _restriccion_interesados AS (
                 SELECT DISTINCT {LC_RESTRICTION_T}.{COL_RRR_PARTY_T_LC_PARTY_F}, {LC_RESTRICTION_T}.{T_ID_F} FROM {schema}.{LC_RESTRICTION_T} WHERE {LC_RESTRICTION_T}.{T_ID_F} IN (SELECT * FROM _restricciones_seleccionadas) AND {LC_RESTRICTION_T}.{COL_RRR_PARTY_T_LC_PARTY_F} IS NOT NULL
             ),
             _restriccion_agrupacion_interesados AS (
                 SELECT DISTINCT {LC_RESTRICTION_T}.{COL_RRR_PARTY_T_LC_GROUP_PARTY_F}, {MEMBERS_T}.{MEMBERS_T_PARTY_F}
                 FROM {schema}.{LC_RESTRICTION_T} LEFT JOIN {schema}.{MEMBERS_T} ON {LC_RESTRICTION_T}.{COL_RRR_PARTY_T_LC_GROUP_PARTY_F} = {MEMBERS_T}.{MEMBERS_T_GROUP_PARTY_F}
                 WHERE {LC_RESTRICTION_T}.{T_ID_F} IN (SELECT * FROM _restricciones_seleccionadas) AND {LC_RESTRICTION_T}.{COL_RRR_PARTY_T_LC_GROUP_PARTY_F} IS NOT NULL
             ),
             _info_contacto_interesados_derecho AS (
                    SELECT {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_LC_PARTY_F},
                      JSON_AGG(
                            JSON_BUILD_OBJECT('id', {LC_PARTY_CONTACT_T}.{T_ID_F},
                                                   'attributes', JSON_BUILD_OBJECT('Teléfono 1', {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_TELEPHONE_NUMBER_1_F},
                                                                                   'Teléfono 2', {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_TELEPHONE_NUMBER_2_F},
                                                                                   'Domicilio notificación', {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_NOTIFICATION_ADDRESS_F},
                                                                                   'Correo electrónico', {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_EMAIL_F})) ORDER BY {LC_PARTY_CONTACT_T}.{T_ID_F})
                    FILTER(WHERE {LC_PARTY_CONTACT_T}.{T_ID_F} IS NOT NULL) AS _interesado_contacto_
                    FROM {schema}.{LC_PARTY_CONTACT_T}
                    WHERE {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_LC_PARTY_F} IN (SELECT _derecho_interesados.{COL_RRR_PARTY_T_LC_PARTY_F} FROM _derecho_interesados)
                    GROUP BY {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_LC_PARTY_F}
             ),
             _info_interesados_derecho AS (
                 SELECT _derecho_interesados.{T_ID_F},
                  JSON_AGG(
                    JSON_BUILD_OBJECT('id', {LC_PARTY_T}.{T_ID_F},
                                      'attributes', JSON_BUILD_OBJECT('Tipo', (SELECT {DISPLAY_NAME_F} FROM {schema}.{LC_PARTY_TYPE_D} WHERE {T_ID_F} = {LC_PARTY_T}.{LC_PARTY_T_TYPE_F}),
                                                                      {LC_PARTY_DOCUMENT_TYPE_D}.{DISPLAY_NAME_F}, {LC_PARTY_T}.{LC_PARTY_T_DOCUMENT_ID_F},
                                                                      'Nombre', {LC_PARTY_T}.{COL_BAUNIT_T_NAME_F},
                                                                      CASE WHEN {LC_PARTY_T}.{LC_PARTY_T_TYPE_F} = 9 THEN 'Tipo interesado jurídico' ELSE 'Género' END,
                                                                      CASE WHEN {LC_PARTY_T}.{LC_PARTY_T_TYPE_F} = 9 THEN (SELECT {DISPLAY_NAME_F} FROM {schema}.{LC_PARTY_TYPE_D} WHERE {T_ID_F} = {LC_PARTY_T}.{LC_PARTY_T_TYPE_F}) ELSE (SELECT {DISPLAY_NAME_F} FROM {schema}.{LC_GENRE_D} WHERE {T_ID_F} = {LC_PARTY_T}.{LC_PARTY_T_GENRE_F}) END,
                                                                      '{LC_PARTY_CONTACT_T}', COALESCE(_info_contacto_interesados_derecho._interesado_contacto_, '[]')))
                 ORDER BY {LC_PARTY_T}.{T_ID_F}) FILTER (WHERE {LC_PARTY_T}.{T_ID_F} IS NOT NULL) AS _interesado_
                 FROM _derecho_interesados LEFT JOIN {schema}.{LC_PARTY_T} ON {LC_PARTY_T}.{T_ID_F} = _derecho_interesados.{COL_RRR_PARTY_T_LC_PARTY_F}
               LEFT JOIN {schema}.{LC_PARTY_DOCUMENT_TYPE_D} ON {LC_PARTY_DOCUMENT_TYPE_D}.{T_ID_F} = {LC_PARTY_T}.{LC_PARTY_T_DOCUMENT_TYPE_F}
                 LEFT JOIN _info_contacto_interesados_derecho ON _info_contacto_interesados_derecho.{LC_PARTY_CONTACT_T_LC_PARTY_F} = {LC_PARTY_T}.{T_ID_F}
                 GROUP BY _derecho_interesados.{T_ID_F}
             ),
             _info_contacto_interesado_agrupacion_interesados_derecho AS (
                    SELECT {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_LC_PARTY_F},
                      JSON_AGG(
                            JSON_BUILD_OBJECT('id', {LC_PARTY_CONTACT_T}.{T_ID_F},
                                                   'attributes', JSON_BUILD_OBJECT('Teléfono 1', {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_TELEPHONE_NUMBER_1_F},
                                                                                   'Teléfono 2', {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_TELEPHONE_NUMBER_2_F},
                                                                                   'Domicilio notificación', {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_NOTIFICATION_ADDRESS_F},
                                                                                   'Correo electrónico', {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_EMAIL_F})) ORDER BY {LC_PARTY_CONTACT_T}.{T_ID_F})
                    FILTER(WHERE {LC_PARTY_CONTACT_T}.{T_ID_F} IS NOT NULL) AS _interesado_contacto_
                    FROM {schema}.{LC_PARTY_CONTACT_T} LEFT JOIN _derecho_interesados ON _derecho_interesados.{COL_RRR_PARTY_T_LC_PARTY_F} = {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_LC_PARTY_F}
                    WHERE {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_LC_PARTY_F} IN (SELECT DISTINCT _derecho_agrupacion_interesados.{MEMBERS_T_PARTY_F} FROM _derecho_agrupacion_interesados)
                    GROUP BY {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_LC_PARTY_F}
             ),
             _info_interesados_agrupacion_interesados_derecho AS (
                 SELECT _derecho_agrupacion_interesados.{COL_RRR_PARTY_T_LC_GROUP_PARTY_F},
                  JSON_AGG(
                    JSON_BUILD_OBJECT('id', {LC_PARTY_T}.{T_ID_F},
                                      'attributes', JSON_BUILD_OBJECT('Tipo', (SELECT {DISPLAY_NAME_F} FROM {schema}.{LC_PARTY_TYPE_D} WHERE {T_ID_F} = {LC_PARTY_T}.{LC_PARTY_T_TYPE_F}),
                                                                      {LC_PARTY_DOCUMENT_TYPE_D}.{DISPLAY_NAME_F}, {LC_PARTY_T}.{LC_PARTY_T_DOCUMENT_ID_F},
                                                                      'Nombre', {LC_PARTY_T}.{COL_BAUNIT_T_NAME_F},
                                                                      'Género', (SELECT {DISPLAY_NAME_F} FROM {schema}.{LC_GENRE_D} WHERE {T_ID_F} = {LC_PARTY_T}.{LC_PARTY_T_GENRE_F}),
                                                                      '{LC_PARTY_CONTACT_T}', COALESCE(_info_contacto_interesado_agrupacion_interesados_derecho._interesado_contacto_, '[]'),
                                                                      '{FRACTION_S}', ROUND(({FRACTION_S}.{FRACTION_S_NUMERATOR_F}::numeric/{FRACTION_S}.{FRACTION_S_DENOMINATOR_F}::numeric)*100,2) ))
                 ORDER BY {LC_PARTY_T}.{T_ID_F}) FILTER (WHERE {LC_PARTY_T}.{T_ID_F} IS NOT NULL) AS _interesado_
                 FROM _derecho_agrupacion_interesados LEFT JOIN {schema}.{LC_PARTY_T} ON {LC_PARTY_T}.{T_ID_F} = _derecho_agrupacion_interesados.{MEMBERS_T_PARTY_F}
               LEFT JOIN {schema}.{LC_PARTY_DOCUMENT_TYPE_D} ON {LC_PARTY_DOCUMENT_TYPE_D}.{T_ID_F} = {LC_PARTY_T}.{LC_PARTY_T_DOCUMENT_TYPE_F}
                 LEFT JOIN _info_contacto_interesado_agrupacion_interesados_derecho ON _info_contacto_interesado_agrupacion_interesados_derecho.{LC_PARTY_CONTACT_T_LC_PARTY_F} = {LC_PARTY_T}.{T_ID_F}
                 LEFT JOIN {schema}.{MEMBERS_T} ON ({MEMBERS_T}.{MEMBERS_T_GROUP_PARTY_F}::text || {MEMBERS_T}.{MEMBERS_T_PARTY_F}::text) = (_derecho_agrupacion_interesados.{COL_RRR_PARTY_T_LC_GROUP_PARTY_F}::text|| {LC_PARTY_T}.{T_ID_F}::text)
                 LEFT JOIN {schema}.{FRACTION_S} ON {MEMBERS_T}.{T_ID_F} = {FRACTION_S}.{FRACTION_S_MEMBER_F}
                 GROUP BY _derecho_agrupacion_interesados.{COL_RRR_PARTY_T_LC_GROUP_PARTY_F}
             ),
             _info_agrupacion_interesados AS (
                 SELECT {LC_RIGHT_T}.{T_ID_F},
                 JSON_AGG(
                    JSON_BUILD_OBJECT('id', {LC_GROUP_PARTY_T}.{T_ID_F},
                                      'attributes', JSON_BUILD_OBJECT('Tipo de agrupación de interesados', (SELECT {DISPLAY_NAME_F} FROM {schema}.{COL_GROUP_PARTY_TYPE_D} WHERE {T_ID_F} = {LC_GROUP_PARTY_T}.{COL_GROUP_PARTY_T_TYPE_F}),
                                                                      'Nombre', {LC_GROUP_PARTY_T}.{COL_BAUNIT_T_NAME_F},
                                                                      '{LC_PARTY_T}', COALESCE(_info_interesados_agrupacion_interesados_derecho._interesado_, '[]')))
                 ORDER BY {LC_GROUP_PARTY_T}.{T_ID_F}) FILTER (WHERE {LC_GROUP_PARTY_T}.{T_ID_F} IS NOT NULL) AS _agrupacioninteresados_
                 FROM {schema}.{LC_GROUP_PARTY_T} LEFT JOIN {schema}.{LC_RIGHT_T} ON {LC_GROUP_PARTY_T}.{T_ID_F} = {LC_RIGHT_T}.{COL_RRR_PARTY_T_LC_GROUP_PARTY_F}
                 LEFT JOIN _info_interesados_agrupacion_interesados_derecho ON _info_interesados_agrupacion_interesados_derecho.{COL_RRR_PARTY_T_LC_GROUP_PARTY_F} = {LC_GROUP_PARTY_T}.{T_ID_F}
                 WHERE {LC_GROUP_PARTY_T}.{T_ID_F} IN (SELECT DISTINCT _derecho_agrupacion_interesados.{COL_RRR_PARTY_T_LC_GROUP_PARTY_F} FROM _derecho_agrupacion_interesados)
                 AND {LC_RIGHT_T}.{T_ID_F} IN (SELECT _derechos_seleccionados.{T_ID_F} FROM _derechos_seleccionados)
                 GROUP BY {LC_RIGHT_T}.{T_ID_F}
             ),
             _info_fuentes_administrativas_derecho AS (
                SELECT {LC_RIGHT_T}.{T_ID_F},
                 JSON_AGG(
                    JSON_BUILD_OBJECT('id', {LC_ADMINISTRATIVE_SOURCE_T}.{T_ID_F},
                                      'attributes', JSON_BUILD_OBJECT('Tipo de fuente administrativa', (SELECT {DISPLAY_NAME_F} FROM {schema}.{COL_ADMINISTRATIVE_SOURCE_TYPE_D} WHERE {T_ID_F} = {LC_ADMINISTRATIVE_SOURCE_T}.{LC_ADMINISTRATIVE_SOURCE_T_TYPE_F}),
                                                                      'Ente emisor', {LC_ADMINISTRATIVE_SOURCE_T}.{LC_ADMINISTRATIVE_SOURCE_T_EMITTING_ENTITY_F},
                                                                      'Estado disponibilidad', (SELECT {DISPLAY_NAME_F} FROM {schema}.{COL_AVAILABILITY_TYPE_D} WHERE {T_ID_F} = {LC_ADMINISTRATIVE_SOURCE_T}.{COL_SOURCE_T_AVAILABILITY_STATUS_F}),
                                                                      'Archivo fuente', {EXT_ARCHIVE_S}.{EXT_ARCHIVE_S_DATA_F}))
                 ORDER BY {LC_ADMINISTRATIVE_SOURCE_T}.{T_ID_F}) FILTER (WHERE {LC_ADMINISTRATIVE_SOURCE_T}.{T_ID_F} IS NOT NULL) AS _fuenteadministrativa_
                FROM {schema}.{LC_RIGHT_T}
                LEFT JOIN {schema}.{COL_RRR_SOURCE_T} ON {LC_RIGHT_T}.{T_ID_F} = {COL_RRR_SOURCE_T}.{COL_RRR_SOURCE_T_LC_RIGHT_F}
                LEFT JOIN {schema}.{LC_ADMINISTRATIVE_SOURCE_T} ON {COL_RRR_SOURCE_T}.{COL_RRR_SOURCE_T_SOURCE_F} = {LC_ADMINISTRATIVE_SOURCE_T}.{T_ID_F}
                LEFT JOIN {schema}.{EXT_ARCHIVE_S} ON {EXT_ARCHIVE_S}.{EXT_ARCHIVE_S_LC_ADMINISTRATIVE_SOURCE_F} = {LC_ADMINISTRATIVE_SOURCE_T}.{T_ID_F}
                WHERE {LC_RIGHT_T}.{T_ID_F} IN (SELECT _derechos_seleccionados.{T_ID_F} FROM _derechos_seleccionados)
                GROUP BY {LC_RIGHT_T}.{T_ID_F}
             ),
            _info_derecho AS (
              SELECT {LC_RIGHT_T}.{COL_BAUNIT_RRR_T_UNIT_F},
                JSON_AGG(
                    JSON_BUILD_OBJECT('id', {LC_RIGHT_T}.{T_ID_F},
                                      'attributes', JSON_BUILD_OBJECT('Tipo de derecho', (SELECT {DISPLAY_NAME_F} FROM {schema}.{LC_RIGHT_TYPE_D} WHERE {T_ID_F} = {LC_RIGHT_T}.{LC_RIGHT_T_TYPE_F}),
                                                                      'Descripción', {LC_RIGHT_T}.{COL_RRR_T_DESCRIPTION_F},
                                                                      '{LC_ADMINISTRATIVE_SOURCE_T}', COALESCE(_info_fuentes_administrativas_derecho._fuenteadministrativa_, '[]'),
                                                                      '{LC_PARTY_T}', COALESCE(_info_interesados_derecho._interesado_, '[]'),
                                                                      '{LC_GROUP_PARTY_T}', COALESCE(_info_agrupacion_interesados._agrupacioninteresados_, '[]')))
                 ORDER BY {LC_RIGHT_T}.{T_ID_F}) FILTER (WHERE {LC_RIGHT_T}.{T_ID_F} IS NOT NULL) AS _derecho_
              FROM {schema}.{LC_RIGHT_T} LEFT JOIN _info_fuentes_administrativas_derecho ON {LC_RIGHT_T}.{T_ID_F} = _info_fuentes_administrativas_derecho.{T_ID_F}
              LEFT JOIN _info_interesados_derecho ON {LC_RIGHT_T}.{T_ID_F} = _info_interesados_derecho.{T_ID_F}
              LEFT JOIN _info_agrupacion_interesados ON {LC_RIGHT_T}.{T_ID_F} = _info_agrupacion_interesados.{T_ID_F}
              WHERE {LC_RIGHT_T}.{T_ID_F} IN (SELECT * FROM _derechos_seleccionados)
              GROUP BY {LC_RIGHT_T}.{COL_BAUNIT_RRR_T_UNIT_F}
            ),
             _info_contacto_interesados_restriccion AS (
                    SELECT {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_LC_PARTY_F},
                      JSON_AGG(
                            JSON_BUILD_OBJECT('id', {LC_PARTY_CONTACT_T}.{T_ID_F},
                                                   'attributes', JSON_BUILD_OBJECT('Teléfono 1', {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_TELEPHONE_NUMBER_1_F},
                                                                                   'Teléfono 2', {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_TELEPHONE_NUMBER_2_F},
                                                                                   'Domicilio notificación', {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_NOTIFICATION_ADDRESS_F},
                                                                                   'Correo electrónico', {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_EMAIL_F})) ORDER BY {LC_PARTY_CONTACT_T}.{T_ID_F})
                    FILTER(WHERE {LC_PARTY_CONTACT_T}.{T_ID_F} IS NOT NULL) AS _interesado_contacto_
                    FROM {schema}.{LC_PARTY_CONTACT_T}
                    WHERE {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_LC_PARTY_F} IN (SELECT _restriccion_interesados.{COL_RRR_PARTY_T_LC_PARTY_F} FROM _restriccion_interesados)
                    GROUP BY {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_LC_PARTY_F}
             ),
             _info_interesados_restriccion AS (
                 SELECT _restriccion_interesados.{T_ID_F},
                  JSON_AGG(
                    JSON_BUILD_OBJECT('id', {LC_PARTY_T}.{T_ID_F},
                                      'attributes', JSON_BUILD_OBJECT('Tipo', {LC_PARTY_T}.{LC_PARTY_T_TYPE_F},
                                                                      {LC_PARTY_DOCUMENT_TYPE_D}.{DISPLAY_NAME_F}, {LC_PARTY_T}.{LC_PARTY_T_DOCUMENT_ID_F},
                                                                      'Nombre', {LC_PARTY_T}.{COL_BAUNIT_T_NAME_F},
                                                                      CASE WHEN {LC_PARTY_T}.{LC_PARTY_T_TYPE_F} = (SELECT {T_ID_F} FROM {schema}.{LC_PARTY_TYPE_D} WHERE {ILICODE_F} LIKE '{LC_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V}') THEN 'Tipo interesado jurídico' ELSE 'Género' END,
                                                                      CASE WHEN {LC_PARTY_T}.{LC_PARTY_T_TYPE_F} = (SELECT {T_ID_F} FROM {schema}.{LC_PARTY_TYPE_D} WHERE {ILICODE_F} LIKE '{LC_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V}') THEN (SELECT {DISPLAY_NAME_F} FROM {schema}.{LC_PARTY_TYPE_D} WHERE {T_ID_F} = {LC_PARTY_T}.{LC_PARTY_T_TYPE_F}) ELSE (SELECT {DISPLAY_NAME_F} FROM {schema}.{LC_GENRE_D} WHERE {T_ID_F} = {LC_PARTY_T}.{LC_PARTY_T_GENRE_F}) END,
                                                                      '{LC_PARTY_CONTACT_T}', COALESCE(_info_contacto_interesados_restriccion._interesado_contacto_, '[]')))
                 ORDER BY {LC_PARTY_T}.{T_ID_F}) FILTER (WHERE {LC_PARTY_T}.{T_ID_F} IS NOT NULL) AS _interesado_
                 FROM _restriccion_interesados LEFT JOIN {schema}.{LC_PARTY_T} ON {LC_PARTY_T}.{T_ID_F} = _restriccion_interesados.{COL_RRR_PARTY_T_LC_PARTY_F}
                 LEFT JOIN {schema}.{LC_PARTY_DOCUMENT_TYPE_D} ON {LC_PARTY_DOCUMENT_TYPE_D}.{T_ID_F} = {LC_PARTY_T}.{LC_PARTY_T_DOCUMENT_TYPE_F}
                 LEFT JOIN _info_contacto_interesados_restriccion ON _info_contacto_interesados_restriccion.{LC_PARTY_CONTACT_T_LC_PARTY_F} = {LC_PARTY_T}.{T_ID_F}
                 GROUP BY _restriccion_interesados.{T_ID_F}
             ),
             _info_contacto_interesado_agrupacion_interesados_restriccion AS (
                    SELECT {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_LC_PARTY_F},
                      JSON_AGG(
                            JSON_BUILD_OBJECT('id', {LC_PARTY_CONTACT_T}.{T_ID_F},
                                                   'attributes', JSON_BUILD_OBJECT('Teléfono 1', {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_TELEPHONE_NUMBER_1_F},
                                                                                   'Teléfono 2', {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_TELEPHONE_NUMBER_2_F},
                                                                                   'Domicilio notificación', {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_NOTIFICATION_ADDRESS_F},
                                                                                   'Correo electrónico', {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_EMAIL_F})) ORDER BY {LC_PARTY_CONTACT_T}.{T_ID_F})
                    FILTER(WHERE {LC_PARTY_CONTACT_T}.{T_ID_F} IS NOT NULL) AS _interesado_contacto_
                    FROM {schema}.{LC_PARTY_CONTACT_T} LEFT JOIN _restriccion_interesados ON _restriccion_interesados.{COL_RRR_PARTY_T_LC_PARTY_F} = {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_LC_PARTY_F}
                    WHERE {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_LC_PARTY_F} IN (SELECT DISTINCT _restriccion_agrupacion_interesados.{MEMBERS_T_PARTY_F} FROM _restriccion_agrupacion_interesados)
                    GROUP BY {LC_PARTY_CONTACT_T}.{LC_PARTY_CONTACT_T_LC_PARTY_F}
             ),
             _info_interesados_agrupacion_interesados_restriccion AS (
                 SELECT _restriccion_agrupacion_interesados.{COL_RRR_PARTY_T_LC_GROUP_PARTY_F},
                  JSON_AGG(
                    JSON_BUILD_OBJECT('id', {LC_PARTY_T}.{T_ID_F},
                                      'attributes', JSON_BUILD_OBJECT('Tipo', (SELECT {DISPLAY_NAME_F} FROM {schema}.{LC_PARTY_TYPE_D} WHERE {T_ID_F} = {LC_PARTY_T}.{LC_PARTY_T_TYPE_F}),
                                                                      {LC_PARTY_DOCUMENT_TYPE_D}.{DISPLAY_NAME_F}, {LC_PARTY_T}.{LC_PARTY_T_DOCUMENT_ID_F},
                                                                      'Nombre', {LC_PARTY_T}.{COL_BAUNIT_T_NAME_F},
                                                                      'Género', (SELECT {DISPLAY_NAME_F} FROM {schema}.{LC_GENRE_D} WHERE {T_ID_F} = {LC_PARTY_T}.{LC_PARTY_T_GENRE_F}),
                                                                      '{LC_PARTY_CONTACT_T}', COALESCE(_info_contacto_interesado_agrupacion_interesados_restriccion._interesado_contacto_, '[]'),
                                                                      '{FRACTION_S}', ROUND(({FRACTION_S}.{FRACTION_S_NUMERATOR_F}::numeric/{FRACTION_S}.{FRACTION_S_DENOMINATOR_F}::numeric)*100,2) ))
                 ORDER BY {LC_PARTY_T}.{T_ID_F}) FILTER (WHERE {LC_PARTY_T}.{T_ID_F} IS NOT NULL) AS _interesado_
                 FROM _restriccion_agrupacion_interesados LEFT JOIN {schema}.{LC_PARTY_T} ON {LC_PARTY_T}.{T_ID_F} = _restriccion_agrupacion_interesados.{MEMBERS_T_PARTY_F}
               LEFT JOIN {schema}.{LC_PARTY_DOCUMENT_TYPE_D} ON {LC_PARTY_DOCUMENT_TYPE_D}.{T_ID_F} = {LC_PARTY_T}.{LC_PARTY_T_DOCUMENT_TYPE_F}
                 LEFT JOIN _info_contacto_interesado_agrupacion_interesados_restriccion ON _info_contacto_interesado_agrupacion_interesados_restriccion.{LC_PARTY_CONTACT_T_LC_PARTY_F} = {LC_PARTY_T}.{T_ID_F}
                 LEFT JOIN {schema}.{MEMBERS_T} ON ({MEMBERS_T}.{MEMBERS_T_GROUP_PARTY_F}::text || {MEMBERS_T}.{MEMBERS_T_PARTY_F}::text) = (_restriccion_agrupacion_interesados.{COL_RRR_PARTY_T_LC_GROUP_PARTY_F}::text|| {LC_PARTY_T}.{T_ID_F}::text)
                 LEFT JOIN {schema}.{FRACTION_S} ON {MEMBERS_T}.{T_ID_F} = {FRACTION_S}.{FRACTION_S_MEMBER_F}
                 GROUP BY _restriccion_agrupacion_interesados.{COL_RRR_PARTY_T_LC_GROUP_PARTY_F}
             ),
             _info_agrupacion_interesados_restriccion AS (
                 SELECT {LC_RESTRICTION_T}.{T_ID_F},
                 JSON_AGG(
                    JSON_BUILD_OBJECT('id', {LC_GROUP_PARTY_T}.{T_ID_F},
                                      'attributes', JSON_BUILD_OBJECT('Tipo de agrupación de interesados', (SELECT {DISPLAY_NAME_F} FROM {schema}.{COL_GROUP_PARTY_TYPE_D} WHERE {T_ID_F} = {LC_GROUP_PARTY_T}.{COL_GROUP_PARTY_T_TYPE_F}),
                                                                      'Nombre', {LC_GROUP_PARTY_T}.{COL_BAUNIT_T_NAME_F},
                                                                      '{LC_PARTY_T}', COALESCE(_info_interesados_agrupacion_interesados_restriccion._interesado_, '[]')))
                 ORDER BY {LC_GROUP_PARTY_T}.{T_ID_F}) FILTER (WHERE {LC_GROUP_PARTY_T}.{T_ID_F} IS NOT NULL) AS _agrupacioninteresados_
                 FROM {schema}.{LC_GROUP_PARTY_T} LEFT JOIN {schema}.{LC_RESTRICTION_T} ON {LC_GROUP_PARTY_T}.{T_ID_F} = {LC_RESTRICTION_T}.{COL_RRR_PARTY_T_LC_GROUP_PARTY_F}
                 LEFT JOIN _info_interesados_agrupacion_interesados_restriccion ON _info_interesados_agrupacion_interesados_restriccion.{COL_RRR_PARTY_T_LC_GROUP_PARTY_F} = {LC_GROUP_PARTY_T}.{T_ID_F}
                 WHERE {LC_GROUP_PARTY_T}.{T_ID_F} IN (SELECT DISTINCT _restriccion_agrupacion_interesados.{COL_RRR_PARTY_T_LC_GROUP_PARTY_F} FROM _restriccion_agrupacion_interesados)
                 AND {LC_RESTRICTION_T}.{T_ID_F} IN (SELECT _restricciones_seleccionadas.{T_ID_F} FROM _restricciones_seleccionadas)
                 GROUP BY {LC_RESTRICTION_T}.{T_ID_F}
             ),
             _info_fuentes_administrativas_restriccion AS (
                SELECT {LC_RESTRICTION_T}.{T_ID_F},
                 JSON_AGG(
                    JSON_BUILD_OBJECT('id', {LC_ADMINISTRATIVE_SOURCE_T}.{T_ID_F},
                                      'attributes', JSON_BUILD_OBJECT('Tipo de fuente administrativa', (SELECT {DISPLAY_NAME_F} FROM {schema}.{COL_ADMINISTRATIVE_SOURCE_TYPE_D} WHERE {T_ID_F} = {LC_ADMINISTRATIVE_SOURCE_T}.{LC_ADMINISTRATIVE_SOURCE_T_TYPE_F}),
                                                                      'Ente emisor', {LC_ADMINISTRATIVE_SOURCE_T}.{LC_ADMINISTRATIVE_SOURCE_T_EMITTING_ENTITY_F},
                                                                      'Estado disponibilidad', (SELECT {DISPLAY_NAME_F} FROM {schema}.{COL_AVAILABILITY_TYPE_D} WHERE {T_ID_F} = {LC_ADMINISTRATIVE_SOURCE_T}.{COL_SOURCE_T_AVAILABILITY_STATUS_F}),
                                                                      'Archivo fuente', {EXT_ARCHIVE_S}.{EXT_ARCHIVE_S_DATA_F}))
                 ORDER BY {LC_ADMINISTRATIVE_SOURCE_T}.{T_ID_F}) FILTER (WHERE {LC_ADMINISTRATIVE_SOURCE_T}.{T_ID_F} IS NOT NULL) AS _fuenteadministrativa_
                FROM {schema}.{LC_RESTRICTION_T}
                LEFT JOIN {schema}.{COL_RRR_SOURCE_T} ON {LC_RESTRICTION_T}.{T_ID_F} ={COL_RRR_SOURCE_T}.{COL_RRR_SOURCE_T_LC_RESTRICTION_F}
                LEFT JOIN {schema}.{LC_ADMINISTRATIVE_SOURCE_T} ON {COL_RRR_SOURCE_T}.{COL_RRR_SOURCE_T_SOURCE_F} = {LC_ADMINISTRATIVE_SOURCE_T}.{T_ID_F}
                LEFT JOIN {schema}.{EXT_ARCHIVE_S} ON {EXT_ARCHIVE_S}.{EXT_ARCHIVE_S_LC_ADMINISTRATIVE_SOURCE_F} = {LC_ADMINISTRATIVE_SOURCE_T}.{T_ID_F}
                WHERE {LC_RESTRICTION_T}.{T_ID_F} IN (SELECT _restricciones_seleccionadas.{T_ID_F} FROM _restricciones_seleccionadas)
                GROUP BY {LC_RESTRICTION_T}.{T_ID_F}
             ),
            _info_restriccion AS (
              SELECT {LC_RESTRICTION_T}.{COL_BAUNIT_RRR_T_UNIT_F},
                JSON_AGG(
                    JSON_BUILD_OBJECT('id', {LC_RESTRICTION_T}.{T_ID_F},
                                      'attributes', JSON_BUILD_OBJECT('Tipo de restricción', (SELECT {DISPLAY_NAME_F} FROM {schema}.{LC_RESTRICTION_TYPE_D} WHERE {T_ID_F} = {LC_RESTRICTION_T}.{LC_RESTRICTION_T_TYPE_F}),
                                                                      'Descripción', {LC_RESTRICTION_T}.{COL_RRR_T_DESCRIPTION_F},
                                                                      '{LC_ADMINISTRATIVE_SOURCE_T}', COALESCE(_info_fuentes_administrativas_restriccion._fuenteadministrativa_, '[]'),
                                                                      '{LC_PARTY_T}', COALESCE(_info_interesados_restriccion._interesado_, '[]'),
                                                                      '{LC_GROUP_PARTY_T}', COALESCE(_info_agrupacion_interesados_restriccion._agrupacioninteresados_, '[]')))
                 ORDER BY {LC_RESTRICTION_T}.{T_ID_F}) FILTER (WHERE {LC_RESTRICTION_T}.{T_ID_F} IS NOT NULL) AS _restriccion_
              FROM {schema}.{LC_RESTRICTION_T} LEFT JOIN _info_fuentes_administrativas_restriccion ON {LC_RESTRICTION_T}.{T_ID_F} = _info_fuentes_administrativas_restriccion.{T_ID_F}
              LEFT JOIN _info_interesados_restriccion ON {LC_RESTRICTION_T}.{T_ID_F} = _info_interesados_restriccion.{T_ID_F}
              LEFT JOIN _info_agrupacion_interesados_restriccion ON {LC_RESTRICTION_T}.{T_ID_F} = _info_agrupacion_interesados_restriccion.{T_ID_F}
              WHERE {LC_RESTRICTION_T}.{T_ID_F} IN (SELECT * FROM _restricciones_seleccionadas)
              GROUP BY {LC_RESTRICTION_T}.{COL_BAUNIT_RRR_T_UNIT_F}
            ),
             _info_predio AS (
                 SELECT {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F},
                        JSON_AGG(JSON_BUILD_OBJECT('id', {LC_PARCEL_T}.{T_ID_F},
                                          'attributes', JSON_BUILD_OBJECT('Nombre', {LC_PARCEL_T}.{COL_BAUNIT_T_NAME_F},
                                                                          'NUPRE', {LC_PARCEL_T}.{LC_PARCEL_T_NUPRE_F},
                                                                          'Id operación', {LC_PARCEL_T}.{LC_PARCEL_T_ID_OPERATION_F},
                                                                          'FMI', ({LC_PARCEL_T}.{LC_PARCEL_T_ORIP_CODE_F} || '-'|| {LC_PARCEL_T}.{LC_PARCEL_T_FMI_F}),
                                                                          'Número predial', {LC_PARCEL_T}.{LC_PARCEL_T_PARCEL_NUMBER_F},
                                                                          'Número predial anterior', {LC_PARCEL_T}.{LC_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F},
                                                                          '{LC_RIGHT_T}', COALESCE(_info_derecho._derecho_, '[]'),
                                                                          '{LC_RESTRICTION_T}', COALESCE(_info_restriccion._restriccion_, '[]')
                                                                         )) ORDER BY {LC_PARCEL_T}.{T_ID_F}) FILTER(WHERE {LC_PARCEL_T}.{T_ID_F} IS NOT NULL) AS _predio_
                 FROM {schema}.{LC_PARCEL_T} LEFT JOIN {schema}.{COL_UE_BAUNIT_T} ON {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_PARCEL_F} = {LC_PARCEL_T}.{T_ID_F}
                 LEFT JOIN _info_derecho ON _info_derecho.{COL_BAUNIT_RRR_T_UNIT_F} = {LC_PARCEL_T}.{T_ID_F}
                 LEFT JOIN _info_restriccion ON _info_restriccion.{COL_BAUNIT_RRR_T_UNIT_F} = {LC_PARCEL_T}.{T_ID_F}
                 WHERE {LC_PARCEL_T}.{T_ID_F} IN (SELECT * FROM _predios_seleccionados)
                    AND {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F} IS NOT NULL
                    AND {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_BUILDING_F} IS NULL
                    AND {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_BUILDING_UNIT_F} IS NULL
                 GROUP BY {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F}
             ),
             _info_terreno AS (
                 SELECT {LC_PLOT_T}.{T_ID_F},
                 JSON_BUILD_OBJECT('id', {LC_PLOT_T}.{T_ID_F},
                                    'attributes', JSON_BUILD_OBJECT(CONCAT('Área' , (SELECT * FROM _unidad_area_terreno)), {LC_PLOT_T}.{LC_PLOT_T_PLOT_AREA_F},
                                                                    '{LC_PARCEL_T}', COALESCE(_info_predio._predio_, '[]')
                                                                   )) AS _terreno_
                 FROM {schema}.{LC_PLOT_T} LEFT JOIN _info_predio ON {LC_PLOT_T}.{T_ID_F} = _info_predio.{COL_UE_BAUNIT_T_LC_PLOT_F}
                 WHERE {LC_PLOT_T}.{T_ID_F} IN (SELECT * FROM _terrenos_seleccionados)
                 ORDER BY {LC_PLOT_T}.{T_ID_F}
             )
            SELECT JSON_BUILD_OBJECT('{LC_PLOT_T}', COALESCE(JSON_AGG(_info_terreno._terreno_), '[]')) FROM _info_terreno
    """

    query = query.format(**vars(names),  # Custom keys are searched in Table And Field Names object
                         schema= schema,
                         custom_filter_plots=custom_filter_plots,
                         custom_filter_parcels=custom_filter_parcels,
                         parcel_fmi=parcel_fmi,
                         parcel_number=parcel_number,
                         LC_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V=LADMNames.LC_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V,
                         previous_parcel_number=previous_parcel_number)
    return query
