from openpyxl import load_workbook


class ExcelAdapter(object):

    def convert_to_list(self, filename, sheet_name, has_header=True):
        data = list()
        wb = load_workbook(filename=filename, data_only=True)
        sheet = wb[sheet_name]
        row_num = 1
        for row in sheet.rows:
            row_data = list()
            if row_num == 1 and has_header:
                row_num += 1
                continue
            for column in range(0, len(row)):
                row_data.append(row[column].value)
            data.append(row_data)
            row_num += 1
        return data


