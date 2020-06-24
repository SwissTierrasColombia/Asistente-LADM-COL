
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
