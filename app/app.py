
import json
import os
import pandas as pd

from flask import Flask, request, jsonify

from db.entities import ApiRequest, AnalysedData, ExpectedResults
from db.repositories import ApiRequestRepository, AnalysedDataRepository, ExpectedResultsRepository

import config
import form_analyser.formanalyser as formanalyser
from form_analyser.form_recognizer_service import FormRecognizerService
from form_analyser.response_handler import ResponseHandler
from utils.base_utils import BaseUtils
from flask_cors import CORS


# Initialise the Services
recognizer_service = FormRecognizerService()
apiRequestRepository = ApiRequestRepository()
analysedDataRepo = AnalysedDataRepository()
expectedResultsRepo = ExpectedResultsRepository()


# Flask app
app = Flask(__name__)
CORS(app)
app.debug = True
app.config['DEBUG'] = True
app.config['FLASK_ENV'] = 'development'
app.use_reloader = True

# Get an ID for this run of the program
instance_id = BaseUtils.get_a_unique_id()
print(f'instance_id = {instance_id}')

# This is a smoke test


@app.route('/')
def homepage():
    request_id = BaseUtils.get_a_unique_id()
    return f'Hello world! :-) time = {BaseUtils.get_timestamp()}, instance_id = {instance_id}, request_id = {request_id}\nSee I fixed it :-)\n'

# This is the user interface


@app.route('/upload-form', methods=['GET'])
def upload_form():
    request_id = BaseUtils.get_a_unique_id()
    import jinja2
    from jinja2 import FileSystemLoader
    environment = jinja2.Environment(loader=FileSystemLoader(os.getcwd()))
    template = environment.get_template("upload-form-template.html")
    return template.render(
        instance_id=instance_id,
        request_id=request_id,
        model_id=config.get_azure_form_recognizer_model_id(),
        endpoint_url=config.get_azure_form_recognizer_endpoint()
    )

# This is the "new" backend which returns the JSON analysis directly to the client.


@app.route('/do-analyse', methods=['POST'])
def do_analyse():
    request_id = BaseUtils.get_a_unique_id()
    pdf_bytes = request.files['file'].read()
    # Expect client to submit `multipart/form-data` with the document uploaded in the "doc" field, e.g. `curl -F 'doc=...;filename=...'`. `data_to_save` will be of type `bytes`.
    form_inputs = request.form.get('stash_input_and_output')
    print(f'{request_id}: form_inputs = {form_inputs}, request.form = {request.form}')

    result = formanalyser.analyse_document(
        pdf_bytes,
        stash_input_and_output=form_inputs,
        request_id=request_id
    )  # Returns a dict

    result['formspoc_request_id'] = request_id  # For troubleshooting purposes!
    return json.dumps(result)


@app.route('/analyze-doc', methods=['POST'])
def analyze_doc():
    apiRequest = ApiRequest(request)
    apiRequestRepository.save_to_db(apiRequest)

    result: ResponseHandler = recognizer_service.analyze(apiRequest)

    if apiRequest.preserve_artefacts:
        result.stash_document()
        result.stash_result()

    response = result.parse()
    apiRequestRepository.save_to_db(response)

    return response.get_json()


@app.route('/list-models', methods=['GET'])
def list_models():

    admin = recognizer_service._setup_admin()
    models = admin.list_document_models()
    print(models)

    model_list = [m.model_id for m in models]
    return jsonify(model_list)


@app.route('/upload-test-data', methods=['POST'])
def upload_file():
    file = request.files['file']
    agent = ""
    user_agent = request.headers.get('User-Agent')
    if user_agent is not None:
        agent = user_agent.split("/")[0]

    if file:
        filename = file.filename
        excel_data = pd.read_excel(file)

        for index, row in excel_data.iterrows():
            expectedResults = ExpectedResults(
                agent=agent, file_name=filename, row=row)
            expectedResultsRepo.save_to_db(expectedResults)

        return 'File uploaded and data stored in the database successfully.'
    else:
        return 'No file uploaded.'


print('Form recognizer initiated!')
