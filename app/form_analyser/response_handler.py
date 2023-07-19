import json

from db.entities import ApiRequest, AnalysedData


class ResponseHandler:
    def __init__(self, request: ApiRequest, raw_response, process_runtime) -> None:
        self.request = request
        self.raw_response = raw_response
        self.process_runtime = process_runtime

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
