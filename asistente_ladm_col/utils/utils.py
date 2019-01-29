import os
try:
    import xlrd
except:
    print("Install library xlrd not found.")

def get_number_of_rows_in_excel_file(excel_file_route, sheet, header_rows=1):
    if os.path.exists(excel_file_route):
        workbook = xlrd.open_workbook(excel_file_route)
        if type(sheet) == int:
            worksheet = workbook.sheet_by_index(sheet)
            return worksheet.nrows - header_rows
        else:
            worksheet = workbook.sheet_by_name(sheet)
            return worksheet.nrows - header_rows
    else:
        print("ERROR: Excel file not found...")

    return None

def set_time_format(time):
    time_format = '.2f'
    unit_millisecond = "ms"
    unit_second = "seg"
    unit_minutes = "min"
    unit_hours = "h"
    unit_days = "D"
    
    if time < 1:
        return "{}{}".format(format(time*1000, time_format), unit_millisecond)
    elif time < 60:
        seg = time
        return "{}{}".format(format(seg, time_format), unit_second)
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