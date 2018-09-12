from qgis.PyQt.QtCore import QCoreApplication, QObject

# For this module use multiline "\" instead of triple double quotes

class HelpStrings(QObject):
    def __init__(self):

        self.WIZ_ADD_POINTS_CADASTRE_PAGE_1_OPTION_BP = QCoreApplication.translate("HelpStrings", "\
Choose this option to load points to <b>Boundary Points</b> layer from <i>LADM_COL</i> model.\
<br><br>\
<b>Boundary Point</b> is a specialized class of <i>LA_Point</i> which stores points that define a boundary.\
Boundary is an instance of <i>LA_BoundaryFaceString</i> class and its specializations.\
")

        self.WIZ_ADD_POINTS_CADASTRE_PAGE_1_OPTION_SP = QCoreApplication.translate("HelpStrings", "\
Choose this option to load points to <b>Survey Points</b> layer from <i>LADM_COL</i> model.\
<br><br>\
<b>Survey Point</b> is a specialized class of <i>LA_Point</i> which represents a building, right of way or auxiliary vertex.\
")

        # <b>Punto de Control</b> es una clase especializada de <i>LA_Punto</i> que representa puntos de la densificación de la red local, que se utiliza en la operación catastral para el levantamiento de información fisica de los objetos territoriales.
        self.WIZ_ADD_POINTS_CADASTRE_PAGE_1_OPTION_CP = QCoreApplication.translate("HelpStrings", "\
Choose this option to load points to <b>Control Points</b> layer from <i>LADM_COL</i> model.\
<br><br>\
<b>Control Point</b> is a specialized class of <i>LA_Point</i> which represents points belonging to the local network, used in cadastre operation for surveying physical information of the territorial objects.\
")

        self.WIZ_ADD_POINTS_CADASTRE_PAGE_2_OPTION_CSV = QCoreApplication.translate("HelpStrings", "\
Add a Comma Separated Values file (CSV), choosing the delimiter and fields that contain point coordinates.\
")

        self.WIZ_ADD_POINTS_CADASTRE_PAGE_3_OPTION_CSV = QCoreApplication.translate("HelpStrings", "\
Add a Comma Separated Values file (CSV), choosing the delimiter and fields that contain point coordinates.<br><br><a href='#template'>Click to download CSV template</a><br><br><a href='#data'>Click to download CSV sample data</a>\
")

        self.WIZ_CREATE_ADMINISTRATIVE_SOURCE_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create an <b>Administrative Source</b> using a form.\
<br><br>\
<b>Administrative Source</b> is a specialization of the <i>COL_Fuente</i> class to store those sources corresponding to documents (mortgage document, notarial documents, historical documents, and the like) that document the relationship between parties and parcels.\
")

        self.WIZ_CREATE_ADMINISTRATIVE_SOURCE_PAGE_1_OPTION_ANOTHER = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to add an <b>Administrative Source</b> with an external resource, such as a CSV file, a QGIS table, etc.\
<br><br>\
<b>Administrative Source</b> is a specialization of the class <i>COL_Fuente</i> to store those sources constituted by documents (mortgage document, notarial documents, historical documents, etc.) that document the relationship between instances of interested and property.\
")

        self.WIZ_CREATE_COL_PARTY_CADASTRE_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Party</b> using a form.\
<br><br>\
<b>Party</b> is a natural or non-natural person who has rights or who is subject to restrictions or responsibilities related to one or more <i>Parcels</i>.\
")

        self.WIZ_CREATE_COL_PARTY_CADASTRE_PAGE_1_OPTION_ANOTHER = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to add a <b>Party</b> with an external resource, such as a CSV file, a QGIS table, etc.\
<br><br>\
<b>Party</b> is a natural or non-natural person who has rights or who is subject to restrictions or responsibilities related to one or more <i>Parcel</i>.\
")

        self.WIZ_CREATE_PARCEL_CADASTRE_PAGE_1_OPTION_EXISTING_PLOT = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Parcel</b> based on existing plots.\
<br><br>\
<b>Parcel</b> is a specialized <i>BA Unit</i> class, which describes the basic administrative unit of Colombian cadastre.\
 The <b>Parcel</b> is the legal territorial unit, which is formed by the plot and may or may not have associated constructions.\
")

        self.WIZ_CREATE_PARCEL_CADASTRE_PAGE_1_OPTION_WITHOUT_GEOM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Parcel</b> without geometry.\
<br><br>\
<b>Parcel</b> is a specialized <i>BA Unit</i> class, which describes the basic administrative unit of Colombian cadastre.\
 The <b>Parcel</b> is the legal territorial unit, which is formed by the plot and may or may not have associated constructions.\
")

        self.WIZ_CREATE_PARCEL_CADASTRE_PAGE_1_OPTION_ANOTHER = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Parcel</b> from external resource, such as a CSV file, a QGIS table, etc.\
<br><br>\
<b>Parcel</b> is a specialized BaUnit Class, which describes the basic administrative unit for the case of Colombia.\
The property is the legal territorial unit of Cadastre.\
It is formed by the terrain and may or may not have associated constructions.\
")

        self.WIZ_CREATE_PLOT_CADASTRE_PAGE_1_OPTION_RLAYER = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Plot</b> from a re-factored layer.\
