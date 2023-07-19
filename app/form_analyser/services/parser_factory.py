from form_analyser.enums.field_parser import FieldParser
from form_analyser.services.parser_service import ParserService, ParseDate, ParseNumbers, CurrencyParser, AbnParser


class ParserFactory:
    """ Return a child object of ParserService depending on type parameter"""

    def create_parser(type: FieldParser) -> ParserService:
        if type == FieldParser.DATE:
            print("Date parser selected")
            return ParseDate()
        elif type == FieldParser.NUMBERS:
            print("Number parser selected")
            return ParseNumbers()
        elif type == FieldParser.CURRENCY:
            print("Currency parser selected")
            return CurrencyParser()
        elif type == FieldParser.ABN:
            print("ABN parser selected")
            return AbnParser()
        else:
            return None
