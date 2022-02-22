# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM-COL
                             --------------------
        begin                : 2021-05-26
        git sha              : :%H$
        copyright            : (C) 2021 by Germán Carrillo (BSF Swissphoto)
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
import webbrowser

from qgis.PyQt.QtCore import (QObject,
                              QCoreApplication,
                              Qt,
                              pyqtSignal,
                              QUrl,
                              QEventLoop)
from qgis.PyQt.QtNetwork import (QNetworkRequest,
                                 QNetworkAccessManager)
from qgis.PyQt.QtWidgets import (QMenu,
                                 QAction,
                                 QApplication,
                                 QLabel)
from qgis.core import (Qgis,
                       QgsFeature,
                       QgsFeatureRequest,
                       QgsExpression,
                       QgsVectorLayer)

from asistente_ladm_col.config.config_db_supported import ConfigDBsSupported
from asistente_ladm_col.app_interface import AppInterface
from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.config.general_config import TEST_SERVER

from asistente_ladm_col.utils.utils import is_connected
from asistente_ladm_col.utils.qt_utils import ProcessWithStatus

from asistente_ladm_col.logic.ladm_col.tree_models import TreeModel


class LADMQueryController(QObject):

    close_view_requested = pyqtSignal()
    zoom_to_features_requested = pyqtSignal(QgsVectorLayer, list, dict)  # layer, ids, t_ids

    def __init__(self, db, ladm_data):
        QObject.__init__(self)

        self._db = db
        self._ladm_data = ladm_data

        self.logger = Logger()
        self.app = AppInterface()
        self.clipboard = QApplication.clipboard()
        self._layers = dict()
        self._ladm_queries = ConfigDBsSupported().get_db_factory(self._db.engine).get_ladm_queries()

        self._restart_dict_of_layers()
        self._add_layers()

        # To cache informal parcels,
        self._informal_parcels_info = tuple()  # ([parcel_t_id: parcel_number], [,], [,], ...)
        self._informal_index = -1
        self._informal_parcels_len = 0  # To avoid calculating this each time

    def _add_layers(self):
        self.app.core.get_layers(self._db, self._layers, load=True)
        if not self._layers:
            self._restart_dict_of_layers()  # Let it ready for the next call
            return None

        # Layer was found, listen to its removal so that we can deactivate the custom tool when that occurs
        self.disconnect_plot_layer()
        self._layers[self._db.names.LC_PLOT_T].willBeDeleted.connect(self._plot_layer_removed)

        # Layer was found, listen to its removal so that we can update the variable properly
        self.disconnect_parcel_layer()
        self._layers[self._db.names.LC_PARCEL_T].willBeDeleted.connect(self._parcel_layer_removed)

        # Layer was found, listen to its removal so that we can update the variable properly
        try:
            self._layers[self._db.names.COL_UE_BAUNIT_T].willBeDeleted.disconnect(self._uebaunit_table_removed)
        except:
            pass
        self._layers[self._db.names.COL_UE_BAUNIT_T].willBeDeleted.connect(self._uebaunit_table_removed)

    def _restart_dict_of_layers(self):
        self._layers = {
            self._db.names.LC_PLOT_T: None,
            self._db.names.LC_PARCEL_T: None,
            self._db.names.COL_UE_BAUNIT_T: None
        }

    def plot_layer(self):
        if self._layers[self._db.names.LC_PLOT_T] is None:
            self._add_layers()
        return self._layers[self._db.names.LC_PLOT_T]

    def parcel_layer(self):
        if self._layers[self._db.names.LC_PARCEL_T] is None:
            self._add_layers()
        return self._layers[self._db.names.LC_PARCEL_T]

    def uebaunit_table(self):
        if self._layers[self._db.names.COL_UE_BAUNIT_T] is None:
            self._add_layers()
        return self._layers[self._db.names.COL_UE_BAUNIT_T]

    def _plot_layer_removed(self):
        # The required layer was removed
        self.close_view_requested.emit()
        self._layers[self._db.names.LC_PLOT_T] = None

    def _parcel_layer_removed(self):
        self._layers[self._db.names.LC_PARCEL_T] = None

    def _uebaunit_table_removed(self):
        self._layers[self._db.names.COL_UE_BAUNIT_T] = None

    def disconnect_plot_layer(self):
        try:
            self._layers[self._db.names.LC_PLOT_T].willBeDeleted.disconnect(self._plot_layer_removed)
        except:
            pass

    def disconnect_parcel_layer(self):
        try:
            self._layers[self._db.names.LC_PARCEL_T].willBeDeleted.disconnect(self._parcel_layer_removed)
        except:
            pass

    def parcel_layer_name(self):
        return self._db.names.LC_PARCEL_T

    def t_id_name(self):
        return self._db.names.T_ID_F

    def parcel_number_name(self):
        return self._db.names.LC_PARCEL_T_PARCEL_NUMBER_F

    def previous_parcel_number_name(self):
        return self._db.names.LC_PARCEL_T_PREVIOUS_PARCEL_NUMBER_F

    def fmi_name(self):
        return self._db.names.LC_PARCEL_T_FMI_F

    def create_model(self, records):
        return TreeModel(self._db.names, data=records)

    def update_db_connection(self, db, ladm_col_db, db_source):
        self.close_view_requested.emit()

    def copy_value(self, value):
        self.clipboard.setText(str(value))

    def open_url(self, url):
        webbrowser.open(url)

    def zoom_to_feature(self, layer, t_id):
        self.zoom_to_features_requested.emit(layer, list(), {self._db.names.T_ID_F: [t_id]})

    def zoom_to_plots(self, plot_ids):
        self.zoom_to_features_requested.emit(self.plot_layer(), plot_ids, dict())

    def zoom_to_resulting_plots(self, records):
        # Zoom to plots retrieved from a search
        plot_t_ids = self._get_plot_t_ids_from_basic_info(records)
        if plot_t_ids:
            features = self._ladm_data.get_features_from_t_ids(self._layers[self._db.names.LC_PLOT_T],
                                                               self._db.names.T_ID_F, plot_t_ids, True, True)
            plot_ids = [feature.id() for feature in features]
            self.zoom_to_features_requested.emit(self.plot_layer(), plot_ids, dict())
            self.plot_layer().selectByIds(plot_ids)

    def _get_plot_t_ids_from_basic_info(self, records):
        res = []
        if records:
            if self._db.names.LC_PLOT_T in records:
                for element in records[self._db.names.LC_PLOT_T]:
                    res.append(element['id'])

        return res

    def open_feature_form(self, layer, t_id):
        # Note that it is important to fetch all feature attributes from the next call
        features = self._ladm_data.get_features_from_t_ids(layer, self._db.names.T_ID_F, [t_id], no_geometry=True)
        if features:
            self.app.gui.open_feature_form(layer, features[0])
        else:
            self.logger.warning(__name__, "No feature found in layer '{}' with t_id '{}'!!!".format(layer.name(), t_id))

    def download_image(self, url):
        res = False
        img = None
        msg = {'text': '', 'level': Qgis.Warning}
        if url:
            self.logger.info(__name__, "Downloading file from {}".format(url))
            msg_status_bar = "Downloading image from document repository (this might take a while)..."
            with ProcessWithStatus(msg_status_bar):
                if is_connected(TEST_SERVER):

                    nam = QNetworkAccessManager()
                    request = QNetworkRequest(QUrl(url))
                    reply = nam.get(request)

                    loop = QEventLoop()
                    reply.finished.connect(loop.quit)
                    loop.exec_()

                    status = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
                    if status == 200:
                        res = True
                        img = reply.readAll()
                    else:
                        res = False
                        msg['text'] = QCoreApplication.translate("SettingsDialog",
                                                                 "There was a problem connecting to the server. The server might be down or the service cannot be reached at the given URL.")
                else:
                    res = False
                    msg['text'] = QCoreApplication.translate("SettingsDialog",
                                                             "There was a problem connecting to Internet.")

        else:
            res = False
            msg['text'] = QCoreApplication.translate("SettingsDialog", "Not valid URL")

        if not res:
            self.logger.log_message(__name__, msg['text'], msg['level'])

        return res, img

    def get_plots_related_to_parcel(self, parcel_t_id):
        return self._ladm_data.get_plots_related_to_parcels(self._db, [parcel_t_id], None, self.plot_layer(), self.uebaunit_table())

    def get_layer(self, table_name):
        return self.app.core.get_layer(self._db, table_name, True)

    def search_data_basic_info(self, **kwargs):
        return self._ladm_queries.get_igac_basic_info(self._db, **kwargs)

    def search_data_legal_info(self, **kwargs):
        return self._ladm_queries.get_igac_legal_info(self._db, **kwargs)

    def search_data_physical_info(self, **kwargs):
        return self._ladm_queries.get_igac_physical_info(self._db, **kwargs)

    def search_data_economic_info(self, **kwargs):
        return self._ladm_queries.get_igac_economic_info(self._db, **kwargs)

    def query_informal_parcels(self):
        """
        :return: Triple --> parcel_number, current, total
        """
        # We always go to the DB to get informality info
        right_layer = self.app.core.get_layer(self._db, self._db.names.LC_RIGHT_T, True)
        informal_parcel_t_ids = self._ladm_data.get_informal_parcel_tids(self._db, right_layer)

        # Overwrite cache
        self._informal_parcels_info = tuple()
        self._informal_index = -1
        self._informal_parcels_len = 0

        if informal_parcel_t_ids:
            # Get parcel info ordered by parcel number
            parcels = self._ladm_data.get_features_from_t_ids(self.parcel_layer(),
                                                              self._db.names.T_ID_F,
                                                              informal_parcel_t_ids,
                                                              no_attributes=False,
                                                              no_geometry=False,
                                                              only_attributes=[self._db.names.LC_PARCEL_T_PARCEL_NUMBER_F],
                                                              order_by=self._db.names.LC_PARCEL_T_PARCEL_NUMBER_F)

            # Create a tuple of lists ([t_id: parcel_number], ...)
            self._informal_parcels_info = tuple([p[self._db.names.T_ID_F], p[self._db.names.LC_PARCEL_T_PARCEL_NUMBER_F]] for p in parcels)
            self._informal_parcels_len = len(self._informal_parcels_info)

        return self.get_next_informal_parcel()

    def get_next_informal_parcel(self):
        return self._traverse_informal_parcel_info()

    def get_previous_informal_parcel(self):
        return self._traverse_informal_parcel_info(False)

    def _traverse_informal_parcel_info(self, next=True):
        """
        Get a triple corresponding to an informal parcel number, the current index and the total of parcels.
        Note that if we get to the end and ask for the next parcel, we start over again. Similarly. if we are in the 1st
        parcel and ask for the previous one, then we get the latest one.

        :param next: Whether we need the next parcel's info or the previous one.
        :return: Triple --> parcel_number, current_idx, total_parcels (the current_idx returned is for display purposes)
        """
        if not self._informal_parcels_len:
            return '', 0, 0

        index = self._informal_index  # Get current index

        if next:  # Now set the current index
            self._informal_index = index + 1 if index + 1 < self._informal_parcels_len else 0
        else:  # Previous
            self._informal_index = index - 1 if index >= 1 else self._informal_parcels_len - 1

        return self._informal_parcels_info[self._informal_index][1], self._informal_index + 1, self._informal_parcels_len
