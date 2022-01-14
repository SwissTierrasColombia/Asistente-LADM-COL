from qgis.PyQt.QtCore import QCoreApplication

from asistente_ladm_col import Logger


class WizardMessagesManager:

    def __init__(self, wizard_tool_name, editing_layer_name):
        self.__WIZARD_TOOL_NAME = wizard_tool_name
        self.__logger = Logger()
        self.__editing_layer_name = editing_layer_name

    def show_wizard_closed_msg(self):
        message = QCoreApplication.translate(
            "WizardTranslations", "'{}' tool has been closed.").format(self.__WIZARD_TOOL_NAME)
        self.__logger.info_msg(__name__, message)

    def show_form_closed_msg(self):
        message = QCoreApplication.translate(
            "WizardTranslations", "'{}' tool has been closed because you just closed the form.")\
            .format(self.__WIZARD_TOOL_NAME)
        self.__logger.info_msg(__name__, message)

    def show_map_tool_changed_msg(self):
        message = QCoreApplication.translate(
            "WizardTranslations", "'{}' tool has been closed because the map tool change.")\
            .format(self.__WIZARD_TOOL_NAME)
        self.__logger.info_msg(__name__, message)

    def show_layer_removed_msg(self):
        message = QCoreApplication.translate(
            "WizardTranslations", "'{}' tool has been closed because you just removed a required layer.")\
            .format(self.__WIZARD_TOOL_NAME)
        self.__logger.info_msg(__name__, message)

    def show_feature_successfully_created_msg(self, feature_name, feature_id):
        message = QCoreApplication.translate(
                "WizardTranslations", "The new {} (t_id={}) was successfully created ")\
                .format(feature_name, feature_id)

        self.__logger.info_msg(__name__, message)

    def show_feature_not_found_in_layer_msg(self):
        message = QCoreApplication.translate(
            "WizardTranslations",
            "'{}' tool has been closed. Feature not found in layer {}... It's not possible create it.") \
            .format(self.__WIZARD_TOOL_NAME, self.__editing_layer_name)

        self.__logger.info_msg(__name__, message)

    def show_feature_not_found_in_layer_warning(self):
        self.__logger.warning(__name__, "Feature not found in layer {} ...".format(self.__editing_layer_name))

    def show_select_a_source_layer_warning(self):
        message = QCoreApplication.translate(
            "WizardTranslations", "Select a source layer to set the field mapping to '{}'.") \
            .format(self.__editing_layer_name)
        self.__logger.warning_msg(__name__, message)
