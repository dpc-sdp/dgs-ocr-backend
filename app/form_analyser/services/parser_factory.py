from form_analyser.enums.field_parser import FieldParser
from form_analyser.services.parser_service import ParserService, ParseDate, ParseNumbers, CurrencyParser, AbnParser
from utils.logger_util import LoggerUtil


logger = LoggerUtil("ParserFactory")

class ParserFactory:
    """ Return a child object of ParserService depending on type parameter"""

    def create_parser(type: FieldParser) -> ParserService:
        if type == FieldParser.DATE:
            logger.info("Date parser selected")
            return ParseDate()
        elif type == FieldParser.NUMBERS:
            logger.info("Number parser selected")
            return ParseNumbers()
        elif type == FieldParser.CURRENCY:
            logger.info("Currency parser selected")
            return CurrencyParser()
        elif type == FieldParser.ABN:
            logger.info("ABN parser selected")
            return AbnParser()
        else:
            return None
