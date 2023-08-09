import time

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer.aio import DocumentAnalysisClient

import config
from form_analyser.response_handler import ResponseHandler
from utils.logger_util import LoggerUtil
from db.entities import ApiRequest
from utils.base_utils import BaseUtils
from flask import abort


class FormRecognizerService:
    """Wrap the Azure Form recognizer service to make it usable."""

    logger = LoggerUtil("FormRecognizerService")

    def __init__(self) -> None:
        self.model_id = config.get_azure_form_recognizer_model_id()

    async def async_analyze(self, model_id, document):
        document_analysis_client = DocumentAnalysisClient(
            endpoint=config.get_azure_form_recognizer_endpoint(),
            credential=AzureKeyCredential(
                config.get_azure_form_recognizer_secret_key())
        )
        async with document_analysis_client as client:
            poller = await client.begin_analyze_document(
                model_id=model_id, document=document
            )
            return await poller.result()

    async def analyze(self, apiRequest: ApiRequest) -> ResponseHandler:
        """Core request method."""

        start_time = time.time()
        self.logger.info(
            f"Initiated cognitive analyze for id:{apiRequest.request_id} on: {BaseUtils.get_datefromtime(start_time)}")
        analyze_document = None
        try:
            analyze_document = await self.async_analyze(
                self.model_id, apiRequest.file_bytes)
        except Exception as e:
            print(f"An error occurred during file parsing: {str(e)}")
            abort(400, 'The file is corrupted or format is unsupported!')

        end_time = time.time()
        process_runtime = round(end_time - start_time, 2)
        self.logger.info(
            f"Completed cognitive analyze for id:{apiRequest.request_id} on: {BaseUtils.get_datefromtime(end_time)} in: {round(process_runtime, 2)} seconds")

        result = analyze_document.to_dict()

        return ResponseHandler(
            request=apiRequest,
            raw_response=result,
            process_runtime=process_runtime
        )
