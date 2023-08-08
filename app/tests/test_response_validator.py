import unittest
import json
import jsonschema
from utils.logger_util import LoggerUtil

from form_analyser.response_handler import ResponseHandler
from db.entities import ApiRequest
from form_analyser.enums.cover_types import CoverTypes

log = LoggerUtil('Integration Test (Resposnse Validator):')


class TestResponseValidator(unittest.TestCase):

    def setUp(self) -> None:
        self.maxDiff = None

        # Load the form analyzer output stored locally
        with open('tests/artefacts/sample_result_aon_coc_main_roads_wa.json') as f:
            self.sample_raw = json.load(f)

        # Call for resposne handler to process the form recogniser output and convert to consumable format
        request = ApiRequest(None, "apiname", False, False)
        request.cover_type = CoverTypes.PROFESSIONAL
        responseHandler = ResponseHandler(
            request=request, raw_response=self.sample_raw, process_runtime=".23")
        self.sample_output = responseHandler.parse()()

        log.info("Setup Completed")
        return super().setUp()

    def test_response_items_returned(self):
        self.assertIsNotNone(self.sample_output.get('expected_fields'))
        # self.assertIsNotNone(self.sample_output.get('custom_model_analysis'))
        # self.assertIsNotNone(self.sample_output.get('extraction_stats'))
        # self.assertIsNotNone(self.sample_output.get('raw_from_formrecognizer'))

    def test_schema_expected_fields(self):
        log.info("Testing JSON Schema")
        # TODO: Need to change the expected_output_schema.json file to reflect all the attributes
        with open('tests/artefacts/expected_output_schema.json') as f:
            expected_output_schema = json.load(f)

        # Extract the output of existing logic
        result_dict = self.sample_output["expected_fields"]

        res = jsonschema.validate(result_dict, expected_output_schema)

        print(res)

        # Validate the sample output against the schema
        try:
            jsonschema.validate(result_dict, expected_output_schema)
            log.info("Schema validation succeeded.")
        except jsonschema.ValidationError as e:
            log.error(f"Schema validation failed. Error: {str(e)}")
            raise e
        self.assertIsNone(res)

    def test_actual_output_api_output(self):
        log.info("Testing API output")
        # Load the schema for expeected output
        # TODO: Need to change the expected_api_output.json file to reflect all the attributes

        with open('tests/artefacts/expected_api_output.json') as f:
            expected_api_output = json.load(f)

        # Extract the output of existing logic
        result_dict = self.sample_output["expected_fields"]

        # print(result_dict)

        # Compare the sample output with the API output
        self.assertDictEqual(result_dict, expected_api_output)
