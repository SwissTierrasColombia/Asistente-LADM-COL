# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-12-02
        git sha              : :%H$
        copyright            : (C) 2019 by Germán Carrillo (BSF Swissphoto)
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
from PyQt5.uic import loadUi
from qgis.PyQt.QtCore import (Qt,
                              QCoreApplication,
                              QSize,
                              pyqtSignal)
from qgis.PyQt.QtWidgets import (QWidget,
                                 QListWidgetItem)

from asistente_ladm_col.lib.logger import Logger
from asistente_ladm_col.lib.st_session.st_session import STSession
from asistente_ladm_col.lib.task_manager.tasks_model import TasksModel
from asistente_ladm_col.utils.ui import get_ui_class, get_ui_file_path

WIDGET_UI = get_ui_class('transition_system/tasks_widget.ui')


class TasksWidget(QWidget, WIDGET_UI):
    task_panel_requested = pyqtSignal(int)  # Selected task_id

    def __init__(self, user):
        QWidget.__init__(self)
        self.setupUi(self)
        self.logger = Logger()
        self.session = STSession()
        self._user = user

        self.lvw_tasks.itemSelectionChanged.connect(self.selection_changed)
        self.btn_start_task.clicked.connect(self.start_task)
        self.btn_close_task.clicked.connect(self.close_task)

        self.initialize_view()
        self.selection_changed()  # Initialize controls

    def initialize_view(self):
        tasks = self._get_user_tasks()
        self.update_task_count_label(len(tasks))
        # tasks_list = [task.get_name() for k, task in tasks.items()]
        #tasks_list = [task["name"] for task in tasks]
        #self.lvw_tasks.setModel(model)
        for k, task in tasks.items():
            self.add_task_widget_item_to_view(task)

    def _get_user_tasks(self):
        tasks = self.session.task_manager.get_tasks(self._user)
        print(len(tasks))
        for k, v in tasks.items():
            print([k], v.get_name())

        return tasks

    def selection_changed(self):
        enable = len(self.lvw_tasks.selectedItems()) == 1
        self.btn_start_task.setEnabled(enable)
        self.btn_close_task.setEnabled(enable)

    def update_task_count_label(self, count):
        self.lbl_task_count.setText(QCoreApplication.translate("TasksWidget",
               "{} pending task{}").format(count, "s" if count>1 else ""))

    def start_task(self):
        items = self.lvw_tasks.selectedItems()
        if items:
            task_id = items[0].data(Qt.UserRole)
            print("TASK id:{} STARTED!".format(task_id))
            self.task_panel_requested.emit(task_id)

    def close_task(self):
        items = self.lvw_tasks.selectedItems()
        if items:
            print("TASK id:{} CLOSED!".format(items[0].data(Qt.UserRole)))

    def add_task_widget_item_to_view(self, task):
        widget_item = loadUi(get_ui_file_path('transition_system/task_widget_item.ui'), QWidget())
        widget_item.lbl_name.setText(task.get_name())
        widget_item.lbl_description.setText(task.get_description())
        widget_item.lbl_status.setText(task.get_status())
        widget_item.lbl_created_at.setText("Created at: {}".format(task.get_creation_date()))
        widget_item.lbl_deadline.setText("Deadline: {}".format(task.get_deadline()))
        item = QListWidgetItem(self.lvw_tasks)
        self.lvw_tasks.setItemWidget(item, widget_item)
        item.setSizeHint(QSize(widget_item.width(), widget_item.height()))
        item.setData(Qt.UserRole, task.id())
        self.lvw_tasks.addItem(item)

    def _get_user_tasks2(self):
        import json
        return json.loads("""[
            {
                "id": 1,
                "name": "Integración XTF",
                "description": "Integración catastro-registro municipio ovejas.",
                "deadline": "2019-11-29T13:32:31.007+0000",
                "createdAt": "2019-11-29T13:32:31.007+0000",
                "closingDate": null,
                "taskState": {
                    "id": 1,
                    "name": "ASIGNADA"
                },
                "members": [
                    {
                        "id": 1,
                        "memberCode": 2,
                        "createdAt": "2019-11-29T13:32:31.014+0000",
                        "user": {
                            "id": 2,
                            "firstName": "German",
                            "lastName": "Carrillo",
                            "email": "carrillo.german@gmail.com",
                            "username": "gcarrillo",
                            "password": "",
                            "enabled": true,
                            "createdAt": "2019-11-29T13:35:42.935+0000",
                            "updatedAt": null,
                            "roles": [
                                {
                                    "id": 2,
                                    "name": "GESTOR"
                                }
                            ]
                        }
                    }
                ],
                "categories": [
                    {
                        "id": 1,
                        "name": "INTEGRACIÓN"
                    }
                ],
                "metadata": [
                    {
                        "id": 1,
                        "key": "hostname",
                        "value": "192.168.98.61"
                    },
                    {
                        "id": 2,
                        "key": "port",
                        "value": "5432"
                    },
                    {
                        "id": 3,
                        "key": "database",
                        "value": "integracion"
                    },
                    {
                        "id": 4,
                        "key": "username",
                        "value": "postgres"
                    },
                    {
                        "id": 5,
                        "key": "password",
                        "value": "123456"
                    }
                ]
            },
            {
                "id": 2,
                "name": "Generar XTF Cobol",
                "description": "Generar insumos en XTF para el municipio ovejas.",
                "deadline": "2019-12-24T23:59:00.007+0000",
                "createdAt": "2019-11-29T13:32:31.007+0000",
                "closingDate": null,
                "taskState": {
                    "id": 1,
                    "name": "ASIGNADA"
                },
                "members": [
                    {
                        "id": 1,
                        "memberCode": 2,
                        "createdAt": "2019-11-29T13:32:31.014+0000",
                        "user": {
                            "id": 2,
                            "firstName": "German",
                            "lastName": "Carrillo",
                            "email": "carrillo.german@gmail.com",
                            "username": "gcarrillo",
                            "password": "",
                            "enabled": true,
                            "createdAt": "2019-11-29T13:35:42.935+0000",
                            "updatedAt": null,
                            "roles": [
                                {
                                    "id": 2,
                                    "name": "GESTOR"
                                }
                            ]
                        }
                    }
                ],
                "categories": [
                    {
                        "id": 2,
                        "name": "GENERACIÓN XTF"
                    }
                ],
                "metadata": [
                    {
                        "id": 1,
                        "key": "hostname",
                        "value": "192.168.98.61"
                    },
                    {
                        "id": 2,
                        "key": "port",
                        "value": "5432"
                    },
                    {
                        "id": 3,
                        "key": "database",
                        "value": "integracion"
                    },
                    {
                        "id": 4,
                        "key": "username",
                        "value": "postgres"
                    },
                    {
                        "id": 5,
                        "key": "password",
                        "value": "123456"
                    }
                ]
            }
        ]""")
