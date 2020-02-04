from qgis.PyQt.QtCore import (QCoreApplication,
                              QObject)

from asistente_ladm_col.config.mapping_config import LADMNames

# For this module use multiline "\" instead of triple double quotes

class HelpStrings(QObject):
    def __init__(self):

        self.CHANGE_DETECTION_SETTING_DIALOG_HELP = QCoreApplication.translate(
            "HelpStrings",
            """Setup the collected and supplies database connection option to make change detection.
                <ul>
                  <li><b>Collected database: </b> is the database associate to field survey, which must conform to the operation model.</li>
                  <li><b>Supplies database: </b> is the database delivered by the cadastral manager, which must conform to the cadastral supplies model.</li>
                </ul>""")

        self.WIZ_ADD_POINTS_OPERATION_PAGE_1_OPTION_BP = QCoreApplication.translate("HelpStrings", "\
Choose this option to load points to <b>Boundary Points</b> layer from <i>LADM_COL</i> model.\
<br><br>\
<b>Boundary Point</b> is a specialized class of <i>LA_Point</i> which stores points that define a boundary.\
Boundary is an instance of <i>LA_BoundaryFaceString</i> class and its specializations.\
")

        self.WIZ_ADD_POINTS_OPERATION_PAGE_1_OPTION_SP = QCoreApplication.translate("HelpStrings", "\
Choose this option to load points to <b>Survey Points</b> layer from <i>LADM_COL</i> model.\
<br><br>\
<b>Survey Point</b> is a specialized class of <i>LA_Point</i> which represents a building, right of way or auxiliary vertex.\
")

        # <b>Punto de Control</b> es una clase especializada de <i>LA_Punto</i> que representa puntos de la densificación de la red local, que se utiliza en la operación catastral para el levantamiento de información fisica de los objetos territoriales.
        self.WIZ_ADD_POINTS_OPERATION_PAGE_1_OPTION_CP = QCoreApplication.translate("HelpStrings", "\
Choose this option to load points to <b>Control Points</b> layer from <i>LADM_COL</i> model.\
<br><br>\
<b>Control Point</b> is a specialized class of <i>LA_Point</i> which represents points belonging to the local network, used in operation operation for surveying physical information of the territorial objects.\
")

        self.WIZ_ADD_POINTS_OPERATION_PAGE_2_OPTION_CSV = QCoreApplication.translate("HelpStrings", "\
Add a Comma Separated Values file (CSV), choosing the delimiter and fields that contain point coordinates.\
")

        self.WIZ_ADD_POINTS_OPERATION_PAGE_3_OPTION_CSV = QCoreApplication.translate("HelpStrings", "\
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

        self.WIZ_CREATE_COL_PARTY_OPERATION_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Party</b> using a form.\
<br><br>\
<b>Party</b> is a natural or non-natural person who has rights or who is subject to restrictions or responsibilities related to one or more <i>Parcels</i>.\
")

        self.WIZ_CREATE_COL_PARTY_OPERATION_PAGE_1_OPTION_ANOTHER = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to add a <b>Party</b> with an external resource, such as a CSV file, a QGIS table, etc.\
<br><br>\
<b>Party</b> is a natural or non-natural person who has rights or who is subject to restrictions or responsibilities related to one or more <i>Parcel</i>.\
")

        self.WIZ_CREATE_PARCEL_OPERATION_PAGE_1_OPTION_EXISTING_PLOT = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Parcel</b> based on existing plots.\
<br><br>\
<b>Parcel</b> is a specialized <i>BA Unit</i> class, which describes the basic administrative unit of Colombian operation.\
 The <b>Parcel</b> is the legal territorial unit, which is formed by the plot and may or may not have associated constructions.\
")

        self.WIZ_CREATE_PARCEL_OPERATION_PAGE_1_OPTION_WITHOUT_GEOM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Parcel</b> without geometry.\
<br><br>\
<b>Parcel</b> is a specialized <i>BA Unit</i> class, which describes the basic administrative unit of Colombian operation.\
 The <b>Parcel</b> is the legal territorial unit, which is formed by the plot and may or may not have associated constructions.\
")

        self.WIZ_CREATE_PARCEL_OPERATION_PAGE_1_OPTION_ANOTHER = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Parcel</b> from external resource, such as a CSV file, a QGIS table, etc.\
<br><br>\
<b>Parcel</b> is a specialized BaUnit Class, which describes the basic administrative unit for the case of Colombia.\
The property is the legal territorial unit of Cadastre.\
It is formed by the terrain and may or may not have associated constructions.\
")

        self.WIZ_CREATE_PARCEL_OPERATION_PAGE_2 = QCoreApplication.translate("HelpStrings", "\
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

        self.WIZ_CREATE_PLOT_OPERATION_PAGE_1_OPTION_RLAYER = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Plot</b> from a re-factored layer.\
<br><br>\
<b>Plot</b> is a portion of land with a defined geographical extension.\
")

        self.WIZ_CREATE_PLOT_OPERATION_PAGE_1_OPTION_BOUNDARIES = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Plot</b> from existing <i>Boundaries</i>.\
<br><br>\
<b>Plot</b> is a portion of land with a defined geographical extension.\
")

        self.WIZ_CREATE_PLOT_OPERATION_PAGE_2 = QCoreApplication.translate("HelpStrings", "\
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

        self.WIZ_CREATE_BUILDING_OPERATION_PAGE_1_OPTION_POINTS = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Building</b> from existing <i>Survey Points</i>.\
<br><br>\
<b>Building</b> is a type of legal space of the building unit of the LADM model that stores data specific of the resulting valuation.\
")

# Elige esta opción si deseas crear una <b>Unidad de Construcción</b> a partir de <i>Puntos</i> existentes.
# <br><br>
# <b>Unidad de Construccion<b> es cada conjunto de materiales consolidados dentro de un <i>Predio</i> que tiene unas caracteristicas especificas en cuanto a elementos constitutivos físicos y usos de los mismos.
        self.WIZ_CREATE_BUILDING_UNIT_OPERATION_PAGE_1_OPTION_POINTS = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Building Unit</b> from existing <i>Survey Points</i>.\
<br><br>\
<b>Building Unit</b> is a group of consolidated materials within a <i>Parcel</i> that has specific characteristics in terms of physical constituent elements and their usage.\
")

        self.WIZ_CREATE_RIGHT_OF_WAY_OPERATION_PAGE_1_OPTION_POINTS = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Right of Way</b> digitizing a polygon using existing <i>Survey Points</i>.\
<br><br>\
<b>Right of Way</b> is a type of spatial unit of the LADM model which allows the representation of a Right of Way associated to a LA_BAUnit.\
")

        self.WIZ_CREATE_RIGHT_OF_WAY_OPERATION_PAGE_1_OPTION2_POINTS = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Right of Way</b> digitizing centerline using existing <i>Survey Points</i> and giving a width value.\
<br><br>\
<b>Right of Way</b> is a type of spatial unit of the LADM model which allows the representation of a Right of Way associated to a LA_BAUnit.\
")

        self.WIZ_ASSOCIATE_EXTADDRESS_OPERATION_PAGE_1 = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to associate an <b>ExtAddress</b> to an existing <i>Spatial Unit</i>.\
<br><br>\
<b>ExtAddress</b> is a class for manage the <i>Spatial Units</i> addresses from <i>LADM-COL model</i>.\
")

        self.WIZ_ASSOCIATE_EXTADDRESS_OPERATION_PAGE_2_OPTION_1 = QCoreApplication.translate("HelpStrings", "\
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

        self.WIZ_ASSOCIATE_EXTADDRESS_OPERATION_PAGE_2_OPTION_2 = QCoreApplication.translate("HelpStrings", "\
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

        self.WIZ_ASSOCIATE_EXTADDRESS_OPERATION_PAGE_2_OPTION_3 = QCoreApplication.translate("HelpStrings", "\
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

# Restricciones a las que está sometido un predio y que inciden sobre los derechos que pueden ejercerse sobre él.
        self.WIZ_CREATE_RESTRICTION_OPERATION_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Restriction</b> based on existing <b>Administrative Source(s)</b>.\
<br><br>\
<b>OP_Restriction</b> are the restrictions on a parcel that affect rights that parties may have over it.\
")

        self.WIZ_CREATE_RESTRICTION_OPERATION_PAGE_2 = QCoreApplication.translate("HelpStrings", "\
Before creating a <b>Restriction</b> you must associate with one or more existing <b>Administrative Sources</b>, First you must select the Administrative Source(s) of interest\
<br><br>\
You can select an Administrative Source(s) by:\
<br><br>\
<b> * Expression</b>: Here you can select using an expression, this has to be valid and \
the selection should take one feature. If the expression gets zero features or more than one, the button for create \
the association will not be activated.\
")

# <b>COL_Derecho</b> es una clase que registra las instancias de los derechos que un interesado ejerce sobre un predio. Es una especialización de la clase LA_RRR del propio modelo.
        self.WIZ_CREATE_RIGHT_OPERATION_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Right</b> based on existing <b>Administrative Source(s)</b>.\
<br><br>\
<b>OP_Right</b> is a class that stores right instances that a party has over a parcel. It is a specialization of the class OP_RRR.\
")

        self.WIZ_CREATE_RIGHT_OPERATION_PAGE_2 = QCoreApplication.translate("HelpStrings", "\
Before creating a <b>Right</b> you must associate with one or more existing <b>Administrative Sources</b>, First you must select the Administrative Source(s) of interest\
<br><br>\
You can select an Administrative Source(s) by:\
<br><br>\
<b> * Expression</b>: Here you can select using an expression, this has to be valid and \
the selection should take one feature. If the expression gets zero features or more than one, the button for create \
the association will not be activated.\
")

        self.WIZ_CREATE_SPATIAL_SOURCE_OPERATION_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Spatial Source</b> using a form. Then select the <b>Spatial Features</b> that you want to associate with the Spatial Source to create.\
<br><br>\
<b>Spatial Source</b> is a specialization of the <i>COL_Fuente</i> class to store those sources corresponding to spatial data (geographic features, satellite imagery, photogrammetric flights, maps, coordinate listings, ancient or modern plans, location descriptions, and the like) that technically document the relationship between parties and parcels.\
")

        self.WIZ_CREATE_SPATIAL_SOURCE_OPERATION_PAGE_2 = QCoreApplication.translate("HelpStrings", "\
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

        self.WIZ_DEFINE_BOUNDARIES_OPERATION_PAGE_1_OPTION_DIGITIZE = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Boundary</b> using QGIS digitizing tools.\
<br><br>\
<b>Boundary</b> is a specialization of the <i>LA_CadenaCarasLindero</i> class to store boundaries that define plots. Two boundaries must not cross or overlap.\
")

        self.DLG_IMPORT_FROM_EXCEL = QCoreApplication.translate("HelpStrings", "\
Use an intermediate Excel structure to import legal (all alphanumeric) data into LADM_COL.<br><br><a href='#template'>Click to download Excel template</a><br><br><a href='#data'>Click to download Excel sample data</a>\
")

        self.WIZ_CREATE_BUILDING_UNIT_VALUATION_PAGE_1_OPTION_FORM = QCoreApplication.translate("HelpStrings", "\
Choose this option if you want to create a <b>Building Unit</b> using a form.\
<br><br>\
<b>Building Unit</b> (valuation model) is a grouping of specific attributes that are needed to appraise the building.\
")

        self.WIZ_CREATE_BUILDING_UNIT_VALUATION_PAGE_2 = QCoreApplication.translate("HelpStrings", "\
To associate the <b>Building unit valuation</b> to an existing <i>Building unit</i>, first you have to select one.\
<br><br>\
There are two ways to select Building unit:\
<br><br>\
1. <b>Selecting building on the map</b>: select one <i>building unit</i> and right click on the map to go back to the wizard, \
which enables the button for creating the association.\
<br><br>\
2. <b>Selecting by expression</b>: select one <i>Building unit</i> using an expression. The selection has to be valid and \
should match only one feature. If the expression matches two or more features, the button for creating \
the association will not be activated.\
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

    def get_refactor_help_string(self, db, layer):
        layer_name = db.get_ladm_layer_name(layer)
        layer_is_spatial = layer.isSpatial()

        # Abre una ventana que te permite establecer una asignación entre la entrada (fuente) {type} y el tipo {type} <b>{name}</b> de LADM_COL.
        return QCoreApplication.translate("HelpStrings", "\
               Choose this option to open a window that allows you to import data from a source {type} into the LADM_COL <b>{name}</b> {type}. \
               <br><br>\
               If the field structure of input and target {type}s differs, you can set a field mapping to define field transformations and correspondence.\
               <br><br>\
               You can select previous mappings in the <b>Recent mappings</b> list, which can save you time taking advantage of mappings that you already used.\
                ").format(
                    name=layer_name,
                    type=QCoreApplication.translate("HelpStrings", "layer") if layer_is_spatial else QCoreApplication.translate("HelpStrings", "table"))

    def get_message_parcel_type(self, parcel_type):
        if parcel_type == LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY:
            return QCoreApplication.translate("HelpStrings",
                                              "When the type of parcel is <b>'No Horizontal Property'</b> the spatial unit associated must be a 'Plot' and optionally one or more 'Buildings' and 'Building Units'")

        elif parcel_type == LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARENT:
            return QCoreApplication.translate("HelpStrings",
                                              "When the type of parcel is <b>'Horizontal Property Parent'</b> the spatial unit associated must be a 'Plot' and optionally one or more 'Buildings'")

        elif parcel_type == LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_PARCEL_UNIT:
            return QCoreApplication.translate("HelpStrings",
                                              "When the type of parcel is <b>'Horizontal Property Parcel Unit'</b> the spatial unit associated must be one or more 'Building Units'")

        elif parcel_type == LADMNames.PARCEL_TYPE_CONDOMINIUM_PARENT:
            return QCoreApplication.translate("HelpStrings",
                                              "When the type of parcel is <b>'Condominium Parent'</b> the spatial unit associated must be a 'Plot' and optionally one or more 'Buildings'")

        elif parcel_type == LADMNames.PARCEL_TYPE_CONDOMINIUM_PARCEL_UNIT:
            return QCoreApplication.translate("HelpStrings",
                                              "When the type of parcel is <b>'Condominium Parcel Unit'</b> the spatial unit associated must be a 'Plot' and optionally one or more 'Buildings'")

        elif parcel_type == LADMNames.PARCEL_TYPE_HORIZONTAL_PROPERTY_MEJORA:
            return QCoreApplication.translate("HelpStrings",
                                              "When the type of parcel is <b>'Horizontal Property Mejora'</b> the spatial unit associated must be a 'Building' or 'Building Unit'")

        elif parcel_type == LADMNames.PARCEL_TYPE_NO_HORIZONTAL_PROPERTY_MEJORA:
            return QCoreApplication.translate("HelpStrings",
                                              "When the type of parcel is <b>'No Horizontal Property Mejora'</b> the spatial unit associated must be a 'Building' or 'Building Unit'")

        elif parcel_type == LADMNames.PARCEL_TYPE_CEMETERY_PARENT:
            return QCoreApplication.translate("HelpStrings",
                                              "When the type of parcel is <b>'Cemetery Parent'</b> the spatial unit associated must be a 'Plot' and optionally one or more 'Buildings'")

        elif parcel_type == LADMNames.PARCEL_TYPE_CEMETERY_PARCEL_UNIT:
            return QCoreApplication.translate("HelpStrings",
                                              "When the type of parcel is <b>'Cemetery Parcel Unit'</b> the spatial unit associated must be a 'Plot'")

        elif parcel_type == LADMNames.PARCEL_TYPE_ROAD:
            return QCoreApplication.translate("HelpStrings",
                                              "When the type of parcel is <b>'Road'</b> the spatial unit associated must be a 'Plot'")

        elif parcel_type == LADMNames.PARCEL_TYPE_PUBLIC_USE:
            return QCoreApplication.translate("HelpStrings",
                                              "When the type of parcel is <b>'Public Use'</b> the spatial unit associated must be a 'Plot' and optionally one or more 'Buildings'")
