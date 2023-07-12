import unittest

from dateutil.tz import tzutc
from datetime import datetime

from utils.date_parser_util import extract_date
from form_analyser.services.response_dto import ValidationDto
from form_analyser.enums.action_status import ActionStatus
from dataclasses import asdict


class TestExtractDateTime(unittest.TestCase):

    def test_extract_datetime(self):

        test_cases = [
            ("1 July 2017", '2017-07-01 00:00:00', "D MMMM YYYY"),
            ("1 July 2017 08:12 AM", '2017-07-01 00:00:00', "D MMMM YYYY h:mm A"),
            ("1 July 2017 15:12", '2017-07-01 00:00:00', "D MMMM YYYY H:mm"),
            ("1/12/2022", '2022-12-01 00:00:00', "D/MM/YYYY"),
            ("1/12/2022 08:12 AM", '2022-12-01 00:00:00', "D/MM/YYYY h:mm A"),
            ("1/12/2022 15:12", '2022-12-01 00:00:00', "D/MM/YYYY H:mm"),
            ("1-12-2022", '2022-12-01 00:00:00', "D-MM-YYYY"),
            ("1-12-2022 08:12 AM", '2022-12-01 00:00:00', "D-MM-YYYY h:mm A"),
            ("1-12-2022 15:12", '2022-12-01 00:00:00', "D-MM-YYYY H:mm"),
            ("19 September, 2022", '2022-09-19 00:00:00', "DD MMMM, YYYY"),
            # ("MMMMMM March 31, 2022", '2022-03-31 00:00:00', "DD MMMM, YYYY"),
            ("19 Sep 2022", '2022-09-19 00:00:00', "DD MMM YYYY"),
            ("Sep 19, 2022", '2022-09-19 00:00:00', "MMM DD, YYYY"),
            ("September 19, 2022", '2022-09-19 00:00:00', "MMMM DD, YYYY"),
            ("July 1, 2022", '2022-07-01 00:00:00', "MMMM D, YYYY"),
            ("1/1/2023", '2023-01-01 00:00:00', "D/M/YYYY"),
            ("11/17/2021", '2021-11-17 00:00:00', "MM/DD/YYYY"),
            ("11/1/2021", '2021-01-11 00:00:00', "DD/M/YYYY"),
            ("11/1/2021 11/1/2021", '2021-01-11 00:00:00', "DD/M/YYYY")
        ]

        for date_string, expected, fmt in test_cases:
            with self.subTest(date_string=date_string):
                inputObj = ValidationDto(
                    name="DateValidation",
                    input=date_string,
                    parms="",
                    output="",
                    status="",
                    message=""
                )
                result = extract_date(inputObj)

                expectedObj = ValidationDto(
                    name="DateValidation",
                    input=date_string,
                    parms="",
                    output=expected,
                    status=ActionStatus.SUCCESS.value,
                    message=f'Successfuly matched with format : {fmt}'
                )

                self.assertEqual(asdict(result), asdict(expectedObj))
