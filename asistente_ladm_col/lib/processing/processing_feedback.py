from qgis.core import QgsProcessingFeedback
from asistente_ladm_col.lib.logger import Logger

class MyFeedBack(QgsProcessingFeedback):

    def setProgressText(self, text):
        Logger().status(text.strip('Running ').split(' [')[0].strip())

    """def pushInfo(self, info):
        print(info)

    def pushCommandInfo(self, info):
        print(info)

    def pushDebugInfo(self, info):
        print(info)

    def pushConsoleInfo(self, info):
        print(info)

    def reportError(self, error, fatalError=False):
        print(error)"""