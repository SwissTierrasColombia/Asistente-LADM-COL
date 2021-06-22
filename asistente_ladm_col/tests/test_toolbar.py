import nose2

from qgis.testing import start_app, unittest

from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.gui.toolbar import ToolBar
from asistente_ladm_col.tests.utils import (import_qgis_model_baker,
                                            import_processing,
                                            import_asistente_ladm_col,
                                            get_iface,
                                            get_copy_gpkg_conn,
                                            unload_qgis_model_baker)

start_app()  # need to start before asistente_ladm_col.tests.utils


class TestToolbar(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import_processing()
        import_asistente_ladm_col()  # Import plugin
        import_qgis_model_baker()
        cls.app = AppInterface()
        cls.toolbar = ToolBar(get_iface())

    def test_build_boundaries(self):
        print('\nINFO: Validating build boundaries...')
        self.db_gpkg = get_copy_gpkg_conn('test_toolbar_gpkg')
        res, code, msg = self.db_gpkg.test_connection()
        self.assertTrue(res, msg)

        layers = {self.db_gpkg.names.LC_BOUNDARY_POINT_T: None,
                  self.db_gpkg.names.LC_BOUNDARY_T: None,
                  self.db_gpkg.names.LC_PLOT_T: None,
                  self.db_gpkg.names.MORE_BFS_T: None,
                  self.db_gpkg.names.LESS_BFS_T: None,
                  self.db_gpkg.names.POINT_BFS_T: None}
        self.app.core.get_layers(self.db_gpkg, layers, load=True)

        print('\nINFO: Check initial data...')
        layers_feature_count = {self.db_gpkg.names.LC_BOUNDARY_POINT_T: 12,
                                self.db_gpkg.names.LC_BOUNDARY_T: 21,
                                self.db_gpkg.names.LC_PLOT_T: 14,
                                self.db_gpkg.names.MORE_BFS_T: 42,
                                self.db_gpkg.names.LESS_BFS_T: 0,
                                self.db_gpkg.names.POINT_BFS_T: 46}

        for layer_name, feature_count in layers_feature_count.items():
            self.assertEqual(layers[layer_name].featureCount(),
                             feature_count,
                             'Features count does not match for the layer {}'.format(layer_name))

        print('\nINFO: Check build boundaries using a selection...')
        boundary_ids = ['c1a08287-4fd5-4504-a6b7-cd029bd0d352', 'e7db709f-f9ef-4d83-b59b-692f1c4f7942',
                        'db813999-3e1e-4539-99b6-7b797b1a3a72', '9831e428-040b-48e1-960a-5546fa47b99e',
                        '9a009adf-6e87-4b04-aeb6-5d0830a848a7', '25509907-7cbc-4c7d-ab76-153898205f80',
                        '1ef74b53-46fa-4dc5-9d85-c25db94f3dcd', '5b7194f2-54d8-4352-a47d-fac7f270a4a1']

        exp = "{} in ({})".format(self.db_gpkg.names.T_ILI_TID_F,
                                  ', '.join("'{}'".format(boundary_id) for boundary_id in boundary_ids))
        layers[self.db_gpkg.names.LC_BOUNDARY_T].selectByExpression(exp)

        self.toolbar.build_boundary(self.db_gpkg)

        layers_feature_count = {self.db_gpkg.names.LC_BOUNDARY_POINT_T: 12,
                                self.db_gpkg.names.LC_BOUNDARY_T: 22,
                                self.db_gpkg.names.LC_PLOT_T: 14,
                                self.db_gpkg.names.MORE_BFS_T: 43,
                                self.db_gpkg.names.LESS_BFS_T: 0,
                                self.db_gpkg.names.POINT_BFS_T: 47}

        for layer_name, feature_count in layers_feature_count.items():
            self.assertEqual(layers[layer_name].featureCount(),
                             feature_count,
                             'Features count does not match for the layer {}'.format(layer_name))

        print('\nINFO: Check build boundaries for all features...')
        layers[self.db_gpkg.names.LC_BOUNDARY_T].selectAll()
        self.toolbar.build_boundary(self.db_gpkg)

        layers_feature_count = {self.db_gpkg.names.LC_BOUNDARY_POINT_T: 12,
                                self.db_gpkg.names.LC_BOUNDARY_T: 25,
                                self.db_gpkg.names.LC_PLOT_T: 14,
                                self.db_gpkg.names.MORE_BFS_T: 44,
                                self.db_gpkg.names.LESS_BFS_T: 0,
                                self.db_gpkg.names.POINT_BFS_T: 50}

        for layer_name, feature_count in layers_feature_count.items():
            self.assertEqual(layers[layer_name].featureCount(),
                             feature_count,
                             'Features count does not match for the layer {}'.format(layer_name))

    @classmethod
    def tearDownClass(cls):
        print("INFO: Unloading Model Baker...")
        unload_qgis_model_baker()


if __name__ == '__main__':
    nose2.main()
