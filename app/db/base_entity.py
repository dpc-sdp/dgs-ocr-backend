
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, VARCHAR

Base = declarative_base()


@dataclass
class BaseEntity(Base):
    """ This is the abastract layer of all the classes and all the comment fileds used in the tables"""
    __abstract__ = True

    id: int = Column(Integer, primary_key=True)
    request_id: str = Column(VARCHAR, unique=True)
    created_on: datetime = Column(DateTime, default=datetime.now)
