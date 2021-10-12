import json
import os
import shutil
import tempfile
import zipfile

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

    def download_file(self, file_url, file_path):
        self.logger.debug(__name__, "Downloading file from ST server ('{}') into '{}'...".format(file_url, file_path))

        headers = {
            'Authorization': "Bearer {}".format(self.st_session.get_logged_st_user().get_token()),
            # 'User-Agent': "PostmanRuntime/7.20.1",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            # 'Postman-Token': "987c7fbf-af4d-42e8-adee-687f35f4a4a0,0547120a-6f8e-42a8-b97f-f052602cc7ff",
            # 'Host': "st.local:8090",
            'Accept-Encoding': "gzip, deflate",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }

        # Download it
        tmpFile = tempfile.mktemp()
        try:
            with requests.request("GET", file_url, headers=headers, stream=True) as response:
                response.raise_for_status()  # Only throws error on 4xx and 5xx codes
                with open(tmpFile, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=self.st_config.DEFAULT_CHUNK_SIZE):
                        f.write(chunk)
        except requests.ConnectionError as e:
            msg = self.st_config.ST_CONNECTION_ERROR_MSG.format(e)
            self.logger.warning(__name__, msg)
            return False, msg
        except requests.exceptions.HTTPError as e:
            if response.status_code == 500:
                msg = self.st_config.ST_STATUS_500_MSG
            elif 500 < response.status_code < 600:
                msg = self.st_config.ST_STATUS_GT_500_MSG
            elif response.status_code == 401:
                msg = self.st_config.ST_STATUS_401_MSG
            else:
                msg = self.st_config.ST_GENERIC_ERROR_MSG.format(e)

            self.logger.warning(__name__, msg)
            return False, msg
        except SSLError as e:
            return False, QCoreApplication.translate("STUtils", "There was a problem downloading the file. Try it again! Details: {}").format(e)

        # Now unzip it
        tmpFolder = tempfile.mktemp()
        res = False
        msg = ""
        try:
            with zipfile.ZipFile(tmpFile, "r") as zip_ref:
                if len(zip_ref.filelist) == 1:
                    member = zip_ref.filelist[0].filename
                    if os.path.splitext(member)[1] == os.path.splitext(file_path)[1]:
                        zip_ref.extract(member, tmpFolder)
                        shutil.move(os.path.join(tmpFolder, member), file_path)
                        res = True
                        msg = "Success!"
                    else:
                        msg = QCoreApplication.translate("STUtils",
                                                         "The file inside the ZIP file does not have the proper extension ({})").format(
                            os.path.splitext(file_path)[1]
                        )
                else:
                    msg = QCoreApplication.translate("STUtils",
                                                     "There should be only one file inside the downloaded ZIP file!")
        except zipfile.BadZipFile as e:
            msg = QCoreApplication.translate("STUtils",
                                             "There was an error with the download. The downloaded file is invalid.")

        try:
            os.remove(tmpFile)
            os.remove(tmpFolder)
        except:
            pass

        return res, msg

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
