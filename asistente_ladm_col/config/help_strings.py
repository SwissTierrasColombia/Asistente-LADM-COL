from qgis.PyQt.QtCore import QCoreApplication

# Elige esta opción para cargar puntos a la capa <b>Punto Lindero</b> del modelo <i>LADM_COL</i>.<br><br><b>Punto Lindero</b> es una clase especializada de <i>LA_Punto</i> que almacena puntos que definen un lindero.Lindero es una instancia de la clase <i>LA_BoundaryFaceString</i> y sus especializaciones.
WIZ_ADD_POINTS_CADASTRE_PAGE_1_OPTION_BP = QCoreApplication.translate("HelpStrings", "\
Choose this option to load points to <b>Boundary Points</b> layer from <i>LADM_COL</i> model.\
<br><br>\
<b>Boundary Point</b> is a specialized class of <i>LA_Point</i> which store points that define a boundary.\
Boundary is an instance of <i>LA_BoundaryFaceString</i> class and its specializations.\
")

# Elige esta opción para cargar puntos a la capa <b>Punto Levantamiento</b> del modelo <i>LADM_COL</i>.<br><br><b>Punto Levantamiento</b> es una clase especializada de <i>LA_Punto</i> que representa la posición horizontal de un vértice de construcción, servidumbre o auxiliares.
WIZ_ADD_POINTS_CADASTRE_PAGE_1_OPTION_SP = QCoreApplication.translate("HelpStrings", "\
Choose this option to load points to <b>Survey Points</b> layer from <i>LADM_COL</i> model.\
<br><br>\
<b>Survey Point</b> is a specialized class of <i>LA_Point</i> which represents a building, right of way or auxiliary vertex.\
")

# Agrega un archivo de valores separados por coma (CSV) u otros como TSV, seleccionando el delimitador y los campos que contienen las coordenadas de los puntos.
WIZ_ADD_POINTS_CADASTRE_PAGE_2_OPTION_CSV = QCoreApplication.translate("HelpStrings", """
Add a Comma Separated Values file (CSV) or others like Tab Separated Values (TSV), choosing the delimiter and fields that contains point coordinates.
""")
