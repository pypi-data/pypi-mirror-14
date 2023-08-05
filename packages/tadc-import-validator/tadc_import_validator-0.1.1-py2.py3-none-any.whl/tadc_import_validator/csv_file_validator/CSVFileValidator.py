import unicodecsv as csv
from logbook import Logger
from ..tadc_import_row import TADCImportRow
from collections import OrderedDict

__author__ = 'timhodson'

log = Logger('CSVFileValidator')


class CSVFileValidator:
    """
    Validates a CSV File presented as a TADC Import data file.
    """

    def __init__(self, csv_file, header_rows=2):
        self.csv_file_name = csv_file
        log.info("Processing File: {}".format(self.csv_file_name))
        self.header_rows = int(header_rows)
        log.info("Expecting {} header rows".format(self.header_rows))

        self.error_summary = OrderedDict()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self

    def validate_file(self):
        """
        Read all rows of a CSV file and output a message about whether is is valid or not.
        :return:
        """

        with open(self.csv_file_name) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', dialect='excel', quotechar='"')
            row_counter = 0
            for row in csvreader:
                if row_counter >= self.header_rows:
                    try:
                        tadc_row = TADCImportRow()
                        tadc_row.load(row)
                        if tadc_row.is_valid():
                            log.info("row {} is valid".format(row_counter))
                        else:
                            log.error(u"row {} is not valid".format(row_counter))
                            for error in tadc_row.get_errors():
                                self.add_error_summary(row_counter, error)
                                log.error(u"column {}: {}".format(error['column'], error['message']))
                    except Exception as e:
                        log.error("{}".format(e.message))
                row_counter += 1
            self.print_error_summary()

    def add_error_summary(self, row, error):
        error_column = error['column']
        error_message = error['message']
        if not self.error_summary.get(row):
            self.error_summary[row] = {}
        if not self.error_summary[row].get(error_column):
            self.error_summary[row][error_column] = error_message

    def print_error_summary(self):
        if len(self.error_summary) > 0:
            log.info("Errors were found for the following columns")
            for row, columns in self.error_summary.iteritems():
                for column in columns:
                    # rows are zero counted so fix with a +1 for humans to read.
                    log.info("Row {} column {} : {}".format(row+1, column, columns[column]))
        else:
            log.info("No errors found. Woohoo!")
