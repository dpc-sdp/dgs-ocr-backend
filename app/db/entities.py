import json
import config
import base64
import form_analyser.response_parsers as parsers

from flask import request, jsonify, abort
from datetime import datetime
from dataclasses import dataclass
from utils.base_utils import BaseUtils
from utils.model_stats import ModelStats
from form_analyser.enums.cover_types import CoverTypes
from sqlalchemy.ext.declarative import declarative_base
from form_analyser.response_validator import ResponseValidator
from sqlalchemy import Column, JSON, Enum as EnumType, VARCHAR
from form_analyser.enums.cover_types import CoverTypes
from db.base_entity import BaseEntity


@dataclass
class ApiRequest(BaseEntity):
    """ This class is used to store all the request realated data"""
    __tablename__ = 'api_requests'

    def __init__(self, request: request, idBase64: bool):
        self.request_id = BaseUtils.get_a_unique_id().strip()
        self.created_on = datetime.now()
        if request is not None:
            user_agent = request.headers.get('User-Agent')

            if user_agent is not None:
                self.agent = user_agent.split("/")[0]

            cover_type = None
            if idBase64:
                self.vaildateRequest(request, 'cover_type',
                                     'Cover type required!')
                cover_type = request.json['cover_type']
                print(f'{cover_type} cover type selected')
                self.vaildateRequest(request, 'file', 'File required!')
                try:
                    self.file_bytes = base64.b64decode(request.json['file'])
                except Exception as e:
                    print(f"An error occurred during file parsing: {str(e)}")
                    abort(400, 'Invalid file!')

                self.vaildateRequest(request, 'filename', 'Filename required!')
                self.file_name = request.json['filename']

                self.vaildateRequest(
                    request, 'content_length', 'Content Length required!')
                self.file_size = request.json['content_length']
            else:
                cover_type = request.form.get('cover_type', None)
                print(f'{cover_type} cover type selected')
                doc = request.files.get('doc')
                self.file_bytes = doc.read() if doc is not None else None
                self.file_name = doc.filename
                self.file_size = doc.content_length

            try:
                self.cover_type = CoverTypes(cover_type)
                print(f'{self.cover_type} cover type selected')
            except Exception as e:
                print(
                    f"An error occurred while parsing cover type: {str(e)}")
                abort(400, 'Invalid cover type!')

            self.preserve_artefacts = request.form.get(
                'stash_input_and_output', False)
            self.model_id = request.form.get('model_id', None)
            self.sample_result = request.form.get('sample_result')

            if self.model_id is None:
                self.model_id = config.get_azure_form_recognizer_model_id()

            self.model_id = self.model_id.strip()

    model_id: str = Column(VARCHAR)
    agent: str = Column(VARCHAR)
    file_name: str = Column(VARCHAR)
    cover_type: str = Column(EnumType(CoverTypes))
    file_size: str = Column(VARCHAR)
    preserve_artefacts: str = Column(VARCHAR)
    sample_result: str = Column(VARCHAR)
    file_stash_location: str = Column(VARCHAR)
    response_stash_location: str = Column(VARCHAR)

    def vaildateRequest(self, request, key, msg):
        if key not in request.json:
            abort(400, msg)


@dataclass
class AnalysedData(BaseEntity):
    """ This class is used to store all the Analisis data """
    __tablename__ = 'api_response'

    def __init__(self, request: ApiRequest, raw_response, process_runtime):
        self.request_id = request.request_id
        self.created_on = datetime.now()
        self.model_id = request.model_id
        self.custom_model_analysis = parsers.analyse_custom_model_for_parsing(
            raw_response)
        self.expected_fields = ResponseValidator(
            self.custom_model_analysis, request.cover_type).build_response(request.request_id)
        # self.extraction_stats = ModelStats().analyse_stats(raw_response, process_runtime)
        self.raw_from_formrecognizer = raw_response

    def __call__(self) -> dict:
        return {
            "request_id": self.request_id,
            "created_on": self.created_on,
            "model_id": self.model_id,
            "expected_fields": self.expected_fields,
            # "extraction_stats": self.extraction_stats,
            "raw_from_formrecognizer": self.raw_from_formrecognizer
        }

    def get_json(self):
        return jsonify(self())

    model_id: str = Column(VARCHAR)
    expected_fields = Column(JSON)
    extraction_stats = Column(JSON)
    custom_model_analysis = Column(JSON)
    raw_from_formrecognizer = Column(JSON)


@ dataclass
class ExpectedResults(BaseEntity):
    """ This class is used to store all the Analisis data """
    __tablename__ = 'expected_results'

    def __init__(self, agent, file_name, row):
        self.request_id = BaseUtils.get_a_unique_id().strip()
        self.created_on = datetime.now()
        self.agent = agent
        self.file_name = file_name
        self.doc_name = self.replaceNanToNone(str(row[0]))
        self.insurer_name = self.replaceNanToNone(str(row[1]))
        self.insurer_names = self.replaceNanToNone(str(row[2]))
        self.insurer_abn = self.replaceNanToNone(str(row[3]))
        self.document_issue_date = self.replaceNanToNone(str(row[4]))
        self.policy_no = self.replaceNanToNone(str(row[5]))
        self.professional = self.replaceNanToNone(str(row[6]))
        self.public = self.replaceNanToNone(str(row[7]))
        self.product = self.replaceNanToNone(str(row[8]))
        self.policy_start_date = self.replaceNanToNone(str(row[10]))
        self.policy_end_date = self.replaceNanToNone(str(row[11]))
        self.policy_currency = self.replaceNanToNone(str(row[12]))
        self.professional_liability_amount = self.replaceNanToNone(
            str(row[13]))
        self.professional_aggregate = self.replaceNanToNone(str(row[14]))
        self.public_liability_amount = self.replaceNanToNone(str(row[15]))
        self.product_liability_amount = self.replaceNanToNone(str(row[16]))
        self.product_aggregate = self.replaceNanToNone(str(row[17]))
        self.region = self.replaceNanToNone(str(row[18]))

    def replaceNanToNone(self, val):
        if val is not None:
            if val.strip() == 'nan':
                return None
        return val.strip()

    agent: str = Column(VARCHAR)
    file_name: str = Column(VARCHAR)
    doc_name: str = Column(VARCHAR)
    insurer_name: str = Column(VARCHAR)
    insurer_names: str = Column(VARCHAR)
    insurer_abn: str = Column(VARCHAR)
    document_issue_date: str = Column(VARCHAR)
    policy_no: str = Column(VARCHAR)
    professional: str = Column(VARCHAR)
    public: str = Column(VARCHAR)
    product: str = Column(VARCHAR)
    policy_start_date: str = Column(VARCHAR)
    policy_end_date: str = Column(VARCHAR)
    policy_currency: str = Column(VARCHAR)
    professional_liability_amount: str = Column(VARCHAR)
    professional_aggregate: str = Column(VARCHAR)
    public_liability_amount: str = Column(VARCHAR)
    product_liability_amount: str = Column(VARCHAR)
    product_aggregate: str = Column(VARCHAR)
    region: str = Column(VARCHAR)
