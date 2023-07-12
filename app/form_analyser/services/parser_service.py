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
        print(validationResponseDto.input)
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

        return date_parser_util.extract_date(validationResponseDto)

    @property
    def value_type(self):
        return 'number'
