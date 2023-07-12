import unittest

from form_analyser.services.validator_service import RequiredValidation, ValidationDto
from form_analyser.enums.action_status import ActionStatus


class TestRequiredValidation(unittest.TestCase):

    def get_expected_success_output(self, value):
        return ValidationDto(
            name='RequiredValidation',
            input=value,
            parms="",
            output="",
            status=ActionStatus.SUCCESS.value,
            message=None
        )

    def get_expected_failed_output(self, value, message):
        return ValidationDto(
            name='RequiredValidation',
            input=value,
            parms="",
            output="",
            status=ActionStatus.FAILED.value,
            message=message
        )

    def test_is_valid_string_success(self):
        validator = RequiredValidation()
        value = "Test Value"
        expected_output = self.get_expected_success_output(value)

        result = validator.is_valid(value)

        self.assertEqual(result, expected_output)

    def test_is_valid_string_fail(self):
        validator = RequiredValidation()
        value = "   "
        expected_output = self.get_expected_failed_output(
            value=value, message="Value Required")

        result = validator.is_valid(value)

        self.assertEqual(result, expected_output)

    def test_is_valid_number_success(self):
        validator = RequiredValidation()
        value = 123
        expected_output = self.get_expected_success_output(value)

        result = validator.is_valid(value)

        self.assertEqual(result, expected_output)

    def test_is_valid_number_fail(self):
        validator = RequiredValidation()
        value = None
        expected_output = self.get_expected_failed_output(
            value=value, message="Value Required")

        result = validator.is_valid(value)

        self.assertEqual(result, expected_output)

    def test_is_valid_other_type_fail(self):
        validator = RequiredValidation()
        value = []
        expected_output = self.get_expected_failed_output(
            value=value, message="Value must be of type str, float or int")

        result = validator.is_valid(value)

        self.assertEqual(result, expected_output)