<br><br>\
<b>Plot</b> is a portion of land with a defined geographical extension.\
")

        self.WIZ_CREATE_PLOT_CADASTRE_PAGE_1_OPTION_BOUNDARIES = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Plot</b> from existing <i>Boundaries</i>.\
<br><br>\
<b>Plot</b> is a portion of land with a defined geographical extension.\
")

        self.WIZ_CREATE_BUILDING_CADASTRE_PAGE_1_OPTION_POINTS = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Building</b> from existing <i>Survey Points</i>.\
<br><br>\
<b>Building</b> is a type of legal space of the building unit of the LADM model that stores data specific of the resulting valuation.\
")

# Elige esta opción si deseas crear una <b>Unidad de Construcción</b> a partir de <i>Puntos</i> existentes.
# <br><br>
# <b>Unidad de Construccion<b> es cada conjunto de materiales consolidados dentro de un <i>Predio</i> que tiene unas caracteristicas especificas en cuanto a elementos constitutivos físicos y usos de los mismos.
        self.WIZ_CREATE_BUILDING_UNIT_CADASTRE_PAGE_1_OPTION_POINTS = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Building Unit</b> from existing <i>Survey Points</i>.\
<br><br>\
<b>Building Unit</b> is a group of consolidated materials within a <i>Parcel</i> that has specific characteristics in terms of physical constituent elements and their usage.\
")

# Clase de tipo LA_RRR que registra las responsabilidades que las instancias de los interesados tienen sobre los predios.
        self.WIZ_CREATE_RESPONSIBILITY_CADASTRE_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you have selected at least one <i>Administrative Source</i> and want to link such selected sources to a new <b>Responsibility</b> that you will create using a form.\
<br><br>\
<b>COL_Responsibility</b> is a class of type <i>LA_RRR</i> which stores responsibilities that parties have over parcels.\
")

# Restricciones a las que está sometido un predio y que inciden sobre los derechos que pueden ejercerse sobre él.
        self.WIZ_CREATE_RESTRICTION_CADASTRE_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you have selected at least one <i>Administrative Source</i> and want to link such selected sources to a new <b>Restriction</b> that you will create using a form.\
<br><br>\
<b>COL_Restriction</b> are the restrictions on a parcel that affect rights that parties may have over it.\
")

# <b>COL_Derecho</b> es una clase que registra las instancias de los derechos que un interesado ejerce sobre un predio. Es una especialización de la clase LA_RRR del propio modelo.
        self.WIZ_CREATE_RIGHT_CADASTRE_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you have selected at least one <i>Administrative Source</i> and want to link such selected sources to a new <b>Right</b> that you will create using a form.\
<br><br>\
<b>COL_Right</b> is a class that stores right instances that a party has over a parcel. It is a specialization of the class LA_RRR.\
")

        self.WIZ_CREATE_SPATIAL_SOURCE_CADASTRE_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Spatial Source</b> using a form. Then select a layer to get all its selected features associated with the newly created <b>Spatial Source</b>.\
<br><br>\
<b>Spatial Source</b> is a specialization of the <i>COL_Fuente</i> class to store those sources corresponding to spatial data (geographic features, satellite imagery, photogrammetric flights, maps, coordinate listings, ancient or modern plans, location descriptions, and the like) that technically document the relationship between parties and parcels.\
")

        self.WIZ_DEFINE_BOUNDARIES_CADASTRE_PAGE_1_OPTION_DIGITIZE = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Boundary</b> using QGIS digitizing tools.\
<br><br>\
<b>Boundary</b> is a specialization of the <i>LA_CadenaCarasLindero</i> class to store boundaries that define plots. Two boundaries must not cross or overlap.\
")

        self.WIZ_CREATE_PROPERTY_RECORD_CARD_PRC_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Property Record Card</b> using a form.\
<br><br>\
<b>Property Record Card</b> is created specifically to store the information collected for the parcels.\
")

        self.WIZ_CREATE_MARKET_RESEARCH_PRC_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Market Research</b> using a form.\
<br><br>\
<b>Market Research</b> is information related to the market research carried out, with the objective to obtain the most probable market values, based on real estate transactions carried out.\
")

        self.WIZ_CREATE_NUCLEAR_FAMILY_PRC_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Nuclear Family</b> using a form.\
<br><br>\
<b>Nuclear Family</b> allows to registry the information related to the nuclear families of the cadastral survey for the pilots of the multipurpose cadastre.\
")

        self.WIZ_CREATE_NATURAL_PARTY_PRC_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Natural Party</b> using a form.\
<br><br>\
<b>Natural Party</b> acting as party.\
")

        self.WIZ_CREATE_LEGAL_PARTY_PRC_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Legal Party</b> using a form.\
<br><br>\
<b>Legañ Party</b> acting as party.\
")

    def get_refactor_help_string(self, layer_name, layer_is_spatial):
        # Abre una ventana que te permite establecer una asignación entre la entrada (fuente) {type} y el tipo {type} <b>{name}</b> de LADM_COL.
        return QCoreApplication.translate("HelpStrings", "\
               Choose this option to open a window that allows you to import data from a source {type} into the LADM_COL <b>{name}</b> {type}. \
               <br><br>\
               If the field structure of input and target {type}s differs, you can set a field mapping to define field transformations and correspondence.\
                ").format(
                    name=layer_name,
                    type=QCoreApplication.translate("HelpStrings", "layer") if layer_is_spatial else QCoreApplication.translate(
                        "HelpStrings", "table"))
