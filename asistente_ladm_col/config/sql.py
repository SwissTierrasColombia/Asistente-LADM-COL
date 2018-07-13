def GET_PARCEL_SQL(db_schema, plot__t_id):
    return """
     SELECT     predio.fmi            AS "Folio" ,
               predio.nupre          AS "NUPRE" ,
               predio.numero_predial AS "Número Predial" ,
               predio.nombre         AS "Nombre del predio" ,
               Json_agg(derecho)     AS derecho ,
               CASE
                          WHEN Json_agg(servidumbre)::text <> '[null]' THEN Json_agg(servidumbre)
                          ELSE NULL
               END AS servidumbre
    FROM       {db_schema}.terreno
    LEFT JOIN  {db_schema}.uebaunit
    ON         terreno.t_id = uebaunit.ue_terreno
    LEFT JOIN  {db_schema}.predio
    ON         predio.t_id = uebaunit.baunit_predio
    INNER JOIN
               (
                         SELECT    col_derecho.unidad_predio ,
                                   col_derecho.tipo "Tipo derecho" ,
                                   col_derecho.codigo_registral_derecho "Codigo Registral" ,
                                   col_derecho.descripcion "Descripción" ,
                                   interesado_natural.documento_identidad "Documento Identidad" ,
                                   interesado_natural.tipo_documento "Tipo Documento" ,
                                   interesado_natural.primer_apellido "Primer Apellido" ,
                                   interesado_natural.primer_nombre "Primer Nombre" ,
                                   interesado_natural.segundo_apellido "Segundo Apellido" ,
                                   interesado_natural.segundo_nombre "Segundo Nombre" ,
                                   interesado_natural.genero "Género"
                         FROM      {db_schema}.col_derecho
                         LEFT JOIN {db_schema}.interesado_natural
                         ON        col_derecho.interesado_interesado_natural = interesado_natural.t_id ) derecho
    ON         derecho.unidad_predio = predio.t_id
    LEFT JOIN
               (
                      SELECT servidumbrepaso.identificador,
                             uebaunit.baunit_predio,
                             uebaunit.ue_servidumbrepaso,
                             servidumbrepaso.etiqueta
                      FROM   {db_schema}.uebaunit
                      JOIN   {db_schema}.servidumbrepaso
                      ON     uebaunit.ue_servidumbrepaso = servidumbrepaso.t_id ) servidumbre
    ON         servidumbre.baunit_predio = predio.t_id
    WHERE      terreno.t_id = '{plot_t_id}'
    GROUP BY   predio.fmi ,
               predio.nupre ,
               predio.numero_predial ,
               predio.nombre;
    """.format(db_schema=db_schema, plot_t_id=plot__t_id)