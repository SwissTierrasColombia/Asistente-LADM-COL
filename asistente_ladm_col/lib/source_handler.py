import os.path

from qgis.core import QgsProject, QgsDataSourceUri, Qgis
from qgis.gui import QgsMessageBar
from qgis.PyQt.QtCore import (
    QEventLoop,
    QUrl,
    pyqtSignal,
    QObject,
    Qt,
    QTextStream,
    QIODevice,
    QCoreApplication
)
from qgis.PyQt.QtWidgets import QDialog, QProgressBar, QSizePolicy, QGridLayout
from qgis.PyQt.QtNetwork import QNetworkRequest, QNetworkAccessManager
from qgis.PyQt.Qt import QNetworkRequest

from ..gui.upload_progress_dialog import UploadProgressDialog

class SourceHandler(QObject):
    """
    Configure behavior of a form when a feature has just been added on a given
    field, which is expected to have an Attachment widget.
    """

    message_with_duration_emitted = pyqtSignal(str, int, int) # Message, level, duration

    def __init__(self):
        QObject.__init__(self)

    def upload_files(self, layer, field_index, features):
        file_features = [feature for feature in features if os.path.isfile(feature[field_index])]
        total = len(features)
        not_found = total - len(file_features)

        upload_dialog = UploadProgressDialog(len(file_features), not_found)
        upload_dialog.show()
        count = 0
        new_values = dict()

        for feature in file_features:
            data_url = feature[field_index]

            url = 'http://geotux.tuxfamily.org'
            nam = QNetworkAccessManager()
            request = QNetworkRequest(QUrl(url))
            reply = nam.get(request)
            reply.downloadProgress.connect(upload_dialog.update_current_progress)
            #reply.uploadProgress.connect(upload_dialog.update_current_progress)

            # We'll block execution until we get response from the server
            loop = QEventLoop()
            reply.finished.connect(loop.quit)
            loop.exec_()
            print("Event Loop finished!")

            response = reply.readAll()
            data = QTextStream(response, QIODevice.ReadOnly)
            content = data.readAll()
            #print("Content read!", content)
            reply.deleteLater()

            new_values[feature.id()] = {field_index : 'http://stackoverflow.com'}
            print(new_values)

            count += 1
            upload_dialog.update_total_progress(count)

        if not_found > 0:
            self.message_with_duration_emitted.emit(
                QCoreApplication.translate("SourceHandler",
                    "{} out of {} records {} ignored because {} file path couldn't be found in the local disk!").format(
                        not_found,
                        total,
                        QCoreApplication.translate("SourceHandler", 'was') if not_found == 1 else QCoreApplication.translate("SourceHandler", 'were'),
                        QCoreApplication.translate("SourceHandler", 'its') if not_found == 1 else QCoreApplication.translate("SourceHandler", 'their')
                    ),
                Qgis.Warning,
                0)
        if len(new_values):
            self.message_with_duration_emitted.emit(
                QCoreApplication.translate("SourceHandler",
                    "{} out of {} files {} uploaded to the server and {} remote location stored in the database!").format(
                        len(new_values),
                        total,
                        QCoreApplication.translate("SourceHandler", 'was') if len(new_values) == 1 else QCoreApplication.translate("SourceHandler", 'were'),
                        QCoreApplication.translate("SourceHandler", 'its') if len(new_values) == 1 else QCoreApplication.translate("SourceHandler", 'their')
                    ),
                Qgis.Info,
                0)

        return new_values

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
