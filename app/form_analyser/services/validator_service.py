from abc import ABC, abstractmethod
from form_analyser.services.response_dto import ValidationDto
from form_analyser.enums.action_status import ActionStatus


class FieldValidationService(ABC):
    """ Abstract FieldValidationService class"""

    @abstractmethod
    def is_valid(self, value) -> ValidationDto:
        pass


class RequiredValidation(FieldValidationService):
    def is_valid(self, value) -> ValidationDto:
        status = None
        message = None

        if isinstance(value, str):
            value_strip = value.strip()
            if value_strip is not None and len(value_strip) > 0:
                status = ActionStatus.SUCCESS.value
            else:
                status = ActionStatus.FAILED.value
                message = 'Value Required'
        elif isinstance(value, float) or isinstance(value, int):
            status = ActionStatus.SUCCESS.value
        elif value is None:
            status = ActionStatus.FAILED.value
            message = 'Value Required'
        elif not isinstance(value, str) or isinstance(value, float) or isinstance(value, int):
            status = ActionStatus.FAILED.value
            message = 'Value must be of type str, float or int'
        else:
            status = ActionStatus.SUCCESS.value

        return ValidationDto(
            name=self.name,
            input=value,
            parms="",
            output="",
            status=status,
            message=message
        )

    @property
    def name(self):
        return 'RequiredValidation'

class MaxLengthValidation(FieldValidationService):
    def __init__(self, max_length):
        self.max_length = max_length

    def is_valid(self, value) -> ValidationDto:
        message = None
        status = None

        if len(value) <= self.max_length:
            status = ActionStatus.SUCCESS.value
        else:
            status = ActionStatus.FAILED.value
            message = f'Invalid character length of {len(value)}'

        return ValidationDto(
            name=self.name,
            input=value,
            parms="",
            output="",
            status=status,
            message=message
        )

    @property
    def name(self):
        return 'MaxLengthValidation'
