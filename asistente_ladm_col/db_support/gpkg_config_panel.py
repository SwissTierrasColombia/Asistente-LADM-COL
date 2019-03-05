from .db_config_panel import DbConfigPanel
from qgis.PyQt.QtCore import (Qt, QCoreApplication,pyqtSignal)
from qgis.core import (Qgis)
from qgis.PyQt.QtWidgets import (QWidget,
                                 QLabel,
                                 QGridLayout,
                                 QLineEdit,
                                 QToolButton)
from .enum_action_type import EnumActionType
from ..utils.qt_utils import ( make_save_file_selector,
                               make_file_selector,
                               Validators,
                               FileValidator)


class GpkgConfigPanel(QWidget, DbConfigPanel):
    notify_message_requested = pyqtSignal(str, Qgis.MessageLevel)

    def __init__(self, parent=None):

        QWidget.__init__(self, parent)
        super(GpkgConfigPanel, self).__init__()
        lbl_file = QLabel(self.tr("Database File"))

        self.txt_file = QLineEdit()

        self.btn_file_browse = QToolButton()
        self.btn_file_browse.setText("...")

        self.action = None

        self.set_action(EnumActionType.OTHER)

        layout = QGridLayout(self)
        layout.addWidget(lbl_file, 0, 0)

        layout.addWidget(self.txt_file, 0, 1)
        layout.addWidget(self.btn_file_browse, 0, 2)

        self.txt_file.textEdited.connect(self._set_params_changed)

    def read_connection_parameters(self):
        dict_conn = dict()
        dict_conn['dbfile'] = self.txt_file.text().strip()

        return dict_conn

    def write_connection_parameters(self, dict_conn):
        self.txt_file.setText(dict_conn['dbfile'])

    def get_keys_connection_parameters(self):
        return list(self.read_connection_parameters().keys())

    def set_action(self, action):
        self.action = action
        try:
            self.btn_file_browse.clicked.disconnect()
        except TypeError:
            pass

        if action == EnumActionType.SCHEMA_IMPORT:
            # TODO DialogImportSchema?
            file_selector = \
            make_save_file_selector(
                self.txt_file,
                title=QCoreApplication.translate("DialogImportSchema", "Create GeoPackage database file"),
                file_filter=QCoreApplication.translate("DialogImportSchema", "GeoPackage Database (*.gpkg)"),
                extension='.gpkg')

        else:
            # TODO DialogExportData?
            file_selector = \
                make_file_selector(self.txt_file,
                title=QCoreApplication.translate("DialogExportData", "Open GeoPackage database file"),
                file_filter=QCoreApplication.translate("DialogExportData","GeoPackage Database (*.gpkg)"))

        self.btn_file_browse.clicked.connect(file_selector)