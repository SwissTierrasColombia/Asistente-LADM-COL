from qgis.PyQt.QtCore import QCoreApplication

"""
For this module use multiline "\" instead of triple double quotes
"""

# Elige esta opción para cargar puntos a la capa <b>Punto Lindero</b> del modelo <i>LADM_COL</i>.
# <br><br>
# <b>Punto Lindero</b> es una clase especializada de <i>LA_Punto</i> que almacena puntos que definen un lindero.
# Lindero es una instancia de la clase <i>LA_BoundaryFaceString</i> y sus especializaciones.
WIZ_ADD_POINTS_CADASTRE_PAGE_1_OPTION_BP = QCoreApplication.translate("HelpStrings", "\
Choose this option to load points to <b>Boundary Points</b> layer from <i>LADM_COL</i> model.\
<br><br>\
<b>Boundary Point</b> is a specialized class of <i>LA_Point</i> which store points that define a boundary.\
Boundary is an instance of <i>LA_BoundaryFaceString</i> class and its specializations.\
")

# Elige esta opción para cargar puntos a la capa <b>Punto Levantamiento</b> del modelo <i>LADM_COL</i>.
# <br><br>
# <b>Punto Levantamiento</b> es una clase especializada de <i>LA_Punto</i> que representa la posición horizontal de un vértice de construcción, servidumbre o auxiliares.
WIZ_ADD_POINTS_CADASTRE_PAGE_1_OPTION_SP = QCoreApplication.translate("HelpStrings", "\
Choose this option to load points to <b>Survey Points</b> layer from <i>LADM_COL</i> model.\
<br><br>\
<b>Survey Point</b> is a specialized class of <i>LA_Point</i> which represents a building, right of way or auxiliary vertex.\
")

# Agrega un archivo de valores separados por coma (CSV) u otros como TSV, seleccionando el delimitador y los campos que contienen las coordenadas de los puntos.
WIZ_ADD_POINTS_CADASTRE_PAGE_2_OPTION_CSV = QCoreApplication.translate("HelpStrings", "\
Add a Comma Separated Values file (CSV) or others like Tab Separated Values (TSV), choosing the delimiter and fields that contains point coordinates.\
")

# Elige esta opción si deseas agregar una <b>Fuente administrativa</b> con un formulario.
# <br><br>
# <b>Fuente administrativa</b> es una Especialización de la clase <i>COL_Fuente</i> para almacenar aquellas fuentes constituidas por documentos (documento hipotecario, documentos notariales, documentos históricos, etc.) que documentan la relación entre instancias de interesados y de predios.
WIZ_CREATE_ADMINISTRATIVE_SOURCE_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to add a <b>Administrative Source</b> with a form.\
<br><br>\
<b>Administrative Source</b> is a specialization of the class <i>COL_Fuente</i> to store those sources constituted by documents (mortgage document, notarial documents, historical documents, etc.) that document the relationship between stakeholders and properties.\
")

# Elige esta opción si deseas agregar una <b>Fuente Administrativa</b> con un recurso externo, como un archivo CSV, una tabla de QGIS, entre otros.
# <br><br>
# <b>Fuente Administrativa</b> es una Especialización de la clase <i>COL_Fuente</i> para almacenar aquellas fuentes constituidas por documentos (documento hipotecario, documentos notariales, documentos históricos, etc.) que documentan la relación entre instancias de interesados y de predios.
WIZ_CREATE_ADMINISTRATIVE_SOURCE_PAGE_1_OPTION_ANOTHER = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to add an <b>Administrative Source</b> with an external resource, such as a CSV file, a QGIS table, etc.\
<br><br>\
<b>Administrative Source</b> is a Specialization of the class <i>COL_Fuente</i> to store those sources constituted by documents (mortgage document, notarial documents, historical documents, etc.) that document the relationship between instances of interested and property.\
")

