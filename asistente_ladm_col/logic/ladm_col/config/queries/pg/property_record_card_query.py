from asistente_ladm_col.logic.ladm_col.config.queries.pg.pg_queries_config_utils import (get_custom_filter_parcels,
                                                                                         get_custom_filter_plots)


def get_igac_property_record_card_query(schema, plot_t_ids, parcel_fmi, parcel_number, previous_parcel_number):
    custom_filter_plots = get_custom_filter_plots(schema, plot_t_ids)
    custom_filter_parcels = get_custom_filter_parcels(schema, plot_t_ids)

    query = """
                WITH
                 unidad_area_terreno AS (
                     SELECT ' [' || setting || ']' FROM {schema}.t_ili2db_column_prop WHERE tablename = 'op_terreno' AND columnname = 'area_terreno' LIMIT 1
                 ),
                 terrenos_seleccionados AS (
                    {custom_filter_plots}
                    SELECT col_uebaunit.ue_op_terreno FROM {schema}.op_predio LEFT JOIN {schema}.col_uebaunit ON op_predio.t_id = col_uebaunit.baunit  WHERE col_uebaunit.ue_op_terreno IS NOT NULL AND CASE WHEN '{parcel_fmi}' = 'NULL' THEN  1 = 2 ELSE (op_predio.codigo_orip || '-'|| op_predio.matricula_inmobiliaria) = '{parcel_fmi}' END
                        UNION
                    SELECT col_uebaunit.ue_op_terreno FROM {schema}.op_predio LEFT JOIN {schema}.col_uebaunit ON op_predio.t_id = col_uebaunit.baunit  WHERE col_uebaunit.ue_op_terreno IS NOT NULL AND CASE WHEN '{parcel_number}' = 'NULL' THEN  1 = 2 ELSE op_predio.numero_predial = '{parcel_number}' END
                        UNION
                    SELECT col_uebaunit.ue_op_terreno FROM {schema}.op_predio LEFT JOIN {schema}.col_uebaunit ON op_predio.t_id = col_uebaunit.baunit  WHERE col_uebaunit.ue_op_terreno IS NOT NULL AND CASE WHEN '{previous_parcel_number}' = 'NULL' THEN  1 = 2 ELSE op_predio.numero_predial_anterior = '{previous_parcel_number}' END
                 ),
                 predios_seleccionados AS (
                    {custom_filter_parcels}
                    SELECT t_id FROM {schema}.op_predio WHERE CASE WHEN '{parcel_fmi}' = 'NULL' THEN  1 = 2 ELSE (op_predio.codigo_orip || '-'|| op_predio.matricula_inmobiliaria) = '{parcel_fmi}' END
                        UNION
                    SELECT t_id FROM {schema}.op_predio WHERE CASE WHEN '{parcel_number}' = 'NULL' THEN  1 = 2 ELSE op_predio.numero_predial = '{parcel_number}' END
                        UNION
                    SELECT t_id FROM {schema}.op_predio WHERE CASE WHEN '{previous_parcel_number}' = 'NULL' THEN  1 = 2 ELSE op_predio.numero_predial_anterior = '{previous_parcel_number}' END
                 ),
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
                                                                             )) ORDER BY op_predio.t_id) FILTER(WHERE op_predio.t_id IS NOT NULL) as op_predio
                     FROM {schema}.op_predio LEFT JOIN {schema}.col_uebaunit ON col_uebaunit.baunit = op_predio.t_id
                     WHERE op_predio.t_id IN (SELECT * FROM predios_seleccionados)
                     AND col_uebaunit.ue_op_terreno IS NOT NULL
                     AND col_uebaunit.ue_op_construccion IS NULL
                     AND col_uebaunit.ue_op_unidadconstruccion IS NULL
                     GROUP BY col_uebaunit.ue_op_terreno
                 ),
                 info_terreno AS (
                    SELECT op_terreno.t_id,
                      json_build_object('id', op_terreno.t_id,
                                        'attributes', json_build_object(CONCAT('Área' , (SELECT * FROM unidad_area_terreno)), op_terreno.area_terreno,
                                                                        'op_predio', COALESCE(info_predio.op_predio, '[]')
                                                                       )) as terreno
                    FROM {schema}.op_terreno LEFT JOIN info_predio ON info_predio.ue_op_terreno = op_terreno.t_id
                    WHERE op_terreno.t_id IN (SELECT * FROM terrenos_seleccionados)
                    ORDER BY op_terreno.t_id
                 )
                 SELECT json_build_object('op_terreno', json_agg(info_terreno.terreno)) FROM info_terreno
    """

    query = query.format(schema=schema, custom_filter_plots=custom_filter_plots, custom_filter_parcels=custom_filter_parcels, parcel_fmi=parcel_fmi, parcel_number=parcel_number,
                         previous_parcel_number=previous_parcel_number)

    return query
