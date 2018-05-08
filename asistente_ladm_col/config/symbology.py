from qgis.core import QgsWkbTypes
from qgis.PyQt.QtGui import QColor

from .table_mapping_config import (
    BOUNDARY_TABLE,
    BOUNDARY_POINT_TABLE,
    SURVEY_POINT_TABLE,
    PLOT_TABLE,
    BUILDING_TABLE
)

LAYERS_STYLE = {
    BOUNDARY_TABLE: {
        QgsWkbTypes.LineGeometry: {
            'symbology': {
                'name': 'Simple line',
                'color': '#45508a',
                'width': '0.16'
            },
            'label' : None
        }
    },
    BOUNDARY_POINT_TABLE: {
        QgsWkbTypes.PointGeometry:{
            'symbology': {
                'name': 'diamond',
                'color': '#487bb6',
                'size': '2'
            },
            'label' : {
                'field_name': 'nombre_punto',
                'text_size' : 8 ,
                'color' : QColor(40,51,105)
            }
        }
    },
    SURVEY_POINT_TABLE: {
        QgsWkbTypes.PointGeometry: {
            'symbology': {
                'name': 'diamond',
                'color': '#b2df8a',
                'size': '2'
            },
            'label': {
                'field_name': 'nombre_punto',
                'text_size' : 8 ,
                'color' : QColor(140,46,0)
            }
        }
    },
    PLOT_TABLE: {
        QgsWkbTypes.PointGeometry: {
            'symbology': {
                'name': 'star',
                'color': '#b80808',
                'size': '4.8'
            },
            'label': {
                'field_name': 'nombre_punto',
                'text_size' : 9 ,
                'color' : QColor(0,0,0)
            }
        },
        QgsWkbTypes.PolygonGeometry: {
            'symbology': {
                'name': 'Simple fill',
                'color': '166,206,227,128',
                'outline_color': '131,167,184,128'
            },
            'label': None
        }
    },
    BUILDING_TABLE: {
        QgsWkbTypes.PointGeometry:{
            'symbology': {
                'name': 'square',
                'color': '#000000',
                'size': '3'
            },
            'label': None
        },
        QgsWkbTypes.PolygonGeometry: {
            'symbology': {
                'name': 'Simple fill',
                'color': '251,154,153,128',
                'outline_color': '148,90,90,128'
            }, 'label': None
        }
    }
}