# Elige esta opción si deseas agregar una <b>Interesado Jurídico</b> con un formulario.
# <br><br>
# <b>Interesado Jurídico</b> es una Persona jurídica que tiene derechos, restricciones o responsabilidades referidas a uno o más predios.
WIZ_CREATE_LEGAL_PARTY_CADASTRE_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to add a <b>Legal Party</b> with with a form.\
<br><br>\
<b>Legal Party</b> is a legal entity that has rights, restrictions or responsibilities related to one or more <i>Parcel</i>.\
")

# Elige esta opción si deseas agregar una <b>Interesado natural</b> con un recurso externo, como un archivo CSV, una tabla de QGIS, entre otros.
# <br><br>
# <b>Interesado natural</b> es una Persona jurídica que tiene derechos, restricciones o responsabilidades referidas a uno o más predios.
WIZ_CREATE_LEGAL_PARTY_CADASTRE_PAGE_1_OPTION_ANOTHER = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to add a <b>Legal Party</b> with an external resource, such as a CSV file, a QGIS table, etc.\
<br><br>\
<b>Legal Party</b> is a legal entity that has rights, restrictions or responsibilities related to one or more <i>Parcel</i>.\
")

# Elige esta opción si deseas agregar una <b>Interesado Natural</b> con un formulario.
# <br><br>
# <b>Interesado Natural</b> es una Persona natural que tiene derechos o a la que le recaen restricciones o responsabilidades referidas a uno o más predios.
WIZ_CREATE_NATURAL_PARTY_CADASTRE_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to add a <b>Natural Party</b> with a form.\
<br><br>\
<b>Natural Party</b> is a natural person who has rights or who is subject to restrictions or responsibilities related to one or more <i>Parcel</i>.\
")

# Elige esta opción si deseas agregar una <b>Interesado Natural</b> con un recurso externo, como un archivo CSV, una tabla de QGIS, entre otros.
# <br><br>
# <b>Interesado Natural</b> es una Persona natural que tiene derechos o a la que le recaen restricciones o responsabilidades referidas a uno o más predios.
WIZ_CREATE_NATURAL_PARTY_CADASTRE_PAGE_1_OPTION_ANOTHER = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to add a <b>Natural Party</b> with an external resource, such as a CSV file, a QGIS table, etc.\
<br><br>\
<b>Natural Party</b> is a natural person who has rights or who is subject to restrictions or responsibilities related to one or more <i>Parcel</i>.\
")

# Elige esta opción si deseas crear un <b>Predio</b> basándose en un <i>Terreno<i> existente.
# <br><br>
# <b>Predio</b> es una Clase especializada de BaUnit, que describe la unidad administrativa básica para el caso de Colombia.
# El predio es la unidad territorial legal propia de Catastro.
# Esta formada por el terreno y puede o no tener construcciones asociadas.
WIZ_CREATE_PARCEL_CADASTRE_PAGE_1_OPTION_EXISTS_PLOT = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Parcel</b> based on an existing plot.\
<br><br>\
<b>Parcel</b> is a specialized BaUnit Class, which describes the basic administrative unit for the case of Colombia.\
The property is the legal territorial unit of Cadastre.\
It is formed by the terrain and may or may not have associated constructions.\
")

# Elige esta opción si deseas crear un <b>Predio</b> sin una geometría asociada.
# <br><br>
# <b>Predio</b> es una Clase especializada de BaUnit, que describe la unidad administrativa básica para el caso de Colombia.
# El predio es la unidad territorial legal propia de Catastro.
# Esta formada por el terreno y puede o no tener construcciones asociadas.
WIZ_CREATE_PARCEL_CADASTRE_PAGE_1_OPTION_WITHOUT_GEOM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Parcel</b> without geometry.\
<br><br>\
<b>Parcel</b> is a specialized BaUnit Class, which describes the basic administrative unit for the case of Colombia.\
The property is the legal territorial unit of Cadastre.\
It is formed by the terrain and may or may not have associated constructions.\
")

