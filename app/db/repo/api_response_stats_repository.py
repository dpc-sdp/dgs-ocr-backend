from utils.logger_util import LoggerUtil
from db.api_response_stats import ApiResponseStats
from db.repo.abstract_repository import AbstractRepository


class ApiResponseStatsRepository(AbstractRepository[ApiResponseStats]):

    logger = LoggerUtil("ApiResponseStatsRepository")

    def __init__(self):
        super().__init__(self.logger)
