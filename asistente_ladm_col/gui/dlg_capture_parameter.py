from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication,
                              QRegExp,
                              pyqtSignal)
from qgis.PyQt.QtGui import QRegExpValidator
from qgis.PyQt.QtWidgets import (QDialog,
                                 QSizePolicy,
                                 QDialogButtonBox)
from qgis.core import Qgis
from qgis.gui import QgsMessageBar

from ..utils import get_ui_class
from ..utils.qt_utils import Validators
from ..lib.dbconnector.pg_connector import PGConnector

DIALOG_UI = get_ui_class('dlg_capture_parameter.ui')

class DialogCaptureParameter(QDialog, DIALOG_UI):

    completed_creation = pyqtSignal(str)

    def __init__(self, dict_conn, type, parent=None):
        """
        Constructor
        :param db: database connection instance
        :param type: type of parameter to capture (database or schema)
        :param parent: parent of dialog
        """
        QDialog.__init__(self, parent)

        # element_type: indicates if I create a database or a schema
        self.type = type
        self.dict_conn = dict_conn
        self.parent = parent
        self.setupUi(self)
        self.message_label.setText(QCoreApplication.translate("DialogCaptureParameter", "Enter the name of the {type}:").format(type=self.type))
        self.setWindowTitle(QCoreApplication.translate("DialogCaptureParameter", "Create {type}").format(type=self.type))

        self.parameter_line_edit.setPlaceholderText(QCoreApplication.translate("DialogCaptureParameter", "[Name of the {type} to be created]").format(type=self.type))
        self.validators = Validators()

        # schema name mustn't have special characters
        regex = QRegExp("[a-zA-Z0-9_]+")
        validator = QRegExpValidator(regex)
        self.parameter_line_edit.setValidator(validator)
        self.parameter_line_edit.setMaxLength(63)
        self.parameter_line_edit.textChanged.connect(self.validators.validate_line_edits_lower_case)
        self.parameter_line_edit.textChanged.emit(self.parameter_line_edit.text())

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.layout().addWidget(self.bar, 0, 0, Qt.AlignTop)

        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.clear()
        self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self.buttonBox.addButton(QCoreApplication.translate("DialogCaptureParameter", "Create {type}").format(type=self.type), QDialogButtonBox.AcceptRole)

    def accepted(self):
        parameter_value = self.parameter_line_edit.text().strip()
        if not parameter_value:
            self.show_message(QCoreApplication.translate("DialogCaptureParameter", "The name of the {type} cannot be empty.").format(type=self.type), Qgis.Warning)
            return

        tmp_db_conn = PGConnector('')
        self.buttonBox.setEnabled(False)
        self.parameter_line_edit.setEnabled(False)

        if self.type == 'database':
            db_name = parameter_value
            # Connection with postgres server
            uri = self.get_connection_uri(self.dict_conn)
            result = tmp_db_conn.create_database(uri, db_name)
        elif self.type == 'schema':
            db_name = self.parent.selected_db_combobox.currentText().strip()
            schema_name = parameter_value
            # Connection with postgres database
            uri = self.get_connection_uri(self.dict_conn, 1)
            result = tmp_db_conn.create_schema(uri, schema_name)

        if result[0]:
            self.buttonBox.clear()
            self.buttonBox.setEnabled(True)
            self.buttonBox.addButton(QDialogButtonBox.Close)
            self.show_message(result[1], Qgis.Success)

            # signal updating the list of databases or schemas
            self.completed_creation.emit(parameter_value)
        else:
            self.show_message(result[1], Qgis.Warning)
            self.buttonBox.setEnabled(True)
            self.parameter_line_edit.setEnabled(True)
            return

    def show_message(self, message, level):
        self.bar.pushMessage("Asistente LADM_COL", message, level, duration=0)

    def get_connection_uri(self, dict_conn, level=0):
        """
        Get connection URI wit postgres DB
        :param dict_conn: dictionary with connection database parameters
        :param level: (int) level of connection with postgres
                    0 = Server
                    1 = Database
        :return: (str) URI connection to DB
        """
        uri = []
        uri += ['host={}'.format(dict_conn['host'])]
        uri += ['port={}'.format(dict_conn['port'])]
        uri += ['user={}'.format(dict_conn['username'])]
        uri += ['password={}'.format(dict_conn['password'])]

        if dict_conn['database'] and level == 1:
            uri += ['dbname={}'.format(dict_conn['database'])]

        return ' '.join(uri)
