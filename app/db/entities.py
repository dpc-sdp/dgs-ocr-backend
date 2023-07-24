import json
import config
import base64
import form_analyser.response_parsers as parsers

from flask import request, jsonify, abort
from datetime import datetime
from dataclasses import dataclass
from utils.base_utils import BaseUtils
from form_analyser.enums.cover_types import CoverTypes
from sqlalchemy.ext.declarative import declarative_base
from form_analyser.response_validator import ResponseValidator
from sqlalchemy import Column, JSON, Integer, DateTime, Enum as EnumType, VARCHAR
from form_analyser.enums.cover_types import CoverTypes
from conf.extensions import db


@dataclass
class ApiRequest(db.Model):
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

    id: int = Column(Integer, primary_key=True)
    request_id: str = Column(VARCHAR, unique=True)
    created_on: datetime = Column(DateTime, default=datetime.now)
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
class AnalysedData(db.Model):
    """ This class is used to store all the Analisis data """
    __tablename__ = 'api_response'

    def __init__(self, request: ApiRequest, raw_response, process_runtime):
        self.request_id = request.request_id
        self.cover_type = request.cover_type
        self.created_on = datetime.now()
        self.model_id = request.model_id
        self.custom_model_analysis = parsers.analyse_custom_model_for_parsing(
            raw_response)
        self.expected_fields = ResponseValidator(
            self.custom_model_analysis, request.cover_type).build_response(request.request_id)
        self.raw_from_formrecognizer = raw_response

    def __call__(self) -> dict:
        return {
            "request_id": self.request_id,
            "created_on": self.created_on,
            "model_id": self.model_id,
            "expected_fields": self.expected_fields
            # "raw_from_formrecognizer": self.raw_from_formrecognizer
        }

    def get_json(self):
        return jsonify(self())

    id: int = Column(Integer, primary_key=True)
    request_id: str = Column(VARCHAR, unique=True)
    created_on: datetime = Column(DateTime, default=datetime.now)
    model_id: str = Column(VARCHAR)
    cover_type: str = Column(EnumType(CoverTypes))
    expected_fields = Column(JSON)
    extraction_stats = Column(JSON)
    custom_model_analysis = Column(JSON)
    raw_from_formrecognizer = Column(JSON)
