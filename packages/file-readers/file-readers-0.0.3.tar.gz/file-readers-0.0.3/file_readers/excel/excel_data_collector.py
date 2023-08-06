from file_readers.data_collector import BaseDataCollector
from openpyxl.cell import column_index_from_string


class ExcelDataCollector(BaseDataCollector):

    def __init__(self, debug=False):
        self.debug = debug
        self.data = []
        self.headers = []

    def collect_data(self, source):
        """Collects all data from a sheet

        Args:
            source: A list or tuple of Cell objects
        """

        row = {}
        for cellObj in source:
            if "1" in cellObj.coordinate:
                self.headers.append(cellObj.value)
                continue

            index = column_index_from_string(cellObj.coordinate[0]) - 1
            header = self.headers[index]
            row[header] = cellObj.value
        if self.debug:
            print(row)
        if row:
            self.data.append(row)
