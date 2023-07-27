
from form_analyser.enums.field_validation import FieldValidation
from form_analyser.services.validator_service import FieldValidationService, RequiredValidation
from utils.logger_util import LoggerUtil


logger = LoggerUtil("FieldBuilder")

class ValidatorFactory:
    """ Return a child object of FieldValidationService depending on the type paramater"""

    def create_parser(type: FieldValidation) -> FieldValidationService:
        if type == FieldValidation.REQUIRED:
            logger.info("Required validation selected")
            return RequiredValidation()
        else:
            return None
