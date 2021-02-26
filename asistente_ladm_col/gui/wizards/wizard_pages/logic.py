from qgis.PyQt.QtCore import ( # QSettings,
                              QCoreApplication,
                              pyqtSignal)

from qgis.core import QgsVectorLayer

from asistente_ladm_col.config.general_config import WIZARD_EDITING_LAYER_NAME, WIZARD_READ_ONLY_FIELDS, \
    WIZARD_MAP_LAYER_PROXY_MODEL
from qgis.core import QgsMapLayerProxyModel


class Logic:
    # TODO maybe, Implement strategy (example: customEstrategy)
    exec_form_advanced = pyqtSignal(QgsVectorLayer)
    prepare_feature_creation_layers = pyqtSignal(str)  # dummy str

    # TODO other parameters iface
    def __init__(self, app, db, layers, wizard_config):
        self.app = app
        self._layers = layers
        self.db = db
        self.wizard_config = wizard_config
        # self.iface = iface

        self.EDITING_LAYER_NAME = self.wizard_config[WIZARD_EDITING_LAYER_NAME]

    def create_from_refactor(self, selected_layer, editing_layer_name, field_mapping):
        res_etl_model = self.app.core.show_etl_model(self.db,
                                                     selected_layer,
                                                     editing_layer_name,
                                                     field_mapping=field_mapping)
        if res_etl_model:  # Features were added?
            self.app.gui.redraw_all_layers()  # Redraw all layers to show imported data

            # If the result of the etl_model is successful and we used a stored recent mapping, we delete the
            # previous mapping used (we give preference to the latest used mapping)
            if field_mapping:
                self.app.core.delete_old_field_mapping(field_mapping)

            self.app.core.save_field_mapping(editing_layer_name)

    def rollback_in_layers_with_empty_editing_buffer(self):
        for layer_name in self._layers:
            if self._layers[layer_name] is not None:  # If the layer was removed, this becomes None
                if self._layers[layer_name].isEditable():
                    if not self._layers[layer_name].editBuffer().isModified():
                        self._layers[layer_name].rollBack()

    def set_ready_only_field(self, read_only=True):
        if self._layers[self.EDITING_LAYER_NAME] is not None:
            for field in self.wizard_config[WIZARD_READ_ONLY_FIELDS]:
                # Not validate field that are read only
                self.app.core.set_read_only_field(self._layers[self.EDITING_LAYER_NAME], field, read_only)

    def get_field_mappings_file_names(self):
        return self.app.core.get_field_mappings_file_names(self.EDITING_LAYER_NAME)

    def get_filters(self):
        return QgsMapLayerProxyModel.Filter(self.wizard_config[WIZARD_MAP_LAYER_PROXY_MODEL])
