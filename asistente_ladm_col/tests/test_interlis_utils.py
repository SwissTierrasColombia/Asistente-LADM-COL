# -*- coding: utf-8 -*-
import nose2
from asistente_ladm_col.lib.model_registry import LADMColModelRegistry

from qgis.testing import (start_app,
                          unittest)

from asistente_ladm_col.config.ladm_names import LADMNames
from asistente_ladm_col.tests.utils import get_test_path
from asistente_ladm_col.utils.interlis_utils import get_models_from_xtf
start_app()


class TestInterlisUtils(unittest.TestCase):

    def test_xtf_with_start_and_closing_tag(self):
        found_models = get_models_from_xtf(get_test_path("xtf/start_and_closing_tag.xtf"))
        # print(get_models_from_xtf("/docs/borrar/xtf/empty_element_tag.xtf"))
        expected_models = [LADMColModelRegistry().model(LADMNames.SUPPLIES_MODEL_KEY).full_name()]

        self.assertEqual(expected_models, found_models)

    def test_xtf_with_empty_element_tag(self):
        found_models = get_models_from_xtf(get_test_path("xtf/empty_element_tag.xtf"))
        expected_models = [LADMColModelRegistry().model(LADMNames.SNR_DATA_SUPPLIES_MODEL_KEY).full_name(),
                           LADMColModelRegistry().model(LADMNames.SUPPLIES_MODEL_KEY).full_name(),
                           LADMColModelRegistry().model(LADMNames.SUPPLIES_INTEGRATION_MODEL_KEY).full_name()]
        self.assertEqual(expected_models.sort(), found_models.sort())

if __name__ == '__main__':
    nose2.main()
