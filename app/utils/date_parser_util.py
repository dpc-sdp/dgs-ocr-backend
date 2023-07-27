import json
import arrow
from form_analyser.services.response_dto import ValidationDto
from form_analyser.enums.action_status import ActionStatus
from utils.logger_util import LoggerUtil

with open("./conf/datetime_config.json") as f:
    config = json.load(f)

date_formats = config["date_formats"]

logger = LoggerUtil("Date Util")


def extract_date(obj: ValidationDto) -> ValidationDto:
    for fmt in date_formats:
        try:
            dt = arrow.get(obj.input, fmt)
            dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
            obj.output = dt.format("YYYY-MM-DD HH:mm:ss")
            obj.status = ActionStatus.SUCCESS.value
            obj.message = f'Successfuly matched with format : {fmt}'
            logger.info(obj.message)
            return obj
        except (ValueError, TypeError, arrow.parser.ParserError):
            continue

    obj.output = None
    obj.status = ActionStatus.FAILED.value
    obj.message = f'Failed match date {obj.input} with existing formats'
    logger.info(obj.message)
    return obj
