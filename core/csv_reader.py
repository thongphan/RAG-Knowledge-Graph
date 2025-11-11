import csv

class CSVReader:
    def __init__(self, filepath, headers=None):
        self.filepath = filepath
        self.headers = headers

    def read_rows(self):
        with open(self.filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=self.headers)
            for row in reader:
                yield row
