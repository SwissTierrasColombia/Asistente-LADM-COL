# Adapted from Model Baker's DbFactory

from asistente_ladm_col.lib.ili.enums import DbIliMode


def get_tool_version(tool, db_ili_version):
    if tool == DbIliMode.ili2gpkg:
        if db_ili_version == 3:
            return '3.11.3'
        else:
            return '4.4.4'
    elif tool == DbIliMode.ili2pg:
        if db_ili_version == 3:
            return '3.11.2'
        else:
            return '4.4.4'
    elif tool == DbIliMode.ili2mssql:
        if db_ili_version == 3:
            return '3.12.2'
        else:
            return '4.4.4'

    return '0'


def get_tool_url(tool, db_ili_version):
    if tool == DbIliMode.ili2gpkg:
        return 'https://downloads.interlis.ch/ili2gpkg/ili2gpkg-{version}.zip'.format(
            version=get_tool_version(tool, db_ili_version))
    elif tool == DbIliMode.ili2pg:
        return 'https://downloads.interlis.ch/ili2pg/ili2pg-{version}.zip'.format(
            version=get_tool_version(tool, db_ili_version))
    elif tool == DbIliMode.ili2mssql:
        return 'https://downloads.interlis.ch/ili2mssql/ili2mssql-{version}.zip'.format(
            version=get_tool_version(tool, db_ili_version))

    return ''
