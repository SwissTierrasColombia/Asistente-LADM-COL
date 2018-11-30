# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-06-09
        git sha              : :%H$
        copyright            : (C) 2018 by Germán Carrillo (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
import json
import os.path

from qgis.PyQt.Qt import QNetworkRequest
from qgis.PyQt.QtCore import (QEventLoop,
                              QUrl,
                              pyqtSignal,
                              QObject,
                              QTextStream,
                              QIODevice,
                              QCoreApplication,
                              QFile,
                              QVariant,
                              QByteArray,
                              QSettings)
from qgis.PyQt.QtNetwork import (QNetworkAccessManager,
                                 QHttpMultiPart,
                                 QHttpPart)
from qgis.core import (QgsProject,
                       QgsDataSourceUri,
                       Qgis,
                       QgsApplication)

from ..config.general_config import (DEFAULT_ENDPOINT_SOURCE_SERVICE,
                                     PLUGIN_NAME,
                                     SOURCE_SERVICE_UPLOAD_SUFFIX)
from ..gui.upload_progress_dialog import UploadProgressDialog


class SourceHandler(QObject):
    """
    Upload source files from a given field of a layer to a remote server that
    is configured in Settings Dialog. The server returns a file URL that is
    then stored in the source table.
    """

    message_with_duration_emitted = pyqtSignal(str, int, int) # Message, level, duration

    def __init__(self, qgis_utils):
        QObject.__init__(self)
        self.log = QgsApplication.messageLog()
        self.qgis_utils = qgis_utils

    def upload_files(self, layer, field_index, features):
        """
        Upload given features' source files to remote server and return a dict
        formatted as changeAttributeValues expects to update 'datos' attribute
        to a remote location.
        """
        # First test if we have Internet connection and a valid service
        dlg = self.qgis_utils.get_settings_dialog()
        res, msg = dlg.is_source_service_valid()
        if not res:
            msg['text'] = QCoreApplication.translate("SourceHandler",
                "No file could be uploaded to the server. You can do it later from the 'Upload Pending Source Files' menu. Reason: {}".format(msg['text']))
            self.message_with_duration_emitted.emit(
                msg['text'],
                msg['level'],
                20)
            return dict()

        file_features = [feature for feature in features if os.path.isfile(feature[field_index])]
        total = len(features)
        not_found = total - len(file_features)

        upload_dialog = UploadProgressDialog(len(file_features), not_found)
        upload_dialog.show()
        count = 0
        upload_errors = 0
        new_values = dict()

        for feature in file_features:
            data_url = feature[field_index]
            file_name = os.path.basename(data_url)

            nam = QNetworkAccessManager()
            #reply.downloadProgress.connect(upload_dialog.update_current_progress)

            multiPart = QHttpMultiPart(QHttpMultiPart.FormDataType)
            textPart = QHttpPart()
            textPart.setHeader(QNetworkRequest.ContentDispositionHeader, QVariant("form-data; name=\"driver\""))
            textPart.setBody(QByteArray().append('Local'))

            filePart = QHttpPart()
            filePart.setHeader(QNetworkRequest.ContentDispositionHeader, QVariant("form-data; name=\"file\"; filename=\"{}\"".format(file_name)))
            file = QFile(data_url)
            file.open(QIODevice.ReadOnly)

            filePart.setBodyDevice(file)
            file.setParent(multiPart)  # we cannot delete the file now, so delete it with the multiPart

            multiPart.append(filePart)
            multiPart.append(textPart)

            service_url = '/'.join([
                QSettings().value('Asistente-LADM_COL/source/service_endpoint', DEFAULT_ENDPOINT_SOURCE_SERVICE),
                SOURCE_SERVICE_UPLOAD_SUFFIX])
            request = QNetworkRequest(QUrl(service_url))
            reply = nam.post(request, multiPart)
            #reply.uploadProgress.connect(upload_dialog.update_current_progress)
            reply.error.connect(self.error_returned)
            multiPart.setParent(reply)

            # We'll block execution until we get response from the server
            loop = QEventLoop()
            reply.finished.connect(loop.quit)
            loop.exec_()

            response = reply.readAll()
            data = QTextStream(response, QIODevice.ReadOnly)
            content = data.readAll()

            if content is None:
                self.log.logMessage("There was an error uploading file '{}'".format(data_url), PLUGIN_NAME, Qgis.Critical)
                upload_errors += 1
                continue

            try:
                response = json.loads(content)
            except json.decoder.JSONDecodeError:
                self.log.logMessage("Couldn't parse JSON response from server for file '{}'!!!".format(data_url), PLUGIN_NAME, Qgis.Critical)
                upload_errors += 1
                continue

            if 'error' in response:
                self.log.logMessage("STATUS: {}. ERROR: {} MESSAGE: {} FILE: {}".format(
                        response['status'],
                        response['error'],
                        response['message'],
                        data_url),
                    PLUGIN_NAME, Qgis.Critical)
                upload_errors += 1
                continue

            reply.deleteLater()

            if 'url' not in response:
                self.log.logMessage("'url' attribute not found in JSON response for file '{}'!".format(data_url), PLUGIN_NAME, Qgis.Critical)
                upload_errors += 1
                continue

            url = self.get_file_url(response['url'])
            new_values[feature.id()] = {field_index : url}

            count += 1
            upload_dialog.update_total_progress(count)

        if not_found > 0:
            self.message_with_duration_emitted.emit(
                QCoreApplication.translate("SourceHandler",
                    "{} out of {} records {} ignored because {} file path couldn't be found in the local disk!").format(
                        not_found,
                        total,
                        QCoreApplication.translate("SourceHandler", "was") if not_found == 1 else QCoreApplication.translate("SourceHandler", "were"),
                        QCoreApplication.translate("SourceHandler", "its") if not_found == 1 else QCoreApplication.translate("SourceHandler", "their")
                    ),
                Qgis.Warning,
                0)
        if len(new_values):
            self.message_with_duration_emitted.emit(
                QCoreApplication.translate("SourceHandler",
                    "{} out of {} files {} uploaded to the server and {} remote location stored in the database!").format(
                        len(new_values),
                        total,
                        QCoreApplication.translate("SourceHandler", "was") if len(new_values) == 1 else QCoreApplication.translate("SourceHandler", "were"),
                        QCoreApplication.translate("SourceHandler", "its") if len(new_values) == 1 else QCoreApplication.translate("SourceHandler", "their")
                    ),
                Qgis.Info,
                0)
        if upload_errors:
            self.message_with_duration_emitted.emit(
                QCoreApplication.translate("SourceHandler",
                    "{} out of {} files could not be uploaded to the server because of upload errors! See log for details.").format(
                        upload_errors,
                        total
                    ),
                Qgis.Warning,
                0)

        return new_values

    def error_returned(self, error_code):
        self.log.logMessage("Qt network error code: {}".format(error_code), PLUGIN_NAME, Qgis.Critical)

    def handle_source_upload(self, layer, field_name):
        field_index = layer.fields().indexFromName(field_name)

        def features_added(layer_id, features):
            modified_layer = QgsProject.instance().mapLayer(layer_id)
            if modified_layer is None or QgsDataSourceUri(modified_layer.source()).table().lower() != layer.name().lower():
                return

            new_values = self.upload_files(modified_layer, field_index, features)
            if new_values:
                modified_layer.dataProvider().changeAttributeValues(new_values)

        layer.committedFeaturesAdded.connect(features_added)

    def get_file_url(self, part):
        endpoint = QSettings().value('Asistente-LADM_COL/source/service_endpoint', DEFAULT_ENDPOINT_SOURCE_SERVICE)
        return '/'.join([endpoint, part[1:] if part.startswith('/') else part])
