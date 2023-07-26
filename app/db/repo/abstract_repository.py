from abc import ABC
from typing import TypeVar, Generic
from utils.db_connection import DbConnection

T = TypeVar('T')


class AbstractRepository(Generic[T], ABC):

    def __init__(self, logger):
        self.logger = logger
        connection = DbConnection()
        self.session = connection.getConnection()

    def save_to_db(self, model: T) -> bool:
        self.logger.debug(f'Creating data: {model}')
        self.session.add(model)
        self.session.commit()
        self.logger.info('Data saved successfully')
        return True

    def update(self, model: T) -> bool:
        self.logger.debug(f'Updating data: {model}')
        self.session.commit()
        self.logger.info('Data updated successfully')
        return True

    def findByRequestId(self, request_id) -> T:
        return self.session.query(T).filter_by(request_id=request_id).first()
