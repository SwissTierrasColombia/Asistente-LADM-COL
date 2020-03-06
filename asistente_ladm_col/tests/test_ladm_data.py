import nose2

from qgis.core import NULL
from qgis.testing import (start_app,
                          unittest)

start_app()  # need to start before asistente_ladm_col.tests.utils

from asistente_ladm_col.utils.qgis_utils import QGISUtils
from asistente_ladm_col.logic.ladm_col.ladm_data import LADM_DATA
from asistente_ladm_col.config.general_config import (LAYER,
                                                      LAYER_NAME)
from asistente_ladm_col.tests.utils import (get_pg_conn,
                                            normalize_response,
                                            restore_schema)


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
