# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin                : 2020-05-06
        git sha              : :%H$
        copyright            : (C) 2020 by Germán Carrillo (SwissTierras Colombia)
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
from qgis import processing
from qgis.core import QgsCoordinateReferenceSystem
from qgis.processing import alg

@alg(name='reprojectlayertoctm12', label='Reproject layer to CTM12',
     group='ladmcol', group_label='LADM-COL')
@alg.input(type=alg.SOURCE, name='INPUT', label='Input layer')
@alg.input(type=alg.VECTOR_LAYER_DEST, name='REPROJECTED_OUTPUT',
           label='Layer in CTM12')

def reprojectlayertoctm12(instance, parameters, context, feedback, inputs):
    """
    Reproject map layers to CTM12.
    """
    if feedback.isCanceled():
        return {}

    reprojected_result = processing.run('native:reprojectlayer',
                                        {'INPUT': parameters['INPUT'],
                                         'TARGET_CRS': QgsCoordinateReferenceSystem(38820),
                                         'OUTPUT': parameters['REPROJECTED_OUTPUT']
                                         },
                                        is_child_algorithm=True,
                                        context=context,
                                        feedback=feedback)

    return {'REPROJECTED_OUTPUT': reprojected_result['OUTPUT']}