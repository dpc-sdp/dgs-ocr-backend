import config
import datetime

from flask import Flask
from extensions import api, db, jwt
from utils.logger_util import LoggerUtil
from resources.login_resource import ns
from resources.ocr_resource import ns1
from flask_jwt_extended import JWTManager

app = Flask(__name__)

logger = LoggerUtil("API")

app.config["SQLALCHEMY_DATABASE_URI"] = config.get_db_uri()
app.config['JWT_SECRET_KEY'] = config.get_jwt_secret_key()
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=30)

api.init_app(app)
db.init_app(app)
jwt.init_app(app)

api.add_namespace(ns)
api.add_namespace(ns1)

logger.info('Form recognizer initiated!')
