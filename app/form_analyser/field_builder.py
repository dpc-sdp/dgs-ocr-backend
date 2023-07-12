from dataclasses import dataclass
from typing import Any

from form_analyser.services.parser_factory import ParserFactory
from form_analyser.services.parser_service import ParserService
from form_analyser.services.validator_factory import ValidatorFactory
from form_analyser.services.validator_service import FieldValidationService
from form_analyser.services.response_dto import ValidationDto
from form_analyser.enums.action_status import ActionStatus


@dataclass
class RawFieldValue:
    input: str
    input_type: str
    confidence: str

    def __call__(self) -> dict:
        return {
            'value': self.input,
            'raw_value': self.input,
            'raw_value_type': self.input_type,
            'confidence': self.confidence,
        }

# @dataclass
# class ResponseField:
#     field_name: str
#     confidence: str
#     # parsers: ParserService

#     @property
#     def field_name(self):
#         return self.field_name


class FieldBuilder:
    def __init__(self):
        self.fields = {}
        self.parsers = {}
        self.validations = {}

    def add_field(self, field_name, raw_field: RawFieldValue, validations=None, parser=None):
        if raw_field is not None:
            self.fields[field_name] = raw_field
        else:
            self.fields[field_name] = None
        self.validations[field_name] = validations
        self.parsers[field_name] = parser

        return self

    def build(self):
        result = {}

        for key, obj in self.fields.items():
            item = {
                "value": None,
                "parsers": [],
                "validations": []
            }
            if obj is not None:
                item.update(obj)
            parsers = self.parsers[key]
            value = item["value"]

            if parsers is not None:
                for parser in parsers:
                    p: ParserService = ParserFactory.create_parser(type=parser)
                    if p:
                        if value is not None:
                            print(value)
                            res: ValidationDto = p.parse(value)
                            item["value"] = res.output
                            item["value_type"] = p.value_type
                            item["parsers"].append(vars(res))
                        else:
                            res: ValidationDto = ValidationDto(
                                name=str(p),
                                input=value,
                                parms="",
                                output="",
                                status=ActionStatus.FAILED.value,
                                message="Invalid value: cannot parse null")
                            item["parsers"].append(vars(res))

            validations = self.validations[key]

            if validations is not None:
                for validation in validations:
                    valid: FieldValidationService = ValidatorFactory.create_parser(
                        type=validation)
                    if valid is not None:
                        res = valid.is_valid(item["value"])
                        item["validations"].append(vars(res))

            result[key] = item

        return result
