import json
import config

import azure.ai.formrecognizer
import azure.core.credentials
from utils.logger_util import LoggerUtil

log = LoggerUtil('Analyzer Gateway')

# The bit that talks to Form Recognizer


def analyse_document_and_wait_for_it(pdf_bytes: bytes) -> dict:
    fr_endpoint = config.get_azure_form_recognizer_endpoint()
    fr_model_id = config.get_azure_form_recognizer_model_id()

    print(f'Processing document using model: {fr_model_id}')

    fr_cred = azure.core.credentials.AzureKeyCredential(
        config.get_azure_form_recognizer_secret_key())
    fr_client = azure.ai.formrecognizer.DocumentAnalysisClient(
        fr_endpoint, fr_cred)

    # Where the magic happens?
    p = fr_client.begin_analyze_document(fr_model_id, pdf_bytes)
    print('Blocking until analysis result comes back')
    p.wait(20)  # Wait for max 20 seconds

    if not p.status() == 'succeeded':
        raise Exception(
            f'Analysis failed or took too long. status = {p.status()}. {p}')

    print(f'It worked. {p.status()} {p}')
    return p.result().to_dict()
