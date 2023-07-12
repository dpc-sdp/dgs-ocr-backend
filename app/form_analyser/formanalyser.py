#!/usr/bin/env python3
import json
import time

import form_analyser.formanalysercore as formanalysercore
import form_analyser.formrecognizer_gateway as fr_gateway
import utils.blobstorage as blobstorage
from utils.logger_util import LoggerUtil


log = LoggerUtil('Main Analyser')


def analyse_document(pdf_bytes: bytes, stash_input_and_output: bool = False, request_id: str = ""):
    if stash_input_and_output:
        # Push to blob storage
        blobstorage.push_blob(f'{request_id}/input.pdf', pdf_bytes)
        log.info("PDF pushed in to the blob")
    # Send to Form Recognizer, get back a dict
    start_time = time.time()
    fr_analysis_result = fr_gateway.analyse_document_and_wait_for_it(pdf_bytes)
    process_runtime = round(time.time() - start_time, 2)
    log.info("Analysis complted on the form analyzer results")

    if stash_input_and_output:
        # Stash result
        blobstorage.push_blob(
            f'{request_id}/fr_analysis_result.json', json.dumps(fr_analysis_result))
        log.info("Form analyzer results pushed in to the blob")

    # Perform our analysis
    our_analysis_result = formanalysercore.analyse(
        fr_analysis_result, process_runtime)
    log.info("Analysis complted on the form analyzer results")
    return our_analysis_result