# Elige esta opción si deseas crear un <b>Predio</b> desde un recurso externo, como un archivo CSV, una tabla de QGIS, entre otros.
# <br><br>
# <b>Predio</b> es una Clase especializada de BaUnit, que describe la unidad administrativa básica para el caso de Colombia.
# El predio es la unidad territorial legal propia de Catastro.
# Esta formada por el terreno y puede o no tener construcciones asociadas.
WIZ_CREATE_PARCEL_CADASTRE_PAGE_1_OPTION_ANOTHER = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Parcel</b> from external resource, such as a CSV file, a QGIS table, etc.\
<br><br>\
<b>Parcel</b> is a specialized BaUnit Class, which describes the basic administrative unit for the case of Colombia.\
The property is the legal territorial unit of Cadastre.\
It is formed by the terrain and may or may not have associated constructions.\
")

# Elige esta opción si deseas crear un <b>Terreno</b> a partir de una capa re-factorizada.
# <br><br>
# <b>Terreno</b> es una porción de tierra con una extensión geográfica definida.
WIZ_CREATE_PLOT_CADASTRE_PAGE_1_OPTION_RLAYER = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Plot</b> from a re-factored layer.\
<br><br>\
<b>Plot</b> is a portion of land with a defined geographical extension.\
")

# Elige esta opción si deseas crear un <b>Terreno</b> a partir de <i>Límites</i> existentes.
# <br><br>
# <b>Terreno</b> es una porción de tierra con una extensión geográfica definida.
WIZ_CREATE_PLOT_CADASTRE_PAGE_1_OPTION_BOUNDARIES = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Plot</b> from existing <i>Boundaries</i>.\
<br><br>\
<b>Plot</b> is a portion of land with a defined geographical extension.\
")

# Seleccione la capa de <b>Terreno</b> de las disponibles en el proyecto de QGIS.
WIZ_CREATE_PLOT_CADASTRE_PAGE_2 = QCoreApplication.translate("HelpStrings", "\
Select the <b>Plot</ b> layer from those available in the QGIS project.\
")

# Elige esta opción si deseas agregar una <b>Responsabilidad</b> con un formulario.
# <br><br>
# <b>COL_Responsabilidad</b> es una clase de tipo <i>LA_RRR</i> que registra las responsabilidades que las instancias de los interesados tienen sobre los predios.
WIZ_CREATE_RESPONSIBILITY_CADASTRE_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to add a <b>Responsibility</b> with a form.\
<br><br>\
<b>COL_Responsibility</b> is a class of type <i>LA_RRR</i> that records the responsibilities that stakeholders have on the premises.\
")

# Elige esta opción si deseas agregar una <b>Responsabilidad</b> desde un recurso externo, como un archivo CSV, una tabla de QGIS, entre otros.
# <br><br>
# <b>COL_Responsabilidad</b> es una clase de tipo <i>LA_RRR</i> que registra las responsabilidades que las instancias de los interesados tienen sobre los predios.
WIZ_CREATE_RESPONSIBILITY_CADASTRE_PAGE_1_OPTION_ANOTHER = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to add a <b>Responsibility</b> from external resource, such as a CSV file, a QGIS table, etc..\
<br><br>\
<b>COL_Responsibility</b> is a class of type <i>LA_RRR</i> that records the responsibilities that stakeholders have on the premises.\
")


#
WIZ_CREATE_RESTRICTION_CADASTRE_PAGE_1_OPTION_ = QCoreApplication.translate("HelpStrings", "\
\
")

#
WIZ_CREATE_RIGHT_CADASTRE_PAGE_1_OPTION_ = QCoreApplication.translate("HelpStrings", "\
\
")

#
WIZ_CREATE_SPATIAL_SOURCE_CADASTRE_PAGE_1_OPTION_ = QCoreApplication.translate("HelpStrings", "\
\
")

#
WIZ_DEFINE_BOUNDARIES_CADASTRE_PAGE_1_OPTION_ = QCoreApplication.translate("HelpStrings", "\
\
")
