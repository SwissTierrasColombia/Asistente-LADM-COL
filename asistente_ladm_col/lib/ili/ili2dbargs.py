# Adapted from Model Baker's DbCommandConfigManager

from asistente_ladm_col.lib.ili.enums import DbIliMode
from asistente_ladm_col.lib.ili.ili2dbconfig import SchemaImportConfiguration


def get_ili2db_args(configuration, hide_password=False):
    """Gets a complete list of ili2db arguments in order to execute the app.

    :param bool hide_password: *True* to mask the password, *False* otherwise.
    :return: ili2db arguments list.
    :rtype: list
    """
    db_args = _get_db_args(configuration, hide_password)

    if type(configuration) is SchemaImportConfiguration:
        db_args += _get_schema_import_args(configuration.tool)

    return configuration.to_ili2db_args(db_args)


def _get_db_args(configuration, hide_password=False):
    su = configuration.db_use_super_login  # Boolean
    db_args = list()

    if configuration.tool == DbIliMode.ili2gpkg:
        db_args = ["--dbfile", configuration.dbfile]
    elif configuration.tool == DbIliMode.ili2pg:
        db_args += ["--dbhost", configuration.dbhost]
        if configuration.dbport:
            db_args += ["--dbport", configuration.dbport]
        if su:
            db_args  += ["--dbusr", configuration.base_configuration.super_pg_user]
        else:
            db_args += ["--dbusr", configuration.dbusr]
        if not su and configuration.dbpwd or su and configuration.base_configuration.super_pg_password:
            if hide_password:
                db_args += ["--dbpwd", '******']
            else:
                if su:
                    db_args += ["--dbpwd", configuration.base_configuration.super_pg_password]
                else:
                    db_args += ["--dbpwd", configuration.dbpwd]
        db_args += ["--dbdatabase", configuration.database]
        db_args += ["--dbschema",
                    configuration.dbschema or configuration.database]
    elif configuration.tool == DbIliMode.ili2mssql:
        db_args += ["--dbhost", configuration.dbhost]
        if configuration.dbport:
            db_args += ["--dbport", configuration.dbport]
        db_args += ["--dbusr", configuration.dbusr]
        if configuration.dbpwd:
            if hide_password:
                db_args += ["--dbpwd", '******']
            else:
                db_args += ["--dbpwd", configuration.dbpwd]
        db_args += ["--dbdatabase", configuration.database]
        db_args += ["--dbschema", configuration.dbschema or configuration.database]
        if configuration.dbinstance:
            db_args += ["--dbinstance", configuration.dbinstance]

    return db_args


def _get_schema_import_args(tool):
    args = list()
    if tool == DbIliMode.ili2pg:
        args += ["--setupPgExt"]
    return args
