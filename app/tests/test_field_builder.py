import unittest

from form_analyser.field_builder import FieldBuilder, RawFieldValue
from form_analyser.enums.field_parser import FieldParser
from form_analyser.enums.field_validation import FieldValidation
from utils.base_utils import BaseUtils
from unittest.mock import patch
from utils.db_connection import DbConnection
from db.repo.api_response_stats_repository import ApiResponseStatsRepository


class TestFieldBuilder(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.instance_id = BaseUtils.get_a_unique_id()
        return super().setUp()

    def build_successful_validation_success(self, value, validator_name):
        return {
            'validations': [{
                'input': value,
                'message': None,
                'name': validator_name,
                'output': '',
                'parms': '',
                'status': 1
            }]
        }

    def build_str_field(self, value):
        with patch.object(ApiResponseStatsRepository, "__init__", **{"return_value": None}) as mock_init:
            return RawFieldValue(
                input=value,
                input_type='str',
                confidence='0.2',
            )()

    def test_build_1_field_no_validations(self):
        with patch.object(ApiResponseStatsRepository, "__init__", **{"return_value": None}) as mock_init,\
                patch.object(ApiResponseStatsRepository, "save_to_db") as save_to_db,\
                patch.object(DbConnection, "getDbUrl", **{"return_value": ''}) as getDbUrl:

            builder = FieldBuilder(self.instance_id)

            result = builder\
                .add_field('quantity', self.build_str_field('10'))\
                .build()

            print(result)

            self.assertDictEqual(
                result, {
                    'quantity': {'value': '10',
                                 'parsers': [],
                                 'validations': [],
                                 'raw_value': '10',
                                 'raw_value_type': 'str',
                                 'confidence': '0.2'}
                })

    def test_build_1_field_with_validations(self):

        with patch.object(ApiResponseStatsRepository, "__init__", **{"return_value": None}) as mock_init,\
                patch.object(ApiResponseStatsRepository, "save_to_db") as save_to_db,\
                patch.object(DbConnection, "getDbUrl", **{"return_value": ''}) as getDbUrl:

            builder = FieldBuilder(self.instance_id)

            result = builder\
                .add_field(
                    'quantity',
                    self.build_str_field('10'),
                    validations=[FieldValidation.REQUIRED]
                )\
                .build()

            # print(result)

            self.assertDictEqual(
                result, {
                    'quantity': {
                        'value': '10',
                        'parsers': [],
                        'confidence': '0.2',
                        'raw_value_type': 'str',
                        'raw_value': '10',
                        **self.build_successful_validation_success('10', 'RequiredValidation')
                        # Below is the expected output not using the helper above
                        # 'validations': [{
                        #     'input': '10',
                        #     'message': '',
                        #     'name': 'RequiredValidation',
                        #     'output': '',
                        #     'parms': '',
                        #     'status': 1
                        # }],
                    }
                })

    def test_build(self):

        with patch.object(ApiResponseStatsRepository, "__init__", **{"return_value": None}) as mock_init,\
                patch.object(ApiResponseStatsRepository, "save_to_db") as save_to_db,\
                patch.object(DbConnection, "getDbUrl", **{"return_value": ''}) as getDbUrl:

            builder = FieldBuilder(self.instance_id)
            # builder.add_field('date', '2022-05-20',
            #                   validations=[FieldValidation.REQUIRED], parser=FieldParser.DATE)

            result = builder\
                .add_field('quantity', self.build_str_field('10'))\
                .add_field('Insured Business', self.build_str_field('10'), validations=[FieldValidation.REQUIRED])\
                .add_field('ABN', self.build_str_field('111 000 222 223'), validations=[FieldValidation.REQUIRED])\
                .build()

            # print(result)

            self.assertDictEqual(
                result, {
                    'ABN': {
                        'confidence': '0.2',
                        'parsers': [],
                        'raw_value_type': 'str',
                        'raw_value': '111 000 222 223',
                        **self.build_successful_validation_success('111 000 222 223', 'RequiredValidation'),
                        'value': '111 000 222 223'
                    },
                    'Insured Business': {
                        'confidence': '0.2',
                        'parsers': [],
                        'raw_value_type': 'str',
                        'raw_value': '10',
                        **self.build_successful_validation_success('10', 'RequiredValidation'),
                        'value': '10'
                    },
                    'quantity': {
                        'confidence': '0.2',
                        'parsers': [],
                        'raw_value_type': 'str',
                        'raw_value': '10',
                        'validations': [],
                        'value': '10'
                    }
                }
            )

    def test_add_field_simple(self):

        with patch.object(ApiResponseStatsRepository, "__init__", **{"return_value": None}) as mock_init,\
                patch.object(ApiResponseStatsRepository, "save_to_db") as save_to_db,\
                patch.object(DbConnection, "getDbUrl", **{"return_value": ''}) as getDbUrl:

            builder = FieldBuilder(self.instance_id)

            result = builder\
                .add_field('quantity', self.build_str_field('10'))\
                .build()

            # {'quantity': {'value': '10', 'parsers': [], 'validations': [], 'raw_value_type': 'str', 'confidence': '0.2'}}

            self.assertEqual(
                result, {
                    'quantity': {
                        'value': '10',
                        'parsers': [],
                        'validations': [],
                        'raw_value': '10',
                        'raw_value_type': 'str',
                        'confidence': '0.2',
                    }
                }
            )

    def test_add_field_date_parsing(self):
        with patch.object(ApiResponseStatsRepository, "__init__", **{"return_value": None}) as mock_init,\
                patch.object(ApiResponseStatsRepository, "save_to_db") as save_to_db,\
                patch.object(DbConnection, "getDbUrl", **{"return_value": ''}) as getDbUrl:

            builder = FieldBuilder(self.instance_id)

            result = builder\
                .add_field(
                    'Date of issue',
                    self.build_str_field('2022-05-20'),
                    parser=[FieldParser.DATE]
                )\
                .build()

            # print(result)

            self.assertDictEqual(
                result, {
                    'Date of issue': {
                        'value': '2022-05-20 00:00:00',
                        'confidence': '0.2',
                        'value_type': 'datetime',
                        'raw_value_type': 'str',
                        'raw_value': '2022-05-20',
                        'parsers': [{'name': 'ParseDate', 'input': '2022-05-20',
                                    'output': '2022-05-20 00:00:00',
                                     'parms': '',
                                     'status': 1, 'message': 'Successfuly matched with format : YYYY-MM-DD'}],
                        'validations': [],
                    }
                }
            )

    def test_add_field_no_validation_or_parsing(self):
        with patch.object(ApiResponseStatsRepository, "__init__", **{"return_value": None}) as mock_init,\
                patch.object(ApiResponseStatsRepository, "save_to_db") as save_to_db,\
                patch.object(DbConnection, "getDbUrl", **{"return_value": ''}) as getDbUrl:

            builder = FieldBuilder(self.instance_id)

            result = builder\
                .add_field(
                    'Date of issue',
                    self.build_str_field('2022-05-20')
                )\
                .build()

            self.assertEqual(
                result, {
                    'Date of issue': {
                        'confidence': '0.2',
                        'validations': [],
                        'parsers': [],
                        'raw_value': '2022-05-20',
                        'value': '2022-05-20',
                        'raw_value_type': 'str'
                    }
                }
            )

    def test_add_field_required_validation(self):
        with patch.object(ApiResponseStatsRepository, "__init__", **{"return_value": None}) as mock_init,\
                patch.object(ApiResponseStatsRepository, "save_to_db") as save_to_db,\
                patch.object(DbConnection, "getDbUrl", **{"return_value": ''}) as getDbUrl:

            builder = FieldBuilder(self.instance_id)

            result = builder\
                .add_field(
                    'Date of issue',
                    self.build_str_field('2022-05-20'),
                    validations=[FieldValidation.REQUIRED],
                )\
                .build()

            # print(result)

            self.assertDictEqual(
                result, {
                    'Date of issue': {
                        'confidence': '0.2',
                        'parsers': [],
                        'value': '2022-05-20',
                        'raw_value': '2022-05-20',
                        'raw_value_type': 'str',
                        **self.build_successful_validation_success('2022-05-20', 'RequiredValidation'),
                    }
                }
            )

    def test_add_field_required_validation_no_value(self):

        with patch.object(ApiResponseStatsRepository, "__init__", **{"return_value": None}) as mock_init,\
                patch.object(ApiResponseStatsRepository, "save_to_db") as save_to_db,\
                patch.object(DbConnection, "getDbUrl", **{"return_value": ''}) as getDbUrl:

            builder = FieldBuilder(self.instance_id)

            result = builder\
                .add_field('Date of issue', self.build_str_field(''),
                           validations=[FieldValidation.REQUIRED],
                           )\
                .build()

            print(result)
    # {'Date of issue': {'value': None, 'parsers': [], 'validations': [{'name': 'RequiredValidation', 'input': None, 'parms': '', 'output': '', 'status': 0, 'message': 'Value Required'}]}}
            self.assertEqual(
                result, {
                    'Date of issue': {
                        'value': '',
                        'confidence': '0.2',
                        'parsers': [],
                        'raw_value': '',
                        # 'validation_status': 'FAIL',
                        'validations': [
                            {'name': 'RequiredValidation', 'input': '', 'parms': '', 'output': '',
                             'status': 0,
                             'message': 'Value Required'}
                        ],
                        'raw_value_type': 'str'
                    }
                }
            )
