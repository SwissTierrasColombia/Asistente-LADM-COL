def get_full_alias(base_alias, units, table, field):
    full_alias = base_alias
    alias_unit = get_ladm_unit(units, table, field)
    if alias_unit:
        full_alias = '{} {}'.format(base_alias,  alias_unit)

    return full_alias


def get_ladm_unit(units, table, field):
    unit_key = table + ".." +field
    return units[unit_key].strip() if unit_key in units else ''