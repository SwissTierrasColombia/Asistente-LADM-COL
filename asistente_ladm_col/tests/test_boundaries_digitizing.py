import qgis
import nose2
import psycopg2
import os

from sys import platform
from qgis.testing import unittest, start_app

start_app() # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.gui.point_spa_uni_cadastre_wizard import PointsSpatialUnitCadastreWizard
from asistente_ladm_col.tests.utils import import_projectgenerator, get_dbconn, get_test_path
from asistente_ladm_col.utils.qgis_utils import QGISUtils

import_projectgenerator()

class TestDigitizing(unittest.TestCase):

    def setUpClass():
        print('setUpClass test_boundaries_digitizing')

    def test_boundaries_digitizing(self):
        print('test_boundaries_digitizing, test buttons explode merge')

    def tearDownClass():
        print('tearDown test_boundaries_digitizing')


if __name__ == '__main__':
    nose2.main()
