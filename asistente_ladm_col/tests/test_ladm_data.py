import nose2

from qgis.testing import (start_app,
                          unittest)

start_app()  # need to start before asistente_ladm_col.tests.utils


class TestLADMData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # TODO: Implement tests for LADM data
        pass

    def test_get_domain_value_from_code(self):
        # TODO: Implement tests for LADM data
        pass

if __name__ == '__main__':
    nose2.main()
