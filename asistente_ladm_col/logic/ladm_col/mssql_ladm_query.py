from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.logic.ladm_col.qgis_ladm_query import QGISLADMQuery


class MSSQLLADMQuery(QGISLADMQuery):
    def __init__(self):
        super(MSSQLLADMQuery, self).__init__()

    @staticmethod
    def get_parcels_with_invalid_department_code(db):
        query = """SELECT {t_id}, {t_ili_tid}
                   FROM {schema}.{op_parcel_t}
                   WHERE len({op_parcel_t_department_f}) != 2 OR
                         {op_parcel_t_department_f} LIKE '%[^0-9]%'
                 """.format(t_id=db.names.T_ID_F,
                            t_ili_tid=db.names.T_ILI_TID_F,
                            schema=db.schema,
                            op_parcel_t=db.names.OP_PARCEL_T,
                            op_parcel_t_department_f=db.names.OP_PARCEL_T_DEPARTMENT_F)
        return db.execute_sql_query(query)

    @staticmethod
    def get_parcels_with_invalid_municipality_code(db):
        query = """SELECT {t_id}, {t_ili_tid}
                   FROM {schema}.{op_parcel_t}
                   WHERE length({op_parcel_t_municipality_f}) !=3 OR
                         {op_parcel_t_municipality_f} ~ '^[0-9]*$' = FALSE
                """.format(t_id=db.names.T_ID_F,
                           t_ili_tid=db.names.T_ILI_TID_F,
                           schema=db.schema,
                           op_parcel_t=db.names.OP_PARCEL_T,
                           op_parcel_t_municipality_f=db.names.OP_PARCEL_T_MUNICIPALITY_F)
        return db.execute_sql_query(query)

    @staticmethod
    def get_parcels_with_invalid_parcel_number(db):
        query = """SELECT {t_id}, {t_ili_tid}
                   FROM {schema}.{op_parcel_t}
                   WHERE length({op_parcel_t_parcel_number_f}) !=30 OR
                         {op_parcel_t_parcel_number_f} ~ '^[0-9]*$' = FALSE
                """.format(t_id=db.names.T_ID_F,
                           t_ili_tid=db.names.T_ILI_TID_F,
                           schema=db.schema,
                           op_parcel_t=db.names.OP_PARCEL_T,
                           op_parcel_t_parcel_number_f=db.names.OP_PARCEL_T_PARCEL_NUMBER_F)
        return db.execute_sql_query(query)

    @staticmethod
    def get_parcels_with_invalid_previous_parcel_number(db):
        query = """SELECT {t_id}, {t_ili_tid}
                   FROM {schema}.{op_parcel_t}
                   WHERE ({op_parcel_t_previous_parcel_number_f} IS NOT NULL AND (length({op_parcel_t_previous_parcel_number_f}) !=20
                   OR ({op_parcel_t_previous_parcel_number_f} ~ '^[0-9]*$') = FALSE))
                """.format(t_id=db.names.T_ID_F,
                           t_ili_tid=db.names.T_ILI_TID_F,
                           schema=db.schema,
                           op_parcel_t=db.names.OP_PARCEL_T,
                           op_parcel_t_previous_parcel_number_f=db.names.OP_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F)
        return db.execute_sql_query(query)

    @staticmethod
    def get_invalid_col_party_type_natural(db):
        query = """SELECT {t_id}, {t_ili_tid},
                                  CASE WHEN {op_party_t_business_name_f} IS NOT NULL THEN 1 ELSE 0 END AS {op_party_t_business_name_f},
                                  CASE WHEN {op_party_t_surname_1_f} IS NULL OR length(trim({op_party_t_surname_1_f})) > 0 is False THEN 1 ELSE 0 END AS {op_party_t_surname_1_f},
                                  CASE WHEN {op_party_t_first_name_1_f} IS NULL OR length(trim({op_party_t_first_name_1_f})) > 0 is False THEN 1 ELSE 0 END AS {op_party_t_first_name_1_f},
                                  CASE WHEN {op_party_t_document_type_f} = (select {t_id} from {schema}.{op_party_document_type_d} where {ilicode} = '{op_party_document_type_d_ilicode_f_nit_v}') THEN 1 ELSE 0 END AS {op_party_t_document_type_f}
                           FROM {schema}.{op_party_t}
                           WHERE {op_party_t_type_f} = (select {t_id} from {schema}.{op_party_type_d} where {ilicode} = '{op_party_type_d_ilicode_f_natural_party_v}')
                                 AND ({op_party_t_business_name_f} IS NOT NULL OR {op_party_t_surname_1_f} IS NULL OR length(trim({op_party_t_surname_1_f})) > 0 is False
                                 OR {op_party_t_first_name_1_f} IS NULL OR length(trim({op_party_t_first_name_1_f})) > 0 is False
                                 OR {op_party_t_document_type_f} = (select {t_id} from {schema}.{op_party_document_type_d} where {ilicode} = '{op_party_document_type_d_ilicode_f_nit_v}'))
                       """.format(t_id=db.names.T_ID_F,
                                  t_ili_tid=db.names.T_ILI_TID_F,
                                  schema=db.schema,
                                  ilicode=db.names.ILICODE_F,
                                  op_party_t=db.names.OP_PARTY_T,
                                  op_party_t_business_name_f=db.names.OP_PARTY_T_BUSINESS_NAME_F,
                                  op_party_t_surname_1_f=db.names.OP_PARTY_T_SURNAME_1_F,
                                  op_party_t_first_name_1_f=db.names.OP_PARTY_T_FIRST_NAME_1_F,
                                  op_party_t_document_type_f=db.names.OP_PARTY_T_DOCUMENT_TYPE_F,
                                  op_party_t_type_f=db.names.OP_PARTY_T_TYPE_F,
                                  op_party_type_d=db.names.OP_PARTY_TYPE_D,
                                  op_party_document_type_d=db.names.OP_PARTY_DOCUMENT_TYPE_D,
                                  op_party_document_type_d_ilicode_f_nit_v=LADMNames.OP_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V,
                                  op_party_type_d_ilicode_f_natural_party_v=LADMNames.OP_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V)
        return db.execute_sql_query(query)

    @staticmethod
    def get_invalid_col_party_type_no_natural(db):
        query = """SELECT {t_id}, {t_ili_tid},
                                  CASE WHEN {op_party_t_business_name_f} IS NULL OR length(trim({op_party_t_business_name_f})) > 0 is False THEN 1 ELSE 0 END AS {op_party_t_business_name_f},
                                  CASE WHEN {op_party_t_surname_1_f} IS NOT NULL THEN 1 ELSE 0 END AS {op_party_t_surname_1_f},
                                  CASE WHEN {op_party_t_first_name_1_f} IS NOT NULL THEN 1 ELSE 0 END AS {op_party_t_first_name_1_f},
                                  CASE WHEN {op_party_t_document_type_f} NOT IN ((select {t_id} from {schema}.{op_party_document_type_d} where {ilicode} = '{op_party_document_type_d_ilicode_f_nit_v}')) THEN 1 ELSE 0 END AS {op_party_t_document_type_f}
                           FROM {schema}.{op_party_t}
                           WHERE {op_party_t_type_f} = (select {t_id} from {schema}.{op_party_type_d} where {ilicode} = '{op_party_type_d_ilicode_f_not_natural_party_v}')
                           AND ({op_party_t_business_name_f} IS NULL OR length(trim({op_party_t_business_name_f})) > 0 is False OR {op_party_t_surname_1_f} IS NOT NULL OR
                           {op_party_t_first_name_1_f} IS NOT NULL OR
                           {op_party_t_document_type_f} NOT IN ((select {t_id} from {schema}.{op_party_document_type_d} where {ilicode} = '{op_party_document_type_d_ilicode_f_nit_v}')))
                        """.format(t_id=db.names.T_ID_F,
                                   t_ili_tid=db.names.T_ILI_TID_F,
                                   schema=db.schema,
                                   ilicode=db.names.ILICODE_F,
                                   op_party_t=db.names.OP_PARTY_T,
                                   op_party_t_business_name_f=db.names.OP_PARTY_T_BUSINESS_NAME_F,
                                   op_party_t_first_name_1_f=db.names.OP_PARTY_T_FIRST_NAME_1_F,
                                   op_party_t_document_type_f=db.names.OP_PARTY_T_DOCUMENT_TYPE_F,
                                   op_party_t_surname_1_f=db.names.OP_PARTY_T_SURNAME_1_F,
                                   op_party_t_type_f=db.names.OP_PARTY_T_TYPE_F,
                                   op_party_type_d=db.names.OP_PARTY_TYPE_D,
                                   op_party_document_type_d=db.names.OP_PARTY_DOCUMENT_TYPE_D,
                                   op_party_document_type_d_ilicode_f_nit_v=LADMNames.OP_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V,
                                   op_party_type_d_ilicode_f_not_natural_party_v=LADMNames.OP_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V)
        return db.execute_sql_query(query)

    @staticmethod
    def get_uebaunit_parcel(db):
        query = """
            SELECT report.{t_id}, {t_ili_tid}, {ilicode} as {op_parcel_t_parcel_type_f}, sum_t, sum_c, sum_uc  FROM (
                   SELECT *
                   FROM (SELECT {t_id}, {t_ili_tid}, {op_parcel_t_parcel_type_f}, sum(count_terreno) sum_t, sum(count_construccion) sum_c, sum(count_unidadconstruccion) sum_uc
                         FROM (SELECT p.{t_id}, p.{t_ili_tid},
                                      p.{op_parcel_t_parcel_type_f},
                                      (CASE WHEN ue.{col_ue_baunit_t_op_plot_f} IS NOT NULL THEN 1 ELSE 0 END) count_terreno,
                                      (CASE WHEN ue.{col_ue_baunit_t_op_building_f} IS NOT NULL THEN 1 ELSE 0 END) count_construccion,
                                      (CASE WHEN ue.{col_ue_baunit_t_op_building_unit_f} IS NOT NULL THEN 1 ELSE 0 END) count_unidadconstruccion
                               FROM {schema}.{op_parcel_t} p left join {schema}.{col_ue_baunit_t} ue on p.{t_id} = ue.{col_ue_baunit_t_parcel_f}) AS p_ue
                               GROUP BY {t_id}, {t_ili_tid}, {op_parcel_t_parcel_type_f}) AS report
                   WHERE ({op_parcel_t_parcel_type_f} = (select {t_id} from {schema}.{op_condition_parcel_type_d} where {ilicode} = '{parcel_type_no_horizontal_property}')
                         AND (sum_t !=1 OR sum_uc != 0))
                         OR ({op_parcel_t_parcel_type_f} in (select {t_id} from {schema}.{op_condition_parcel_type_d} where {ilicode} in ('{parcel_type_horizontal_property_parent}', '{parcel_type_condominium_parent}', '{parcel_type_cemetery_parent}', '{parcel_type_public_use}', '{parcel_type_condominium_parcel_unit}'))
                         AND (sum_t!=1 OR sum_uc > 0))
                         OR ({op_parcel_t_parcel_type_f} in (select {t_id} from {schema}.{op_condition_parcel_type_d} where {ilicode} in ('{parcel_type_road}', '{parcel_type_cemetery_parcel_unit}'))
                         AND (sum_t !=1 OR sum_uc > 0 OR sum_c > 0))
                         OR ({op_parcel_t_parcel_type_f}= (select {t_id} from {schema}.{op_condition_parcel_type_d} where {ilicode} = '{parcel_type_horizontal_property_parcel_unit}')
                         AND (sum_t !=0 OR sum_c != 0 OR sum_uc = 0 ))
                         OR ({op_parcel_t_parcel_type_f} in (select {t_id} from {schema}.{op_condition_parcel_type_d} where {ilicode} in ('{parcel_type_horizontal_property_mejora}', '{parcel_type_no_horizontal_property_mejora}'))
                         AND (sum_t !=0 OR sum_c != 1 OR sum_uc != 0))
            ) as report join {schema}.{op_condition_parcel_type_d} ON report.{op_parcel_t_parcel_type_f} = {op_condition_parcel_type_d}.{t_id}
                """.format(t_id=db.names.T_ID_F,
                           t_ili_tid=db.names.T_ILI_TID_F,
                           schema=db.schema,
                           ilicode=db.names.ILICODE_F,
                           op_parcel_t=db.names.OP_PARCEL_T,
                           col_ue_baunit_t=db.names.COL_UE_BAUNIT_T,
                           col_ue_baunit_t_op_plot_f=db.names.COL_UE_BAUNIT_T_OP_PLOT_F,
                           col_ue_baunit_t_op_building_f=db.names.COL_UE_BAUNIT_T_OP_BUILDING_F,
                           col_ue_baunit_t_op_building_unit_f=db.names.COL_UE_BAUNIT_T_OP_BUILDING_UNIT_F,
                           op_condition_parcel_type_d=db.names.OP_CONDITION_PARCEL_TYPE_D,
                           op_parcel_t_parcel_type_f=db.names.OP_PARCEL_T_PARCEL_TYPE_F,
                           col_ue_baunit_t_parcel_f=db.names.COL_UE_BAUNIT_T_PARCEL_F,
                           parcel_type_no_horizontal_property=LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY,
                           parcel_type_horizontal_property_parent=LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT,
                           parcel_type_horizontal_property_parcel_unit=LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT,
                           parcel_type_cemetery_parcel_unit=LADMNames.PARCEL_TYPE_CEMETERY_PARCEL_UNIT,
                           parcel_type_cemetery_parent=LADMNames.PARCEL_TYPE_CEMETERY_PARENT,
                           parcel_type_road=LADMNames.PARCEL_TYPE_ROAD,
                           parcel_type_public_use=LADMNames.PARCEL_TYPE_PUBLIC_USE,
                           parcel_type_condominium_parent=LADMNames.PARCEL_TYPE_CONDOMINIUM_PARENT,
                           parcel_type_condominium_parcel_unit=LADMNames.PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT,
                           parcel_type_no_horizontal_property_mejora=LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA,
                           parcel_type_horizontal_property_mejora=LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA)
        return db.execute_sql_query(query)

    @staticmethod
    def get_parcels_with_invalid_parcel_type_and_22_position_number(db):
        query = """
            SELECT report.{t_id}, report.{t_ili_tid}, {ilicode} as {op_parcel_t_parcel_type_f}
            FROM (
                   SELECT {t_id}, {t_ili_tid},
                          {op_parcel_t_parcel_type_f}
                   FROM {schema}.{op_parcel_t}
                   WHERE ({op_parcel_t_parcel_number_f} IS NOT NULL
                          AND (substring({op_parcel_t_parcel_number_f},22,1) != '0'
                          AND {op_parcel_t_parcel_type_f}=(select {t_id} from {schema}.{op_condition_parcel_type_d} where {ilicode} = '{parcel_type_no_horizontal_property}'))
                          OR (substring({op_parcel_t_parcel_number_f},22,1) != '9' AND {op_parcel_t_parcel_type_f} in (select {t_id} from {schema}.{op_condition_parcel_type_d} where {ilicode} in ('{parcel_type_horizontal_property_parent}', '{parcel_type_horizontal_property_parcel_unit}')))
                          OR (substring({op_parcel_t_parcel_number_f},22,1) != '8' AND {op_parcel_t_parcel_type_f} in (select {t_id} from {schema}.{op_condition_parcel_type_d} where {ilicode} in ('{parcel_type_condominium_parent}', '{parcel_type_condominium_parcel_unit}')))
                          OR (substring({op_parcel_t_parcel_number_f},22,1) != '7' AND {op_parcel_t_parcel_type_f} in (select {t_id} from {schema}.{op_condition_parcel_type_d} where {ilicode} in ('{parcel_type_cemetery_parent}', '{parcel_type_cemetery_parcel_unit}')))
                          OR (substring({op_parcel_t_parcel_number_f},22,1) != '5' AND {op_parcel_t_parcel_type_f} in (select {t_id} from {schema}.{op_condition_parcel_type_d} where {ilicode} in ('{parcel_type_horizontal_property_mejora}', '{parcel_type_no_horizontal_property_mejora}')))
                          OR (substring({op_parcel_t_parcel_number_f},22,1) != '4' AND {op_parcel_t_parcel_type_f}=(select {t_id} from {schema}.{op_condition_parcel_type_d} where {ilicode} = '{parcel_type_road}'))
                          OR (substring({op_parcel_t_parcel_number_f},22,1) != '3' AND {op_parcel_t_parcel_type_f}=(select {t_id} from {schema}.{op_condition_parcel_type_d} where {ilicode} = '{parcel_type_public_use}')))
            ) AS report join {schema}.{op_condition_parcel_type_d} on report.{op_parcel_t_parcel_type_f} = {op_condition_parcel_type_d}.{t_id}
                """.format(t_id=db.names.T_ID_F,
                           t_ili_tid=db.names.T_ILI_TID_F,
                           schema=db.schema,
                           ilicode=db.names.ILICODE_F,
                           op_parcel_t=db.names.OP_PARCEL_T,
                           op_condition_parcel_type_d=db.names.OP_CONDITION_PARCEL_TYPE_D,
                           op_parcel_t_parcel_number_f=db.names.OP_PARCEL_T_PARCEL_NUMBER_F,
                           op_parcel_t_parcel_type_f=db.names.OP_PARCEL_T_PARCEL_TYPE_F,
                           parcel_type_no_horizontal_property=LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY,
                           parcel_type_horizontal_property_parent=LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT,
                           parcel_type_horizontal_property_parcel_unit=LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT,
                           parcel_type_cemetery_parcel_unit=LADMNames.PARCEL_TYPE_CEMETERY_PARCEL_UNIT,
                           parcel_type_cemetery_parent=LADMNames.PARCEL_TYPE_CEMETERY_PARENT,
                           parcel_type_road=LADMNames.PARCEL_TYPE_ROAD,
                           parcel_type_public_use=LADMNames.PARCEL_TYPE_PUBLIC_USE,
                           parcel_type_condominium_parent=LADMNames.PARCEL_TYPE_CONDOMINIUM_PARENT,
                           parcel_type_condominium_parcel_unit=LADMNames.PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT,
                           parcel_type_no_horizontal_property_mejora=LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA,
                           parcel_type_horizontal_property_mejora=LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA)
        return db.execute_sql_query(query)

    @staticmethod
    def get_duplicate_records_in_table(db, table_name, fields_to_check):
        query = """
                    SELECT string_agg({t_ili_tid}::text, ',') as duplicate_uuids, COUNT({t_id}) as duplicate_total
                    FROM {schema}.{table_name}
                    GROUP BY {fields}
                    HAVING COUNT({t_id}) > 1
                """.format(t_id=db.names.T_ID_F,
                           t_ili_tid=db.names.T_ILI_TID_F,
                           schema=db.schema,
                           table_name=table_name,
                           fields=','.join(fields_to_check))
        return db.execute_sql_query(query)

    @staticmethod
    def get_group_party_fractions_that_do_not_make_one(db):
        query = """
                    SELECT {members_t_group_party_f} as agrupacion, string_agg({t_id}::text, ',') as miembros, SUM(parte) suma_fracciones  FROM (
                    SELECT {fraction_s_numerator_f}::float/{fraction_s_denominator_f} AS parte, {fraction_s_member_f} FROM {schema}.{fraction_s}
                    ) AS fraccion_parte join {schema}.{members_t} on fraccion_parte.{fraction_s_member_f} = {members_t}.{t_id}
                    GROUP BY {members_t_group_party_f}
                    HAVING SUM(parte) != 1
                """.format(t_id=db.names.T_ID_F,
                           schema=db.schema,
                           members_t=db.names.MEMBERS_T,
                           fraction_s_member_f=db.names.FRACTION_S_MEMBER_F,
                           fraction_s=db.names.FRACTION_S,
                           fraction_s_numerator_f=db.names.FRACTION_S_NUMERATOR_F,
                           fraction_s_denominator_f=db.names.FRACTION_S_DENOMINATOR_F,
                           members_t_group_party_f=db.names.MEMBERS_T_GROUP_PARTY_F)
        return db.execute_sql_query(query)

    @staticmethod
    def get_parcels_with_no_right(db):
        query = """SELECT {t_id}, {t_ili_tid}
                   FROM {schema}.{op_parcel_t}
                   WHERE {t_id} NOT IN (SELECT {col_baunit_rrr_t_unit_f} FROM {schema}.{op_right_t})
                """.format(t_id=db.names.T_ID_F,
                           t_ili_tid=db.names.T_ILI_TID_F,
                           schema=db.schema,
                           op_parcel_t=db.names.OP_PARCEL_T,
                           op_right_t=db.names.OP_RIGHT_T,
                           col_baunit_rrr_t_unit_f=db.names.COL_BAUNIT_RRR_T_UNIT_F)
        return db.execute_sql_query(query)

    @staticmethod
    def get_parcels_with_repeated_domain_right(db):
        query = """SELECT conteo.{col_baunit_rrr_t_unit_f} AS {t_id}, {t_ili_tid}
                   FROM {schema}.{op_parcel_t}, (SELECT {col_baunit_rrr_t_unit_f}, count({op_right_t_type_f}) as dominios
                                                            FROM {schema}.{op_right_t}
                                                            WHERE {op_right_t_type_f} = (SELECT {t_id} FROM {schema}.{op_right_type_d} WHERE {ilicode} = '{op_right_type_d_ilicode_f_ownership_v}')
                                                            GROUP BY {col_baunit_rrr_t_unit_f}) as conteo
                   WHERE {t_id} = conteo.{col_baunit_rrr_t_unit_f} and conteo.dominios > 1
                """.format(t_id=db.names.T_ID_F,
                           t_ili_tid=db.names.T_ILI_TID_F,
                           schema=db.schema,
                           ilicode=db.names.ILICODE_F,
                           op_parcel_t=db.names.OP_PARCEL_T,
                           op_right_t=db.names.OP_RIGHT_T,
                           op_right_type_d=db.names.OP_RIGHT_TYPE_D,
                           col_baunit_rrr_t_unit_f=db.names.COL_BAUNIT_RRR_T_UNIT_F,
                           op_right_t_type_f=db.names.OP_RIGHT_T_TYPE_F,
                           op_right_type_d_ilicode_f_ownership_v=LADMNames.OP_RIGHT_TYPE_D_ILICODE_F_OWNERSHIP_V)
        return db.execute_sql_query(query)
