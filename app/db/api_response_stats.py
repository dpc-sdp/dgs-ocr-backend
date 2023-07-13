

from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import Column, VARCHAR
from db.base_entity import BaseEntity


@dataclass
class ApiResponseStats(BaseEntity):
    """ This class is used to store all the Analisis data """
    __tablename__ = 'api_response_stats'

    def __init__(self, request_id, field_name, item):
        self.request_id = request_id
        self.created_on = datetime.now()
        self.field_name = field_name
        self.f_value = item["value"]
        self.confidence = item["confidence"]
        self.is_value_blank = self.is_none_or_empty(item["raw_value"])
        self.is_failed_to_parse = self.is_none_or_empty(item["value"])

    def is_none_or_empty(self, value):
        return value is None or value == ''

    field_name: str = Column(VARCHAR)
    confidence: str = Column(VARCHAR)
    f_value: str = Column(VARCHAR)
    is_value_blank: str = Column(VARCHAR)
    is_failed_to_parse: str = Column(VARCHAR)
    servicenow_feedback: str = Column(VARCHAR)
