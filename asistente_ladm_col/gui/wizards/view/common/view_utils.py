# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-09-10
        git sha              : :%H$
        copyright            : (C) 2019 by Leo Cardona (BFS Swissphoto)
                               (C) 2021 by Yesid Polanía (BFS Swissphoto)
        email                : leo.cardona.p@gmail.com
                               yesidpol.3@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
 """
from qgis.PyQt.QtCore import (QSettings,
                              QObject,
                              pyqtSignal,
                              QCoreApplication)
from qgis.PyQt.QtWidgets import (QWizard,
                                 QMessageBox)


class ViewUtils:

    @staticmethod
    def show_message_associate_geometry_creation(message) -> bool:
        # TODO parent in message box
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText(message)
        msg.setWindowTitle(QCoreApplication.translate("WizardTranslations", "Continue editing?"))
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.No).setText(QCoreApplication.translate("WizardTranslations", "No, close the wizard"))
        reply = msg.exec_()

        return reply != QMessageBox.No

    @staticmethod
    def enable_digitize_actions(iface, enable: bool):
        iface.actionToggleEditing().setVisible(enable)

        iface.actionSaveActiveLayerEdits().setVisible(enable)
        iface.actionSaveAllEdits().setVisible(enable)
        iface.actionSaveEdits().setVisible(enable)

        iface.actionAllEdits().setVisible(enable)
        iface.actionCancelAllEdits().setVisible(enable)
        iface.actionCancelEdits().setVisible(enable)

        iface.actionRollbackAllEdits().setVisible(enable)
        iface.actionRollbackEdits().setVisible(enable)
