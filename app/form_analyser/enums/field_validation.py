from enum import Enum


class FieldValidation(Enum):
    REQUIRED = 'required'
    NOT_EMPTY = 'not_empty'
    GREATER_THAN_ZERO = 'greater_than_zero'
