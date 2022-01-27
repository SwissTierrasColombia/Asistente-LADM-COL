from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication)
from qgis.PyQt.QtGui import QIcon

from qgis.core import QgsLayerTreeNode

from asistente_ladm_col.utils.singleton import SingletonQObject

INDICATOR_TOOLTIP = "INDICATOR_TOOLTIP"
INDICATOR_ICON = "INDICATOR_ICON"
INDICATOR_SLOT = "INDICATOR_SLOT"


class LayerTreeIndicatorConfig(QObject, metaclass=SingletonQObject):
    def __init__(self):
        QObject.__init__(self)

        self._slot_caller = None

    def set_slot_caller(self, slot_caller):
        self._slot_caller = slot_caller

    def get_indicators_config(self, node_name, node_type, names):
        """
        Gets the configuration of layer tree node indicators. Each node could have several indicators.

        :param node_name: Layer tree node name
        :param node_type: QgsLayerTreeNode.NodeType
        :param names: DBMappingRegistry instance to read layer names from
        :return: List of indicators data. Each indicator config data is a dict, which has these mandatory keys:
                    INDICATOR_TOOLTIP,
                    INDICATOR_ICON,
                    INDICATOR_SLOT
        """
        indicators_config = []

        if node_type == QgsLayerTreeNode.NodeGroup:
            pass
        elif node_type == QgsLayerTreeNode.NodeLayer:
            if node_name == names.LC_PLOT_T:
                indicators_config = [{
                    INDICATOR_TOOLTIP: QCoreApplication.translate("LayerTreeIndicatorConfig", "<b>Show informality</b><br>Show informal plots in the map"),
                    INDICATOR_ICON: QIcon(":/Asistente-LADM-COL/resources/images/informality.svg"),
                    INDICATOR_SLOT: self._slot_caller.show_informal_plots
                }]
            elif node_name == names.LC_BUILDING_T:
                indicators_config = [{
                    INDICATOR_TOOLTIP: QCoreApplication.translate("LayerTreeIndicatorConfig", "<b>Show informality</b><br>Show informal buildings in the map"),
                    INDICATOR_ICON: QIcon(":/Asistente-LADM-COL/resources/images/informality.svg"),
                    INDICATOR_SLOT: self._slot_caller.show_informal_buildings
                }]
            elif node_name == names.LC_BUILDING_UNIT_T:
                indicators_config = [{
                    INDICATOR_TOOLTIP: QCoreApplication.translate("LayerTreeIndicatorConfig", "<b>Show informality</b><br>Show informal building units in the map"),
                    INDICATOR_ICON: QIcon(":/Asistente-LADM-COL/resources/images/informality.svg"),
                    INDICATOR_SLOT: self._slot_caller.show_informal_building_units
                }]

        return indicators_config

