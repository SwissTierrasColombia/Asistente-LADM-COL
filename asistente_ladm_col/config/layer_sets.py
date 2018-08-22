from .table_mapping_config import *

# Configure layer sets to appear in the load layers dialog
# Each layer set is a key-value pair where key is the name of the layer set
# and the value is a list of layers to load
LAYER_SETS = {
    'Datos de Interesados': [
        GENDER_TYPE_TABLE,
        NATURAL_PARTY_TABLE,
        PARTY_DOCUMENT_TYPE_TABLE,
        PARTY_TYPE_TABLE
    ],
    'Punto Lindero, Lindero y Terreno': [
        BOUNDARY_POINT_TABLE,
        BOUNDARY_TABLE,
        PLOT_TABLE,
        MORE_BOUNDARY_FACE_STRING_TABLE,
        LESS_TABLE,
        POINT_BOUNDARY_FACE_STRING_TABLE
    ]
}
