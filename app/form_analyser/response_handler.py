import json

from utils import blobstorage
from db.entities import ApiRequest, AnalysedData


class ResponseHandler:
    def __init__(self, request: ApiRequest, raw_response, process_runtime) -> None:
        self.request = request
        self.raw_response = raw_response
        self.process_runtime = process_runtime

    def stash_document(self):
        file_stash_location = f'{self.request.request_id}/input.pdf'
        # pdf_bytes: bytes, stash_input_and_output: bool = False, request_id: str = "")
        blobstorage.push_blob(file_stash_location, self.request.file_bytes)

    def stash_result(self):
        response_stash_location = f'{self.request.request_id}/fr_analysis_result.json'
        blobstorage.push_blob(response_stash_location,
                              json.dumps(self.raw_response))

    def get_document(self):
        return self.raw_response.get('documents')

    def get_fields(self):
        doc = self.get_document()
        return doc[0] if doc else None

    def parse(self):
        """Parse Form Recognizer response."""
        return AnalysedData(request=self.request,
                            raw_response=self.raw_response,
                            process_runtime=self.process_runtime)
