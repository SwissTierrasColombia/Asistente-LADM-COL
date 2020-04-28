import nose2
from qgis.testing import unittest
import pyodbc


class TestMsSql(unittest.TestCase):

    def test_dummy(self):
        uri = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=mssql,1433;DATABASE=ladm_col;UID=sa;PWD=<YourStrong!Passw0rd>"

        con = pyodbc.connect(uri)

