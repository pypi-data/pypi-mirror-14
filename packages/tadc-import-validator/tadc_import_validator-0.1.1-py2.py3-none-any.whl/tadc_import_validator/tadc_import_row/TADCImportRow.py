import string
import re
from logbook import Logger

log = Logger("TADCImportRow")


class TADCImportRow:
    """
    A class which represents and validates an import row of a "TADC Import Spreadsheet"
    Probably better ways to name this but for now we'll go with this.
    """

    # Date format expected by this class.
    DATE_FORMAT_REGEX = re.compile(u"\d{4}[/]\d{2}[/]\d{2}")  # e.g. 2015/01/31
    YEAR_FORMAT_REGEX = re.compile(u"\d{4}")  # 4 digits
    PAGE_NUMBER_REGEX = re.compile(u"^\d+$")  # one or more digits for the WHOLE string.

    def __init__(self):
        # the row dictionary while we work on it internally
        self._row = {}
        # a list of errors when validating
        self._errors = []
        # current column we are working on
        self._current_column = ''
        # make sure that our internal model is set up
        self.initialise()

        # validation rules
        self.validationRules = {
            "A": {"name": "Course Code", "kev": "rfe_code",
                  "rule": self.validate_mandatory,
                  "error": "Missing mandatory field"},
            "B": {"name": "Course Description", "kev": "rfe_name",
                  "rule": self.validate_mandatory,
                  "error": "Missing mandatory field"},
            "C": {"name": "Student numbers", "kev": "rfe_size",
                  "rule": self.validate_mandatory,
                  "error": "Missing mandatory field"},
            "D": {"name": "Request start date", "kev": "rfe_sdate", "kevParser": "kevDate",
                  "rule": self.validate_date,
                  "error": "Missing mandatory date field, or field is incorrectly formatted"},
            "E": {"name": "Request end date", "kev": "rfe_edate", "kevParser": "kevDate",
                  "rule": self.validate_date,
                  "error": "Missing mandatory date field, or field is incorrectly formatted"},
            "F": {"name": "Requester Name", "kev": "req_name",
                  "rule": self.validate_mandatory,
                  "error": "Missing mandatory field"},
            "G": {"name": "Requester email", "kev": "req_email",
                  "rule": self.validate_mandatory,
                  "error": "Missing mandatory field"},
            "H": {"name": "Section Type (chapter, article, page range)", "kev": "rft_genre",
                  "kevParser": "kevSectionType",
                  "rule": self.validate_section_type,
                  "error": "Field should be 'C', 'Chapter', 'P', 'Page Range', 'Article' or 'A'"},
            "I": {"name": "ISBN / ISSN", "kev": "rft_isbn", "kevParser": "kevISBN"},
            "J": {"name": "DOI", "kev": "rft_doi", "kevParser": "kevDOI"},
            "K": {"name": "Title of Book/Journal",
                  "rule": self.validate_mandatory,
                  "error": "Missing mandatory field"},
            "L": {"name": "Author of Book"},
            "M": {"name": "Journal Year",
                  "rule": self.validate_journal_year,
                  "error": "Missing field for articles"},
            "N": {"name": "Volume Number",
                  "rule": self.validate_journal_volume,
                  "error": "Missing field for articles"},
            "O": {"name": "Issue"},
            "P": {"name": "Extract title", "kev": "rft_atitle",
                  "rule": self.validate_extract_title,
                  "error": "Missing mandatory field"},
            "Q": {"name": "Author of Extract",
                  "rule": self.validate_author_of_extract,
                  "error": "Missing mandatory field"},
            "R": {"name": "Publisher",
                  "rule": self.validate_publisher_name,
                  "error": "Missing mandatory field"},
            "S": {"name": "Place of publication"},
            "T": {"name": "Page No. From", "kev": "rft_spage",
                  "rule": self.validate_page_number,
                  "error": "Starting page number either missing mandatory field or contains a page range"},
            "U": {"name": "Page No. To", "kev": "rft_epage",
                  "rule": self.validate_page_number,
                  "error": "Ending page number either missing mandatory field or contains a page range"},
            "V": {"name": "Source",
                  "rule": self.validate_source,
                  "error": "Field should be 'A', 'C' or 'D'"},
            "W": {"name": "FILENAME",
                  "rule": self.validate_mandatory,
                  "error": "Missing mandatory field"},
            "X": {"name": "LIST ITEM URL"},
            "Y": {"name": "Local URL/Location"},
            "Z": {"name": "Contains incidental artwork",
                  "rule": self.validate_incidental_artwork,
                  "error": "Must be a value of either 'y' or 'n'"}
        }

    def initialise(self):
        """
        Setup our basic dict ready to hold some data.
        :return:
        """
        for letter in list(string.ascii_uppercase):
            self._row[letter] = {"value": ""}

    def output_for_csv(self):
        """
        Build a list object redy to be written to a CSV file.
        :return:
        """
        output = []
        for letter in string.ascii_uppercase:
            if self._row[letter]['value'] in [None, "None"]:
                output.append("")
            else:
                output.append(self._row[letter]['value'])
        return output

    def output_for_invalid_csv(self):
        """
        Build a list object ready to be written to a CSV file.
        This will include reasons why the row is invalid
        :return:
        """
        output = []
        for letter in string.ascii_uppercase:
            output.append(self._row[letter]['value'])

        error_column = []
        for error in self.get_errors():
            error_column.append(u"column {}: {}".format(error['column'], error['message']))
        output.append(u", ".join(error_column))

        return output

    def add_data_to_column(self, column, data):
        """
        Load some data for particular column into the row.
        :param column:
        :param data:
        :return:
        """
        # make sure this is a string
        data = unicode(data)
        self._row[column]['value'] = data.strip()

    def load(self, row):
        """
        Load a list representing a TADC import row into our internal structures.
        :param row:
        :return:
        """
        for idx, letter in enumerate(string.ascii_uppercase):
            if idx < len(row):
                self.add_data_to_column(letter, row[idx])
            else:
                self.add_data_to_column(letter, '')

    def validate(self):
        """
        Validate that the data we have is valid.
        :return:
        """
        # reset any errors
        self._errors = []
        # check each column against it's appropriate validation rule
        for column in self._row.keys():
            self._current_column = column
            rule = self.validationRules[column].get('rule', self.trust_this_value)
            rule(self._row[column]['value'])

    def validate_mandatory(self, val):
        """
        This column is mandatory and so there should be a value.
        """
        if val.strip() != '':
            return True
        self.set_rule_error()
        return False

    def validate_section_type(self, val):
        """
        Validate the section types are correct values
        """
        if val.lower() in ['a', 'c', 'p', 'article', 'chapter', 'page range']:
            return True
        self.set_rule_error()
        return False

    def validate_journal_volume(self, val):
        """
        year, issue or volume should be present
        """
        if all([val.strip() == '', self._row['M']['value'].strip() == '', self._row['O']['value'].strip() == '']):
            self.set_rule_error()
            return False
        return True

    def validate_journal_year(self, val):
        """
        year, issue or volume should be present
        """
        if all([val.strip() == '', self._row['N']['value'].strip() == '', self._row['O']['value'].strip() == '']):
            self.set_rule_error()
            return False
        # if not re.match(self.YEAR_FORMAT_REGEX, val.strip()):
        #     self.set_rule_error()
        #     return False
        return True

    def validate_journal_issue(self, val):
        """
        year, issue or volume should be present
        """
        if all([val.strip() == '', self._row['M']['value'].strip() == '', self._row['N']['value'].strip() == '']):
            self.set_rule_error()
            return False
        return True

    def validate_extract_title(self, val):
        """
        If an article or chapter we care that the extract title is false - other wise we don't care
        :param val:
        :return:
        """
        if self._row['H']['value'].lower() in ['a', 'article', 'c', 'chapter']:
            if val.strip() == '':
                self.set_rule_error()
                return False
            return True
        return True

    def validate_author_of_extract(self, val):
        """
        Author of extract should be present if this is an article
        If a book or chapter, only mandatory if the book author is not set.
        """
        if self._row['H']['value'].lower() in ['a', 'article']:
            if val.strip() == '':
                self.set_rule_error()
                return False
            return True
        elif val.strip() == '' and self._row['L']['value'].strip() == '':
            self.set_rule_error()
            return False
        return True

    def validate_publisher_name(self, val):
        """
        Publisher name should be present for everything except articles
        :return:
        """
        if self._row['H']['value'].lower() in ['a', 'article']:
            return True

        if val.strip() == '':
            self.set_rule_error()
            return False

    def validate_source(self, val):
        """
        Source values should be one of these A, B, C, D
        :return:
        """
        if val.strip() not in ['A', 'B', 'C', 'D']:
            self.set_rule_error()
            return False
        return True

    @staticmethod
    def trust_this_value(val):
        """
        We don't actually care about this value so hey it's valid!
        :param val:
        :return:
        """
        return True

    def validate_date(self, val):
        if val.strip() == '':
            self.set_rule_error()
            return False
        if re.match(self.DATE_FORMAT_REGEX, val.strip()):
            return True
        self.set_rule_error()
        return False

    def validate_page_number(self, val):
        if not re.match( self.PAGE_NUMBER_REGEX , val):
            self.set_rule_error()
            return False
        return True

    def validate_incidental_artwork(self, val):
        """
        Check that if a value is set it is either 'y' or 'n'
        """
        if val.strip() == '':
            return True
        elif val not in ['y', 'n']:
            self.set_rule_error()
            return False

    def set_rule_error(self):
        """
        Set an error message based on the column which is currently being validated
        """
        row_error = {
                "column": self._current_column,
                "message": u"{} value: '{}' error: {}".format(
                    self.validationRules[self._current_column]['name'],
                    self._row[self._current_column]['value'],
                    self.validationRules[self._current_column]['error']
                )
            }

        self._errors.append(row_error)

    def get_errors(self):
        return self._errors

    def is_valid(self):
        """
        Check to see if this row is valid.
        Each call to is_valid() will validate all values and raise an exception for the whole row.
        """
        self.validate()
        if len(self.get_errors()) > 0:
            #raise TADCImportRowValidationException("Some values were not valid", self.get_errors())
            return False
        return True


class TADCImportRowValidationException(Exception):
    """
    TADC Import Row validation exception
    """
    def __init__(self, message, errors):
        super(Exception, self).__init__(message)
        self.errors = errors
