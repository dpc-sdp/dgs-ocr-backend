from flask_restx import fields
from extensions import api

login_request_model = api.model('LoginRequest', {
    'username': fields.String(description='Username'),
    'password': fields.String(description='Password')
})

login_response_model = api.model('LoginResponse', {
    'access_token': fields.String(description='Access Token')
})

upload_request_model = api.model('UploadRequest', {
    'cover_type': fields.String(description='Cover type fo the uploading document [public, product or professional]'),
    'filename': fields.String(description='Name of the uploaded file'),
    'content_length': fields.String(description='Sized of the uploading file'),
    'file': fields.String(description='Base64 encoded file'),
})

authorizations_obj = {
    "jsonWebToken": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}
