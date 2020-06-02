def get_custom_filter_plots(names, schema, plot_t_ids):
    custom_filter_plots = ''  # Do not apply filter if no ids exist
    if plot_t_ids and plot_t_ids != 'NULL':
        custom_filter_plots = """SELECT {T_ID_F} AS {COL_UE_BAUNIT_T_LC_PLOT_F} FROM {schema}.{LC_PLOT_T} WHERE {T_ID_F} IN ({plot_t_ids})
        UNION""".format(schema=schema,
                        T_ID_F=names.T_ID_F,
                        LC_PLOT_T=names.LC_PLOT_T,
                        COL_UE_BAUNIT_T_LC_PLOT_F=names.COL_UE_BAUNIT_T_LC_PLOT_F,
                        plot_t_ids=','.join([str(plot_t_id) for plot_t_id in plot_t_ids]))
    return custom_filter_plots


def get_custom_filter_parcels(names, schema, plot_t_ids):
    custom_filter_parcels = ''  # Do not apply filter if no ids exist
    if plot_t_ids and plot_t_ids != 'NULL':
        custom_filter_parcels += """SELECT {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_PARCEL_F} AS {T_ID_F} FROM {schema}.{COL_UE_BAUNIT_T} WHERE {COL_UE_BAUNIT_T}.{COL_UE_BAUNIT_T_LC_PLOT_F} IN ({plot_t_ids})
        UNION""".format(schema=schema,
                        T_ID_F=names.T_ID_F,
                        COL_UE_BAUNIT_T=names.COL_UE_BAUNIT_T,
                        COL_UE_BAUNIT_T_PARCEL_F=names.COL_UE_BAUNIT_T_PARCEL_F,
                        COL_UE_BAUNIT_T_LC_PLOT_F=names.COL_UE_BAUNIT_T_LC_PLOT_F,
                        plot_t_ids=','.join([str(plot_t_id) for plot_t_id in plot_t_ids]))
    return custom_filter_parcels
