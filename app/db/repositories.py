from utils.logger_util import LoggerUtil
from db.entities import ApiRequest, AnalysedData
from db.repo.abstract_repository import AbstractRepository


class ApiRequestRepository(AbstractRepository[ApiRequest]):

    logger = LoggerUtil("ApiRequestRepository")

    def __init__(self):
        super().__init__(self.logger)


class AnalysedDataRepository(AbstractRepository[AnalysedData]):

    logger = LoggerUtil("AnalysedDataRepository")

    def __init__(self):
        super().__init__(self.logger)
