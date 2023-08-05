import time
import sys
import datetime
import os
from logbook import Logger, FileHandler, StreamHandler
from tadc_import_validator.csv_file_validator import CSVFileValidator

__author__ = 'timhodson'

log = Logger("validate_csv_file")


def main():
    """
    The main routine which kicks everything off
    :return:
    """

    # register some logging handlers
    log_handler = FileHandler('/tmp/validate_csv_{}.log'.format(os.path.basename(time.strftime('%Y%m%d-%H%M%S'))),
                          mode='w', level='DEBUG', bubble=True)
    stdout_handler = StreamHandler(sys.stdout, level='INFO', bubble=True)

    with stdout_handler.applicationbound():
        with log_handler.applicationbound():
            start = time.time()
            log.info("starting at {}".format(time.strftime('%l:%M%p %Z on %b %d, %Y')))

            if len(sys.argv) < 3:
                log.error("You need to specify the path to a CSV file and how many header rows are present")
                log.error("Usage: {} ./path/to/file.csv <numHeaderRows>".format(sys.argv[0]))
                exit(1)
            else:
                filename = sys.argv[1]
                header_rows = sys.argv[2]

            with CSVFileValidator(csv_file=filename, header_rows=header_rows) as validator:
                validator.validate_file()
                log.info("Running time: {}".format(str(datetime.timedelta(seconds=(round(time.time() - start, 3))))))

if __name__ == "__main__":
    main()