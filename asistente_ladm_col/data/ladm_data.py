# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-03-20
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
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsApplication,
                       QgsFeatureRequest,
                       QgsExpression,
                       QgsWkbTypes,
                       Qgis)

from ..config.table_mapping_config import (ID_FIELD,
                                           PLOT_TABLE,
                                           UEBAUNIT_TABLE_PARCEL_FIELD,
                                           UEBAUNIT_TABLE_PLOT_FIELD,
                                           UEBAUNIT_TABLE,
                                           PARCEL_TABLE)

class LADM_DATA():
    """
    High-level class to get related information from the LADM-COL database.
    """
    def __init__(self, qgis_utils):
        self.qgis_utils = qgis_utils
        self.log = QgsApplication.messageLog()

    def get_plots_related_to_parcel(self, db, t_id, field_name=ID_FIELD, plot_layer=None, uebaunit_table=None):
        """
        :param db: DB Connector object
        :param t_id: parcel t_id
        :param field_name: The field name to get from DB for the matching features, use None for the QGIS internal ID
        :param plot_layer: Plot QGIS layer, in case it exists already in the caller
        :param uebaunit_table: UEBaunit QGIS table, in case it exists already in the caller
        :return: list of plot ids related to the parcel
        """
        required_layers = {
            PLOT_TABLE: {'name': PLOT_TABLE, 'geometry': QgsWkbTypes.PolygonGeometry},
            UEBAUNIT_TABLE: {'name': UEBAUNIT_TABLE, 'geometry': None}}

        if plot_layer is not None:
            del required_layers[PLOT_TABLE]
        if uebaunit_table is not None:
            del required_layers[UEBAUNIT_TABLE]

        if required_layers:
            res_layers = self.qgis_utils.get_layers(db, required_layers, load=True)

            if PLOT_TABLE in required_layers:
                plot_layer = res_layers[PLOT_TABLE]
                if plot_layer is None:
                    self.qgis_utils.message_emitted.emit(
                        QCoreApplication.translate("LADM_DATA", "Plot layer couldn't be found... {}").format(
                                                            db.get_description()),
                                                   Qgis.Warning)
                    return

            if UEBAUNIT_TABLE in required_layers:
                uebaunit_table = res_layers[UEBAUNIT_TABLE]
                if uebaunit_table is None:
                    self.qgis_utils.message_emitted.emit(
                        QCoreApplication.translate("LADM_DATA", "UEBAUnit table couldn't be found... {}").format(
                            db.get_description()),
                        Qgis.Warning)
                    return

        features = uebaunit_table.getFeatures("{}={} AND {} IS NOT NULL".format(
                                                    UEBAUNIT_TABLE_PARCEL_FIELD,
                                                    t_id,
                                                    UEBAUNIT_TABLE_PLOT_FIELD))

        plot_t_ids = list()
        for feature in features:
            plot_t_ids.append(feature[UEBAUNIT_TABLE_PLOT_FIELD])

        if field_name == ID_FIELD:
            return plot_t_ids

        plot_ids = list()
        if plot_t_ids:
            request = QgsFeatureRequest(
                        QgsExpression("{} IN ({})".format(ID_FIELD,
                                                          ",".join([str(id) for id in plot_t_ids]))))

            field_found = False
            if field_name is None: # We are only interested in the QGIS internal id, no need to get other fields
                request.setNoAttributes()
            else:
                field_found = plot_layer.fields().indexOf(field_name) != -1
                if field_found:
                    request.setSubsetOfAttributes([field_name], plot_layer.fields())

            request.setFlags(QgsFeatureRequest.NoGeometry)
            features = plot_layer.getFeatures(request)

            for feature in features:
                if field_name is None:
                    plot_ids.append(feature.id())
                else:
                    if field_found:
                        plot_ids.append(feature[field_name])

        return plot_ids

    def get_parcels_related_to_plot(self, db, t_id, field_name=ID_FIELD, parcel_table=None, uebaunit_table=None):
        """
        :param db: DB Connector object
        :param t_id: plot t_id
        :param field_name: The field name to get from DB for the matching features, use None for the QGIS internal ID
        :param parcel_table: Parcel QGIS layer, in case it exists already in the caller
        :param uebaunit_table: UEBaunit QGIS table, in case it exists already in the caller
        :return: list of parcel ids related to the parcel
        """
        required_layers = {
            PARCEL_TABLE: {'name': PARCEL_TABLE, 'geometry': None},
            UEBAUNIT_TABLE: {'name': UEBAUNIT_TABLE, 'geometry': None}}

        if parcel_table is not None:
            del required_layers[PARCEL_TABLE]
        if uebaunit_table is not None:
            del required_layers[UEBAUNIT_TABLE]

        if required_layers:
            res_layers = self.qgis_utils.get_layers(db, required_layers, load=True)

            if PARCEL_TABLE in required_layers:
                parcel_table = res_layers[PARCEL_TABLE]
                if parcel_table is None:
                    self.qgis_utils.message_emitted.emit(
                        QCoreApplication.translate("LADM_DATA", "Parcel table couldn't be found... {}").format(
                                                            db.get_description()),
                                                   Qgis.Warning)
                    return

            uebaunit_table = res_layers[UEBAUNIT_TABLE]
            if uebaunit_table is None:
                self.qgis_utils.message_emitted.emit(
                    QCoreApplication.translate("LADM_DATA", "UEBAUnit table couldn't be found... {}").format(
                        db.get_description()),
                    Qgis.Warning)
                return

        features = uebaunit_table.getFeatures("{}={} AND {} IS NOT NULL".format(
                                                    UEBAUNIT_TABLE_PLOT_FIELD,
                                                    t_id,
                                                    UEBAUNIT_TABLE_PARCEL_FIELD))

        parcel_t_ids = list()
        for feature in features:
            parcel_t_ids.append(feature[UEBAUNIT_TABLE_PARCEL_FIELD])

        if field_name == ID_FIELD:
            return parcel_t_ids

        parcel_ids = list()
        if parcel_t_ids:
            request = QgsFeatureRequest(
                        QgsExpression("{} IN ({})".format(ID_FIELD,
                                                          ",".join([str(id) for id in parcel_t_ids]))))

            field_found = False
            if field_name is None:  # We are only interested in the QGIS internal id, no need to get other fields
                request.setNoAttributes()
            else:
                field_found = parcel_table.fields().indexOf(field_name) != -1
                if field_found:
                    request.setSubsetOfAttributes([ID_FIELD, field_name], parcel_table.fields())

            features = parcel_table.getFeatures(request)

            for feature in features:
                if field_name is None:
                    parcel_ids.append(feature.id())
                else:
                    if field_found:
                        parcel_ids.append(feature[field_name])

        return parcel_ids
