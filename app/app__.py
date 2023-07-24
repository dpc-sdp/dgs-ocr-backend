
import json
import os
import datetime

from flask import Flask, request, jsonify
from flask_restx import Api, Resource, reqparse, fields
from werkzeug.datastructures import FileStorage

from db.entities import ApiRequest
from db.repositories import ApiRequestRepository, AnalysedDataRepository

from flask import Flask, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt

import config
from form_analyser.form_recognizer_service import FormRecognizerService
from form_analyser.response_handler import ResponseHandler
from utils.key_authentication import api_key_required
from utils.base_utils import BaseUtils
from flask_cors import CORS
from utils.logger_util import LoggerUtil
from utils.mask_utils import mask_username
from utils.api_response import ApiResponse


# Initialise the Services
recognizer_service = FormRecognizerService()
apiRequestRepository = ApiRequestRepository()
analysedDataRepo = AnalysedDataRepository()


# Flask app
app = Flask(__name__)
CORS(app)
app.debug = eval(config.get_debugMode())
app.config['DEBUG'] = eval(config.get_debugMode())
app.config['FLASK_ENV'] = config.get_environment()

logger = LoggerUtil("API")

# Replace with your own secret key
app.config['JWT_SECRET_KEY'] = config.get_jwt_secret_key()
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=30)
jwt = JWTManager(app)
jwt._set_error_handler_callbacks(app)

# Get an ID for this run of the program
instance_id = BaseUtils.get_a_unique_id()
print(f'instance_id = {instance_id}')


api = Api(app, version='1.0', title='DSG OCR API',
          description='API documentaion to access the DSG OCR', add_specs=False
          )

ns = api.namespace('api/user', description='User access controls')
ns1 = api.namespace('api/ocr', description='OCR apis')


@app.errorhandler(404)
def page_not_found(error):
    return ApiResponse().custom(404, 'not_found', 'Page not found')


@app.errorhandler(400)
def bad_request(error):
    return ApiResponse().badRequest(error.description)


@app.errorhandler(408)
def timeout_handler(error):
    return ApiResponse().timeout(error.description)


@jwt.expired_token_loader
def expired_token_callback(header, date):
    return ApiResponse().unauthorized('Token has expired!')


@app.errorhandler(Exception)
def exception_handler(error):
    print(error)
    return ApiResponse().error('An internal server error occurred!')


@app.errorhandler(500)
def internal_server_error(error):
    print(error)
    return ApiResponse().error('An internal server error occurred!')


@ns.route('/login', endpoint='login')
class LoginResource(Resource):

    login_model = api.model('UserLogin', {
        'username': fields.String(description='Username'),
        'password': fields.String(description='Password')
    })

    response_model = api.model('LoginResponse', {
        'access_token': fields.String(description='Access Token')
    })

    @api.expect(login_model, validate=True)
    @api.marshal_with(response_model)
    def post(self):
        logger.info("User login initiated!")
        # Get the username and password from the request
        username = request.json['username']
        password = request.json['password']
        maskedUsername = mask_username(username)
        logger.debug(f'Received login request for username: {maskedUsername}')

        if ((username == config.get_username() and password == config.get_password()) or
                (username == config.get_sn_username() and password == config.get_sn_password())):
            logger.info(f'User {maskedUsername} logged in successfully')
        else:
            logger.warning(
                f'Failed login attempt for username: {maskedUsername}')
            return ApiResponse().unauthorized('Invalid username or password!')

        # If authentication is successful, create and return an access token
        access_token = create_access_token(identity=username)
        logger.info(f'Token issed for user {maskedUsername}')
        return {'access_token': access_token}


# Logout API
BLOCKLIST = set()


@ns.route('/logout', endpoint='logout')
class LogoutResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("Authentication", type=str, location="headers",
                        help="Authentication token", required=True)

    @jwt_required()  # Requires a valid JWT token
    @api.doc(parser=parser, responses={403: 'Not Authorized'})
    def post(self):
        logger.info("User logout initiated!")
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        logger.info("User logged out successfully!")
        return ApiResponse().sucesss('Logged out successfully')


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    logger.warning("Invalid Token! The token has been revoked")
    return ApiResponse().unauthorized("Invalid Token! The token has been revoked")


@jwt.unauthorized_loader
def unauthorized_callback(callback):
    logger.warning('Authentication required: Missing Authorization Header')
    return ApiResponse().unauthorized('Authentication required')


@ns1.route('/analyze-doc', endpoint='analyze-doc')
class UploadResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("Authentication", type=str, location="headers",
                        help="Authentication token", required=True)
    parser.add_argument("cover_type", type=str,
                        location='form', help="Cover type fo the uploading document [public, product or professional]", required=True)
    parser.add_argument("doc", location='files', type=FileStorage,
                        help="Uploaded file", required=True)

    @jwt_required()  # Requires a valid JWT token
    @api.doc(parser=parser, responses={403: 'Not Authorized'})
    def post(self):
        apiRequest = ApiRequest(request, False)
        apiRequestRepository.save_to_db(apiRequest)

        result: ResponseHandler = recognizer_service.analyze(apiRequest)

        response = result.parse()
        # apiRequestRepository.save_to_db(response)

        return response.get_json()


@ns1.route('/analyze', endpoint='analyze')
class AnalyzeResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("Authentication", type=str, location="headers",
                        help="Authentication token", required=True)
    parser.add_argument("X-API-Key", type=str, location="headers",
                        help="API Key", required=True)
    parser.add_argument("cover_type", type=str,
                        location='form', help="Cover type fo the uploading document [public, product or professional]", required=True)
    parser.add_argument("filename", type=str, location='form',
                        help="Name of the uploaded file", required=True)
    parser.add_argument("content_length", location='form',
                        type=str, help="Sized of the uploading file", required=True)
    parser.add_argument("file", type=str, location='form',
                        help="Base64 encoded file", required=True)

    @jwt_required()
    @api_key_required
    @api.doc(parser=parser, responses={403: 'Not Authorized'})
    def post(self):
        apiRequest = ApiRequest(request, True)
        apiRequestRepository.save_to_db(apiRequest)

        result: ResponseHandler = recognizer_service.analyze(apiRequest)

        response = result.parse()
        # apiRequestRepository.save_to_db(response)

        return response.get_json()


user_model = api.model('User', {
    'name': fields.String(required=True, description='User name'),
    'age': fields.Integer(required=True, description='User age')
})


@api.route('/user')
class UserResource(Resource):
    @api.expect(user_model, validate=True)
    def post(self):
        data = request.json
        # Process the data as needed (e.g., save to a database)
        return {'message': 'User data received', 'data': data}, 201


logger.info('Form recognizer initiated!')
