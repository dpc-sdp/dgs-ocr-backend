import re
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
    obj.input = remove_text_ignore_case(obj.input, "at ")
    for fmt in date_formats:
        try:
            dt = arrow.get(obj.input, fmt)
            obj.output = dt.format("YYYY-MM-DD HH:mm")
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


def remove_text_ignore_case(sentence, text_to_remove):
    # Create a regular expression pattern with the 're.IGNORECASE' flag to ignore case
    pattern = re.compile(re.escape(text_to_remove), re.IGNORECASE)

    # Use the 'sub' function to replace occurrences of the text_to_remove with an empty string
    result_sentence = pattern.sub('', sentence)

    return result_sentence
