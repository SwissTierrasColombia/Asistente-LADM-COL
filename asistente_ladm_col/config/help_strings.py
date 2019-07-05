from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject)

from .table_mapping_config import (PLOT_TABLE,
                                   BUILDING_TABLE,
                                   BUILDING_UNIT_TABLE,
                                   PARCEL_TYPE_NO_HORIZONTAL_PROPERTY,
                                   PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT,
                                   PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT,
                                   PARCEL_TYPE_CONDOMINIUM_PARENT,
                                   PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT,
                                   PARCEL_TYPE_MEJORA,
                                   PARCEL_TYPE_CEMETERY_PARENT,
                                   PARCEL_TYPE_CEMETERY_PRIVATE_UNIT,
                                   PARCEL_TYPE_ROAD,
                                   PARCEL_TYPE_PUBLIC_USE,
                                   PARCEL_TYPE_STORE,
                                   PARCEL_TYPE_PARKING,
                                   PARCEL_TYPE_WAREHOUSE)

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

        self.WIZ_CREATE_PARCEL_CADASTRE_PAGE_2 = QCoreApplication.translate("HelpStrings", "\
Before creating a <b>Parcel</b>  you must associate with one or more existing <b>Spatial Units</b>.\
<br><br>\
{msg_parcel_type}\
<br>\
There are two ways to associate:\
<br><br>\
1. <b>Selecting Spatial Unit(s) on the map</b>: Here you can select on the map and immediately it will come back to wizard, \
this enables the button for create the association.\
<br><br>\
2. <b>Selecting Spatial Unit(s) by expression</b>: Here you can select using an expression, this has to be valid and \
the selection should take one feature. If the expression gets zero features or more than one, the button for create \
the association will not be activated.\
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
To create a <b>plot</b> you can use the existing boundaries, first you have at least one.\
<br><br>\
There are three ways to select boundaries:\
<br><br>\
1. <b>Selecting Boundaries on the map</b>: select one o more <i>Boundaries</i> and right click on the map to go back to the wizard, \
which enables the button for creating the plots.\
<br><br>\
2. <b>Selecting by expression</b>: select one o more <i>Boundaries</i> using an expression.\
If one or more boundaries were selected the button for creating the plots will be enable.\
<br><br>\
3. <b>Select all boundaries</b>: Select all boundaries available, If one or more boundaries were selected the button for creating the plots will be enable.\
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

        self.WIZ_CREATE_RIGHT_OF_WAY_CADASTRE_PAGE_1_OPTION_POINTS = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Right of Way</b> digitizing a polygon using existing <i>Survey Points</i>.\
<br><br>\
<b>Right of Way</b> is a type of spatial unit of the LADM model which allows the representation of a Right of Way associated to a LA_BAUnit.\
")

        self.WIZ_CREATE_RIGHT_OF_WAY_CADASTRE_PAGE_1_OPTION2_POINTS = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Right of Way</b> digitizing centerline using existing <i>Survey Points</i> and giving a width value.\
<br><br>\
<b>Right of Way</b> is a type of spatial unit of the LADM model which allows the representation of a Right of Way associated to a LA_BAUnit.\
")

        self.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_1 = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to associate an <b>ExtAddress</b> to an existing <i>Spatial Unit</i>.\
<br><br>\
<b>ExtAddress</b> is a class for manage the <i>Spatial Units</i> addresses from <i>LADM-COL model</i>.\
")

        self.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_2_OPTION_1 = QCoreApplication.translate("HelpStrings", "\
To associate the <b>ExtAddress</b> to an existing <i>Plot</i>, first you have to select one.\
<br><br>\
There are two ways to select Plots:\
<br><br>\
1. <b>Selecting Plot on the map</b>: select one <i>Plot</i> and right click on the map to go back to the wizard, \
which enables the button for creating the association.\
<br><br>\
2. <b>Selecting by expression</b>: select one <i>Plot</i> using an expression. The selection has to be valid and \
should match only one feature. If the expression matches two or more features, the button for creating \
the association will not be activated.\
")

        self.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_2_OPTION_2 = QCoreApplication.translate("HelpStrings", "\
To associate the <b>ExtAddress</b> to an existing <i>Building</i>, first you have to select one.\
<br><br>\
There are two ways to select Buildings:\
<br><br>\
1. <b>Selecting Building on the map</b>: select one <i>Building</i> and right click on the map to go back to the wizard, \
which enables the button for creating the association.\
<br><br>\
2. <b>Selecting by expression</b>:  select one <i>Building</i> using an expression. The selection has to be valid and \
should match only one feature. If the expression matches two or more features, the button for creating \
the association will not be activated.\
")

        self.WIZ_ASSOCIATE_EXTADDRESS_CADASTRE_PAGE_2_OPTION_3 = QCoreApplication.translate("HelpStrings", "\
To associate the <b>ExtAddress</b> to an existing <i>Building Unit</i>, first you have to select one.\
<br><br>\
There are two ways to select Building Units:\
<br><br>\
1. <b>Selecting Building Unit on the map</b>: select one <i>Building Unit</i> and right click on the map to go back to the wizard, \
which enables the button for creating the association.\
<br><br>\
2. <b>Selecting by expression</b>: select one <i>Building Unit</i> using an expression. The selection has to be valid and \
should match only one feature. If the expression matches two or more features, the button for creating \
the association will not be activated.\
")

# Clase de tipo LA_RRR que registra las responsabilidades que las instancias de los interesados tienen sobre los predios.
        self.WIZ_CREATE_RESPONSIBILITY_CADASTRE_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Responsibility</b> based on existing <b>Administrative Source(s)</b>.\
<br><br>\
<b>COL_Responsibility</b> is a class of type <i>LA_RRR</i> which stores responsibilities that parties have over parcels.\
")

        self.WIZ_CREATE_RESPONSIBILITY_CADASTRE_PAGE_2 = QCoreApplication.translate("HelpStrings", "\
Before creating a <b>Responsibility</b> you must associate with one or more existing <b>Administrative Sources</b>, First you must select the Administrative Source(s) of interest\
<br><br>\
You can select an Administrative Source(s) by:\
<br><br>\
<b> * Expression</b>: Here you can select using an expression, this has to be valid and \
the selection should take one feature. If the expression gets zero features or more than one, the button for create \
the association will not be activated.\
")

# Restricciones a las que está sometido un predio y que inciden sobre los derechos que pueden ejercerse sobre él.
        self.WIZ_CREATE_RESTRICTION_CADASTRE_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Restriction</b> based on existing <b>Administrative Source(s)</b>.\
<br><br>\
<b>COL_Restriction</b> are the restrictions on a parcel that affect rights that parties may have over it.\
")

        self.WIZ_CREATE_RESTRICTION_CADASTRE_PAGE_2 = QCoreApplication.translate("HelpStrings", "\
Before creating a <b>Restriction</b> you must associate with one or more existing <b>Administrative Sources</b>, First you must select the Administrative Source(s) of interest\
<br><br>\
You can select an Administrative Source(s) by:\
<br><br>\
<b> * Expression</b>: Here you can select using an expression, this has to be valid and \
the selection should take one feature. If the expression gets zero features or more than one, the button for create \
the association will not be activated.\
")

# <b>COL_Derecho</b> es una clase que registra las instancias de los derechos que un interesado ejerce sobre un predio. Es una especialización de la clase LA_RRR del propio modelo.
        self.WIZ_CREATE_RIGHT_CADASTRE_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Right</b> based on existing <b>Administrative Source(s)</b>.\
<br><br>\
<b>COL_Right</b> is a class that stores right instances that a party has over a parcel. It is a specialization of the class LA_RRR.\
")

        self.WIZ_CREATE_RIGHT_CADASTRE_PAGE_2 = QCoreApplication.translate("HelpStrings", "\
Before creating a <b>Right</b> you must associate with one or more existing <b>Administrative Sources</b>, First you must select the Administrative Source(s) of interest\
<br><br>\
You can select an Administrative Source(s) by:\
<br><br>\
<b> * Expression</b>: Here you can select using an expression, this has to be valid and \
the selection should take one feature. If the expression gets zero features or more than one, the button for create \
the association will not be activated.\
")

        self.WIZ_CREATE_SPATIAL_SOURCE_CADASTRE_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Spatial Source</b> using a form. Then select the <b>Spatial Features</b> that you want to associate with the Spatial Source to create.\
<br><br>\
<b>Spatial Source</b> is a specialization of the <i>COL_Fuente</i> class to store those sources corresponding to spatial data (geographic features, satellite imagery, photogrammetric flights, maps, coordinate listings, ancient or modern plans, location descriptions, and the like) that technically document the relationship between parties and parcels.\
")

        self.WIZ_CREATE_SPATIAL_SOURCE_CADASTRE_PAGE_2 = QCoreApplication.translate("HelpStrings", "\
Before creating a <b>Spatial Source</b>  you must associate with one or more existing <b>Spatial Features</b>, First you must select the Spatial feature(s) of interest\
<br><br>\
There are two ways to associate:\
<br><br>\
1. <b>Selecting Spatial Feature(s) on the map</b>: Here you can select on the map and immediately it will come back to wizard, \
this enables the button for create the association.\
<br><br>\
2. <b>Selecting Spatial Unit(s) by expression</b>: Here you can select using an expression, this has to be valid and \
the selection should take one feature. If the expression gets zero features or more than one, the button for create \
the association will not be activated.\
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
<b>Legal Party</b> acting as party.\
")

        self.DLG_IMPORT_FROM_EXCEL = QCoreApplication.translate("HelpStrings", "\
Use an intermediate Excel structure to import legal (all alphanumeric) data into LADM_COL.<br><br><a href='#template'>Click to download Excel template</a><br><br><a href='#data'>Click to download Excel sample data</a>\
")

        self.WIZ_CREATE_PARCEL_VALUATION_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Parcel</b> using a form.\
<br><br>\
<b>Parcel</b> is a grouping of specific attributes that are needed to appraise the parcel.\
")

        self.WIZ_CREATE_HORIZONTAL_PROPERTY_VALUATION_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Horizontal Property Valuation</b> using a form.\
<br><br>\
<b>Horizontal Property Valuation</b> stores information related to the property, or basic unit of the plot, which serves as a main parcel to a horizontal property element.\
")

        self.WIZ_CREATE_COMMON_EQUIPMENT_VALUATION_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Common Equipment</b> using a form.\
<br><br>\
<b>Common Equipment</b> stores information relative to the common equipment of the horizontal property main parcel.\
")

        self.WIZ_CREATE_BUILDING_VALUATION_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Building</b> using a form.\
<br><br>\
<b>Building</b> (valuation model) is a grouping of specific attributes that are needed to appraise the building.\
")

        self.WIZ_CREATE_BUILDING_UNIT_VALUATION_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Building Unit</b> using a form.\
<br><br>\
<b>Building Unit</b> (valuation model) is a grouping of specific attributes that are needed to appraise the building.\
")

        self.WIZ_CREATE_BUILDING_UNIT_QUALIFICATION_NO_CONVENTIONAL_VALUATION_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
<b>Building Unit Qualification (unconventional)</b> is a class to store data for the valuation of the building unit.")

        self.WIZ_CREATE_BUILDING_UNIT_QUALIFICATION_CONVENTIONAL_VALUATION_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
<b>Building Unit Qualification (conventional)</b> is a class to store data for the valuation of the building unit.")

        self.WIZ_CREATE_GEOECONOMIC_ZONE_VALUATION_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Geoeconomic Zone</b> using a form.\
<br><br>\
<b>Geoeconomic Zone</b> allows you to manage areas with similar economic and geographical characteristics.\
")

        self.WIZ_CREATE_PHYSICAL_ZONE_VALUATION_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Physical Zone</b> using a form.\
<br><br>\
<b>Physical Zone</b> allows you to manage regions with similar physic characteristics.\
")

        self.WIZ_USING_FORM_BUILDING_UNIT_QUALIFICATION_PAGE_2_OPTION = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Conventional Building Unit Qualification</b> using a form.")

        self.WIZ_USING_FORM_BUILDING_UNIT_NO_QUALIFICATION_PAGE_2_OPTION = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create an <b>Unconventional Building Unit Qualification</b> using a form.")

        self.MESSAGE_PARCEL_TYPES = {
            PARCEL_TYPE_NO_HORIZONTAL_PROPERTY: QCoreApplication.translate("HelpStrings", "Cuando el tipo de predio es <b>'{parcel_type}'</b> la unidad espacial asociada debe ser un '{plot_table}' y opcionalmente una o mas '{building_table}es' y '{building_unit_table}'").format(parcel_type=PARCEL_TYPE_NO_HORIZONTAL_PROPERTY, plot_table=PLOT_TABLE, building_table=BUILDING_TABLE, building_unit_table=BUILDING_UNIT_TABLE),
            PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT: QCoreApplication.translate("HelpStrings", "Cuando el tipo de predio es <b>'{parcel_type}'</b> la unidad espacial asociada debe ser un '{plot_table}' y opcionalmente una o más '{building_table}es'").format(parcel_type=PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT, plot_table=PLOT_TABLE, building_table=BUILDING_TABLE),
            PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT: QCoreApplication.translate("HelpStrings", "Cuando el tipo de predio es <b>'{parcel_type}'</b> la unidad espacial asociada deber una o más '{building_unit_table}'").format(parcel_type=PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT, building_unit_table=BUILDING_UNIT_TABLE),
            PARCEL_TYPE_CONDOMINIUM_PARENT: QCoreApplication.translate("HelpStrings", "Cuando el tipo de predio es <b>'{parcel_type}'</b> la unidad espacial asociada debe ser un '{plot_table}' y opcionalmente una o más '{building_table}es'").format(parcel_type=PARCEL_TYPE_CONDOMINIUM_PARENT, plot_table=PLOT_TABLE, building_table=BUILDING_TABLE),
            PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT: QCoreApplication.translate("HelpStrings", "Cuando el tipo de predio es  <b>'{parcel_type}'</b> la unidad espacial asociada debe ser un '{plot_table}' y opcionalmente una o más '{building_table}es'").format(parcel_type=PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT, plot_table=PLOT_TABLE, building_table=BUILDING_TABLE),
            PARCEL_TYPE_MEJORA: QCoreApplication.translate("HelpStrings","Cuando el tipo de predio es <b>'{parcel_type}'</b> la unidad espacial asociada debe ser una '{building_table}' o '{building_unit_table}'").format(parcel_type=PARCEL_TYPE_MEJORA, building_table=BUILDING_TABLE, building_unit_table=BUILDING_UNIT_TABLE),
            PARCEL_TYPE_CEMETERY_PARENT: QCoreApplication.translate("HelpStrings", "Cuando el tipo de predio es <b>'{parcel_type}'</b> la unidad espacial asociada la unidad espacial asociada debe ser un '{plot_table}' y opcionalmente una o más '{building_table}es'").format(parcel_type=PARCEL_TYPE_CEMETERY_PARENT, plot_table=PLOT_TABLE, building_table=BUILDING_TABLE),
            PARCEL_TYPE_CEMETERY_PRIVATE_UNIT: QCoreApplication.translate("HelpStrings","Cuando el tipo de predio es <b>'{parcel_type}'</b> la unidad espacial asociada la unidad espacial asociada debe ser un '{plot_table}'").format(parcel_type=PARCEL_TYPE_CEMETERY_PRIVATE_UNIT, plot_table=PLOT_TABLE),
            PARCEL_TYPE_ROAD: QCoreApplication.translate("HelpStrings","Cuando el tipo de predio es <b>'{parcel_type}'</b> la unidad espacial asociada la unidad espacial asociada debe ser un '{plot_table}'").format(parcel_type=PARCEL_TYPE_ROAD, plot_table=PLOT_TABLE),
            PARCEL_TYPE_PUBLIC_USE: QCoreApplication.translate("HelpStrings","Cuando el tipo de predio es <b>'{parcel_type}'</b> la unidad espacial asociada la unidad espacial asociada debe ser un '{plot_table}' y opcionalmente una o más '{building_table}es'").format(parcel_type=PARCEL_TYPE_PUBLIC_USE, plot_table=PLOT_TABLE, building_table=BUILDING_TABLE),
            PARCEL_TYPE_STORE: QCoreApplication.translate("HelpStrings", ""),
            PARCEL_TYPE_PARKING: QCoreApplication.translate("HelpStrings",""),
            PARCEL_TYPE_WAREHOUSE: QCoreApplication.translate("HelpStrings", "")
        }

    def get_refactor_help_string(self, layer_name, layer_is_spatial):
        # Abre una ventana que te permite establecer una asignación entre la entrada (fuente) {type} y el tipo {type} <b>{name}</b> de LADM_COL.
        return QCoreApplication.translate("HelpStrings", "\
               Choose this option to open a window that allows you to import data from a source {type} into the LADM_COL <b>{name}</b> {type}. \
               <br><br>\
               If the field structure of input and target {type}s differs, you can set a field mapping to define field transformations and correspondence.\
               <br><br>\
               You can select previous mappings in the <b>Recent mappings</b> list, which can save you time taking advantage of mappings that you already used.\
                ").format(
                    name=layer_name,
                    type=QCoreApplication.translate("HelpStrings", "layer") if layer_is_spatial else QCoreApplication.translate(
                        "HelpStrings", "table"))
