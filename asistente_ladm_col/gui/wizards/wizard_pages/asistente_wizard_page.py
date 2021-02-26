from qgis.PyQt.QtWidgets import QWizardPage
from asistente_ladm_col.utils.ui import load_ui


class AsistenteWizardPage(QWizardPage):

    def __init__(self, ui_path):
        super(AsistenteWizardPage, self).__init__()
        load_ui(ui_path, self)
