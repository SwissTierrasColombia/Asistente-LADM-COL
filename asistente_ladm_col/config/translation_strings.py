from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication)
from asistente_ladm_col.config.enums import EnumQualityRuleType
from asistente_ladm_col.config.general_config import (COLLECTED_DB_SOURCE,
                                                      SUPPLIES_DB_SOURCE)

ERROR_LAYER_GROUP_PREFIX = "ERROR_LAYER_GROUP_PREFIX"
RIGHT_OF_WAY_LINE_LAYER = "RIGHT_OF_WAY_LINE_LAYER"

TOOLBAR_BUILD_BOUNDARY = QCoreApplication.translate("TranslatableConfigStrings", "Build boundaries...")
TOOLBAR_MOVE_NODES = QCoreApplication.translate("TranslatableConfigStrings", "Move nodes...")
TOOLBAR_FILL_POINT_BFS = QCoreApplication.translate("TranslatableConfigStrings", "Fill Point BFS")
TOOLBAR_FILL_MORE_BFS_LESS = QCoreApplication.translate("TranslatableConfigStrings", "Fill More BFS and Less")
TOOLBAR_FILL_RIGHT_OF_WAY_RELATIONS = QCoreApplication.translate("TranslatableConfigStrings", "Fill Right of Way Relations")
TOOLBAR_IMPORT_FROM_INTERMEDIATE_STRUCTURE = QCoreApplication.translate("TranslatableConfigStrings", "Import from intermediate structure")
TOOLBAR_FINALIZE_GEOMETRY_CREATION = QCoreApplication.translate("TranslatableConfigStrings", "Finalize geometry creation")


class TranslatableConfigStrings(QObject):
    help_get_domain_code_from_value = QCoreApplication.translate("TranslatableConfigStrings", "Gets the t_id that corresponds to a domain value") + \
                                         QCoreApplication.translate("TranslatableConfigStrings", "<h4>Syntax</h4>") + \
                                         "<span class=\"functionname\">get_domain_code_from_value</span>(" \
                                         "<span class=\"argument\">domain_table</span>, " \
                                         "<span class=\"argument\">value</span>, " \
                                         "<span class=\"argument\">value_is_ilicode</span>, " \
                                         "<span class=\"argument\">validate_conn</span>)" + \
                                         QCoreApplication.translate("TranslatableConfigStrings", "<h4>Arguments</h4>") + \
                                         "<span class=\"argument\">domain_table</span> " + QCoreApplication.translate("TranslatableConfigStrings", "Domain table name or layer obj") + \
                                         "<br><span class=\"argument\">value</span> " + QCoreApplication.translate("TranslatableConfigStrings", "Domain value to look for") + \
                                         "<br><span class=\"argument\">value_is_ilicode</span> " + QCoreApplication.translate("TranslatableConfigStrings", "Whether value is iliCode or dispName") + \
                                         "<br><span class=\"argument\">validate_conn</span> " + QCoreApplication.translate("TranslatableConfigStrings", "Whether validate connection or not") + \
                                         QCoreApplication.translate("TranslatableConfigStrings", "<h4>Examples</h4>") + \
                                         """<pre>get_domain_code_from_value( 
  'lc_condicionprediotipo',
  'NPH',
  True,
  False) → {}</pre>""".format(QCoreApplication.translate("TranslatableConfigStrings", "Gets the t_id of NPH in\n  domain lc_condicionprediotipo"))

    help_get_default_basket = QCoreApplication.translate("TranslatableConfigStrings",
                                                       "Gets the t_id of the default basket in the current DB. This function creates the basket if it does not exist yet. If the DB does not support baskets, it returns None.") + \
                                      QCoreApplication.translate("TranslatableConfigStrings", "<h4>Syntax</h4>") + \
                                      "<span class=\"functionname\">get_default_basket()</span>" + \
                                      QCoreApplication.translate("TranslatableConfigStrings", "<h4>Examples</h4>") + \
                                      """<pre>get_default_basket() → {}</pre>""".format(QCoreApplication.translate("TranslatableConfigStrings",
                                                       "\nGets the t_id of\nthe default basket"))

    help_get_multi_domain_code_from_value = QCoreApplication.translate("TranslatableConfigStrings", "Gets the t_id that corresponds to a (child) domain value") + \
                                      QCoreApplication.translate("TranslatableConfigStrings", "<h4>Syntax</h4>") + \
                                      "<span class=\"functionname\">get_multi_domain_code_from_value</span>(" \
                                      "<span class=\"argument\">domain_table</span>, " \
                                      "<span class=\"argument\">value</span>, " \
                                      "<span class=\"argument\">child_domain_table</span>)" +  \
                                      QCoreApplication.translate("TranslatableConfigStrings", "<h4>Arguments</h4>") + \
                                      "<span class=\"argument\">domain_table</span> " + QCoreApplication.translate(
        "TranslatableConfigStrings", "Domain table name or layer obj") + \
                                      "<br><span class=\"argument\">value</span> " + QCoreApplication.translate(
        "TranslatableConfigStrings", "Domain value to look for") + \
                                      "<br><span class=\"argument\">child_domain_table</span> " + QCoreApplication.translate(
        "TranslatableConfigStrings", "Name of the child domain to disambiguate with other duplicated ilicodes from other models") + \
                                      QCoreApplication.translate("TranslatableConfigStrings", "<h4>Examples</h4>") + \
                                      """<pre>get_multi_domain_code_from_value( 
  'col_fuenteadministrativatipo',
  'Documento_Publico.Acto_Administrativo',
  'Ambiente_V0_1.MA_FuenteAdministrativaTipo')<br> → {}</pre>""".format(QCoreApplication.translate("TranslatableConfigStrings",
                                                         "Gets the t_id of Acto_Administrativo in\n  domain col_fuenteadministrativatipo\n and child domain MA_FuenteAdministrativaTipo."))

    def __init__(self):
        pass

    @staticmethod
    def tr_db_source(source):
        if source == COLLECTED_DB_SOURCE:
            return QCoreApplication.translate("TranslatableConfigStrings", "COLLECTED")
        elif source == SUPPLIES_DB_SOURCE:
            return QCoreApplication.translate("TranslatableConfigStrings", "SUPPLIES")

    @staticmethod
    def get_translatable_config_strings():
        return {
            ERROR_LAYER_GROUP_PREFIX: QCoreApplication.translate("TranslatableConfigStrings", "Quality errors"),
            RIGHT_OF_WAY_LINE_LAYER: QCoreApplication.translate("TranslatableConfigStrings", "Right of way line"),
            EnumQualityRuleType.GENERIC: QCoreApplication.translate("TranslatableConfigStrings", "Generic quality rules"),
            EnumQualityRuleType.POINT: QCoreApplication.translate("TranslatableConfigStrings", "Point quality rules"),
            EnumQualityRuleType.LINE: QCoreApplication.translate("TranslatableConfigStrings", "Line quality rules"),
            EnumQualityRuleType.POLYGON: QCoreApplication.translate("TranslatableConfigStrings", "Polygon quality rules"),
            EnumQualityRuleType.LOGIC: QCoreApplication.translate("TranslatableConfigStrings", "Logic quality rules")
        }
