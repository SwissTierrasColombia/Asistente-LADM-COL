# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2018-02-06
        git sha              : :%H$
        copyright            : (C) 2018 by Germán Carrillo (BSF Swissphoto)
        email                : gcarrillo@linuxmail.org
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
import qgis
from qgis.PyQt.QtCore import QObject

class ProjectGeneratorUtils(QObject):

    def __init__(self):
        QObject.__init__(self)

    def load_layers(self, layer_list, db):
        if 'projectgenerator' in qgis.utils.plugins:
            pg = qgis.utils.plugins["projectgenerator"]
            generator = pg.get_generator()("ili2pg" if db.mode=="pg" else "ili2gpkg",
                db.uri, "smart2", db.schema)
            layers = generator.layers(layer_list)
            relations = generator.relations(layers, layer_list)
            legend = generator.legend(layers)
            pg.create_project(layers, relations, legend)
        else:
            print("El plugin Project Generator es un prerrequisito, instálalo antes de usar Asistente LADM_COL.")
