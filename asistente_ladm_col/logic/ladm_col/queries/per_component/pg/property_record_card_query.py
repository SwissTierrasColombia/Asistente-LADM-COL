def get_igac_property_record_card_query(schema, plot_t_id, parcel_fmi, parcel_number, previous_parcel_number, cadastral_form_model):
    query = """
                WITH
                 unidad_area_terreno AS (
                     SELECT ' [' || setting || ']' FROM {schema}.t_ili2db_column_prop WHERE tablename = 'op_terreno' AND columnname = 'area_terreno' LIMIT 1
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
    """

    if cadastral_form_model:
        query += """
                 predio_formulario_unico AS (
                     SELECT fcm_formulario_unico_cm.t_id FROM {schema}.fcm_formulario_unico_cm WHERE fcm_formulario_unico_cm.op_predio IN (SELECT * FROM predios_seleccionados)
                 ),
                 fcm_contacto_visita AS (
                    SELECT fcm_contacto_visita.fcm_formulario,
                        json_agg(
                                json_build_object('id', fcm_contacto_visita.t_id,
                                                       'attributes', json_build_object('Nombre de quien atendió', fcm_contacto_visita.nombre_quien_atendio,
                                                                                       'Relación con el predio', fcm_contacto_visita.relacion_con_predio,
                                                                                       'Domicilio de notificación', fcm_contacto_visita.domicilio_notificaciones,
                                                                                       'Celular', fcm_contacto_visita.celular,
                                                                                       'Correo electrónico', fcm_contacto_visita.correo_electronico,
                                                                                       'Autoriza notificaciones', fcm_contacto_visita.autoriza_notificaciones))
                        ORDER BY fcm_contacto_visita.t_id) FILTER(WHERE fcm_contacto_visita.t_id IS NOT NULL) AS fcm_contacto_visita
                    FROM {schema}.fcm_contacto_visita WHERE fcm_contacto_visita.fcm_formulario IN (SELECT * FROM predio_formulario_unico)
                    GROUP BY fcm_contacto_visita.fcm_formulario
                 ),
        """

    query += """
                 info_predio AS (
                     SELECT col_uebaunit.ue_op_terreno,
                            json_agg(json_build_object('id', op_predio.t_id,
                                              'attributes', json_build_object('Nombre', op_predio.nombre
                                                                              , 'Departamento', op_predio.departamento
                                                                              , 'Municipio', op_predio.municipio
                                                                              , 'NUPRE', op_predio.nupre
                                                                              , 'FMI', (op_predio.codigo_orip || '-'|| op_predio.matricula_inmobiliaria)
                                                                              , 'Número predial', op_predio.numero_predial
                                                                              , 'Número predial anterior', op_predio.numero_predial_anterior
                                                                              , 'Tipo', (SELECT dispname FROM {schema}.op_prediotipo WHERE t_id = op_predio.tipo)
    """

    if cadastral_form_model:
        query += """
                    															  , 'Corregimiento', fcm_formulario_unico_cm.corregimiento
                    															  , 'Localidad/Comuna', fcm_formulario_unico_cm.localidad_comuna
                    															  , 'Barrio/Vereda', fcm_formulario_unico_cm.barrio_vereda
                    															  , 'Formalidad', (SELECT dispname FROM {schema}.fcm_formalidadtipo WHERE t_id = fcm_formulario_unico_cm.formalidad)
                    															  , 'Destinación económica', (SELECT dispname FROM {schema}.fcm_destinacioneconomicatipo WHERE t_id = fcm_formulario_unico_cm.destinacion_economica)
                    															  , 'Clase suelo', (SELECT dispname FROM {schema}.fcm_clasesuelotipo WHERE t_id = fcm_formulario_unico_cm.clase_suelo)
                    															  , 'Categoría suelo', (SELECT dispname FROM {schema}.fcm_categoriasuelotipo WHERE t_id = fcm_formulario_unico_cm.categoria_suelo)
                    															  , 'Tiene FMI', fcm_formulario_unico_cm.tiene_fmi
                    															  , 'Fecha de inicio de tenencia', fcm_formulario_unico_cm.fecha_inicio_tenencia
                    															  , 'Número predial del predio matriz', fcm_formulario_unico_cm.numero_predial_predio_matriz
                    															  , 'Observaciones', fcm_formulario_unico_cm.observaciones
                    															  , 'Fecha de visita predial', fcm_formulario_unico_cm.fecha_visita_predial
                    															  , 'Nombre del reconocedor', fcm_formulario_unico_cm.nombre_reconocedor
                    															  , 'Contacto de visita', COALESCE(fcm_contacto_visita.fcm_contacto_visita, '[]')
        """
    else:
        query += """
                    															  , 'Corregimiento', NULL
                    															  , 'Localidad/Comuna', NULL
                    															  , 'Barrio/Vereda', NULL
                    															  , 'Formalidad', NULL
                    															  , 'Destinación económica', NULL
                    															  , 'Clase suelo', NULL
                    															  , 'Categoría suelo', NULL
                    															  , 'Tiene FMI', NULL
                    															  , 'Fecha de inicio de tenencia', NULL
                    															  , 'Número predial del predio matriz', NULL
                    															  , 'Observaciones', NULL
                    															  , 'Fecha de visita predial', NULL
                    															  , 'Nombre del reconocedor', NULL
                    															  , 'Contacto de visita', NULL
        """

    query += """
                                                                             )) ORDER BY op_predio.t_id) FILTER(WHERE op_predio.t_id IS NOT NULL) as op_predio
                     FROM {schema}.op_predio LEFT JOIN {schema}.col_uebaunit ON col_uebaunit.baunit = op_predio.t_id
    """

    if cadastral_form_model:
        query += """
                    	 LEFT JOIN {schema}.fcm_formulario_unico_cm ON op_predio.t_id = fcm_formulario_unico_cm.op_predio
                    	 LEFT JOIN fcm_contacto_visita ON fcm_contacto_visita.fcm_formulario = fcm_formulario_unico_cm.t_id
        """

    query += """
                     WHERE op_predio.t_id IN (SELECT * FROM predios_seleccionados)
                     AND col_uebaunit.ue_op_terreno IS NOT NULL
                     AND col_uebaunit.ue_op_construccion IS NULL
                     AND col_uebaunit.ue_op_unidadconstruccion IS NULL
                     GROUP BY col_uebaunit.ue_op_terreno
                 ),
                 info_terreno AS (
                    SELECT op_terreno.t_id,
                      json_build_object('id', op_terreno.t_id,
                                        'attributes', json_build_object(CONCAT('Área de op_terreno' , (SELECT * FROM unidad_area_terreno)), op_terreno.area_terreno,
                                                                        'op_predio', COALESCE(info_predio.op_predio, '[]')
                                                                       )) as op_terreno
                    FROM {schema}.op_terreno LEFT JOIN info_predio ON info_predio.ue_op_terreno = op_terreno.t_id
                    WHERE op_terreno.t_id IN (SELECT * FROM terrenos_seleccionados)
                    ORDER BY op_terreno.t_id
                 )
                 SELECT json_agg(info_terreno.op_terreno) AS op_terreno FROM info_terreno
    """

    query = query.format(schema=schema, plot_t_id=plot_t_id, parcel_fmi=parcel_fmi, parcel_number=parcel_number,
                         previous_parcel_number=previous_parcel_number)

    return query
