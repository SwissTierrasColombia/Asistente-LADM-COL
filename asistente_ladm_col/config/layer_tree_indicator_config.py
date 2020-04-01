from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication)
from qgis.PyQt.QtGui import QIcon

from qgis.core import QgsLayerTreeNode

from asistente_ladm_col.config.translation_strings import (TranslatableConfigStrings,
                                                           ERROR_LAYER_GROUP)
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

    def get_indicators_config(self, node_name, node_type):
        """
        Gets the configuration of layer tree node indicators. Each node could have several indicators.

        :param node_name: Layer tree node name
        :param node_type: QgsLayerTreeNode.NodeType
        :return: List of indicators data. Each indicator config data is a dict, which has these mandatory keys:
                    INDICATOR_TOOLTIP,
                    INDICATOR_ICON,
                    INDICATOR_SLOT
        """
        indicators_config = []
        translated_strings = TranslatableConfigStrings.get_translatable_config_strings()

        if node_type == QgsLayerTreeNode.NodeGroup:
            if node_name == translated_strings[ERROR_LAYER_GROUP]:
                indicators_config = [{
                    INDICATOR_TOOLTIP: QCoreApplication.translate("LayerTreeIndicatorConfig", "<b>Export</b><br>Export quality errors to GeoPackage"),
                    INDICATOR_ICON: QIcon(":/Asistente-LADM_COL/resources/images/save.svg"),
                    INDICATOR_SLOT: self._slot_caller.export_error_group
                }, {
                    INDICATOR_TOOLTIP: QCoreApplication.translate("LayerTreeIndicatorConfig",
                                                                  "<b>Export</b><br>Export quality errors to PDF"),
                    INDICATOR_ICON: QIcon(":/Asistente-LADM_COL/resources/images/pdf.svg"),
                    INDICATOR_SLOT: self._slot_caller.show_log_quality_dialog
                }]
        elif node_type == QgsLayerTreeNode.NodeLayer:
            pass

        return indicators_config

