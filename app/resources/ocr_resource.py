from flask import request
from flask_restx import Resource, Namespace, reqparse
from werkzeug.datastructures import FileStorage
from db.entities import ApiRequest
from db.repositories import ApiRequestRepository
from form_analyser.form_recognizer_service import FormRecognizerService
from form_analyser.response_handler import ResponseHandler
from flask_jwt_extended import jwt_required
from utils.key_authentication import api_key_required
from resources.api_models import authorizations_obj, upload_request_model

recognizer_service = FormRecognizerService()
apiRequestRepository = ApiRequestRepository()

ns1 = Namespace('api/ocr', description='OCR apis',
                authorizations=authorizations_obj)


@ns1.route('/analyze', endpoint='analyze')
class AnalyzeResource(Resource):

    method_decorators = [jwt_required()]

    @ns1.expect(upload_request_model)
    @ns1.doc(security='apikey')
    def post(self):
        apiRequest = ApiRequest(request, True)
        apiRequestRepository.save_to_db(apiRequest)

        result: ResponseHandler = recognizer_service.analyze(apiRequest)

        response = result.parse()
        # apiRequestRepository.save_to_db(response)

        return response.get_json()


@ns1.route('/analyze-doc')
class UploadResource(Resource):

    method_decorators = [jwt_required()]

    parser = reqparse.RequestParser()
    parser.add_argument("cover_type", type=str,
                        location='form', help="Cover type fo the uploading document [public, product or professional]", required=True)
    parser.add_argument("doc", location='files', type=FileStorage,
                        help="Uploaded file", required=True)

    @ns1.expect(parser)
    @ns1.doc(security='apikey')
    def post(self):
        apiRequest = ApiRequest(request, False)
        apiRequestRepository.save_to_db(apiRequest)

        result: ResponseHandler = recognizer_service.analyze(apiRequest)

        response = result.parse()
        # apiRequestRepository.save_to_db(response)

        return response.get_json()
