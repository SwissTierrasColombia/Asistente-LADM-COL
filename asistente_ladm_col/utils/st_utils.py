import json
import requests

from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication)

from asistente_ladm_col.config.transitional_system_config import TransitionalSystemConfig
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.transitional_system.st_session.st_session import STSession


class STUtils(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.logger = Logger()
        self.st_session = STSession()
        self.st_config = TransitionalSystemConfig()

    def upload_files(self, url, other_params, files, comments):
        self.logger.debug(__name__, "Preparing PUT request ({}, {}, number of files: {}, {})".format(
            url,
            other_params,
            len(files),
            comments))

        payload = {'observations': comments}
        payload.update(other_params)

        headers = {
            'Authorization': "Bearer {}".format(self.st_session.get_logged_st_user().get_token())
        }

        msg = ""
        try:
            self.logger.debug(__name__, "Uploading files to transitional system...")
            response = requests.request("PUT", url, headers=headers, data=payload, files=files)
        except requests.ConnectionError as e:
            msg = self.st_config.ST_CONNECTION_ERROR_MSG.format(e)
            self.logger.warning(__name__, msg)
            return False, msg

        status_ok = response.status_code == 200
        if status_ok:
            msg = QCoreApplication.translate("STUtils", "The file was successfully uploaded to the Transitional System!")
            self.logger.success(__name__, msg)
        else:
            if response.status_code == 500:
                msg = self.st_config.ST_STATUS_500_MSG
                self.logger.warning(__name__, self.st_config.ST_STATUS_500_MSG)
            elif response.status_code > 500 and response.status_code < 600:
                msg = self.st_config.ST_STATUS_GT_500_MSG
                self.logger.warning(__name__, self.st_config.ST_STATUS_GT_500_MSG)
            elif response.status_code == 401:
                msg = self.st_config.ST_STATUS_401_MSG
                self.logger.warning(__name__, self.st_config.ST_STATUS_401_MSG)
            elif response.status_code == 422:
                 response_data = json.loads(response.text)
                 msg = QCoreApplication.translate("STUtils", "File was not uploaded! Details: {}").format(response_data['message'])
                 self.logger.warning(__name__, msg)
            else:
                msg = QCoreApplication.translate("STUtils", "Status code not handled: {}").format(response.status_code)
                self.logger.warning(__name__, msg)

        return status_ok, msg
