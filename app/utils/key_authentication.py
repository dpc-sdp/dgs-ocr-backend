
import config

from functools import wraps
from flask import request
from flask_jwt_extended import get_jwt_identity
from utils.api_response import ApiResponse


def jwt_or_api_key_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # verify_jwt_in_request_optional()
        current_user = get_jwt_identity()
        if current_user:
            return fn(*args, **kwargs)
        else:
            api_key = request.headers.get('X-API-Key')
            if api_key == config.get_api_key():
                # API key is valid, proceed with the protected route
                return fn(*args, **kwargs)
            else:
                return ApiResponse().unauthorized('Authentication required!')
    return wrapper


def api_key_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key == config.get_api_key():
            # API key is valid, proceed with the protected route
            return fn(*args, **kwargs)
        else:
            return ApiResponse().unauthorized('Authentication required!')
    return wrapper
