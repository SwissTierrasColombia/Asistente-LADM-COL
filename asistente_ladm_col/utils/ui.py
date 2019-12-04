import os

from qgis.PyQt.uic import loadUiType, loadUi


def get_ui_class(ui_file):
    """Get UI Python class from .ui file.
       Can be filename.ui or subdirectory/filename.ui
    :param ui_file: The file of the ui in svir.ui
    :type ui_file: str
    """
    ui_file_path = get_ui_file_path(ui_file)
    return loadUiType(ui_file_path)[0]


def get_ui_file_path(ui_file):
    os.path.sep.join(ui_file.split('/'))
    ui_file_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            'ui',
            ui_file
        )
    )

    return ui_file_path


def load_ui(ui_file, baseinstance):
    ui_file_path = get_ui_file_path(ui_file)
    loadUi(ui_file_path, baseinstance)