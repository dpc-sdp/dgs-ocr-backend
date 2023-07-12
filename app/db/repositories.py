from abc import ABC
from typing import TypeVar, Generic
from utils.logger_util import LoggerUtil
from utils.db_connection import DbConnection
from db.entities import ApiRequest, AnalysedData, ExpectedResults

T = TypeVar('T')


class AbstractRepository(Generic[T], ABC):

    def __init__(self, logger):
        self.logger = logger
        connection = DbConnection()
        self.session = connection.getConnection()

    def save_to_db(self, model: T) -> bool:
        self.logger.info(f'Creating data: {model}')
        self.session.add(model)
        self.session.commit()
        self.logger.info('Data saved successfully')
        return True

    def update(self, model: T) -> bool:
        self.logger.info(f'Updating data: {model}')
        self.session.commit()
        self.logger.info('Data updated successfully')
        return True

    def findByRequestId(self, request_id) -> T:
        return self.session.query(T).filter_by(request_id=request_id).first()


class ApiRequestRepository(AbstractRepository[ApiRequest]):

    logger = LoggerUtil("ApiRequestRepository")

    def __init__(self):
        super().__init__(self.logger)


class AnalysedDataRepository(AbstractRepository[AnalysedData]):

    logger = LoggerUtil("AnalysedDataRepository")

    def __init__(self):
        super().__init__(self.logger)


class ExpectedResultsRepository(AbstractRepository[ExpectedResults]):

    logger = LoggerUtil("ExpectedResultsRepository")

    def __init__(self):
        super().__init__(self.logger)
