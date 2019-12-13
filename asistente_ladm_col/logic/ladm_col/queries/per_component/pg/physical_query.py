def get_igac_physical_query(schema, plot_t_id, parcel_fmi, parcel_number, previous_parcel_number, valuation_model):

    query = """
            WITH
             unidad_area_terreno AS (
                 SELECT ' [' || setting || ']' FROM {schema}.t_ili2db_column_prop WHERE tablename = 'op_terreno' AND columnname = 'area_terreno' LIMIT 1
             ),
             unidad_area_construida_uc AS (
                 SELECT ' [' || setting || ']' FROM {schema}.t_ili2db_column_prop WHERE tablename = 'op_unidadconstruccion' AND columnname = 'area_construida' LIMIT 1
             ),
             unidad_area_privada_construida_uc AS (
                 SELECT ' [' || setting || ']' FROM {schema}.t_ili2db_column_prop WHERE tablename = 'op_unidadconstruccion' AND columnname = 'area_privada_construida' LIMIT 1
             ),
             unidad_longitud_lindero AS (
                 SELECT ' [' || setting || ']' FROM {schema}.t_ili2db_column_prop WHERE tablename = 'op_lindero' AND columnname = 'longitud' LIMIT 1
             ),
             terrenos_seleccionados AS (
                SELECT {plot_t_id} AS ue_op_terreno WHERE '{plot_t_id}' <> 'NULL'
                    UNION
                SELECT col_uebaunit.ue_op_terreno FROM {schema}.op_predio LEFT JOIN {schema}.col_uebaunit ON op_predio.t_id = col_uebaunit.baunit  WHERE col_uebaunit.ue_op_terreno IS NOT NULL AND CASE WHEN '{parcel_fmi}' = 'NULL' THEN  1 = 2 ELSE (op_predio.codigo_orip || '-'|| op_predio.matricula_inmobiliaria) = '{parcel_fmi}' END
                    UNION
                SELECT col_uebaunit.ue_op_terreno FROM {schema}.op_predio LEFT JOIN {schema}.col_uebaunit ON op_predio.t_id = col_uebaunit.baunit  WHERE col_uebaunit.ue_op_terreno IS NOT NULL AND CASE WHEN '{parcel_number}' = 'NULL' THEN  1 = 2 ELSE op_predio.numero_predial = '{parcel_number}' END
                    UNION
                SELECT col_uebaunit.ue_op_terreno FROM {schema}.op_predio LEFT JOIN {schema}.col_uebaunit ON op_predio.t_id = col_uebaunit.baunit  WHERE col_uebaunit.ue_op_terreno IS NOT NULL AND CASE WHEN '{previous_parcel_number}' = 'NULL' THEN  1 = 2 ELSE op_predio.numero_predial_anterior = '{previous_parcel_number}' END
             ),
             predios_seleccionados AS (
                SELECT col_uebaunit.baunit as t_id FROM {schema}.col_uebaunit WHERE col_uebaunit.ue_op_terreno = {plot_t_id} AND '{plot_t_id}' <> 'NULL'
                    UNION
                SELECT t_id FROM {schema}.op_predio WHERE CASE WHEN '{parcel_fmi}' = 'NULL' THEN  1 = 2 ELSE (op_predio.codigo_orip || '-'|| op_predio.matricula_inmobiliaria) = '{parcel_fmi}' END
                    UNION
                SELECT t_id FROM {schema}.op_predio WHERE CASE WHEN '{parcel_number}' = 'NULL' THEN  1 = 2 ELSE op_predio.numero_predial = '{parcel_number}' END
                    UNION
                SELECT t_id FROM {schema}.op_predio WHERE CASE WHEN '{previous_parcel_number}' = 'NULL' THEN  1 = 2 ELSE op_predio.numero_predial_anterior = '{previous_parcel_number}' END
             ),
             construcciones_seleccionadas AS (
                 SELECT ue_op_construccion FROM {schema}.col_uebaunit WHERE col_uebaunit.baunit IN (SELECT predios_seleccionados.t_id FROM predios_seleccionados WHERE predios_seleccionados.t_id IS NOT NULL) AND ue_op_construccion IS NOT NULL
             ),
             unidadesconstruccion_seleccionadas AS (
                 SELECT op_unidadconstruccion.t_id FROM {schema}.op_unidadconstruccion WHERE op_unidadconstruccion.op_construccion IN (SELECT ue_op_construccion FROM construcciones_seleccionadas)
             ),
            punto_lindero_externos_seleccionados AS (
                 SELECT DISTINCT col_masccl.ue_mas_op_terreno, op_puntolindero.t_id
                 FROM {schema}.op_puntolindero LEFT JOIN {schema}.col_puntoccl ON op_puntolindero.t_id = col_puntoccl.punto_op_puntolindero
                 LEFT JOIN {schema}.op_lindero ON col_puntoccl.ccl = op_lindero.t_id
                 LEFT JOIN {schema}.col_masccl ON op_lindero.t_id = col_masccl.ccl_mas
                 WHERE col_masccl.ue_mas_op_terreno IN (SELECT * FROM terrenos_seleccionados)
                 ORDER BY col_masccl.ue_mas_op_terreno, op_puntolindero.t_id
            ),
            punto_lindero_internos_seleccionados AS (
                SELECT DISTINCT col_menosccl.ue_menos_op_terreno, op_puntolindero.t_id
                FROM {schema}.op_puntolindero LEFT JOIN {schema}.col_puntoccl ON op_puntolindero.t_id = col_puntoccl.punto_op_puntolindero
                LEFT JOIN {schema}.op_lindero ON col_puntoccl.ccl = op_lindero.t_id
                LEFT JOIN {schema}.col_menosccl ON op_lindero.t_id = col_menosccl.ccl_menos
                WHERE col_menosccl.ue_menos_op_terreno IN (SELECT * FROM terrenos_seleccionados)
              ORDER BY col_menosccl.ue_menos_op_terreno, op_puntolindero.t_id
            ),
             uc_fuente_espacial AS (
                SELECT col_uefuente.ue_op_unidadconstruccion,
                    json_agg(
                            json_build_object('id', op_fuenteespacial.t_id,
                                                   'attributes', json_build_object('Tipo de fuente espacial', (SELECT dispname FROM {schema}.col_fuenteespacialtipo WHERE t_id = op_fuenteespacial.tipo),
                                                                                   'Estado disponibilidad', (SELECT dispname FROM {schema}.col_estadodisponibilidadtipo WHERE t_id = op_fuenteespacial.estado_disponibilidad),
                                                                                   'Tipo principal', (SELECT dispname FROM {schema}.ci_forma_presentacion_codigo WHERE t_id = op_fuenteespacial.tipo_principal),
                                                                                   'Fecha documento', op_fuenteespacial.fecha_documento_fuente,
                                                                                   'Archivo fuente', extarchivo.datos))
                    ORDER BY op_fuenteespacial.t_id) FILTER(WHERE col_uefuente.fuente_espacial IS NOT NULL) AS op_fuenteespacial
                FROM {schema}.col_uefuente LEFT JOIN {schema}.op_fuenteespacial ON col_uefuente.fuente_espacial = op_fuenteespacial.t_id
                LEFT JOIN {schema}.extarchivo ON extarchivo.op_fuenteespacial_ext_archivo_id = op_fuenteespacial.t_id
                WHERE col_uefuente.ue_op_unidadconstruccion IN (SELECT * FROM unidadesconstruccion_seleccionadas)
                GROUP BY col_uefuente.ue_op_unidadconstruccion
             ),
            info_uc AS (
                 SELECT op_unidadconstruccion.op_construccion,
                        json_agg(json_build_object('id', op_unidadconstruccion.t_id,
                                          'attributes', json_build_object('Número de pisos', op_unidadconstruccion.total_pisos,
                                                                          'Uso', (SELECT dispname FROM {schema}.op_usouconstipo WHERE t_id = op_unidadconstruccion.uso),
                                                                          'Tipo construcción', (select dispname from {schema}.OP_ConstruccionTipo where t_id = op_unidadconstruccion.tipo_construccion),
                                                                          'Tipo unidad de construcción', (select dispname from {schema}.OP_UnidadConstruccionTipo where t_id = op_unidadconstruccion.tipo_unidad_construccion),
                                                                          CONCAT('Área privada construida' , (SELECT * FROM unidad_area_privada_construida_uc)), op_unidadconstruccion.area_privada_construida,
                                                                          CONCAT('Área construida' , (SELECT * FROM unidad_area_construida_uc)), op_unidadconstruccion.area_construida,
                                                                          'op_fuenteespacial', COALESCE(uc_fuente_espacial.op_fuenteespacial, '[]')
                                                                         )) ORDER BY op_unidadconstruccion.t_id) FILTER(WHERE op_unidadconstruccion.t_id IS NOT NULL) AS op_unidadconstruccion
                 FROM {schema}.op_unidadconstruccion LEFT JOIN uc_fuente_espacial ON op_unidadconstruccion.t_id = uc_fuente_espacial.ue_op_unidadconstruccion
                 WHERE op_unidadconstruccion.t_id IN (SELECT * FROM unidadesconstruccion_seleccionadas)
                 GROUP BY op_unidadconstruccion.op_construccion
             ),
             c_fuente_espacial AS (
                SELECT col_uefuente.ue_op_construccion,
                    json_agg(
                            json_build_object('id', op_fuenteespacial.t_id,
                                                   'attributes', json_build_object('Tipo de fuente espacial', (SELECT dispname FROM {schema}.col_fuenteespacialtipo WHERE t_id = op_fuenteespacial.tipo),
                                                                                   'Estado disponibilidad', (SELECT dispname FROM {schema}.col_estadodisponibilidadtipo WHERE t_id = op_fuenteespacial.estado_disponibilidad),
                                                                                   'Tipo principal', (SELECT dispname FROM {schema}.ci_forma_presentacion_codigo WHERE t_id = op_fuenteespacial.tipo_principal),
                                                                                   'Fecha documento', op_fuenteespacial.fecha_documento_fuente,
                                                                                   'Archivo fuente', extarchivo.datos))
                    ORDER BY op_fuenteespacial.t_id) FILTER(WHERE col_uefuente.fuente_espacial IS NOT NULL) AS op_fuenteespacial
                FROM {schema}.col_uefuente LEFT JOIN {schema}.op_fuenteespacial ON col_uefuente.fuente_espacial = op_fuenteespacial.t_id
                LEFT JOIN {schema}.extarchivo ON extarchivo.op_fuenteespacial_ext_archivo_id = op_fuenteespacial.t_id
                WHERE col_uefuente.ue_op_construccion IN (SELECT * FROM construcciones_seleccionadas)
                GROUP BY col_uefuente.ue_op_construccion
             ),
             info_construccion as (
              SELECT col_uebaunit.baunit,
                    json_agg(json_build_object('id', op_construccion.t_id,
                                      'attributes', json_build_object('Área construcción', op_construccion.area_construccion,
                                                                      'Ńúmero de pisos', op_construccion.numero_pisos,
                                                                      'op_fuenteespacial', COALESCE(c_fuente_espacial.op_fuenteespacial, '[]'),
                                                                      'op_unidadconstruccion', COALESCE(info_uc.op_unidadconstruccion, '[]')
                                                                     )) ORDER BY op_construccion.t_id) FILTER(WHERE op_construccion.t_id IS NOT NULL) as op_construccion
              FROM {schema}.op_construccion LEFT JOIN c_fuente_espacial ON op_construccion.t_id = c_fuente_espacial.ue_op_construccion
              LEFT JOIN info_uc ON op_construccion.t_id = info_uc.op_construccion
              LEFT JOIN {schema}.col_uebaunit ON col_uebaunit.ue_op_construccion = op_construccion.t_id
              WHERE op_construccion.t_id IN (SELECT * FROM construcciones_seleccionadas)
              GROUP BY col_uebaunit.baunit
             ),
             info_predio AS (
                 SELECT col_uebaunit.ue_op_terreno,
                        json_agg(json_build_object('id', op_predio.t_id,
                                          'attributes', json_build_object('Nombre', op_predio.nombre,
                                                                          'NUPRE', op_predio.nupre,
                                                                          'FMI', (op_predio.codigo_orip || '-'|| op_predio.matricula_inmobiliaria),
                                                                          'Número predial', op_predio.numero_predial,
                                                                          'Número predial anterior', op_predio.numero_predial_anterior,
                                                                          'op_construccion', COALESCE(info_construccion.op_construccion, '[]')
                                                                         )) ORDER BY op_predio.t_id) FILTER(WHERE op_predio.t_id IS NOT NULL) as op_predio
                 FROM {schema}.op_predio LEFT JOIN info_construccion ON op_predio.t_id = info_construccion.baunit
                 LEFT JOIN {schema}.col_uebaunit ON col_uebaunit.baunit = info_construccion.baunit
                 WHERE op_predio.t_id = info_construccion.baunit
                 AND col_uebaunit.ue_op_terreno IS NOT NULL
                 AND col_uebaunit.ue_op_construccion IS NULL
                 AND col_uebaunit.ue_op_unidadconstruccion IS NULL
                 GROUP BY col_uebaunit.ue_op_terreno
             ),
             t_fuente_espacial AS (
                SELECT col_uefuente.ue_op_terreno,
                    json_agg(
                            json_build_object('id', op_fuenteespacial.t_id,
                                                   'attributes', json_build_object('Tipo de fuente espacial', (SELECT dispname FROM {schema}.col_fuenteespacialtipo WHERE t_id = op_fuenteespacial.tipo),
                                                                                   'Estado disponibilidad', (SELECT dispname FROM {schema}.col_estadodisponibilidadtipo WHERE t_id = op_fuenteespacial.estado_disponibilidad),
                                                                                   'Tipo principal', (SELECT dispname FROM {schema}.ci_forma_presentacion_codigo WHERE t_id = op_fuenteespacial.tipo_principal),
                                                                                   'Fecha documento', op_fuenteespacial.fecha_documento_fuente,
                                                                                   'Archivo fuente', extarchivo.datos))
                    ORDER BY op_fuenteespacial.t_id) FILTER(WHERE col_uefuente.fuente_espacial IS NOT NULL) AS op_fuenteespacial
                FROM {schema}.col_uefuente LEFT JOIN {schema}.op_fuenteespacial ON col_uefuente.fuente_espacial = op_fuenteespacial.t_id
                LEFT JOIN {schema}.extarchivo ON extarchivo.op_fuenteespacial_ext_archivo_id = op_fuenteespacial.t_id
                WHERE col_uefuente.ue_op_terreno IN (SELECT * FROM terrenos_seleccionados)
                GROUP BY col_uefuente.ue_op_terreno
             ),
             info_linderos_externos AS (
                SELECT col_masccl.ue_mas_op_terreno,
                    json_agg(
                            json_build_object('id', op_lindero.t_id,
                                                   'attributes', json_build_object(CONCAT('Longitud' , (SELECT * FROM unidad_longitud_lindero)), op_lindero.longitud))
                    ORDER BY op_lindero.t_id) FILTER(WHERE op_lindero.t_id IS NOT NULL) AS op_lindero
                FROM {schema}.op_lindero LEFT JOIN {schema}.col_masccl ON op_lindero.t_id = col_masccl.ccl_mas
                WHERE col_masccl.ue_mas_op_terreno IN (SELECT * FROM terrenos_seleccionados)
                GROUP BY col_masccl.ue_mas_op_terreno
             ),
             info_linderos_internos AS (
                SELECT col_menosccl.ue_menos_op_terreno,
                    json_agg(
                            json_build_object('id', op_lindero.t_id,
                                                   'attributes', json_build_object(CONCAT('Longitud' , (SELECT * FROM unidad_longitud_lindero)), op_lindero.longitud))
                    ORDER BY op_lindero.t_id) FILTER(WHERE op_lindero.t_id IS NOT NULL) AS op_lindero
                FROM {schema}.op_lindero LEFT JOIN {schema}.col_menosccl ON op_lindero.t_id = col_menosccl.ccl_menos
                WHERE col_menosccl.ue_menos_op_terreno IN (SELECT * FROM terrenos_seleccionados)
                GROUP BY col_menosccl.ue_menos_op_terreno
             ),
            info_punto_lindero_externos AS (
                SELECT punto_lindero_externos_seleccionados.ue_mas_op_terreno,
                        json_agg(
                            json_build_object('id', op_puntolindero.t_id,
                                                   'attributes', json_build_object('Nombre', op_puntolindero.id_punto_lindero,
                                                                                   'coordenadas', concat(st_x(op_puntolindero.geometria),
                                                                                                 ' ', st_y(op_puntolindero.geometria),
                                                                                                 CASE WHEN st_z(op_puntolindero.geometria) IS NOT NULL THEN concat(' ', st_z(op_puntolindero.geometria)) END))
                        ) ORDER BY op_puntolindero.t_id) FILTER(WHERE op_puntolindero.t_id IS NOT NULL) AS op_puntolindero
                FROM {schema}.op_puntolindero LEFT JOIN punto_lindero_externos_seleccionados ON op_puntolindero.t_id = punto_lindero_externos_seleccionados.t_id
                WHERE punto_lindero_externos_seleccionados.ue_mas_op_terreno IS NOT NULL
                GROUP BY punto_lindero_externos_seleccionados.ue_mas_op_terreno
             ),
             info_punto_lindero_internos AS (
                 SELECT punto_lindero_internos_seleccionados.ue_menos_op_terreno,
                        json_agg(
                            json_build_object('id', op_puntolindero.t_id,
                                                   'attributes', json_build_object('Nombre', op_puntolindero.id_punto_lindero,
                                                                                   'coordenadas', concat(st_x(op_puntolindero.geometria),
                                                                                                 ' ', st_y(op_puntolindero.geometria),
                                                                                                 CASE WHEN st_z(op_puntolindero.geometria) IS NOT NULL THEN concat(' ', st_z(op_puntolindero.geometria)) END))
                        ) ORDER BY op_puntolindero.t_id) FILTER(WHERE op_puntolindero.t_id IS NOT NULL) AS op_puntolindero
                 FROM {schema}.op_puntolindero LEFT JOIN punto_lindero_internos_seleccionados ON op_puntolindero.t_id = punto_lindero_internos_seleccionados.t_id
                 WHERE punto_lindero_internos_seleccionados.ue_menos_op_terreno IS NOT NULL
                 GROUP BY punto_lindero_internos_seleccionados.ue_menos_op_terreno
             ),
            info_puntolevantamiento AS (
                SELECT col_uebaunit.ue_op_terreno,
                        json_agg(
                                json_build_object('id', puntoslevantamiento_seleccionados.t_id_puntolevantamiento,
                                                       'attributes', json_build_object('coordenadas', concat(st_x(puntoslevantamiento_seleccionados.geometria),
                                                                                                 ' ', st_y(puntoslevantamiento_seleccionados.geometria),
                                                                                                 CASE WHEN st_z(puntoslevantamiento_seleccionados.geometria) IS NOT NULL THEN concat(' ', st_z(puntoslevantamiento_seleccionados.geometria)) END)
                                                                                      ))
                        ORDER BY puntoslevantamiento_seleccionados.t_id_puntolevantamiento) FILTER(WHERE puntoslevantamiento_seleccionados.t_id_puntolevantamiento IS NOT NULL) AS op_puntolevantamiento
                FROM
                (
                    SELECT op_puntolevantamiento.t_id AS t_id_puntolevantamiento, op_puntolevantamiento.geometria, op_construccion.t_id AS t_id_construccion  FROM {schema}.op_construccion, {schema}.op_puntolevantamiento
                    WHERE ST_Intersects(op_construccion.geometria, op_puntolevantamiento.geometria) = True AND op_construccion.t_id IN (SELECT * from construcciones_seleccionadas)
                ) AS puntoslevantamiento_seleccionados
                LEFT JOIN {schema}.col_uebaunit AS uebaunit_construccion  ON uebaunit_construccion.ue_op_construccion = puntoslevantamiento_seleccionados.t_id_construccion
                LEFT JOIN {schema}.col_uebaunit AS col_uebaunit ON col_uebaunit.baunit = uebaunit_construccion.baunit
                WHERE col_uebaunit.ue_op_terreno IS NOT NULL AND
                      col_uebaunit.ue_op_construccion IS NULL AND
                      col_uebaunit.ue_op_unidadconstruccion IS NULL
                GROUP BY col_uebaunit.ue_op_terreno
            ),
             info_terreno AS (
                SELECT op_terreno.t_id,
                  json_build_object('id', op_terreno.t_id,
                                    'attributes', json_build_object(CONCAT('Área calculada' , (SELECT * FROM unidad_area_terreno)), op_terreno.area_terreno,
                                                                    'op_predio', COALESCE(info_predio.op_predio, '[]'),
                                                                    'Linderos externos', json_build_object('op_lindero', COALESCE(info_linderos_externos.op_lindero, '[]'),
                                                                                                           'op_puntolindero', COALESCE(info_punto_lindero_externos.op_puntolindero, '[]')),
                                                                    'Linderos internos', json_build_object('op_lindero', COALESCE(info_linderos_internos.op_lindero, '[]'),
                                                                                                           'op_puntolindero', COALESCE(info_punto_lindero_internos.op_puntolindero, '[]')),
                                                                    'op_puntolevantamiento', COALESCE(info_puntolevantamiento.op_puntolevantamiento, '[]'),
                                                                    'op_fuenteespacial', COALESCE(t_fuente_espacial.op_fuenteespacial, '[]')
                                                                   )) as op_terreno
                FROM {schema}.op_terreno LEFT JOIN info_predio ON info_predio.ue_op_terreno = op_terreno.t_id
                LEFT JOIN t_fuente_espacial ON op_terreno.t_id = t_fuente_espacial.ue_op_terreno
                LEFT JOIN info_linderos_externos ON op_terreno.t_id = info_linderos_externos.ue_mas_op_terreno
                LEFT JOIN info_linderos_internos ON op_terreno.t_id = info_linderos_internos.ue_menos_op_terreno
                LEFT JOIN info_punto_lindero_externos ON op_terreno.t_id = info_punto_lindero_externos.ue_mas_op_terreno
                LEFT JOIN info_punto_lindero_internos ON op_terreno.t_id = info_punto_lindero_internos.ue_menos_op_terreno
                LEFT JOIN info_puntolevantamiento ON op_terreno.t_id = info_puntolevantamiento.ue_op_terreno
                WHERE op_terreno.t_id IN (SELECT * FROM terrenos_seleccionados)
              ORDER BY op_terreno.t_id
             )
             SELECT json_agg(info_terreno.op_terreno) AS op_terreno FROM info_terreno
    """

    query = query.format(schema= schema, plot_t_id=plot_t_id, parcel_fmi=parcel_fmi, parcel_number=parcel_number, previous_parcel_number=previous_parcel_number)

    return query
