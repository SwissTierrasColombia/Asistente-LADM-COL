import os

from qgis.PyQt.QtCore import QEventLoop, QUrl, pyqtSignal, QObject
from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt.QtNetwork import QNetworkRequest, QNetworkAccessManager
from qgis.PyQt.Qt import QNetworkRequest

class SourceHandler(QObject):
    """
    Configure behavior of a form when a feature has just been added on a given
    field, which is expected to have an Attachment widget.
    """

    response_ready = pyqtSignal()

    def __init__(self, iface):
        QObject.__init__(self)
        self.iface = iface

    def handle_source_upload(self, layer, field_name):
        index = layer.fields().indexFromName(field_name)

        def fetchResource(url):
            request = QNetworkRequest(QUrl(url))
            nam.get(request)

        def request_finished(reply):
            reDir = reply.attribute(QNetworkRequest.RedirectionTargetAttribute)
            if reDir is not None:
                if reDir.isRelative():
                    reDir = reply.url().resolved(reDir)
                if not reDir.isEmpty():
                    print("Redirecting to {}...".format(reDir.url()))
                    fetchResource(reDir.url())
                    return

            print("Finished with code ", reply.attribute(QNetworkRequest.HttpStatusCodeAttribute))
            self.response_ready.emit()
            # allData = reply.readAll()
            # response = QTextStream(allData, QIODevice.ReadOnly)
            # data = response.readAll()

        nam = QNetworkAccessManager()
        nam.finished.connect(request_finished)
        url = 'http://geotux.co'

        def feature_added(fid):
            # Upload to server and get returner id (URL)
            dialogs = self.iface.mainWindow().findChildren(QDialog, 'featureactiondlg:{}:0'.format(layer.id()))
            if len(dialogs) == 1:
                dialogs[0].setEnabled(False) # Prevent the user to click Ok again

                # We'll block execution until we get response from the server
                event_loop = QEventLoop()
                self.response_ready.connect(event_loop.quit)
                fetchResource(url)
                event_loop.exec_()
                print("Event Loop finished!")

                layer.editBuffer().changeAttributeValue(fid, index, 'http://stackoverflow.com')
                dialogs[0].setEnabled(True)
            else:
                # This might happen if the user has opened two feature forms
                pass

        layer.featureAdded.connect(feature_added)
