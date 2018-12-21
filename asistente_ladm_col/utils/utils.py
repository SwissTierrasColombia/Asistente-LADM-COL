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