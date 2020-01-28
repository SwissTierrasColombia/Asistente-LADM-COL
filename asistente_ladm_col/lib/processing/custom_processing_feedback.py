from qgis.core import QgsProcessingFeedback
from asistente_ladm_col.lib.logger import Logger

class CustomFeedback(QgsProcessingFeedback):

    def setProgressText(self, text):
        """
        Format message to print the description of processes in a model.

        :param text: Original message corresponding to a description in a Model process
        """
        Logger().status(text.strip('Running').split(' [')[0].strip())