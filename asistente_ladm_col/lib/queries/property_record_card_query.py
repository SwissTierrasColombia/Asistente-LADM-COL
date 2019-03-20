def get_igac_property_record_card_query(schema, plot_t_id, parcel_fmi, parcel_number, previous_parcel_number, property_record_card_model):

    query = """
    WITH
     unidad_area_calculada_terreno AS (
         SELECT ' [' || setting || ']' FROM {schema}.t_ili2db_column_prop WHERE tablename = 'terreno' AND columnname = 'area_calculada' LIMIT 1
     ),
     terrenos_seleccionados AS (
        SELECT {plot_t_id} AS ue_terreno WHERE '{plot_t_id}' <> 'NULL'
            UNION
        SELECT uebaunit.ue_terreno FROM {schema}.predio LEFT JOIN {schema}.uebaunit ON predio.t_id = uebaunit.baunit_predio  WHERE uebaunit.ue_terreno IS NOT NULL AND CASE WHEN '{parcel_fmi}' = 'NULL' THEN  1 = 2 ELSE predio.fmi = '{parcel_fmi}' END
            UNION
        SELECT uebaunit.ue_terreno FROM {schema}.predio LEFT JOIN {schema}.uebaunit ON predio.t_id = uebaunit.baunit_predio  WHERE uebaunit.ue_terreno IS NOT NULL AND CASE WHEN '{parcel_number}' = 'NULL' THEN  1 = 2 ELSE predio.numero_predial = '{parcel_number}' END
            UNION
        SELECT uebaunit.ue_terreno FROM {schema}.predio LEFT JOIN {schema}.uebaunit ON predio.t_id = uebaunit.baunit_predio  WHERE uebaunit.ue_terreno IS NOT NULL AND CASE WHEN '{previous_parcel_number}' = 'NULL' THEN  1 = 2 ELSE predio.numero_predial_anterior = '{previous_parcel_number}' END
     ),
     predios_seleccionados AS (
        SELECT uebaunit.baunit_predio as t_id FROM {schema}.uebaunit WHERE uebaunit.ue_terreno = {plot_t_id} AND '{plot_t_id}' <> 'NULL'
            UNION
        SELECT t_id FROM {schema}.predio WHERE CASE WHEN '{parcel_fmi}' = 'NULL' THEN  1 = 2 ELSE predio.fmi = '{parcel_fmi}' END
            UNION
        SELECT t_id FROM {schema}.predio WHERE CASE WHEN '{parcel_number}' = 'NULL' THEN  1 = 2 ELSE predio.numero_predial = '{parcel_number}' END
            UNION
        SELECT t_id FROM {schema}.predio WHERE CASE WHEN '{previous_parcel_number}' = 'NULL' THEN  1 = 2 ELSE predio.numero_predial_anterior = '{previous_parcel_number}' END
     ),
    """

    if property_record_card_model:
        query += """
     predio_ficha_seleccionados AS (
         SELECT predio_ficha.t_id FROM {schema}.predio_ficha WHERE predio_ficha.crpredio IN (SELECT * FROM predios_seleccionados)
     ),
     fpredio_investigacion_mercado AS (
        SELECT investigacionmercado.fichapredio,
            json_agg(
                    json_build_object('id', investigacionmercado.t_id,
                                           'attributes', json_build_object('Disponible en el mercado', investigacionmercado.disponible_mercado,
                                                                           'Tipo de oferta', investigacionmercado.tipo_oferta,
                                                                           'Valor', investigacionmercado.valor,
                                                                           'Nombre oferente', investigacionmercado.nombre_oferente,
                                                                           'Teléfono contacto oferente', investigacionmercado.telefono_contacto_oferente,
                                                                           'Observaciones', investigacionmercado.observaciones))
            ) FILTER(WHERE investigacionmercado.t_id IS NOT NULL) AS investigacionmercado
        FROM {schema}.investigacionmercado WHERE investigacionmercado.fichapredio IN (SELECT * FROM predio_ficha_seleccionados)
        GROUP BY investigacionmercado.fichapredio
     ),
     fpredio_nucleo_familiar AS (
        SELECT nucleofamiliar.fichapredio,
            json_agg(
                    json_build_object('id', nucleofamiliar.t_id,
                                           'attributes', json_build_object('Documento de identidad', nucleofamiliar.documento_identidad,
                                                                           'Tipo de documento', nucleofamiliar.tipo_documento,
                                                                           'Organo emisor', nucleofamiliar.organo_emisor,
                                                                           'Fecha de emisión', nucleofamiliar.fecha_emision,
                                                                           'Primer nombre', nucleofamiliar.primer_nombre,
                                                                           'Segundo nombre', nucleofamiliar.segundo_nombre,
                                                                           'Primer apellido', nucleofamiliar.primer_apellido,
                                                                           'Segundo apellido', nucleofamiliar.segundo_apellido,
                                                                           'Fecha de nacimiento', nucleofamiliar.fecha_nacimiento,
                                                                           'Lugar de nacimiento', nucleofamiliar.lugar_nacimiento,
                                                                           'Nacionalidad', nucleofamiliar.nacionalidad,
                                                                           'Discapacidad', nucleofamiliar.discapacidad,
                                                                           'Género', nucleofamiliar.genero,
                                                                           'Habita predio', nucleofamiliar.habita_predio,
                                                                           'Parentesco', nucleofamiliar.parentesco,
                                                                           'Etnia', nucleofamiliar.etnia,
                                                                           'Dirección', nucleofamiliar.direccion,
                                                                           'Celular', nucleofamiliar.celular))
            ) FILTER(WHERE nucleofamiliar.t_id IS NOT NULL) AS nucleofamiliar
        FROM {schema}.nucleofamiliar WHERE nucleofamiliar.fichapredio IN (SELECT * FROM predio_ficha_seleccionados)
        GROUP BY nucleofamiliar.fichapredio
     ),
        """

    query += """
     info_predio AS (
         SELECT uebaunit.ue_terreno,
                json_agg(json_build_object('id', predio.t_id,
                                  'attributes', json_build_object('Nombre', predio.nombre
                                                                  , 'Departamento', predio.departamento
                                                                  , 'Municipio', predio.municipio
                                                                  , 'Zona', predio.zona
                                                                  , 'NUPRE', predio.nupre
                                                                  , 'FMI', predio.fmi
                                                                  , 'Número predial', predio.numero_predial
                                                                  , 'Número predial anterior', predio.numero_predial_anterior
                                                                  , 'Tipo', predio.tipo
    """

    if property_record_card_model:
        query += """
    --															  , 'Sector', predio_ficha.sector
                                                                  , 'Localidad/Comuna', predio_ficha.localidad_comuna
                                                                  , 'Barrio', predio_ficha.barrio
                                                                  , 'Manzana/Vereda', predio_ficha.manzana_vereda
                                                                  , 'Terreno', predio_ficha.terreno
                                                                  , 'Condición propiedad', predio_ficha.condicion_propiedad
                                                                  , 'Edificio', predio_ficha.edificio
                                                                  , 'Piso', predio_ficha.piso
                                                                  , 'Unidad', predio_ficha.unidad
                                                                  , 'Estado NUPRE', predio_ficha.estado_nupre
                                                                  , 'Destinación económica', predio_ficha.destinacion_economica
                                                                  , 'Tipo de predio', predio_ficha.predio_tipo
                                                                  , 'Tipo predio público', predio_ficha.tipo_predio_publico
                                                                  , 'Formalidad', predio_ficha.formalidad
                                                                  , 'Estrato', predio_ficha.estrato
                                                                  , 'Clase suelo POT', predio_ficha.clase_suelo_pot
                                                                  , 'Categoría suelo POT', predio_ficha.categoria_suelo_pot
                                                                  , 'Derecho FMI', predio_ficha.derecho_fmi
                                                                  , 'Inscrito RUPTA', predio_ficha.inscrito_rupta
                                                                  , 'Fecha medida RUPTA', predio_ficha.fecha_medida_rupta
                                                                  , 'Anotación FMI RUPTA', predio_ficha.anotacion_fmi_rupta
                                                                  , 'Inscrito protección colectiva', predio_ficha.inscrito_proteccion_colectiva
                                                                  , 'Fecha protección colectiva', predio_ficha.fecha_proteccion_colectiva
                                                                  , 'Anotación FMI protección colectiva', predio_ficha.anotacion_fmi_proteccion_colectiva
                                                                  , 'Inscrito proteccion Ley 1448', predio_ficha.inscrito_proteccion_ley1448
                                                                  , 'Fecha protección ley 1448', predio_ficha.fecha_proteccion_ley1448
                                                                  , 'Anotación FDM Ley 1448', predio_ficha.anotacion_fmi_ley1448
                                                                  , 'Inscripción URT', predio_ficha.inscripcion_urt
                                                                  , 'Fecha de inscripción URT', predio_ficha.fecha_inscripcion_urt
                                                                  , 'Anotación FMI URT', predio_ficha.anotacion_fmi_urt
                                                                  , 'Vigencia fiscal', predio_ficha.vigencia_fiscal
                                                                  , 'Observaciones', predio_ficha.observaciones
                                                                  , 'Fecha visita predial', predio_ficha.fecha_visita_predial
                                                                  , 'Nombre quien atendio', predio_ficha.nombre_quien_atendio
                                                                  , 'Número de documento de quien atendio', predio_ficha.numero_documento_quien_atendio
                                                                  , 'Categoría quien atendio', predio_ficha.categoria_quien_atendio
                                                                  , 'Tipo de documento de quien atendio', predio_ficha.tipo_documento_quien_atendio
                                                                  , 'Nombre encuestador', predio_ficha.nombre_encuestador
                                                                  , 'Número de documento encuestador', predio_ficha.numero_documento_encuestador
                                                                  , 'Tipo de documento encuestador', predio_ficha.tipo_documento_encuestador
                                                                  , 'nucleofamiliar', COALESCE(fpredio_nucleo_familiar.nucleofamiliar, '[]')
                                                                  , 'investigacionmercado', COALESCE(fpredio_investigacion_mercado.investigacionmercado, '[]')
        """

    query += """
                                                                 ))) FILTER(WHERE predio.t_id IS NOT NULL) as predio
         FROM {schema}.predio LEFT JOIN {schema}.uebaunit ON uebaunit.baunit_predio = predio.t_id
    """

    if property_record_card_model:
        query += """
         LEFT JOIN {schema}.predio_ficha ON predio_ficha.crpredio = predio.t_id
         LEFT JOIN fpredio_nucleo_familiar ON fpredio_nucleo_familiar.fichapredio = predio_ficha.t_id
         LEFT JOIN fpredio_investigacion_mercado ON fpredio_investigacion_mercado.fichapredio = predio_ficha.t_id
        """

    query += """
         WHERE predio.t_id IN (SELECT * FROM predios_seleccionados) AND uebaunit.ue_terreno IS NOT NULL
         GROUP BY uebaunit.ue_terreno
     ),
     info_terreno AS (
        SELECT terreno.t_id,
          json_build_object('id', terreno.t_id,
                            'attributes', json_build_object(CONCAT('Área de terreno' , (SELECT * FROM unidad_area_calculada_terreno)), terreno.area_calculada,
                                                            'predio', COALESCE(info_predio.predio, '[]')
                                                           )) as terreno
        FROM {schema}.terreno LEFT JOIN info_predio ON info_predio.ue_terreno = terreno.t_id
        WHERE terreno.t_id IN (SELECT * FROM terrenos_seleccionados)
     )
    SELECT json_agg(info_terreno.terreno) AS terreno FROM info_terreno
    """

    query = query.format(schema= schema, plot_t_id=plot_t_id, parcel_fmi=parcel_fmi, parcel_number=parcel_number, previous_parcel_number=previous_parcel_number)

    return query
