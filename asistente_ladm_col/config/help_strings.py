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

        self.WIZ_CREATE_LEGAL_PARTY_CADASTRE_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Legal Party</b> using a form.\
<br><br>\
<b>Legal Party</b> is a legal entity that has rights, restrictions or responsibilities related to one or more <i>Parcels</i>.\
")

        self.WIZ_CREATE_LEGAL_PARTY_CADASTRE_PAGE_1_OPTION_ANOTHER = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to add a <b>Legal Party</b> with an external resource, such as a CSV file, a QGIS table, etc.\
<br><br>\
<b>Legal Party</b> is a legal entity that has rights, restrictions or responsibilities related to one or more <i>Parcel</i>.\
")

        self.WIZ_CREATE_NATURAL_PARTY_CADASTRE_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Natural Party</b> using a form.\
<br><br>\
<b>Natural Party</b> is a natural person who has rights or who is subject to restrictions or responsibilities related to one or more <i>Parcels</i>.\
")

        self.WIZ_CREATE_NATURAL_PARTY_CADASTRE_PAGE_1_OPTION_ANOTHER = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to add a <b>Natural Party</b> with an external resource, such as a CSV file, a QGIS table, etc.\
<br><br>\
<b>Natural Party</b> is a natural person who has rights or who is subject to restrictions or responsibilities related to one or more <i>Parcel</i>.\
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

        self.WIZ_CREATE_PLOT_CADASTRE_PAGE_2 = QCoreApplication.translate("HelpStrings", "\
Select the <b>Plot</ b> layer from those available in the QGIS project.\
")

        self.WIZ_CREATE_BUILDING_CADASTRE_PAGE_1_OPTION_POINTS = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Building</b> from existing <i>Survey Points</i>.\
<br><br>\
<b>Building</b> is a type of legal space of the building unit of the LADM model that stores data specific of the resulting valuation.\
")

        self.WIZ_CREATE_RESPONSIBILITY_CADASTRE_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to add a <b>Responsibility</b> with a form.\
<br><br>\
<b>COL_Responsibility</b> is a class of type <i>LA_RRR</i> that records the responsibilities that stakeholders have on the premises.\
")

        self.WIZ_CREATE_RESPONSIBILITY_CADASTRE_PAGE_1_OPTION_ANOTHER = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to add a <b>Responsibility</b> from external resource, such as a CSV file, a QGIS table, etc..\
<br><br>\
<b>COL_Responsibility</b> is a class of type <i>LA_RRR</i> that records the responsibilities that stakeholders have on the premises.\
")

        self.WIZ_CREATE_RESTRICTION_CADASTRE_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to add a <b>Restriction</b> with a form.\
<br><br>\
<b>COL_Restriction</b> are the restrictions to which a property is subject and that affect the rights that may be exercised over it.\
")

        self.WIZ_CREATE_RESTRICTION_CADASTRE_PAGE_1_OPTION_ANOTHER = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to add a <b>Restriction</b> from external resource, such as a CSV file, a QGIS table, etc.\
<br><br>\
<b>COL_Restriction</b> are the restrictions to which a property is subject and that affect the rights that may be exercised over it.\
")

        self.WIZ_CREATE_RIGHT_CADASTRE_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to add a <b>Right</b> with a form.\
<br><br>\
<b>COL_Right</ b> is a class that registers the instances of rights that an interested party exercises over a property. It is a specialization of the class LA_RRR of the model itself.\
")

        self.WIZ_CREATE_RIGHT_CADASTRE_PAGE_1_OPTION_ANOTHER = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to add a <b>Right</b> from external resource, such as a CSV file, a QGIS table, etc.\
<br><br>\
<b>COL_Right</ b> is a class that registers the instances of rights that an interested party exercises over a property. It is a specialization of the class LA_RRR of the model itself.\
")

        self.WIZ_CREATE_SPATIAL_SOURCE_CADASTRE_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Spatial Source</b> using a form.\
<br><br>\
<b>Spatial Source</b> is a specialization of the <i>COL_Fuente</i> class to store those sources corresponding to spatial data (geographic features, satellite imagery, photogrammetric flights, maps, coordinate listings, ancient or modern plans, location descriptions, and the like) that technically document the relationship between parties and parcels.\
")

        self.WIZ_DEFINE_BOUNDARIES_CADASTRE_PAGE_1_OPTION_DIGITIZE = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Boundary</b> using QGIS digitizing tools.\
<br><br>\
<b>Boundary</b> is a specialization of the <i>LA_CadenaCarasLindero</i> class to store boundaries that define plots. Two boundaries must not cross or overlap.\
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
