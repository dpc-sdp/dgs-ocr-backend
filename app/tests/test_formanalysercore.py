#!/usr/bin/env python3

import json
import unittest
import logging

from form_analyser import formanalysercore

class TestFixture:
    def __init__(self) -> None:
        self.sample_result = self.load_json_file()

    def load_json_file(self, path: str = 'tests/artefacts/sample_result.json'):
        with open(path) as f:
            return json.load(f)

class SomeTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_fixture = TestFixture()

    @unittest.skip("needed to be fixed")
    def test_dummy_test(self):
        x = formanalysercore.analyse(self.test_fixture.sample_result)
        self.assertEqual(x['who_da_best'], 'Servian da best')

    @unittest.skip('')
    def test_parse_with_json_path(self):
        self.test_fixture = TestFixture()
        json_path = "ssdf"

        x = formanalysercore.analyse_json_path(self.test_fixture.sample_result, json_path)
        print(x)
        self.assertEqual(x["Policy Number:"], '93392294')

    def test_parse_with_table_parser(self):
        self.test_fixture = TestFixture()

        table = formanalysercore.analyse_table(self.test_fixture.sample_result)
        logging.info(table)
        
        self.assertEqual(table["Insured:"], 'Servian Pty Ltd')
        self.assertEqual(table["Policy Number:"], '93392294')
        self.assertEqual(table["Policy Type:"], 'Information Technology Liability')
        self.assertEqual(table["Policy Period:"], 'From: 31/03/2019 To: 31/03/2020')
