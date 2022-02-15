from asistente_ladm_col.config.query_names import QueryNames
from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.logic.ladm_col.qgis_ladm_query import QGISLADMQuery
from asistente_ladm_col.logic.ladm_col.config.queries.pg import (basic_query,
                                                                 economic_query,
                                                                 physical_query,
                                                                 legal_query,
                                                                 property_record_card_query)


class PGLADMQuery(QGISLADMQuery):
    def __init__(self):
        super(PGLADMQuery, self).__init__()

    @staticmethod
    def get_igac_basic_info(db, **kwargs):
        """
        Query by component: Basic info
        :param kwargs: dict with one of the following key-value param
               plot_t_ids
               parcel_fmi
               parcel_number
               previous_parcel_number
        :return:
        """
        params = QGISLADMQuery._get_parameters(kwargs)
        query = basic_query.get_igac_basic_query(names=db.names,
                                                 schema=db.schema,
                                                 plot_t_ids=params[QueryNames.SEARCH_KEY_PLOT_T_IDS],
                                                 parcel_fmi=params[QueryNames.SEARCH_KEY_PARCEL_FMI],
                                                 parcel_number=params[QueryNames.SEARCH_KEY_PARCEL_NUMBER],
                                                 previous_parcel_number=params[QueryNames.SEARCH_KEY_PREVIOUS_PARCEL_NUMBER])
        return PGLADMQuery._get_query_results(db, query)

    @staticmethod
    def get_igac_legal_info(db, **kwargs):
        """
        Query by component: Legal info
        :param kwargs: dict with one of the following key-value param
               plot_t_ids
               parcel_fmi
               parcel_number
               previous_parcel_number
        :return:
        """
        params = QGISLADMQuery._get_parameters(kwargs)
        query = legal_query.get_igac_legal_query(names=db.names,
                                                 schema=db.schema,
                                                 plot_t_ids=params[QueryNames.SEARCH_KEY_PLOT_T_IDS],
                                                 parcel_fmi=params[QueryNames.SEARCH_KEY_PARCEL_FMI],
                                                 parcel_number=params[QueryNames.SEARCH_KEY_PARCEL_NUMBER],
                                                 previous_parcel_number=params[QueryNames.SEARCH_KEY_PREVIOUS_PARCEL_NUMBER])
        return PGLADMQuery._get_query_results(db, query)

    @staticmethod
    def get_igac_property_record_card_info(db, **kwargs):
        """
        Query by component: Legal info
        :param kwargs: dict with one of the following key-value param
               plot_t_ids
               parcel_fmi
               parcel_number
               previous_parcel_number
        :return:
        """
        params = QGISLADMQuery._get_parameters(kwargs)
        query = property_record_card_query.get_igac_property_record_card_query(names=db.names,
                                                                               schema=db.schema,
                                                                               plot_t_ids=params[QueryNames.SEARCH_KEY_PLOT_T_IDS],
                                                                               parcel_fmi=params[QueryNames.SEARCH_KEY_PARCEL_FMI],
                                                                               parcel_number=params[QueryNames.SEARCH_KEY_PARCEL_NUMBER],
                                                                               previous_parcel_number=params[QueryNames.SEARCH_KEY_PREVIOUS_PARCEL_NUMBER])
        return PGLADMQuery._get_query_results(db, query)

    @staticmethod
    def get_igac_physical_info(db, **kwargs):
        """
        Query by component: Physical info
        :param kwargs: dict with one of the following key-value param
               plot_t_ids
               parcel_fmi
               parcel_number
               previous_parcel_number
        :return:
        """
        params = QGISLADMQuery._get_parameters(kwargs)
        query = physical_query.get_igac_physical_query(names=db.names,
                                                       schema=db.schema,
                                                       plot_t_ids=params[QueryNames.SEARCH_KEY_PLOT_T_IDS],
                                                       parcel_fmi=params[QueryNames.SEARCH_KEY_PARCEL_FMI],
                                                       parcel_number=params[QueryNames.SEARCH_KEY_PARCEL_NUMBER],
                                                       previous_parcel_number=params[QueryNames.SEARCH_KEY_PREVIOUS_PARCEL_NUMBER])
        return PGLADMQuery._get_query_results(db, query)

    @staticmethod
    def get_igac_economic_info(db, **kwargs):
        """
        Query by component: Economic info
        :param kwargs: dict with one of the following key-value param
               plot_t_ids
               parcel_fmi
               parcel_number
               previous_parcel_number
        :return:
        """
        params = QGISLADMQuery._get_parameters(kwargs)
        query = economic_query.get_igac_economic_query(names=db.names,
                                                       schema=db.schema,
                                                       plot_t_ids=params[QueryNames.SEARCH_KEY_PLOT_T_IDS],
                                                       parcel_fmi=params[QueryNames.SEARCH_KEY_PARCEL_FMI],
                                                       parcel_number=params[QueryNames.SEARCH_KEY_PARCEL_NUMBER],
                                                       previous_parcel_number=params[QueryNames.SEARCH_KEY_PREVIOUS_PARCEL_NUMBER])
        return PGLADMQuery._get_query_results(db, query)

    @staticmethod
    def _get_query_results(db, query):
        res, msg = db.check_and_fix_connection()
        if not res:
            return None
        cur = db.conn.cursor()
        cur.execute(query)
        query_result = cur.fetchone()[0]

        # self.logger.debug(__name__, "QUERY:".format(query))
        return query_result

    @staticmethod
    def get_parcels_with_invalid_department_code(db):
        query = """SELECT {t_id}, {t_ili_tid}
                   FROM {schema}.{lc_parcel_t}
                   WHERE length({lc_parcel_t_department_f}) !=2 OR
                         {lc_parcel_t_department_f} ~ '^[0-9]*$' = FALSE
                 """.format(t_id=db.names.T_ID_F,
                            t_ili_tid=db.names.T_ILI_TID_F,
                            schema=db.schema,
                            lc_parcel_t=db.names.LC_PARCEL_T,
                            lc_parcel_t_department_f=db.names.LC_PARCEL_T_DEPARTMENT_F)
        return db.execute_sql_query(query)

    @staticmethod
    def get_parcels_with_invalid_municipality_code(db):
        query = """SELECT {t_id}, {t_ili_tid}
                   FROM {schema}.{lc_parcel_t}
                   WHERE length({lc_parcel_t_municipality_f}) !=3 OR
                         {lc_parcel_t_municipality_f} ~ '^[0-9]*$' = FALSE
                """.format(t_id=db.names.T_ID_F,
                           t_ili_tid=db.names.T_ILI_TID_F,
                           schema=db.schema,
                           lc_parcel_t=db.names.LC_PARCEL_T,
                           lc_parcel_t_municipality_f=db.names.LC_PARCEL_T_MUNICIPALITY_F)
        return db.execute_sql_query(query)

    @staticmethod
    def get_parcels_with_invalid_parcel_number(db):
        query = """SELECT {t_id}, {t_ili_tid}
                   FROM {schema}.{lc_parcel_t}
                   WHERE length({lc_parcel_t_parcel_number_f}) !=30 OR
                         {lc_parcel_t_parcel_number_f} ~ '^[0-9]*$' = FALSE
                """.format(t_id=db.names.T_ID_F,
                           t_ili_tid=db.names.T_ILI_TID_F,
                           schema=db.schema,
                           lc_parcel_t=db.names.LC_PARCEL_T,
                           lc_parcel_t_parcel_number_f=db.names.LC_PARCEL_T_PARCEL_NUMBER_F)
        return db.execute_sql_query(query)

    @staticmethod
    def get_parcels_with_invalid_previous_parcel_number(db):
        query = """SELECT {t_id}, {t_ili_tid}
                   FROM {schema}.{lc_parcel_t}
                   WHERE ({lc_parcel_t_previous_parcel_number_f} IS NOT NULL AND (length({lc_parcel_t_previous_parcel_number_f}) !=20
                   OR ({lc_parcel_t_previous_parcel_number_f} ~ '^[0-9]*$') = FALSE))
                """.format(t_id=db.names.T_ID_F,
                           t_ili_tid=db.names.T_ILI_TID_F,
                           schema=db.schema,
                           lc_parcel_t=db.names.LC_PARCEL_T,
                           lc_parcel_t_previous_parcel_number_f=db.names.LC_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F)
        return db.execute_sql_query(query)

    @staticmethod
    def get_invalid_col_party_type_natural(db):
        query = """SELECT {t_id}, {t_ili_tid},
                          CASE WHEN {lc_party_t_business_name_f} IS NOT NULL THEN 1 ELSE 0 END AS {lc_party_t_business_name_f},
                          CASE WHEN {lc_party_t_surname_1_f} IS NULL OR length(trim({lc_party_t_surname_1_f})) > 0 is False THEN 1 ELSE 0 END AS {lc_party_t_surname_1_f},
                          CASE WHEN {lc_party_t_first_name_1_f} IS NULL OR length(trim({lc_party_t_first_name_1_f})) > 0 is False THEN 1 ELSE 0 END AS {lc_party_t_first_name_1_f},
                          CASE WHEN {lc_party_t_document_type_f} = (select {t_id} from {schema}.{lc_party_document_type_d} where {ilicode} = '{lc_party_document_type_d_ilicode_f_nit_v}') THEN 1 ELSE 0 END AS {lc_party_t_document_type_f}
                   FROM {schema}.{lc_party_t}
                   WHERE {lc_party_t_type_f} = (select {t_id} from {schema}.{lc_party_type_d} where {ilicode} = '{lc_party_type_d_ilicode_f_natural_party_v}')
                         AND ({lc_party_t_business_name_f} IS NOT NULL OR {lc_party_t_surname_1_f} IS NULL OR length(trim({lc_party_t_surname_1_f})) > 0 is False
                         OR {lc_party_t_first_name_1_f} IS NULL OR length(trim({lc_party_t_first_name_1_f})) > 0 is False
                         OR {lc_party_t_document_type_f} = (select {t_id} from {schema}.{lc_party_document_type_d} where {ilicode} = '{lc_party_document_type_d_ilicode_f_nit_v}'))
               """.format(t_id=db.names.T_ID_F,
                          t_ili_tid=db.names.T_ILI_TID_F,
                          schema=db.schema,
                          ilicode=db.names.ILICODE_F,
                          lc_party_t=db.names.LC_PARTY_T,
                          lc_party_t_business_name_f=db.names.LC_PARTY_T_BUSINESS_NAME_F,
                          lc_party_t_surname_1_f=db.names.LC_PARTY_T_SURNAME_1_F,
                          lc_party_t_first_name_1_f=db.names.LC_PARTY_T_FIRST_NAME_1_F,
                          lc_party_t_document_type_f=db.names.LC_PARTY_T_DOCUMENT_TYPE_F,
                          lc_party_t_type_f=db.names.LC_PARTY_T_TYPE_F,
                          lc_party_type_d=db.names.LC_PARTY_TYPE_D,
                          lc_party_document_type_d=db.names.LC_PARTY_DOCUMENT_TYPE_D,
                          lc_party_document_type_d_ilicode_f_nit_v=LADMNames.LC_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V,
                          lc_party_type_d_ilicode_f_natural_party_v=LADMNames.LC_PARTY_TYPE_D_ILICODE_F_NATURAL_PARTY_V)
        return db.execute_sql_query(query)

    @staticmethod
    def get_invalid_col_party_type_no_natural(db):
        query = """SELECT {t_id}, {t_ili_tid},
                          CASE WHEN {lc_party_t_business_name_f} IS NULL OR length(trim({lc_party_t_business_name_f})) > 0 is False THEN 1 ELSE 0 END AS {lc_party_t_business_name_f},
                          CASE WHEN {lc_party_t_surname_1_f} IS NOT NULL THEN 1 ELSE 0 END AS {lc_party_t_surname_1_f},
                          CASE WHEN {lc_party_t_first_name_1_f} IS NOT NULL THEN 1 ELSE 0 END AS {lc_party_t_first_name_1_f},
                          CASE WHEN {lc_party_t_document_type_f} NOT IN ((select {t_id} from {schema}.{lc_party_document_type_d} where {ilicode} = '{lc_party_document_type_d_ilicode_f_nit_v}')) THEN 1 ELSE 0 END AS {lc_party_t_document_type_f}
                   FROM {schema}.{lc_party_t}
                   WHERE {lc_party_t_type_f} = (select {t_id} from {schema}.{lc_party_type_d} where {ilicode} = '{lc_party_type_d_ilicode_f_not_natural_party_v}')
                   AND ({lc_party_t_business_name_f} IS NULL OR length(trim({lc_party_t_business_name_f})) > 0 is False OR {lc_party_t_surname_1_f} IS NOT NULL OR
                   {lc_party_t_first_name_1_f} IS NOT NULL OR
                   {lc_party_t_document_type_f} NOT IN ((select {t_id} from {schema}.{lc_party_document_type_d} where {ilicode} = '{lc_party_document_type_d_ilicode_f_nit_v}')))
                """.format(t_id=db.names.T_ID_F,
                           t_ili_tid=db.names.T_ILI_TID_F,
                           schema=db.schema,
                           ilicode=db.names.ILICODE_F,
                           lc_party_t=db.names.LC_PARTY_T,
                           lc_party_t_business_name_f=db.names.LC_PARTY_T_BUSINESS_NAME_F,
                           lc_party_t_first_name_1_f=db.names.LC_PARTY_T_FIRST_NAME_1_F,
                           lc_party_t_document_type_f=db.names.LC_PARTY_T_DOCUMENT_TYPE_F,
                           lc_party_t_surname_1_f=db.names.LC_PARTY_T_SURNAME_1_F,
                           lc_party_t_type_f=db.names.LC_PARTY_T_TYPE_F,
                           lc_party_type_d=db.names.LC_PARTY_TYPE_D,
                           lc_party_document_type_d=db.names.LC_PARTY_DOCUMENT_TYPE_D,
                           lc_party_document_type_d_ilicode_f_nit_v=LADMNames.LC_PARTY_DOCUMENT_TYPE_D_ILICODE_F_NIT_V,
                           lc_party_type_d_ilicode_f_not_natural_party_v=LADMNames.LC_PARTY_TYPE_D_ILICODE_F_NOT_NATURAL_PARTY_V)
        return db.execute_sql_query(query)

    @staticmethod
    def get_uebaunit_parcel(db):
        query = """
            select report.{t_id}, report.{t_ili_tid}, {ilicode} as {lc_parcel_t_parcel_type_f}, sum_t, sum_c, sum_uc
            from (select p.{t_id}, p.{t_ili_tid}, {lc_parcel_t_parcel_type_f}, count({col_ue_baunit_t_lc_plot_f}) sum_t,
                        count({col_ue_baunit_t_lc_building_f}) sum_c, count({col_ue_baunit_t_lc_building_unit_f}) sum_uc
                    from {schema}.{lc_parcel_t} p
                    left join {schema}.{col_ue_baunit_t} ue on p.{t_id} = ue.{col_ue_baunit_t_parcel_f}
                    group by p.{t_id}) as report
            join {schema}.{lc_condition_parcel_type_d} cp on report.{lc_parcel_t_parcel_type_f} = cp.{t_id}
            where
                ({ilicode} in ('{parcel_type_no_horizontal_property}', '{parcel_type_public_use}')
                    and sum_t != 1)
                or ({ilicode} in ('{parcel_type_horizontal_property_parent}', '{parcel_type_condominium_parent}', '{parcel_type_cemetery_parent}', '{parcel_type_condominium_parcel_unit}')
                    and (sum_t != 1 or sum_uc > 0))
                or ({ilicode} in ('{parcel_type_road}', '{parcel_type_cemetery_parcel_unit}')
                    and (sum_t != 1 or sum_uc > 0 or sum_c > 0))
                or ({ilicode} = '{parcel_type_horizontal_property_parcel_unit}'
                    and (sum_t > 0 or sum_c > 0 or sum_uc = 0 ))
                or ({ilicode} in ('{parcel_type_horizontal_property_mejora}', '{parcel_type_no_horizontal_property_mejora}')
                    and (sum_t > 0 or sum_c != 1 or sum_uc > 0));
                """.format(t_id=db.names.T_ID_F,
                           t_ili_tid=db.names.T_ILI_TID_F,
                           schema=db.schema,
                           ilicode=db.names.ILICODE_F,
                           lc_parcel_t=db.names.LC_PARCEL_T,
                           col_ue_baunit_t=db.names.COL_UE_BAUNIT_T,
                           col_ue_baunit_t_lc_plot_f=db.names.COL_UE_BAUNIT_T_LC_PLOT_F,
                           col_ue_baunit_t_lc_building_f=db.names.COL_UE_BAUNIT_T_LC_BUILDING_F,
                           col_ue_baunit_t_lc_building_unit_f=db.names.COL_UE_BAUNIT_T_LC_BUILDING_UNIT_F,
                           lc_condition_parcel_type_d=db.names.LC_CONDITION_PARCEL_TYPE_D,
                           lc_parcel_t_parcel_type_f=db.names.LC_PARCEL_T_PARCEL_TYPE_F,
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
            with parcels
            as (
                select p.{t_id}, p.{t_ili_tid}, {ilicode}, substring({lc_parcel_t_parcel_number_f},22,1) as pos22
                from {schema}.{lc_parcel_t} p
                join {schema}.{lc_condition_parcel_type_d} cpt on {lc_parcel_t_parcel_type_f} = cpt.{t_id}
            )
            select {t_id}, {t_ili_tid}, {ilicode} as {lc_parcel_t_parcel_type_f}
            from parcels
            where pos22 is null
                or (pos22 != '0' and {ilicode} = '{parcel_type_no_horizontal_property}')
                or (pos22 != '9' and {ilicode} in ('{parcel_type_horizontal_property_parent}', '{parcel_type_horizontal_property_parcel_unit}'))
                or (pos22 != '8' and {ilicode} in ('{parcel_type_condominium_parent}', '{parcel_type_condominium_parcel_unit}'))
                or (pos22 != '7' and {ilicode} in ('{parcel_type_cemetery_parent}', '{parcel_type_cemetery_parcel_unit}'))
                or (pos22 != '5' and {ilicode} in ('{parcel_type_horizontal_property_mejora}', '{parcel_type_no_horizontal_property_mejora}'))
                or (pos22 != '4' and {ilicode} = '{parcel_type_road}')
                or (pos22 != '3' and {ilicode} = '{parcel_type_public_use}');
                """.format(t_id=db.names.T_ID_F,
                           t_ili_tid=db.names.T_ILI_TID_F,
                           schema=db.schema,
                           ilicode=db.names.ILICODE_F,
                           lc_parcel_t=db.names.LC_PARCEL_T,
                           lc_condition_parcel_type_d=db.names.LC_CONDITION_PARCEL_TYPE_D,
                           lc_parcel_t_parcel_number_f=db.names.LC_PARCEL_T_PARCEL_NUMBER_F,
                           lc_parcel_t_parcel_type_f=db.names.LC_PARCEL_T_PARCEL_TYPE_F,
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
                   FROM {schema}.{lc_parcel_t}
                   WHERE {t_id} NOT IN (SELECT {col_baunit_rrr_t_unit_f} FROM {schema}.{lc_right_t})
                """.format(t_id=db.names.T_ID_F,
                           t_ili_tid=db.names.T_ILI_TID_F,
                           schema=db.schema,
                           lc_parcel_t=db.names.LC_PARCEL_T,
                           lc_right_t=db.names.LC_RIGHT_T,
                           col_baunit_rrr_t_unit_f=db.names.COL_BAUNIT_RRR_T_UNIT_F)
        return db.execute_sql_query(query)

    @staticmethod
    def get_parcels_with_repeated_domain_right(db):
        query = """SELECT {t_ili_tid}, conteo.dominios
                   FROM {schema}.{lc_parcel_t}, (SELECT {col_baunit_rrr_t_unit_f},
                                                        count({lc_right_t_type_f}) as conteo,
                                                        string_agg(cast({t_ili_tid} as text), ';') as dominios
                                                            FROM {schema}.{lc_right_t}
                                                            WHERE {lc_right_t_type_f} = (SELECT {t_id} FROM {schema}.{lc_right_type_d} WHERE {ilicode} = '{lc_right_type_d_ilicode_f_ownership_v}')
                                                            GROUP BY {col_baunit_rrr_t_unit_f}) as conteo
                   WHERE {t_id} = conteo.{col_baunit_rrr_t_unit_f} and conteo.conteo > 1
                """.format(t_id=db.names.T_ID_F,
                           t_ili_tid=db.names.T_ILI_TID_F,
                           schema=db.schema,
                           ilicode=db.names.ILICODE_F,
                           lc_parcel_t=db.names.LC_PARCEL_T,
                           lc_right_t=db.names.LC_RIGHT_T,
                           lc_right_type_d=db.names.LC_RIGHT_TYPE_D,
                           col_baunit_rrr_t_unit_f=db.names.COL_BAUNIT_RRR_T_UNIT_F,
                           lc_right_t_type_f=db.names.LC_RIGHT_T_TYPE_F,
                           lc_right_type_d_ilicode_f_ownership_v=LADMNames.LC_RIGHT_TYPE_D_ILICODE_F_OWNERSHIP_V)
        return db.execute_sql_query(query)
