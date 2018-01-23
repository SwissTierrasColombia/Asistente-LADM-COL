import os

from qgis.PyQt.uic import loadUiType
from qgis.PyQt.QtWidgets import QWizard

def get_ui_class(ui_file):
    """Get UI Python class from .ui file.
       Can be filename.ui or subdirectory/filename.ui
    :param ui_file: The file of the ui in svir.ui
    :type ui_file: str
    """
    os.path.sep.join(ui_file.split('/'))
    ui_file_path = os.path.abspath(
            os.path.join(
                    os.path.dirname(__file__),
                    os.pardir,
                    'ui',
                    ui_file
            )
    )
    return loadUiType(ui_file_path)[0]

def disable_next_wizard(self):
    btnList = [QWizard.HelpButton, QWizard.Stretch, QWizard.FinishButton, QWizard.CancelButton]
    self.setButtonLayout(btnList)

def enable_next_wizard(self):
    btnList = [QWizard.HelpButton, QWizard.Stretch, QWizard.NextButton, QWizard.FinishButton, QWizard.CancelButton]
    self.setButtonLayout(btnList)
