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
    if time < 60:
        return "{}{}".format(format(time, time_format), "seg")
    elif time >= 60 and time < 3600:
        return "{}{}".format(format(time/float(60), time_format), "min")
    elif time >= 3600 and time < 86400:
        return "{}{}".format(format(time/float(3600), time_format), "h")
    elif time >= 86400:
        return "{}{}".format(format(time/float(86400), time_format), "D")