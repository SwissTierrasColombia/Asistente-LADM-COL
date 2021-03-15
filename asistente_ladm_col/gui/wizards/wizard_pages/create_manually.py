from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject)


class CreateManually(QObject):
    # problema con los parámetros

    def __init__(self, iface, app, logger, layer, feature_name):
        super(CreateManually, self).__init__()
        self.__iface = iface
        self.__app = app
        self.__layer = layer

        self.__logger = logger
        self.__feature_name = feature_name
        self.__observer = None

    def register_observer(self, observer):
        self.__observer = observer

    def create_manually(self):
        # --------------------------------------- self.edit_feature()
        # selecciona el layer como capa actual
        self.__iface.layerTreeView().setCurrentLayer(self.__layer)
        # agrega el método para el evento ¿?
        if self.__observer:
            self.__layer.committedFeaturesAdded.connect(self.__observer.finish_feature_creation)
        # ---------------------------------------++++ self.open_form(self._layers[self.EDITING_LAYER_NAME])
        # pone la capa en modo editable
        if not self.__layer.isEditable():
            self.__layer.startEditing()
        # --------------------------------------------++++ self.exec_form(layer)
        feature = self.__app.core.get_new_feature(self.__layer)  # self.get_feature_exec_form(layer)
        self.__exec_form(self.__layer, feature)
        self.__iface.mapCanvas().refresh()

    def __exec_form(self, layer, feature):
        dialog = self.__iface.getFeatureForm(layer, feature)
        if self.__observer:
            dialog.rejected.connect(self.__observer.form_rejected)
        dialog.setModal(True)

        if dialog.exec_():
            if self.__observer:
                self.__observer.exec_form_advanced(layer)
            saved = layer.commitChanges()

            if not saved:
                layer.rollBack()
                self.__logger.warning_msg(__name__,
                                        QCoreApplication.translate("WizardTranslations", "Error while saving changes. {} could not be created.").format(self.__feature_name))

                for e in layer.commitErrors():
                    self.__logger.warning(__name__, "Commit error: {}".format(e))
        else:
            layer.rollBack()
