from qgis.utils import qgsfunction
from qgis.core import (QgsExpression,
                       QgsFeatureRequest,
                       QgsFeature)

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
    try:
        from asistente_ladm_col.config.table_mapping_config import Names
    except:
        return -1 if debug else None

    from qgis import utils
    if not "asistente_ladm_col" in utils.plugins:
        return -2 if debug else None
    plugin = utils.plugins["asistente_ladm_col"]
    db = plugin.get_db_connection()
    res = db.test_connection()[0] if validate_conn else True
    db.get_table_and_field_names()
    names = Names()
    if names.T_ID_F is None:
        return -3 if debug else None

    if res:
        if type(domain_table) is str:
            domain_table = plugin.qgis_utils.get_layer(db, domain_table, None, True, emit_map_freeze=False)
            if domain_table is None:
                return -4 if debug else None

        expression = "\"{}\" = '{}'".format(names.ILICODE_F if value_is_ilicode else names.DISPLAY_NAME_F, value)
        request = QgsFeatureRequest(QgsExpression(expression))
        request.setSubsetOfAttributes([names.T_ID_F], domain_table.fields())

        features = domain_table.getFeatures(request)
        feature = QgsFeature()
        if features.nextFeature(feature):
            return feature[names.T_ID_F]

    return -5 if debug else None
