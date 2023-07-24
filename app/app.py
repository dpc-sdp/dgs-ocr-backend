
import config
import datetime


from flask_cors import CORS
from flask import Flask, request, send_file
from flask_jwt_extended import jwt_required, create_access_token, get_jwt

from db.entities import ApiRequest
from db.repositories import ApiRequestRepository
from form_analyser.form_recognizer_service import FormRecognizerService
from form_analyser.response_handler import ResponseHandler
from utils.key_authentication import api_key_required
from utils.base_utils import BaseUtils
from utils.logger_util import LoggerUtil
from utils.mask_utils import mask_username
from utils.api_response import ApiResponse
from conf.swagger_ui_blueprint import swagger_ui_blueprint, SWAGGER_URL
from conf.extensions import db, jwt


# Initialise the Services
recognizer_service = FormRecognizerService()
apiRequestRepository = ApiRequestRepository()

# Flask app
app = Flask(__name__)
CORS(app)
app.debug = eval(config.get_debugMode())
app.config['DEBUG'] = eval(config.get_debugMode())
app.config['FLASK_ENV'] = config.get_environment()
app.config["SQLALCHEMY_DATABASE_URI"] = config.get_azure_form_recognizer_db_uri()
app.config['JWT_SECRET_KEY'] = config.get_jwt_secret_key()
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=30)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

db.init_app(app)
jwt.init_app(app)
jwt._set_error_handler_callbacks(app)

# Create an application context
with app.app_context():
    # Perform database operations within the application context
    db.create_all()

logger = LoggerUtil("API")

# Get an ID for this run of the program
instance_id = BaseUtils.get_a_unique_id()
logger.info(f'instance_id = {instance_id}')


@app.errorhandler(404)
def page_not_found(error):
    logger.error(error)
    return ApiResponse().custom(404, 'not_found', 'Page not found')


@app.errorhandler(400)
def bad_request(error):
    logger.error(error)
    return ApiResponse().badRequest(error.description)


@app.errorhandler(408)
def timeout_handler(error):
    logger.error(error)
    return ApiResponse().timeout(error.description)


@jwt.expired_token_loader
def expired_token_callback(header, date):
    return ApiResponse().unauthorized('Token has expired!')


@app.errorhandler(Exception)
def exception_handler(error):
    logger.error(error)
    return ApiResponse().error('An internal server error occurred!')


@app.errorhandler(500)
def internal_server_error(error):
    logger.error(error)
    return ApiResponse().error('An internal server error occurred!')


@app.route('/swagger.json')
def serve_swagger_json():
    return send_file('config/swagger.json')


@app.route('/api/v1/user/login', methods=['POST'])
def login():
    logger.info("User login initiated!")
    # Get the username and password from the request
    username = request.json.get('username')
    password = request.json.get('password')
    maskedUsername = mask_username(username)
    logger.debug(f'Received login request for username: {maskedUsername}')

    if ((username == config.get_username() and password == config.get_password()) or
            (username == config.get_sn_username() and password == config.get_sn_password())):
        logger.info('Login in successful')
    else:
        logger.warning(f'Failed login attempt for username: {maskedUsername}')
        return ApiResponse().unauthorized('Invalid username or password!')

    # If authentication is successful, create and return an access token
    access_token = create_access_token(identity=username)
    logger.info(f'User {maskedUsername} logged in successfully')
    return {'access_token': access_token}

# Logout API


BLOCKLIST = set()


@app.route('/api/v1/user/logout', methods=['POST'])
@jwt_required()  # Requires a valid JWT token
def logout():
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


@app.route('/api/v1/ocr/analyze-doc', methods=['POST'])
@jwt_required()
def analyze_doc():
    apiRequest = ApiRequest(request, False)
    apiRequestRepository.save_to_db(apiRequest)

    result: ResponseHandler = recognizer_service.analyze(apiRequest)

    response = result.parse()
    # apiRequestRepository.save_to_db(response)

    return response.get_json()


@app.route('/api/v1/ocr/analyze', methods=['POST'])
@jwt_required()
@api_key_required
def analyze():
    apiRequest = ApiRequest(request, True)
    apiRequestRepository.save_to_db(apiRequest)

    result: ResponseHandler = recognizer_service.analyze(apiRequest)

    response = result.parse()
    # apiRequestRepository.save_to_db(response)

    return response.get_json()


logger.info('Form recognizer initiated!')
