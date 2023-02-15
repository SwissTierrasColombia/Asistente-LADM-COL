

class PgParcelWithoutAssociatedAddress:

    @staticmethod
    def execute(db):
        # TODO: In order to map the predio_direccion field, the model must be updated.
        # TODO: By the moment it will be used statically
        query = """SELECT {t_id}, {t_ili_tid}
                   FROM {schema}.{fdc_parcel_t}
                   WHERE {t_id} NOT IN (
                        SELECT DISTINCT cca_predio_direccion
                        FROM {schema}.{ext_address_s} WHERE cca_predio_direccion IS NOT NULL)
                 """.format(t_id=db.names.T_ID_F,
                            t_ili_tid=db.names.T_ILI_TID_F,
                            ilicode=db.names.ILICODE_F,
                            schema=db.schema,
                            ext_address_s=db.names.EXT_ADDRESS_S,
                            fdc_parcel_t=db.names.FDC_PARCEL_T)

        return db.execute_sql_query(query)
