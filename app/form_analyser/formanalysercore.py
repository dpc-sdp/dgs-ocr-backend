#!/usr/bin/env python3

import copy
from jsonpath2.path import Path
from utils.model_stats import ModelStats


def analyse(fr_analysis: dict, process_runtime):
    # Ideally pull out some ABN's or something based on a config file... for now just send back
    # Form Recognizer's analysis, but with random flourishes
    our_analysis = {}
    our_analysis['custom_model_analysis'] = analyse_custom_model(fr_analysis)
    our_analysis['custom_model_stats'] = ModelStats(
    ).analyse_custom_model_for_stats(fr_analysis, process_runtime)
    our_analysis['table_analysis'] = analyse_table(fr_analysis)
    our_analysis['raw_from_formrecognizer'] = copy.deepcopy(fr_analysis)

    return our_analysis


def analyse_json_path(fr_analysis: dict, json_path):
    "using jsonpath package, locate the field of interest"
    return Path(fr_analysis, json_path)


def analyse_table(fr_analysis: dict) -> dict:
    if fr_analysis.get('tables') is None or len(fr_analysis.get('tables')) == 0:
        return {}

    table_raw = fr_analysis['tables'][0]  # TODO: iterate over tables
    cells = table_raw['cells']
    table = {}

    for i, cell in enumerate(cells):
        try:
            next_cell = i+1
            table.update({cell['content']: cells[next_cell]['content']})
        except IndexError:
            print('TODO: safe check index')

    return table


def analyse_custom_model(fr_analysis: dict) -> dict:
    custom_model_table = {}

    if len(fr_analysis['documents']) != 0:

        fields_raw = fr_analysis['documents'][0]  # TODO: iterate over tables
        fields = fields_raw['fields']

        for key in fields.keys():
            custom_model_table.update({key: fields[key]['content']})

    return custom_model_table
