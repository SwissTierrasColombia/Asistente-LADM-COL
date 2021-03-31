
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtWidgets import QMessageBox

from asistente_ladm_col.utils.select_map_tool import SelectMapTool


class SelectFeaturesOnMapWrapper:

    def __init__(self, iface, logger):
        self.__iface = iface
        self.__canvas = self.__iface.mapCanvas()
        self.__map_tool = self.__canvas.mapTool()
        self.__select_maptool = None

        self.__observer = None
        self.__logger = logger

    def __map_tool_changed(self, new_tool, old_tool):
        self.__canvas.mapToolSet.disconnect(self.__map_tool_changed)

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setText(QCoreApplication.translate("WizardTranslations", "Do you really want to change the map tool?"))
        msg.setWindowTitle(QCoreApplication.translate("WizardTranslations", "CHANGING MAP TOOL?"))
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText(QCoreApplication.translate("WizardTranslations", "Yes, and close the wizard"))
        msg.button(QMessageBox.No).setText(QCoreApplication.translate("WizardTranslations", "No, continue editing"))
        reply = msg.exec_()

        if reply == QMessageBox.No:
            self.__canvas.setMapTool(old_tool)
            self.__canvas.mapToolSet.connect(self.__map_tool_changed)
        else:
            self.__notify_map_tool_close()

    def select_features_on_map(self, layer):
        self.__iface.setActiveLayer(layer)

        # ------- self.setVisible(False)  # Make wizard disappear
        # Enable Select Map Tool
        self.__select_maptool = SelectMapTool(self.__canvas, layer, multi=True)
        self.__canvas.setMapTool(self.__select_maptool)

        # Connect signal that check if map tool change
        # This is necessary after select the maptool
        self.__canvas.mapToolSet.connect(self.__map_tool_changed)

        # Connect signal that check a feature was selected
        self.__select_maptool.features_selected_signal.connect(self.__features_selected)

    def __features_selected(self):
        self.__notify_feature_selected()

        # Disconnect signal that check if map tool change
        # This is necessary before changing the tool to the user's previous selection
        self.__canvas.mapToolSet.disconnect(self.__map_tool_changed)
        self.__canvas.setMapTool(self.__map_tool)

        self.__logger.info(__name__, "Select maptool SIGNAL disconnected")
        self.__select_maptool.features_selected_signal.disconnect(self.__features_selected)

    def register_observer(self, observer):
        self.__observer = observer

    def __notify_map_tool_close(self):
        if self.__observer:
            self.__observer.map_tool_changed()

    def __notify_feature_selected(self):
        if self.__observer:
            self.__observer.feature_selected()
