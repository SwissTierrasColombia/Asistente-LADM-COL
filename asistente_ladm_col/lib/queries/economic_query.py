def get_igac_economic_query(schema, plot_t_id, parcel_fmi, parcel_number, previous_parcel_number, property_record_card_model, valuation_model):

    query = """
    WITH
     unidad_avaluo_predio AS (
         SELECT ' [' || setting || ']' FROM {schema}.t_ili2db_column_prop WHERE tablename LIKE 'predio' AND columnname LIKE 'avaluo_predio' LIMIT 1
     ),
     unidad_area_calculada_terreno AS (
         SELECT ' [' || setting || ']' FROM {schema}.t_ili2db_column_prop WHERE tablename = 'terreno' AND columnname = 'area_calculada' LIMIT 1
     ),
     unidad_area_construida_uc AS (
         SELECT ' [' || setting || ']' FROM {schema}.t_ili2db_column_prop WHERE tablename = 'unidadconstruccion' AND columnname = 'area_construida' LIMIT 1
     ),
     unidad_valor_m2_construccion_u_c AS (
         SELECT ' [' || setting || ']' FROM {schema}.t_ili2db_column_prop WHERE tablename = 'unidad_construccion' AND columnname = 'valor_m2_construccion' LIMIT 1
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
     construcciones_seleccionadas AS (
         SELECT ue_construccion FROM {schema}.uebaunit WHERE uebaunit.baunit_predio IN (SELECT predios_seleccionados.t_id FROM predios_seleccionados WHERE predios_seleccionados.t_id IS NOT NULL) AND ue_construccion IS NOT NULL
     ),
     unidadesconstruccion_seleccionadas AS (
         SELECT unidadconstruccion.t_id FROM {schema}.unidadconstruccion WHERE unidadconstruccion.construccion IN (SELECT ue_construccion FROM construcciones_seleccionadas)
     ),
    """

    if valuation_model:
        query += """
     info_calificacion_convencional AS (
        SELECT avaluounidadconstruccion.aucons,
                    json_build_object('id', calificacion_convencional.t_id,
                                           'attributes', json_build_object('Tipo calificar', calificacion_convencional.tipo_calificar
                                                                           , 'Armazón', calificacion_convencional.armazon
                                                                           , 'Puntos armazón', calificacion_convencional.puntos_armazon
                                                                           , 'Muros', calificacion_convencional.muros
                                                                           , 'Puntos muro', calificacion_convencional.puntos_muro
                                                                           , 'Cubierta', calificacion_convencional.cubierta
                                                                           , 'Puntos cubierta', calificacion_convencional.puntos_cubierta
                                                                           , 'Conservación estructura', calificacion_convencional.conservacion_estructura
                                                                           , 'Puntos estructura conservación', calificacion_convencional.puntos_estructura_conservacion
                                                                           , 'Subtotal estructura', calificacion_convencional.sub_total_estructura
                                                                           , 'Fachada', calificacion_convencional.fachada
                                                                           , 'Puntos fachada', calificacion_convencional.puntos_fachada
                                                                           , 'Cubrimientos muros', calificacion_convencional.cubrimiento_muros
                                                                           , 'Puntos cubrimiento muros', calificacion_convencional.puntos_cubrimiento_muros
                                                                           , 'Piso', calificacion_convencional.piso
                                                                           , 'Puntos piso', calificacion_convencional.puntos_piso
                                                                           , 'Conservación acabados', calificacion_convencional.conservacion_acabados
                                                                           , 'Puntos conservación acabados', calificacion_convencional.puntos_conservacion_acabados
                                                                           , 'Subtotal acabados', calificacion_convencional.sub_total_acabados
                                                                           , 'Tamaño baño', calificacion_convencional.tamanio_banio
                                                                           , 'Puntos tamaño baño', calificacion_convencional.puntos_tamanio_banio
                                                                           , 'Enchape baño', calificacion_convencional.enchape_banio
                                                                           , 'Puntos enchape baño', calificacion_convencional.puntos_enchape_banio
                                                                           , 'Mobiliario baño', calificacion_convencional.mobiliario_banio
                                                                           , 'Puntos mobiliario baño', calificacion_convencional.puntos_mobiliario_banio
                                                                           , 'Conservación baño', calificacion_convencional.conservacion_banio
                                                                           , 'Puntos conservación baño', calificacion_convencional.puntos_conservacion_banio
                                                                           , 'Subtotal baño', calificacion_convencional.sub_total_banio
                                                                           , 'Tamaño cocina', calificacion_convencional.tamanio_cocina
                                                                           , 'Puntos tamaño cocina', calificacion_convencional.puntos_tamanio_cocina
                                                                           , 'Enchape cocina', calificacion_convencional.enchape_cocina
                                                                           , 'Puntos enchape cocina', calificacion_convencional.puntos_enchape_cocina
                                                                           , 'Mobiliario cocina', calificacion_convencional.mobiliario_cocina
                                                                           , 'Puntos mobiliario cocina', calificacion_convencional.puntos_mobiliario_cocina
                                                                           , 'Conservación cocina', calificacion_convencional.conservacion_cocina
                                                                           , 'Puntos conservacion cocina', calificacion_convencional.puntos_conservacion_cocina
                                                                           , 'Subtotal cocina', calificacion_convencional.sub_total_cocina
                                                                           , 'Total residencial y comercial', calificacion_convencional.total_residencial_y_comercial
                                                                           , 'Cerchas', calificacion_convencional.cerchas
                                                                           , 'Puntos cerchas', calificacion_convencional.puntos_cerchas
                                                                           , 'Total industrial', calificacion_convencional.total_industrial))
            AS calificacion_convencional
        FROM {schema}.calificacion_convencional LEFT JOIN {schema}.avaluounidadconstruccion ON calificacion_convencional.unidadconstruccion = avaluounidadconstruccion.aucons
        WHERE avaluounidadconstruccion.ucons IN (SELECT * FROM unidadesconstruccion_seleccionadas)
     ),
     info_calificacion_no_convencional AS (
        SELECT avaluounidadconstruccion.aucons,
                    json_build_object('id', calificacion_no_convencional.t_id,
                                           'attributes', json_build_object('Tipo de anexo', calificacion_no_convencional.tipo_anexo
                                                                           , 'Descripción anexo', calificacion_no_convencional.descripcion_anexo
                                                                           , 'Puntaje anexo', calificacion_no_convencional.puntaje_anexo))
            AS calificacion_no_convencional
        FROM {schema}.calificacion_no_convencional LEFT JOIN {schema}.avaluounidadconstruccion ON calificacion_no_convencional.unidadconstruccion = avaluounidadconstruccion.aucons
        WHERE avaluounidadconstruccion.ucons IN (SELECT * FROM unidadesconstruccion_seleccionadas)
     ),
        """

    query += """
     info_uc AS (
         SELECT unidadconstruccion.construccion,
                json_agg(json_build_object('id', unidadconstruccion.t_id,
                                  'attributes', json_build_object('Número de pisos', unidadconstruccion.numero_pisos
                                                                  , CONCAT('Área construida' , (SELECT * FROM unidad_area_construida_uc)), unidadconstruccion.area_construida
    """

    if valuation_model:
        query += """
                                                                  , 'Uso',  unidad_construccion.uso
                                                                  , 'Destino económico',  unidad_construccion.destino_econo
                                                                  , 'Tipología',  unidad_construccion.tipologia
                                                                  , 'Puntuación',  unidad_construccion.puntuacion
                                                                  , CONCAT('Valor m2 construcción' , (SELECT * FROM unidad_valor_m2_construccion_u_c)),  unidad_construccion.valor_m2_construccion
                                                                  , 'Año construcción',  unidad_construccion.anio_construction
                                                                  , 'Estado conservación',  unidad_construccion.estado_conservacion
                                                                  , 'Número de habitaciones',  unidad_construccion.num_habitaciones
                                                                  , 'Número de baños',  unidad_construccion.num_banios
                                                                  , 'Número de cocinas',  unidad_construccion.num_cocinas
                                                                  , 'Número de oficinas',  unidad_construccion.num_oficinas
                                                                  , 'Número de estudios',  unidad_construccion.num_estudios
                                                                  , 'Número de bodegas',  unidad_construccion.num_bodegas
                                                                  , 'Numero de locales',  unidad_construccion.num_locales
                                                                  , 'Número de salas',  unidad_construccion.num_salas
                                                                  , 'Número de comedores',  unidad_construccion.num_comedores
                                                                  , 'Material',  unidad_construccion.material
                                                                  , 'Estilo',  unidad_construccion.estilo
                                                                  , 'Acceso',  unidad_construccion.acceso
                                                                  , 'nivel de acceso',  unidad_construccion.nivel_de_acceso
                                                                  , 'Ubicación en copropiedad',  unidad_construccion.ubicacion_en_copropiedad
                                                                  , 'Disposición',  unidad_construccion.disposicion
                                                                  , 'Funcionalidad',  unidad_construccion.funcionalidad
                                                                  , 'Tipo de construcción',  unidad_construccion.construccion_tipo
                                                                  , 'Calificación', CASE WHEN info_calificacion_convencional.calificacion_convencional IS NOT NULL THEN
                                                                                        COALESCE(info_calificacion_convencional.calificacion_convencional, '[]')
                                                                                    ELSE
                                                                                        COALESCE(info_calificacion_no_convencional.calificacion_no_convencional, '[]')
                                                                                    END
        """

    query += """
                                                                 ))) FILTER(WHERE unidadconstruccion.t_id IS NOT NULL)  as unidadconstruccion
         FROM {schema}.unidadconstruccion
    """

    if valuation_model:
        query += """
         LEFT JOIN {schema}.avaluounidadconstruccion ON unidadconstruccion.t_id = avaluounidadconstruccion.ucons
         LEFT JOIN {schema}.unidad_construccion ON avaluounidadconstruccion.aucons = unidad_construccion.t_id
         LEFT JOIN info_calificacion_convencional ON unidad_construccion.t_id = info_calificacion_convencional.aucons
         LEFT JOIN info_calificacion_no_convencional ON unidad_construccion.t_id = info_calificacion_no_convencional.aucons
        """

    query += """
         WHERE unidadconstruccion.t_id IN (SELECT * FROM unidadesconstruccion_seleccionadas)
         GROUP BY unidadconstruccion.construccion
     ),
     info_construccion as (
         SELECT uebaunit.baunit_predio,
                json_agg(json_build_object('id', construccion.t_id,
                                  'attributes', json_build_object('Área construcción', construccion.area_construccion,
                                                                  'unidadconstruccion', COALESCE(info_uc.unidadconstruccion, '[]')
                                                                 ))) FILTER(WHERE construccion.t_id IS NOT NULL) as construccion
         FROM {schema}.construccion LEFT JOIN info_uc ON construccion.t_id = info_uc.construccion
         LEFT JOIN {schema}.uebaunit ON uebaunit.ue_construccion = info_uc.construccion
         WHERE construccion.t_id IN (SELECT * FROM construcciones_seleccionadas)
         GROUP BY uebaunit.baunit_predio
     ),
     info_predio AS (
         SELECT uebaunit.ue_terreno,
                json_agg(json_build_object('id', predio.t_id,
                                  'attributes', json_build_object('Nombre', predio.nombre,
                                                                  'Departamento', predio.departamento,
                                                                  'Municipio', predio.municipio,
                                                                  'Zona', predio.zona,
                                                                  'NUPRE', predio.nupre,
                                                                  'FMI', predio.fmi,
                                                                  'Número predial', predio.numero_predial,
                                                                  'Número predial anterior', predio.numero_predial_anterior,
                                                                  CONCAT('Avalúo predio' , (select * from unidad_avaluo_predio)), predio.avaluo_predio,
                                                                  'Tipo', predio.tipo,
    """

    if property_record_card_model:
        query += """
                                                                  'Destinación económica', predio_ficha.destinacion_economica,
        """

    query += """
                                                                  'construccion', COALESCE(info_construccion.construccion, '[]')
                                                                 ))) FILTER(WHERE predio.t_id IS NOT NULL) as predio
         FROM {schema}.predio LEFT JOIN {schema}.uebaunit ON uebaunit.baunit_predio = predio.t_id
         LEFT JOIN info_construccion ON predio.t_id = info_construccion.baunit_predio
    """

    if property_record_card_model:
        query += """
         LEFT JOIN {schema}.predio_ficha ON predio_ficha.crpredio = predio.t_id
        """

    query += """
         WHERE predio.t_id IN (SELECT * FROM predios_seleccionados) AND uebaunit.ue_terreno IS NOT NULL
         GROUP BY uebaunit.ue_terreno
     ),
    """

    if valuation_model:
        query += """
     info_zona_homogenea_geoeconomica AS (
        SELECT terreno.t_id,
            json_agg(
                    json_build_object('id', zona_homogenea_geoeconomica.t_id,
                                           'attributes', json_build_object('Porcentaje', ROUND((st_area(st_intersection(terreno.poligono_creado, zona_homogenea_geoeconomica.geometria))/ st_area(terreno.poligono_creado))::numeric * 100,2),
                                                                           'Valor', zona_homogenea_geoeconomica.valor,
                                                                           'Identificador', zona_homogenea_geoeconomica.identificador))
            ) FILTER(WHERE zona_homogenea_geoeconomica.t_id IS NOT NULL) AS zona_homogenea_geoeconomica
        FROM {schema}.terreno, {schema}.zona_homogenea_geoeconomica
        WHERE terreno.t_id IN (SELECT * FROM terrenos_seleccionados) AND
              st_intersects(terreno.poligono_creado, zona_homogenea_geoeconomica.geometria) = True AND
              st_area(st_intersection(terreno.poligono_creado, zona_homogenea_geoeconomica.geometria)) > 0
        GROUP BY terreno.t_id
     ),
     info_zona_homogenea_fisica AS (
        SELECT terreno.t_id,
            json_agg(
                    json_build_object('id', zona_homogenea_fisica.t_id,
                                           'attributes', json_build_object('Porcentaje', ROUND((st_area(st_intersection(terreno.poligono_creado, zona_homogenea_fisica.geometria))/ st_area(terreno.poligono_creado))::numeric * 100, 2),
                                                                           'Identificador', zona_homogenea_fisica.identificador))
            ) FILTER(WHERE zona_homogenea_fisica.t_id IS NOT NULL) AS zona_homogenea_fisica
        FROM {schema}.terreno, {schema}.zona_homogenea_fisica
        WHERE terreno.t_id IN (SELECT * FROM terrenos_seleccionados) AND
              st_intersects(terreno.poligono_creado, zona_homogenea_fisica.geometria) = True AND
              st_area(st_intersection(terreno.poligono_creado, zona_homogenea_fisica.geometria)) > 0
        GROUP BY terreno.t_id
     ),
        """

    query += """
     info_terreno AS (
        SELECT terreno.t_id,
          json_build_object('id', terreno.t_id,
                            'attributes', json_build_object(CONCAT('Área de terreno' , (SELECT * FROM unidad_area_calculada_terreno)), terreno.area_calculada
    """

    if valuation_model:
        query += """
                                                            , 'zona_homogenea_geoeconomica', COALESCE(info_zona_homogenea_geoeconomica.zona_homogenea_geoeconomica, '[]')
                                                            , 'zona_homogenea_fisica', COALESCE(info_zona_homogenea_fisica.zona_homogenea_fisica, '[]')
        """

    query += """
                                                            , 'predio', COALESCE(info_predio.predio, '[]')
                                                           )) as terreno
        FROM {schema}.terreno LEFT JOIN info_predio ON info_predio.ue_terreno = terreno.t_id
    """

    if valuation_model:
        query += """
        LEFT JOIN info_zona_homogenea_geoeconomica ON info_zona_homogenea_geoeconomica.t_id = terreno.t_id
        LEFT JOIN info_zona_homogenea_fisica ON info_zona_homogenea_fisica.t_id = terreno.t_id
        """

    query += """
        WHERE terreno.t_id IN (SELECT * FROM terrenos_seleccionados)
     )
    SELECT json_agg(info_terreno.terreno) AS terreno FROM info_terreno
    """

    query = query.format(schema= schema, plot_t_id=plot_t_id, parcel_fmi=parcel_fmi, parcel_number=parcel_number, previous_parcel_number=previous_parcel_number)

    return query
