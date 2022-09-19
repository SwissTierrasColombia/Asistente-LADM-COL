from qgis.utils import qgsfunction

from asistente_ladm_col.config.translation_strings import TranslatableConfigStrings


@qgsfunction(args='auto', group='LADM-COL', referenced_columns=[], helpText=TranslatableConfigStrings.help_get_domain_code_from_value)
def get_domain_code_from_value(domain_table, value, value_is_ilicode, validate_conn, feature, parent):
    """
    Gets a t_id from a domain value

    : param domain_table: Either a string (class name in the DB) or a Vector Layer
    : param value: Domain value to look for
    : param value_is_ilicode: Whether 'value' is iliCode or not (if not, it's dispName)
    : param validate_conn: Whether to call test_connection (might be costly in batch) or not
    : param feature: Not used, but mandatory for QGIS
    : param parent: Not used, but mandatory for QGIS
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


@qgsfunction(args='auto', group='LADM-COL', referenced_columns=[])
def get_domain_value_from_code(domain_table, code, value_is_ilicode, validate_conn, feature, parent):
    """
    Gets a domain value from its t_id

    : param domain_table: Either a string (class name in the DB) or a Vector Layer
    : param code: t_id to search in the domain
    : param value_is_ilicode: Whether 'value' is iliCode or not (if not, it's dispName)
    : param validate_conn: Whether to call test_connection (might be costly in batch) or not
    : param feature: Not used, but mandatory for QGIS
    : param parent: Not used, but mandatory for QGIS
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

@qgsfunction(args='auto', group='LADM-COL', referenced_columns=[])
def get_domain_value_from_code_db(db_source, domain_table, code, value_is_ilicode, validate_conn, feature, parent):
    """
    Gets a domain value from its t_id

    : param db_source: Define if db connection is 'COLLECTED', 'SUPPLIES'
    : param domain_table: Either a string (class name in the DB) or a Vector Layer
    : param code: t_id to search in the domain
    : param value_is_ilicode: Whether 'value' is iliCode or not (if not, it's dispName)
    : param validate_conn: Whether to call test_connection (might be costly in batch) or not
    : param feature: Not used, but mandatory for QGIS
    : param parent: Not used, but mandatory for QGIS
    """
    debug = False
    res = None

    from qgis import utils
    if not "asistente_ladm_col" in utils.plugins:
        res = -1 if debug else None
    else:
        plugin = utils.plugins["asistente_ladm_col"]  # Dict of active plugins
        db = plugin.get_db_connection(db_source)
        db_ready = db.test_connection()[0] if validate_conn else True
        if db_ready:
            if db.names.T_ID_F is None:
                res = -2 if debug else None
            else:
                res = plugin.ladm_data.get_domain_value_from_code(db, domain_table, code, value_is_ilicode)
        else:
            res = -3 if debug else None

    return res

@qgsfunction(args='auto', group='LADM-COL', referenced_columns=[], helpText=TranslatableConfigStrings.help_get_multi_domain_code_from_value)
def get_multi_domain_code_from_value(domain_table, value, child_domain_table, feature, parent):
    """
    Gets a t_id from both a domain ilicode and a child domain class name.
    When a DB has more than 1 child domain, the ilicode may be duplicated,
    so we need the child_domain_table name to disambiguate.

    : param domain_table: Either a string (class name in the DB) or a Vector Layer
    : param value: Domain value (ilicode) to look for
    : param child_domain_table: Name of the child domain table
    : param feature: Not used, but mandatory for QGIS
    : param parent: Not used, but mandatory for QGIS
    """
    debug = False
    res = None

    from qgis import utils
    if not "asistente_ladm_col" in utils.plugins:
        res = -1 if debug else None
    else:
        plugin = utils.plugins["asistente_ladm_col"]  # Dict of active plugins
        db = plugin.get_db_connection()
        if db.names.T_ID_F is None:
            db.names.test_connection()  # First build the DBMappingRegistry object

        res = plugin.ladm_data.get_domain_code_from_value(db, domain_table, value, True, child_domain_table)

    return res


@qgsfunction(args='auto', group='LADM-COL', referenced_columns=[])
def get_informal_plots(feature, parent):
    """
    Get all plot t_ids whose associated parcels are informal
    (i.e., have an occupation/possession right type)
    """
    debug = False
    res = None

    from qgis import utils
    if not "asistente_ladm_col" in utils.plugins:
        res = -1 if debug else None
    else:
        plugin = utils.plugins["asistente_ladm_col"]  # Dict of active plugins
        db = plugin.get_db_connection()

        if db.names.T_ID_F is None:
            res = -2 if debug else None
        else:
            res = plugin.ladm_data.get_informal_plot_tids(db)

    return res


@qgsfunction(args='auto', group='LADM-COL', referenced_columns=[])
def get_informal_buildings(feature, parent):
    """
    Get all building t_ids whose associated parcels are informal
    (i.e., have an occupation/possession right type)
    """
    debug = False
    res = None

    from qgis import utils
    if not "asistente_ladm_col" in utils.plugins:
        res = -1 if debug else None
    else:
        plugin = utils.plugins["asistente_ladm_col"]  # Dict of active plugins
        db = plugin.get_db_connection()

        if db.names.T_ID_F is None:
            res = -2 if debug else None
        else:
            res = plugin.ladm_data.get_informal_building_tids(db)

    return res


@qgsfunction(args='auto', group='LADM-COL', referenced_columns=[])
def get_informal_building_units(feature, parent):
    """
    Get all building unit t_ids whose associated parcels are informal
    (i.e., have an occupation/possession right type)
    """
    debug = False
    res = None

    from qgis import utils
    if not "asistente_ladm_col" in utils.plugins:
        res = -1 if debug else None
    else:
        plugin = utils.plugins["asistente_ladm_col"]  # Dict of active plugins
        db = plugin.get_db_connection()

        if db.names.T_ID_F is None:
            res = -2 if debug else None
        else:
            res = plugin.ladm_data.get_informal_building_unit_tids(db)

    return res


@qgsfunction(args='auto', group='LADM-COL', referenced_columns=[], helpText=TranslatableConfigStrings.help_get_default_basket)
def get_default_basket(feature, parent):
    """
    Gets the t_id from the default basket in the DB. If it does not exist,
    it first creates the default basket and returns the newly created t_id.

    :param feature: Not used, but mandatory for QGIS
    :param parent: Not used, but mandatory for QGIS
    """
    debug = False
    res = None

    from qgis import utils
    if not "asistente_ladm_col" in utils.plugins:
        res = -1 if debug else None
    else:
        plugin = utils.plugins["asistente_ladm_col"]  # Dict of active plugins
        db = plugin.get_db_connection()
        if db.names.T_ID_F is None:
            db.names.test_connection()  # First build the DBMappingRegistry object

        res = plugin.ladm_data.get_default_basket_id(db)

    return res


@qgsfunction(args='auto', group='LADM-COL')
def get_domain_description_from_code(value, table, feature, parent):
    """
    Gets a description from a domain value

    value: Domain value to look for
    table: Dict to look for. Options = (construction, destinacion)
    feature: Not used, but mandatory for QGIS
    parent: Not used, but mandatory for QGIS
    """    
    construction_uses = {'1':'Vivienda hasta 3 pisos',
    '2':'Ramadas - Cobertizos - Caneyes',
    '3':'Galpones - Gallineros',
    '4':'Establos - Pesebreras - Caballerizas',
    '5':'Cocheras - Marraneras - Porquerizas',
    '6':'Bodega Casa Bomba',
    '7':'Industrias',
    '8':'Silos',
    '9':'Piscinas',
    '10':'Tanques',
    '11':'Beneficiaderos',
    '12':'Colegio y Universidades',
    '13':'Biblioteca',
    '14':'Garajes Cubiertos',
    '16':'Bodegas Comerciales - Grandes Almacenes',
    '18':'Secaderos',
    '19':'Clinicas - Hospitales - Centros Medicos',
    '20':'Pozos',
    '21':'Kioscos',
    '23':'Albercas - Banaderas',
    '25':'Hoteles en PH',
    '26':'Corrales',
    '27':'Casa Elbas',
    '28':'Comercio',
    '29':'Iglesia',
    '31':'Hoteles',
    '33':'Clubes - Casinos',
    '34':'Oficinas - Consultorios',
    '35':'Apartamentos mas de 4 Pisos',
    '36':'Restaurantes',
    '37':'Pensiones y Residencias',
    '38':'Puestos de Salud',
    '39':'Parqueaderos',
    '40':'Barracas',
    '41':'Teatro - Cinemas',
    '42':'Aulas de Clases',
    '43':'Coliseos',
    '44':'Casas de Culto',
    '45':'Talleres',
    '46':'Jardin Infantil en Casa',
    '47':'Torres de Enfriamiento',
    '48':'Muelles',
    '49':'Estacion de Bombeo',
    '50':'Estadios - Plaza de Toros',
    '51':'Carceles',
    '52':'Parque Cementerios',
    '53':'Vivienda Colonial',
    '54':'Comercio Colonial',
    '55':'Oficinas - Consultorios Coloniales',
    '56':'Apartamentos en Edificio de 4 y 5 Pisos (Cartagena)',
    '58':'Centros Comerciales',
    '60':'Canchas de Tenis',
    '62':'Toboganes',
    '63':'Vivienda Recreacional',
    '64':'Camaroneras',
    '65':'Fuertes y Castillos',
    '66':'Murallas',
    '70':'Vivienda hasta 3 pisos en PH',
    '71':'Apartamentos 4 y m?s pisos en PH',
    '72':'Vivienda Recreacional en PH',
    '73':'Bodegas Casa Bomba en PH',
    '74':'Bodegas Comerciales en PH',
    '75':'Comercio en PH',
    '76':'Centros Comerciales en PH',
    '77':'Oficinas Consultorios en PH',
    '78':'Parqueaderos en PH',
    '79':'Garajes en PH',
    '80':'Industrias en PH',
    '82':'Marquesinas - Patios Cubiertos',
    '83':'Lagunas de Oxidacion',
    '84':'Vía Ferrea',
    '85':'Carretera',
    '86':'Teatro - Cinemas en PH',
    '87':'Iglesia en PH',
    '88':'Restaurantes en PH',
    '89':'Hotel Colonial',
    '90':'Restaurante Colonial',
    '91':'Entidad Educativa Colonial - Colegio Colonial',
    '99':'Cimientos, Estructura, Muros y Placa Base'}
    
    economic_destination = {'A':'Habitacional',
    'B':'Industrial',
    'C':'Comercial',
    'D':'Agropecuario',
    'E':'Minero',
    'F':'Cultural',
    'G':'Recreacional',
    'H':'Salubridad',
    'I':'Institucional',
    'J':'Educativo',
    'K':'Religioso',
    'L':'Agricola',
    'M':'Pecuario',
    'N':'Agroindustrial',
    'O':'Forestal',
    'P':'Uso Público',
    'Q':'Servicios Especiales',
    'R':'Lote urbanizable no urbanizado',
    'S':'Lote urbanizado no construido o edificado',
    'T':'Lote No Urbanizable',
    '0':'No especificado'}

    domain_dict = {}

    if table == 'construction':
        domain_dict = construction_uses
    elif table == 'destinacion':
        domain_dict = economic_destination
        
    if value in domain_dict:
        return domain_dict['{}'.format(value)]

    return None
