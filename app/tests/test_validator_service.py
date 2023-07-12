from unittest import TestCase

from form_analyser.services.validator_service import FieldValidationService, RequiredValidation, MaxLengthValidation
from form_analyser.services.response_dto import ValidationDto


class MockFieldValidationService(FieldValidationService):
    def is_valid(self, value) -> ValidationDto:
        # return ValidationResponseDto(True, None)
        return ValidationDto(
            name='test_name',
            input='test_value',
            parms="paramsx",
            output="outputx",
            status="1",
            message="test message"
        )


class TestValidatorService(TestCase):

    def setUp(self) -> None:
        self.validator = RequiredValidation()
        return super().setUp()
    def test_is_valid(self):
        mock_service = MockFieldValidationService()

        response = mock_service.is_valid('value')
        # print(vars(response))

        self.assertIsInstance(response, ValidationDto)
        self.assertEqual(response.name, 'test_name')
        self.assertEqual(response.input, 'test_value')
        self.assertEqual(response.parms, 'paramsx')
        self.assertEqual(response.output, 'outputx')
        self.assertEqual(response.status, '1')
        self.assertEqual(response.message, 'test message')

    def test_valid_string(self):
        # Arrange
        value = "Hello, world!"

        # Act
        response = self.validator.is_valid(value)

        # Assert
        self.assertEqual(response.status, 1)
        self.assertEqual(response.message, None)

    def test_empty_string(self):
        # Arrange
        value = ""

        # Act
        response = self.validator.is_valid(value)

        # Assert
        self.assertEqual(response.status, 0)
        self.assertEqual(response.message, "Value Required")

    def test_none_value(self):
        # Arrange
        value = None

        # Act
        response = self.validator.is_valid(value)

        # Assert
        self.assertEqual(response.status, 0)
        self.assertEqual(response.message, "Value Required")

    def test_valid_number(self):
        # Arrange
        value = 42

        # Act
        response = self.validator.is_valid(value)

        # Assert
        self.assertEqual(response.status, 1)
        self.assertEqual(response.message, None)

    def test_valid_bool(self):
        # Arrange
        value = True

        # Act
        response = self.validator.is_valid(value)

        # Assert
        self.assertEqual(response.status, 1)
        self.assertEqual(response.message, None)

    def test_valid_list(self):
        # Arrange
        value = [1, 2, 3]

        # Act
        response = self.validator.is_valid(value)

        # Assert
        self.assertEqual(response.status, 0)
        self.assertEqual(response.message,
                         'Value must be of type str, float or int')

    def test_name_property(self):
        # Arrange
        validator = RequiredValidation()

        # Act
        name = validator.name

        # Assert
        self.assertEqual(name, "RequiredValidation")

    def test_valid_value(self):
        max_length = 10
        validation = MaxLengthValidation(max_length)
        value = 'validvalue'
        response = validation.is_valid(value)
        self.assertEqual(response.status, 1)
        self.assertEqual(response.message, None)

    def test_invalid_value(self):
        max_length = 10
        validation = MaxLengthValidation(max_length)
        value = 'this value is too long'
        response = validation.is_valid(value)
        self.assertEqual(response.status, 0)
        self.assertEqual(response.message, 'Invalid character length of 22')
