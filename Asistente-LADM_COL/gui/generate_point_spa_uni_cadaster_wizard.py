from qgis.PyQt.QtWidgets import QWizard

from ..utils import get_ui_class

WIZARD_UI = get_ui_class('wiz_add_points_cadaster.ui')

class GeneratePointsSpatialUnitCadasterWizard(QWizard, WIZARD_UI):
    def __init__(self, iface, parent=None):
        QWizard.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
