import time

import azure.ai.formrecognizer
import azure.core.credentials

import config
from form_analyser.response_handler import ResponseHandler
from utils.logger_util import LoggerUtil
from db.entities import ApiRequest
from flask import abort


class FormRecognizerService:
    """Wrap the Azure Form recognizer service to make it usable."""

    logger = LoggerUtil("FormRecognizerService")

    def __init__(self) -> None:
        self.endpoint = config.get_azure_form_recognizer_endpoint()
        self.model_id = config.get_azure_form_recognizer_model_id()
        self.secret_key = config.get_azure_form_recognizer_secret_key()

        self.client = self._setup()

    def _setup(self):
        fr_cred = azure.core.credentials.AzureKeyCredential(self.secret_key)
        return azure.ai.formrecognizer.DocumentAnalysisClient(self.endpoint, fr_cred)

    def _setup_admin(self):
        fr_cred = azure.core.credentials.AzureKeyCredential(self.secret_key)
        return azure.ai.formrecognizer.DocumentModelAdministrationClient(self.endpoint, fr_cred)

    def analyze(self, apiRequest: ApiRequest) -> ResponseHandler:
        """Core request method."""

        start_time = time.time()
        analyze_document = None
        try:
            analyze_document = self.client.begin_analyze_document(
                self.model_id, apiRequest.file_bytes)
        except Exception as e:
            print(f"An error occurred during file parsing: {str(e)}")
            abort(400, 'The file is corrupted or format is unsupported!')

        self.logger.info('Blocking until analysis result comes back')
        analyze_document.wait(40)  # Wait for max 20 seconds

        if analyze_document.status() != 'succeeded':
            msg = f'Analysis timeout. status = {analyze_document.status()}'
            self.logger.error(msg)
            abort(408, msg)

        process_runtime = round(time.time() - start_time, 2)
        self.logger.info(
            f'Analysis succeeded. {analyze_document.status()} {analyze_document}')

        result = analyze_document.result().to_dict()

        return ResponseHandler(
            request=apiRequest,
            raw_response=result,
            process_runtime=process_runtime
        )
