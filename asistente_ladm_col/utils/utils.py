# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              Asistente LADM_COL
                             --------------------
        begin                : 2019-02-06
        git sha              : :%H$
        copyright            : (C) 2019 by Jhon Galindo
        email                : jhonsigpjc@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import (QObject,
                              pyqtSignal,
                              QCoreApplication)

class Utils(QObject):
    log_excel_show_message_emitted = pyqtSignal(str, str)

    def __init__(self):
        QObject.__init__(self)
 
    def set_time_format(self, time):
        time_format = '.1f'
        unit_millisecond = "ms"
        unit_second = "seg"
        unit_minutes = "min"
        unit_hours = "h"
        unit_days = "D"
        
        if time < 1:
            return "{}{}".format(format(time*1000, '.0f'), unit_millisecond)
        elif time < 60:
            return "{}{}".format(format(time, time_format), unit_second)
        elif time >= 60 and time < 3600:
            minu = int(time/float(60))
            seg = 60*(time/float(60) - minu)
            return "{}{} {}{}".format(minu, unit_minutes, format(seg, time_format), unit_second)
        elif time >= 3600 and time < 86400:
            h = int(time/float(3600))
            minu = int(60*(time/float(3600) - h))
            seg = 60*((60*(time/float(3600) - h)) - minu)
            return "{}{} {}{} {}{}".format(h, unit_hours, minu, unit_minutes, format(seg, time_format), unit_second)
        elif time >= 86400:
            D = int(time/float(86400))
            h = int(24*(time/float(86400) - D))
            minu = int(60*((24*(time/float(86400) - D) - h)))
            seg = 60*((60*((24*(time/float(86400) - D) - h))) - minu)
            return "{}{} {}{} {}{} {}{}".format(D, unit_days, h, unit_hours, minu, unit_minutes, format(seg, time_format), unit_second)

    def send_signal_log_excel(self, msg, text):
        self.log_excel_show_message_emitted.emit(msg, text)
