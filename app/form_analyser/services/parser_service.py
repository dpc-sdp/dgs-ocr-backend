import re
from abc import abstractmethod
from utils import date_parser_util
from form_analyser.services.response_dto import ValidationDto
from dateutil.parser import parse
from form_analyser.enums.action_status import ActionStatus


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
        # return date_parser_util.extract_date(validationResponseDto)
        if value is not None:
            try:
                value = remove_text_ignore_case(
                    value, ["local standard time", "(", ")", "on", "at"])
                validationResponseDto.output = parse_datetime(
                    value).strftime("%Y-%m-%d %H:%M")
                validationResponseDto.status = ActionStatus.SUCCESS.value
            except (ValueError, TypeError):
                validationResponseDto.output = None
                validationResponseDto.message = 'Failed to parse date'

            if validationResponseDto.output is None:
                validationResponseDto = date_parser_util.extract_date(
                    validationResponseDto)

        return validationResponseDto

    @property
    def value_type(self):
        return 'datetime'


class ParseTime(ParserService):
    """ Child of ParserService and used to parse date strings to time"""

    def __str__(self) -> str:
        return 'ParseTime'

    def parse(self, value) -> ValidationDto:
        validationResponseDto = ValidationDto(
            name=str(self),  input=value, parms="", output="", status="", message="")
        # return date_parser_util.extract_date(validationResponseDto)
        if value is not None:
            try:
                timezone = get_timezone(value)
                value = remove_text_ignore_case(
                    value, ["local standard time", "(", ")", "on", "at"])
                validationResponseDto.output = parse_datetime(
                    value).strftime("%H:%M")
                if timezone is not None:
                    validationResponseDto.output = validationResponseDto.output+" " + timezone

                validationResponseDto.status = ActionStatus.SUCCESS.value
            except (ValueError, TypeError):
                validationResponseDto.output = "00:00"
                validationResponseDto.message = 'Failed to parse time'

            if validationResponseDto.output is None:
                validationResponseDto = date_parser_util.extract_date(
                    validationResponseDto)

        return validationResponseDto

    @property
    def value_type(self):
        return 'time'


timezone_pattern = re.compile(
    r'\b(?:LST|AEST|Local Standard Time|local standard time)\b', re.IGNORECASE)


def get_timezone(dt_string):
    match = timezone_pattern.search(dt_string)
    if match:
        return match.group(0)
    return None


def parse_datetime(date_time_str):
    try:
        date_time_obj = parse(date_time_str)
        return date_time_obj
    except ValueError:
        # If the string cannot be parsed, you can raise an exception or return None, depending on your needs.
        raise ValueError("Unable to parse the date and time string.")


def remove_text_ignore_case(sentence, texts_to_remove):
    # Iterate through each text in the texts_to_remove array
    for text in texts_to_remove:
        # Create a regular expression pattern with the 're.IGNORECASE' flag to ignore case
        pattern = re.compile(re.escape(text), re.IGNORECASE)

        # Use the 'sub' function to replace occurrences of the text with an empty string
        sentence = pattern.sub('', sentence)

    return sentence


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
