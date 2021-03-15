from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject)
from qgis.core import QgsProject


class CreateManuallySpatial: #  (QObject):

    # # feature_editing
    # __register_finish_feature
    # feature_for_dialog_getting
    # geometry_finalized
    # dialog_succeed
    # invalid_geometry
    # zero_or_many_features_adde

    def __init__(self, iface, app, logger, layer, feature_name, tolerance=None):
        # super(CreateManuallySpatial, self).__init__()
        self.__iface = iface
        self.__app = app
        self.__layer = layer
        self.__logger = logger
        self.__feature_name = feature_name
        self.__tolerance = tolerance
        self.__layer_to_edit = layer
        self.__observer = None

    def register_observer(self, observer):
        self.__observer = observer

    # def __notify_feature_editing(self, create_manually_params):
    #     if self.__observer:
    #         self.__observer.feature_editing(create_manually_params)

    def __register_finish_feature(self):
        if self.__observer:
            self.__layer.committedFeaturesAdded.connect(self.__observer.finish_feature_creation)

    def __register_form_rejected_signal(self, dialog):
        if self.__observer:
            dialog.rejected.connect(self.__observer.form_rejected)

    def __notify_feature_for_dialog_getting(self, feature_params):
        if self.__observer:
            self.__observer.feature_for_dialog_getting(feature_params)

    def __notify_geometry_finalized(self, finalized_geometry_params):
        if self.__observer:
            self.__observer.geometry_finalized(finalized_geometry_params)

    def __notify_dialog_succeed(self, dialog_succeed_params):
        if self.__observer:
            self.__observer.dialog_succeed(dialog_succeed_params)

    def __notify_invalid_geometry(self, invalid_geometry_params):
        if self.__observer:
            self.__observer.invalid_geometry(invalid_geometry_params)

    def __notify_zero_or_many_features_added(self, zero_or_many_features_added_params):
        if self.__observer:
            self.__observer.zero_or_many_features_added(zero_or_many_features_added_params)

    def create_manually(self, layer_to_edit=None):
        #  params = {"layer": self.__edited_layer, "cancel": False}

        #     edit_feature(): *******************************************************************
        #  self.__notify_feature_editing(params)

        #  if not params['cancel']:
        #    return
        if layer_to_edit:
            self.__layer_to_edit = layer_to_edit

        layer = self.__layer_to_edit

        self.__iface.layerTreeView().setCurrentLayer(layer)
        self.__register_finish_feature()

        # Disable transactions groups
        QgsProject.instance().setAutoTransaction(False)

        # Activate snapping
        if self.__tolerance:
            self.__app.core.active_snapping_all_layers(self.__tolerance)
        else:
            self.__app.core.active_snapping_all_layers()

        # ------------------------------------- self.open_form(self._layers[self.EDITING_LAYER_NAME])
        if not layer.isEditable():
            layer.startEditing()

        # oculta el formulario
        self.__app.core.suppress_form(layer, True)
        self.__iface.actionAddFeature().trigger()
        # ------------------------------------------

        self.__logger.info_msg(__name__, QCoreApplication.translate("WizardTranslations",
                                                                  "You can now start capturing {} digitizing on the map...").format(
            self.__feature_name))

    def save_created_geometry(self):
        layer = self.__layer_to_edit

        if layer.editBuffer() and len(layer.editBuffer().addedFeatures()) == 1:
            feature = [value for index, value in layer.editBuffer().addedFeatures().items()][0]

            if feature.geometry().isGeosValid():
                self.exec_form()
            else:
                self.__notify_invalid_geometry({"layer": layer})
        elif layer.editBuffer():
            self.__notify_zero_or_many_features_added(
                {"len_features_added": len(layer.editBuffer().addedFeatures()), "layer": layer})

    def exec_form(self):
        self.__notify_geometry_finalized({"finalized": False})

        params = {"feature": None, "layer": self.__layer_to_edit, "customized_feature": False}

        self.__notify_feature_for_dialog_getting(params)

        if not params["customized_feature"]:
            feature = self.__get_added_feature()
        else:
            feature = params["feature"]

        layer = self.__layer

        print(layer)
        print(feature)
        dialog = self.__iface.getFeatureForm(layer, feature)
        self.__register_form_rejected_signal(dialog)
        dialog.setModal(True)

        if dialog.exec_():
            self.__notify_dialog_succeed({"layer": layer})
            saved = layer.commitChanges()

            if not saved:
                layer.rollBack()
                self.__logger.warning_msg(__name__, QCoreApplication.translate("WizardTranslations", "Error while saving changes. {} could not be created.").format(self.__feature_name))
                for e in layer.commitErrors():
                    self.__logger.warning(__name__, "Commit error: {}".format(e))
        else:
            layer.rollBack()
        self.__iface.mapCanvas().refresh()

    #  ok
    def __get_added_feature(self):
        # [value for index, value in layer.editBuffer().addedFeatures().items()][0]
        feature = None
        for id, added_feature in self.__layer_to_edit.editBuffer().addedFeatures().items():
            feature = added_feature
            break

        return feature
