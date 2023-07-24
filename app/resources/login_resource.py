
import config

from flask_restx import Resource, Namespace
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

from utils.api_response import ApiResponse
from utils.mask_utils import mask_username
from utils.logger_util import LoggerUtil
from resources.api_models import login_request_model, login_response_model, authorizations_obj

# Logout API
BLOCKLIST = set()

ns = Namespace('api/user', description='User access controls',
               authorizations=authorizations_obj)

logger = LoggerUtil("LoginResource")
logoutLogger = LoggerUtil("LogoutResource")


@ns.route('/login')
class LoginResource(Resource):

    @ns.expect(login_request_model, validate=True)
    @ns.marshal_with(login_response_model)
    def post(self):
        logger.info("User login initiated!")
        # Get the username and password from the request
        username = ns.payload['username']
        password = ns.payload['password']
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


@ns.route('/logout')
class LogoutResource(Resource):

    method_decorators = [jwt_required()]

    @ns.doc('user_logout', security='apikey')
    def post(self):
        logoutLogger.info("User logout initiated!")
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        logoutLogger.info("User logged out successfully!")
        return ApiResponse().sucesss('Logged out successfully')
