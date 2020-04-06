def get_custom_filter_plots(schema, plot_t_ids):
    custom_filter_plots = ''  # Do not apply filter if no ids exist
    if plot_t_ids and plot_t_ids != 'NULL':
        custom_filter_plots = """SELECT t_id AS ue_op_terreno from {schema}.op_terreno WHERE t_id in ({plot_t_ids})  
        UNION""".format(schema=schema, plot_t_ids=','.join([str(plot_t_id) for plot_t_id in plot_t_ids]))
    return custom_filter_plots


def get_custom_filter_parcels(schema, plot_t_ids):
    custom_filter_parcels = ''  # Do not apply filter if no ids exist
    if plot_t_ids and plot_t_ids != 'NULL':
        custom_filter_parcels += """SELECT col_uebaunit.baunit as t_id FROM {schema}.col_uebaunit WHERE col_uebaunit.ue_op_terreno IN ({plot_t_ids}) 
        UNION""".format(schema=schema, plot_t_ids=','.join([str(plot_t_id) for plot_t_id in plot_t_ids]))
    return custom_filter_parcels
