import json
import requests

from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication)

from asistente_ladm_col.config.transition_system_config import TransitionSystemConfig
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.transition_system.st_session.st_session import STSession


class STUtils(QObject):

    def __init__(self):
        QObject.__init__(self)
        self.logger = Logger()
        self.st_session = STSession()
        self.st_config = TransitionSystemConfig()

    def upload_file(self, request_id, supply_type, file_path, comments):
        url = self.st_config.ST_UPLOAD_FILE_SERVICE_URL.format(request_id)

        payload = {'typeSupplyId': supply_type,
                   'observations': comments}
        files = [
            ('files[]', open(file_path, 'rb'))
        ]
        headers = {
            'Authorization': "Bearer {}".format(self.st_session.get_logged_st_user().get_token())
        }

        try:
            self.logger.debug(__name__, "Uploading file to transition system...")
            response = requests.request("PUT", url, headers=headers, data=payload, files=files)
        except requests.ConnectionError as e:
            msg = QCoreApplication.translate("STUtils", "There was an error accessing the upload file service. Details: {}".format(e))
            self.logger.warning(__name__, msg)
            return False, msg

        status_OK = response.status_code == 200
        response_data = json.loads(response.text)
        if status_OK:
            msg = QCoreApplication.translate("STUtils", "The file was successfully uploaded to the Transition System!")
            self.logger.success(__name__, msg)
        else:
             if response.status_code == 500:
                msg = QCoreApplication.translate("STUtils", "There is an error in the Transition System server! Message from server: '{}'".format(response_data["message"]))
                self.logger.warning(__name__, msg)
             elif response.status_code == 401:
                msg = QCoreApplication.translate("STUtils", "Unauthorized client!")
                self.logger.warning(__name__, msg)

        return status_OK, msg
