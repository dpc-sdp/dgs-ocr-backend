
from dataclasses import dataclass
from flask import jsonify


@dataclass
class ApiResponse():

    def custom(self, code, type,  message):
        self.code = code
        self.type = type
        self.message = message
        return self.json()

    def sucesss(self, message):
        return self.custom(200, 'sucesss',  message)

    def unauthorized(self, message):
        return self.custom(401, 'unauthorized', message)

    def error(self, message):
        return self.custom(500, 'internal_error',  message)

    def badRequest(self, message):
        return self.custom(400, 'bad_request', message)

    def timeout(self, message):
        return self.custom(408, 'timeout', message)

    def json(self) -> dict:
        return 401, {
            'code': self.code,
            'type': self.type,
            'msg': self.message
        }
