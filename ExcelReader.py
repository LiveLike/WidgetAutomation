import openpyxl


def read_excel(file_path, sheet_name):
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook[sheet_name]

        data = []
        column_names = [cell.value for cell in sheet[1]]

        for row in sheet.iter_rows(min_row=2, values_only=True):
            if row[0] is None:
                break
            row_dict = {column_names[i]: value for i, value in enumerate(row)}
            data.append(row_dict)

        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
