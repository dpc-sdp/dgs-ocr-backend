import unittest
from form_analyser.services.validator_service import MaxLengthValidation, ValidationDto
from form_analyser.enums.action_status import ActionStatus


class TestMaxLengthValidation(unittest.TestCase):

    def test_valid_value(self):
        max_length_validation = MaxLengthValidation(max_length=5)
        validation_result = max_length_validation.is_valid("Test1")
        expected_result = ValidationDto(
            name="MaxLengthValidation",
            input="Test1",
            parms="",
            output="",
            status=ActionStatus.SUCCESS.value,
            message=None
        )
        self.assertEqual(expected_result, validation_result)

    def test_invalid_value(self):
        max_length_validation = MaxLengthValidation(max_length=5)
        validation_result = max_length_validation.is_valid("Test 1")
        expected_result = ValidationDto(
            name="MaxLengthValidation",
            input="Test 1",
            parms="",
            output="",
            status=ActionStatus.FAILED.value,
            message="Invalid character length of 6"
        )
        self.assertEqual(expected_result, validation_result)
