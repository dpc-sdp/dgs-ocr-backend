import copy
from jsonpath2.path import Path
from form_analyser.field_builder import RawFieldValue


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


def analyse_custom_model_for_parsing(fr_analysis: dict) -> dict:
    custom_model_table = {}

    if len(fr_analysis['documents']) != 0:

        fields_raw = fr_analysis['documents'][0]  # TODO: iterate over tables
        fields = fields_raw['fields']

        for key in fields.keys():
            custom_model_table.update({
                key: RawFieldValue(
                    input=fields[key]['content'],
                    input_type=fields[key]['value_type'],
                    confidence=fields[key]['confidence'],
                )()
            })

    return custom_model_table
