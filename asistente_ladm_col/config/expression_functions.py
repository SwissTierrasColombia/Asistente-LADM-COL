from qgis.utils import qgsfunction

@qgsfunction(args='auto', group='LADM_COL')
def get_domain_code_from_value(domain_table, value, value_is_ilicode, validate_conn, feature, parent):
    """
    Gets a t_id from a domain value

    domain_table: Either a string (class name in the DB) or a Vector Layer
    value: Domain value to look for
    value_is_ilicode: Whether 'value' is iliCode or not (if not, it's dispName)
    validate_conn: Whether to call test_connection (might be costly in batch) or not
    feature: Not used, but mandatory for QGIS
    parent: Not used, but mandatory for QGIS
    """
    debug = False
    res = None

    from qgis import utils
    if not "asistente_ladm_col" in utils.plugins:
        res = -1 if debug else None
    else:
        plugin = utils.plugins["asistente_ladm_col"]  # Dict of active plugins
        db = plugin.get_db_connection()
        db_ready = db.test_connection()[0] if validate_conn else True
        if db_ready:
            if db.names.T_ID_F is None:
                res = -2 if debug else None
            else:
                res = plugin.ladm_data.get_domain_code_from_value(db, domain_table, value, value_is_ilicode)
        else:
            res = -3 if debug else None

    return res


@qgsfunction(args='auto', group='LADM_COL')
def get_domain_value_from_code(domain_table, code, value_is_ilicode, validate_conn, feature, parent):
    """
    Gets a t_id from a domain value

    domain_table: Either a string (class name in the DB) or a Vector Layer
    code: t_id to search in the domain
    value_is_ilicode: Whether 'value' is iliCode or not (if not, it's dispName)
    validate_conn: Whether to call test_connection (might be costly in batch) or not
    feature: Not used, but mandatory for QGIS
    parent: Not used, but mandatory for QGIS
    """
    debug = False
    res = None

    from qgis import utils
    if not "asistente_ladm_col" in utils.plugins:
        res = -1 if debug else None
    else:
        plugin = utils.plugins["asistente_ladm_col"]  # Dict of active plugins
        db = plugin.get_db_connection()
        db_ready = db.test_connection()[0] if validate_conn else True
        if db_ready:
            if db.names.T_ID_F is None:
                res = -2 if debug else None
            else:
                res = plugin.ladm_data.get_domain_value_from_code(db, domain_table, code, value_is_ilicode)
        else:
            res = -3 if debug else None

    return res
