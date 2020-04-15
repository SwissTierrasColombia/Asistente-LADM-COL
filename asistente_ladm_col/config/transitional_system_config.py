from qgis.PyQt.QtCore import (QObject,
                              QSettings,
                              QCoreApplication)

from asistente_ladm_col.utils.singleton import SingletonQObject


class TransitionalSystemConfig(QObject, metaclass=SingletonQObject):
    ST_DEFAULT_DOMAIN = "https://apist-pruebas.proadmintierra.info"  # "http://apist.proadmintierra.info"
    ST_LOGIN_SERVICE_PAYLOAD = "username={}&password={}&grant_type=password"
    encoded = b'c3Qtd2ViLWpqOHNmUUVVOm5FSmVzR3ZF'  # b'c3Qtd2ViLWRldmVsb3AtZHZLREtnUXI6MTIzNDU='
    ST_LOGIN_AUTHORIZATION_CLIENT = "Basic {}".format(encoded.decode('utf-8'))
    ST_EXPECTED_RESPONSE = "unauthorized"

    ST_CONNECTION_ERROR_MSG = QCoreApplication.translate("TransitionalSystemConfig", "There was an error accessing the task service. Details: {}")
    ST_STATUS_500_MSG = QCoreApplication.translate("TransitionalSystemConfig", "There is an error in the task server! (Status: 500)")
    ST_STATUS_GT_500_MSG = QCoreApplication.translate("TransitionalSystemConfig", "A connection could not be established with the server, it is possible that the server is not running.")
    ST_STATUS_401_MSG = QCoreApplication.translate("TransitionalSystemConfig", "Unauthorized client! (Status: 401)")

    TASK_TITLE_TEXT_CSS = "font-size: 11pt;font-weight: bold;color: rgb(54, 54, 54);"  # dark-gray
    TASK_TITLE_SELECTED_TEXT_CSS = "font-size: 11pt;font-weight: bold;color: rgb(236, 236, 236);"  # light-gray, almost white
    TASK_NORMAL_TEXT_CSS = "font-size: 9pt;color: rgb(54, 54, 54);"  # dark-gray
    TASK_NORMAL_SELECTED_TEXT_CSS = "font-size: 9pt;color: rgb(236, 236, 236);"  # light-gray, almost white
    TASK_DATE_TEXT_CSS = "font-size: 8pt;font-style: italic;color: rgb(125, 125, 125);"  # gray
    TASK_DATE_SELECTED_TEXT_CSS = "font-size: 8pt;font-style: italic;color: rgb(187, 187, 187);"  # light-gray
    TASK_ASSIGNED_STATUS_TEXT_CSS = "font-size: 10pt;color: rgb(255, 174, 0);"  # orange
    TASK_STARTED_STATUS_TEXT_CSS = "font-size: 10pt;color: rgb(90, 170, 78);"  # green
    TASK_STARTED_STATUS_SELECTED_TEXT_CSS = "font-size: 10pt;color: rgb(159, 207, 151);"  # light-green

    TASK_TITLE_BIG_TEXT_CSS = "font-size: 14pt;font-weight: bold;color: rgb(54, 54, 54);"  # dark-gray
    TASK_ASSIGNED_STATUS_BIG_TEXT_CSS = "font-size: 12pt;color: rgb(255, 174, 0);"  # orange
    TASK_STARTED_STATUS_BIG_TEXT_CSS = "font-size: 12pt;color: rgb(79, 157, 66);"  # different-green

    def __init__(self):
        QObject.__init__(self)

    def get_domain(self):
        return QSettings().value('Asistente-LADM-COL/sources/service_transitional_system', self.ST_DEFAULT_DOMAIN)

    @property
    def ST_LOGIN_SERVICE_URL(self):
        return "{}/api/security/oauth/token".format(self.get_domain())

    @property
    def ST_GET_TASKS_SERVICE_URL(self):
        return "{}/api/workspaces/v1/tasks/pending".format(self.get_domain())

    @property
    def ST_START_TASK_SERVICE_URL(self):
        return "{}/api/workspaces/v1/tasks/{{}}/start".format(self.get_domain())

    @property
    def ST_CANCEL_TASK_SERVICE_URL(self):
        return "{}/api/workspaces/v1/tasks/{{}}/cancel".format(self.get_domain())

    @property
    def ST_CLOSE_TASK_SERVICE_URL(self):
        return "{}/api/workspaces/v1/tasks/{{}}/finish".format(self.get_domain())

    @property
    def ST_UPLOAD_FILE_SERVICE_URL(self):
        return "{}/api/workspaces/v1/providers/requests/{{}}".format(self.get_domain())
