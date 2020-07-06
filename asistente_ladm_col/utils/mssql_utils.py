import re


def is_libqt5sql5_odbc_available():
    from qgis.PyQt.QtSql import QSqlDatabase
    db = QSqlDatabase.addDatabase("QODBC")
    return db.isValid()


def is_pyodbc_available():
    result = False
    try:
        import pyodbc
        result = True
    except ModuleNotFoundError:
        pass
    return result


def check_if_odbc_exists():
    result = False

    try:
        odbc_drivers = get_odbc_drivers()
        result = len(odbc_drivers) != 0
    except ModuleNotFoundError:
        pass
    return result


def get_odbc_drivers():
    # Borrowed from Model Baker
    import pyodbc
    result = list()
    regex_list = ['sql.*server', 'mssql', 'FreeTDS']
    for item in pyodbc.drivers():
        regex_sql_server = "({})".format("|".join(regex_list))

        x = re.search(regex_sql_server, item, re.IGNORECASE)

        if x:
            result.append(item)

    return result
