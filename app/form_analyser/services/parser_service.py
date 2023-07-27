import re
from abc import abstractmethod
from utils import date_parser_util
from form_analyser.services.response_dto import ValidationDto


class ParserService:
    """ Asbstact ParserService class"""

    @abstractmethod
    def parse(self, value) -> ValidationDto:
        pass


class ParseDate(ParserService):
    """ Child of ParserService and used to parse date strings"""

    def __str__(self) -> str:
        return 'ParseDate'

    def parse(self, value) -> ValidationDto:
        validationResponseDto = ValidationDto(
            name=str(self),  input=value, parms="", output="", status="", message="")
        return date_parser_util.extract_date(validationResponseDto)

    @property
    def value_type(self):
        return 'datetime'


class ParseNumbers(ParserService):
    """ Child of ParserService and used to parse numbers from strings"""

    def __str__(self) -> str:
        return 'ParseNumbers'

    def parse(self, value) -> ValidationDto:
        validationResponseDto = ValidationDto(
            name=str(self),  input=value, parms="", output="", status="", message="")

        if value is not None:
            try:
                pattern = r"[^\d.]"
                stripped_string = re.sub(pattern, "", value)
                number = float(stripped_string)
                validationResponseDto.output = number
            except (ValueError, TypeError):
                validationResponseDto.output = None
                validationResponseDto.message = 'Failed to parse number'

        return validationResponseDto

    @property
    def value_type(self):
        return 'number'


class CurrencyParser(ParserService):
    """ Child of ParserService and used to parse currency from strings"""

    def __str__(self) -> str:
        return 'CurrencyParser'

    def parse(self, value) -> ValidationDto:
        validationResponseDto = ValidationDto(
            name=str(self),  input=value, parms="", output="", status="", message="")

        if value is not None:
            try:
                # Remove non-numeric characters from the string
                numeric_string = ''.join(filter(str.isdigit, value))

                # Convert the string to float
                number = float(numeric_string)
                validationResponseDto.output = number
            except (ValueError, TypeError):
                validationResponseDto.output = None
                validationResponseDto.message = 'Failed to parse currency'

        return validationResponseDto

    @property
    def value_type(self):
        return 'currency'


class AbnParser(ParserService):
    """ Child of AbnParser and used to parse ABN from strings"""

    def __str__(self) -> str:
        return 'AbnParser'

    def parse(self, value) -> ValidationDto:
        validationResponseDto = ValidationDto(
            name=str(self),  input=value, parms="", output="", status="", message="")

        validationResponseDto.output = None
        if value is not None:
            try:
                if value.strip() != "":
                    # Remove spaces
                    string = value.replace(" ", "")
                    # Remove special characters
                    string = re.sub(r"[^\w\s]", "", string)
                    # Trim the text
                    string = string.strip()
                    validationResponseDto.output = string

            except (ValueError, TypeError):
                validationResponseDto.message = 'Failed to parse abn'

        return validationResponseDto

    @property
    def value_type(self):
        return 'abn'
