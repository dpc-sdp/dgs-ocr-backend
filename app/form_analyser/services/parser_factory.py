from form_analyser.enums.field_parser import FieldParser
from form_analyser.services.parser_service import ParserService, ParseDate, ParseNumbers


class ParserFactory:
    """ Return a child object of ParserService depending on type parameter"""

    def create_parser(type: FieldParser) -> ParserService:
        if type == FieldParser.DATE:
            print("Date parser selected")
            return ParseDate()
        elif type == FieldParser.INTEGER:
            print("Number parser selected")
            return ParseNumbers()
        else:
            return None
