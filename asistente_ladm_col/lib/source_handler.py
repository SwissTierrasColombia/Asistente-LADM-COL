import os.path

from qgis.gui import QgsMessageBar
from qgis.PyQt.QtCore import (
    QEventLoop,
    QUrl,
    pyqtSignal,
    QObject,
    Qt,
    QTextStream,
    QIODevice
)
from qgis.PyQt.QtWidgets import QDialog, QProgressBar, QSizePolicy, QGridLayout
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

        def feature_added(fid):
            features = layer.editBuffer().addedFeatures()
            if fid in features:
                feature = features[fid]
                data_url = feature[index]
                if not os.path.isfile(data_url):
                    print("Value entered into field 'datos' is not a file! Therefore, it wasn't uploaded to the server.")
                    return

                # Upload to server and get returner id (URL)
                dialogs = self.iface.mainWindow().findChildren(QDialog, 'featureactiondlg:{}:0'.format(layer.id()))
                if len(dialogs) == 1:
                    dlg = dialogs[0]

                    bar = QgsMessageBar()
                    bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
                    dlg.setLayout(QGridLayout())
                    dlg.layout().addWidget(bar, 0, 0, Qt.AlignTop)

                    widget = self.iface.messageBar().createMessage("Asistente LADM_COL","Uploading file...")
                    progress_bar = QProgressBar()
                    widget.layout().addWidget(progress_bar)
                    bar.pushWidget(widget, 0, 0)

                    dlg.setEnabled(False) # Prevent the user from clicking Ok again

                    def update_progress(current, total):
                        print(current, total)
                        if total == 0 and current == 0 or total == -1:
                            progress_bar.setRange(0, 0)
                        elif total > 0:
                            progress_bar.setRange(0, 100)
                            progress_bar.setValue(100 * current/total)

                    url = 'http://geotux.tuxfamily.org'
                    nam = QNetworkAccessManager()
                    request = QNetworkRequest(QUrl(url))
                    reply = nam.get(request)
                    reply.downloadProgress.connect(update_progress)
                    reply.uploadProgress.connect(update_progress)

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

                    layer.editBuffer().changeAttributeValue(fid, index, 'http://stackoverflow.com')
                    dlg.setEnabled(True)
                else:
                    # This might happen if the user has opened two feature forms
                    print("More than one feature form dialog found!")
            else:
                # This might happen if the feature is being added from attr table
                print("Feature not found in edit buffer!")

        layer.featureAdded.connect(feature_added)
