from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from resources.login_resource import ns
from resources.ocr_resource import ns1
from extensions import jwt
from utils.logger_util import LoggerUtil


logger = LoggerUtil("ErrorHandler")


# Custom error handler for namespace ns
@ns.errorhandler(500)
def custom_error_handler_ns(error):
    return {'message': 'Custom error response for namespace ns - 500'}, 500


@ns.errorhandler(401)
def custom_error_handler_ns(error):
    return {'message': 'Custom error response for namespace ns - 401'}, 401


@ns.errorhandler(200)
def custom_error_handler_ns(error):
    return {'message': 'Custom error response for namespace ns - 200'}, 200


@ns.errorhandler(400)
def custom_error_handler_ns(error):
    return {'message': 'Custom error response for namespace ns - 400'}, 400

# Custom error handler for namespace ns1


@ns1.errorhandler(500)
def custom_error_handler_ns1(error):
    return {'message': 'Custom error response for namespace ns1 - 500'}, 500


@ns1.errorhandler(401)
def custom_error_handler_ns1(error):
    return {'message': 'Custom error response for namespace ns1 - 401'}, 401


@ns1.errorhandler(200)
def custom_error_handler_ns1(error):
    return {'message': 'Custom error response for namespace ns1 - 200'}, 200


@ns1.errorhandler(400)
def custom_error_handler_ns1(error):
    return {'message': 'Custom error response for namespace ns1 - 400'}, 400

# Custom error handler for JWT errors (All namespaces)


@jwt.expired_token_loader
def custom_expired_token_callback(expired_token):
    return {'message': 'Custom response for expired token'}, 401


@jwt.invalid_token_loader
def custom_invalid_token_callback(reason):
    return {'message': 'Custom response for invalid token'}, 401


@jwt.unauthorized_loader
def custom_unauthorized_callback(reason):
    return {'message': 'Custom response for unauthorized request'}, 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    logger.warning("Invalid Token! The token has been revoked")
    return ApiResponse().unauthorized("Invalid Token! The token has been revoked")


@jwt.unauthorized_loader
def unauthorized_callback(callback):
    logger.warning('Authentication required: Missing Authorization Header')
    return ApiResponse().unauthorized('Authentication required')
