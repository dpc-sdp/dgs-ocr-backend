from enum import Enum
from utils import date_parser_util

from form_analyser.field_builder import FieldBuilder
from form_analyser.enums.field_validation import FieldValidation
from form_analyser.enums.field_parser import FieldParser


class ValidatorBase:
    def __init__(self, value) -> None:
        self.value = value

    def clean(self):
        raise NotImplementedError()


class DateValidator(ValidatorBase):
    def __str__(self) -> str:
        return 'DateValidator'

    def clean(self):
        return date_parser_util.extract_date(self.value)


class ResponseValidator:
    def __init__(self, fields: dict) -> None:
        self.fields: dict = fields

    def _get(self, field_name, default_value=None):
        return self.fields.get(field_name, default_value)

    def _validate(self, validator, field_name, default_value=None):
        field = self._get(field_name, default_value)

        return validator(field).clean()

    def build_response(self):

        builder = FieldBuilder()\
            .add_field('Insured Business', self._get('Insured Business'),
                       validations=[FieldValidation.REQUIRED])\
            .add_field('ABN', self._get('ABN'),
                       validations=[FieldValidation.REQUIRED])\
            .add_field('Date of issue', self._get('issue date'),
                       validations=[FieldValidation.REQUIRED],
                       parser=[FieldParser.DATE])\
            .add_field('Geographical Limit', self._get('Geographical Limit'),
                       validations=[FieldValidation.REQUIRED])\
            .add_field('Amount Limit', self._get('amount limit'),
                       validations=[FieldValidation.REQUIRED])\
            .add_field('Insurer Name', self._get('insurer name'),
                       validations=[FieldValidation.REQUIRED])\
            .add_field('Policy Number', self._get('policy number'),
                       validations=[FieldValidation.REQUIRED])\
            .add_field('Policy Period From', self._get('policy period from'),
                       validations=[FieldValidation.REQUIRED],
                       parser=[FieldParser.DATE])\
            .add_field('Policy Period To', self._get('policy period to'),
                       validations=[FieldValidation.REQUIRED],
                       parser=[FieldParser.DATE])\
            .add_field('policy type', self._get('policy type'),
                       validations=[FieldValidation.REQUIRED])\

        response = builder.build()

        return response

# expected_field_output = {
#     "fields":{
#         "ABN": {
#                 "value": "17 000 434 720",
#                 "value_type": "string",
#                 # "validation": 'Validators.DATE',
#                 "validators": [
#                     {"name":"", "parms":"", "input":"", "status":"", "message":""}
#                 ],
#                 "parser": [
#                     {"name":"", "parms":"", "input":"", "status":"", "message":""}
#                 ],
#                 "confidence":"",
#                 "raw_input":"",
#                 # {
#                 #     "type": "string_val",
#                 #     "params": "8 digits"
#                 # }
#             }
#         },
#     "status": ""
# }
#
# Field
# Type
# Validation on API
# Insured Business
# Text
# max length, valid characters
# Policy Type (e.g. Professional indemnity)
# Text
# From defined list, value might drive rest of structure
# ABN of company insured
# Text (11 digits)
# Optional
# text format (11 digits) with no leading 0
# validate with ABR checksum ?
# Insurer Name
# Text
# max length, valid characters
# Policy Number
# Text
# max length, valid characters
# Date of issue
# Date (dd/mm/yyyy)
# valid date
# Start Validity
# Datetime (UTC?)
# valid date time
# End Validity
# Datetime (UTC?)
# valid date time, greater than start validity
# Amount Limit
# Number
# valid number, associated with $ or AUD
# Geographical Limit
# Text
# max length, valid characters
