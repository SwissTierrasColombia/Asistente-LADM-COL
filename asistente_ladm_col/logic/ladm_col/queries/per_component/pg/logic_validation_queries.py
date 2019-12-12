from qgis.PyQt.QtCore import QCoreApplication


def get_logic_validation_queries(schema, names):
    return {
            'DEPARTMENT_CODE_VALIDATION': {
                'query': """SELECT {id} FROM {schema}.{table} p WHERE (p.{field} IS NOT NULL AND (length(p.{field}) !=2 OR (p.{field}~ '^[0-9]*$') = FALSE))""".format(
                    schema=schema, table=names.OP_PARCEL_T, id=names.T_ID_F, field=names.OP_PARCEL_T_DEPARTMENT_F),
                'desc_error': 'Department code must have two numerical characters.',
                'table_name': QCoreApplication.translate("LogicChecksConfigStrings",
                                                         "Logic Consistency Errors in table '{table}'").format(
                    table=names.OP_PARCEL_T),
                'table': names.OP_PARCEL_T},
            'MUNICIPALITY_CODE_VALIDATION': {
                'query': """SELECT {id} FROM {schema}.{table} p WHERE (p.{field} IS NOT NULL AND (length(p.{field}) !=3 OR (p.{field}~ '^[0-9]*$') = FALSE))""".format(
                    schema=schema, table=names.OP_PARCEL_T, id=names.T_ID_F, field=names.OP_PARCEL_T_MUNICIPALITY_F),
                'desc_error': 'Municipality code must have three numerical characters.',
                'table_name': QCoreApplication.translate("LogicChecksConfigStrings",
                                                         "Logic Consistency Errors in table '{table}'").format(
                    table=names.OP_PARCEL_T),
                'table': names.OP_PARCEL_T},
            'PARCEL_NUMBER_VALIDATION': {
                'query': """SELECT {id} FROM {schema}.{table} p WHERE (p.{field} IS NOT NULL AND (length(p.{field}) !=30 OR (p.{field}~ '^[0-9]*$') = FALSE))""".format(
                    schema=schema, table=names.OP_PARCEL_T, id=names.T_ID_F, field=names.OP_PARCEL_T_PARCEL_NUMBER_F),
                'desc_error': 'Parcel number must have 30 numerical characters.',
                'table_name': QCoreApplication.translate("LogicChecksConfigStrings",
                                                         "Logic Consistency Errors in table '{table}'").format(
                    table=names.OP_PARCEL_T),
                'table': names.OP_PARCEL_T},
            'PARCEL_NUMBER_BEFORE_VALIDATION': {
                'query': """SELECT {id} FROM {schema}.{table} p WHERE (p.{field} IS NOT NULL AND (length(p.{field}) !=20 OR (p.{field}~ '^[0-9]*$') = FALSE))""".format(
                    schema=schema, table=names.OP_PARCEL_T, id=names.T_ID_F, field=names.OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F),
                'desc_error': 'Parcel number before must have 20 numerical characters.',
                'table_name': QCoreApplication.translate("LogicChecksConfigStrings",
                                                         "Logic Consistency Errors in table '{table}'").format(
                    table=names.OP_PARCEL_T),
                'table': names.OP_PARCEL_T},
            'COL_PARTY_TYPE_NATURAL_VALIDATION': {
                'query': """
                        SELECT p.{id},
                               CASE WHEN p.{business_name} IS NOT NULL THEN 1 ELSE 0 END AS "{business_name}",
                               CASE WHEN p.{col_party_surname} IS NULL OR length(trim(p.{col_party_surname})) > 0 is False THEN 1 ELSE 0 END "{col_party_surname}",
                               CASE WHEN p.{col_party_first_name} IS NULL OR length(trim(p.{col_party_first_name})) > 0 is False THEN 1 ELSE 0 END "{col_party_first_name}",
                               CASE WHEN p.{col_party_doc_type} = (select {id} from {schema}.{OP_PARTY_DOCUMENT_TYPE_D} where {ILICODE_F} = '{OP_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V}') THEN 1 ELSE 0 END "{col_party_doc_type}"
                        FROM {schema}.{table} p
                        WHERE p.{col_party_type} = (select {id} from {schema}.{OP_PARTY_TYPE_D} where {ILICODE_F} = '{OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V}') AND (
                            p.{business_name} IS NOT NULL OR
                            p.{col_party_surname} IS NULL OR
                            length(trim(p.{col_party_surname})) > 0 is False OR
                            p.{col_party_first_name} IS NULL OR 
                            length(trim(p.{col_party_first_name})) > 0 is False OR
                            p.{col_party_doc_type} = (select {id} from {schema}.{OP_PARTY_DOCUMENT_TYPE_D} where {ILICODE_F} = '{OP_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V}'))
                """.format(schema=schema,
                           table=names.OP_PARTY_T,
                           id=names.T_ID_F,
                           col_party_type=names.OP_PARTY_T_TYPE_F,
                           OP_PARTY_TYPE_D=names.OP_PARTY_TYPE_D,
                           ILICODE_F=names.ILICODE_F,
                           OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V=names.OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V,
                           OP_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V=names.OP_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V,
                           OP_PARTY_DOCUMENT_TYPE_D=names.OP_PARTY_DOCUMENT_TYPE_D,
                           business_name=names.OP_PARTY_T_BUSINESS_NAME_F,
                           col_party_surname=names.OP_PARTY_T_SURNAME_1_F,
                           col_party_first_name=names.OP_PARTY_T_FIRST_NAME_1_F,
                           col_party_doc_type=names.OP_PARTY_T_DOCUMENT_TYPE_F),
                'desc_error': 'Party with type \'Persona_Natural\' is invalid.',
                'table_name': QCoreApplication.translate("LogicChecksConfigStrings",
                                                         "Logic Consistency Errors in table '{table}'").format(
                    table=names.OP_PARTY_T),
                'table': names.OP_PARTY_T},
            'COL_PARTY_TYPE_NO_NATURAL_VALIDATION': {
                'query': """
                            SELECT p.{id},
                                   CASE WHEN p.{business_name} IS NULL OR length(trim(p.{business_name})) > 0 is False THEN 1 ELSE 0 END AS "{business_name}",
                                   CASE WHEN p.{col_party_surname} IS NOT NULL THEN 1 ELSE 0 END AS "{col_party_surname}",
                                   CASE WHEN p.{col_party_first_name} IS NOT NULL THEN 1 ELSE 0 END AS "{col_party_first_name}",
                                   CASE WHEN p.{col_party_doc_type} NOT IN ((select {id} from {schema}.{OP_PARTY_DOCUMENT_TYPE_D} where {ILICODE_F} = '{OP_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V}')) THEN 1 ELSE 0 END AS "{col_party_doc_type}"
                            FROM {schema}.{table} p
                            WHERE p.{col_party_type} = (select {id} from {schema}.{OP_PARTY_TYPE_D} where {ILICODE_F} = '{OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V}') AND (
                                p.{business_name} IS NULL OR
                                length(trim(p.{business_name})) > 0 is False OR
                                p.{col_party_surname} IS NOT NULL OR
                                p.{col_party_first_name} IS NOT NULL OR
                                p.{col_party_doc_type} NOT IN ((select {id} from {schema}.{OP_PARTY_DOCUMENT_TYPE_D} where {ILICODE_F} = '{OP_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V}')))
                        """.format(schema=schema, table=names.OP_PARTY_T, id=names.T_ID_F,
                                   OP_PARTY_TYPE_D=names.OP_PARTY_TYPE_D, ILICODE_F=names.ILICODE_F, OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V=names.OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V,
                                   OP_PARTY_DOCUMENT_TYPE_D=names.OP_PARTY_DOCUMENT_TYPE_D, OP_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V=names.OP_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V,
                                   col_party_type=names.OP_PARTY_T_TYPE_F, business_name=names.OP_PARTY_T_BUSINESS_NAME_F,
                                   col_party_surname=names.OP_PARTY_T_SURNAME_1_F,
                                   col_party_first_name=names.OP_PARTY_T_FIRST_NAME_1_F,
                                   col_party_doc_type=names.OP_PARTY_T_DOCUMENT_TYPE_F),
                'desc_error': 'Party with type \'Persona_No_Natural\' is invalid.',
                'table_name': QCoreApplication.translate("LogicChecksConfigStrings",
                                                         "Logic Consistency Errors in table '{table}'").format(
                    table=names.OP_PARTY_T),
                'table': names.OP_PARTY_T},
            'UEBAUNIT_PARCEL_VALIDATION': {
                'query': """
                    SELECT * FROM (
                        SELECT {id}, {parcel_type}, sum(count_terreno) sum_t, sum(count_construccion) sum_c, sum(count_unidadconstruccion) sum_uc FROM (
                            SELECT p.{id},
                                    p.{parcel_type},
                                    (CASE WHEN ue.{ueb_plot} IS NOT NULL THEN 1 ELSE 0 END) count_terreno,
                                    (CASE WHEN ue.{ueb_building} IS NOT NULL THEN 1 ELSE 0 END) count_construccion,
                                    (CASE WHEN ue.{ueb_building_unit} IS NOT NULL THEN 1 ELSE 0 END) count_unidadconstruccion
                            FROM {schema}.{input_table} p left join {schema}.{join_table} ue on p.{id} = ue.{join_field}
                        ) AS p_ue GROUP BY {id}, {parcel_type}
                    ) AS report WHERE
                               ({parcel_type}= (select {id} from {schema}.{OP_CONDITION_PARCEL_TYPE_D} where {ILICODE_F} = '{PARCEL_TYPE_NO_HORIZONTAL_PROPERTY}') AND (sum_t !=1 OR sum_uc != 0)) OR 
                               ({parcel_type} in (select {id} from {schema}.{OP_CONDITION_PARCEL_TYPE_D} where {ILICODE_F} in ('{PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT}', '{PARCEL_TYPE_CONDOMINIUM_PARENT}', '{PARCEL_TYPE_CEMETERY_PARENT}', '{PARCEL_TYPE_PUBLIC_USE}', '{PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT}')) AND (sum_t!=1 OR sum_uc > 0)) OR 
                               ({parcel_type} in (select {id} from {schema}.{OP_CONDITION_PARCEL_TYPE_D} where {ILICODE_F} in ('{PARCEL_TYPE_ROAD}', '{PARCEL_TYPE_CEMETERY_PARCEL_UNIT}')) AND (sum_t !=1 OR sum_uc > 0 OR sum_c > 0)) OR 
                               ({parcel_type}= (select {id} from {schema}.{OP_CONDITION_PARCEL_TYPE_D} where {ILICODE_F} = '{PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT}') AND (sum_t !=0 OR sum_c != 0 OR sum_uc = 0 )) OR 
                               ({parcel_type} in (select {id} from {schema}.{OP_CONDITION_PARCEL_TYPE_D} where {ILICODE_F} in ('{PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA}', '{PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA}')) AND (sum_t !=0 OR sum_c != 1 OR sum_uc != 0))
                """.format(schema=schema, input_table=names.OP_PARCEL_T, join_table=names.COL_UE_BAUNIT_T,
                           OP_CONDITION_PARCEL_TYPE_D=names.OP_CONDITION_PARCEL_TYPE_D, ILICODE_F=names.ILICODE_F, PARCEL_TYPE_NO_HORIZONTAL_PROPERTY=names.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY,
                           PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT=names.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT,
                           PARCEL_TYPE_CONDOMINIUM_PARENT=names.PARCEL_TYPE_CONDOMINIUM_PARENT,
                           PARCEL_TYPE_CEMETERY_PARENT=names.PARCEL_TYPE_CEMETERY_PARENT,
                           PARCEL_TYPE_PUBLIC_USE=names.PARCEL_TYPE_PUBLIC_USE,
                           PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT=names.PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT,
                           PARCEL_TYPE_CEMETERY_PARCEL_UNIT=names.PARCEL_TYPE_CEMETERY_PARCEL_UNIT, PARCEL_TYPE_ROAD=names.PARCEL_TYPE_ROAD,
                           PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT=names.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT,
                           PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA=names.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA, PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA=names.PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA,
                           join_field=names.COL_UE_BAUNIT_T_PARCEL_F, id=names.T_ID_F, parcel_type=names.OP_PARCEL_T_PARCEL_TYPE_F,
                           ueb_plot=names.COL_UE_BAUNIT_T_OP_PLOT_F, ueb_building=names.COL_UE_BAUNIT_T_OP_BUILDING_F,
                           ueb_building_unit=names.COL_UE_BAUNIT_T_OP_BUILDING_UNIT_F),
                'desc_error': 'Parcel must have one or more spatial units associated with it.',
                'table_name': QCoreApplication.translate("LogicChecksConfigStrings",
                                                         "Errors in relationships between Spatial Units and Parcels"),
                'table': names.OP_PARCEL_T},
            'PARCEL_TYPE_AND_22_POSITION_OF_PARCEL_NUMBER_VALIDATION': {
                'query': """
                        SELECT p.{id}, p.{parcel_type} FROM {schema}.{table} p
                        WHERE (p.{parcel_number} IS NOT NULL AND 
                               (substring(p.{parcel_number},22,1) != '0' AND p.{parcel_type}=(select {id} from {schema}.{OP_CONDITION_PARCEL_TYPE_D} where {ILICODE_F} = '{PARCEL_TYPE_NO_HORIZONTAL_PROPERTY}')) OR
                               (substring(p.{parcel_number},22,1) != '9' AND p.{parcel_type} in (select {id} from {schema}.{OP_CONDITION_PARCEL_TYPE_D} where {ILICODE_F} in ('{PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT}', '{PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT}'))) OR
                               (substring(p.{parcel_number},22,1) != '8' AND p.{parcel_type} in (select {id} from {schema}.{OP_CONDITION_PARCEL_TYPE_D} where {ILICODE_F} in ('{PARCEL_TYPE_CONDOMINIUM_PARENT}', '{PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT}'))) OR
                               (substring(p.{parcel_number},22,1) != '7' AND p.{parcel_type} in (select {id} from {schema}.{OP_CONDITION_PARCEL_TYPE_D} where {ILICODE_F} in ('{PARCEL_TYPE_CEMETERY_PARENT}', '{PARCEL_TYPE_CEMETERY_PARCEL_UNIT}'))) OR
                               (substring(p.{parcel_number},22,1) != '5' AND p.{parcel_type} in (select {id} from {schema}.{OP_CONDITION_PARCEL_TYPE_D} where {ILICODE_F} in ('{PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA}', '{PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA}'))) OR
                               (substring(p.{parcel_number},22,1) != '4' AND p.{parcel_type}=(select {id} from {schema}.{OP_CONDITION_PARCEL_TYPE_D} where {ILICODE_F} = '{PARCEL_TYPE_ROAD}')) OR
                               (substring(p.{parcel_number},22,1) != '3' AND p.{parcel_type}=(select {id} from {schema}.{OP_CONDITION_PARCEL_TYPE_D} where {ILICODE_F} = '{PARCEL_TYPE_PUBLIC_USE}'))
                            )""".format(schema=schema, table=names.OP_PARCEL_T, id=names.T_ID_F,
                                    OP_CONDITION_PARCEL_TYPE_D=names.OP_CONDITION_PARCEL_TYPE_D, ILICODE_F=names.ILICODE_F, PARCEL_TYPE_NO_HORIZONTAL_PROPERTY=names.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY,
                                    PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT=names.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT, PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT=names.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT,
                                    PARCEL_TYPE_CONDOMINIUM_PARENT=names.PARCEL_TYPE_CONDOMINIUM_PARENT, PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT=names.PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT,
                                    PARCEL_TYPE_CEMETERY_PARENT=names.PARCEL_TYPE_CEMETERY_PARENT, PARCEL_TYPE_CEMETERY_PARCEL_UNIT=names.PARCEL_TYPE_CEMETERY_PARCEL_UNIT,
                                    PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA=names.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA, PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA=names.PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA,
                                    PARCEL_TYPE_ROAD=names.PARCEL_TYPE_ROAD, PARCEL_TYPE_PUBLIC_USE=names.PARCEL_TYPE_PUBLIC_USE,
                                    parcel_number=names.OP_PARCEL_T_PARCEL_NUMBER_F, parcel_type=names.OP_PARCEL_T_PARCEL_TYPE_F),
                'desc_error': 'The position 22 of the parcel number must correspond to the type of parcel.',
                'table_name': QCoreApplication.translate("LogicChecksConfigStrings",
                                                         "Logic Consistency Errors in table '{table}'").format(
                    table=names.OP_PARCEL_T),
                'table': names.OP_PARCEL_T},
            'DUPLICATE_RECORDS_IN_TABLE': {
                'query': """
                    SELECT array_to_string(duplicate_ids, ',') AS "duplicate_ids", duplicate_total
                    FROM (
                        SELECT unique_concat,  array_agg({id}) duplicate_ids, array_length(array_agg({id}), 1) duplicate_total
                        FROM (
                            SELECT concat({fields}) unique_concat, {id}, 
                            row_number() OVER(PARTITION BY {fields} ORDER BY {id} asc) AS row
                            FROM {schema}.{table}
                        ) AS count_rows
                        GROUP BY unique_concat
                    ) report
                    WHERE duplicate_total > 1
                """,
                'desc_error': 'Check duplicate records in a table',
                'table_name': '',
                'table': ''},
            'GROUP_PARTY_FRACTIONS_SHOULD_SUM_1': {
                'query': """WITH grupos AS (
                        SELECT array_agg({T_ID_F}) AS tids, {MEMBERS_T_GROUP_PARTY_F}
                        FROM {schema}.{members}
                        GROUP BY {MEMBERS_T_GROUP_PARTY_F}
                    ),
                     sumas AS (
                        SELECT grupos.{MEMBERS_T_GROUP_PARTY_F}, grupos.tids as miembros, SUM({fraction}.{FRACTION_S_NUMERATOR_F}::float/{fraction}.{FRACTION_S_DENOMINATOR_F}) as suma_fracciones
                        FROM {schema}.{fraction}, grupos
                        WHERE {FRACTION_S_MEMBER_F} = ANY(grupos.tids)
                        GROUP BY {MEMBERS_T_GROUP_PARTY_F}, tids
                    )
                    SELECT sumas.*
                    FROM sumas
                    WHERE sumas.suma_fracciones != 1""".format(schema=schema,
                                                               T_ID_F=names.T_ID_F,
                                                               MEMBERS_T_GROUP_PARTY_F=names.MEMBERS_T_GROUP_PARTY_F,
                                                               fraction=names.FRACTION_S,
                                                               FRACTION_S_NUMERATOR_F=names.FRACTION_S_NUMERATOR_F,
                                                               FRACTION_S_DENOMINATOR_F=names.FRACTION_S_DENOMINATOR_F,
                                                               FRACTION_S_MEMBER_F=names.FRACTION_S_MEMBER_F,
                                                               members=names.MEMBERS_T),
                'desc_error': 'Group Party Fractions should sum 1',
                'table_name': QCoreApplication.translate("LogicChecksConfigStrings", "Fractions do not sum 1").format(
                    names.OP_PARCEL_T),
                'table': '{fraction}_and_{members}'.format(fraction=names.FRACTION_S, members=names.MEMBERS_T)},
            'PARCELS_WITH_NO_RIGHT': {
                'query': """SELECT p.{T_ID_F}
                   FROM {schema}.{table} p
                   WHERE p.{T_ID_F} NOT IN (
                        SELECT {COL_BAUNIT_RRR_T_UNIT_F} FROM {schema}.{OP_RIGHT_T})""".format(schema=schema,
                                                                                               table=names.OP_PARCEL_T,
                                                                                               OP_RIGHT_T=names.OP_RIGHT_T,
                                                                                               COL_BAUNIT_RRR_T_UNIT_F=names.COL_BAUNIT_RRR_T_UNIT_F,
                                                                                               T_ID_F=names.T_ID_F),
                'desc_error': 'Get parcels with no right',
                'table_name': QCoreApplication.translate("LogicChecksConfigStrings", "Parcels with no right"),
                'table': names.OP_PARCEL_T},
            'PARCELS_WITH_REPEATED_DOMAIN_RIGHT': {
                'query': """SELECT conteo.{COL_BAUNIT_RRR_T_UNIT_F}
                    FROM {schema}.{table} p, (
                        SELECT {COL_BAUNIT_RRR_T_UNIT_F}, count({OP_RIGHT_T_TYPE_F}) as dominios
                        FROM {schema}.{OP_RIGHT_T}
                        WHERE {OP_RIGHT_T_TYPE_F}= (SELECT {T_ID_F} FROM {schema}.{OP_RIGHT_TYPE_D} WHERE {ILICODE_F} = '{OP_RIGHT_TYPE_D_ILICODE_F_OWNERSHIP_V}')
                        GROUP BY {COL_BAUNIT_RRR_T_UNIT_F}
                    ) as conteo
                    WHERE p.{T_ID_F} = conteo.{COL_BAUNIT_RRR_T_UNIT_F} and conteo.dominios > 1""".format(schema=schema,
                                                                                                          OP_RIGHT_TYPE_D=names.OP_RIGHT_TYPE_D,
                                                                                                          ILICODE_F=names.ILICODE_F,
                                                                                                          OP_RIGHT_TYPE_D_ILICODE_F_OWNERSHIP_V=names.OP_RIGHT_TYPE_D_ILICODE_F_OWNERSHIP_V,
                                                                                                          T_ID_F=names.T_ID_F,
                                                                                                          OP_RIGHT_T=names.OP_RIGHT_T,
                                                                                                          OP_RIGHT_T_TYPE_F=names.OP_RIGHT_T_TYPE_F,
                                                                                                          COL_BAUNIT_RRR_T_UNIT_F=names.COL_BAUNIT_RRR_T_UNIT_F,
                                                                                                          table=names.OP_PARCEL_T),
                'desc_error': 'Get parcels with duplicate rights',
                'table_name': QCoreApplication.translate("LogicChecksConfigStrings",
                                                         "Parcels with repeated domain right"),
                'table': names.OP_PARCEL_T}
        }